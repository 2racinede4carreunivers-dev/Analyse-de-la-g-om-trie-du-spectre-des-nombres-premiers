import csv, sys, sympy
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, candidats
CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
with CSV.open(encoding="utf-8") as fh:
    for row in csv.reader(fh):
        if len(row)>3 and row[3]=="CATALOGUE":
            k=int(row[0]); c=candidats(k); j=BRANCHES.index(row[1])
            print(f"k={k:<3} {row[1]:<6} valeur={row[2]:<12} candidat={c[j]:<12} premier={sympy.isprime(c[j])}")
