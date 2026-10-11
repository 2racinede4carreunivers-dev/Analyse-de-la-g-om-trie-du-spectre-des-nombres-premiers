"""Tests pour le Modele de Certitude + Boucle Logique + Reponse Modeste.

Le slow-motion debugger applique maintenant un modele a 8 criteres
(3 questions Q1/Q2/Q3) sur la requete decomposee, applique une boucle
logique de sursaut, et produit une REQUETE MODESTE reformulee + une
REPONSE MODESTE certifiee par spectral_core.
"""
from __future__ import annotations

from src.multiloop.certainty_model import (
    CertaintyModel, CertaintyQuestion, CRITERIA,
)
from src.multiloop.logical_loop import LogicalLoop
from src.multiloop.request_decomposer import RequestDecomposer
from src.multiloop.slow_motion_debugger import SlowMotionDebugger
from src.multiloop.coherence_detector import CoherenceReport
from src.core.spectral_core import SpectralMethodCore
from src.adapters.corpus.certainty_kernel import CertaintyKernel
from src.core.types import FinalAnswer


# ==========================================================================
# CertaintyModel : 8 criteres / 3 questions
# ==========================================================================
class TestCertaintyModelBasic:
    def test_three_questions(self):
        questions = CertaintyModel.questions()
        assert set(questions.keys()) == {
            "Q1_POSITION", "Q2_MODELE", "Q3_CONFIGURATION",
        }

    def test_eight_criteria(self):
        criteria = CertaintyModel.criteria()
        assert len(criteria) == 8
        codes = {c.code for c in criteria}
        assert codes == {f"C{i}" for i in range(1, 9)}

    def test_each_criterion_has_skip_strategy(self):
        for c in CRITERIA:
            assert c.skip_strategy, f"{c.code} doit avoir une skip_strategy"

    def test_criteria_repartition_par_question(self):
        from collections import Counter
        repart = Counter(c.question for c in CRITERIA)
        # Q1=2 (position+premier_connu), Q2=2 (ratio+intent),
        # Q3=4 (tuples_presents, symetrie, premiers, ratio_atteignable)
        assert repart[CertaintyQuestion.Q1_POSITION] == 2
        assert repart[CertaintyQuestion.Q2_MODELE] == 2
        assert repart[CertaintyQuestion.Q3_CONFIGURATION] == 4


# ==========================================================================
# CertaintyModel : evaluation
# ==========================================================================
class TestCertaintyModelEvaluate:
    def setup_method(self):
        self.core = SpectralMethodCore()
        self.model = CertaintyModel(spectral_core=self.core)
        self.dec = RequestDecomposer()

    def test_reconstruction_position_valide_tout_pass(self):
        decomposed = self.dec.decompose("reconstruire le 10eme premier en rapport 1/2")
        ev = self.model.evaluate(decomposed)
        assert ev.is_fully_certain
        assert len(ev.violated_codes) == 0

    def test_position_hors_table_viole_c1(self):
        decomposed = self.dec.decompose("reconstruire le 99999eme premier en rapport 1/2")
        ev = self.model.evaluate(decomposed)
        assert "C1" in ev.violated_codes

    def test_symetrie_mismatch_viole_c6(self):
        decomposed = self.dec.decompose(
            "rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)"
        )
        ev = self.model.evaluate(decomposed)
        assert "C6" in ev.violated_codes
        # Et la motivation doit mentionner les tailles
        c6 = next(r for r in ev.results if r.code == "C6")
        assert "|A|" in c6.detail or "asym" in c6.detail.lower()

    def test_certainty_ratio_partiel(self):
        decomposed = self.dec.decompose(
            "rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)"
        )
        ev = self.model.evaluate(decomposed)
        # Au moins C6 et C8 doivent echouer
        assert ev.certainty_ratio < 1.0
        assert ev.certainty_ratio > 0.0


# ==========================================================================
# LogicalLoop : produire la requete modeste
# ==========================================================================
class TestLogicalLoop:
    def setup_method(self):
        self.core = SpectralMethodCore()
        self.model = CertaintyModel(spectral_core=self.core)
        self.loop = LogicalLoop(spectral_core=self.core)
        self.dec = RequestDecomposer()

    def test_symetrie_violee_genere_sursaut_drop_symmetry(self):
        decomposed = self.dec.decompose(
            "rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)"
        )
        ev = self.model.evaluate(decomposed)
        modest = self.loop.derive_modest_request(decomposed, ev)
        # Au moins un sursaut "drop_symmetry" doit avoir ete applique
        strategies = [s["strategy"] for s in modest.skips_applied]
        assert "drop_symmetry" in strategies
        # La requete modeste doit etre soit asymetrique, soit ramenee a 1x1 :
        # ces 2 cas sont MODESTES et satisfont la coherence epipolaire.
        lower = modest.canonical_text.lower()
        assert ("asymetrique" in lower) or ("1x1" in lower) or ("elementaire" in lower)

    def test_position_hors_table_genere_drop_position(self):
        from src.spectral.prime_table import max_position
        decomposed = self.dec.decompose(
            "reconstruire le 99999eme premier en rapport 1/2"
        )
        ev = self.model.evaluate(decomposed)
        modest = self.loop.derive_modest_request(decomposed, ev)
        strategies = [s["strategy"] for s in modest.skips_applied]
        assert "drop_position" in strategies
        # La position modeste doit etre ramenee dans la table
        assert modest.position is not None
        assert 1 <= modest.position <= max_position()

    def test_requete_deja_coherente_aucun_sursaut(self):
        decomposed = self.dec.decompose(
            "reconstruire le 10eme premier en rapport 1/2"
        )
        ev = self.model.evaluate(decomposed)
        modest = self.loop.derive_modest_request(decomposed, ev)
        assert len(modest.skips_applied) == 0
        assert modest.position == 10
        assert modest.ratio == "1/2"

    def test_modest_request_serialisable(self):
        import json
        decomposed = self.dec.decompose(
            "reconstruire le 10eme premier en rapport 1/2"
        )
        ev = self.model.evaluate(decomposed)
        modest = self.loop.derive_modest_request(decomposed, ev)
        # Doit etre JSON-serialisable (pour audit)
        json.dumps(modest.to_dict())


# ==========================================================================
# SlowMotionDebugger : integration complete
# ==========================================================================
class TestSlowMotionIntegration:
    def setup_method(self):
        self.dbg = SlowMotionDebugger(
            certainty_kernel=CertaintyKernel(),
            spectral_core=SpectralMethodCore(),
        )
        self.report = CoherenceReport(
            score=0.5, incoherent=True, signals=["test"],
            best_candidate_score=5.0,
        )

    def test_structured_data_contient_certainty_evaluation(self):
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        res = self.dbg.debug(
            question="rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)",
            final=final, coherence_report=self.report, skip_auto_audit=True,
        )
        ev = res.structured_data["certainty_evaluation"]
        assert "passed_codes" in ev
        assert "violated_codes" in ev
        assert len(ev["results"]) == 8
        assert ev["certainty_ratio"] < 1.0  # car C6/C8 violes

    def test_structured_data_contient_modest_request(self):
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        res = self.dbg.debug(
            question="rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)",
            final=final, coherence_report=self.report, skip_auto_audit=True,
        )
        mr = res.structured_data["modest_request"]
        assert mr["canonical_text"]
        assert "skips_applied" in mr
        assert len(mr["skips_applied"]) > 0  # au moins drop_symmetry

    def test_structured_data_contient_modest_certified(self):
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        res = self.dbg.debug(
            question="rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)",
            final=final, coherence_report=self.report, skip_auto_audit=True,
        )
        mc = res.structured_data["modest_certified"]
        assert mc["summary"]
        # La reponse modeste doit citer la methode
        assert mc.get("method")

    def test_timeline_contient_8_etapes_minimum(self):
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        res = self.dbg.debug(
            question="rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)",
            final=final, coherence_report=self.report, skip_auto_audit=True,
        )
        labels = {ev["label"] for ev in res.structured_data["debug_timeline"]}
        assert "EVALUATION_CERTITUDE" in labels
        assert "BOUCLE_LOGIQUE" in labels
        assert "REPONSE_MODESTE" in labels
        assert "REFORMULATIONS" in labels

    def test_reponse_modeste_resoud_effectivement(self):
        """La reponse modeste doit avoir un summary non-vide ET coherent."""
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        res = self.dbg.debug(
            question="reconstruire le 10eme premier en rapport 1/2",
            final=final, coherence_report=self.report, skip_auto_audit=True,
        )
        mc = res.structured_data["modest_certified"]
        # Pour la 10eme position, le premier est 29
        assert "29" in mc["summary"]

    def test_reponse_modeste_symetrie_violee_resoud_en_asymetrique(self):
        """Cas Philippe : la reponse modeste doit donner le RsP asymetrique."""
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        res = self.dbg.debug(
            question="rapport spectral symetrique 4*4 entre (7,23,79,31) et (17,11,3)",
            final=final, coherence_report=self.report, skip_auto_audit=True,
        )
        mc = res.structured_data["modest_certified"]
        # La reponse modeste doit explicitement calculer un rapport spectral
        # (configuration asymetrique apres sursaut)
        assert mc["summary"]
        assert "Rapport spectral" in mc["summary"] or "RsP" in mc["summary"]

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
