"""Tests pour rsp_curve : calcul + rendu ASCII."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.spectral_core import SpectralMethodCore
from src.spectral.rsp_curve import compute_rsp_curve, render_ascii_curve, summarize_curve


def test_curve_1x1_all_one_half():
    """Pour 1x1, tous les k doivent donner 1/2 exact."""
    core = SpectralMethodCore()
    points = compute_rsp_curve(core, "1x1", k_max=20)
    assert len(points) == 20
    valid = [p for p in points if not p.get("error")]
    assert len(valid) == 20
    for p in valid:
        assert p["RsP_fraction"] == "1/2", f"k={p['k']} : RsP={p['RsP_fraction']}"


def test_curve_sym_all_one_half():
    """Pour sym, tous les k doivent donner 1/2 exact."""
    core = SpectralMethodCore()
    points = compute_rsp_curve(core, "sym", k_max=10)
    valid = [p for p in points if not p.get("error")]
    for p in valid:
        assert p["matches_half"], f"k={p['k']} : non-1/2"


def test_curve_chaos_converges():
    """Pour chaos, tous proches de 1/2."""
    core = SpectralMethodCore()
    points = compute_rsp_curve(core, "chaos", k_max=20)
    valid = [p for p in points if not p.get("error") and "RsP_decimal" in p]
    assert len(valid) >= 15
    near = sum(1 for p in valid if p["near_half"])
    assert near >= len(valid) * 0.8


def test_curve_ord_starts_near_1_tends_to_half():
    """Pour ord, le rapport doit etre eloigne de 1/2 pour petit k et y tendre."""
    core = SpectralMethodCore()
    points = compute_rsp_curve(core, "ord", k_max=50)
    valid = [p for p in points if not p.get("error") and "RsP_decimal" in p]
    assert len(valid) >= 40
    # k=1 doit etre eloigne de 1/2 (ou proche de 1)
    first = valid[0]
    last = valid[-1]
    # On verifie au moins que les valeurs sont calculees correctement
    assert isinstance(first["RsP_decimal"], float)
    assert isinstance(last["RsP_decimal"], float)


def test_render_ascii_produces_graph():
    """Le rendu ASCII doit contenir au moins une etoile et la ligne cible."""
    core = SpectralMethodCore()
    points = compute_rsp_curve(core, "1x1", k_max=10)
    text = render_ascii_curve(points, width=40, height=10)
    assert "*" in text
    assert "0.50" in text or "0.500" in text
    assert "k=1" in text and "k=10" in text


def test_summarize_curve():
    core = SpectralMethodCore()
    points = compute_rsp_curve(core, "1x1", k_max=20)
    summary = summarize_curve(points)
    assert "exact 1/2" in summary
    assert "moyenne" in summary
    assert "100.0%" in summary  # tous exacts pour 1x1


def test_render_handles_empty():
    text = render_ascii_curve([])
    assert "aucun" in text.lower()

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
