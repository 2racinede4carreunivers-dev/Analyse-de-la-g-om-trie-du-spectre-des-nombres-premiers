"""
spectral_core.py  —  Moteur de calcul spectral principal
═══════════════════════════════════════════════════════════
CORRECTIONS appliquées (DEF-02 + DEF-03) :
  • SA/SB calculés via ratio_dispatcher (plus de constantes hardcodées)
  • Base = k (plus hardcodée à 2)
  • Invariant sélectionné selon formulas.symmetric_invariant
  • model fixé par dispatch, jamais par valeur par défaut interne
  • equation_holds seul n'est plus présenté comme preuve suffisante
═══════════════════════════════════════════════════════════
"""

import re
import logging
from fractions import Fraction
from dataclasses import dataclass

from ratio_dispatcher import dispatch_from_prompt, UnknownRatioError

logger = logging.getLogger("gabriel.spectral_core")


@dataclass
class SpectralResult:
    k:              int
    n:              int
    p:              int
    model:          str       # ex: '1/4'   — CORRECTION DEF-02
    base:           int
    SA:             float
    SB:             float
    SA_exact:       str
    SB_exact:       str
    digamma:        float
    p_reconstruit:  int
    equation_holds: bool
    invariant:      str       # invariant correct selon k — CORRECTION DEF-03
    provenance:     str = "SpectralCore"


class SpectralCore:
    """
    Résout la reconstruction du premier p par la méthode spectrale.

    CORRECTION DEF-02 : formules SA/SB lues depuis ratio_dispatcher.
    CORRECTION DEF-03 : invariant déterminé par formulas.symmetric_invariant.
    """

    def solve(self, user_prompt: str, p_candidate: int) -> SpectralResult:
        # 1. Dispatch — UnknownRatioError si ratio absent (CORRECTION DEF-01)
        ratio_str, formulas = dispatch_from_prompt(user_prompt)
        logger.info("SpectralCore : model=%r, prompt=%r", ratio_str, user_prompt[:60])

        # 2. Extraction de n
        m = re.search(r"n\s*=\s*(\d+)", user_prompt)
        if not m:
            raise ValueError("Paramètre n introuvable dans le prompt.")
        n = int(m.group(1))
        k = formulas.k

        # 3. Calcul SA et SB avec la bonne base (CORRECTION DEF-02)
        SA_frac = formulas.compute_SA(n)
        SB_frac = formulas.compute_SB(n)
        logger.info("SA(%d)=%s, SB(%d)=%s", n, SA_frac, n, SB_frac)

        # 4. Digamma et reconstruction
        dig_frac   = formulas.compute_digamma(n, p_candidate)
        p_rec      = formulas.reconstruct_prime(n, p_candidate)
        eq_holds   = (p_rec == p_candidate)

        # 5. Invariant correct selon k (CORRECTION DEF-03)
        invariant = formulas.invariant_label(n)
        logger.info("Invariant : %s", invariant)

        return SpectralResult(
            k             = k,
            n             = n,
            p             = p_candidate,
            model         = ratio_str,        # CORRECTION DEF-02
            base          = formulas.base,
            SA            = float(SA_frac),
            SB            = float(SB_frac),
            SA_exact      = str(SA_frac),
            SB_exact      = str(SB_frac),
            digamma       = float(dig_frac),
            p_reconstruit = p_rec,
            equation_holds= eq_holds,
            invariant     = invariant,        # CORRECTION DEF-03
        )


# ─────────────────────────────────────────────────────────
#  TESTS UNITAIRES
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests spectral_core ===")
    core   = SpectralCore()
    prompt = "Reconstruit le premier pour le rapport 1/4 pour n=23"
    result = core.solve(prompt, p_candidate=1097)

    assert result.model == "1/4",   f"model={result.model}"
    assert result.base  == 4,       f"base={result.base}"
    assert abs(result.SA - 88327434098004) < 1e4, f"SA={result.SA}"
    assert abs(result.SB - 353309736387924) < 1e5, f"SB={result.SB}"
    assert result.p_reconstruit == 1097, f"p={result.p_reconstruit}"
    assert "asymetrique" in result.invariant or "position != n" in result.invariant

    print(f"  OK  model     = {result.model!r}")
    print(f"  OK  base      = {result.base}")
    print(f"  OK  SA(23)    = {result.SA:.6e}")
    print(f"  OK  SB(23)    = {result.SB:.6e}")
    print(f"  OK  p rec     = {result.p_reconstruit}")
    print(f"  OK  invariant = {result.invariant}")
    print("\nTous les tests spectral_core : OK")
