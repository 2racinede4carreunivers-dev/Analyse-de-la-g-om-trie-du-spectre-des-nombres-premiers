"""
Déclencheur automatique de la 7ème loop (Slow-Motion Debugger).

Logique :
  1. Utilisateur pose une question Q1 → agent répond A1 (multiloop)
  2. Utilisateur détecte une incohérence et repose → détection automatique
  3. Agent reconnaît pattern de retour (question contient mots clés ou incohérence)
  4. Déclenche SlowMotionDebugger pour reformulation
  5. Offre à l'utilisateur de sauvegarder la timeline dans la DB

Commandes utilisateur déclenchant la 7ème loop :
  - "7eme loop" / "7e loop" / "septieme loop"
  - "debug" + description d'une incohérence
  - "slow-motion"
  - "troubleshoot"
  - "incoherence" / "incohérence"
"""
from __future__ import annotations

import logging
import re
from typing import Optional

from ..core.spectral_types import FinalAnswer, QuestionContext
from ..multiloop.coherence_detector import CoherenceDetector, CoherenceReport
from ..multiloop.slow_motion_debugger import SlowMotionDebugger, DebugTimeline


logger = logging.getLogger(__name__)


class SlowMotionTrigger:
    """Detecte et déclenche automatiquement la 7ème loop."""
    
    KEYWORDS_7_LOOP = {
        "7eme loop", "7e loop", "septieme loop", "7ième loop",
        "slow-motion", "slow motion", "debugger", "troubleshoot",
        "incoherence", "incohérence", "incohérent", "incoherent",
        "contradiction", "incompatible", "incomplet", "incomplete",
        "erreur", "erreur logique", "illogique", "absurde",
        "inconsistant", "inconsistance", "ne cohere pas",
        "faux lien", "mauvais lien", "disjonction logique",
    }
    
    PATTERNS_RETOUR = [
        r"(?:tu affirm|tu dis|tu rapport|ton rapport|tes données).*(?:incomp|incomp|contradict)",
        r"(?:le(?:s|ur).*?)(?:valeur|chiffre|nombre).*(?:ne match|ne correspond|incomp)",
        r"(?:dans|dans le|selon).*(?:fragment|script|thy|hol).*(?:erreur|faux|ne cohere)",
        r"(?:entre|entre la|entre ton).*(?:affirmation|equation|calcul|lemma).*(?:incohérence|contradiction)",
    ]
    
    def __init__(
        self,
        slow_motion_debugger: Optional[SlowMotionDebugger] = None,
        coherence_detector: Optional[CoherenceDetector] = None,
    ):
        self.debugger = slow_motion_debugger
        self.coherence = coherence_detector or CoherenceDetector()
        logger.info("SlowMotionTrigger initialized")
    
    def should_trigger_7_loop(self, question: str, previous_answer: Optional[FinalAnswer] = None) -> bool:
        """
        Detecte si la question actuelle demande de lancer la 7ème loop.
        
        Retourne True si :
          1. Question contient un mot-clé 7_LOOP
          2. OU question contient un pattern de retour + incohérence detectée précédemment
          3. OU coherence_detector signale une incoherence dans la reponse precedente
        """
        q_lower = question.lower()
        
        # Test 1 : keyword direct
        for kw in self.KEYWORDS_7_LOOP:
            if kw in q_lower:
                logger.info("7ème loop détectée : keyword '%s'", kw)
                return True
        
        # Test 2 : pattern de retour + reponse precedente incoherente
        if previous_answer is not None:
            for pattern in self.PATTERNS_RETOUR:
                if re.search(pattern, question, re.IGNORECASE):
                    logger.info("7ème loop détectée : pattern retour '%s'", pattern)
                    return True
        
        return False
    
    async def trigger(
        self,
        question: str,
        previous_answer: FinalAnswer,
        ctx: QuestionContext,
        precomputed_facts: dict | None = None,
    ) -> FinalAnswer:
        """
        Lance la 7ème loop (SlowMotionDebugger) sur demande.
        
        Args:
            question: la question déclenchant la 7ème loop
            previous_answer: la reponse precedente jugée incoherente
            ctx: contexte Question
            precomputed_facts: facts calcules pour la question precedente
        
        Returns:
            FinalAnswer reformulée par le debugger
        """
        if self.debugger is None:
            raise ValueError("SlowMotionDebugger non configur")
        
        logger.info("=== 7ème LOOP DECLENCHEE ===")
        logger.info("  Question precedente : %s", ctx.raw_question[:100])
        logger.info("  Incohérence detectée dans la reponse")
        
        # Evaluer la coherence de la reponse precedente
        coherence_report = self.coherence.evaluate(
            question=ctx.raw_question,
            candidates=previous_answer.candidates or [],
            best_answer_text=previous_answer.answer_text,
            precomputed_facts=precomputed_facts or {},
        )
        logger.info("  Coherence score : %.2f", coherence_report.score)
        logger.info("  Signals : %s", coherence_report.signals[:5])
        
        # Lancer le debugger
        reformulated = self.debugger.debug(
            question=ctx.raw_question,
            final=previous_answer,
            coherence_report=coherence_report,
            precomputed_facts=precomputed_facts,
            skip_auto_audit=False,  # AUTO-AUDIT activé
        )
        
        return reformulated
    
    def render_7_loop_help(self) -> str:
        """Affiche l'aide sur la 7ème loop."""
        return f"""
COMMANDES 7ème LOOP (Slow-Motion Debugger Troubleshooting)
────────────────────────────────────────────────────────────
La 7ème loop s'active automatiquement ou manuellement pour :
  • Décomposer une question complexe en segments logiques
  • Identifier les parties cohérentes vs incoherentes
  • By-passer les segments problematiques
  • Reformuler une requête canonique simplifiée
  • Résoudre via le CertaintyKernel (sans LLM)
  • Générer une réponse CERTAINE avec timeline tracée
  • Proposer des reformulations pour l'utilisateur

MOTS-CLÉS DÉCLENCHEURS :
{chr(10).join(f"  • {kw}" for kw in sorted(self.KEYWORDS_7_LOOP)[:10])}
  ... et {len(self.KEYWORDS_7_LOOP) - 10} autres

EXEMPLE :
  Philippe > [reçoit une reponse incohérente]
  Philippe > Incohérence detectée : ton fragment HOL dit 61.0 mais tu dis 847998.0
  Gabriel  > [7ème loop déclenche automatiquement]
  Gabriel  > [Timeline complète + reformulation proposée]
  Gabriel  > Acceptez-vous de sauvegarder cette solution dans la DB ? (oui/non)

VOIR AUSSI :
  debug "<question>"          Debugger manuel avec commentaires
  verifier <position>         Validation toolkit (sympy, z3, wolfram)
  valider <position>          Boucle Wolfram <-> Gabriel <-> Isabelle
  historique                  Audits sauvegardés
"""
