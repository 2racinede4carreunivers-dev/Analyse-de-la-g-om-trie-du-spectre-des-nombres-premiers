"""
SpectralGap — Calcul direct de l'ecart spectral entre deux primes/positions.

Aucun appel LLM. S'appuie uniquement sur :
  - spectral_core (SA, SB, INVARIANT 1/2)
  - prime_table (lookup direct)
  - certainty_kernel (citations)

Accepte en entree :
  - Deux POSITIONS (entiers 1..1000)
  - Deux PRIMES (entiers > 1, auto-detection par reverse lookup dans la table)
  - Un mix (l'agent detecte selon les valeurs)

Calcule :
  - delta_n      : ecart de positions (n2 - n1)
  - delta_p      : ecart entre primes (p2 - p1)
  - delta_SA     : SA(n2) - SA(n1)
  - delta_SB     : SB(n2) - SB(n1)
  - RsP          : delta_SA / delta_SB (DOIT etre 1/2)
  - D(n,p)       : SB(n) - SA(n) - 64*p (definition geometrique du spectre)
  - delta_D      : D(n2,p2) - D(n1,p1)
  - invariant_ok : delta_SA / delta_SB == 1/2 exactement
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from ..core.spectral_core import SpectralMethodCore
from ..spectral.prime_table import nth_prime, PRIMES


Z_RATIO_1_2 = 64  # constante du rapport 1/2


@dataclass
class GapPoint:
    """Un point spectral (position, prime, SA, SB, D)."""
    position: int
    prime: int
    SA: float
    SB: float
    D: float  # SB - SA - 64*p


@dataclass
class GapResult:
    """Resultat d'un calcul d'ecart spectral entre deux points."""
    point1: GapPoint
    point2: GapPoint
    delta_n: int
    delta_p: int
    delta_SA: float
    delta_SB: float
    rsP_fraction: str        # representation "X/Y" simplifiee
    rsP_decimal: float
    invariant_ok: bool       # delta_SA / delta_SB == 1/2 ?
    delta_D: float
    ratio: str = "1/2"


def _resolve_input(value: int) -> tuple[int, int]:
    """
    Resoudre une entree utilisateur en (position, prime).
    
    Logique :
      - Si value <= 1000 ET value figure dans le tableau des primes a sa position :
        on prend value comme POSITION (lookup direct).
      - Si value figure dans PRIMES (reverse lookup) : on prend value comme PRIME
        et on en deduit la position.
      - Si ambigu (value est a la fois <= 1000 et un nombre premier) : on prefere
        la POSITION (interpretation prioritaire pour les petits indices).
    """
    if value < 1:
        raise ValueError(f"Valeur invalide : {value}. Doit etre >= 1.")
    # Cas 1 : interpretation comme position (priorite si <= 1000)
    if 1 <= value <= len(PRIMES):
        return value, PRIMES[value - 1]
    # Cas 2 : interpretation comme prime (reverse lookup)
    try:
        idx = PRIMES.index(value)
        return idx + 1, value
    except ValueError:
        raise ValueError(
            f"Valeur {value} : ni une position valide (1..{len(PRIMES)}) "
            f"ni un nombre premier connu dans la table."
        )


def compute_gap(value1: int, value2: int, ratio: str = "1/2") -> GapResult:
    """
    Calcul direct de l'ecart spectral entre deux entrees (positions ou primes).
    
    Args:
        value1: entier representant la 1re position OU le 1er prime.
        value2: entier representant la 2e position OU le 2e prime.
        ratio: pour le moment, uniquement "1/2".
    
    Returns:
        GapResult avec tous les invariants spectraux calcules.
    """
    if ratio != "1/2":
        raise ValueError(f"compute_gap : seul le rapport 1/2 est supporte (recu : {ratio})")

    n1, p1 = _resolve_input(value1)
    n2, p2 = _resolve_input(value2)
    if n1 == n2:
        raise ValueError(f"Les deux points sont identiques (position={n1}). Choisissez deux positions distinctes.")

    # Calcul direct depuis les formules certifiees (methode_spectral.thy)
    # SA(n) = (3.25/2) * 2^n - 2 = (13/8) * 2^n - 2
    # SB(n) = (6.5/2) * 2^n - 66 = (13/4) * 2^n - 66
    def _SA(n: int) -> float:
        return (13.0 / 8.0) * (2 ** n) - 2.0

    def _SB(n: int) -> float:
        return (13.0 / 4.0) * (2 ** n) - 66.0

    point1 = GapPoint(
        position=n1, prime=p1,
        SA=_SA(n1), SB=_SB(n1),
        D=_SB(n1) - _SA(n1) - Z_RATIO_1_2 * p1,
    )
    point2 = GapPoint(
        position=n2, prime=p2,
        SA=_SA(n2), SB=_SB(n2),
        D=_SB(n2) - _SA(n2) - Z_RATIO_1_2 * p2,
    )

    delta_n = n2 - n1
    delta_p = p2 - p1
    delta_SA = point2.SA - point1.SA
    delta_SB = point2.SB - point1.SB

    # RsP = delta_SA / delta_SB en fraction exacte
    # On utilise Fraction pour eviter les erreurs flottantes (les SA/SB sont
    # mathematiquement des fractions de 2^n).
    try:
        rsP_frac = Fraction(delta_SA).limit_denominator(1_000_000_000) / Fraction(delta_SB).limit_denominator(1_000_000_000)
        rsP_str = f"{rsP_frac.numerator}/{rsP_frac.denominator}"
        invariant_ok = rsP_frac == Fraction(1, 2)
    except (ZeroDivisionError, ValueError):
        rsP_str = "indefini"
        invariant_ok = False
    rsP_decimal = (delta_SA / delta_SB) if delta_SB != 0 else float("nan")

    delta_D = point2.D - point1.D

    return GapResult(
        point1=point1, point2=point2,
        delta_n=delta_n, delta_p=delta_p,
        delta_SA=delta_SA, delta_SB=delta_SB,
        rsP_fraction=rsP_str, rsP_decimal=rsP_decimal,
        invariant_ok=invariant_ok,
        delta_D=delta_D, ratio=ratio,
    )


def render_gap_report(result: GapResult) -> str:
    """Rendu texte lisible pour affichage CLI."""
    p1, p2 = result.point1, result.point2
    inv_mark = "[OK]" if result.invariant_ok else "[ECHEC]"
    lines = [
        "ECART SPECTRAL — rapport " + result.ratio,
        "=" * 60,
        f"Point 1 : position={p1.position:<5} prime={p1.prime:<6} SA={p1.SA:.0f}  SB={p1.SB:.0f}  D={p1.D:.2f}",
        f"Point 2 : position={p2.position:<5} prime={p2.prime:<6} SA={p2.SA:.0f}  SB={p2.SB:.0f}  D={p2.D:.2f}",
        "-" * 60,
        f"delta_n        = {result.delta_n}",
        f"delta_p        = {result.delta_p}",
        f"delta_SA       = {result.delta_SA:.2f}",
        f"delta_SB       = {result.delta_SB:.2f}",
        f"delta_D        = {result.delta_D:.2f}",
        f"RsP            = delta_SA / delta_SB = {result.rsP_fraction}  ({result.rsP_decimal:.6f})",
        f"INVARIANT 1/2  = {inv_mark}  (RsP doit etre 1/2)",
    ]
    return "\n".join(lines)
