"""Tests pour src/visualization/auto_trigger.py.

Verifie la detection deterministe d'intention de visualisation depuis
des questions francaises naturelles (avec et sans accents).
"""
from __future__ import annotations

import pytest

from src.visualization import (
    CurveKind,
    VisualizationIntent,
    detect_visualization_intent,
)


# --------------------------------------------------------------------------
# Cas positifs : la detection doit retourner un Intent
# --------------------------------------------------------------------------
@pytest.mark.parametrize("question,expected_kind", [
    # SA
    ("Trace la courbe de SA(n) pour n=1..50", CurveKind.SA),
    ("Peux-tu illustrer l'evolution de SA sur 1..30 ?", CurveKind.SA),
    ("Dessine la suite alternee A", CurveKind.SA),
    # SB
    ("Affiche la courbe de SB(n) entre 1 et 100", CurveKind.SB),
    ("Comment se comporte SB sur 1..50 ?", CurveKind.SB),
    # SA_SB superpose
    ("Trace les deux suites SA et SB sur 1..40", CurveKind.SA_SB),
    ("Visualise SA et SB ensemble", CurveKind.SA_SB),
    # Ratio SA/SB
    ("Montre la convergence du ratio SA/SB", CurveKind.RATIO_SA_SB),
    ("Trace le rapport spectral asymptotique sur 1..100", CurveKind.RATIO_SA_SB),
    ("Illustre la convergence vers 1/2", CurveKind.RATIO_SA_SB),
    # Digamma
    ("Trace l'evolution de digamma pour n=1..50", CurveKind.DIGAMMA),
    ("Comment evolue la fonction psi sur 1..30 ?", CurveKind.DIGAMMA),
    # Invariant
    ("Trace l'invariant D(n,P) sur 1..50", CurveKind.INVARIANT),
    ("Dessine l'evolution de l'invariant entre 1 et 100", CurveKind.INVARIANT),
    # Gap
    ("Trace les ecarts entre primes consecutifs sur 1..200", CurveKind.GAP),
    ("Visualise les gaps de 1 a 100", CurveKind.GAP),
    # Prime
    ("Trace la croissance des premiers de 1 a 100", CurveKind.PRIME),
    ("Dessine p(n) sur les 50 premiers nombres premiers", CurveKind.PRIME),
])
def test_detect_positive(question: str, expected_kind: CurveKind):
    intent = detect_visualization_intent(question)
    assert intent is not None, f"Pas de detection pour : {question}"
    assert intent.kind == expected_kind, f"Mauvais kind pour : {question}"
    assert 1 <= intent.n_min < intent.n_max <= 1000


# --------------------------------------------------------------------------
# Cas negatifs : la detection doit retourner None
# --------------------------------------------------------------------------
@pytest.mark.parametrize("question", [
    "",
    "   ",
    "Bonjour Gabriel",
    "Quel est le 26eme nombre premier ?",
    "Reconstruis le 42eme nombre premier",
    "Calcule l'ecart spectral entre 26 et 56",  # 'ecart' SANS mot-cle viz
    "Aide",
    "Affiche la version",  # 'affiche' present mais pas de type math
    # 'affiche' EST un mot viz et 'version' n'est pas un type math, donc bon cas negatif
])
def test_detect_negative(question: str):
    intent = detect_visualization_intent(question)
    assert intent is None, f"Detection inattendue pour : '{question}'"


# --------------------------------------------------------------------------
# Detection d'intervalles
# --------------------------------------------------------------------------
@pytest.mark.parametrize("question,expected_range", [
    ("Trace SA n=1..50", (1, 50)),
    ("Trace SA de 1 a 100", (1, 100)),
    ("Trace SA entre 5 et 25", (5, 25)),
    ("Trace SA sur [1,200]", (1, 200)),
    ("Trace SA sur 10..40", (10, 40)),
    ("Trace la courbe de SA pour les 100 premiers", (1, 100)),
    # Accents
    ("Trace SA de 1 à 50", (1, 50)),
    # Forme frequente en NL : n=1 a n=100
    ("Trace le rapport spectral asymetrique chaotique pour n=1 a n=100", (1, 100)),
    ("Trace le digamma pour n=1 à n=100", (1, 100)),
    # Inversion auto
    ("Trace SA de 50 a 10", (10, 50)),
    # Bornage automatique
    ("Trace SA de 1 a 99999", (1, 1000)),
])
def test_range_extraction(question: str, expected_range: tuple[int, int]):
    intent = detect_visualization_intent(question)
    assert intent is not None
    assert (intent.n_min, intent.n_max) == expected_range


def test_default_range_when_unspecified():
    """Si pas d'intervalle dans la question, on doit utiliser 1..50 par defaut."""
    intent = detect_visualization_intent("Trace la courbe de SA")
    assert intent is not None
    assert intent.n_min == 1
    assert intent.n_max == 50


# --------------------------------------------------------------------------
# Detection PNG
# --------------------------------------------------------------------------
@pytest.mark.parametrize("question,want_png", [
    ("Trace SA sur 1..50", False),
    ("Trace SA sur 1..50 et exporte en PNG", True),
    ("Genere une image de la convergence SA/SB pour mon article scientifique", True),
    ("Trace SA sur 1..50 et sauvegarde le fichier", True),
    ("Trace SA pour un rapport citable", True),
])
def test_png_intent_detection(question: str, want_png: bool):
    intent = detect_visualization_intent(question)
    assert intent is not None
    assert intent.want_png == want_png


# --------------------------------------------------------------------------
# Robustesse : accents, casse, ponctuation
# --------------------------------------------------------------------------
def test_accents_handled():
    a = detect_visualization_intent("Trace l'évolution de SA")
    b = detect_visualization_intent("Trace l'evolution de SA")
    assert a is not None and b is not None
    assert a.kind == b.kind == CurveKind.SA


def test_case_insensitive():
    a = detect_visualization_intent("TRACE LA COURBE DE DIGAMMA")
    b = detect_visualization_intent("trace la courbe de digamma")
    assert a is not None and b is not None
    assert a.kind == b.kind == CurveKind.DIGAMMA


# --------------------------------------------------------------------------
# Champ reasoning et metadata
# --------------------------------------------------------------------------
def test_intent_has_reasoning():
    intent = detect_visualization_intent("Trace la convergence du ratio SA/SB sur 1..100")
    assert intent is not None
    assert intent.reasoning
    assert "ratio" in intent.reasoning.lower() or "rapport" in intent.reasoning.lower()
    assert intent.matched_keywords
    assert intent.confidence > 0.0


# --------------------------------------------------------------------------
# Regressions : ne pas regenerer un graphique quand on demande une explication
# --------------------------------------------------------------------------
@pytest.mark.parametrize("question", [
    "Peux-tu expliquer plus en detail le dernier graphique ?",
    "Peux-tu identifier les axes de ce graphique et expliquer pourquoi ?",
    "Analyse ce graphe et explique la legende",
])
def test_explanation_followup_does_not_trigger_visualization(question: str):
    intent = detect_visualization_intent(question)
    assert intent is None, "Une demande d'explication ne doit pas relancer un auto-graphique"


def test_user_exact_three_prompt_sequence_regression():
    """Reproduit les 3 prompts exacts rapportes par l'utilisateur."""
    q1 = "Détermine le rapport spectral asymétrique chaotique sous forme d'un graphique pour n=1 a n=100?"
    q2 = "Détermine un graphique du digamma pour n=1 à n=100"
    q3 = "Peux-tu expliquer le dernier graphique, identifier les axes et pourquoi la valeur converge?"

    i1 = detect_visualization_intent(q1)
    assert i1 is not None
    assert i1.kind == CurveKind.RATIO_SA_SB
    assert i1.rsp_config == "chaos-savard"
    assert (i1.n_min, i1.n_max) == (1, 100)

    i2 = detect_visualization_intent(q2)
    assert i2 is not None
    assert i2.kind == CurveKind.DIGAMMA
    assert (i2.n_min, i2.n_max) == (1, 100)

    i3 = detect_visualization_intent(q3)
    assert i3 is None
