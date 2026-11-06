import csv, sys, sympy
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, candidats
CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
rows=[]
with CSV.open(encoding="utf-8") as fh:
    for i,row in enumerate(csv.reader(fh)):
        if i%37==0: rows.append((int(row[0]), row[1]))
print("CONTROLE A : sur les cas AMBIGUS (regle muette), la vraie branche est-elle prime ?")
amb=0; ok=0; other=0
for k,br in rows:
    c=candidats(k); j=BRANCHES.index(br)
    if sympy.isprime(c[j]):
        amb+=1
        # combien d'autres branches sont aussi premieres ?
        npre=sum(1 for i in range(4) if i!=j and sympy.isprime(c[i]))
        if npre==0: ok+=1
        else: other+=1
print(f"  echantillon {len(rows)}  |  vrais cas ambigus {amb}  |  branche vraie = premier UNIQUE {ok}  |  +autres premiers {other}")
