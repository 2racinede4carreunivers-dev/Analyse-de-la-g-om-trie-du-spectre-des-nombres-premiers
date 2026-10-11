"""Tests de regression anti-hallucination pour le rapport spectral 1/14 (k=14).

Le rapport 1/14 a historiquement fait halluciner un LLM en injectant le facteur du
regime 1/2 (64 = 2^6) et « Candidat: Non déterminé ». Le facteur d’un rapport 1/k
(k>=3) est le facteur GENERIQUE k^6 (14^6 = 7529536), JAMAIS 64 (64 = 2^6 est
exclusif a 1/2). Facteur geometrique niveau 2 = sqrt(1+k^2) : 1/14 -> sqrt(197)
= 14.0356688476, g(k)=sqrt(197)/14=1.0025477748. 4 branches Digamma a n=10 COMPOSES.

Verrouille : (1) routage RAG 1/14 -> regime_parametrique_1_k (jamais 1/2) ;
(2) facteur k^6 dans le prompt (64 etiqule exclusif 1/2) ; (3) ABSENCE de
« facteur 64 » / « Non déterminé » dans le resume src/ ; (4) coherences valeurs.
NOTE : « 64 » apparait legitennement dans SA(19)=6403350348031690322234 et dans
« 2^6 = 64 » etiquete exclusif 1/2 — ce n’est PAS l’hallucination.
"""
from __future__ import annotations

import math
import re

import pytest

from memory import (
    DICTIONNAIRE_SPECTRAL,
    AdaptateurCognitifSpectral,
    preparer_requete_avec_rag,
)
from memory.dictionnaire_spectral import Regime, regime_count

from src.core.spectral_core import SpectralMethodCore
from src.core.pipeline import Pipeline
from src.core.zeta_denominator_core import (
    calculer_zeta_denominator,
    extraire_k_depuis_rapport,
    valider_zeta_usage,
)

K = 14
K6 = 7529536                       # 14 ** 6
SQRT197 = math.sqrt(197)           # 14.0356688476...  (numerateur facteur geometrique)
GK = SQRT197 / K                   # 1.0025477748... (g(k), rendu par le resume)
SA_19 = 6403350348031690322234
SB_19 = 89646904872443656981754
SA_10 = 309923810490
SB_10 = 4338925817338
CANDIDATS_C_N10 = {535079, 535107, 534897, 535289}  # 4 branches Digamma n=10 COMPOSES
REGIME_PARAM = "regime_parametrique_1_k"
REGIME_1_2 = "regime_1_2_positif"


def _match_keywords(patterns, text):
    out = []
    for p in patterns:
        m = re.compile(p, re.IGNORECASE).search(text)
        if m:
            out.append(m.group(0))
    return out


@pytest.fixture(scope="module")
def regime_param():
    return DICTIONNAIRE_SPECTRAL[REGIME_PARAM]


@pytest.fixture(scope="module")
def rapport_19():
    return SpectralMethodCore().rapport_convolutif_non_typique("1/14", 19)


@pytest.fixture(scope="module")
def rapport_10():
    return SpectralMethodCore().rapport_convolutif_non_typique("1/14", 10)


@pytest.fixture(scope="module")
def summary(rapport_19):
    facts = dict(rapport_19)
    facts["model"] = "1/14"
    facts["equation_holds"] = False
    return Pipeline._append_convolution_summary("Réponse.", facts)


# 1. Dictionnaire : compte de regimes BLOQUE a 13 (regression)
def test_dictionnaire_conserve_exactement_13_regimes():
    assert regime_count() == 13
    assert REGIME_PARAM in DICTIONNAIRE_SPECTRAL
    assert REGIME_1_2 in DICTIONNAIRE_SPECTRAL


def test_regle_3_globale_est_generique_k6(regime_param):
    from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral
    rg = AdaptateurCognitifSpectral.REGLES_GLOBALES
    assert "REGLE 3" in rg                        # cle conservee (test existant)
    assert "JAMAIS de generalisations" not in rg  # regle obsolete retiree
    assert "k^6" in rg
    assert "7529536" in rg                        # 14^6
    assert "2^6 = 64" in rg                       # 64 etiqule EXCLUSIF 1/2
    assert "sqrt(197)" in rg


# 2. Routage memoire RAG : 1/14 -> regime_parametrique_1_k, jamais 1/2
def test_1_14_pattern_detection_matche_1_sur_14_mais_pas_1_sur_2(regime_param):
    assert "1/14" in _match_keywords(regime_param.patterns_detection, "rapport 1/14")
    assert "1/2" not in _match_keywords(regime_param.patterns_detection, "rapport 1/2")


def test_1_14_route_memoire_vers_regime_generique():
    regimes, _ = AdaptateurCognitifSpectral().detecter_regimes(
        "Reconstruire le rapport 1/14 (k=14) pour n=19"
    )
    assert REGIME_PARAM in regimes
    assert REGIME_1_2 not in regimes              # le contenu 1/2 ne doit pas fuiter


def test_1_14_prompt_contient_k6_et_exclut_64_comme_facteur():
    analyse = preparer_requete_avec_rag(
        "Reconstruire le rapport 1/14 (k=14) pour n=19"
    )
    prompt = analyse["prompt_augmente"]
    regimes = analyse["regimes_detectes"]
    assert REGIME_PARAM in regimes
    assert REGIME_1_2 not in regimes
    assert "k^6" in prompt
    assert "7529536" in prompt                    # 14^6
    assert "2^6 = 64" in prompt                   # 64 = 2^6 etiqule EXCLUSIF 1/2
    assert "sqrt(197)" in prompt
    assert "14.0356688476" in prompt
    assert "JAMAIS de generalisations" not in prompt


# 3. Coherences des valeurs de reference (suites / equations / meta)
def test_1_14_meta_et_suites(rapport_19):
    assert rapport_19["k"] == 14
    assert rapport_19["rapport"] == "1/14"
    assert rapport_19["_k"] == 14
    assert rapport_19["_zeta_used"] == K6        # 14^6, jamais 64
    assert rapport_19["_zeta_patch_applied"] is True
    assert rapport_19["equation_A"]["forme"] == "A(n) = (38221/35672) * 14^n + (-14/13)"
    assert rapport_19["equation_B"]["forme"] == "B(n) = (38221/2548) * 14^n + (-97883982/13)"
    assert rapport_19["cible"]["somme_A"] == SA_19
    assert rapport_19["cible"]["somme_B"] == SB_19
    assert rapport_19["reference_n10"]["somme_A"] == SA_10
    assert rapport_19["reference_n10"]["somme_B"] == SB_10


def test_1_14_candidats_n10_quatre_composes(rapport_10):
    """Les 4 branches Digamma a n=10 sont COMPOSES, facteur zeta = k^6 = 7529536."""
    poss = rapport_10["niveau_1"]["possibilites"]
    assert len(poss) == 4
    assert {p["position"] for p in poss} == {7, 8}      # n-3, n-2
    assert {p["signe"] for p in poss} == {1, -1}
    assert all(p["verdict"] == "COMPOSE" for p in poss)
    assert all(p["zeta"] == K6 for p in poss)           # facteur k^6
    assert all(p["zeta"] != 64 for p in poss)           # jamais le facteur 1/2
    assert {p["C"] for p in poss} == CANDIDATS_C_N10


def test_1_14_zeta_denominator_core():
    """couche src/core : 1/14 -> k^6 = 7529536, et jamais 64."""
    assert extraire_k_depuis_rapport("1/14") == 14
    assert extraire_k_depuis_rapport("1/2") == 2
    assert calculer_zeta_denominator("1/14") == K6
    assert calculer_zeta_denominator("1/2") == 64
    assert valider_zeta_usage("1/14", K6) is True
    assert valider_zeta_usage("1/14", 64) is False     # REGRESSION 64


# 4. Resume cognitif : anti-hallucination (facteur 64 / Non déterminé)
def test_1_14_summary_contient_k6_et_facteur_geometrique(summary):
    assert "7529536" in summary                  # k^6 = 14^6
    assert "Zêta=7529536" in summary              # facteur de reconstruction = k^6
    assert "1.0025477748" in summary              # g(k) = sqrt(197)/14
    assert math.isclose(SQRT197, 14.0356688476, abs_tol=1e-6)
    assert math.isclose(GK, 1.0025477748, rel_tol=1e-9)
    assert "[COMPOSE]" in summary
    assert "A(16)+" in summary and "A(16)-" in summary
    assert "A(17)+" in summary and "A(17)-" in summary


def test_1_14_summary_anti_hallucination_facteur_64(summary):
    """Le facteur 64 ne doit jamais apparaitre comme facteur de reconstruction."""
    low = summary.lower()
    assert "facteur 64" not in low
    assert "zêta=64" not in low
    assert "zêta = 64" not in low
    # la formule 1/2 digamma = SB - 64*p ne doit pas fuiter dans le resume 1/14
    assert "/ 64" not in summary
    assert "- 64 *" not in summary
    assert "-64*" not in summary.replace(" ", "")


def test_1_14_summary_anti_hallucination_non_determiné(summary):
    """Ni « Candidat: Non déterminé », ni « Non déterminé » ne figurent dans le resume."""
    assert "candidat: non déterminé" not in summary.lower()
    assert "non déterminé" not in summary.lower()

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
