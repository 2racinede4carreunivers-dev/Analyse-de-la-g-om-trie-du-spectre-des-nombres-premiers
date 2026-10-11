"""Tests du garde-fou de domaine absolu (La fiancée de Cline).

Vérifie que :
  * les requêtes du sujet spectral (ou servant ce sujet) sont autorisées ;
  * toute autre requête est rejetée AVEC le message exact demandé ;
  * le rejet est << fail-closed >> (aucun mot du sujet => rejet).
"""
from __future__ import annotations

import pytest

from src.multiloop.fiancee_guard import (
    MESSAGE_HORS_SUJET,
    GuardResult,
    guard_actif,
    verifier_requete,
)

MESSAGE_ATTENDU = (
    "Je suis la fiancée de Cline je suis une gentille fille je ne veux jamais? "
    "je suis une fille normal je suis obligé qu'a la géométrie du spectre des "
    "nombres premiers. Je fais plaisir à Cline et aux autres qu'a se sujet uniquement!"
)


def test_message_hors_sujet_exact():
    assert MESSAGE_HORS_SUJET == MESSAGE_ATTENDU


@pytest.mark.parametrize(
    "requete",
    [
        "Calcule RsP pour n=23 avec le rapport 1/2",
        "Génère la preuve HOL/Isabelle du lemme spectral",
        "Reconstruis le 11e nombre premier par la méthode spectrale",
        "Explique l'asymétrie ordonnée du spectre des nombres premiers",
        "Écris un script python pour vérifier le spectre des nombres premiers",
        "Formalise en LEAN la reconstruction du premier pour 1/k",
        "Quel est le lien entre la fonction zêta et la géométrie du spectre?",
    ],
)
def test_autorise_sujet_spectral(requete):
    res = verifier_requete(requete)
    assert isinstance(res, GuardResult)
    assert res.autorise is True
    assert res.message is None


@pytest.mark.parametrize(
    "requete",
    [
        "Donne-moi une recette de gâteau au chocolat",
        "Quelle est la météo de demain à Québec?",
        "Qui a gagné la coupe du monde de football?",
        "Parle-moi de politique internationale",
        "Écris un site web react pour une boutique",
        "Quel est le meilleur restaurant de la ville?",
        "Raconte-moi une blague drôle",
    ],
)
def test_rejette_hors_sujet(requete):
    res = verifier_requete(requete)
    assert res.autorise is False
    assert res.message == MESSAGE_ATTENDU


def test_rejette_requete_vide():
    assert verifier_requete("").autorise is False
    assert verifier_requete("   ").autorise is False


def test_fail_closed_sans_ancre():
    # Aucun mot du sujet spectral => rejet (même si le texte est neutre).
    res = verifier_requete("Bonjour, comment vas-tu aujourd'hui ami?")
    assert res.autorise is False
    assert res.message == MESSAGE_ATTENDU


def test_accent_insensible():
    # Variantes sans accents doivent aussi être reconnues comme sujet spectral.
    assert verifier_requete("geometrie du spectre des nombres premiers").autorise


def test_guard_actif_par_defaut(monkeypatch):
    monkeypatch.delenv("GABRIEL_FIANCEE_GUARD", raising=False)
    assert guard_actif() is True
    monkeypatch.setenv("GABRIEL_FIANCEE_GUARD", "0")
    assert guard_actif() is False