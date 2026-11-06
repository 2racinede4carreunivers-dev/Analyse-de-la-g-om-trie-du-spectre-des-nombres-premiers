"""COUVERTURE DU CRIBLAGE MODULAIRE : classes a survivant UNIQUE.

Fait cle : c(k) = B0(k) +/- k^e est un polynome en k, donc
  c(k) mod p  ne depend que de  k mod p.
=> pour tout jeu de premier P, le masque "branches eliminees" est une
   fonction de k mod M, M = produit(P). C'est une REGLE arithmétique
   pure, sans aucun test de primalite.

Si le masque laisse UN SEUL survivant, la branche est DETERMINEE.
On mesure :
  - le % d'ancres placees dans une classe a survivant unique
  - la purete de la regle "survivant unique" sur ces ancres
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


PRIMES = [3, 5, 7, 11, 13, 17, 19, 23]


def kill_table(p):
    tab = np.zeros(p, dtype=np.int32)
    for r in range(p):
        m = 0
        for j, c in enumerate(cand(r)):
            if c % p == 0:
                m |= 1 << j
        tab[r] = m
    return tab


def main():
    t0 = time.time()
    ks, bs = load()
    n = len(ks)
    print(f"ancres {n}  ({time.time()-t0:.0f}s)")
    print(f"k min {ks.min()}  k max {ks.max()}\n")

    tables = {p: kill_table(p) for p in PRIMES}

    print(f"{'M':>9} {'classes 1 surv':>15} {'ancres uniq':>12} "
          f"{'purete regle':>14} {'ancres ambigus':>15}")
    M = 1
    for nb, p in enumerate(PRIMES, start=1):
        M *= p
        masks = np.zeros(M, dtype=np.int32)
        for q in PRIMES[:nb]:
            t = tables[q]
            for r in range(q):
                masks[r::q] |= t[r]
        popc = np.zeros(M, dtype=np.int8)
        for j in range(4):
            popc += ((masks >> j) & 1).astype(np.int8)
        surv = 4 - popc
        uniq_classes = surv == 1
        keys = (ks % M).astype(np.int64)
        is_uniq = uniq_classes[keys]
        amb = ~is_uniq
        if is_uniq.any():
            # branche predite = unique branche non tuee
            surv_branch = np.zeros(M, dtype=np.int8)
            for j in range(4):
                alive = ((masks >> j) & 1) == 0
                surv_branch[alive] = j
            pred = surv_branch[keys]
            m_ok = is_uniq & (pred == bs)
            pure = m_ok.sum() / max(is_uniq.sum(), 1)
        else:
            pure = float("nan")
        print(f"{M:>9} {uniq_classes.mean():>14.2%} {is_uniq.mean():>11.2%} "
              f"{pure:>13.4%} {amb.mean():>14.2%}")
    print(f"\n({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
