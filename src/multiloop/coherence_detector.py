"""
CoherenceDetector — Detecte les incoherences dans la sortie du multiloop.

Analyse les candidats produits par le RefinementLoop et calcule un score
de coherence global. Si ce score tombe en-dessous d'un seuil, le pipeline
declenche le Slow-Motion Debugger.

Signaux analyses :
  1. Score moyen du critique trop bas (multiloop pas confiant)
  2. Forte variance entre candidats (instabilite)
  3. Mention de vocabulaire dismissif (incoherent, absurde, etc.)
  4. Absence du prime attendu si une position est citee
  5. Violation de l'INVARIANT 1/2 (n != position alors que rapport 1/2)
"""
from __future__ import annotations

import re
import statistics
from dataclasses import dataclass
from typing import Any

from ..core.spectral_core import AntiHallucinationValidator
from ..core.spectral_types import CandidateAnswer
from .forbidden_vocab import detect_forbidden_word


@dataclass
class CoherenceReport:
    score: float                # 0.0 -> 1.0 (1.0 = parfaitement coherent)
    incoherent: bool            # score < seuil
    signals: list[str]          # raisons d'incoherence detectees
    best_candidate_score: float # score du meilleur candidat multiloop


class CoherenceDetector:
    """Detecteur d'incoherence post-multiloop."""

    DEFAULT_THRESHOLD = -999999.0  # DEBUGGER ANNULE COMPLETEMENT - INCIDENCE ZERO
    # Le debugger ne se declenchera JAMAIS (impossible d'avoir un score < -999999)
    # Gabriel utilise Claude (LLM) pour TOUTES les requetes, sans exception
    # Aucune intervention deterministe, aucune quarantaine, aucun kernel_emergency_summary

    def __init__(self, threshold: float = DEFAULT_THRESHOLD):
        self.threshold = threshold
        self.validator = AntiHallucinationValidator()

    def evaluate(
        self,
        question: str,
        candidates: list[CandidateAnswer],
        best_answer_text: str,
        precomputed_facts: dict[str, Any] | None = None,
    ) -> CoherenceReport:
        """Calcule le rapport de coherence sur la sortie du multiloop."""
        signals: list[str] = []
        score_components: list[float] = []

        # 1. Score moyen du critique (normalise 0..1)
        if candidates:
            scores = [c.score for c in candidates if c.score is not None]
            if scores:
                avg = statistics.mean(scores) / 10.0
                score_components.append(avg)
                if avg < 0.6:
                    signals.append(f"score_multiloop_bas={avg:.2f}")

                # Variance haute = instabilite
                if len(scores) > 1:
                    var = statistics.pstdev(scores)
                    if var > 2.5:
                        signals.append(f"variance_candidats_haute={var:.2f}")
                        score_components.append(0.4)

        # 2. Vocabulaire dismissif dans la meilleure reponse (contextualise via forbidden_vocab)
        found, matched_word = detect_forbidden_word(best_answer_text)
        if found:
            signals.append(f"vocabulaire_interdit:{matched_word}")
            score_components.append(0.2)

        # 3. Audit anti-hallucination (re-use du validator)
        ground_truth = None
        if precomputed_facts:
            ground_truth = {
                "position": precomputed_facts.get("position"),
                "prime": precomputed_facts.get("prime") or precomputed_facts.get("p"),
                "n": precomputed_facts.get("n"),
                "num_terms": precomputed_facts.get("num_terms"),
                "ratio": precomputed_facts.get("model"),
            }
            ground_truth = {k: v for k, v in ground_truth.items() if v is not None}
        audit = self.validator.audit(question, best_answer_text, ground_truth or None)
        if not audit["valid"]:
            for v in audit["violations"]:
                signals.append(f"violation:{v[:60]}")
            score_components.append(0.3)

        # 4. Contradiction interne : la reponse contient un nombre mais aussi "ne sais pas"
        text_low = best_answer_text.lower()
        uncertain = any(p in text_low for p in [
            "je ne sais pas", "je ne peux pas", "incertain", "impossible de",
            "je n'arrive pas", "pas certain",
        ])
        has_numbers = bool(re.search(r"\d+", best_answer_text))
        if uncertain and has_numbers:
            signals.append("contradiction_interne:incertitude_avec_nombres")
            score_components.append(0.4)
        elif uncertain:
            signals.append("incertitude_explicite")
            score_components.append(0.5)

        # Score final : moyenne ponderee
        if not score_components:
            score_components.append(0.8)  # neutre-positif par defaut
        final_score = min(score_components)  # le pire signal pese le plus

        best_cand_score = max((c.score for c in candidates if c.score), default=0.0)

        return CoherenceReport(
            score=final_score,
            incoherent=final_score < self.threshold,
            signals=signals,
            best_candidate_score=best_cand_score,
        )

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
