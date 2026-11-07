"""Axe 2 - Raisonnement par construction : ProofTrace + invariants.

Chaque calcul important produit une `ProofTrace` structuree :
  hypotheses -> regles appliquees -> conclusion + verification d'invariants
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional


@dataclass
class ProofStep:
    """Une etape de preuve : regle appliquee + entree + sortie."""
    step_number: int
    rule_name: str
    input_state: dict[str, Any]
    output_state: dict[str, Any]
    justification: str = ""

    def to_text(self) -> str:
        return (
            f"  Etape {self.step_number}. [{self.rule_name}] {self.justification}\n"
            f"    In  : {self.input_state}\n"
            f"    Out : {self.output_state}"
        )


@dataclass
class ProofTrace:
    """Trace complete d'un raisonnement par construction."""
    title: str
    hypotheses: list[str] = field(default_factory=list)
    steps: list[ProofStep] = field(default_factory=list)
    conclusion: str = ""
    invariants_checked: list[dict[str, Any]] = field(default_factory=list)
    is_valid: bool = True
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def add_step(
        self, rule_name: str, input_state: dict[str, Any],
        output_state: dict[str, Any], justification: str = "",
    ) -> ProofStep:
        step = ProofStep(
            step_number=len(self.steps) + 1,
            rule_name=rule_name,
            input_state=input_state,
            output_state=output_state,
            justification=justification,
        )
        self.steps.append(step)
        return step

    def check_invariant(
        self, name: str, condition: bool, details: str = ""
    ) -> bool:
        result = {"name": name, "passed": bool(condition), "details": details}
        self.invariants_checked.append(result)
        if not condition:
            self.is_valid = False
        return condition

    def conclude(self, conclusion: str) -> None:
        self.conclusion = conclusion

    def to_text(self) -> str:
        lines = [
            f"=== PROOF TRACE : {self.title} ===",
            "",
            "Hypotheses :",
        ]
        for h in self.hypotheses:
            lines.append(f"  - {h}")
        lines.append("")
        lines.append("Etapes :")
        for s in self.steps:
            lines.append(s.to_text())
        lines.append("")
        if self.invariants_checked:
            lines.append("Invariants verifies :")
            for inv in self.invariants_checked:
                mark = "[OK]" if inv["passed"] else "[FAIL]"
                lines.append(f"  {mark} {inv['name']} : {inv['details']}")
            lines.append("")
        lines.append(f"Conclusion : {self.conclusion}")
        lines.append(f"Validite globale : {'VALID' if self.is_valid else 'INVALID'}")
        return "\n".join(lines)


def check_invariant(name: str, condition: bool, details: str = "") -> dict:
    """Helper standalone pour verifier un invariant hors ProofTrace."""
    return {"name": name, "passed": bool(condition), "details": details}
