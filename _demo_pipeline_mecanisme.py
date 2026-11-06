"""Demonstration en direct : ce que le pipeline fait reellement, k par k.

1. n=10 (les grandes reconstructions) : arithmetique pure + test de primalite,
   AUCUNE table de premiers appelee (raccourci O(1) v7.9).
2. n!=10 : LA table est utilisee via sympy.primepi / sympy.prime
   (= ce que le .thy appelle tblPremiers), avec decalage de rang n-10.
3. Le catalogue ANCHORS_N10 (k=2..9, codes en dur) sert de VALIDATION.
"""
import sys
import time

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
sys.path.insert(0, PROJ + r"\pipeline_cognitif")

from multi_ratio_dispatcher import (MultiRatioDispatcher, ANCHORS_N10,
                                    _position_dans_P, _nieme_premier)

print("Catalogue code en dur (ANCHORS_N10) :", ANCHORS_N10)

d = MultiRatioDispatcher()

print("\n=== 1. n=10 : ancrage par ARITHMETIQUE (aucune table) ===")
t0 = time.time()
res = d.requete(n=10, liste_k=[3, 30, 100])
dt = time.time() - t0
for k, r in res.resultats.items():
    src = "REF (catalogue)" if k in ANCHORS_N10 else "DYN"
    print(f" k={k:<4} ancre={r.premier_ancre_n10}  statut="
          f"{'UNIQUE' if len(r.candidats_ancre_n10)==1 else 'AMBIGU/ABSENT'}"
          f"  src={src}  rang={r.position_dans_P}")
print(f" Duree : {dt:.4f} s  (primepi JAMAIS appele pour n=10)")

print("\n=== 2. n!=10 : LA TABLE (sympy.primepi/prime) + decalage de rang ===")
t0 = time.time()
res = d.requete(n=12, liste_k=[3])
dt = time.time() - t0
for k, r in res.resultats.items():
    print(f" k={k} : ancre={r.premier_ancre_n10}")
    print(f"   rang base  = primepi(ancre) = "
          f"{_position_dans_P(r.premier_ancre_n10)}")
    print(f"   rang cible = rang base + (12-10) = "
          f"{_position_dans_P(r.premier_ancre_n10) + 2}")
    print(f"   P(n=12)    = prime(rang cible) = {r.premier_n}")
    print(f"   digamma    = SB(k,12) - P*k^6 = {r.digamma_calcule}")
    print(f"   12e premier vrai : {__import__('sympy').prime(12)} "
          f"(different : la sequence de k=3 part de 227)")
print(f" Duree : {dt:.4f} s")

print("\n=== 3. Test exact du chemin 'tblPremiers' ===")
print(" primepi(227) =", _position_dans_P(227), "(227 = 49e premier)")
print(" prime(51)    =", _nieme_premier(51))
print(" -> (227 rank 49) + 2 = rank 51 -> 233 ; le pipeline calcule bien")
print("    P = tblPremiers[rang_base + n - 10] via sympy, sans fichier table.")
