"""
Tests pour AuditStore + integration audits dans le SlowMotionDebugger
et la DebugSession.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rich.console import Console

from src.adapters.corpus.certainty_kernel import CertaintyKernel
from src.audit import AuditRecord, AuditStore
from src.core.spectral_core import SpectralMethodCore
from src.core.types import CandidateAnswer, FinalAnswer
from src.multiloop.coherence_detector import CoherenceReport
from src.multiloop.slow_motion_debugger import SlowMotionDebugger
from src.ui.debug_session import DebugSession


THEORIES = str(ROOT / "theories")


@pytest.fixture
def tmp_store(tmp_path: Path) -> AuditStore:
    return AuditStore(base_dir=tmp_path / "audits")


# ============================================================
# AuditRecord : construction et signature
# ============================================================

def test_build_record_assigns_id_and_timestamp():
    rec = AuditStore.build_record(
        intervention_type="verifier",
        question="verifier 26 1/2",
        certified_answer="Le 26-eme premier est 101.",
        position=26,
        prime_value=101,
        ratio="1/2",
    )
    assert len(rec.id) == 8
    assert rec.timestamp.endswith("+00:00") or "T" in rec.timestamp
    assert rec.ratio == "1/2"
    assert rec.signature_sha256
    assert len(rec.signature_sha256) == 64  # SHA-256 hex


def test_build_record_rejects_unsupported_ratio():
    """v2 accepte 1/2, 1/3, 1/4 et 1/2,1/3,1/4. Doit toujours rejeter les autres."""
    with pytest.raises(ValueError):
        AuditStore.build_record(
            intervention_type="test",
            question="x",
            certified_answer="y",
            ratio="1/5",  # inconnu : doit etre rejete
        )


def test_signature_is_deterministic_for_same_content():
    rec1 = AuditStore.build_record(
        intervention_type="test",
        question="q",
        certified_answer="a",
        position=5, prime_value=11,
    )
    # Force le meme id et timestamp pour comparer la signature pure
    rec1_copy = AuditRecord(
        id=rec1.id, timestamp=rec1.timestamp,
        intervention_type=rec1.intervention_type, question=rec1.question,
        ratio=rec1.ratio, position=rec1.position, prime_value=rec1.prime_value,
        certified_answer=rec1.certified_answer,
    )
    rec1_copy.signature_sha256 = rec1_copy.compute_signature()
    assert rec1.signature_sha256 == rec1_copy.signature_sha256


def test_signature_changes_on_tampering():
    rec = AuditStore.build_record(
        intervention_type="t", question="q", certified_answer="a",
        position=5, prime_value=11,
    )
    orig_sig = rec.signature_sha256
    rec.certified_answer = "TAMPERED"
    new_sig = rec.compute_signature()
    assert orig_sig != new_sig


# ============================================================
# AuditStore : persistence
# ============================================================

def test_save_creates_json_file(tmp_store: AuditStore):
    rec = AuditStore.build_record(
        intervention_type="verifier", question="verifier 26",
        certified_answer="ok", position=26, prime_value=101,
    )
    path = tmp_store.save(rec)
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["id"] == rec.id
    assert data["position"] == 26
    assert data["signature_sha256"] == rec.signature_sha256


def test_get_roundtrip(tmp_store: AuditStore):
    rec = AuditStore.build_record(
        intervention_type="verifier", question="q",
        certified_answer="a", position=5, prime_value=11,
    )
    tmp_store.save(rec)
    loaded = tmp_store.get(rec.id)
    assert loaded is not None
    assert loaded.id == rec.id
    assert loaded.signature_sha256 == rec.signature_sha256
    assert tmp_store.verify(loaded) is True


def test_verify_detects_tampering(tmp_store: AuditStore, tmp_path: Path):
    rec = AuditStore.build_record(
        intervention_type="t", question="q", certified_answer="a",
        position=5, prime_value=11,
    )
    path = tmp_store.save(rec)
    # Tamper avec le fichier sur disque
    data = json.loads(path.read_text(encoding="utf-8"))
    data["certified_answer"] = "HACKED"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    loaded = tmp_store.get(rec.id)
    assert tmp_store.verify(loaded) is False


def test_list_records_filters_position(tmp_store: AuditStore):
    for pos, prime in [(5, 11), (26, 101), (5, 11)]:
        rec = AuditStore.build_record(
            intervention_type="t", question="q", certified_answer="a",
            position=pos, prime_value=prime,
        )
        tmp_store.save(rec)
    pos_5 = tmp_store.list_records(position=5)
    pos_26 = tmp_store.list_records(position=26)
    assert len(pos_5) == 2
    assert len(pos_26) == 1


def test_list_records_filters_intervention(tmp_store: AuditStore):
    types = ["verifier", "debug_manual", "verifier", "slow_motion_auto"]
    for t in types:
        rec = AuditStore.build_record(
            intervention_type=t, question="q", certified_answer="a",
            position=5, prime_value=11,
        )
        tmp_store.save(rec)
    veri = tmp_store.list_records(intervention_type="verifier")
    assert len(veri) == 2


def test_list_records_limit(tmp_store: AuditStore):
    for i in range(10):
        rec = AuditStore.build_record(
            intervention_type="t", question=f"q{i}", certified_answer="a",
            position=5, prime_value=11,
        )
        tmp_store.save(rec)
    recs = tmp_store.list_records(limit=3)
    assert len(recs) == 3


# ============================================================
# Citation
# ============================================================

def test_cite_markdown_contains_essential_info(tmp_store: AuditStore):
    rec = AuditStore.build_record(
        intervention_type="verifier", question="verifier 26 1/2",
        certified_answer="Le 26-eme premier est 101.",
        position=26, prime_value=101,
        citations_thy=["methode_spectral.thy::prime_equation_identity"],
        toolkit_reports={"sympy": {"identity_verified": True}},
    )
    tmp_store.save(rec)
    md = tmp_store.cite(rec.id, format="markdown")
    assert rec.id in md
    assert "26" in md
    assert "101" in md
    assert "methode_spectral.thy" in md
    assert "sympy" in md
    assert rec.signature_sha256 in md
    assert "verifiee" in md  # signature valide


def test_cite_latex_format(tmp_store: AuditStore):
    rec = AuditStore.build_record(
        intervention_type="verifier", question="q",
        certified_answer="a", position=26, prime_value=101,
    )
    tmp_store.save(rec)
    latex = tmp_store.cite(rec.id, format="latex")
    assert "\\begin{quote}" in latex
    assert "\\textbf" in latex
    assert "\\end{quote}" in latex


def test_cite_text_format(tmp_store: AuditStore):
    rec = AuditStore.build_record(
        intervention_type="verifier", question="q",
        certified_answer="a", position=26, prime_value=101,
    )
    tmp_store.save(rec)
    text = tmp_store.cite(rec.id, format="text")
    assert "AUDIT" in text
    assert rec.id in text


def test_cite_unknown_id(tmp_store: AuditStore):
    cit = tmp_store.cite("deadbeef", format="markdown")
    assert "introuvable" in cit.lower()


# ============================================================
# Integration : SlowMotionDebugger cree un audit auto
# ============================================================

def _make_final(text: str) -> FinalAnswer:
    return FinalAnswer(
        question_id="t", answer_text=text, structured_data={},
        confidence=0.5, iterations_used=1, best_score=4.0,
        candidates=[CandidateAnswer(
            iteration=0, text="", structured_data={}, used_engines=["llm"],
            score=4.0, critique="",
        )],
        explanation="",
    )


def test_slowmo_creates_audit_when_store_provided(tmp_store: AuditStore):
    debugger = SlowMotionDebugger(
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
        audit_store=tmp_store,
    )
    report = CoherenceReport(score=0.2, incoherent=True, signals=["test"], best_candidate_score=4.0)
    final = _make_final("le 26eme premier est 97 (faux)")
    result = debugger.debug(
        question="Reconstruis le 26eme premier en rapport 1/2",
        final=final, coherence_report=report,
    )
    assert "audit_id" in result.structured_data
    audit_id = result.structured_data["audit_id"]
    loaded = tmp_store.get(audit_id)
    assert loaded is not None
    assert loaded.intervention_type == "slow_motion_auto"
    assert loaded.position == 26
    assert loaded.prime_value == 101


def test_slowmo_skips_audit_when_disabled(tmp_store: AuditStore):
    debugger = SlowMotionDebugger(
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
        audit_store=tmp_store,
    )
    report = CoherenceReport(score=0.2, incoherent=True, signals=[], best_candidate_score=4.0)
    final = _make_final("x")
    result = debugger.debug(
        question="Reconstruis le 26eme premier en rapport 1/2",
        final=final, coherence_report=report,
        skip_auto_audit=True,
    )
    assert "audit_id" not in result.structured_data


# ============================================================
# Integration : DebugSession.verifier_position cree un audit
# ============================================================

@pytest.mark.asyncio
async def test_verifier_creates_audit(tmp_store: AuditStore):
    session = DebugSession(
        console=Console(force_terminal=False, no_color=True),
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
        audit_store=tmp_store,
    )
    audit_id = await session.verifier_position(position=26, ratio="1/2")
    assert audit_id is not None
    rec = tmp_store.get(audit_id)
    assert rec is not None
    assert rec.intervention_type == "verifier"
    assert rec.position == 26
    assert rec.prime_value == 101
    assert "sympy" in rec.toolkit_reports or "mpmath" in rec.toolkit_reports


@pytest.mark.asyncio
async def test_verifier_rejects_unsupported_ratio(tmp_store: AuditStore):
    session = DebugSession(
        console=Console(force_terminal=False, no_color=True),
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
        audit_store=tmp_store,
    )
    audit_id = await session.verifier_position(position=26, ratio="1/3")
    assert audit_id is None


# ============================================================
# Integration : DebugSession execute => audit "debug_manual"
# ============================================================

@pytest.mark.asyncio
async def test_debug_session_creates_manual_audit(tmp_store: AuditStore):
    session = DebugSession(
        console=Console(force_terminal=False, no_color=True),
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
        audit_store=tmp_store,
    )
    inputs = iter(["c", "verification croisee Wolfram", "e"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 26eme premier en rapport 1/2")
    assert result is not None
    audit_id = result.structured_data.get("audit_id")
    assert audit_id is not None
    rec = tmp_store.get(audit_id)
    assert rec.intervention_type == "debug_manual"
    assert rec.user_comment == "verification croisee Wolfram"
    assert rec.position == 26
    # Verifier la signature
    assert tmp_store.verify(rec) is True

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
