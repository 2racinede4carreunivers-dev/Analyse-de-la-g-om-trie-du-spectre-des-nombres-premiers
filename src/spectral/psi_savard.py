"""
psi_savard.py — Fonction Ψ_Savard(x, n) et Ψ classique de Tchebychev.

Compare la fonction psi de Tchebychev classique :

    Ψ(x) = Σ_{p^k ≤ x} log(p)          (von Mangoldt : forme élémentaire)

à la forme SAVARD (Isabelle/HOL, definition `psi_savard`) :

    Ψ_Savard(x, n) = x − 2^n/SB(n) − log10(2π) − ½·log10(1 − x^{-2})

où SB(n) = (6.5/2)·2^n − 66 est la seconde suite invariante Savard, et
log10 est le logarithme en base 10 (choix de l'auteur, encapsulé dans
`log10_savard` dans `methode_spectral.thy`, section XIII.1).

Validations numériques du .thy (section XIII.2) :
    Ψ_Savard(30, 10)  = 28.888143698...   (premier visé : 29)
    Ψ_Savard(98, 25)  = 96.894150249...   (premier visé : 97)
    Ψ_Savard(228, 49) = 226.894132001...  (premier visé : 227)

Le module fournit également un utilitaire d'export LaTeX (table + code
tikz/pgfplots) directement insérable dans le document
`docs/geometrie_spectre_premiers.tex`, section VI.
"""
from __future__ import annotations

import math
from typing import List, Tuple, Dict

from .suites import SB


TWO_PI = 2.0 * math.pi
LOG10_2PI = math.log10(TWO_PI)


# =============================================================
# Ψ classique de Tchebychev — forme élémentaire (von Mangoldt)
# =============================================================

def _sieve_primes(upper: int) -> List[int]:
    """Crible d'Ératosthène rapide jusqu'à `upper` inclus."""
    if upper < 2:
        return []
    sieve = bytearray(b"\x01") * (upper + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(upper ** 0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start::step] = bytearray(len(range(start, upper + 1, step)))
    return [i for i in range(2, upper + 1) if sieve[i]]


def chebyshev_psi(x: float) -> float:
    """
    Ψ(x) = Σ_{p^k ≤ x} log(p), version élémentaire de Tchebychev.

    Convergent vers x pour x → ∞ (théorème des nombres premiers).
    Ex: Ψ(30) ≈ 28.4718...
    """
    if x < 2:
        return 0.0
    upper = int(math.floor(x))
    primes = _sieve_primes(upper)
    total = 0.0
    for p in primes:
        pk = p
        while pk <= x:
            total += math.log(p)
            pk *= p
    return total


# =============================================================
# Ψ_Savard(x, n) — formule spectrale du document
# =============================================================

def psi_savard(x: float, n: int) -> float:
    """
    Ψ_Savard(x, n) = x − 2^n/SB(n) − log10(2π) − ½·log10(1 − x^{-2})

    Formule spectrale du Chapitre VI (Pont Tchebychev–Savard–Zêta),
    identique à la définition `psi_savard` de `methode_spectral.thy`.

    Validations reproduisant celles du fichier .thy :
        psi_savard(30, 10)  ~ 28.888
        psi_savard(98, 25)  ~ 96.894
        psi_savard(228, 49) ~ 226.894
    """
    if x <= 1:
        raise ValueError(f"psi_savard requiert x > 1 ; recu x = {x}")
    if n < 1:
        raise ValueError(f"psi_savard requiert n >= 1 ; recu n = {n}")
    sb_n = float(SB(n))
    two_n = 2.0 ** n
    zeta_term = -0.5 * math.log10(1.0 - 1.0 / (x * x))
    return x - (two_n / sb_n) - LOG10_2PI + zeta_term


def psi_savard_decomposition(x: float, n: int) -> Dict[str, float]:
    """Retourne chaque terme de Ψ_Savard(x, n) séparément (traçable)."""
    sb_n = float(SB(n))
    two_n = 2.0 ** n
    return {
        "x": float(x),
        "SB_n": sb_n,
        "two_n": two_n,
        "spectral_ratio": two_n / sb_n,        # = 2^n / SB(n)
        "log10_2pi": LOG10_2PI,
        "half_log10_correction": -0.5 * math.log10(1.0 - 1.0 / (x * x)),
        "psi_savard": psi_savard(x, n),
    }


# =============================================================
# Table comparative Ψ_Tchebychev vs Ψ_Savard
# =============================================================

def build_comparison_table(
    x_values: List[float], n: int
) -> List[Dict[str, float]]:
    """
    Pour chaque x ∈ x_values, calcule Ψ(x), Ψ_Savard(x, n), l'écart et
    l'écart relatif à x (précision spectrale : |Ψ_Savard − x| / x).
    """
    rows: List[Dict[str, float]] = []
    for x in x_values:
        psi_class = chebyshev_psi(x)
        psi_sav = psi_savard(x, n)
        rows.append({
            "x": float(x),
            "psi_tchebychev": psi_class,
            "psi_savard": psi_sav,
            "ecart_absolu": psi_sav - psi_class,
            "ecart_relatif_x": abs(psi_sav - x) / x if x != 0 else float("nan"),
        })
    return rows


# =============================================================
# Export LaTeX — table + graphique pgfplots
# =============================================================

def _fmt_float(v: float, precision: int = 4) -> str:
    """Formatage pour LaTeX (garde 4 décimales, pas de notation exp inutile)."""
    if math.isnan(v) or math.isinf(v):
        return "\\text{n/a}"
    return f"{v:.{precision}f}"


def to_latex_table(
    rows: List[Dict[str, float]], n: int, caption: str | None = None
) -> str:
    """Génère un tableau LaTeX (booktabs) directement insérable."""
    if caption is None:
        caption = (
            f"Comparaison $\\Psi(x)$ (Tchebychev classique) vs "
            f"$\\Psi_{{\\text{{Savard}}}}(x, n={n})$"
        )
    lines: List[str] = []
    lines.append("\\begin{table}[h]")
    lines.append("\\centering")
    lines.append(f"\\caption{{{caption}}}")
    lines.append(f"\\label{{tab:psi_savard_n{n}}}")
    lines.append("\\begin{tabular}{rrrrr}")
    lines.append("\\toprule")
    lines.append(
        "$x$ & $\\Psi(x)$ & $\\Psi_{\\text{Savard}}(x, n)$ & "
        "$\\Psi_{\\text{Savard}} - \\Psi$ & "
        "$|\\Psi_{\\text{Savard}} - x| / x$ \\\\"
    )
    lines.append("\\midrule")
    for r in rows:
        lines.append(
            f"{_fmt_float(r['x'], 0)} & "
            f"{_fmt_float(r['psi_tchebychev'])} & "
            f"{_fmt_float(r['psi_savard'])} & "
            f"{_fmt_float(r['ecart_absolu'])} & "
            f"{_fmt_float(r['ecart_relatif_x'], 6)} \\\\"
        )
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def to_latex_pgfplots(
    rows: List[Dict[str, float]], n: int, caption: str | None = None
) -> str:
    """
    Génère un graphique pgfplots comparant Ψ(x), Ψ_Savard(x, n) et y = x.
    Nécessite le package pgfplots dans le préambule LaTeX (pas de par défaut ici).
    """
    if caption is None:
        caption = (
            f"Convergence de $\\Psi_{{\\text{{Savard}}}}(x, n={n})$ "
            f"et $\\Psi(x)$ vers $y = x$"
        )
    coords_savard = " ".join(f"({r['x']:.4f},{r['psi_savard']:.6f})" for r in rows)
    coords_tcheb = " ".join(f"({r['x']:.4f},{r['psi_tchebychev']:.6f})" for r in rows)
    coords_y_eq_x = " ".join(f"({r['x']:.4f},{r['x']:.4f})" for r in rows)
    lines: List[str] = []
    lines.append("\\begin{figure}[h]")
    lines.append("\\centering")
    lines.append("\\begin{tikzpicture}")
    lines.append("\\begin{axis}[")
    lines.append("    width=0.85\\textwidth, height=7cm,")
    lines.append("    xlabel={$x$}, ylabel={$\\Psi$},")
    lines.append("    grid=both, legend pos=north west,")
    lines.append("    legend style={font=\\small},")
    lines.append("]")
    lines.append(f"\\addplot[thick, blue,   mark=*]  coordinates {{{coords_savard}}};")
    lines.append(f"\\addplot[thick, red,    mark=x]  coordinates {{{coords_tcheb}}};")
    lines.append(f"\\addplot[dashed, gray]           coordinates {{{coords_y_eq_x}}};")
    lines.append(
        "\\legend{$\\Psi_{\\text{Savard}}(x,n)$, $\\Psi(x)$ Tchebychev, $y = x$}"
    )
    lines.append("\\end{axis}")
    lines.append("\\end{tikzpicture}")
    lines.append(f"\\caption{{{caption}}}")
    lines.append(f"\\label{{fig:psi_savard_n{n}}}")
    lines.append("\\end{figure}")
    return "\n".join(lines)


def to_latex_document(
    rows: List[Dict[str, float]], n: int, standalone: bool = False
) -> str:
    """
    Assemble table + graphique.
    Si `standalone=True`, produit un document LaTeX autonome compilable.
    Sinon, produit un fragment insérable dans un document existant.
    """
    body = to_latex_table(rows, n) + "\n\n" + to_latex_pgfplots(rows, n)
    if not standalone:
        return body
    preamble = (
        "\\documentclass[11pt,a4paper]{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[T1]{fontenc}\n"
        "\\usepackage[french]{babel}\n"
        "\\usepackage{amsmath,amssymb,booktabs,pgfplots}\n"
        "\\pgfplotsset{compat=1.18}\n"
        "\\begin{document}\n\n"
    )
    return preamble + body + "\n\n\\end{document}\n"


__all__ = [
    "chebyshev_psi",
    "psi_savard",
    "psi_savard_decomposition",
    "build_comparison_table",
    "to_latex_table",
    "to_latex_pgfplots",
    "to_latex_document",
]
