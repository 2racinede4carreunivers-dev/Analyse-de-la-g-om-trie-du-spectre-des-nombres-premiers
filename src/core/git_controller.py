#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitController - Accès Git complet pour l'agent Gabriel.

Enveloppe sécurisée autour du binaire `git` (déjà présent dans l'image
Docker, cf. Dockerfile.cli). Permet à l'agent d'exécuter l'ensemble des
opérations Git courantes : status, add, commit, push, pull, fetch, merge,
branch, checkout, log, diff, clone, remote, config, tag, stash, reset.

Sécurité :
  - Liste blanche de sous-commandes autorisées.
  - Le token GitHub (GITHUB_TOKEN) n'apparaît JAMAIS en clair : il est
    injecté dans l'URL distante au moment du push/pull/fetch, puis masqué
    dans toute sortie affichée.
  - `push` sur la branche protégée (main/master) exige un flag explicite
    `allow_main_push=True`.
  - Timeout sur chaque appel git (évite qu'un git interactif - ex. demande
    d'identifiants - ne bloque l'agent).

Tout est synchrone (subprocess) pour rester simple et fiable dans le CLI.
"""
from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Sous-commandes git autorisées (lecture + écriture contrôlée)
ALLOWED_SUBCOMMANDS = {
    "status", "add", "commit", "push", "pull", "fetch", "merge",
    "branch", "checkout", "switch", "log", "diff", "show", "clone",
    "remote", "config", "tag", "stash", "reset", "init", "rev-parse",
    "ls-files", "restore", "rebase", "cherry-pick", "describe",
    "shortlog", "blame", "reflog", "clean", "mv", "rm",
}

# Branches considérées comme protégées (push nécessite un flag explicite)
PROTECTED_BRANCHES = {"main", "master", "trunk"}

# Options/sous-commandes INTERDITES (sécurité)
FORBIDDEN_PATTERNS = [
    r"\b--exec\b",
    r"\b--upload-pack\b",
    r"\b--receive-pack\b",
    r"\bfilter-branch\b",
    r"\bupdate-ref\b",
]

_TOKEN_RE = re.compile(r"(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")


def _mask(text: str) -> str:
    """Masque tout token GitHub présent dans une chaîne (logs/sortie)."""
    if not text:
        return text
    return _TOKEN_RE.sub("***TOKEN_MASQUE***", text)


class GitError(Exception):
    """Erreur d'utilisation du GitController."""


class GitResult:
    """Résultat normalisé d'une commande git."""

    def __init__(self, ok: bool, command: str, stdout: str = "",
                 stderr: str = "", returncode: int = 0):
        self.ok = ok
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def __bool__(self) -> bool:
        return self.ok

    def __repr__(self) -> str:  # pragma: no cover - debug
        return f"GitResult(ok={self.ok}, rc={self.returncode}, cmd={self.command!r})"

    def combined(self) -> str:
        """Sortie combinée (stdout + stderr), token masqué."""
        out = (self.stdout or "").strip()
        err = (self.stderr or "").strip()
        merged = out
        if err:
            merged = (out + "\n" + err) if out else err
        return _mask(merged)


class GitController:
    """
    Contrôleur Git pour l'agent. Opère sur un dépôt local (repo_path).

    Usage:
        git = GitController(repo_path="/home/agent/app")
        git.status()
        git.add(".")
        git.commit("message")
        git.push()
    """

    def __init__(self, repo_path: str | Path = ".", timeout: int = 60):
        self.repo_path = Path(repo_path).resolve()
        self.timeout = timeout
        self.token = os.environ.get("GITHUB_TOKEN", "").strip()
        self.username = os.environ.get("GITHUB_USERNAME", "").strip()

    # ------------------------------------------------------------------
    # Bas niveau
    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        """git installé ?"""
        return shutil.which("git") is not None

    def is_repo(self) -> bool:
        """Le chemin est-il un dépôt git ?"""
        res = self._run(["rev-parse", "--is-inside-work-tree"], check=False)
        return res.ok and res.stdout.strip() == "true"

    def _build_env(self) -> dict:
        """Environnement git non interactif + identité par défaut si absente."""
        env = os.environ.copy()
        # Empêche git d'ouvrir un éditeur/pager interactif qui bloquerait l'agent
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["GIT_PAGER"] = "cat"
        env["GIT_EDITOR"] = "true"          # commit sans ouvrir d'éditeur
        env["GIT_MERGE_AUTOEDIT"] = "no"
        # Identité de repli (écrasée par git config local si déjà définie)
        env.setdefault("GIT_AUTHOR_NAME", self.username or "Gabriel Agent")
        env.setdefault("GIT_AUTHOR_EMAIL",
                       f"{self.username or 'gabriel'}@users.noreply.github.com")
        env.setdefault("GIT_COMMITTER_NAME", self.username or "Gabriel Agent")
        env.setdefault("GIT_COMMITTER_EMAIL",
                       f"{self.username or 'gabriel'}@users.noreply.github.com")
        return env

    def _check_allowed(self, args: list[str]) -> None:
        if not args:
            raise GitError("Commande git vide.")
        sub = args[0]
        if sub not in ALLOWED_SUBCOMMANDS:
            raise GitError(
                f"Sous-commande git non autorisée : '{sub}'. "
                f"Autorisees : {sorted(ALLOWED_SUBCOMMANDS)}"
            )
        joined = " ".join(args)
        for pat in FORBIDDEN_PATTERNS:
            if re.search(pat, joined):
                raise GitError(f"Option git interdite (motif '{pat}') dans : {joined}")

    def _run(self, args: list[str], check: bool = True,
             input_text: Optional[str] = None) -> GitResult:
        """
        Exécute `git <args>` dans self.repo_path.
        Retourne toujours un GitResult (jamais d'exception sur échec git).
        """
        if not self.is_available():
            return GitResult(False, "git " + " ".join(args),
                             stderr="git non installé dans cet environnement.")
        try:
            self._check_allowed(args)
        except GitError as exc:
            return GitResult(False, "git " + " ".join(args), stderr=str(exc))
        cmd = ["git", "-C", str(self.repo_path)] + args
        cmd_str = "git " + " ".join(args)
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(self.repo_path),
                env=self._build_env(),
                input=input_text,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
            ok = proc.returncode == 0
            result = GitResult(ok, cmd_str, proc.stdout, proc.stderr, proc.returncode)
            if not ok and check:
                logger.debug("git a échoué (rc=%s): %s\n%s",
                             proc.returncode, cmd_str, _mask(proc.stderr))
            return result
        except subprocess.TimeoutExpired:
            return GitResult(False, cmd_str,
                             stderr=f"Timeout git ({self.timeout}s) sur : {cmd_str}")
        except FileNotFoundError:
            return GitResult(False, cmd_str, stderr="Binaire git introuvable.")
        except Exception as exc:  # pragma: no cover
            return GitResult(False, cmd_str, stderr=f"Erreur git : {exc}")

    # ------------------------------------------------------------------
    # URL distante avec injection du token (masqué partout)
    # ------------------------------------------------------------------
    def _authed_remote_url(self, remote: str = "origin") -> Optional[str]:
        """
        Retourne l'URL du remote avec le token injecté (https).
        Ex: https://<token>@github.com/user/repo.git
        Retourne None si pas de remote configuré.
        """
        base = self._run(["remote", "get-url", remote], check=False)
        url = base.stdout.strip()
        if not url:
            return None
        if not self.token:
            return url  # pas de token : on tente sans (SSH/credential helper)
        # Normalise en https
        if url.startswith("git@github.com:"):
            url = "https://github.com/" + url.split("git@github.com:", 1)[1]
        # Injecte le token dans l'autorité de l'URL https
        m = re.match(r"https://([^/@]+@)?(.+)", url)
        if m:
            return f"https://{self.token}@{m.group(2)}"
        return url

    # ------------------------------------------------------------------
    # Lecture (jamais destructrices)
    # ------------------------------------------------------------------
    def status(self, short: bool = False) -> GitResult:
        return self._run(["status", "--short"] if short else ["status"])

    def current_branch(self) -> str:
        res = self._run(["rev-parse", "--abbrev-ref", "HEAD"], check=False)
        return res.stdout.strip() if res.ok else ""

    def log(self, n: int = 10, oneline: bool = True) -> GitResult:
        args = ["log", f"-n{n}"]
        if oneline:
            args.append("--oneline")
            args.append("--decorate")
        return self._run(args)

    def diff(self, target: str = "") -> GitResult:
        args = ["diff"]
        if target:
            args.append(target)
        return self._run(args)

    def show(self, ref: str = "HEAD") -> GitResult:
        return self._run(["show", ref])

    def branch_list(self) -> GitResult:
        return self._run(["branch", "-a"])

    def remote_list(self) -> GitResult:
        return self._run(["remote", "-v"])

    def rev_parse(self, ref: str = "HEAD") -> str:
        res = self._run(["rev-parse", ref], check=False)
        return res.stdout.strip() if res.ok else ""

    def list_files(self) -> list[str]:
        res = self._run(["ls-files"], check=False)
        return res.stdout.splitlines() if res.ok else []

    # ------------------------------------------------------------------
    # Écriture contrôlée
    # ------------------------------------------------------------------
    def add(self, paths: str = ".") -> GitResult:
        targets = paths.split() if paths else ["."]
        return self._run(["add"] + targets)

    def commit(self, message: str, add_all: bool = False) -> GitResult:
        if not message or not message.strip():
            raise GitError("Message de commit vide.")
        if add_all:
            self.add(".")
        return self._run(["commit", "-m", message])

    def push(self, remote: str = "origin", branch: str = "",
             set_upstream: bool = True, allow_main_push: bool = False,
             force: bool = False) -> GitResult:
        if not branch:
            branch = self.current_branch() or "HEAD"
        if branch in PROTECTED_BRANCHES and not allow_main_push:
            return GitResult(
                False, f"git push {remote} {branch}",
                stderr=(f"Push sur branche protégée '{branch}' bloqué. "
                        f"Utilisez 'git push --force-main' pour confirmer."),
            )
        url = self._authed_remote_url(remote)
        if url is None:
            return GitResult(False, f"git push {remote} {branch}",
                             stderr=f"Aucun remote '{remote}' configuré.")
        args = ["push"]
        if force:
            args.append("--force-with-lease")
        if set_upstream:
            args += ["-u", url, branch]
        else:
            args += [url, branch]
        return self._run(args)

    def pull(self, remote: str = "origin", branch: str = "",
             rebase: bool = False) -> GitResult:
        if not branch:
            branch = self.current_branch() or "HEAD"
        url = self._authed_remote_url(remote)
        if url is None:
            return GitResult(False, f"git pull {remote} {branch}",
                             stderr=f"Aucun remote '{remote}' configuré.")
        args = ["pull", url, branch]
        if rebase:
            args.insert(1, "--rebase")
        return self._run(args)

    def fetch(self, remote: str = "origin", prune: bool = True) -> GitResult:
        url = self._authed_remote_url(remote)
        if url is None:
            return GitResult(False, f"git fetch {remote}",
                             stderr=f"Aucun remote '{remote}' configuré.")
        args = ["fetch", url]
        if prune:
            args.append("--prune")
        return self._run(args)

    def merge(self, branch: str, no_ff: bool = False) -> GitResult:
        args = ["merge"]
        if no_ff:
            args.append("--no-ff")
        args.append(branch)
        return self._run(args)

    def rebase(self, onto: str) -> GitResult:
        return self._run(["rebase", onto])

    def cherry_pick(self, ref: str) -> GitResult:
        return self._run(["cherry-pick", ref])

    def branch_create(self, name: str, checkout: bool = True) -> GitResult:
        if checkout:
            return self._run(["checkout", "-b", name])
        return self._run(["branch", name])

    def branch_delete(self, name: str, force: bool = False) -> GitResult:
        return self._run(["branch", "-D" if force else "-d", name])

    def checkout(self, ref: str, create: bool = False) -> GitResult:
        if create:
            return self._run(["checkout", "-b", ref])
        return self._run(["checkout", ref])

    def switch(self, ref: str, create: bool = False) -> GitResult:
        if create:
            return self._run(["switch", "-c", ref])
        return self._run(["switch", ref])

    def restore(self, paths: str = ".") -> GitResult:
        return self._run(["restore"] + paths.split())

    def reset(self, mode: str = "--soft", ref: str = "HEAD~1") -> GitResult:
        if mode not in ("--soft", "--mixed", "--hard"):
            raise GitError("reset: mode doit être --soft, --mixed ou --hard.")
        return self._run(["reset", mode, ref])

    def stash(self, action: str = "push", message: str = "") -> GitResult:
        args = ["stash", action]
        if action == "push" and message:
            args += ["-m", message]
        return self._run(args)

    def tag_create(self, name: str, message: str = "") -> GitResult:
        args = ["tag", "-a", name]
        if message:
            args += ["-m", message]
        return self._run(args)

    def clone(self, url: str, dest: str = "") -> GitResult:
        authed = url
        if self.token and "github.com" in url and "@" not in url.split("://", 1)[-1].split("/")[0]:
            authed = re.sub(r"https://", f"https://{self.token}@", url, count=1)
        args = ["clone", authed]
        if dest:
            args.append(dest)
        return self._run(args)

    def remote_add(self, name: str, url: str) -> GitResult:
        return self._run(["remote", "add", name, url])

    def remote_set_url(self, name: str, url: str) -> GitResult:
        return self._run(["remote", "set-url", name, url])

    def config_set(self, key: str, value: str, local: bool = True) -> GitResult:
        args = ["config"]
        if local:
            args.append("--local")
        args += [key, value]
        return self._run(args)

    def init(self) -> GitResult:
        return self._run(["init"])

    def clean_untracked(self, dry_run: bool = True) -> GitResult:
        args = ["clean", "-fd"]
        if dry_run:
            args.append("-n")
        return self._run(args)

    # ------------------------------------------------------------------
    # Raccourcis haut niveau
    # ------------------------------------------------------------------
    def quick_commit(self, message: str, paths: str = ".") -> GitResult:
        """add + commit en une étape."""
        add_res = self.add(paths)
        if not add_res.ok:
            return add_res
        return self.commit(message)

    def sync(self, commit_message: str = "", remote: str = "origin",
             allow_main_push: bool = False) -> dict:
        """
        Workflow complet : status -> add -> commit (si message) -> pull -> push.
        Retourne un dict détaillé (jamais de token en clair).
        """
        report: dict = {"steps": [], "ok": True}
        st = self.status(short=True)
        report["steps"].append(("status", st.ok, st.combined()))

        dirty = bool(st.stdout.strip())
        if commit_message and dirty:
            c = self.quick_commit(commit_message)
            report["steps"].append(("commit", c.ok, c.combined()))
            if not c.ok:
                report["ok"] = False
        elif commit_message and not dirty:
            report["steps"].append(("commit", True, "Rien à commiter (propre)."))

        pl = self.pull(remote=remote)
        report["steps"].append(("pull", pl.ok, pl.combined()))
        if not pl.ok:
            report["ok"] = False

        ps = self.push(remote=remote, allow_main_push=allow_main_push)
        report["steps"].append(("push", ps.ok, ps.combined()))
        if not ps.ok:
            report["ok"] = False
        return report


def get_git_controller(repo_path: str | Path | None = None) -> GitController:
    """
    Fabrique : retourne un GitController pointant sur repo_path.
    Si repo_path est None, utilise GABRIEL_GIT_REPO (défini dans docker-compose)
    ou le répertoire courant.
    """
    if repo_path is None:
        repo_path = os.environ.get("GABRIEL_GIT_REPO", ".")
    return GitController(repo_path=repo_path)
