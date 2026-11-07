"""
Enregistrement enrichi des sessions slow-motion pour meta-learning.

Capture :
  1. Timeline COMPLETE (T1-T8) avec DECISIONS prises à chaque étape
  2. Quels TOOLKIT ont été utilisés et COMMENT
  3. La STRATEGIE reformulation appliquée
  4. LESSONS LEARNED pour appliquer à des problèmes similaires
  5. SIGNATURE de l'incoherence pour matching futur
"""
from __future__ import annotations

import logging
import re
import uuid
from typing import Any, Optional

from ..core.spectral_types import FinalAnswer, QuestionContext
from ..learning.debugging_expertise import (
    CoherenceSignature,
    DebugSessionRecord,
    ReformulationStrategy,
    TimelineStep,
    ToolkitUsage,
    ExpertiseLibrary,
)
from ..multiloop.coherence_detector import CoherenceReport
from ..multiloop.slow_motion_debugger import DebugTimeline, SlowMotionDebugger
from ..multiloop.request_decomposer import DecomposedRequest


logger = logging.getLogger(__name__)


class SlowMotionRecorder:
    """
    Enregistre les sessions slow-motion pour meta-learning.
    
    A la fin d'une session, crée un DebugSessionRecord qui sera
    stocké en BD et consulté pour les prochaines sessions similaires.
    """
    
    def __init__(self, expertise_lib: Optional[ExpertiseLibrary] = None):
        self.expertise = expertise_lib or ExpertiseLibrary()
    
    async def record_session(
        self,
        original_question: str,
        debugger_result: FinalAnswer,
        coherence_report: CoherenceReport,
        decomposed: DecomposedRequest,
        timeline_events: list[dict],  # Les events du DebugTimeline
        toolkit_reports: Optional[dict[str, Any]] = None,
    ) -> DebugSessionRecord:
        """
        Crée un DebugSessionRecord à partir d'une session slow-motion.
        
        Args:
            original_question: la question posée par l'utilisateur
            debugger_result: la FinalAnswer produite par SlowMotionDebugger
            coherence_report: le rapport d'incoherence détecté
            decomposed: la décomposition de la requête
            timeline_events: les 8 étapes du timeline slow-motion
            toolkit_reports: rapports d'utilisation des outils (spectral_core, sympy, z3, etc.)
        
        Returns:
            DebugSessionRecord prêt à être stocké dans ExpertiseLibrary
        """
        session_id = f"dbg_{uuid.uuid4().hex[:8]}"
        timestamp = self._get_timestamp()
        
        # Extraire le pattern de la question
        question_pattern = self._extract_pattern(original_question)
        
        # Construire la signature d'incoherence
        coherence_sig = self._build_coherence_signature(coherence_report)
        
        # Construire les steps du timeline avec decisions
        timeline_steps = self._build_timeline_steps(timeline_events, toolkit_reports or {})
        
        # Extraire les usages des toolkits
        toolkit_usages = self._extract_toolkit_usages(toolkit_reports or {})
        
        # Construire la stratégie de reformulation
        reformulation = self._build_reformulation_strategy(decomposed, debugger_result)
        
        # Extraire les lessons learned
        lessons = self._extract_lessons(
            original_question,
            decomposed,
            coherence_report,
            debugger_result,
            toolkit_reports or {},
        )
        
        # Créer le record
        record = DebugSessionRecord(
            session_id=session_id,
            timestamp=timestamp,
            original_question=original_question,
            question_pattern=question_pattern,
            domain=self._infer_domain(decomposed),
            ratio_model=decomposed.detected_ratio or "1/2",
            coherence_signature=coherence_sig,
            coherence_score_before=coherence_report.score,
            timeline_steps=timeline_steps,
            toolkit_usages=toolkit_usages,
            reformulation_strategy=reformulation,
            reformulated_question=debugger_result.answer_text[:200],  # première phrase
            final_answer=debugger_result.answer_text,
            coherence_score_after=1.0,  # Après slow-motion, c'est certain
            success_validation=debugger_result.structured_data.get("validation", {}),
            lessons_learned=lessons,
            confidence=0.9,  # Haute confiance car slow-motion = kernel+spectral
        )
        
        # Ajouter à la bibliothèque
        self.expertise.add_session(record)
        
        logger.info(
            "Session enregistrée : id=%s, domain=%s, pattern=%s, lessons=%d",
            session_id, record.domain, question_pattern[:30], len(lessons),
        )
        
        return record
    
    def _extract_pattern(self, question: str) -> str:
        """
        Extrait un pattern regex de la question pour matching futur.
        
        Exemples :
          "Reconstruis le 18ème premier" → r"(\d+).*premier"
          "Quel est le rapport spectral entre (1,2,3) et (5,7,11)" → r"rapport.*\(\d+[,\d]*\).*\(\d+[,\d]*\)"
        """
        q_low = question.lower()
        
        # Pattern reconstruction
        if "premier" in q_low and any(kw in q_low for kw in ["eme", "ième", "position", "rang"]):
            return r"(?:reconstruis|quel.*premier|(\d+).*premier|position.*(\d+))"
        
        # Pattern ratio
        if "rapport" in q_low and ("spectral" in q_low or "(" in question):
            return r"rapport.*\(\d+[,\d]*\).*\(\d+[,\d]*\)"
        
        # Pattern gap
        if "ecart" in q_low and ("premiere" in q_low or "nombre" in q_low):
            return r"ecart.*(\d+).*(\d+)"
        
        # Fallback : keywords génériques
        keywords = re.findall(r"\b[a-z]{4,}\b", q_low)
        if keywords:
            return "|".join(keywords[:5])  # Top 5 keywords
        
        return r".*"
    
    def _build_coherence_signature(self, report: CoherenceReport) -> CoherenceSignature:
        """Construit une signature d'incoherence pour indexation."""
        # Inférer le type d'incoherence
        incoherence_type = "generic"
        if "contradiction" in report.signals:
            incoherence_type = "logical_contradiction"
        elif "mismatch" in report.signals:
            incoherence_type = "value_mismatch"
        elif "incomplete" in report.signals:
            incoherence_type = "incomplete_definition"
        
        return CoherenceSignature(
            incoherence_type=incoherence_type,
            affected_concepts=report.signals[:5],  # Top 5 signaux
            affected_sections=[],  # À remplir si info dispo
            severity=1.0 - report.score,  # Plus bas le score, plus grave
        )
    
    def _build_timeline_steps(
        self,
        timeline_events: list[dict],
        toolkit_reports: dict[str, Any],
    ) -> list[TimelineStep]:
        """Construit les steps du timeline avec decisions."""
        steps = []
        
        for i, event in enumerate(timeline_events, 1):
            # Décision prise à cette étape
            decision = self._infer_decision(event)
            
            # Outil utilisé si applicable
            toolkit_used = None
            if "spectral_core" in str(toolkit_reports) and i == 6:
                toolkit_used = ToolkitUsage(
                    toolkit_name="spectral_core",
                    operation="reconstruct_prime_1_2 or analyze_ratio",
                    input_values={},
                    output_values=toolkit_reports.get("spectral_core", {}),
                    success=True,
                    execution_time_ms=10.0,
                )
            
            step = TimelineStep(
                step=i,
                label=event.get("label", f"T{i}"),
                detail=event.get("detail", ""),
                decision_taken=decision,
                toolkit_used=toolkit_used,
            )
            steps.append(step)
        
        return steps
    
    def _infer_decision(self, event: dict) -> str:
        """Infère la décision Gabriel a pris à cette étape."""
        label = event.get("label", "").upper()
        detail = event.get("detail", "").lower()
        
        if label == "DECOMPOSITION":
            return "Décomposer la requête en segments logiques"
        elif label == "BYPASS_SEGMENTS":
            return "Identifier et ignorer segments incoherent"
        elif label == "REQUETE_CANONIQUE":
            return "Reconstruire une requête simplifiée"
        elif label == "RESOLUTION_CERTIFIEE":
            return "Résoudre via CertaintyKernel (pas LLM)"
        elif label == "REFORMULATIONS":
            return "Proposer reformulations alternatives"
        elif label == "REPONSE_CERTIFIEE":
            return "Générer réponse finale certaine"
        else:
            return f"Decision: {label[:50]}"
    
    def _extract_toolkit_usages(self, toolkit_reports: dict[str, Any]) -> list[ToolkitUsage]:
        """Extrait les usages des différents outils."""
        usages = []
        
        for tool_name, report in toolkit_reports.items():
            if tool_name == "spectral_core" and isinstance(report, dict):
                usages.append(ToolkitUsage(
                    toolkit_name="spectral_core",
                    operation=report.get("method", "analyze"),
                    input_values={"position": report.get("position"), "prime": report.get("p")},
                    output_values={"result": report.get("value")},
                    success=report.get("success", True),
                    execution_time_ms=report.get("exec_time", 5.0),
                ))
            elif tool_name == "z3" and isinstance(report, dict):
                usages.append(ToolkitUsage(
                    toolkit_name="z3",
                    operation=report.get("solver_type", "sat"),
                    input_values=report.get("constraints", {}),
                    output_values=report.get("solution", {}),
                    success=report.get("satisfiable", False),
                    execution_time_ms=report.get("exec_time", 10.0),
                ))
        
        return usages
    
    def _build_reformulation_strategy(
        self,
        decomposed: DecomposedRequest,
        result: FinalAnswer,
    ) -> Optional[ReformulationStrategy]:
        """Construit la stratégie de reformulation appliquée."""
        bypassed = [
            s.text for s in getattr(decomposed, "incoherent_segments", [])
        ]
        
        return ReformulationStrategy(
            segments_bypassed=bypassed,
            canonical_form=getattr(decomposed, "canonical_form", ""),
            decomposition_method="request_decomposer (regex + intent detection)",
            reconstruction_steps=[
                "T1: Recevoir requête",
                "T2: Décomposer en segments",
                "T3-T4: Identifier et by-passer incoherences",
                "T5: Reconstruire canonique",
                "T6: Résoudre via kernel (certain)",
                "T7-T8: Générer réponse + timeline",
            ],
            key_insight=self._extract_key_insight(result),
        )
    
    def _extract_key_insight(self, result: FinalAnswer) -> str:
        """Extrait la clé pour résoudre le problème (en 1 phrase)."""
        # Heuristique : chercher "INVARIANT", "clé", "secret", etc.
        text_low = (result.answer_text or "").lower()
        
        if "invariant" in text_low:
            # Extraire la phrase avec INVARIANT
            lines = result.answer_text.split("\n")
            for line in lines:
                if "invariant" in line.lower():
                    return line.strip()[:100]
        
        # Sinon : première phrase de la réponse
        sentences = result.answer_text.split(".")
        if sentences:
            return sentences[0][:100]
        
        return "Utiliser le CertaintyKernel pour certitude absolue"
    
    def _extract_lessons(
        self,
        question: str,
        decomposed: DecomposedRequest,
        coherence: CoherenceReport,
        result: FinalAnswer,
        toolkit_reports: dict[str, Any],
    ) -> list[str]:
        """
        Extrait les lessons learned de cette session.
        
        Ces leçons seront réutilisées pour les problèmes similaires.
        """
        lessons = []
        
        # Leçon 1 : Quel type d'incoherence nous avons rencontré
        if coherence.signals:
            lessons.append(f"Incoherence type '{coherence.signals[0]}' → résolvable par by-pass segments")
        
        # Leçon 2 : Quel toolkit était efficace
        if toolkit_reports.get("spectral_core"):
            lessons.append("spectral_core fournit certitude absolue (preferer au LLM)")
        if toolkit_reports.get("z3"):
            lessons.append("z3 peut valider contradictions logiques (utiliser pour coherence check)")
        
        # Leçon 3 : Pattern de la question
        if "premier" in question.lower():
            lessons.append("Questions sur 'N-ème premier' → invariant n = position (1/2 uniquement)")
        if "rapport" in question.lower():
            lessons.append("Questions sur 'rapport spectral' → configuration nxn vs 1x1 critique")
        
        # Leçon 4 : Stratégie générale
        lessons.append("Décomposer + by-pass incoherences + résoudre par kernel = certitude")
        lessons.append("Ne JAMAIS relancer LLM après slow-motion (elle invente)")
        
        return list(set(lessons))  # Déduplicate
    
    def _infer_domain(self, decomposed: DecomposedRequest) -> str:
        """Infère le domaine mathématique."""
        intent = getattr(decomposed, "detected_intent", "general")
        if intent == "reconstruction":
            return "spectral_reconstruction"
        elif intent == "ratio":
            return "spectral_ratio"
        elif intent == "gap":
            return "spectral_gap"
        else:
            return "general"
    
    def _get_timestamp(self) -> str:
        """Timestamp ISO."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()
    
    def get_expertise_for_question(self, question: str) -> Optional[ReformulationStrategy]:
        """
        Consulte la bibliothèque d'expertise pour une question.
        
        Si une stratégie similaire existe, l'agent peut l'appliquer
        AVANT de relancer le multiloop.
        """
        return self.expertise.get_reformulation_strategy_for_pattern(question)
