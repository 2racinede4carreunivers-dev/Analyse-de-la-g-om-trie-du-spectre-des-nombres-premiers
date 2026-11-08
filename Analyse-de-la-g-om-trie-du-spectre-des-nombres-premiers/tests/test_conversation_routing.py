from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

from src.core.conversational_memory import ConversationalMemory
from src.core.llm_manager import LLMManager
from src.core.orchestrator import Orchestrator
from src.core.spectral_types import QuestionContext
from src.multiloop.pre_reasoner import PreReasoner, RequestMode
from src.multiloop.refinement_loop import RefinementLoop


def test_long_french_summary_is_routed_to_fast_verbal_mode():
    question = (
        "Merci bonne fille Gabriel? Est-ce que tu peux me faire un résumé complet "
        "de la géométrie du spectre des nombres premiers? Quels sont les points "
        "les plus marquants de cette géométrie?"
    )

    plan = PreReasoner().plan(question)

    assert plan.mode is RequestMode.RAPIDE
    assert plan.n_iterations == 1
    assert plan.skip_silent_audit


def test_failed_ollama_probe_is_retried():
    manager = LLMManager({"llm": {"primary": "ollama", "ollama_only": True}})
    manager.ollama.is_available = AsyncMock(side_effect=[False, True])

    assert asyncio.run(manager._check_ollama()) is False
    assert asyncio.run(manager._check_ollama()) is True
    assert manager.ollama.is_available.await_count == 2


def test_local_only_error_reports_model_and_timeout(monkeypatch):
    monkeypatch.delenv("OLLAMA_ONLY", raising=False)
    manager = LLMManager({
        "llm": {
            "primary": "ollama",
            "ollama_only": True,
            "ollama": {
                "model": "qwen2.5-coder:7b",
                "timeout_seconds": 17,
            },
        }
    })
    manager._check_ollama = AsyncMock(return_value=True)
    manager.ollama.generate = AsyncMock(return_value=None)

    response = asyncio.run(manager.generate("Question de test."))

    assert "qwen2.5-coder:7b" in response
    assert "17 s" in response
    assert "cloud" in response


def test_fast_verbal_response_uses_one_generation_and_skips_critic():
    llm = MagicMock()
    llm.generate = AsyncMock(return_value="Réponse conversationnelle.")
    critic = MagicMock()
    critic.critique = AsyncMock()
    loop = RefinementLoop(
        llm=llm,
        critic=critic,
        config={
            "multiloop": {
                "max_iterations": 3,
                "num_candidates_per_round": 2,
            }
        },
    )

    result = asyncio.run(loop.run(
        QuestionContext(question_id="test", raw_question="Résumé?"),
        max_iterations_override=1,
        num_candidates_override=1,
        skip_critique=True,
    ))

    llm.generate.assert_awaited_once()
    critic.critique.assert_not_awaited()
    assert result.answer_text == "Réponse conversationnelle."
    assert result.structured_data["critique_skipped"] is True
    assert result.best_score == 0


def test_llm_error_is_not_saved_in_conversation_memory():
    orchestrator = Orchestrator.__new__(Orchestrator)
    orchestrator.config = {}
    orchestrator.memory = []
    orchestrator.pipeline = MagicMock()
    orchestrator.pipeline.llm.conversation_memory = ConversationalMemory()
    result = MagicMock()
    result.answer_text = "[ERREUR LLM] Ollama n'a pas répondu."
    orchestrator.pipeline.process = AsyncMock(return_value=result)

    returned = asyncio.run(orchestrator.ask("Question interrompue"))

    assert returned is result
    assert orchestrator.memory == []
    assert orchestrator.conversation_memory.is_empty()
