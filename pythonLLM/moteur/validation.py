# -*- coding: utf-8 -*-
"""
moteur/validation.py — validation grammaticale et deontique d'une commande.

Deux couches de verification, sans execution du code :

1. Grammaire (correspondance de Curry-Howard, invariant INV-CURRY-HOWARD) :
   chaque option appartient au registre, sa valeur appartient a son domaine
   (enum ferme, entier, booleen), et son arite (prend_valeur) est respectee.

2. Deontique (invariant INV-DEONTIQUE) : les exclusions mutuelles sont
   verifiees (ex. ``--tui`` vs ``--json``), ainsi que les obligations.

Retourne une liste de violations. Une liste vide == commande valide.
"""
from __future__ import annotations

from typing import List, Tuple

from .banque import Banque
from .grammaire import EXCLUSIONS, option_par_long, options_obligatoires
from ..modele.entites import CommandeCline


def valider_commande(commande: CommandeCline, banque: Banque) -> Tuple[str, ...]:
    """Retourne le tuple des codes de regle violes (vide si valide)."""
    violations: List[str] = []
    options_presentes = {nom for nom, _ in commande.options}

    # --- 1. Grammaire : existence, arite, domaine de valeurs ---
    for nom, valeur in commande.options:
        opt = option_par_long(nom)
        if opt is None:
            violations.append(f"GRAMMAIRE-OPTION-INCONNUE:{nom}")
            continue
        if opt.prend_valeur:
            if valeur is None:
                violations.append(f"GRAMMAIRE-VALEUR-MANQUANTE:{nom}")
                continue
            violations.extend(_valider_valeur(nom, valeur, opt.type))
        else:
            if valeur is not None:
                violations.append(f"GRAMMAIRE-VALEUR-INATTENDUE:{nom}")

    # Doublons d'options (une option ne doit pas apparaitre deux fois).
    vus = set()
    for nom, _ in commande.options:
        if nom in vus:
            violations.append(f"GRAMMAIRE-DOUBLON:{nom}")
        vus.add(nom)

    # --- 2. Deontique : exclusions mutuelles ---
    for a, b in EXCLUSIONS:
        if a in options_presentes and b in options_presentes:
            violations.append(f"DEONTIQUE-EXCLUSION:{a}|{b}")

    # --- 2b. Deontique : obligations ---
    for opt in options_obligatoires():
        if opt.long not in options_presentes:
            violations.append(f"DEONTIQUE-OBLIGATION:{opt.long}")

    return tuple(violations)


def _valider_valeur(nom: str, valeur: str, type_opt) -> List[str]:
    """Valide une valeur contre son TypeOption. Retourne les violations."""
    problems: List[str] = []
    if type_opt.nom == "enum" or type_opt.nom in ("booleen_valeur", "niveau_reflexion", "mode_compaction"):
        if valeur not in type_opt.enum_valeurs:
            problems.append(f"GRAMMAIRE-ENUM:{nom}:{valeur}")
    elif type_opt.nom == "entier":
        try:
            int(valeur)
        except ValueError:
            problems.append(f"GRAMMAIRE-ENTIER:{nom}:{valeur}")
    # chemin / texte : tout non vide est accepte (domaine large mais borne).
    elif type_opt.nom in ("chemin", "texte"):
        if valeur == "":
            problems.append(f"GRAMMAIRE-VIDE:{nom}")
    return problems
