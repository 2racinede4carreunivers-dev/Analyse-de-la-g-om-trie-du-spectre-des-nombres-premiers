"""VALIDATION DE LA REGLE DE BRANCHE (_regle_branche.py).

Controles :
  1) le mapping B0 + signe*terme reproduit la valeur du CSV (modele) ;
  2) le criblage n'elimine JAMAIS la vraie branche ;
  3) sur les ancres a survivant unique, la regle est exacte a 100 % ;
  4) la regle ne teste PAS la primalite (elle est modulaire).

Lancement :  python _valider_regle_branche.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import (  # noqa: E402
    BRANCHES, M_CRIBLAGE, PRIMES_CRIBLAGE, candidats, survivants,
)

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
           r"\_ancres_uniques.csv")


def main():
    n = 0
    uniq_total = 0
    uniq_ok = 0
    violations = 0
    ko = []
    with CSV.open("r", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            k, br, val = int(row[0]), row[1], int(row[2])
            n += 1
            c = candidats(k)
            j = BRANCHES.index(br)
            # 1) modele polynomial
            if c[j] != val and len(ko) < 10:
                ko.append((k, br, val, c[j]))
            # 2) le criblage n'elimine pas la vraie branche
            if any(c[j] % p == 0 for p in PRIMES_CRIBLAGE):
                violations += 1
            # 3) exactitude quand le survivant est unique
            s = survivants(k)
            if len(s) == 1:
                uniq_total += 1
                if s[0] == br:
                    uniq_ok += 1
                elif len(ko) < 20:
                    ko.append((k, br, s[0], "SURVIVANT FAUX"))

    print(f"ancres analysees              : {n:,}")
    print(f"ecarts modele polynomial      : {len(ko)}")
    print(f"violations criblage (0 attendu): {violations}")
    print(f"ancres a survivant unique     : {uniq_total:,} "
          f"({uniq_total/n:.2%})")
    print(f"exactitude sur ces ancres     : {uniq_ok:,}/{uniq_total:,} "
          f"= {uniq_ok/max(uniq_total,1):.6%}")
    print(f"module de criblage M          : {M_CRIBLAGE:,}")
    for item in ko:
        print("  KO:", item)
    return 0 if (not ko and violations == 0
                 and uniq_ok == uniq_total) else 1


if __name__ == "__main__":
    sys.exit(main())
