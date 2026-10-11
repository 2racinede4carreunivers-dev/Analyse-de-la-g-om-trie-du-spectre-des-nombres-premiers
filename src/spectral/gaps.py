"""
Equation generale d'ecart entre deux nombres premiers.

Formule (corpus Savard) :
  gap_equation_1_3(A_next, B_high, D_high, D_low) = (A_next - B_high + D_high - D_low) / 729
  gap_equation_1_4(A_next, B_high, D_high, D_low) = (A_next - B_high + D_high - D_low) / 4096

Resultat = quantite d'entiers entre p_high et p_low (peut etre negative).

Trois cas couverts :
  (+,+) : deux premiers positifs (memes signes)
  (-,-) : deux indices spectraux negatifs (suites SB_neg, SA_neg)
  (-,+) : configuration mixte
"""
from __future__ import annotations

from fractions import Fraction

from .suites import SA, SA_mix, SB, SB_mix, get_suite_functions
from ..core.spectral_types import GapKind


def gap_equation(
    A_next,
    B_high,
    D_high,
    D_low,
    model: str = "1/3",
) -> Fraction:
    """
    Forme generale (sections IX et VIII du corpus) :
       gap_equation = (A_next - (B_high - D_high) - D_low) / factor
                    = (A_next - B_high + D_high - D_low) / factor

    A_next : somme de la suite A pour le premier suivant du plus petit
    B_high : somme de la suite B pour le plus grand premier
    D_high : Digamma du plus grand
    D_low  : Digamma du plus petit
    """
    fns = get_suite_functions(model)
    factor = fns["factor"]
    A_next_f = Fraction(A_next) if not isinstance(A_next, Fraction) else A_next
    B_high_f = Fraction(B_high) if not isinstance(B_high, Fraction) else B_high
    D_high_f = Fraction(D_high) if not isinstance(D_high, Fraction) else D_high
    D_low_f = Fraction(D_low) if not isinstance(D_low, Fraction) else D_low
    return (A_next_f - (B_high_f - D_high_f) - D_low_f) / factor


# =============================================================
# Helpers : detection du cas (+,+), (-,-) ou (-,+)
# =============================================================

def detect_gap_kind(p_high, p_low) -> GapKind:
    """Detecte la categorie d'ecart d'apres les signes."""
    if p_high >= 0 and p_low >= 0:
        return GapKind.POS_POS
    if p_high <= 0 and p_low <= 0:
        return GapKind.NEG_NEG
    return GapKind.NEG_POS


# =============================================================
# Gap (+,+) : utilise les suites positives (SA, SB, A_1_3, etc.)
# =============================================================

def gap_positive(
    A_next,
    B_high,
    D_high,
    D_low,
    model: str = "1/3",
) -> Fraction:
    """Gap pour deux premiers positifs - utilise gap_equation standard."""
    return gap_equation(A_next, B_high, D_high, D_low, model)


# =============================================================
# Gap (-,-) : utilise les suites negatives
# =============================================================

def gap_negative(
    A_next,
    B_high,
    D_high,
    D_low,
    factor: int = 64,
) -> Fraction:
    """
    Gap pour deux indices spectraux negatifs.
    Le diviseur depend du modele (64 pour 1/2, 729 pour 1/3, 4096 pour 1/4).
    """
    A_next_f = Fraction(A_next) if not isinstance(A_next, Fraction) else A_next
    B_high_f = Fraction(B_high) if not isinstance(B_high, Fraction) else B_high
    D_high_f = Fraction(D_high) if not isinstance(D_high, Fraction) else D_high
    D_low_f = Fraction(D_low) if not isinstance(D_low, Fraction) else D_low
    return (A_next_f - (B_high_f - D_high_f) - D_low_f) / factor


# =============================================================
# Gap (-,+) : configuration mixte, utilise les suites mixtes
# =============================================================

def gap_mixed(
    A_next,
    B_high,
    D_high,
    D_low,
    factor: int = 64,
) -> Fraction:
    """
    Gap mixte (-,+) - inclut le zero dans la progression spectrale.
    Forme identique a la formule generale mais le zero est compte.
    """
    A_next_f = Fraction(A_next) if not isinstance(A_next, Fraction) else A_next
    B_high_f = Fraction(B_high) if not isinstance(B_high, Fraction) else B_high
    D_high_f = Fraction(D_high) if not isinstance(D_high, Fraction) else D_high
    D_low_f = Fraction(D_low) if not isinstance(D_low, Fraction) else D_low
    return (A_next_f - (B_high_f - D_high_f) - D_low_f) / factor


# =============================================================
# Dispatcher unifie pour les 3 cas
# =============================================================

def compute_gap(
    p_high: int,
    p_low: int,
    A_next,
    B_high,
    D_high,
    D_low,
    model: str = "1/3",
) -> dict:
    """
    Calcul unifie de l'ecart entre deux premiers, automatiquement adapte
    a la configuration (+,+), (-,-) ou (-,+).
    """
    kind = detect_gap_kind(p_high, p_low)
    fns = get_suite_functions(model)
    factor = fns["factor"]

    if kind == GapKind.POS_POS:
        gap = gap_positive(A_next, B_high, D_high, D_low, model)
        formula_used = f"gap_equation_{model.replace('/', '_')}"
    elif kind == GapKind.NEG_NEG:
        gap = gap_negative(A_next, B_high, D_high, D_low, factor)
        formula_used = "gap_negative (suites negatives)"
    else:
        gap = gap_mixed(A_next, B_high, D_high, D_low, factor)
        formula_used = "gap_mixed (-,+)"

    return {
        "kind": kind.value,
        "model": model,
        "factor": factor,
        "p_high": p_high,
        "p_low": p_low,
        "A_next": Fraction(A_next),
        "B_high": Fraction(B_high),
        "D_high": Fraction(D_high),
        "D_low": Fraction(D_low),
        "gap": gap,
        "gap_float": float(gap),
        "formula_used": formula_used,
        "expected_gap_signed": p_low - p_high,
    }
