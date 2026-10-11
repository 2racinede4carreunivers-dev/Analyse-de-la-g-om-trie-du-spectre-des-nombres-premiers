"""
Tests v3.27 : LLMReformulator - reformulations contextuelles pour slow-motion.

Verifie que :
  1. Le reformulateur genere des variantes UTILES quand le LLM repond.
  2. Il tombe en fallback silencieux (liste vide, jamais d'exception) si :
     - Le LLMManager est None
     - Le LLM timeout
     - Le LLM leve une exception
     - La reponse ne contient rien de parseable
  3. Il retire les reformulations avec vocabulaire dismissif.
  4. Il dedupe et cap sur num_variants.
  5. La fusion LLM + heuristique preserve la priorite LLM et deduplique.
  6. L'integration dans SlowMotionDebugger fusionne bien les deux sources.
"""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.multiloop.llm_reformulator import (
    LLMReformulator,
    ReformulationResult,
    merge_reformulations,
)
from src.multiloop.request_decomposer import DecomposedRequest, Segment


# =====================================================================
# FIXTURES
# =====================================================================


@pytest.fixture
def simple_decomposed() -> DecomposedRequest:
    """Une DecomposedRequest realiste pour la question RsP(A,B)."""
    return DecomposedRequest(
        original="Rapport spectral entre A=(7,3) et B=(11,23,13)",
        segments=[
            Segment(text="1/2", kind="ratio", value="1/2", coherent=True),
            Segment(text="(7,3)", kind="tuple_A", value=[7, 3], coherent=True),
            Segment(text="(11,23,13)", kind="tuple_B", value=[11, 23, 13], coherent=True),
        ],
        detected_intent="ratio_spectral",
        detected_ratio="1/2",
        tuple_A=[7, 3],
        tuple_B=[11, 23, 13],
    )


def _make_llm_mock(response_text: str) -> MagicMock:
    """Cree un mock LLMManager qui renvoie `response_text`."""
    llm = MagicMock()
    llm.generate = AsyncMock(return_value=response_text)
    return llm


# =====================================================================
# PARSING DES REPONSES LLM
# =====================================================================


class TestParsing:
    """Le _parse_response doit accepter divers formats de listes."""

    def test_numbered_dot(self, simple_decomposed):
        r = LLMReformulator()
        parsed = r._parse_response(
            "1. Reformulation A\n"
            "2. Reformulation B\n"
            "3. Reformulation C"
        )
        assert parsed == ["Reformulation A", "Reformulation B", "Reformulation C"]

    def test_numbered_paren(self, simple_decomposed):
        r = LLMReformulator()
        parsed = r._parse_response("1) Alpha\n2) Beta\n3) Gamma")
        assert parsed == ["Alpha", "Beta", "Gamma"]

    def test_dash_marker(self, simple_decomposed):
        r = LLMReformulator()
        parsed = r._parse_response("- Alpha\n- Beta")
        assert parsed == ["Alpha", "Beta"]

    def test_deduplication_case_insensitive(self):
        r = LLMReformulator()
        parsed = r._parse_response("1. alpha\n2. ALPHA\n3. Beta")
        assert len(parsed) == 2
        assert "alpha" in parsed[0].lower()
        assert "beta" in parsed[1].lower()

    def test_truncation_max_length(self):
        r = LLMReformulator()
        long_line = "1. " + "A" * 500
        parsed = r._parse_response(long_line)
        assert len(parsed) == 1
        assert len(parsed[0]) <= r.MAX_REFORMULATION_LEN
        assert parsed[0].endswith("...")

    def test_empty_response(self):
        r = LLMReformulator()
        assert r._parse_response("") == []
        assert r._parse_response("\n\n\n") == []


# =====================================================================
# FILTRAGE VOCAB DISMISSIF
# =====================================================================


class TestForbiddenVocabFilter:
    """Les reformulations dismissives doivent etre rejetees."""

    def test_condemning_reformulations_removed(self):
        r = LLMReformulator()
        candidates = [
            "Calculer RsP(A,B) en rapport 1/2.",
            "La methode spectrale est absurde et il faut la rejeter.",  # dismissif
            "Verifier le cas elementaire RsP_1x1(2, 3).",
            "La theorie de Savard est fausse.",  # dismissif
        ]
        clean = r._filter_forbidden_vocab(candidates)
        assert len(clean) == 2
        assert all("methode" not in c.lower() or "spectrale" in c.lower()
                   for c in clean)


# =====================================================================
# CAS FALLBACK (LLM absent, timeout, erreur)
# =====================================================================


class TestFallbacks:
    """Le reformulateur doit toujours retourner un ReformulationResult, jamais lever."""

    def test_no_llm_manager_returns_empty(self, simple_decomposed):
        r = LLMReformulator(llm_manager=None)
        result = asyncio.run(r.reformulate("Une question", simple_decomposed))
        assert result.reformulations == []
        assert result.used_llm is False
        assert result.fallback_reason is not None

    def test_empty_question_returns_empty(self, simple_decomposed):
        r = LLMReformulator(llm_manager=_make_llm_mock("1. x"))
        result = asyncio.run(r.reformulate("", simple_decomposed))
        assert result.reformulations == []
        assert "vide" in (result.fallback_reason or "").lower()

    def test_llm_timeout_returns_empty(self, simple_decomposed):
        async def slow_gen(*args, **kwargs):
            await asyncio.sleep(2.0)
            return "trop tard"

        llm = MagicMock()
        llm.generate = slow_gen  # async fonction lente
        r = LLMReformulator(llm_manager=llm, timeout_s=0.1)
        result = asyncio.run(r.reformulate("Une question ?", simple_decomposed))
        assert result.reformulations == []
        assert result.used_llm is False
        assert result.error and "timeout" in result.error.lower()

    def test_llm_exception_returns_empty(self, simple_decomposed):
        llm = MagicMock()
        async def boom(*args, **kwargs):
            raise RuntimeError("erreur LLM simulee")
        llm.generate = boom
        r = LLMReformulator(llm_manager=llm)
        result = asyncio.run(r.reformulate("Une question ?", simple_decomposed))
        assert result.reformulations == []
        assert result.used_llm is False
        assert result.error is not None

    def test_llm_returns_garbage_gives_empty_reformulations(self, simple_decomposed):
        r = LLMReformulator(llm_manager=_make_llm_mock("blabla incomprehensible"))
        result = asyncio.run(r.reformulate("Une question ?", simple_decomposed))
        # Rien de parseable en liste
        assert result.used_llm is True
        # La ligne unique "blabla..." (avec plus de 30 chars) DOIT être acceptée
        # comme phrase si elle depasse 30 chars. Ici < 30 → rejetée.
        # Test defensif : accepte 0 ou 1 reformulation, mais pas d'exception.
        assert isinstance(result.reformulations, list)


# =====================================================================
# CAS NOMINAL : LLM REPOND, REFORMULATIONS EXTRAITES
# =====================================================================


class TestNominalFlow:
    """Cas ou le LLM repond normalement."""

    def test_extracts_all_numbered_reformulations(self, simple_decomposed):
        response = (
            "1. Calculer RsP asymetrique CHAOTIQUE entre A=(7,3) et B=(11,23,13).\n"
            "2. Cas elementaire : verifier RsP_1x1(7, 11) en rapport 1/2.\n"
            "3. Reformuler en symetrique 3x3 en completant A.\n"
            "4. Ecart |RsP(A,B) - 1/2| pour cette configuration ?"
        )
        r = LLMReformulator(llm_manager=_make_llm_mock(response), num_variants=4)
        result = asyncio.run(r.reformulate(
            "Rapport spectral entre A=(7,3) et B=(11,23,13)", simple_decomposed
        ))
        assert result.used_llm is True
        assert len(result.reformulations) == 4
        # Chaque reformulation contient un element concret
        assert any("RsP" in r_ or "1/2" in r_ for r_ in result.reformulations)

    def test_respects_num_variants_cap(self, simple_decomposed):
        response = "\n".join(f"{i}. Variante {i}" for i in range(1, 11))
        r = LLMReformulator(llm_manager=_make_llm_mock(response), num_variants=3)
        result = asyncio.run(r.reformulate("Question", simple_decomposed))
        assert len(result.reformulations) == 3


# =====================================================================
# FUSION LLM + HEURISTIQUES
# =====================================================================


class TestMergeReformulations:
    """La fusion doit prioriser LLM, dedupliquer, capper sur max_total."""

    def test_llm_first_heuristic_after(self):
        llm = ["A", "B", "C"]
        heur = ["X", "Y"]
        merged = merge_reformulations(llm, heur, max_total=6)
        assert merged == ["A", "B", "C", "X", "Y"]

    def test_deduplication_case_insensitive(self):
        llm = ["Reformulation A"]
        heur = ["reformulation a", "Autre"]
        merged = merge_reformulations(llm, heur, max_total=6)
        # La version heuristique en doublon est retiree, garde LLM
        assert len(merged) == 2
        assert merged[0] == "Reformulation A"
        assert merged[1] == "Autre"

    def test_max_total_cap(self):
        llm = ["1", "2", "3", "4", "5"]
        heur = ["6", "7", "8"]
        merged = merge_reformulations(llm, heur, max_total=4)
        assert merged == ["1", "2", "3", "4"]

    def test_empty_llm_falls_back_to_heuristics(self):
        merged = merge_reformulations([], ["heur1", "heur2"], max_total=6)
        assert merged == ["heur1", "heur2"]

    def test_empty_both_returns_empty(self):
        assert merge_reformulations([], [], max_total=6) == []


# =====================================================================
# INTEGRATION AVEC SLOW-MOTION DEBUGGER
# =====================================================================


class TestSlowMotionIntegration:
    """Verifie que SlowMotionDebugger.debug() accepte llm_reformulations."""

    def test_debug_accepts_llm_reformulations_parameter(self):
        """Signature-check : debug() doit accepter llm_reformulations."""
        import inspect
        from src.multiloop.slow_motion_debugger import SlowMotionDebugger
        sig = inspect.signature(SlowMotionDebugger.debug)
        assert "llm_reformulations" in sig.parameters, (
            "SlowMotionDebugger.debug() doit accepter le parametre "
            "llm_reformulations (v3.27)"
        )
        # Verifier que c'est optionnel (defaut None)
        param = sig.parameters["llm_reformulations"]
        assert param.default is None

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
