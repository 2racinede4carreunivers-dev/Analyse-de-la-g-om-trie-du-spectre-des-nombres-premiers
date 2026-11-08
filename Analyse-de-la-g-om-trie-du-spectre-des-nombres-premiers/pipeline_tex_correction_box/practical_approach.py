#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lignes dans le fichier: {len(lines)}")

# Afficher lignes 2367 à 2567 (100 lignes avant et après la ligne 2467)
print("\n=== LIGNES 2367-2567 (100 lignes avant et après la ligne 2467) ===")
start = 2366  # index 0-based
end = min(2567, len(lines))  # index 0-based, exclusive

for i in range(start, end):
    print(f"{i+1:4d} | {lines[i].rstrip()[:120]}")

# Vérifier s'il y a des boitenote dans cette zone
import re
begin_pat = re.compile(r'\\\\begin\{(boitenote[^}]*)\}')
end_pat = re.compile(r'\\\\end\{(boitenote[^}]*)\}')

print("\n=== Recherche de boitenote dans la zone 2367-2567 ===")
found_begin = 0
found_end = 0
for i in range(start, end):
    for m in begin_pat.finditer(lines[i]):
        found_begin += 1
        print(f"  \\begin{{boitenote}} à la ligne {i+1}")
    for m in end_pat.finditer(lines[i]):
        found_end += 1
        print(f"  \\end{{boitenote}} à la ligne {i+1}")

if found_begin == 0 and found_end == 0:
    print("Aucun environnement boitenote trouvé dans cette zone (lignes 2367-2567)")