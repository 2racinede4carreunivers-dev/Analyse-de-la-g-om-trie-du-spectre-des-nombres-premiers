"""Tests de Gabriel_Dev_analyste_informatique (banque + auto-analyse + patches).

Le script est a la racine du depot et N'EST PAS un paquet : on le charge par
chemin via importlib. Ce choix garde les tests executables y dans
l'environnement local restreint (httpx/sympy absents).

Couvre : integrite du corpus, index/schema neuronal, kill-switch, detection
statique (docstring / import mort / TODO en commentaire uniquement), contrats
de patch au format variateur, et l'absence d'ecriture sur le depot vivant.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
CHEMIN = RACINE / "Gabriel_Dev_analyste_informatique.py"

_NOM = "_gabriel_dev_analyste_test"
if _NOM in sys.modules:
    gab = sys.modules[_NOM]
else:
    _spec = importlib.util.spec_from_file_location(_NOM, CHEMIN)
    assert _spec and _spec.loader, "script d'analyste introuvable"
    gab = importlib.util.module_from_spec(_spec)
    sys.modules[_NOM] = gab
    _spec.loader.exec_module(gab)


# ── banque / corpus ──────────────────────────────────────────────────────
def test_corpus_sans_doublon_ni_cible_morte():
    cles = [e[0] for e in gab.CORPUS]
    assert len(cles) == len(set(cles)), "cle de noeud dupliquee"
    manquantes = {
        cible for *_, liens in gab.CORPUS for cible, _ in liens
    } - set(cles)
    assert not manquantes, f"liens vers noeuds inexistants : {sorted(manquantes)}"


def test_schema_cinq_tables(tmp_path):
    banque = gab.BanqueAnalyste(tmp_path / "b.db")
    with banque._conn() as conn:
        tables = {
            r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
    assert {"noeuds", "liens", "index_termes", "propositions",
            "telechargements"} <= tables


def test_amorcage_idempotent():
    banque = gab.BanqueAnalyste(":memory:")
    n1 = banque.amorcer()
    stats_avant = banque.stats()
    banque.amorcer()
    assert banque.stats() == stats_avant, "amorcage non idempotent"
    assert stats_avant["noeuds"] >= n1
    assert stats_avant["liens"] > 0
    assert stats_avant["termes"] > 100
    banque.fermer()


def test_recherche_et_cone_de_voisinage():
    banque = gab.BanqueAnalyste(":memory:")
    banque.amorcer()
    res = banque.rechercher("preuve par l'absurde des nombres premiers")
    assert res, "recherche vide"
    assert {r["cle"] for r in res} & {
        "preuve-par-absurde", "nombres-premiers", "theorie-des-nombres",
    }
    voisins = banque.voisins("nombres-premiers")
    assert voisins
    assert all(v["relation"] in gab.RELATIONS_VALIDES for v in voisins)
    trace = banque.tracer_voisinage("spectre-geometrique", profondeur=2)
    assert trace and all("voisins" in n for n in trace)
    banque.fermer()


def test_liens_refuse_relation_inconnue_et_boucle():
    banque = gab.BanqueAnalyste(":memory:")
    banque.amorcer()
    a = banque.noeud("nombres-premiers").id
    b = banque.noeud("logique-fol").id
    assert banque.lier(a, b, "relation-inventee") is False
    assert banque.lier(a, a, "utilise") is False
    assert banque.lier(a, b, "utilise") is True
    assert banque.lier(a, b, "utilise") is False, "doublon non refuse"
    banque.fermer()

# ── kill-switch ──────────────────────────────────────────────────────────
def test_kill_switch_coup_tout(monkeypatch):
    monkeypatch.setenv(gab.KILL_SWITCH, "0")
    assert gab.actif() is False
    assert gab.construire_propositions(
        gab.BanqueAnalyste(":memory:"), "x"
    ) == []
    monkeypatch.delenv(gab.KILL_SWITCH)
    assert gab.actif() is True


# ── analyse statique ─────────────────────────────────────────────────────
def test_analyse_detecte_doc_import_mort_et_todo_commentaire(tmp_path):
    source = tmp_path / "mod.py"
    source.write_text(
        "import math\n"
        "import json\n"
        "\n"
        "# TODO: completer ce module\n"
        "TEXT = \"le TODO n est pas un chantier\"\n"
        "\n"
        "def f():\n"
        "    return json.dumps(1)\n",
        encoding="utf-8",
    )
    res = gab.analyser_fichier(source)
    assert res["parseable"] and res["doc_module"] is False
    assert [i["nom"] for i in res["imports_morts"]] == ["math"]
    # Le TODO de la chaine ne compte PAS : seul le commentaire est retenu.
    assert [t["ligne"] for t in res["todos"]] == [4]
    assert res["fonctions_sans_doc"] == [{"nom": "f", "ligne": 7}]


def test_suppression_valide_rejette_import_multi_lignes():
    texte = "from a import (\n    x,\n    y,\n)\nprint(x, y)\n"
    assert gab._suppression_valide(texte, 1) is False
    assert gab._suppression_valide("import math\nprint(1)\n", 1) is True
    assert gab._suppression_valide("print(1)\n", 1) is False  # pas un import


def test_parcourir_py_exclut_le_dossier_data():
    cibles = gab.parcourir_py(gab.RACINE)
    assert cibles
    assert not any("data" in p.relative_to(gab.RACINE).parts for p in cibles)
    assert not any(".venv" in p.relative_to(gab.RACINE).parts for p in cibles)


def test_extraction_html_ignore_les_scripts():
    brut = "<html><head><style>x{}</style></head><body><p>Algorithme " \
           "spectral</p><script>alert(1)</script></body></html>"
    texte = gab.html_vers_texte(brut)
    assert "Algorithme spectral" in texte
    assert "alert" not in texte
    assert "x{}" not in texte


# ── contrats + sandbox ───────────────────────────────────────────────────
def test_contrat_au_format_variateur():
    p = gab.PropositionAnalyste(
        categorie="test_manquant", fichier="src/x.py", titre="t", justification="j",
        operation={"op": "creer_fichier", "cible": "tests/test_x.py",
                   "contenu": "def test_ok():\n    assert True\n"},
    )
    contrat = gab.contrat_pour(p, "requete spectrale")
    assert set(contrat) == {"meta", "operations"}
    assert contrat["operations"] == [p.operation]
    assert contrat["meta"]["role"] == "dev-analyste"
    assert gab.contrat_pour(
        gab.PropositionAnalyste(
            categorie="marqueur_todo", fichier="a.py", titre="t", justification="j",
        ), "x"
    ) is None


def test_test_propose_est_compilable():
    code = gab._test_propose("mon_module")
    compile(code, "test_propose.py", "exec")
    assert "def test_mon_module_parseable()" in code


def test_simulation_ecrit_uniquement_dans_la_sandbox(tmp_path):
    depot = tmp_path / "depot"
    (depot / "src").mkdir(parents=True)
    cible = depot / "src" / "mod.py"
    cible.write_text("import math\nprint(1)\n", encoding="utf-8")
    avant = cible.read_bytes()

    banque = gab.BanqueAnalyste(tmp_path / "b.db")
    banque.amorcer()
    rapport = gab.analyser(
        "tests et documentation du code", banque=banque, racine=depot,
        plafond=20, journal=False,
    )
    assert not rapport["erreurs"], rapport["erreurs"]
    # Depot vivant strictement intact.
    assert cible.read_bytes() == avant
    assert sorted(p.name for p in depot.rglob("*")) == ["mod.py", "src"]
    # Les simulations ont bien porte sur des contrats.
    s0 = rapport["simulations"][0] if rapport["simulations"] else {}
    if s0.get("statut") != "indisponible":
        assert rapport["contrats"] == len(rapport["simulations"])
    for s in rapport["simulations"]:
        assert s.get("echouees", 0) == 0, s.get("defaillances")
    banque.fermer()


def test_analyser_respecte_le_kill_switch(tmp_path, monkeypatch):
    monkeypatch.setenv(gab.KILL_SWITCH, "0")
    banque = gab.BanqueAnalyste(tmp_path / "b.db")
    rapport = gab.analyser("x", banque=banque, journal=False)
    assert rapport["actif"] is False
    assert rapport["propositions"] == []
    assert "GABRIEL_DEV_ANALYSTE" in rapport["annule"]
    banque.fermer()


def test_resume_texte_est_lisible():
    banque = gab.BanqueAnalyste(":memory:")
    banque.amorcer()
    rapport = gab.analyser(
        "documentation et tests du depot", banque=banque, plafond=3, journal=False,
    )
    texte = gab.resume_texte(rapport)
    assert "[analyste]" in texte and "proposition" in texte
    banque.fermer()


def test_coherence_entre_connaissance_et_proposition():
    """Chaque categorie emporte des competences referencables dans la banque."""
    banque = gab.BanqueAnalyste(":memory:")
    banque.amorcer()
    for categorie, cles in gab.LIAISON_CONNAISSANCE.items():
        assert categorie and cles
        for cle in cles:
            assert banque.noeud(cle) is not None, f"noeud absent : {cle}"
    banque.fermer()
