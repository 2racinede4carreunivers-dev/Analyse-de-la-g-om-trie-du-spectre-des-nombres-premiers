"""
Tests v3.21 : vérifie les corrections Isabelle/HOL signalées par Philippe
(2026-07-04) après ouverture du fichier .thy dans Isabelle.

Bugs corrigés :
1-6. Les 6 lemmes `composite_X_not_prime` (X = 4, 9, 15, 51, 91, 121)
     doivent utiliser une preuve par TÉMOIN EXPLICITE (exhibition d'un
     diviseur) car `by (auto simp: prime_nat_iff)` échoue chez Isabelle.
7-8. Les théorèmes `composite_no_reconstruction_position` et
     `no_reconstruction_for_{4,9,15,51,91,121}` avaient une erreur de type :
     `SB (real n)` alors que `SB :: nat => real` accepte un `nat`.
11.  Le lemme `rapport_spectral_tend_vers_demi` utilise maintenant
     `by (simp add: field_simps)` au lieu de `by simp`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="module")
def thy_content() -> str:
    thy = ROOT / "theories" / "methode_spectral.thy"
    return thy.read_text(encoding="utf-8")


# ============================================================================
# Fix bugs 1-6 : preuves par témoin explicite
# ============================================================================

class TestCompositeProofsHaveExplicitWitness:
    """Les 6 lemmes composite_X_not_prime doivent utiliser une preuve par
    témoin explicite (pattern `dvd` + prime_nat_iff), pas le raccourci
    `by (auto simp: prime_nat_iff)` qui échoue dans Isabelle."""

    @pytest.mark.parametrize("value,witness", [
        (4, 2),
        (9, 3),
        (15, 3),
        (51, 3),
        (91, 7),
        (121, 11),
    ])
    def test_lemma_uses_witness_pattern(self, thy_content, value, witness):
        # Le lemme doit contenir `(witness::nat) dvd value` comme témoin
        expected_witness = f"({witness}::nat) dvd {value}"
        assert expected_witness in thy_content, (
            f"Le lemme composite_{value}_not_prime doit exhiber le témoin "
            f"'{expected_witness}' (diviseur non trivial de {value})"
        )

    def test_no_auto_simp_prime_nat_iff_shortcut(self, thy_content):
        """Le raccourci `by (auto simp: prime_nat_iff)` doit avoir disparu
        des 6 lemmes de non-primalité (Isabelle ne le résout pas)."""
        # On tolère la mention dans les commentaires mais pas comme tactique
        # directe sous un lemme composite_X_not_prime.
        # Recherche : "composite_N_not_prime" suivi de "by (auto simp: prime_nat_iff)"
        # dans la même zone (max 200 chars entre les 2).
        import re
        problematic = re.findall(
            r"composite_\d+_not_prime.{1,200}by \(auto simp:\s*prime_nat_iff\)",
            thy_content, re.DOTALL,
        )
        assert not problematic, (
            f"Un lemme composite_X_not_prime utilise encore le raccourci "
            f"`by (auto simp: prime_nat_iff)` qui echoue : {problematic}"
        )

    def test_uses_metis_prime_nat_iff_instead(self, thy_content):
        """Les preuves finalisent avec `by (metis prime_nat_iff)` (ou similaire)."""
        # Chaque lemme doit avoir "metis prime_nat_iff" dans sa preuve
        count = thy_content.count("by (metis prime_nat_iff)")
        assert count >= 6, (
            f"Attendu au moins 6 occurrences de 'by (metis prime_nat_iff)' "
            f"(une par lemme composite), trouvé {count}"
        )


# ============================================================================
# Fix bugs 7-8 : corrections de type SB(n) / digamma_calc(n, C)
# ============================================================================

class TestReconstructionTheoremTypeCorrect:
    """Le théorème composite_no_reconstruction_position ne doit PLUS
    utiliser `SB (real n)` ni `digamma_calc (real n) (real C)` — ces
    fonctions attendent des `nat`, pas des `real`."""

    def test_main_theorem_no_real_wrapper_around_sb(self, thy_content):
        # Extrait le bloc du théorème
        import re
        m = re.search(
            r"theorem composite_no_reconstruction_position:(.*?)qed\n",
            thy_content, re.DOTALL,
        )
        assert m is not None
        block = m.group(1)
        # `SB (real n)` NE DOIT PLUS apparaître
        assert "SB (real n)" not in block, (
            "composite_no_reconstruction_position ne doit plus wrapper "
            "n dans `real` avant SB (SB attend un nat)"
        )
        assert "digamma_calc (real n)" not in block, (
            "digamma_calc attend deux nat, pas des real"
        )
        # `SB n` doit apparaître (forme correcte)
        assert "SB n" in block

    @pytest.mark.parametrize("value", [4, 9, 15, 51, 91, 121])
    def test_numerical_corollaries_no_real_wrapper(self, thy_content, value):
        import re
        m = re.search(
            rf"theorem no_reconstruction_for_{value}:(.*?)by simp",
            thy_content, re.DOTALL,
        )
        assert m is not None
        block = m.group(1)
        assert "SB (real n)" not in block, (
            f"no_reconstruction_for_{value} ne doit plus wrapper n dans real"
        )
        # Doit référencer digamma_calc n <value> (sans wrapper real)
        assert f"digamma_calc n {value}" in block, (
            f"no_reconstruction_for_{value} doit utiliser 'digamma_calc n {value}' "
            f"(sans real wrapper)"
        )


# ============================================================================
# Fix bug 11 : preuve_rapport_spectral_limite_savard utilise field_simps
# (renommee dans validation#16 de `rapport_spectral_tend_vers_demi`)
# ============================================================================

class TestRapportSpectralUsesFieldSimps:
    def test_lemma_uses_field_simps(self, thy_content):
        import re
        # Validation#16 : le lemme s'appelle maintenant
        # `preuve_rapport_spectral_limite_savard`
        m = re.search(
            r"lemma preuve_rapport_spectral_limite_savard:(.*?)qed",
            thy_content, re.DOTALL,
        )
        assert m is not None, (
            "Le lemme `preuve_rapport_spectral_limite_savard` doit exister "
            "(remplace `rapport_spectral_tend_vers_demi` en validation#16)"
        )
        block = m.group(1)
        assert "field_simps" in block or "algebra_simps" in block, (
            "preuve_rapport_spectral_limite_savard doit utiliser "
            "`field_simps` ou `algebra_simps` pour manipuler les fractions"
        )
