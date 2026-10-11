"""Tests pour la convention chaos-Savard et le module question_graphs.

Couverture :
  1. ratio_chaos_savard : formule alternee + cas mathematiques reels
  2. build_chaos_savard_blocks : construction A=[k+1..2k], B=[2k+1, 1..k]
  3. compute_rsp_curve avec config="chaos-savard" : convergence vers 1/2
  4. question_graphs : mapping Q1.a/b/c/d, Q2, Q3.a/b/c
  5. detect_gap_question et detect_rsp_question
  6. generate_graphs_for_question : produit des PNG
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from src.core.spectral_core import SpectralMethodCore
from src.spectral.ratios import (
    _alternating_diff,
    build_chaos_savard_blocks,
    ratio_chaos_savard,
)
from src.spectral.rsp_curve import compute_rsp_curve


@pytest.fixture(scope="module")
def core():
    return SpectralMethodCore()


# ---------------------------------------------------------------------------
# 1. Formule alternee
# ---------------------------------------------------------------------------
class TestAlternatingDiff:
    def test_alt_simple(self):
        # alt([4.5]) = 4.5
        assert _alternating_diff([Fraction(45, 10)]) == Fraction(45, 10)

    def test_alt_2_elements(self):
        # alt([11, 1.25]) = 11 - 1.25 = 9.75
        result = _alternating_diff([Fraction(11), Fraction(125, 100)])
        assert result == Fraction(975, 100)

    def test_alt_3_elements(self):
        # alt([50, 1.25, 4.5]) = 50 - 1.25 - 4.5 = 44.25
        result = _alternating_diff([
            Fraction(50), Fraction(125, 100), Fraction(45, 10)
        ])
        assert result == Fraction(4425, 100)

    def test_alt_vide_leve(self):
        with pytest.raises(ValueError):
            _alternating_diff([])


# ---------------------------------------------------------------------------
# 2. Construction des blocs chaos-Savard
# ---------------------------------------------------------------------------
class TestBuildChaosSavardBlocks:
    def test_k1(self):
        A, B = build_chaos_savard_blocks(1)
        assert A == [2]                  # position de p_2 = 3
        assert B == [3, 1]               # p_3 = 5, p_1 = 2

    def test_k2(self):
        A, B = build_chaos_savard_blocks(2)
        assert A == [3, 4]               # positions de p_3, p_4 = 5, 7
        assert B == [5, 1, 2]            # p_5, p_1, p_2

    def test_k3(self):
        A, B = build_chaos_savard_blocks(3)
        assert A == [4, 5, 6]
        assert B == [7, 1, 2, 3]

    def test_k_invalide(self):
        with pytest.raises(ValueError, match="k doit etre >= 1"):
            build_chaos_savard_blocks(0)

    def test_taille_blocks(self):
        for k in range(1, 8):
            A, B = build_chaos_savard_blocks(k)
            assert len(A) == k
            assert len(B) == k + 1


# ---------------------------------------------------------------------------
# 3. ratio_chaos_savard : valeurs Philippe (exactes pour k=2,3,4)
# ---------------------------------------------------------------------------
class TestRatioChaosSavard:
    def test_k2_exact(self):
        """k=2 : (5-7)-(11-2-3) -> 0.3243626062..."""
        A = [3, 4]
        B = [5, 1, 2]
        ratio = float(ratio_chaos_savard(A, B))
        assert abs(ratio - 0.3243626062) < 1e-8

    def test_k3_exact(self):
        """k=3 : (7-11-13)-(17-2-3-5) -> 0.4554917444..."""
        A = [4, 5, 6]
        B = [7, 1, 2, 3]
        ratio = float(ratio_chaos_savard(A, B))
        assert abs(ratio - 0.4554917444) < 1e-8

    def test_k4_exact(self):
        """k=4 : (11-13-17-19)-(23-2-3-5-7) -> 0.4896130005..."""
        A = [5, 6, 7, 8]
        B = [9, 1, 2, 3, 4]
        ratio = float(ratio_chaos_savard(A, B))
        assert abs(ratio - 0.4896130005) < 1e-8

    def test_convergence_vers_un_demi(self):
        """Au-dela de k=5, le ratio est tres proche de 1/2."""
        for k in range(6, 15):
            A, B = build_chaos_savard_blocks(k)
            ratio = float(ratio_chaos_savard(A, B))
            assert abs(ratio - 0.5) < 0.01, f"k={k}, ratio={ratio}"

    def test_denominateur_nul_leve(self):
        # Trouver un cas ou alt_SB(A) - alt_SB(B) = 0 est difficile en pratique.
        # Test theorique avec mock : si A == B (memes positions), alors num=0=den
        # mais on attend une exception car ZeroDivision. Verifions via une
        # paire artificielle :
        # A = [1] et B = [1] : alt_SB([1]) - alt_SB([1]) = 0
        with pytest.raises(ValueError, match="alt_SB"):
            ratio_chaos_savard([1], [1])

    def test_a_vide_leve(self):
        with pytest.raises(ValueError):
            ratio_chaos_savard([], [1])

    def test_b_vide_leve(self):
        with pytest.raises(ValueError):
            ratio_chaos_savard([1], [])


# ---------------------------------------------------------------------------
# 4. compute_rsp_curve avec config="chaos-savard"
# ---------------------------------------------------------------------------
class TestRspCurveChaosSavard:
    def test_curve_15_points(self, core):
        points = compute_rsp_curve(core, "chaos-savard", k_max=15)
        # 15 points sans erreur
        valid = [p for p in points if not p.get("error")]
        assert len(valid) == 15

    def test_curve_converge(self, core):
        points = compute_rsp_curve(core, "chaos-savard", k_max=10)
        last_5 = [p["RsP_decimal"] for p in points[-5:] if not p.get("error")]
        for r in last_5:
            assert abs(r - 0.5) < 0.05, f"Devrait converger vers 1/2, recu {r}"

    def test_curve_premiers_points_reels(self, core):
        points = compute_rsp_curve(core, "chaos-savard", k_max=5)
        # k=2 -> A primes = [5, 7], B primes = [11, 2, 3]
        p2 = points[1]
        assert p2["A"] == [5, 7]
        assert p2["B"] == [11, 2, 3]
        assert abs(p2["RsP_decimal"] - 0.3243626062) < 1e-8


# ---------------------------------------------------------------------------
# 5. question_graphs : mapping et detection
# ---------------------------------------------------------------------------
class TestQuestionGraphsMapping:
    def test_questions_supportees(self):
        from src.engines.question_graphs import list_questions
        qs = list_questions()
        for q in ("Q1.a", "Q1.b", "Q1.c", "Q1.d", "Q2", "Q3.a", "Q3.b", "Q3.c"):
            assert q in qs

    def test_q2_genere_2_graphs(self):
        from src.engines.question_graphs import graph_count_for
        assert graph_count_for("Q2") == 2

    def test_q1_x_genere_1_graph(self):
        from src.engines.question_graphs import graph_count_for
        for q in ("Q1.a", "Q1.b", "Q1.c", "Q1.d"):
            assert graph_count_for(q) == 1

    def test_q3_x_genere_1_graph(self):
        from src.engines.question_graphs import graph_count_for
        for q in ("Q3.a", "Q3.b", "Q3.c"):
            assert graph_count_for(q) == 1

    def test_q_inexistante_zero_graph(self):
        from src.engines.question_graphs import graph_count_for
        assert graph_count_for("Q99") == 0


class TestDetectGapQuestion:
    def test_pos_pos(self):
        from src.engines.question_graphs import detect_gap_question
        assert detect_gap_question(5, 7) == "Q3.a"
        assert detect_gap_question(101, 199) == "Q3.a"

    def test_neg_neg(self):
        from src.engines.question_graphs import detect_gap_question
        assert detect_gap_question(-19, -5) == "Q3.b"
        assert detect_gap_question(-101, -7) == "Q3.b"

    def test_mixte(self):
        from src.engines.question_graphs import detect_gap_question
        assert detect_gap_question(-5, 7) == "Q3.c"
        assert detect_gap_question(11, -3) == "Q3.c"


class TestDetectRspQuestion:
    def test_sym(self):
        from src.engines.question_graphs import detect_rsp_question
        assert detect_rsp_question("sym") == "Q1.b"
        assert detect_rsp_question("nxn_symetrique") == "Q1.b"

    def test_chaos(self):
        from src.engines.question_graphs import detect_rsp_question
        assert detect_rsp_question("chaos") == "Q1.c"
        assert detect_rsp_question("asym_chaotique") == "Q1.c"
        assert detect_rsp_question("chaos-savard") == "Q1.c"

    def test_ord(self):
        from src.engines.question_graphs import detect_rsp_question
        assert detect_rsp_question("ord") == "Q1.d"
        assert detect_rsp_question("asym_ordonnee") == "Q1.d"

    def test_1x1(self):
        from src.engines.question_graphs import detect_rsp_question
        assert detect_rsp_question("1x1") == "Q1.a"


# ---------------------------------------------------------------------------
# 6. generate_graphs_for_question (smoke test : PNG sont crees)
# ---------------------------------------------------------------------------
class TestGenerateGraphsForQuestion:
    def test_q1c_genere_un_png(self, core, tmp_path):
        from src.engines.question_graphs import (
            generate_graphs_for_question, MATPLOTLIB_AVAILABLE,
        )
        if not MATPLOTLIB_AVAILABLE:
            pytest.skip("matplotlib non installe")
        paths = generate_graphs_for_question(
            question="Q1.c", core=core, params={},
            output_dir=tmp_path,
        )
        assert len(paths) == 1
        assert paths[0].exists()
        assert paths[0].suffix == ".png"
        assert "Q1c" in paths[0].name
        assert "chaos-savard" in paths[0].name

    def test_q2_genere_2_png(self, core, tmp_path):
        from src.engines.question_graphs import (
            generate_graphs_for_question, MATPLOTLIB_AVAILABLE,
        )
        if not MATPLOTLIB_AVAILABLE:
            pytest.skip("matplotlib non installe")
        paths = generate_graphs_for_question(
            question="Q2", core=core, params={"n": 26},
            output_dir=tmp_path,
        )
        assert len(paths) == 2
        names = [p.name for p in paths]
        assert any("SA_SB" in n for n in names)
        assert any("digamma" in n for n in names)

    def test_q3a_genere_un_png_gap(self, core, tmp_path):
        from src.engines.question_graphs import (
            generate_graphs_for_question, MATPLOTLIB_AVAILABLE,
        )
        if not MATPLOTLIB_AVAILABLE:
            pytest.skip("matplotlib non installe")
        paths = generate_graphs_for_question(
            question="Q3.a", core=core, params={"p1": 5, "p2": 7},
            output_dir=tmp_path,
        )
        assert len(paths) == 1
        assert "Q3a" in paths[0].name
        assert "gap" in paths[0].name

    def test_question_inconnue_zero_png(self, core, tmp_path):
        from src.engines.question_graphs import generate_graphs_for_question
        paths = generate_graphs_for_question(
            question="Q99", core=core, output_dir=tmp_path,
        )
        assert paths == []


# ---------------------------------------------------------------------------
# 7. Integration CLI : _auto_generate_question_graphs existe
# ---------------------------------------------------------------------------
class TestCLIIntegration:
    def test_helper_existe(self):
        from src.ui.cli import CLIInterface
        assert hasattr(CLIInterface, "_auto_generate_question_graphs")

    def test_helper_signature(self):
        from src.ui.cli import CLIInterface
        import inspect
        sig = inspect.signature(CLIInterface._auto_generate_question_graphs)
        params = list(sig.parameters.keys())
        assert "qcode" in params
        assert "params" in params

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
