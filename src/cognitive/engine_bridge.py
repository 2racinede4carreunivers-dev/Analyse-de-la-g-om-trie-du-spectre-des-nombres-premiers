"""Pont d'integration des 4 axes cognitifs dans le moteur Gabriel.

Ce module connecte :
  - Axe 2 (ProofTrace + invariants) aux calculs spectraux
  - Axe 3 (RegimeOntology) pour la classification du regime applique
  - Axe 4 (EpistemicClaim) pour marquer chaque resultat (CERTAIN / CONJECTURE / HORS_DOMAINE)
  - Axe 5 (MetaReasoner) pour la statistique d'auto-evaluation par categorie

Fournit :
  - `CognitiveResult` : enveloppe d'un resultat numerique avec sa trace + sa claim
  - `build_gap_result` / `build_reconstruct_result` / `build_rsp_1x1_result`
  - `get_meta_reasoner()` : singleton MetaReasoner par defaut
"""
from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Optional

from .epistemic import Certainty, EpistemicClaim, Provenance, mark_claim
from .meta_reasoning import MetaReasoner
from .proof_trace import ProofTrace
from .regime_ontology import RegimeOntology
from .traced_calculations import (
    traced_gap, traced_reconstruct, traced_rsp_1x1,
)


# --------------------------------------------------------------------------
# Singleton MetaReasoner (centralise les stats Gabriel)
# --------------------------------------------------------------------------
_META_REASONER: Optional[MetaReasoner] = None
_DEFAULT_LEARNING_DIR = Path("data/learning")


def get_meta_reasoner(learning_dir: Path | str | None = None) -> MetaReasoner:
    """Retourne (et lazy-init) le MetaReasoner singleton de Gabriel."""
    global _META_REASONER
    if _META_REASONER is None:
        base = Path(learning_dir) if learning_dir else _DEFAULT_LEARNING_DIR
        _META_REASONER = MetaReasoner(
            errors_file=base / "errors.jsonl",
            stats_file=base / "stats.json",
        )
    return _META_REASONER


def reset_meta_reasoner() -> None:
    """Utile pour les tests : oublie l'instance singleton courante."""
    global _META_REASONER
    _META_REASONER = None


# --------------------------------------------------------------------------
# Enveloppe cognitive d'un resultat
# --------------------------------------------------------------------------
@dataclass
class CognitiveResult:
    """Resultat numerique enveloppe d'une trace de preuve et d'une claim."""
    value: Any                                # la valeur calculee (int, Fraction, etc.)
    proof_trace: ProofTrace
    claim: EpistemicClaim
    category: str                             # cle MetaReasoner ('gap_pos_pos', ...)
    regime: Optional[str] = None              # ex: 'regime_positif', 'modele_1_2'
    extras: dict[str, Any] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return self.proof_trace.is_valid


# --------------------------------------------------------------------------
# Helpers Axe 3 : ontologie -> categorie + regime
# --------------------------------------------------------------------------
_ONTOLOGY = RegimeOntology()


def _regime_for_gap(p1: int, p2: int) -> tuple[str, str]:
    """Determine (category MetaReasoner, regime ontologique) pour un gap."""
    if p1 >= 0 and p2 >= 0:
        return "gap_pos_pos", "regime_positif"
    if p1 < 0 and p2 < 0:
        return "gap_neg_neg", "regime_negatif"
    return "gap_mixed", "regime_mixte"


def _category_for_reconstruction(model_name: str) -> str:
    return f"reconstruction_{model_name.replace('/', '_')}"


def _regime_for_model(model_name: str) -> str:
    return f"modele_{model_name.replace('/', '_')}"


# --------------------------------------------------------------------------
# Builders
# --------------------------------------------------------------------------
def build_gap_result(p1: int, p2: int) -> CognitiveResult:
    """Calcule un gap + produit une trace + une claim epistemique."""
    gap, trace = traced_gap(p1, p2)
    category, regime = _regime_for_gap(p1, p2)

    if trace.is_valid:
        claim = mark_claim(
            statement=f"gap({p1}, {p2}) = {gap}",
            certainty=Certainty.CERTAIN,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={"gap": gap, "case": regime},
        )
    else:
        claim = mark_claim(
            statement=f"gap({p1}, {p2}) (invariants violes)",
            certainty=Certainty.HORS_DOMAINE,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={"gap": gap, "trace_valid": False},
            limits=["Au moins un invariant de symetrie/positivite a echoue."],
        )

    return CognitiveResult(
        value=gap, proof_trace=trace, claim=claim,
        category=category, regime=regime,
        extras={"p1": p1, "p2": p2},
    )


def build_reconstruct_result(
    n: int, actual_prime: int, model_name: str = "1/2",
) -> CognitiveResult:
    """Reconstruit le n-ieme premier + produit trace + claim."""
    rec, trace = traced_reconstruct(n, actual_prime, model_name)
    category = _category_for_reconstruction(model_name)
    regime = _regime_for_model(model_name)

    is_exact = (rec == actual_prime)
    if trace.is_valid and is_exact:
        claim = mark_claim(
            statement=(
                f"Le {n}-ieme premier reconstruit via modele {model_name} "
                f"vaut {rec} (= {actual_prime} de reference)."
            ),
            certainty=Certainty.CERTAIN,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={
                "n": n, "model": model_name,
                "reconstructed": str(rec), "actual_prime": actual_prime,
            },
        )
    elif is_exact:
        claim = mark_claim(
            statement=(
                f"Reconstruction {n} via {model_name} = {rec} mais un invariant "
                "secondaire a echoue."
            ),
            certainty=Certainty.CONJECTURE,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={"n": n, "model": model_name, "reconstructed": str(rec)},
            limits=["Au moins un invariant secondaire a echoue."],
        )
    else:
        claim = mark_claim(
            statement=(
                f"Reconstruction {n} via {model_name} ne correspond PAS au premier "
                f"{actual_prime}."
            ),
            certainty=Certainty.HORS_DOMAINE,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={
                "n": n, "model": model_name,
                "reconstructed": str(rec), "actual_prime": actual_prime,
            },
            limits=["Invariant principal d'exactitude viole."],
        )

    return CognitiveResult(
        value=rec, proof_trace=trace, claim=claim,
        category=category, regime=regime,
        extras={"n": n, "actual_prime": actual_prime, "model": model_name},
    )


def build_rsp_1x1_result(
    n1: int, n2: int, model_name: str = "1/2",
) -> CognitiveResult:
    """Calcule le ratio 1x1 + trace + claim."""
    ratio, trace = traced_rsp_1x1(n1, n2, model_name)
    category = "ratio_1x1"
    regime = _regime_for_model(model_name)

    if trace.is_valid:
        claim = mark_claim(
            statement=(
                f"RsP_1x1({n1}, {n2}) via modele {model_name} = {ratio} "
                f"(rapport exact 1/{model_name.split('/')[-1]})."
            ),
            certainty=Certainty.CERTAIN,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={"n1": n1, "n2": n2, "model": model_name, "ratio": str(ratio)},
        )
    else:
        claim = mark_claim(
            statement=(
                f"RsP_1x1({n1}, {n2}) via modele {model_name} : invariants violes."
            ),
            certainty=Certainty.HORS_DOMAINE,
            provenance=[Provenance.SPECTRAL_CORE],
            evidence={"n1": n1, "n2": n2, "model": model_name, "ratio": str(ratio)},
            limits=["Cas 1x1 doit donner un ratio EXACT."],
        )

    return CognitiveResult(
        value=ratio, proof_trace=trace, claim=claim,
        category=category, regime=regime,
        extras={"n1": n1, "n2": n2, "model": model_name},
    )


# --------------------------------------------------------------------------
# Enregistrement automatique dans MetaReasoner
# --------------------------------------------------------------------------
def record_cognitive_result(result: CognitiveResult,
                            meta: Optional[MetaReasoner] = None) -> None:
    """Enregistre l'issue (succes/echec) du resultat dans le MetaReasoner."""
    if meta is None:
        meta = get_meta_reasoner()
    success = result.is_valid and (
        result.claim.certainty == Certainty.CERTAIN
    )
    details = {
        "value": str(result.value),
        "claim": result.claim.certainty.value,
        "extras": {k: str(v) for k, v in result.extras.items()},
    }
    meta.record(result.category, success=success, details=details)
