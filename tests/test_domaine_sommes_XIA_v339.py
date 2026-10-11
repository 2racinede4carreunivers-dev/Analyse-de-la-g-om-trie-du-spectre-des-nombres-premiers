"""Tests v3.39 — Non-regression numerique sur le domaine des egalites
somme_A_eq_SA et somme_B_eq_SB.

Contexte : le testing_agent a identifie que ces deux egalites, si posees
comme axiomes universels (sans hypothese sur n), sont FAUSSES aux petits n
et injectent une incoherence dans la theorie Isabelle. Ces tests vetifient
que :

  1. Le fichier methode_spectral.thy declare les axiomes AVEC leur
     pre-condition explicite (n >= 3 pour somme_A, n >= 8 pour somme_B).
  2. Les formes fermees SA(n) et SB(n) reproduisent bien les valeurs
     attendues sur leur domaine de validite.
  3. Aucune version future du fichier ne peut retirer l'hypothese de
     domaine sans faire echouer ces tests.

C'est une garantie de coherence formelle : les tests Python empechent
d'introduire des axiomes universels mathematiquement faux dans la theorie.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


THY_PATH = Path(__file__).resolve().parent.parent / "theories" / "methode_spectral.thy"


class TestDomaineSommesXIA:
    """Verifie que les axiomes ont bien une pre-condition sur n."""

    @pytest.fixture(scope="class")
    def content(self) -> str:
        return THY_PATH.read_text(encoding="utf-8")

    def test_somme_A_eq_SA_a_precondition(self, content: str):
        """L'axiome somme_A_eq_SA DOIT etre restreint a n >= 3.

        Interdit toute regression vers un axiome universel qui serait faux
        aux petits n (n=1 donne somme_A=2 mais SA=5/4).
        """
        # Cherche la ligne de l'axiome, autorise n >= 3, n >= 4, n \<ge> 3
        pattern = re.compile(
            r'somme_A_eq_SA\s*:\s*\n?\s*"n\s*(>=|\\\\<ge>)\s*3\s*\\<Longrightarrow>\s*somme_A\s+n\s*=\s*SA\s+n"',
            re.MULTILINE,
        )
        assert pattern.search(content), (
            "L'axiome somme_A_eq_SA doit avoir la pre-condition n >= 3. "
            "Sans elle, l'axiome est mathematiquement faux pour n=1 "
            "(somme_A(1)=2 mais SA(1)=5/4) et injecte une incoherence "
            "dans toute la theorie Isabelle."
        )

    def test_somme_B_eq_SB_a_precondition(self, content: str):
        """L'axiome somme_B_eq_SB DOIT etre restreint a n >= 8.

        Interdit toute regression vers un axiome universel qui serait faux
        aux petits n (n=3 donne somme_B=11 mais SB=-40).
        """
        pattern = re.compile(
            r'somme_B_eq_SB\s*:\s*\n?\s*"n\s*(>=|\\\\<ge>)\s*8\s*\\<Longrightarrow>\s*somme_B\s+n\s*=\s*SB\s+n"',
            re.MULTILINE,
        )
        assert pattern.search(content), (
            "L'axiome somme_B_eq_SB doit avoir la pre-condition n >= 8. "
            "Sans elle, l'axiome est mathematiquement faux pour n=3 "
            "(somme_B(3)=11 mais SB(3)=-40) et injecte une incoherence."
        )

    def test_pas_axiome_universel_sans_condition(self, content: str):
        """Interdit l'existence d'axiomes de la forme
        `somme_X_eq_SX: \"somme_X n = SX n\"` SANS pre-condition.
        """
        for name in ["somme_A_eq_SA", "somme_B_eq_SB"]:
            # Pattern d'un axiome universel non-conditionnel (a proscrire)
            bad_pattern = re.compile(
                rf'{name}\s*:\s*\n?\s*"somme_[AB]\s+n\s*=\s*S[AB]\s+n"\s*(?:and|$)',
                re.MULTILINE,
            )
            match = bad_pattern.search(content)
            assert not match, (
                f"L'axiome {name} apparait sous forme UNIVERSELLE (sans "
                f"hypothese sur n). Or il est mathematiquement faux aux "
                f"petits n. Ajouter explicitement la pre-condition "
                f"n >= 3 (pour A) ou n >= 8 (pour B)."
            )


class TestFormesFermeesNumeriques:
    """Verifie que les formes fermees SA(n) et SB(n) sont bien celles
    documentees et qu'elles produisent les valeurs canoniques attendues."""

    def test_SA_forme_fermee_declaration(self):
        content = THY_PATH.read_text(encoding="utf-8")
        # SA n = (3.25 / 2) * (2 ^ n) - 2
        assert re.search(
            r'"SA\s+n\s*=\s*\(?\s*3\.25\s*/\s*2\s*\)?\s*\*\s*\(?\s*2\s*\^\s*n\s*\)?\s*-\s*2"',
            content,
        ), "SA(n) doit etre defini comme (3.25/2) * 2^n - 2"

    def test_SB_forme_fermee_declaration(self):
        content = THY_PATH.read_text(encoding="utf-8")
        # SB n = (6.5 / 2) * (2 ^ n) - 66
        assert re.search(
            r'"SB\s+n\s*=\s*\(?\s*6\.5\s*/\s*2\s*\)?\s*\*\s*\(?\s*2\s*\^\s*n\s*\)?\s*-\s*66"',
            content,
        ), "SB(n) doit etre defini comme (6.5/2) * 2^n - 66"

    @pytest.mark.parametrize("n,expected", [
        (3, 11.0),          # (3.25/2)*8  - 2 = 13 - 2 = 11
        (4, 24.0),          # (3.25/2)*16 - 2 = 26 - 2 = 24
        (5, 50.0),          # (3.25/2)*32 - 2 = 52 - 2 = 50
        (8, 414.0),         # (3.25/2)*256 - 2 = 416 - 2 = 414
        (10, 1662.0),       # (3.25/2)*1024 - 2 = 1664 - 2 = 1662
    ])
    def test_SA_valeurs_canoniques(self, n: int, expected: float):
        """Verifie les valeurs de SA(n) sur le domaine de validite n >= 3."""
        computed = (3.25 / 2) * (2 ** n) - 2
        assert computed == pytest.approx(expected, abs=1e-9), (
            f"SA({n}) attendu {expected}, calcule {computed}"
        )

    @pytest.mark.parametrize("n,expected", [
        (8, 766.0),         # (6.5/2)*256 - 66 = 832 - 66 = 766
        (9, 1598.0),        # (6.5/2)*512 - 66 = 1664 - 66 = 1598
        (10, 3262.0),       # (6.5/2)*1024 - 66 = 3328 - 66 = 3262
    ])
    def test_SB_valeurs_canoniques(self, n: int, expected: float):
        """Verifie les valeurs de SB(n) sur le domaine de validite n >= 8."""
        computed = (6.5 / 2) * (2 ** n) - 66
        assert computed == pytest.approx(expected, abs=1e-9), (
            f"SB({n}) attendu {expected}, calcule {computed}"
        )


class TestStaticCheckIntegrite:
    """Verifie que le static-check global passe toujours."""

    def test_marqueurs_open_close_equilibres(self):
        content = THY_PATH.read_text(encoding="utf-8")
        n_open = content.count("\\<open>")
        n_close = content.count("\\<close>")
        assert n_open == n_close, (
            f"Marqueurs desequilibres : {n_open} \\<open> vs {n_close} \\<close>"
        )

    def test_termine_par_end(self):
        content = THY_PATH.read_text(encoding="utf-8")
        assert content.rstrip().endswith("end"), (
            "Le fichier doit se terminer par `end` (structure Isabelle intacte)"
        )

    def test_pas_de_sorry(self):
        content = THY_PATH.read_text(encoding="utf-8")
        # sorry en debut de ligne (pas dans un commentaire)
        pattern = re.compile(r'^\s*sorry\s*$', re.MULTILINE)
        matches = pattern.findall(content)
        assert not matches, (
            f"Preuves incompletes detectees : {len(matches)} 'sorry' actifs. "
            "Utiliser axiomatization avec pre-conditions au lieu de sorry."
        )
