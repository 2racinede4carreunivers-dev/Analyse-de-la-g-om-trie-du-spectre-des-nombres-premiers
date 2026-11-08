# -*- coding: utf-8 -*-
"""Tests de la couche reponse MULTI-RAPPORTS (src/core/multi_ratio_response.py).

Le module est charge PAR CHEMIN de fichier pour eviter src/core/__init__.py
(pydantic requis) : les tests tournent en local (sympy + pytest seuls) et
pareillement dans le conteneur.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "core" / "multi_ratio_response.py"
_spec = importlib.util.spec_from_file_location("multi_ratio_response", _MODULE_PATH)
mr = importlib.util.module_from_spec(_spec)
# dataclass() resout cls.__module__ via sys.modules -> enregistrer avant exec
import sys as _sys
_sys.modules.setdefault("multi_ratio_response", mr)
_spec.loader.exec_module(mr)


# --- Detection -------------------------------------------------------------

def test_detection_plage_simple():
    req = mr.detecter_requete_multi_rapports(
        "Reconstruis les rapports 1/2 a 1/111 pour n=10"
    )
    assert req is not None
    assert req.k_debut == 2 and req.k_fin == 111
    assert req.n == 10
    assert req.nb_rapports == 110
    assert req.source == "plage"


def test_detection_lots_multiples():
    req = mr.detecter_requete_multi_rapports(
        "lots de rapports : 1/2-1/10, 1/11-1/20 puis 1/21-1/30"
    )
    assert req is not None
    assert req.k_debut == 2 and req.k_fin == 30
    assert req.source == "lots"
    assert len(req.lots) == 3


def test_detection_liste_explicite():
    req = mr.detecter_requete_multi_rapports("liste des rapports 1/3, 1/5, 1/7 svp")
    assert req is not None
    assert req.liste_k == [3, 5, 7]
    assert req.source == "liste"


def test_detection_tous_les_rapports():
    req = mr.detecter_requete_multi_rapports("tous les rapports 1/k please")
    assert req is not None
    assert req.liste_k == list(range(2, 10))
    assert req.source == "tous"


def test_detection_k_plage():
    req = mr.detecter_requete_multi_rapports("reconstruits k=2..15 s'il te plait")
    assert req is not None
    assert req.k_debut == 2 and req.k_fin == 15


def test_pas_de_detection_mono_rapport():
    assert mr.detecter_requete_multi_rapports(
        "Reconstruis le 10e premier en rapport 1/2"
    ) is None


def test_pas_de_detection_hors_contexte():
    assert mr.detecter_requete_multi_rapports("calcule 1/2 - 1/3") is None


def test_detection_n_explicite():
    req = mr.detecter_requete_multi_rapports("rapports 1/2 a 1/5 avec n=12")
    assert req is not None
    assert req.n == 12


# --- Generation du tableau (deterministe) ----------------------------------

def test_generation_dispatcher_petite_plage():
    req = mr.detecter_requete_multi_rapports("reconstruis les rapports 1/2 a 1/6")
    texte, stats = mr.generer_tableau_multi_rapports(req, {"tableau_comparatif": True})
    assert "REQUETE MULTI-RATIO" in texte
    assert "1/2" in texte and "1/6" in texte
    assert "[PREMIER TROUVE]" in texte
    assert stats["multi_ratio_nb"] == 5
    assert stats["multi_ratio_succes"] >= 4
    assert stats["multi_ratio_source"] == "dispatcher" or stats[
        "multi_ratio_source"
    ].startswith("fichier:")


def test_generation_depuis_fichier_precalcule_si_disponible():
    req = mr.detecter_requete_multi_rapports("rapports 1/10 a 1/20 pour n=10")
    texte, stats = mr.generer_tableau_multi_rapports(req, {})
    if stats["multi_ratio_source"].startswith("fichier:"):
        assert "fichier precalcule" in texte
        assert "1/10" in texte and "1/20" in texte
    assert stats["multi_ratio_succes"] >= 0


def test_refus_plage_trop_large_sans_fichier():
    req = mr.RequeteMultiRapports(
        n=10, k_debut=900000, k_fin=900500,
        liste_k=list(range(900000, 900501)), lots=[(900000, 900500)],
        source="plage",
    )
    texte, stats = mr.generer_tableau_multi_rapports(
        req, {"max_k_calcul_direct": 100}
    )
    assert stats["multi_ratio_source"] == "refus"
    assert "Plage trop large" in texte
    assert "generer_reconstruction_1k.py" in texte


# --- Enrichissement de la reponse finale ----------------------------------

class _FakeAnswer:
    def __init__(self):
        self.answer_text = "Reponse LLM courte."
        self.structured_data = {"n": 10}


def test_enrichissement_idempotent():
    ans = _FakeAnswer()
    question = "Reconstruis les rapports 1/2 a 1/5 pour n=10"
    assert mr.enrichir_reponse_multi_rapports(question, ans, {}) is True
    assert mr.MARQUEUR_MULTI_RATIO in ans.answer_text
    assert "Reponse LLM courte." in ans.answer_text
    assert ans.structured_data["multi_ratio_nb"] == 4
    # marqueur deja present -> 2e appel sans effet
    assert mr.enrichir_reponse_multi_rapports(question, ans, {}) is False


def test_enrichissement_sans_requete_inchange():
    ans = _FakeAnswer()
    avant = ans.answer_text
    assert mr.enrichir_reponse_multi_rapports(
        "Explique la methode spectrale", ans, {}
    ) is False
    assert ans.answer_text == avant


def test_enrichissement_desactive():
    ans = _FakeAnswer()
    assert mr.enrichir_reponse_multi_rapports(
        "rapports 1/2 a 1/5", ans, {"enabled": False}
    ) is False
    assert mr.MARQUEUR_MULTI_RATIO not in ans.answer_text


# --- Consigne LLM : formulation PAR LOTS ----------------------------------

def test_consigne_prompt_par_lots():
    prompt = (
        "QUESTION DE L'UTILISATEUR :\n"
        "Reconstruis les rapports 1/2 a 1/111 pour n=10"
    )
    out = mr.consigne_prompt_multi_rapports(prompt)
    assert "[CONSIGNE MULTI-RAPPORTS]" in out
    assert "PAR LOTS" in out
    assert "1/2-1/11" in out
    assert "NE RESUME PAS" in out


def test_consigne_prompt_absente_sans_requete():
    prompt = "QUESTION DE L'UTILISATEUR :\nQu'est-ce que 2+2 ?"
    assert mr.consigne_prompt_multi_rapports(prompt) == prompt
