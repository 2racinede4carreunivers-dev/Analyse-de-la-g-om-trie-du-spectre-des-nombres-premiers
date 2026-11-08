# -*- coding: utf-8 -*-
"""
moteur/intention.py — classification d'intention par regles ordonnees.

Les regles sont evaluees dans l'ordre de priorite croissante (ordre total : la
base garantit l'unicite de la priorite). La premiere regle dont la condition
est satisfaite gagne. En cas d'absence de terme reconnu, on retient l'intention
neutre ``analyse_generale`` uniquement si la regle par defaut l'autorise ;
sinon ``None`` signale un futur refus (aucune invention).
"""
from __future__ import annotations

from typing import FrozenSet, Optional

from .banque import Banque
from ..modele.entites import ResultatReconnaissance

INTENTION_NEUTRE = "analyse_generale"


def classer_intention(
    resultat: ResultatReconnaissance, banque: Banque, lemmes_requete: FrozenSet[str]
) -> Optional[str]:
    """Retourne l'intention classee, ou None si aucune regle ne s'applique.

    ``lemmes_requete`` est l'ensemble des lemmes normalises presents dans la
    requete (deja reconnus ou non). Une regle s'active si :
      - son ``champ_requis`` a un score > 0, et
      - au moins un de ses ``mots_declencheurs`` est dans ``lemmes_requete``.
    La regle par defaut (champ_requis is None, aucun declencheur) capture toute
    requete ou au moins un terme du corpus est reconnu.
    """
    for regle in banque.regles:  # deja trie par priorite croissante
        if regle.champ_requis is None and not regle.mots_declencheurs:
            # Regle par defaut : ne s'applique que si un terme est reconnu.
            if not resultat.aucun_terme:
                return regle.intention
            continue
        # Condition de champ.
        if regle.champ_requis is not None:
            if resultat.score_champ(regle.champ_requis) == 0:
                continue
        # Condition de declencheur (appartenance ensembliste exacte).
        if regle.mots_declencheurs:
            if not any(m in lemmes_requete for m in regle.mots_declencheurs):
                continue
        return regle.intention
    return None
