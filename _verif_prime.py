import csv, sys, sympy
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import B0

def SA(n): return Fraction(13,8)*2**n - 2
def SB(n): return Fraction(13,4)*2**n - 66

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
rows=[]
with CSV.open(encoding="utf-8") as fh:
    for i,row in enumerate(csv.reader(fh)):
        if i<8: rows.append((int(row[0]),row[1],int(row[2])))
        else: break
print("k      branche   valeur_corrigee   64*P-(SB-SA)  P reel  ?")
for k,br,val in rows:
    n = k//2
    P = int(sympy.prime(n))
    h = 64*P - (SB(n)-SA(n))
    print(f"{k:<6} {br:<8} {val:<18} {str(h):<15} {P:<7} {abs(h)==val}")
