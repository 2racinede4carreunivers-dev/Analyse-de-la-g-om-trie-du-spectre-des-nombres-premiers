"""Renderer Rich (tableau) pour CurveData.

Affiche les donnees sous forme tabulaire, compact pour articles ou rapports.
Si plus de 30 lignes : affiche les 15 premieres + ... + 15 dernieres (centre).
"""
from __future__ import annotations

from rich.table import Table

from .curves import CurveData


def _fmt_int(v: int | float, max_digits: int = 18) -> str:
    """Format compact pour grands entiers."""
    if isinstance(v, float):
        return f"{v:.6g}"
    s = str(v)
    if len(s) <= max_digits:
        return s
    # Compact : "1.234e30"
    sign = "-" if v < 0 else ""
    abs_s = s.lstrip("-")
    exp = len(abs_s) - 1
    mantissa = abs_s[0] + "." + abs_s[1:6]
    return f"{sign}{mantissa}e{exp}"


def render_table(curve: CurveData, max_rows: int = 30) -> Table:
    """Construit un objet Rich Table pour la courbe.

    Args:
        curve: CurveData a afficher.
        max_rows: nombre max de lignes (si depasse, on tronque avec '...' au milieu).

    Returns:
        rich.table.Table prete a etre `console.print()`.
    """
    has_secondary = bool(curve.secondary_points)
    title = curve.title + (f"  ({curve.scale})" if curve.scale != "linear" else "")
    table = Table(
        title=title,
        title_style="bold cyan",
        header_style="bold magenta",
        show_lines=False,
    )

    table.add_column("n", justify="right", style="bold")
    table.add_column("prime P(n)", justify="right")
    table.add_column(curve.kind.value, justify="right")
    if has_secondary:
        table.add_column(curve.secondary_label, justify="right")
    if curve.scale != "linear":
        table.add_column(f"{curve.kind.value} ({curve.scale})", justify="right", style="dim")

    pts = curve.points
    sec_pts = curve.secondary_points
    n_total = len(pts)

    if n_total <= max_rows:
        indices = list(range(n_total))
    else:
        half = max_rows // 2
        indices = list(range(half)) + [-1] + list(range(n_total - half, n_total))

    for idx in indices:
        if idx == -1:
            # Ligne de troncature
            ellipsis_row = ["...", "...", "..."]
            if has_secondary:
                ellipsis_row.append("...")
            if curve.scale != "linear":
                ellipsis_row.append("...")
            table.add_row(*ellipsis_row, style="dim")
            continue
        p = pts[idx]
        row = [
            str(p.n),
            str(p.prime) if p.prime is not None else "-",
            _fmt_int(p.y_exact),
        ]
        if has_secondary:
            sec = sec_pts[idx] if idx < len(sec_pts) else None
            row.append(_fmt_int(sec.y_exact) if sec else "-")
        if curve.scale != "linear":
            row.append(f"{p.y_float:.4g}")
        table.add_row(*row)

    table.caption = f"Formule : {curve.formula}   |   Points : {n_total}"
    table.caption_style = "italic dim"
    return table
