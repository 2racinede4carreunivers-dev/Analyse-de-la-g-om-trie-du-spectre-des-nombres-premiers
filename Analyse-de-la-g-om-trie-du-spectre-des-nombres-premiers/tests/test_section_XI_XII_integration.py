"""Tests pytest pour Section XI et XII de methode_spectral.thy.

Verifie :
  - Module memory.methode_spectral_section_XII charge et helpers fonctionnent
  - 11/11 OK Suite A pour n=1 a 11 (constructions term-by-term)
  - 3/3 OK Suite B pour n=8, 9, 10 (avec substitution position 6)
  - Sommes fermees identiques aux constructions terme-a-terme pour n>=3
  - Theoreme RsP_k = 1/k verifie numeriquement pour k=2,3,4
  - Adaptateur RAG detecte les nouveaux regimes XI/XII
  - Le fichier methode_spectral.thy passe le static-check
"""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _resolve_theory_path(filename: str = "methode_spectral.thy") -> Path:
    """Resout le chemin du fichier .thy en testant plusieurs emplacements.

    En local : ROOT/theories/<filename>.
    Dans Docker : /theories/<filename> (mount externe), /home/agent/app/theories/<filename>,
    ou le chemin ROOT classique.
    """
    import os as _os
    candidates = [
        Path(_os.environ.get("GABRIEL_THEORIES_DIR", "")) / filename,
        ROOT / "theories" / filename,
        Path("/theories") / filename,
        Path("/home/agent/app/theories") / filename,
        Path("/app/agent-multiloop-Gabriel-local/theories") / filename,
    ]
    for c in candidates:
        if c.exists():
            return c
    return ROOT / "theories" / filename  # default (sera caught by assert)


# =============================================================================
# Section XII : verifications numeriques des helpers
# =============================================================================
class TestSectionXIIHelpers:
    """Verifie les helpers de calcul de Section XII."""

    @pytest.fixture(autouse=True)
    def _setup(self):
        from memory.methode_spectral_section_XII import (
            construire_suite_A, construire_suite_B,
            somme_A_pos, somme_B_pos,
            somme_A_neg, somme_B_neg,
        )
        self.construire_A = construire_suite_A
        self.construire_B = construire_suite_B
        self.somme_A_pos = somme_A_pos
        self.somme_B_pos = somme_B_pos
        self.somme_A_neg = somme_A_neg
        self.somme_B_neg = somme_B_neg

    @pytest.mark.parametrize("n,expected", [
        (1,  [2]),
        (2,  [2, 3]),
        (3,  [2, 3, 6]),
        (4,  [2, 4, 6, 12]),
        (5,  [2, 4, 8, 12, 24]),
        (6,  [2, 4, 8, 16, 24, 48]),
        (7,  [2, 4, 8, 16, 32, 48, 96]),
        (8,  [2, 4, 8, 16, 32, 64, 96, 192]),
        (9,  [2, 4, 8, 16, 32, 64, 128, 192, 384]),
        (10, [2, 4, 8, 16, 32, 64, 128, 256, 384, 768]),
        (11, [2, 4, 8, 16, 32, 64, 128, 256, 512, 768, 1536]),
    ])
    def test_construction_suite_A_k2(self, n, expected):
        """Suite A pour k=2, a_1=2, doit correspondre aux exemples Savard."""
        got = self.construire_A(2, n)
        assert got == [Fraction(x) for x in expected]

    @pytest.mark.parametrize("n,expected", [
        (8,  [2, 4, 8, 16, 32, 128, 192, 384]),
        (9,  [2, 4, 8, 16, 32, 128, 256, 384, 768]),
        (10, [2, 4, 8, 16, 32, 128, 256, 512, 768, 1536]),
    ])
    def test_construction_suite_B_k2(self, n, expected):
        """Suite B pour k=2 avec substitution position 6 (n >= 8)."""
        got = self.construire_B(2, n)
        assert got == [Fraction(x) for x in expected]

    def test_suite_B_egale_suite_A_si_n_lt_8(self):
        """Pour n < 8, suite B = suite A (pas de substitution)."""
        for n in range(1, 8):
            assert self.construire_B(2, n) == self.construire_A(2, n)

    @pytest.mark.parametrize("n,expected", [
        (3, Fraction(11)),
        (4, Fraction(24)),
        (5, Fraction(50)),
        (6, Fraction(102)),
        (7, Fraction(206)),
        (8, Fraction(414)),
        (10, Fraction(1662)),
    ])
    def test_somme_construction_egale_formule_fermee_n_ge_3(self, n, expected):
        """Pour n>=3 : sum(construction A) = somme_A_pos_k(2, n) = SA(n)."""
        sum_construction = sum(self.construire_A(2, n))
        formule = self.somme_A_pos(2, n)
        assert sum_construction == expected
        assert formule == expected

    def test_somme_negative_savard(self):
        """Verification des sommes negatives confirmees par Philippe Savard."""
        # -2 (1er negatif, 1 terme) = -3/8
        assert self.somme_A_neg(2, 1) == Fraction(-3, 8)
        # -5 (3eme negatif, 3 termes) = -51/32 = -1.59375
        assert self.somme_A_neg(2, 3) == Fraction(-51, 32)
        # -47 (15eme negatif, 15 termes)
        expected_m47 = Fraction(13, 4) / Fraction(2) ** 15 - Fraction(2)
        assert self.somme_A_neg(2, 15) == expected_m47

    @pytest.mark.parametrize("k", [2, 3, 4])
    def test_theoreme_rapport_spectral_universel(self, k):
        """Theoreme : RsP_k(k, n1, n2) = 1/k pour k in {2,3,4}."""
        n1, n2 = 5, 8
        A_diff = self.somme_A_pos(k, n1) - self.somme_A_pos(k, n2)
        B_diff = self.somme_B_pos(k, n1) - self.somme_B_pos(k, n2)
        assert A_diff / B_diff == Fraction(1, k)


# =============================================================================
# Section XI et XII : enregistrement dans le RAG
# =============================================================================
class TestSectionsXIXIIEnregistrement:
    def test_section_XI_module_charge(self):
        from memory.methode_spectral_section_XI import get_section_XI_entries
        entries = get_section_XI_entries()
        assert len(entries) >= 8
        codes = {e["metadata"]["code"] for e in entries}
        # 8 regles XI.1 a XI.8
        assert "XI.1" in codes
        assert "XI.5" in codes  # substitution position 6 dans suite B

    def test_section_XII_module_charge(self):
        from memory.methode_spectral_section_XII import get_section_XII_entries
        entries = get_section_XII_entries()
        assert len(entries) >= 10
        codes = {e["metadata"]["code"] for e in entries}
        assert "XII.1" in codes
        assert "XII.9" in codes  # theoreme RsP_k

    def test_regimes_XI_XII_dans_dictionnaire(self):
        from memory.dictionnaire_spectral import DICTIONNAIRE_SPECTRAL
        assert "regime_construction_termes" in DICTIONNAIRE_SPECTRAL
        assert "regime_parametrique_1_k" in DICTIONNAIRE_SPECTRAL
        # Verifie que les 10 anciens regimes existent toujours
        anciens = [
            "regime_1_2_positif", "regime_mixte", "regime_1_4", "regime_1_3",
            "regime_negatif", "ecarts_spectraux", "invariants_transition",
            "geometrie_critique", "blocs_asymetriques", "suites_finies",
        ]
        for r in anciens:
            assert r in DICTIONNAIRE_SPECTRAL, f"Regime ancien {r} disparu !"

    def test_adaptateur_RAG_detecte_construction(self):
        from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral
        ad = AdaptateurCognitifSpectral()
        analyse = ad.analyser("Construis-moi la suite A pour 7 termes en k=2")
        assert "regime_construction_termes" in analyse.regimes_detectes

    def test_adaptateur_RAG_detecte_parametrique(self):
        from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral
        ad = AdaptateurCognitifSpectral()
        analyse = ad.analyser("alpha_A et alpha_B pour rapport spectral 1/k")
        assert "regime_parametrique_1_k" in analyse.regimes_detectes


# =============================================================================
# Fichier .thy : static-check Isabelle
# =============================================================================
class TestTheoryFile:
    def test_methode_spectral_thy_existe(self):
        thy_path = _resolve_theory_path("methode_spectral.thy")
        assert thy_path.exists(), (
            f"methode_spectral.thy introuvable parmi les emplacements teste(s). "
            f"Defini GABRIEL_THEORIES_DIR pour pointer vers le dossier theories."
        )

    def test_methode_spectral_thy_static_check(self):
        """Le static-check passe (0 erreur). Warnings autorises."""
        thy_path = _resolve_theory_path("methode_spectral.thy")
        if not thy_path.exists():
            pytest.skip(f"methode_spectral.thy introuvable a {thy_path}")
        # Le script de static-check vit dans le repo, pas dans le mount theories
        script_candidates = [
            ROOT / "scripts" / "isabelle_static_check.py",
            Path("/home/agent/app/scripts/isabelle_static_check.py"),
            Path("/app/agent-multiloop-Gabriel-local/scripts/isabelle_static_check.py"),
        ]
        script = next((s for s in script_candidates if s.exists()), None)
        if script is None:
            pytest.skip("isabelle_static_check.py introuvable")
        result = subprocess.run(
            [sys.executable, str(script), str(thy_path)],
            capture_output=True, text=True, check=False,
        )
        assert result.returncode == 0, f"static-check FAIL:\n{result.stdout}"
        assert "RESULT: OK" in result.stdout or "RESULT: PASS" in result.stdout
