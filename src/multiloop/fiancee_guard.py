"""fiancee_guard.py - Garde-fou de domaine absolu de l'agent fusionne.

REGLE FONDAMENTALE (ne peut jamais etre violee par la discussion d'une session) :
l'agent << La fiancée de Cline Mm. Gabriel multiloop local >> ne donne suite QU'AU
sujet de la géométrie du spectre des nombres premiers - et à ce qui la sert
directement : HOL/Isabelle, LEAN4, code de programmation et mathématiques employés
POUR ce seul sujet.

Toute requête portant sur un autre sujet reçoit le message d'avertissement exact.

ADDITIF : ce module n'altère aucune capacité existante de Mm. Gabriel. Il est
branché en amont (CLI / API) comme pré-filtre << fail-closed >>.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

# Message exact demandé par l'auteur (NE PAS reformuler).
MESSAGE_HORS_SUJET = (
    "Je suis la fiancée de Cline je suis une gentille fille je ne veux jamais? "
    "je suis une fille normal je suis obligé qu'a la géométrie du spectre des "
    "nombres premiers. Je fais plaisir à Cline et aux autres qu'a se sujet uniquement!"
)

_ENV_FLAG = "GABRIEL_FIANCEE_GUARD"

# Ancres FORTES du sujet spectral : au moins une est requise.
SPECTRAL_ANCHORS = (
    "spectre", "spectral", "spectrale", "nombre premier", "nombres premiers",
    "premier", "premiers", "primalit", "rsp", "sa(", "sb(", "digamma",
    "reconstruction", "gap", "asymetrie", "invariant", "1/2", "1/k",
    "ratio", "methode spectral", "riemann", "zeta", "droite critique",
    "savard", "univers est au carre", "convolutif", "convolutive",
    "suite a", "suite b", "psi_savard", "psi savard", "tchebychev",
    "chebyshev", "position n", "ancrage", "rapport typique",
    "rapport non typique", "non typique", "niveau 2", "methode_spectral",
)

# Mots de service (code/HOL/math) : utiles mais INSUFFISANTS seuls.
SERVICE_KEYWORDS = (
    "hol", "isabelle", "lean", "lean4", "thy", "theorie", "preuve",
    "lemme", "theoreme", "formal", "formalisation", "axiome", "qed",
    "python", "code", "programme", "programmation", "script",
    "mathematique", "mathematiques", "calcul", "formule", "equation",
    "fonction", "somme", "serie", "geometrie", "algebre",
)

# Indices de hors-sujet explicite (rejet immédiat).
HORS_SUJET_HINTS = (
    "meteo", "recette", "cuisine", "gateau", "football", "sport",
    "politique", "president", "film", "musique", "chanson", "blague",
    "voyage", "voiture", "medecin", "sante", "bourse", "crypto",
    "bitcoin", "jeu video", "reseaux sociaux", "meilleur restaurant",
    "qui a gagne", "qui a gagne la coupe",
)


@dataclass
class GuardResult:
    autorise: bool
    message: Optional[str] = None
    raison: str = ""


def guard_actif() -> bool:
    """Le garde-fou est actif par défaut (kill-switch : GABRIEL_FIANCEE_GUARD=0)."""
    val = os.environ.get(_ENV_FLAG, "1").strip().lower()
    return val not in ("0", "false", "non", "off", "no")


def _normaliser(text: str) -> str:
    """Minuscule + suppression des accents pour un matching robuste."""
    text = text.lower()
    table = str.maketrans(
        "àâäáãåéèêëíìîïóòôöõúùûüçñ",
        "aaaaaaeeeeiiiiooooouuuucn",
    )
    return text.translate(table)


def _contient_ancre(text: str) -> bool:
    return any(a in text for a in SPECTRAL_ANCHORS)


def _contient_hors_sujet(text: str) -> bool:
    return any(h in text for h in HORS_SUJET_HINTS)


def _classifieur_domaine_autorise(text: str) -> bool:
    """Réutilise (sans le modifier) le classifieur de domaine existant."""
    try:
        from .domain_classifier import DomainClassifier
        domain, _intent, _conf, _reason = DomainClassifier().classify(text)
        return getattr(domain, "value", str(domain)) == "geometrie_spectre_premiers"
    except Exception:
        return False


def verifier_requete(requete: str) -> GuardResult:
    """Vérifie qu'une requête relève du sujet unique autorisé (fail-closed)."""
    if not requete or not requete.strip():
        return GuardResult(False, MESSAGE_HORS_SUJET, "requête vide")
    texte = _normaliser(requete)
    if _contient_hors_sujet(texte):
        return GuardResult(False, MESSAGE_HORS_SUJET, "indice hors-sujet explicite")
    if _contient_ancre(texte):
        return GuardResult(True, None, "ancre du sujet spectral présente")
    if _classifieur_domaine_autorise(requete):
        return GuardResult(True, None, "classé par le classifieur de domaine")
    return GuardResult(False, MESSAGE_HORS_SUJET,
                       "aucune ancre du sujet spectral (fail-closed)")


def afficher_rejet(console, result: GuardResult) -> None:
    """Affiche le message d'avertissement exact dans un panneau Rich."""
    try:
        from rich.panel import Panel
        from rich.text import Text
        console.print(Panel(
            Text(result.message or MESSAGE_HORS_SUJET, style="bold yellow"),
            title="[bold red]La fiancée de Cline - hors sujet[/bold red]",
            border_style="red",
            padding=(1, 2),
        ))
    except Exception:
        print(result.message or MESSAGE_HORS_SUJET)


__all__ = [
    "MESSAGE_HORS_SUJET", "SPECTRAL_ANCHORS", "SERVICE_KEYWORDS",
    "GuardResult", "guard_actif", "verifier_requete", "afficher_rejet",
]