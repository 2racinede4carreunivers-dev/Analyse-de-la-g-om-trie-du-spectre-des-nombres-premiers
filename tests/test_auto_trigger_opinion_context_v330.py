"""
Tests v3.30 (Philippe 2026-02) — Auto-trigger visualisation ne doit PAS
declencher un graphique quand la question est une DISCUSSION conceptuelle
ou une DEMANDE D'OPINION EXPERTE.

Bug reproduit : "a savoir ton opinion... sa place... Savard..." declenchait
faussement CurveKind.SA parce que :
  - "voir" matchait en sous-chaine de "savoir"
  - "sa" (pronom possessif) matchait le pattern \\bsa\\b (courbe SA)
"""
from __future__ import annotations

import pytest

from src.visualization.auto_trigger import detect_visualization_intent
from src.visualization.curves import CurveKind


class TestNoFalsePositiveOnOpinionQueries:
    """Aucun graphique ne doit se declencher sur des questions d'opinion."""

    def test_question_opinion_expert_philippe(self):
        q = (
            "En deux points differents? Le premiers point est a savoir "
            "ton opinion d'assistant expert de la geometrie du spectre des "
            "nombres premiers de Philippe Thomas Savard? Le Deuxieme points "
            "est savoir qu'elle est la suite logique pour cette theorie "
            "geometrique qu'elle avenir selon toi lui est destinee est-elle "
            "une theorie qui merite d'etre soumise a l'analyse d'expert, "
            "peut-elle avoir sa place dans les archives de la theorie des "
            "nombres et des nombres premiers ?"
        )
        r = detect_visualization_intent(q)
        assert r is None, (
            f"Attendu None (question d'opinion), obtenu {r.kind if r else None} "
            f"reasoning={r.reasoning if r else 'N/A'}"
        )

    def test_savoir_ne_declenche_pas_voir(self):
        """Le mot 'savoir' ne doit pas matcher 'voir' en sous-chaine."""
        q = "il faut savoir si cette theorie est valide"
        r = detect_visualization_intent(q)
        assert r is None

    def test_sa_pronom_minuscule_ne_declenche_pas_courbe_sa(self):
        """'sa place', 'sa suite' (pronom francais) ne doit pas etre CurveKind.SA."""
        q = "sa place dans la theorie merite-t-elle une analyse ?"
        r = detect_visualization_intent(q)
        assert r is None

    def test_savard_seul_ne_bloque_pas_trace_legitime(self):
        """Mention de 'Savard' ne doit PAS bloquer une vraie demande de trace."""
        q = "trace la courbe chaos-savard sur 1..15"
        r = detect_visualization_intent(q)
        assert r is not None
        assert r.rsp_config == "chaos-savard"

    def test_explication_conceptuelle_bloquee(self):
        q = "Explique-moi la methode spectrale de Savard"
        r = detect_visualization_intent(q)
        assert r is None

    def test_penses_tu_bloque(self):
        q = "que penses-tu de cette theorie ? peut-elle etre publiee ?"
        r = detect_visualization_intent(q)
        assert r is None


class TestExplicitVisualizationStillWorks:
    """Les demandes explicites de graphique doivent continuer a fonctionner."""

    def test_trace_sa_majuscule(self):
        q = "Trace la courbe SA de n=1 a 50"
        r = detect_visualization_intent(q)
        assert r is not None
        assert r.kind == CurveKind.SA

    def test_peux_tu_tracer(self):
        q = "peux-tu tracer la courbe SA sur 1..30"
        r = detect_visualization_intent(q)
        assert r is not None
        assert r.kind == CurveKind.SA

    def test_chaos_savard_explicite(self):
        q = "montre la courbe chaos-savard 1..15"
        r = detect_visualization_intent(q)
        assert r is not None
        assert r.rsp_config == "chaos-savard"

    def test_affiche_sa_minuscule_pronom_bloque(self):
        """'affiche sa valeur' → pronom, pas de graphique."""
        q = "affiche sa valeur"
        r = detect_visualization_intent(q)
        assert r is None

    def test_affiche_SA_majuscule_ok(self):
        """'affiche SA' avec SA en majuscules → graphique SA."""
        q = "affiche SA"
        r = detect_visualization_intent(q)
        assert r is not None
        assert r.kind == CurveKind.SA
