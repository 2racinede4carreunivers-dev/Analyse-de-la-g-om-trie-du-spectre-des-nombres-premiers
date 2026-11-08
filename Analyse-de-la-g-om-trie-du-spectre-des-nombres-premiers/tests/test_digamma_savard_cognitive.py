import asyncio
from fractions import Fraction

import pytest

from src.core.integrateur_memoire import IntegrateurMemoireGabriel
from src.core import llm_manager
from src.core.pipeline import Pipeline
from src.multiloop.pre_reasoner import PreReasoner
from src.spectral.digamma_savard_cognitive import (
    digamma_savard_context_for_query,
    digamma_savard_facts_for_query,
    digamma_savard_n10,
    spectral_sums,
)
from src.spectral.convolutive_primality_evidence import (
    convolutive_primality_context_for_query,
)


@pytest.mark.parametrize(
    ("k", "expected_sa", "expected_sb"),
    [(2, 1662, 3262), (3, 79824, 238746)],
)
def test_closed_form_sums_match_document_anchor_values(k, expected_sa, expected_sb):
    sum_a, sum_b = spectral_sums(k, 10)

    assert sum_a == Fraction(expected_sa)
    assert sum_b == Fraction(expected_sb)


@pytest.mark.parametrize(
    ("k", "branch", "digamma", "candidate_p"),
    [(2, "A(8)-", 1406, 29), (3, "A(8)-", 73263, 227)],
)
def test_unique_survivor_reconstructs_document_anchor(k, branch, digamma, candidate_p):
    result = digamma_savard_n10(k)

    assert result.status == "branche_unique"
    assert result.survivors == ((branch, candidate_p),)
    assert result.digamma == digamma
    assert result.candidate_p == candidate_p
    assert result.primality_proven is False


def test_multiple_survivors_are_reported_as_indeterminate():
    result = digamma_savard_n10(4)

    assert result.status == "indetermine"
    assert result.digamma is None
    assert result.candidate_p is None
    assert len(result.survivors) == 2


@pytest.mark.parametrize("k", [True, 1, 0, -2, 2.5])
def test_digamma_rejects_invalid_k(k):
    with pytest.raises(ValueError):
        digamma_savard_n10(k)


def test_digamma_reference_is_retrieved_only_for_related_questions():
    assert digamma_savard_context_for_query("Explique le Digamma Savard") 
    assert not digamma_savard_context_for_query("Bonjour, comment vas-tu?")


def test_llm_manager_has_semantic_memory_enabled():
    assert isinstance(llm_manager.INTEGRATEUR_MEMOIRE, IntegrateurMemoireGabriel)


def test_integrator_augments_question_with_bounded_digamma_reference():
    integrator = IntegrateurMemoireGabriel()
    prompt = (
        "PLAN COGNITIF\n"
        "QUESTION DE L'UTILISATEUR :\n"
        "Explique la fonction Digamma Savard et ses quatre branches.\n"
    )

    augmented = integrator.augmenter_prompt(prompt, domaine="spectral")

    assert "MÉMOIRE SÉMANTIQUE PERTINENTE" in augmented
    assert "k^5-k^3+k-1" in augmented
    assert "ne prouve pas" in augmented


def test_digamma_memory_remains_separate_from_convolutive_validation_memory():
    integrator = IntegrateurMemoireGabriel()

    augmented = integrator.augmenter_prompt(
        "QUESTION DE L'UTILISATEUR :\n"
        "Calcule le Digamma Savard pour k=2.\n",
        domaine="spectral",
    )

    assert "Digamma_Savard/Cline" in augmented
    assert "k^5-k^3+k-1" in augmented
    assert "6 849 579" not in augmented
    assert "Validation intégrale : NON" not in augmented


def test_integrator_retrieves_related_concepts_for_general_spectral_question():
    integrator = IntegrateurMemoireGabriel()
    prompt = (
        "QUESTION DE L'UTILISATEUR :\n"
        "Fais un résumé de la géométrie spectrale des nombres premiers.\n"
    )

    augmented = integrator.augmenter_prompt(prompt, domaine="spectral")

    assert "MÉMOIRE SÉMANTIQUE PERTINENTE" in augmented
    assert "réponse développée et structurée" in augmented


def test_integrator_does_not_inject_irrelevant_digamma_reference():
    integrator = IntegrateurMemoireGabriel()
    prompt = "QUESTION DE L'UTILISATEUR :\nBonjour.\n"

    augmented = integrator.augmenter_prompt(prompt)

    assert "Digamma_Savard/Cline" not in augmented


def test_convolutive_primality_report_is_retrieved_with_its_integrity_caveat():
    context = convolutive_primality_context_for_query(
        "Quel est le résultat du rapport de validation de primalité des ancrages?"
    )

    assert "6 849 579" in context
    assert "100.000000 %" in context
    assert "Validation intégrale : NON" in context
    assert "une ligne mal formée" in context
    assert "le résultat déclaré du rapport" in " ".join(context.split())


def test_integrator_injects_convolutive_evidence_only_for_related_questions():
    integrator = IntegrateurMemoireGabriel()
    prompt = (
        "QUESTION DE L'UTILISATEUR :\n"
        "Résume la validation de primalité des ancrages convolutifs.\n"
    )

    augmented = integrator.augmenter_prompt(prompt, domaine="spectral")

    assert "6 849 579" in augmented
    assert "PARI/GP isprime" in augmented
    assert "Validation intégrale : NON" in augmented

    unrelated = integrator.augmenter_prompt("QUESTION DE L'UTILISATEUR :\nBonjour.\n")
    assert "6 849 579" not in unrelated


def test_pipeline_facts_are_computed_only_when_question_supplies_k():
    facts = digamma_savard_facts_for_query("Explique le Digamma Savard pour k=2.")
    ambiguous = digamma_savard_facts_for_query("Le criblage Digamma du rapport 1/4?")

    assert facts is not None
    assert facts["status"] == "branche_unique"
    assert facts["somme_suite_A"] == 1662
    assert facts["somme_suite_B"] == 3262
    assert facts["Digamma_calcule"] == 1406
    assert facts["candidat_P"] == 29
    assert facts["preuve_de_primalite"] is False
    assert ambiguous is not None
    assert ambiguous["status"] == "indetermine"
    assert ambiguous["candidat_P"] is None
    assert digamma_savard_facts_for_query("Explique la fonction Digamma Savard.") is None


@pytest.mark.parametrize(
    ("question", "expected_status", "expected_values"),
    [
        ("Explique la fonction Digamma Savard pour k=2.", "branche_unique", ("1406", "29")),
        ("Explique le criblage Digamma du rapport 1/4.", "indetermine", ()),
    ],
)
def test_pipeline_returns_deterministic_digamma_report(
    question, expected_status, expected_values
):
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.pre_reasoner = PreReasoner()

    answer = asyncio.run(pipeline.process(question))
    facts = answer.structured_data["digamma_savard_cognitive"]

    assert facts["status"] == expected_status
    assert "Digamma_Savard/Cline" in answer.answer_text
    for value in expected_values:
        assert value in answer.answer_text
    if expected_status == "indetermine":
        assert "Aucun Digamma ni candidat P n'est sélectionné." in answer.answer_text
