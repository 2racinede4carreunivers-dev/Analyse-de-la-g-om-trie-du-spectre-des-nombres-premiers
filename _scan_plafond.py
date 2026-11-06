"""PLAFOND + SAFETY sur un ECHANTILLON (les nombres atteignent 10^33,
le test de primalte complet y serait trop lent).

Note de validite : Miller-Rabin avec les bases 2..37 est DETERMINISTE
seulement pour n < 3.3e24. Au-dela, le resultat est probabiliste
(les faux pseudopremiers sont extremement rares mais possibles).
"""
import math
import random
import re
import sys
import time
from pathlib import Path

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
REPORT = Path(PROJ) / "reconstruction_4M.txt"
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 30000

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


def B0_depuis_ancre(ancre, k, pos, signe):
    if pos == 8 and signe == "-":
        return ancre - k * k
    if pos == 8 and signe == "+":
        return ancre + k * k
    if pos == 7 and signe == "+":
        return ancre + k
    return ancre - k


def primes_upto(B):
    sieve = bytearray([1]) * B
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(B ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, B, i)))
    return [i for i in range(2, B) if sieve[i]]


t0 = time.time()
ks, brs, B0s, ancres = [], [], [], []
with REPORT.open("r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 7 or not parts[0].startswith("1/"):
            continue
        if parts[4] not in ("UNIQUE", "CATALOGUE") or not parts[2].isdigit():
            continue
        k = int(parts[0].split("/")[1])
        ancre = int(parts[2])
        cands = rx.findall(parts[6])
        if not cands:
            continue
        vrai = [c for c in cands if int(c[2]) == ancre] or cands[:1]
        pos, signe = vrai[0][0], vrai[0][1]
        ks.append(k)
        brs.append({("8", "-"): 0, ("8", "+"): 1,
                    ("7", "+"): 2, ("7", "-"): 3}[(pos, signe)])
        B0s.append(B0_depuis_ancre(ancre, k, int(pos), signe))
        ancres.append(ancre)
n = len(ks)
print(f"Ancres chargees : {n:,}  ({time.time()-t0:.0f}s)")

random.seed(20261019)
idx = random.sample(range(n), min(SAMPLE, n))
print(f"Echantillon : {len(idx):,}\n")

# ---- G : plafond theorique -------------------------------------------
print("=" * 78)
print("G — PLAFOND : combien d'ancres ont un PREMIER unique parmi les 4 ?")
print("=" * 78)
zero = uniq = multi = 0
for i in idx:
    B0, k = B0s[i], ks[i]
    ps = [c for c in (B0 + k*k, B0 - k*k, B0 - k, B0 + k) if is_prime(c)]
    if not ps:
        zero += 1
    elif len(ps) == 1:
        uniq += 1
    else:
        multi += 1
m = len(idx)
print(f"  0 premier parmi les 4 : {zero:,} ({zero/m:.4%})")
print(f"  1 premier  UNIQUE      : {uniq:,} ({uniq/m:.4%})")
print(f"  2+ premiers            : {multi:,} ({multi/m:.4%})")
print(f"  => plafond d'un selecteur PARFAIT : {uniq/m:.4%}")

# ---- F : safety ------------------------------------------------------
print("\n" + "=" * 78)
print("F — SAFETY : le choix du criblage peut-il etre un COMPOSE ?")
print("=" * 78)
for B in (100, 1000, 20000):
    prim = math.prod(primes_upto(B))
    faux = tot = 0
    ex = []
    for i in idx:
        B0, k = B0s[i], ks[i]
        surv = [c for c in (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
                if math.gcd(c, prim) == 1]
        if not surv:
            continue
        tot += 1
        if not is_prime(surv[0]):
            faux += 1
            if len(ex) < 3:
                ex.append((k, surv[0]))
    print(f"  borne {B:>6} : choix non-premier {faux:>6,} / {tot:,} "
          f"({faux/max(tot,1):.4%})")
    for k, c in ex:
        print(f"      k={k} choisi={c}")

# ---- H : le criblage ameliore-t-il la selection par COMPARAISON ? ------
print("\n" + "=" * 78)
print("H — Le premier survivant, ou le PLUS GRAND survivant ?")
print("=" * 78)
for B in (1000, 20000):
    prim = math.prod(primes_upto(B))
    premier = plusgrand = 0
    for i in idx:
        B0, k = B0s[i], ks[i]
        cands = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
        surv = [c for c in cands if math.gcd(c, prim) == 1]
        if not surv:
            continue
        vrai = cands[brs[i]]
        premier += (surv[0] == vrai)
        plusgrand += (max(surv) == vrai)
    print(f"  borne {B:>6} : premier survivant {premier/m:.4%} | "
          f"plus grand survivant {plusgrand/m:.4%}")

