"""Demonstration : d'ou vient vraiment "l'ensemble P complet" pour n != 10.

1. Verification des exemples Niveau 5 du document (k=13, 42, 54) :
   rang_base = primepi(ancre), P(k,n) = prime(rang_base + n - 10).
2. Contre-exemple : une graine PREMIERE arbitraire (aucune origine spectrale)
   produit exactement le meme type d'"ensemble P complet" autour d'elle.
3. Couts de primepi (indicatifs) pour evaluer la faisabilite sur ancres 10^33.
"""
import random
import time

import sympy

# --- 1. Exemples du document (pages 35 / A.2) --------------------------------
print("=== 1. Exemples Niveau 5 du document ===")
cases = [
    # (k, P(k, n=10), n cible, P(k, n) documente)
    (13, 368939, 15, 369023),
    (42, 130617143, 15, 130617251),
    (54, 459010529, 15, 459010597),
]
for k, p10, n, attendu in cases:
    r = int(sympy.primepi(p10))
    obtenu = int(sympy.prime(r + (n - 10)))
    print(f"  k={k:<3} ancre={p10:<12} rang=primepi-> {r:<10} "
          f"P(n={n})={obtenu} attendu={attendu} OK={obtenu == attendu}")

# Documente aussi : 1/3 -> 227 = 49e premier ; n=9 et n=11 autour
r227 = int(sympy.primepi(227))
print(f"  k=3   ancre=227 rang={r227} (doc: 49e) ; "
      f"P(n=9)={sympy.prime(r227 - 1)}, P(n=11)={sympy.prime(r227 + 1)}")

# --- 2. Contre-exemple : graine arbitraire -----------------------------------
print("\n=== 2. Graine premiere arbitraire (aucun rapport 1/k) ===")
rng = random.Random(7)
graine = int(sympy.nextprime(rng.randrange(10**6, 10**7)))
rang = int(sympy.primepi(graine))
print(f"  graine={graine}, rang={rang}")
for dn in (-1, +1, +5):
    q = sympy.prime(rang + dn)
    print(f"  'reconstruction' rang{dn:+d} -> {q} "
          f"(premier par construction: {sympy.isprime(q)})")
print("  => meme mecanique que le Niveau 5 : la table prime/primepi fait tout le travail.")

# --- 3. Cout de primepi ( bornes de faisabilite ) ----------------------------
print("\n=== 3. Cout indicatif de sympy.primepi ===")
for expo in (6, 8, 9):
    t0 = time.perf_counter()
    sympy.primepi(10**expo)
    print(f"  primepi(10^{expo}) : {time.perf_counter() - t0:.2f} s")
print("  (projet lui-meme documente 'blocage 2h' pour primepi sur ancre ~10^20,")
print("   voir patch v7.9 — or les ancres du test 4M valent ~10^33.)")
