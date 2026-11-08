"""Tests pytest pour Gabriel v5.2 - HOL/Isabelle Formal Code Generation.

Convertit l'ancien script `test_gabriel_v5.2.py` en suite pytest propre.
Les tests dependants d'un module non present (`memory.prompt_injector_enhanced`)
sont skippes avec un message clair.

Conformement a la convention pytest : nom de fichier sans point dans la racine.
"""
from __future__ import annotations

import pytest


# --------------------------------------------------------------------------
# Test 1 : HOL/Isabelle Formal Generator (operationnel)
# --------------------------------------------------------------------------
class TestHOLFormalGenerator:
    """Verifie que le generateur produit du code Isabelle formel correct."""

    @pytest.fixture
    def generator(self):
        from src.hol_isabelle_formal_generator import HOLIsabelleResponseGenerator
        return HOLIsabelleResponseGenerator()

    def test_isabelle_theory_generation_non_empty(self, generator):
        """La generation doit produire une theorie Isabelle non vide."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        assert isinstance(isabelle, str)
        assert len(isabelle) > 1000, "Theorie generee trop courte"

    def test_isabelle_has_theory_header(self, generator):
        """La theorie generee doit commencer par 'theory Spectral_Primes'."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        # Le nom peut etre 'Spectral_Primes' ou 'Spectral_Primes_Savard' selon la version
        assert "theory Spectral_Primes" in isabelle

    def test_isabelle_has_definition_A(self, generator):
        """La theorie doit definir la suite A : nat ⇒ real."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        assert "definition A ::" in isabelle
        # Doit utiliser le type nat ⇒ real (ou nat => real selon encoding)
        assert ("nat ⇒ real" in isabelle) or ("nat => real" in isabelle)

    def test_isabelle_formula_A_correct(self, generator):
        """La formule A(n) = (13/8) * 2^n - 2 doit etre presente (conforme .thy)."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        # Plusieurs formes acceptees
        formula_variants = [
            "A n = (13 / 8) * (2 ^ n) - 2",
            "A n = (13/8) * (2 ^ n) - 2",
            "(13 / 8) * (2 ^ n) - 2",
        ]
        assert any(v in isabelle for v in formula_variants), (
            f"Aucune variante de la formule A(n) trouvee dans la theorie generee"
        )

    def test_isabelle_has_digamma(self, generator):
        """La theorie doit definir digamma."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        assert "definition digamma" in isabelle

    def test_isabelle_has_theorem(self, generator):
        """La theorie doit contenir au moins un theoreme."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        assert "theorem " in isabelle

    def test_isabelle_ends_properly(self, generator):
        """La theorie doit se terminer par 'end' (fermeture Isabelle)."""
        isabelle = generator.generate_isabelle_spectral_theory("Reconstruction primes")
        assert isabelle.rstrip().endswith("end")


# --------------------------------------------------------------------------
# Test 2-4 : Prompt Injector Enhanced (module non present, skip)
# --------------------------------------------------------------------------
class TestPromptInjectorEnhanced:
    """Tests dependant de `memory.prompt_injector_enhanced` (non livre).

    Ces tests sont conserves pour reference mais skippes : le module
    `memory.prompt_injector_enhanced` n'est pas present dans l'arborescence.
    A reactiver une fois le module ajoute.
    """

    @pytest.fixture
    def injector(self):
        pytest.importorskip(
            "memory.prompt_injector_enhanced",
            reason="Module memory.prompt_injector_enhanced non present dans le repo"
        )
        from memory.prompt_injector_enhanced import PromptInjector
        return PromptInjector()

    def test_query_type_detection_hol(self, injector):
        detected = injector.detect_query_type("Génère théorie HOL pour RSA")
        assert "hol" in detected.lower()

    def test_query_type_detection_rsa(self, injector):
        detected = injector.detect_query_type("Calcule RSA([2], [3,5])")
        assert "rsa" in detected.lower()

    def test_query_type_detection_riemann(self, injector):
        detected = injector.detect_query_type("Explique zéros Riemann")
        assert "riemann" in detected.lower()

    def test_hol_strict_injection(self, injector):
        injected = injector.inject_for_claude_hol(
            "Génère théorie Isabelle pour reconstruction premiers"
        )
        assert "SPÉCIFICATIONS HOL4/ISABELLE/LEAN4 FORMELLES STRICTES" in injected
        assert "definition A ::" in injected

    def test_hol_validation_good_code(self, injector):
        good_code = """
theory Spectral_Primes imports Main begin
definition A :: "nat ⇒ real" where
  "A n = (13 / 8) * (2 ^ n) - 2"
theorem convergence: "∀ k. P k"
end
"""
        val = injector.validate_llm_response(good_code, "hol_proof_generation")
        assert val["is_compliant"] is True
        assert val["score"] >= 0.5

    def test_hol_validation_pseudo_code_rejected(self, injector):
        bad_code = """
fun A(n) = (3.25 / 2) * (2 pow n) - 2
fun digamma_calcule(n, p) = B(n) - 64 * p
"""
        val = injector.validate_llm_response(bad_code, "hol_proof_generation")
        # Le pseudo-code doit echouer ou avoir un score bas
        assert (val["is_compliant"] is False) or (val["score"] < 0.5)


# --------------------------------------------------------------------------
# Test 5 : Integration Gabriel v5.2 (necessite injector + safe budget)
# --------------------------------------------------------------------------
class TestGabrielV52Integration:
    """Test d'integration : Gabriel + Injector + Safe Budget."""

    def test_gabriel_safe_budget_available(self):
        """Le module GabrielLLMIntegrationSafeBudget doit etre importable."""
        try:
            from src.gabriel_llm_integration_safe import GabrielLLMIntegrationSafeBudget
        except ImportError as exc:
            pytest.skip(f"Module gabriel_llm_integration_safe non disponible : {exc}")
        assert GabrielLLMIntegrationSafeBudget is not None

    def test_full_integration_skipped_if_injector_missing(self):
        """Integration complete : skip si l'injector manque."""
        try:
            from memory.prompt_injector_enhanced import PromptInjector  # noqa: F401
        except ImportError:
            pytest.skip("memory.prompt_injector_enhanced non present, integration complete non testable")
        # Si on arrive ici, l'integration est possible
        from src.gabriel_llm_integration_safe import GabrielLLMIntegrationSafeBudget
        gabriel = GabrielLLMIntegrationSafeBudget(monthly_budget_usd=7.0)
        assert gabriel is not None
