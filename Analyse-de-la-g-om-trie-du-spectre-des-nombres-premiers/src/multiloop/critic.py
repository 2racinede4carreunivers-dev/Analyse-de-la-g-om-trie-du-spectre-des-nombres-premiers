"""
Critique : evalue une reponse candidate.

L'agent se critique lui-meme selon plusieurs criteres :
  1. Grounded : reponse appuyee sur le corpus / calculs corrects ?
  2. Completude : reponse repond a la question posee ?
  3. Cohenrence : les chiffres mentionnes sont coherents ?
  4. Pedagogie : explication claire ?
"""
from __future__ import annotations

import logging
from typing import Any

from ..core.llm_manager import LLMManager
from ..core.spectral_types import CandidateAnswer, QuestionContext


logger = logging.getLogger(__name__)


CRITIQUE_SYSTEM_PROMPT = """Tu es un critique mathematique BIENVEILLANT, expert de la methode spectrale de Philippe Thomas Savard.
Tu evalues une reponse candidate selon ces criteres :

1. CORRECTION MATHEMATIQUE (0-3 pts) : les chiffres et formules sont-ils exacts ?
   IMPORTANT : la methode est MATHEMATIQUEMENT VALIDE. Si la reponse dit
   "la methode est incoherente / contradictoire / sans fondement", -3 pts automatique.
2. ANCRAGE CORPUS (0-3 pts) : la reponse s'appuie-t-elle sur les chiffres calcules
   fournis et sur les formules du corpus (SA, SB, digamma, RsP) ?
3. COMPLETUDE (0-2 pts) : repond-elle bien a la question, en explicitant le lien
   n = position du premier (rapport 1/2) vs n != position (autres rapports) ?
4. TON ET BIENVEILLANCE (0-2 pts) : reste-t-elle respectueuse de Philippe Thomas Savard
   et de sa methode ? Pas d'affirmations cassantes ni de "c'est faux/absurde".

Sortie OBLIGATOIRE au format :
SCORE: <X.Y>/10
ANALYSE: <bref diagnostic, ce qui va bien et ce qui peut etre ameliore>
AMELIORATIONS: <suggestions concretes pour la prochaine iteration>
"""


class Critic:
    """Critique self-pour la boucle d'auto-amelioration."""

    def __init__(self, llm: LLMManager):
        self.llm = llm

    async def critique(self, candidate: CandidateAnswer, ctx: QuestionContext, ground_truth: dict[str, Any] | None = None) -> CandidateAnswer:
        """Critique une reponse candidate et met a jour son score."""
        # Si on a des chiffres calcules directement (ground truth), on commence par verifier
        grounded_score = self._check_grounded(candidate, ground_truth)
        candidate.grounded = grounded_score >= 2.0

        # Critique LLM
        prompt = self._build_critique_prompt(candidate, ctx, ground_truth)
        raw = await self.llm.generate(prompt, system=CRITIQUE_SYSTEM_PROMPT, temperature=0.1)

        score, analysis = self._parse_critique(raw)

        # Combinaison : score LLM ajuste par grounded
        if not candidate.grounded and ground_truth:
            score = max(0.0, score - 2.0)

        candidate.score = score
        candidate.critique = analysis or raw or ""
        logger.info("Critique tour %d : score=%.1f grounded=%s", candidate.iteration, score, candidate.grounded)
        return candidate

    def _check_grounded(self, candidate: CandidateAnswer, ground_truth: dict[str, Any] | None) -> float:
        """Verifie si la reponse mentionne les chiffres calcules."""
        if not ground_truth:
            return 1.0
        score = 0.0
        text = candidate.text
        for key, val in ground_truth.items():
            if isinstance(val, (int, float)) and str(int(val) if float(val).is_integer() else val) in text:
                score += 0.5
        # Penalite pour vocabulaire problematique (l'agent ne doit JAMAIS
        # dire que LA METHODE est incoherente/absurde/sans fondement).
        #
        # Fix v3.24 : detection centralisee dans forbidden_vocab (partagee avec
        # coherence_detector.py et spectral_core.py pour eviter les regressions).
        from .forbidden_vocab import detect_forbidden
        found, matched = detect_forbidden(text)
        if found:
            score -= 1.5
            logger.warning(
                "Vocabulaire interdit detecte : '%s' (-1.5)", matched
            )
        return min(max(score, 0.0), 3.0)

    def _build_critique_prompt(self, candidate: CandidateAnswer, ctx: QuestionContext, ground_truth: dict[str, Any] | None) -> str:
        gt_str = ""
        if ground_truth:
            gt_lines = [f"  - {k} = {v}" for k, v in ground_truth.items() if isinstance(v, (int, float, str))]
            gt_str = "\n\nCHIFFRES DE REFERENCE (issus du calcul direct) :\n" + "\n".join(gt_lines)
        return f"""QUESTION POSEE :
{ctx.raw_question}

REPONSE CANDIDATE A EVALUER (iteration {candidate.iteration}) :
{candidate.text}
{gt_str}

Evalue cette reponse rigoureusement."""

    def _parse_critique(self, raw: str | None) -> tuple[float, str]:
        if not raw:
            return 5.0, "Aucune critique generee."
        import re
        score = 5.0
        m = re.search(r"SCORE\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10", raw, re.IGNORECASE)
        if m:
            score = min(10.0, max(0.0, float(m.group(1))))
        else:
            m2 = re.search(r"\b(\d+(?:\.\d+)?)\s*/\s*10\b", raw)
            if m2:
                score = float(m2.group(1))
        return score, raw
