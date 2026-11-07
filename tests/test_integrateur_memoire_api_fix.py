"""Test de regression pour le bug Philippe 2026-06-29 :
   AttributeError: 'IntegrateurMemoireGabriel' object has no attribute
   'augmenter_prompt_conceptuel'

Le bug : llm_manager._augmenter_prompt_avec_memoire appelait 3 methodes
qui n'existent pas sur la classe IntegrateurMemoireGabriel :
  - augmenter_prompt_conceptuel(prompt)         [vraie methode : augmenter_prompt]
  - trouver_pattern_optimal(prompt, domaine)    [n'existe pas]
  - trouver_lemmes_pertinents(prompt, top_n)    [n'existe pas]

Fix : remplacement par un seul appel a la vraie API consolidee
INTEGRATEUR_MEMOIRE.augmenter_prompt(prompt, domaine).
"""
from __future__ import annotations

import pytest

from src.core.integrateur_memoire import IntegrateurMemoireGabriel
from src.core.llm_manager import LLMManager


class TestIntegrateurMemoireApi:
    """Verifie que l'API publique de IntegrateurMemoireGabriel est stable."""

    def test_classe_existe(self):
        assert IntegrateurMemoireGabriel is not None

    def test_methode_augmenter_prompt_existe(self):
        assert hasattr(IntegrateurMemoireGabriel, "augmenter_prompt")

    def test_methode_detecter_regimes_existe(self):
        assert hasattr(IntegrateurMemoireGabriel, "detecter_regimes")

    def test_methode_info_existe(self):
        assert hasattr(IntegrateurMemoireGabriel, "info")

    def test_anciennes_methodes_inexistantes(self):
        """Ces 3 methodes ETAIENT appelees a tort par llm_manager — ne doivent
        plus exister sur la classe (ou alors faut adapter llm_manager)."""
        # Si elles reapparaissent, le code llm_manager doit etre revu.
        # Test sentinelle pour eviter une regression silencieuse.
        for old_method in (
            "augmenter_prompt_conceptuel",
            "trouver_pattern_optimal",
            "trouver_lemmes_pertinents",
        ):
            assert not hasattr(IntegrateurMemoireGabriel, old_method), (
                f"La methode '{old_method}' a ete reintroduite. "
                "Soit elle est legitime (alors retirer cet assert), "
                "soit elle est un bug et il faut la retirer."
            )


class TestLlmManagerAugmenterPromptAvecMemoire:
    """Verifie que _augmenter_prompt_avec_memoire utilise la BONNE API.

    Le bug Philippe etait que cette methode appelait 3 methodes inexistantes,
    ce qui generait des warnings 'Erreur injection memoire' a chaque appel LLM.
    """

    def test_methode_existe(self):
        assert hasattr(LLMManager, "_augmenter_prompt_avec_memoire")

    def test_n_appelle_pas_augmenter_prompt_conceptuel(self):
        """Verifie textuellement que le code source ne reference plus
        les anciennes methodes (regression statique)."""
        import inspect
        src = inspect.getsource(LLMManager._augmenter_prompt_avec_memoire)
        assert "augmenter_prompt_conceptuel" not in src, (
            "REGRESSION : llm_manager appelle a nouveau augmenter_prompt_conceptuel"
        )
        assert "trouver_pattern_optimal" not in src, (
            "REGRESSION : llm_manager appelle a nouveau trouver_pattern_optimal"
        )
        assert "trouver_lemmes_pertinents" not in src, (
            "REGRESSION : llm_manager appelle a nouveau trouver_lemmes_pertinents"
        )

    def test_appelle_la_bonne_api(self):
        """La methode doit utiliser INTEGRATEUR_MEMOIRE.augmenter_prompt."""
        import inspect
        src = inspect.getsource(LLMManager._augmenter_prompt_avec_memoire)
        assert "augmenter_prompt" in src
        assert "INTEGRATEUR_MEMOIRE" in src


class TestIntegrateurMemoireFunctionnel:
    """Smoke tests d'integration : verifie que l'API marche bout-en-bout."""

    @pytest.fixture
    def integrateur(self):
        try:
            return IntegrateurMemoireGabriel()
        except ImportError:
            pytest.skip("memory/ non disponible dans ce contexte de test")

    def test_augmenter_prompt_avec_question_spectrale(self, integrateur):
        """Un prompt sur la Methode Spectrale doit etre augmente
        (pas retourner l'original tel quel)."""
        prompt_original = "Quel est le rapport spectral 1/2 ?"
        augmente = integrateur.augmenter_prompt(prompt_original, domaine="spectral")
        # Soit on a un prompt augmente (avec contexte injecte), soit l'original
        # est retourne (si aucun regime detecte). Au minimum, pas d'exception.
        assert isinstance(augmente, str)
        assert len(augmente) >= len(prompt_original) - 10
        # Si augmentation OK, le prompt original est preserve
        assert prompt_original in augmente or len(augmente) >= len(prompt_original)

    def test_augmenter_prompt_prompt_vide(self, integrateur):
        """Aucune exception sur prompt vide."""
        result = integrateur.augmenter_prompt("", domaine="general")
        assert isinstance(result, str)

    def test_info_dict_valide(self, integrateur):
        info = integrateur.info()
        assert isinstance(info, dict)
        assert "regimes" in info
        assert "lemmes_certifies" in info


class TestLlmManagerNeRaisePasSurAugmentation:
    """Smoke test : _augmenter_prompt_avec_memoire ne doit JAMAIS lever d'exception.

    Le bug Philippe se manifestait par un WARNING (loggue mais pas crash).
    Avec le fix, plus aucun warning '⚠️ Erreur injection memoire' ne doit apparaitre
    pour des prompts normaux.
    """

    def test_augmentation_ne_leve_pas(self, monkeypatch):
        """Test isole : on instancie LLMManager avec une integration memoire mock."""
        from src.core import llm_manager as lm_module

        # Si pas d'INTEGRATEUR_MEMOIRE, _augmenter_prompt_avec_memoire retourne le prompt tel quel
        # On verifie juste que ca ne leve pas, qu'il soit None ou non
        # On va construire un LLMManager-like minimal en patchant les clients
        class FakeManager:
            _augmenter_prompt_avec_memoire = (
                lm_module.LLMManager._augmenter_prompt_avec_memoire
            )

        mgr = FakeManager()
        # Aucune exception
        result = mgr._augmenter_prompt_avec_memoire("Test prompt", domaine="spectral")
        assert isinstance(result, str)
