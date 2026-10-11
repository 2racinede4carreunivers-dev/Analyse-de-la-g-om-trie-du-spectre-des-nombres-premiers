"""Tests du raisonnement recursif (auto-programmation sandboxee).

Vérifie :
  * le moteur sandbox applique en dry-run sans écrire ;
  * l'écriture réelle reste confinée à la sandbox + snapshot + rollback ;
  * la vérification de syntaxe bloque les patches invalides ;
  * le détecteur de manque et la boucle encadrée (désactivée par défaut).
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from src.multiloop.raisonnement_recursif import (
    MESSAGE_AUTOPROGRAMMATION,
    PipelineAutoProgrammation,
    VariateurSandboxError,
    construire_contrat_squelette,
    detecter_manque,
    tenter_raisonnement_recursif,
)

MESSAGE_AUTO_ATTENDU = (
    "Cline s'occupe de s'oblige à sa fiancée, Mm. Gabriel s'auto programme "
    "pour une mise à jour conforme aux exigeances de la requête."
)


def test_message_autoprogrammation_exact():
    assert MESSAGE_AUTOPROGRAMMATION == MESSAGE_AUTO_ATTENDU


def test_dry_run_n_ecrit_pas(tmp_path):
    moteur = PipelineAutoProgrammation(tmp_path, dry_run=True)
    contrat = construire_contrat_squelette(
        "spectral", ["spectre"],
        {"op": "creer_fichier", "cible": "t.py", "contenu": "x = 1\n"},
    )
    rapport = moteur.appliquer_contrat(contrat)
    assert rapport["dry_run"] is True
    assert rapport["simules"] == 1
    assert rapport["echouees"] == 0
    assert not (tmp_path / "t.py").exists()


def test_ecriture_sandbox_snapshot_rollback(tmp_path):
    # 1. création réelle dans la sandbox
    moteur = PipelineAutoProgrammation(tmp_path, dry_run=False)
    c1 = construire_contrat_squelette(
        "spectral", ["spectre"],
        {"op": "creer_fichier", "cible": "t.py", "contenu": "x = 1\n"},
    )
    r1 = moteur.appliquer_contrat(c1)
    assert (tmp_path / "t.py").exists()
    assert r1["snapshot"]

    # 2. modification
    c2 = construire_contrat_squelette(
        "spectral", ["spectre"],
        {"op": "remplacer_texte", "cible": "t.py",
         "ancien_texte": "x = 1", "nouveau_texte": "x = 2"},
    )
    r2 = moteur.appliquer_contrat(c2)
    assert "x = 2" in (tmp_path / "t.py").read_text(encoding="utf-8")

    # 3. rollback restaure l'état précédent
    moteur.rollback(r2["snapshot"])
    assert "x = 1" in (tmp_path / "t.py").read_text(encoding="utf-8")


def test_operation_inconnue_rejetee(tmp_path):
    moteur = PipelineAutoProgrammation(tmp_path, dry_run=True)
    contrat = construire_contrat_squelette(
        "spectral", ["spectre"],
        {"op": "executer_python", "contenu": "print('x')"},
    )
    rapport = moteur.appliquer_contrat(contrat)
    assert rapport["echouees"] == 1
    assert rapport["defaillances"][0]["type"] == "executer_python"


def test_verification_syntaxe_python(tmp_path):
    moteur = PipelineAutoProgrammation(tmp_path, dry_run=True)
    contrat = construire_contrat_squelette(
        "spectral", ["spectre"],
        {"op": "creer_fichier", "cible": "bad.py", "contenu": "def (: pass\n"},
    )
    rapport = moteur.appliquer_contrat(contrat)
    assert rapport["echouees"] == 1


def test_confinement_sandbox(tmp_path):
    """Une cible absolue (hors sandbox) est re-racinee : rien n'est écrit dehors."""
    moteur = PipelineAutoProgrammation(tmp_path, dry_run=False)
    contrat = construire_contrat_squelette(
        "spectral", ["x"],
        {"op": "creer_fichier", "cible": str(tmp_path.parent / "evil_out.py"), "contenu": "y = 1\n"},
    )
    moteur.appliquer_contrat(contrat)
    assert not (tmp_path.parent / "evil_out.py").exists()


def test_detecteur_manque():
    assert detecter_manque("").manque is True
    assert detecter_manque("je ne sais pas répondre").manque is True
    assert detecter_manque("Voici la preuve du lemme spectral RsP.").manque is False


def test_recursif_desactive_par_defaut(monkeypatch):
    monkeypatch.delenv("GABRIEL_RECURSIVE", raising=False)
    res = tenter_raisonnement_recursif("spectre", "je ne sais pas")
    assert res is not None
    assert "desactive" in res["etat"]


def test_recursif_active_dry_run(tmp_path, monkeypatch):
    monkeypatch.setenv("GABRIEL_RECURSIVE", "1")
    monkeypatch.delenv("GABRIEL_RECURSIVE_APPLY", raising=False)
    res = tenter_raisonnement_recursif(
        "reconstruis le premier pour le spectre", "je ne sais pas",
        sandbox_root=str(tmp_path),
    )
    assert res is not None
    assert res["message"] == MESSAGE_AUTOPROGRAMMATION
    assert res["rapport"]["simules"] == 1


def test_cible_hors_sandbox_leve_erreur(tmp_path):
    moteur = PipelineAutoProgrammation(tmp_path, dry_run=False)
    # Un chemin relatif qui s'échappe de la sandbox est refusé.
    with pytest.raises(VariateurSandboxError):
        moteur._resoudre("../evil_escape.py")