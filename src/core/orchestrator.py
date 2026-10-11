"""Orchestrator : facade haut-niveau de l'agent."""
from __future__ import annotations

import logging
from typing import Any, Callable

from .pipeline import Pipeline
from .pipeline_with_gap_detection import PipelineWithGapDetection
from .spectral_types import FinalAnswer


logger = logging.getLogger(__name__)


class Orchestrator:
    """Wrapper haut-niveau autour du pipeline (interface stable pour l'UI)."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        base_pipeline = Pipeline(config)
        # CORRECTION : Wrapper le pipeline avec détection d'écart
        # Cela force la détection des écarts AVANT le multiloop
        self.pipeline = PipelineWithGapDetection(base_pipeline)
        self.memory: list[dict[str, str]] = []
        logger.info("✓ Orchestrator with GapDetection initialized")

    @property
    def conversation_memory(self):
        """Accès direct à la mémoire conversationnelle courte du LLM
        (utilisée pour introspection CLI et pour la commande `reset`)."""
        return self.pipeline.llm.conversation_memory

    async def ask(
        self,
        question: str,
        progress_cb: Callable[[dict[str, Any]], None] | None = None,
        force_mode: Any = None,
    ) -> FinalAnswer:
        result = await self.pipeline.process(question, progress_cb=progress_cb, force_mode=force_mode)
        # Journal léger (backward-compatible)
        self.memory.append({"role": "user", "content": question})
        self.memory.append({"role": "assistant", "content": result.answer_text})
        # P1 : enregistrer le tour dans la mémoire conversationnelle courte
        # pour qu'il soit injecté dans le prompt du prochain appel LLM.
        try:
            self.conversation_memory.add(question, result.answer_text or "")
        except Exception as exc:  # pragma: no cover
            logger.warning("Impossible d'enregistrer le tour conversationnel : %s", exc)
        return result

    def reset_conversation(self) -> None:
        """Vide la mémoire conversationnelle courte (nouvelle session)."""
        self.memory.clear()
        try:
            self.conversation_memory.clear()
        except Exception:  # pragma: no cover
            pass

    def get_context(self) -> str:
        return f"{len(self.memory)} echanges en memoire."

    def get_memory(self, last_n: int = 5) -> str:
        if not self.memory:
            return "(memoire vide)"
        slice_ = self.memory[-last_n * 2 :]
        lines = []
        for m in slice_:
            tag = "Q" if m["role"] == "user" else "A"
            lines.append(f"[{tag}] {m['content'][:200]}")
        return "\n".join(lines)
