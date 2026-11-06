import csv, sys, sympy
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, PRIMES_CRIBLAGE, candidats

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
rows = []
with CSV.open(encoding="utf-8") as fh:
    for i, row in enumerate(csv.reader(fh)):
        if i % 113 == 0:
            rows.append((int(row[0]), row[1]))
print(f"echantillon : {len(rows)} ancres")
n=bp=up=mp=0; ru=rok=0
for k, br in rows:
    c = candidats(k); j = BRANCHES.index(br)
    prim = [sympy.isprime(x) for x in c]
    n += 1
    if prim[j]: bp += 1
    idx = [i for i,p in enumerate(prim) if p]
    if len(idx)==1: up += 1
    elif len(idx)>1: mp += 1
    surv = [i for i in range(4) if all(c[i] % p for p in PRIMES_CRIBLAGE)]
    if len(surv)==1:
        ru += 1
        if surv[0]==j: rok += 1
print(f"branche du corpus EST premier        : {bp}/{n}")
print(f"branche du corpus = PREMIER UNIQUE    : {up}/{n}")
print(f"plusieurs premiers simultanes        : {mp}/{n}")
print(f"regle se prononce (survivant unique)  : {ru}/{n}")
print(f"  et exacte                           : {rok}/{ru}")
