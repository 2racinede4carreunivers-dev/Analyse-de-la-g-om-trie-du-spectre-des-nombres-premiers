"""
Tests v3.23 : verifie le correctif "i-eme premier" reporte par Philippe le
2026-07-09. Avant le fix : "Peux tu reconstruire le i-eme premier ?" declenchait
le Slow-Motion Debugger avec score 0.40 et basculait sur kernel_emergency_summary
(perte de contexte, pas de reference a prime_i). Apres fix : detection du pattern
generique + reponse dediee citant prime_i + theoreme prime_equation_prime_i.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.multiloop.request_decomposer import RequestDecomposer  # noqa: E402


class TestDetectGenericPrimeIQuery:
    """Le decomposer doit detecter les requetes generiques sur prime_i."""

    @pytest.fixture(scope="class")
    def dec(self):
        return RequestDecomposer()

    @pytest.mark.parametrize("question", [
        "Peux-tu reconstruire le i-ème premier ?",
        "Determine le i-eme premier",
        "Reconstruire le i-ième premier",
        "Reconstruis le n-ième nombre premier",
        "Comment definir prime_i ?",
        "Que vaut le n-eme premier ?",
        "Peux-tu m'expliquer prime_i",
    ])
    def test_pattern_detected(self, dec, question):
        result = dec.decompose(question)
        assert result.is_generic_prime_i_query is True, (
            f"Question '{question}' aurait du declencher is_generic_prime_i_query"
        )

    @pytest.mark.parametrize("question", [
        "Reconstruis le 5-ieme premier",       # nombre concret
        "Peux-tu reconstruire le 100e premier ?",  # nombre concret
        "Le 12-ieme nombre premier",           # nombre concret
        "Rapport spectral 2*2",                # autre intent
    ])
    def test_pattern_not_confused_by_numeric(self, dec, question):
        """Ne doit PAS declencher pour les positions concretes."""
        result = dec.decompose(question)
        # Ces requetes sont valides mais AVEC un nombre concret :
        # elles ne doivent pas etre marquees "generique"
        assert result.is_generic_prime_i_query is False, (
            f"Question '{question}' a un nombre concret, ne doit pas etre generique"
        )


class TestSlowMotionAnsweGenericPrimeI:
    """Le Slow-Motion Debugger doit repondre correctement avec prime_i."""

    def test_kernel_generic_prime_i_method(self):
        """Verifie que _solve_certified retourne bien la reponse
        prime_i quand is_generic_prime_i_query est True."""
        from src.multiloop.slow_motion_debugger import SlowMotionDebugger
        from src.multiloop.request_decomposer import DecomposedRequest

        # Instancier le debugger avec ses dependances legeres
        try:
            dbg = SlowMotionDebugger()
        except TypeError:
            # Certaines versions requierent des params obligatoires
            pytest.skip("SlowMotionDebugger requiert des dependances")

        dec = DecomposedRequest(original="Peux-tu reconstruire le i-eme premier?")
        dec.is_generic_prime_i_query = True
        dec.detected_intent = "reconstruction"

        result = dbg._solve_certified(dec)
        assert result is not None
        assert "prime_i" in result["summary"], (
            "La reponse doit mentionner prime_i explicitement"
        )
        assert "prime_equation_prime_i" in result["summary"], (
            "La reponse doit citer le theoreme prime_equation_prime_i"
        )
        assert result["method"] == "kernel_generic_prime_i (v3.23)"
        # Doit contenir des exemples concrets
        assert "examples" in result
        assert len(result["examples"]) >= 4

    def test_examples_are_correct(self):
        """Les exemples numeriques generes doivent etre les bons premiers."""
        from src.multiloop.slow_motion_debugger import SlowMotionDebugger
        from src.multiloop.request_decomposer import DecomposedRequest

        try:
            dbg = SlowMotionDebugger()
        except TypeError:
            pytest.skip("SlowMotionDebugger requiert des dependances")

        dec = DecomposedRequest(original="prime_i c'est quoi?")
        dec.is_generic_prime_i_query = True
        result = dbg._solve_certified(dec)

        # Exemples attendus: prime_i(1)=2, prime_i(5)=11, prime_i(10)=29, prime_i(100)=541
        examples_dict = dict(result["examples"])
        assert examples_dict[1] == 2
        assert examples_dict[5] == 11
        assert examples_dict[10] == 29
        assert examples_dict[100] == 541

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
