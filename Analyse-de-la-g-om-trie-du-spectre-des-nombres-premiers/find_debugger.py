#!/usr/bin/env python3
import os
os.chdir(r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\src\core")

with open('pipeline.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Trouver la ligne avec "if coherence.incoherent"
for i, line in enumerate(lines):
    if 'if coherence.incoherent' in line:
        print("Found at line", i+1)
        # Afficher les 25 lignes suivantes
        for j in range(i, min(i+25, len(lines))):
            print(f"{j+1}: {lines[j]}", end='')
        break
