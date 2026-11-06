"""TEST DE LA REGLE HYBRIDE DE SELECTION (fournie par l'utilisateur).

Regle :
  B0 = (SB - SA)/k^6
  candidats : B0+k^2, B0-k^2, B0+k, B0-k
  choix :  k=2          -> B0 + k^2
           k>=4 pair    -> B0 - k^2
           k impair     -> B0 + k^2
  Digamma = SB - k^6 * P_cand

TEST 1 : ancres connues k=2..9 (catalogue ANCHORS_N10 = verite terrain).
TEST 2 : rapport reconstruction_4M.txt — chaque ligne UNIQUE/CATALOGUE
         indique la vraie branche retenue (A(8)-, A(8)+, A(7)+, A(7)-),
         donc on peut comparer P_cand a l'ancre reelle.
"""
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

import sympy

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
sys.path.insert(0, PROJ + r"\pipeline_cognitif")
from suites_geometriques_niveau2 import CalculateurNiveau1Entiers  # noqa: E402
from multi_ratio_dispatcher import ANCHORS_N10                     # noqa: E402


def regle(B0: int, k: int) -> int:
    """Règle hybride de l'utilisateur."""
    if k == 2:
        return B0 + k * k
    if k % 2 == 0:
        return B0 - k * k
    return B0 + k * k


def B0_depuis_ancre(ancre: int, k: int, pos: int, signe: str) -> int:
    """Inverse la branche pour recuperer B0 : ancre = B0 +/- k^2 ou +/- k."""
    if pos == 8 and signe == "-":
        return ancre - k * k          # ancre = B0 + k^2
    if pos == 8 and signe == "+":
        return ancre + k * k          # ancre = B0 - k^2
    if pos == 7 and signe == "+":
        return ancre + k              # ancre = B0 - k
    return ancre - k                  # ancre = B0 + k   (A(7)-)


# --------------------------------------------------------------- TEST 1 ---
print("=" * 78)
print("TEST 1 — Ancres connues k=2..9 (verite : catalogue ANCHORS_N10)")
print("=" * 78)
print(f"{'k':>3} {'B0':>8} {'regle':>8} {'catalogue':>10} {'ok':>4}   "
      f"observation")
score1 = 0
for k in range(2, 10):
    r10 = CalculateurNiveau1Entiers(k=k).calculer(10)
    B0 = (r10.somme_B - r10.somme_A) // k**6
    pred = regle(B0, k)
    cat = ANCHORS_N10[k]
    ok = pred == cat
    score1 += ok
    if ok:
        obs = "match"
    else:
        f = sympy.factorint(pred)
        obs = f"pred={pred} COMPOSE={f} | vrai={cat}"
    print(f"{k:>3} {B0:>8} {pred:>8} {cat:>10} {'OUI' if ok else 'NON':>4}   {obs}")
print(f"\n Score k=2..9 : {score1}/8")

# --------------------------------------------------------------- TEST 2 ---
print()
print("=" * 78)
print("TEST 2 — Rapport reconstruction_4M.txt (676 195 ancres)")
print("=" * 78)

REPORT = Path(PROJ) / "reconstruction_4M.txt"
rx = re.compile(r"A\((\d)\)([+-])=(\d+)")

t0 = time.time()
n_total = n_match = 0
statuts = Counter()
par_branch = Counter()
contingence = Counter()        # (parite, branche) -> n
match_par_branch = Counter()
mismatches = []

with REPORT.open("r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 7 or not parts[0].startswith("1/"):
            continue
        statut = parts[4]
        statuts[statut] += 1
        if statut not in ("UNIQUE", "CATALOGUE") or not parts[2].isdigit():
            continue
        k = int(parts[0].split("/")[1])
        ancre = int(parts[2])
        cands = rx.findall(parts[6])
        if not cands:
            continue
        vrai = [c for c in cands if int(c[2]) == ancre]
        pos, signe = (int(vrai[0][0]), vrai[0][1]) if vrai \
            else (int(cands[0][0]), cands[0][1])
        branche = f"A({pos}){signe}"
        B0 = B0_depuis_ancre(ancre, k, pos, signe)
        pred = regle(B0, k)

        n_total += 1
        parite = "pair" if k % 2 == 0 else "impair"
        contingence[(parite, branche)] += 1
        par_branch[branche] += 1
        if pred == ancre:
            n_match += 1
            match_par_branch[branche] += 1
        elif len(mismatches) < 25000:
            mismatches.append((k, ancre, pred, branche))
duree = time.time() - t0

print(f" Lignes par statut : {dict(statuts)}")
print(f" Ancres testees (UNIQUE+CATALOGUE) : {n_total:,}  ({duree:.0f}s)")
print(f" MATCH exact regle == ancre        : {n_match:,} "
      f"({100*n_match/n_total:.2f} %)")
print(f" ECARTS                            : {n_total-n_match:,} "
      f"({100*(n_total-n_match)/n_total:.2f} %)")

print("\n Repartition des vraies branches (ancres uniques) :")
for b, c in par_branch.most_common():
    print(f"   {b:8} {c:>9,}  ({100*c/n_total:5.2f} %)  "
          f"match {match_par_branch[b]:>7,} ({100*match_par_branch[b]/c:5.2f} %)")

plafond = contingence[("impair", "A(8)-")] + contingence[("pair", "A(8)+")]
print(f"\n Plafond theorique de la regle (elle ne choisit que 8-/8+) : "
      f"{plafond:,} / {n_total:,} = {100*plafond/n_total:.2f} %")
print(f" Ancres sur A(7)+/A(7)- = echec automatique : "
      f"{par_branch['A(7)+']+par_branch['A(7)-']:,}")

print("\n Contingence parite(k) x vraie branche :")
hdr = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
print(f"{'':10}" + "".join(f"{h:>12}" for h in hdr))
for par in ("impair", "pair"):
    print(f"{par:10}" + "".join(f"{contingence[(par,h)]:>12,}" for h in hdr))


# --- Parmi les ecarts : compose (benin) ou AUTRE PREMIER (faux ancre) ? ---
print(f"\n Primalite de P_cand sur echantillon d'ecarts "
      f"({len(mismatches):,} cas collectes)...")
n_comp = n_autre_prem = 0
exemples = []
for k, ancre, pred, branche in mismatches:
    if sympy.isprime(pred):
        n_autre_prem += 1
        if len(exemples) < 5:
            exemples.append((k, ancre, pred, branche))
    else:
        n_comp += 1
tot_e = len(mismatches)
print(f"   P_cand COMPOSE (echec benin)        : {n_comp:,}/{tot_e:,} "
      f"({100*n_comp/tot_e:.1f} %)")
print(f"   P_cand AUTRE PREMIER (faux ancre)   : {n_autre_prem:,}/{tot_e:,} "
      f"({100*n_autre_prem/tot_e:.1f} %)")
for k, ancre, pred, branche in exemples:
    print(f"     ex. k={k}: ancre={ancre} ({branche}) vs regle={pred} "
          f"= AUTRE PREMIER")

# --- Controle de fidelite : B0 rapport == (SB-SA)/k^6 recalcule ? ---
print("\n Controle de fidelite : recalcul SA/SB pour 30 ancres au hasard")
rng2 = random.Random(20261019)
ech = set(rng2.sample(range(n_total), 30))
bad = 0
vu = 0
with REPORT.open("r", encoding="utf-8", errors="replace") as f:
    for line in f:
        if "|" not in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 7 or not parts[0].startswith("1/"):
            continue
        if parts[4] not in ("UNIQUE", "CATALOGUE") or not parts[2].isdigit():
            continue
        idx = vu
        vu += 1
        if idx not in ech:
            continue
        k = int(parts[0].split("/")[1])
        ancre = int(parts[2])
        cands = rx.findall(parts[6])
        vrai = [c for c in cands if int(c[2]) == ancre] or cands[:1]
        pos, signe = int(vrai[0][0]), vrai[0][1]
        B0_rapport = B0_depuis_ancre(ancre, k, pos, signe)
        r10 = CalculateurNiveau1Entiers(k=k).calculer(10)
        B0_calc = (r10.somme_B - r10.somme_A) // k**6
        if B0_rapport != B0_calc:
            bad += 1
            print(f"   DIVERGENCE k={k}: rapport={B0_rapport} "
                  f"!= recalcule={B0_calc}")
print(f"   controles OK : {30-bad}/30")

print()
print("=" * 78)
print("VERDICT")
print("=" * 78)
print(f" Match observe     : {100*n_match/n_total:.2f} %  "
      f"({n_match:,}/{n_total:,})")
print(f" Plafond theorique : {100*plafond/n_total:.2f} %  "
      f"(branches A(8) uniquement)")
