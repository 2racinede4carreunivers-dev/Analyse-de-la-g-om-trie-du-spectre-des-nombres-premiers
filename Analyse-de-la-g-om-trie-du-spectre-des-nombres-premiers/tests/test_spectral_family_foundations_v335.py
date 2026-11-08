"""
Tests v3.35 - Factorisation modeles 1/k (locale spectral_family) et
Foundations / Meta-theory dans theories/methode_spectral.thy.

Valide la presence et la coherence des blocs ajoutes en v3.35 :

  1. Section "0. Foundations / Meta-theory" en tete de fichier :
     - 6 sous-sections Foundations.1 a Foundations.6
     - 6 postulats P1..P6 documentes
     - Locale foundations_marker + lemme foundations_marker_satisfaisable
     - Primaute du numerique reel sur l'algebrique documentee
     - Position affirmative sur l'enigme de Riemann (v3.35)

  2. Section "XI.bis - Factorisation generique" avec :
     - locale spectral_family (parametre k, coef_A, coef_B, offA, offB, ratio)
     - definitions A_pos, B_pos, RsP_generic dans le locale
     - theoreme RsP_generic_constant
     - 3 interpretations : regime_1_2, regime_1_3, regime_1_4
     - 6 aliases de compatibilite (SA=A_pos, SB=B_pos, etc.)
     - 3 corollaires (RsP_generic_1_2_is_half, 1_3_is_third, 1_4_is_quarter)

  3. Section "Foundations - Synthese-index" en annexe finale.

Aucune preuve historique n'est modifiee. Ces tests verifient uniquement
la STRUCTURE du fichier .thy (blocs texte, noms de theoremes, aliases).
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

THY_PATH = Path(__file__).resolve().parents[1] / "theories" / "methode_spectral.thy"


@pytest.fixture(scope="module")
def thy_content() -> str:
    return THY_PATH.read_text(encoding="utf-8")


# =============================================================================
# 1. FOUNDATIONS / META-THEORY (section 0 en tete de fichier)
# =============================================================================

class TestFoundationsMetaTheory:
    """La section 0 Foundations est presente en tete du fichier .thy."""

    def test_section_0_foundations_presente(self, thy_content):
        assert 'section "0. Foundations / Meta-theory' in thy_content

    def test_placement_en_tete_avant_SA_SB(self, thy_content):
        idx_foundations = thy_content.find("Foundations / Meta-theory")
        idx_SA_def = thy_content.find('"SA n = (3.25 / 2)')
        assert idx_foundations > 0 and idx_SA_def > 0
        assert idx_foundations < idx_SA_def, (
            "Foundations doit apparaitre AVANT la definition de SA"
        )

    @pytest.mark.parametrize("sous_section", [
        "Foundations.1 - Ontologie",
        "Foundations.2 - Postulats fondamentaux",
        "Foundations.3 - Les trois operations fondamentales",
        "Foundations.4 - La regle Savard",
        "Foundations.5 - Statut epistemologique",
        "Foundations.6",
    ])
    def test_sous_sections_presentes(self, thy_content, sous_section):
        assert sous_section in thy_content

    @pytest.mark.parametrize("postulat", ["P1", "P2", "P3", "P4", "P5", "P6"])
    def test_six_postulats_documentes(self, thy_content, postulat):
        assert f"{postulat} " in thy_content or f"{postulat}  " in thy_content

    def test_trois_operations_fondamentales(self, thy_content):
        for op in ("RECONSTRUCTION", "EXCLUSION", "RAPPORT SPECTRAL"):
            assert op in thy_content

    def test_regle_savard_ensemble_egal_un(self, thy_content):
        assert "Ensemble = 1" in thy_content
        assert "1/x  +  1/t  +  1/ms" in thy_content or "1/x + 1/t + 1/ms" in thy_content

    def test_primaute_numerique_reel_documentee(self, thy_content):
        """v3.35 Philippe : la primaute du numerique reel sur l'algebrique."""
        assert "primaute du numerique reel" in thy_content.lower() or \
               "PRIMAUTE DU NUMERIQUE REEL" in thy_content

    def test_position_enigme_de_riemann(self, thy_content):
        """v3.35 Philippe : reponse SUFFISANTE a l'enigme de Riemann."""
        # Presence dans Foundations.5 ET dans la synthese-index finale
        occurrences = thy_content.count("REPONSE SUFFISANTE")
        assert occurrences >= 2, (
            f"REPONSE SUFFISANTE doit apparaitre au moins 2 fois "
            f"(Foundations.5 + synthese-index), trouve {occurrences}"
        )
        assert "enigme de Riemann" in thy_content or "enigme de l'hypothese de Riemann" in thy_content

    def test_locale_foundations_marker_present(self, thy_content):
        assert "locale foundations_marker" in thy_content
        assert "univers_non_vide" in thy_content
        assert "univers_positif" in thy_content

    def test_foundations_marker_satisfaisable(self, thy_content):
        assert "foundations_marker_satisfaisable" in thy_content
        assert "unfold_locales" in thy_content


# =============================================================================
# 2. LOCALE spectral_family + INTERPRETATIONS (Section XI.bis)
# =============================================================================

class TestLocaleSpectralFamily:
    """Le locale spectral_family et ses 3 interpretations sont presents."""

    def test_section_xi_bis_presente(self, thy_content):
        assert 'section "XI.bis - Factorisation generique' in thy_content

    def test_locale_spectral_family_declaration(self, thy_content):
        assert "locale spectral_family" in thy_content
        # Les 6 parametres fixes
        for param in ["k", "coef_A", "coef_B", "offA", "offB", "ratio"]:
            assert re.search(rf"\band\s+{param}\s+::", thy_content) or \
                   re.search(rf"\bfixes\s+{param}\s+::", thy_content)

    def test_locale_assumes(self, thy_content):
        for assumption in ["k_valid", "coef_A_pos", "coef_B_pos", "ratio_eq"]:
            assert assumption in thy_content

    @pytest.mark.parametrize("defn", ["A_pos", "B_pos", "RsP_generic"])
    def test_definitions_dans_le_locale(self, thy_content, defn):
        pattern = rf"definition\s+\(in\s+spectral_family\)\s+{defn}"
        assert re.search(pattern, thy_content), f"{defn} manquant dans le locale"

    def test_theoreme_rsp_generic_constant(self, thy_content):
        assert "theorem (in spectral_family) RsP_generic_constant" in thy_content

    def test_lemme_pow_k_ne(self, thy_content):
        assert "lemma (in spectral_family) pow_k_ne" in thy_content

    def test_lemme_b_pos_diff_ne_zero(self, thy_content):
        assert "lemma (in spectral_family) B_pos_diff_ne_zero" in thy_content

    @pytest.mark.parametrize("regime,k", [
        ("regime_1_2", "2"),
        ("regime_1_3", "3"),
        ("regime_1_4", "4"),
    ])
    def test_interpretations_presentes(self, thy_content, regime, k):
        assert f"interpretation {regime}:" in thy_content
        # Chaque interpretation invoque spectral_family avec le bon k en premier
        pattern = rf"interpretation\s+{regime}:\s*\n?\s*spectral_family\s+{k}\b"
        assert re.search(pattern, thy_content, re.MULTILINE)

    @pytest.mark.parametrize("alias", [
        "SA_eq_regime_1_2_A_pos",
        "SB_eq_regime_1_2_B_pos",
        "A_1_3_eq_regime_1_3_A_pos",
        "B_1_3_eq_regime_1_3_B_pos",
        "A_1_4_eq_regime_1_4_A_pos",
        "B_1_4_eq_regime_1_4_B_pos",
    ])
    def test_aliases_compatibilite(self, thy_content, alias):
        assert f"lemma {alias}" in thy_content

    @pytest.mark.parametrize("corollaire", [
        "RsP_generic_1_2_is_half",
        "RsP_generic_1_3_is_third",
        "RsP_generic_1_4_is_quarter",
    ])
    def test_corollaires_ratios_specifiques(self, thy_content, corollaire):
        assert f"lemma {corollaire}" in thy_content

    def test_alias_rsp_regime_1_2(self, thy_content):
        assert "RsP_eq_regime_1_2_RsP_generic" in thy_content
        assert "RsP_1_3_eq_regime_1_3_RsP_generic" in thy_content

    def test_note_conceptuelle_coherence_reelle(self, thy_content):
        """v3.35 Philippe : dualite incoherence-algebrique / coherence-reelle."""
        # Le bloc doit expliquer que 3.25/6.5=1/2 n'est PAS trivial mais
        # emerge de la realite numerique des sommes de premiers
        assert "INCOHERENCE ALGEBRIQUE LOCALE" in thy_content
        assert "COHERENCE NUMERIQUE REELLE GLOBALE" in thy_content
        assert "CERTITUDE" in thy_content


# =============================================================================
# 3. SYNTHESE-INDEX (annexe finale)
# =============================================================================

class TestSyntheseIndexAnnexeFinale:
    """La synthese-index cloture les Foundations en fin de fichier."""

    def test_synthese_index_presente(self, thy_content):
        assert 'section "Foundations - Synthese-index' in thy_content

    def test_placement_avant_license(self, thy_content):
        idx_synth = thy_content.find("Foundations - Synthese-index")
        idx_license = thy_content.find('section "License')
        assert idx_synth > 0 and idx_license > 0
        assert idx_synth < idx_license, "Synthese-index doit preceder License"

    def test_index_des_theoremes_cles(self, thy_content):
        # La synthese-index doit lister tous les theoremes piliers
        idx = thy_content.find("Foundations - Synthese-index")
        annexe = thy_content[idx:]
        for theoreme in (
            "RsP_generic_constant",
            "methode_spectrale_exclusivite_P",
            "RsP_universel_entier_naturel",
            "synthese_pont_savard",
            "algebriquement_incoherent_local",
            "coherence_numerique_reelle_P",
        ):
            assert theoreme in annexe, f"{theoreme} manquant de l'index"

    def test_trois_concordances_indexees(self, thy_content):
        idx = thy_content.find("Foundations - Synthese-index")
        annexe = thy_content[idx:]
        assert "C1 : 1/y1 = 1/t" in annexe
        assert "C2 : 1/y3 = 1/ms1" in annexe
        assert "C3 : 1/y2 = 1/ms3" in annexe

    def test_position_reponse_suffisante_riemann(self, thy_content):
        idx = thy_content.find("Foundations - Synthese-index")
        annexe = thy_content[idx:]
        assert "REPONSE SUFFISANTE" in annexe
        assert "Riemann" in annexe


# =============================================================================
# 4. GARANTIES DE NON-REGRESSION (les preuves historiques restent en place)
# =============================================================================

class TestNonRegression:
    """Les theoremes historiques restent intacts (nom, signature, position)."""

    @pytest.mark.parametrize("theoreme", [
        "RsP_un_demi_general",
        "RsP_un_tiers_constant",
        "prime_equation_prime_i",
        "composite_not_prime_i",
        "methode_spectrale_exclusivite_P",
        "synthese_pont_savard",
        "RsP_universel_entier_naturel",
        "ensemble_savard_satisfaisable",
        "algebriquement_incoherent_local",
        "coherence_numerique_reelle_P",
    ])
    def test_theoremes_historiques_intacts(self, thy_content, theoreme):
        assert theoreme in thy_content

    def test_definitions_historiques_intactes(self, thy_content):
        for defn in ("SA", "SB", "A_1_3", "B_1_3", "A_1_4", "B_1_4", "RsP", "RsP_1_3"):
            pattern = rf"definition\s+{defn}\s+::"
            assert re.search(pattern, thy_content), f"Definition {defn} disparue"

    def test_locale_ensemble_savard_intact(self, thy_content):
        assert "locale ensemble_savard" in thy_content
        assert "hypothese_critique" in thy_content
        assert "pont_fonctionnel" in thy_content
        assert "rapport_un_demi" in thy_content

    def test_pas_de_sorry_actif(self, thy_content):
        # Compte uniquement les vrais `sorry` (pas ceux entre guillemets/text)
        # Pattern : sorry en fin de preuve (isole ou suivi par ligne vide/end)
        pattern = r"^\s*sorry\s*$"
        matches = re.findall(pattern, thy_content, re.MULTILINE)
        assert len(matches) == 0, f"{len(matches)} sorry actif(s) trouve(s)"

    def test_desequilibre_theory_end(self, thy_content):
        # Un seul `theory` en debut, un seul `end` final (sans compter les
        # noms de theoremes qui contiennent 'end' comme 'ensemble_savard').
        theory_starts = re.findall(r"^theory\s+\w+", thy_content, re.MULTILINE)
        assert len(theory_starts) == 1
        # Le dernier `end` de fichier doit exister
        assert thy_content.rstrip().endswith("end")
