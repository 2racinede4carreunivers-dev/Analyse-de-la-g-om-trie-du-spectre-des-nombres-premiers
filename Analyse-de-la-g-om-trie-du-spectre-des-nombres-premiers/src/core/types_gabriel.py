"""Types Pydantic partages par tout l'agent."""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SpectralModel(str, Enum):
    """Modeles spectraux supportes (du corpus Savard)."""
    RATIO_1_2 = "1/2"
    RATIO_1_3 = "1/3"
    RATIO_1_4 = "1/4"


class AsymmetryKind(str, Enum):
    """4 configurations du rapport spectral."""
    SYM_1x1 = "symmetric_1x1"          # P1 * P2
    SYM_NxN = "symmetric_nxn"          # Pn * Pn
    ASYM_ORDERED = "asymmetric_ordered"
    ASYM_CHAOTIC = "asymmetric_chaotic"


class GapKind(str, Enum):
    """3 cas d'ecart entre nombres premiers."""
    POS_POS = "++"
    NEG_NEG = "--"
    NEG_POS = "-+"


class CognitiveConcept(BaseModel):
    """Concept mathematique extrait par le moteur d'abstraction."""
    name: str
    category: str
    keywords: list[str] = []
    related_to: list[str] = []
    confidence: float = 1.0


class QuestionContext(BaseModel):
    """Contexte d'une question utilisateur."""
    question_id: str
    raw_question: str
    detected_domain: str | None = None
    detected_model: SpectralModel | None = None
    concepts: list[CognitiveConcept] = []
    metadata: dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CandidateAnswer(BaseModel):
    """Reponse candidate produite par un tour de boucle."""
    iteration: int
    text: str
    structured_data: dict[str, Any] = {}
    score: float = 0.0
    critique: str = ""
    grounded: bool = False
    used_engines: list[str] = []


class FinalAnswer(BaseModel):
    """Reponse finale de l'agent apres multi-loop."""
    question_id: str
    answer_text: str
    structured_data: dict[str, Any] = {}
    confidence: float = 0.0
    iterations_used: int = 0
    best_score: float = 0.0
    candidates: list[CandidateAnswer] = []
    explanation: str = ""
    hol_script: str | None = None

    # ----- Axe 4 (Epistemic) + Axe 2 (ProofTrace) : optionnels -----
    # On les expose comme dicts pour rester JSON-serialisables sans
    # introduire de dependance circulaire sur le package cognitive.
    epistemic_claim: dict[str, Any] | None = None
    proof_traces: list[dict[str, Any]] = []


class PipelineStep(str, Enum):
    """Etapes du pipeline cognitif."""
    ABSTRACTION = "abstraction"
    META_REASONING = "meta_reasoning"
    CONCEPT_NAVIGATION = "concept_navigation"
    GENERALIZATION = "generalization"
    THEOREM_DISCOVERY = "theorem_discovery"
    HOL_GENERATION = "hol_generation"
    ISABELLE_VALIDATION = "isabelle_validation"
    RESPONSE = "response"
