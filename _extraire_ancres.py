"""Extraction des ancres UNIQUE (k -> branche correcte) depuis reconstruction_4M.txt.

Le fichier fait 431 Mo : lecture ligne a ligne, on ne garde que les lignes
de detail 'Rapport | ... | UNIQUE | ... | Branche=X=Y'.

Sortie : _ancres_uniques.csv  (k, branche, valeur)
"""
import csv
import re
from pathlib import Path

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
REPORT = Path(PROJ) / "reconstruction_4M.txt"
OUT = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")

rx_ligne = re.compile(
    r"^\s*1/(\d+)\s*\|.*\|\s*(UNIQUE|CATALOGUE)\s*\|.*\|\s*A\((\d)\)([+-])=(\d+)\s*$"
)

n_total = 0
n_ecu = 0
with REPORT.open("r", encoding="utf-8", errors="replace") as fh, \
        OUT.open("w", newline="", encoding="utf-8") as fout:
    w = csv.writer(fout)
    for line in fh:
        if "UNIQUE" not in line and "CATALOGUE" not in line:
            continue
        n_total += 1
        m = rx_ligne.match(line)
        if not m:
            continue
        k, statut, pos, signe, val = int(m.group(1)), m.group(2), \
            int(m.group(3)), m.group(4), int(m.group(5))
        w.writerow([k, f"A({pos}){signe}", val, statut])
        n_ecu += 1

print(f"lignes detail candidates : {n_total}")
print(f"ancres ecrites           : {n_ecu}")
print(f"-> {OUT}")
