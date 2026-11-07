# -*- coding: utf-8 -*-
"""
test_pythonLLM_computationnel.py — suite de tests du pipeline computationnaliste.

Couvre : normalisation, reconnaissance (appartenance ensembliste), scoring
exact (Fraction), classification d'intention (règles ordonnées), validation
grammaticale et déontique, traçage SHA-256 chaîné, refus formel et émission.

Conventions du dépôt : fonctions ``test_*`` simples, exécutables par
``python -m pytest test_pythonLLM_computationnel.py``.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from pythonLLM.moteur.normalisation import normaliser
from pythonLLM.moteur.reconnaissance import reconnaitre
from pythonLLM.moteur.scoring import calculer_scores
from pythonLLM.moteur.intention import classer_intention
from pythonLLM.moteur.construction import construire_commande
from pythonLLM.moteur.validation import valider_commande
from pythonLLM.moteur.trace import Tracer, GENESE
from pythonLLM.moteur.emission import ligne_powershell, ligne_sh, rapport_markdown
from pythonLLM.moteur.pipeline import executer_pipeline
from pythonLLM.moteur.banque import Banque
from pythonLLM.modele.entites import ResultatReconnaissance, CommandeCline


@pytest.fixture(scope="module")
def banque() -> Banque:
    return Banque()


# =============================================================================
# Normalisation
# =============================================================================
def test_normalisation_retire_accents():
    assert normaliser("Graphe Àrbre") == ("graphe", "arbre")


def test_normalisation_minuscule_et_tokens():
    assert normaliser("L'Arbre de Cayley !") == ("l", "arbre", "de", "cayley")


def test_normalisation_vide():
    assert normaliser("") == ()
    assert normaliser("   ") == ()


def test_normalisation_deterministe():
    a = normaliser("Vérification de la preuve")
    b = normaliser("Verification de la preuve")
    assert a == b  # accents ignores -> meme tuple


# =============================================================================
# Reconnaissance (appartenance ensembliste exacte)
# =============================================================================
def test_reconnaissance_graphe(banque):
    notions, res = reconnaitre("analyse ce graphe de dependances", banque)
    lemmes = set(res.termes_reconnus)
    assert "graphe" in lemmes
    assert not res.aucun_terme


def test_reconnaissance_hors_corpus(banque):
    _, res = reconnaitre("bonjour comment allez vous", banque)
    assert res.aucun_terme
    assert res.termes_reconnus == ()


def test_reconnaissance_ordre_deterministe(banque):
    _, r1 = reconnaitre("graphe arbre preuve", banque)
    _, r2 = reconnaitre("preuve arbre graphe", banque)
    # L'ordre des termes reconnus suit le corpus, pas l'ordre de saisie.
    assert r1.termes_reconnus == r2.termes_reconnus

# =============================================================================
# Scoring exact (Fraction, zero arrondi)
# =============================================================================
def test_scoring_est_fraction(banque):
    notions, res = reconnaitre("graphe arbre", banque)
    res = calculer_scores(notions, banque, res)
    for _, score in res.scores:
        assert isinstance(score, Fraction)


def test_scoring_somme_bornee(banque):
    notions, res = reconnaitre("graphe arbre preuve modulo entier", banque)
    res = calculer_scores(notions, banque, res)
    for _, score in res.scores:
        assert Fraction(0) <= score <= Fraction(1)


def test_scoring_champ_absent_zero(banque):
    notions, res = reconnaitre("graphe", banque)
    res = calculer_scores(notions, banque, res)
    assert res.score_champ("STATISTIQUES") == Fraction(0)
    assert res.score_champ("GEOMETRIE") > Fraction(0)


# =============================================================================
# Classification d'intention (regles ordonnees, ordre total)
# =============================================================================
def test_intention_structure_graphe(banque):
    notions, res = reconnaitre("graphe arbre foret", banque)
    res = calculer_scores(notions, banque, res)
    lemmes = {"graphe", "arbre", "foret"}
    assert classer_intention(res, banque, lemmes) == "structure_graphe"


def test_intention_preuve_formelle(banque):
    notions, res = reconnaitre("preuve demonstration lean", banque)
    res = calculer_scores(notions, banque, res)
    lemmes = {"preuve", "demonstration", "lean"}
    assert classer_intention(res, banque, lemmes) == "preuve_formelle"


def test_intention_priorite_graphe_sur_preuve(banque):
    # 'graphe' (priorite 1) gagne meme si 'preuve' (priorite 2) est present.
    notions, res = reconnaitre("graphe preuve", banque)
    res = calculer_scores(notions, banque, res)
    lemmes = {"graphe", "preuve"}
    assert classer_intention(res, banque, lemmes) == "structure_graphe"


def test_intention_aucune_si_vide(banque):
    res = ResultatReconnaissance(aucun_terme=True)
    assert classer_intention(res, banque, set()) is None


# =============================================================================
# Construction et validation
# =============================================================================
def test_construction_gabarit_valide(banque):
    notions, res = reconnaitre("graphe", banque)
    res = calculer_scores(notions, banque, res)
    cmd = construire_commande("structure_graphe", "graphe", res, banque)
    assert cmd is not None
    assert cmd.argv()[0] == "cline"
    assert valider_commande(cmd, banque) == ()


def test_construction_intention_inconnue_refus(banque):
    notions, res = reconnaitre("graphe", banque)
    res = calculer_scores(notions, banque, res)
    cmd = construire_commande("intention_qui_nexiste_pas", "graphe", res, banque)
    assert cmd is None  # pas d'invention de gabarit


def test_validation_detecte_option_inconnue(banque):
    cmd = CommandeCline(options=(("--option-fantome", None),))
    violations = valider_commande(cmd, banque)
    assert any("OPTION-INCONNUE" in v for v in violations)


def test_validation_detecte_exclusion(banque):
    cmd = CommandeCline(options=(("--tui", None), ("--json", None)))
    violations = valider_commande(cmd, banque)
    assert any("EXCLUSION" in v for v in violations)


def test_validation_detecte_valeur_enum_invalide(banque):
    cmd = CommandeCline(options=(("--thinking", "bambou"),))
    violations = valider_commande(cmd, banque)
    assert any("ENUM" in v for v in violations)


# =============================================================================
# Tracage SHA-256 chaine
# =============================================================================
def test_trace_genese_et_chainage():
    t = Tracer()
    e1 = t.ajouter("etape1", "a")
    assert e1.empreinte_precedente == GENESE
    e2 = t.ajouter("etape2", "b")
    assert e2.empreinte_precedente == e1.empreinte  # chainage
    assert e1.empreinte != e2.empreinte


def test_trace_inalterable():
    t1 = Tracer(); t1.ajouter("x", "donnee")
    t2 = Tracer(); t2.ajouter("x", "donnee_modifiee")
    assert t1.etapes()[0].empreinte != t2.etapes()[0].empreinte


def test_trace_deterministe():
    t1 = Tracer(); t1.ajouter("x", "stable")
    t2 = Tracer(); t2.ajouter("x", "stable")
    assert t1.empreinte_finale == t2.empreinte_finale


# =============================================================================
# Emission
# =============================================================================
def test_emission_quote_powershell():
    assert ligne_powershell(("cline", "l'arbre")) == "'cline' 'l''arbre'"


def test_emission_quote_sh():
    assert ligne_sh(("cline", "l'arbre")) == "'cline' 'l'\\''arbre'"


# =============================================================================
# Pipeline de bout en bout
# =============================================================================
def test_pipeline_graphe_genere_commande(banque):
    r = executer_pipeline("analyse ce graphe et sa connexite", banque=banque)
    assert not r.est_refus
    assert r.intention == "structure_graphe"
    assert r.argv[0] == "cline"
    assert valider_commande(r.commande, banque) == ()


def test_pipeline_refus_hors_corpus(banque):
    r = executer_pipeline("bonjour comment allez vous", banque=banque)
    assert r.est_refus
    assert r.refus.etape == "reconnaissance"
    assert r.argv == ()


def test_pipeline_calcul_exact(banque):
    r = executer_pipeline("calcule en arithmetique modulaire", banque=banque)
    assert not r.est_refus
    assert r.intention == "calcul_exact"


def test_pipeline_trace_presente(banque):
    r = executer_pipeline("verifie la preuve lean", banque=banque)
    assert len(r.trace) >= 5
    for i in range(1, len(r.trace)):
        assert r.trace[i].empreinte_precedente == r.trace[i - 1].empreinte


def test_pipeline_deterministe(banque):
    r1 = executer_pipeline("analyse ce graphe", banque=banque)
    r2 = executer_pipeline("analyse ce graphe", banque=banque)
    assert r1.argv == r2.argv
    assert r1.trace[-1].empreinte == r2.trace[-1].empreinte


def test_pipeline_rapport_markdown(banque):
    r = executer_pipeline("analyse ce graphe", banque=banque)
    md = rapport_markdown(r)
    assert "Rapport de derivation" in md
    assert "structure_graphe" in md

