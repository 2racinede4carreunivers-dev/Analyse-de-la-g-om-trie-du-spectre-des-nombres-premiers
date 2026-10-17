# -*- coding: utf-8 -*-
"""
moteur/emission.py — emission des artefacts (shell + rapport Markdown).

L'argv typé est cite de maniere sure pour chaque shell cible :
- PowerShell : guillemets simples avec échappement par doublage ;
- POSIX sh/bash : guillemets simples avec échappement ``'`` -> ``'\\''``.

Le rapport Markdown rend compte de la dérivation complète : intention,
scores (fractions exactes), invariants appliqués, trace SHA-256 et argv final.
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

from ..modele.entites import ResultatPipeline


def _quote_powershell(arg: str) -> str:
    return "'" + arg.replace("'", "''") + "'"


def _quote_sh(arg: str) -> str:
    return "'" + arg.replace("'", "'\\''") + "'"


def ligne_powershell(argv: Tuple[str, ...]) -> str:
    return " ".join(_quote_powershell(a) for a in argv)


def ligne_sh(argv: Tuple[str, ...]) -> str:
    return " ".join(_quote_sh(a) for a in argv)


def rapport_markdown(resultat: ResultatPipeline) -> str:
    """Rend le rapport Markdown de la derivation."""
    lignes = []
    lignes.append("# Rapport de derivation pythonLLM (computationnaliste)")
    lignes.append("")
    lignes.append(f"- **Requete** : {resultat.requete}")
    lignes.append(f"- **Intention** : {resultat.intention or '(aucune)'}")
    if resultat.est_refus:
        lignes.append(f"- **Issue** : REFUS FORMEL — {resultat.refus.motif}")
        lignes.append(f"- **Etape du refus** : {resultat.refus.etape}")
    else:
        lignes.append("- **Issue** : commande valide generee")
    lignes.append("")

    # Scores exacts.
    lignes.append("## Scores par champ (arithnetique exacte)")
    lignes.append("")
    lignes.append("| Champ | Score |")
    lignes.append("|---|---|")
    for code, score in resultat.reconnaissance.scores:
        lignes.append(f"| {code} | {score} |")
    lignes.append("")

    # Termes reconnus.
    lignes.append("## Termes reconnus (appartenance ensembliste)")
    lignes.append("")
    if resultat.reconnaissance.termes_reconnus:
        lignes.append(", ".join(f"`{t}`" for t in resultat.reconnaissance.termes_reconnus))
    else:
        lignes.append("_aucun terme reconnu_")
    lignes.append("")

    # Commande.
    if not resultat.est_refus and resultat.argv:
        lignes.append("## Commande generee")
        lignes.append("")
        lignes.append("```bash")
        lignes.append(ligne_sh(resultat.argv))
        lignes.append("```")
        lignes.append("")

    # Trace.
    lignes.append("## Trace de derivation (SHA-256 chaine)")
    lignes.append("")
    lignes.append("| # | Etape | Empreinte |")
    lignes.append("|---|---|---|")
    for e in resultat.trace:
        lignes.append(f"| {e.ordre} | {e.nom} | `{e.empreinte[:16]}…` |")
    lignes.append("")
    return "\n".join(lignes)


def emettre(resultat: ResultatPipeline, dossier: Path) -> Tuple[Path, Path, Path]:
    """Ecrit .ps1, .sh et .md dans ``dossier`` et retourne les trois chemins."""
    dossier.mkdir(parents=True, exist_ok=True)
    p_ps1 = dossier / "commande_cline.ps1"
    p_sh = dossier / "commande_cline.sh"
    p_md = dossier / "rapport_derivation.md"

    argv = resultat.argv
    if not resultat.est_refus and argv:
        p_ps1.write_text(
            "# Emission pythonLLM — commande Cline CLI (PowerShell)\n"
            + ligne_powershell(argv) + "\n",
            encoding="utf-8",
        )
        p_sh.write_text(
            "#!/usr/bin/env bash\n"
            "# Emission pythonLLM — commande Cline CLI (sh/bash)\n"
            "set -euo pipefail\n"
            + ligne_sh(argv) + "\n",
            encoding="utf-8",
        )
    else:
        motif = resultat.refus.motif if resultat.refus else "inconnu"
        p_ps1.write_text(
            "# REFUS FORMEL — aucune commande emise\n# " + motif + "\n",
            encoding="utf-8",
        )
        p_sh.write_text(
            "#!/usr/bin/env bash\n"
            "# REFUS FORMEL — aucune commande emise\n"
            "echo \"refus: " + motif + "\" >&2\n"
            "exit 2\n",
            encoding="utf-8",
        )

    p_md.write_text(rapport_markdown(resultat), encoding="utf-8")
    return p_ps1, p_sh, p_md
