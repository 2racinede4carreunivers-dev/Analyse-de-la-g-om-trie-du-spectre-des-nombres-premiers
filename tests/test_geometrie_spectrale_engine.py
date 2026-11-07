"""Tests pour le GeometrieSpectraleEngine et les 3 modeles spectraux.

Couverture :
  - 3 modeles : 1/2, 1/3, 1/4
  - 8 questions : Q1.a (1x1), Q1.b (n×n sym), Q1.c (chaos), Q1.d (ord),
                  Q2 (reconstruction), Q3.a (+,+), Q3.b (-,-), Q3.c (-,+)
  - Total : ~30 tests
"""
from __future__ import annotations

from fractions import Fraction

import pytest

from src.core.spectral_core import SpectralMethodCore
from src.engines.geometrie_spectrale_engine import (
    GeometrieSpectraleEngine,
    ComparativeReport,
)
from src.spectral.spectral_models import (
    Model_1_2,
    Model_1_3,
    Model_1_4,
    get_model,
    list_models,
    all_models,
    RatioResult,
    ReconstructionResult,
    GapResult,
)


@pytest.fixture(scope="module")
def core() -> SpectralMethodCore:
    return SpectralMethodCore()


@pytest.fixture(scope="module")
def engine(core: SpectralMethodCore) -> GeometrieSpectraleEngine:
    return GeometrieSpectraleEngine(core)


# ==========================================================================
# Tests : disponibilite des 3 modeles
# ==========================================================================
def test_three_models_registered():
    assert set(list_models()) == {"1/2", "1/3", "1/4"}
    assert len(all_models()) == 3


def test_get_model_invalid():
    with pytest.raises(ValueError):
        get_model("1/5")


def test_model_attributes():
    """Chaque modele a les bons facteurs."""
    m1 = get_model("1/2")
    assert m1.n_factor == 2 and m1.reconstruction_factor == 64
    assert m1.ratio == Fraction(1, 2)

    m2 = get_model("1/3")
    assert m2.n_factor == 3 and m2.reconstruction_factor == 729
    assert m2.ratio == Fraction(1, 3)

    m3 = get_model("1/4")
    assert m3.n_factor == 4 and m3.reconstruction_factor == 4096
    assert m3.ratio == Fraction(1, 4)


# ==========================================================================
# Q1.a : RsP 1x1 - EXACT pour les 3 modeles
# ==========================================================================
@pytest.mark.parametrize("model_name,expected", [
    ("1/2", Fraction(1, 2)),
    ("1/3", Fraction(1, 3)),
    ("1/4", Fraction(1, 4)),
])
def test_q1a_rsp_1x1_exact_for_each_model(model_name, expected):
    m = get_model(model_name)
    r = m.RsP_1x1(3, 5)
    assert r.ratio == expected
    assert r.is_exact is True
    assert r.case == "1x1"


def test_q1a_rsp_1x1_invalid_same_n(engine):
    with pytest.raises(ValueError):
        engine.compute_rsp_1x1("1/2", 5, 5)


def test_q1a_all_models_returns_3_results(engine):
    report = engine.compute_rsp_1x1_all_models(3, 5)
    assert isinstance(report, ComparativeReport)
    assert report.question == "Q1.a"
    assert len(report.results_by_model) == 3
    for name, res in report.results_by_model.items():
        assert isinstance(res, RatioResult)
        assert res.is_exact is True


# ==========================================================================
# Q1.b : RsP n×n symetrique - EXACT pour les 3 modeles
# ==========================================================================
@pytest.mark.parametrize("model_name,expected", [
    ("1/2", Fraction(1, 2)),
    ("1/3", Fraction(1, 3)),
    ("1/4", Fraction(1, 4)),
])
def test_q1b_rsp_nxn_symetrique_exact(model_name, expected):
    """|A|==|B| -> ratio EXACT."""
    m = get_model(model_name)
    r = m.RsP_nxn([2, 3, 4], [5, 6, 7], case="nxn_symetrique")
    assert r.ratio == expected
    assert r.is_exact is True


def test_q1b_validation_empty():
    """A_positions ou B_positions vides -> erreur."""
    m = get_model("1/2")
    with pytest.raises(ValueError):
        m.RsP_nxn([], [1, 2])
    with pytest.raises(ValueError):
        m.RsP_nxn([1], [])


def test_q1b_validation_same_positions():
    m = get_model("1/2")
    with pytest.raises(ValueError):
        m.RsP_nxn([1, 2, 3], [1, 2, 3])


# ==========================================================================
# Q1.c : RsP asymetrique chaotique - convergence (pas exact mais proche)
# ==========================================================================
@pytest.mark.parametrize("model_name", ["1/2", "1/3", "1/4"])
def test_q1c_rsp_chaotique_convergence(model_name):
    """|A|!=|B| -> ratio proche mais pas exact."""
    m = get_model(model_name)
    r = m.RsP_nxn([2, 9, 11], [7, 5, 10, 15], case="asym_chaotique")
    # Convergence : delta tres petit
    assert r.is_close is True, f"Delta {r.convergence_delta_float} trop grand pour {model_name}"


# ==========================================================================
# Q1.d : RsP asymetrique ordonnee
# ==========================================================================
@pytest.mark.parametrize("model_name,expected", [
    ("1/2", Fraction(1, 2)),
    ("1/3", Fraction(1, 3)),
    ("1/4", Fraction(1, 4)),
])
def test_q1d_rsp_ordonnee_symmetrical_sizes(model_name, expected):
    """Si |A|==|B| meme avec ordre different -> ratio EXACT."""
    m = get_model(model_name)
    r = m.RsP_nxn([2, 4, 6], [3, 5, 7], case="asym_ordonnee")
    assert r.ratio == expected
    assert r.is_exact is True


# ==========================================================================
# Q2 : Reconstruction du N-ieme nombre premier
# ==========================================================================
@pytest.mark.parametrize("model_name", ["1/2", "1/3", "1/4"])
@pytest.mark.parametrize("n,actual", [
    (1, 2), (5, 11), (10, 29), (26, 101), (100, 541),
])
def test_q2_reconstruction_exact(model_name, n, actual):
    """Les 3 modeles doivent tous reconstruire le bon nombre premier."""
    m = get_model(model_name)
    r = m.reconstruct_nth_prime(n, actual)
    assert r.is_exact is True, (
        f"Modele {model_name} n={n} : reconstructed={r.reconstructed_prime} "
        f"!= actual={actual}"
    )


def test_q2_via_engine_uses_table(engine, core):
    """Engine reconstruction utilise la table de primes du core."""
    report = engine.reconstruct_all_models(26)  # 26e prime = 101
    assert report.question == "Q2"
    assert len(report.results_by_model) == 3
    for name, res in report.results_by_model.items():
        assert isinstance(res, ReconstructionResult)
        assert res.actual_prime == 101
        assert res.is_exact is True


def test_q2_invalid_n_without_actual(engine):
    """Si on demande n hors table sans actual_prime, erreur."""
    with pytest.raises(ValueError):
        engine.reconstruct_all_models(99999)


# ==========================================================================
# Q3 : Gap (3 cas)
# ==========================================================================
@pytest.mark.parametrize("model_name", ["1/2", "1/3", "1/4"])
@pytest.mark.parametrize("p1,p2,expected,case", [
    # (+,+)
    (11, 23, 11, "++"),
    (2, 3, 0, "++"),  # entre 2 et 3 il n'y a aucun entier
    (5, 11, 5, "++"),
    # (-,-)
    (-19, -5, 13, "--"),
    (-41, -5, 35, "--"),
    (-3, -47, 43, "--"),
    # (-,+)
    (-7, 11, 17, "-+"),
    (-2, 5, 6, "-+"),
])
def test_q3_gap_all_cases(model_name, p1, p2, expected, case):
    m = get_model(model_name)
    r = m.gap(p1, p2)
    assert r.case == case, f"Mauvais cas detecte pour ({p1}, {p2})"
    assert r.gap_count == expected


def test_q3_gap_same_number(engine):
    r = engine.compute_gap("1/2", 7, 7)
    assert r.gap_count == 0


def test_q3_gap_via_engine_all_models(engine):
    """Gap independant du modele : les 3 doivent retourner la meme valeur."""
    report = engine.compute_gap_all_models(11, 23)
    assert report.question == "Q3.a"
    values = {res.gap_count for res in report.results_by_model.values()}
    assert len(values) == 1, "Gap doit etre identique entre modeles"
    assert values.pop() == 11


# ==========================================================================
# answer_all_questions : couverture complete des 8 questions
# ==========================================================================
def test_answer_all_questions_returns_8_reports(engine):
    """L'API unifiee doit retourner exactement 8 rapports."""
    reports = engine.answer_all_questions()
    assert len(reports) == 8
    question_ids = {r.question for r in reports}
    assert question_ids == {"Q1.a", "Q1.b", "Q1.c", "Q1.d", "Q2", "Q3.a", "Q3.b", "Q3.c"}


def test_answer_all_questions_to_text(engine):
    """Tous les rapports doivent generer un rendu textuel non vide."""
    reports = engine.answer_all_questions()
    for r in reports:
        txt = r.to_text()
        assert txt
        assert "Modele 1/2" in txt
        assert "Modele 1/3" in txt
        assert "Modele 1/4" in txt


# ==========================================================================
# Verification cross-modeles : meme reconstruction independamment du modele
# ==========================================================================
@pytest.mark.parametrize("n,actual", [(1, 2), (5, 11), (26, 101), (50, 229)])
def test_three_models_reconstruct_same_prime(n, actual):
    """Les 3 modeles doivent retourner exactement le meme premier."""
    results = []
    for name in list_models():
        m = get_model(name)
        r = m.reconstruct_nth_prime(n, actual)
        assert r.is_exact
        results.append(r.reconstructed_prime)
    assert all(int(r) == actual for r in results)


# ==========================================================================
# Verification metaformula : ratio cible exact des 3 modeles
# ==========================================================================
def test_metaformula_ratio_targets():
    """Pour chaque modele, ratio attendu = 1/n_factor."""
    assert get_model("1/2").ratio == Fraction(1, 2)
    assert get_model("1/3").ratio == Fraction(1, 3)
    assert get_model("1/4").ratio == Fraction(1, 4)


# ==========================================================================
# Test d'integration : engine sans spectral_core
# ==========================================================================
def test_engine_without_spectral_core():
    """Engine doit fonctionner sans spectral_core si actual_prime fourni."""
    e = GeometrieSpectraleEngine(spectral_core=None)
    # Reconstruction avec actual_prime
    r = e.reconstruct_all_models(26, actual_prime=101)
    assert len(r.results_by_model) == 3
    # RsP et gap ne dependent pas du core
    rsp = e.compute_rsp_1x1_all_models(3, 5)
    assert len(rsp.results_by_model) == 3
    gap = e.compute_gap_all_models(11, 23)
    assert len(gap.results_by_model) == 3

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
