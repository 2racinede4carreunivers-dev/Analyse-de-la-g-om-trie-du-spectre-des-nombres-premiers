"""Régressions QA du routage CLI ``image`` et des chemins Windows."""
from __future__ import annotations

import io
import re
from pathlib import Path

import pytest
from PIL import Image
from rich.console import Console

from src.core import filesystem_access as fa
from src.ui import cli as cli_module
from src.ui.cli import CLIInterface


def _cli_without_runtime() -> CLIInterface:
    """Construit uniquement le dispatcher, sans initialiser le pipeline LLM."""
    return CLIInterface.__new__(CLIInterface)


def _capture_console(monkeypatch: pytest.MonkeyPatch) -> io.StringIO:
    output = io.StringIO()
    monkeypatch.setattr(
        cli_module,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=180),
    )
    return output


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, expected_path, expected_question",
    [
        (
            r"image C:\theorie-mathematique-philippe-thomas-savard-2026\assets\images\figure.png Peux-tu analyser la géométrie et les zéros ?",
            r"C:\theorie-mathematique-philippe-thomas-savard-2026\assets\images\figure.png",
            "Peux-tu analyser la géométrie et les zéros ?",
        ),
        (
            "image c:/dossier/figure.png Décris les axes précisément",
            "c:/dossier/figure.png",
            "Décris les axes précisément",
        ),
        (
            r"image D:\images\figure.png Quelle courbe est critique ?",
            r"D:\images\figure.png",
            "Quelle courbe est critique ?",
        ),
    ],
)
async def test_image_alias_is_handled_before_natural_pipeline(
    command: str,
    expected_path: str,
    expected_question: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str | None]] = []

    def fake_analyser_image(chemin: str, question: str | None = None) -> str:
        calls.append((chemin, question))
        return "Analyse simulée"

    monkeypatch.setattr(fa, "analyser_image", fake_analyser_image)
    _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(command)

    assert handled is True
    assert calls == [(expected_path, expected_question)]


@pytest.mark.asyncio
async def test_image_alias_with_mount_map_reaches_missing_key_error_without_api_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image_dir = tmp_path / "sub"
    image_dir.mkdir()
    Image.new("RGB", (3, 3), color="blue").save(image_dir / "vision.png")
    monkeypatch.setenv("WINDOWS_MOUNT_MAP", f"C:={tmp_path}")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("CLAUDE_API_KEY", raising=False)
    output = _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(
        r"image C:\sub\vision.png Analyse cette figure en détail"
    )

    assert handled is True
    rendered = output.getvalue()
    assert "Analyse Claude Vision en cours" in rendered
    assert "Cle Anthropic manquante" in rendered


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command, expected_fragments",
    [
        (
            r"image C:\Users\Philippe\image.png Analyse ceci",
            ("Chemin Windows detecte", "WINDOWS_MOUNT_MAP", "docker-compose"),
        ),
        (
            r"image C:\theorie-mathematique-philippe-thomas-savard-2026\assets\images\x.png Analyse ceci",
            ("Chemin Windows detecte", "theorie-savard", "docker-compose.yml"),
        ),
    ],
)
async def test_image_alias_reports_explicit_windows_mount_help(
    command: str,
    expected_fragments: tuple[str, ...],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("WINDOWS_MOUNT_MAP", raising=False)
    output = _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(command)

    assert handled is True
    rendered = output.getvalue()
    for fragment in expected_fragments:
        assert fragment in rendered


@pytest.mark.asyncio
@pytest.mark.parametrize("alias", ["analyser-image", "analyser"])
async def test_existing_analysis_aliases_still_work(
    alias: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str | None]] = []

    def fake_analyser_image(chemin: str, question: str | None = None) -> str:
        calls.append((chemin, question))
        return "ok"

    monkeypatch.setattr(fa, "analyser_image", fake_analyser_image)
    _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(
        f"{alias} /tmp/figure.png question avec accents éàç"
    )

    assert handled is True
    assert calls == [("/tmp/figure.png", "question avec accents éàç")]


@pytest.mark.asyncio
@pytest.mark.parametrize("alias", ["voir-image", "voir"])
async def test_existing_preview_aliases_still_work(
    alias: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image_path = tmp_path / "native.png"
    Image.new("RGB", (5, 4), color="green").save(image_path)
    output = _capture_console(monkeypatch)

    handled = await _cli_without_runtime()._handle_special(f"{alias} {image_path}")

    assert handled is True
    rendered = output.getvalue()
    assert "Apercu image" in rendered
    assert "5 x 4 px" in rendered


def test_commands_panel_lists_image_alias(monkeypatch: pytest.MonkeyPatch) -> None:
    output = _capture_console(monkeypatch)

    _cli_without_runtime()._show_full_commands()

    rendered = output.getvalue()
    normalized = re.sub(r"\s+", " ", rendered)
    assert "FICHIERS & IMAGES" in normalized
    assert "image <chemin> [question]" in normalized
    assert "analyse Claude Vision" in normalized


def test_mount_map_supports_lowercase_drive_forward_slashes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    destination = tmp_path / "dossier" / "fichier.txt"
    destination.parent.mkdir()
    destination.write_text("contenu", encoding="utf-8")
    monkeypatch.setenv("WINDOWS_MOUNT_MAP", f"C:={tmp_path};D:=/mnt/d")

    result = fa.lire_fichier("c:/dossier/fichier.txt")

    assert result.path == destination
    assert result.content == "contenu"


def test_canonical_windows_path_checks_known_mounts(monkeypatch: pytest.MonkeyPatch) -> None:
    expected = Path("/home/agent/app/data/theorie-savard/assets/images/figure.png")
    original_exists = Path.exists

    def selective_exists(path: Path) -> bool:
        if path == expected:
            return True
        return original_exists(path)

    monkeypatch.delenv("WINDOWS_MOUNT_MAP", raising=False)
    monkeypatch.setattr(Path, "exists", selective_exists)

    resolved = fa._resolve(
        r"C:\theorie-mathematique-philippe-thomas-savard-2026\assets\images\figure.png"
    )

    assert resolved == expected

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
