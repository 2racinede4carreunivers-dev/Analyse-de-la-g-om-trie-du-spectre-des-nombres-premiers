#!/usr/bin/env python3
"""
INSTRUCTION D'INTÉGRATION MANUELLE - Mode Cinématique Intelligent

Trouve la ligne dans src/ui/cli.py (ligne ~2980) :

    if not live_trace:
        console.print("\n  [dim]Reflexion en cours (multi-loop self-critique)...[/dim]")
        answer = await self.orchestrator.ask(user_input)
    else:

ET REMPLACE LE BLOC ENTIER (lignes ~2978-3030) PAR:

───────────────────────────────────────────────────────────────────

live_trace = self._env_enabled("GABRIEL_LIVE_TRACE", default=True)
cinematic = self._env_enabled("GABRIEL_CINEMATIC", default=True)  
verbose_trace = self._env_enabled("GABRIEL_TRACE_VERBOSE", default=True)
use_intelligent_cinematic = self._env_enabled("GABRIEL_INTELLIGENT_CINEMATIC", default=True)

# NEW: Utiliser le CinematicOrchestrator intelligent si activé
if use_intelligent_cinematic and cinematic:
    try:
        from .cinematic_orchestrator import CinematicOrchestrator, FastModeBypass
        bypass = FastModeBypass()
        
        # Tentative de réponse rapide
        if fast_answer := bypass.try_fast_response(user_input):
            console.print(f"\\n  [bright_cyan]Réponse immédiate:[/bright_cyan]\\n  {fast_answer}\\n")
            continue
        
        # Orchestrateur avec cinématique
        orch = CinematicOrchestrator(self.orchestrator.pipeline, verbose=verbose_trace)
        answer = await orch.process(user_input, print_cinematic=True)
    except Exception as exc:
        logger.debug(f"CinematicOrchestrator fallback : {exc}")
        # Fallback au mode normal en cas d'erreur
        answer = await self.orchestrator.ask(user_input)
elif not live_trace:
    console.print("\\n  [dim]Reflexion en cours (multi-loop self-critique)...[/dim]")
    answer = await self.orchestrator.ask(user_input)
else:
    progress_state: dict[str, object] = {
        "phase": "Initialisation",
        "detail": "Preparation de la requete",
        "iteration": 0,
        "max_iterations": 0,
        "best_score": None,
        "verbose_trace": verbose_trace,
        "assumptions": [],
        "options": [],
        "recent_events": [],
    }
    live_handle: list[Live | None] = [None]
    progress_cb = self._make_progress_callback(
        progress_state,
        live_handle,
        cinematic=cinematic,
        verbose_trace=verbose_trace,
    )
    with Live(
        self._render_live_progress_panel(progress_state),
        console=console,
        refresh_per_second=8,
        transient=True,
    ) as live:
        live_handle[0] = live
        answer = await self.orchestrator.ask(
            user_input,
            progress_cb=progress_cb,
        )

───────────────────────────────────────────────────────────────────

ENSUITE:

1. Reconstruire l'image:
   docker build -f Dockerfile.cli -t llm-agent-multiloop:latest .

2. Redémarrer Gabriel:
   docker compose down
   docker compose up -d

3. Tester:
   Gabriel> Reconstruis le 63e premier
   
   Vous devriez voir le chronomètre + barre de progression + loops affichés!

"""

print(__doc__)
