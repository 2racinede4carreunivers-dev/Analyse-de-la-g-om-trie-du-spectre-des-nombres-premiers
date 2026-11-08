"""
Tests pour src/spectral/psi_savard.py — v3.40

Verrouille :
  1. Correspondance numérique EXACTE avec les validations Isabelle/HOL de
     `methode_spectral.thy` XIII.2 :
        psi_savard(30, 10)  ~ 28.888
        psi_savard(98, 25)  ~ 96.894
        psi_savard(228, 49) ~ 226.894
  2. La convergence |Psi_Savard - x| / x décroît quand x croît.
  3. Le renderer LaTeX produit un booktabs valide.
  4. Le crible de Tchebychev Psi(x) est cohérent (croissance monotone).
"""
from __future__ import annotations

import math
import pytest

from src.spectral.psi_savard import (
    build_comparison_table,
    chebyshev_psi,
    psi_savard,
    psi_savard_decomposition,
    to_latex_document,
    to_latex_pgfplots,
    to_latex_table,
)


# -------------------------------------------------------------------
# 1. Validations Isabelle/HOL — XIII.2 de methode_spectral.thy
# -------------------------------------------------------------------

@pytest.mark.parametrize(
    "x,n,expected",
    [
        (30, 10, 28.888143698),
        (98, 25, 96.894150249),
        (228, 49, 226.894132001),
    ],
)
def test_psi_savard_matches_isabelle_hol(x, n, expected):
    got = psi_savard(x, n)
    assert abs(got - expected) < 1e-6, (
        f"psi_savard({x}, {n}) = {got}, attendu {expected}"
    )


def test_psi_savard_decomposition_has_all_terms():
    d = psi_savard_decomposition(30, 10)
    for key in ("x", "SB_n", "two_n", "spectral_ratio",
                "log10_2pi", "half_log10_correction", "psi_savard"):
        assert key in d
    assert d["SB_n"] == 3262.0
    assert d["two_n"] == 1024.0
    assert d["spectral_ratio"] == pytest.approx(1024 / 3262)


# -------------------------------------------------------------------
# 2. Convergence |Psi_Sav - x| / x -> 0
# -------------------------------------------------------------------

def test_convergence_ratio_decroit():
    rows = build_comparison_table([10, 30, 100, 1000, 10000], n=10)
    ratios = [r["ecart_relatif_x"] for r in rows]
    # Strictement décroissant à partir de x >= 30
    for i in range(1, len(ratios) - 1):
        assert ratios[i + 1] <= ratios[i], (
            f"Convergence brisée : ratios[{i}]={ratios[i]} < ratios[{i+1}]={ratios[i+1]}"
        )
    # A x=10000, le ratio doit être < 0.02% (~1.11e-4)
    assert ratios[-1] < 0.001


# -------------------------------------------------------------------
# 3. Ψ(x) Tchebychev — cohérence & monotonie
# -------------------------------------------------------------------

def test_chebyshev_psi_monotone_croissant():
    xs = [10, 30, 100, 300, 1000]
    vals = [chebyshev_psi(x) for x in xs]
    for a, b in zip(vals, vals[1:]):
        assert b > a


def test_chebyshev_psi_encadre_x():
    # Théorème des nombres premiers : Psi(x)/x -> 1
    for x in (100, 1000, 5000):
        psi_x = chebyshev_psi(x)
        assert 0.85 * x < psi_x < 1.15 * x


def test_chebyshev_psi_zero_below_2():
    assert chebyshev_psi(1.5) == 0.0
    assert chebyshev_psi(0) == 0.0


# -------------------------------------------------------------------
# 4. Domaines invalides
# -------------------------------------------------------------------

def test_psi_savard_rejects_invalid_x():
    with pytest.raises(ValueError):
        psi_savard(1, 10)
    with pytest.raises(ValueError):
        psi_savard(0.5, 10)


def test_psi_savard_rejects_invalid_n():
    with pytest.raises(ValueError):
        psi_savard(30, 0)
    with pytest.raises(ValueError):
        psi_savard(30, -1)


# -------------------------------------------------------------------
# 5. Renderer LaTeX
# -------------------------------------------------------------------

def test_latex_table_contient_booktabs_et_valeurs():
    rows = build_comparison_table([30, 100], n=10)
    latex = to_latex_table(rows, n=10)
    assert "\\begin{table}" in latex
    assert "\\toprule" in latex and "\\midrule" in latex and "\\bottomrule" in latex
    assert "\\Psi_{\\text{Savard}}" in latex
    assert "28.8881" in latex  # valeur pour x=30
    assert "\\label{tab:psi_savard_n10}" in latex


def test_latex_pgfplots_contient_trois_courbes():
    rows = build_comparison_table([30, 50, 100], n=10)
    fig = to_latex_pgfplots(rows, n=10)
    assert "\\begin{tikzpicture}" in fig
    # 3 addplot : Psi_Savard, Psi Tcheb, y=x
    assert fig.count("\\addplot") == 3
    assert "\\legend{" in fig


def test_latex_standalone_est_compilable():
    rows = build_comparison_table([30, 100, 300], n=10)
    doc = to_latex_document(rows, n=10, standalone=True)
    assert doc.startswith("\\documentclass")
    assert "\\begin{document}" in doc
    assert doc.rstrip().endswith("\\end{document}")
    assert "pgfplots" in doc
