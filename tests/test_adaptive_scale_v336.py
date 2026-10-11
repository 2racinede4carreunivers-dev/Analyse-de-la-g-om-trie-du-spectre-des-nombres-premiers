"""Tests v3.36 — Auto-adaptive scale for RsP graphs.

Bug reporte par Philippe : le graphique "comparaison asymetrique ordonnee"
pour n=1..100 ecrasait visuellement la convergence (pic k=2 a 1.05, creux
k=1 a -0.17). La courbe convergeait bien vers 1/2 mais l'axe y trop large
rendait la fine convergence illisible.

Solution : detection automatique d'outliers + convergence claire vers
target_line, bascule sur un rendu double-panneau (overview + zoom).
"""
from __future__ import annotations

import pytest
from pathlib import Path

from src.core.spectral_core import SpectralMethodCore
from src.engines.question_graphs import _build_rsp_curve_data
from src.visualization.curves import CurveData, CurveKind, CurvePoint
from src.visualization.png_renderer import (
    _should_use_dual_panel, MATPLOTLIB_AVAILABLE, render_png,
)


@pytest.fixture(scope="module")
def core():
    return SpectralMethodCore()


class TestAdaptiveScaleDetection:
    """Le detecteur de double-panneau doit choisir correctement."""

    def test_ord_n1_100_triggers_dual_panel(self, core):
        c = _build_rsp_curve_data(core, "ord", 1, 100)
        assert c.adaptive_scale is True
        # 3 outliers (k=1,2,3) + 97 converges -> doit basculer en dual
        assert _should_use_dual_panel(c) is True

    def test_chaos_savard_n1_15_triggers_dual_panel(self, core):
        c = _build_rsp_curve_data(core, "chaos-savard", 1, 15)
        # k=1..4 divergent, k=5..15 converges -> mix, doit basculer
        assert _should_use_dual_panel(c) is True

    def test_1x1_stays_single_panel(self, core):
        # 1x1 est EXACTEMENT 0.5 partout -> pas de divergence -> single panel
        c = _build_rsp_curve_data(core, "1x1", 1, 50)
        assert _should_use_dual_panel(c) is False

    def test_sym_stays_single_panel(self, core):
        # Symetrique nxn : ratio = 1/2 exact -> pas de divergence
        c = _build_rsp_curve_data(core, "sym", 1, 50)
        assert _should_use_dual_panel(c) is False

    def test_adaptive_scale_disabled_forces_single(self):
        # Meme si donnees "dual-panel-worthy", adaptive_scale=False bloque
        pts = [CurvePoint(n=1, y_exact=0.0, y_float=-0.5)]
        pts += [CurvePoint(n=k, y_exact=0.0, y_float=0.5) for k in range(2, 20)]
        c = CurveData(
            kind=CurveKind.RATIO_SA_SB, n_min=1, n_max=19, scale="linear",
            title="t", x_label="x", y_label="y", points=pts,
            target_line=0.5, adaptive_scale=False,
        )
        assert _should_use_dual_panel(c) is False

    def test_no_target_line_disables_dual_panel(self):
        pts = [CurvePoint(n=k, y_exact=0, y_float=float(k)) for k in range(1, 20)]
        c = CurveData(
            kind=CurveKind.PRIME, n_min=1, n_max=19, scale="linear",
            title="t", x_label="x", y_label="y", points=pts,
            target_line=None, adaptive_scale=True,
        )
        assert _should_use_dual_panel(c) is False


class TestEffectiveKMaxWithPrimeTableLimit:
    """Quand user demande k_max > limite table primes, on ajuste."""

    def test_ord_n1_1000_capped_at_499(self, core):
        # ord requiert 2k+1 primes -> 1000 primes -> k_max effectif = 499
        c = _build_rsp_curve_data(core, "ord", 1, 1000)
        assert c.n_max == 499
        assert len(c.points) == 499
        assert "limite" in c.title.lower()

    def test_ord_n1_100_no_cap(self, core):
        # 100 << 499, aucune limitation
        c = _build_rsp_curve_data(core, "ord", 1, 100)
        assert c.n_max == 100
        assert "limite" not in c.title.lower()


@pytest.mark.skipif(not MATPLOTLIB_AVAILABLE, reason="matplotlib requis")
class TestRenderPngAdaptive:
    """Verifie le rendu PNG effectif (non-regression)."""

    def test_ord_n1_100_generates_png(self, core, tmp_path):
        c = _build_rsp_curve_data(core, "ord", 1, 100)
        out = render_png(c, tmp_path, dpi=80, filename="test_ord_n1_100")
        assert out.exists()
        assert out.stat().st_size > 5000  # PNG non-vide

    def test_ord_n1_1000_generates_png(self, core, tmp_path):
        c = _build_rsp_curve_data(core, "ord", 1, 1000)
        out = render_png(c, tmp_path, dpi=80, filename="test_ord_n1_1000")
        assert out.exists()
        assert out.stat().st_size > 5000

    def test_1x1_still_generates_single_panel(self, core, tmp_path):
        c = _build_rsp_curve_data(core, "1x1", 1, 50)
        out = render_png(c, tmp_path, dpi=80, filename="test_1x1")
        assert out.exists()

    def test_convergence_values_correct_ord(self, core):
        """Verifie les valeurs numeriques : k=1: -0.17, k=2: +1.05,
        k>=5 doit converger vers 0.5 (comportement mathematique valide)."""
        c = _build_rsp_curve_data(core, "ord", 1, 20)
        by_k = {p.n: p.y_float for p in c.points}
        assert by_k[1] == pytest.approx(-0.170213, abs=1e-4)
        assert by_k[2] == pytest.approx(1.052632, abs=1e-4)
        # A partir de k=5, convergence stricte
        for k in range(5, 21):
            assert abs(by_k[k] - 0.5) < 0.01, f"k={k}: {by_k[k]} loin de 0.5"


class TestAutoTriggerLargeRange:
    """L'auto_trigger doit accepter des ranges jusqu'a 1000."""

    def test_range_1_to_1000_detected(self):
        from src.visualization.auto_trigger import detect_visualization_intent
        q = "Genere le graphique du rapport spectral asymetrique ordonnee sur n=1..1000"
        intent = detect_visualization_intent(q)
        assert intent is not None
        assert intent.n_min == 1
        assert intent.n_max == 1000
        assert intent.rsp_config == "ord"

    def test_range_1000_premiers_detected(self):
        from src.visualization.auto_trigger import detect_visualization_intent
        q = "Peux-tu tracer le graphique du rapport spectral asymetrique ordonnee pour les 1000 premiers nombres premiers"
        intent = detect_visualization_intent(q)
        assert intent is not None
        assert intent.n_max == 1000
        assert intent.rsp_config == "ord"

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
