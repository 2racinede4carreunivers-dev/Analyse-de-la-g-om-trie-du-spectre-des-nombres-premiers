"""Tests du garde-fou REPONSE DIRECTE (aucun preambule redondant, sans exception)."""
from __future__ import annotations

import asyncio

import pytest

from src.spectral.direct_answer_guard import (
    DIRECT_ANSWER_RULES,
    is_non_answer,
    strip_meta_discourse,
)
from src.spectral.spectral_knowledge import build_grounded_system_prompt
from src.multiloop.pre_reasoner import _INSTANTANE_TEMPLATES


# Reponse exacte rapportee par Philippe (session du 2026-11-04)
REPONSE_SESSION = (
    "Bonjour! Je suis Gabriel, agent spécialisé dans la géométrie du spectre des "
    "nombres premiers de Philippe Thomas Savard. Je suis ici pour vous aider dans "
    "vos recherches sur cette théorie fascinante. Pourriez-vous me préciser sur "
    "quel rapport spectral vous souhaitez obtenir des informations? Je peux vous "
    "donner un résumé exhaustif des caractéristiques de la géométrie du spectre "
    "des nombres premiers et des deux piliers de cette géométrie, soit la session "
    "HOL/isabelle et le système convolutif concernant la reconstruction des "
    "nombres premiers et les rapports typiques et non-typiques."
)

CONTENU = (
    "La géométrie du spectre repose sur deux piliers. Le premier est la session "
    "HOL/Isabelle, qui prouve RsP = 1/2 pour la configuration 1*1. Le second est "
    "le système convolutif, qui reconstruit p = (SB(n) - digamma) / 64."
)


def test_reponse_de_la_session_est_une_non_reponse():
    assert is_non_answer(REPONSE_SESSION)
    assert strip_meta_discourse(REPONSE_SESSION) == ""


@pytest.mark.parametrize("preambule", [
    "Bonjour!",
    "Bonjour Philippe,",
    "Bonjour ! Je suis Gabriel, agente dédiée à la Méthode Spectrale.",
    "Je suis Gabriel.",
    "Je suis ici pour vous aider.",
    "Avec plaisir !",
    "Excellente question !",
    "Oui, je peux.",
    "Bien sûr.",
    "Je peux vous décrire les couleurs selon la toiture, les volets et le revêtement.",
    "Si vous le désirez, je peux vous donner un résumé exhaustif.",
    "Je serais ravie de vous répondre.",
    "Pourriez-vous me préciser quel rapport vous intéresse ?",
    "Sur quel rapport spectral souhaitez-vous des informations ?",
])
def test_preambule_retire_en_tete(preambule):
    assert strip_meta_discourse(preambule + " " + CONTENU) == CONTENU
    assert strip_meta_discourse(preambule + "\n\n" + CONTENU) == CONTENU


@pytest.mark.parametrize("offre", [
    "N'hésitez pas à me demander d'autres détails.",
    "Souhaitez-vous que je détaille la Section XIII ?",
    "Voulez-vous que je continue ?",
    "Je reste à votre disposition.",
])
def test_offre_finale_retiree(offre):
    assert strip_meta_discourse(CONTENU + "\n\n" + offre) == CONTENU


def test_cumul_preambule_et_offre():
    texte = REPONSE_SESSION + "\n\n" + CONTENU + "\n\nN'hésitez pas si vous voulez plus."
    assert strip_meta_discourse(texte) == CONTENU


def test_corps_de_reponse_jamais_modifie():
    # Une phrase "je peux" AU MILIEU du contenu n'est pas touchee.
    texte = (
        "Le rapport 1/2 est prouvé en Isabelle. Je peux reconstruire 29 avec n=10. "
        "Le facteur est 64."
    )
    assert strip_meta_discourse(texte) == texte


def test_contenu_markdown_et_decimaux_conserves():
    texte = "## Rapport typique\n- RsP = 0.5 (1/2)\n- n = 10 -> p = 29"
    assert strip_meta_discourse(texte) == texte
    assert not is_non_answer(texte)


def test_erreur_llm_preservee():
    err = "[ERREUR LLM] Tous les LLM indisponibles."
    assert strip_meta_discourse(err) == err
    assert not is_non_answer(err)


def test_regles_injectees_dans_le_prompt_systeme():
    prompt = build_grounded_system_prompt()
    assert DIRECT_ANSWER_RULES in prompt
    assert "REPONSE DIRECTE OBLIGATOIRE" in prompt
    # Plus aucun modele d'auto-presentation ni d'invitation a demander une precision
    assert "Je suis Gabriel, dedie" not in prompt
    assert "pouvez-vous preciser" not in prompt.lower()
    assert "pourriez-vous preciser" not in prompt.lower()


def test_gabarits_instantanes_sans_enumeration_ni_question():
    for _pattern, template in _INSTANTANE_TEMPLATES:
        assert "?" not in template, template
        assert "Je suis Gabriel" not in template, template
        assert "Astuce" not in template, template


# ---------------------------------------------------------------------------
# Integration RefinementLoop : regeneration si le LLM ne produit qu'un preambule
# ---------------------------------------------------------------------------
class _FakeLLM:
    def __init__(self, outputs):
        self.outputs = list(outputs)
        self.prompts: list[str] = []

    async def generate(self, prompt, system=None, temperature=None, include_conversation=False):
        self.prompts.append(prompt)
        return self.outputs.pop(0)


class _Ctx:
    question_id = "t1"
    raw_question = (
        "Peux-tu générer un résumé exhaustif des caractéristiques de la géométrie "
        "du spectre des nombres premiers ?"
    )


def _run_loop(outputs):
    from src.multiloop.refinement_loop import RefinementLoop

    llm = _FakeLLM(outputs)
    loop = RefinementLoop(llm, critic=None, config={"multiloop": {"max_iterations": 1}})
    final = asyncio.run(
        loop.run(_Ctx(), None, None, max_iterations_override=1,
                 num_candidates_override=1, skip_critique=True)
    )
    return llm, final


def test_refinement_regenere_quand_preambule_seul():
    llm, final = _run_loop([REPONSE_SESSION, "Bonjour ! " + CONTENU])
    assert len(llm.prompts) == 2
    assert "AUCUN contenu" in llm.prompts[1]
    assert final.answer_text == CONTENU


def test_refinement_nettoie_sans_regenerer_si_contenu_present():
    llm, final = _run_loop(["Bonjour Philippe ! Je suis Gabriel. " + CONTENU])
    assert len(llm.prompts) == 1
    assert final.answer_text == CONTENU
    assert "Commence directement par le contenu demande" in llm.prompts[0]
