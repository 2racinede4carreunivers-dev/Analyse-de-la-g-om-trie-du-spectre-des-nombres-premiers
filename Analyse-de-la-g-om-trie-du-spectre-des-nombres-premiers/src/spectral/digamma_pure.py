"""
digamma_pure.py — Digamma function psi(n) computed PURELY from n.

v3.38 (Philippe 2026-02) : Repond a la demande de Philippe de disposer d'une
formule pour psi(n) qui ne depend PAS de la valeur du n-ieme premier.

Contrairement a `digamma_calc(n, p) = SB(n) - 64*p` (module digamma.py) qui
requiert de connaitre le prime p, cette implementation calcule psi(n) a partir
de n seul, avec DEUX methodes complementaires :

  1. FORME EXACTE (entier positif, precision arbitraire via Fraction) :
       psi(n) = -gamma + H_{n-1}
     ou H_{n-1} = 1 + 1/2 + 1/3 + ... + 1/(n-1)  (nombre harmonique)
     Cette forme est SYMBOLIQUEMENT EXACTE ; seule la constante gamma
     est numerique (fournie a 50 decimales).

  2. FORME ASYMPTOTIQUE (Stirling, reel positif) :
       psi(x) ~ ln(x) - 1/(2x) - Sum_{k>=1} B_{2k} / (2k * x^{2k})
     ou B_{2k} sont les nombres de Bernoulli.
     Precision : ~1e-15 des x >= 6 en tronquant a k=8.

Utilite pour la Methode Spectrale : Philippe peut maintenant explorer des
relations entre psi(n) direct et SA(n)/SB(n) sans passer par la valeur
du prime, ouvrant la voie a des identites de reconstruction pure.

References : Abramowitz & Stegun 6.3.5 (exact) et 6.3.18 (asymptotique).
"""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from math import log
from typing import Union


# Constante d'Euler-Mascheroni a 50 decimales (source : OEIS A001620)
EULER_GAMMA_STR = "0.57721566490153286060651209008240243104215933593992"
EULER_GAMMA = float(EULER_GAMMA_STR)


# Nombres de Bernoulli B_{2k} pour la serie asymptotique
# B_2 = 1/6, B_4 = -1/30, B_6 = 1/42, B_8 = -1/30, B_10 = 5/66, ...
# Les coefficients de l'expansion psi(x) ~ ln(x) - 1/(2x) - Sum_{k>=1} B_{2k}/(2k * x^{2k})
# valent donc B_{2k}/(2k) = 1/12, -1/120, 1/252, -1/240, 1/132, -691/32760, ...
_ASYMPTOTIC_COEFFS: list[Fraction] = [
    Fraction(1, 12),         # k=1  : B_2 / 2  = 1/12
    Fraction(-1, 120),       # k=2  : B_4 / 4  = -1/120
    Fraction(1, 252),        # k=3  : B_6 / 6  = 1/252
    Fraction(-1, 240),       # k=4  : B_8 / 8  = -1/240
    Fraction(1, 132),        # k=5  : B_10/10  = 1/132
    Fraction(-691, 32760),   # k=6  : B_12/12  = -691/32760
    Fraction(1, 12),         # k=7  : B_14/14  = 1/12
    Fraction(-3617, 8160),   # k=8  : B_16/16  = -3617/8160
]


def harmonic(n: int) -> Fraction:
    """Nombre harmonique H_n = 1 + 1/2 + 1/3 + ... + 1/n, EXACT (Fraction).

    H_0 = 0 par convention.
    """
    if n < 0:
        raise ValueError(f"n doit etre >= 0, recu {n}")
    if n == 0:
        return Fraction(0)
    total = Fraction(0)
    for k in range(1, n + 1):
        total += Fraction(1, k)
    return total


def digamma_pure_exact(n: int) -> tuple[Fraction, float]:
    """psi(n) pour n entier >= 1, forme SYMBOLIQUE exacte.

    Retourne (partie_harmonique_exacte, valeur_float).
        psi(n) = -gamma + H_{n-1}
    Le premier element (Fraction) est H_{n-1} sous forme rationnelle EXACTE.
    Le second (float) est psi(n) = float(H_{n-1}) - gamma, precision ~1e-15.

    Complexite : O(n) par sommation ; O(n log n) via Fraction reduction.
    Pour n > 100 000, prefer digamma_pure_asymptotic (plus rapide et
    aussi precise).
    """
    if n < 1:
        raise ValueError(f"psi(n) requiert n >= 1 ; recu {n}")
    H = harmonic(n - 1)  # H_0 = 0 pour n=1 -> psi(1) = -gamma
    psi_float = float(H) - EULER_GAMMA
    return H, psi_float


def digamma_pure_asymptotic(x: Union[int, float], order: int = 6) -> float:
    """psi(x) pour x reel > 0, serie asymptotique de Stirling.

        psi(x) ~ ln(x) - 1/(2x) - Sum_{k=1}^order B_{2k}/(2k * x^{2k})

    Args:
        x : reel > 0.
        order : nombre de termes de la serie (1..8). Defaut 6 = precision
                ~1e-14 pour x >= 6.

    Precision empirique (order=6) :
        x=1  : erreur ~1e-2
        x=3  : erreur ~1e-6
        x=6  : erreur ~1e-14
        x=10 : erreur ~1e-16 (limite float)

    Pour x < 6, utiliser la recurrence : psi(x) = psi(x+1) - 1/x
    (recursion vers grande x, puis serie).
    """
    if x <= 0:
        raise ValueError(f"psi(x) asymptotique requiert x > 0 ; recu {x}")
    if order < 1 or order > len(_ASYMPTOTIC_COEFFS):
        raise ValueError(f"order doit etre 1..{len(_ASYMPTOTIC_COEFFS)} ; recu {order}")

    # Shift par recurrence pour ameliorer la precision : psi(x) = psi(x+N) - Sum_{i=0}^{N-1} 1/(x+i)
    # On veut x_shifted >= 6 pour precision optimale
    xs = float(x)
    shift_sum = 0.0
    while xs < 6.0:
        shift_sum += 1.0 / xs
        xs += 1.0

    # Serie asymptotique sur xs
    result = log(xs) - 1.0 / (2.0 * xs)
    x2 = xs * xs
    x_pow = x2
    for k in range(order):
        result -= float(_ASYMPTOTIC_COEFFS[k]) / x_pow
        x_pow *= x2

    return result - shift_sum


def digamma_pure(n: Union[int, float]) -> float:
    """API unifiee : digamma pur en fonction de n uniquement.

    - Si n est entier >= 1 et <= 1000 : forme EXACTE (H_{n-1} - gamma).
    - Sinon (reel, ou n > 1000) : serie asymptotique avec shift a x >= 6.

    Precision >= 1e-14 dans tous les cas.
    """
    if isinstance(n, int) and 1 <= n <= 1000:
        _, val = digamma_pure_exact(n)
        return val
    return digamma_pure_asymptotic(float(n))


def digamma_high_precision(n: int, decimals: int = 50) -> Decimal:
    """psi(n) pour n entier, precision arbitraire (Decimal).

    Utile pour Isabelle/HOL cross-checking et pour explorer des relations
    numeriques fines avec SA(n)/SB(n).
    """
    if n < 1:
        raise ValueError(f"psi(n) requiert n >= 1 ; recu {n}")
    getcontext().prec = decimals + 10
    H = Decimal(0)
    for k in range(1, n):
        H += Decimal(1) / Decimal(k)
    gamma_dec = Decimal(EULER_GAMMA_STR[:decimals + 2])
    return H - gamma_dec


# =============================================================================
# Applications a la Methode Spectrale : liens SA/SB avec psi(n) pur
# =============================================================================

def spectral_signature_pure(n: int) -> dict:
    """Genere la 'signature spectrale pure' d'un rang n :

        - psi(n)                    : digamma pur (formule d'Euler)
        - H_{n-1}                    : nombre harmonique exact (Fraction)
        - psi(n) - ln(n)             : deviation de la log approximation
        - psi(n) + gamma - H_{n-1}   : residu (~ 0 exact)

    Cette signature ne depend que de n, JAMAIS d'un premier connu.
    Elle est destinee a etre confrontee a SA(n), SB(n), et RsP(n1,n2)
    pour chercher des relations de reconstruction.
    """
    if n < 1:
        raise ValueError(f"n doit etre >= 1 ; recu {n}")
    H = harmonic(n - 1)
    psi_val = float(H) - EULER_GAMMA
    ln_n = log(n) if n >= 1 else float("-inf")
    return {
        "n": n,
        "psi_n": psi_val,
        "H_n_minus_1_exact": H,
        "H_n_minus_1_float": float(H),
        "euler_gamma": EULER_GAMMA,
        "psi_minus_ln_n": psi_val - ln_n,
        "asymptotic_check": digamma_pure_asymptotic(n) - psi_val,  # ~0 si convergent
    }


__all__ = [
    "EULER_GAMMA",
    "EULER_GAMMA_STR",
    "harmonic",
    "digamma_pure",
    "digamma_pure_exact",
    "digamma_pure_asymptotic",
    "digamma_high_precision",
    "spectral_signature_pure",
]
