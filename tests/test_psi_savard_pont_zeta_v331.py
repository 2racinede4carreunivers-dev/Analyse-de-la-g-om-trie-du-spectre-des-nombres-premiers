"""
Tests v3.31 (Philippe 2026-02) - Formule spectrale de Savard (pont psi/zeta).

Valide :
  1. La formule psi_savard reproduit numeriquement les deux exemples fournis
     par Philippe : psi(30, n=10) ~= 28.888 et psi(98, n=25) ~= 96.894.
  2. Les composants (2^n/SB(n), log10(2*pi), correction) sont exacts.
  3. La section XIII est bien presente dans methode_spectral.thy avec les
     definitions et les lemmes numeriques attendus.
  4. La conjecture est clairement documentee et NON demontree (statut
     honnete : pas de sorry, pas de theorem RH_holds).
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

from src.core.spectral_core import SpectralMethodCore


THY_PATH = Path(__file__).resolve().parents[1] / "theories" / "methode_spectral.thy"


@pytest.fixture(scope="module")
def core() -> SpectralMethodCore:
    return SpectralMethodCore()


@pytest.fixture(scope="module")
def thy_content() -> str:
    return THY_PATH.read_text(encoding="utf-8")


class TestNumericalMatchPhilippe:
    """La formule reproduit les valeurs annoncees par Philippe."""

    def test_prime_29_position_10(self, core):
        """psi_savard(x=30, n=10) doit valoir ~= 28.8881437."""
        r = core.compute_psi_savard(n=10, x=30.0)
        assert "error" not in r
        assert r["prime"] == 29
        assert r["SB_n"] == 3262
        assert r["power_2_n"] == 1024
        # Valeur attendue = 28.888143698...
        assert math.isclose(r["psi_savard"], 28.888143698680, abs_tol=1e-9)

    def test_prime_97_position_25(self, core):
        """psi_savard(x=98, n=25) doit valoir ~= 96.8941502."""
        r = core.compute_psi_savard(n=25, x=98.0)
        assert "error" not in r
        assert r["prime"] == 97
        assert r["SB_n"] == 109051838
        assert r["power_2_n"] == 33554432
        # Valeur attendue = 96.894150248...
        assert math.isclose(r["psi_savard"], 96.894150248989, abs_tol=1e-9)

    def test_default_x_is_prime_plus_one(self, core):
        """Sans x explicite, on doit prendre prime(n) + 1."""
        r10 = core.compute_psi_savard(n=10)
        assert r10["x"] == 30.0  # 29 + 1
        r25 = core.compute_psi_savard(n=25)
        assert r25["x"] == 98.0  # 97 + 1


class TestFormulaComponents:
    """Chaque composant de la formule est exact et bien exposé."""

    def test_terme_zeta_savard_at_10(self, core):
        r = core.compute_psi_savard(n=10, x=30.0)
        # 2^10 / SB(10) = 1024 / 3262
        assert math.isclose(r["terme_zeta_savard"], 1024 / 3262, rel_tol=1e-15)

    def test_terme_zeta_savard_at_25(self, core):
        r = core.compute_psi_savard(n=25, x=98.0)
        assert math.isclose(
            r["terme_zeta_savard"], 33554432 / 109051838, rel_tol=1e-15,
        )

    def test_log10_2pi_correct(self, core):
        r = core.compute_psi_savard(n=10, x=30.0)
        assert math.isclose(r["log10_2pi"], math.log10(2 * math.pi), rel_tol=1e-15)

    def test_citations_present(self, core):
        r = core.compute_psi_savard(n=10, x=30.0)
        assert any("psi_savard" in c for c in r["citations"])
        assert any("composite_pair_no_rsp_positions" in c for c in r["citations"])

    def test_conjecture_note(self, core):
        r = core.compute_psi_savard(n=10, x=30.0)
        assert "CONJECTURE" in r["note"].upper()


class TestErrorHandling:
    """Comportement robuste sur entrees invalides."""

    def test_n_out_of_range(self, core):
        r = core.compute_psi_savard(n=99999)
        assert "error" in r

    def test_n_zero(self, core):
        r = core.compute_psi_savard(n=0)
        assert "error" in r

    def test_x_below_one(self, core):
        r = core.compute_psi_savard(n=10, x=0.5)
        assert "error" in r


class TestIsabelleTheorySection:
    """La section XIII doit exister dans methode_spectral.thy."""

    def test_section_xiii_present(self, thy_content):
        assert "section \"XIII." in thy_content
        assert "Pont Savard" in thy_content

    def test_psi_savard_definition_present(self, thy_content):
        assert re.search(
            r"definition\s+psi_savard\s*::",
            thy_content,
        ), "definition psi_savard manquante"

    def test_rapport_zeta_savard_definition_present(self, thy_content):
        assert re.search(
            r"definition\s+rapport_zeta_savard\s*::",
            thy_content,
        )

    def test_log10_savard_definition_present(self, thy_content):
        assert re.search(
            r"definition\s+log10_savard\s*::",
            thy_content,
        )

    def test_lemma_rapport_at_10_present(self, thy_content):
        assert "rapport_zeta_savard_at_10" in thy_content

    def test_lemma_rapport_at_25_present(self, thy_content):
        assert "rapport_zeta_savard_at_25" in thy_content

    def test_three_pillars_referenced(self, thy_content):
        """Les 3 piliers (theoremes deja prouves) doivent etre cites."""
        assert "composite_not_prime_i" in thy_content
        assert "composite_no_reconstruction_position" in thy_content
        assert "composite_pair_no_rsp_positions" in thy_content

    def test_no_sorry_added_in_section_xiii(self, thy_content):
        """La section XIII ne doit contenir AUCUN sorry actif."""
        # Extrait la section XIII
        idx = thy_content.find("section \"XIII.")
        assert idx > 0
        # Fin : jusqu'a la section License
        end = thy_content.find("section \"License", idx)
        section_xiii = thy_content[idx:end] if end > 0 else thy_content[idx:]
        # Verifier qu'il n'y a pas de "sorry" hors commentaire
        # On tolere le mot "sorry" dans les commentaires (* ... *) ou text <open> ...
        # Recherche : ligne contenant 'sorry' seul (pas dans un texte)
        for line in section_xiii.splitlines():
            stripped = line.strip()
            if stripped.startswith("(*") or stripped.startswith("--"):
                continue
            # Ignorer les lignes dans les blocs text <open> ... <close>
            # (heuristique simple : chercher 'sorry' comme mot isole hors chaine)
            if re.search(r"\bsorry\b", stripped) and not stripped.startswith("(*"):
                # Verifier que ce n'est pas dans un text-block
                # (heuristique : ligne n'ayant pas de guillemets ni de mot francais)
                # Simple : refuse tout 'sorry' comme mot isole.
                pytest.fail(
                    f"'sorry' trouve dans la section XIII : {line!r}"
                )

    def test_no_axiomatization_in_section_xiii(self, thy_content):
        """Aucun axiomatization frauduleux dans XIII."""
        idx = thy_content.find("section \"XIII.")
        end = thy_content.find("section \"License", idx)
        section_xiii = thy_content[idx:end] if end > 0 else thy_content[idx:]
        assert "axiomatization" not in section_xiii, (
            "axiomatization trouve dans section XIII - le pont doit rester "
            "conjectural (texte), pas un axiome introduit."
        )

    def test_double_argument_documented(self, thy_content):
        """Les DEUX arguments (numerique + structurel) doivent etre documentes."""
        idx = thy_content.find("section \"XIII.")
        end = thy_content.find("section \"License", idx)
        section_xiii = thy_content[idx:end] if end > 0 else thy_content[idx:]
        assert "ARGUMENT 1" in section_xiii
        assert "ARGUMENT 2" in section_xiii
        # Verification numerique explicite pour les 2 exemples
        assert "28.888" in section_xiii or "28,888" in section_xiii
        assert "96.894" in section_xiii or "96,894" in section_xiii

    def test_statut_formel_explicite(self, thy_content):
        """v3.34 : Le statut affirmatif (theoreme du locale) doit etre documente.

        A la demande de Philippe (2026-02) la Section XIII n'est plus presentee
        comme une conjecture : dans le cadre du locale `ensemble_savard`, dont
        la SATISFAISABILITE est demontree (theoreme
        `ensemble_savard_satisfaisable`), l'egalite RsP = Re = 1/2 est un
        THEOREME (alignement_central, conclusion_ensemble, synthese_pont_savard).

        La vision structurelle Ensemble = 1/x + 1/t + 1/ms avec ses trois
        concordances (Tchebychev = psi_savard, zeros non-triviaux = positions,
        Re = 1/2 = RsP) doit etre presente.
        """
        idx = thy_content.find("section \"XIII.")
        end = thy_content.find("section \"License", idx)
        section_xiii = thy_content[idx:end] if end > 0 else thy_content[idx:]
        # La conclusion doit affirmer que RsP = Re = 1/2 est VRAI dans le locale
        assert "VRAI" in section_xiii or "theoreme" in section_xiii.lower()
        # La vision structurelle doit etre documentee
        assert "Ensemble" in section_xiii
        assert "trois concordances" in section_xiii.lower() or "3 concordances" in section_xiii.lower()
        # Le locale doit etre reference comme cadre formel
        assert "ensemble_savard" in section_xiii
        assert "satisfaisabilit" in section_xiii.lower() or "SATISFAISABILITE" in section_xiii

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
