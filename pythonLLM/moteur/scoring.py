# -*- coding: utf-8 -*-
"""
moteur/scoring.py — scoring exact par champ (arithmetique Fraction).

Le score d'un champ est la fraction (nb de notions reconnues du champ) /
(nb de notions total du champ). Aucun flottant : ``fractions.Fraction``
garantit une comparaison et un departage exacts (invariant INV-EXACTITUDE).
Les scores sont retournes dans l'ordre de poids des champs (ordre total), ce
qui rend le departage deterministe en cas d'egalite.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Dict, Tuple

from .banque import Banque
from ..modele.entites import Notion, ResultatReconnaissance


def calculer_scores(
    notions: Tuple[Notion, ...], banque: Banque, resultat: ResultatReconnaissance
) -> ResultatReconnaissance:
    """Renseigne ``resultat.scores`` et retourne un nouveau ResultatReconnaissance.

    Le denominateur par champ est le nombre total de notions de ce champ dans
    le corpus (normalisation par la taille du champ). Un champ absent de la
    requete a un score de 0.
    """
    # Compte des notions reconnues par champ.
    compte: Dict[str, int] = {}
    for n in notions:
        compte[n.champ_code] = compte.get(n.champ_code, 0) + 1

    # Taille de chaque champ dans le corpus.
    total_champ: Dict[str, int] = {}
    for n in banque.notions.values():
        total_champ[n.champ_code] = total_champ.get(n.champ_code, 0) + 1

    scores: list[Tuple[str, Fraction]] = []
    for code in banque.champ_ordre():  # ordre de poids croissant
        num = compte.get(code, 0)
        den = total_champ.get(code, 1)
        scores.append((code, Fraction(num, den)))

    return ResultatReconnaissance(
        scores=tuple(scores),
        termes_reconnus=resultat.termes_reconnus,
        aucun_terme=resultat.aucun_terme,
    )
