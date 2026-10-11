"""
Tests v3.30 (Philippe 2026-02) — Parsing des requetes de rapport spectral
asymetrique chaotique / ordonnee au format "Bloc A= {...} Bloc B= {...}".

Reproduit le bug rapporte : le multi-loop echouait a extraire les blocs
formates avec des accolades OU avec des labels "Bloc A=" / "Bloc B=".
"""
from __future__ import annotations

import pytest

from src.multiloop.request_decomposer import RequestDecomposer
from src.core.spectral_core import SpectralMethodCore


@pytest.fixture
def decomposer() -> RequestDecomposer:
    return RequestDecomposer()


@pytest.fixture
def core() -> SpectralMethodCore:
    return SpectralMethodCore()


class TestBlocAccoladeParsing:
    """Extraction des blocs avec accolades { }."""

    def test_accolades_avec_labels(self, decomposer):
        q = (
            "Determine le rapport spectral 1/2 asymetrique chaotique entre les "
            "blocs premiers A et B suivant: Bloc A= {7,11,23} "
            "Bloc B= {29,31,17,53,2}"
        )
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 23]
        assert dec.tuple_B == [29, 31, 17, 53, 2]
        assert dec.detected_intent == "ratio_spectral"
        assert dec.detected_ratio == "1/2"
        assert dec.announced_symmetric is False

    def test_accolades_sans_labels(self, decomposer):
        q = "rapport spectral {7,11,23} {29,31,17}"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 23]
        assert dec.tuple_B == [29, 31, 17]

    def test_ordonnee_avec_labels_et_accolades(self, decomposer):
        q = (
            "Determine le rapport spectral asymetrique ordonnee: "
            "Bloc A= {2,3,5} Bloc B= {7,11,13,17}"
        )
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [2, 3, 5]
        assert dec.tuple_B == [7, 11, 13, 17]
        assert dec.announced_symmetric is False
        assert dec.detected_ratio == "1/2"

    def test_parentheses_avec_labels(self, decomposer):
        q = "rapport spectral Bloc A= (7,11,23) Bloc B= (29,31,17,53,2)"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 23]
        assert dec.tuple_B == [29, 31, 17, 53, 2]

    def test_format_mixte_labels_accolades_parentheses(self, decomposer):
        q = "asymetrique chaotique Bloc A= {7,11,23} Bloc B= (29,31,17,53,2)"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 23]
        assert dec.tuple_B == [29, 31, 17, 53, 2]

    def test_crochets_supportes(self, decomposer):
        q = "rapport spectral Bloc A= [7,11,23] Bloc B= [29,31,17]"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 23]
        assert dec.tuple_B == [29, 31, 17]

    def test_labels_sans_delimiters(self, decomposer):
        q = "rapport spectral asymetrique chaotique A=7,11,2 B=23,17,43,31,29"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 2]
        assert dec.tuple_B == [23, 17, 43, 31, 29]

    def test_labels_sans_delimiters_avec_et(self, decomposer):
        q = "Bloc A= 7,11,2 et Bloc B= 23,17,43,31,29"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 11, 2]
        assert dec.tuple_B == [23, 17, 43, 31, 29]


class TestIntentDetection:
    """Detection d'intent pour asymetrique chaotique / ordonnee."""

    def test_intent_asym_chaotique(self, decomposer):
        q = "rapport spectral asymetrique chaotique Bloc A= {2,3} Bloc B= {5,7,11}"
        dec = decomposer.decompose(q)
        assert dec.detected_intent == "ratio_spectral"
        assert dec.announced_symmetric is False

    def test_intent_asym_ordonnee(self, decomposer):
        q = "rapport spectral asymetrique ordonnee Bloc A= {2,3} Bloc B= {5,7,11}"
        dec = decomposer.decompose(q)
        assert dec.detected_intent == "ratio_spectral"
        assert dec.announced_symmetric is False

    def test_intent_asym_chaotique_accent(self, decomposer):
        q = "rapport spectral asymétrique chaotique Bloc A= {2,3} Bloc B= {5,7,11}"
        dec = decomposer.decompose(q)
        assert dec.detected_intent == "ratio_spectral"
        assert dec.announced_symmetric is False


class TestEndToEndComputation:
    """Le pipeline complet doit produire un rapport valide."""

    def test_chaotique_calcul(self, decomposer, core):
        q = "asymetrique chaotique Bloc A= {7,11,23} Bloc B= {29,31,17,53,2}"
        dec = decomposer.decompose(q)
        assert dec.tuple_A and dec.tuple_B
        result = core.analyze_spectral_ratio(dec.tuple_A, dec.tuple_B)
        assert "error" not in result
        assert result["configuration"] in ("asym_chaotique", "asym_ordonnee")
        assert "RsP_fraction" in result
        assert "RsP_decimal" in result

    def test_ordonnee_calcul(self, decomposer, core):
        # Configuration ordonnee : |B|=|A|+1, listes croissantes, max(A)<min(B).
        q = "asymetrique ordonnee Bloc A= {2,3,5} Bloc B= {7,11,13,17}"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [2, 3, 5]
        assert dec.tuple_B == [7, 11, 13, 17]
        result = core.analyze_spectral_ratio(dec.tuple_A, dec.tuple_B)
        assert "error" not in result
        assert result["configuration"] == "asym_ordonnee"

    def test_symetrique_ne_regresse_pas(self, decomposer, core):
        """Regression: format nxn classique doit toujours fonctionner."""
        q = "rapport spectral symetrique 3*3 (7,23,2) (29,17,13)"
        dec = decomposer.decompose(q)
        assert dec.tuple_A == [7, 23, 2]
        assert dec.tuple_B == [29, 17, 13]
        assert dec.detected_intent == "ratio_spectral_nxn"
        assert dec.announced_symmetric is True

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
