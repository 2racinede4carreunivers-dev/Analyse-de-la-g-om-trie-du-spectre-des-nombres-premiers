#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Extraire 75 lignes avant et 75 lignes après la zone problématique (ligne 4027)
start = max(0, 4027 - 75 - 1)  # -1 pour le index 0
end = min(len(lines), 4027 + 75)

print("=== EXTRACTION AUTOUR DE LA LIGNE 4027 (75 lignes avant/après) ===\n")

# Lignes avant (du début de notre fenêtre)
for i in range(start, 4027):  # 4027 est la ligne \begin{boitenote}
    print(f"{i+1:4d} | {lines[i].rstrip()[:100]}")

print("\n--- Zone du boitenote problématique (lignes 4026-4031) ---\n")

# Les lignes du boitenote problématique
for i in range(4025, min(4032, len(lines))):
    print(f"{i+1:4d} | {lines[i].rstrip()[:100]}")

print("\n=== LIGNES APRÈS LA ZONE (à partir de 4032) ===\n")

# Lignes après
for i in range(4031, min(4040, len(lines))):
    print(f"{i+1:4d} | {lines[i].rstrip()[:100]}")

print(f"\nTotal lignes extraites: {end - start}")