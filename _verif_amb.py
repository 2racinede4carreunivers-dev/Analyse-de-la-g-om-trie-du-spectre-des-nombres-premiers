import csv, sys, sympy
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, candidats, survivants

def spf(n):
    for q in sympy.primerange(2, 500):
        if n % q == 0: return q
    return None

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
amb=0; shown=0
print("=== CAS AMBIGUS : la VRAI branche est-elle prime ? ===")
with CSV.open(encoding="utf-8") as fh:
    for row in csv.reader(fh):
        k=int(row[0]); br=row[1]
        s=survivants(k)
        if len(s)!=1:
            amb+=1
            if shown<4:
                shown+=1
                c=candidats(k)
                print(f"\nk={k}  branche vraie (VRAI terrain) : {br}")
                for j,name in enumerate(BRANCHES):
                    tag = "<== VRAI" if name==br else ""
                    print(f"   {name:<7} = {c[j]:<22} plus petit facteur = {str(spf(c[j])):<6} {tag}")
print(f"\nTotal cas ambigus : {amb:,}")
