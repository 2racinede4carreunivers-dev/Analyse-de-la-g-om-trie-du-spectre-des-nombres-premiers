"""Tests du module de proposition d'amelioration (post-blocage du 8e moteur).

Charge `proposition_code.py` par chemin lorsque le paquet src.multiloop n'est
pas importable (httpx absent de l'environnement local) : les memes tests
s'executent dans le build complet et ici.

Couvre : le declencheur (il faut un BLOCAGE non resolu), le tirage des
propositions, le message en francais, et l'absence d'ecriture sur le depot.
"""
from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
CHEMIN = RACINE / "src" / "multiloop" / "raisonnement_recursif" / "proposition_code.py"


def _charger():
    """Import normal si possible, sinon chargement par chemin."""
    try:
        from src.multiloop.raisonnement_recursif import proposition_code as mod
        return mod
    except Exception:
        pass
    nom = "_gabriel_proposition_code_test"
    if nom in sys.modules:
        return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, CHEMIN)
    assert spec and spec.loader, "module proposition_code introuvable"
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


pc = _charger()


def _faux_resultat(**kwargs) -> types.SimpleNamespace:
    base = dict(
        declenche=True, blocage="Le depasse le perimetre de connaissance actuel.",
        reponse_modeste=None, citable=False, archive_id=42,
    )
    base.update(kwargs)
    return types.SimpleNamespace(**base)

# ── declencheur : la possibilite d'amelioration ──────────────────────────
def test_declencheur_exige_un_blocage_non_resolu():
    ok, raison = pc.evaluer_possibilite(_faux_resultat())
    assert ok and "blocage" in raison

    assert pc.evaluer_possibilite(_faux_resultat(declenche=False))[0] is False
    # Sans blocage, la requete est couverte : rien a ameliorer.
    ok_couvert, raison_couvert = pc.evaluer_possibilite(
        _faux_resultat(blocage="")
    )
    assert ok_couvert is False and "couverte" in raison_couvert

    # Un contexte de progression ne BLOQUE pas : l'oracle qui repond a la
    # question modeste ne resout pas la requete d'origine.
    ok_ctx, raison_ctx = pc.evaluer_possibilite(
        _faux_resultat(reponse_modeste="29", citable=True)
    )
    assert ok_ctx is True
    assert "question modeste resolue" in raison_ctx
    assert "timeline deja citable" in raison_ctx


def test_declencheur_respecte_le_kill_switch(monkeypatch):
    monkeypatch.setenv(pc.KILL_SWITCH, "0")
    assert pc.analyste_actif() is False
    ok, raison = pc.evaluer_possibilite(_faux_resultat())
    assert ok is False and pc.KILL_SWITCH in raison
    monkeypatch.delenv(pc.KILL_SWITCH)
    assert pc.analyste_actif() is True


def test_chargeur_analyste_exporte_le_pipeline():
    analyseur = pc.charger_analyste()
    assert analyseur is not None
    for attr in ("BanqueAnalyste", "construire_propositions", "contrat_pour",
                 "simuler", "RACINE"):
        assert hasattr(analyseur, attr), f"attribut absent : {attr}"
    assert pc.SCRIPT_ANALYSTE.name == "Gabriel_Dev_analyste_informatique.py"

# ── proposition de code ──────────────────────────────────────────────────
def test_proposition_code_accesseurs():
    note = pc.PropositionCode(
        categorie="marqueur_todo", fichier="a.py", titre="t", justification="j",
    )
    assert note.patchable is False and note.op == "—" and note.cible == "a.py"
    patch = pc.PropositionCode(
        categorie="test_manquant", fichier="src/a.py", titre="t", justification="j",
        operation={"op": "creer_fichier", "cible": "tests/test_a.py"},
        competences=["tests-logiciels"],
    )
    assert patch.patchable and patch.op == "creer_fichier"
    assert patch.cible == "tests/test_a.py"
    d = patch.to_dict()
    assert d["competences"] == ["tests-logiciels"] and d["patchable"] is True


def test_tirage_des_propositions_apres_blocage():
    analyseur = pc.charger_analyste()
    banque = analyseur.BanqueAnalyste(":memory:")
    banque.amorcer()
    devenir = pc.proposer_amelioration(
        "prouver l'exclusivite des nombres premiers par l'absurde",
        _faux_resultat(), plafond=4, banque=banque,
    )
    banque.fermer()

    assert devenir.declenche is True
    assert devenir.propositions, "aucune proposition malgre le blocage"
    assert all(isinstance(p, pc.PropositionCode) for p in devenir.propositions)
    assert devenir.message and "blocage" in devenir.message.lower()
    # Aucune ecriture : on insiste sur la garantie dans le message.
    assert "dépôt vivant intact" in devenir.message or "depot vivant intact" \
        in devenir.message
    # Les simulations restent en dry-run.
    for s in devenir.simulations:
        assert s.get("dry_run", True) is True
    assert devenir.to_dict()["simulations_propres"] == devenir.simulations_propres


def test_tirage_sans_blocage_ne_propose_rien():
    devenir = pc.proposer_amelioration(
        "x", _faux_resultat(blocage=""), plafond=3,
    )
    assert devenir.declenche is False
    assert devenir.propositions == [] and devenir.contrats == 0
    assert "Analyse du depot non declenchee" in devenir.message


def test_message_sans_proposition_est_propre():
    devenir = pc.DevenirCode(declenche=True, requete="x", raison="test")
    texte = pc.composer_message(devenir)
    assert "aucune" in texte.lower() or "n'a identifie" in texte
    assert pc.MESSAGE_BLOCAGE_REPERE


def test_resume_cinematique():
    devenir = pc.DevenirCode(
        declenche=True, requete="x",
        propositions=[pc.PropositionCode(
            categorie="import_mort", fichier="a.py", titre="t", justification="j",
            operation={"op": "supprimer_lignes"},
        )],
    )
    ev = pc.resume_cinematique(devenir)
    assert ev["step"] == "proposition_code"
    assert ev["propositions"] == 1 and ev["patchables"] == 1
    assert ev["categorie_principale"] == "import_mort"
