"""Tests pour src/cognitive/engine_bridge.py (Axes 2/3/4/5 integration).

Couvre :
  - build_gap_result : trace + claim + categorie + regime
  - build_reconstruct_result : succes/echec, certainty
  - build_rsp_1x1_result
  - record_cognitive_result -> MetaReasoner stats
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from src.cognitive import (
    Certainty,
    Provenance,
    build_gap_result,
    build_reconstruct_result,
    build_rsp_1x1_result,
    get_meta_reasoner,
    record_cognitive_result,
    reset_meta_reasoner,
)
from src.cognitive.engine_bridge import _regime_for_gap


# ==========================================================================
# build_gap_result
# ==========================================================================
class TestBuildGapResult:
    def test_gap_positive_certain(self):
        res = build_gap_result(11, 23)
        assert res.value == 11
        assert res.claim.certainty == Certainty.CERTAIN
        assert Provenance.SPECTRAL_CORE in res.claim.provenance
        assert res.category == "gap_pos_pos"
        assert res.regime == "regime_positif"
        assert res.is_valid is True
        # La trace contient les invariants symetrie/positivite
        names = {i["name"] for i in res.proof_trace.invariants_checked}
        assert "symetrie" in names
        assert "positivite" in names

    def test_gap_neg_neg(self):
        res = build_gap_result(-19, -5)
        assert res.value == 13
        assert res.category == "gap_neg_neg"
        assert res.regime == "regime_negatif"
        assert res.claim.certainty == Certainty.CERTAIN

    def test_gap_mixed(self):
        res = build_gap_result(-7, 11)
        assert res.value == 17
        assert res.category == "gap_mixed"
        assert res.regime == "regime_mixte"

    def test_gap_self_zero(self):
        res = build_gap_result(5, 5)
        assert res.value == 0
        assert res.claim.certainty == Certainty.CERTAIN

    def test_gap_claim_citable(self):
        res = build_gap_result(11, 23)
        assert res.claim.can_cite() is True


# ==========================================================================
# build_reconstruct_result
# ==========================================================================
class TestBuildReconstructResult:
    def test_reconstruct_1_2_certain(self):
        # 10e premier = 29
        res = build_reconstruct_result(n=10, actual_prime=29, model_name="1/2")
        assert res.value == 29
        assert res.claim.certainty == Certainty.CERTAIN
        assert res.category == "reconstruction_1_2"
        assert res.regime == "modele_1_2"
        assert res.is_valid is True

    def test_reconstruct_1_3(self):
        res = build_reconstruct_result(n=10, actual_prime=29, model_name="1/3")
        assert res.value == 29
        assert res.category == "reconstruction_1_3"
        assert res.claim.certainty == Certainty.CERTAIN

    def test_reconstruct_1_4(self):
        res = build_reconstruct_result(n=26, actual_prime=101, model_name="1/4")
        assert res.value == 101
        assert res.category == "reconstruction_1_4"
        assert res.regime == "modele_1_4"


# ==========================================================================
# build_rsp_1x1_result
# ==========================================================================
class TestBuildRsp1x1Result:
    def test_rsp_1x1_exact_1_2(self):
        res = build_rsp_1x1_result(3, 5, model_name="1/2")
        from fractions import Fraction
        assert res.value == Fraction(1, 2)
        assert res.claim.certainty == Certainty.CERTAIN
        assert res.category == "ratio_1x1"
        assert res.regime == "modele_1_2"

    def test_rsp_1x1_exact_1_3(self):
        res = build_rsp_1x1_result(3, 5, model_name="1/3")
        from fractions import Fraction
        assert res.value == Fraction(1, 3)
        assert res.claim.certainty == Certainty.CERTAIN

    def test_rsp_1x1_exact_1_4(self):
        res = build_rsp_1x1_result(3, 5, model_name="1/4")
        from fractions import Fraction
        assert res.value == Fraction(1, 4)
        assert res.claim.certainty == Certainty.CERTAIN

    def test_rsp_1x1_indices_egaux_hors_domaine(self):
        # n1 == n2 => RsP indefini
        res = build_rsp_1x1_result(5, 5, model_name="1/2")
        assert res.claim.certainty == Certainty.HORS_DOMAINE
        assert res.is_valid is False


# ==========================================================================
# MetaReasoner enregistrement
# ==========================================================================
class TestMetaReasonerIntegration:
    def setup_method(self):
        # Repartir d'un MetaReasoner propre dans un tmpdir
        reset_meta_reasoner()
        self._tmp = tempfile.mkdtemp(prefix="meta_test_")
        self.meta = get_meta_reasoner(learning_dir=self._tmp)

    def test_record_gap_success(self):
        res = build_gap_result(11, 23)
        record_cognitive_result(res, meta=self.meta)
        stats = self.meta.report()
        assert stats["gap_pos_pos"]["total"] == 1
        assert stats["gap_pos_pos"]["successes"] == 1

    def test_record_multiple_categories(self):
        record_cognitive_result(build_gap_result(11, 23), meta=self.meta)
        record_cognitive_result(build_gap_result(-19, -5), meta=self.meta)
        record_cognitive_result(
            build_reconstruct_result(10, 29, "1/2"), meta=self.meta,
        )
        stats = self.meta.report()
        assert stats["gap_pos_pos"]["total"] == 1
        assert stats["gap_neg_neg"]["total"] == 1
        assert stats["reconstruction_1_2"]["total"] == 1

    def test_record_failure_logs_error(self):
        # RsP 1x1 avec n1==n2 -> claim HORS_DOMAINE -> success=False
        res = build_rsp_1x1_result(5, 5, model_name="1/2")
        record_cognitive_result(res, meta=self.meta)
        stats = self.meta.report()
        assert stats["ratio_1x1"]["total"] == 1
        assert stats["ratio_1x1"]["successes"] == 0
        # Et un fichier d'erreur a ete cree
        errors_file = Path(self._tmp) / "errors.jsonl"
        assert errors_file.exists()


# ==========================================================================
# Helpers Axe 3
# ==========================================================================
class TestRegimeMapping:
    def test_regime_pos_pos(self):
        cat, reg = _regime_for_gap(11, 23)
        assert cat == "gap_pos_pos"
        assert reg == "regime_positif"

    def test_regime_neg_neg(self):
        cat, reg = _regime_for_gap(-19, -5)
        assert cat == "gap_neg_neg"
        assert reg == "regime_negatif"

    def test_regime_mixed(self):
        cat, reg = _regime_for_gap(-7, 11)
        assert cat == "gap_mixed"
        assert reg == "regime_mixte"
