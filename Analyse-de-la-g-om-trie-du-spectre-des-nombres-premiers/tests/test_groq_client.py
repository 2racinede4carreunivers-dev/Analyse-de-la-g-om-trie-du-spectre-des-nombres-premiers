from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.adapters.llm.groq_client import GroqClient
from src.core.llm_manager import LLMManager


def test_groq_client_reads_key_from_environment(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    assert GroqClient().is_available()


def test_groq_client_rejects_empty_or_placeholder_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    assert not GroqClient().is_available()
    assert not GroqClient(api_key="VOTRE_CLE_GROQ_ICI").is_available()


@pytest.mark.asyncio
async def test_groq_chat_uses_openai_compatible_client():
    create = AsyncMock(
        return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="  Reponse Groq  "))]
        )
    )
    client = GroqClient(api_key="test-key", model="test-model")
    client._client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )

    response = await client.chat([{"role": "user", "content": "Bonjour"}])

    assert response == "Reponse Groq"
    create.assert_awaited_once()
    assert create.await_args.kwargs["model"] == "test-model"


@pytest.mark.asyncio
async def test_manager_uses_groq_after_ollama_fails():
    manager = LLMManager(
        {
            "llm": {
                "primary": "ollama",
                "ollama_only": False,
                "ollama": {"model": "qwen2.5-coder:7b"},
                "groq": {"model": "test-model"},
            }
        }
    )
    manager._check_ollama = AsyncMock(return_value=False)
    manager.groq.is_available = lambda: True
    manager.groq.generate = AsyncMock(return_value="Reponse Groq")

    response = await manager.generate("Explique le spectre des nombres premiers.")

    assert response == "Reponse Groq"
    manager.groq.generate.assert_awaited_once()


@pytest.mark.asyncio
async def test_manager_chat_uses_groq_after_ollama_fails():
    manager = LLMManager(
        {
            "llm": {
                "primary": "ollama",
                "ollama_only": False,
                "ollama": {"model": "qwen2.5-coder:7b"},
                "groq": {"model": "test-model"},
            }
        }
    )
    manager._check_ollama = AsyncMock(return_value=False)
    manager.groq.is_available = lambda: True
    manager.groq.chat = AsyncMock(return_value="Reponse Groq")

    response = await manager.chat([{"role": "user", "content": "Bonjour"}])

    assert response == "Reponse Groq"
    manager.groq.chat.assert_awaited_once()


@pytest.mark.asyncio
async def test_manager_local_only_mode_does_not_call_groq(monkeypatch):
    monkeypatch.delenv("OLLAMA_ONLY", raising=False)
    manager = LLMManager(
        {
            "llm": {
                "primary": "ollama",
                "ollama_only": True,
                "ollama": {"model": "qwen2.5-coder:7b"},
            }
        }
    )
    manager._check_ollama = AsyncMock(return_value=False)
    manager.groq.is_available = lambda: True
    manager.groq.generate = AsyncMock(return_value="Unexpected")

    response = await manager.generate("Question de test.")

    assert response.startswith("[ERREUR LLM]")
    manager.groq.generate.assert_not_awaited()
