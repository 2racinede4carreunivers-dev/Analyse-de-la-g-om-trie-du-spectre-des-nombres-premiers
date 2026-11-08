"""Renderer ASCII generique pour CurveData.

Trace une courbe (eventuellement avec une serie secondaire) dans une grille
de caracteres, avec ligne de reference optionnelle (target_line).
"""
from __future__ import annotations

from math import isfinite

from .curves import CurveData


def render_ascii(curve: CurveData, width: int = 70, height: int = 20) -> str:
    """Rendu ASCII d'un CurveData.

    Trace les points avec '*' (serie principale) et 'o' (serie secondaire si presente).
    Une ligne de reference '.' est tracee si target_line est definie.
    Les axes affichent valeurs min/max et bornes n.
    """
    pts = [p for p in curve.points if p.y_float is not None and isfinite(p.y_float)]
    if not pts:
        return f"  (aucun point valide pour {curve.kind.value})"

    sec_pts = [p for p in curve.secondary_points if p.y_float is not None and isfinite(p.y_float)]

    all_ys = [p.y_float for p in pts] + [p.y_float for p in sec_pts]
    if curve.target_line is not None and isfinite(curve.target_line):
        all_ys.append(curve.target_line)

    y_min = min(all_ys)
    y_max = max(all_ys)
    if abs(y_max - y_min) < 1e-12:
        y_max = y_min + 1.0  # evite division par zero

    pad = (y_max - y_min) * 0.05
    y_min -= pad
    y_max += pad

    ks = [p.n for p in pts]
    n_min, n_max = min(ks), max(ks)
    span_n = max(1, n_max - n_min)

    def y_to_row(v: float) -> int:
        ratio = (y_max - v) / (y_max - y_min)
        return max(0, min(height - 1, int(round(ratio * (height - 1)))))

    def n_to_col(n: int) -> int:
        return int(round((n - n_min) / span_n * (width - 1)))

    grid = [[" "] * width for _ in range(height)]

    # Ligne de reference
    if curve.target_line is not None and isfinite(curve.target_line):
        if y_min <= curve.target_line <= y_max:
            row = y_to_row(curve.target_line)
            for x in range(width):
                grid[row][x] = "."

    # Serie secondaire (en premier pour qu'elle soit derriere)
    for p in sec_pts:
        x = n_to_col(p.n)
        y = y_to_row(p.y_float)
        if grid[y][x] in (" ", "."):
            grid[y][x] = "o"

    # Serie principale
    for p in pts:
        x = n_to_col(p.n)
        y = y_to_row(p.y_float)
        grid[y][x] = "*"

    # Construction du rendu
    lines = [
        f"  {curve.title}",
        f"  echelle = {curve.scale}  |  formule : {curve.formula}",
        "",
    ]

    for i, row in enumerate(grid):
        if i == 0:
            label = f"{y_max:>10.3g} |"
        elif i == height - 1:
            label = f"{y_min:>10.3g} |"
        elif curve.target_line is not None and i == y_to_row(curve.target_line):
            label = f"{curve.target_line:>10.3g} +"
        else:
            label = "           |"
        lines.append(label + "".join(row))

    lines.append("           +" + "-" * width)
    n_label = f"           n={n_min}" + " " * max(0, width - 12 - len(str(n_max))) + f"n={n_max}"
    lines.append(n_label)

    # Legende
    legend = "  Legende : * = " + curve.kind.value
    if sec_pts:
        legend += f"   o = {curve.secondary_label}"
    if curve.target_line is not None:
        legend += f"   . = {curve.target_label or 'reference'} ({curve.target_line:.3g})"
    lines.append("")
    lines.append(legend)

    # Stats compactes
    y_first = pts[0].y_float
    y_last = pts[-1].y_float
    lines.append(
        f"  Stats : n_points={len(pts)}  y(n={n_min})={y_first:.4g}  "
        f"y(n={n_max})={y_last:.4g}  y_min={min(p.y_float for p in pts):.4g}  "
        f"y_max={max(p.y_float for p in pts):.4g}"
    )
    return "\n".join(lines)
