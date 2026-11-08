#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\theories\tex\Le-systeme-convolutif-Gabriel_corrige.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Chercher \begin{tcb@savebox} et \end{tcb@savebox}
for i, line in enumerate(lines, 1):
    if "\\begin{tcb@savebox}" in line or "\\end{tcb@savebox}" in line:
        print(f"Ligne {i}: {line.rstrip()[:120]}")