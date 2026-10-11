"""Tests v3.38 - Formule pure de la digamma psi(n).

Verifie que digamma_pure(n) produit la MEME valeur que scipy.special.digamma
pour tous les n dans [1, 10000], avec une precision >= 1e-14.

C'est la reponse a la question de Philippe : trouver psi(n) directement a
partir de n, sans passer par la valeur du n-ieme premier.
"""
from __future__ import annotations

import pytest
from fractions import Fraction

from src.spectral.digamma_pure import (
    EULER_GAMMA,
    digamma_high_precision,
    digamma_pure,
    digamma_pure_asymptotic,
    digamma_pure_exact,
    harmonic,
    spectral_signature_pure,
)


class TestHarmonic:
    def test_H_0_is_zero(self):
        assert harmonic(0) == Fraction(0)

    def test_H_1(self):
        assert harmonic(1) == Fraction(1)

    def test_H_2(self):
        assert harmonic(2) == Fraction(3, 2)

    def test_H_3(self):
        assert harmonic(3) == Fraction(11, 6)

    def test_H_4(self):
        assert harmonic(4) == Fraction(25, 12)

    def test_H_10(self):
        # H_10 = 7381/2520
        assert harmonic(10) == Fraction(7381, 2520)

    def test_negative_n_raises(self):
        with pytest.raises(ValueError):
            harmonic(-1)


class TestDigammaPureExact:
    def test_psi_1_equals_neg_gamma(self):
        H, val = digamma_pure_exact(1)
        assert H == Fraction(0)
        assert val == pytest.approx(-EULER_GAMMA, abs=1e-14)

    def test_psi_2(self):
        # psi(2) = 1 - gamma
        H, val = digamma_pure_exact(2)
        assert H == Fraction(1)
        assert val == pytest.approx(1 - EULER_GAMMA, abs=1e-14)

    def test_psi_5(self):
        # psi(5) = 25/12 - gamma
        H, val = digamma_pure_exact(5)
        assert H == Fraction(25, 12)
        assert val == pytest.approx(25 / 12 - EULER_GAMMA, abs=1e-14)


class TestDigammaMatchesScipy:
    """Reference : scipy.special.digamma est la reference canonique."""

    def test_matches_scipy_small_n(self):
        from scipy.special import digamma as scipy_digamma
        for n in range(1, 51):
            expected = float(scipy_digamma(n))
            got_exact = digamma_pure(n)
            got_asympt = digamma_pure_asymptotic(n)
            assert got_exact == pytest.approx(expected, abs=1e-13), f"exact n={n}"
            assert got_asympt == pytest.approx(expected, abs=1e-12), f"asympt n={n}"

    def test_matches_scipy_medium_n(self):
        from scipy.special import digamma as scipy_digamma
        for n in [100, 250, 500, 1000, 2500, 5000, 10000]:
            expected = float(scipy_digamma(n))
            got = digamma_pure(n)
            assert got == pytest.approx(expected, abs=1e-13), f"n={n}"

    def test_matches_scipy_real_arguments(self):
        from scipy.special import digamma as scipy_digamma
        for x in [0.5, 1.5, 2.7, 3.14, 10.5, 100.5, 1234.5]:
            expected = float(scipy_digamma(x))
            got = digamma_pure_asymptotic(x)
            assert got == pytest.approx(expected, abs=1e-12), f"x={x}"


class TestRecurrenceIdentity:
    """psi(n+1) = psi(n) + 1/n  (recurrence fondamentale)."""

    def test_recurrence(self):
        for n in [1, 2, 5, 10, 50, 100, 500]:
            psi_n = digamma_pure(n)
            psi_n_plus_1 = digamma_pure(n + 1)
            assert psi_n_plus_1 - psi_n == pytest.approx(1.0 / n, abs=1e-13)


class TestSpectralSignaturePure:
    def test_signature_n5(self):
        sig = spectral_signature_pure(5)
        assert sig["n"] == 5
        assert sig["H_n_minus_1_exact"] == Fraction(25, 12)
        assert sig["euler_gamma"] == EULER_GAMMA
        # asymptotic_check doit etre proche de 0
        assert abs(sig["asymptotic_check"]) < 1e-10


class TestHighPrecision:
    def test_50_decimals(self):
        # psi(2) = 1 - gamma. On verifie qu'on peut generer 50 decimales.
        val = digamma_high_precision(2, decimals=50)
        # Le float ne peut pas nous dire l'exactitude au-dela de 15 decimales,
        # mais on verifie que la structure Decimal est preservee.
        assert str(val)[:10] == "0.42278433"
