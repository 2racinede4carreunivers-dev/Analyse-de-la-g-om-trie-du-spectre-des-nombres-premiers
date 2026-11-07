"""
Tests pour la preuve par l'absurde : la Methode Spectrale exclut strictement
les composes.

Couvre :
- Le module src/spectral/composite_absurdity_prover.py (unit).
- L'integration dans PipelineWithGapDetection : quand un compose est
  detecte dans une requete d'ecart, un FinalAnswer pedagogique est retourne
  au lieu de tenter (et echouer silencieusement) le GapSolver.
- La reference au fichier Isabelle/HOL theories/methode_spectral.thy et
  presence des theoremes attendus.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.spectral.composite_absurdity_prover import (
    CompositeRejection,
    build_composite_rejection,
    detect_composite_in_gap_request,
    factorize,
    is_prime,
    nearest_primes,
)


# ============================================================================
# UNIT — is_prime, factorize, nearest_primes
# ============================================================================

class TestIsPrime:
    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                                    47, 53, 59, 97, 947])
    def test_primes(self, n):
        assert is_prime(n) is True
        assert is_prime(-n) is True  # convention Methode Spectrale

    @pytest.mark.parametrize("n", [0, 1, -1, 4, 6, 8, 9, 10, 12, 14, 15,
                                    16, 18, 20, 21, 22, 24, 25, 27,
                                    49, 51, 91, 121])
    def test_composites_and_units(self, n):
        assert is_prime(n) is False
        if n != 0:
            assert is_prime(-n) is False

    def test_beyond_table(self):
        # Au-dela des 1000 premiers indexes (>= 7919), utilise le fallback naif
        # 7907 est le 1000e premier, 7919 est premier, 7920 = 2^4 * 3^2 * 5 * 11
        assert is_prime(7919) is True
        assert is_prime(7920) is False


class TestFactorize:
    @pytest.mark.parametrize("n,expected", [
        (4, [2, 2]),
        (9, [3, 3]),
        (15, [3, 5]),
        (51, [3, 17]),
        (91, [7, 13]),
        (121, [11, 11]),
        (100, [2, 2, 5, 5]),
        (-51, [3, 17]),  # signe ignore
    ])
    def test_decomposition(self, n, expected):
        assert factorize(n) == expected

    @pytest.mark.parametrize("n", [0, 1, -1])
    def test_edge_cases(self, n):
        assert factorize(n) == []


class TestNearestPrimes:
    def test_composite_51(self):
        below, above = nearest_primes(51)
        assert below == 47
        assert above == 53

    def test_composite_9(self):
        below, above = nearest_primes(9)
        assert below == 7
        assert above == 11

    def test_prime_returns_itself(self):
        # Cas ou l'on demande le voisin d'un premier : retourne (p, p)
        # (le caller doit d'abord filtrer via is_prime)
        below, above = nearest_primes(7)
        assert below == 7
        assert above == 7


# ============================================================================
# UNIT — build_composite_rejection
# ============================================================================

class TestBuildCompositeRejection:
    def test_returns_none_for_prime(self):
        assert build_composite_rejection(7) is None
        assert build_composite_rejection(-7) is None
        assert build_composite_rejection(947) is None

    def test_returns_none_for_units(self):
        assert build_composite_rejection(0) is None
        assert build_composite_rejection(1) is None
        assert build_composite_rejection(-1) is None

    def test_returns_rejection_for_51(self):
        rej = build_composite_rejection(51)
        assert rej is not None
        assert rej.value == 51
        assert rej.factors == [3, 17]
        assert rej.is_negative is False
        assert rej.nearest_prime_below == 47
        assert rej.nearest_prime_above == 53
        assert rej.thy_reference == "no_spectral_position_for_51"

    def test_returns_rejection_for_negative_51(self):
        rej = build_composite_rejection(-51)
        assert rej is not None
        assert rej.value == -51
        assert rej.factors == [3, 17]
        assert rej.is_negative is True
        # Les voisins sont retournés en valeur absolue ; le signe est reconstruit
        # côté texte pédagogique.
        assert rej.nearest_prime_below == 47

    @pytest.mark.parametrize("n,expected_thy", [
        (4, "no_spectral_position_for_4"),
        (9, "no_spectral_position_for_9"),
        (15, "no_spectral_position_for_15"),
        (51, "no_spectral_position_for_51"),
        (91, "no_spectral_position_for_91"),
        (121, "no_spectral_position_for_121"),
    ])
    def test_canonical_thy_reference(self, n, expected_thy):
        rej = build_composite_rejection(n)
        assert rej is not None
        assert rej.thy_reference == expected_thy

    def test_non_canonical_composite_has_empty_thy_ref(self):
        # 25 = 5*5 n'est PAS dans le corpus canonique
        rej = build_composite_rejection(25)
        assert rej is not None
        assert rej.thy_reference == ""


class TestPedagogicalText:
    def test_text_contains_rejection_marker(self):
        rej = build_composite_rejection(51)
        text = rej.to_pedagogical_text()
        assert "[ARRET]" in text
        assert "51" in text
        assert "n'est pas un nombre premier" in text

    def test_text_contains_decomposition(self):
        rej = build_composite_rejection(51)
        text = rej.to_pedagogical_text()
        assert "3 x 17" in text or "3 × 17" in text

    def test_text_references_isabelle(self):
        rej = build_composite_rejection(51)
        text = rej.to_pedagogical_text()
        assert "composite_not_prime_i" in text
        assert "methode_spectral.thy" in text
        assert "no_spectral_position_for_51" in text

    def test_text_suggests_nearest_primes(self):
        rej = build_composite_rejection(51)
        text = rej.to_pedagogical_text()
        assert "47" in text and "53" in text

    def test_negative_composite_decomposition(self):
        rej = build_composite_rejection(-51)
        text = rej.to_pedagogical_text()
        assert "-51" in text
        # Voisins negatifs suggeres
        assert "-47" in text or "-53" in text


# ============================================================================
# UNIT — detect_composite_in_gap_request
# ============================================================================

class TestDetectCompositeInGapRequest:
    def test_both_primes_no_rejection(self):
        assert detect_composite_in_gap_request([-7, -5]) == []
        assert detect_composite_in_gap_request([3, 23]) == []
        assert detect_composite_in_gap_request([-31, 17]) == []

    def test_one_composite_returns_one_rejection(self):
        rejs = detect_composite_in_gap_request([-7, -51])
        assert len(rejs) == 1
        assert rejs[0].value == -51

    def test_two_composites_returns_two_rejections(self):
        rejs = detect_composite_in_gap_request([15, 51])
        assert len(rejs) == 2
        assert {r.value for r in rejs} == {15, 51}

    def test_order_preserved(self):
        rejs = detect_composite_in_gap_request([51, 15])
        assert [r.value for r in rejs] == [51, 15]


# ============================================================================
# INTEGRATION — PipelineWithGapDetection intercepte les composés
# ============================================================================

class TestPipelineInterceptsComposites:
    def _make_pipeline(self):
        from src.core.pipeline_with_gap_detection import PipelineWithGapDetection

        base = MagicMock()
        base.spectral_core = MagicMock()

        async def fake_process(question):
            # Ne devrait PAS être appelé pour une requête à composé
            from src.core.types import FinalAnswer
            return FinalAnswer(
                question_id="fallback",
                answer_text="FALLBACK_MULTILOOP",
                structured_data={},
                confidence=0.0,
            )

        base.process = fake_process
        return PipelineWithGapDetection(base)

    def test_composite_rejection_for_minus7_minus51(self):
        """Cas exact rapporté par Philippe : gap(-7, -51) doit produire un
        rejet pédagogique, PAS un échec silencieux ni un fallback multiloop."""
        pipeline = self._make_pipeline()
        result = asyncio.run(pipeline.process(
            "Détermine l'écart négative entre les premiers -7 et -51"
        ))
        assert result.answer_text != "FALLBACK_MULTILOOP", (
            "Le pipeline NE DOIT PAS retomber sur le multiloop standard "
            "quand un composé est détecté (comportement pédagogique)"
        )
        assert "-51" in result.answer_text
        assert "n'est pas un nombre premier" in result.answer_text
        assert result.structured_data["rejection_type"] == "composite_detected"
        assert result.structured_data["thy_theorem"] == "composite_not_prime_i"

    def test_no_rejection_when_both_primes(self):
        """Cas nominal : les deux nombres sont premiers → GapSolver résout."""
        pipeline = self._make_pipeline()
        result = asyncio.run(pipeline.process(
            "Écart entre -19 et -5"
        ))
        # Le GapSolver doit avoir été invoqué et réussi
        # (structured_data.gap_type devrait exister)
        assert (
            result.structured_data.get("gap_type") == "negative_negative"
            or result.answer_text != "FALLBACK_MULTILOOP"
        )

    def test_rejection_structured_data_contains_thy_refs(self):
        pipeline = self._make_pipeline()
        result = asyncio.run(pipeline.process(
            "Écart entre 15 et 47"
        ))
        composites = result.structured_data.get("composites", [])
        assert len(composites) >= 1
        c15 = next((c for c in composites if c["value"] == 15), None)
        assert c15 is not None
        assert c15["thy_reference"] == "no_spectral_position_for_15"
        assert c15["decomposition"] == "15 = 3 x 5"


# ============================================================================
# ISABELLE — Vérifie que la nouvelle section existe dans methode_spectral.thy
# ============================================================================

class TestIsabelleHOLSection:
    @pytest.fixture(scope="class")
    def thy_content(self) -> str:
        thy = ROOT / "theories" / "methode_spectral.thy"
        assert thy.exists(), f"Fichier {thy} absent"
        return thy.read_text(encoding="utf-8")

    def test_section_header_present(self, thy_content):
        assert (
            'section "Preuve par l\'absurde : la Methode Spectrale '
            'exclut strictement les composes"' in thy_content
        )

    def test_main_theorem_present(self, thy_content):
        assert "theorem composite_not_prime_i:" in thy_content
        assert "ALL i. C ~= prime_i i" in thy_content

    def test_corollary_present(self, thy_content):
        assert "spectral_method_exclusively_for_primes" in thy_content

    @pytest.mark.parametrize("value", [4, 9, 15, 51, 91, 121])
    def test_numerical_theorem_for_each_canonical_composite(self, thy_content, value):
        assert f"no_spectral_position_for_{value}:" in thy_content
        assert f"composite_{value}_not_prime:" in thy_content

    def test_interpretation_text_present(self, thy_content):
        # La section d'interprétation doit mentionner le log Gabriel comme
        # preuve empirique (idée originale Philippe). Le texte peut être
        # sur plusieurs lignes → on normalise les whitespaces avant la
        # recherche.
        import re
        normalized = re.sub(r"\s+", " ", thy_content)
        assert "log Gabriel" in normalized or "Log Gabriel" in normalized
        assert "CONTRAPOSITION EFFECTIVE" in normalized

    def test_philippe_attribution_present(self, thy_content):
        # L'idée originale doit être attribuée à Philippe (respect de l'auteur)
        assert "Philippe Thomas Savard" in thy_content
        assert "2026-07-02" in thy_content or "juillet 2026" in thy_content


# ============================================================================
# END-TO-END : le message Philippe exact
# ============================================================================

def test_e2e_philippe_original_query():
    """Reproduit la requête exacte de Philippe le 2026-07-02.

    Requête : "Détermine l'écart négative entre les premiers -7 et -51"
    Attendu : rejet pédagogique + décomposition -51 = 3 × 17 + référence
    au théorème composite_not_prime_i.
    """
    from src.core.pipeline_with_gap_detection import PipelineWithGapDetection

    base = MagicMock()
    base.spectral_core = MagicMock()

    async def fake_process(question):
        from src.core.types import FinalAnswer
        return FinalAnswer(
            question_id="should_not_happen",
            answer_text="NEVER",
            structured_data={},
        )

    base.process = fake_process
    pipeline = PipelineWithGapDetection(base)

    result = asyncio.run(pipeline.process(
        "Détermine l'écart négative entre les premiers -7 et -51"
    ))
    txt = result.answer_text
    # Vérifications clés
    assert "-51" in txt
    # Pour un composé négatif, le texte affiche "-51 = -(3 x 17) = -51"
    assert "3 x 17" in txt or "3 × 17" in txt
    assert "composite_not_prime_i" in txt
    assert "methode_spectral.thy" in txt
    assert result.confidence == 1.0
    assert result.structured_data["rejection_type"] == "composite_detected"

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
