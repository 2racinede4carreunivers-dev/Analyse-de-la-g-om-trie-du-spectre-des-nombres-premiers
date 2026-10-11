"""
Tests pour le AntiHallucinationValidator.audit() et SilentAuditLoop.

Verifie que :
  1. audit() detecte les hallucinations de prime
  2. audit() detecte la violation de l'INVARIANT 1/2 (n != position)
  3. audit() detecte le vocabulaire interdit
  4. audit() retourne valid=True quand tout est correct
  5. SilentAuditLoop corrige silencieusement via re-prompt mock
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import pytest

# Permettre l'import depuis src/
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.spectral_core import AntiHallucinationValidator
from src.core.types import FinalAnswer
from src.multiloop.silent_audit import SilentAuditLoop


# ---------- Tests unitaires AntiHallucinationValidator.audit() ----------

def test_audit_valid_answer_passes():
    """Une reponse correcte avec le bon prime doit passer."""
    v = AntiHallucinationValidator()
    question = "Reconstruis le 26eme nombre premier en rapport 1/2"
    answer = (
        "Pour la position 26, le nombre premier est 101. "
        "Avec n=26 et 26 termes dans A et B, l'invariant est respecte."
    )
    result = v.audit(question, answer)
    assert result["valid"] is True, f"Devrait passer mais : {result['violations']}"
    assert result["violations"] == []


def test_audit_detects_wrong_prime():
    """Une reponse avec un mauvais prime doit etre rejetee."""
    v = AntiHallucinationValidator()
    question = "Reconstruis le 26eme premier"
    answer = (
        "Le 26eme nombre premier est 97. "  # FAUX : 26eme = 101
        "Avec n=26 termes, l'invariant est respecte."
    )
    result = v.audit(question, answer)
    assert result["valid"] is False
    assert any("101" in v for v in result["violations"])


def test_audit_detects_invariant_violation_1_2():
    """INVARIANT 1/2 : si question parle de position 26, n DOIT etre 26."""
    v = AntiHallucinationValidator()
    question = "Reconstruis le 26eme nombre premier en rapport 1/2"
    answer = (
        "Le 26eme nombre premier est 101. "
        "Avec n=10 termes dans A et B."  # VIOLATION : n=10 != position=26
    )
    result = v.audit(question, answer)
    assert result["valid"] is False
    assert any("INVARIANT" in v for v in result["violations"])


def test_audit_detects_forbidden_vocabulary():
    """Le vocabulaire dismissif est interdit."""
    v = AntiHallucinationValidator()
    question = "Reconstruis le 5eme premier"
    answer = "Le 5eme nombre premier est 11. Mais cette methode est incoherente."
    result = v.audit(question, answer)
    assert result["valid"] is False
    assert any("incoherent" in v.lower() for v in result["violations"])


def test_audit_corrective_prompt_contains_truth():
    """Le prompt correctif doit contenir la verite terrain."""
    v = AntiHallucinationValidator()
    question = "Reconstruis le 26eme premier"
    answer = "Le 26eme nombre premier est 97."  # faux
    result = v.audit(question, answer)
    assert result["valid"] is False
    assert "101" in result["corrective_prompt"]  # vraie valeur
    assert "26" in result["corrective_prompt"]


def test_audit_extract_position_variations():
    """L'extraction de position doit gerer plusieurs formats."""
    v = AntiHallucinationValidator()
    cases = [
        ("Reconstruis le 26eme premier", 26),
        ("le 26e nombre premier", 26),
        ("le 26ème premier", 26),
        ("le 26ième nombre premier", 26),
        ("position 56", 56),
        ("rang 100", 100),
    ]
    for text, expected in cases:
        got = v._extract_position(text)
        assert got == expected, f"'{text}' -> got {got}, expected {expected}"


def test_audit_no_position_returns_valid():
    """Si pas de position dans la question, validation passe (rien a verifier)."""
    v = AntiHallucinationValidator()
    result = v.audit("Bonjour, comment vas-tu ?", "Tres bien merci.")
    assert result["valid"] is True


# ---------- Tests SilentAuditLoop avec LLM mock ----------

class _MockLLM:
    """LLM mock qui retourne une reponse predefinie."""
    def __init__(self, responses: list[str]):
        self.responses = list(responses)
        self.calls = 0

    async def generate(self, prompt: str, system: str = "", temperature: float = 0.1) -> str:
        self.calls += 1
        if self.responses:
            return self.responses.pop(0)
        return ""


def _make_final(text: str) -> FinalAnswer:
    return FinalAnswer(
        question_id="test-id",
        answer_text=text,
        structured_data={},
        confidence=0.5,
        iterations_used=1,
        best_score=8.0,
        candidates=[],
        explanation="",
    )


@pytest.mark.asyncio
async def test_silent_audit_passes_valid_answer():
    """Si la reponse est deja valide, aucun re-prompt."""
    config = {"audit": {"enabled": True, "max_retries": 2}}
    mock_llm = _MockLLM([])  # pas de reponse car aucun re-prompt attendu
    audit = SilentAuditLoop(mock_llm, config)

    question = "Reconstruis le 26eme premier en rapport 1/2"
    final = _make_final("Le 26eme nombre premier est 101 avec n=26 termes.")
    facts = {"position": 26, "prime": 101, "n": 26, "num_terms": 26, "model": "1/2"}

    result = await audit.audit_and_correct(question, final, facts)
    assert mock_llm.calls == 0
    assert "101" in result.answer_text


@pytest.mark.asyncio
async def test_silent_audit_corrects_hallucination():
    """Si hallucination, re-prompte le LLM et retourne la version corrigee."""
    config = {"audit": {"enabled": True, "max_retries": 2}}
    corrected = "Le 26eme nombre premier est 101 avec n=26 termes dans A et B."
    mock_llm = _MockLLM([corrected])
    audit = SilentAuditLoop(mock_llm, config)

    question = "Reconstruis le 26eme premier en rapport 1/2"
    final = _make_final("Le 26eme premier est 97 avec n=10 termes.")  # FAUX
    facts = {"position": 26, "prime": 101, "n": 26, "num_terms": 26, "model": "1/2"}

    result = await audit.audit_and_correct(question, final, facts)
    assert mock_llm.calls == 1, "Le LLM aurait du etre re-prompte 1 fois"
    assert result.answer_text == corrected


@pytest.mark.asyncio
async def test_silent_audit_disabled_skips():
    """Si audit.enabled=False, ne fait rien."""
    config = {"audit": {"enabled": False}}
    mock_llm = _MockLLM([])
    audit = SilentAuditLoop(mock_llm, config)

    original = "Reponse fausse 97"
    final = _make_final(original)
    result = await audit.audit_and_correct("Le 26eme premier", final, {"position": 26, "prime": 101})
    assert result.answer_text == original
    assert mock_llm.calls == 0


@pytest.mark.asyncio
async def test_silent_audit_max_retries_then_gives_up():
    """Apres max_retries echecs, annote le FinalAnswer et arrete."""
    config = {"audit": {"enabled": True, "max_retries": 2}}
    # Le LLM continue de halluciner : retourne tout le temps la mauvaise reponse
    bad_answers = ["Le 26eme premier est 97.", "Le 26eme est encore 97."]
    mock_llm = _MockLLM(bad_answers)
    audit = SilentAuditLoop(mock_llm, config)

    question = "Reconstruis le 26eme premier"
    final = _make_final("Le 26eme est 97.")  # faux des le depart
    facts = {"position": 26, "prime": 101, "model": "1/2"}

    result = await audit.audit_and_correct(question, final, facts)
    assert mock_llm.calls == 2, f"Devrait etre 2 retries, got {mock_llm.calls}"
    assert result.structured_data.get("audit_failed") is True
    assert "audit_violations" in result.structured_data

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
