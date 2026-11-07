"""Tests pour src/visualization (courbes ASCII, Rich, PNG)."""
from __future__ import annotations

from pathlib import Path

import pytest

from src.core.spectral_core import SpectralMethodCore
from src.visualization import (
    CurveData,
    CurveKind,
    compute_curve,
    list_supported_kinds,
    render_ascii,
    render_table,
    render_png,
    MATPLOTLIB_AVAILABLE,
)


@pytest.fixture(scope="module")
def core() -> SpectralMethodCore:
    return SpectralMethodCore()


# --------------------------------------------------------------------------
# compute_curve : calculs de donnees
# --------------------------------------------------------------------------
def test_list_supported_kinds():
    kinds = list_supported_kinds()
    assert {"SA", "SB", "SA_SB", "digamma", "invariant", "ratio", "gap", "prime"} <= set(kinds)


def test_compute_SA_returns_exact_integers(core):
    c = compute_curve(core, "SA", 1, 10, scale="linear")
    assert c.kind == CurveKind.SA
    assert len(c.points) == 10
    # SA(1) = (13*2)/8 - 2 = 26/8 - 2 = 3 - 2 = 1
    assert c.points[0].y_exact == 1
    # SA(10) = (13*1024)/8 - 2 = 13312/8 - 2 = 1664 - 2 = 1662
    assert c.points[9].y_exact == 1662


def test_compute_SB_returns_exact_integers(core):
    c = compute_curve(core, "SB", 1, 10, scale="linear")
    assert len(c.points) == 10
    # SB(10) = (13*1024)/4 - 66 = 3328 - 66 = 3262
    assert c.points[9].y_exact == 3262


def test_compute_ratio_converges_to_half(core):
    """Test critique : SA/SB doit converger vers 1/2."""
    c = compute_curve(core, "ratio", 1, 100)
    assert c.scale == "linear"
    assert c.target_line == 0.5
    last_ratio = c.points[-1].y_float
    # A n=100, doit etre tres proche de 0.5
    assert abs(last_ratio - 0.5) < 0.01


def test_compute_digamma_matches_reconstruction(core):
    """digamma(n) doit correspondre a SB(n) - 64 * P(n)."""
    c = compute_curve(core, "digamma", 1, 20, scale="linear")
    for p in c.points:
        expected = core._SB_int(p.n) - 64 * p.prime
        assert p.y_exact == expected, f"digamma mismatch a n={p.n}"


def test_compute_gap_consecutive_primes(core):
    """Gap = p(n+1) - p(n)."""
    c = compute_curve(core, "gap", 1, 30, scale="linear")
    assert c.points[0].y_exact == 1  # gap entre 2 et 3
    assert c.points[1].y_exact == 2  # gap entre 3 et 5
    # Tous les gaps doivent etre positifs
    assert all(p.y_exact > 0 for p in c.points)


def test_compute_invariant_x8_is_int(core):
    """D_x8 doit etre exact en entier."""
    c = compute_curve(core, "invariant", 1, 20, scale="linear")
    for p in c.points:
        assert isinstance(p.y_exact, int), f"y_exact n'est pas int a n={p.n}"


def test_compute_SA_SB_has_two_series(core):
    c = compute_curve(core, "SA_SB", 1, 20)
    assert len(c.points) == 20  # serie SA
    assert len(c.secondary_points) == 20  # serie SB
    # v3.25 : label enrichi ("SB(n) : somme alternee B" au lieu de "SB")
    assert "SB" in c.secondary_label, (
        f"secondary_label doit contenir 'SB', trouve: {c.secondary_label!r}"
    )
    # v3.25 : nouveaux champs enrichis
    assert c.primary_label != "", "primary_label doit etre defini pour la lisibilite"
    assert c.critical_summary != "", "critical_summary doit etre defini (max 750 char)"
    assert len(c.critical_summary) <= 750, "critical_summary doit etre <= 750 char"
    assert c.axis_legend, "axis_legend doit contenir les explications des series"


def test_compute_validates_bounds(core):
    with pytest.raises(ValueError):
        compute_curve(core, "SA", 0, 10)
    with pytest.raises(ValueError):
        compute_curve(core, "SA", 1, 99999)
    with pytest.raises(ValueError):
        compute_curve(core, "SA", 50, 10)


def test_compute_invalid_kind(core):
    with pytest.raises(ValueError):
        compute_curve(core, "inexistant_kind", 1, 10)


def test_compute_invalid_scale(core):
    with pytest.raises(ValueError):
        compute_curve(core, "SA", 1, 10, scale="exponentiel")


def test_auto_scale_picks_log_for_growth(core):
    """SA explose en 2^n, donc en auto sur 1..50 on doit avoir log10."""
    c = compute_curve(core, "SA", 1, 50)  # scale=auto par defaut
    assert c.scale == "log10"


def test_auto_scale_picks_linear_for_negative(core):
    """digamma sur 1..10 a des valeurs negatives -> linear (pas log)."""
    c = compute_curve(core, "digamma", 1, 10)
    assert c.scale == "linear"


# --------------------------------------------------------------------------
# render_ascii
# --------------------------------------------------------------------------
def test_render_ascii_returns_string(core):
    c = compute_curve(core, "SA", 1, 20)
    out = render_ascii(c)
    assert isinstance(out, str)
    assert "SA" in out
    assert "n=1" in out
    assert "n=20" in out


def test_render_ascii_handles_empty():
    # CurveData vide
    empty = CurveData(
        kind=CurveKind.SA, n_min=1, n_max=0, scale="linear",
        title="empty", x_label="n", y_label="y", points=[],
    )
    out = render_ascii(empty)
    assert "aucun point" in out.lower()


# --------------------------------------------------------------------------
# render_table
# --------------------------------------------------------------------------
def test_render_table_returns_rich_table(core):
    from rich.table import Table
    c = compute_curve(core, "digamma", 1, 10)
    t = render_table(c)
    assert isinstance(t, Table)
    assert t.title and "Digamma" in str(t.title)


def test_render_table_truncates_large_dataset(core):
    c = compute_curve(core, "SA", 1, 200)
    t = render_table(c, max_rows=30)
    # On ne peut pas facilement compter les lignes Rich, mais on s'assure que
    # ca ne plante pas et que le titre est correct
    assert isinstance(t.title, str)


# --------------------------------------------------------------------------
# render_png
# --------------------------------------------------------------------------
@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib non installe")
def test_render_png_creates_file(core, tmp_path: Path):
    c = compute_curve(core, "SA_SB", 1, 30)
    out = render_png(c, output_dir=tmp_path, dpi=80)
    assert out.exists()
    assert out.suffix == ".png"
    assert out.stat().st_size > 1000  # au moins 1Ko


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib non installe")
def test_render_png_custom_filename(core, tmp_path: Path):
    c = compute_curve(core, "ratio", 1, 50)
    out = render_png(c, output_dir=tmp_path, dpi=80, filename="custom_ratio")
    assert out.name == "custom_ratio.png"


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib non installe")
def test_render_png_raises_for_empty(core, tmp_path: Path):
    empty = CurveData(
        kind=CurveKind.SA, n_min=1, n_max=0, scale="linear",
        title="empty", x_label="n", y_label="y", points=[],
    )
    with pytest.raises(ValueError):
        render_png(empty, output_dir=tmp_path)


# --------------------------------------------------------------------------
# CurveData.summary (utile pour audit)
# --------------------------------------------------------------------------
def test_curve_summary_for_audit(core):
    c = compute_curve(core, "ratio", 1, 50)
    s = c.summary()
    assert s["kind"] == "ratio"
    assert s["n_min"] == 1 and s["n_max"] == 50
    assert s["n_points"] == 50
    assert "y_first" in s and "y_last" in s
    assert s["formula"]

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
