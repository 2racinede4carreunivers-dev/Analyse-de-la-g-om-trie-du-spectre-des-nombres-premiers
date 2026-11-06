import sys, sympy
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, PRIMES_CRIBLAGE, candidats
def surv(k):
    c=candidats(k)
    return [BRANCHES[i] for i in range(4) if all(c[i]%p for p in PRIMES_CRIBLAGE)]
ks=list(range(4_000_001, 4_000_001+3000))
n=0; avec=0; muet=0; exact=0; faux=0; sans=0
for k in ks:
    c=candidats(k); n+=1
    premiers=[BRANCHES[i] for i in range(4) if sympy.isprime(c[i])]
    if len(premiers)==0: sans+=1; continue
    avec+=1
    s=surv(k)
    if len(s)!=1: muet+=1; continue
    if s[0]==premiers[0]: exact+=1
    else: faux+=1
print("=== HORS-CORPUS, restreint aux k ayant >=1 candidat premier ===")
print(f"  k testes                          : {n}")
print(f"  aucun candidat premier (hors jeu) : {sans}")
print(f"  avec >=1 premier (vrai terrain)   : {avec}")
print(f"  dont regle muette (ambigu)         : {muet}")
print(f"  regle se prononce                 : {exact+faux}")
print(f"  et CORRECTE                        : {exact}")
print(f"  et FAUSSE                         : {faux}")
