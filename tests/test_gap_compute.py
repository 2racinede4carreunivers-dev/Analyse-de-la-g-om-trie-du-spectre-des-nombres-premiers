"""Tests pour la commande gap (ecart spectral direct sans LLM)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.spectral.gap_compute import compute_gap, render_gap_report, _resolve_input
from src.spectral.prime_table import nth_prime


def test_resolve_input_as_position():
    pos, prime = _resolve_input(26)
    assert pos == 26
    assert prime == 101  # 26e premier


def test_resolve_input_position_5():
    pos, prime = _resolve_input(5)
    assert pos == 5
    assert prime == 11


def test_resolve_input_as_prime_when_not_in_position_range():
    # 1009 est un prime mais hors range position (1..1000)
    pos, prime = _resolve_input(1009)
    assert prime == 1009
    # Doit etre la position correcte
    assert nth_prime(pos) == 1009


def test_resolve_input_rejects_invalid():
    with pytest.raises(ValueError):
        _resolve_input(0)
    with pytest.raises(ValueError):
        # 1500 n'est ni une position valide (>1000) ni un prime
        _resolve_input(1500)


def test_compute_gap_two_positions():
    result = compute_gap(26, 56, ratio="1/2")
    assert result.point1.position == 26
    assert result.point1.prime == 101
    assert result.point2.position == 56
    assert result.point2.prime == 263  # 56e premier
    assert result.delta_n == 30
    assert result.delta_p == 263 - 101


def test_compute_gap_invariant_holds():
    """L'INVARIANT 1/2 doit etre verifie : delta_SA / delta_SB == 1/2."""
    for v1, v2 in [(5, 10), (26, 56), (100, 200), (50, 150)]:
        result = compute_gap(v1, v2, ratio="1/2")
        assert result.invariant_ok, \
            f"INVARIANT 1/2 viole pour ({v1},{v2}) : RsP={result.rsP_fraction}"
        assert result.rsP_fraction == "1/2"


def test_compute_gap_rejects_identical():
    with pytest.raises(ValueError):
        compute_gap(26, 26, ratio="1/2")


def test_compute_gap_rejects_unsupported_ratio():
    with pytest.raises(ValueError):
        compute_gap(26, 56, ratio="1/3")


def test_compute_gap_render_text():
    result = compute_gap(26, 56, ratio="1/2")
    text = render_gap_report(result)
    assert "ECART SPECTRAL" in text
    assert "1/2" in text
    assert "[OK]" in text
    assert "26" in text and "56" in text
    assert "101" in text and "263" in text


def test_compute_gap_with_prime_values():
    """Si on passe des primes au-dela de la table position, doit fonctionner."""
    # 1009 est le 169e premier
    result = compute_gap(1009, 1013, ratio="1/2")
    assert result.point1.prime == 1009
    assert result.point2.prime == 1013
    assert result.invariant_ok


def test_compute_gap_D_calculation():
    """D(n,p) = SB(n) - SA(n) - 64*p doit etre coherent entre les deux points."""
    result = compute_gap(26, 56, ratio="1/2")
    # delta_D = D2 - D1
    expected_delta = result.point2.D - result.point1.D
    assert abs(result.delta_D - expected_delta) < 1e-6

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
