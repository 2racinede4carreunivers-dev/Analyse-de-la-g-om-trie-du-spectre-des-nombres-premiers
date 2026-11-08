"""
pipeline_tex_correction_box.py — Orchestrateur du pipeline de correction LaTeX.

Ce module enchaîne les quatre étapes du pipeline :

  1. analyste_tex.py         — Tokenisation et analyse du fichier .tex
  2. miktex_rules.py         — Base de règles de compilation MiKTeX
  3. investigation_gabriel_tex.py — Détection d'erreurs (drapeaux)
  4. tex_fixe_commande.py    — Correction logique (stack-based)

Usage
-----
    python pipeline_tex_correction_box.py [chemin/vers/fichier.tex]

Si aucun chemin n'est fourni, le fichier par défaut est utilisé.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ajouter le répertoire courant au path pour les imports locaux
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyste_tex import analyze_tex_file
from miktex_rules import create_miktex_rules_db
from investigation_gabriel_tex import investigate, save_investigation_flags
from tex_fixe_commande import fix_tex_file, generate_correction_report


# ── Pipeline ─────────────────────────────────────────────────────────────────

def run_pipeline(tex_path: str | Path) -> dict:
    """
    Exécute le pipeline complet de correction LaTeX.

    Parameters
    ----------
    tex_path : str | Path
        Chemin vers le fichier .tex à analyser et corriger.

    Returns
    -------
    dict
        Dictionnaire contenant les chemins vers tous les fichiers générés
        et le résumé des résultats.
    """
    tex_path = Path(tex_path).resolve()
    repo_root = Path(__file__).resolve().parent.parent
    box_dir = Path(__file__).resolve().parent
    data_dir = box_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Chemins de sortie
    analysis_db = data_dir / "relever_CMD_tex_v2.db"
    rules_db = data_dir / "miktex_compilation_rules.db"
    flags_db = data_dir / "investigation_flags.db"
    fixed_tex = data_dir / f"{tex_path.stem}_fixe.tex"
    report_path = data_dir / "rapport_correction.txt"

    print("=" * 60)
    print("PIPELINE DE CORRECTION LaTeX — Étape 1/4 : Analyse du fichier .tex")
    print("=" * 60)

    # ── Étape 1 : Tokenisation et analyse ───────────────────────────────

    print(f"\n[1/4] Analyse de : {tex_path}")
    db_path = analyze_tex_file(tex_path, data_dir)
    print(f"      Base d'analyse créée : {db_path}")

    # ── Étape 2 : Base de règles de compilation ─────────────────────────

    print("\n[2/4] Création de la base de règles de compilation MiKTeX")
    create_miktex_rules_db(rules_db)
    print(f"      Base de règles créée : {rules_db}")

    # ── Étape 3 : Détection d'erreurs (investigation) ───────────────────

    print("\n[3/4] Détection d'erreurs (investigation)")
    flags = investigate(analysis_db)
    save_investigation_flags(flags, flags_db)
    print(f"      {len(flags)} drapeau(x) détecté(x)")
    print(f"      Base de drapeaux sauvegardée : {flags_db}")

    # ── Étape 4 : Correction logique ────────────────────────────────────

    print("\n[4/4] Correction automatique du fichier .tex")
    fixed_path = fix_tex_file(tex_path, flags_db, fixed_tex)
    generate_correction_report(flags_db, report_path)
    print(f"      Fichier corrigé : {fixed_path}")
    print(f"      Rapport de correction : {report_path}")

    # ── Résumé ──────────────────────────────────────────────────────────

    env_fixes = sum(1 for f in flags if f.rule_id in ("R_TCOLORBOX_CLOSE", "R_BALANCED_ENVS"))
    bs_fixes = sum(1 for f in flags if f.rule_id == "R_NO_BARE_BACKSLASH")
    brace_issues = sum(1 for f in flags if f.rule_id == "R_BRACE_BALANCE")
    doc_issues = sum(1 for f in flags if f.rule_id == "R_DOCUMENT_STRUCTURE")

    print("\n" + "=" * 60)
    print("RÉSUMÉ DU PIPELINE")
    print("=" * 60)
    print(f"  Fichier source : {tex_path}")
    print(f"  Total drapeaux : {len(flags)}")
    print(f"  • Environnements à fermer : {env_fixes}")
    print(f"  • Backslashes isolés : {bs_fixes}")
    print(f"  • Problèmes d'accolades : {brace_issues}")
    print(f"  • Problèmes de structure document : {doc_issues}")
    print(f"  Fichier corrigé : {fixed_path}")
    print(f"  Rapport : {report_path}")
    print("=" * 60)

    return {
        "tex_path": tex_path,
        "analysis_db": db_path,
        "rules_db": rules_db,
        "flags_db": flags_db,
        "fixed_tex": fixed_path,
        "report": report_path,
        "total_flags": len(flags),
        "env_fixes": env_fixes,
        "bs_fixes": bs_fixes,
        "brace_issues": brace_issues,
        "doc_issues": doc_issues,
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tex_path = sys.argv[1]
    else:
        tex_path = Path(__file__).resolve().parent.parent / "theories" / "tex" / "Le-systeme-convolutif-Gabriel.tex"

    run_pipeline(tex_path)
