"""VERIFIE LE MAPPING BRANCHE <-> POLYNOME SUR TOUT LE CSV DES ANCRES."""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _modele_branches import BRANCHES, candidate  # noqa: E402

CSV = Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
           r"\_ancres_uniques.csv")


def main():
    n = ok = 0
    cpt = Counter()
    ko = []
    with CSV.open("r", encoding="utf-8") as fh:
        for row in csv.reader(fh):
            k, br, val = int(row[0]), row[1], int(row[2])
            n += 1
            if candidate(k, br) == val:
                ok += 1
                cpt[br] += 1
            elif len(ko) < 15:
                ko.append((k, br, val, candidate(k, br)))
    print(f"ancres verifiees : {n}")
    print(f"mapping correct  : {ok}/{n} ({ok/max(n,1):.4%})")
    print(f"repartition branches : {dict(cpt)}")
    if ko:
        print("\nEchecs :")
        for k, br, val, att in ko:
            print(f"  k={k:<8} {br:<6} csv={val:<18} attendu={att:<18}")


if __name__ == "__main__":
    main()
