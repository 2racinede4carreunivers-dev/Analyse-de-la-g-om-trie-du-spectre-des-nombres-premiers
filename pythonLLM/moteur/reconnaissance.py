# -*- coding: utf-8 -*-
"""
moteur/reconnaissance.py — reconnaissance par appartenance ensembliste exacte.

Aucune approximation : un token de la requete est reconnu si et seulement si
son lemme appartient a l'ensemble ``banque.lemmes``. Les doublons sont
conserves pour le comptage mais la trace ne retient que les lemmes distincts,
dans l'ordre du corpus (ordre des champs par poids, puis ordre d'insertion).
"""
from __future__ import annotations

from typing import Tuple

from .banque import Banque
from .normalisation import normaliser
from ..modele.entites import Notion, ResultatReconnaissance


def reconnaitre(requete: str, banque: Banque) -> Tuple[Tuple[Notion, ...], ResultatReconnaissance]:
    """Retourne ``(notions_reconnues, resultat)``.

    ``notions_reconnues`` preserve l'ordre d'apparition des champs par poids,
    puis l'ordre des notions dans la base. ``resultat`` porte les lemmes
    distincts reconnus et le drapeau ``aucun_terme``.
    """
    tokens = normaliser(requete)
    ordre_champs = banque.champ_ordre()
    index_champ = {code: i for i, code in enumerate(ordre_champs)}

    # Ensemble des lemmes presents dans la requete (distincts).
    presents = {t for t in tokens if t in banque.lemmes}

    # Notions reconnues, triees de maniere deterministe.
    notions_triees = sorted(
        (banque.notions[l] for l in presents),
        key=lambda n: (index_champ.get(n.champ_code, 999), n.lemme),
    )
    lemmes_reconnus = tuple(n.lemme for n in notions_triees)
    resultat = ResultatReconnaissance(
        scores=(),  # renseigne par le module scoring
        termes_reconnus=lemmes_reconnus,
        aucun_terme=len(lemmes_reconnus) == 0,
    )
    return tuple(notions_triees), resultat
