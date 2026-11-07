"""
Test end-to-end de la mémoire conversationnelle : simule 3 questions
consécutives et vérifie que le prompt injecté au LLM contient bien le
contexte des tours précédents (le bug "Le plan trifocal oublié" corrigé).
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _make_llm_manager_with_stubbed_clients():
    """Instancie un LLMManager réel, mais stub les clients LLM sous-jacents
    (Ollama/Claude/OpenAI) pour intercepter les prompts."""
    from src.core.llm_manager import LLMManager

    cfg = {
        "llm": {"primary": "claude", "fallback_1": "openai"},
        "claude": {"model": "claude-3-5-sonnet-latest"},
        "openai": {"model": "gpt-4o"},
        "ollama": {"model": "llama3.2"},
        "conversation": {"max_turns": 3, "max_chars_per_field": 800},
    }
    mgr = LLMManager(cfg)

    mgr.ollama = MagicMock()
    mgr.ollama.is_available = AsyncMock(return_value=False)
    mgr._ollama_available = False

    # Compteur d'appels et capture des prompts
    mgr._prompts_captured = []

    async def fake_claude_generate(prompt, system=None, temperature=0.2):
        mgr._prompts_captured.append(prompt)
        idx = len(mgr._prompts_captured)
        return f"REPONSE_CLAUDE_{idx}"

    mgr.claude = MagicMock()
    mgr.claude.is_available = MagicMock(return_value=True)
    mgr.claude.generate = AsyncMock(side_effect=fake_claude_generate)

    mgr.openai = MagicMock()
    mgr.openai.is_available = MagicMock(return_value=False)
    return mgr


def test_e2e_multi_turn_conversation_context_is_propagated():
    """Scénario Philippe :
       1er tour : 'Quels sont les 3 régimes RsP ?'
       2e tour  : 'Le plan trifocal ?' -- Gabriel doit voir le tour 1.
       3e tour  : 'Et le rôle du zéro ?' -- Gabriel doit voir les tours 1+2.
    """
    mgr = _make_llm_manager_with_stubbed_clients()

    # --- Tour 1 : mémoire vide, aucun contexte injecté ---
    r1 = asyncio.run(mgr.generate(
        "Quels sont les 3 régimes RsP ?",
        include_conversation=True,
    ))
    assert r1 == "REPONSE_CLAUDE_1"
    prompt_1 = mgr._prompts_captured[0]
    assert "3 régimes RsP" in prompt_1
    # Tour 1 : rien à injecter (mémoire vide)
    assert "CONTEXTE CONVERSATIONNEL" not in prompt_1

    # Simuler l'enregistrement du tour (fait normalement par Orchestrator.ask)
    mgr.conversation_memory.add(
        "Quels sont les 3 régimes RsP ?", r1,
    )

    # --- Tour 2 : le contexte du tour 1 DOIT être injecté ---
    r2 = asyncio.run(mgr.generate(
        "Le plan trifocal ?",
        include_conversation=True,
    ))
    prompt_2 = mgr._prompts_captured[1]
    assert "Le plan trifocal ?" in prompt_2
    assert "CONTEXTE CONVERSATIONNEL" in prompt_2, (
        "Le tour 2 DOIT contenir le contexte du tour 1 (bug 'plan trifocal oublié')"
    )
    assert "3 régimes RsP" in prompt_2  # question du tour 1 visible
    assert "REPONSE_CLAUDE_1" in prompt_2  # réponse du tour 1 visible
    assert "[Tour -1]" in prompt_2

    mgr.conversation_memory.add("Le plan trifocal ?", r2)

    # --- Tour 3 : le contexte des tours 1 ET 2 doit être injecté ---
    r3 = asyncio.run(mgr.generate(
        "Et le rôle du zéro dans la Méthode Spectrale ?",
        include_conversation=True,
    ))
    prompt_3 = mgr._prompts_captured[2]
    assert "rôle du zéro" in prompt_3
    assert "CONTEXTE CONVERSATIONNEL" in prompt_3
    assert "2 tours précédents" in prompt_3
    assert "3 régimes RsP" in prompt_3
    assert "Le plan trifocal" in prompt_3
    assert "REPONSE_CLAUDE_1" in prompt_3
    assert "REPONSE_CLAUDE_2" in prompt_3
    assert "[Tour -2]" in prompt_3
    assert "[Tour -1]" in prompt_3


def test_e2e_ring_buffer_only_keeps_last_3():
    """Après 5 tours, seuls les 3 derniers doivent apparaître dans le prompt."""
    mgr = _make_llm_manager_with_stubbed_clients()

    for i in range(1, 6):  # tours 1 → 5
        r = asyncio.run(mgr.generate(
            f"QUESTION_UNIQUE_{i}",
            include_conversation=True,
        ))
        mgr.conversation_memory.add(f"QUESTION_UNIQUE_{i}", r)

    # 6e tour : le contexte doit contenir QUESTION_UNIQUE_3, 4, 5
    asyncio.run(mgr.generate(
        "NOUVELLE_Q",
        include_conversation=True,
    ))
    prompt_final = mgr._prompts_captured[-1]

    assert "QUESTION_UNIQUE_3" in prompt_final
    assert "QUESTION_UNIQUE_4" in prompt_final
    assert "QUESTION_UNIQUE_5" in prompt_final
    # Les 2 plus anciens ont été évincés
    assert "QUESTION_UNIQUE_1" not in prompt_final
    assert "QUESTION_UNIQUE_2" not in prompt_final


def test_e2e_conversation_flag_off_isolates_calls():
    """Si include_conversation=False, aucun contexte n'est injecté même
    si la mémoire est pleine (cas critic/silent_audit/debat)."""
    mgr = _make_llm_manager_with_stubbed_clients()
    mgr.conversation_memory.add("Q_HISTORIQUE_SECRETE", "REPONSE_SECRETE")

    asyncio.run(mgr.generate("Q_CRITIC_INDEPENDANTE", include_conversation=False))
    prompt = mgr._prompts_captured[0]
    assert "Q_CRITIC_INDEPENDANTE" in prompt
    assert "Q_HISTORIQUE_SECRETE" not in prompt
    assert "REPONSE_SECRETE" not in prompt


def test_e2e_orchestrator_auto_records_and_injects():
    """Simule le flow réel Orchestrator.ask() → mémoire remplie
    automatiquement → tour suivant injecte le contexte."""
    from src.core.orchestrator import Orchestrator

    orch = Orchestrator.__new__(Orchestrator)
    orch.config = {}
    orch.memory = []

    mock_pipeline = MagicMock()
    from src.core.conversational_memory import ConversationalMemory
    mock_pipeline.llm.conversation_memory = ConversationalMemory(max_turns=3)

    turn_count = {"n": 0}

    async def fake_process(question, progress_cb=None, force_mode=None):
        turn_count["n"] += 1
        answer = MagicMock()
        answer.answer_text = f"REPONSE_ORCH_{turn_count['n']}"
        return answer

    mock_pipeline.process = fake_process
    orch.pipeline = mock_pipeline

    # 3 tours consécutifs
    asyncio.run(orch.ask("Quels sont les 3 régimes RsP ?"))
    asyncio.run(orch.ask("Le plan trifocal ?"))
    asyncio.run(orch.ask("Et le rôle du zéro ?"))

    cm = orch.conversation_memory
    assert len(cm) == 3
    turns = cm.turns()
    assert turns[0].question == "Quels sont les 3 régimes RsP ?"
    assert turns[1].question == "Le plan trifocal ?"
    assert turns[2].question == "Et le rôle du zéro ?"
    assert turns[0].answer == "REPONSE_ORCH_1"
    assert turns[1].answer == "REPONSE_ORCH_2"
    assert turns[2].answer == "REPONSE_ORCH_3"

    # Le bloc contexte contient les 3 tours dans le bon ordre
    block = cm.build_context_block()
    assert "[Tour -3]" in block
    assert "[Tour -2]" in block
    assert "[Tour -1]" in block


def test_config_yaml_conversation_section_optional():
    """Le module doit fonctionner même si config['conversation'] est absent
    (défauts sensibles : 3 tours, 1500 chars)."""
    from src.core.llm_manager import LLMManager

    cfg = {
        "llm": {"primary": "claude", "fallback_1": "openai"},
        "claude": {"model": "claude-3-5-sonnet-latest"},
        "openai": {"model": "gpt-4o"},
        "ollama": {"model": "llama3.2"},
        # PAS de section 'conversation'
    }
    mgr = LLMManager(cfg)
    assert mgr.conversation_memory.max_turns == 3
    assert mgr.conversation_memory.max_chars_per_field == 1500
