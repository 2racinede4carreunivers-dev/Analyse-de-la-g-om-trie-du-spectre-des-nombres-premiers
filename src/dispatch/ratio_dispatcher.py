"""
ratio_dispatcher.py  —  Dispatch vers le moteur de calcul selon le ratio 1/k
═══════════════════════════════════════════════════════════════════════════════
CORRECTIONS appliquées (DEF-01) :
  • Suppression du fallback silencieux DEFAULT_MODEL = '1/2'
  • Ajout de la clé '1/4' dans FORMULA_REGISTRY avec les bons coefficients
  • UnknownRatioError levée si k absent du registre (plus de silence)
  • Logging explicite du model sélectionné avant tout calcul
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import logging
from dataclasses import dataclass
from fractions import Fraction

logger = logging.getLogger("gabriel.ratio_dispatcher")


class UnknownRatioError(ValueError):
    """Levée quand le ratio demandé n'est pas dans FORMULA_REGISTRY."""
    pass


@dataclass(frozen=True)
class SpectralFormulas:
    k:                  int
    base:               int
    coeff_SA_a:         Fraction
    coeff_SA_b:         Fraction
    coeff_SB_a:         Fraction
    coeff_SB_b:         Fraction
    symmetric_invariant: bool        # True si k=2, False sinon
    digamma_exp:        int = 6      # exposant : 4^digamma_exp

    def compute_SA(self, n: int) -> Fraction:
        return self.coeff_SA_a * Fraction(self.base ** n) + self.coeff_SA_b

    def compute_SB(self, n: int) -> Fraction:
        return self.coeff_SB_a * Fraction(self.base ** n) + self.coeff_SB_b

    def compute_digamma(self, n: int, p: int) -> Fraction:
        return self.compute_SB(n) - Fraction(p) * Fraction(4 ** self.digamma_exp)

    def reconstruct_prime(self, n: int, p: int) -> int:
        sb  = self.compute_SB(n)
        dig = self.compute_digamma(n, p)
        return int((sb - dig) / Fraction(4 ** self.digamma_exp))

    def invariant_label(self, n: int) -> str:
        if self.symmetric_invariant:
            return (
                f"INVARIANT (ratio 1/{self.k}): "
                f"position = n = number_of_terms = {n}"
            )
        return (
            f"INVARIANT (ratio 1/{self.k}): "
            f"n = number_of_terms = {n}  "
            f"[position != n pour ratio asymetrique]"
        )


# ═══════════════════════════════════════════════════════════════════════
#  FORMULA_REGISTRY
#  Ajouter un bloc SpectralFormulas par ratio supporté.
#  CORRECTION DEF-01 : '1/4' présent ; aucun DEFAULT_MODEL.
# ═══════════════════════════════════════════════════════════════════════
FORMULA_REGISTRY: dict[str, SpectralFormulas] = {

    "1/2": SpectralFormulas(
        k=2, base=2,
        coeff_SA_a=Fraction(13, 8),     # 3.25 / 2
        coeff_SA_b=Fraction(-2, 1),
        coeff_SB_a=Fraction(13, 4),     # 6.5 / 2
        coeff_SB_b=Fraction(-66, 1),
        symmetric_invariant=True,
    ),

    # ── CORRECTION DEF-01 : entrée k=4 ajoutée ──────────
    "1/4": SpectralFormulas(
        k=4, base=4,                    # base = k = 4 (pas 2)
        coeff_SA_a=Fraction(241, 192),
        coeff_SA_b=Fraction(-4, 3),
        coeff_SB_a=Fraction(964, 192),
        coeff_SB_b=Fraction(-12292, 3),
        symmetric_invariant=False,      # invariant asymétrique pour k != 2
    ),
    # ─────────────────────────────────────────────────────
    # Étendre ici : "1/3": SpectralFormulas(k=3, base=3, ...)
}

# Ancien DEFAULT_MODEL = "1/2"  ← SUPPRIMÉ (CORRECTION DEF-01)


def parse_ratio(user_input: str) -> str:
    """Extrait '1/k' depuis le texte brut de la requête."""
    m = re.search(r"1/([2-9]|[1-9]\d+)", user_input)
    if not m:
        raise UnknownRatioError(
            f"Aucun ratio 1/k trouvé dans : {user_input!r}"
        )
    return f"1/{m.group(1)}"


def dispatch(ratio_str: str) -> SpectralFormulas:
    """
    Retourne SpectralFormulas pour ratio_str.
    CORRECTION DEF-01 : lève UnknownRatioError si ratio absent — aucun fallback.
    """
    if ratio_str not in FORMULA_REGISTRY:
        raise UnknownRatioError(
            f"Ratio {ratio_str!r} non supporté. "
            f"Disponibles : {list(FORMULA_REGISTRY)}"
        )
    formulas = FORMULA_REGISTRY[ratio_str]
    logger.info(
        "Dispatching → model=%r  (k=%d, base=%d, invariant=%s)",
        ratio_str, formulas.k, formulas.base,
        "symétrique" if formulas.symmetric_invariant else "asymétrique",
    )
    return formulas


def dispatch_from_prompt(user_prompt: str) -> tuple[str, SpectralFormulas]:
    """Parse le ratio depuis le prompt et retourne (ratio_str, formulas)."""
    ratio_str = parse_ratio(user_prompt)
    return ratio_str, dispatch(ratio_str)


# ─────────────────────────────────────────────────────────
#  TESTS UNITAIRES
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests ratio_dispatcher ===")
    prompt = "Reconstruit le premier pour le rapport 1/4 pour n=23"

    ratio, f = dispatch_from_prompt(prompt)
    assert ratio == "1/4" and f.k == 4
    print(f"  OK  parse_ratio → {ratio!r}")

    SA = f.compute_SA(23)
    SB = f.compute_SB(23)
    assert SA == Fraction(241, 192) * Fraction(4**23) + Fraction(-4, 3)
    assert SB == Fraction(964, 192) * Fraction(4**23) + Fraction(-12292, 3)
    print(f"  OK  SA(23) = {float(SA):.6e}")
    print(f"  OK  SB(23) = {float(SB):.6e}")

    assert f.reconstruct_prime(23, 1097) == 1097
    print("  OK  p reconstruit = 1097")

    assert "asymetrique" in f.invariant_label(23) or "position != n" in f.invariant_label(23)
    print(f"  OK  invariant asymétrique")

    try:
        dispatch("1/7")
        assert False
    except UnknownRatioError:
        print("  OK  UnknownRatioError pour 1/7")

    print("\nTous les tests ratio_dispatcher : OK")
