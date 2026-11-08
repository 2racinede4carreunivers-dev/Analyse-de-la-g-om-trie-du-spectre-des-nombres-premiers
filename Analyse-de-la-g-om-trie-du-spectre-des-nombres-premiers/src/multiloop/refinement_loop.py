"""
Boucle de raffinement multi-loop :
  1. Genere N candidats
  2. Critique chacun
  3. Si meilleur score < seuil, genere une nouvelle iteration avec critique en entree
  4. Repete jusqu'a max_iterations ou score >= seuil
  5. Retourne la meilleure reponse
"""
from __future__ import annotations

import logging
import json
from typing import Any, Callable

from ..core.llm_manager import LLMManager
from ..core.spectral_types import CandidateAnswer, FinalAnswer, QuestionContext
from ..spectral.spectral_knowledge import build_grounded_system_prompt
from ..spectral.direct_answer_guard import (
    DIRECT_ANSWER_RETRY_INSTRUCTION,
    is_non_answer,
    strip_meta_discourse,
)
from .critic import Critic


logger = logging.getLogger(__name__)


GROUNDED_SYSTEM_PROMPT = build_grounded_system_prompt()


REFINEMENT_INSTRUCTION = """Voici la critique constructive de ta reponse precedente :
---
{critique}
---
Score precedent : {score}/10.

Ameliore ta reponse en tenant compte de ces remarques.
RAPPEL CRITIQUE : utilise UNIQUEMENT les chiffres calcules fournis, n'invente RIEN.
Reste bienveillant et ne dis JAMAIS que la methode est incoherente."""


class RefinementLoop:
    """Boucle multi-loop avec self-critique."""

    def __init__(self, llm: LLMManager, critic: Critic, config: dict[str, Any]):
        self.llm = llm
        self.critic = critic
        ml_cfg = config.get("multiloop", {})
        self.max_iterations = int(ml_cfg.get("max_iterations", 3))
        self.min_score = float(ml_cfg.get("min_acceptance_score", 8.0))
        self.num_candidates = int(ml_cfg.get("num_candidates_per_round", 2))

    async def run(
        self,
        ctx: QuestionContext,
        precomputed_facts: dict[str, Any] | None = None,
        base_prompt: str | None = None,
        progress_cb: Callable[[dict[str, Any]], None] | None = None,
        max_iterations_override: int | None = None,
        num_candidates_override: int | None = None,
        skip_critique: bool = False,
    ) -> FinalAnswer:
        """Execute la boucle multi-loop et retourne la meilleure reponse.

        Si ``max_iterations_override`` est fourni (>=1), il remplace la valeur
        configuree ``self.max_iterations`` uniquement pour cet appel. Cela
        permet au PreReasoner d'imposer 1/2/3/4 iterations selon la nature
        de la requete.
        """
        all_candidates: list[CandidateAnswer] = []
        best: CandidateAnswer | None = None
        last_critique: str = ""

        # Nombre d'iterations effectif (override du PreReasoner ou config)
        if isinstance(max_iterations_override, int) and max_iterations_override >= 1:
            effective_max = max_iterations_override
        else:
            effective_max = self.max_iterations
        if isinstance(num_candidates_override, int) and num_candidates_override >= 1:
            effective_candidates = num_candidates_override
        else:
            effective_candidates = self.num_candidates

        for iteration in range(1, effective_max + 1):
            logger.info("=== Multi-loop iteration %d/%d ===", iteration, effective_max)
            if progress_cb:
                progress_cb({
                    "event": "multiloop_iteration_start",
                    "iteration": iteration,
                    "max_iterations": effective_max,
                })
            round_candidates = []
            for cand_idx in range(effective_candidates):
                prompt = self._build_prompt(ctx, precomputed_facts, base_prompt, last_critique, iteration)
                # Temperature un peu plus haute pour diversifier les candidats
                temp = 0.2 + 0.1 * cand_idx
                text = await self.llm.generate(
                    prompt,
                    system=GROUNDED_SYSTEM_PROMPT,
                    temperature=temp,
                    include_conversation=True,
                )
                # Reponse directe obligatoire : si le LLM n'a produit qu'un
                # preambule (salutation, auto-presentation, enumeration de
                # capacites, demande de precision), on regenere une fois avec
                # une consigne corrective, puis on retire tout preambule.
                if text and not text.startswith("[ERREUR LLM]") and is_non_answer(text):
                    logger.warning("Reponse sans contenu (preambule seul) -> regeneration directe")
                    retry = await self.llm.generate(
                        prompt + "\n\n" + DIRECT_ANSWER_RETRY_INSTRUCTION,
                        system=GROUNDED_SYSTEM_PROMPT,
                        temperature=temp,
                        include_conversation=True,
                    )
                    if retry and not retry.startswith("[ERREUR LLM]"):
                        text = retry
                if text and not text.startswith("[ERREUR LLM]"):
                    text = strip_meta_discourse(text) or text
                cand = CandidateAnswer(
                    iteration=iteration,
                    text=text or "[Vide]",
                    structured_data=precomputed_facts or {},
                    used_engines=["llm", "multiloop"],
                )
                if cand.text.startswith("[ERREUR LLM]"):
                    cand.structured_data["llm_error"] = True
                    cand.critique = "La génération a échoué; aucune critique ni nouvelle tentative n'a été lancée."
                    all_candidates.append(cand)
                    if progress_cb:
                        progress_cb({
                            "event": "multiloop_candidate_scored",
                            "iteration": iteration,
                            "candidate": cand_idx + 1,
                            "num_candidates": effective_candidates,
                            "score": 0.0,
                        })
                    return FinalAnswer(
                        question_id=ctx.question_id,
                        answer_text=cand.text,
                        structured_data=cand.structured_data,
                        confidence=0.0,
                        iterations_used=iteration,
                        best_score=0.0,
                        candidates=all_candidates,
                        explanation=cand.critique,
                    )
                if skip_critique:
                    cand.critique = (
                        "Critique omise pour réduire la latence du mode verbal; "
                        "réponse non vérifiée indépendamment."
                    )
                    cand.used_engines.append("critique_skipped")
                else:
                    cand = await self.critic.critique(cand, ctx, precomputed_facts)
                round_candidates.append(cand)
                all_candidates.append(cand)
                if progress_cb:
                    progress_cb({
                        "event": "multiloop_candidate_scored",
                        "iteration": iteration,
                        "candidate": cand_idx + 1,
                        "num_candidates": effective_candidates,
                        "score": cand.score,
                    })

            # Selection du meilleur du tour
            round_best = max(round_candidates, key=lambda c: c.score)
            if best is None or round_best.score > best.score:
                best = round_best
            last_critique = round_best.critique

            if progress_cb:
                progress_cb({
                    "event": "multiloop_iteration_end",
                    "iteration": iteration,
                    "best_score": best.score if best else 0.0,
                })

            # Arret si score suffisant
            if best.score >= self.min_score:
                logger.info("Score suffisant (%.1f >= %.1f). Arret.", best.score, self.min_score)
                if progress_cb:
                    progress_cb({
                        "event": "multiloop_early_stop",
                        "iteration": iteration,
                        "best_score": best.score,
                        "threshold": self.min_score,
                    })
                break

        assert best is not None
        return FinalAnswer(
            question_id=ctx.question_id,
            answer_text=best.text,
            structured_data={
                **best.structured_data,
                "critique_skipped": skip_critique,
            },
            confidence=best.score / 10.0,
            iterations_used=best.iteration,
            best_score=best.score,
            candidates=all_candidates,
            explanation=best.critique,
        )

    def _build_prompt(
        self,
        ctx: QuestionContext,
        facts: dict[str, Any] | None,
        base_prompt: str | None,
        last_critique: str,
        iteration: int,
    ) -> str:
        parts: list[str] = []
        if base_prompt:
            parts.append(base_prompt)
        parts.append(f"QUESTION DE L'UTILISATEUR :\n{ctx.raw_question}\n")
        if facts:
            parts.append(
                "CHIFFRES CALCULES (a utiliser textuellement) :\n"
                + json.dumps(facts, ensure_ascii=False, default=str, indent=2)
            )
        if iteration > 1 and last_critique:
            parts.append(REFINEMENT_INSTRUCTION.format(critique=last_critique, score="precedent"))
        parts.append(
            "\nReponds en francais, de maniere structuree et complete. "
            "Commence directement par le contenu demande : aucune salutation, "
            "aucune presentation de toi-meme, aucune enumeration de tes "
            "capacites, aucune reformulation de la question, aucune demande "
            "de precision, aucune offre finale. Traite chaque element demande."
        )
        return "\n\n".join(parts)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
