#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
correction_finale.py — Applique la correction définitive sur Le-systeme-convolutif-Gabriel.tex.

Corrections appliquées :
  1. Fermeture des 24 environnements boitenote non fermés (insertion de \end{boitenote})
  2. Suppression des 2 backslashes isolés (lignes 2258 et 2263) -> "There's no line here to end"
  3. Sauvegarde du fichier corrigé

Usage : python correction_finale.py
"""
from __future__ import annotations
import re
from pathlib import Path

TEX_SRC = Path(r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\Le-systeme-convolutif-Gabriel.tex")
TEX_OUT = Path(r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\Le-systeme-convolutif-Gabriel_corrige.tex")

# Lignes (1-based) des \bare backslash à supprimer
BARE_BACKSLASH_LINES = {2258, 2263}

# Positions d'insertion de \end{boitenote} : (ligne_begin, ligne_insertion_avant)
INSERTIONS = [
    (232, 383), (383, 452), (452, 879), (879, 1121), (1121, 1130),
    (1130, 1710), (1710, 2158), (2158, 2527), (2527, 2533), (2533, 2539),
    (2539, 2550), (2550, 2556), (2556, 3257), (3257, 3402), (3402, 3450),
    (3450, 3490), (3490, 3608), (3608, 3686), (3686, 3772), (3772, 3811),
    (3811, 3879), (3879, 3913), (3913, 4003), (4003, 4021),
]

def main() -> int:
    lines = TEX_SRC.read_text(encoding="utf-8").split("\n")
    original_count = len(lines)

    # ── 1. Supprimer les backslashes isolés (en ordre décroissant) ──
    removed_bs = 0
    for ln in sorted(BARE_BACKSLASH_LINES, reverse=True):
        idx = ln - 1
        if 0 <= idx < len(lines) and lines[idx].strip() == "\\":
            lines.pop(idx)
            removed_bs += 1
            print(f"  [BS] Ligne {ln}: backslash isolé supprimé")

    # ── 2. Insérer \end{boitenote} (en ordre décroissant de ligne_insertion) ──
    # Trier par ligne_insertion descendante pour ne pas décaler les indices
    insertions_sorted = sorted(INSERTIONS, key=lambda x: x[1], reverse=True)
    inserted = 0
    for begin_line, insert_before in insertions_sorted:
        idx = insert_before - 1  # 1-based -> 0-based
        if 0 <= idx <= len(lines):
            lines.insert(idx, "\\end{boitenote}")
            inserted += 1
            print(f"  [ENV] \end{{boitenote}} inséré avant ligne {insert_before} (ferme begin ligne {begin_line})")

    # ── 3. Sauvegarder ──
    TEX_OUT.write_text("\n".join(lines), encoding="utf-8")

    print()
    print("=" * 60)
    print("CORRECTION TERMINÉE")
    print("=" * 60)
    print(f"  Fichier source : {TEX_SRC}")
    print(f"  Fichier corrigé : {TEX_OUT}")
    print(f"  Lignes originales : {original_count}")
    print(f"  Backslashes isolés supprimés : {removed_bs}")
    print(f"  \\end{{boitenote}} insérés : {inserted}")
    print(f"  Lignes finales : {len(lines)}")
    print("=" * 60)

    # ── 4. Vérification rapide ──
    content = TEX_OUT.read_text(encoding="utf-8")
    begin_count = len(re.findall(r"\\begin\{boitenote\}", content))
    end_count = len(re.findall(r"\\end\{boitenote\}", content))
    print()
    print("VÉRIFICATION :")
    print(f"  \\begin{{boitenote}} : {begin_count}")
    print(f"  \\end{{boitenote}}   : {end_count}")
    print(f"  Équilibré : {'OUI' if begin_count == end_count else 'NON'}")

    return 0 if begin_count == end_count and removed_bs == 2 and inserted == 24 else 1

if __name__ == "__main__":
    raise SystemExit(main())