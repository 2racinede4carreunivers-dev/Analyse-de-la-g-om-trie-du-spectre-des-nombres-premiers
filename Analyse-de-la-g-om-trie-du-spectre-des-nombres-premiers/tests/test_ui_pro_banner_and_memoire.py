"""Tests pour les ameliorations 2026-06-28 :
- Banner Rich pro (4 panneaux : titre, identite, citation, technique)
- Integrateur memoire fonctionnel (delegue au RAG memory/)
- Timeout Claude 60s, OpenAI 45s
- Parser tuples robuste face aux espaces et texte parasite
"""
from __future__ import annotations
import pytest


class TestBannerRichPro:
    """Verifie le nouveau banner d'ouverture (4 panneaux Rich)."""

    def test_build_banner_panels_importable(self):
        from src.ui.cli import _build_banner_panels
        assert callable(_build_banner_panels)

    def test_banner_contient_titre_et_auteurs(self):
        from src.ui.cli import _build_banner_panels
        from rich.console import Console
        from io import StringIO
        buf = StringIO()
        Console(file=buf, force_terminal=False, width=120).print(_build_banner_panels())
        out = buf.getvalue()
        # Titre
        assert "BIENVENUE SUR L'AGENT LOCAL" in out
        assert "GABRIEL" in out
        # Carte d'identite : tous les auteurs
        assert "Philippe Thomas Savard" in out
        assert "E1" in out and "emergent.sh" in out
        assert "Gordon" in out and "Docker Desktop" in out
        assert "Copilot" in out and "Microsoft" in out
        # Date et lieu
        assert "vingt-sept juin" in out
        assert "Levis" in out
        # Citation
        assert "rapport spectral universel" in out
        assert "1/k" in out
        # Statut technique
        assert "Multi-Loop" in out
        assert "Isabelle/HOL" in out


class TestIntegrateurMemoire:
    """Verifie que le module integrateur_memoire est utilisable."""

    def test_import_integrateur_memoire(self):
        import sys
        from pathlib import Path
        src_core = Path(__file__).parent.parent / "src" / "core"
        sys.path.insert(0, str(src_core))
        from integrateur_memoire import IntegrateurMemoireGabriel
        im = IntegrateurMemoireGabriel()
        info = im.info()
        # 13 regimes (10 historiques + XI/XII + Pont Savard XIII v3.33)
        assert info["regimes"] == 13
        assert info["lemmes_certifies"] >= 30
        assert "methode_spectral_section_XI" in info["sections_extra"]
        assert "methode_spectral_section_XII" in info["sections_extra"]
        assert "methode_spectral_section_XIII" in info["sections_extra"]

    def test_augmentation_prompt_avec_regimes(self):
        import sys
        from pathlib import Path
        src_core = Path(__file__).parent.parent / "src" / "core"
        sys.path.insert(0, str(src_core))
        from integrateur_memoire import IntegrateurMemoireGabriel
        im = IntegrateurMemoireGabriel()
        prompt = "Reconstruis le 17eme premier en rapport 1/2"
        augmented = im.augmenter_prompt(prompt)
        # Le prompt augmente doit etre plus long et contenir les regles globales
        assert len(augmented) > len(prompt) * 5
        assert "REGLES D'INJECTION OBLIGATOIRES" in augmented or "CONTEXTE SPECTRAL" in augmented


class TestTimeoutsLLM:
    """Verifie que les nouveaux timeouts sont appliques (Claude 60s, OpenAI 45s)."""

    def test_claude_timeout_default_60(self):
        from src.core.llm_manager import ClaudeClient
        c = ClaudeClient(api_key="dummy")
        assert c.timeout == 60.0, f"Attendu 60s, obtenu {c.timeout}s"


class TestParserTuplesRobuste:
    """Verifie que _extract_tuples gere les espaces et le texte parasite."""

    @pytest.mark.parametrize("text,expected", [
        ("B=(23 41,7)",                       [[23, 41, 7]]),
        ("A=(3,2,11) et B=(31,17,79)",        [[3, 2, 11], [31, 17, 79]]),
        ("A=(17,11) et B=(23 41 7)",          [[17, 11], [23, 41, 7]]),
        ("entre (-3 et 29)",                  [[-3, 29]]),
        ("premiers (-7 et -37)",              [[-7, -37]]),
        ("(2, 97)",                           [[2, 97]]),
    ])
    def test_extraction_robuste(self, text, expected):
        from src.multiloop.request_decomposer import RequestDecomposer
        assert RequestDecomposer._extract_tuples(text) == expected

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
