#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Show lines 4020-4030
print("=== LIGNES 4020-4030 ===")
for i in range(4019, min(4030, len(lines))):
    print(f"{i+1:4d} | {lines[i].rstrip()[:120]}")

# Also count boitenote around this area
import re
begin_pat = re.compile(r"\\begin\{(boitenote[^}]*)\}")
end_pat = re.compile(r"\\end\{(boitenote[^}]*)\}")
for i in range(4018, min(4035, len(lines))):
    for m in begin_pat.finditer(lines[i]):
        print(f"  \\begin{{boitenote}} found at line {i+1}: {lines[i].rstrip()[:80]}")
    for m in end_pat.finditer(lines[i]):
        print(f"  \\end{{boitenote}} found at line {i+1}: {lines[i].rstrip()[:80]}")
PYEOF