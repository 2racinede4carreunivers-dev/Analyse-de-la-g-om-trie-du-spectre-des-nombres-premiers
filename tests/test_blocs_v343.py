"""Régressions statiques pour la section HOL v3.43 des blocs A_k / B_k."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
THY_PATH = ROOT / "theories" / "methode_spectral.thy"
SECTION_TITLE = 'section "Blocs A_k / B_k et rapport spectral de blocs (v3.43)"'
NEXT_SECTION = 'section "Rapport spectral 1/3 negatif"'
EXPECTED_DECLARATIONS = (
    "bloc_A_k",
    "bloc_B_k",
    "somme_bloc",
    "RsP_bloc",
    "RsP_bloc_extreme",
    "ponderation_bloc",
    "S_pondere",
    "card_bloc_A_k",
    "card_bloc_B_k",
    "asymetrie_structurelle_blocs",
    "bloc_A_1_singleton",
    "bloc_B_1_paire",
    "somme_bloc_B_1",
    "RsP_bloc_extreme_at_1",
    "ponderation_bloc_uniforme",
    "S_pondere_uniforme",
    "ponderation_bloc_complexe",
    "S_pondere_complexe",
    "ponderation_bloc_complexe_uniforme",
    "ponderation_bloc_complexe_of_real",
)
CENTRAL_REGIME_DECLARATIONS = (
    "RsP_un_demi_general",
    "prime_equation_prime_i",
    "composite_not_prime_i",
    "synthese_pont_savard",
    "ensemble_savard_satisfaisable",
    "pont_spectral_direct_final",
)


@pytest.fixture(scope="module")
def raw_content() -> bytes:
    return THY_PATH.read_bytes()


@pytest.fixture(scope="module")
def thy_content(raw_content: bytes) -> str:
    return raw_content.decode("utf-8", errors="strict")


@pytest.fixture(scope="module")
def section_v343(thy_content: str) -> str:
    start = thy_content.find(SECTION_TITLE)
    assert start >= 0, "Section v3.43 introuvable"
    end = thy_content.find(NEXT_SECTION, start)
    assert end > start, "La borne de fin de la section v3.43 est introuvable"
    return thy_content[start:end]


# Encodage, enveloppe Isabelle et délimiteurs du fichier complet.
class TestMethodeSpectralFileIntegrity:
    def test_utf8_strict_without_bom_crlf_or_nul(self, raw_content: bytes):
        raw_content.decode("utf-8", errors="strict")
        assert not raw_content.startswith(b"\xef\xbb\xbf")
        assert b"\r\n" not in raw_content
        assert b"\x00" not in raw_content

    def test_no_disallowed_control_characters(self, thy_content: str):
        disallowed = [
            (index, ord(char))
            for index, char in enumerate(thy_content)
            if ord(char) < 32 and char not in {"\n"}
        ]
        assert not disallowed, f"Caractères de contrôle interdits: {disallowed[:5]}"

    def test_native_theory_header_and_final_end(self, thy_content: str):
        nonempty_lines = [line.strip() for line in thy_content.splitlines() if line.strip()]
        assert nonempty_lines[0] == "theory methode_spectral"
        assert nonempty_lines[-1] == "end"

    def test_cartouches_are_balanced(self, thy_content: str):
        assert thy_content.count(r"\<open>") == thy_content.count(r"\<close>")

    def test_ml_comments_are_balanced(self, thy_content: str):
        assert thy_content.count("(*") == thy_content.count("*)")

    def test_file_is_nfc_normalized(self, thy_content: str):
        assert unicodedata.normalize("NFC", thy_content) == thy_content

    def test_exact_delimiter_counts_are_preserved(self, thy_content: str):
        assert thy_content.count(r"\<open>") == 105
        assert thy_content.count(r"\<close>") == 105
        assert thy_content.count("(*") == 380
        assert thy_content.count("*)") == 380


# Présence, positionnement et contenu documentaire de la nouvelle section.
class TestBlocSectionV343:
    def test_section_is_inserted_after_asymmetric_comparison(self, thy_content: str):
        previous = thy_content.find(
            'section "Methode de comparaison asymetrique pour 1/2 et 1/4"'
        )
        current = thy_content.find(SECTION_TITLE)
        following = thy_content.find(NEXT_SECTION, current)
        assert 0 <= previous < current < following

    def test_all_requested_declarations_are_unique(self, section_v343: str):
        for name in EXPECTED_DECLARATIONS:
            matches = re.findall(
                rf"(?m)^\s*(?:definition|lemma)\s+{re.escape(name)}\b",
                section_v343,
            )
            assert len(matches) == 1, f"Déclaration {name}: {len(matches)} occurrence(s)"

    @pytest.mark.parametrize(
        "label",
        (
            "1. DEFINITION DES BLOCS.",
            "2. COMPARAISON ASYMETRIQUE ORDONNEE.",
            "3. COMPARAISON ASYMETRIQUE CHAOTIQUE.",
            "4. EXTENSION COMPLEXE.",
        ),
    )
    def test_four_requested_topics_are_documented(self, section_v343: str, label: str):
        assert label in section_v343

    def test_complex_extension_links_to_xiii_4_b(self, section_v343: str):
        assert "XIII.4.b" in section_v343
        assert "pont_spectral_direct_final" in section_v343
        assert "Re(S_complexe(A_k, B_k)) = 1/2" in section_v343

    def test_no_axiom_or_unfinished_proof_in_added_section(self, section_v343: str):
        active_lines = [
            line.strip()
            for line in section_v343.splitlines()
            if line.strip() and not line.lstrip().startswith("(*")
        ]
        active = "\n".join(active_lines)
        assert not re.search(r"(?m)^\s*axiomatization\b", active)
        assert not re.search(r"(?m)^\s*(?:sorry|oops)\s*$", active)

    def test_each_new_lemma_has_a_closed_proof_command(self, section_v343: str):
        declarations = list(
            re.finditer(r"(?m)^\s*(?:definition|lemma)\s+([A-Za-z0-9_]+)\b", section_v343)
        )
        for index, match in enumerate(declarations):
            name = match.group(1)
            if name not in EXPECTED_DECLARATIONS or not match.group(0).lstrip().startswith("lemma"):
                continue
            body_end = declarations[index + 1].start() if index + 1 < len(declarations) else len(section_v343)
            body = section_v343[match.end():body_end]
            assert re.search(r"\b(?:by|proof)\b", body), (
                f"Le lemme {name} ne contient pas de commande de preuve"
            )
            if re.search(r"\bproof\b", body):
                assert re.search(r"(?m)^\s*qed\b", body), f"Le lemme {name} n'est pas clos par qed"

    def test_real_weighted_definitions_have_expected_types(self, section_v343: str):
        assert 'definition ponderation_bloc :: "real list \\<Rightarrow> real list \\<Rightarrow> real"' in section_v343
        assert re.search(
            r'definition S_pondere :: "real list \\<Rightarrow> real list \\<Rightarrow>\s*'
            r'real list \\<Rightarrow> real list \\<Rightarrow> real"',
            section_v343,
        )

    def test_false_equivalence_claims_are_replaced_by_exact_warning(self, section_v343: str):
        assert "NE SONT PAS" in section_v343
        assert "n'est PAS forcee a 1/2" in section_v343
        assert "observable spectrale DIFFERENTE" in section_v343
        assert "reformulation equivalente" not in section_v343
        assert "se reduisent numeriquement au meme regime central : RsP = 1/2" not in section_v343

    def test_failed_proof_regression_uses_nat_numeral_rewrite(self, section_v343: str):
        # v3.45.1 : preuves directes avec numeral_2_eq_2 (les tentatives
        # precedentes via eval_nat_numeral + bloc_B_1_paire cascade avaient
        # echoue en compilation Isabelle reelle sur GitHub Actions).
        assert re.search(
            r"lemma bloc_B_1_paire:.*?by \(simp add: bloc_B_k_def numeral_2_eq_2\)",
            section_v343,
            flags=re.DOTALL,
        )
        assert re.search(
            r"lemma somme_bloc_B_1:.*?by \(simp add: somme_bloc_def bloc_B_k_def numeral_2_eq_2\)",
            section_v343,
            flags=re.DOTALL,
        )
        assert re.search(
            r"lemma RsP_bloc_extreme_at_1:.*?"
            r"by \(simp add: RsP_bloc_extreme_def somme_bloc_def bloc_B_k_def numeral_2_eq_2\)",
            section_v343,
            flags=re.DOTALL,
        )
        # Garde-fou : les anciennes tactiques fragiles ne doivent PLUS apparaitre
        assert "upt_conv_Cons eval_nat_numeral" not in section_v343
        assert "simp add: bloc_B_1_paire)" not in section_v343
        assert "simp add: somme_bloc_B_1 eval_nat_numeral" not in section_v343

    def test_corrective_warning_counterexample_and_anchor_are_intact(self, section_v343: str):
        assert "RsP_bloc(1) = -91/90" in section_v343
        assert "Ancrage syntaxique" in section_v343
        assert "ceci ne signifie PAS que RsP_bloc(k) sur SA/SB vaut" in section_v343
        assert re.search(r"(?m)^lemma bloc_A_k_pour_SA:", section_v343)
        assert re.search(r"(?m)^lemma bloc_B_k_pour_SB:", section_v343)

    def test_complex_weighted_definitions_have_expected_types(self, section_v343: str):
        assert (
            'definition ponderation_bloc_complexe :: "complex list \\<Rightarrow> '
            'complex list \\<Rightarrow> complex"'
        ) in section_v343
        assert re.search(
            r'definition S_pondere_complexe :: "complex list \\<Rightarrow> '
            r'complex list \\<Rightarrow>\s*complex list \\<Rightarrow> '
            r'complex list \\<Rightarrow> complex"',
            section_v343,
        )

    def test_complex_lemmas_are_formalized_without_axioms(self, thy_content: str, section_v343: str):
        assert 'imports Complex_Main' in thy_content
        assert re.search(
            r"lemma ponderation_bloc_complexe_uniforme:\s*"
            r'"length coeffs = length valeurs \\<Longrightarrow>.*?'
            r'ponderation_bloc_complexe coeffs valeurs = sum_list valeurs"',
            section_v343,
            flags=re.DOTALL,
        )
        injection = re.search(
            r"lemma ponderation_bloc_complexe_of_real:(.*?)(?=\n(?:lemma|definition|text|section)\b)",
            section_v343,
            flags=re.DOTALL,
        )
        assert injection, "Lemme d'injection réel vers complexe introuvable"
        assert "complex_of_real" in injection.group(1)
        assert "ponderation_bloc cs vs" in injection.group(1)
        assert re.search(r"\b(?:by|proof)\b", injection.group(1))


# Non-régression des déclarations centrales existantes.
def test_central_regime_declarations_are_preserved(thy_content: str):
    for name in CENTRAL_REGIME_DECLARATIONS:
        assert re.search(
            rf"(?m)^\s*(?:lemma|theorem)\s+(?:\([^)]*\)\s+)?{re.escape(name)}\b",
            thy_content,
        ), f"Déclaration centrale manquante: {name}"
