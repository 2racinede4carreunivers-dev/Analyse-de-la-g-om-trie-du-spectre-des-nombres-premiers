"""Tests du pipeline de production du rapport présentenciel (.tex).

Exécution :
    python -m pytest tests/test_pipeline_rapport_presentenciel.py
    python tests/test_pipeline_rapport_presentenciel.py   # sans pytest
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import pipeline_rapport_presentenciel as pipe  # noqa: E402


def _base_temporaire():
    dossier = tempfile.TemporaryDirectory()
    conn = pipe.ouvrir_base(Path(dossier.name) / "test.db")
    pipe.semer(conn)
    return dossier, conn


def test_recevabilite_non_coupable_sous_reserve() -> None:
    dossier, conn = _base_temporaire()
    try:
        decision = pipe.evaluer_recevabilite(conn, "non_coupable")
        assert decision.conclusion == "SOUS_RESERVE_VERDICT"
        assert decision.recu is True
        assert decision.regle_code == "R_NON_COUPABLE"
        assert "sous réserve" in decision.titre_document
        assert "721 (1)" in decision.motifs[0]
        assert len(decision.chemin) >= 5
        assert decision.demandes
    finally:
        conn.close()
        dossier.cleanup()


def test_recevabilite_coupable_immediate() -> None:
    dossier, conn = _base_temporaire()
    try:
        decision = pipe.evaluer_recevabilite(conn, "coupable")
        assert decision.conclusion == "IMMEDIATE"
        assert decision.recu is True
        assert decision.regle_code == "R_COUPABLE"
        assert decision.demandes
    finally:
        conn.close()
        dossier.cleanup()


def test_recevabilite_acquittement_impossible() -> None:
    dossier, conn = _base_temporaire()
    try:
        decision = pipe.evaluer_recevabilite(conn, "acquittement")
        assert decision.conclusion == "IMPOSSIBLE"
        assert decision.recu is False
        assert decision.demandes == []
    finally:
        conn.close()
        dossier.cleanup()


def test_plaidoyer_inconnu_rejete() -> None:
    dossier, conn = _base_temporaire()
    try:
        try:
            pipe.evaluer_recevabilite(conn, "autre")
        except ValueError:
            pass
        else:  # pragma: no cover - le levé est attendu
            raise AssertionError("ValueError attendu pour un plaidoyer inconnu")
    finally:
        conn.close()
        dossier.cleanup()


def test_graphe_complet() -> None:
    dossier, conn = _base_temporaire()
    try:
        comptes = {
            table: conn.execute(
                f"SELECT COUNT(*) FROM {table}"  # noqa: S608
            ).fetchone()[0]
            for table in ("source", "noeud", "lien", "regle", "section",
                          "section_decision")
        }
        assert comptes["source"] >= 10
        assert comptes["noeud"] >= 19
        assert comptes["lien"] >= 25
        assert comptes["regle"] == 3
        assert comptes["section"] == 7
        assert comptes["section_decision"] == 20
    finally:
        conn.close()
        dossier.cleanup()


def test_propagation_atteint_les_sections() -> None:
    dossier, conn = _base_temporaire()
    try:
        activation = pipe.propager(conn, "dec_sous_reserve")
        assert activation["dec_sous_reserve"] == 1.0
        assert any(code.startswith("sec_") for code in activation)
        assert activation.get("sec_analyse", 0.0) > 0.0
    finally:
        conn.close()
        dossier.cleanup()


def test_echapper_latex_caracteres_reserves() -> None:
    assert pipe.echapper_latex("a_b") == "a\\_b"
    assert pipe.echapper_latex("100%") == "100\\%"
    assert pipe.echapper_latex("a & b") == "a \\& b"
    assert pipe.echapper_latex("coût $5") == "coût \\$5"
    assert pipe.echapper_latex("n#1") == "n\\#1"


def test_lire_extrait_ignore_les_commentaires() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "extrait.tex"
        chemin.write_text(
            "% consigne : utiliser \\section*{...}\n"
            "\\section*{Faits}\n"
            "Les faits.\n",
            encoding="utf-8",
        )
        blocs = pipe.lire_extrait(chemin)
        assert len(blocs) == 1
        assert blocs[0][0] == "Faits"
        assert blocs[0][1] == "Les faits."


def test_generation_tex_valide() -> None:
    dossier, conn = _base_temporaire()
    sortie_dossier = tempfile.TemporaryDirectory()
    try:
        extrait = Path(sortie_dossier.name) / "extrait.tex"
        extrait.write_text(
            "\\section*{Faits}\nFait contesté par la défense.\n",
            encoding="utf-8",
        )
        ctx = pipe.Contexte(plaidoyer="non_coupable")
        decision = pipe.evaluer_recevabilite(conn, "non_coupable")
        blocs = pipe.lire_extrait(extrait)
        tex = pipe.generer_tex(
            conn, ctx, decision, blocs,
            Path(sortie_dossier.name) / "rapport.tex",
        )
        validation = pipe.valider_tex(tex, ctx, decision)
        assert validation["ok"], validation["erreurs"]
        assert validation["accolades_ecart"] == 0
        texte = tex.read_text(encoding="utf-8")
        assert r"\begin{document}" in texte
        assert r"\end{document}" in texte
        assert "721 (1)" in texte
        assert "23 octobre 2026" in texte
        assert "9 h 30" in texte
        assert "salle 2.15" in texte
        assert decision.titre_document in texte
        assert "Fait contesté par la défense." in texte
        assert r"\section{Faits allégués}" in texte
    finally:
        conn.close()
        dossier.cleanup()
        sortie_dossier.cleanup()


def test_document_acquittement_sans_section_demandes() -> None:
    dossier, conn = _base_temporaire()
    sortie_dossier = tempfile.TemporaryDirectory()
    try:
        ctx = pipe.Contexte(plaidoyer="acquittement")
        decision = pipe.evaluer_recevabilite(conn, "acquittement")
        tex = pipe.generer_tex(
            conn, ctx, decision, [],
            Path(sortie_dossier.name) / "rapport.tex",
        )
        texte = tex.read_text(encoding="utf-8")
        assert r"\section{Demandes}" not in texte
        validation = pipe.valider_tex(tex, ctx, decision)
        assert validation["ok"], validation["erreurs"]
    finally:
        conn.close()
        dossier.cleanup()
        sortie_dossier.cleanup()


if __name__ == "__main__":
    tests = [
        (nom, obj)
        for nom, obj in sorted(globals().items())
        if nom.startswith("test_") and callable(obj)
    ]
    echec = 0
    for nom, fonction in tests:
        try:
            fonction()
            print(f"OK   {nom}")
        except AssertionError as exc:
            echec += 1
            print(f"FAIL {nom} : {exc}")
    print(f"\n{len(tests) - echec}/{len(tests)} tests réussis")
    raise SystemExit(1 if echec else 0)

