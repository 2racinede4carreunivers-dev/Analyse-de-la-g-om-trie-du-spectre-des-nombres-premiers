"""SCAN DE CORRELATIONS — quel critere arithmetique simple predit la
BRANCHE du Digamma (A(8)-, A(8)+, A(7)+, A(7)-) ?

Verite terrain : reconstruction_4M.txt, ancres UNIQUE+CATALOGUE (676 195).
B0 = (SB-SA)/k^6 (controle 30/30 au scan precedent).
Candidats dans l'ORDRE Digamma : [B0+k^2, B0-k^2, B0-k, B0+k].

PARTIE 1 : chargement + taux de base + test de validite du criblage.
PARTIE 2 : scan de features modulaires (train/test 50/50).
PARTIE 3 : regle 'premier candidat survivant au criblage' (primorials).
"""
import math
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
REPORT = Path(PROJ) / "reconstruction_4M.txt"

LABELS = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
CODE = {("8", "-"): 0, ("8", "+"): 1, ("7", "+"): 2, ("7", "-"): 3}
rx = re.compile(r"A\((\d)\)([+-])=(\d+)")


def B0_depuis_ancre(ancre, k, pos, signe):
    if pos == 8 and signe == "-":
        return ancre - k * k
    if pos == 8 and signe == "+":
        return ancre + k * k
    if pos == 7 and signe == "+":
        return ancre + k
    return ancre - k


def candidats(B0, k):
    return [B0 + k * k, B0 - k * k, B0 - k, B0 + k]


t0 = time.time()
ks, brs, B0s = [], [], []
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
        brs.append(CODE[(pos, signe)])
        B0s.append(B0_depuis_ancre(ancre, k, int(pos), signe))
n = len(ks)
print(f" Ancres chargees : {n:,}  ({time.time()-t0:.0f}s)")
freq = Counter(brs)
base = max(freq.values()) / n
for b in range(4):
    print(f"   {LABELS[b]:6} {freq[b]:>9,}  ({100*freq[b]/n:5.2f} %)")
print(f" Base rate (deviner toujours la branche la plus frequente) : "
      f"{base:.4%}")
print(f" Regle parite de l'utilisateur                     : 25.35 %")

# --- Test de validite du criblage : la vraie branche est toujours premiere
primes_small = [p for p in range(2, 1000)
                if all(p % d for d in range(2, int(p**0.5) + 1))]
primorial = math.prod(primes_small)
viol = sum(1 for i in range(n)
           if math.gcd(candidats(B0s[i], ks[i])[brs[i]], primorial) != 1)
print(f"\n Validite criblage : vraie branche divisible par un petit premier"
      f" (<1000) : {viol} cas (attendu 0 — l'ancre est premiere)")


# ------------------------------------------------ PARTIE 2 : features -----
print()
print("=" * 78)
print("PARTIE 2 — Scan de corrélations modulaires (train/test 50/50)")
print("=" * 78)

rng = random.Random(42)
idx = list(range(n))
rng.shuffle(idx)
cut = n // 2
train, test = idx[:cut], idx[cut:]


def evalue(feature_fn):
    """Lookup table majority sur train, accuracy sur test."""
    tbl = {}
    for i in train:
        f = feature_fn(i)
        c = tbl.setdefault(f, [0, 0, 0, 0])
        c[brs[i]] += 1
    ok = 0
    for i in test:
        f = feature_fn(i)
        counts = tbl.get(f)
        pred = max(range(4), key=lambda b: counts[b]) if counts else 0
        ok += (pred == brs[i])
    return ok / len(test)


resultats = []
print(f"\n{'feature':>18} {'accuracy test':>14} {'vs base':>10}")
for m in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 24):
    resultats.append((f"k mod {m}", evalue(lambda i, m=m: ks[i] % m)))
for m in (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16, 24):
    resultats.append((f"B0 mod {m}", evalue(lambda i, m=m: B0s[i] % m)))
for a in (3, 4, 6):
    for b in (3, 4, 6):
        resultats.append(
            (f"(k mod {a},B0 mod {b})",
             evalue(lambda i, a=a, b=b: (ks[i] % a, B0s[i] % b))))
resultats.sort(key=lambda t: -t[1])
for nom, acc in resultats[:12]:
    print(f"{nom:>20} {acc:>13.4%} {100*(acc-0.2884):>+9.2f} pts")

# --------------------------------- PARTIE 3 : criblage primorial ----------
print()
print("=" * 78)
print("PARTIE 3 — Règle : premier candidat SURVIVANT au criblage")
print("  (elimine un candidat si un petit premier le divise ;")
print("   aucun test de primalite — arithmetique modulaire uniquement)")
print("=" * 78)


def premiers_jusqua(B):
    return [p for p in range(2, B)
            if all(p % d for d in range(2, int(p**0.5) + 1))]


for B in (5, 7, 11, 20, 100, 1000):
    P = premiers_jusqua(B)
    prim = math.prod(P)
    ok = abstention = 0
    for i in range(n):
        B0, k = B0s[i], ks[i]
        choix = -1
        for code, c in enumerate((B0 + k*k, B0 - k*k, B0 - k, B0 + k)):
            if math.gcd(c, prim) == 1:
                choix = code
                break
        if choix < 0:
            abstention += 1          # les 4 elimines : cas limite
        elif choix == brs[i]:
            ok += 1
    acc = ok / n
    print(f" criblage < {B:>4} ({len(P):>2} premiers) : "
          f"accuracy {acc:>7.4%}   (abstentions {abstention:,})")

print()
print(" Interpretation : le criblage ecarte les branches dont le candidat")
print(" est divisible par un petit premier — c'est le MEILLEUR candidat")
print(" arithmetique possible : il imite partiellement le test de primalite.")

