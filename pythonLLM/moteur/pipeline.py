# -*- coding: utf-8 -*-
"""
moteur/pipeline.py — orchestration du pipeline computationnaliste.

Enchainement deterministe, trace a chaque etape :

    normalisation -> reconnaissance (appartenance) -> scoring exact
    -> classification d'intention (regles ordonnees) -> construction (AST)
    -> validation (grammaire + deontique) -> emission.

Tout au long, le pipeline n'invente jamais : si une etape echoue, un
RefusFormel justifie est produit. La trace SHA-256 est toujours renseignee.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from .banque import Banque
from .construction import construire_commande
from .intention import classer_intention
from .normalisation import normaliser, rejoindre
from .reconnaissance import reconnaitre
from .scoring import calculer_scores
from .trace import Tracer
from .validation import valider_commande
from ..modele.entites import (
    RefusFormel,
    ResultatPipeline,
)


def executer_pipeline(
    requete: str,
    banque: Optional[Banque] = None,
    cwd: Optional[str] = None,
    tracer: Optional[Tracer] = None,
) -> ResultatPipeline:
    """Execute une traversee complete et retourne un ResultatPipeline trace."""
    banque = banque or Banque()
    tracer = tracer or Tracer()

    # --- Etape 1 : normalisation ---
    tokens = normaliser(requete)
    tracer.ajouter("normalisation", rejoindre(tokens) if tokens else "(vide)")

    # --- Etape 2 : reconnaissance (appartenance ensembliste) ---
    notions, resultat = reconnaitre(requete, banque)
    tracer.ajouter("reconnaissance", ",".join(resultat.termes_reconnus) or "(aucun)")

    # Refus si aucun terme reconnu : le corpus ne couvre pas la requete.
    if resultat.aucun_terme:
        refus = RefusFormel(
            motif="aucun terme de la requete n'appartient au corpus normatif ; "
                  "refus d'inventer une commande hors cadre formel.",
            etape="reconnaissance",
        )
        tracer.ajouter("refus", refus.motif)
        return ResultatPipeline(
            requete=requete, intention=None, reconnaissance=resultat,
            commande=None, refus=refus, trace=tracer.etapes(), argv=(),
        )

    # --- Etape 3 : scoring exact ---
    resultat = calculer_scores(notions, banque, resultat)
    dominant = resultat.champ_dominant() or "?"
    tracer.ajouter("scoring", f"dominant={dominant}")

    # --- Etape 4 : classification d'intention (regles ordonnees) ---
    lemmes_requete = frozenset(t for t in tokens if t in banque.lemmes)
    intention = classer_intention(resultat, banque, lemmes_requete)
    tracer.ajouter("intention", intention or "(aucune)")
    if intention is None:
        refus = RefusFormel(
            motif="aucune regle d'intention ordonnee ne s'applique ; "
                  "classification indeterminee, refus d'inventer.",
            etape="intention",
        )
        tracer.ajouter("refus", refus.motif)
        return ResultatPipeline(
            requete=requete, intention=None, reconnaissance=resultat,
            commande=None, refus=refus, trace=tracer.etapes(), argv=(),
        )

    # --- Etape 5 : construction de l'AST ---
    commande = construire_commande(intention, requete, resultat, banque, cwd=cwd)
    tracer.ajouter("construction", " ".join(commande.argv()) if commande else "(echec)")
    if commande is None:
        refus = RefusFormel(
            motif=f"aucun gabarit valide pour l'intention '{intention}'.",
            etape="construction",
        )
        tracer.ajouter("refus", refus.motif)
        return ResultatPipeline(
            requete=requete, intention=intention, reconnaissance=resultat,
            commande=None, refus=refus, trace=tracer.etapes(), argv=(),
        )

    # --- Etape 6 : validation (grammaire + deontique) ---
    violations = valider_commande(commande, banque)
    tracer.ajouter("validation", ";".join(violations) if violations else "OK")
    if violations:
        refus = RefusFormel(
            motif="commande invalide au regard de la grammaire ou de la deontologie.",
            etape="validation",
            invariants=violations,
        )
        tracer.ajouter("refus", refus.motif)
        return ResultatPipeline(
            requete=requete, intention=intention, reconnaissance=resultat,
            commande=None, refus=refus, trace=tracer.etapes(), argv=(),
        )

    # --- Succes ---
    return ResultatPipeline(
        requete=requete, intention=intention, reconnaissance=resultat,
        commande=commande, refus=None, trace=tracer.etapes(), argv=commande.argv(),
    )
