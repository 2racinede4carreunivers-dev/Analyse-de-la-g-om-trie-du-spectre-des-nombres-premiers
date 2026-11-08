"""
Tests v3.20 :
  1. Timeout Claude passe a 90s (config.yaml + .env).
  2. Detection RsP config force want_png=True par defaut.
  3. Extension preuve par l'absurde a la reconstruction et au rapport spectral.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# ============================================================================
# FIX 1 — Timeout Claude passe a 90s
# ============================================================================

class TestClaudeTimeout90s:
    def test_config_yaml_claude_timeout_is_90(self):
        cfg_path = ROOT / "config.yaml"
        content = cfg_path.read_text(encoding="utf-8")
        # Rechercher la valeur claude.timeout_seconds
        # (bloc simple, une seule occurrence dans la section claude:)
        m = re.search(
            r"claude:.*?timeout_seconds:\s*(\d+)",
            content, re.DOTALL,
        )
        assert m is not None, "Impossible de trouver claude.timeout_seconds"
        assert int(m.group(1)) == 90, (
            f"config.yaml claude.timeout_seconds doit valoir 90, "
            f"obtenu {m.group(1)}"
        )

    def test_env_claude_timeout_is_90(self):
        env_path = ROOT / ".env"
        content = env_path.read_text(encoding="utf-8")
        m = re.search(r"^CLAUDE_TIMEOUT_SECONDS=(\d+)", content, re.MULTILINE)
        assert m is not None
        assert int(m.group(1)) == 90


# ============================================================================
# FIX 2 — Detection RsP config -> want_png=True automatique
# ============================================================================

class TestRspConfigForcesPng:
    """Quand une config RsP specifique est detectee (chaos-savard, ord, sym,
    1x1), want_png=True est force par defaut."""

    @pytest.mark.parametrize("query,expected_cfg", [
        (
            "Détermine le graphique représentant la valeur des blocs A et B "
            "pour la comparaison asymétrique ordonnée",
            "ord",
        ),
        (
            "Trace la courbe pour la configuration chaos-savard",
            "chaos-savard",
        ),
        (
            "Montre le graphique de la configuration symétrique n x n",
            "sym",
        ),
        (
            "Graphique 1x1 classique",
            "1x1",
        ),
    ])
    def test_rsp_config_detected_forces_png(self, query, expected_cfg):
        from src.visualization import detect_visualization_intent
        intent = detect_visualization_intent(query)
        assert intent is not None, f"Intent non detecte pour : {query}"
        assert intent.rsp_config == expected_cfg
        assert intent.want_png is True, (
            f"Config RsP '{expected_cfg}' devrait forcer want_png=True, "
            f"obtenu {intent.want_png}"
        )

    def test_no_rsp_config_leaves_png_opt_in(self):
        """Sans config RsP specifique, want_png reste opt-in (mots-cles)."""
        from src.visualization import detect_visualization_intent
        # Question qui declenche une courbe simple sans RsP config
        intent = detect_visualization_intent(
            "Trace la courbe des sommes SA et SB de 1 a 100"
        )
        assert intent is not None
        assert intent.rsp_config is None
        # Aucun mot-cle PNG dans cette question -> want_png False
        assert intent.want_png is False

    def test_rsp_config_with_explicit_png_still_true(self):
        from src.visualization import detect_visualization_intent
        intent = detect_visualization_intent(
            "Trace en PNG le graphique chaos-savard pour publication"
        )
        assert intent is not None
        assert intent.rsp_config == "chaos-savard"
        assert intent.want_png is True


# ============================================================================
# FIX 3 — Extension preuve par l'absurde : reconstruction + RsP
# ============================================================================

class TestExtensionReconstructionInThyFile:
    @pytest.fixture(scope="class")
    def thy_content(self) -> str:
        thy = ROOT / "theories" / "methode_spectral.thy"
        return thy.read_text(encoding="utf-8")

    def test_main_reconstruction_theorem_present(self, thy_content):
        assert "theorem composite_no_reconstruction_position:" in thy_content

    @pytest.mark.parametrize("value", [4, 9, 15, 51, 91, 121])
    def test_numerical_reconstruction_theorem(self, thy_content, value):
        assert f"theorem no_reconstruction_for_{value}:" in thy_content

    def test_subsection_header_present(self, thy_content):
        assert (
            'subsection "Extension - Preuve par l\'absurde pour la '
            'reconstruction des premiers"' in thy_content
        )


class TestExtensionRspInThyFile:
    @pytest.fixture(scope="class")
    def thy_content(self) -> str:
        return (ROOT / "theories" / "methode_spectral.thy").read_text(
            encoding="utf-8"
        )

    def test_pair_rsp_theorem_present(self, thy_content):
        assert "theorem composite_pair_no_rsp_positions:" in thy_content

    def test_single_rsp_theorem_present(self, thy_content):
        assert "theorem composite_single_no_rsp_position:" in thy_content

    def test_subsection_header_present(self, thy_content):
        assert (
            'subsection "Extension - Preuve par l\'absurde pour le '
            'rapport spectral RsP"' in thy_content
        )


class TestSyntheseThreePillars:
    @pytest.fixture(scope="class")
    def thy_content(self) -> str:
        return (ROOT / "theories" / "methode_spectral.thy").read_text(
            encoding="utf-8"
        )

    def test_synthese_subsection_present(self, thy_content):
        assert "3 piliers" in thy_content or "trois piliers" in thy_content.lower()

    def test_three_pillars_names_all_present(self, thy_content):
        # Normaliser espaces pour tolerer les sauts de ligne dans la
        # section text \<open>...\<close>
        norm = re.sub(r"\s+", " ", thy_content)
        assert "PILIER 1" in norm and "ECART" in norm.upper()
        assert "PILIER 2" in norm and "RECONSTRUCTION" in norm.upper()
        assert "PILIER 3" in norm and "RAPPORT" in norm.upper()

    def test_conclusion_definitive_present(self, thy_content):
        norm = re.sub(r"\s+", " ", thy_content)
        assert "CONSEQUENCE DEFINITIVE" in norm
        assert "caracterise EXACTEMENT" in norm


# ============================================================================
# FIX 3bis — Pedagogical text mentionne les 3 piliers
# ============================================================================

class TestPedagogicalTextMentionsThreePillars:
    """Le message pedagogique retourne a l'utilisateur mentionne maintenant
    les 3 theoremes/extensions."""

    def test_text_references_reconstruction_extension(self):
        from src.spectral.composite_absurdity_prover import (
            build_composite_rejection,
        )
        rej = build_composite_rejection(51)
        text = rej.to_pedagogical_text()
        assert "composite_no_reconstruction_position" in text
        assert "reconstruction" in text.lower()

    def test_text_references_rsp_extension(self):
        from src.spectral.composite_absurdity_prover import (
            build_composite_rejection,
        )
        rej = build_composite_rejection(51)
        text = rej.to_pedagogical_text()
        assert "composite_pair_no_rsp_positions" in text
        assert "rapport spectral" in text.lower() or "RsP" in text
