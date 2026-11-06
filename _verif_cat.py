import csv, sys, sympy
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, candidats
CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
rows=[]
with CSV.open(encoding="utf-8") as fh:
    for i,row in enumerate(csv.reader(fh)):
        if i%10==0: rows.append((int(row[0]), row[1], row[3] if len(row)>3 else "?"))
nonprime=[]; ncat=0
for k,br,st in rows:
    if st=="CATALOGUE": ncat+=1
    c=candidats(k); j=BRANCHES.index(br)
    if not sympy.isprime(c[j]): nonprime.append((k,br,st))
print(f"echantillon 1/10 : {len(rows)} ancres   (dont CATALOGUE : {ncat})")
print(f"branche 'vraie' NON premiere : {len(nonprime)}")
for x in nonprime[:5]: print("   ", x)
# les 4 CATALOGUE exacts
with CSV.open(encoding="utf-8") as fh:
    for row in csv.reader(fh):
        if len(row)>3 and row[3]=="CATALOGUE":
            k=int(row[0]); c=candidats(k); j=BRANCHES.index(row[1])
            print(f"  CATALOGUE k={k} {row[1]} val={row[2]} candidat={c[j]} premier={sympy.isprime(c[j])}")
