"""REGLE MODULAIRE PURE : 'premier candidat survivant au criblage'.

Pour chaque k, on elimine tout candidat divisible par un premier p du
jeu de primes P (criblage deterministe, aucune primalite testee).
On garde le PREMIER survivant dans l'ordre [A(8)-, A(8)+, A(7)+, A(7)-].

On mesure l'accuracy contre la vraie branche des 676 191 ancres.
Le meme algorithme, applique avec un jeu de primes plus grand, doit
-> 100% si la regle est "la branche = candidat premier".
"""
import csv
import time
from pathlib import Path

import numpy as np

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
           r"\_ancres_uniques.csv")
BR = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
BIDX = {b: i for i, b in enumerate(BR)}


def B0(k):
    return k**5 - k**3 + k - 1


def cand(k):
    b = B0(k)
    return (b + k * k, b - k * k, b - k, b + k)


def load():
    ks, bs = [], []
    with CSV.open("r", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            ks.append(int(row[0]))
            bs.append(BIDX[row[1]])
    return np.array(ks, dtype=np.int64), np.array(bs, dtype=np.int8)


def primes_upto(B):
    sieve = np.ones(B + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(B ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = False
    return [i for i in range(2, B + 1) if sieve[i]]


def main():
    t0 = time.time()
    ks, bs = load()
    n = len(ks)
    print(f"ancres {n}  ({time.time()-t0:.0f}s)")
    base = max(np.bincount(bs, minlength=4)) / n
    print(f"base rate {base:.4%}\n")

    for B in (5, 7, 11, 13, 17, 31, 100, 1000):
        P = primes_upto(B)
        ok = 0
        abst = 0
        for i in range(n):
            k = int(ks[i])
            cs = cand(k)
            surv = [j for j in range(4)
                    if all(cs[j] % p for p in P)]
            if not surv:
                abst += 1
            elif surv[0] == int(bs[i]):
                ok += 1
        print(f" primes < {B:>5} ({len(P):>3}) : accuracy {ok/n:>8.4%}"
              f"  abstentions {abst:>6}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
