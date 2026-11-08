"""
Tests v3.28 : Detection de contexte conversationnel pour bloquer l'auto-trigger
de visualisation quand la question est une discussion conceptuelle et non
une demande explicite de graphique.

Contexte : Philippe (2026-02) a rapporte que Gabriel declenchait a tort la
visualisation SA lorsqu'il expliquait un schema d'Archimede/quadrature de
parabole, parce que la question contenait des mots-cles isoles ("voir",
"schema", "represente") + un "sa" dans "sa longueur".

Objectif : garantir que le contexte conversationnel prime sur les mots-cles
techniques isoles, tout en preservant les demandes viz legitimes.
"""
from __future__ import annotations

import pytest

from src.visualization.auto_trigger import (
    detect_visualization_intent,
    _has_conversational_context,
    _CONVERSATIONAL_ANTI_PATTERNS,
    _normalize,
)


# =====================================================================
# CONTEXTE CONVERSATIONNEL : BLOQUE L'AUTO-TRIGGER
# =====================================================================


class TestConversationalContextBlocks:
    """Questions conceptuelles/discussion doivent NE PAS declencher de graphique."""

    def test_archimedes_parabola_scenario(self):
        """Scenario exact rapporte par Philippe (2026-02)."""
        q = (
            "Il s'agit en soit d'un schema inspire l'approche d'Archimede pour "
            "definir que les 4/3*aire du triangle donne l'aire d'une parabole "
            "il s'agit de l'exemple de la pese pour determiner a l'aide de cette "
            "peser theorique l'affirmation de la quadrature de la parabole? "
            "Le schema est constitue de la droite critique et coupe au tiers de "
            "sa longueur. Si tu observe bien les annotations tu peux voir que "
            "cette section a l'aire egale a l'aire de la parabole?"
        )
        assert detect_visualization_intent(q) is None, (
            "La question sur Archimede/parabole ne doit PAS auto-declencher "
            "une visualisation SA/SB"
        )

    @pytest.mark.parametrize("question", [
        "Il s'agit d'un triangle inscrit dans un cercle, laisse-moi t'expliquer.",
        "En soit, cette figure represente l'aire d'un rectangle. En realite...",
        "D'abord tu vois le triangle, ensuite le carre annote dans la parabole.",
        "Peux-tu comprendre le principe de la quadrature d'Archimede ?",
        "Explique-moi la difference entre l'aire et le perimetre du triangle.",
    ])
    def test_conceptual_discussions_blocked(self, question):
        assert detect_visualization_intent(question) is None, (
            f"Question conceptuelle ne devrait pas declencher viz : {question!r}"
        )

    def test_detects_2_or_more_markers(self):
        # 2 marqueurs = declanche le blocage
        q_norm = _normalize("Il s'agit en soit d'un triangle")
        is_conv, hits = _has_conversational_context(q_norm, len(q_norm))
        assert is_conv is True
        assert len(hits) >= 2

    def test_single_marker_short_question_ok(self):
        # 1 marqueur + question courte = laisse passer (pas assez conversationnel)
        q_norm = _normalize("aire de SA")
        is_conv, hits = _has_conversational_context(q_norm, len(q_norm))
        assert is_conv is False

    def test_single_marker_long_question_blocked(self):
        # 1 marqueur + question longue (>300 chars) = declanche le blocage
        long_q = ("Peux-tu m'aider avec ceci ? " * 20) + " et l'aire du triangle."
        q_norm = _normalize(long_q)
        is_conv, hits = _has_conversational_context(q_norm, len(long_q))
        assert is_conv is True


# =====================================================================
# DEMANDES VIZ LEGITIMES : DOIVENT PASSER
# =====================================================================


class TestLegitVizStillWorks:
    """Les demandes explicites de visualisation ne doivent PAS etre bloquees."""

    @pytest.mark.parametrize("q,expected_kind", [
        ("trace la courbe SA de 1 a 50", "SA"),
        ("montre-moi le rapport spectral pour n de 1 a 100", "ratio"),
        ("graphique de SA et SB avec export PNG", "SA_SB"),
        ("convergence de SA/SB vers 1/2", "ratio"),
        ("dessine la digamma sur 1..30", "digamma"),
        ("visualiser les ecarts entre premiers 1..50", "gap"),
        ("courbe SA de 1 a 100", "SA"),
    ])
    def test_explicit_viz_requests(self, q, expected_kind):
        intent = detect_visualization_intent(q)
        assert intent is not None, f"Demande viz explicite non detectee : {q!r}"
        assert intent.kind.value == expected_kind, (
            f"Type incorrect pour {q!r} : {intent.kind.value} vs {expected_kind}"
        )


# =====================================================================
# ANTI-PATTERNS : COUVERTURE
# =====================================================================


class TestAntiPatternsCoverage:
    """Verifie que les anti-patterns cles sont bien enregistres."""

    def test_archimedes_and_classical_math(self):
        for keyword in ["archimede", "parabole", "quadrature", "riemann",
                        "pythagore", "euclide"]:
            assert keyword in _CONVERSATIONAL_ANTI_PATTERNS, (
                f"Anti-pattern manquant : {keyword}"
            )

    def test_discussion_markers(self):
        for keyword in ["il s'agit", "laisse moi", "en soit", "en fait",
                        "je t'explique"]:
            assert keyword in _CONVERSATIONAL_ANTI_PATTERNS

    def test_geometric_non_spectral(self):
        for keyword in ["triangle", "carre", "rectangle", "cercle",
                        "aire", "surface", "peser"]:
            assert keyword in _CONVERSATIONAL_ANTI_PATTERNS
