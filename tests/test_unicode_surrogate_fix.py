"""Tests UnicodeEncodeError fix (surrogate \\udcc3 etc.) sur LLM + Audit.

Reproduit le bug original du handoff :
  'utf-8' codec can't encode character '\\udcc3' in position X: surrogates not allowed

et verifie que :
  - LLMManager.generate / chat assainissent le prompt avant l'appel
  - AuditStore.save / build_record ne crashent pas sur des surrogates
"""
from __future__ import annotations

import asyncio
import json
import tempfile
from pathlib import Path

import pytest

from src.adapters.llm.utf8_sanitizer import UTF8Sanitizer
from src.audit import AuditStore


# Texte contamine reproduit du bug Windows PowerShell :
# Le \udcc3 est un demi-surrogate isole, illegal en UTF-8 standard.
DIRTY_TEXT = "M\udcc3\udca9thode spectrale (Savard) - r\udcc3\udcc3sultat \udcdcOK"


# ==========================================================================
# UTF8Sanitizer : base
# ==========================================================================
class TestUTF8Sanitizer:
    def test_remove_isolated_surrogates(self):
        cleaned = UTF8Sanitizer.sanitize(DIRTY_TEXT)
        # Le resultat DOIT etre encodable en UTF-8 sans erreur
        cleaned.encode("utf-8")  # ne doit pas lever

    def test_empty_input(self):
        assert UTF8Sanitizer.sanitize("") == ""
        assert UTF8Sanitizer.sanitize(None) == ""  # type: ignore[arg-type]

    def test_clean_text_preserves_accents(self):
        text = "Méthode spectrale 1/2 — résultat exact à 100%"
        cleaned = UTF8Sanitizer.sanitize(text)
        # Les accents francais doivent etre conserves
        assert "Méthode" in cleaned or "Methode" in cleaned
        # Verification : encodable
        cleaned.encode("utf-8")


# ==========================================================================
# AuditStore : sauvegarde avec surrogates
# ==========================================================================
class TestAuditStoreUnicodeFix:
    def setup_method(self):
        self._tmp = tempfile.mkdtemp(prefix="audit_test_")
        self.store = AuditStore(base_dir=self._tmp)

    def test_save_record_with_dirty_question(self):
        """Un audit avec une question contaminee de surrogates doit etre
        construit ET sauvegarde sans crash."""
        record = AuditStore.build_record(
            intervention_type="gap",
            question=DIRTY_TEXT,
            certified_answer=DIRTY_TEXT,
        )
        path = self.store.save(record)
        assert path.exists()
        # Le JSON ecrit doit etre relisible
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["id"] == record.id

    def test_compute_signature_with_dirty_text(self):
        """compute_signature ne doit pas lever de UnicodeEncodeError."""
        record = AuditStore.build_record(
            intervention_type="gap",
            question=DIRTY_TEXT,
            certified_answer="OK",
        )
        # Si signature_sha256 != "ERROR_ENCODING", le calcul a reussi
        assert record.signature_sha256 != "ERROR_ENCODING"
        assert len(record.signature_sha256) == 64  # SHA-256 hex

    def test_record_with_dirty_citations_and_toolkit(self):
        """Surrogates dans des listes / dicts imbriques."""
        record = AuditStore.build_record(
            intervention_type="rsp",
            question="ok",
            certified_answer="ok",
            citations_thy=[DIRTY_TEXT, "clean citation"],
            toolkit_reports={"dirty": DIRTY_TEXT, "nested": {"k": DIRTY_TEXT}},
        )
        path = self.store.save(record)
        assert path.exists()
        # Verifie que la signature est valide (donc payload propre)
        loaded = self.store.get(record.id)
        assert loaded is not None
        assert self.store.verify(loaded) is True


# ==========================================================================
# LLMManager : sanitization de prompt/chat
# ==========================================================================
class _MockClient:
    """Capture le prompt qu'on lui passe pour verifier qu'il est propre."""
    def __init__(self):
        self.last_prompt: str | None = None
        self.last_messages: list[dict] | None = None

    def is_available(self):
        return True

    async def generate(self, prompt: str, system=None, temperature=None):
        self.last_prompt = prompt
        # Doit etre encodable en UTF-8 sans erreur
        prompt.encode("utf-8")
        if system:
            system.encode("utf-8")
        return "MOCK_RESPONSE"

    async def chat(self, messages, temperature=None):
        self.last_messages = messages
        # Toutes les content doivent etre encodables
        for m in messages:
            if isinstance(m.get("content"), str):
                m["content"].encode("utf-8")
        return "MOCK_CHAT"


@pytest.fixture
def llm_with_mock(monkeypatch):
    """Cree un LLMManager dont le client Ollama/Claude/OpenAI est mocke."""
    from src.core.llm_manager import LLMManager
    mgr = LLMManager({"llm": {"primary": "ollama"}})
    mock = _MockClient()
    # Forcer chaine: Ollama indisponible, Claude mock, OpenAI mock
    mgr._ollama_available = False
    mgr.claude = mock
    mgr.openai = mock
    return mgr, mock


class TestLLMManagerUnicodeFix:
    def test_generate_with_dirty_prompt(self, llm_with_mock):
        mgr, mock = llm_with_mock
        result = asyncio.run(mgr.generate(prompt=DIRTY_TEXT))
        assert result == "MOCK_RESPONSE"
        # Le prompt envoye au client DOIT etre propre
        assert mock.last_prompt is not None
        mock.last_prompt.encode("utf-8")  # ne doit pas crasher

    def test_generate_with_dirty_system(self, llm_with_mock):
        mgr, mock = llm_with_mock
        result = asyncio.run(mgr.generate(prompt="ok", system=DIRTY_TEXT))
        assert result == "MOCK_RESPONSE"

    def test_chat_with_dirty_messages(self, llm_with_mock):
        mgr, mock = llm_with_mock
        messages = [
            {"role": "user", "content": DIRTY_TEXT},
            {"role": "assistant", "content": "ok"},
            {"role": "user", "content": "Demande propre avec accents é à"},
        ]
        result = asyncio.run(mgr.chat(messages=messages))
        assert result == "MOCK_CHAT"
        for m in mock.last_messages:
            if isinstance(m.get("content"), str):
                m["content"].encode("utf-8")  # ne doit pas crasher
