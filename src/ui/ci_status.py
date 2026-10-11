"""Utilitaire CI : exécute la suite pytest locale et formate un résumé Rich.

Sert deux usages :
  1. Commande CLI `ci` : affiche le résultat détaillé des tests.
  2. Bannière d'ouverture : affiche un résumé compact (XXX/YYY OK).

Aucune dépendance réseau : tout est exécuté localement, en sous-processus.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CISummary:
    """Résumé de l'exécution pytest locale."""
    passed: int
    failed: int
    errors: int
    skipped: int
    total: int
    duration_s: float
    ok: bool
    raw_tail: str  # Dernières lignes brutes pour debug

    @property
    def badge(self) -> str:
        """Badge texte court pour la bannière (ex: '161/161 OK')."""
        if self.ok and self.failed == 0 and self.errors == 0:
            return f"{self.passed}/{self.total} OK"
        return f"{self.passed}/{self.total} ({self.failed} fail, {self.errors} err)"

    @property
    def style(self) -> str:
        """Couleur Rich associée au résultat."""
        if self.ok and self.failed == 0 and self.errors == 0:
            return "bold green"
        return "bold red"


_REPO_ROOT = Path(__file__).resolve().parents[2]


def _find_tests_dir() -> Path:
    """Cherche le dossier 'tests' a plusieurs emplacements possibles.

    Couvre les cas :
      1. Execution dev locale (depuis le repo)              -> <repo>/tests
      2. Execution dans Docker (CWD=/home/agent/app)        -> ./tests (si monte)
      3. Execution dans Docker (avec /app)                   -> /app/tests
      4. Variable d'environnement explicite GABRIEL_TESTS_DIR
      5. Chemins Docker montes via docker-compose.yml
    """
    # Priorite 1 : variable d'environnement explicite (set dans docker-compose.yml)
    env_dir = os.environ.get("GABRIEL_TESTS_DIR")
    if env_dir:
        p = Path(env_dir)
        if p.is_dir():
            return p

    # Priorite 2 : a cote du module (cas dev local)
    candidate = _REPO_ROOT / "tests"
    if candidate.is_dir():
        return candidate

    # Priorite 3 : depuis CWD (cas Docker avec WORKDIR==/home/agent/app)
    cwd_candidate = Path.cwd() / "tests"
    if cwd_candidate.is_dir():
        return cwd_candidate

    # Priorite 4 : chemin absolu Docker standard (/home/agent/app/tests monte par compose)
    docker_std = Path("/home/agent/app/tests")
    if docker_std.is_dir():
        return docker_std

    # Priorite 5 : emplacements alternatifs connus
    for alt in ("/app/tests", "/workspace/tests"):
        p = Path(alt)
        if p.is_dir():
            return p

    # Fallback : on retourne le chemin ideal pour avoir un message d'erreur clair
    return _REPO_ROOT / "tests"


_TESTS_DIR = _find_tests_dir()

# Regex pour parser la ligne de résumé pytest.
# Pytest produit des lignes comme :
#   "667 passed, 1 warning in 1.99s"
#   "1 failed, 687 passed, 4 skipped, 2 warnings in 21.27s"
#   "6 failed, 655 passed, 6 skipped, 2 warnings in 40.66s"
# L'ORDRE des nombres varie selon la presence d'echecs : il faut parser
# CHAQUE compteur independamment via une regex globale.
_DURATION_RE = re.compile(r"in\s+([\d.]+)s", re.IGNORECASE)
_PASSED_RE = re.compile(r"(\d+)\s+passed", re.IGNORECASE)
_FAILED_RE = re.compile(r"(\d+)\s+failed", re.IGNORECASE)
_ERRORS_RE = re.compile(r"(\d+)\s+error", re.IGNORECASE)
_SKIPPED_RE = re.compile(r"(\d+)\s+skipped", re.IGNORECASE)


def _parse_summary_line(line: str) -> tuple[int, int, int, int, float]:
    """Parse une ligne de resume pytest en (passed, failed, errors, skipped, duration).

    Ordre-agnostique : marche pour "X passed, Y failed", "Y failed, X passed", etc.
    Si une categorie est absente, retourne 0.
    """
    def _first_int(rgx: re.Pattern, text: str) -> int:
        m = rgx.search(text)
        return int(m.group(1)) if m else 0

    passed = _first_int(_PASSED_RE, line)
    failed = _first_int(_FAILED_RE, line)
    errors = _first_int(_ERRORS_RE, line)
    skipped = _first_int(_SKIPPED_RE, line)
    dur_match = _DURATION_RE.search(line)
    duration = float(dur_match.group(1)) if dur_match else 0.0
    return passed, failed, errors, skipped, duration


def run_pytest_local(timeout_s: int = 120) -> CISummary:
    """Exécute `python -m pytest tests/ -q --tb=no` localement et parse le résultat.

    Renvoie un `CISummary`. Ne lève jamais : encapsule les erreurs dans le résumé.
    """
    if not _TESTS_DIR.is_dir():
        msg = (
            f"Tests directory introuvable: {_TESTS_DIR}\n\n"
            "  Cause probable : Gabriel tourne dans Docker et le dossier 'tests/'\n"
            "  n'a pas ete monte/copie dans le conteneur. Solutions :\n\n"
            "  Solution 1 (RECOMMANDEE - appliquee dans docker-compose.yml v5.4) :\n"
            "      Verifiez que le volume est presente :\n"
            "        - ./tests:/home/agent/app/tests:ro\n"
            "      Et que GABRIEL_TESTS_DIR==/home/agent/app/tests est set.\n\n"
            "  Solution 2 : lancez les tests directement sur votre PC avec :\n"
            "      python -m pytest tests/ -v\n\n"
            "  Solution 3 : definissez manuellement GABRIEL_TESTS_DIR\n"
            "      (variable d'environnement dans docker-compose.yml)"
        )
        return CISummary(0, 0, 1, 0, 0, 0.0, False, msg)

    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", str(_TESTS_DIR), "-q", "--tb=no", "--no-header"],
            cwd=str(_REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return CISummary(0, 0, 1, 0, 0, float(timeout_s), False,
                         f"Timeout (>{timeout_s}s) en exécutant pytest")
    except FileNotFoundError as exc:
        return CISummary(0, 0, 1, 0, 0, 0.0, False, f"Pytest introuvable: {exc}")

    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    tail = "\n".join(output.strip().splitlines()[-8:])

    passed = failed = errors = skipped = 0
    duration = 0.0

    # Cherche la dernière ligne contenant "passed" / "failed" / "in Xs"
    summary_line = ""
    for line in reversed(output.splitlines()):
        if " in " in line and ("passed" in line or "failed" in line or "error" in line):
            summary_line = line
            break

    if summary_line:
        passed, failed, errors, skipped, duration = _parse_summary_line(summary_line)

    total = passed + failed + errors + skipped
    # OK seulement si : exit code 0 + 0 failed + 0 errors + au moins 1 test passe
    ok = (proc.returncode == 0) and (failed == 0) and (errors == 0) and (passed > 0)

    return CISummary(
        passed=passed,
        failed=failed,
        errors=errors,
        skipped=skipped,
        total=total,
        duration_s=duration,
        ok=ok,
        raw_tail=tail,
    )
