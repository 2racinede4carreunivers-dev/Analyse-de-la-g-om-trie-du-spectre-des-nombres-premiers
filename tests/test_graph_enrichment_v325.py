"""
Tests v3.25 : enrichissement des graphiques (Philippe 2026-02).

Verifie que chaque type de courbe fournit :
  1. Un titre explicite (avec formule ou contexte)
  2. Des axes orthographies (labels descriptifs, pas juste "n")
  3. Un resume critique (max 750 caracteres) explicant :
     - ce que le graphique MONTRE
     - ce qu'il NE MONTRE PAS
     - la source (methode_spectral.thy si applicable)
  4. Une legende d'axes exploitable
  5. Un primary_label descriptif (pas le simple enum value "SA_SB")
"""
from __future__ import annotations

import pytest

from src.core.spectral_core import SpectralMethodCore
from src.visualization.curves import CurveKind, compute_curve


@pytest.fixture(scope="module")
def core() -> SpectralMethodCore:
    return SpectralMethodCore()


# =====================================================================
# GARANTIES SUR TOUS LES TYPES DE COURBES
# =====================================================================


ALL_KINDS_LINEAR = [
    (CurveKind.SA, 1, 15),
    (CurveKind.SB, 1, 15),
    (CurveKind.SA_SB, 1, 15),
    (CurveKind.DIGAMMA, 1, 15),
    (CurveKind.INVARIANT, 1, 15),
    (CurveKind.RATIO_SA_SB, 1, 15),
    (CurveKind.GAP, 1, 15),
    (CurveKind.PRIME, 1, 15),
]


@pytest.mark.parametrize("kind,n_min,n_max", ALL_KINDS_LINEAR)
class TestGraphEnrichmentV325:
    """Chaque type de courbe DOIT fournir les champs enrichis."""

    def test_title_is_descriptive(self, core, kind, n_min, n_max):
        c = compute_curve(core, kind, n_min, n_max)
        assert len(c.title) > 20, (
            f"Titre trop court pour {kind.value} : {c.title!r}. "
            f"Doit contenir formule + range."
        )
        assert f"n = {n_min}" in c.title or f"n={n_min}" in c.title, (
            f"Titre doit mentionner le range n : {c.title!r}"
        )

    def test_x_label_orthographic(self, core, kind, n_min, n_max):
        c = compute_curve(core, kind, n_min, n_max)
        # Doit contenir "indice" ou "position" (nom orthographie), pas juste "n"
        low = c.x_label.lower()
        assert any(kw in low for kw in ["indice", "position", "n :"]), (
            f"x_label trop court/opaque pour {kind.value} : {c.x_label!r}. "
            f"Doit expliquer ce qu'est n."
        )

    def test_y_label_orthographic(self, core, kind, n_min, n_max):
        c = compute_curve(core, kind, n_min, n_max)
        assert len(c.y_label) > 5, (
            f"y_label trop court pour {kind.value} : {c.y_label!r}"
        )

    def test_critical_summary_present(self, core, kind, n_min, n_max):
        c = compute_curve(core, kind, n_min, n_max)
        assert c.critical_summary != "", (
            f"critical_summary vide pour {kind.value}"
        )

    def test_critical_summary_max_750_chars(self, core, kind, n_min, n_max):
        """Contrainte Philippe 2026-02 : max 750 caracteres."""
        c = compute_curve(core, kind, n_min, n_max)
        assert len(c.critical_summary) <= 750, (
            f"critical_summary depasse 750 char ({len(c.critical_summary)}) "
            f"pour {kind.value}"
        )

    def test_critical_summary_scholarly_structure(self, core, kind, n_min, n_max):
        """Le resume critique doit dire ce qu'il MONTRE ET ce qu'il NE MONTRE PAS."""
        c = compute_curve(core, kind, n_min, n_max)
        low = c.critical_summary.lower()
        assert "graphique" in low or "trace" in low, (
            f"critical_summary doit decrire ce qu'il trace pour {kind.value}"
        )
        # Note critique : mention explicite de ce que le graphique ne montre pas
        assert "ne montre pas" in low or "n'affiche pas" in low, (
            f"critical_summary doit avoir une clause 'NE MONTRE PAS' pour {kind.value}. "
            f"Trouve : {c.critical_summary}"
        )

    def test_axis_legend_populated(self, core, kind, n_min, n_max):
        c = compute_curve(core, kind, n_min, n_max)
        assert len(c.axis_legend) >= 2, (
            f"axis_legend doit avoir au moins 2 entrees pour {kind.value}. "
            f"Trouve : {c.axis_legend}"
        )
        # La cle "n" doit toujours etre presente (c'est l'axe X commun)
        assert "n" in c.axis_legend, (
            f"axis_legend doit contenir 'n' comme cle pour {kind.value}"
        )

    def test_primary_label_readable(self, core, kind, n_min, n_max):
        c = compute_curve(core, kind, n_min, n_max)
        # Ne doit pas etre le nom brut de l'enum (ex: "SA_SB")
        assert c.primary_label != "", (
            f"primary_label vide pour {kind.value}"
        )
        assert "_" not in c.primary_label or "(n)" in c.primary_label, (
            f"primary_label ne doit pas ressembler a un enum brut pour {kind.value}. "
            f"Trouve : {c.primary_label!r}"
        )


# =====================================================================
# CAS SPECIFIQUE : DIGAMMA
# =====================================================================


class TestDigammaClarity:
    """
    Philippe (2026-02) : soupcon que le graphique digamma ne corresponde pas
    a la question posee. Verifie que le titre et le resume levent toute
    ambiguite sur la formule et le ratio specifique (1/2).
    """

    def test_digamma_title_mentions_ratio_1_2(self, core):
        c = compute_curve(core, CurveKind.DIGAMMA, 1, 15)
        assert "1/2" in c.title, (
            f"Le titre digamma DOIT mentionner le ratio 1/2 pour lever "
            f"toute ambiguite (constante 64 est specifique a ce ratio). "
            f"Trouve : {c.title!r}"
        )

    def test_digamma_summary_warns_about_ratio_specificity(self, core):
        c = compute_curve(core, CurveKind.DIGAMMA, 1, 15)
        low = c.critical_summary.lower()
        assert "1/2" in low, "Le resume digamma doit mentionner le ratio 1/2"
        # Doit avertir que la constante 64 est SPECIFIQUE au ratio
        assert any(kw in low for kw in ["specifique", "attention", "1/3"]), (
            f"Le resume digamma doit avertir que la constante 64 est specifique "
            f"au ratio 1/2 (pas 1/3, 1/4). Trouve : {c.critical_summary}"
        )

    def test_digamma_formula_explicit(self, core):
        c = compute_curve(core, CurveKind.DIGAMMA, 1, 15)
        assert "64" in c.formula, (
            f"La formule digamma doit contenir 64 (constante specifique 1/2). "
            f"Trouve : {c.formula!r}"
        )
        assert "128/2" in c.formula or "= 128" in c.formula, (
            f"La formule doit expliquer que 64 = 128/2. Trouve : {c.formula!r}"
        )


# =====================================================================
# TRUNCATION DEFENSIVE
# =====================================================================


class TestCriticalSummaryTruncation:
    """Verifie que __post_init__ tronque bien a 750 caracteres."""

    def test_manually_long_summary_gets_truncated(self):
        from src.visualization.curves import CurveData, CurveKind
        long_text = "A" * 1000
        c = CurveData(
            kind=CurveKind.SA,
            n_min=1, n_max=10, scale="linear",
            title="T", x_label="X", y_label="Y",
            points=[],
            critical_summary=long_text,
        )
        assert len(c.critical_summary) <= 750
        assert c.critical_summary.endswith("...")

    def test_exactly_750_chars_not_truncated(self):
        from src.visualization.curves import CurveData, CurveKind
        text = "A" * 750
        c = CurveData(
            kind=CurveKind.SA,
            n_min=1, n_max=10, scale="linear",
            title="T", x_label="X", y_label="Y",
            points=[],
            critical_summary=text,
        )
        assert len(c.critical_summary) == 750
        assert not c.critical_summary.endswith("...")

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
