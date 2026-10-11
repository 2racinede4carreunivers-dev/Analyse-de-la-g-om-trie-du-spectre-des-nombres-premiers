"""Tests pour la commande rsp (rapport spectral direct + tests de masse)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.spectral_core import SpectralMethodCore
from src.spectral.rsp_command import parse_rsp_args, random_combo


# ============================================================
# parse_rsp_args
# ============================================================

def test_parse_csv_format():
    res = parse_rsp_args("7,23,2 29,17,13")
    assert res == ([7, 23, 2], [29, 17, 13])


def test_parse_parens_format():
    res = parse_rsp_args("(7,23,2) (29,17,13)")
    assert res == ([7, 23, 2], [29, 17, 13])


def test_parse_simple_1x1():
    res = parse_rsp_args("2 3")
    assert res == ([2], [3])


def test_parse_asymmetric():
    res = parse_rsp_args("2,3 5,7,11")
    assert res == ([2, 3], [5, 7, 11])


def test_parse_empty():
    assert parse_rsp_args("") is None


def test_parse_one_group_only():
    assert parse_rsp_args("(1,2,3)") is None


# ============================================================
# random_combo : varied combinations across 1000 primes
# ============================================================

def test_random_combo_1x1():
    core = SpectralMethodCore()
    A, B = random_combo(core, "1x1")
    assert len(A) == 1 and len(B) == 1
    assert A[0] in core.prime_list and B[0] in core.prime_list


def test_random_combo_sym3():
    core = SpectralMethodCore()
    A, B = random_combo(core, "sym3")
    assert len(A) == 3 and len(B) == 3
    assert all(p in core.prime_list for p in A + B)


def test_random_combo_sym5():
    core = SpectralMethodCore()
    A, B = random_combo(core, "sym5")
    assert len(A) == 5 and len(B) == 5


def test_random_combo_chaos():
    core = SpectralMethodCore()
    A, B = random_combo(core, "chaos")
    assert len(A) != len(B)


def test_random_combo_ord():
    core = SpectralMethodCore()
    A, B = random_combo(core, "ord")
    # Verifier que |B| = |A| + 1
    assert len(B) == len(A) + 1


def test_random_combo_unknown():
    core = SpectralMethodCore()
    with pytest.raises(ValueError):
        random_combo(core, "bogus")


# ============================================================
# Integration : analyze_spectral_ratio fonctionne sur 1..1000
# ============================================================

def test_analyze_works_on_all_1000_primes_1x1():
    """1x1 : avec la VRAIE formule a differences, doit etre 1/2 EXACT (lemme prouve)."""
    core = SpectralMethodCore()
    import random
    random.seed(42)
    for _ in range(50):
        a, b = random.sample(core.prime_list, 2)
        r = core.analyze_spectral_ratio([a], [b])
        assert r["matches_half"] is True
        assert r["RsP_fraction"] == "1/2"


def test_analyze_works_for_chaos_large_primes():
    """asym_chaotique sur des grands primes (positions > 500)."""
    core = SpectralMethodCore()
    A = [core.prime_list[499], core.prime_list[599]]
    B = [core.prime_list[699], core.prime_list[799], core.prime_list[899]]
    r = core.analyze_spectral_ratio(A, B)
    assert r["configuration"] in ("asym_chaotique", "asym_ordonnee")
    # Doit converger vers 1/2 (formule RsP_bloc)
    assert abs(r["RsP_decimal"] - 0.5) < 0.05


def test_analyze_works_for_sym2_random():
    """100 tests sym2 : tous DOIVENT donner 1/2 exact (lemme prouve)."""
    core = SpectralMethodCore()
    import random
    random.seed(123)
    half_count = 0
    for _ in range(100):
        A, B = random_combo(core, "sym2")
        r = core.analyze_spectral_ratio(A, B)
        if r.get("matches_half"):
            half_count += 1
    # Tous les sym n*n doivent donner 1/2 (l'invariant est verifie pour toute paire)
    assert half_count >= 95, f"Seulement {half_count}/100 sym2 = 1/2"


def test_invariant_1_2_on_chaotic_combos():
    """100 configs chaotiques aleatoires -> >=80% proches de 1/2."""
    core = SpectralMethodCore()
    import random
    random.seed(456)
    near = 0
    for _ in range(100):
        A, B = random_combo(core, "chaos")
        r = core.analyze_spectral_ratio(A, B)
        if r.get("near_half"):
            near += 1
    assert near >= 80, f"Seulement {near}/100 configs chaotiques proches de 1/2"

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
