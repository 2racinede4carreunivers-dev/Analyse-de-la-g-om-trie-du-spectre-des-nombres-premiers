"""Package cognitive : 4 axes d'amelioration du raisonnement de Gabriel.

  - proof_trace        (Axe 2) Raisonnement par construction : trace de preuve + invariants
  - regime_ontology    (Axe 3) Raisonnement ontologique : hierarchie des regimes spectraux
  - epistemic          (Axe 4) Raisonnement epistemologique : 3 niveaux de certitude
  - meta_reasoning     (Axe 5) Meta-raisonnement : auto-evaluation + memoire d'erreur
"""
from __future__ import annotations

from .proof_trace import ProofTrace, ProofStep, check_invariant
from .regime_ontology import RegimeOntology, RegimeRelation
from .epistemic import Certainty, EpistemicClaim, Provenance, mark_claim
from .meta_reasoning import MetaReasoner, ConfidenceLevel
from .traced_calculations import (
    traced_gap, traced_reconstruct, traced_rsp_1x1, trace_to_json,
)
from .engine_bridge import (
    CognitiveResult, build_gap_result, build_reconstruct_result,
    build_rsp_1x1_result, get_meta_reasoner, reset_meta_reasoner,
    record_cognitive_result,
)

__all__ = [
    "ProofTrace", "ProofStep", "check_invariant",
    "RegimeOntology", "RegimeRelation",
    "Certainty", "EpistemicClaim", "Provenance", "mark_claim",
    "MetaReasoner", "ConfidenceLevel",
    "traced_gap", "traced_reconstruct", "traced_rsp_1x1", "trace_to_json",
    "CognitiveResult", "build_gap_result", "build_reconstruct_result",
    "build_rsp_1x1_result", "get_meta_reasoner", "reset_meta_reasoner",
    "record_cognitive_result",
]
