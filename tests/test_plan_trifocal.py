"""Tests pour src/spectral/plan_trifocal.py (Section X methode_spectral.thy)."""
from __future__ import annotations

from fractions import Fraction

import pytest

from src.spectral import (
    PlanTrifocal, TrifocalAxis, TrifocalValidation,
    POSTULATES, AXIS_DESCRIPTIONS,
)


# ==========================================================================
# Axes & postulats (lecture seule)
# ==========================================================================
class TestTrifocalAxes:
    def test_three_axes(self):
        axes = PlanTrifocal.axes()
        assert set(axes.keys()) == {"FZg", "HyRi", "MsP"}

    def test_axis_descriptions_non_empty(self):
        for axis in TrifocalAxis:
            assert AXIS_DESCRIPTIONS[axis]
            assert len(AXIS_DESCRIPTIONS[axis]) > 20


class TestPostulates:
    def test_five_postulates(self):
        assert len(POSTULATES) == 5
        codes = {p.code for p in POSTULATES}
        assert codes == {"P1", "P2", "P3", "P4", "P5"}

    def test_postulate_p1_concerns_fzg_and_msp(self):
        p1 = next(p for p in POSTULATES if p.code == "P1")
        assert TrifocalAxis.FZG in p1.axes
        assert TrifocalAxis.MSP in p1.axes

    def test_postulate_p2_about_demi(self):
        p2 = next(p for p in POSTULATES if p.code == "P2")
        assert "1/2" in p2.statement

    def test_postulate_p5_courbure(self):
        p5 = next(p for p in POSTULATES if p.code == "P5")
        assert "HypR_demi_solFinal" in p5.statement or "courbure" in p5.statement.lower()


# ==========================================================================
# Validation epipolaire (necessite spectral_core)
# ==========================================================================
class _FakeSpectralCore:
    """Minimal pour fournir get_prime_at_position."""
    def __init__(self, prime_at):
        self._prime_at = prime_at

    def get_prime_at_position(self, n: int):
        return self._prime_at.get(n)


class TestValidate:
    def setup_method(self):
        # 10e premier = 29, 26e = 101
        self.core = _FakeSpectralCore({10: 29, 26: 101, 1: 2})
        self.plan = PlanTrifocal(spectral_core=self.core)

    def test_validate_n10_modele_1_2_full_coherent(self):
        v = self.plan.validate(n=10, model_name="1/2")
        assert v.n == 10
        assert v.prime == 29
        assert v.msp_demi == Fraction(1, 2)
        assert v.hypR_demi == Fraction(1, 2)
        assert v.msp_equation_holds is True
        assert v.p1_positions_match is True
        assert v.p2_demi_equal is True
        assert v.epipolar_coherent is True

    def test_validate_n26_modele_1_2_coherent(self):
        v = self.plan.validate(n=26, model_name="1/2")
        assert v.prime == 101
        assert v.epipolar_coherent is True

    def test_validate_modele_1_3_p2_fail(self):
        """Modele 1/3 -> demi=1/3 != HypR_demi=1/2 donc P2 echoue."""
        v = self.plan.validate(n=10, model_name="1/3")
        assert v.msp_equation_holds is True
        assert v.msp_demi == Fraction(1, 3)
        assert v.p2_demi_equal is False  # 1/3 != 1/2
        assert v.epipolar_coherent is False

    def test_validate_modele_1_4_p2_fail(self):
        v = self.plan.validate(n=26, model_name="1/4")
        assert v.msp_demi == Fraction(1, 4)
        assert v.p2_demi_equal is False
        assert v.epipolar_coherent is False

    def test_validate_position_invalide(self):
        plan = PlanTrifocal(spectral_core=_FakeSpectralCore({}))
        with pytest.raises(ValueError):
            plan.validate(n=999, model_name="1/2")

    def test_validate_n_zero(self):
        with pytest.raises(ValueError):
            self.plan.validate(n=0, model_name="1/2")

    def test_validate_to_text(self):
        v = self.plan.validate(n=10, model_name="1/2")
        text = v.to_text()
        assert "n=10" in text
        assert "VALIDE" in text


# ==========================================================================
# Lien Riemann (texte)
# ==========================================================================
class TestRiemannLink:
    def test_riemann_statement_has_three_axes(self):
        text = PlanTrifocal.riemann_link_statement()
        assert "FZg" in text
        assert "HyRi" in text
        assert "MsP" in text

    def test_riemann_statement_has_five_postulates(self):
        text = PlanTrifocal.riemann_link_statement()
        for code in ("P1", "P2", "P3", "P4", "P5"):
            assert code in text

    def test_riemann_statement_has_demi(self):
        text = PlanTrifocal.riemann_link_statement()
        assert "1/2" in text


# ==========================================================================
# EpistemicClaim integration (Axe 4)
# ==========================================================================
class TestEpistemicClaim:
    def setup_method(self):
        self.core = _FakeSpectralCore({10: 29})
        self.plan = PlanTrifocal(spectral_core=self.core)

    def test_claim_certain_when_coherent(self):
        from src.cognitive import Certainty
        v = self.plan.validate(n=10, model_name="1/2")
        claim = self.plan.epistemic_claim(v)
        assert claim.certainty == Certainty.CERTAIN
        assert claim.can_cite() is True

    def test_claim_conjecture_for_1_3(self):
        from src.cognitive import Certainty
        v = self.plan.validate(n=10, model_name="1/3")
        claim = self.plan.epistemic_claim(v)
        # MsP OK mais P2 KO -> CONJECTURE
        assert claim.certainty == Certainty.CONJECTURE
        assert claim.limits  # contient des limites

    def test_claim_hors_domaine_when_msp_fails(self):
        from src.cognitive import Certainty
        # Forcer un echec MsP en mockant le retour
        v = TrifocalValidation(
            n=5, prime=11, model_name="1/2",
            msp_demi=Fraction(1, 2), hypR_demi=Fraction(1, 2),
            p1_positions_match=False, p2_demi_equal=True,
            msp_equation_holds=False, epipolar_coherent=False,
            details={},
        )
        claim = self.plan.epistemic_claim(v)
        assert claim.certainty == Certainty.HORS_DOMAINE
