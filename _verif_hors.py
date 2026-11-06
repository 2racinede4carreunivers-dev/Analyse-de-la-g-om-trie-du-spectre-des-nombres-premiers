import sys, sympy
sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES, PRIMES_CRIBLAGE, candidats
# VERITE INDEPENDANTE : test de primalite reel (sympy), sur des k ou le moteur
# d origine a ECHOUE (1/10, 1/11, 1/12, 1/14 ...) puis sur un balayage large.
def sieve_survivor(k):
    c=candidats(k)
    return [BRANCHES[i] for i in range(4) if all(c[i]%p for p in PRIMES_CRIBLAGE)]
echecs=[10,11,12,14,16,17,19,20,21,22,23,24,25,26,27,28,29,30]
print("=== k ou le moteur d origine a ECHOUE (verite = primalite reelle) ===")
for k in echecs:
    c=candidats(k)
    prim=[BRANCHES[i] if sympy.isprime(c[i]) else None for i in range(4)]
    vrais=[x for x in prim if x]
    s=sieve_survivor(k)
    verdict = "OK" if (len(vrais)==1 and s==vrais) else ("AMBIGU" if len(vrais)!=1 else "ECHEC")
    print(f"k={k:<3} vrais premiers={vrais}  crible={s}  -> {verdict}")
