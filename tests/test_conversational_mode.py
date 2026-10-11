"""
Tests v3.24 : verifie le mode "conversation libre" ajoute pour permettre
a Gabriel de tenir une discussion naturelle sur la Methode Spectrale sans
que le Slow-Motion Debugger ne s'active des la moindre reformulation.

Reporte par Philippe le 2026-07-09 : "l'agent Gabriel ne parvient pas
beaucoup a tenir la discussion en dehors des 3 questions canoniques.
A chaque fois que je tente une question qui necessite de sa part de
repondre pour tenir la conversation, le Slow-Motion s'enclenche."

Solution :
1. Detection des patterns conversationnels dans RequestDecomposer
   (is_conversational=True).
2. Dans le pipeline, si is_conversational + coherence >= 0.30,
   bypass du Slow-Motion (mode "conversation libre").
3. Le Slow-Motion reste actif pour les vraies incoherences graves
   (coherence < 0.30) et les 3 questions canoniques strictes.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.multiloop.request_decomposer import RequestDecomposer  # noqa: E402


class TestDetectConversationalPatterns:
    """Le decomposer detecte les questions conversationnelles."""

    @pytest.fixture(scope="class")
    def dec(self):
        return RequestDecomposer()

    @pytest.mark.parametrize("question", [
        "Qu'est-ce que la Methode Spectrale ?",
        "Peux-tu m'expliquer comment marche RsP ?",
        "Explique-moi les 3 piliers de la theorie",
        "Comment fais-tu pour reconstruire un premier ?",
        "Pourquoi le rapport spectral vaut 1/2 ?",
        "Dis-moi ce que tu penses de mes suites A et B",
        "Peux-tu me resumer les regles de construction ?",
        "Aide-moi a comprendre le postulat spectral",
        "Quelle est la difference entre suite A et suite B ?",
        "Que veut dire prime_i ?",
        "Definition de digamma_calc ?",
        "Parle-moi de la Section XI",
    ])
    def test_pattern_conversationnel_detected(self, dec, question):
        result = dec.decompose(question)
        assert result.is_conversational is True, (
            f"Question conversationnelle non detectee : '{question}'"
        )

    @pytest.mark.parametrize("question", [
        "Reconstruis le 5-ieme premier",
        "RsP(2, 5) = ?",
        "Ecart entre 11 et 13",
        "Rapport spectral 3*3 entre A=(2,3,5) et B=(7,11,13)",
        "digamma_calc(10, 29) = ?",
    ])
    def test_canonical_not_flagged_conversational(self, dec, question):
        """Les 3 questions canoniques strictes ne doivent PAS etre
        marquees conversationnelles (elles gardent le Slow-Motion strict)."""
        result = dec.decompose(question)
        assert result.is_conversational is False, (
            f"Question canonique marquee conversationnelle a tort : '{question}'"
        )


class TestConversationalBypassInPipeline:
    """Le pipeline doit passer en mode conversation libre quand la requete
    est conversationnelle ET que la coherence multiloop est >= 0.30."""

    def test_pipeline_uses_decomposer(self):
        """Verifie que Pipeline expose bien un slow_motion.decomposer
        pour permettre la detection conversationnelle."""
        try:
            from src.core.pipeline import Pipeline
        except ImportError:
            pytest.skip("Pipeline non importable dans ce contexte")

        # Verifie que Pipeline peut acceder au decomposer via slow_motion
        pipeline_src = Path(ROOT / "src" / "core" / "pipeline.py").read_text()
        assert "self.slow_motion.decomposer.decompose(question)" in pipeline_src, (
            "Pipeline doit utiliser slow_motion.decomposer pour la detection "
            "conversationnelle (correctif v3.24)"
        )

    def test_conversational_bypass_logic(self):
        """Verifie la logique de bypass dans le code source."""
        pipeline_src = Path(ROOT / "src" / "core" / "pipeline.py").read_text()

        # 3 marqueurs cle du correctif v3.24
        markers = [
            "MODE CONVERSATION",
            "conversational_bypass",
            "is_conversational",
            "coherence.score >= 0.30",
        ]
        for marker in markers:
            assert marker in pipeline_src, (
                f"Marqueur v3.24 manquant dans pipeline.py : '{marker}'"
            )

    def test_bypass_only_if_coherence_ok(self):
        """Le bypass ne doit s'activer QUE si coherence >= 0.30
        (protege contre les vraies incoherences graves)."""
        pipeline_src = Path(ROOT / "src" / "core" / "pipeline.py").read_text()
        # Verifie le pattern de la condition
        assert "coherence.score >= 0.30" in pipeline_src

    def test_slow_motion_still_activates_for_incoherent(self):
        """v3.32 : Philippe a mis le debugger Slow-Motion EN PAUSE volontaire
        (commit 'PAUSE debugger timeline', voir GABRIEL_DEBUGGER_PAUSE_STATUS.md).
        Le pipeline ne declenche plus le kernel d'urgence : Claude repond a
        toutes les requetes. Ce test sentinelle verifie que la PAUSE est
        explicitement documentee dans le code (pas une suppression muette)."""
        pipeline_src = Path(ROOT / "src" / "core" / "pipeline.py").read_text()
        assert "DEBUGGER ANNULE COMPLETEMENT" in pipeline_src, (
            "La pause du debugger doit rester explicitement documentee dans "
            "pipeline.py. Si le Slow-Motion est reactive, restaurer l'assertion "
            "'coherence.incoherent and not conversational_bypass'."
        )


class TestConversationalRegression:
    """Verifie que les questions canoniques strictes gardent le comportement
    d'avant (pas de bypass). Aucune regression sur le Slow-Motion strict."""

    @pytest.fixture(scope="class")
    def dec(self):
        return RequestDecomposer()

    def test_canonical_reconstruction_still_strict(self, dec):
        r = dec.decompose("Reconstruis le 100-ieme premier avec rapport 1/2")
        assert r.detected_intent == "reconstruction"
        assert r.is_conversational is False

    def test_canonical_rsp_still_strict(self, dec):
        r = dec.decompose("Calcul du rapport spectral entre positions 10 et 20")
        assert r.detected_intent in ("ratio_spectral", "ratio_spectral_nxn",
                                     "reconstruction")
        assert r.is_conversational is False

    def test_canonical_gap_still_strict(self, dec):
        r = dec.decompose("Ecart spectral entre 29 et 31")
        # Detecte 'gap' comme intent
        assert r.detected_intent == "gap"
        assert r.is_conversational is False


class TestConversationalCoverage:
    """Verifie la couverture des patterns conversationnels courants."""

    @pytest.fixture(scope="class")
    def dec(self):
        return RequestDecomposer()

    def test_all_10_conversational_patterns_work(self, dec):
        """Chaque famille de pattern conversationnel doit detecter au moins
        un exemple representatif."""
        examples_per_pattern = {
            "qu-est-ce-que": "Qu'est-ce que le digamma calcule ?",
            "explique": "Explique le postulat spectral",
            "comment-question": "Comment marche la reconstruction ?",
            "pourquoi": "Pourquoi utiliser 1/2 et pas 1/3 ?",
            "peux-tu-me-dire": "Peux-tu me dire ce qu'est SA ?",
            "definition": "Definition du rapport spectral",
            "que-penses-tu": "Que penses-tu de ma conjecture ?",
            "aide-moi": "Aide-moi a formaliser la preuve",
            "difference": "Difference entre suite A et suite B",
            "resume": "Resume la Methode Spectrale",
        }
        for name, question in examples_per_pattern.items():
            result = dec.decompose(question)
            assert result.is_conversational, (
                f"Pattern '{name}' non declenche par : '{question}'"
            )

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
