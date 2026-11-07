"""
rsp_curve.py — Calcul d'une courbe d'evolution du rapport spectral
pour k = 1, 2, ..., k_max, avec rendu ASCII en terminal.

Configurations supportees :
  - "1x1"          : pour chaque k, paire (prime_k, prime_(k+1)) -> attendu 1/2
  - "sym"          : pour chaque k, deux blocs symetriques de taille k -> attendu 1/2
  - "chaos"        : pour chaque k, A de taille k et B de taille k+2 chaotique
  - "ord"          : asymetrie ordonnee A=k, B=k+1 -> 1 pour petit k, vers 1/2 grand k
  - "chaos-savard" : convention alternee Savard (formule alt(X)=X[0]-X[1]-...)
                     A = [p_{k+1}..p_{2k}], B = [p_{2k+1}, p_1..p_k]
                     Diverge fortement pour k=1 puis converge vers 1/2.
"""
from __future__ import annotations

from typing import Any, Optional

from ..core.spectral_core import SpectralMethodCore
from .ratios import build_chaos_savard_blocks, ratio_chaos_savard


def compute_rsp_curve(
    core: SpectralMethodCore,
    config: str,
    k_max: int = 50,
) -> list[dict[str, Any]]:
    """
    Calcule le RsP pour k de 1 a k_max.
    Retourne une liste de dicts : [{'k': 1, 'RsP_decimal': 0.5, 'RsP_fraction': '1/2', ...}, ...]
    """
    # Cas special chaos-savard : formule alternee specifique
    if config == "chaos-savard":
        return _compute_curve_chaos_savard(core, k_max)

    points = []
    for k in range(1, k_max + 1):
        try:
            A, B = _build_config(core, config, k)
            r = core.analyze_spectral_ratio(A, B)
            points.append({
                "k": k,
                "A": A, "B": B,
                "configuration": r.get("configuration", "?"),
                "RsP_fraction": r.get("RsP_fraction", "n/a"),
                "RsP_decimal": r.get("RsP_decimal", float("nan")),
                "matches_half": r.get("matches_half", False),
                "near_half": r.get("near_half", False),
                "error": r.get("error"),
            })
        except (ValueError, IndexError) as exc:
            points.append({"k": k, "error": str(exc)})
    return points


def _compute_curve_chaos_savard(
    core: SpectralMethodCore,
    k_max: int,
) -> list[dict[str, Any]]:
    """Construit la courbe chaos-Savard : convention alternee Philippe Thomas Savard.

    Pour chaque k, calcule RsP_chaos_savard(A, B) avec :
      A = positions [k+1, ..., 2k]
      B = positions [2k+1, 1, 2, ..., k]
      |A| = k, |B| = k+1
      RsP = (alt_SA(A) - alt_SA(B)) / (alt_SB(A) - alt_SB(B))
      alt(X) = X[0] - X[1] - ... - X[n]
    """
    points: list[dict[str, Any]] = []
    primes = core.prime_list
    for k in range(1, k_max + 1):
        try:
            if 2 * k + 1 > len(primes):
                raise IndexError(f"2k+1 > {len(primes)} (taille table primes)")
            A_pos, B_pos = build_chaos_savard_blocks(k)
            ratio = ratio_chaos_savard(A_pos, B_pos, model="1/2")
            r_float = float(ratio)
            matches_half = ratio == 0.5
            near_half = abs(r_float - 0.5) <= 0.05
            # Pour l'affichage : convertir les positions en primes reels
            A_primes = [primes[p - 1] for p in A_pos]
            B_primes = [primes[p - 1] for p in B_pos]
            points.append({
                "k": k,
                "A": A_primes,
                "B": B_primes,
                "A_positions": A_pos,
                "B_positions": B_pos,
                "configuration": "chaos-savard",
                "RsP_fraction": f"{ratio.numerator}/{ratio.denominator}",
                "RsP_decimal": r_float,
                "matches_half": matches_half,
                "near_half": near_half,
                "error": None,
            })
        except (ValueError, IndexError) as exc:
            points.append({"k": k, "error": str(exc)})
    return points



def _build_config(core: SpectralMethodCore, config: str, k: int) -> tuple[list[int], list[int]]:
    """Construit deux blocs A, B pour une config et un k donnes."""
    primes = core.prime_list
    if config == "1x1":
        # paire (prime_k, prime_(k+1))
        if k + 1 > len(primes):
            raise IndexError(f"k+1 > 1000")
        return [primes[k - 1]], [primes[k]]
    if config == "sym":
        # A = k premiers a partir de position 1, B = k premiers a partir de position k+1
        if 2 * k > len(primes):
            raise IndexError(f"2k > 1000")
        return primes[:k], primes[k:2 * k]
    if config == "chaos":
        # A = k premiers, B = k+2 premiers decalages
        if k + (k + 2) > len(primes):
            raise IndexError(f"taille trop grande")
        # ordre "chaotique" : inverser les blocs
        return list(reversed(primes[:k])), list(reversed(primes[k:k + k + 2]))
    if config == "ord":
        # A = primes[0..k-1], B = primes[k..2k] (croissants, |B|=|A|+1)
        if 2 * k + 1 > len(primes):
            raise IndexError(f"2k+1 > 1000")
        return primes[:k], primes[k:2 * k + 1]
    raise ValueError(f"Config inconnue : {config}")


def render_ascii_curve(
    points: list[dict[str, Any]],
    width: int = 60,
    height: int = 18,
    target: float = 0.5,
) -> str:
    """
    Rendu ASCII de la courbe k -> RsP_decimal avec ligne de reference target=0.5.
    """
    # Filtre les points valides
    valid = [(p["k"], p["RsP_decimal"]) for p in points
             if "RsP_decimal" in p and p.get("RsP_decimal") is not None
             and not (isinstance(p["RsP_decimal"], float) and p["RsP_decimal"] != p["RsP_decimal"])]  # NaN check
    if not valid:
        return "(aucun point valide a tracer)"

    ks = [k for k, _ in valid]
    vals = [v for _, v in valid]

    vmin = min(min(vals), target) - 0.05
    vmax = max(max(vals), target) + 0.05
    if vmax - vmin < 0.01:
        vmax = vmin + 0.1

    def y_to_row(v: float) -> int:
        # 0 = top, height-1 = bottom
        ratio = (vmax - v) / (vmax - vmin) if vmax != vmin else 0.5
        return max(0, min(height - 1, int(round(ratio * (height - 1)))))

    target_row = y_to_row(target)

    grid = [[" "] * width for _ in range(height)]
    # Ligne de reference y = 0.5
    for x in range(width):
        grid[target_row][x] = "."

    # Trace les points
    k_min, k_max = min(ks), max(ks)
    span_k = max(1, k_max - k_min)
    for k, v in valid:
        x = int(round((k - k_min) / span_k * (width - 1)))
        y = y_to_row(v)
        grid[y][x] = "*"

    # Construire le rendu avec axes
    lines = [f"  RsP (cible 1/2 = {target:.2f})"]
    for i, row in enumerate(grid):
        # Affiche la valeur a gauche pour quelques lignes
        if i == 0:
            label = f"{vmax:>5.3f} |"
        elif i == height - 1:
            label = f"{vmin:>5.3f} |"
        elif i == target_row:
            label = f"{target:>5.3f} +"
        else:
            label = "      |"
        lines.append(label + "".join(row))
    lines.append("      +" + "-" * width)
    lines.append(f"        k={k_min}" + " " * (width - 10) + f"k={k_max}")
    return "\n".join(lines)


def summarize_curve(points: list[dict[str, Any]]) -> str:
    """Resume statistique de la courbe."""
    valid = [p for p in points if "RsP_decimal" in p and not p.get("error")]
    if not valid:
        return "(aucun point valide)"
    exact = sum(1 for p in valid if p["matches_half"])
    near = sum(1 for p in valid if p["near_half"] and not p["matches_half"])
    far = len(valid) - exact - near
    vals = [p["RsP_decimal"] for p in valid]
    avg = sum(vals) / len(vals)
    return (
        f"Points calcules : {len(valid)}/{len(points)}\n"
        f"  exact 1/2     : {exact} ({100*exact/len(valid):.1f}%)\n"
        f"  proche 1/2    : {near} ({100*near/len(valid):.1f}%)\n"
        f"  eloigne 1/2   : {far} ({100*far/len(valid):.1f}%)\n"
        f"  moyenne RsP   : {avg:.4f}\n"
        f"  k=1 -> RsP    : {valid[0]['RsP_decimal']:.4f}\n"
        f"  k={valid[-1]['k']} -> RsP   : {valid[-1]['RsP_decimal']:.4f}"
    )

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
