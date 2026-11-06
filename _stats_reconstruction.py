"""Analyse statistique du rapport de reconstruction (ancres 1/k).

- format, statuts, slots Digamma
- taux d'ancres UNIQUE vs baseline de hasard (1 chance sur ln(N), 4 essais)
- doublons d'ancres, coherence ancre == P(n=10) == slot
- echantillon de primalite croisee (sympy)
"""
import math
import random
from collections import Counter
from pathlib import Path

import sympy

PATH = Path(
    r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
    r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
    r"\reconstruction_4M.txt"
)

head, tail = [], []
status_field = Counter()
part_lens = Counter()
slots = Counter()
digit_counts = Counter()
anchors = set()
dup_anchors = 0
k_lines = 0
note_lines = 0
other_lines = 0
internal_mismatch = 0
expected_success = 0.0
k_min = k_max = None
samples = []

# reservoir sampling pour test de primalite
RESERVOIR = 3000
reservoir = []
rng = random.Random(20261019)

with PATH.open("r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if len(head) < 12:
            head.append(line.rstrip("\n"))
        tail.append(line.rstrip("\n"))
        if len(tail) > 12:
            tail.pop(0)

        s = line.strip()
        if not s:
            continue
        if s.startswith("Note:"):
            note_lines += 1
            continue
        if "|" not in s:
            other_lines += 1
            continue

        parts = [p.strip() for p in s.split("|")]
        first = parts[0]
        if "/" not in first:
            other_lines += 1
            continue
        try:
            k = int(first.split("/")[1])
        except ValueError:
            other_lines += 1
            continue

        k_lines += 1
        if k_min is None or k < k_min:
            k_min = k
        if k_max is None or k > k_max:
            k_max = k
        part_lens[len(parts)] += 1
        if len(parts) > 4:
            status_field[parts[4]] += 1
        if len(parts) > 6 and "=" in parts[6]:
            slots[parts[6].split("=")[0]] += 1

        # ancre (champ 2) si numerique
        anchor = None
        if len(parts) > 2 and parts[2].isdigit():
            anchor = int(parts[2])
            digit_counts[len(parts[2])] += 1
            if anchor in anchors:
                dup_anchors += 1
            else:
                anchors.add(anchor)
            if len(reservoir) < RESERVOIR:
                reservoir.append(anchor)
            else:
                j = rng.randrange(k_lines)
                if j < RESERVOIR:
                    reservoir[j] = anchor
            # coherence interne : ancre == P(n=10) == valeur du slot
            if len(parts) > 3 and parts[3].isdigit() and int(parts[3]) != anchor:
                internal_mismatch += 1
            elif len(parts) > 6 and "=" in parts[6]:
                try:
                    if int(parts[6].split("=", 1)[1]) != anchor:
                        internal_mismatch += 1
                except ValueError:
                    pass

        # baseline de hasard : N ~= k^5 (constante negligeable dans ln)
        n_est = float(anchor) if anchor else float(k) ** 5
        p1 = 1.0 / math.log(n_est)
        expected_success += 1.0 - (1.0 - p1) ** 4

        if k_lines % 400_000 == 0 and len(samples) < 8:
            samples.append(s[:220])

print("=== ENTETE (12 premieres lignes) ===")
for l in head:
    print("   ", l[:220])
print("=== QUEUE (12 dernieres lignes) ===")
for l in tail:
    print("   ", l[:220])
print()
print("=== VOLUMETRIE ===")
print(f"k-lines        : {k_lines:,}   (k de {k_min:,} a {k_max:,})")
print(f"lignes Note    : {note_lines:,}")
print(f"autres lignes  : {other_lines:,}")
print(f"nb de champs   : {dict(part_lens)}")
print()
print("=== STATUTS (champ 5) ===")
for st, c in status_field.most_common(15):
    print(f"   {st!r:30} {c:>10,}")
print()
print("=== SLOTS DIGAMMA ===")
for sl, c in slots.most_common(12):
    print(f"   {sl:8} {c:>10,}")
print()
print("=== ANCRES ===")
print(f"distinctes     : {len(anchors):,}")
print(f"en doublon     : {dup_anchors:,}")
print(f"incoherences ancre/P/slot : {internal_mismatch:,}")
print("chiffres       :", dict(sorted(digit_counts.items())))
print()
print("=== OBSERVE vs BASELINE DE HASARD ===")
print(f"succes attendus si 4 essais aleatoires (1/ln N) : {expected_success:,.0f}")
print(f"taux attendu                                    : {expected_success / max(k_lines,1):.4%}")
n_uniq = status_field.get("UNIQUE", 0)
print(f"taux UNIQUE observe                             : {n_uniq / max(k_lines,1):.4%}")
if expected_success > 0:
    print(f"ratio observe/attendu                           : {n_uniq / expected_success:.3f}")
print()
print("=== ECHANTILLONS A MI-CHEMIN ===")
for s in samples:
    print("   ", s)
print()

if reservoir:
    bad = [a for a in reservoir if not sympy.isprime(a)]
    print(f"=== PRIMALITE (echantillon {len(reservoir)}) ===")
    print("   non premiers :", len(bad))
    if bad:
        for a in bad[:10]:
            print("     ", a, sympy.factorint(a))
