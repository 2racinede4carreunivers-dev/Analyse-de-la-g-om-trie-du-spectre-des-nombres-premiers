"""Tests de la fonction vision de Gabriel : commandes !image / !analyser /
!historique, chemins Windows natifs et systeme de vision complet."""
from __future__ import annotations

import io
from pathlib import Path

import pytest
from PIL import Image, ImageDraw
from rich.console import Console

from src.core import vision_gabriel as vg
from src.ui import cli as cli_module
from src.ui.cli import CLIInterface


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _cli_without_runtime() -> CLIInterface:
    """Construit uniquement le dispatcher, sans initialiser le pipeline LLM."""
    return CLIInterface.__new__(CLIInterface)


def _capture_console(monkeypatch: pytest.MonkeyPatch) -> io.StringIO:
    output = io.StringIO()
    monkeypatch.setattr(
        cli_module,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=200),
    )
    return output


def _make_figure(path: Path) -> None:
    img = Image.new("RGB", (120, 90), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 10, 80, 70), outline="black", width=3)
    draw.line((10, 80, 110, 80), fill="black", width=2)
    draw.line((10, 10, 10, 80), fill="black", width=2)
    img.save(path, format="PNG")


@pytest.fixture(autouse=True)
def _fresh_terminal_vision(monkeypatch: pytest.MonkeyPatch):
    """Isole l'historique des images entre chaque test (singleton)."""
    monkeypatch.setattr(vg, "_terminal_vision", None)
    yield
    monkeypatch.setattr(vg, "_terminal_vision", None)


# ------------------------------------------------------------------
# Commande !image : analyse locale + guidance Claude Vision
# ------------------------------------------------------------------

@pytest.mark.asyncio
async def test_image_commande_charge_analyse_locale(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    p = tmp_path / "figure_locale.png"
    _make_figure(p)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
    output = _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(f"!image {p}")

    assert handled is True
    rendered = output.getvalue()
    # Rapport local affiche (metadonnees reelles)
    assert "Vision Gabriel (local)" in rendered
    assert "figure_locale.png" in rendered
    assert "120x90 px" in rendered
    # Pas de cle Claude -> guidance explicite (pas de plantage)
    assert "Cle Anthropic manquante" in rendered
    # L'historique est renseigne
    tv = vg.get_terminal_vision()
    assert len(tv.historique_images) == 1
    assert tv.historique_images[0]["chemin"] == str(p)


@pytest.mark.asyncio
async def test_image_commande_affiche_usage_sans_argument(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special("!image")

    assert handled is True
    assert "Usage : !image <chemin>" in output.getvalue()


@pytest.mark.asyncio
async def test_image_commande_image_inexistante(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(
        r"!image C:\dossier_qui_n_existe_pas\manque.png"
    )

    assert handled is True
    assert "Erreur" in output.getvalue()


# ------------------------------------------------------------------
# Commandes !analyser et !historique (persistance du singleton)
# ------------------------------------------------------------------

@pytest.mark.asyncio
async def test_analyser_et_historique_persistent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    p = tmp_path / "derniere.png"
    _make_figure(p)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
    output = _capture_console(monkeypatch)

    await _cli_without_runtime()._handle_special(f"!image {p}")
    handled_analyser = await _cli_without_runtime()._handle_special("!analyser")
    handled_hist = await _cli_without_runtime()._handle_special("!historique")

    assert handled_analyser is True
    assert handled_hist is True
    rendered = output.getvalue()
    assert "DERNI" in rendered
    assert str(p) in rendered
    assert "Images charg" in rendered


# ------------------------------------------------------------------
# Systeme de vision complet (regression : imports paquet/plat)
# ------------------------------------------------------------------

def test_complete_vision_system_capabilities_disponibles() -> None:
    import src.complete_vision_system as cvs

    assert cvs.VISION_AVAILABLE is True
    assert cvs.ADVANCED_VISION_AVAILABLE is True
    assert cvs.ACCESS_AVAILABLE is True


def test_analyse_complete_fonctionnelle(tmp_path: Path) -> None:
    import src.complete_vision_system as cvs

    p = tmp_path / "formes.png"
    _make_figure(p)

    result = cvs.analyze_image_complete(str(p))

    assert result.success is True, result.error_message
    assert result.full_report
    assert "geometric" in result.capabilities_used


def test_gabriel_image_interface_disponible() -> None:
    import src.gabriel_image_interface as gii

    assert gii.VISION_AVAILABLE is True
    interface = gii.get_gabriel_image_interface()
    assert interface.vision_system is not None


# ------------------------------------------------------------------
# Analyse locale de VisionGabriel : metadonnees reelles
# ------------------------------------------------------------------

def test_vision_gabriel_description_metadonnees_reelles(tmp_path: Path) -> None:
    p = tmp_path / "meta.png"
    _make_figure(p)

    vision = vg.VisionGabriel()
    analyse = vision.analyser_image(str(p))

    assert "erreur" not in analyse
    # Description construite depuis PIL (pas de placeholder)
    assert "120x90 px" in analyse["description"]
    assert "PNG" in analyse["description"]
    # OCR honnete : pas de faux texte extrait
    assert "OCR local indisponible" in analyse["texte"]
    # Base64 disponible pour transmission API
    assert len(analyse["base64"]) > 0


def test_pipeline_vision_degradation_propre() -> None:
    """Les commandes ! du pipeline Vision_agent_image ne planent jamais, meme
    si ses sous-modules sont absents du depot (degradation explicite)."""
    from Vision_agent_image.pipeline_vision import traiter_commande

    rep = traiter_commande("!figures")
    assert rep is not None
    assert ("Figures" in rep) or ("Module vision absent" in rep)
    assert traiter_commande("une question naturelle") is None

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports

