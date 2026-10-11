"""
Silent Audit Loop : Garde-fou final anti-hallucination.

Apres le pipeline complet (5 moteurs + multi-loop), avant d'afficher la
reponse, on l'audite silencieusement contre la verite terrain spectrale.
Si une violation est detectee, on re-prompte le LLM avec un prompt correctif
injectant les valeurs correctes, jusqu'a max_retries.

Le tout est SILENCIEUX : aucun message d'erreur n'apparait a l'utilisateur,
seulement les tentatives sont loggees au niveau INFO/WARNING.
"""
from __future__ import annotations

import logging
from typing import Any

from ..core.llm_manager import LLMManager
from ..core.spectral_core import AntiHallucinationValidator
from ..core.spectral_types import FinalAnswer
from ..spectral.spectral_knowledge import build_grounded_system_prompt


logger = logging.getLogger(__name__)

GROUNDED_SYSTEM_PROMPT = build_grounded_system_prompt()


class SilentAuditLoop:
    """
    Boucle d'audit silencieux post-pipeline.
    
    Usage :
        audit = SilentAuditLoop(llm, config)
        final = await audit.audit_and_correct(question, final_answer, precomputed_facts)
    """

    def __init__(self, llm: LLMManager, config: dict[str, Any]):
        self.llm = llm
        self.validator = AntiHallucinationValidator()
        audit_cfg = config.get("audit", {}) if config else {}
        self.enabled = bool(audit_cfg.get("enabled", True))
        self.max_retries = int(audit_cfg.get("max_retries", 2))
        self.temperature = float(audit_cfg.get("temperature", 0.1))

    async def audit_and_correct(
        self,
        question: str,
        final: FinalAnswer,
        precomputed_facts: dict[str, Any] | None = None,
    ) -> FinalAnswer:
        """
        Audite la reponse finale et corrige silencieusement si necessaire.
        
        Args:
            question: La question utilisateur originale.
            final: La FinalAnswer produite par le pipeline.
            precomputed_facts: Les facts calcules par le module spectral
                              (utilises comme verite terrain prioritaire).
        
        Returns:
            FinalAnswer : soit l'originale (si valide), soit une version corrigee.
        """
        if not self.enabled:
            return final

        # Construire la verite terrain depuis les facts precomputes
        ground_truth = self._extract_ground_truth(precomputed_facts)

        for attempt in range(1, self.max_retries + 2):  # +2 : audit initial + N retries
            audit_result = self.validator.audit(
                question=question,
                answer=final.answer_text,
                ground_truth=ground_truth,
            )

            if audit_result["valid"]:
                if attempt > 1:
                    logger.info(
                        "[AUDIT] Reponse validee apres %d tentative(s) de correction.",
                        attempt - 1,
                    )
                else:
                    logger.debug("[AUDIT] Reponse validee au premier passage.")
                return final

            # Violation detectee
            if attempt > self.max_retries:
                # On a epuise les retries : log critique mais on retourne quand meme
                # (mieux qu'un crash ; le user verra la derniere version)
                logger.error(
                    "[AUDIT] Echec apres %d tentatives. Violations residuelles : %s",
                    self.max_retries,
                    audit_result["violations"],
                )
                # On annote le FinalAnswer pour traçabilite
                final.structured_data = dict(final.structured_data or {})
                final.structured_data["audit_failed"] = True
                final.structured_data["audit_violations"] = audit_result["violations"]
                return final

            logger.warning(
                "[AUDIT] Tentative %d/%d : violations = %s",
                attempt,
                self.max_retries,
                audit_result["violations"],
            )

            # Re-prompt silencieux
            corrected_text = await self._reprompt(
                question=question,
                previous_answer=final.answer_text,
                corrective_prompt=audit_result["corrective_prompt"],
                ground_truth=audit_result["ground_truth"],
            )

            if corrected_text:
                final.answer_text = corrected_text
                final.iterations_used = (final.iterations_used or 0) + 1
            else:
                # Re-prompt a echoue (LLM down) : sortir et retourner ce qu'on a
                logger.error("[AUDIT] Re-prompt LLM vide. Arret.")
                break

        return final

    @staticmethod
    def _extract_ground_truth(facts: dict[str, Any] | None) -> dict[str, Any] | None:
        """Extrait la verite terrain depuis les precomputed_facts."""
        if not facts:
            return None
        gt: dict[str, Any] = {}
        if "position" in facts:
            gt["position"] = facts["position"]
        if "prime" in facts or "p" in facts:
            gt["prime"] = facts.get("prime") or facts.get("p")
        if "n" in facts:
            gt["n"] = facts["n"]
        if "num_terms" in facts:
            gt["num_terms"] = facts["num_terms"]
        if "model" in facts:
            gt["ratio"] = facts["model"]
        return gt if gt else None

    async def _reprompt(
        self,
        question: str,
        previous_answer: str,
        corrective_prompt: str,
        ground_truth: dict[str, Any],
    ) -> str:
        """Demande au LLM une version corrigee, en injectant la verite terrain."""
        prompt = f"""{corrective_prompt}

Ta reponse precedente (a corriger) :
---
{previous_answer}
---

Produis maintenant la reponse corrigee, complete, factuelle, en francais.
"""
        try:
            text = await self.llm.generate(
                prompt,
                system=GROUNDED_SYSTEM_PROMPT,
                temperature=self.temperature,
            )
            return text or ""
        except Exception as exc:
            logger.error("[AUDIT] Erreur re-prompt LLM : %s", exc)
            return ""

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
