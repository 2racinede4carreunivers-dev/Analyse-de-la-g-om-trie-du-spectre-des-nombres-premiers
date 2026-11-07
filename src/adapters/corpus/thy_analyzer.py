"""Analyseur structural d'un fichier .thy arbitraire pour la commande CLI
`analyse-thy <chemin>` de Gabriel.

v3.39 (Philippe 2026-02) : Permet a Philippe de demander a Gabriel d'analyser
un fichier .thy quelconque monte dans le conteneur, en particulier ceux du
sous-dossier `theories/projects/` qui ne sont PAS charges par le RAG.

Sortie : dictionnaire structure avec sections, definitions, lemmes, axiomes,
+ diagnostic Isabelle statique (via scripts/isabelle_static_check.py).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Any


_RE_THEORY = re.compile(r'^\s*theory\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)
_RE_IMPORTS = re.compile(r'^\s*imports\s+([^\n]+)', re.MULTILINE)
_RE_SECTION = re.compile(r'^\s*section\s+"([^"]+)"', re.MULTILINE)
_RE_SUBSECTION = re.compile(r'^\s*subsection\s+"([^"]+)"', re.MULTILINE)
_RE_DEFINITION = re.compile(r'^\s*definition\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)
_RE_LEMMA = re.compile(r'^\s*lemma\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)
_RE_THEOREM = re.compile(r'^\s*theorem\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)
_RE_AXIOMATIZATION = re.compile(r'^\s*axiomatization', re.MULTILINE)
_RE_LOCALE = re.compile(r'^\s*locale\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)
_RE_TYPEDECL = re.compile(r'^\s*typedecl\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)
_RE_FUN = re.compile(r'^\s*fun\s+([A-Za-z_][A-Za-z_0-9]*)', re.MULTILINE)


def analyse_thy_file(path: str | Path) -> dict[str, Any]:
    """Analyse structurelle d'un fichier .thy arbitraire.

    Retourne un dict :
      {
        "path", "size_bytes", "lines",
        "theory_name", "imports",
        "sections": [str, ...],
        "subsections": [str, ...],
        "definitions": [str, ...],
        "lemmas": [str, ...],
        "theorems": [str, ...],
        "locales": [str, ...],
        "typedecls": [str, ...],
        "fun_declarations": [str, ...],
        "n_axiomatizations": int,
        "static_check_output": str,   # sortie de isabelle_static_check.py
        "static_check_ok": bool,
        "warnings": [str, ...],
      }

    Raises:
        FileNotFoundError: si `path` n'existe pas.
        ValueError: si le fichier n'a pas d'entete `theory ... begin`.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Fichier .thy introuvable : {p}")
    if not p.is_file():
        raise ValueError(f"N'est pas un fichier regulier : {p}")

    text = p.read_text(encoding="utf-8", errors="replace")

    m_theory = _RE_THEORY.search(text)
    if not m_theory:
        raise ValueError(f"Aucune declaration `theory ...` trouvee dans {p}")

    m_imports = _RE_IMPORTS.search(text)

    result: dict[str, Any] = {
        "path": str(p.absolute()),
        "size_bytes": p.stat().st_size,
        "lines": text.count("\n") + 1,
        "theory_name": m_theory.group(1),
        "imports": m_imports.group(1).strip() if m_imports else "(none)",
        "sections": _RE_SECTION.findall(text),
        "subsections": _RE_SUBSECTION.findall(text),
        "definitions": _RE_DEFINITION.findall(text),
        "lemmas": _RE_LEMMA.findall(text),
        "theorems": _RE_THEOREM.findall(text),
        "locales": _RE_LOCALE.findall(text),
        "typedecls": _RE_TYPEDECL.findall(text),
        "fun_declarations": _RE_FUN.findall(text),
        "n_axiomatizations": len(_RE_AXIOMATIZATION.findall(text)),
        "warnings": [],
    }

    # Diagnostic Isabelle statique
    script = Path(__file__).resolve().parent.parent.parent / "scripts" / "isabelle_static_check.py"
    if script.exists():
        try:
            proc = subprocess.run(
                [sys.executable, str(script), str(p)],
                capture_output=True, text=True, timeout=30,
            )
            result["static_check_output"] = proc.stdout
            result["static_check_ok"] = proc.returncode == 0
            if proc.returncode != 0:
                result["warnings"].append(
                    f"static-check a signale des problemes (exit {proc.returncode})"
                )
        except subprocess.TimeoutExpired:
            result["static_check_output"] = "TIMEOUT (30s)"
            result["static_check_ok"] = False
            result["warnings"].append("static-check timeout")
        except Exception as exc:
            result["static_check_output"] = f"Erreur : {exc}"
            result["static_check_ok"] = False
    else:
        result["static_check_output"] = "(script isabelle_static_check.py absent)"
        result["static_check_ok"] = None

    # Vérifie theory / end
    if not text.rstrip().endswith("end"):
        result["warnings"].append("Le fichier ne se termine pas par `end` (structure Isabelle incomplete)")

    # Nom de theory doit correspondre au nom du fichier (convention Isabelle)
    expected_name = p.stem
    if result["theory_name"] != expected_name:
        result["warnings"].append(
            f"Nom de theory `{result['theory_name']}` != nom du fichier `{expected_name}` "
            f"-> Isabelle refusera de charger ce fichier tant que ce n'est pas aligne"
        )

    return result


def format_analysis_report(analysis: dict[str, Any]) -> str:
    """Formatte l'analyse en un rapport lisible pour le terminal (Rich-friendly).

    Utilise du markup Rich (pas de couleurs brutes) pour etre affiche via
    `rich.console.Console.print()` dans le CLI de Gabriel.
    """
    lines: list[str] = []
    lines.append(f"[bold cyan]Analyse structurelle du fichier .thy[/bold cyan]")
    lines.append(f"  [dim]Chemin  :[/dim] {analysis['path']}")
    lines.append(f"  [dim]Taille  :[/dim] {analysis['size_bytes']:,} octets  ({analysis['lines']:,} lignes)")
    lines.append(f"  [dim]Theory  :[/dim] [bold]{analysis['theory_name']}[/bold]")
    lines.append(f"  [dim]Imports :[/dim] {analysis['imports']}")
    lines.append("")

    lines.append(f"[bold]Structure decouverte :[/bold]")
    lines.append(f"  - [green]{len(analysis['sections'])}[/green] sections")
    lines.append(f"  - [green]{len(analysis['subsections'])}[/green] subsections")
    lines.append(f"  - [green]{len(analysis['definitions'])}[/green] definitions")
    lines.append(f"  - [green]{len(analysis['lemmas'])}[/green] lemmas")
    lines.append(f"  - [green]{len(analysis['theorems'])}[/green] theorems")
    lines.append(f"  - [green]{len(analysis['locales'])}[/green] locales")
    lines.append(f"  - [green]{len(analysis['typedecls'])}[/green] typedecls")
    lines.append(f"  - [green]{len(analysis['fun_declarations'])}[/green] fun-declarations")
    lines.append(f"  - [green]{analysis['n_axiomatizations']}[/green] blocs axiomatization")
    lines.append("")

    if analysis["sections"]:
        lines.append("[bold]Sections (max 15 premieres) :[/bold]")
        for i, sec in enumerate(analysis["sections"][:15], 1):
            lines.append(f"  {i:>3}. {sec}")
        if len(analysis["sections"]) > 15:
            lines.append(f"  ... et {len(analysis['sections']) - 15} de plus")
        lines.append("")

    if analysis["locales"]:
        lines.append(f"[bold]Locales declarees :[/bold]")
        lines.append(f"  {', '.join(analysis['locales'])}")
        lines.append("")

    if analysis["theorems"]:
        lines.append(f"[bold]Theoremes (max 10 premiers) :[/bold]")
        for th in analysis["theorems"][:10]:
            lines.append(f"  * {th}")
        lines.append("")

    if analysis["warnings"]:
        lines.append("[bold yellow]Avertissements :[/bold yellow]")
        for w in analysis["warnings"]:
            lines.append(f"  ! {w}")
        lines.append("")

    if analysis.get("static_check_ok") is True:
        lines.append("[bold green]Static-check Isabelle : OK[/bold green]")
    elif analysis.get("static_check_ok") is False:
        lines.append("[bold red]Static-check Isabelle : ECHEC[/bold red]")
        lines.append("[dim]Sortie complete :[/dim]")
        for l in analysis["static_check_output"].splitlines()[:30]:
            lines.append(f"  {l}")

    return "\n".join(lines)


__all__ = ["analyse_thy_file", "format_analysis_report"]
