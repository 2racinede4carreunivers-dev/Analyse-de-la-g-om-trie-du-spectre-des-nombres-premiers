"""
Intégration de la meta-learning dans le Pipeline.

Workflow :
  1. SlowMotionDebugger.debug() → FinalAnswer reformulée
  2. Demander utilisateur : "Acceptez-vous cette reformulation ?"
  3. Si OUI :
       a. Enregistrer session dans ExpertiseLibrary via SlowMotionRecorder
       b. Créer DebugSessionRecord avec lessons + timeline complète
       c. Sauvegarder en DB JSON (cumul permanent)
  4. Pour prochaines questions similaires :
       a. Chercher expertise.find_similar_sessions()
       b. Récupérer stratégie → appliquer AVANT multiloop
       c. Si réussi → augmenter confiance expertise
"""
from __future__ import annotations

import logging
from typing import Any, Optional

from ..core.spectral_types import FinalAnswer, QuestionContext
from ..learning.debugging_expertise import ExpertiseLibrary
from ..learning.slowmotion_recorder import SlowMotionRecorder
from ..multiloop.coherence_detector import CoherenceDetector, CoherenceReport
from ..multiloop.request_decomposer import DecomposedRequest
from ..multiloop.slow_motion_debugger import SlowMotionDebugger


logger = logging.getLogger(__name__)


class MetaLearningManager:
    """
    Gère la méta-apprentissage : enregistrement et réutilisation
    des stratégies de débogage.
    """
    
    def __init__(
        self,
        expertise_lib: Optional[ExpertiseLibrary] = None,
        slow_motion_recorder: Optional[SlowMotionRecorder] = None,
    ):
        self.expertise = expertise_lib or ExpertiseLibrary()
        self.recorder = slow_motion_recorder or SlowMotionRecorder(expertise_lib=self.expertise)
        logger.info("MetaLearningManager initialized")
    
    async def record_successful_debug_session(
        self,
        original_question: str,
        debugger_result: FinalAnswer,
        coherence_report: CoherenceReport,
        decomposed: DecomposedRequest,
        timeline_events: list[dict],
        toolkit_reports: Optional[dict[str, Any]] = None,
        user_validation: bool = True,
    ) -> str:
        """
        Enregistre une session de débogage réussie pour réutilisation future.
        
        Args:
            original_question: la question posée
            debugger_result: la réponse produite par SlowMotionDebugger
            coherence_report: le rapport d'incoherence détecté
            decomposed: la décomposition de la requête
            timeline_events: les événements du timeline T1-T8
            toolkit_reports: rapports des toolkits utilisés
            user_validation: l'utilisateur a accepté la reformulation ?
        
        Returns:
            session_id (pour tracking + citation)
        """
        if not user_validation:
            logger.info("Session non validée par utilisateur → non enregistrée")
            return ""
        
        record = await self.recorder.record_session(
            original_question=original_question,
            debugger_result=debugger_result,
            coherence_report=coherence_report,
            decomposed=decomposed,
            timeline_events=timeline_events,
            toolkit_reports=toolkit_reports,
        )
        
        logger.info(
            "Session meta-learning enregistrée : id=%s (archivée en DB pour réutilisation)",
            record.session_id,
        )
        return record.session_id
    
    def should_apply_previous_strategy(
        self,
        question: str,
        coherence_report: Optional[CoherenceReport] = None,
    ) -> bool:
        """
        Vérifie si une stratégie d'expertise similaire existe.
        
        Si oui, l'agent devrait l'appliquer AVANT de relancer
        le multiloop standard.
        """
        strategy = self.expertise.get_reformulation_strategy_for_pattern(question)
        return strategy is not None
    
    def apply_learned_strategy(
        self,
        question: str,
        previous_answer: FinalAnswer,
    ) -> Optional[FinalAnswer]:
        """
        Applique une stratégie de réparation apprise sur une question similaire.
        
        Returns:
            FinalAnswer reformulée si stratégie trouvée, None sinon
        """
        strategy = self.expertise.get_reformulation_strategy_for_pattern(question)
        if strategy is None:
            return None
        
        logger.info(
            "Appliquer stratégie apprise : segments_bypassed=%s, canonical=%s",
            strategy.segments_bypassed[:2], strategy.canonical_form[:50],
        )
        
        # Ici, on pourrait appliquer les étapes de la stratégie
        # en décomposant question → appliquant les mêmes étapes
        # que celles qui ont marché la fois précédente.
        # Pour l'instant : on signale seulement qu'une stratégie existe.
        
        return None  # A implémenter avec full strategy replay
    
    def get_expertise_summary(self) -> dict[str, Any]:
        """Retourne un résumé de l'expertise accumulée."""
        return self.expertise.export_summary()
    
    def get_lessons_for_context(self, domain: str = "", ratio_model: str = "") -> list[str]:
        """Récupère les leçons apprises pour un contexte spécifique."""
        return self.expertise.get_lessons_learned(domain=domain, ratio_model=ratio_model)


class PipelineWithMetaLearning:
    """
    Wrapper du Pipeline qui intègre la meta-learning.
    
    Ajoute la capture et réutilisation des stratégies slow-motion.
    """
    
    def __init__(self, base_pipeline):
        self.pipeline = base_pipeline
        self.meta_learning = MetaLearningManager()
    
    async def process_with_learning(
        self,
        question: str,
        previous_answer: Optional[FinalAnswer] = None,
        user_accepted_reformulation: bool = False,
        timeline_events: Optional[list[dict]] = None,
        toolkit_reports: Optional[dict[str, Any]] = None,
    ) -> FinalAnswer:
        """
        Processe une question en intégrant meta-learning.
        
        Flow :
          1. Consulter expertise → si stratégie existe, l'appliquer
          2. Sinon : pipeline normal
          3. Si slow-motion declenché ET utilisateur accepte :
             → enregistrer session pour expertise future
        """
        
        # Step 1 : Vérifier expertise
        if self.meta_learning.should_apply_previous_strategy(question):
            logger.info("Expertise trouvée → appliquer stratégie apprise")
            learned_answer = self.meta_learning.apply_learned_strategy(question, previous_answer or FinalAnswer(
                question_id="",
                answer_text="",
            ))
            if learned_answer:
                return learned_answer
        
        # Step 2 : Exécuter pipeline normal
        result = await self.pipeline.process(question, previous_answer)
        
        # Step 3 : Si slow-motion a été utilisé ET user valide
        if user_accepted_reformulation and result.structured_data.get("slow_motion_triggered"):
            # Extraire les infos pour enregistrement
            decomposed = DecomposedRequest(
                detected_intent=result.structured_data.get("decomposition", {}).get("intent"),
                detected_ratio=result.structured_data.get("decomposition", {}).get("ratio"),
            )
            
            coherence_report = CoherenceReport(
                score=result.structured_data.get("coherence_score", 0.5),
                incoherent=result.structured_data.get("coherence_score", 1.0) < 0.55,
                signals=result.structured_data.get("coherence_signals", []),
            )
            
            # Enregistrer la session
            session_id = await self.meta_learning.record_successful_debug_session(
                original_question=question,
                debugger_result=result,
                coherence_report=coherence_report,
                decomposed=decomposed,
                timeline_events=timeline_events or result.structured_data.get("debug_timeline", []),
                toolkit_reports=toolkit_reports,
                user_validation=user_accepted_reformulation,
            )
            
            # Ajouter session_id à la réponse
            result.structured_data["learning_session_id"] = session_id
        
        return result
