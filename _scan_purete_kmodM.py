"""PURETES DE LA REGLE 'k mod M' -> BRANCHE.

Fait cle : B0(k) = k^5 - k^3 + k - 1 est une FONCTION de k, donc
(k mod M, B0 mod M) est deterministe par k mod M seulement.
=> toute regle conjointe se reduit a une regle sur k mod M.

On mesure pour M = 2..600 la purete du classifieur argmax(k mod M).
"""
import csv
import sys
from collections import Counter
from pathlib import Path

import numpy as np

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
           r"\_ancres_uniques.csv")
BR = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
BIDX = {b: i for i, b in enumerate(BR)}


def load():
    ks, bs = [], []
    with CSV.open("r", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            ks.append(int(row[0]))
            bs.append(BIDX[row[1]])
    return np.array(ks, dtype=np.int64), np.array(bs, dtype=np.int8)


def main():
    ks, bs = load()
    n = len(ks)
    print(f"ancres : {n}")
    base = max(Counter(bs.tolist()).values()) / n
    print(f"base rate (branche majoritaire) : {base:.4%}\n")
    print(f"{'M':>5} {'purete':>10} {'vs base (pts)':>14}")
    res = []
    for M in range(2, 601):
        keys = ks % M
        # comptage par (classe, branche)
        flat = keys.astype(np.int64) * 4 + bs
        cnt = np.bincount(flat, minlength=M * 4).reshape(M, 4)
        ok = cnt.max(axis=1).sum()
        pure = ok / n
        res.append((pure, M))
        if M <= 30 or M % 50 == 0:
            print(f"{M:>5} {pure:>9.4%} {100*(pure-base):>+13.2f}")
    res.sort(reverse=True)
    print("\nTOP 12 modules M pour la regle 'k mod M' :")
    for pure, M in res[:12]:
        print(f"    M={M:>4}  purete {pure:.4%}  ({100*(pure-base):+.2f} pts)")


if __name__ == "__main__":
    main()
