"""Tests pour le debug_toolkit : sympy, mpmath, z3."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.debug_toolkit import (
    MpmathValidator, SympyValidator, ToolkitRegistry, Z3Prover,
)
from src.spectral.prime_table import nth_prime


# ============================================================
# Registry
# ============================================================

def test_registry_detects_installed_tools():
    reg = ToolkitRegistry()
    # sympy et mpmath sont des dependances obligatoires
    assert reg.is_available("sympy")
    assert reg.is_available("mpmath")
    # z3 doit etre dispo (ajoute dans requirements.txt)
    assert reg.is_available("z3"), "z3-solver devrait etre installe via requirements.txt"


def test_registry_render_includes_all_tools():
    reg = ToolkitRegistry()
    text = reg.render_table()
    assert "sympy" in text
    assert "mpmath" in text
    assert "z3" in text


# ============================================================
# SympyValidator
# ============================================================

def test_sympy_validator_position_26():
    """Verifie SA(26), SB(26) et l'identite pour le 26e premier = 101."""
    v = SympyValidator()
    report = v.validate(position=26, ratio="1/2", prime=101)
    assert report["supported"]
    # SA(26) = 13/8 * 2^26 - 2 = 13 * 2^23 - 2 = 109051902
    assert report["SA"] == 13 * (2 ** 23) - 2
    # SB(26) = 13/4 * 2^26 - 66 = 13 * 2^24 - 66 = 218103742
    assert report["SB"] == 13 * (2 ** 24) - 66
    assert report["identity_verified"] is True
    assert report["P_reconstruit"] == 101


def test_sympy_validator_position_5():
    """5e premier = 11."""
    v = SympyValidator()
    report = v.validate(position=5, ratio="1/2", prime=11)
    assert report["supported"]
    assert report["identity_verified"] is True
    assert report["P_reconstruit"] == 11


def test_sympy_validator_rejects_unsupported_ratio():
    v = SympyValidator()
    report = v.validate(position=5, ratio="1/3", prime=11)
    assert not report["supported"]


def test_sympy_render_text():
    v = SympyValidator()
    report = v.validate(position=26, ratio="1/2", prime=101)
    text = v.render(report)
    assert "26" in text
    assert "sympy" in text.lower()
    assert "OK" in text


# ============================================================
# MpmathValidator
# ============================================================

def test_mpmath_validator_matches_sympy():
    """Pour des positions raisonnables, mpmath et sympy doivent concorder."""
    mp_v = MpmathValidator(precision=80)
    sp_v = SympyValidator()
    for pos in [5, 26, 100]:
        prime = nth_prime(pos)
        mp_report = mp_v.validate(pos, "1/2", prime)
        sp_report = sp_v.validate(pos, "1/2", prime)
        assert mp_report["supported"] and sp_report["supported"]
        # Pour grands n, comparer via la representation entiere de mpmath
        # (float perdrait des chiffres - precisement pourquoi mpmath existe).
        import mpmath
        sa_mpf = mpmath.mpf(mp_report["SA"])
        sb_mpf = mpmath.mpf(mp_report["SB"])
        assert int(sa_mpf) == sp_report["SA"], f"pos={pos} : SA mismatch"
        assert int(sb_mpf) == sp_report["SB"], f"pos={pos} : SB mismatch"
        assert mp_report["identity_verified"] is True


def test_mpmath_high_precision_large_position():
    """Position 500 : mpmath doit garder la precision."""
    v = MpmathValidator(precision=200)
    prime = nth_prime(500)
    report = v.validate(500, "1/2", prime)
    assert report["supported"]
    assert report["identity_verified"] is True


def test_mpmath_render_text():
    v = MpmathValidator()
    report = v.validate(26, "1/2", 101)
    text = v.render(report)
    assert "mpmath" in text.lower()
    assert "OK" in text


# ============================================================
# Z3Prover
# ============================================================

def test_z3_available():
    assert Z3Prover.is_available()


def test_z3_proves_invariant_1_2():
    p = Z3Prover()
    report = p.prove_invariant_1_2(position=26)
    assert report["supported"]
    assert report["proven"] is True
    assert report["counter_example"] is None


def test_z3_proves_reconstruction_identity():
    p = Z3Prover()
    report = p.prove_reconstruction_identity()
    assert report["supported"]
    assert report["proven"] is True


def test_z3_validate_full():
    p = Z3Prover()
    report = p.validate(position=26, ratio="1/2", prime=101)
    assert report["supported"]
    assert report["all_proven"] is True


def test_z3_rejects_unsupported_ratio():
    p = Z3Prover()
    report = p.validate(position=26, ratio="1/3", prime=101)
    assert not report["supported"]


def test_z3_render_text():
    p = Z3Prover()
    report = p.validate(26, "1/2", 101)
    text = p.render(report)
    assert "z3" in text.lower()
    assert "PROUVE" in text


# ============================================================
# Cross-validation : 3 outils doivent etre d'accord
# ============================================================

def test_three_tools_agree_on_position_26():
    """sympy, mpmath et z3 doivent tous valider la reconstruction du 26e premier."""
    pos, prime = 26, 101
    sp_v = SympyValidator()
    mp_v = MpmathValidator()
    z3_v = Z3Prover()
    sp_report = sp_v.validate(pos, "1/2", prime)
    mp_report = mp_v.validate(pos, "1/2", prime)
    z3_report = z3_v.validate(pos, "1/2", prime)
    assert sp_report["identity_verified"] is True
    assert mp_report["identity_verified"] is True
    assert z3_report["all_proven"] is True

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
