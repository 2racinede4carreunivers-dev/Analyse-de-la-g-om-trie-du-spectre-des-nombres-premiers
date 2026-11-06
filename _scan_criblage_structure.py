"""STRUCTURE : le signal 'k mod M' vient-il du CRIBLAGE par les premiers de M ?

Pour un premier p, candidat c(k) = B0(k) + s*k^e est divisible par p
selon k mod p. On construit donc :
  KILL[p][r] = ensemble des branches eliminees pour k = r (mod p)

Puis on mesure, pour M = produit de premiers, le nombre de survivants
par classe k mod M -> plafond theorique de la regle "argmax".
"""
import csv
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


PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]


def kill_table(p):
    """KILL[p][r] = bitmask des branches divisibles par p pour k = r mod p."""
    tab = []
    for r in range(p):
        m = 0
        for j, c in enumerate(cand(r)):
            if c % p == 0:
                m |= 1 << j
        tab.append(m)
    return tab


def main():
    ks, bs = load()
    n = len(ks)
    base = max(np.bincount(bs, minlength=4)) / n
    print(f"ancres {n}  base {base:.4%}\n")

    print("Table d'elimination par premier p (branches divisibles) :")
    tables = {}
    for p in PRIMES:
        t = kill_table(p)
        tables[p] = t
        dist = {}
        for m in t:
            dist[m] = dist.get(m, 0) + 1
        s = "  ".join(
            "r={}:{}".format(r, "+".join(BR[j] for j in range(4) if m >> j & 1) or "-")
            for r, m in enumerate(t)
        )
        print(f"  p={p:>2} : {s}")

    # --- purete et survivants pour M = produit de premiers ---------------
    print(f"\n{'M':>8} {'purge':>9} {'survivants/ classe':>22} {'1 survivant':>12}")
    for nb in range(1, 7):
        M = 1
        for p in PRIMES[:nb]:
            M *= p
        masks = np.zeros(M, dtype=np.int32)
        for p in PRIMES[:nb]:
            t = tables[p]
            for r, m in enumerate(t):
                idx = np.arange(r, M, p)
                masks[idx] |= m
        surv = 4 - np.array([bin(int(x)).count("1") for x in masks])
        keys = ks % M
        flat = keys.astype(np.int64) * 4 + bs
        cnt = np.bincount(flat, minlength=M * 4).reshape(M, 4)
        pure = cnt.max(axis=1).sum() / n
        uniq = (surv == 1).mean()
        print(f"{M:>8} {pure:>8.4%} {surv.mean():>18.2f} {uniq:>11.1%}")


if __name__ == "__main__":
    main()
