"""Package 'memory' - Dictionnaire spectral et adaptateur cognitif RAG.

Ce package implemente le systeme RAG semantique de Gabriel v6.2 :
  - dictionnaire_spectral : 9 regimes mathematiques de Philippe Thomas Savard
  - adaptateur_cognitif_rag : detection regex + injection contexte dans prompt Claude
"""
from __future__ import annotations

from .dictionnaire_spectral import (
    DICTIONNAIRE_SPECTRAL,
    Regime,
    get_regime,
    list_regimes,
)
from .adaptateur_cognitif_rag import (
    AdaptateurCognitifSpectral,
    preparer_requete_avec_rag,
)

__all__ = [
    "DICTIONNAIRE_SPECTRAL",
    "Regime",
    "get_regime",
    "list_regimes",
    "AdaptateurCognitifSpectral",
    "preparer_requete_avec_rag",
]
