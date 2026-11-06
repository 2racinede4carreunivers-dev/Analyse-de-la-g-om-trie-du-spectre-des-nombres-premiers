"""SCAN PROFOND DU CRIBLAGE — quelle borne, quelle regle finale ?
  A) diagnostic des anomalies
  B) convergence accuracy/survivants vs borne
  C) regle 'survivant UNIQUE' -> taux de certitude
  D) k mod 5 ajoute-t-il par-dessus le criblage ?
  E) ancres connues k=2..9
  F) safety: le choix final peut-il etre un COMPOSE ?
  G) plafond: combien d'ancres ont un PREMIER unique parmi les 4 ?
"""
import math
import re
import time
from pathlib import Path

PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
REPORT = Path(PROJ) / "reconstruction_4M.txt"

LABELS = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
CODE = {("8", "-"): 0, ("8", "+"): 1, ("7", "+"): 2, ("7", "-"): 3}
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


def charger():
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
            brs.append(CODE[(pos, signe)])
            B0s.append(B0_depuis_ancre(ancre, k, int(pos), signe))
            ancres.append(ancre)
    return ks, brs, B0s, ancres


if __name__ == "__main__":
    t0 = time.time()
    ks, brs, B0s, ancres = charger()
    n = len(ks)
    print(f"Ancres chargees : {n:,}  ({time.time()-t0:.0f}s)")
    print(f"k      : min {min(ks)}  max {max(ks):,}")
    print(f"ancre  : min {min(ancres):,}  max {max(ancres):,}")
    mx = max(max(B0s[i] + ks[i] ** 2, B0s[i] + ks[i]) for i in range(n))
    print(f"candidat max : {mx:,}")

    # ------------------------------------------------------------ A -----
    print("\n" + "=" * 78)
    print("A — Diagnostic : branche 'vraie' != ancre du rapport ?")
    print("=" * 78)
    anomalies = []
    for i in range(n):
        B0, k = B0s[i], ks[i]
        c = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)[brs[i]]
        if c != ancres[i]:
            anomalies.append(i)
    print(f"Anomalies : {len(anomalies)}")
    for i in anomalies[:10]:
        B0, k = B0s[i], ks[i]
        print(f"  k={k} ancre={ancres[i]} B0={B0}")
        print(f"     cands={B0+k*k}, {B0-k*k}, {B0-k}, {B0+k}")
        print(f"     ancre {'PREMIERE' if is_prime(ancres[i]) else 'COMPOSEE'}")

    # ------------------------------------------------------------ B -----
    print("\n" + "=" * 78)
    print("B — Convergence de la borne de criblage")
    print("=" * 78)
    print(f"\n{'borne':>7} {'nb prim':>8} {'accuracy':>10} {'surv moy':>9} "
          f"{'vrai survit':>12} {'unique %':>9} {'acc|unique':>11}")
    for B in (5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 20000):
        P = primes_upto(B)
        prim = math.prod(P)
        ok = surv_tot = vrai_survit = 0
        uniq_ok = uniq_tot = 0
        for i in range(n):
            B0, k = B0s[i], ks[i]
            surv = [c for c in (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
                    if math.gcd(c, prim) == 1]
            surv_tot += len(surv)
            if not surv:
                continue
            vrai_survit += (surv[0] == (B0 + k*k, B0 - k*k,
                                        B0 - k, B0 + k)[brs[i]])
            ok += (surv[0] == (B0 + k*k, B0 - k*k,
                               B0 - k, B0 + k)[brs[i]])
            if len(surv) == 1:
                uniq_tot += 1
                uniq_ok += (surv[0] == (B0 + k*k, B0 - k*k,
                                        B0 - k, B0 + k)[brs[i]])
        print(f"{B:>7} {len(P):>8} {ok/n:>9.4%} {surv_tot/n:>9.2f} "
              f"{vrai_survit/n:>11.4%} {uniq_tot/n:>8.4%} "
              f"{(uniq_ok/uniq_tot if uniq_tot else 0):>10.4%}")

    # ------------------------------------------------------------ C -----
    print("\n" + "=" * 78)
    print("C — Regle 'survivant UNIQUE' : precision quand le criblage tranche")
    print("=" * 78)
    for B in (20, 100, 1000, 20000):
        P = primes_upto(B)
        prim = math.prod(P)
        u_tot = u_ok = multi_tot = 0
        for i in range(n):
            B0, k = B0s[i], ks[i]
            cands = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
            surv = [c for c in cands if math.gcd(c, prim) == 1]
            if len(surv) == 1:
                u_tot += 1
                u_ok += (surv[0] == cands[brs[i]])
            elif len(surv) > 1:
                multi_tot += 1
        print(f"  borne {B:>6} : unique {u_tot:>7,} ({u_tot/n:6.2%}) "
              f"dont correct {u_ok:,} ({u_ok/max(u_tot,1):7.4%}) | "
              f"ambigus {multi_tot:,}")

    # ------------------------------------------------------------ D -----
    print("\n" + "=" * 78)
    print("D — k mod 5 : signal REEL ou artefact du bruit ?")
    print("=" * 78)
    P = primes_upto(1000)
    prim = math.prod(P)
    conf = {}
    for i in range(n):
        B0, k = B0s[i], ks[i]
        cands = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
        surv = [c for c in cands if math.gcd(c, prim) == 1]
        if not surv:
            continue
        key = (ks[i] % 5, cands.index(surv[0]))
        conf[key] = conf.get(key, 0) + 1
    print("\n  table (k mod 5) x (branche choisie par criblage) :")
    print("        " + "".join(f"{LABELS[b]:>9}" for b in range(4)))
    for r in range(5):
        ligne = "".join(f"{conf.get((r,b),0):>9,}" for b in range(4))
        tot = sum(conf.get((r, b), 0) for b in range(4))
        print(f"  k%5={r} {ligne}   tot {tot:,}")
    print("\n  -> distribution du k mod 5 par branche VRAIE (vérité terrain) :")
    vt = {}
    for i in range(n):
        key = (brs[i], ks[i] % 5)
        vt[key] = vt.get(key, 0) + 1
    print("        " + "".join(f"{r:>9}" for r in range(5)))
    for b in range(4):
        print(f"  {LABELS[b]:6}" + "".join(f"{vt.get((b,r),0):>9,}" for r in range(5)))

    # ------------------------------------------------------------ E -----
    print("\n" + "=" * 78)
    print("E — Ancres connues k=2..9 : regle criblage vs regle parite")
    print("=" * 78)
    CATALOGUE = {
        2: (25, 29, "A(8)-"), 3: (218, 227, "A(8)-"),
        4: (963, 947, "A(8)+"), 5: (3004, 2999, "A(7)+"),
        6: (7565, 7529, "A(8)+"), 7: (16470, 16519, "A(8)-"),
        8: (32263, 32327, "A(8)-"), 9: (58328, 58337, "A(7)-"),
    }
    for B in (20, 100, 1000, 20000):
        P = primes_upto(B)
        prim = math.prod(P)
        print(f"\n  --- criblage < {B} ---")
        score = 0
        for k in sorted(CATALOGUE):
            B0, vrai, etiquette = CATALOGUE[k]
            cands = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
            surv = [c for c in cands if math.gcd(c, prim) == 1]
            if not surv:
                choix, etiq = "AUCUN", "-"
            else:
                choix = surv[0]
                etiq = LABELS[cands.index(choix)]
            ok = (choix == vrai)
            score += ok
            print(f"   k={k}: cands={list(cands)} | survivants={surv} "
                  f"| choisi={choix} ({etiq}) | vrai={vrai} ({etiquette}) "
                  f"{'OK' if ok else 'NON'}")
        print(f"   SCORE criblage : {score}/8")

    # ------------------------------------------------------------ F -----
    print("\n" + "=" * 78)
    print("F — SAFETY : le choix final peut-il etre un COMPOSE ?")
    print("=" * 78)
    for B in (100, 1000, 20000):
        P = primes_upto(B)
        prim = math.prod(P)
        compose_faux = 0
        total = 0
        exemples = []
        for i in range(n):
            B0, k = B0s[i], ks[i]
            cands = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
            surv = [c for c in cands if math.gcd(c, prim) == 1]
            if not surv:
                continue
            total += 1
            if not is_prime(surv[0]):
                compose_faux += 1
                if len(exemples) < 5:
                    exemples.append((k, surv[0], cands))
        print(f"  borne {B:>6} : choix non-premier {compose_faux:>7,} / "
              f"{total:,} ({compose_faux/max(total,1):.4%})")
        for k, c, cands in exemples:
            print(f"      k={k} choisi={c} cands={list(cands)}")

    # ------------------------------------------------------------ G -----
    print("\n" + "=" * 78)
    print("G — PLAFOND : combien d'ancres ont un PREMIER unique ?")
    print("=" * 78)
    zero = uniq = multi = 0
    for i in range(n):
        B0, k = B0s[i], ks[i]
        cands = (B0 + k*k, B0 - k*k, B0 - k, B0 + k)
        ps = [c for c in cands if is_prime(c)]
        if not ps:
            zero += 1
        elif len(ps) == 1:
            uniq += 1
        else:
            multi += 1
    print(f"  0 premier parmi les 4 : {zero:,} ({zero/n:.4%})")
    print(f"  1 premier  UNIQUE      : {uniq:,} ({uniq/n:.4%})")
    print(f"  2+ premiers            : {multi:,} ({multi/n:.4%})")
    print(f"\n  => plafond theorique d'un selecteur PARFAIT : {uniq/n:.4%}")



