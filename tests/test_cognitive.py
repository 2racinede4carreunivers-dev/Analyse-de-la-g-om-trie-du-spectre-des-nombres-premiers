"""Tests pour src/cognitive/ : ProofTrace, RegimeOntology, Epistemic, MetaReasoner."""
from __future__ import annotations

from pathlib import Path

import pytest

from src.cognitive import (
    ProofTrace, ProofStep, check_invariant,
    RegimeOntology, RegimeRelation,
    Certainty, EpistemicClaim, mark_claim,
    MetaReasoner, ConfidenceLevel,
)
from src.cognitive.epistemic import Provenance


# ==========================================================================
# Axe 2 : ProofTrace
# ==========================================================================
class TestProofTrace:
    def test_create_and_add_steps(self):
        trace = ProofTrace(title="Reconstruction p=29 via modele 1/2")
        trace.hypotheses = ["n=5", "p=29"]
        step = trace.add_step(
            "SB_eval", input_state={"n": 5}, output_state={"SB": 38.0},
            justification="SB(5) = (13/4)*32 - 66 = 38",
        )
        assert step.step_number == 1
        assert len(trace.steps) == 1

    def test_invariant_check_passes(self):
        trace = ProofTrace(title="Test invariant")
        assert trace.check_invariant("symetrie", True, "OK")
        assert trace.is_valid is True

    def test_invariant_check_fails(self):
        trace = ProofTrace(title="Test invariant fail")
        trace.check_invariant("ratio == 1/2", False, "ratio = 1/3 inattendu")
        assert trace.is_valid is False

    def test_to_text_format(self):
        trace = ProofTrace(title="Demo")
        trace.hypotheses = ["h1"]
        trace.add_step("rule_x", {"a": 1}, {"b": 2}, "justification")
        trace.check_invariant("inv1", True, "ok")
        trace.conclude("Demo OK")
        txt = trace.to_text()
        assert "PROOF TRACE : Demo" in txt
        assert "rule_x" in txt
        assert "inv1" in txt
        assert "VALID" in txt

    def test_standalone_check_invariant(self):
        r = check_invariant("test", True, "ok")
        assert r["passed"] is True


# ==========================================================================
# Axe 3 : RegimeOntology
# ==========================================================================
class TestRegimeOntology:
    @pytest.fixture
    def onto(self) -> RegimeOntology:
        return RegimeOntology()

    def test_get_entity(self, onto):
        e = onto.get("modele_1_2")
        assert e.niveau == "modele"
        assert e.parent == "univers_spectral"

    def test_get_invalid_raises(self, onto):
        with pytest.raises(ValueError):
            onto.get("inexistant")

    def test_ancestors(self, onto):
        ancestors = onto.ancestors("bloc_symetrique")
        assert "regime_positif" in ancestors
        assert "modele_1_2" in ancestors
        assert "univers_spectral" in ancestors

    def test_relations_modele_extension(self, onto):
        rels = onto.relations_of("modele_1_4")
        # 1/4 etend 1/2
        assert (RegimeRelation.EXTENSION, "modele_1_2") in rels

    def test_compatibility(self, onto):
        # bloc_sym et bloc_chaos sont incompatibles
        assert not onto.is_compatible("bloc_symetrique", "bloc_chaotique")
        # bloc_sym et regime_positif sont compatibles (specialisation)
        assert onto.is_compatible("bloc_symetrique", "regime_positif")

    def test_list_by_level(self, onto):
        modeles = onto.list_by_level("modele")
        assert set(modeles) == {"modele_1_2", "modele_1_3", "modele_1_4"}


# ==========================================================================
# Axe 4 : Epistemic
# ==========================================================================
class TestEpistemic:
    def test_certain_claim_citable(self):
        c = mark_claim(
            "prime(26) = 101",
            Certainty.CERTAIN,
            provenance=Provenance.SPECTRAL_CORE,
            evidence={"n": 26, "p": 101},
        )
        assert c.can_cite() is True

    def test_conjecture_not_citable(self):
        c = mark_claim(
            "Tous les zeros sont sur Re=1/2",
            Certainty.CONJECTURE,
            provenance=Provenance.LLM_CLAUDE,
        )
        assert c.can_cite() is False

    def test_hors_domaine_not_citable(self):
        c = mark_claim("Je ne sais pas X", Certainty.HORS_DOMAINE)
        assert c.can_cite() is False

    def test_to_text_format(self):
        c = mark_claim(
            "x=42", Certainty.CERTAIN, Provenance.CERTAINTY_KERNEL,
            evidence={"calc": "42"}, limits=["domaine restreint"],
        )
        txt = c.to_text()
        assert "[CERTAIN]" in txt
        assert "CertaintyKernel" in txt
        assert "domaine restreint" in txt

    def test_llm_only_not_citable(self):
        """Une affirmation venant uniquement du LLM ne doit pas etre citable."""
        c = mark_claim(
            "stmt", Certainty.CERTAIN,
            provenance=[Provenance.LLM_CLAUDE, Provenance.LLM_OPENAI],
        )
        assert c.can_cite() is False


# ==========================================================================
# Axe 5 : MetaReasoner
# ==========================================================================
class TestMetaReasoner:
    @pytest.fixture
    def meta(self, tmp_path: Path) -> MetaReasoner:
        return MetaReasoner(
            errors_file=tmp_path / "errors.jsonl",
            stats_file=tmp_path / "stats.json",
        )

    def test_initial_confidence_unknown(self, meta):
        assert meta.get_confidence("reconstruction_1_2") == ConfidenceLevel.UNKNOWN

    def test_record_success(self, meta):
        for _ in range(5):
            meta.record("gap_pos_pos", success=True)
        assert meta.get_confidence("gap_pos_pos") == ConfidenceLevel.HIGH

    def test_record_partial_success(self, meta):
        # 7 succes / 10 -> 70% -> MEDIUM
        for i in range(10):
            meta.record("ratio_chaos", success=(i < 7))
        assert meta.get_confidence("ratio_chaos") == ConfidenceLevel.MEDIUM

    def test_record_failures_low_confidence(self, meta):
        # 2 succes / 10 -> 20% -> LOW
        for i in range(10):
            meta.record("riemann_conjecture", success=(i < 2))
        assert meta.get_confidence("riemann_conjecture") == ConfidenceLevel.LOW

    def test_should_activate_slow_motion(self, meta):
        # 1/5 succes -> LOW -> active slow motion
        for i in range(5):
            meta.record("riemann_conjecture", success=(i < 1))
        assert meta.should_activate_slow_motion("riemann_conjecture") is True

    def test_report_contains_all_default_categories(self, meta):
        rep = meta.report()
        assert "reconstruction_1_2" in rep
        assert "gap_pos_pos" in rep
        assert "isabelle_proof" in rep

    def test_persistence_errors_file(self, meta, tmp_path):
        meta.record("gap_pos_pos", success=False, details={"question": "gap(0,0)"})
        errors_file = tmp_path / "errors.jsonl"
        assert errors_file.exists()
        content = errors_file.read_text(encoding="utf-8")
        assert "gap_pos_pos" in content

    def test_persistence_stats_reload(self, tmp_path):
        m1 = MetaReasoner(
            errors_file=tmp_path / "e.jsonl",
            stats_file=tmp_path / "s.json",
        )
        for _ in range(5):
            m1.record("gap_pos_pos", success=True)
        # Reload : verifier que les stats persistent
        m2 = MetaReasoner(
            errors_file=tmp_path / "e.jsonl",
            stats_file=tmp_path / "s.json",
        )
        assert m2.stats["gap_pos_pos"].total == 5
        assert m2.stats["gap_pos_pos"].successes == 5
