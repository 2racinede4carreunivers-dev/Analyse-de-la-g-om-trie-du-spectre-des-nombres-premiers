"""
Tests pour la mémoire conversationnelle courte (P1).

Couvre :
- La classe ConversationalMemory (ring-buffer, troncature, sérialisation).
- L'intégration dans LLMManager (flag `include_conversation`).
- L'intégration dans Orchestrator (enregistrement automatique + reset).
- L'intégration dans RefinementLoop (activation du flag pour la génération
  de réponse principale, mais pas pour critic/audit).
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.core.conversational_memory import (
    ConversationalMemory,
    ConversationTurn,
    merge_context_into_prompt,
)


# ============================================================================
# UNIT — ConversationalMemory
# ============================================================================

class TestConversationalMemoryBasics:
    def test_starts_empty(self):
        m = ConversationalMemory(max_turns=3)
        assert m.is_empty()
        assert len(m) == 0
        assert m.last() is None
        assert m.turns() == []

    def test_add_single_turn(self):
        m = ConversationalMemory(max_turns=3)
        m.add("Quel est le plan trifocal ?", "C'est le régime symétrique...")
        assert len(m) == 1
        assert not m.is_empty()
        assert m.last().question == "Quel est le plan trifocal ?"
        assert m.last().answer == "C'est le régime symétrique..."

    def test_add_multiple_turns_preserves_order(self):
        m = ConversationalMemory(max_turns=5)
        m.add("Q1", "A1")
        m.add("Q2", "A2")
        m.add("Q3", "A3")
        turns = m.turns()
        assert [t.question for t in turns] == ["Q1", "Q2", "Q3"]
        assert [t.answer for t in turns] == ["A1", "A2", "A3"]

    def test_ring_buffer_evicts_oldest(self):
        m = ConversationalMemory(max_turns=2)
        m.add("Q1", "A1")
        m.add("Q2", "A2")
        m.add("Q3", "A3")  # évince Q1
        turns = m.turns()
        assert len(turns) == 2
        assert turns[0].question == "Q2"
        assert turns[1].question == "Q3"

    def test_clear(self):
        m = ConversationalMemory()
        m.add("Q", "A")
        m.clear()
        assert m.is_empty()

    def test_snapshot(self):
        m = ConversationalMemory()
        m.add("Q1", "A1")
        m.add("Q2", "A2")
        snap = m.snapshot()
        assert snap == [
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ]


class TestConversationalMemoryValidation:
    def test_rejects_max_turns_lt_1(self):
        with pytest.raises(ValueError):
            ConversationalMemory(max_turns=0)
        with pytest.raises(ValueError):
            ConversationalMemory(max_turns=-1)

    def test_rejects_max_chars_too_small(self):
        with pytest.raises(ValueError):
            ConversationalMemory(max_chars_per_field=50)

    def test_rejects_non_string_add(self):
        m = ConversationalMemory()
        with pytest.raises(TypeError):
            m.add(42, "A")  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            m.add("Q", None)  # type: ignore[arg-type]

    def test_ignores_empty_qa(self):
        m = ConversationalMemory()
        m.add("   ", "\t\n")
        assert m.is_empty()


class TestConversationalMemoryTruncation:
    def test_truncates_long_answers(self):
        m = ConversationalMemory(max_chars_per_field=200)
        long_answer = "A" * 500
        m.add("Q", long_answer)
        stored = m.last().answer
        assert len(stored) <= 200
        assert stored.endswith("...")

    def test_short_answers_untouched(self):
        m = ConversationalMemory(max_chars_per_field=200)
        m.add("Q", "réponse courte")
        assert m.last().answer == "réponse courte"


class TestBuildContextBlock:
    def test_empty_returns_empty_string(self):
        m = ConversationalMemory()
        assert m.build_context_block() == ""

    def test_single_turn_block(self):
        m = ConversationalMemory()
        m.add("Le plan trifocal ?", "Régime symétrique.")
        block = m.build_context_block()
        assert "CONTEXTE CONVERSATIONNEL" in block
        assert "1 tour précédent" in block
        assert "Le plan trifocal" in block
        assert "Régime symétrique" in block
        assert "[Tour -1]" in block
        assert "NOUVELLE question" in block

    def test_two_turns_singular_plural(self):
        m = ConversationalMemory()
        m.add("Q1", "A1")
        m.add("Q2", "A2")
        block = m.build_context_block()
        assert "2 tours précédents" in block
        assert "[Tour -2]" in block
        assert "[Tour -1]" in block

    def test_order_oldest_to_newest(self):
        m = ConversationalMemory(max_turns=3)
        m.add("REGIMES", "Il y a 3 régimes...")
        m.add("TRIFOCAL", "Oui, symétrique.")
        m.add("ZERO", "Le zéro est spécial.")
        block = m.build_context_block()
        i_regimes = block.find("REGIMES")
        i_trifocal = block.find("TRIFOCAL")
        i_zero = block.find("ZERO")
        assert 0 < i_regimes < i_trifocal < i_zero

    def test_custom_header(self):
        m = ConversationalMemory()
        m.add("Q", "A")
        block = m.build_context_block(header="== HISTORIQUE CUSTOM ==")
        assert "HISTORIQUE CUSTOM" in block
        # Le header par défaut ne doit PAS apparaître
        assert "CONTEXTE CONVERSATIONNEL" not in block


class TestMergeContextIntoPrompt:
    def test_empty_context_returns_prompt_unchanged(self):
        assert merge_context_into_prompt("QUESTION", "") == "QUESTION"

    def test_context_is_prepended(self):
        merged = merge_context_into_prompt("QUESTION", "[CONTEXTE]")
        assert merged.startswith("[CONTEXTE]")
        assert merged.endswith("QUESTION")


# ============================================================================
# INTEGRATION — LLMManager avec ConversationalMemory
# ============================================================================

class TestLLMManagerConversationInjection:
    """Vérifie que LLMManager.generate() injecte le contexte SEULEMENT quand
    include_conversation=True est passé."""

    def _make_manager(self):
        # Import différé pour éviter d'initialiser Ollama/Claude/OpenAI
        # au load des tests.
        from src.core.llm_manager import LLMManager
        cfg = {
            "llm": {"primary": "claude", "fallback_1": "openai"},
            "claude": {"model": "claude-3-5-sonnet-latest"},
            "openai": {"model": "gpt-4o"},
            "ollama": {"model": "llama3.2"},
            "conversation": {"max_turns": 3, "max_chars_per_field": 500},
        }
        mgr = LLMManager(cfg)
        # On stub les 3 clients pour capturer les prompts finaux
        mgr.ollama = MagicMock()
        mgr.ollama.is_available = AsyncMock(return_value=False)
        mgr.ollama.generate = AsyncMock(return_value=None)
        mgr._ollama_available = False

        mgr.claude = MagicMock()
        mgr.claude.is_available = MagicMock(return_value=True)
        mgr.claude.generate = AsyncMock(return_value="RÉPONSE_CLAUDE")

        mgr.openai = MagicMock()
        mgr.openai.is_available = MagicMock(return_value=False)
        return mgr

    def test_memory_attribute_exists(self):
        mgr = self._make_manager()
        assert isinstance(mgr.conversation_memory, ConversationalMemory)
        assert mgr.conversation_memory.max_turns == 3

    def test_generate_without_flag_does_not_inject(self):
        mgr = self._make_manager()
        mgr.conversation_memory.add("Q_hist", "A_hist_XYZ_UNIQUE")
        asyncio.run(mgr.generate("NOUVELLE_QUESTION"))
        # Récupère le prompt réellement envoyé à Claude
        sent_prompt = mgr.claude.generate.call_args.args[0]
        assert "NOUVELLE_QUESTION" in sent_prompt
        assert "A_hist_XYZ_UNIQUE" not in sent_prompt
        assert "CONTEXTE CONVERSATIONNEL" not in sent_prompt

    def test_generate_with_flag_injects(self):
        mgr = self._make_manager()
        mgr.conversation_memory.add("Q_hist", "A_hist_XYZ_UNIQUE")
        asyncio.run(mgr.generate("NOUVELLE_QUESTION", include_conversation=True))
        sent_prompt = mgr.claude.generate.call_args.args[0]
        assert "NOUVELLE_QUESTION" in sent_prompt
        assert "A_hist_XYZ_UNIQUE" in sent_prompt
        assert "CONTEXTE CONVERSATIONNEL" in sent_prompt

    def test_generate_with_flag_but_empty_memory_no_prefix(self):
        mgr = self._make_manager()
        # Mémoire vide
        asyncio.run(mgr.generate("NOUVELLE_QUESTION", include_conversation=True))
        sent_prompt = mgr.claude.generate.call_args.args[0]
        assert "NOUVELLE_QUESTION" in sent_prompt
        assert "CONTEXTE CONVERSATIONNEL" not in sent_prompt


# ============================================================================
# INTEGRATION — Orchestrator enregistre après ask()
# ============================================================================

class TestOrchestratorRecordsConversation:
    """Vérifie que Orchestrator.ask() enregistre bien chaque tour dans la
    mémoire conversationnelle du LLM."""

    def _mock_orchestrator(self):
        from src.core.orchestrator import Orchestrator
        # On ne peut pas construire un vrai Orchestrator sans config lourde,
        # donc on bypasse __init__ et on injecte des mocks minimalistes.
        orch = Orchestrator.__new__(Orchestrator)
        orch.config = {}
        orch.memory = []

        # Mock pipeline avec un llm qui possède une vraie ConversationalMemory
        mock_pipeline = MagicMock()
        mock_pipeline.llm.conversation_memory = ConversationalMemory(max_turns=3)

        async def fake_process(question, progress_cb=None, force_mode=None):
            answer = MagicMock()
            answer.answer_text = f"RÉPONSE_À: {question}"
            return answer
        mock_pipeline.process = fake_process

        orch.pipeline = mock_pipeline
        return orch

    def test_ask_records_turn(self):
        orch = self._mock_orchestrator()
        asyncio.run(orch.ask("Le plan trifocal ?"))
        cm = orch.conversation_memory
        assert len(cm) == 1
        assert cm.last().question == "Le plan trifocal ?"
        assert "Le plan trifocal ?" in cm.last().answer

    def test_ask_records_multiple_turns(self):
        orch = self._mock_orchestrator()
        asyncio.run(orch.ask("Q1"))
        asyncio.run(orch.ask("Q2"))
        asyncio.run(orch.ask("Q3"))
        assert len(orch.conversation_memory) == 3
        assert [t.question for t in orch.conversation_memory.turns()] == [
            "Q1", "Q2", "Q3",
        ]

    def test_reset_conversation_clears_memory(self):
        orch = self._mock_orchestrator()
        asyncio.run(orch.ask("Q1"))
        asyncio.run(orch.ask("Q2"))
        orch.reset_conversation()
        assert orch.conversation_memory.is_empty()
        assert orch.memory == []

    def test_ring_buffer_respected(self):
        """max_turns=3 → seuls les 3 derniers restent."""
        orch = self._mock_orchestrator()
        for i in range(5):
            asyncio.run(orch.ask(f"Q{i}"))
        cm = orch.conversation_memory
        assert len(cm) == 3
        assert [t.question for t in cm.turns()] == ["Q2", "Q3", "Q4"]


# ============================================================================
# INTEGRATION — RefinementLoop active include_conversation=True
# ============================================================================

class TestRefinementLoopActivatesConversation:
    def test_generate_called_with_include_conversation_true(self):
        """Le RefinementLoop DOIT appeler llm.generate(include_conversation=True)
        pour la génération de réponse principale."""
        from src.multiloop.refinement_loop import RefinementLoop
        from src.core.types import QuestionContext

        # Mock LLM
        mock_llm = MagicMock()
        mock_llm.generate = AsyncMock(return_value="candidat_texte")

        # Mock critic
        mock_critic = MagicMock()
        async def fake_critique(cand, ctx, facts):
            cand.score = 9.0
            cand.critique = "OK"
            return cand
        mock_critic.critique = fake_critique

        loop = RefinementLoop(
            llm=mock_llm,
            critic=mock_critic,
            config={"multiloop": {"max_iterations": 1,
                                  "min_acceptance_score": 8.0,
                                  "num_candidates_per_round": 1}},
        )

        ctx = QuestionContext(question_id="test", raw_question="Q?")
        asyncio.run(loop.run(ctx, precomputed_facts=None, base_prompt=None))

        # Vérifier que TOUS les appels à generate ont include_conversation=True
        assert mock_llm.generate.called
        for call in mock_llm.generate.call_args_list:
            assert call.kwargs.get("include_conversation") is True, (
                "RefinementLoop DOIT propager include_conversation=True"
            )


# ============================================================================
# INTEGRATION — Critic et SilentAudit N'activent PAS include_conversation
# ============================================================================

class TestCriticDoesNotInjectConversation:
    """Le critic doit rester neutre et ne PAS voir l'historique conversationnel
    (sinon il pourrait critiquer une réponse pour être hors-sujet par rapport
    à un tour précédent, ce qui n'a pas de sens)."""

    def test_critic_generate_call_has_no_conversation_flag(self):
        import inspect
        from src.multiloop import critic as critic_module
        src = inspect.getsource(critic_module)
        # Le critic.py NE DOIT PAS activer include_conversation=True
        assert "include_conversation=True" not in src, (
            "critic.py ne doit PAS activer include_conversation=True"
        )


class TestSilentAuditDoesNotInjectConversation:
    def test_silent_audit_generate_call_has_no_conversation_flag(self):
        import inspect
        from src.multiloop import silent_audit
        src = inspect.getsource(silent_audit)
        assert "include_conversation=True" not in src, (
            "silent_audit.py ne doit PAS activer include_conversation=True"
        )
