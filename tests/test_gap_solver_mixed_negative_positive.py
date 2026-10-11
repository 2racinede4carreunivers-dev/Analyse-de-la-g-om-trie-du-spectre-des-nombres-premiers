"""
Tests pour _solve_mixed : écart spectral entre un premier négatif et un
premier positif.

Cas couverts :
1. Cas "standard" (-31, 17) — référence fournie par l'utilisateur, attendu = -47
2. Cas "pont ZÉRO" (-2, 37) — p_min = -2 force pos_suivant_min = 0,
   ce qui faisait précédemment échouer GapSolver (`nth_prime(0) -> None`).
3. Variantes du pont zéro pour valider la généralisation.
4. Inversion des arguments (37, -2) doit donner le même résultat.
5. La cohérence avec la règle |p1 - p2| - 1.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.spectral.gap_solver_corrected import GapSolver


@pytest.fixture
def solver() -> GapSolver:
    return GapSolver()


# ---------------------------------------------------------------------------
# 1. Référence fournie par l'utilisateur : (-31, 17) => -47
# ---------------------------------------------------------------------------

def test_mixed_minus31_plus17_reference(solver: GapSolver):
    """Exemple manuel fourni par l'utilisateur :
       (-31, 17) -> 47 nombres entre eux (signe = -47).
    """
    result = solver.solve_gap(-31, 17)
    assert result is not None, "GapSolver ne doit jamais retourner None pour (-31, 17)"
    assert result.gap_type == "mixed"
    assert result.p1 == -31
    assert result.p2 == 17
    assert abs(result.gap_count) == 47, (
        f"|Gap(-31, 17)| attendu = 47 (= |-31 - 17| - 1), "
        f"obtenu = {result.gap_count}"
    )
    # digamma_max = SB(7) - 64*17 = 350 - 1088 = -738 (référence utilisateur)
    assert result.digamma_max == pytest.approx(-738.0, abs=1e-6)


# ---------------------------------------------------------------------------
# 2. Bug rapporté : (-2, 37) provoquait "GapSolver échoué pour mixed"
# ---------------------------------------------------------------------------

def test_mixed_minus2_plus37_zero_bridge(solver: GapSolver):
    """Régression du bug : p_min = -2 force pos_suivant_min = 0.
       Doit maintenant retourner un résultat valide grâce au pont ZÉRO.
    """
    result = solver.solve_gap(-2, 37)
    assert result is not None, (
        "REGRESSION : _solve_mixed(-2, 37) ne doit plus retourner None "
        "(pont ZÉRO doit être activé)"
    )
    assert result.gap_type == "mixed"
    assert result.p1 == -2
    assert result.p2 == 37
    # |gap| = |-2 - 37| - 1 = 38
    assert abs(result.gap_count) == 38, (
        f"|Gap(-2, 37)| attendu = 38, obtenu = {result.gap_count}"
    )
    # Le pont ZÉRO doit être signalé dans la validation
    assert result.validation.get("zero_bridge") is True
    assert result.validation.get("zero_special") is True
    assert result.position_suivant_min == 0
    assert result.p_suivant_min == 0


def test_mixed_minus2_plus37_explanation_mentions_zero_bridge(solver: GapSolver):
    """L'explication doit mentionner le pont ZÉRO pour la traçabilité."""
    result = solver.solve_gap(-2, 37)
    assert result is not None
    assert "ZÉRO" in result.explanation
    assert "pont" in result.explanation.lower()


# ---------------------------------------------------------------------------
# 3. Inversion des arguments — doit donner le même résultat
# ---------------------------------------------------------------------------

def test_mixed_args_order_independent(solver: GapSolver):
    """solve_gap(-2, 37) == solve_gap(37, -2) (sauf trace de l'ordre d'appel)."""
    r1 = solver.solve_gap(-2, 37)
    r2 = solver.solve_gap(37, -2)
    assert r1 is not None and r2 is not None
    assert r1.gap_count == r2.gap_count
    assert r1.p1 == r2.p1 and r1.p2 == r2.p2  # normalisé p_min, p_max


# ---------------------------------------------------------------------------
# 4. Variantes du pont ZÉRO : p_min = -2 avec divers p_max
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "p_max,expected_abs_gap",
    [
        (3, 4),     # -2 et 3 : -1, 0, 1, 2 = 4 nombres entre
        (5, 6),     # -2 et 5 : -1, 0, 1, 2, 3, 4 = 6
        (7, 8),
        (11, 12),
        (13, 14),
        (17, 18),
        (19, 20),
        (23, 24),
        (37, 38),
        (41, 42),
        (97, 98),
    ],
)
def test_mixed_minus2_plus_various(solver: GapSolver, p_max: int, expected_abs_gap: int):
    """Pour p_min = -2 (pont ZÉRO), |gap| doit toujours = |p_max - (-2)| - 1."""
    result = solver.solve_gap(-2, p_max)
    assert result is not None, f"GapSolver doit gérer (-2, {p_max})"
    assert abs(result.gap_count) == expected_abs_gap, (
        f"|Gap(-2, {p_max})| attendu = {expected_abs_gap}, "
        f"obtenu = {result.gap_count}"
    )
    assert result.validation.get("zero_bridge") is True


# ---------------------------------------------------------------------------
# 5. Cas "non-pont" : p_min différent de -2, pos_suivant_min reste négatif
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "p_min,p_max,expected_abs_gap",
    [
        (-3, 5, 7),     # |-3 - 5| - 1 = 7
        (-5, 7, 11),    # 11
        (-7, 11, 17),
        (-11, 13, 23),
        (-13, 17, 29),
        (-17, 19, 35),
        (-19, 23, 41),
        (-23, 29, 51),
        (-29, 31, 59),
        (-31, 17, 47),  # ré-affirme la référence utilisateur
    ],
)
def test_mixed_no_zero_bridge_invariant(
    solver: GapSolver, p_min: int, p_max: int, expected_abs_gap: int
):
    """Pour |p_min| > 2, pas de pont ZÉRO ; |gap| = |p_min - p_max| - 1."""
    result = solver.solve_gap(p_min, p_max)
    assert result is not None
    assert abs(result.gap_count) == expected_abs_gap
    assert result.validation.get("zero_bridge") is False


# ---------------------------------------------------------------------------
# 6. SA(0) — la valeur de référence utilisée par le pont ZÉRO
# ---------------------------------------------------------------------------

def test_SA_at_position_zero_value(solver: GapSolver):
    """SA(0) = (3.25/2) * 2^0 - 2 = 1.625 - 2 = -0.375 (pont ZÉRO)."""
    sa0 = solver._compute_SA_negative(0)
    assert sa0 == pytest.approx(-0.375, abs=1e-9)


# ---------------------------------------------------------------------------
# 7. La détection d'intent "mixed" via solve_gap (entry-point public)
# ---------------------------------------------------------------------------

def test_solve_gap_routes_to_mixed(solver: GapSolver):
    """solve_gap(-2, 37) doit appeler _solve_mixed (pas _solve_negative_negative)."""
    result = solver.solve_gap(-2, 37)
    assert result is not None
    assert result.gap_type == "mixed"


def test_solve_gap_routes_to_mixed_inverted(solver: GapSolver):
    """solve_gap(37, -2) doit aussi router vers _solve_mixed."""
    result = solver.solve_gap(37, -2)
    assert result is not None
    assert result.gap_type == "mixed"
