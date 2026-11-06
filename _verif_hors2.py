import sys, sympy
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, PRIMES_CRIBLAGE, candidats
def surv(k):
    c=candidats(k)
    return [BRANCHES[i] for i in range(4) if all(c[i]%p for p in PRIMES_CRIBLAGE)]
# k hors corpus (>= 4 000 001), verite INDEPENDANTE = primalite reelle
ks=list(range(4_000_001, 4_000_001+1500))
muet=0; prononce=0; exact=0; faux=0; composite=0
for k in ks:
    s=surv(k)
    c=candidats(k)
    if len(s)!=1:
        muet+=1; continue
    prononce+=1
    j=BRANCHES.index(s[0])
    if sympy.isprime(c[j]): exact+=1
    else: faux+=1
print("=== HORS-CORPUS (k = 4 000 001 ...), verite = primalite reelle (sympy) ===")
print(f"  k testes              : {len(ks)}")
print(f"  regle muette          : {muet}")
print(f"  regle se prononce     : {prononce}")
print(f"  survivant = PREMIER   : {exact}  ({exact/max(prononce,1):.4%})")
print(f"  survivant = COMPOSE   : {faux}  ({faux/max(prononce,1):.4%})")
