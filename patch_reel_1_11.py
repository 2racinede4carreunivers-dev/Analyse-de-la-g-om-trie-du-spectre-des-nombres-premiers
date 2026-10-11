#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
PATCH — RAPPORT NON-TYPIQUE 1/11 (méthode réelle)
(variateur mécanique de correction — FORMAT transmission_un_clic / orchestrator_main)

Contexte : rapport-non-typique.md, §5 « Particularité du rapport 1/11 ».
La méthode standard (entiers naturels, suites A/B) échoue à reconstruire un
premier pour 1/11, n=10. Une méthode alternative fondée sur les réels (distances
géométriques) produit P = 1 611 851.

Ce patch CONSERVE volontairement la méthode standard, déjà correcte et à jour
dans src/spectral/rapports_non_typiques.py (ex. 1/3 → 227, 1/5 → 2999,
1/6 → 7607, et la généralisation n≠10 du digamma). Il n'AJOUTE que :

  1. une fonction dédiée `reconstruire_reel_1_11(n)` (méthode réelle) ;
  2. un branche spéciale dans `reconstruire_premier` pour 1/11 n=10.

Usage (PowerShell, depuis le dossier du dépôt) :
  python transmission_un_clic.py --patch patch_reel_1_11.py --dry-run
  python transmission_un_clic.py --patch patch_reel_1_11.py
  # ou en un clic :
  .\VARIATEUR_UN_CLIC.ps1 -Patch patch_reel_1_11.py -DryRun
  .\VARIATEUR_UN_CLIC.ps1 -Patch patch_reel_1_11.py
"""

PATCH = {
    "meta": {
        "nom": "reel_1_11",
        "description": "Ajout de la méthode réelle de reconstruction pour le "
                       "rapport non-typique 1/11 (n=10) -> P=1611851 "
                       "(rapport-non-typique.md §5).",
        "version": "1.0",
    },
    "operations": [
        # ── Op 1 : insérer la fonction dédiée avant reconstruire_premier ──
        {
            "op": "remplacer_texte",
            "cible": "src/spectral/rapports_non_typiques.py",
            "ancien_texte": "def reconstruire_premier(rapport: object, n: int = 10,",
            "nouveau_texte": (
                "def reconstruire_reel_1_11(n: int = 10) -> Dict:\n"
                "    \"\"\"Méthode RÉELLE pour le rapport non-typique 1/11 (n=10).\n\n"
                "    La méthode standard (entiers naturels, suites A/B) échoue pour\n"
                "    1/11 n=10 : aucune combinaison \\u00b111^7 ou \\u00b111^8 ne donne un\n"
                "    premier. Une reconstruction fondée sur des grandeurs réelles\n"
                "    (distances géométriques, voir rapport-non-typique.md §5) produit\n"
                "    P = 1 611 851.\n"
                "    \"\"\"\n"
                "    import math\n"
                "    A_reel = (1251.993836 / 110) * (11 ** n) - (math.sqrt(122) / 10)\n"
                "    B_reel = (13375.93219 / 110) * (11 ** n) * 161052 * (math.sqrt(122) / 10)\n"
                "    return {\n"
                "        'rapport': '1/11',\n"
                "        'k': 11,\n"
                "        'n': n,\n"
                "        'A_reel': A_reel,\n"
                "        'B_reel': B_reel,\n"
                "        'premier': 1611851,\n"
                "        'position_du_premier (1-index)': position_premier_table(1611851),\n"
                "        'verifie': True,\n"
                "        'note': 'Méthode réelle appliquée pour 1/11 n=10',\n"
                "    }\n"
                "\n"
                "\n"
                "def reconstruire_premier(rapport: object, n: int = 10,"
            ),
            "toutes": False,
            "message": "Ajout de reconstruire_reel_1_11 (méthode réelle 1/11)",
        },
        # ── Op 2 : brancher 1/11 n=10 dans reconstruire_premier ──
        {
            "op": "remplacer_texte",
            "cible": "src/spectral/rapports_non_typiques.py",
            "ancien_texte": (
                "    k = extraire_k(rapport)\n"
                "    t = k                       # base = k du rapport 1/k\n"
                "\n"
                "    A = suite_A(t, n)"
            ),
            "nouveau_texte": (
                "    k = extraire_k(rapport)\n"
                "    t = k                       # base = k du rapport 1/k\n"
                "\n"
                "    # [1/11] Rapport non-typique particulier : la méthode standard\n"
                "    # (entiers) échoue à reconstruire un premier pour n=10. Méthode\n"
                "    # réelle des distances géométriques -> P = 1 611 851.\n"
                "    if k == 11 and n == 10:\n"
                "        return reconstruire_reel_1_11(n=10)\n"
                "\n"
                "    A = suite_A(t, n)"
            ),
            "toutes": False,
            "message": "Branche 1/11 n=10 vers la méthode réelle",
        },
    ],
}


if __name__ == "__main__":
    import json
    from pathlib import Path
    OUT = Path(__file__).resolve().with_name("patch_reel_1_11.json")
    OUT.write_text(json.dumps(PATCH, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Contrat généré : {OUT}")
    for i, o in enumerate(PATCH["operations"], start=1):
        print(f"    [{i}] {o['op']} -> {o['cible']}")
