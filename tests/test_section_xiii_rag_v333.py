"""
Tests v3.33 (Philippe 2026-06) - Apprentissage de la Section XIII par Gabriel.

Valide :
  1. Le module memoire `memory/methode_spectral_section_XIII.py` :
     regles RAG, helpers psi_savard, 4 validations canoniques exactes.
  2. Le nouveau regime `regime_pont_savard` dans le Dictionnaire Spectral
     (13e regime) : lemmes certifies, definitions HOL, nomenclature.
  3. La detection automatique par l'AdaptateurCognitifSpectral : les
     requetes sur Tchebychev / zeta / Riemann / psi_savard declenchent
     l'injection du contexte Pont Savard dans le prompt LLM.
  4. L'IntegrateurMemoireGabriel charge la section XIII (sections_extra).
"""
from __future__ import annotations

import math

import pytest

from memory.dictionnaire_spectral import (
    DICTIONNAIRE_SPECTRAL,
    get_regime,
    regime_count,
    total_lemmes,
)
from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral
from memory.methode_spectral_section_XIII import (
    ENSEMBLE_STRUCTURE,
    NOMENCLATURE_ENSEMBLE,
    SECTION_XIII_REGLES,
    TROIS_CONCORDANCES,
    VALIDATIONS_CANONIQUES,
    get_section_XIII_entries,
    psi_savard,
    rapport_zeta_savard,
    render_ensemble_structure_summary,
    render_section_XIII_summary,
    verifier_validations_canoniques,
)


class TestModuleSectionXIII:
    """Le module memoire Section XIII est complet et exact."""

    def test_sept_regles_presentes(self):
        codes = [r["code"] for r in SECTION_XIII_REGLES]
        assert codes == [f"XIII.{i}" for i in range(1, 8)]

    def test_entrees_rag_generees(self):
        entries = get_section_XIII_entries()
        assert len(entries) == 7
        for e in entries:
            assert e["id"].startswith("section_XIII_")
            assert e["metadata"]["section"] == "XIII"
            assert "methode_spectral.thy" in e["metadata"]["source_thy"]

    def test_summary_injectable(self):
        s = render_section_XIII_summary()
        assert "XIII" in s
        assert "psi_savard" in s
        assert "Tchebychev" in s or "SB(n)" in s

    def test_nomenclature_complete(self):
        assert set(NOMENCLATURE_ENSEMBLE) == {
            "1/y1", "1/y2", "1/y3", "1/t", "1/ms1", "1/ms2", "1/ms3",
        }
        assert NOMENCLATURE_ENSEMBLE["1/ms3"]["symbole"] == "ms_rapport"
        assert NOMENCLATURE_ENSEMBLE["1/y2"]["symbole"] == "zeta_critique"

    def test_statut_affirmatif_dans_regles(self):
        """v3.34 : la 7e regle affirme le statut de THEOREME du locale
        (et non plus 'N'EST PAS une preuve'). Voir Section XIII v3.34."""
        r7 = SECTION_XIII_REGLES[6]
        assert r7["nom"] == "statut_affirmatif_theoreme_du_locale"
        texte = r7["regle"]
        assert "THEOREME" in texte
        assert "VRAI" in texte
        assert "ensemble_savard" in texte
        assert "TROIS CONCORDANCES" in texte
        # L'ancienne formulation "N'EST PAS une preuve" ne doit plus etre presente
        assert "N'EST PAS une preuve" not in texte

    def test_trois_concordances_completes(self):
        """v3.34 : les 3 concordances C1, C2, C3 sont declarees et documentees."""
        codes = [c["code"] for c in TROIS_CONCORDANCES]
        assert codes == ["C1", "C2", "C3"]
        c1, c2, c3 = TROIS_CONCORDANCES
        assert c1["egalite"] == "1/y1 = 1/t"
        assert c2["egalite"] == "1/y3 = 1/ms1"
        assert c3["egalite"] == "1/y2 = 1/ms3"
        # Chaque concordance a un role dans le pont
        for c in TROIS_CONCORDANCES:
            assert c["role_dans_le_pont"]
            assert c["preuve"]
            assert c["sens"]

    def test_ensemble_structure_ontologique(self):
        """v3.34 : la structure Ensemble = 1/x + 1/t + 1/ms est documentee."""
        assert ENSEMBLE_STRUCTURE["ensemble_unitaire"]["valeur"] == 1
        vues = ENSEMBLE_STRUCTURE["vues_du_meme_ensemble"]
        assert set(vues) == {"1/x", "1/t", "1/ms"}
        assert vues["1/x"]["identite"] == "zeta"
        assert vues["1/t"]["identite"] == "psi_savard"
        assert vues["1/ms"]["identite"] == "methode_spectrale"
        assert vues["1/x"]["decomposition"] == ["1/y1", "1/y2", "1/y3"]
        assert vues["1/ms"]["decomposition"] == ["1/ms1", "1/ms2", "1/ms3"]
        assert "RsP = Re = 1/2" in ENSEMBLE_STRUCTURE["conclusion"]

    def test_ensemble_structure_summary_injectable(self):
        """v3.34 : le rendu textuel de la structure est utilisable en injection LLM."""
        s = render_ensemble_structure_summary()
        assert "Ensemble = 1" in s
        assert "1/x" in s and "1/t" in s and "1/ms" in s
        assert "TROIS CONCORDANCES" in s
        for concordance in TROIS_CONCORDANCES:
            assert concordance["egalite"] in s


class TestHelpersPsiSavard:
    """Les helpers reproduisent exactement les valeurs de Philippe."""

    @pytest.mark.parametrize("v", VALIDATIONS_CANONIQUES, ids=lambda v: f"n={v['n']}")
    def test_validation_canonique(self, v):
        assert math.isclose(psi_savard(v["x"], v["n"]), v["psi_savard"], abs_tol=1e-9)

    def test_verifier_validations_toutes_ok(self):
        verdicts = verifier_validations_canoniques()
        assert len(verdicts) == 4
        assert all(r["ok"] for r in verdicts)

    def test_rapport_zeta_savard_at_10(self):
        assert math.isclose(rapport_zeta_savard(10), 1024 / 3262, rel_tol=1e-15)

    def test_rapport_zeta_savard_at_49(self):
        assert math.isclose(
            rapport_zeta_savard(49), 562949953421312 / 1829587348619198, rel_tol=1e-15,
        )

    def test_n_zero_rejete(self):
        with pytest.raises(ValueError):
            psi_savard(30.0, 0)

    def test_x_invalide_rejete(self):
        with pytest.raises(ValueError):
            psi_savard(0.5, 10)


class TestRegimePontSavard:
    """Le 13e regime est enregistre dans le Dictionnaire Spectral."""

    def test_regime_present(self):
        assert "regime_pont_savard" in DICTIONNAIRE_SPECTRAL
        assert regime_count() == 13

    def test_lemmes_certifies(self):
        r = get_regime("regime_pont_savard")
        lemmes = " ".join(r.lemmes_certifies)
        for lem in (
            "rapport_zeta_savard_at_10", "rapport_zeta_savard_at_49",
            "alignement_central", "ensemble_savard_satisfaisable",
            "pont_spectral_direct_final", "synthese_pont_savard",
            "methode_spectrale_exclusivite_P",
        ):
            assert lem in lemmes, f"lemme {lem} manquant"

    def test_definitions_hol(self):
        r = get_regime("regime_pont_savard")
        assert "psi_savard" in r.definitions_hol
        assert "locale_ensemble_savard" in r.definitions_hol
        assert "nomenclature_savard" in r.definitions_hol

    def test_regle_statut_affirmatif(self):
        """v3.34 : les regles cognitives du regime portent le statut affirmatif
        (theoreme du locale, universalite) et non plus 'jamais une preuve'."""
        r = get_regime("regime_pont_savard")
        texte = " ".join(r.regles_cognitives + r.avertissements)
        # Marqueurs de la nouvelle vision affirmative
        assert "THEOREME" in texte
        assert "ensemble_savard" in texte
        assert "satisfaisabilite" in texte.lower() or "SATISFAISABILITE" in texte
        # La structure ontologique et les trois concordances sont referencees
        assert "1/x + 1/t + 1/ms" in texte or "TROIS CONCORDANCES" in texte
        # Universalite mentionnee
        assert "universel" in texte.lower() or "universalite" in texte.lower()

    def test_exemples_numeriques(self):
        r = get_regime("regime_pont_savard")
        exemples = " ".join(r.exemples_valides)
        for val in ("28.888143698", "96.894150249", "226.894132001", "-100.798158152"):
            assert val in exemples

    def test_total_lemmes_augmente(self):
        assert total_lemmes() >= 60


class TestDetectionRAG:
    """L'adaptateur RAG detecte le Pont Savard dans les requetes naturelles."""

    @pytest.fixture(scope="class")
    def adaptateur(self):
        return AdaptateurCognitifSpectral()

    @pytest.mark.parametrize("requete", [
        "Explique-moi l'equation psi_savard pour x=30",
        "Quel est le lien entre Tchebychev et la methode spectrale ?",
        "La fonction zeta de Riemann et la droite critique Re=1/2",
        "Presente le theoreme de l'Ensemble du pont Savard",
        "Que vaut rapport_zeta_savard(49) ?",
        "Les zeros non-triviaux ont-ils Re=1/2 ?",
    ])
    def test_requetes_declenchent_pont_savard(self, adaptateur, requete):
        regimes, _ = adaptateur.detecter_regimes(requete)
        assert "regime_pont_savard" in regimes, (
            f"regime_pont_savard non detecte pour : {requete!r} (detectes : {regimes})"
        )

    def test_requete_generique_ne_declenche_pas(self, adaptateur):
        regimes, _ = adaptateur.detecter_regimes("Bonjour Gabriel, comment vas-tu ?")
        assert "regime_pont_savard" not in regimes

    def test_contexte_injecte_contient_lemmes(self, adaptateur):
        analyse = adaptateur.analyser("Parle-moi du pont Savard et de psi_savard")
        assert "PONT SAVARD" in analyse.contexte_brut.upper()
        assert "ensemble_savard_satisfaisable" in analyse.contexte_brut
        assert "REQUETE UTILISATEUR" in analyse.prompt_augmente


class TestIntegrateurMemoire:
    """L'integrateur memoire charge la section XIII."""

    def test_section_xiii_dans_sections_extra(self):
        import sys
        from pathlib import Path
        src_core = Path(__file__).parent.parent / "src" / "core"
        sys.path.insert(0, str(src_core))
        from integrateur_memoire import IntegrateurMemoireGabriel
        im = IntegrateurMemoireGabriel()
        info = im.info()
        assert "methode_spectral_section_XIII" in info["sections_extra"]
        assert info["regimes"] == 13

    def test_prompt_augmente_via_integrateur(self):
        import sys
        from pathlib import Path
        src_core = Path(__file__).parent.parent / "src" / "core"
        sys.path.insert(0, str(src_core))
        from integrateur_memoire import IntegrateurMemoireGabriel
        im = IntegrateurMemoireGabriel()
        prompt = im.augmenter_prompt("Explique le pont Savard entre Tchebychev et zeta")
        assert "psi_savard" in prompt
