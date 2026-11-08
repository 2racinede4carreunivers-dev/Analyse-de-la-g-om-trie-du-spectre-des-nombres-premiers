"""
spectral_model.py  —  Registre des formules spectrales par ratio k
════════════════════════════════════════════════════════════════════
CORRECTION appliquée (DEF-04) :
  • Bloc k=4 ajouté dans FORMULA_REGISTRY
  • base = k pour chaque entrée (pas hardcodée à 2)
  • get_formulas(k) lève KeyError si k non supporté (plus de fallback)
════════════════════════════════════════════════════════════════════
"""

from fractions import Fraction
from dataclasses import dataclass


@dataclass(frozen=True)
class SpectralFormulas:
    """Formules spectrales pour un ratio 1/k donné."""
    k:           int
    base:        int
    coeff_SA_a:  Fraction     # SA(n) = coeff_SA_a * base^n + coeff_SA_b
    coeff_SA_b:  Fraction
    coeff_SB_a:  Fraction     # SB(n) = coeff_SB_a * base^n + coeff_SB_b
    coeff_SB_b:  Fraction
    symmetric:   bool         # True si k=2

    def compute_SA(self, n: int) -> Fraction:
        return self.coeff_SA_a * Fraction(self.base ** n) + self.coeff_SA_b

    def compute_SB(self, n: int) -> Fraction:
        return self.coeff_SB_a * Fraction(self.base ** n) + self.coeff_SB_b


FORMULA_REGISTRY: dict[str, SpectralFormulas] = {

    "1/2": SpectralFormulas(
        k=2, base=2,
        coeff_SA_a=Fraction(13, 8),
        coeff_SA_b=Fraction(-2, 1),
        coeff_SB_a=Fraction(13, 4),
        coeff_SB_b=Fraction(-66, 1),
        symmetric=True,
    ),

    # ── CORRECTION DEF-04 : entrée k=4 ──────────────────
    "1/4": SpectralFormulas(
        k=4, base=4,                       # base = 4, PAS 2
        coeff_SA_a=Fraction(241, 192),
        coeff_SA_b=Fraction(-4, 3),
        coeff_SB_a=Fraction(964, 192),
        coeff_SB_b=Fraction(-12292, 3),
        symmetric=False,
    ),

    # ── Entrée k=3 (ratio 1/3) ───────────────────────────
    "1/3": SpectralFormulas(
        k=3, base=3,
        coeff_SA_a=Fraction(73, 108),
        coeff_SA_b=Fraction(-3, 2),
        coeff_SB_a=Fraction(219, 108),
        coeff_SB_b=Fraction(-1461, 2),
        symmetric=False,
    ),
    # ─────────────────────────────────────────────────────
}


def get_formulas(k: int) -> SpectralFormulas:
    """
    Retourne SpectralFormulas pour 1/k.
    CORRECTION DEF-04 : lève KeyError si k absent — aucun fallback vers k=2.
    """
    key = f"1/{k}"
    if key not in FORMULA_REGISTRY:
        raise KeyError(
            f"Ratio '1/{k}' non supporté. Disponibles : {list(FORMULA_REGISTRY)}"
        )
    return FORMULA_REGISTRY[key]


# ─────────────────────────────────────────────────────────
#  TESTS UNITAIRES
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests spectral_model ===")
    f4 = get_formulas(4)
    SA = f4.compute_SA(23)
    SB = f4.compute_SB(23)

    assert SA == Fraction(241, 192) * Fraction(4**23) + Fraction(-4, 3)
    assert SB == Fraction(964, 192) * Fraction(4**23) + Fraction(-12292, 3)
    assert f4.base == 4 and not f4.symmetric
    print(f"  OK  SA(23) k=4 = {float(SA):.6e}")
    print(f"  OK  SB(23) k=4 = {float(SB):.6e}")
    print(f"  OK  base=4, symmetric=False")

    f2 = get_formulas(2)
    assert f2.base == 2 and f2.symmetric
    print("  OK  k=2 : base=2, symmetric=True")

    try:
        get_formulas(7)
        assert False
    except KeyError:
        print("  OK  KeyError pour k=7")

    print("\nTous les tests spectral_model : OK")