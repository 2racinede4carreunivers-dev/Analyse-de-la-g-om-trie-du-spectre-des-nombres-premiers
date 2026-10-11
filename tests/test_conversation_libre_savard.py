"""Tests pour les 2 ameliorations 2026-06-28 :
1. System prompt enrichi (lexique technique + garde-fou domaine + opinion epistemologique)
2. Conversation libre / intent general avec plan d'action Savard
"""
from __future__ import annotations
import pytest


class TestSystemPromptEnrichi:
    """Verifie que le system prompt contient tous les nouveaux blocs."""

    @pytest.fixture
    def prompt(self):
        from src.spectral.spectral_knowledge import build_grounded_system_prompt
        return build_grounded_system_prompt()

    def test_garde_fou_domaine_present(self, prompt):
        assert "DOMAINE DE COMPETENCE STRICT" in prompt
        assert "univers au carre" in prompt.lower()
        assert "Geometrie du spectre" in prompt or "GEOMETRIE DU SPECTRE" in prompt

    def test_lexique_technique_present(self, prompt):
        assert "LEXIQUE TECHNIQUE SAVARD" in prompt
        # Termes cles du lexique
        for terme in ("rapport spectral", "suite A", "suite B", "digamma",
                      "plan trifocal", "asymetrie ordonnee", "asymetrie chaotique",
                      "postulat spectral", "droite critique"):
            assert terme.lower() in prompt.lower(), f"Terme '{terme}' absent du lexique"

    def test_references_auteurs_classiques(self, prompt):
        # Auteurs cites dans le lexique pour conversation libre
        for auteur in ("Bernhard Riemann", "Leonhard Euler", "von Mangoldt",
                       "Hadamard", "Hardy", "David Hilbert"):
            assert auteur in prompt, f"Auteur '{auteur}' absent"

    def test_autorise_opinion_epistemologique(self, prompt):
        # L'agent doit pouvoir exprimer une opinion informee
        assert "opinion" in prompt.lower()
        assert "epistemolog" in prompt.lower() or "intuition" in prompt.lower()

    def test_refus_hors_domaine(self, prompt):
        # Garde-fou explicite
        assert "Tu NE PEUX PAS" in prompt or "tu NE PEUX PAS" in prompt
        # Liste de domaines exclus
        for hors in ("politique", "cuisine", "sport", "medic", "financ"):
            assert hors in prompt.lower(), f"Le hors-domaine '{hors}' devrait etre liste"

    def test_taille_prompt_substantielle(self, prompt):
        # Avant: ~3500 chars. Apres: ~12000+ chars (avec lexique + garde-fou)
        assert len(prompt) > 8000, f"Prompt trop court: {len(prompt)} chars"


class TestMetaReasoningConversationLibre:
    """Verifie que l'intent 'general' a maintenant un plan d'action conversationnel."""

    def test_intent_general_a_plan_savard(self):
        from src.engines.meta_reasoning.meta_reasoning import ProofPlanner
        from src.core.types import QuestionContext

        ctx = QuestionContext(question_id="t1", raw_question="Test", metadata={})
        plan = ProofPlanner().plan(
            ctx,
            {"intent": "general"},
            {"strategy": "default", "default_model": "claude-sonnet-4-5"},
        )
        steps_str = " ".join(plan["steps"]).lower()
        assert "domaine" in steps_str
        assert ("lexique" in steps_str) or ("trifocal" in steps_str)
        assert "opinion" in steps_str or "epistemolog" in steps_str

    def test_intent_epistemological_route_vers_conversation(self):
        from src.engines.meta_reasoning.meta_reasoning import ProofPlanner
        from src.core.types import QuestionContext

        ctx = QuestionContext(question_id="t2", raw_question="Test", metadata={})
        plan = ProofPlanner().plan(
            ctx,
            {"intent": "epistemological"},
            {"strategy": "default", "default_model": "claude-sonnet-4-5"},
        )
        assert len(plan["steps"]) >= 5
        steps_str = " ".join(plan["steps"]).lower()
        assert "domaine" in steps_str
        assert "opinion" in steps_str
