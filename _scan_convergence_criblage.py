"""CONVERGENCE DU CRIBLAGE : la regle couvre-t-elle TOUTES les ancres ?

Fait : la vraie branche correspond a un candidat PREMIER, donc jamais
elimine par le criblage (0 violation). La question : en ajoutant des
premiers, la classe k mod M finit-elle par laisser UN SEUL survivant
(= la vraie branche) pour 100 % des ancres ?

Implementation vectorisee (numpy) : pour chaque premier p, le motif
d'elimination ne depend que de k mod p, donc on calcule B0(r) mod p
sur r = k mod p (exponentiation modulaire, pas de debordement).
"""
import csv
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import BRANCHES  # noqa: E402

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
           r"\_ancres_uniques.csv")


def load():
    ks, bs = [], []
    with CSV.open("r", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            ks.append(int(row[0]))
            bs.append(BRANCHES.index(row[1]))
    return (np.array(ks, dtype=np.int64),
            np.array(bs, dtype=np.int8))


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

    alive = np.full(n, 0b1111, dtype=np.uint8)
    P = primes_upto(3000)
    print(f"jeu de primes : {len(P)} (jusqu'a 3000)\n")
    print(f"{'#primes':>9} {'couverture':>12} {'exactitude':>12} "
          f"{'integrite':>11} {'ambigu':>9}")

    idx = 0
    for B in (23, 100, 1000, 3000):
        while idx < len(P) and P[idx] <= B:
            p = P[idx]
            idx += 1
            r = ks % p
            r2 = (r * r) % p
            r3 = (r2 * r) % p
            r5 = (r2 * r3) % p
            b0 = (r5 - r3 + r - 1) % p
            mods = ((b0 + r2) % p, (b0 - r2) % p, (b0 - r) % p, (b0 + r) % p)
            for j in range(4):
                kill = (mods[j] == 0)
                alive[kill] &= np.uint8(~(1 << j) & 0xFF)

        popc = np.zeros(n, dtype=np.uint8)
        for j in range(4):
            popc += ((alive >> j) & 1).astype(np.uint8)
        alive_ok = ((alive >> bs.astype(np.int64)) & 1).astype(bool)
        uniq = popc == 1
        surv_is_true = uniq & alive_ok
        print(f"{idx:>9} {uniq.mean():>11.2%} "
              f"{surv_is_true.sum()/max(uniq.sum(),1):>11.4%} "
              f"{alive_ok.mean():>10.2%} {(popc>1).mean():>8.2%}"
              f"   ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
