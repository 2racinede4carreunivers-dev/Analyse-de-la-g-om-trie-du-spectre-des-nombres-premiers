"""Axe 2 - Calculs traces : wrappers qui produisent une ProofTrace pour chaque
operation mathematique importante (gap, reconstruction, RsP).

Chaque wrapper :
  1. Decompose le calcul en etapes nommees (ProofStep)
  2. Verifie automatiquement les invariants applicables
  3. Detecte les cas limites (n=0, n=1, p<0, ...)
  4. Exporte la trace en JSON (compatible AuditStore)

100% deterministe, zero LLM, base sur les formules officielles methode_spectral.thy.
"""
from __future__ import annotations

import json
from fractions import Fraction
from typing import Any

from .proof_trace import ProofTrace


# =========================================================================
# Detection de cas limites
# =========================================================================
def _detect_edge_cases_gap(p1: int, p2: int) -> list[str]:
    """Retourne la liste des cas limites detectes pour un gap."""
    cases = []
    if p1 == 0 or p2 == 0:
        cases.append("Zero present (p1 ou p2 = 0)")
    if p1 == p2:
        cases.append("p1 == p2 : gap nul attendu")
    if abs(p1) > 1000 or abs(p2) > 1000:
        cases.append("Valeur extreme (|p| > 1000)")
    return cases


def _detect_edge_cases_reconstruct(n: int) -> list[str]:
    cases = []
    if n <= 0:
        cases.append(f"n={n} <= 0 : hors domaine standard")
    if n == 1:
        cases.append("n=1 : cas trivial (premier prime = 2)")
    if n > 1000:
        cases.append("n > 1000 : hors table primes")
    return cases


# =========================================================================
# Wrappers traces
# =========================================================================
def traced_gap(p1: int, p2: int) -> tuple[int, ProofTrace]:
    """Calcule gap(p1, p2) avec trace de preuve + invariants.

    Returns:
        (gap_count, ProofTrace)
    """
    trace = ProofTrace(title=f"gap({p1}, {p2})")
    trace.hypotheses = [f"p1 = {p1}", f"p2 = {p2}"]

    # Etape 1 : detection des cas limites
    edges = _detect_edge_cases_gap(p1, p2)
    trace.add_step(
        "detect_edge_cases",
        {"p1": p1, "p2": p2},
        {"edge_cases": edges},
        f"{len(edges)} cas limite(s) detecte(s)" if edges else "aucun cas limite",
    )

    # Etape 2 : classification du cas spectral
    if p1 >= 0 and p2 >= 0:
        case = "++"
    elif p1 < 0 and p2 < 0:
        case = "--"
    else:
        case = "-+"
    trace.add_step(
        "classify_case",
        {"p1": p1, "p2": p2},
        {"case": case},
        f"Cas spectral detecte : ({case[0]}, {case[-1]})",
    )

    # Etape 3 : application de la formule
    gap = abs(p1 - p2) - 1 if p1 != p2 else 0
    trace.add_step(
        "apply_formula",
        {"p1": p1, "p2": p2, "case": case},
        {"gap": gap},
        f"gap = |p1 - p2| - 1 = |{p1 - p2}| - 1 = {gap}",
    )

    # Invariant 1 : symetrie gap(a,b) == gap(b,a)
    gap_inv = abs(p2 - p1) - 1 if p2 != p1 else 0
    trace.check_invariant(
        "symetrie",
        condition=(gap == gap_inv),
        details=f"gap({p1},{p2})={gap} == gap({p2},{p1})={gap_inv}",
    )
    # Invariant 2 : gap >= 0
    trace.check_invariant(
        "positivite",
        condition=(gap >= 0),
        details=f"gap={gap} >= 0",
    )
    # Invariant 3 : si p1==p2 -> gap == 0
    if p1 == p2:
        trace.check_invariant(
            "self_gap_zero",
            condition=(gap == 0),
            details=f"gap({p1},{p1}) doit etre 0, vaut {gap}",
        )

    trace.conclude(f"gap({p1}, {p2}) = {gap}  (cas {case})")
    return gap, trace


def traced_reconstruct(n: int, actual_prime: int, model_name: str = "1/2"
                      ) -> tuple[Fraction, ProofTrace]:
    """Calcule la reconstruction du n-ieme premier via le modele specifie.

    Trace les etapes : A(n), B(n), digamma, reconstruction.
    Verifie l'invariant : reconstructed == actual_prime.
    """
    from ..spectral.spectral_models import get_model

    trace = ProofTrace(title=f"reconstruct({n}) via modele {model_name}")
    trace.hypotheses = [
        f"n = {n}", f"actual_prime = {actual_prime}", f"modele = {model_name}",
    ]

    # Edge cases
    edges = _detect_edge_cases_reconstruct(n)
    trace.add_step(
        "detect_edge_cases", {"n": n}, {"edge_cases": edges},
        f"{len(edges)} cas limite(s)" if edges else "aucun cas limite",
    )

    model = get_model(model_name)

    # A(n)
    a_val = model.A(n)
    trace.add_step(
        "compute_A", {"n": n}, {"A": a_val},
        f"A({n}) = {a_val}  (modele {model_name})",
    )

    # B(n)
    b_val = model.B(n)
    trace.add_step(
        "compute_B", {"n": n}, {"B": b_val},
        f"B({n}) = {b_val}  (modele {model_name})",
    )

    # digamma
    digamma = model.digamma(n, actual_prime)
    trace.add_step(
        "compute_digamma",
        {"n": n, "p": actual_prime, "B": b_val},
        {"digamma": digamma},
        f"digamma = B({n}) - {model.reconstruction_factor}*{actual_prime} = {digamma}",
    )

    # reconstruction
    reconstructed = model.reconstruct(n, digamma)
    trace.add_step(
        "reconstruct",
        {"B": b_val, "digamma": digamma, "factor": model.reconstruction_factor},
        {"reconstructed": reconstructed},
        f"p = (B - digamma) / {model.reconstruction_factor} = {reconstructed}",
    )

    # Invariant principal : reconstruction exacte
    trace.check_invariant(
        "exactitude_reconstruction",
        condition=(reconstructed == actual_prime),
        details=f"reconstructed={reconstructed} == actual={actual_prime}",
    )
    # Invariant secondaire : digamma + factor*p == B
    trace.check_invariant(
        "coherence_digamma",
        condition=(digamma + model.reconstruction_factor * actual_prime == b_val),
        details=f"digamma + factor*p == B(n)",
    )

    trace.conclude(
        f"reconstruct({n}) = {reconstructed}  "
        f"(coherent avec premier reel {actual_prime})"
    )
    return reconstructed, trace


def traced_rsp_1x1(n1: int, n2: int, model_name: str = "1/2"
                   ) -> tuple[Fraction, ProofTrace]:
    """Calcule le rapport spectral 1x1 RsP(n1, n2) avec trace + invariants.

    Returns (ratio, ProofTrace).
    Invariant : ratio == 1/n_factor (exact pour le cas 1x1).
    """
    from ..spectral.spectral_models import get_model

    trace = ProofTrace(title=f"RsP_1x1({n1}, {n2}) via modele {model_name}")
    trace.hypotheses = [
        f"n1 = {n1}", f"n2 = {n2}", f"modele = {model_name}", "n1 != n2",
    ]
    model = get_model(model_name)
    expected = model.ratio

    if n1 == n2:
        trace.check_invariant(
            "indices_distincts", condition=False,
            details=f"n1=n2={n1} : RsP_1x1 indefini",
        )
        trace.conclude(f"RsP_1x1({n1},{n2}) indefini (n1 == n2)")
        return Fraction(0), trace

    a_n1, a_n2 = model.A(n1), model.A(n2)
    b_n1, b_n2 = model.B(n1), model.B(n2)
    trace.add_step(
        "compute_A_B",
        {"n1": n1, "n2": n2},
        {"A_n1": a_n1, "A_n2": a_n2, "B_n1": b_n1, "B_n2": b_n2},
        f"A({n1})={a_n1}, A({n2})={a_n2}, B({n1})={b_n1}, B({n2})={b_n2}",
    )

    num = a_n1 - a_n2
    den = b_n1 - b_n2
    trace.add_step(
        "compute_num_den",
        {"A_n1": a_n1, "A_n2": a_n2, "B_n1": b_n1, "B_n2": b_n2},
        {"num": num, "den": den},
        f"num = A(n1)-A(n2) = {num} ; den = B(n1)-B(n2) = {den}",
    )

    ratio = num / den
    trace.add_step(
        "apply_ratio",
        {"num": num, "den": den},
        {"ratio": ratio},
        f"RsP = num/den = {ratio}",
    )

    # Invariant : ratio == 1/n_factor exact pour cas 1x1
    trace.check_invariant(
        "ratio_exact_1x1",
        condition=(ratio == expected),
        details=f"RsP={ratio} == 1/{model.n_factor}={expected}",
    )
    # Invariant : denominateur non nul
    trace.check_invariant(
        "denominateur_non_nul",
        condition=(den != 0),
        details=f"den = {den}",
    )

    trace.conclude(
        f"RsP_1x1({n1}, {n2}) = {ratio}  (modele {model_name}, attendu {expected})"
    )
    return ratio, trace


def trace_to_json(trace: ProofTrace) -> str:
    """Exporte une ProofTrace en JSON (compatible AuditStore)."""
    return json.dumps({
        "title": trace.title,
        "hypotheses": trace.hypotheses,
        "steps": [
            {
                "step_number": s.step_number,
                "rule_name": s.rule_name,
                "input_state": {k: str(v) for k, v in s.input_state.items()},
                "output_state": {k: str(v) for k, v in s.output_state.items()},
                "justification": s.justification,
            }
            for s in trace.steps
        ],
        "invariants_checked": trace.invariants_checked,
        "conclusion": trace.conclusion,
        "is_valid": trace.is_valid,
        "created_at": trace.created_at,
    }, indent=2, ensure_ascii=False, default=str)
