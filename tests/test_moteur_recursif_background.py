"""Tests du 8e moteur (arriere-plan) : raisonnement recursif.

Couvre : decomposition lexicale, generation de question modeste, oracle numerique
(repli local), archivage des timelines (preuves citables) et la boucle du moteur.
"""
from __future__ import annotations

from src.multiloop.raisonnement_recursif import (
    MESSAGE_AUTOPROGRAMMATION,
    ArchiveurTimeline,
    MoteurRecursifBackground,
    OracleNumerique,
    analyser,
    construire_questions_modestes,
    meilleure_question_modeste,
)

REQUETE = (
    "Comment reconstruire le 137ieme nombre premier avec la methode spectrale "
    "et le rapport 1/2 ?"
)


def test_message_autoprogrammation_exact():
    assert MESSAGE_AUTOPROGRAMMATION == (
        "Cline s'occupe de s'oblige à sa fiancée, Mm. Gabriel s'auto programme "
        "pour une mise à jour conforme aux exigeances de la requête."
    )


def test_decomposeur_lexical():
    analyse = analyser(REQUETE)
    assert len(analyse.divisions) >= 1
    assert len(analyse.tokens) > 3
    assert "137" in analyse.nombres
    # au moins une ancre du sujet spectral
    assert analyse.ancres, "aucune ancre spectrale detectee"
    assert analyse.couverture > 0


def test_generateur_question_modeste():
    analyse = analyser(REQUETE)
    questions = construire_questions_modestes(analyse)
    assert questions
    best = meilleure_question_modeste(analyse)
    assert isinstance(best, str) and best


def test_oracle_repli_local():
    oracle = OracleNumerique()
    assert oracle._est_premier(137) is True
    assert oracle._est_premier(138) is False
    assert oracle._nieme_premier(10) == 29
    res = oracle.interroger_sync("quel est le 137e nombre premier ?")
    assert res.outcome in ("verified", "inconclusive", "indisponible")


def test_archiveur_timeline(tmp_path):
    arch = ArchiveurTimeline(tmp_path / "tl.db")
    qid = arch.archiver(
        requete=REQUETE, question_modeste="Quel est le 137e premier ?",
        reponse="773", divisions=["a", "b"], ancres=["premier"], resolue=True,
    )
    assert qid > 0
    assert arch.statistiques()["resolues"] >= 1
    assert arch.rechercher(["premier"]) != []

    qid2 = arch.archiver(
        requete="question floue", question_modeste="Qu'est-ce que le spectre ?",
        reponse=None, blocage="manque", resolue=False,
    )
    assert any(x["id"] == qid2 for x in arch.lister_non_resolues())
    arch.marquer_resolue(qid2, "resolue plus tard")
    assert arch.statistiques()["citables"] >= 2


def test_engine_traiter(tmp_path):
    arch = ArchiveurTimeline(tmp_path / "tl.db")
    moteur = MoteurRecursifBackground(archiveur=arch, oracle=OracleNumerique())
    res = moteur.traiter(REQUETE, reponse=None, session_id="pytest")
    assert res.declenche is True
    assert res.message == MESSAGE_AUTOPROGRAMMATION
    assert res.divisions
    assert res.question_modeste
    assert isinstance(res.oracle, dict) and "outcome" in res.oracle
    assert len(res.blocage) > 20
    assert res.archive_id is not None
    d = res.to_dict()
    assert d["requete"] == REQUETE
    assert "total" in moteur.statistiques()