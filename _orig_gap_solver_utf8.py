"""
GAP SOLVER - Formule CORRECTE pour n├®gatifs.

COMPR├ëHENSION FINALE :

Pour les nombres N├ëGATIFS, l'ordre est INVERS├ë :
  Position -1 = -2 (1er premier n├®gatif, le PLUS GRAND)
  Position -2 = -3 (2e premier n├®gatif)
  Position -3 = -5 (3e premier n├®gatif)
  Position -4 = -7 (4e premier n├®gatif)
  ...
  Position -8 = -19 (8e premier n├®gatif, le PLUS PETIT dans notre exemple)

Pour (-19, -5) :
  Position(-19) = -8
  Position(-5) = -3
  Premier SUIVANT -19 (direction +vers 0) = -17 (position -7)
  
  SA(-7) signifie : le 7e premier N├ëGATIF = -17 Ô£ô
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Optional

from .prime_table import nth_prime, prime_position


logger = logging.getLogger(__name__)


@dataclass
class GapResult:
    """R├®sultat d'un calcul d'├®cart."""
    p1: int
    p2: int
    gap_type: str
    
    position_min: int
    position_max: int
    position_suivant_min: int
    p_suivant_min: int
    
    SA_suivant_min: float
    SB_max: float
    digamma_max: float
    digamma_min: float
    
    gap_count: int
    gap_float: float
    
    formula_used: str
    explanation: str
    validation: dict[str, Any]


class GapSolver:
    """R├®sout les ├®carts avec la formule CORRECTE."""
    
    def __init__(self, spectral_core=None):
        self.core = spectral_core
        logger.info("GapSolver initialized")
    
    def solve_gap(self, p1: int, p2: int) -> Optional[GapResult]:
        """R├®sout les ├®carts selon le type."""
        if p1 > 0 and p2 > 0:
            return self._solve_positive_positive(p1, p2)
        elif p1 < 0 and p2 < 0:
            return self._solve_negative_negative(p1, p2)
        elif (p1 < 0 and p2 > 0) or (p1 > 0 and p2 < 0):
            return self._solve_mixed(p1, p2)
        else:
            return None
    
    def _solve_positive_positive(self, p1: int, p2: int) -> Optional[GapResult]:
        """CAS (+,+)."""
        logger.info(f"Solving gap (+,+) : p1={p1}, p2={p2}")
        
        p_min = min(p1, p2)
        p_max = max(p1, p2)
        
        pos_min = prime_position(p_min)
        pos_max = prime_position(p_max)
        
        if pos_min is None or pos_max is None:
            return None
        
        pos_suivant_min = pos_min + 1
        p_suivant_min = nth_prime(pos_suivant_min)
        
        if p_suivant_min is None:
            return None
        
        sa_suivant_min = self._compute_SA(pos_suivant_min)
        sb_max = self._compute_SB(pos_max)
        digamma_max = self._compute_digamma_int(pos_max, p_max)
        digamma_min = self._compute_digamma_int(pos_min, p_min)
        
        term_a = sa_suivant_min - (sb_max - digamma_max)
        term_b = digamma_min
        gap_float = (term_a - term_b) / 64
        gap_count = int(round(gap_float))
        
        logger.info(f"(+,+) : ({term_a:.2f} - {term_b:.2f}) / 64 = {gap_float:.2f} ÔåÆ {gap_count}")
        
        return GapResult(
            p1=p_min, p2=p_max, gap_type="positive_positive",
            position_min=pos_min, position_max=pos_max,
            position_suivant_min=pos_suivant_min, p_suivant_min=p_suivant_min,
            SA_suivant_min=sa_suivant_min, SB_max=sb_max, digamma_max=digamma_max,
            digamma_min=digamma_min,
            gap_count=gap_count, gap_float=gap_float,
            formula_used="gap = (SA(n_next) - (SB(n_max) - dgm(n_max)) - dgm(n_min)) / 64",
            explanation=f"Entre {p_min} et {p_max} : {gap_count} nombres",
            validation={"source": "methode_spectral.thy::gap_positive_positive"},
        )
    
    def _solve_negative_negative(self, p1: int, p2: int) -> Optional[GapResult]:
        """
        CAS (-,-) : FORMULE CORRECTE.
        
        Les positions pour n├®gatifs :
          Position(-2) = -1 (1er premier n├®gatif)
          Position(-3) = -2 (2e premier n├®gatif)
          ...
          Position(-19) = -8
          Position(-5) = -3
          
        Premier SUIVANT -19 (vers 0) = -17 (position -7)
        
        Terme A = SA(pos_suivant_min) - (SB(pos_max) - dgm(pos_max))
        Terme B = dgm(pos_min)
        gap = (Terme A - Terme B) / 64
        """
        logger.info(f"Solving gap (-,-) : p1={p1}, p2={p2}")
        
        p_min_value = min(p1, p2)
        p_max_value = max(p1, p2)
        
        logger.info(f"(-,-) : p_min={p_min_value}, p_max={p_max_value}")
        
        abs_min = abs(p_min_value)
        abs_max = abs(p_max_value)
        
        pos_min_abs = prime_position(abs_min)
        pos_max_abs = prime_position(abs_max)
        
        if pos_min_abs is None or pos_max_abs is None:
            logger.error(f"Cannot find positions for {abs_min} or {abs_max}")
            return None
        
        pos_min = -pos_min_abs
        pos_max = -pos_max_abs
        
        # Premier SUIVANT le plus petit (vers 0) : position + 1
        pos_suivant_min = pos_min + 1
        
        # CRUCIAL : R├®cup├®rer le VRAI premier n├®gatif ├á cette position
        # Position -7 = 7e premier n├®gatif = -17
        abs_suivant = abs(pos_suivant_min)
        p_suivant_min_candidate = nth_prime(abs_suivant)
        
        if p_suivant_min_candidate is None:
            logger.error(f"Cannot find prime at position {abs_suivant}")
            return None
        
        p_suivant_min = -p_suivant_min_candidate
        logger.info(f"(-,-) : pos_suivant_min={pos_suivant_min}, p_suivant_min={p_suivant_min}")
        
        sa_suivant_min = self._compute_SA_negative(pos_suivant_min)
        sb_max = self._compute_SB_negative(pos_max)
        digamma_max = self._compute_digamma_int_negative(pos_max, p_max_value)
        digamma_min = self._compute_digamma_int_negative(pos_min, p_min_value)
        
        term_a = sa_suivant_min - (sb_max - digamma_max)
        term_b = digamma_min
        gap_float = (term_a - term_b) / 64
        gap_count = int(round(gap_float))
        
        logger.info(f"(-,-) : Terme A={term_a:.6f}, Terme B={term_b:.6f}")
        logger.info(f"(-,-) : ({term_a:.6f} - {term_b:.6f}) / 64 = {gap_float:.2f} ÔåÆ {gap_count}")
        
        return GapResult(
            p1=p_min_value, p2=p_max_value, gap_type="negative_negative",
            position_min=pos_min, position_max=pos_max,
            position_suivant_min=pos_suivant_min, p_suivant_min=p_suivant_min,
            SA_suivant_min=sa_suivant_min, SB_max=sb_max, digamma_max=digamma_max,
            digamma_min=digamma_min,
            gap_count=gap_count, gap_float=gap_float,
            formula_used="gap = (SA(n_next) - (SB(n_max) - dgm(n_max)) - dgm(n_min)) / 64",
            explanation=f"Entre {p_min_value} et {p_max_value} : {gap_count} nombres",
            validation={"source": "methode_spectral.thy::gap_negative_negative"},
        )
    
    def _solve_mixed(self, p1: int, p2: int) -> Optional[GapResult]:
        """CAS (-,+).

        Note Z├ëRO SP├ëCIAL : si p_min = -2 (premier n├®gatif le plus proche de
        z├®ro), alors pos_min = -1 et pos_suivant_min = 0. Position 0 ne
        correspond ├á aucun premier (z├®ro est trait├® comme un point
        symbolique dans la M├®thode Spectrale). La formule SA(0) reste
        cependant calculable directement : SA(0) = (3.25/2)┬À2^0 - 2 = -0.375.
        """
        logger.info(f"Solving gap (-,+) MIXED : p1={p1}, p2={p2}")

        if p1 < p2:
            p_min, p_max = p1, p2
        else:
            p_min, p_max = p2, p1

        abs_min = abs(p_min)
        pos_min_abs = prime_position(abs_min)
        pos_max = prime_position(p_max)

        if pos_min_abs is None or pos_max is None:
            logger.error(
                f"_solve_mixed: position introuvable pour |p_min|={abs_min} "
                f"ou p_max={p_max}"
            )
            return None

        pos_min = -pos_min_abs
        pos_suivant_min = pos_min + 1
        zero_bridge = (pos_suivant_min == 0)

        if zero_bridge:
            # Cas limite : p_min = -2. Le ┬½ premier suivant ┬╗ franchit
            # z├®ro (position 0). On garde la formule SA(0) mais
            # p_suivant_min est symboliquement 0.
            p_suivant_min = 0
            logger.info(
                "_solve_mixed: pont Z├ëRO activ├® (p_min=-2). "
                "pos_suivant_min=0, SA(0) sera utilis├®e."
            )
        else:
            abs_suivant = abs(pos_suivant_min)
            p_suivant_min_candidate = nth_prime(abs_suivant)
            if p_suivant_min_candidate is None:
                logger.error(
                    f"_solve_mixed: nth_prime({abs_suivant}) a retourn├® None"
                )
                return None
            p_suivant_min = -p_suivant_min_candidate

        sa_suivant_min = self._compute_SA_negative(pos_suivant_min)
        sb_max = self._compute_SB(pos_max)
        digamma_max = self._compute_digamma_int(pos_max, p_max)
        digamma_min = self._compute_digamma_int_negative(pos_min, p_min)

        term_a = sa_suivant_min - (sb_max - digamma_max)
        term_b = digamma_min
        gap_float = (term_a - term_b) / 64
        gap_count = int(round(gap_float))

        logger.info(
            f"(-,+) MIXED : SA({pos_suivant_min})={sa_suivant_min:.4f}, "
            f"SB({pos_max})={sb_max:.4f}, dgm_max={digamma_max:.4f}, "
            f"dgm_min={digamma_min:.4f}"
        )
        logger.info(
            f"(-,+) MIXED : ({term_a:.4f} - {term_b:.4f}) / 64 = "
            f"{gap_float:.4f} ÔåÆ {gap_count}"
        )

        explanation = (
            f"Entre {p_min} et {p_max} : {gap_count} nombres (Z├ëRO SP├ëCIAL)"
        )
        if zero_bridge:
            explanation += " [pont Z├ëRO : p_min=-2, SA(0) utilis├®]"

        return GapResult(
            p1=p_min, p2=p_max, gap_type="mixed",
            position_min=pos_min, position_max=pos_max,
            position_suivant_min=pos_suivant_min, p_suivant_min=p_suivant_min,
            SA_suivant_min=sa_suivant_min, SB_max=sb_max, digamma_max=digamma_max,
            digamma_min=digamma_min,
            gap_count=gap_count, gap_float=gap_float,
            formula_used="gap = (SA(n_next) - (SB(n_max) - dgm(n_max)) - dgm(n_min)) / 64 [MIXTE]",
            explanation=explanation,
            validation={
                "source": "methode_spectral.thy::gap_mixed",
                "zero_special": True,
                "zero_bridge": zero_bridge,
            },
        )
    
    # ========================================================================
    # HELPERS
    # ========================================================================
    
    def _compute_SA(self, n: int) -> float:
        """SA(n) pour n positif."""
        return (3.25 / 2) * (2 ** n) - 2
    
    def _compute_SB(self, n: int) -> float:
        """SB(n) pour n positif."""
        return (6.5 / 2) * (2 ** n) - 66
    
    def _compute_SA_negative(self, n: int) -> float:
        """SA(n) pour n n├®gatif. N doit ├¬tre n├®gatif."""
        return (3.25 / 2) * (2 ** n) - 2
    
    def _compute_SB_negative(self, n: int) -> float:
        """SB(n) pour n n├®gatif. N doit ├¬tre n├®gatif."""
        return (6.5 / 2) * (2 ** n) - 66
    
    def _compute_digamma_int(self, n: int, p: int) -> float:
        """digamma_int(n, p) = SB(n) - 64*p"""
        sb = self._compute_SB(n)
        return sb - 64 * p
    
    def _compute_digamma_int_negative(self, n: int, p: int) -> float:
        """digamma_int(n, p) pour n├®gatifs."""
        sb = self._compute_SB_negative(n)
        return sb - 64 * p
