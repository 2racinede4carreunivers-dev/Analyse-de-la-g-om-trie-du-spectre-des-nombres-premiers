"""Planner : sequence d'execution des moteurs. Squelette pour extension future."""
from __future__ import annotations

from typing import Any


class Planner:
    """Planner sequentiel. Pour l'instant, delegue au Pipeline."""

    def __init__(self, config: dict[str, Any]):
        self.config = config

    def plan(self, ctx: dict[str, Any]) -> list[str]:
        """Retourne la liste des etapes activees dans la config."""
        pipe_cfg = self.config.get("pipeline", {})
        steps = []
        if pipe_cfg.get("enable_abstraction", True):
            steps.append("abstraction")
        if pipe_cfg.get("enable_meta_reasoning", True):
            steps.append("meta_reasoning")
        if pipe_cfg.get("enable_concept_navigation", True):
            steps.append("concept_navigation")
        if pipe_cfg.get("enable_generalization", True):
            steps.append("generalization")
        if pipe_cfg.get("enable_theorem_discovery", False):
            steps.append("theorem_discovery")
        if pipe_cfg.get("enable_hol_generation", True):
            steps.append("hol_generation")
        if pipe_cfg.get("enable_isabelle_validation", False):
            steps.append("isabelle_validation")
        steps.append("response")
        return steps
