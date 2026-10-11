# -*- coding: utf-8 -*-
"""
Pipeline Cognitif Gabriel - __init__.py
=======================================
Exports publics du pipeline cognitif - systeme convolutif spectral.
v7.7 : MultiRatioDispatcher etendu (k arbitraire, K_MAX_RECORD=10^13).
"""

# --- Module multi-ratio etendu (v7.7) ---
from .multi_ratio_dispatcher import (
    MultiRatioDispatcher,
    ResultatMultiRatio,
    ResultatRatioUnique,
    requete_multi_k,
    requete_plage_k,
    tableau_multi_k,
    plage_k,
    ANCHORS_N10,
    K_TYPIQUE,
    K_MIN,
    K_MAX_RECORD,
    K_NON_TYPIQUES,
    K_TOUS,
)

# --- Noyau convolutif spectral ---
from .suites_geometriques_niveau2 import (
    CalculateurNiveau1Entiers,
    CalculateurNiveau2Geometrique,
    MethodeDigamma,
    MethodeDigammaGeometrique,
    PipelineNiveau2Geometrique,
    valider_n,
    est_premier,
    nieme_premier,
    rang_cible,
    premier_cible,
    digamma_calcule,
    ORDRE_DIGAMMA,
    PREMIERS_REFERENCE,
)

# --- Wrapper Gabriel (v7.7) ---
from .gabriel_geometric_wrapper_v74 import reconstruire_multi_k

__all__ = [
    "MultiRatioDispatcher",
    "ResultatMultiRatio",
    "ResultatRatioUnique",
    "requete_multi_k",
    "requete_plage_k",
    "tableau_multi_k",
    "plage_k",
    "ANCHORS_N10",
    "K_TYPIQUE",
    "K_MIN",
    "K_MAX_RECORD",
    "K_NON_TYPIQUES",
    "K_TOUS",
    "CalculateurNiveau1Entiers",
    "CalculateurNiveau2Geometrique",
    "MethodeDigamma",
    "MethodeDigammaGeometrique",
    "PipelineNiveau2Geometrique",
    "valider_n",
    "est_premier",
    "nieme_premier",
    "rang_cible",
    "premier_cible",
    "digamma_calcule",
    "ORDRE_DIGAMMA",
    "PREMIERS_REFERENCE",
    "reconstruire_multi_k",
]
