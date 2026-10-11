"""
Suites spectrales SA, SB, A_1_3, B_1_3, A_1_4, B_1_4, mixtes et negatives.
Implementation directe du corpus methode_spectral.thy de Philippe Thomas Savard.
"""
from __future__ import annotations

from fractions import Fraction


# =============================================================
# Rapport 1/2 - Suites positives
# =============================================================

def SA(n: int) -> Fraction:
    """SA(n) = (3.25 / 2) * 2^n - 2"""
    return Fraction(13, 8) * Fraction(2) ** n - Fraction(2)


def SB(n: int) -> Fraction:
    """SB(n) = (6.5 / 2) * 2^n - 66"""
    return Fraction(13, 4) * Fraction(2) ** n - Fraction(66)


# =============================================================
# Rapport 1/3
# =============================================================

def A_1_3(n: int) -> Fraction:
    """A_1_3(n) = ((73/9)/12) * 3^n - 1.5"""
    return Fraction(73, 9 * 12) * Fraction(3) ** n - Fraction(3, 2)


def B_1_3(n: int) -> Fraction:
    """B_1_3(n) = ((219/9)/12) * 3^n - (487 * 1.5)"""
    return Fraction(219, 9 * 12) * Fraction(3) ** n - Fraction(487 * 3, 2)


# =============================================================
# Rapport 1/4
# =============================================================

def A_1_4(n: int) -> Fraction:
    """A_1_4(n) = ((241/16)/12) * 4^n - 4/3"""
    return Fraction(241, 16 * 12) * Fraction(4) ** n - Fraction(4, 3)


def B_1_4(n: int) -> Fraction:
    """B_1_4(n) = ((964/16)/12) * 4^n - (3073 * 4/3)"""
    return Fraction(964, 16 * 12) * Fraction(4) ** n - Fraction(3073 * 4, 3)


# =============================================================
# Suites mixtes (-,+)
# =============================================================

def SA_mix(n: int) -> Fraction:
    """SA_mix(n) = 48 + 13/(2^(n+2))"""
    return Fraction(48) + Fraction(13, 2 ** (n + 2))


def SB_mix(n: int) -> Fraction:
    """SB_mix(n) = -28 + 13/(2^(n+1))"""
    return Fraction(-28) + Fraction(13, 2 ** (n + 1))


# =============================================================
# Sommes de blocs (n*n)
# =============================================================

def sum_SA(indices: list[int]) -> Fraction:
    return sum((SA(i) for i in indices), Fraction(0))


def sum_SB(indices: list[int]) -> Fraction:
    return sum((SB(i) for i in indices), Fraction(0))


def sum_A_1_3(indices: list[int]) -> Fraction:
    return sum((A_1_3(i) for i in indices), Fraction(0))


def sum_B_1_3(indices: list[int]) -> Fraction:
    return sum((B_1_3(i) for i in indices), Fraction(0))


def sum_A_1_4(indices: list[int]) -> Fraction:
    return sum((A_1_4(i) for i in indices), Fraction(0))


def sum_B_1_4(indices: list[int]) -> Fraction:
    return sum((B_1_4(i) for i in indices), Fraction(0))


# =============================================================
# Selection de modele
# =============================================================

SUITES_BY_MODEL = {
    "1/2": {"A": SA, "B": SB, "sumA": sum_SA, "sumB": sum_SB, "base": 2, "factor": 64},
    "1/3": {"A": A_1_3, "B": B_1_3, "sumA": sum_A_1_3, "sumB": sum_B_1_3, "base": 3, "factor": 729},
    "1/4": {"A": A_1_4, "B": B_1_4, "sumA": sum_A_1_4, "sumB": sum_B_1_4, "base": 4, "factor": 4096},
}


def get_suite_functions(model: str) -> dict:
    if model not in SUITES_BY_MODEL:
        raise ValueError(f"Modele spectral inconnu : {model}. Choix : {list(SUITES_BY_MODEL)}")
    return SUITES_BY_MODEL[model]
