"""COMBIEN DE CANDIDATS PREMIERS PAR ANCRE ?

B0(k) = k^5 - k^3 + k - 1  (derive, verifie k=2..9)
candidats : c0=B0+k^2, c1=B0-k^2, c2=B0-k, c3=B0+k

On compte les premiers parmi les 4 pour un balayage de k, et on
compare a la "vraie branche" du rapport reconstruction_4M.txt.
"""
import re
import sys
from pathlib import Path

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
REPORT = Path(PROJ) / "reconstruction_4M.txt"
rx = re.compile(r"A\((\d)\)([+-])=(\d+)")


def is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def B0(k):
    return k**5 - k**3 + k - 1


def candidats(k):
    b = B0(k)
    return (b + k * k, b - k * k, b - k, b + k)


if __name__ == "__main__":
    KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    print("=" * 78)
    print(f"Balayage k = 2..{KMAX} : combien de candidats premiers ?")
    print("=" * 78)
    from collections import Counter
    cnt = Counter()
    exemples_multi = []
    for k in range(2, KMAX + 1):
        cands = candidats(k)
        ps = [c for c in cands if is_prime(c)]
        cnt[len(ps)] += 1
        if len(ps) > 1 and len(exemples_multi) < 12:
            exemples_multi.append((k, cands, ps))
    for nbr in sorted(cnt):
        print(f"  {nbr} premier(s) parmi les 4 : {cnt[nbr]:>5} k "
              f"({cnt[nbr]/max(sum(cnt.values()),1):.2%})")
    print("\n  Exemples avec PLUSIEURS premiers :")
    for k, cands, ps in exemples_multi:
        print(f"    k={k:>4} cands={list(cands)} premiers={ps}")
