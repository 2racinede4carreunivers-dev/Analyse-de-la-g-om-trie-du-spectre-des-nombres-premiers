"""Tests pour memory/dictionnaire_spectral.py et memory/adaptateur_cognitif_rag.py."""
from __future__ import annotations

from fractions import Fraction

import pytest

from memory import (
    DICTIONNAIRE_SPECTRAL,
    Regime,
    AdaptateurCognitifSpectral,
    get_regime,
    list_regimes,
    preparer_requete_avec_rag,
)
from memory.dictionnaire_spectral import regime_count, total_lemmes


# ==========================================================================
# Dictionnaire spectral
# ==========================================================================
def test_dictionnaire_contient_13_regimes():
    """Dictionnaire : 10 regimes historiques + XI/XII + Pont Savard (XIII)."""
    assert regime_count() == 13
    expected = {
        # 10 regimes historiques
        "regime_1_2_positif", "regime_mixte", "regime_1_4", "regime_1_3",
        "regime_negatif", "ecarts_spectraux", "invariants_transition",
        "geometrie_critique", "blocs_asymetriques", "suites_finies",
        # 2 regimes ajoutes 2026-02-17 (Section XI/XII)
        "regime_construction_termes", "regime_parametrique_1_k",
        # Regime ajoute 2026-06 (Section XIII, Pont Savard v3.33)
        "regime_pont_savard",
    }
    assert set(list_regimes()) == expected


def test_get_regime_invalid_raises():
    with pytest.raises(ValueError):
        get_regime("regime_inexistant")


def test_each_regime_has_required_fields():
    """Chaque regime doit avoir au moins concepts_cles, patterns, definitions, lemmes."""
    for nom, regime in DICTIONNAIRE_SPECTRAL.items():
        assert isinstance(regime, Regime)
        assert regime.nom == nom
        assert regime.titre, f"{nom} : titre manquant"
        assert regime.patterns_detection, f"{nom} : patterns manquants"
        assert regime.definitions_hol, f"{nom} : definitions HOL manquantes"
        assert regime.lemmes_certifies, f"{nom} : lemmes manquants"
        assert regime.regles_cognitives, f"{nom} : regles manquantes"


def test_ratios_corrects():
    """Verifier les ratios attendus pour les regimes ayant un ratio."""
    assert get_regime("regime_1_2_positif").ratio_attendu == Fraction(1, 2)
    assert get_regime("regime_1_3").ratio_attendu == Fraction(1, 3)
    assert get_regime("regime_1_4").ratio_attendu == Fraction(1, 4)
    assert get_regime("regime_negatif").ratio_attendu == Fraction(1, 2)
    assert get_regime("regime_mixte").ratio_attendu == Fraction(1, 2)
    # Ces regimes n'ont pas de ratio cible (gaps, invariants, etc.)
    assert get_regime("ecarts_spectraux").ratio_attendu is None
    assert get_regime("invariants_transition").ratio_attendu is None


def test_total_lemmes_minimum():
    """Le dictionnaire doit avoir au moins 20 lemmes au total."""
    assert total_lemmes() >= 20


def test_to_prompt_context_non_empty():
    """Chaque regime doit produire un bloc texte injectable non vide."""
    for nom, regime in DICTIONNAIRE_SPECTRAL.items():
        ctx = regime.to_prompt_context()
        assert ctx
        assert regime.titre.upper() in ctx.upper()


# ==========================================================================
# Adaptateur RAG - detection
# ==========================================================================
@pytest.fixture
def adapt() -> AdaptateurCognitifSpectral:
    return AdaptateurCognitifSpectral()


@pytest.mark.parametrize("requete,expected_regimes", [
    # Regime 1/2 positif
    ("Reconstruis le premier 29 en regime 1/2", ["regime_1_2_positif"]),
    ("Calcule SA et SB pour n=10", ["regime_1_2_positif"]),
    # Regime mixte
    ("Asymptote K6 en suites mixtes", ["regime_mixte"]),
    # Regime 1/4
    ("Verifie le regime 1/4 avec p=947", ["regime_1_4"]),
    # Regime 1/3
    ("Extension cubique 1/3 pour p=227", ["regime_1_3"]),
    # Regime negatif
    ("Utilise powr pour indices negatifs", ["regime_negatif"]),
    # Ecarts spectraux
    ("Calcule le gap entre 11 et 23", ["ecarts_spectraux"]),
    # Invariants transition
    ("SB - 2*SA = -62", ["invariants_transition"]),
    # Geometrie critique
    ("Verifie le plan trifocal FZg HyRi MsP", ["geometrie_critique"]),
    # Blocs asymetriques
    ("Bloc 3x3 asymetrique chaotique", ["blocs_asymetriques"]),
    # Suites finies
    ("Quelle est la valeur de SB(1) ? -59.5 ?", ["suites_finies"]),
])
def test_detection_regimes_simples(adapt, requete, expected_regimes):
    regimes, _ = adapt.detecter_regimes(requete)
    for exp in expected_regimes:
        assert exp in regimes, f"Regime {exp} non detecte dans '{requete}', recu : {regimes}"


def test_detection_multiple_regimes(adapt):
    """Une requete complexe doit detecter plusieurs regimes."""
    requete = "Calcule le gap mixte entre -13 et 47 en regime negatif"
    regimes, _ = adapt.detecter_regimes(requete)
    # Doit detecter au minimum ecarts_spectraux ET regime_negatif
    assert "ecarts_spectraux" in regimes
    assert "regime_negatif" in regimes
    # Et probablement regime_mixte aussi
    assert len(regimes) >= 2


def test_detection_aucun_regime(adapt):
    """Une question hors-sujet ne doit detecter aucun regime."""
    regimes, _ = adapt.detecter_regimes("Quelle heure est-il ?")
    assert regimes == []


def test_matched_keywords_renvoyes(adapt):
    """Les mots-cles trouves doivent etre renvoyes pour chaque regime."""
    requete = "Calcule SA(5) en regime 1/2"
    _, matched = adapt.detecter_regimes(requete)
    assert "regime_1_2_positif" in matched
    assert len(matched["regime_1_2_positif"]) > 0


# ==========================================================================
# Adaptateur RAG - construction prompt
# ==========================================================================
def test_construire_prompt_sans_regime(adapt):
    """Si aucun regime detecte, prompt = requete brute."""
    prompt = adapt.construire_prompt_augmente("Question generique", "")
    assert prompt == "Question generique"


def test_construire_prompt_avec_contexte(adapt):
    """Prompt avec contexte doit contenir regles globales + contexte + requete."""
    contexte = "Contexte test"
    prompt = adapt.construire_prompt_augmente("Ma question", contexte)
    assert "REGLES D'INJECTION OBLIGATOIRES" in prompt
    assert "Contexte test" in prompt
    assert "Ma question" in prompt


def test_analyser_workflow_complet(adapt):
    """Test du workflow complet : detection + contexte + prompt."""
    analyse = adapt.analyser("Calcule le gap entre 11 et 23")
    assert analyse.requete_originale == "Calcule le gap entre 11 et 23"
    assert "ecarts_spectraux" in analyse.regimes_detectes
    assert analyse.nombre_regimes >= 1
    assert "ECARTS SPECTRAUX" in analyse.contexte_brut.upper()
    assert "REGLES D'INJECTION" in analyse.prompt_augmente
    assert "Calcule le gap entre 11 et 23" in analyse.prompt_augmente


def test_regles_globales_toujours_presentes(adapt):
    """Les 6 regles globales doivent etre dans tout prompt augmente."""
    analyse = adapt.analyser("regime 1/2 reconstruction")
    prompt = analyse.prompt_augmente
    for i in range(1, 7):
        assert f"REGLE {i}" in prompt, f"Regle {i} absente du prompt"


# ==========================================================================
# API haut niveau : preparer_requete_avec_rag
# ==========================================================================
def test_preparer_requete_avec_rag_returns_dict():
    """L'API attendue par gabriel_v6_2_rag.py doit retourner un dict avec les bonnes cles."""
    result = preparer_requete_avec_rag("Calcule gap mixte -13 47")
    assert isinstance(result, dict)
    assert "prompt_augmente" in result
    assert "regimes_detectes" in result
    assert "contexte_brut" in result
    assert "matched_keywords" in result
    assert "nombre_regimes" in result


def test_preparer_requete_detecte_correctement():
    """Verifier que la fonction publique detecte bien les regimes."""
    result = preparer_requete_avec_rag("Reconstruction du premier 29 en regime 1/2")
    assert "regime_1_2_positif" in result["regimes_detectes"]
    assert result["nombre_regimes"] >= 1


def test_preparer_requete_vide_pas_de_crash():
    """Requete vide ne doit pas crasher."""
    result = preparer_requete_avec_rag("")
    assert result["regimes_detectes"] == []
    assert result["nombre_regimes"] == 0


# ==========================================================================
# Integration : gabriel_v6_2_rag.py peut maintenant importer
# ==========================================================================
def test_gabriel_v6_2_rag_can_import():
    """Le module gabriel_v6_2_rag doit pouvoir importer memory.* sans erreur."""
    # On teste juste les imports critiques sans construire l'objet
    # (qui necessiterait une cle API Claude)
    from memory.adaptateur_cognitif_rag import preparer_requete_avec_rag as _prep
    from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral as _Adapt
    assert callable(_prep)
    assert _Adapt is not None
