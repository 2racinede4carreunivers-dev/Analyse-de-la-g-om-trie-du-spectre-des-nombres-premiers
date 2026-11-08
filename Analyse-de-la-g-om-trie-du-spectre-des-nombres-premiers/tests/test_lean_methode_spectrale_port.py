"""
Tests v3.22 : verifie l'existence et la structure du portage Lean 4 de
`theories/MethodeSpectrale.lean` (portage 1:1 depuis methode_spectral.thy).

Ces tests sont STRUCTURELS uniquement : ils verifient que toutes les
definitions et theoremes cles du fichier Isabelle sont bien presents
dans la version Lean 4. Ils N'EXECUTENT PAS Lean (non installe dans
l'environnement Docker de Gabriel — la compilation doit etre faite
cote utilisateur avec `lake build` + Mathlib).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="module")
def lean_content() -> str:
    lean = ROOT / "theories" / "MethodeSpectrale.lean"
    assert lean.exists(), (
        "Le fichier Lean 4 theories/MethodeSpectrale.lean doit exister"
    )
    return lean.read_text(encoding="utf-8")


# ============================================================================
# Structure Lean 4 : imports Mathlib et namespace
# ============================================================================


class TestLeanFileStructure:
    def test_imports_mathlib(self, lean_content):
        assert "import Mathlib.Data.Real.Basic" in lean_content
        assert "import Mathlib.Data.Nat.Prime.Basic" in lean_content

    def test_namespace_declared(self, lean_content):
        assert "namespace MethodeSpectrale" in lean_content
        assert "end MethodeSpectrale" in lean_content


# ============================================================================
# Section 1 & 2 : SA, SB, RsP
# ============================================================================


class TestSuitesAndRsP:
    def test_SA_definition(self, lean_content):
        assert "def SA (n : ℕ) : ℝ :=" in lean_content

    def test_SB_definition(self, lean_content):
        assert "def SB (n : ℕ) : ℝ :=" in lean_content

    def test_RsP_definition(self, lean_content):
        assert "def RsP (n1 n2 : ℕ) : ℝ :=" in lean_content

    def test_RsP_un_demi_theorem(self, lean_content):
        assert "theorem RsP_un_demi_general" in lean_content


# ============================================================================
# Section 3 : digamma_calc et prime_equation
# ============================================================================


class TestDigammaAndPrimeEquation:
    def test_digamma_calc_defined(self, lean_content):
        assert "def digamma_calc (n : ℕ) (p : ℕ) : ℝ :=" in lean_content

    def test_prime_equation_defined(self, lean_content):
        assert "def prime_equation (n : ℕ) (p : ℕ) : ℝ :=" in lean_content

    def test_prime_equation_identity(self, lean_content):
        assert "lemma prime_equation_identity" in lean_content


# ============================================================================
# Section 5 : Exemples numeriques 29, 31, 37, 41
# ============================================================================


class TestNumericalExamples:
    @pytest.mark.parametrize("name,value", [
        ("n29", "10"),
        ("n31", "11"),
        ("n37", "12"),
        ("n41", "13"),
    ])
    def test_prime_positions_defined(self, lean_content, name, value):
        assert f"def {name} : ℕ := {value}" in lean_content

    @pytest.mark.parametrize("lemma_name,expected", [
        ("SA_10", "1662"),
        ("SB_10", "3262"),
        ("SA_11", "3326"),
        ("SB_11", "6590"),
        ("SA_12", "6654"),
        ("SB_12", "13246"),
        ("SA_13", "13310"),
        ("SB_13", "26558"),
    ])
    def test_numerical_lemmas_present(self, lean_content, lemma_name, expected):
        assert f"lemma {lemma_name}" in lean_content
        assert expected in lean_content


# ============================================================================
# Section 7 : prime_i (i-ieme premier via choix classique)
# ============================================================================


class TestPrimeI:
    def test_position_axiom(self, lean_content):
        assert "axiom position" in lean_content

    def test_prime_position_exists_axiom(self, lean_content):
        assert "axiom prime_position_exists" in lean_content

    def test_prime_i_definition(self, lean_content):
        assert "def prime_i (i : ℕ) : ℕ" in lean_content
        assert "Classical.choose" in lean_content

    def test_prime_i_is_prime(self, lean_content):
        assert "lemma prime_i_is_prime" in lean_content

    def test_prime_i_position(self, lean_content):
        assert "lemma prime_i_position" in lean_content


# ============================================================================
# Section 8-11 : LES 3 PILIERS DE LA METHODE SPECTRALE
# ============================================================================


class TestThreePillars:
    """Verifie que les 3 piliers sont bien formalises en Lean."""

    def test_pilier_1_composite_not_prime_i(self, lean_content):
        """Pilier 1 - Aucun compose n'est un prime_i."""
        assert "theorem composite_not_prime_i" in lean_content

    def test_pilier_2_composite_no_reconstruction(self, lean_content):
        """Pilier 2 - Aucun compose ne peut etre reconstruit."""
        assert "theorem composite_no_reconstruction_position" in lean_content

    def test_pilier_3_composite_pair_no_rsp(self, lean_content):
        """Pilier 3 - Aucun couple de composes ne peut occuper des positions RsP."""
        assert "theorem composite_pair_no_rsp_positions" in lean_content
        assert "theorem composite_single_no_rsp_position" in lean_content

    def test_synthese_documented(self, lean_content):
        """La synthese des 3 piliers doit etre documentee."""
        assert "PILIER 1" in lean_content
        assert "PILIER 2" in lean_content
        assert "PILIER 3" in lean_content
        assert "CONSEQUENCE DEFINITIVE" in lean_content


# ============================================================================
# Section 9-10 : 6 composes canoniques (4, 9, 15, 51, 91, 121)
# ============================================================================


class TestSixCompositesCanonical:
    @pytest.mark.parametrize("value", [4, 9, 15, 51, 91, 121])
    def test_composite_not_prime_lemma(self, lean_content, value):
        assert f"lemma composite_{value}_not_prime" in lean_content

    @pytest.mark.parametrize("value", [4, 9, 15, 51, 91, 121])
    def test_no_spectral_position(self, lean_content, value):
        assert f"theorem no_spectral_position_for_{value}" in lean_content

    @pytest.mark.parametrize("value", [4, 9, 15, 51, 91, 121])
    def test_no_reconstruction(self, lean_content, value):
        assert f"theorem no_reconstruction_for_{value}" in lean_content


# ============================================================================
# Section XI : Regles de construction (bugs 9 & 10 des .thy)
# ============================================================================


class TestSectionXI:
    """Verifie que la Section XI est correctement portee, avec les
    corrections des bugs 9 (fun -> def) et 10 (sorry -> conditionnels)."""

    def test_terme_progression_simple(self, lean_content):
        assert "def terme_progression_simple" in lean_content

    def test_avant_dernier(self, lean_content):
        assert "def avant_dernier" in lean_content

    def test_dernier_terme(self, lean_content):
        assert "def dernier_terme" in lean_content

    def test_terme_suite_A_uses_def(self, lean_content):
        """Bug 9 : terme_suite_A doit etre `def` (pas de recursion)."""
        assert "def terme_suite_A" in lean_content

    def test_terme_suite_B_uses_def(self, lean_content):
        """Bug 9 : terme_suite_B doit etre `def` (pas de recursion)."""
        assert "def terme_suite_B" in lean_content

    def test_somme_suite_defined(self, lean_content):
        assert "def somme_suite" in lean_content
        assert "Finset.Icc 1 n" in lean_content

    def test_somme_A_close(self, lean_content):
        assert "def somme_A_close" in lean_content

    def test_somme_B_close(self, lean_content):
        assert "def somme_B_close" in lean_content

    def test_rapport_spectral_AB(self, lean_content):
        assert "def rapport_spectral_AB" in lean_content

    def test_no_sorry_in_lean_file(self, lean_content):
        """Bug 10 : aucun `sorry` actif dans le fichier Lean."""
        for i, line in enumerate(lean_content.splitlines(), start=1):
            stripped = line.strip()
            # `sorry` isole (comme tactique complete de preuve)
            assert stripped != "sorry", (
                f"Ligne {i} : `sorry` actif detecte (bug 10 non corrige)"
            )

    def test_somme_A_lemma_conditional(self, lean_content):
        """Bug 10 : somme_A_construction_eq_formule enonce conditionnellement."""
        assert "lemma somme_A_construction_eq_formule" in lean_content
        assert "savard_A :" in lean_content

    def test_somme_B_lemma_conditional(self, lean_content):
        """Bug 10 : somme_B_construction_eq_formule enonce conditionnellement."""
        assert "lemma somme_B_construction_eq_formule" in lean_content
        assert "savard_B :" in lean_content

    def test_conjecture_documented(self, lean_content):
        """Les formules fermees Savard sont documentees comme CONJECTURES."""
        assert "CONJECTURE" in lean_content.upper()


# ============================================================================
# Sections XII-XXV : port integral (RsP_nn, trifocal, 1/3, 1/4, mix,
# suites negatives, asymetries, ecarts, zeta, Riemann, Section XII paramétrique)
# ============================================================================


class TestRsP_nn:
    """Section XII : Rapport spectral n x n (listes)."""

    def test_RsP_nn_defined(self, lean_content):
        assert "def RsP_nn (A_indices B_indices : List ℕ) : ℝ :=" in lean_content

    def test_A3_B3_examples(self, lean_content):
        assert "def A3 : List ℕ := [2, 9, 10]" in lean_content
        assert "def B3 : List ℕ := [3, 11, 15]" in lean_content


class TestTrifocal:
    """Section XIII : Plan trifocal - lien Riemann."""

    def test_axioms_present(self, lean_content):
        for a in ["postulate_positions", "postulate_demi",
                  "postulate_aire_rectangle", "postulate_combinatoire_1",
                  "postulate_combinatoire_2", "postulate_courbure",
                  "postulate_solution"]:
            assert f"axiom {a}" in lean_content, f"Axiome {a} manquant"

    def test_lemmas_present(self, lean_content):
        for lem in ["positions_coincident_trifocal", "demi_coincident_trifocal",
                    "aire_rectangle_decompose", "combinatoire_mixte_stricte",
                    "courbure_induite_par_surcombinatoire",
                    "solution_epipolaire_Riemann"]:
            assert f"theorem {lem}" in lean_content, f"Theoreme {lem} manquant"


class TestModele_1_4:
    """Section XIV : Modele spectral 1/4."""

    def test_A_1_4_B_1_4(self, lean_content):
        assert "def A_1_4 (n : ℕ) : ℝ" in lean_content
        assert "def B_1_4 (n : ℕ) : ℝ" in lean_content

    def test_premier_947(self, lean_content):
        assert "lemma preuve_premier_947" in lean_content
        assert "5260628" in lean_content  # somme B 947
        assert "1316180" in lean_content  # somme A 947

    def test_spectral_postulate_1_4(self, lean_content):
        assert "axiom spectral_postulate_1_4" in lean_content


class TestModele_1_3:
    """Section XV : Modele spectral 1/3."""

    def test_A_1_3_B_1_3(self, lean_content):
        assert "def A_1_3 (n : ℕ) : ℝ" in lean_content
        assert "def B_1_3 (n : ℕ) : ℝ" in lean_content

    def test_premier_227(self, lean_content):
        assert "lemma preuve_premier_227" in lean_content
        assert "238746" in lean_content  # somme B 227
        assert "79824" in lean_content   # somme A 227

    def test_spectral_postulate_1_3(self, lean_content):
        assert "axiom spectral_postulate_1_3" in lean_content


class TestRsP_1_3_et_1_4:
    """Section XVI : RsP_1_3 et RsP_1_4."""

    def test_RsP_un_tiers_constant(self, lean_content):
        assert "theorem RsP_un_tiers_constant" in lean_content

    def test_RsP_un_quart_constant(self, lean_content):
        assert "theorem RsP_un_quart_constant" in lean_content


class TestSuitesMixtes:
    """Section XVII : Suites mixtes SA_mix, SB_mix."""

    @pytest.mark.parametrize("name", [
        "SA_mix", "SB_mix", "SA_mix_closed_form", "SB_mix_closed_form",
        "SA_mix_step", "SB_mix_step", "SA_mix_limit_shape", "SB_mix_limit_shape",
        "digamma_mix", "premier_mix", "premier_mix_rewrite",
        "K6", "digamma_mix_6", "premier_mix_6",
        "digamma_mix_6_value", "premier_mix_6_value",
    ])
    def test_element_present(self, lean_content, name):
        assert name in lean_content, f"Element {name} manquant"


class TestSuitesNegatives:
    """Section XVIII : Suites negatives (SA_neg_eq, SB_neg_eq, RsP_neg)."""

    def test_SA_SB_neg(self, lean_content):
        assert "def SA_neg_eq (n : ℝ) : ℝ" in lean_content
        assert "def SB_neg_eq (n : ℝ) : ℝ" in lean_content

    def test_digamma_neg_calc(self, lean_content):
        assert "def digamma_neg_calc" in lean_content
        assert "lemma digamma_neg_calc_equation_alt" in lean_content

    def test_RsP_neg_axiom(self, lean_content):
        assert "axiom spectral_ratio_neg_un_demi" in lean_content
        assert "lemma RsP_neg_un_demi_general" in lean_content


class TestAsymetries:
    """Section XIX : Geometrie spectrale, asymetries ordonnee/chaotique."""

    def test_int_versions(self, lean_content):
        for name in ["indice_valide", "liste_strictement_croissante",
                     "asymetrique_ordonnee", "asymetrique_chaotique",
                     "asymetrie_implique_indices_valides"]:
            assert name in lean_content, f"Def {name} manquante"

    def test_nat_versions(self, lean_content):
        for name in ["indice_valide_nat", "liste_strictement_croissante_nat",
                     "asymetrique_ordonnee_nat", "asymetrique_chaotique_nat",
                     "asymetrie_nat_implique_indices_valides"]:
            assert name in lean_content, f"Def {name} manquante"


class TestComparaisonAsym:
    """Section XX : Methode de comparaison asymetrique 1/2 et 1/4."""

    def test_sommes_blocs(self, lean_content):
        for name in ["somme_SA_bloc", "somme_SB_bloc",
                     "somme_A_1_4_bloc", "somme_B_1_4_bloc"]:
            assert name in lean_content, f"Def {name} manquante"

    def test_RsP_blocs(self, lean_content):
        assert "def RsP_bloc_1_2" in lean_content
        assert "def RsP_bloc_1_4" in lean_content

    def test_comparaisons(self, lean_content):
        for name in ["comparaison_asym_ordonnee_1_2",
                     "comparaison_asym_chaotique_1_2",
                     "comparaison_asym_ordonnee_1_4",
                     "comparaison_asym_chaotique_1_4"]:
            assert name in lean_content, f"Def {name} manquante"


class TestRsPNegatif_1_3_1_4:
    """Section XXI : Rapports spectraux negatifs 1/3 et 1/4."""

    def test_SA_SB_neg_un_tiers(self, lean_content):
        assert "def SA_neg_eq_un_tiers" in lean_content
        assert "def SB_neg_eq_un_tiers" in lean_content
        assert "def RsP_neg_un_tiers" in lean_content
        assert "axiom spectral_ratio_neg_un_tiers" in lean_content

    def test_SA_SB_neg_un_quart(self, lean_content):
        assert "def SA_neg_eq_un_quart" in lean_content
        assert "def SB_neg_eq_un_quart" in lean_content
        assert "def RsP_neg_un_quart" in lean_content
        assert "axiom spectral_ratio_neg_un_quart" in lean_content


class TestEcartsSpectraux:
    """Section XXII : Ecarts spectraux (exemples numeriques cles)."""

    def test_gap_m19_m5(self, lean_content):
        assert "lemma gap_m19_m5" in lean_content
        assert "def SA_m7_val" in lean_content
        assert "def SB_m5_val" in lean_content

    def test_gap_m31_17(self, lean_content):
        assert "lemma gap_m31_17" in lean_content
        assert "def SA_m29_val" in lean_content

    def test_ecart_227_173(self, lean_content):
        assert "lemma ecart_227_173_1_3" in lean_content
        assert "lemma ecart_227_173_1_3_via_gap_equation" in lean_content
        assert "def gap_equation_1_3" in lean_content
        assert "axiom spectral_gap_postulate_1_3" in lean_content

    def test_ecart_947_881(self, lean_content):
        assert "lemma ecart_947_881_1_4_via_gap_equation" in lean_content
        assert "def gap_equation_1_4" in lean_content
        assert "axiom spectral_gap_postulate_1_4" in lean_content


class TestZetaAxiomatique:
    """Section XXIII : Axiomatisation analytique (zeros de zeta)."""

    def test_zeta_types(self, lean_content):
        for name in ["axiom zero_zeta", "axiom Re_zero_zeta",
                     "axiom Im_zero_zeta", "axiom prime_position_from_zero",
                     "axiom explicit_formula_axiom",
                     "axiom indice_spectral", "axiom premier_spectral"]:
            assert name in lean_content, f"Axiome/type {name} manquant"

    def test_concordance(self, lean_content):
        assert "axiom concordance_spectrale" in lean_content
        assert "axiom zero_associe" in lean_content


class TestRiemannAxiomatique:
    """Section XXIV : Hypothese de Riemann (axiomatique)."""

    def test_riemann_hypothesis(self, lean_content):
        assert "axiom Riemann_Hypothesis" in lean_content
        assert "Re_cz r = 1 / 2" in lean_content

    def test_aires_droite_critique(self, lean_content):
        for name in ["axiom T ", "axiom Tn ", "axiom T_rest",
                     "axiom relative_value", "axiom geometric_area",
                     "axiom mixed_gap_surplus", "axiom complementary_areas",
                     "axiom all_zeros_on_critical_line"]:
            assert name in lean_content, f"Axiome {name} manquant"


class TestSectionXII_Parametrique:
    """Section XII Isabelle (== XXV Lean) : construction generalisee 1/k_i."""

    def test_constantes_savard(self, lean_content):
        for name in ["alpha_A_k", "alpha_B_k", "offset_A_k", "offset_B_k"]:
            assert f"def {name}" in lean_content, f"Constante {name} manquante"

    def test_sommes_pos_neg(self, lean_content):
        for name in ["somme_A_pos_k", "somme_B_pos_k",
                     "somme_A_neg_k", "somme_B_neg_k"]:
            assert f"def {name}" in lean_content, f"Somme {name} manquante"

    def test_compatibilite_k_2(self, lean_content):
        assert "lemma somme_A_pos_k_eq_SA" in lean_content
        assert "lemma somme_B_pos_k_eq_SB" in lean_content

    def test_construction_terme_a_terme(self, lean_content):
        assert "def terme_A_pos" in lean_content
        assert "def terme_B_pos" in lean_content

    @pytest.mark.parametrize("lemma_name", [
        "suite_A_1_terme", "suite_A_2_termes_pos1", "suite_A_2_termes_pos2",
        "suite_A_3_termes_pos3", "suite_A_4_termes_pos3", "suite_A_4_termes_pos4",
        "suite_A_5_termes_pos4", "suite_A_5_termes_pos5",
        "suite_A_7_termes_pos6", "suite_A_7_termes_pos7",
        "suite_A_8_termes_pos6", "suite_A_8_termes_pos7", "suite_A_8_termes_pos8",
        "suite_B_8_termes_pos6", "suite_B_8_termes_pos7", "suite_B_8_termes_pos8",
        "suite_B_9_termes_pos6", "suite_B_9_termes_pos7", "suite_B_9_termes_pos9",
        "suite_B_10_termes_pos8", "suite_B_10_termes_pos10",
    ])
    def test_20_validations_numeriques(self, lean_content, lemma_name):
        assert f"lemma {lemma_name}" in lean_content, (
            f"Validation {lemma_name} manquante (Section XII paramétrique)"
        )

    def test_sommes_fermees_validations(self, lean_content):
        for name in ["somme_A_pos_11", "somme_B_pos_11",
                     "somme_A_neg_k_value", "somme_A_neg_m2",
                     "somme_A_neg_m5", "somme_B_neg_m5",
                     "somme_B_neg_m5_decimal"]:
            assert f"lemma {name}" in lean_content, f"Lemme {name} manquant"

    def test_RsP_k_universal(self, lean_content):
        assert "def RsP_k" in lean_content
        assert "def RsP_neg_k" in lean_content
        assert "theorem RsP_k_egale_un_sur_k_pos" in lean_content


# ============================================================================
# Meta : verification globale de completude
# ============================================================================


class TestPortCompletude:
    """Verifie que la traduction est integrale (comptes de sections/defs)."""

    def test_lean_file_size_reasonable(self, lean_content):
        # Le fichier Lean doit contenir au moins ~800 lignes apres port complet
        n_lines = len(lean_content.splitlines())
        assert n_lines >= 800, (
            f"Le fichier Lean fait seulement {n_lines} lignes — "
            f"le port complet devrait faire >= 800 lignes"
        )

    def test_no_sorry_anywhere(self, lean_content):
        """Regression globale : aucun `sorry` actif nulle part."""
        for i, line in enumerate(lean_content.splitlines(), start=1):
            stripped = line.strip()
            assert stripped != "sorry", f"Ligne {i} : `sorry` actif detecte"

    def test_all_25_sections_present(self, lean_content):
        """Verifie qu'on a bien les 25 sections de la traduction complete."""
        expected_sections = [
            "SECTION 1",  # SA, SB
            "SECTION 2",  # RsP 1/2
            "SECTION 3",  # digamma_calc, prime_equation
            "SECTION 4",  # postulat positif
            "SECTION 5",  # exemples numeriques
            "SECTION 6",  # equation generale reconstruction
            "SECTION 7",  # prime_i
            "SECTION 8",  # pilier 1
            "SECTION 9",  # 6 composes
            "SECTION 10", # pilier 2
            "SECTION 11", # pilier 3
            "SECTION XI", # regles construction A/B
            "SECTION XII",  # RsP n x n
            "SECTION XIII", # trifocal
            "SECTION XIV",  # 1/4
            "SECTION XV",   # 1/3
            "SECTION XVI",  # RsP 1/3 et 1/4
            "SECTION XVII", # suites mixtes
            "SECTION XVIII",# suites negatives
            "SECTION XIX",  # asymetries
            "SECTION XX",   # comparaison asym
            "SECTION XXI",  # RsP neg 1/3, 1/4
            "SECTION XXII", # ecarts spectraux
            "SECTION XXIII",# zeta axiomatique
            "SECTION XXIV", # Riemann axiomatique
        ]
        for sec in expected_sections:
            assert sec in lean_content, f"Section attendue absente : {sec}"
