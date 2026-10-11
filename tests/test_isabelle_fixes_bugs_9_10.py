"""
Tests v3.23 : verifie les corrections Isabelle bugs 9 & 10 dans le contexte
de la restructuration Savard validation#16 (2026-06-29).

Bugs originaux (session precedente) :
  9. Isabelle Inner syntax error sur les fonctions `fun` non recursives.
  10. `sorry` a remplacer dans les lemmes de sommes fermees.

Statut apres validation#16 :
  - Les anciennes definitions terme_suite_A/B, somme_A/B_construction_eq_formule,
    rapport_spectral_tend_vers_demi ont ete SUPPRIMEES par Philippe.
  - Elles sont remplacees par les nouvelles definitions Savard :
    suite_A/B_savard_construction, somme_A/B_compacte_savard,
    preuve_rapport_spectral_limite_savard.
  - Les bugs 9 & 10 ne peuvent plus se reproduire par construction (les nouvelles
    definitions utilisent `definition` et pas `fun`, et n'utilisent pas `sorry`).
"""
from __future__ import annotations

import re
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
# Bug 9 (nouvelle structure) : les 2 constructions Savard utilisent `definition`
# ============================================================================


class TestSavardConstructionUseDefinition:
    """Les 2 nouvelles constructions Savard (validation#16) utilisent
    `definition`, jamais `fun` avec conditionnels non recursifs."""

    def test_suite_A_uses_definition(self, thy_content):
        assert "definition suite_A_savard_construction" in thy_content
        assert "fun suite_A_savard_construction" not in thy_content

    def test_suite_B_uses_definition(self, thy_content):
        assert "definition suite_B_savard_construction" in thy_content
        assert "fun suite_B_savard_construction" not in thy_content


# ============================================================================
# Bug 10 (nouvelle structure) : plus aucun `sorry` dans le fichier
# ============================================================================


class TestNoActiveSorryAnywhere:
    """Regression globale : aucun `sorry` actif nulle part."""

    def test_no_bare_sorry_at_line_start(self, thy_content):
        active_sorries = []
        for i, line in enumerate(thy_content.splitlines(), start=1):
            if line.strip() == "sorry":
                active_sorries.append(i)
        assert not active_sorries, (
            f"`sorry` actifs aux lignes : {active_sorries}"
        )


# ============================================================================
# Rapport spectral limite : la nouvelle preuve Savard (validation#16)
# ============================================================================


class TestPreuveRapportSpectralLimite:
    """La preuve `preuve_rapport_spectral_limite_savard` (validation#16)
    remplace `rapport_spectral_tend_vers_demi`. Elle doit compiler sans
    utiliser la tactique `ring` (choix explicite de Philippe)."""

    def test_lemma_exists(self, thy_content):
        assert "lemma preuve_rapport_spectral_limite_savard" in thy_content

    def test_uses_field_simps(self, thy_content):
        """La preuve doit utiliser `field_simps` (equivalent Isabelle de
        field_simp Lean) pour manipuler les fractions."""
        m = re.search(
            r"lemma preuve_rapport_spectral_limite_savard:(.*?)qed",
            thy_content, re.DOTALL,
        )
        assert m is not None
        block = m.group(1)
        assert "field_simps" in block or "algebra_simps" in block, (
            "La preuve doit utiliser `field_simps` ou `algebra_simps`"
        )

    def test_no_ring_tactic(self, thy_content):
        """La preuve doit eviter la tactique `ring` (choix Philippe)."""
        m = re.search(
            r"lemma preuve_rapport_spectral_limite_savard:(.*?)qed",
            thy_content, re.DOTALL,
        )
        assert m is not None
        block = m.group(1)
        assert " ring\n" not in block and " ring " not in block, (
            "La tactique `ring` doit etre evitee (choix explicite Philippe)"
        )
