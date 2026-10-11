"""
Moteur de Meta-raisonnement (PROFOND).

Selectionne la strategie selon l'intent detecte :
  - reconstruction -> module spectral.reconstructor
  - ratio          -> module spectral.ratios
  - gap            -> module spectral.gaps
  - riemann_link   -> explication conceptuelle via LLM grounded sur corpus
  - general        -> reponse LLM grounded
"""
from __future__ import annotations

import logging
from typing import Any

from ...core.spectral_types import PipelineStep, QuestionContext, SpectralModel


logger = logging.getLogger(__name__)


STRATEGY_BY_INTENT = {
    "reconstruction": "spectral_reconstruction",
    "ratio": "spectral_ratio_compute",
    "gap": "spectral_gap_compute",
    "riemann_link": "explain_riemann_concordance",
    "general": "llm_grounded_response",
}


class GoalAnalyzer:
    """Analyse l'objectif de la question."""

    def analyze(self, ctx: QuestionContext) -> dict[str, Any]:
        intent = ctx.metadata.get("intent", "general")
        numbers = ctx.metadata.get("numbers_mentioned", [])
        return {
            "intent": intent,
            "needs_computation": intent in {"reconstruction", "ratio", "gap"},
            "needs_llm_explanation": True,
            "needs_hol_generation": intent in {"reconstruction"},
            "model": ctx.detected_model,
            "numbers": numbers,
        }


class StrategySelector:
    """Selectionne la strategie d'execution."""

    def select(self, ctx: QuestionContext, goal: dict[str, Any]) -> dict[str, Any]:
        intent = goal["intent"]
        strategy_name = STRATEGY_BY_INTENT.get(intent, "llm_grounded_response")
        pipeline_steps = [PipelineStep.ABSTRACTION, PipelineStep.META_REASONING]
        if goal["needs_computation"]:
            pipeline_steps.append(PipelineStep.CONCEPT_NAVIGATION)
        pipeline_steps.append(PipelineStep.GENERALIZATION)
        if goal["needs_hol_generation"]:
            pipeline_steps.append(PipelineStep.HOL_GENERATION)
        pipeline_steps.append(PipelineStep.RESPONSE)

        logger.info("Strategie selectionnee : %s (intent=%s)", strategy_name, intent)
        return {
            "strategy": strategy_name,
            "pipeline_steps": [s.value for s in pipeline_steps],
            "default_model": ctx.detected_model.value if ctx.detected_model else "1/2",
        }


class ProofPlanner:
    """Planifie l'organisation de la preuve / explication mathematique."""

    def plan(self, ctx: QuestionContext, goal: dict[str, Any], strategy: dict[str, Any]) -> dict[str, Any]:
        plan = {
            "strategy": strategy["strategy"],
            "model": strategy["default_model"],
            "steps": [],
        }
        intent = goal["intent"]

        if intent == "reconstruction":
            plan["steps"] = [
                "Identifier n (nb termes dans A et B) et le modele spectral.",
                "Calculer SA(n) et SB(n) via les formules du corpus.",
                "Calculer digamma_calc(n, p) = SB(n) - factor * p.",
                "Verifier prime_equation(n, p) = (SB(n) - digamma_calc) / factor = p.",
                "Generer un fragment HOL de validation.",
                "Expliquer le resultat en francais.",
            ]
        elif intent == "ratio":
            plan["steps"] = [
                "Identifier les indices A et B fournis.",
                "Detecter automatiquement la configuration (1x1, n*n, asym ordonnee, asym chaotique).",
                "Selectionner le modele spectral (1/2, 1/3, 1/4) selon le contexte.",
                "Calculer le rapport spectral via les formules du corpus.",
                "Comparer avec la valeur attendue 1/k.",
                "Expliquer la configuration et le rapport obtenu.",
            ]
        elif intent == "gap":
            plan["steps"] = [
                "Identifier les deux premiers p_high et p_low.",
                "Detecter le cas (+,+), (-,-) ou (-,+).",
                "Determiner les valeurs spectrales : A_next, B_high, D_high, D_low.",
                "Appliquer gap_equation = (A_next - B_high + D_high - D_low) / factor.",
                "Verifier que le resultat egale p_low - p_high.",
                "Expliquer le sens du resultat (quantite d'entiers entre p_high et p_low).",
            ]
        elif intent == "riemann_link":
            plan["steps"] = [
                "Resumer la formule explicite de Riemann-von Mangoldt.",
                "Montrer la concordance avec le rapport spectral 1/2.",
                "Decrire le plan trifocal (FZg, HyRi, MsP).",
                "Conclure sur la condition geometrique HypR_demi_solFinal.",
            ]
        elif intent in {"epistemological", "conversation", "general"}:
            plan["steps"] = [
                "Verifier que la question reste DANS LE DOMAINE Savard "
                "(geometrie spectrale, theorie univers carre, RH, fonction zeta).",
                "Si HORS-DOMAINE : refuser poliment en une phrase et proposer "
                "un sujet spectral connexe.",
                "Si DANS LE DOMAINE : mener une conversation NUANCEE en employant "
                "le LEXIQUE TECHNIQUE Savard (RsP, suite A/B, digamma, plan trifocal, "
                "asymetrie ordonnee/chaotique, postulat spectral, etc.).",
                "Citer naturellement Riemann/Euler/Hilbert/Hardy/von Mangoldt si pertinent.",
                "Exprimer une OPINION mathematique informee si la question est "
                "epistemologique, en la marquant explicitement comme telle.",
                "Conclure en invitant Philippe a approfondir un point precis.",
            ]
        else:
            # Conversation libre / question hors des 3 intents techniques.
            # Garde-fou domaine + lexique technique injectes via le system prompt.
            plan["steps"] = [
                "Verifier que la question relève du domaine Savard (geometrie spectrale, "
                "theorie univers carre, RH, fonction zeta). Si HORS-DOMAINE, refuser poliment.",
                "Mener une conversation NUANCEE en s'appuyant sur le lexique technique "
                "Savard (RsP, suites A/B, digamma, plan trifocal, asymetrie, axiomes).",
                "Citer Riemann/Euler/Hilbert/Hardy/von Mangoldt si pertinent.",
                "Exprimer une opinion epistemologique informee si la question le demande, "
                "en la marquant comme telle ('mon intuition mathematique suggere...').",
                "Inviter Philippe a preciser ou approfondir.",
            ]
        return plan
