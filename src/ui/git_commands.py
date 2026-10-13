#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
git_commands.py - Commandes Git pour le CLI Gabriel.

Séparé du CLI (comme latex_commands.py) pour rester lisible.
Expose handle_git_command(cmd, console) -> bool.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Sous-commandes de lecture/écriture reconnues (pour l'aide et le dispatch)
READ_SUBS = {"status", "log", "diff", "show", "branch", "remote", "rev-parse"}
WRITE_SUBS = {"add", "commit", "pull", "fetch", "merge", "checkout", "switch",
              "tag", "stash", "reset", "restore"}
SPECIAL_SUBS = {"push", "sync"}

HELP_PANEL = (
    "  [bold]git <sous-commande> [args][/bold]\n\n"
    "  [cyan]Lecture[/cyan]  : status, log [n], diff [cible], show [ref],\n"
    "                branch, remote -v, rev-parse\n"
    "  [cyan]Écriture[/cyan] : add [chemins], commit -m \"msg\", pull, fetch,\n"
    "                merge <branche>, checkout <ref> [-b], tag <nom>,\n"
    "                stash, reset --soft, restore\n"
    "  [cyan]Push[/cyan]     : push   (branche protégée main/master bloquée)\n"
    "                push --force-main   (confirme le push sur main)\n"
    "  [cyan]Sync[/cyan]     : sync -m \"msg\"   (status+add+commit+pull+push)\n"
    "\n  [dim]Le token GitHub (GITHUB_TOKEN) est masqué dans toute sortie.[/dim]"
)


def _extract_message(args: list) -> str:
    """Message d'un `git commit -m "..."` / `-m=...` / `commit message libre`."""
    if not args:
        return ""
    if "-m" in args:
        i = args.index("-m")
        rest = args[i + 1:]
        if rest:
            return " ".join(rest).strip().strip('"').strip("'")
    if args and args[0].startswith("-m="):
        return args[0][3:].strip().strip('"').strip("'")
    if args and not args[0].startswith("-"):
        return " ".join(args).strip().strip('"').strip("'")
    return ""


def handle_git_command(cmd: str, console) -> bool:
    """Traite `git <sous-commande> [args]`. Retourne True si géré."""
    from ..core.git_controller import get_git_controller
    from rich.panel import Panel

    body = cmd.strip()
    if body.lower().startswith("git "):
        body = body[4:]
    elif body.lower() == "git":
        body = ""
    tokens = body.split()
    git = get_git_controller()  # respecte GABRIEL_GIT_REPO si défini

    if not git.is_available():
        console.print("\n  [red]git n'est pas installé dans cet environnement.[/red]\n")
        return True
    if not git.is_repo():
        console.print(
            "\n  [red]Le répertoire courant n'est pas un dépôt git.[/red]\n"
            "  [dim]Initialisez avec `git init` ou placez-vous dans le dépôt.[/dim]\n"
        )
        return True

    if not tokens or tokens[0] in {"help", "aide", "?"}:
        console.print(Panel(HELP_PANEL, title="[bold cyan]COMMANDES GIT[/bold cyan]",
                            border_style="cyan", padding=(1, 2)))
        return True

    sub = tokens[0]
    args = tokens[1:]

    def _show(res, title: str) -> None:
        color = "green" if res.ok else "red"
        mark = "[OK]" if res.ok else "[X]"
        out = res.combined()
        console.print(f"\n  [{color}]{mark} {title}[/{color}]")
        if out:
            console.print(Panel(out, border_style=color, padding=(0, 2)))

    try:
        # ---------- LECTURE ----------
        if sub == "status":
            _show(git.status(short=("--short" in args or "-s" in args)), "git status")
        elif sub == "log":
            n = next((int(a) for a in args if a.isdigit()), 10)
            _show(git.log(n=n), f"git log -n{n}")
        elif sub == "diff":
            _show(git.diff(" ".join(args)), "git diff")
        elif sub == "show":
            _show(git.show(args[0] if args else "HEAD"), "git show")
        elif sub == "branch":
            _show(git.branch_list(), "git branch -a")
        elif sub == "remote":
            _show(git.remote_list(), "git remote -v")
        elif sub == "rev-parse":
            console.print(f"\n  [cyan]{git.rev_parse(args[0] if args else 'HEAD')}[/cyan]\n")

        # ---------- ÉCRITURE ----------
        elif sub == "add":
            paths = " ".join(args) if args else "."
            _show(git.add(paths), f"git add {paths}")
        elif sub == "commit":
            msg = _extract_message(args)
            if not msg:
                console.print('\n  [yellow]Usage : git commit -m "votre message"[/yellow]\n')
                return True
            _show(git.commit(msg), f'git commit -m "{msg[:50]}"')
        elif sub == "pull":
            _show(git.pull(rebase="--rebase" in args), "git pull")
        elif sub == "fetch":
            _show(git.fetch(), "git fetch --prune")
        elif sub == "merge":
            if not args:
                console.print("\n  [yellow]Usage : git merge <branche>[/yellow]\n")
                return True
            _show(git.merge(args[0], no_ff="--no-ff" in args), f"git merge {args[0]}")
        elif sub in {"checkout", "switch"}:
            if not args:
                console.print(f"\n  [yellow]Usage : git {sub} <ref> [-b][/yellow]\n")
                return True
            create = "-b" in args or "-c" in args
            ref = next((a for a in args if not a.startswith("-")), "")
            _show(git.checkout(ref, create=create), f"git {sub} {ref}")
        elif sub == "tag":
            if not args:
                console.print("\n  [yellow]Usage : git tag <nom>[/yellow]\n")
                return True
            _show(git.tag_create(args[0]), f"git tag {args[0]}")
        elif sub == "stash":
            action = args[0] if args and args[0] in {"pop", "list", "clear", "apply"} else "push"
            _show(git.stash(action), f"git stash {action}")
        elif sub == "reset":
            mode = next((a for a in args if a.startswith("--")), "--soft")
            _show(git.reset(mode), f"git reset {mode} HEAD~1")
        elif sub == "restore":
            _show(git.restore(" ".join(args) if args else "."), "git restore")

        # ---------- PUSH / SYNC ----------
        elif sub == "push":
            allow_main = "--force-main" in args or "--allow-main" in args
            res = git.push(allow_main_push=allow_main)
            color = "green" if res.ok else "red"
            mark = "[OK]" if res.ok else "[X]"
            console.print(f"\n  [{color}]{mark} git push[/{color}]")
            out = res.combined()
            if out:
                console.print(Panel(out, border_style=color, padding=(0, 2)))
        elif sub == "sync":
            msg = _extract_message(args) or "chore: synchronisation Gabriel"
            allow_main = "--force-main" in args
            report = git.sync(commit_message=msg, allow_main_push=allow_main)
            color = "green" if report["ok"] else "red"
            lines = [f"  {'[OK]' if ok else '[X]'} {step}: {(out or '(vide)')[:120]}"
                     for step, ok, out in report["steps"]]
            console.print(f"\n  [{color}]git sync (status+commit+pull+push)[/{color}]")
            console.print(Panel("\n".join(lines), border_style=color, padding=(0, 2)))
        else:
            console.print(
                f"\n  [yellow]Sous-commande git non gérée : '{sub}'.[/yellow]\n"
                "  [dim]Tapez `git help` pour la liste des commandes supportées.[/dim]\n"
            )
    except Exception as exc:
        logger.exception("Erreur commande git")
        console.print(f"\n  [red]Erreur git : {exc}[/red]\n")
    return True

