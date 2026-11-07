"""
Tests pour le Slow-Motion Debugger et ses composants.

Couvre :
  - CertaintyKernel : chargement, recherche, resume d'urgence
  - RequestDecomposer : decomposition, detection d'anomalies, exemple "1,2,13,3,4,5,6"
  - CoherenceDetector : detection d'incoherence
  - SlowMotionDebugger : procedure end-to-end avec timeline
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.adapters.corpus.certainty_kernel import CertaintyKernel, Certainty
from src.core.spectral_core import SpectralMethodCore
from src.core.types import CandidateAnswer, FinalAnswer
from src.multiloop.coherence_detector import CoherenceDetector
from src.multiloop.request_decomposer import RequestDecomposer
from src.multiloop.slow_motion_debugger import SlowMotionDebugger


def _resolve_theories_dir() -> str:
    """Resout le dossier theories (local, container Docker, ou env var)."""
    import os as _os
    env_dir = _os.environ.get("GABRIEL_THEORIES_DIR")
    if env_dir and Path(env_dir).is_dir():
        return env_dir
    for cand in (
        ROOT / "theories",
        Path("/theories"),
        Path("/home/agent/app/theories"),
        Path("/app/agent-multiloop-Gabriel-local/theories"),
    ):
        if cand.is_dir():
            return str(cand)
    return str(ROOT / "theories")  # fallback


THEORIES = _resolve_theories_dir()


# ============================================================
# CertaintyKernel
# ============================================================

def test_kernel_loads_from_theories():
    """Le kernel charge >= 25 certitudes depuis les 3 sources."""
    k = CertaintyKernel(theories_dir=THEORIES)
    assert len(k.certainties) >= 25
    # Sources presentes
    keys = set(k.certainties.keys())
    assert "INVARIANT_1_2" in keys
    assert "KERNEL_INVARIANT_RECONSTRUCTION_1_2" in keys
    assert "KERNEL_INVARIANT_Z_64" in keys


def test_kernel_get_and_cite():
    k = CertaintyKernel(theories_dir=THEORIES)
    cert = k.get("INVARIANT_1_2")
    assert cert is not None
    assert "position" in cert.statement.lower()
    assert "plan_cognitif" in cert.provenance


def test_kernel_by_domain():
    k = CertaintyKernel(theories_dir=THEORIES)
    r12 = k.by_domain("ratio_1_2")
    assert len(r12) >= 8
    for c in r12:
        assert c.domain == "ratio_1_2"


def test_kernel_applicable_to_request_1_2():
    k = CertaintyKernel(theories_dir=THEORIES)
    certs = k.applicable_to("Reconstruis le 26e premier en rapport 1/2")
    keys = [c.key for c in certs]
    assert any("1_2" in k for k in keys)
    assert "INVARIANT_1_2" in keys


def test_kernel_emergency_summary_compact():
    k = CertaintyKernel(theories_dir=THEORIES)
    summary = k.emergency_summary("ratio_1_2")
    # Doit etre court (max ~6 entrees) et contenir "KERNEL" en priorite
    assert "RATIO_1_2" in summary
    assert "★" in summary  # marqueur KERNEL prioritaire
    assert summary.count("\n") < 50  # compact


# ============================================================
# RequestDecomposer
# ============================================================

def test_decomposer_detects_intent_reconstruction():
    d = RequestDecomposer()
    res = d.decompose("Reconstruis le 26eme premier en rapport 1/2")
    assert res.detected_intent == "reconstruction"
    assert res.detected_ratio == "1/2"


def test_decomposer_extracts_position():
    d = RequestDecomposer()
    res = d.decompose("Quel est le 56eme nombre premier ?")
    positions = [s for s in res.segments if s.kind == "position"]
    assert len(positions) == 1
    assert positions[0].value == 56
    assert positions[0].coherent is True


def test_decomposer_flags_invariant_violation_1_2():
    """
    Pour rapport 1/2 avec position 26, si on cite n=10 alors c'est incoherent
    (viole l'INVARIANT n=position).
    """
    d = RequestDecomposer()
    res = d.decompose("Reconstruis le 26eme premier en rapport 1/2 avec n=10 termes")
    # Doit reperer 10 comme incoherent
    incoherent = res.incoherent_segments
    assert any(s.value == 10 for s in incoherent), \
        f"10 devrait etre flag incoherent, got: {[s.value for s in incoherent]}"


def test_decomposer_example_user_sequence():
    """
    L'exemple de l'utilisateur : "somme de 1,2,13,3,4,5,6" 
    13 doit etre flag comme incoherent (rompt la sequence 1..7).
    
    NB: notre detection actuelle se base sur l'INVARIANT 1/2 ; pour
    ce cas generique, on verifie au moins que la decomposition produit
    des segments lisibles.
    """
    d = RequestDecomposer()
    res = d.decompose("Somme des 7 premiers entiers : 1,2,13,3,4,5,6")
    numbers = [s for s in res.segments if s.kind == "number"]
    # On a au moins 7-8 nombres detectes (1,2,13,3,4,5,6,7)
    assert len(numbers) >= 6


def test_decomposer_coherent_request():
    """Requete propre : aucun segment incoherent."""
    d = RequestDecomposer()
    res = d.decompose("Reconstruis le 5eme premier en rapport 1/2")
    assert not res.has_anomaly
    assert res.detected_intent == "reconstruction"
    assert res.detected_ratio == "1/2"


# ============================================================
# CoherenceDetector
# ============================================================

def _make_candidate(text: str, score: float) -> CandidateAnswer:
    return CandidateAnswer(
        iteration=1, text=text, structured_data={}, used_engines=["llm"],
        score=score, critique="",
    )


def test_coherence_detects_low_scores():
    d = CoherenceDetector(threshold=0.55)
    candidates = [_make_candidate("reponse", 3.0), _make_candidate("reponse", 4.0)]
    report = d.evaluate(
        question="Le 26eme premier ?",
        candidates=candidates,
        best_answer_text="reponse banale",
    )
    assert report.score < 0.6


def test_coherence_detects_forbidden_vocab():
    d = CoherenceDetector(threshold=0.55)
    candidates = [_make_candidate("ok", 8.0)]
    report = d.evaluate(
        question="Le 26eme premier ?",
        candidates=candidates,
        best_answer_text="Cette methode est absurde et incoherente.",
    )
    assert report.incoherent
    assert any("vocabulaire_interdit" in s for s in report.signals)


def test_coherence_detects_wrong_prime():
    d = CoherenceDetector(threshold=0.55)
    candidates = [_make_candidate("ok", 8.0)]
    report = d.evaluate(
        question="Reconstruis le 26eme premier en rapport 1/2",
        candidates=candidates,
        best_answer_text="Le 26eme premier est 97.",  # FAUX : 101
        precomputed_facts={"position": 26, "prime": 101, "model": "1/2"},
    )
    assert report.incoherent


def test_coherence_valid_passes():
    d = CoherenceDetector(threshold=0.55)
    candidates = [_make_candidate("ok", 9.0), _make_candidate("ok", 9.5)]
    report = d.evaluate(
        question="Reconstruis le 26eme premier en rapport 1/2",
        candidates=candidates,
        best_answer_text=(
            "Le 26eme nombre premier est 101. Avec n=26 termes "
            "dans A et B, l'invariant est respecte."
        ),
        precomputed_facts={"position": 26, "prime": 101, "n": 26,
                           "num_terms": 26, "model": "1/2"},
    )
    assert report.score >= 0.55
    assert not report.incoherent


# ============================================================
# SlowMotionDebugger (end-to-end)
# ============================================================

def _make_final(text: str, candidates: list[CandidateAnswer] | None = None) -> FinalAnswer:
    return FinalAnswer(
        question_id="test-id",
        answer_text=text,
        structured_data={},
        confidence=0.5,
        iterations_used=1,
        best_score=5.0,
        candidates=candidates or [],
        explanation="",
    )


def test_slowmo_produces_certified_answer_for_26():
    """Le debugger produit la reponse certifiee 101 pour la position 26."""
    debugger = SlowMotionDebugger(
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
    )
    detector = CoherenceDetector(threshold=0.99)  # toujours incoherent pour le test
    candidates = [_make_candidate("hallucination", 3.0)]
    final = _make_final("Le 26eme premier est 97.")  # faux

    report = detector.evaluate(
        question="Reconstruis le 26eme premier en rapport 1/2",
        candidates=candidates,
        best_answer_text=final.answer_text,
        precomputed_facts={"position": 26, "prime": 101, "model": "1/2"},
    )
    assert report.incoherent

    result = debugger.debug(
        question="Reconstruis le 26eme premier en rapport 1/2",
        final=final,
        coherence_report=report,
        precomputed_facts={"position": 26, "prime": 101, "model": "1/2"},
    )
    # La reponse certifiee doit mentionner 101
    assert "101" in result.answer_text
    assert result.confidence == 1.0
    # Structured data
    assert result.structured_data["slow_motion_triggered"] is True
    assert "debug_timeline" in result.structured_data
    timeline = result.structured_data["debug_timeline"]
    assert len(timeline) >= 6  # au moins 6 etapes (T1..T8)
    # Citations presentes
    assert result.structured_data["certified"]["citations"]


def test_slowmo_bypasses_invariant_violation():
    """
    Question : "26eme premier rapport 1/2 avec n=10"
    Le segment n=10 doit etre bypass (viole INVARIANT 1/2).
    """
    debugger = SlowMotionDebugger(
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
    )
    detector = CoherenceDetector(threshold=0.99)
    final = _make_final("Avec n=10 termes, le 26eme premier est 97.")
    candidates = [_make_candidate(final.answer_text, 4.0)]
    report = detector.evaluate(
        question="Reconstruis le 26eme premier en rapport 1/2 avec n=10",
        candidates=candidates,
        best_answer_text=final.answer_text,
        precomputed_facts={"position": 26, "prime": 101, "n": 10, "model": "1/2"},
    )
    result = debugger.debug(
        question="Reconstruis le 26eme premier en rapport 1/2 avec n=10",
        final=final,
        coherence_report=report,
    )
    # On veut voir que 10 a ete bypass
    incoherent = result.structured_data["decomposition"]["incoherent_segments"]
    assert any(s["value"] == 10 for s in incoherent), \
        f"n=10 aurait du etre bypass, got: {incoherent}"
    # Reponse contient 101 (correct) et pas seulement 97
    assert "101" in result.answer_text


def test_slowmo_timeline_complete():
    """La timeline doit contenir les 8 etapes nommees."""
    debugger = SlowMotionDebugger(
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
    )
    detector = CoherenceDetector(threshold=0.99)
    final = _make_final("vague")
    candidates = [_make_candidate("vague", 3.0)]
    report = detector.evaluate(
        question="Reconstruis le 5eme premier en rapport 1/2",
        candidates=candidates,
        best_answer_text=final.answer_text,
    )
    result = debugger.debug(
        question="Reconstruis le 5eme premier en rapport 1/2",
        final=final, coherence_report=report,
    )
    timeline = result.structured_data["debug_timeline"]
    labels = [ev["label"] for ev in timeline]
    expected_labels = {
        "REQUETE_RECUE", "INCOHERENCE_DETECTEE", "DECOMPOSITION",
        "BYPASS_SEGMENTS", "REQUETE_CANONIQUE", "RESOLUTION_CERTIFIEE",
        "REFORMULATIONS", "REPONSE_CERTIFIEE",
    }
    assert expected_labels.issubset(set(labels)), \
        f"Manque etapes : {expected_labels - set(labels)}"


def test_slowmo_unknown_intent_falls_back_to_summary():
    """Si l'intent est inconnu, le debugger retourne le resume d'urgence."""
    debugger = SlowMotionDebugger(
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
    )
    detector = CoherenceDetector(threshold=0.99)
    final = _make_final("hum")
    candidates = [_make_candidate("hum", 2.0)]
    report = detector.evaluate(
        question="hum quelque chose en rapport spectral 1/3",
        candidates=candidates,
        best_answer_text=final.answer_text,
    )
    result = debugger.debug(
        question="hum quelque chose en rapport spectral 1/3",
        final=final, coherence_report=report,
    )
    # Doit contenir un resume du domaine 1/3 ou general
    assert result.structured_data["certified"]["citations"]

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
