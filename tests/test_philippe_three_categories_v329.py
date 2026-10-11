"""Tests v3.29 : les 3 categories obligatoires de Philippe (2026-02).

Philippe a identifie 3 categories de questions que Gabriel DOIT resoudre :
  1. Reconstruction du i-ieme premier
  2. Rapport spectral (symetrique n*n, asymetrique chaotique, asymetrique ordonnee)
  3. Ecart entre premiers
"""
from __future__ import annotations

import pytest

from src.core.spectral_core import SpectralMethodCore


@pytest.fixture(scope="module")
def core() -> SpectralMethodCore:
    return SpectralMethodCore()


# =====================================================================
# Q1 : RECONSTRUCTION DU i-IEME PREMIER
# =====================================================================


class TestReconstruction:

    @pytest.mark.parametrize("n,p_expected", [
        (1, 2), (2, 3), (5, 11), (10, 29), (33, 137), (100, 541),
    ])
    def test_reconstruction_correct(self, core, n, p_expected):
        data = core.reconstruct_prime_1_2(n)
        assert data is not None, f"reconstruct_prime_1_2({n}) doit retourner PrimeSpectralData"
        assert data.prime_value == p_expected, (
            f"n={n} : reconstruction = {data.prime_value}, attendu = {p_expected}"
        )


# =====================================================================
# Q2 : RAPPORT SPECTRAL (3 MODES)
# =====================================================================


class TestRapportSpectralSymetrique:
    """Nouvelle methode compute_RsP_bloc_sym (v3.29)."""

    def test_2x2_near_half(self, core):
        r = core.compute_RsP_bloc_sym([2, 3], [5, 7])
        assert "RsP_decimal" in r
        assert r["near_half"], f"Sym 2x2 doit etre proche de 1/2, obtenu {r['RsP_decimal']}"

    def test_3x3_near_half(self, core):
        r = core.compute_RsP_bloc_sym([1, 2, 3], [4, 5, 6])
        assert r["near_half"], f"Sym 3x3 doit etre proche de 1/2, obtenu {r['RsP_decimal']}"

    def test_config_string(self, core):
        r = core.compute_RsP_bloc_sym([1, 2, 3], [4, 5, 6])
        assert r["configuration"] == "sym_3x3"
        assert r["n_size"] == 3

    def test_asymmetric_rejected(self, core):
        r = core.compute_RsP_bloc_sym([1, 2], [3, 4, 5])
        assert "error" in r, "|A| != |B| doit renvoyer une erreur"

    def test_theorem_reference(self, core):
        r = core.compute_RsP_bloc_sym([2, 3], [5, 7])
        assert "methode_spectral.thy" in r["theorem_reference"]


class TestRapportSpectralChaotique:
    """Verifie que le mode chaotique existant continue de fonctionner."""

    def test_chaotique_7_3_vs_11_23_13(self, core):
        r = core.compute_RsP_bloc_asym([7, 3], [11, 23, 13])
        assert r["near_half"]
        assert abs(r["RsP_decimal"] - 0.5) < 0.01
        assert r["configuration"] == "asym_chaotique"


class TestRapportSpectralOrdonnee:
    """Verifie que le mode ordonnee (|B|=|A|+1, chronologique) fonctionne."""

    def test_ordonnee_2_3_vs_5_7_11(self, core):
        r = core.compute_RsP_ordonnee([2, 3], [5, 7, 11])
        assert "error" not in r
        assert r["configuration"] == "asym_ordonnee"


# =====================================================================
# Q3 : ECARTS ENTRE PREMIERS
# =====================================================================


class TestGapDirect:
    """Nouvelle methode compute_gap_between_primes (v3.29)."""

    @pytest.mark.parametrize("i,j,expected_gap", [
        (1, 2, 1),      # 2, 3
        (10, 11, 2),    # 29, 31
        (33, 34, 2),    # 137, 139
    ])
    def test_gap_correct(self, core, i, j, expected_gap):
        r = core.compute_gap_between_primes(i, j)
        assert r["gap_direct"] == expected_gap, (
            f"gap({i}, {j}) = {r['gap_direct']}, attendu {expected_gap}"
        )

    def test_out_of_range_returns_error(self, core):
        r = core.compute_gap_between_primes(1001, 1002)
        assert "error" in r


class TestGapSpectral:
    """Nouvelle methode compute_gap_spectral (v3.29)."""

    def test_ratio_1_3_returns_result(self, core):
        r = core.compute_gap_spectral(10, ratio="1/3")
        assert "gap_spectral_reconstructed" in r
        assert r["ratio"] == "1/3"
        assert "methode_spectral.thy::spectral_gap_postulate_1_3" in r["theorem_reference"]

    def test_ratio_1_4_returns_result(self, core):
        r = core.compute_gap_spectral(10, ratio="1/4")
        assert "gap_spectral_reconstructed" in r
        assert r["ratio"] == "1/4"

    def test_invalid_ratio_returns_error(self, core):
        r = core.compute_gap_spectral(10, ratio="1/5")
        assert "error" in r

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
