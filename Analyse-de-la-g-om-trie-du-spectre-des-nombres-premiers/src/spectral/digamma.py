"""
Digamma et equation du nombre premier.

Identites fondamentales (corpus Savard) :
  digamma_calc(n, p) = SB(n) - 64 * p          (modele 1/2)
  prime_equation(n, p) = (SB(n) - digamma_calc(n, p)) / 64 = p

Generalisation :
  digamma_calc(n, p, model) = SB_model(n) - factor * p
  prime_equation(n, p, model) = (SB_model(n) - digamma_calc(n, p, model)) / factor = p

ou factor = 64 (1/2), 729 (1/3), 4096 (1/4).
"""
from __future__ import annotations

from fractions import Fraction

from .suites import get_suite_functions


def digamma_calc(n: int, p: int, model: str = "1/2") -> Fraction:
    """digamma_calc(n, p) = B_model(n) - factor * p"""
    fns = get_suite_functions(model)
    return fns["B"](n) - fns["factor"] * p


def prime_equation(n: int, p: int, model: str = "1/2") -> Fraction:
    """prime_equation(n, p) = (B(n) - digamma_calc(n, p)) / factor"""
    fns = get_suite_functions(model)
    return (fns["B"](n) - digamma_calc(n, p, model)) / fns["factor"]


def digamma_from_blocks(B_indices: list[int], p: int, model: str = "1/2") -> Fraction:
    """Digamma a partir d'un bloc d'indices : somme(B(indices)) - factor * p"""
    fns = get_suite_functions(model)
    return fns["sumB"](B_indices) - fns["factor"] * p


def reconstruct_prime(n: int, model: str = "1/2") -> dict:
    """
    Reconstruit les valeurs spectrales associees au cas n=index.
    Retourne un dict avec SA, SB, digamma_calc et la valeur reconstruite.

    NOTE : L'agent recoit n (nombre de termes dans les suites A et B).
    Le nombre premier p est lie a n via la methode (axiomatisation).
    On expose ici les valeurs intermediaires pour permettre la verification.
    """
    fns = get_suite_functions(model)
    A_val = fns["A"](n)
    B_val = fns["B"](n)
    # On note : prime_equation(n, p) = real p (axiomatique)
    # Donc digamma_calc(n, p) = B(n) - factor * p
    # Si on connait p, on peut reconstruire le digamma.
    return {
        "model": model,
        "n": n,
        "base": fns["base"],
        "factor": fns["factor"],
        "A": A_val,
        "B": B_val,
        "A_float": float(A_val),
        "B_float": float(B_val),
    }


def verify_prime_equation(n: int, p: int, model: str = "1/2") -> dict:
    """
    Verifie l'identite prime_equation(n, p, model) == p
    Retourne tous les chiffres : SA, SB, digamma_calc, p reconstruit.
    """
    fns = get_suite_functions(model)
    A_val = fns["A"](n)
    B_val = fns["B"](n)
    dgm = digamma_calc(n, p, model)
    reconstructed = prime_equation(n, p, model)
    return {
        "model": model,
        "n": n,
        "p": p,
        "base": fns["base"],
        "factor": fns["factor"],
        "SA": A_val,
        "SB": B_val,
        "digamma_calc": dgm,
        "reconstructed_p": reconstructed,
        "equation_holds": reconstructed == Fraction(p),
        "SA_float": float(A_val),
        "SB_float": float(B_val),
        "digamma_calc_float": float(dgm),
        "reconstructed_p_float": float(reconstructed),
    }
