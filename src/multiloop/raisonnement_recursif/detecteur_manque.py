"""detecteur_manque.py - Declencheur du raisonnement recursif de l'agent fusionne.

Principe (encadre) : lorsqu'une requete est VALIDE (dans le sujet spectral, donc
autorisee par fiancee_guard) mais que le pipeline expert ne fournit pas le
necessaire pour y repondre, l'agent bascule en << auto-programmation >> : il
genere un patch de correction .json, l'applique dans une SANDBOX isolee (dry-run
par defaut), se verifie, et peut se rollback.

SECURITE :
  * desactive par defaut ; activation explicite via GABRIEL_RECURSIVE=1 ;
  * applique en sandbox, jamais dans le depot vivant ;
  * dry-run par defaut (GABRIEL_RECURSIVE_APPLY=1 pour ecriture reelle sandboxee).

ADDITIF : observe le pipeline, ne le modifie pas.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Optional

from .messages import MESSAGE_AUTOPROGRAMMATION
from .pipeline_auto_programmation import (
    PipelineAutoProgrammation,
    construire_contrat_squelette,
)

# Marqueurs d'un manque de connaissance dans une reponse du pipeline expert.
MARQUEURS_MANQUE = (
    "je ne sais pas", "je n'ai pas", "pas implemente", "pas encore implemente",
    "aucun ancrage", "non disponible", "impossible de repondre",
    "hors de ma portee", "je ne possede pas", "connaissance absente",
    "pas de fait", "sans fondement disponible",
)


@dataclass
class DiagnosticManque:
    manque: bool
    raison: str = ""
    indices: list[str] = field(default_factory=list)


def _recursif_actif() -> bool:
    return os.environ.get("GABRIEL_RECURSIVE", "0").strip().lower() in (
        "1", "true", "oui", "on", "yes",
    )


def _apply_reel() -> bool:
    return os.environ.get("GABRIEL_RECURSIVE_APPLY", "0").strip().lower() in (
        "1", "true", "oui", "on", "yes",
    )


def _texte_de(answer: Any) -> str:
    if answer is None:
        return ""
    if isinstance(answer, str):
        return answer
    for attr in ("text", "answer", "response", "content", "message"):
        val = getattr(answer, attr, None)
        if isinstance(val, str) and val.strip():
            return val
    return str(answer)


def detecter_manque(answer: Any) -> DiagnosticManque:
    """Detecte si la reponse du pipeline expert trahit un manque de connaissance."""
    texte = _texte_de(answer).strip()
    if not texte:
        return DiagnosticManque(True, "reponse vide ou absente")

    bas = texte.lower()
    indices = [m for m in MARQUEURS_MANQUE if m in bas]
    if indices:
        return DiagnosticManque(True, "marqueurs de manque detectes", indices)

    # FinalAnswer sans faits (facts) -> conjecture non etayee.
    facts = getattr(answer, "facts", None)
    if facts is not None and isinstance(facts, (list, tuple, dict)) and len(facts) == 0:
        return DiagnosticManque(True, "aucun fait (facts) fourni par le pipeline")

    certainty = getattr(answer, "certainty", None)
    cert_val = getattr(certainty, "value", certainty)
    if cert_val is not None and str(cert_val).upper() in {
        "CONJECTURE", "HORS_DOMAINE", "INCONNU",
    }:
        return DiagnosticManque(True, f"certitude faible ({cert_val})")

    return DiagnosticManque(False, "connaissance suffisante")


def tenter_raisonnement_recursif(
    question: str,
    answer: Any = None,
    role: Optional[str] = None,
    mots_cles: Optional[list[str]] = None,
    sandbox_root: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Tente une auto-programmation encadree si un manque est detecte.

    Retourne un dict {message, diagnostic, rapport} si la boucle est declenchee,
    sinon None (aucun manque, ou fonctionnalite desactivee).
    """
    diag = detecter_manque(answer)
    if not diag.manque:
        return None

    if not _recursif_actif():
        return {
            "message": MESSAGE_AUTOPROGRAMMATION,
            "diagnostic": diag,
            "rapport": None,
            "etat": "desactive (GABRIEL_RECURSIVE=0)",
        }

    # Patch squelette : cible volontairement non destructive (fichier neuf en sandbox).
    op = {
        "op": "creer_fichier",
        "cible": "auto_extension_spectrale.py",
        "contenu": (
            "# Auto-extension generee par le raisonnement recursif (sandbox)\n"
            f"# Requete : {question[:200]!r}\n"
            "def extension_spectrale():\n"
            "    return {'statut': 'a_completer', 'sujet': 'spectre des nombres premiers'}\n"
        ),
    }
    contrat = construire_contrat_squelette(
        role=role or "spectral",
        mots_cles=mots_cles or ["spectre", "nombre premier", "reconstruction"],
        operation=op,
        description=f"Auto-programmation pour : {question[:160]}",
    )
    moteur = PipelineAutoProgrammation(
        sandbox_root=sandbox_root, dry_run=not _apply_reel(),
    )
    rapport = moteur.appliquer_contrat(contrat)
    return {
        "message": MESSAGE_AUTOPROGRAMMATION,
        "diagnostic": diag,
        "rapport": rapport,
        "etat": "applique (sandbox)",
    }


__all__ = ["DiagnosticManque", "detecter_manque", "tenter_raisonnement_recursif"]