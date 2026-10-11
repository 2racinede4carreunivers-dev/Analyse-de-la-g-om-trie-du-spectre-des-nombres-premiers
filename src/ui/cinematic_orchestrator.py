"""
Orchestrateur: Analyse de Complexité + Affichage Cinématique Intégré.

Ce module unit:
  1. Analyseur de complexité → détecte nombre de loops optimal
  2. Affichage cinématique → montre chronomètre + progression
  3. Intégration avec Pipeline → injecte le progress_cb optimisé

Utilisation:
  ```python
  orchestrator = CinematicOrchestrator(pipeline)
  final_answer = await orchestrator.process(question)
  ```
"""
from __future__ import annotations

import logging
from typing import Optional, Any

from .complexity_analyzer import ComplexityAnalyzer, ResponseMode
from .cinematic_display import CinematicDisplay, CinematicProgressCallback

logger = logging.getLogger(__name__)


class CinematicOrchestrator:
    """Orchestre l'analyse + affichage cinématique pour une requête."""
    
    def __init__(self, pipeline: Any, verbose: bool = False):
        """
        Args:
            pipeline: L'instance Pipeline de Gabriel
            verbose: Si True, log les décisions de complexité
        """
        self.pipeline = pipeline
        self.analyzer = ComplexityAnalyzer()
        self.verbose = verbose
        self.last_profile = None
        self.last_display = None
    
    async def process(
        self,
        question: str,
        intent: Optional[str] = None,
        print_cinematic: bool = True,
    ) -> Any:
        """
        Traite une requête avec analyse de complexité + cinématique.
        
        Args:
            question: La question de l'utilisateur
            intent: Intent optionnel détecté (accélère l'analyse)
            print_cinematic: Si True, affiche le cinématique pendant le traitement
        
        Returns:
            FinalAnswer du pipeline
        """
        
        # 1. Analyser la complexité
        profile = self.analyzer.analyze(question, intent)
        self.last_profile = profile
        
        if self.verbose:
            logger.info(f"Complexité détectée: {profile.mode.value} "
                       f"({profile.num_loops} loops, score={profile.complexity_score:.1f})")
            logger.info(f"Facteurs: {', '.join(profile.factors)}")
            logger.info(f"Recommandation: {profile.recommendation}")
        
        # 2. Créer le CinematicDisplay
        display = CinematicDisplay(
            num_loops=profile.num_loops,
            estimated_duration_sec=profile.estimated_duration_sec,
        )
        self.last_display = display
        
        # 3. Afficher le header initial
        if print_cinematic:
            print("\n" + display.render_cinematic_header() + "\n")
        
        # 4. Créer le progress callback cinématique
        progress_callback = CinematicProgressCallback(display).on_progress
        
        # 5. Appeler le pipeline avec le callback
        try:
            final_answer = await self.pipeline.process(
                question,
                progress_cb=progress_callback,
            )
        except Exception as exc:
            logger.error(f"Pipeline error: {exc}")
            raise
        
        # 6. Afficher le résumé cinématique final
        if print_cinematic:
            display.state.current_stage = "done"
            print("\n" + display.display_cinematic() + "\n")
        
        # 7. Annoter la réponse avec les métadonnées de complexité
        if hasattr(final_answer, 'metadata'):
            final_answer.metadata = {
                **(final_answer.metadata or {}),
                "complexity_mode": profile.mode.value,
                "complexity_loops": profile.num_loops,
                "complexity_score": profile.complexity_score,
                "complexity_factors": profile.factors,
                "complexity_confidence": profile.confidence,
                "cinematic_elapsed_sec": display.state.elapsed_sec,
            }
        
        return final_answer
    
    def get_complexity_report(self) -> dict[str, Any]:
        """Retourne un rapport détaillé sur la dernière analyse."""
        if not self.last_profile:
            return {}
        
        profile = self.last_profile
        display = self.last_display
        
        report = {
            "mode": profile.mode.value,
            "num_loops": profile.num_loops,
            "confidence": profile.confidence,
            "complexity_score": profile.complexity_score,
            "factors": profile.factors,
            "recommendation": profile.recommendation,
            "can_use_fast_mode": profile.can_use_fast_mode,
        }
        
        if display:
            report["elapsed_sec"] = display.state.elapsed_sec
            report["progress_percent"] = display.state.progress_percent
            report["events_log"] = display.state.events_log
        
        return report
    
    def suggest_fast_alternative(self, question: str) -> Optional[str]:
        """Suggère un raccourci mode Rapide si possible."""
        return self.analyzer.suggest_fast_response(question)


# Utilitaire: Mode "Réponse Rapide" bypass
class FastModeBypass:
    """
    Bypasse le multiloop pour les questions triviales.
    
    Utilisation:
      ```python
      bypass = FastModeBypass()
      if fast_answer := bypass.try_fast_response(question):
          print(fast_answer)
          return  # Skip pipeline entièrement
      
      # Sinon, utiliser l'orchestrator normal
      orch = CinematicOrchestrator(pipeline)
      await orch.process(question)
      ```
    """
    
    FAST_PATTERNS: list[tuple[str, str]] = [
        (r"\b(?:qu'est[- ]?ce que|c'est quoi)\s+(?:gabriel|la methode)",
         "Gabriel est un agent multiloop basé sur la Méthode Spectrale de Philippe Thomas Savard."),
        (r"\b(?:le premier nombre premier|premier premier)\b",
         "Le premier nombre premier est 2."),
        (r"\b(?:le (?:2|deuxième|deuxi[eè]me)\s+(?:nombre\s+)?premier)\b",
         "Le deuxième nombre premier est 3."),
        (r"\b(?:le (?:3|troisi[eè]me)\s+(?:nombre\s+)?premier)\b",
         "Le troisième nombre premier est 5."),
        (r"\b(?:qu'est[- ]?ce qu'une position)\b",
         "La position est le rang d'un nombre premier dans la séquence ordonnée."),
        (r"\b(?:quels? sont? (?:les )?(?:premiers|premiers nombres))\b",
         "Les premiers nombres premiers sont: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ..."),
    ]

    @staticmethod
    def try_fast_response(question: str) -> Optional[str]:
        """Retourne une réponse rapide si le pattern correspond, sinon None."""
        import re
        q_low = question.lower()

        for pattern, response in FastModeBypass.FAST_PATTERNS:
            if re.search(pattern, q_low):
                return response

        return None
