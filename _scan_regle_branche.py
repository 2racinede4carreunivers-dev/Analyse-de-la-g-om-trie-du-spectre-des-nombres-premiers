"""CHERCHE LA REGLE DETERMINISTE DE BRANCHE.

Le but : trouver une fonction arithmetique simple de (k, B0) qui
determine QUEL candidat est premier (la branche), SANS test de primalite.

On mesure la PURETE d'un classifieur : 1.0 = toujours correct.

Etapes :
  1) purete de "k mod M" seul            pour M = 2..120
  2) purete de "(k mod M, B0 mod M)"     pour M = 2..40
  3) tableau complet du meilleur M
  4) contrainte dure : quels (k mod M) interdisent quelles branches
"""
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
REPORT = Path(PROJ) / "reconstruction_4M.txt"
LABELS = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
rx = re.compile(r"A\((\d)\)([+-])=(\d+)")


def B0_depuis_ancre(ancre, k, pos, signe):
    if pos == 8 and signe == "-":
        return ancre - k * k
    if pos == 8 and signe == "+":
        return ancre + k * k
    if pos == 7 and signe == "+":
        return ancre + k
    return ancre - k


def charger():
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
            brs.append({("8", "-"): 0, ("8", "+"): 1,
                        ("7", "+"): 2, ("7", "-"): 3}[(pos, signe)])
            B0s.append(B0_depuis_ancre(ancre, k, int(pos), signe))
    return ks, brs, B0s


t0 = time.time()
ks, brs, B0s = charger()
n = len(ks)
print(f"Ancres chargees : {n:,}  ({time.time()-t0:.0f}s)")
base = max(Counter(brs).values()) / n
print(f"Base rate (branche la plus frequente) : {base:.4%}\n")

# ---- 1) purete de "k mod M" -------------------------------------------
print("=" * 78)
print("1 — Purete de la regle 'k mod M' (argmax par classe)")
print("=" * 78)
print(f"{'M':>5} {'purete':>10} {'vs base':>9} {'classes':>8}")
best_k = []
for M in range(2, 121):
    cnt = defaultdict(Counter)
    for i in range(n):
        cnt[ks[i] % M][brs[i]] += 1
    ok = sum(max(c.values()) for c in cnt.values())
    pure = ok / n
    best_k.append((pure, M))
    if M <= 20 or M % 10 == 0:
        print(f"{M:>5} {pure:>9.4%} {100*(pure-base):>+8.2f} {len(cnt):>8}")
best_k.sort(reverse=True)
print("\n  TOP 10 modules pour k seul :")
for pure, M in best_k[:10]:
    print(f"    M={M:>4}  purete {pure:.4%}  ({100*(pure-base):+.2f} pts)")

# ---- 2) purete de (k mod M, B0 mod M) ----------------------------------
print("\n" + "=" * 78)
print("2 — Purete de la regle '(k mod M, B0 mod M)'")
print("=" * 78)
print(f"{'M':>5} {'purete':>10} {'vs base':>9} {'classes':>9}")
best2 = []
for M in range(2, 41):
    cnt = defaultdict(Counter)
    for i in range(n):
        cnt[(ks[i] % M, B0s[i] % M)][brs[i]] += 1
    ok = sum(max(c.values()) for c in cnt.values())
    pure = ok / n
    best2.append((pure, M))
    if M <= 12 or M % 5 == 0:
        print(f"{M:>5} {pure:>9.4%} {100*(pure-base):>+8.2f} {len(cnt):>9}")
best2.sort(reverse=True)
print("\n  TOP 10 modules pour (k, B0) :")
for pure, M in best2[:10]:
    print(f"    M={M:>4}  purete {pure:.4%}  ({100*(pure-base):+.2f} pts)")


