#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Afficher lignes 2460-2480
print("=== LIGNES 2460-2480 ===")
for i in range(2459, min(2480, len(lines))):
    print(f"{i+1:4d} | {lines[i].rstrip()[:120]}")

# Chercher les boitenote dans cette zone
import re
begin_pat = re.compile(r'\\\\begin\{(boitenote[^}]*)\}')
end_pat = re.compile(r'\\\\end\{(boitenote[^}]*)\}')

print("\n=== ZONE BOITENOTE DANS CETTE AREE ===")
for i in range(2459, min(2480, len(lines))):
    for m in begin_pat.finditer(lines[i]):
        print(f"  \\begin{{boitenote}} trouvé à la ligne {i+1}")
    for m in end_pat.finditer(lines[i]):
        print(f"  \\end{{boitenote}} trouvé à la ligne {i+1}")