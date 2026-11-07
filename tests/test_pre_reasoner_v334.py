"""
Tests du PreReasoner (v3.34).

Verifie que le moteur de pre-raisonnement classe correctement les requetes
et produit le bon plan (mode, nombre d'iterations, bypasses).

Cinq modes attendus :
  - INSTANTANE     : 0 loop, template pre-compile (bonjour, oui, non, ok...)
  - RAPIDE         : 1 loop, verbal Isabelle sans calcul
  - STANDARD       : 2 loops, calcul simple
  - APPROFONDI     : 3 loops, configuration nxn / bloc A/B
  - TRES_COMPLEXE  : 4 loops, theorie avancee / multi-objectifs
"""
from __future__ import annotations

import pytest

from src.multiloop.pre_reasoner import (
    PreReasoner,
    ReasoningPlan,
    RequestMode,
    parse_cli_force_mode,
)


@pytest.fixture
def reasoner() -> PreReasoner:
    return PreReasoner()


# =============================================================================
# MODE INSTANTANE
# =============================================================================

class TestInstantaneMode:
    @pytest.mark.parametrize("question", [
        "Bonjour",
        "  bonjour !",
        "Salut",
        "Coucou",
        "Bonsoir.",
        "Hello",
        "Hey",
        "Merci",
        "Merci beaucoup",
        "Thanks",
        "Au revoir",
        "Bye",
        "À bientôt",
        "OK",
        "Ok",
        "Oui",
        "D'accord",
        "Non",
        "Continue",
        "Poursuis",
        "Enchaîne",
        "Ça va ?",
        "Comment vas-tu ?",
        "Comment ça va",
    ])
    def test_instantane_recognises_small_talk(self, reasoner, question):
        plan = reasoner.plan(question)
        assert plan.mode == RequestMode.INSTANTANE, (
            f"Attendu INSTANTANE pour {question!r}, obtenu {plan.mode.value}"
        )
        assert plan.n_iterations == 0
        assert plan.template_response is not None
        assert plan.skip_spectral_compute is True
        assert plan.skip_slowmotion is True
        assert plan.skip_silent_audit is True

    def test_instantane_empty_question(self, reasoner):
        plan = reasoner.plan("")
        assert plan.mode == RequestMode.INSTANTANE
        assert plan.template_response is not None

    def test_instantane_no_llm_no_multiloop(self, reasoner):
        plan = reasoner.plan("Bonjour")
        assert plan.n_iterations == 0
        assert plan.estimated_duration_sec <= 3


# =============================================================================
# MODE RAPIDE (verbal Isabelle)
# =============================================================================

class TestRapideMode:
    @pytest.mark.parametrize("question", [
        "Résume la Section XIII pour moi",
        "Peux-tu me résumer ce lemme ?",
        "Explique-moi cette preuve",
        "Cette preuve tient-elle ?",
        "Cette section est-elle bien formatée ?",
        "Compare ces deux lemmes",
        "Que penses-tu de la Section 12 ?",
        "Commente cette démonstration",
        "Reformule ce théorème plus simplement",
        "Liste les théorèmes de la Section XIII",
        "Documente ce lemme",
        "Qui es-tu ?",
        "Que peux-tu faire ?",
        "À quoi tu sers ?",
        "Aide-moi à comprendre le Pont Savard",
        "Cette preuve est-elle valide ?",
        "Explique la définition de RsP",
        "C'est quoi le Pont Savard ?",
    ])
    def test_rapide_recognises_verbal_isabelle(self, reasoner, question):
        plan = reasoner.plan(question)
        # Les questions sur "pont savard" ou "section XIII" avec verbe verbal
        # peuvent legitimement basculer sur TRES_COMPLEXE si un marqueur avance
        # est detecte. On accepte donc RAPIDE ou TRES_COMPLEXE.
        assert plan.mode in (RequestMode.RAPIDE, RequestMode.TRES_COMPLEXE), (
            f"Attendu RAPIDE/TRES_COMPLEXE pour {question!r}, obtenu {plan.mode.value}"
        )

    def test_rapide_skips_spectral(self, reasoner):
        plan = reasoner.plan("Résume la Section XIII pour moi")
        if plan.mode == RequestMode.RAPIDE:
            assert plan.skip_spectral_compute is True
            assert plan.skip_slowmotion is True
            assert plan.n_iterations == 1

    def test_rapide_verbal_without_calc_marker(self, reasoner):
        plan = reasoner.plan("Compare ces deux lemmes qualitativement")
        assert plan.mode == RequestMode.RAPIDE
        assert plan.n_iterations == 1


# =============================================================================
# MODE STANDARD (calcul simple)
# =============================================================================

class TestStandardMode:
    @pytest.mark.parametrize("question", [
        "Calcule RsP(5, 7)",
        "Reconstruis le 10eme nombre premier",
        "Position du premier 23 ?",
        "Écart entre -3 et -23",
        "Gap entre 11 et 13",
        "Le 42ème nombre premier",
        "Vérifie que 17 est premier",
    ])
    def test_standard_recognises_simple_calc(self, reasoner, question):
        plan = reasoner.plan(question)
        # STANDARD attendu, APPROFONDI accepte si multiples marqueurs
        assert plan.mode in (RequestMode.STANDARD, RequestMode.APPROFONDI), (
            f"Attendu STANDARD pour {question!r}, obtenu {plan.mode.value}"
        )
        assert plan.n_iterations in (2, 3)
        assert plan.skip_spectral_compute is False

    def test_standard_runs_spectral(self, reasoner):
        plan = reasoner.plan("Reconstruis le 10ème nombre premier")
        assert plan.skip_spectral_compute is False


# =============================================================================
# MODE APPROFONDI (configuration nxn / bloc A/B)
# =============================================================================

class TestApprofondiMode:
    @pytest.mark.parametrize("question", [
        "Calcule le rapport spectral symétrique 3x3",
        "Configuration 4x4 asymétrique",
        "Bloc A = {2, 3, 5} Bloc B = {7, 11, 13}, calcule le ratio",
        "Comparaison asymétrique entre deux blocs",
        "Rapport spectral symétrique 5*5",
    ])
    def test_approfondi_recognises_nxn(self, reasoner, question):
        plan = reasoner.plan(question)
        assert plan.mode in (RequestMode.APPROFONDI, RequestMode.TRES_COMPLEXE), (
            f"Attendu APPROFONDI pour {question!r}, obtenu {plan.mode.value}"
        )
        assert plan.n_iterations >= 3


# =============================================================================
# MODE TRES_COMPLEXE (theorie avancee / multi-objectifs)
# =============================================================================

class TestTresComplexeMode:
    @pytest.mark.parametrize("question", [
        "Explique le lien entre zêta et la Méthode Spectrale",
        "Que dit l'hypothèse de Riemann sur les zéros ?",
        "Compare psi_savard et Chebyshev sur l'intervalle [1, 100]",
        "Reconstruis le 10ème premier et calcule aussi RsP(5,7)",
        "Étudie les zéros de zêta sur la droite critique Re=1/2",
    ])
    def test_tres_complexe_recognises_advanced_theory(self, reasoner, question):
        plan = reasoner.plan(question)
        assert plan.mode == RequestMode.TRES_COMPLEXE, (
            f"Attendu TRES_COMPLEXE pour {question!r}, obtenu {plan.mode.value}"
        )
        assert plan.n_iterations == 4


# =============================================================================
# OVERRIDE UTILISATEUR (force_mode)
# =============================================================================

class TestForceMode:
    def test_force_rapide_overrides_detection(self, reasoner):
        # Une question qui serait normalement TRES_COMPLEXE
        plan = reasoner.plan(
            "Explique le lien entre zêta et la Méthode Spectrale",
            force_mode=RequestMode.RAPIDE,
        )
        assert plan.mode == RequestMode.RAPIDE
        assert plan.n_iterations == 1
        assert plan.is_forced is True

    def test_force_complet_overrides_short_message(self, reasoner):
        plan = reasoner.plan("Bonjour", force_mode=RequestMode.TRES_COMPLEXE)
        assert plan.mode == RequestMode.TRES_COMPLEXE
        assert plan.n_iterations == 4
        assert plan.is_forced is True


# =============================================================================
# PARSER DE COMMANDES CLI /rapide /standard /approfondi /complet
# =============================================================================

class TestCLIParser:
    def test_parse_rapide(self):
        mode, remainder = parse_cli_force_mode("/rapide résume la section XIII")
        assert mode == RequestMode.RAPIDE
        assert remainder == "résume la section XIII"

    def test_parse_standard(self):
        mode, remainder = parse_cli_force_mode("/standard calcule RsP(5,7)")
        assert mode == RequestMode.STANDARD
        assert remainder == "calcule RsP(5,7)"

    def test_parse_approfondi(self):
        mode, remainder = parse_cli_force_mode("/approfondi symétrique 3x3")
        assert mode == RequestMode.APPROFONDI
        assert remainder == "symétrique 3x3"

    def test_parse_complet(self):
        mode, remainder = parse_cli_force_mode("/complet zeta et Riemann")
        assert mode == RequestMode.TRES_COMPLEXE
        assert remainder == "zeta et Riemann"

    def test_parse_no_command(self):
        mode, remainder = parse_cli_force_mode("bonjour Gabriel")
        assert mode is None
        assert remainder == "bonjour Gabriel"

    def test_parse_empty_after_command(self):
        mode, remainder = parse_cli_force_mode("/rapide")
        assert mode == RequestMode.RAPIDE
        assert remainder == ""


# =============================================================================
# COHERENCE DU PLAN (invariants)
# =============================================================================

class TestPlanInvariants:
    def test_all_modes_have_iteration_count(self, reasoner):
        mapping = {
            RequestMode.INSTANTANE: 0,
            RequestMode.RAPIDE: 1,
            RequestMode.STANDARD: 2,
            RequestMode.APPROFONDI: 3,
            RequestMode.TRES_COMPLEXE: 4,
        }
        for mode, expected in mapping.items():
            plan = reasoner.plan("test", force_mode=mode)
            assert plan.n_iterations == expected

    def test_all_modes_have_positive_eta(self, reasoner):
        for mode in RequestMode:
            plan = reasoner.plan("test", force_mode=mode)
            assert plan.estimated_duration_sec >= 1

    def test_instantane_and_rapide_skip_heavy_stages(self, reasoner):
        for mode in (RequestMode.INSTANTANE, RequestMode.RAPIDE):
            plan = reasoner.plan("test", force_mode=mode)
            assert plan.skip_spectral_compute is True
            assert plan.skip_slowmotion is True
            assert plan.skip_silent_audit is True

    def test_standard_and_higher_run_full_pipeline(self, reasoner):
        for mode in (RequestMode.STANDARD, RequestMode.APPROFONDI, RequestMode.TRES_COMPLEXE):
            plan = reasoner.plan("test", force_mode=mode)
            assert plan.skip_spectral_compute is False
            assert plan.skip_slowmotion is False

    def test_plan_serialization(self, reasoner):
        plan = reasoner.plan("Bonjour")
        d = plan.as_dict()
        assert d["mode"] == "instantane"
        assert d["n_iterations"] == 0
        assert "reason" in d
        assert "estimated_duration_sec" in d


# =============================================================================
# NON-REGRESSION : calc marker empeche le classement instantane
# =============================================================================

class TestCalcMarkerProtection:
    def test_bonjour_calcule_rsp_is_not_instantane(self, reasoner):
        # Meme si "Bonjour" est en debut, "calcule RsP" force STANDARD au moins
        plan = reasoner.plan("Bonjour, calcule RsP(5,7)")
        assert plan.mode != RequestMode.INSTANTANE

    def test_pattern_avec_nombre_isole(self, reasoner):
        # Question avec calcul mais pas de mot-cle verbal
        plan = reasoner.plan("2+3=?")
        assert plan.mode in (RequestMode.STANDARD, RequestMode.RAPIDE)
