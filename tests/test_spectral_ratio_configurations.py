"""Tests pour les nouvelles capacites de rapport spectral multi-configurations."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.spectral_core import SpectralMethodCore
from src.multiloop.request_decomposer import RequestDecomposer


# ============================================================
# SpectralMethodCore : nouvelles methodes
# ============================================================

def test_classify_configuration_1x1():
    c = SpectralMethodCore()
    assert c.classify_configuration([3], [5]) == "1x1"


def test_classify_configuration_symmetric_nxn():
    c = SpectralMethodCore()
    assert c.classify_configuration([1, 2, 3], [4, 5, 6]) == "symmetric_nxn"
    assert c.classify_configuration([10, 20], [5, 15]) == "symmetric_nxn"


def test_classify_configuration_asym_ordonnee():
    c = SpectralMethodCore()
    # |B|=|A|+1, croissant, max(A)<min(B)
    assert c.classify_configuration([1, 2], [3, 4, 5]) == "asym_ordonnee"


def test_classify_configuration_asym_chaotique():
    c = SpectralMethodCore()
    # longueurs differentes mais pas l'ordre ordonne
    assert c.classify_configuration([5, 1], [2, 3, 4]) == "asym_chaotique"


def test_primes_to_positions_simple():
    c = SpectralMethodCore()
    # 2 est le 1er premier, 7 est le 4e, 23 est le 9e
    positions, was_prime = c.primes_to_positions([2, 7, 23])
    assert positions == [1, 4, 9]
    assert all(was_prime)


def test_compute_RsP_nn_1x1_is_one_half():
    """Cas 1*1 : (SA(5)-SA(10))/(SB(5)-SB(10)) = 1/2 EXACT (lemme prouve)."""
    c = SpectralMethodCore()
    result = c.compute_RsP_nn([5], [10])
    assert result["configuration"] == "1x1"
    assert result["matches_half"] is True  # invariant 1/2 prouve
    assert result["RsP_fraction"] == "1/2"


def test_analyze_spectral_ratio_user_question():
    """
    Question utilisateur : "rapport spectral symetrique 3*3 pour (7,23,2) et (29,17,13)"
    Avec la VRAIE formule a differences : toutes les paires doivent donner 1/2.
    """
    c = SpectralMethodCore()
    result = c.analyze_spectral_ratio([7, 23, 2], [29, 17, 13])
    assert result["configuration"] == "symmetric_nxn"
    assert sorted(result["A_positions"]) == sorted([4, 9, 1])
    assert sorted(result["B_positions"]) == sorted([10, 7, 6])
    # CORRECTION : avec la vraie formule a differences, toutes les paires = 1/2
    assert result["matches_half"] is True
    assert result["RsP_fraction"] == "1/2"
    assert result["citations"]


def test_analyze_spectral_ratio_asym_chaotique():
    """Exemple PDF page 28 : A=(3,23) B=(41,29,31) -> RsP ~= 0.498."""
    c = SpectralMethodCore()
    result = c.analyze_spectral_ratio([3, 23], [41, 29, 31])
    assert result["configuration"] in ("asym_chaotique", "asym_ordonnee")
    assert result["near_half"] or abs(result["RsP_decimal"] - 0.5) < 0.01


def test_analyze_spectral_ratio_philippe_reported_case():
    """Cas reporte: A={7,11,2}, B={23,17,43,31,29} doit etre chaotique proche de 1/2."""
    c = SpectralMethodCore()
    result = c.analyze_spectral_ratio([7, 11, 2], [23, 17, 43, 31, 29])
    assert result["configuration"] == "asym_chaotique"
    assert abs(result["RsP_decimal"] - 0.5) < 0.01


# ============================================================
# RequestDecomposer : detection ratio_spectral_nxn
# ============================================================

def test_decomposer_detects_ratio_spectral_nxn():
    d = RequestDecomposer()
    res = d.decompose(
        "Peux-tu determiner le rapport spectral symetrique 3*3 pour "
        "les nombres premiers suivants (7,23,2) et (29,17,13) ?"
    )
    assert res.detected_intent == "ratio_spectral_nxn"
    assert res.tuple_A == [7, 23, 2]
    assert res.tuple_B == [29, 17, 13]
    assert res.config_size == 3
    assert res.detected_ratio == "1/2"  # auto-detect


def test_decomposer_extract_tuples():
    """Test du helper d'extraction de tuples."""
    tuples = RequestDecomposer._extract_tuples("foo (1, 2, 3) et bar (4; 5; 6)")
    assert tuples == [[1, 2, 3], [4, 5, 6]]


def test_decomposer_extract_tuples_single():
    tuples = RequestDecomposer._extract_tuples("foo (42) bar")
    assert tuples == [[42]]


def test_decomposer_extract_tuples_plain_labels():
    tuples = RequestDecomposer._extract_tuples(
        "asymetrique chaotique A=7,11,2 B=23,17,43,31,29"
    )
    assert tuples == [[7, 11, 2], [23, 17, 43, 31, 29]]


def test_decomposer_empty_tuples():
    tuples = RequestDecomposer._extract_tuples("aucune parenthese")
    assert tuples == []


# ============================================================
# Integration : SlowMotionDebugger resout la question
# ============================================================

@pytest.mark.asyncio
async def test_slow_motion_resolves_3x3_ratio():
    """Le debugger doit produire une reponse CONCRETE pour la question 3*3."""
    from rich.console import Console
    from src.adapters.corpus.certainty_kernel import CertaintyKernel
    from src.ui.debug_session import DebugSession

    session = DebugSession(
        console=Console(force_terminal=False, no_color=True),
        certainty_kernel=CertaintyKernel(theories_dir=str(ROOT / "theories")),
        spectral_core=SpectralMethodCore(),
    )
    from unittest.mock import patch
    inputs = iter(["e"])  # execute direct
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run(
            "Peux-tu determiner le rapport spectral symetrique 3*3 "
            "pour les nombres premiers (7,23,2) et (29,17,13)?"
        )
    assert result is not None
    # La reponse certifiee doit mentionner les primes ou positions
    text = result.answer_text
    assert "RsP" in text or "rapport" in text.lower()
    # Doit etre une vraie analyse, pas le message generique
    assert "non resolvable" not in text.lower()


def test_kernel_has_new_configurations():
    """Le kernel doit contenir les 4 nouvelles certitudes de configuration."""
    from src.adapters.corpus.certainty_kernel import CertaintyKernel
    k = CertaintyKernel(theories_dir=str(ROOT / "theories"))
    assert k.get("KERNEL_CONFIG_1X1") is not None
    assert k.get("KERNEL_CONFIG_NXN_SYM") is not None
    assert k.get("KERNEL_CONFIG_ASYM_ORD") is not None
    assert k.get("KERNEL_CONFIG_ASYM_CHAOS") is not None

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
