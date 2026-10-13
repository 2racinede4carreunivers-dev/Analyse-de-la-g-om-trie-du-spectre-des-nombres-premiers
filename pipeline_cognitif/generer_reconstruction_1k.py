#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_reconstruction_1k.py
============================
Génère la reconstruction des nombres premiers pour une PLAGE de rapports 1/k
(k = k_debut .. k_fin) à une valeur de n commune (défaut n=10), et écrit le
résultat dans un fichier .txt.

Pour chaque rapport 1/k : type (typique / non typique), ancre n=10, premier
reconstruit P(n), statut de l'ancrage (UNIQUE / CATALOGUE / AMBIGU / ABSENT / ECHEC).
En en-tête et en pied : la QUANTITÉ D'ANCRAGES RECONSTRUITS (succès / total).

Usage :
    python pipeline_cognitif/generer_reconstruction_1k.py
    python pipeline_cognitif/generer_reconstruction_1k.py --n 10 --k-debut 2 --k-fin 100001 --out reconstruction_1k.txt
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Rendre le module dispatcher importable quel que soit le répertoire courant
_ICI = Path(__file__).resolve().parent
if str(_ICI) not in sys.path:
    sys.path.insert(0, str(_ICI))

from multi_ratio_dispatcher import MultiRatioDispatcher, K_MAX_RECORD  # noqa: E402


def generer(n: int, k_debut: int, k_fin: int, out_path: Path) -> dict:
    """Boucle la reconstruction 1/k sur [k_debut, k_fin] pour n, écrit out_path."""
    if k_fin > K_MAX_RECORD:
        raise ValueError(f"k_fin={k_fin} depasse K_MAX_RECORD={K_MAX_RECORD:,}")
    if k_debut < 2:
        raise ValueError("k_debut doit etre >= 2")
    if k_fin < k_debut:
        raise ValueError("k_fin doit etre >= k_debut")

    liste_k = list(range(k_debut, k_fin + 1))
    total = len(liste_k)
    print(f"[*] Reconstruction 1/k pour n={n} | k={k_debut}..{k_fin} ({total:,} rapports)")
    print("[*] Calcul en cours (raccourci O(1) actif pour n=10)...")

    t0 = time.time()
    dispatcher = MultiRatioDispatcher(verbose=False)
    res = dispatcher.requete(n=n, liste_k=liste_k)
    duree = time.time() - t0

    nb_succes = nb_echec = 0
    par_statut = {"UNIQUE": 0, "CATALOGUE": 0, "AMBIGU": 0, "ABSENT": 0}
    for r in res.resultats.values():
        if r.reconstruction_reussie and r.premier_n is not None:
            nb_succes += 1
        else:
            nb_echec += 1
        if len(r.candidats_ancre_n10) > 1:
            par_statut["AMBIGU" if r.ancrage_dynamique else "CATALOGUE"] += 1
        elif len(r.candidats_ancre_n10) == 1:
            par_statut["UNIQUE"] += 1
        else:
            par_statut["ABSENT"] += 1

    taux = (100.0 * nb_succes / total) if total else 0.0
    sep_eq = "=" * 100
    sep = "-" * 100
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(sep_eq + "\n")
        f.write(" RECONSTRUCTION DES NOMBRES PREMIERS - RAPPORTS 1/k (SYSTEME CONVOLUTIF)\n")
        f.write(sep_eq + "\n")
        f.write(f" Valeur de n (nombre de termes) : {n}\n")
        f.write(f" Plage des rapports             : 1/{k_debut}  a  1/{k_fin}\n")
        f.write(f" Nombre total de rapports 1/k    : {total:,}\n")
        f.write(f" Duree du calcul                 : {duree:.2f} s\n")
        f.write(sep_eq + "\n\n")
        f.write(" QUANTITE D'ANCRAGES RECONSTRUITS\n")
        f.write(sep + "\n")
        f.write(f"   Ancrages reconstruits (succes) : {nb_succes:,} / {total:,}\n")
        f.write(f"   Echecs d'ancrage               : {nb_echec:,} / {total:,}\n")
        f.write(f"   Taux de reussite               : {taux:.2f} %\n")
        f.write("\n   Detail par statut d'ancrage :\n")
        f.write(f"     - UNIQUE    (1 candidat premier)  : {par_statut['UNIQUE']:,}\n")
        f.write(f"     - CATALOGUE (ancre du catalogue)  : {par_statut['CATALOGUE']:,}\n")
        f.write(f"     - AMBIGU    (multi, dynamique)    : {par_statut['AMBIGU']:,}\n")
        f.write(f"     - ABSENT    (aucun ancrage n=10)  : {par_statut['ABSENT']:,}\n")
        f.write("\n" + sep_eq + "\n")
        f.write(" DETAIL PAR RAPPORT 1/k\n")
        f.write(sep_eq + "\n")
        f.write(f"{'Rapport':>12} | {'Type':>11} | {'Ancre n=10':>16} | "
                f"{'P(n)':>16} | {'Statut':>9} | {'Src':>4} | Branches\n")
        f.write(sep + "\n")
        for k in liste_k:
            r = res.resultats.get(k)
            if r is None:
                continue
            typ = "typique" if r.typique else "non typique"
            a = str(r.premier_ancre_n10) if r.premier_ancre_n10 is not None else "-"
            p = str(r.premier_n) if r.premier_n is not None else "-"
            if len(r.candidats_ancre_n10) > 1:
                statut = "AMBIGU" if r.ancrage_dynamique else "CATALOGUE"
            elif len(r.candidats_ancre_n10) == 1:
                statut = "UNIQUE"
            else:
                statut = "ABSENT"
            src = "DYN" if r.ancrage_dynamique else "REF"
            branches = ", ".join(
                f"A({pos}){'+' if s > 0 else '-'}={pr}"
                for pos, s, pr in r.candidats_ancre_n10
            ) or "-"
            ok_tag = "" if (r.reconstruction_reussie and r.premier_n is not None) else " [ECHEC]"
            f.write(f"{'1/' + str(k):>12} | {typ:>11} | {a:>16} | "
                    f"{p:>16} | {statut:>9} | {src:>4} | {branches}{ok_tag}\n")
        f.write(sep + "\n")
        f.write(f" TOTAL ancrages reconstruits : {nb_succes:,} / {total:,} ({taux:.2f} %)\n")
        f.write(sep_eq + "\n")

    return {"n": n, "k_debut": k_debut, "k_fin": k_fin, "total": total,
            "succes": nb_succes, "echec": nb_echec, "duree": duree,
            "par_statut": par_statut, "out": str(out_path)}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstruction des premiers pour une plage de rapports 1/k.")
    parser.add_argument("--n", type=int, default=10, help="Nombre de termes (defaut 10).")
    parser.add_argument("--k-debut", type=int, default=2, help="k de debut (defaut 2).")
    parser.add_argument("--k-fin", type=int, default=100001, help="k de fin (defaut 100001).")
    parser.add_argument("--out", type=str, default="reconstruction_1k.txt",
                        help="Fichier .txt de sortie.")
    args = parser.parse_args()

    out_path = Path(args.out)
    stats = generer(args.n, args.k_debut, args.k_fin, out_path)

    taux = (100.0 * stats["succes"] / stats["total"]) if stats["total"] else 0.0
    print("\n[OK] Termine.")
    print(f"    Fichier ecrit        : {out_path.resolve()}")
    print(f"    n                    : {stats['n']}")
    print(f"    Plage 1/k            : 1/{stats['k_debut']} .. 1/{stats['k_fin']}")
    print(f"    Ancrages reconstruits: {stats['succes']:,} / {stats['total']:,} ({taux:.2f} %)")
    print(f"    Duree                : {stats['duree']:.2f} s")


if __name__ == "__main__":
    main()
