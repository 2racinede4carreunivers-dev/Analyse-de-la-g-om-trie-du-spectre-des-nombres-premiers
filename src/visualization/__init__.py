"""Visualisation Gabriel : courbes & tableaux ASCII / Rich / PNG.

Module 100% data-centric. Chaque type de courbe est calcule sous forme de
`CurveData` (dataclass) puis rendu par 3 renderers independants :
  - ascii_renderer : terminal pur, hors-ligne
  - rich_renderer  : tableau Rich (joli affichage CLI)
  - png_renderer   : matplotlib (export image scientifique citable)

Usage type :
    from src.visualization import compute_curve, render_ascii, render_table, render_png

    curve = compute_curve(core, kind="SA", n_min=1, n_max=50, scale="log10")
    print(render_ascii(curve))
    print(render_table(curve))   # Rich Panel + Table
    path = render_png(curve, output_dir=Path("data/graphs"))
"""
from __future__ import annotations

from .curves import (
    CurveData,
    CurvePoint,
    CurveKind,
    compute_curve,
    list_supported_kinds,
)
from .ascii_renderer import render_ascii
from .rich_renderer import render_table
from .png_renderer import render_png, MATPLOTLIB_AVAILABLE
from .auto_trigger import VisualizationIntent, detect_visualization_intent

__all__ = [
    "CurveData",
    "CurvePoint",
    "CurveKind",
    "compute_curve",
    "list_supported_kinds",
    "render_ascii",
    "render_table",
    "render_png",
    "MATPLOTLIB_AVAILABLE",
    "VisualizationIntent",
    "detect_visualization_intent",
]
