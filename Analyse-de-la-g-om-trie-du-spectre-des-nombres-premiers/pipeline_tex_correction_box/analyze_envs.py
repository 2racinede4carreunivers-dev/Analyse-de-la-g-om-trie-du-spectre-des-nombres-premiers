#!/usr/bin/env python3
import re
from collections import Counter

path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

begin_pat = re.compile(r"\\begin{(boitenote[^}]*|tcb@savebox[^}]*)}")
end_pat = re.compile(r"\\end{(boitenote[^}]*|tcb@savebox[^}]*)}")

opens = []
closes = []

for i, line in enumerate(lines, 1):
    for m in begin_pat.finditer(line):
        opens.append((m.group(1), i))
    for m in end_pat.finditer(line):
        closes.append((m.group(1), i))

print("=== BOITENOTE/SAVEBOX ANALYSIS ===")
print(f"Total opened: {len(opens)}")
print(f"Total closed: {len(closes)}")

open_counts = Counter([e for e, _ in opens])
close_counts = Counter([e for e, _ in closes])
all_envs = set(open_counts.keys()) | set(close_counts.keys())

print()
print("Differences (ouvert - fermé):")
for env in sorted(all_envs):
    b = open_counts.get(env, 0)
    c = close_counts.get(env, 0)
    diff = b - c
    status = "OK" if diff == 0 else "PROBLEM"
    print(f"  {env}: opened={b}, closed={c}, diff={diff} [{status}]")

# Show last 10 lines
print()
print("=== DERNIERES LIGNES DU FICHIER ===")
for i in range(max(0, len(lines)-10), len(lines)):
    print(f"{i+1:4d} | {lines[i].rstrip()[:80]}")