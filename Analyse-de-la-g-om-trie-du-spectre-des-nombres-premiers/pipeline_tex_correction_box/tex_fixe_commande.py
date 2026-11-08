"""
tex_fixe_commande.py — Correction logique des erreurs LaTeX (approche stack-based).

Ce module lit les drapeaux d'erreur produits par ``investigation_gabriel_tex.py``
et applique des corrections automatiques sur le fichier source .tex :

  1. Fermeture des environnements non fermés : insertion de \\end{env} à la
     ligne appropriée (juste avant \\end{document} ou avant le prochain
     \\begin d'un environnement de même niveau).
  2. Suppression des backslashes isolés (\\\\ seul sur une ligne).
  3. Avertissement sur les problèmes d'accolades (non corrigé automatiquement).

Le fichier corrigé est écrit avec le suffixe ``_fixe`` avant l'extension.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

# ── Correction ───────────────────────────────────────────────────────────────

def fix_tex_file(tex_path: Path, flags_db: Path, output_path: Path | None = None) -> Path:
    """
    Applique les corrections automatiques au fichier .tex source.

    Parameters
    ----------
    tex_path : Path
        Chemin vers le fichier .tex source.
    flags_db : Path
        Chemin vers ``investigation_flags.db``.
    output_path : Path | None
        Chemin du fichier corrigé. Si None, ajoute le suffixe ``_fixe``.

    Returns
    -------
    Path
        Chemin vers le fichier corrigé.
    """
    if output_path is None:
        output_path = tex_path.with_stem(tex_path.stem + "_fixe")

    content = tex_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Charger les drapeaux
    conn = sqlite3.connect(str(flags_db))
    cursor = conn.cursor()

    # Récupérer les environnements non fermés (triés par ligne descendante
    # pour insérer sans décaler les numéros de ligne)
    cursor.execute(
        "SELECT line_num, col_num, description, env_name "
        "FROM investigation_flags "
        "WHERE rule_id IN ('R_TCOLORBOX_CLOSE', 'R_BALANCED_ENVS') "
        "ORDER BY line_num DESC"
    )
    unclosed = cursor.fetchall()

    # Récupérer les backslashes isolés
    cursor.execute(
        "SELECT line_num, col_num "
        "FROM investigation_flags "
        "WHERE rule_id = 'R_NO_BARE_BACKSLASH' "
        "ORDER BY line_num DESC"
    )
    bare_backslashes = cursor.fetchall()

    conn.close()

    # ── Correction 1 : Fermeture des environnements non fermés ──────────

    for line_num, col_num, description, env_name in unclosed:
        # Insérer \\end{env} à la ligne indiquée (1-based -> 0-based)
        insert_at = max(0, line_num - 1)
        end_cmd = f"\\end{{{env_name}}}"
        lines.insert(insert_at, end_cmd)

    # ── Correction 2 : Suppression des backslashes isolés ───────────────

    for line_num, col_num in bare_backslashes:
        idx = line_num - 1  # 1-based -> 0-based
        if 0 <= idx < len(lines):
            line = lines[idx]
            # Si la ligne ne contient que \\ (éventuellement des espaces)
            if line.strip() == "\\":
                lines[idx] = ""  # Remplacer par une ligne vide
            elif line.strip().startswith("\\"):
                # Le \\ est en début de ligne, le retirer
                lines[idx] = line.replace("\\", "", 1)

    # ── Écriture du fichier corrigé ─────────────────────────────────────

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def generate_correction_report(flags_db: Path, report_path: Path) -> None:
    """
    Génère un rapport de correction lisible.

    Parameters
    ----------
    flags_db : Path
        Chemin vers ``investigation_flags.db``.
    report_path : Path
        Chemin vers le fichier de rapport à créer.
    """
    conn = sqlite3.connect(str(flags_db))
    cursor = conn.cursor()

    cursor.execute(
        "SELECT rule_id, severity, line_num, col_num, description, env_name "
        "FROM investigation_flags ORDER BY rule_id, line_num"
    )
    rows = cursor.fetchall()
    conn.close()

    # Compter par type
    env_fixes = sum(1 for r in rows if r[0] in ("R_TCOLORBOX_CLOSE", "R_BALANCED_ENVS"))
    bs_fixes = sum(1 for r in rows if r[0] == "R_NO_BARE_BACKSLASH")
    brace_issues = sum(1 for r in rows if r[0] == "R_BRACE_BALANCE")
    doc_issues = sum(1 for r in rows if r[0] == "R_DOCUMENT_STRUCTURE")

    lines = [
        "=" * 70,
        "RAPPORT DE CORRECTION LaTeX",
        "=" * 70,
        "",
        f"Total de drapeaux détectés : {len(rows)}",
        f"  • Environnements à fermer : {env_fixes}",
        f"  • Backslashes isolés à corriger : {bs_fixes}",
        f"  • Problèmes d'accolades : {brace_issues}",
        f"  • Problèmes de structure document : {doc_issues}",
        "",
        "-" * 70,
        "DÉTAIL DES CORRECTIONS APPLIQUÉES",
        "-" * 70,
        "",
    ]

    for rule_id, severity, line, col, desc, env_name in rows:
        target = f" [{env_name}]" if env_name else ""
        lines.append(f"  L{line}:{col} [{severity}] {rule_id}{target}: {desc}")

    lines.append("")
    lines.append("=" * 70)
    lines.append("FIN DU RAPPORT")
    lines.append("=" * 70)

    report_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    tex_path = repo_root / "theories" / "tex" / "Le-systeme-convolutif-Gabriel.tex"
    flags_db = repo_root / "pipeline_tex_correction_box" / "data" / "investigation_flags.db"
    output_path = repo_root / "pipeline_tex_correction_box" / "data" / "Le-systeme-convolutif-Gabriel_fixe.tex"
    report_path = repo_root / "pipeline_tex_correction_box" / "data" / "rapport_correction.txt"

    fix_tex_file(tex_path, flags_db, output_path)
    generate_correction_report(flags_db, report_path)

    print(f"Fichier corrigé : {output_path}")
    print(f"Rapport : {report_path}")
