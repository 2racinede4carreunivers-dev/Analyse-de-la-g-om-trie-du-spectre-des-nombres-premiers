"""
Tests v3.32 (Philippe 2026-06) - Section XIII professionnelle : Le Pont Savard.

Valide :
  1. Les deux NOUVELLES verifications numeriques de Philippe :
     psi_savard(228, n=49) ~= 226.894132 et psi_savard(-100, n=-26) ~= -100.7981582
     (regime negatif desormais supporte par compute_psi_savard).
  2. La Section XIII reecrite professionnellement :
     - locale ensemble_savard (hypotheses coherentes, PAS d'axiomatisation),
     - theoreme de satisfaisabilite (temoin RsP 1 2),
     - alignement central 1/ms3 = 1/y2 (ms_rapport = zeta_critique),
     - theoremes pont_spectral_direct_final et synthese_pont_savard,
     - nomenclature originale de l'auteur documentee (y1..y3, t, ms1..ms3),
     - AUCUN axiome contradictoire (l'ancienne axiomatisation AX1-AX11
       impliquait 1 = 3 et a ete remplacee).
  3. Unification : une seule definition psi_savard (plus de doublon
     Psi_savard / Sb_n non definie).
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


@pytest.fixture(scope="module")
def section_xiii(thy_content) -> str:
    idx = thy_content.find('section "XIII.')
    assert idx > 0, "section XIII introuvable"
    end = thy_content.find('section "License', idx)
    return thy_content[idx:end] if end > 0 else thy_content[idx:]


class TestNumericalNewCasesPhilippe:
    """Les 2 nouveaux exemples numeriques de Philippe (228 et -100)."""

    def test_prime_227_position_49(self, core):
        """psi_savard(x=228, n=49) doit valoir ~= 226.894132."""
        r = core.compute_psi_savard(n=49, x=228.0)
        assert "error" not in r
        assert r["prime"] == 227
        assert r["SB_n"] == 1829587348619198
        assert r["power_2_n"] == 562949953421312
        assert math.isclose(r["psi_savard"], 226.894132001183, abs_tol=1e-9)

    def test_regime_negatif_x_moins_100(self, core):
        """psi_savard(x=-100, n=-26) doit valoir ~= -100.7981582."""
        r = core.compute_psi_savard(n=-26, x=-100.0)
        assert "error" not in r
        assert r["prime"] == -101
        assert r["regime"] == "negatif"
        assert math.isclose(r["psi_savard"], -100.798158152322, abs_tol=1e-9)

    def test_regime_negatif_default_x(self, core):
        """Sans x explicite pour n=-26, x = -101 + 1 = -100."""
        r = core.compute_psi_savard(n=-26)
        assert r["x"] == -100.0

    def test_regime_positif_flag(self, core):
        r = core.compute_psi_savard(n=10, x=30.0)
        assert r["regime"] == "positif"

    def test_n_zero_toujours_rejete(self, core):
        assert "error" in core.compute_psi_savard(n=0)

    def test_x_dans_moins_1_plus_1_rejete(self, core):
        """|x| <= 1 doit etre rejete (log10(1 - 1/x^2) non defini)."""
        assert "error" in core.compute_psi_savard(n=-26, x=-0.5)
        assert "error" in core.compute_psi_savard(n=10, x=0.5)


class TestSectionXIIIProfessionnelle:
    """Structure de la Section XIII reecrite."""

    def test_titre_professionnel(self, thy_content):
        assert 'section "XIII. Le Pont Savard' in thy_content

    def test_locale_ensemble_savard(self, section_xiii):
        assert "locale ensemble_savard" in section_xiii

    def test_symboles_professionnels(self, section_xiii):
        for sym in (
            "zeta_tchebychev", "zeta_critique", "zeta_positions",
            "tau_savard", "ms_reconstruction", "ms_exclusion", "ms_rapport",
        ):
            assert sym in section_xiii, f"symbole {sym} manquant"

    def test_hypotheses_du_locale(self, section_xiii):
        assert "hypothese_critique" in section_xiii
        assert "pont_fonctionnel" in section_xiii
        assert "rapport_un_demi" in section_xiii

    def test_theoremes_du_pont(self, section_xiii):
        for thm in (
            "theorem (in ensemble_savard) alignement_central",
            "theorem (in ensemble_savard) alignement_inverse",
            "theorem (in ensemble_savard) conclusion_ensemble",
            "theorem ensemble_savard_satisfaisable",
            "theorem pont_spectral_direct_final",
            "theorem synthese_pont_savard",
        ):
            assert thm in section_xiii, f"{thm} manquant"

    def test_satisfaisabilite_via_rsp(self, section_xiii):
        """Le temoin de coherence est le vrai rapport spectral RsP 1 2."""
        assert "RsP 1 2" in section_xiii
        assert "RsP_un_demi_general" in section_xiii

    def test_nomenclature_auteur_documentee(self, section_xiii):
        """La nomenclature originale (y1..y3, t, ms1..ms3) reste documentee."""
        for token in ("1/y1", "1/y2", "1/y3", "1/t", "1/ms1", "1/ms2", "1/ms3"):
            assert token in section_xiii, f"nomenclature {token} manquante"

    def test_validation_numerique_228(self, section_xiii):
        assert "rapport_zeta_savard_at_49" in section_xiii
        assert "psi_savard_at_49_228_expanded" in section_xiii
        assert "226.894132" in section_xiii

    def test_cas_negatif_documente(self, section_xiii):
        assert "-100.7981582" in section_xiii

    def test_aucune_axiomatisation(self, section_xiii):
        """Plus aucun 'axiomatization' dans la section XIII."""
        assert "axiomatization" not in section_xiii

    def test_ancienne_axiomatisation_contradictoire_supprimee(self, thy_content):
        """AX1..AX11 (E=1 vs E=3, incoherent) doivent avoir disparu."""
        for ax in ("AX1:", "AX8:", "psi_Psavard", "Validation_Savard_global"):
            assert ax not in thy_content, f"{ax} encore present"

    def test_doublon_psi_savard_supprime(self, thy_content):
        """Une seule definition psi_savard, plus de Psi_savard/Sb_n."""
        assert len(re.findall(r"definition\s+psi_savard\s*::", thy_content)) == 1
        assert 'consts\n  Sb_n' not in thy_content
        assert "definition Psi_savard" not in thy_content

    def test_aucun_sorry(self, section_xiii):
        for line in section_xiii.splitlines():
            stripped = line.strip()
            if stripped.startswith("(*") or stripped.startswith("--"):
                continue
            assert not re.search(r"\bsorry\b", stripped), f"sorry trouve : {line!r}"

    def test_statut_honnete(self, section_xiii):
        """v3.34 (Philippe 2026-02) : le "statut honnete" devient un statut
        AFFIRMATIF. Dans le cadre du locale `ensemble_savard`, RsP = Re = 1/2
        n'est plus une conjecture mais un THEOREME du locale (satisfaisabilite
        demontree). La Section XIII doit :
          - affirmer explicitement RsP = Re = 1/2 comme VRAI,
          - referencer le locale ensemble_savard comme cadre formel,
          - documenter les trois concordances de l'auteur.
        """
        # Affirmation forte : RsP = Re = 1/2 est VRAI dans le cadre du locale
        assert "VRAI" in section_xiii
        # Trois concordances documentees
        assert "1/y1" in section_xiii and "1/y2" in section_xiii and "1/y3" in section_xiii
        assert "1/ms1" in section_xiii and "1/ms3" in section_xiii
        # Cadre formel : locale + satisfaisabilite
        assert "ensemble_savard" in section_xiii
        # Universalite mentionnee
        assert "UNIVERSALITE" in section_xiii or "universel" in section_xiii.lower()

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
