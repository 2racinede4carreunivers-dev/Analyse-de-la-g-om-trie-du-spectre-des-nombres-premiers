#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Afficher lignes 4030 à 4100
print("=== LIGNES 4030-4100 ===")
for i in range(4029, min(4100, len(lines))):
    print(f"{i+1:4d} | {lines[i].rstrip()[:120]}")