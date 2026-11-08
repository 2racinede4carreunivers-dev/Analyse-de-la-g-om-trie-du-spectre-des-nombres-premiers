#!/usr/bin/env python3
import sys

path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Supprimer la ligne 82 (index 81) qui contient \end{document} placé par erreur
del lines[81]  # 0-indexed, line 82 is at index 81

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Ligne 82 supprimee. Nouveau nombre de lignes :", len(lines))