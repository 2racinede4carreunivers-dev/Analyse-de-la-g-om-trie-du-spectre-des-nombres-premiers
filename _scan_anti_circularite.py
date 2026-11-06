"""GARDE-FOU CIRCULARITE : la regle 'survivant unique' est-elle triviale ?

Trois controles :
 1) Couverture : quelle part des ancres est placee dans une classe
    a survivant unique ?
 2) Controle par randomisation : si on permute aleatoirement les
    SIGNEES de P = B0 + s*k^e (branches fictives), la regle donne-t-elle
    encore 100% ? Si oui, la regle ne dit rien.
 3) Hors-sample : appliquee a des k arbitraires (non-ancre), la regle
    designe-t-elle une branche ? Et cette branche est-elle coherente
    avec le fait que le candidat designe soit premier ?
"""
import csv
import random
from pathlib import Path

import numpy as np

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
           r"\_ancres_uniques.csv")
BR = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
BIDX = {b: i for i, b in enumerate(BR)}
PRIMES = [3, 5, 7, 11, 13, 17, 19, 23]


def load():
    ks, bs = [], []
    with CSV.open("r", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            ks.append(int(row[0]))
            bs.append(BIDX[row[1]])
    return np.array(ks, dtype=np.int64), np.array(bs, dtype=np.int8)


def build_masks(cand_fn, M):
    masks = np.zeros(M, dtype=np.int32)
    for p in PRIMES:
        for r in range(p):
            m = 0
            for j, c in enumerate(cand_fn(r)):
                if c % p == 0:
                    m |= 1 << j
            masks[r::p] |= m
    return masks


def survivor_branch(masks, M):
    """branche unique survivante par classe (ou -1 si ambigu)."""
    out = np.full(M, -1, dtype=np.int8)
    for j in range(4):
        alive = ((masks >> j) & 1) == 0
        cur = out[alive]
        ok = cur == -1
        out[alive] = np.where(ok, j, -2)
    return out


def main():
    ks, bs = load()
    n = len(ks)
    M = 1
    for p in PRIMES:
        M *= p
    print(f"ancres {n}   M = {M}\n")

    # --- 1) regle reelle ---------------------------------------------------
    def cand_reel(k):
        b = k**5 - k**3 + k - 1
        return (b + k * k, b - k * k, b - k, b + k)

    masks = build_masks(cand_reel, M)
    sb = survivor_branch(masks, M)
    keys = (ks % M).astype(np.int64)
    pred = sb[keys]
    uniq = pred >= 0
    ok = (pred[uniq] == bs[uniq]).sum()
    print(f"1) couverture unique : {uniq.mean():.2%} des ancres")
    print(f"   purete sur ces ancres : {ok}/{uniq.sum()} = {ok/uniq.sum():.6%}")
    print(f"   classes ambigues (>=2 survivants) : {(pred==-2).mean():.2%}\n")

    # --- 2) randomisation des signes ---------------------------------------
    print("2) controle par randomisation (signes permutes) :")
    rng = random.Random(7)
    for trial in range(3):
        pert = list(range(4))
        rng.shuffle(pert)
        base = cand_reel(0)

        def cand_fake(k, pert=pert):
            b = k**5 - k**3 + k - 1
            vals = [b + k * k, b - k * k, b - k, b + k]
            return tuple(vals[pert[j]] for j in range(4))

        mk = build_masks(cand_fake, M)
        s2 = survivor_branch(mk, M)
        p2 = s2[keys]
        u2 = p2 >= 0
        o2 = (p2[u2] == bs[u2]).sum()
        print(f"   essai {trial} (perm {pert}) : couverture {u2.mean():.2%}"
              f"  purete {o2/max(u2.sum(),1):.6%}")

    # --- 3) hors-sample ----------------------------------------------------
    print("\n3) hors-sample (k arbitraires, hors ancres) :")
    surv_ok = 0
    surv_tot = 0
    for k in range(4_000_000, 4_000_000 + 20000):
        c = cand_reel(k)
        s = [j for j in range(4) if all(c[j] % p for p in PRIMES)]
        if len(s) == 1:
            surv_tot += 1
            if c[s[0]] % 2 == 1:      # survivant impair
                surv_ok += 1
    print(f"   k hors-sample a survivant unique : {surv_tot}/20000")
    print(f"   dont candidat impair : {surv_ok}/{surv_tot}")


if __name__ == "__main__":
    main()
