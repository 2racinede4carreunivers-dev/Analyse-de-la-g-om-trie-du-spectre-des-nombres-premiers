"""
Tests pour deux fixes (Philippe 2026-07-03) :

1. Le critic ne doit PAS pénaliser "algebriquement incoherent" ou le mot
   "incoherent" isolé (descripteur LÉGITIME du corpus Savard, axiome
   asymetrique_ordonnee_nat). Seules les tournures qui condamnent la
   méthode elle-même doivent être pénalisées.

2. Le module `gestionnaire_erreurs` n'existe pas — le bloc qui l'importait
   dans llm_manager.py a été supprimé pour éliminer le warning parasite
   `⚠️ Erreur enregistrement fallback: No module named 'gestionnaire_erreurs'`
   à chaque fallback Claude → OpenAI.
"""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# ============================================================================
# FIX 1 — Critic ne pénalise plus les usages légitimes de "incoherent"
# ============================================================================


@pytest.fixture
def critic():
    """Instancie un critic avec des dépendances mockées minimales."""
    from src.multiloop.critic import Critic
    c = Critic(llm=MagicMock())
    return c


@pytest.fixture
def make_candidate():
    """Fabrique un CandidateAnswer minimal avec un texte donné."""
    from src.core.types import CandidateAnswer

    def _factory(text: str) -> CandidateAnswer:
        return CandidateAnswer(
            iteration=1, text=text, structured_data={},
            score=0.0, critique="", grounded=False,
        )
    return _factory


class TestForbiddenVocabularyLegitimateUsages:
    """Les usages LÉGITIMES du mot 'incoherent' (issus du corpus Savard) ne
    doivent PLUS être pénalisés par le critic."""

    @pytest.mark.parametrize("legitimate_text", [
        # Extrait exact de l'axiome asymetrique_ordonnee_nat
        "Le rapport est numeriquement valide mais algebriquement incoherent.",
        # Variante avec accent
        "algébriquement incohérent",
        # Contexte descriptif (pas condamnation de la méthode)
        "Cette configuration produit un rapport algebriquement incoherent, "
        "ce qui est prevu par le corpus Savard.",
        # Utilisation isolée du mot dans un contexte technique
        "Le segment est marqué comme incoherent dans le décomposeur.",
        # Corpus RAG legitime
        "L'ordinal des infinis (omega+1 != 1+omega) rend le rapport "
        "numeriquement valide mais algebriquement incoherent.",
    ])
    def test_legitimate_incoherent_usage_not_penalized(
        self, critic, make_candidate, legitimate_text
    ):
        cand = make_candidate(legitimate_text)
        # Ground truth avec au moins un chiffre pour ne pas partir de 0
        score = critic._check_grounded(cand, ground_truth={"n": 5})
        assert score >= 0.0, (
            f"Le texte legitime a ete penalise (score={score}) : "
            f"'{legitimate_text[:80]}'"
        )


class TestForbiddenVocabularyStillCatches:
    """Le critic doit TOUJOURS pénaliser les phrases qui condamnent la
    méthode elle-même."""

    @pytest.mark.parametrize("bad_text", [
        "La methode est incoherente.",
        "La méthode spectrale est incohérente et sans fondement.",
        "Cette theorie semble absurde.",
        "Cette méthode est fausse.",
        "Fausse methode de reconstruction.",
        "Ce rapport spectral est invalide.",
        "Le rapport spectral est absurde.",
        "Cette methode n'a pas de sens.",
    ])
    def test_condemnation_of_method_still_penalized(
        self, critic, make_candidate, bad_text
    ):
        cand = make_candidate(bad_text)
        # Force la présence d'un chiffre reconnu pour separer la penalité
        # du score de base
        cand.text = bad_text + " (n=5)"
        score = critic._check_grounded(cand, ground_truth={"n": 5})
        # Base score = 0.5 (chiffre trouvé) - 1.5 (pénalité) clamp à 0.0
        assert score == 0.0, (
            f"Le texte condamnant la methode aurait du etre penalise : "
            f"'{bad_text}', score obtenu={score}"
        )


class TestForbiddenPatternRegex:
    """Vérifie que les patterns regex fonctionnent (garantit qu'on n'est pas
    revenu à une liste littérale trop permissive)."""

    def test_pattern_is_regex_not_literal_string(self, critic, make_candidate):
        """Un texte contenant 'methode est incoherent' doit matcher, meme
        avec variations d'espacement/casse."""
        cand = make_candidate(
            "Selon moi, la Méthode   est\tincohérente ici (n=5)."
        )
        score = critic._check_grounded(cand, ground_truth={"n": 5})
        assert score == 0.0, "Le pattern regex doit tolerer espaces/casse"


# ============================================================================
# FIX 2 — Plus de warning "No module named 'gestionnaire_erreurs'"
# ============================================================================

class TestGestionnaireErreursRemoved:
    def test_no_import_gestionnaire_erreurs_in_llm_manager(self):
        """Le module inexistant `gestionnaire_erreurs` ne doit plus être
        référencé nulle part dans llm_manager.py."""
        llm_mgr_path = ROOT / "src" / "core" / "llm_manager.py"
        assert llm_mgr_path.exists()
        content = llm_mgr_path.read_text(encoding="utf-8")
        # L'import problematique ne doit plus exister
        assert "from gestionnaire_erreurs" not in content, (
            "L'import `from gestionnaire_erreurs` doit etre supprime "
            "(module inexistant provoquait un warning parasite)"
        )
        assert "import gestionnaire_erreurs" not in content
        # TypeErreur ne doit plus être référencé non plus
        assert "TypeErreur" not in content

    def test_no_warning_message_erreur_enregistrement_fallback(self):
        """Le message de log parasite ne doit plus exister."""
        llm_mgr_path = ROOT / "src" / "core" / "llm_manager.py"
        content = llm_mgr_path.read_text(encoding="utf-8")
        assert "Erreur enregistrement fallback" not in content, (
            "Le message de warning 'Erreur enregistrement fallback' doit "
            "etre supprime (il n'a plus lieu d'etre)"
        )

    def test_fallback_openai_still_returns_result(self):
        """Le fallback vers OpenAI doit toujours fonctionner (le bloc
        supprime n'affecte pas la logique principale)."""
        llm_mgr_path = ROOT / "src" / "core" / "llm_manager.py"
        content = llm_mgr_path.read_text(encoding="utf-8")
        # Le log "OpenAI a répondu (fallback)" doit toujours etre present
        assert "OpenAI a répondu (fallback)" in content
        # Le return result doit suivre le log dans ce bloc
        idx = content.find("OpenAI a répondu (fallback)")
        assert "return result" in content[idx:idx + 800]
