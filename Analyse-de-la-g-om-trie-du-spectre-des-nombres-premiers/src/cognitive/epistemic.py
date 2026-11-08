"""Axe 4 - Raisonnement epistemologique : 3 niveaux de certitude.

Chaque affirmation produite par Gabriel est etiquetee avec :
  - CERTAIN     : calcul exact (Fraction / Isabelle / verifie toolkit)
  - CONJECTURE  : extrapolation coherente mais pas prouvee
  - HORS_DOMAINE: Gabriel reconnait ne pas pouvoir repondre formellement

Et un marqueur de provenance (qui a produit l'affirmation).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class Certainty(str, Enum):
    CERTAIN = "CERTAIN"
    CONJECTURE = "CONJECTURE"
    HORS_DOMAINE = "HORS_DOMAINE"


class Provenance(str, Enum):
    CERTAINTY_KERNEL = "CertaintyKernel"
    SPECTRAL_CORE = "SpectralCore"
    LLM_CLAUDE = "LLM_Claude"
    LLM_OPENAI = "LLM_OpenAI"
    WOLFRAM = "Wolfram"
    ISABELLE = "Isabelle"
    LEAN4 = "Lean4"
    SYMPY = "sympy"
    MPMATH = "mpmath"
    Z3 = "z3"
    USER = "user"


@dataclass
class EpistemicClaim:
    """Une affirmation avec son niveau de certitude et sa provenance."""
    statement: str
    certainty: Certainty
    provenance: list[Provenance] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    limits: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def can_cite(self) -> bool:
        """Une affirmation citable doit etre CERTAIN avec provenance verifiee."""
        return (
            self.certainty == Certainty.CERTAIN
            and any(p in {Provenance.CERTAINTY_KERNEL, Provenance.SPECTRAL_CORE,
                          Provenance.ISABELLE, Provenance.LEAN4,
                          Provenance.WOLFRAM, Provenance.SYMPY,
                          Provenance.MPMATH, Provenance.Z3}
                    for p in self.provenance)
        )

    def to_text(self) -> str:
        prov = ", ".join(p.value for p in self.provenance) or "non specifiee"
        marker = {
            Certainty.CERTAIN: "[CERTAIN]",
            Certainty.CONJECTURE: "[CONJECTURE]",
            Certainty.HORS_DOMAINE: "[HORS DOMAINE]",
        }[self.certainty]
        lines = [f"{marker} {self.statement}", f"  Provenance : {prov}"]
        if self.evidence:
            lines.append(f"  Evidence   : {self.evidence}")
        if self.limits:
            lines.append("  Limites    :")
            for lim in self.limits:
                lines.append(f"    - {lim}")
        return "\n".join(lines)


def mark_claim(
    statement: str,
    certainty: Certainty,
    provenance: list[Provenance] | Provenance | None = None,
    evidence: Optional[dict] = None,
    limits: Optional[list[str]] = None,
) -> EpistemicClaim:
    """Helper de construction rapide d'une EpistemicClaim."""
    if provenance is None:
        provs: list[Provenance] = []
    elif isinstance(provenance, Provenance):
        provs = [provenance]
    else:
        provs = list(provenance)
    return EpistemicClaim(
        statement=statement,
        certainty=certainty,
        provenance=provs,
        evidence=evidence or {},
        limits=limits or [],
    )
