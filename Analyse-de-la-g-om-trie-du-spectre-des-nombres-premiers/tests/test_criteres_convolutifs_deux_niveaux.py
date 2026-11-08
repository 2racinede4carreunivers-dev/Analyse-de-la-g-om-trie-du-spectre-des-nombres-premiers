"""Tests du contrat cognitif à deux niveaux (rapports typique 1/2 et non typiques 1/k).

Ces tests garantissent que les points obligatoires sont présents par défaut à
chaque requête :
  1. niveau 1 (entier) : quatre possibilités Digamma (positions n-3 / n-2, ±) ;
  2. si le niveau 1 ne retourne aucun premier : la démarche de niveau 1 qui
     n'aboutit pas, puis la démarche de niveau 2 (géométrique) ;
  3. si aucun niveau ne retourne d'ancrage : l'énoncé explicite d'absence
     d'ancrage pour un premier pour le rapport 1/k considéré.
"""
from __future__ import annotations

import math

from src.core.pipeline import Pipeline
from src.core.spectral_core import SpectralMethodCore
from src.spectral.rapports_non_typiques import (
    criteres_obligatoires,
    niveau_1_entier,
    niveau_2_geometrique,
    quatre_possibilites_digamma,
)


# ── NIVEAU 1 : quatre possibilités Digamma ────────────────────────────────────

def test_quatre_possibilites_digamma_positions_et_signes() -> None:
    possibilites = quatre_possibilites_digamma("1/5", 10)

    assert len(possibilites) == 4
    assert {p["position"] for p in possibilites} == {7, 8}
    assert {p["signe"] for p in possibilites} == {1, -1}


def test_niveau_1_retourne_un_ancrage_pour_1_5() -> None:
    niveau1 = niveau_1_entier("1/5", 10)

    premiers = [p for p in niveau1["possibilites"] if p["premier"]]
    assert niveau1["ancrage_retourne"] is True
    assert [p["C"] for p in premiers] == [2999]
    assert "A(7)+" in niveau1["branches_retenues"]


def test_niveau_1_sans_premier_pour_1_81() -> None:
    niveau1 = niveau_1_entier("1/81", 10)

    assert niveau1["ancrage_retourne"] is False
    assert all(p["verdict"] == "COMPOSE" for p in niveau1["possibilites"])
    assert "AUCUN ancrage" in niveau1["demarche"]


# ── NIVEAU 2 : même démarche, termes géométriques ─────────────────────────────

def test_niveau_2_est_determine_quand_le_niveau_1_echoue() -> None:
    niveau2 = niveau_2_geometrique("1/81", 10)

    assert niveau2["niveau"] == 2
    assert math.isclose(niveau2["facteur_g"], math.sqrt(1 + 81 * 81) / 81)
    # Les huit branches réelles universelles sont évaluées.
    assert len(niveau2["branches_reelles"]) == 8
    assert "géométriques" in niveau2["demarche"]


def test_niveau_2_facteur_commun_et_terme_geometrique() -> None:
    niveau2 = niveau_2_geometrique("1/5", 10)

    for p in niveau2["possibilites"]:
        assert p["niveau"] == 2
        assert "sqrt(1+k^2)/k" in p["note"]


# ── POINTS OBLIGATOIRES ───────────────────────────────────────────────────────

def test_criteres_obligatoires_ancrage_niveau_1() -> None:
    criteres = criteres_obligatoires("1/5", 10)

    assert criteres["ancrage_niveau_1"] is True
    assert criteres["ancrage_retourne"] is True
    assert criteres["aucun_ancrage"] is False
    assert "NIVEAU 1" in criteres["point_1_niveau_1"]
    assert "niveau 1" in criteres["point_2_niveau_2"].lower()


def test_criteres_obligatoires_enonce_absence_ancrage() -> None:
    criteres = criteres_obligatoires("1/81", 10)

    assert criteres["ancrage_niveau_1"] is False
    assert criteres["ancrage_niveau_2"] is False
    assert criteres["aucun_ancrage"] is True
    assert "NE retourne AUCUN ancrage" in criteres["point_1_niveau_1"]
    assert "démarche géométrique est déterminée" in criteres["point_2_niveau_2"]
    assert "ne retourne aucun ancrage pour un premier" in criteres["point_3_verdict"]


def test_criteres_obligatoires_trois_points_toujours_presents() -> None:
    for rapport in ("1/5", "1/81", "1/23"):
        criteres = criteres_obligatoires(rapport, 10)
        assert criteres["point_1_niveau_1"]
        assert criteres["point_2_niveau_2"]
        assert criteres["point_3_verdict"]
        assert criteres["reponse_obligatoire"].count("POINT") >= 3


# ── RAPPORT TYPIQUE 1/2 ───────────────────────────────────────────────────────

def test_rapport_typique_1_2_expose_les_memes_criteres() -> None:
    rapport = SpectralMethodCore().rapport_convolutif_typique(10)

    assert rapport["niveau_1"] is not None
    assert len(rapport["niveau_1"]["possibilites"]) == 4
    assert rapport["ancrage_niveau_1"] is True
    assert 29 in [p["C"] for p in rapport["niveau_1"]["possibilites"] if p["premier"]]


def test_rapport_typique_1_2_niveau_2_par_rang() -> None:
    rapport = SpectralMethodCore().rapport_convolutif_typique(27)

    assert rapport["niveau_1"]["ancrage_retourne"] is False
    assert rapport["niveau_2"]["ancrage_retourne"] is True
    rang = rapport["niveau_2"]["reconstruction_par_rang"]
    assert rang["verifie"] is True
    assert rang["premier_cible"] == 103
    assert rapport["cible"]["premier"] == 103


# ── INTÉGRATION PIPELINE ──────────────────────────────────────────────────────

def test_resume_pipeline_contient_les_criteres_obligatoires() -> None:
    facts = SpectralMethodCore().rapport_convolutif_non_typique("1/81", 10)
    facts["model"] = "1/81"
    facts["equation_holds"] = False

    resume = Pipeline._append_convolution_summary("Réponse.", facts)

    assert "### Critères convolutifs obligatoires (niveaux 1 et 2)" in resume
    assert "Niveau 1 — entier" in resume
    assert "Niveau 2 — géométrique" in resume
    assert "A(7)+" in resume and "A(8)-" in resume
    assert "ne retourne aucun ancrage pour un premier" in resume


def test_prompt_contient_les_criteres_obligatoires() -> None:
    facts = SpectralMethodCore().rapport_convolutif_non_typique("1/81", 10)
    facts["model"] = "1/81"

    class Ctx:
        metadata: dict = {}
        raw_question = "Reconstruire le rapport 1/81 pour n=10"

    prompt = Pipeline._build_base_prompt(
        Pipeline.__new__(Pipeline), Ctx(), {"model": "1/81"}, {}, [], facts
    )

    assert "CRITÈRES CONVOLUTIFS OBLIGATOIRES" in prompt
    assert "point_1_niveau_1" in prompt
    assert "point_2_niveau_2" in prompt
    assert "point_3_verdict" in prompt
    assert "n-3 et n-2" in prompt
    assert "sqrt((k^(i-1))^2 + (k^i)^2)" in prompt


def test_aucun_premier_non_certifie_n_est_annonce() -> None:
    rapport = SpectralMethodCore().rapport_convolutif_non_typique("1/81", 10)

    assert rapport["premier_indetermine"] is True
    assert rapport["cible"]["premier"] is None
    assert rapport["aucun_ancrage"] is True

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
