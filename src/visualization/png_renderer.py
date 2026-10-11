"""Renderer PNG (matplotlib) pour CurveData.

Genere une figure PNG haute resolution adaptee aux articles scientifiques.
Si matplotlib n'est pas disponible, leve une ImportError explicite.

v3.36 (Philippe 2026-02) : Mode "adaptive_scale" — pour les courbes RsP
qui divergent a petits blocs puis convergent vers une cible (ex: 1/2),
on bascule automatiquement sur un double panneau (overview + zoom
convergence) quand les donnees le justifient. Cela evite qu'un pic
initial ecrase la resolution visuelle de la convergence.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .curves import CurveData

try:
    import matplotlib
    matplotlib.use("Agg")  # Backend non-interactif, pas de display requis
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# Palette scientifique cohérente (bleu nuit + bordeaux + vert cible)
COLOR_PRIMARY   = "#1f4e8c"   # bleu nuit
COLOR_SECONDARY = "#c0392b"   # bordeaux
COLOR_TARGET    = "#27ae60"   # vert
COLOR_ANNOTATE  = "#8e44ad"   # violet (points remarquables)
COLOR_DIVERG    = "#d35400"   # orange (points divergents)
COLOR_GRID      = "#cccccc"


def _slugify(s: str) -> str:
    """Convertit une string en nom de fichier safe."""
    keep = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
    out = []
    for c in s:
        if c in keep:
            out.append(c)
        elif c.isspace() or c in "()":
            out.append("_")
    return "".join(out).strip("_") or "curve"


def _should_use_dual_panel(curve: CurveData) -> bool:
    """v3.36 : Decide si on bascule en double panneau (overview + zoom).

    Criteres cumulatifs (tous requis) :
      1. curve.adaptive_scale = True
      2. curve.target_line n'est pas None
      3. Au moins un point diverge de la cible de plus de 3x la fenetre de zoom
      4. Au moins 50% des points sont dans la fenetre de zoom (convergence
         claire vers la cible)
      5. Il y a au moins 8 points pour justifier le zoom
    """
    if not curve.adaptive_scale or curve.target_line is None:
        return False
    pts = [p for p in curve.points if p.y_float is not None]
    if len(pts) < 8:
        return False
    target = curve.target_line
    window = max(curve.zoom_y_window, 1e-6)
    outlier_threshold = 3 * window
    n_outliers = sum(1 for p in pts if abs(p.y_float - target) > outlier_threshold)
    n_converged = sum(1 for p in pts if abs(p.y_float - target) <= window)
    if n_outliers == 0:
        return False  # rien a "cacher" via zoom
    if n_converged < 0.5 * len(pts):
        return False  # pas assez de convergence pour justifier le zoom
    return True


def _plot_series_on_axis(ax, curve: CurveData, xs, ys, *,
                        show_legend: bool = True,
                        annotate_endpoints: bool = True,
                        highlight_divergent: bool = False,
                        divergent_threshold: Optional[float] = None) -> None:
    """Trace la courbe (et eventuellement la ligne cible) sur un axis donne."""
    primary_label = curve.primary_label or curve.kind.value
    ax.plot(xs, ys, marker="o", markersize=4.5, linewidth=1.6,
            color=COLOR_PRIMARY, label=primary_label,
            markeredgecolor="white", markeredgewidth=0.6, zorder=3)

    # Serie secondaire si presente
    if curve.secondary_points:
        sec_xs = [p.n for p in curve.secondary_points if p.y_float is not None]
        sec_ys = [p.y_float for p in curve.secondary_points if p.y_float is not None]
        ax.plot(sec_xs, sec_ys, marker="s", markersize=4.0, linewidth=1.3,
                color=COLOR_SECONDARY, linestyle="--",
                label=curve.secondary_label,
                markeredgecolor="white", markeredgewidth=0.5, zorder=3)

    # Ligne de reference
    if curve.target_line is not None:
        ax.axhline(curve.target_line, color=COLOR_TARGET, linestyle=":",
                   linewidth=1.8,
                   label=curve.target_label or f"cible {curve.target_line:.4g}",
                   zorder=2)

    # Highlight des points divergents (mode adaptive)
    if highlight_divergent and curve.target_line is not None and divergent_threshold is not None:
        div_xs = [x for x, y in zip(xs, ys) if abs(y - curve.target_line) > divergent_threshold]
        div_ys = [y for y in ys if abs(y - curve.target_line) > divergent_threshold]
        if div_xs:
            ax.scatter(div_xs, div_ys, s=90, facecolors="none",
                       edgecolors=COLOR_DIVERG, linewidths=1.6, zorder=5,
                       label="divergence attendue (petits blocs)")

    # Annotations sur points remarquables (premier, dernier, extremums)
    if annotate_endpoints and len(xs) >= 2 and curve.target_line is not None:
        ax.annotate(
            f"{ys[0]:.4f}",
            xy=(xs[0], ys[0]),
            xytext=(8, 8), textcoords="offset points",
            fontsize=8, color=COLOR_ANNOTATE,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=COLOR_ANNOTATE, lw=0.7, alpha=0.85),
            zorder=4,
        )
        ax.annotate(
            f"{ys[-1]:.4f}",
            xy=(xs[-1], ys[-1]),
            xytext=(-50, 8), textcoords="offset points",
            fontsize=8, color=COLOR_ANNOTATE,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=COLOR_ANNOTATE, lw=0.7, alpha=0.85),
            zorder=4,
        )

    ax.set_xlabel(curve.x_label, fontsize=10.5, color="#444444")
    ax.set_ylabel(curve.y_label, fontsize=10.5, color="#444444")
    ax.grid(True, alpha=0.4, linestyle=":", color=COLOR_GRID, zorder=1)
    if show_legend:
        ax.legend(loc="best", fontsize=9, framealpha=0.92, edgecolor="#888888")

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color("#888888")
        ax.spines[spine].set_linewidth(0.8)


def _render_single_panel(curve: CurveData, xs, ys, dpi: int, out_path: Path) -> Path:
    """Rendu classique (un seul panneau)."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=dpi)
    fig.patch.set_facecolor("#fafafa")
    ax.set_facecolor("#ffffff")

    _plot_series_on_axis(ax, curve, xs, ys)

    # Point divergent max (si distance a la cible > 5%) — annotation classique
    if curve.target_line is not None and len(xs) >= 2:
        distances = [abs(y - curve.target_line) for y in ys]
        i_max = distances.index(max(distances))
        if distances[i_max] > 0.05 and i_max not in (0, len(ys) - 1):
            ax.annotate(
                f"max ecart\n{ys[i_max]:.4f}",
                xy=(xs[i_max], ys[i_max]),
                xytext=(10, -30), textcoords="offset points",
                fontsize=7.5, color=COLOR_ANNOTATE,
                bbox=dict(boxstyle="round,pad=0.25", fc="white",
                          ec=COLOR_ANNOTATE, lw=0.7, alpha=0.85),
                arrowprops=dict(arrowstyle="->", color=COLOR_ANNOTATE,
                                lw=0.7, alpha=0.7),
                zorder=4,
            )

    ax.set_title(curve.title, fontsize=13, fontweight="bold", pad=15, color="#222222")

    bottom_reserve = _apply_footer_and_summary(fig, curve)
    plt.tight_layout(rect=[0, bottom_reserve, 1, 1])
    plt.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path


def _render_dual_panel(curve: CurveData, xs, ys, dpi: int, out_path: Path) -> Path:
    """v3.36 : Rendu double panneau — overview complet + zoom convergence.

    Panneau du haut : vue complete (toutes les valeurs y, montre la divergence).
    Panneau du bas : zoom [target - window, target + window] (montre la
                     convergence fine vers la cible sur toute la plage k).
    """
    target = curve.target_line
    window = max(curve.zoom_y_window, 1e-6)
    divergent_threshold = 3 * window

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=(10, 9.2), dpi=dpi,
        gridspec_kw={"height_ratios": [1.15, 1.0], "hspace": 0.32},
    )
    fig.patch.set_facecolor("#fafafa")
    ax_top.set_facecolor("#ffffff")
    ax_bot.set_facecolor("#ffffff")

    # --- Panneau du haut : overview complet ---
    _plot_series_on_axis(ax_top, curve, xs, ys,
                        show_legend=True, annotate_endpoints=True,
                        highlight_divergent=True,
                        divergent_threshold=divergent_threshold)
    ax_top.set_title(
        f"{curve.title}\nVue complete — signature spectrale (divergence a petits blocs)",
        fontsize=11, fontweight="bold", pad=8, color="#222222",
    )

    # --- Panneau du bas : zoom sur la convergence ---
    _plot_series_on_axis(ax_bot, curve, xs, ys,
                        show_legend=False, annotate_endpoints=False)
    y_low = target - window
    y_high = target + window
    ax_bot.set_ylim(y_low, y_high)

    # Compte les points hors fenetre pour l'annotation
    outliers = [(x, y) for x, y in zip(xs, ys) if not (y_low <= y <= y_high)]
    n_out = len(outliers)

    zoom_title = (
        f"Zoom sur la convergence — fenetre y = [{y_low:.4f}, {y_high:.4f}] "
        f"(cible {target:.4f})"
    )
    if n_out > 0:
        first_out_ks = [x for x, _ in outliers[:min(5, n_out)]]
        zoom_title += f"\n{n_out} point(s) hors echelle (k={first_out_ks}) — voir vue du haut"
    ax_bot.set_title(zoom_title, fontsize=10.5, fontweight="bold",
                     pad=8, color="#222222")

    # Petite bulle explicative sur le panneau du bas
    ax_bot.text(
        0.99, 0.06,
        "Convergence RsP -> cible : les points hors fenetre du haut sont\n"
        "attendus (blocs trop petits pour equilibrer la comparaison).",
        transform=ax_bot.transAxes,
        ha="right", va="bottom", fontsize=7.5,
        color="#555555", style="italic",
        bbox=dict(boxstyle="round,pad=0.35", fc="#fafcff", ec="#aab8c9",
                  lw=0.6, alpha=0.9),
    )

    bottom_reserve = _apply_footer_and_summary(fig, curve)
    # v3.36 : subplots_adjust au lieu de tight_layout (evite le warning de
    # compatibilite avec le rect + hspace explicite du gridspec).
    # bottom_reserve garantit que le footer ne chevauche pas le xlabel du
    # panneau inferieur. top=0.90 laisse de la place pour un titre 2-lignes.
    safe_bottom = bottom_reserve + 0.04
    fig.subplots_adjust(left=0.09, right=0.97, bottom=safe_bottom,
                        top=0.90, hspace=0.42)
    plt.savefig(out_path, dpi=dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    return out_path


def _apply_footer_and_summary(fig, curve: CurveData) -> float:
    """Applique le resume critique + legende d'axes + footer scientifique.
    Retourne la fraction de hauteur reservee au bas de la figure.
    """
    has_summary = bool(curve.critical_summary)
    has_axis_legend = bool(curve.axis_legend)

    bottom_reserve = 0.06
    if has_summary:
        bottom_reserve += 0.14
    if has_axis_legend:
        bottom_reserve += 0.03 + 0.025 * len(curve.axis_legend)

    if has_summary:
        summary_text = _wrap_text(curve.critical_summary, width=115)
        y_position = bottom_reserve - 0.05
        fig.text(
            0.5, y_position, summary_text,
            ha="center", va="top", fontsize=8,
            color="#333333",
            bbox=dict(boxstyle="round,pad=0.5", fc="#f4f4f8",
                      ec="#666666", lw=0.6, alpha=0.95),
            wrap=True,
        )

    if has_axis_legend:
        legend_lines = [f"  {k} : {v}" for k, v in curve.axis_legend.items()]
        legend_text = "Legende des axes et series :\n" + "\n".join(legend_lines)
        y_legend = 0.045 + (0.02 if has_summary else 0)
        fig.text(
            0.015, y_legend, legend_text,
            ha="left", va="bottom", fontsize=7,
            color="#555555", family="monospace",
        )

    footer = f"Formule : {curve.formula}    |    Genere le : {curve.generated_at[:19]}Z"
    fig.text(0.5, 0.020, footer, ha="center", fontsize=7,
             style="italic", color="#555555")
    fig.text(0.99, 0.004, "Gabriel Multi-Loop Agent  -  Methode Spectrale Savard",
             ha="right", fontsize=6.5, color="#888888", style="italic")

    return bottom_reserve


def render_png(
    curve: CurveData,
    output_dir: Path | str,
    dpi: int = 150,
    filename: Optional[str] = None,
) -> Path:
    """Rend une CurveData en PNG haute resolution.

    v3.36 : Si `curve.adaptive_scale=True` et que la courbe presente des
    outliers precoces + une convergence claire vers `target_line`, bascule
    automatiquement en mode double panneau (overview + zoom convergence).

    Args:
        curve: CurveData a rendre.
        output_dir: repertoire de sortie (cree si absent).
        dpi: resolution (150 = bonne qualite article, 300 = print).
        filename: nom du fichier (sans extension). Defaut : auto-genere.

    Returns:
        Path du PNG cree.

    Raises:
        ImportError: si matplotlib n'est pas installe.
    """
    if not MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib n'est pas installe. Installez-le via 'pip install matplotlib' "
            "ou utilisez render_ascii / render_table comme alternative."
        )

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
        filename = f"{ts}_{_slugify(curve.kind.value)}_n{curve.n_min}-{curve.n_max}_{curve.scale}"
    out_path = output_dir / f"{filename}.png"

    pts = [p for p in curve.points if p.y_float is not None]
    if not pts:
        raise ValueError(f"Aucun point a tracer pour {curve.kind.value}")

    xs = [p.n for p in pts]
    ys = [p.y_float for p in pts]

    if _should_use_dual_panel(curve):
        return _render_dual_panel(curve, xs, ys, dpi, out_path)
    return _render_single_panel(curve, xs, ys, dpi, out_path)


def _wrap_text(text: str, width: int = 115) -> str:
    """Wrap un texte pour l'affichage matplotlib (respecte les phrases)."""
    import textwrap
    lines: list[str] = []
    for para in text.split("\n"):
        lines.extend(textwrap.wrap(para, width=width) or [""])
    return "\n".join(lines)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
