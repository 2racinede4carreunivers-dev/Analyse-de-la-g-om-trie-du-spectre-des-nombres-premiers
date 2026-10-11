"""
Debug Toolkit — Vrais outils de verification formelle pour le debugger.

Trois validateurs essentiels embarques dans l'image Docker :
  - SympyValidator    : validation symbolique des formules SA, SB
  - MpmathValidator   : recalcul a precision arbitraire (100 chiffres)
  - Z3Prover          : preuve formelle de l'INVARIANT 1/2 par SMT solver

Chaque validateur expose une API simple : validate(position, ratio) -> dict
"""
from .registry import ToolkitRegistry, ToolInfo
from .sympy_validator import SympyValidator
from .mpmath_validator import MpmathValidator
from .z3_prover import Z3Prover

__all__ = [
    "ToolkitRegistry", "ToolInfo",
    "SympyValidator", "MpmathValidator", "Z3Prover",
]
