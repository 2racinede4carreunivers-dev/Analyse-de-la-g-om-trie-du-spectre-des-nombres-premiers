#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pythonLLM_computationnel.py — wrapper racine du pipeline pythonLLM.

Interface en langage naturel vers le terminal : l'utilisateur saisit une
demande en francais libre ; le pipeline computationnaliste la traduit en une
commande ``cline`` typee, validee et tracee, puis (option) l'execute.

Ce pipeline NE fait aucune statistique floue : il reconnait les termes par
appartenance ensembliste exacte contre une base SQLite de corpus normatif,
classe par des regles ordonnees a ordre total, valide grammaticalement et au
regard d'une logique deontique, et refuse formellement plutot que d'inventer.

Usage :
    python pythonLLM_computationnel.py "analyse ce graphe de dependances"
    python pythonLLM_computationnel.py --executer "verifie la preuve Lean"
    python pythonLLM_computationnel.py --construire-db
    python pythonLLM_computationnel.py --cwd C:\\mon\\projet "..."

Options :
    --executer        : execute reellement la commande cline si le binaire
                        existe ; sinon emission seule (mode sec par defaut).
    --construire-db   : (re)construit la base SQLite du corpus puis quitte.
    --cwd CHEMIN      : fixe le repertoire de travail transmis a cline (-c).
    --sorties DOSSIER : dossier d'emission (defaut pythonLLM/sorties).
    -h, --help        : aide.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# La sortie console doit etre UTF-8 meme si le terminal est en cp850.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

from pythonLLM.moteur.banque import Banque  # noqa: E402
from pythonLLM.moteur.emission import emettre, ligne_powershell, ligne_sh  # noqa: E402
from pythonLLM.moteur.pipeline import executer_pipeline  # noqa: E402

SORTIES_DEFAUT = RACINE / "pythonLLM" / "sorties"


def _construire_db() -> int:
    from pythonLLM.corpus.construire_db import construire
    cible = RACINE / "pythonLLM" / "corpus" / "corpus_computationnel.db"
    p = construire(cible)
    print(f"Base SQLite creee : {p}")
    return 0


def _afficher_resultat(resultat) -> None:
    """Affiche un resume lisible du resultat."""
    print("=" * 70)
    print(f"Requete   : {resultat.requete}")
    print(f"Intention : {resultat.intention or '(aucune)'}")
    if resultat.reconnaissance.termes_reconnus:
        print("Termes    : " + ", ".join(resultat.reconnaissance.termes_reconnus))
    print("-" * 70)
    if resultat.est_refus:
        print("ISSUE : REFUS FORMEL")
        print(f"  Etape  : {resultat.refus.etape}")
        print(f"  Motif  : {resultat.refus.motif}")
        if resultat.refus.invariants:
            print("  Regles : " + ", ".join(resultat.refus.invariants))
    else:
        print("Commande (PowerShell) :")
        print("  " + ligne_powershell(resultat.argv))
        print("Commande (sh/bash) :")
        print("  " + ligne_sh(resultat.argv))
    print("-" * 70)
    print(f"Empreinte finale SHA-256 : {resultat.trace[-1].empreinte if resultat.trace else '(vide)'}")
    print("=" * 70)


def _executer_reel(resultat) -> int:
    """Execute la commande cline si le binaire est disponible."""
    binaire = shutil.which("cline") or shutil.which("cline.cmd")
    if binaire is None:
        print("[emission seche] binaire 'cline' introuvable ; commande non executee.")
        return 0
    print(f"[execution] {' '.join(resultat.argv)}")
    proc = subprocess.run(list(resultat.argv))
    return proc.returncode


def _principal(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="pythonLLM_computationnel.py",
        description="Pipeline computationnaliste : langage naturel -> commande cline typee.",
        add_help=True,
    )
    parser.add_argument("requete", nargs="*", help="La demande en langage naturel.")
    parser.add_argument("--executer", action="store_true",
                        help="Execute reellement la commande si 'cline' est installe.")
    parser.add_argument("--construire-db", action="store_true",
                        help="(Re)construit la base SQLite du corpus puis quitte.")
    parser.add_argument("--cwd", default=None, help="Repertoire de travail pour cline (-c).")
    parser.add_argument("--sorties", default=str(SORTIES_DEFAUT),
                        help="Dossier d'emission des artefacts.")
    args = parser.parse_args(argv)

    if args.construire_db:
        return _construire_db()

    if not args.requete:
        parser.print_help()
        return 0

    requete = " ".join(args.requete)
    banque = Banque()
    resultat = executer_pipeline(requete, banque=banque, cwd=args.cwd)

    _afficher_resultat(resultat)

    # Emission des artefacts (.ps1 / .sh / .md).
    chemins = emettre(resultat, Path(args.sorties))
    print("Artefacts emis :")
    for c in chemins:
        print(f"  {c}")

    if args.executer and not resultat.est_refus:
        return _executer_reel(resultat)

    # Code de retour : 0 si commande valide, 2 si refus formel.
    return 2 if resultat.est_refus else 0


if __name__ == "__main__":
    raise SystemExit(_principal())
