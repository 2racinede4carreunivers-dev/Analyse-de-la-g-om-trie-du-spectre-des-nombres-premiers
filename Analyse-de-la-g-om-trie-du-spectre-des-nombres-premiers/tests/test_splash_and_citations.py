"""Tests pour les commandes splash/about/citation et la citation Riemann."""
from __future__ import annotations
import pytest


class TestCitationsHistoriques:
    """Verifie les 5 citations historiques (Riemann, Euler, Hilbert, Hardy)."""

    def test_5_citations_definies(self):
        from src.ui.cli import CITATIONS_HISTORIQUES
        assert len(CITATIONS_HISTORIQUES) == 5

    def test_citation_riemann_1859_presente(self):
        """La citation fondatrice de l'Hypothese de Riemann doit etre presente."""
        from src.ui.cli import CITATIONS_HISTORIQUES
        riemann_1859 = [
            c for c in CITATIONS_HISTORIQUES
            if c["auteur"] == "Bernhard Riemann" and c["annee"] == "1859"
        ]
        assert len(riemann_1859) >= 1, "Citation Riemann 1859 introuvable"
        # Verifie le coeur du texte : 'toutes les racines sont reelles'
        fondateur = riemann_1859[0]
        assert "racines" in fondateur["texte"].lower()
        assert "reelles" in fondateur["texte"].lower() or "réelles" in fondateur["texte"].lower()
        assert "Primzahlen" in fondateur["source"]

    def test_tous_auteurs_attendus(self):
        from src.ui.cli import CITATIONS_HISTORIQUES
        auteurs = {c["auteur"] for c in CITATIONS_HISTORIQUES}
        assert "Bernhard Riemann" in auteurs
        assert "Leonhard Euler" in auteurs
        assert "David Hilbert" in auteurs
        assert "Godfrey Harold Hardy" in auteurs

    def test_chaque_citation_a_champs_obligatoires(self):
        from src.ui.cli import CITATIONS_HISTORIQUES
        for cit in CITATIONS_HISTORIQUES:
            assert "auteur" in cit and cit["auteur"]
            assert "annee" in cit and cit["annee"]
            assert "source" in cit and cit["source"]
            assert "texte" in cit and len(cit["texte"]) > 50
            assert "note" in cit

    def test_pick_citation_deterministe_par_jour(self):
        from src.ui.cli import _pick_citation
        cit1 = _pick_citation()
        cit2 = _pick_citation()
        # Deux appels consecutifs le meme jour -> meme citation
        assert cit1["auteur"] == cit2["auteur"]
        assert cit1["annee"] == cit2["annee"]


class TestBannerContientCitationDuJour:
    def test_5e_panneau_present_dans_banner(self):
        from src.ui.cli import _build_banner_panels
        from rich.console import Console
        from io import StringIO
        buf = StringIO()
        Console(file=buf, force_terminal=False, width=120).print(_build_banner_panels())
        out = buf.getvalue()
        assert "Citation historique du jour" in out


class TestCommandesSplashAbout:
    """Verifie que splash/about/banner/citation sont reconnues."""

    def test_commandes_dans_autocomplete(self):
        from src.ui.keybindings import DEFAULT_COMMANDS
        for cmd in ("splash", "about", "banner", "citation", "citations", "cite"):
            assert cmd in DEFAULT_COMMANDS, f"{cmd} absent de DEFAULT_COMMANDS"

    def test_help_text_mentionne_splash_et_citation(self):
        from src.ui.cli import HELP_TEXT
        assert "splash" in HELP_TEXT
        assert "about" in HELP_TEXT
        assert "citation" in HELP_TEXT

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
