"""ROBUSTESSE : la regle 'k mod M' est-elle vraie ou du sur-apprentissage ?

1) split deterministe 50/50 (hash du k) : purete apprise sur train,
   evaluee sur test.
2) decomposition CRT : k mod 3, k mod 5, k mod 7 testes separement.
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


def purity(ks, bs, keys, M):
    flat = keys.astype(np.int64) * 4 + bs
    cnt = np.bincount(flat, minlength=M * 4).reshape(M, 4)
    return cnt.max(axis=1).sum() / len(bs)


def main():
    ks, bs = load()
    n = len(ks)
    base = max(Counter(bs.tolist()).values()) / n
    # split deterministe : depend uniquement du k (pas de l'ordre du fichier)
    h = (ks * 2654435761) % 1000003
    train = h < 500000
    print(f"ancres {n}  |  train {train.sum()}  test {(~train).sum()}")
    print(f"base rate {base:.4%}\n")

    print(f"{'M':>5} {'train':>9} {'test':>9} {'ecart':>8}")
    for M in (3, 5, 7, 15, 21, 35, 105, 210, 315, 420, 525):
        pt = purity(ks[train], bs[train], ks[train] % M, M)
        pv = purity(ks[~train], bs[~train], ks[~train] % M, M)
        print(f"{M:>5} {pt:>8.4%} {pv:>8.4%} {100*(pv-pt):>+7.2f}")

    print("\ndecomposition CRT (test seul) :")
    for m in (3, 5, 7):
        pv = purity(ks[~train], bs[~train], ks[~train] % m, m)
        print(f"  k mod {m:>2} : {pv:.4%}  ({100*(pv-base):+.2f} pts)")
    # combinaisons
    for mods in ((3, 5), (3, 7), (5, 7), (3, 5, 7)):
        M = 1
        for m in mods:
            M *= m
        pv = purity(ks[~train], bs[~train], ks[~train] % M, M)
        print(f"  k mod {'x'.join(map(str, mods)):>6} : {pv:.4%}")


if __name__ == "__main__":
    main()
