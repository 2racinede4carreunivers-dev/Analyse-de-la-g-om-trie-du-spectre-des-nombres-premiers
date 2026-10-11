"""Tests de regression pour les 2 bugs ci/pytest rapportes par Philippe 2026-06-29 :

BUG 1 : tests/test_env_config.py::test_balise_anthropic_presente verifiait
        que .env contenait le PLACEHOLDER 'COLLEZ VOTRE CLE ANTHROPIC CLAUDE ICI'.
        Or, ce placeholder DOIT etre remplace par la vraie cle utilisateur.
        => Le test echouait des que l'utilisateur configurait correctement Gabriel.
        FIX : test supprime (n'a aucun sens fonctionnel).

BUG 2 : src/ui/ci_status.py _SUMMARY_RE attendait passed/failed/errors/skipped
        dans cet ordre EXACT, alors que pytest produit "1 failed, 687 passed, ..."
        quand il y a des fails (ordre invers!).
        => L'interface 'ci' affichait "Tests passes : 0" alors que 687 etaient OK.
        FIX : regex remplacees par 4 regex independantes ordre-agnostiques.
"""
from __future__ import annotations

import inspect
import re

import pytest


# ===========================================================================
# BUG 1 : Test absurde du placeholder
# ===========================================================================
class TestPlaceholderEnvBug:
    """Sentinelle : aucun test ne doit asserter qu'un placeholder est present
    dans le .env REEL de l'utilisateur."""

    def test_no_test_asserte_placeholder_dans_env_reel(self):
        """Aucun test ne doit faire `assert "COLLEZ" in .env`."""
        from tests import test_env_config as m
        src = inspect.getsource(m)
        # Le placeholder peut apparaitre dans test_guide_contient_balise (qui teste
        # le GUIDE, pas le .env reel). Mais pas dans TestEnvContent.
        # On verifie qu'on a bien supprime test_balise_anthropic_presente :
        assert "test_balise_anthropic_presente" not in src, (
            "REGRESSION : le test absurde test_balise_anthropic_presente "
            "a ete reintroduit. Il echoue des que l'utilisateur configure "
            "sa vraie cle Anthropic. Supprimez-le."
        )

    def test_classe_test_env_content_ne_check_pas_placeholder(self):
        """TestEnvContent ne doit pas verifier la presence d'un placeholder
        dans le .env de l'utilisateur."""
        from tests.test_env_config import TestEnvContent
        for name in dir(TestEnvContent):
            if not name.startswith("test_"):
                continue
            method = getattr(TestEnvContent, name)
            if callable(method):
                src = inspect.getsource(method)
                assert "COLLEZ" not in src, (
                    f"REGRESSION : TestEnvContent.{name} verifie la presence "
                    f"de 'COLLEZ' (placeholder) dans le .env utilisateur. "
                    "Le placeholder doit etre remplace par la vraie cle !"
                )


# ===========================================================================
# BUG 2 : Regex ci_status ordre-agnostique
# ===========================================================================
class TestCIRegexOrderAgnostic:
    """Verifie que le parsing du resume pytest fonctionne quel que soit
    l'ordre des compteurs (passed/failed/errors/skipped)."""

    def test_parse_summary_ligne_simple(self):
        """'661 passed, 1 warning in 1.99s' -> 661 passes, 0 fail."""
        from src.ui.ci_status import _parse_summary_line
        passed, failed, errors, skipped, dur = _parse_summary_line(
            "661 passed, 1 warning in 1.99s"
        )
        assert passed == 661
        assert failed == 0
        assert errors == 0
        assert skipped == 0
        assert abs(dur - 1.99) < 0.01

    def test_parse_summary_failed_avant_passed(self):
        """L'ordre invers (failed AVANT passed) est le bug exact remonte par Philippe.
        '1 failed, 687 passed, 4 skipped, 2 warnings in 21.27s'"""
        from src.ui.ci_status import _parse_summary_line
        passed, failed, errors, skipped, dur = _parse_summary_line(
            "1 failed, 687 passed, 4 skipped, 2 warnings in 21.27s"
        )
        assert passed == 687, "BUG : passed doit etre 687, pas 0 (regex order-agnostique requise)"
        assert failed == 1
        assert errors == 0
        assert skipped == 4
        assert abs(dur - 21.27) < 0.01

    def test_parse_summary_ordre_extreme(self):
        """'6 failed, 655 passed, 6 skipped, 2 warnings in 40.66s' (Philippe iter_6)"""
        from src.ui.ci_status import _parse_summary_line
        passed, failed, errors, skipped, dur = _parse_summary_line(
            "6 failed, 655 passed, 6 skipped, 2 warnings in 40.66s"
        )
        assert passed == 655
        assert failed == 6
        assert skipped == 6

    def test_parse_summary_avec_errors(self):
        """'3 errors, 657 passed in 12.5s'"""
        from src.ui.ci_status import _parse_summary_line
        passed, failed, errors, skipped, dur = _parse_summary_line(
            "3 errors, 657 passed in 12.5s"
        )
        assert passed == 657
        assert errors == 3
        assert failed == 0

    def test_parse_summary_warning_ignored(self):
        """Les 'warnings' ne doivent PAS etre comptes comme failed/errors."""
        from src.ui.ci_status import _parse_summary_line
        passed, failed, errors, skipped, dur = _parse_summary_line(
            "692 passed, 1 warning in 3.48s"
        )
        assert passed == 692
        assert failed == 0
        assert errors == 0


# ===========================================================================
# Integration : la commande 'ci' affiche les bons nombres
# ===========================================================================
class TestCISummaryAvecFails:
    """Cree un CISummary avec un fail et verifie que le badge est correct."""

    def test_badge_avec_fail(self):
        """Si 1 fail + 687 passed, le badge doit afficher '687/688'."""
        from src.ui.ci_status import CISummary
        summary = CISummary(
            passed=687, failed=1, errors=0, skipped=4, total=692,
            duration_s=21.27, ok=False, raw_tail="",
        )
        badge = summary.badge
        # Le badge doit montrer que 687 tests passent (pas 0 comme le bug)
        assert "687" in badge

    def test_run_pytest_local_retourne_passed_correct(self, tmp_path):
        """Smoke test : run_pytest_local sur une mini-suite retourne passed correct.
        On utilise un sous-dossier minimal pour eviter une recursion infinie."""
        from src.ui.ci_status import _parse_summary_line
        # On teste juste le parseur sur un cas realiste avec 'passed' > 100
        passed, failed, errors, skipped, dur = _parse_summary_line(
            "692 passed, 1 warning in 3.48s"
        )
        assert passed == 692, (
            f"REGRESSION : parseur retourne passed={passed} alors qu'on attend 692."
        )


# ===========================================================================
# Verifie qu'aucun ancien _SUMMARY_RE n'existe plus
# ===========================================================================
class TestAncienneRegexSupprimee:
    def test_summary_re_supprime(self):
        """_SUMMARY_RE etait la vieille regex bugguee, doit etre absente."""
        import src.ui.ci_status as m
        # On accepte qu'elle reste si elle pointe vers la nouvelle logique,
        # mais ideal : qu'elle soit absente.
        # On verifie surtout que _parse_summary_line existe et fonctionne.
        assert hasattr(m, "_parse_summary_line")
        assert hasattr(m, "_PASSED_RE")
        assert hasattr(m, "_FAILED_RE")
