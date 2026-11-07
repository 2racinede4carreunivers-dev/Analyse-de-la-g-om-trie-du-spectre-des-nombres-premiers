"""Test pour Pipeline._annotate_epistemic (Axes 4+5 integration finale)."""
from __future__ import annotations

import tempfile

import pytest

from src.core.types import FinalAnswer
from src.cognitive import reset_meta_reasoner


# Test isole sans construire un Pipeline complet (qui charge .thy etc.)
# On instancie un faux objet avec juste la methode necessaire.
class _FakePipeline:
    """Pipeline minimal pour tester _annotate_epistemic sans charger les .thy."""

    def __init__(self, learning_dir):
        from src.cognitive import get_meta_reasoner
        reset_meta_reasoner()
        self.meta_reasoner = get_meta_reasoner(learning_dir=learning_dir)

    # On reutilise la VRAIE methode du Pipeline
    from src.core.pipeline import Pipeline
    _annotate_epistemic = Pipeline._annotate_epistemic


@pytest.fixture
def fake_pipeline():
    with tempfile.TemporaryDirectory() as tmp:
        yield _FakePipeline(learning_dir=tmp)


class TestAnnotateEpistemic:
    def test_reconstruction_certain(self, fake_pipeline):
        final = FinalAnswer(question_id="q1", answer_text="Le 26e premier est 101.",
                            best_score=9.5, iterations_used=1)
        facts = {
            "n": 26, "p": 101, "model": "1/2",
            "equation_holds": True, "SA_float": 12.0, "SB_float": 24.0,
        }
        fake_pipeline._annotate_epistemic(
            final, facts, {"intent": "reconstruction"}, qid="q1",
        )
        assert final.epistemic_claim is not None
        assert final.epistemic_claim["certainty"] == "CERTAIN"
        assert "SpectralCore" in final.epistemic_claim["provenance"]
        assert final.epistemic_claim["can_cite"] is True

    def test_reconstruction_hors_domaine(self, fake_pipeline):
        final = FinalAnswer(question_id="q2", answer_text="Erreur calcul.",
                            best_score=2.0)
        facts = {"error": "Position 9999 hors table"}
        fake_pipeline._annotate_epistemic(
            final, facts, {"intent": "reconstruction"}, qid="q2",
        )
        assert final.epistemic_claim["certainty"] == "HORS_DOMAINE"
        assert "Position 9999" in final.epistemic_claim["evidence"]["error"]

    def test_pure_llm_response_conjecture(self, fake_pipeline):
        final = FinalAnswer(question_id="q3",
                            answer_text="Une conjecture sur Riemann...",
                            best_score=8.0)
        # Aucun fact precomputed
        fake_pipeline._annotate_epistemic(final, {}, {"intent": "general"}, qid="q3")
        assert final.epistemic_claim["certainty"] == "CONJECTURE"
        assert "LLM" in str(final.epistemic_claim["provenance"])

    def test_meta_reasoner_records_call(self, fake_pipeline):
        final = FinalAnswer(question_id="q4", answer_text="ok", best_score=9.0)
        facts = {"n": 10, "p": 29, "model": "1/2", "equation_holds": True}
        fake_pipeline._annotate_epistemic(
            final, facts, {"intent": "reconstruction"}, qid="q4",
        )
        report = fake_pipeline.meta_reasoner.report()
        assert report["reconstruction_1_2"]["total"] >= 1
        assert report["reconstruction_1_2"]["successes"] >= 1
