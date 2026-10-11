"""Alias de compatibilite : src.prompt_injector -> memory.prompt_injector_enhanced.

Certaines integrations historiques (gabriel_llm_integration_safe) importent
`from src.prompt_injector import PromptInjector`. Ce module est un thin wrapper
qui re-exporte la version officielle depuis `memory/prompt_injector_enhanced.py`.
"""
from __future__ import annotations

from memory.prompt_injector_enhanced import (  # noqa: F401
    PromptInjector,
    ValidationResult,
    HOL_STRICT_SPEC,
    RSA_SPEC,
    RIEMANN_SPEC,
)

__all__ = [
    "PromptInjector",
    "ValidationResult",
    "HOL_STRICT_SPEC",
    "RSA_SPEC",
    "RIEMANN_SPEC",
]
