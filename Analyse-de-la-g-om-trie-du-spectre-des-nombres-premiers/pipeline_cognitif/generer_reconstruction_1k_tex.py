#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generer_reconstruction_1k_tex.py
================================
Genere la RECONSTRUCTION des rapports 1/k non typiques pour une plage k_debut..k_fin
a une valeur de n commune (defaut n=10) et ecrit un rapport LaTeX (.tex) qui
recense, pour TOUS les rapports generes, combien d'ancrages pour un nombre premier
ont ete trouves en trois categories :

    1. UNIQUE : un seul candidat premier parmi les 4 essais Digamma
    2. AMBIGU : plusieurs candidats premiers (confirmation requise)
    3. TOTAL  : somme UNIQUE + AMBIGU (rapports avec ancrage)

Traitement par chunks (defaut 50 000 k) : la memoire reste stable meme pour
plusieurs millions de rapports (le cache d'ancres du dispatcher est purge a
chaque chunk). Rapport non typique = k != 2 (tous les k >= 3).

Usage :
    python pipeline_cognitif/generer_reconstruction_1k_tex.py
    python pipeline_cognitif/generer_reconstruction_1k_tex.py --n 10 \
        --k-debut 1000001 --k-fin 3000001 --out rapports_non_typiques.tex
    # avec detail exhaustif par rapport dans un .txt accompagne :
    ... --detail rapports_non_typiques_detail.txt
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Rendre le module dispatcher importable quel que soit le repertoire courant
_ICI = Path(__file__).resolve().parent
if str(_ICI) not in sys.path:
    sys.path.insert(0, str(_ICI))

from multi_ratio_dispatcher import MultiRatioDispatcher, K_MAX_RECORD  # noqa: E402


def _statut(r) -> str:
    """Statut d'ancrage d'un resultat : UNIQUE / AMBIGU / ABSENT."""
    n_cand = len(r.candidats_ancre_n10)
    if n_cand == 1:
        return "UNIQUE"
    if n_cand > 1:
        return "AMBIGU"
    return "ABSENT"


def _pct(x: int, total: int) -> float:
    return (100.0 * x / total) if total else 0.0


def generer_tex(n: int, k_debut: int, k_fin: int, out_path: Path,
                chunk: int, detail_path: Optional[Path] = None,
                ancres_seules: bool = False) -> dict:
    """Boucle la reconstruction 1/k sur [k_debut, k_fin] par chunks, ecrit out_path (.tex)."""
    if k_fin > K_MAX_RECORD:
        raise ValueError(f"k_fin={k_fin} depasse K_MAX_RECORD={K_MAX_RECORD:,}")
    if k_debut < 3:
        raise ValueError("k_debut doit etre >= 3 (rapports non typiques)")
    if k_fin < k_debut:
        raise ValueError("k_fin doit etre >= k_debut")

    total = k_fin - k_debut + 1
    print(f"[*] Reconstruction 1/k (non typiques) pour n={n} | "
          f"k={k_debut}..{k_fin} ({total:,} rapports)")
    print(f"[*] Chunks de {chunk:,} k - memoire stable, purge du cache par chunk.")

    t0 = time.time()
    nb_unique = nb_ambigue = nb_absent = 0
    nb_succes = nb_echec = 0
    traite = 0

    detail_f = open(detail_path, "w", encoding="utf-8") if detail_path else None
    if detail_f:
        if ancres_seules:
            detail_f.write("% Rapports AVEC ancrage (UNIQUE + AMBIGU) uniquement\n")
        detail_f.write(f"{'Rapport':>12} | {'Ancre n=10':>16} | {'P(n)':>16} | "
                       f"{'Statut':>7} | Branches\n")
        detail_f.write("-" * 100 + "\n")

    try:
        for debut in range(k_debut, k_fin + 1, chunk):
            fin = min(debut + chunk - 1, k_fin)
            liste_k = list(range(debut, fin + 1))
            # Dispatcher neuf par chunk : le cache d'ancres ne grossit pas
            dispatcher = MultiRatioDispatcher(verbose=False)
            res = dispatcher.requete(n=n, liste_k=liste_k)

            for k in liste_k:
                r = res.resultats.get(k)
                if r is None:
                    continue
                st = _statut(r)
                if st == "UNIQUE":
                    nb_unique += 1
                elif st == "AMBIGU":
                    nb_ambigue += 1
                else:
                    nb_absent += 1
                if r.reconstruction_reussie and r.premier_n is not None:
                    nb_succes += 1
                else:
                    nb_echec += 1
                if detail_f and not (ancres_seules and st == "ABSENT"):
                    a = str(r.premier_ancre_n10) if r.premier_ancre_n10 is not None else "-"
                    p = str(r.premier_n) if r.premier_n is not None else "-"
                    branches = ", ".join(
                        f"A({pos}){'+' if s > 0 else '-'}={pr}"
                        for pos, s, pr in r.candidats_ancre_n10
                    ) or "-"
                    detail_f.write(f"{'1/' + str(k):>12} | {a:>16} | {p:>16} | "
                                   f"{st:>7} | {branches}\n")

            traite += len(liste_k)
            dt = time.time() - t0
            debit = traite / dt if dt else 0.0
            reste = (total - traite) / debit if debit else 0.0
            print(f"    [{traite:,}/{total:,}] {100.0 * traite / total:5.1f} % | "
                  f"{debit:,.0f} k/s | reste ~{reste / 60:.1f} min", flush=True)
    finally:
        if detail_f:
            detail_f.close()

    duree = time.time() - t0
    nb_ancrage = nb_unique + nb_ambigue
    nb_total = total

    # ------------------------------------------------------------------ .tex
    maintenant = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    u_pct, a_pct = _pct(nb_unique, total), _pct(nb_ambigue, total)
    t_pct, s_pct = _pct(nb_ancrage, total), _pct(nb_absent, total)
    tex = []
    tex.append("% !TeX program = pdflatex")
    tex.append("% ============================================================")
    tex.append("% Rapports NON TYPIQUES 1/k - Reconstruction des nombres premiers")
    tex.append("% Systeme convolutif spectral - Pipeline Cognitif Gabriel")
    tex.append(f"% Genere le {maintenant}")
    tex.append("% ============================================================")
    tex.append(r"\documentclass[12pt]{article}")
    tex.append(r"\usepackage[utf8]{inputenc}")
    tex.append(r"\usepackage[french]{babel}")
    tex.append(r"\usepackage{booktabs}")
    tex.append(r"\usepackage{geometry}")
    tex.append(r"\geometry{margin=2.2cm}")
    tex.append(r"\title{Reconstruction des nombres premiers\\"
               rf"Rapports non typiques $1/k$ --- ancrages $n={n}$")
    tex.append(r"}")
    tex.append(r"\author{Pipeline cognitif Gabriel --- methode Savard}")
    tex.append(r"\date{" + maintenant + "}")
    tex.append(r"\begin{document}")
    tex.append(r"\maketitle")
    tex.append("")
    tex.append(r"\section*{Parametres}")
    tex.append(r"\begin{itemize}")
    tex.append(rf"\item Nombre de termes commun a tous les rapports : $n={n}$")
    tex.append(rf"\item Plage des rapports non typiques : $1/{k_debut}$ a $1/{k_fin}$")
    tex.append(rf"\item Nombre total de rapports generes : {nb_total:,}")
    tex.append(rf"\item Duree du calcul : {duree:.1f} s")
    tex.append(r"\end{itemize}")
    tex.append("")
    tex.append(r"\section*{Ancrages pour un nombre premier}")
    tex.append("")
    tex.append(r"Pour chaque rapport $1/k$, les quatre branches Digamma "
               r"$(8,-1)$, $(8,+1)$, $(7,+1)$, $(7,-1)$ sont testees : un "
               r"seul candidat premier produit un ancrage \textbf{unique}, "
               r"plusieurs candidats produisent un ancrage \textbf{ambigu}.")
    tex.append("")
    tex.append(r"\begin{table}[h!]")
    tex.append(r"\centering")
    tex.append(rf"\caption{{Synthese des ancrages pour $n={n}$ sur "
               rf"{nb_total:,} rapports non typiques.}}")
    tex.append(r"\begin{tabular}{lrr}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Categorie} & \textbf{Nombre de rapports} & "
               r"\textbf{Pourcentage} \\")
    tex.append(r"\midrule")
    tex.append(rf"1. Unique (un seul candidat premier) & {nb_unique:,} & {u_pct:.2f}\,\% \\")
    tex.append(rf"2. Ambigue (plusieurs candidats premiers) & {nb_ambigue:,} & {a_pct:.2f}\,\% \\")
    tex.append(r"\midrule")
    tex.append(rf"\textbf{{3. Total unique + ambigu}} & \textbf{{{nb_ancrage:,}}} "
               rf"& \textbf{{{t_pct:.2f}\,\%}} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table}")
    tex.append("")
    tex.append(r"\section*{Details complementaires}")
    tex.append(r"\begin{itemize}")
    tex.append(rf"\item Rapports sans aucun ancrage : {nb_absent:,} ({s_pct:.2f}\,\%)")
    tex.append(rf"\item Reconstructions reussies (premier $P(n)$ obtenu) : "
               rf"{nb_succes:,} ({_pct(nb_succes, total):.2f}\,\%)")
    tex.append(rf"\item Echecs d'ancrage : {nb_echec:,}")
    if detail_path:
        tex.append(rf"\item Detail exhaustif par rapport : "
                   rf"\texttt{{{detail_path.name}}}")
    tex.append(r"\end{itemize}")
    tex.append("")
    tex.append(r"\end{document}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(tex) + "\n", encoding="utf-8")

    return {"n": n, "k_debut": k_debut, "k_fin": k_fin, "total": total,
            "unique": nb_unique, "ambigue": nb_ambigue, "absent": nb_absent,
            "ancrage": nb_ancrage, "succes": nb_succes, "echec": nb_echec,
            "duree": duree, "out": str(out_path)}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstruction 1/k (non typiques) -> rapport LaTeX .tex.")
    parser.add_argument("--n", type=int, default=10,
                        help="Nombre de termes, commun a tous les rapports (defaut 10).")
    parser.add_argument("--k-debut", type=int, default=1000001,
                        help="k de debut (defaut 1000001).")
    parser.add_argument("--k-fin", type=int, default=3000001,
                        help="k de fin (defaut 3000001).")
    parser.add_argument("--out", type=str,
                        default="rapports_non_typiques_1000001_3000001.tex",
                        help="Fichier .tex de sortie.")
    parser.add_argument("--chunk", type=int, default=50000,
                        help="Taille des chunks de traitement (defaut 50000).")
    parser.add_argument("--detail", type=str, default=None,
                        help="Optionnel : fichier .txt de detail exhaustif par rapport.")
    parser.add_argument("--ancres-seules", action="store_true",
                        help="Avec --detail : n'ecrire que les rapports AVEC ancrage "
                             "(UNIQUE + AMBIGU), pas les ABSENT.")
    args = parser.parse_args()

    if args.chunk < 1:
        parser.error("--chunk doit etre >= 1")

    out_path = Path(args.out)
    detail_path = Path(args.detail) if args.detail else None
    stats = generer_tex(args.n, args.k_debut, args.k_fin, out_path,
                        args.chunk, detail_path, args.ancres_seules)

    print("\n[OK] Termine.")
    print(f"    Fichier .tex ecrit   : {stats['out']}")
    print(f"    n                    : {stats['n']}")
    print(f"    Plage 1/k            : 1/{stats['k_debut']} .. 1/{stats['k_fin']}")
    print(f"    1. UNIQUE            : {stats['unique']:,}")
    print(f"    2. AMBIGU            : {stats['ambigue']:,}")
    print(f"    3. TOTAL unique+amb. : {stats['ancrage']:,}")
    print(f"    Sans ancrage         : {stats['absent']:,}")
    print(f"    Duree                : {stats['duree']:.1f} s")


if __name__ == "__main__":
    main()

