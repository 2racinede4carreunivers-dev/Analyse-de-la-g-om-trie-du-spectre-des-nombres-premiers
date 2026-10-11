"""
Tests pour DebugSession (mode debugger manuel pedagogique).

On simule les entrees clavier en patchant `console.input` et on verifie :
  - Validation des limites de longueur (requete + commentaire)
  - Toggle de segments par lettre
  - Ajout d'un commentaire et re-decomposition
  - Execution finale produisant une FinalAnswer certifiee
  - Annulation propre (q)
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from rich.console import Console

from src.ui.debug_session import (
    DebugSession, MAX_REQUEST_CHARS, MAX_COMMENT_CHARS, _DebugState,
)


THEORIES = str(ROOT / "theories")


def _make_session() -> DebugSession:
    from src.adapters.corpus.certainty_kernel import CertaintyKernel
    from src.core.spectral_core import SpectralMethodCore
    return DebugSession(
        console=Console(force_terminal=False, no_color=True, record=True),
        certainty_kernel=CertaintyKernel(theories_dir=THEORIES),
        spectral_core=SpectralMethodCore(),
    )


# ---------- Validations de longueur ----------

def test_validate_question_length_accepts_normal():
    ok, _ = DebugSession.validate_question_length("Reconstruis le 26eme premier")
    assert ok


def test_validate_question_length_rejects_empty():
    ok, msg = DebugSession.validate_question_length("")
    assert not ok and "vide" in msg.lower()


def test_validate_question_length_rejects_too_long():
    q = "x" * (MAX_REQUEST_CHARS + 1)
    ok, msg = DebugSession.validate_question_length(q)
    assert not ok
    assert str(MAX_REQUEST_CHARS) in msg


def test_validate_comment_length_accepts_normal():
    ok, _ = DebugSession.validate_comment_length("petit ajustement")
    assert ok


def test_validate_comment_length_rejects_too_long():
    c = "x" * (MAX_COMMENT_CHARS + 1)
    ok, msg = DebugSession.validate_comment_length(c)
    assert not ok
    assert str(MAX_COMMENT_CHARS) in msg


def test_validate_max_combined_fits():
    """1600 + 400 doit etre exactement le total max."""
    q = "a" * MAX_REQUEST_CHARS
    c = "b" * MAX_COMMENT_CHARS
    ok_q, _ = DebugSession.validate_question_length(q)
    ok_c, _ = DebugSession.validate_comment_length(c)
    assert ok_q and ok_c
    assert MAX_REQUEST_CHARS + MAX_COMMENT_CHARS == 2000


# ---------- _DebugState ----------

def test_debug_state_combined_no_comment():
    state = _DebugState(base_question="Reconstruis le 26eme premier")
    assert state.combined_question == "Reconstruis le 26eme premier"


def test_debug_state_combined_with_comment():
    state = _DebugState(base_question="Reconstruis le 26eme premier", comment="en rapport 1/2")
    assert "en rapport 1/2" in state.combined_question
    assert "Reconstruis le 26eme premier" in state.combined_question


# ---------- Flux interactif (simulation clavier) ----------

@pytest.mark.asyncio
async def test_session_quit_immediately():
    """Tapez 'q' au premier prompt -> session annulee."""
    session = _make_session()
    inputs = iter(["q"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 26eme premier en rapport 1/2")
    assert result is None


@pytest.mark.asyncio
async def test_session_execute_immediately_certified_answer():
    """Tapez 'e' direct -> resultat certifie produit."""
    session = _make_session()
    inputs = iter(["e"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 26eme premier en rapport 1/2")
    assert result is not None
    assert "101" in result.answer_text
    assert result.confidence == 1.0
    assert result.structured_data.get("manual_debug") is True


@pytest.mark.asyncio
async def test_session_toggle_segment_then_execute():
    """
    Tapez 'A' pour basculer le premier segment (position 26 en GARDE -> BYPASS) puis 'e'.
    La reponse certifiee devrait alors etre moins precise (position bypassed).
    """
    session = _make_session()
    inputs = iter(["A", "e"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 26eme premier en rapport 1/2")
    assert result is not None
    bypass = result.structured_data.get("forced_bypass", [])
    assert "A" in bypass


@pytest.mark.asyncio
async def test_session_add_comment_and_execute():
    """Tapez 'c' puis un commentaire valide puis 'e'."""
    session = _make_session()
    inputs = iter(["c", "verifie via Wolfram aussi", "e"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 26eme premier en rapport 1/2")
    assert result is not None
    assert result.structured_data.get("user_comment") == "verifie via Wolfram aussi"
    # La reponse doit toujours mentionner 101 (le commentaire ne change pas la requete)
    assert "101" in result.answer_text


@pytest.mark.asyncio
async def test_session_rejects_oversized_comment_then_accepts():
    """Tente un commentaire trop long, puis un valide."""
    session = _make_session()
    too_long = "x" * (MAX_COMMENT_CHARS + 50)
    inputs = iter(["c", too_long, "c", "court commentaire", "e"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 26eme premier en rapport 1/2")
    assert result is not None
    assert result.structured_data.get("user_comment") == "court commentaire"


@pytest.mark.asyncio
async def test_session_rejects_oversized_question():
    """Requete > 1600 caracteres -> rejet immediat, pas d'interaction."""
    session = _make_session()
    huge = "x" * (MAX_REQUEST_CHARS + 1)
    result = await session.run(huge)
    assert result is None


@pytest.mark.asyncio
async def test_session_unknown_command_ignored_then_execute():
    """Une commande inconnue ne sort pas de la boucle."""
    session = _make_session()
    inputs = iter(["zzz", "e"])
    with patch.object(session.console, "input", side_effect=lambda *_a, **_k: next(inputs)):
        result = await session.run("Reconstruis le 5eme premier en rapport 1/2")
    assert result is not None
    assert "11" in result.answer_text  # 5e premier = 11

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
