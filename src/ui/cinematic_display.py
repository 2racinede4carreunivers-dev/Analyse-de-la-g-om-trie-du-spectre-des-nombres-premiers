"""
Affichage Cinématique pour Gabriel - Mode Réponse en Temps Réel.

Affiche:
  1. Le nombre de loops prévus
  2. Le chronomètre progressif
  3. Les étapes en cours
  4. La progression visuelle (barre + pourcentage)

Compatible avec Rich Console pour un affichage élégant.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable


class AnimationFrame(Enum):
    """Frames d'animation pour le spinner."""
    DOTS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    DASHES = ["−", "\\", "|", "/"]
    ARROW = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
    DOTS_SMOOTH = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]


@dataclass
class CinematicState:
    """État courant du mode cinématique."""
    num_loops_planned: int
    loop_current: int = 0
    iteration_current: int = 0
    start_time: float = 0.0
    
    # Étapes visibles à l'utilisateur
    current_step: str = "Initialisation..."
    current_stage: str = "abstraction"
    
    # Estimation
    estimated_duration_sec: int = 30
    
    # Événements
    events_log: list[str] = None
    
    def __post_init__(self):
        if self.events_log is None:
            self.events_log = []
        if self.start_time == 0.0:
            self.start_time = time.time()
    
    @property
    def elapsed_sec(self) -> float:
        """Temps écoulé en secondes."""
        return time.time() - self.start_time
    
    @property
    def progress_percent(self) -> int:
        """Progression en pourcentage (0-100)."""
        if self.estimated_duration_sec == 0:
            return 0
        return min(100, int((self.elapsed_sec / self.estimated_duration_sec) * 100))
    
    @property
    def remaining_sec(self) -> int:
        """Temps restant estimé."""
        return max(0, int(self.estimated_duration_sec - self.elapsed_sec))
    
    @property
    def formatted_time(self) -> str:
        """Format du temps: MM:SS"""
        elapsed = int(self.elapsed_sec)
        minutes = elapsed // 60
        seconds = elapsed % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    @property
    def formatted_remaining(self) -> str:
        """Format du temps restant: MM:SS"""
        remaining = self.remaining_sec
        minutes = remaining // 60
        seconds = remaining % 60
        return f"{minutes:02d}:{seconds:02d}"


class CinematicDisplay:
    """Gère l'affichage cinématique Rich en temps réel."""
    
    # Mapping étape interne -> label utilisateur
    STAGE_LABELS = {
        "abstraction": "📝 Abstraction contextuelle",
        "intent_hypotheses": "🎯 Analyse d'intention",
        "assumptions_detected": "⚠️ Hypothèses détectées",
        "meta_reasoning": "🧠 Méta-raisonnement",
        "navigation": "🗺️ Navigation conceptuelle",
        "spectral_compute": "⚡ Calcul spectral direct",
        "verification": "✔️ Vérification indépendante",
        "generalization": "📊 Généralisation",
        "multiloop_start": "🔄 Boucle multi-itération",
        "refinement": "✨ Raffinement de réponse",
        "silent_audit": "🛡️ Audit silencieux",
        "hol_generation": "📚 Génération HOL/Isabelle",
        "epistemic": "🏛️ Marquage épistémique",
        "auto_programmation": "💞 Cline s'occupe de sa fiancée (auto-programmation)",
        "moteur_recursif": "🧩 8e moteur : raisonnement récursif (divisions → question modeste → oracle)",
        "done": "✅ Terminé",
    }
    
    def __init__(self, num_loops: int, estimated_duration_sec: int = 30):
        self.state = CinematicState(
            num_loops_planned=num_loops,
            estimated_duration_sec=estimated_duration_sec,
        )
        self.console = None
        self.animation_index = 0
        self._try_import_rich()
    
    def _try_import_rich(self):
        """Import Rich Console si disponible."""
        try:
            from rich.console import Console
            self.console = Console()
        except ImportError:
            self.console = None
    
    def render_cinematic_header(self) -> str:
        """Rend le header cinématique avec nombre de loops + chronomètre."""
        
        header_lines = [
            "╔" + "═" * 58 + "╗",
            "║  GABRIEL - Mode Réponse Intelligente (Cinématique)        ║",
            "╠" + "═" * 58 + "╣",
        ]
        
        # Ligne 1: Nombre de loops
        loops_text = f"Loops prévues: {self.state.loop_current}/{self.state.num_loops_planned}"
        header_lines.append(f"║  {loops_text:<56}  ║")
        
        # Ligne 2: Chronomètre + progression
        time_text = f"⏱️ {self.state.formatted_time} / ~{self.state.formatted_remaining}"
        header_lines.append(f"║  {time_text:<56}  ║")
        
        # Ligne 3: Barre de progression
        progress_bar = self._render_progress_bar()
        header_lines.append(f"║  {progress_bar:<56}  ║")
        
        # Ligne 4: Étape actuelle
        stage_label = self.STAGE_LABELS.get(self.state.current_stage, self.state.current_stage)
        header_lines.append(f"║  {stage_label:<56}  ║")
        
        header_lines.append("╚" + "═" * 58 + "╝")
        
        return "\n".join(header_lines)
    
    def _render_progress_bar(self, width: int = 50) -> str:
        """Rend une barre de progression avec animation."""
        percent = self.state.progress_percent
        filled = int(width * percent / 100)
        empty = width - filled
        
        # Animation du spinner à droite
        spinner = AnimationFrame.DOTS.value
        spinner_char = spinner[self.animation_index % len(spinner)]
        self.animation_index += 1
        
        bar = (
            "[" +
            "█" * filled +
            "░" * empty +
            f"] {percent:3d}% {spinner_char}"
        )
        return bar
    
    def render_cinematic_body(self) -> str:
        """Rend le corps du rapport avec les étapes."""
        body_lines = [""]
        
        # Section des loops complétées
        if self.state.loop_current > 0:
            body_lines.append("📍 Loops complétées:")
            for i in range(1, self.state.loop_current + 1):
                body_lines.append(f"   ✓ Loop {i}/5 terminée")
        
        # Section des loops en cours
        if self.state.loop_current < self.state.num_loops_planned:
            body_lines.append(f"")
            body_lines.append(f"🔄 Loop {self.state.loop_current + 1}/{self.state.num_loops_planned} en cours...")
            body_lines.append(f"   Itération {self.state.iteration_current}/5")
        
        # Section des événements récents
        if self.state.events_log:
            body_lines.append("")
            body_lines.append("📝 Derniers événements:")
            for evt in self.state.events_log[-3:]:
                body_lines.append(f"   • {evt}")
        
        return "\n".join(body_lines)
    
    def update_from_progress_event(self, event: dict) -> None:
        """Met à jour l'état depuis un événement progress_cb."""
        
        event_type = event.get("event", "")
        
        # Mapping événement -> stage interne
        stage_map = {
            "abstraction_done": "abstraction",
            "intent_hypotheses": "intent_hypotheses",
            "assumptions_detected": "assumptions_detected",
            "meta_reasoning_done": "meta_reasoning",
            "navigation_done": "navigation",
            "spectral_compute_done": "spectral_compute",
            "verification_done": "verification",
            "generalization_done": "generalization",
            "multiloop_start": "multiloop_start",
            "multiloop_iteration": "refinement",
            "silent_audit_done": "silent_audit",
            "hol_generated": "hol_generation",
            "epistemic_annotated": "epistemic",
            "pipeline_done": "done",
        }
        
        if event_type in stage_map:
            self.state.current_stage = stage_map[event_type]
        
        # Mise à jour du texte d'étape
        if event_type == "multiloop_iteration":
            self.state.loop_current = event.get("loop", 0)
            self.state.iteration_current = event.get("iteration", 0)
            self.state.current_step = (
                f"Loop {self.state.loop_current}/5 - "
                f"Itération {self.state.iteration_current}"
            )
        elif event_type == "spectral_parse_strategy":
            strategy = event.get("strategy", "")
            self.state.current_step = f"Stratégie spectrale: {strategy}"
        elif event_type == "decision_gate":
            intent = event.get("goal_intent", "general")
            self.state.current_step = f"Décision: intent={intent}"
        
        # Log l'événement
        if event_type not in ("pipeline_start",):
            evt_log = f"{event_type} @ {self.state.formatted_time}"
            self.state.events_log.append(evt_log)
            if len(self.state.events_log) > 10:
                self.state.events_log = self.state.events_log[-10:]
    
    def display_cinematic(self) -> str:
        """Retourne le texte complet cinématique à afficher."""
        header = self.render_cinematic_header()
        body = self.render_cinematic_body()
        return header + body
    
    def print_cinematic(self) -> None:
        """Affiche le cinématique (Rich ou plaintext)."""
        if self.console:
            self.console.clear()
        
        output = self.display_cinematic()
        print(output)
    
    def to_rich_panel(self):
        """Retourne un Panel Rich pour intégration élégante."""
        try:
            from rich.panel import Panel
            from rich.text import Text
            from rich.box import ROUNDED
            
            content = Text(self.display_cinematic(), style="cyan")
            panel = Panel(
                content,
                title="[bold]Mode Cinématique[/bold]",
                border_style="cyan",
                box=ROUNDED,
                padding=(1, 2),
            )
            return panel
        except ImportError:
            return self.display_cinematic()


class CinematicProgressCallback:
    """
    Wrapper de progress_cb pour intégrer CinematicDisplay.
    
    Utilisation:
    ```python
    display = CinematicDisplay(num_loops=3, estimated_duration_sec=30)
    callback = CinematicProgressCallback(display)
    
    # Passer à pipeline.process()
    await pipeline.process(question, progress_cb=callback.on_progress)
    ```
    """
    
    def __init__(
        self,
        cinematic_display: CinematicDisplay,
        on_update: Optional[Callable[[], None]] = None,
    ):
        self.display = cinematic_display
        self.on_update = on_update  # callback supplémentaire si UI externe
    
    def on_progress(self, event: dict) -> None:
        """Callback à passer à pipeline.process()."""
        self.display.update_from_progress_event(event)
        
        if self.on_update:
            self.on_update()
        
        # Afficher le cinématique à chaque mise à jour (optionnel - peut laguer)
        # self.display.print_cinematic()
