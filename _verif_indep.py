import csv, sys
from pathlib import Path
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, M_CRIBLAGE, PRIMES_CRIBLAGE, candidats, survivants

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
n=0; uniq=0; ok=0; viol=0; ecarts=0; statuts={}
with CSV.open(encoding="utf-8") as fh:
    for row in csv.reader(fh):
        k=int(row[0]); br=row[1]; val=int(row[2])
        st=row[3] if len(row)>3 else "?"
        statuts[st]=statuts.get(st,0)+1
        n+=1
        c=candidats(k); j=BRANCHES.index(br)
        if c[j]!=val: ecarts+=1
        if any(c[j]%p==0 for p in PRIMES_CRIBLAGE): viol+=1
        s=survivants(k)
        if len(s)==1:
            uniq+=1
            if s[0]==br: ok+=1
print("lignes CSV          :", f"{n:,}")
print("statuts UNIQUE/CAT  :", statuts)
print("ecarts polynome     :", ecarts)
print("violations criblage  :", viol)
print("survivant unique    :", f"{uniq:,}", f"({uniq/n:.2%})")
print("exactitude          :", f"{ok:,}/{uniq:,}", f"= {ok/max(uniq,1):.6%}")
print("M                   :", f"{M_CRIBLAGE:,}")
