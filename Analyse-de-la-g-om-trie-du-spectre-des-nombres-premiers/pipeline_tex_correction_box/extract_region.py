#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lignes : {len(lines)}")
print(f"\n=== RÉGION AUTOUR DE LA LIGNE 4027 (50 lignes avant/après) ===\n")

# Extraire 50 lignes avant et 50 lignes après la ligne 4027
start = max(0, 4027 - 50 - 1)  # -1 pour index 0
end = min(len(lines), 4027 + 50)

for i in range(start, end):
    print(f"{i+1:4d} | {lines[i].rstrip()}")