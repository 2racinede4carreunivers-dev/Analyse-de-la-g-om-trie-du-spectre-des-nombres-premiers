# -*- coding: utf-8 -*-
"""
moteur/construction.py — instanciation d'un gabarit -> AST de commande.

Chaque intention active un gabarit d'options valide (tire de la grammaire du
CLI). On ne concatene jamais de texte : on assemble un ``CommandeCline`` dont
les options sont des paires ``(nom_long, valeur)`` typees. La requete
normalisee, rejointe en phrase, devient l'argument positionnel (le « prompt »).
"""
from __future__ import annotations

from typing import Optional, Tuple

from .banque import Banque
from .normalisation import rejoindre, normaliser
from ..modele.entites import CommandeCline, ResultatReconnaissance

# Gabarits par intention : tuples d'options (nom_long, valeur_ou_None).
# Les noms longs appartiennent tous a la grammaire (valides au validateur).
_GABARITS = {
    "structure_graphe": (
        ("--thinking", "high"),
        ("--auto-approve", "true"),
        ("--json", None),
    ),
    "preuve_formelle": (
        ("--thinking", "xhigh"),
        ("--auto-approve", "true"),
    ),
    "calcul_exact": (
        ("--thinking", "high"),
        ("--auto-approve", "true"),
    ),
    "conformite_normative": (
        ("--plan", None),
        ("--thinking", "high"),
    ),
    "validation_code": (
        ("--thinking", "medium"),
        ("--auto-approve", "true"),
    ),
    "modelisation_incertaine": (
        ("--thinking", "low"),
        ("--auto-approve", "true"),
    ),
    "analyse_generale": (
        ("--thinking", "medium"),
        ("--auto-approve", "true"),
    ),
}


def construire_commande(
    intention: str,
    requete: str,
    resultat: ResultatReconnaissance,
    banque: Banque,
    cwd: Optional[str] = None,
) -> Optional[CommandeCline]:
    """Assemble l'AST de commande pour l'intention donnee.

    Retourne None si l'intention est inconnue (pas de gabarit) : le pipeline
    emettra alors un refus formel plutot que d'inventer des options.
    """
    gabarit = _GABARITS.get(intention)
    if gabarit is None:
        return None

    options: list[Tuple[str, Optional[str]]] = []
    if cwd is not None:
        options.append(("--cwd", cwd))
    options.extend(gabarit)

    # Le prompt est la requete normalisee rejointe (reproductible, sans bruit).
    prompt = rejoindre(normaliser(requete))
    return CommandeCline(
        executable="cline",
        sous_commande=None,
        options=tuple(options),
        arguments=(prompt,) if prompt else (),
    )
