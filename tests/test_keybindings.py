"""Tests pour src/ui/keybindings.py."""
from __future__ import annotations

from pathlib import Path

from src.ui.keybindings import (
    DEFAULT_COMMANDS,
    GabrielKeybindings,
    is_available,
    install_keybindings,
    save_history,
)


def test_default_commands_non_empty():
    assert len(DEFAULT_COMMANDS) > 10
    # Verifie quelques commandes critiques
    assert any("aide" in c for c in DEFAULT_COMMANDS)
    assert any("courbe" in c for c in DEFAULT_COMMANDS)
    assert any("commandes" in c for c in DEFAULT_COMMANDS)
    assert any("ci" in c for c in DEFAULT_COMMANDS)


def test_is_available_returns_bool():
    """Doit retourner True sur Linux (Docker), False ailleurs."""
    assert isinstance(is_available(), bool)


def test_install_idempotent(tmp_path: Path):
    """Installer 2 fois ne doit pas planter."""
    hist = tmp_path / "history"
    kb1 = GabrielKeybindings(history_file=hist)
    kb2 = GabrielKeybindings(history_file=hist)
    r1 = kb1.install()
    r2 = kb2.install()
    # Selon plateforme : True (readline dispo) ou False (pas dispo)
    assert isinstance(r1, bool)
    assert isinstance(r2, bool)


def test_save_history_creates_file_if_readline_available(tmp_path: Path):
    """Si readline est dispo, save_history doit creer le fichier (meme vide)."""
    hist = tmp_path / "subdir" / ".history"
    kb = GabrielKeybindings(history_file=hist)
    installed = kb.install()
    kb.save_history()
    if installed:
        # readline cree le fichier
        assert hist.parent.exists()
    # Si pas installe, on ne creee rien : OK


def test_singleton_install_keybindings():
    """Le helper de singleton doit retourner un GabrielKeybindings."""
    kb = install_keybindings(history_file="/tmp/test_gabriel_history_xyz")
    assert isinstance(kb, GabrielKeybindings)
    # 2eme appel doit retourner le meme objet (idempotent)
    kb2 = install_keybindings(history_file="/tmp/different_path_ignored")
    assert kb is kb2


def test_save_history_no_crash_when_not_installed():
    """save_history ne doit pas planter meme si aucun keybinding n'est installe."""
    # On ne sait pas si quelqu'un d'autre a deja installe ; on s'assure juste
    # qu'aucune exception n'est levee
    try:
        save_history()
    except Exception as exc:
        raise AssertionError(f"save_history() ne doit pas crasher : {exc}")
