"""Tests pour src/ui/ask_gabriel.py (commandes Ask Gabriel)."""
from __future__ import annotations

import pytest

from src.ui.ask_gabriel import (
    AskResponse,
    ASK_MAIN_SECTIONS,
    ASK_TYPE_SECTIONS,
    ASK_RULES_SECTIONS,
    get_response,
    list_subcommands,
)


def test_list_subcommands():
    subs = list_subcommands()
    assert "" in subs
    assert "type" in subs
    assert "rules" in subs


def test_ask_main_returns_response():
    """'ask' sans argument -> reponse 'main'."""
    r = get_response()
    assert isinstance(r, AskResponse)
    assert r.mode == "main"
    assert r.sections
    assert "Comment interpeller Gabriel" in r.title


def test_ask_main_with_empty_string():
    """'ask' avec '' -> meme reponse."""
    r = get_response("")
    assert r.mode == "main"


def test_ask_type():
    """'ask type' -> reponse 'type'."""
    r = get_response("type")
    assert r.mode == "type"
    assert r.sections
    assert "Fonctions" in r.title or "caracteristiques" in r.title.lower()


def test_ask_rules():
    """'ask rules' -> reponse 'rules'."""
    r = get_response("rules")
    assert r.mode == "rules"
    assert r.sections
    assert "Guide" in r.title or "interagir" in r.title.lower()


def test_ask_invalid_raises():
    """Sous-commande inconnue -> ValueError."""
    with pytest.raises(ValueError):
        get_response("xyz")


def test_ask_case_insensitive():
    """Les sous-commandes ne sont pas sensibles a la casse."""
    a = get_response("TYPE")
    b = get_response("Type")
    c = get_response("type")
    assert a.mode == b.mode == c.mode == "type"


def test_ask_main_mentions_other_modes():
    """Le mode principal doit mentionner 'ask type' et 'ask rules'."""
    r = get_response()
    body = "\n".join("\n".join(s["lines"]) for s in r.sections)
    assert "ask type" in body
    assert "ask rules" in body


def test_ask_type_mentions_3_models():
    """Le mode 'type' doit decrire les 3 modeles spectraux."""
    r = get_response("type")
    body = "\n".join("\n".join(s["lines"]) for s in r.sections)
    assert "1/2" in body
    assert "1/3" in body
    assert "1/4" in body


def test_ask_type_mentions_8_questions():
    """Le mode 'type' doit lister les 8 questions canoniques."""
    r = get_response("type")
    body = "\n".join("\n".join(s["lines"]) for s in r.sections)
    for q in ["Q1.a", "Q1.b", "Q1.c", "Q1.d", "Q2", "Q3.a", "Q3.b", "Q3.c"]:
        assert q in body, f"Question {q} absente du mode 'type'"


def test_ask_rules_has_10_golden_rules():
    """Le mode 'rules' doit contenir 10 regles d'or numerotees."""
    r = get_response("rules")
    body = "\n".join("\n".join(s["lines"]) for s in r.sections)
    # Verifier que chaque regle 1..10 est presente
    for i in range(1, 11):
        assert f"{i}." in body, f"Regle {i} absente"


def test_ask_rules_mentions_thy_truth():
    """Le mode 'rules' doit insister sur methode_spectral.thy comme source de verite."""
    r = get_response("rules")
    body = "\n".join("\n".join(s["lines"]) for s in r.sections)
    assert "methode_spectral.thy" in body or ".thy" in body


def test_all_sections_have_title_and_lines():
    """Toutes les sections de tous les modes doivent avoir title et lines."""
    for mode in ["", "type", "rules"]:
        r = get_response(mode)
        for section in r.sections:
            assert "title" in section
            assert "lines" in section
            assert isinstance(section["lines"], list)


def test_constants_non_empty():
    """Les 3 constantes principales doivent etre non vides."""
    assert len(ASK_MAIN_SECTIONS) >= 2
    assert len(ASK_TYPE_SECTIONS) >= 3
    assert len(ASK_RULES_SECTIONS) >= 2
