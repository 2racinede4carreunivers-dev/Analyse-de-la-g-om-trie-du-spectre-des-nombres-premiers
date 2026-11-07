"""Exact rational-gap solver - correction pour gap queries (positifs,
negatifs, mixtes) en arithmetique Fraction exacte, reproduisant la formule
de methode_spectral.thy pour TOUS les cas de premiers.

Formule (theories/methode_spectral.thy : gap_neg_val, gap_mix_val,
gap_equation_1_3, gap_equation_1_4) :

    gap = ( SA(n_suivant_min) - SB(n_max)
            + digamma(n_max, p_max) - digamma(n_min, p_min) ) / 64

ou digamma(n, p) = SB(n) - 64*p, avec :
    SA(n) = (3.25/2)*2^n - 2 = (13/8)*2^n - 2
    SB(n) = (6.5/2)*2^n - 66 = (13/4)*2^n - 66

Positions signees (convention du solveur original) :
    position(-2) = -1, position(-3) = -2, position(-5) = -3, ...
    position(-p_k) = -k ou p_k est le k-ieme premier positif.
Le premier suivant p_min vers les valeurs croissantes est la position
n_min + 1 ; pour p_min = -2 on atteint la position 0 (valeur 0, hors
table des premiers) : le "Pont ZERO" (cas special des tests).

Identite algebrique exacte, pour tout entier n (Fraction comprise car
Fraction(2)**n est exact aussi pour n < 0) :
    SA(n+1) - SB(n) = 13/8*2^(n+1) - 2 - (13/4*2^n - 66) = 64

La formule spectrale se simplifie donc EXACTEMENT en :
    gap = 1 - (p_max - p_min) = p_min - p_max + 1

Le calcul est pourtant effectue via la formule spectrale complete en
Fractions exactes (miroir de la demonstration .thy), puis controle contre
l'identite simplifiee (validation["identite_exacte"]). Aucune derive
float64 : gap_count est toujours un int exact ; gap_float sert a
l'affichage seul. Les valeurs SA/SB/digamma intermediaires sont
conservees exactes jusqu'a la conversion d'affichage finale.

Examples .thy : (23,7) -> -15, (-19,-5) -> -13, (-31,17) -> -47.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Optional

from .prime_table import PRIMES, nth_prime, prime_position

logger = logging.getLogger(__name__)

MAX_POSITION = len(PRIMES)  # positions 1..MAX_POSITION (table etendue 100001)


@dataclass
class GapResult:
    """Resultat d'un calcul d'ecart de gap spectral."""
    p1: int
    p2: int
    gap_type: str
    position_min: int
    position_max: int
    position_suivant_min: int
    p_suivant_min: Optional[int]
    SA_suivant_min: float
    SB_max: float
    digamma_max: float
    digamma_min: float
    gap_count: int
    gap_float: float
    formula_used: str
    explanation: str
    validation: dict


class GapSolver:
    """Resolve prime-gap spectral queries with exact rational arithmetic.

    Accepte un eventuel spectral_core (pipeline) ; celui-ci n'est pas
    necessaire au calcul : la formule .thy est autonome.
    """

    def __init__(self, spectral_core=None):
        self.core = spectral_core
        self.max_position = MAX_POSITION
        logger.info("GapSolver initialized (exact Fraction arithmetic)")

    # ------------------------------------------------------------------
    # Spectral building blocks (exact Fraction arithmetic)
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_SA(n: int) -> Fraction:
        """SA(n) = (3.25/2)*2^n - 2, exact (13/8 = 3.25/2), n quelconque."""
        return Fraction(13, 8) * (Fraction(2) ** n) - 2

    @staticmethod
    def _compute_SB(n: int) -> Fraction:
        """SB(n) = (6.5/2)*2^n - 66, exact (13/4 = 6.5/2), n quelconque."""
        return Fraction(13, 4) * (Fraction(2) ** n) - 66

    @classmethod
    def _compute_SA_negative(cls, n: int) -> Fraction:
        """SA(n) pour n <= 0 : meme formule, exacte en Fraction."""
        return cls._compute_SA(n)

    @classmethod
    def _compute_SB_negative(cls, n: int) -> Fraction:
        """SB(n) pour n <= 0 : meme formule, exacte en Fraction."""
        return cls._compute_SB(n)

    @classmethod
    def _compute_digamma_int(cls, n: int, p: int) -> Fraction:
        """digamma(n, p) = SB(n) - 64*p (conforme methode_spectral.thy)."""
        return cls._compute_SB(n) - 64 * p

    @classmethod
    def _compute_digamma_int_negative(cls, n: int, p: int) -> Fraction:
        """digamma(n, p) pour position negative et/ou premier negatif."""
        return cls._compute_SB_negative(n) - 64 * p

    # ------------------------------------------------------------------
    # Conversion sure Fraction -> float (jamais OverflowError)
    # ------------------------------------------------------------------

    @staticmethod
    def _to_float_safe(value: Fraction) -> float:
        """Fraction -> float sans jamais lever OverflowError.

        Hors portee float64 (grandes positions n >= 58 ou tres negatives),
        retourne +/-inf SANS planter ; gap_count reste lui toujours exact.
        """
        try:
            return float(value)
        except OverflowError:
            num = abs(value.numerator)
            den = value.denominator
            exp = num.bit_length() - den.bit_length()
            mant = Fraction(num, den) / (Fraction(2) ** exp)
            while mant >= 2:
                mant /= 2
                exp += 1
            while mant < 1:
                mant *= 2
                exp -= 1
            try:
                return math.ldexp(float(mant), exp)
            except OverflowError:
                return float("-inf") if value < 0 else float("inf")

    # ------------------------------------------------------------------
    # Finalisation : gap exact + float d'affichage
    # ------------------------------------------------------------------

    def _finaliser_gap(
        self,
        sa_suivant: Fraction,
        sb_max: Fraction,
        digamma_max: Fraction,
        digamma_min: Fraction,
    ) -> tuple[int, float]:
        """gap = (SA_suivant - SB_max + digamma_max - digamma_min) / 64.

        Retourne (gap_count exact int, gap_float). La Fraction obtenue est
        un entier exact (identite SA(n+1) - SB(n) = 64) : aucun arrondi,
        aucune derive float64.
        """
        numerator = sa_suivant - sb_max + digamma_max - digamma_min
        gap_exact = numerator / 64
        if gap_exact.denominator == 1:
            gap_count = gap_exact.numerator
        else:
            # Ne devrait jamais arriver (identite exacte) : arrondi au plus
            # proche pour rester utilisable ; tracee dans validation.
            gap_count = int(round(float(gap_exact)))
        return gap_count, float(gap_count)

    # ------------------------------------------------------------------
    # Resolution des entrees (premier, sinon position) en positions signees
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_input(value: int) -> tuple[int, int]:
        """Resout une entree utilisateur en (position signee, premier).

        Regles :
          - value > 0 :
              * si value est un premier de la table -> position = rang (1..)
              * sinon, si 1 <= value <= MAX_POSITION -> position (rsp/gap)
              * sinon ValueError
          - value < 0 :
              * si |value| est un premier -> position = -rang (negatif)
              * sinon ValueError
          - value = 0 -> ValueError (ni premier ni position)
        """
        if value == 0:
            errmsg = "Valeur invalide : 0. Attendu un premier ou une position."
            raise ValueError(errmsg)
        if value > 0:
            pos = prime_position(value)
            if pos is not None:
                return pos, value
            if 1 <= value <= MAX_POSITION:
                p = nth_prime(value)
                if p is not None:
                    return value, p
            errmsg = (
                "Valeur " + str(value)
                + " : ni un premier de la table ni une position valide (1.."
                + str(MAX_POSITION) + ")."
            )
            raise ValueError(errmsg)
        # value < 0 : premier negatif (position signee negative)
        pos = prime_position(-value)
        if pos is None:
            errmsg = (
                "Valeur negative " + str(value) + " : " + str(-value)
                + " n'est pas un premier de la table (|p| <= "
                + str(PRIMES[-1]) + ")."
            )
            raise ValueError(errmsg)
        return -pos, value

    @classmethod
    def _prime_at_signed_position(cls, position: int) -> Optional[int]:
        """Premier associe a une position signee.

        - position 0 -> 0 (Pont ZERO : valeur 0 hors table des premiers)
        - position < 0 -> premier negatif oppose
        - position hors table (apres le dernier premier) -> None
        """
        if position == 0:
            return 0
        if position < 0:
            p = nth_prime(-position)
            return None if p is None else -p
        return nth_prime(position)


    # ------------------------------------------------------------------
    # Worker commun : formule spectrale exacte (.thy), tous signes
    # ------------------------------------------------------------------

    def _solve_pair(self, p1: int, p2: int, gap_type: str) -> GapResult:
        """Calcule l'ecart spectral entre deux premiers (signes quelconques).

        Normalise (p_min, p_max), resout les positions signees, applique la
        formule .thy en Fractions exactes puis verifie l'identite
        gap = prime_min - prime_max + 1.
        """
        p_min, p_max = min(p1, p2), max(p1, p2)
        n_min, prime_min = self._resolve_input(p_min)
        n_max, prime_max = self._resolve_input(p_max)

        n_suivant = n_min + 1
        p_suivant = self._prime_at_signed_position(n_suivant)
        zero_bridge = (n_suivant == 0)

        sa_suivant = self._compute_SA(n_suivant)
        sb_max = self._compute_SB(n_max)
        digamma_max = self._compute_digamma_int(n_max, prime_max)
        digamma_min = self._compute_digamma_int(n_min, prime_min)

        gap_count, gap_float = self._finaliser_gap(
            sa_suivant, sb_max, digamma_max, digamma_min
        )

        identite = prime_min - prime_max + 1
        validation: dict[str, Any] = {
            "zero_bridge": zero_bridge,
            "zero_special": zero_bridge,
            "identite_exacte": gap_count == identite,
            "identite_attendue": identite,
            "gap_exact": str(Fraction(gap_count)),
            "arithmetic": "Fraction exact (aucune derive float64)",
        }

        formula_used = (
            "gap = (SA(n_suivant_min) - SB(n_max) + digamma(n_max,p_max) "
            "- digamma(n_min,p_min)) / 64 ; digamma(n,p) = SB(n) - 64*p "
            "[methode_spectral.thy : gap_neg_val/gap_mix_val/"
            "gap_equation_1_3/gap_equation_1_4]"
        )

        lines: list[str] = []
        lines.append(
            "Ecart spectral " + gap_type + " : " + str(prime_min)
            + " vs " + str(prime_max) + "."
        )
        lines.append(
            "Positions signees : n_min = " + str(n_min)
            + ", n_max = " + str(n_max)
            + ", n_suivant_min = " + str(n_suivant)
            + " (p_suivant_min = " + str(p_suivant) + ")."
        )
        lines.append(
            "SA(n_suivant_min) = " + str(sa_suivant)
            + " ; SB(n_max) = " + str(sb_max)
            + " ; digamma(n_max) = " + str(digamma_max)
            + " ; digamma(n_min) = " + str(digamma_min) + "."
        )
        numerator = sa_suivant - sb_max + digamma_max - digamma_min
        lines.append(
            "gap = (" + str(numerator) + ") / 64 = " + str(gap_count)
            + " (Fraction exacte)."
        )
        lines.append(
            "Identite SA(n+1) - SB(n) = 64 : gap = p_min - p_max + 1 = "
            + str(identite) + " ; verifie = "
            + str(validation["identite_exacte"]) + "."
        )
        lines.append(
            "Signe : gap_count <= 0 pour premiers distincts vaut -(nombre "
            "d'entiers strictement entre p_min et p_max)."
        )
        if zero_bridge:
            lines.append(
                "Pont ZÉRO : la position 0 (valeur 0) est atteinte entre "
                "-2 et 2 ; SA(0) = " + str(self._compute_SA(0))
                + " remplace le premier suivant hors table (cas special)."
            )
        explanation = "\n".join(lines)

        return GapResult(
            p1=prime_min,
            p2=prime_max,
            gap_type=gap_type,
            position_min=n_min,
            position_max=n_max,
            position_suivant_min=n_suivant,
            p_suivant_min=p_suivant,
            SA_suivant_min=self._to_float_safe(sa_suivant),
            SB_max=self._to_float_safe(sb_max),
            digamma_max=self._to_float_safe(digamma_max),
            digamma_min=self._to_float_safe(digamma_min),
            gap_count=gap_count,
            gap_float=gap_float,
            formula_used=formula_used,
            explanation=explanation,
            validation=validation,
        )

    # ------------------------------------------------------------------
    # Cas (+,+), (-,-) et mixte
    # ------------------------------------------------------------------

    def _solve_positive_positive(self, p1: int, p2: int) -> GapResult:
        """CAS (+,+) : deux premiers positifs."""
        logger.info("Solving gap (+,+) : p1=%d, p2=%d", p1, p2)
        return self._solve_pair(p1, p2, "positive_positive")

    def _solve_negative_negative(self, p1: int, p2: int) -> GapResult:
        """CAS (-,-) : deux premiers negatifs (ordre inverse)."""
        logger.info("Solving gap (-,-) : p1=%d, p2=%d", p1, p2)
        return self._solve_pair(p1, p2, "negative_negative")

    def _solve_mixed(self, p1: int, p2: int) -> GapResult:
        """CAS mixte : un premier negatif et un premier positif."""
        logger.info("Solving gap mixte : p1=%d, p2=%d", p1, p2)
        return self._solve_pair(p1, p2, "mixed")


    # ------------------------------------------------------------------
    # API publique
    # ------------------------------------------------------------------

    def solve_gap(self, p1: int, p2: int) -> Optional[GapResult]:
        """Resout l'ecart spectral selon le type de signes.

        Retourne un GapResult pour (+,+), (-,-) et le cas mixte ;
        None si l'un des deux vaut 0 (ni premier positif, ni negatif).
        """
        if p1 > 0 and p2 > 0:
            return self._solve_positive_positive(p1, p2)
        if p1 < 0 and p2 < 0:
            return self._solve_negative_negative(p1, p2)
        if (p1 < 0 < p2) or (p2 < 0 < p1):
            return self._solve_mixed(p1, p2)
        return None
