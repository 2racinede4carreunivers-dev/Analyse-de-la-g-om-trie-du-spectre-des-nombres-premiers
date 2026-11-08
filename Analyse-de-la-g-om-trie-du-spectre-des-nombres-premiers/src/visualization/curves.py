"""Calcul des donnees pour les courbes Gabriel.

Tous les calculs utilisent SpectralMethodCore (entiers exacts Python).
Pour SA/SB/digamma qui explosent en 2^n, on peut appliquer un changement
d'echelle (log10 / log2) au moment du rendu, jamais au calcul lui-meme :
le CurveData contient toujours les valeurs exactes (Decimal/int) en y_exact,
et une projection float (y_float) pour le rendu rapide.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from math import log10, log2
from typing import Any, Optional

from ..core.spectral_core import SpectralMethodCore, SpectralRatio


class CurveKind(str, Enum):
    """Types de courbes supportes."""
    SA = "SA"                # Somme alternee A : (13.2^n)/8 - 2
    SB = "SB"                # Somme alternee B : (13.2^n)/4 - 66
    SA_SB = "SA_SB"          # Superposition SA + SB sur le meme graphique
    DIGAMMA = "digamma"      # digamma(n) = SB - 64*P (selon reconstruction 1/2)
    INVARIANT = "invariant"  # D(n,P) = SB - SA - Z*P (devrait etre constant/regulier)
    RATIO_SA_SB = "ratio"    # SA / SB (devrait converger vers 1/2)
    GAP = "gap"              # Delta_p = p(n+1) - p(n) en fonction de n
    PRIME = "prime"          # p(n) en fonction de n (croissance des premiers)


@dataclass
class CurvePoint:
    """Un point exact (entier) + sa projection float pour rendu."""
    n: int
    y_exact: int | float           # valeur exacte (entier Python ou float si invariant float)
    y_float: float                 # projection pour rendu (eventuellement log)
    prime: Optional[int] = None    # le n-ieme premier, pour reference
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class CurveData:
    """Conteneur generique pour une courbe."""
    kind: CurveKind
    n_min: int
    n_max: int
    scale: str                          # "linear" | "log10" | "log2"
    title: str
    x_label: str
    y_label: str
    points: list[CurvePoint]
    # Pour SA_SB : on a 2 series ; on stocke series secondaire ici
    secondary_points: list[CurvePoint] = field(default_factory=list)
    secondary_label: str = ""
    # v3.25 : Label explicite de la serie principale (defaut = curve.kind.value)
    primary_label: str = ""
    # Ligne de reference (eg. 0.5 pour le ratio)
    target_line: Optional[float] = None
    target_label: str = ""
    # Metadata pour audit citable
    formula: str = ""                   # formule mathematique exacte utilisee
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    # v3.25 : Resume critique scholarly (max 750 caracteres) rendu sous le graphique.
    # Doit decrire : (a) ce que la courbe MONTRE, (b) ce qu'elle ne montre PAS,
    # (c) le contexte theorique, (d) la reference bibliographique si pertinente.
    critical_summary: str = ""
    # v3.25 : Legende explicite des axes (rendue en bas a droite du graphique).
    # Format : {"n": "indice de position...", "SA(n)": "somme alternee A..."}
    axis_legend: dict[str, str] = field(default_factory=dict)
    # v3.36 (Philippe 2026-02) : Auto-adaptation d'echelle pour graphiques RsP
    # comportant une divergence a petits blocs + convergence a grands blocs.
    # Quand True, render_png bascule en mode double-panneau si les donnees
    # remplissent les criteres (outliers precoces + convergence tardive vers
    # target_line). Sinon rendu classique inchange.
    adaptive_scale: bool = False
    # v3.36 : Fenetre y "zoom convergence" (defaut : target +/- 0.02).
    # Ignore si adaptive_scale=False.
    zoom_y_window: float = 0.02

    def __post_init__(self) -> None:
        # Validation : critical_summary tronque a 750 caracteres (choix Philippe 2026-02)
        if len(self.critical_summary) > 750:
            self.critical_summary = self.critical_summary[:747] + "..."

    def summary(self) -> dict[str, Any]:
        """Resume compact pour audit JSON."""
        if not self.points:
            return {"kind": self.kind.value, "n_points": 0}
        y_vals = [p.y_float for p in self.points]
        return {
            "kind": self.kind.value,
            "n_min": self.n_min, "n_max": self.n_max,
            "scale": self.scale,
            "n_points": len(self.points),
            "y_first": self.points[0].y_float,
            "y_last": self.points[-1].y_float,
            "y_min": min(y_vals),
            "y_max": max(y_vals),
            "formula": self.formula,
            "target_line": self.target_line,
        }


# --------------------------------------------------------------------------
# Helpers de projection (log / linear)
# --------------------------------------------------------------------------
def _project(value: int | float, scale: str) -> float:
    """Projette une valeur exacte vers float selon l'echelle choisie."""
    v = float(value) if not isinstance(value, int) else value
    if scale == "log10":
        if isinstance(v, int):
            # Pour les tres grands entiers, log10 direct du float perd la precision ;
            # on utilise len(str) comme approximation rapide.
            if v <= 0:
                return float("nan")
            # log10(v) approx : on calcule via la longueur decimale + premiers chiffres
            s = str(v)
            return (len(s) - 1) + log10(float(s[:15]) / (10 ** (min(len(s), 15) - 1)))
        if v <= 0:
            return float("nan")
        return log10(v)
    if scale == "log2":
        if isinstance(v, int):
            if v <= 0:
                return float("nan")
            return v.bit_length() - 1 + log2(float(v >> max(0, v.bit_length() - 30)) /
                                              (1 << min(30, v.bit_length() - 1))) if v.bit_length() > 30 else log2(v)
        if v <= 0:
            return float("nan")
        return log2(v)
    return float(v)


# --------------------------------------------------------------------------
# Calculateurs par type de courbe
# --------------------------------------------------------------------------
def _compute_SA(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    pts = []
    for n in range(n_min, n_max + 1):
        sa = core._SA_int(n)
        pts.append(CurvePoint(n=n, y_exact=sa, y_float=_project(sa, scale),
                              prime=core.get_prime_at_position(n)))
    return CurveData(
        kind=CurveKind.SA, primary_label="SA(n) : somme alternee A", n_min=n_min, n_max=n_max, scale=scale,
        title=f"Suite spectrale A : SA(n) = (13.2^n)/8 - 2   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="SA(n) : somme alternee A" + (f"  (echelle {scale})" if scale != "linear" else ""),
        points=pts,
        formula="SA(n) = (13 * 2^n) / 8 - 2",
        axis_legend={
            "n": "indice de position (n=1 pour p1=2, n=2 pour p2=3, ...)",
            "SA(n)": "valeur exacte de la somme alternee A a la position n",
        },
        critical_summary=(
            "GRAPHIQUE : trace la suite spectrale A definie par SA(n) = (13.2^n)/8 - 2, "
            "premier des deux invariants de la Methode Spectrale 1/2 de Savard. "
            "L'axe horizontal represente l'indice de position n dans la table des "
            "1000 premiers (n=1 correspond a p1=2). L'axe vertical donne la valeur "
            "exacte de SA(n), calculee en arithmetique entiere Python. "
            "NE MONTRE PAS le rapport spectral SA/SB (voir courbe RATIO) ni la "
            "reconstruction des premiers (voir courbe DIGAMMA). "
            "Source : methode_spectral.thy::somme_A_compacte_savard."
        ),
    )


def _compute_SB(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    pts = []
    for n in range(n_min, n_max + 1):
        sb = core._SB_int(n)
        pts.append(CurvePoint(n=n, y_exact=sb, y_float=_project(sb, scale),
                              prime=core.get_prime_at_position(n)))
    return CurveData(
        kind=CurveKind.SB, primary_label="SB(n) : somme alternee B", n_min=n_min, n_max=n_max, scale=scale,
        title=f"Suite spectrale B : SB(n) = (13.2^n)/4 - 66   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="SB(n) : somme alternee B" + (f"  (echelle {scale})" if scale != "linear" else ""),
        points=pts,
        formula="SB(n) = (13 * 2^n) / 4 - 66",
        axis_legend={
            "n": "indice de position (n=1 pour p1=2, n=2 pour p2=3, ...)",
            "SB(n)": "valeur exacte de la somme alternee B a la position n",
        },
        critical_summary=(
            "GRAPHIQUE : trace la suite spectrale B definie par SB(n) = (13.2^n)/4 - 66, "
            "second des deux invariants de la Methode Spectrale 1/2. "
            "Par construction, SB(n) = 2 * (SA(n) + 2) - 66 : SB croit deux fois plus "
            "vite que SA. L'axe horizontal est l'indice de position n dans la table "
            "des 1000 premiers ; l'axe vertical donne la valeur exacte de SB(n) "
            "(arithmetique entiere Python). "
            "NE MONTRE PAS le rapport SA/SB. "
            "Source : methode_spectral.thy::somme_B_compacte_savard."
        ),
    )


def _compute_SA_SB(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    sa_pts, sb_pts = [], []
    for n in range(n_min, n_max + 1):
        sa, sb = core._SA_int(n), core._SB_int(n)
        sa_pts.append(CurvePoint(n=n, y_exact=sa, y_float=_project(sa, scale),
                                 prime=core.get_prime_at_position(n)))
        sb_pts.append(CurvePoint(n=n, y_exact=sb, y_float=_project(sb, scale),
                                 prime=core.get_prime_at_position(n)))
    return CurveData(
        kind=CurveKind.SA_SB, primary_label="SA(n) : somme alternee A", n_min=n_min, n_max=n_max, scale=scale,
        title=f"Superposition SA(n) et SB(n) - Methode Spectrale 1/2   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label=("Valeurs SA(n) et SB(n) " + (f"({scale})" if scale != "linear" else "(lineaire)")),
        points=sa_pts,
        secondary_points=sb_pts,
        secondary_label="SB(n) : somme alternee B",
        formula="SA(n) = (13.2^n)/8 - 2  ;  SB(n) = (13.2^n)/4 - 66",
        axis_legend={
            "n": "indice de position (n=1 pour p1=2, n=2 pour p2=3, ...)",
            "SA(n) - bleu": "somme alternee A, formule (13.2^n)/8 - 2",
            "SB(n) - bordeaux": "somme alternee B, formule (13.2^n)/4 - 66",
        },
        critical_summary=(
            "GRAPHIQUE : superposition des deux suites spectrales SA(n) et SB(n) "
            "sur le meme axe, permettant la comparaison visuelle de leur croissance "
            "et de leur rapport. La courbe bleue est SA, la bordeaux est SB. "
            "On voit que SB(n) ~= 2 * SA(n) pour n grand, ce qui refletera le "
            "rapport asymptotique SA/SB -> 1/2 (voir courbe RATIO). "
            "NE MONTRE PAS la valeur du rapport lui-meme (echelle absolue). "
            "Sources : methode_spectral.thy::somme_A_compacte_savard, somme_B_compacte_savard."
        ),
    )


def _compute_digamma(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    pts = []
    for n in range(n_min, n_max + 1):
        data = core.reconstruct_prime_1_2(n)
        if data is None:
            continue
        dig = int(data.digamma)
        pts.append(CurvePoint(n=n, y_exact=dig, y_float=_project(dig, scale),
                              prime=data.prime_value,
                              extra={"SA": int(data.SA_sum), "SB": int(data.SB_sum)}))
    return CurveData(
        kind=CurveKind.DIGAMMA, primary_label="Digamma_1/2(n)", n_min=n_min, n_max=n_max, scale=scale,
        title=(
            f"Digamma_1/2(n) = SB(n) - 64 . P(n)   "
            f"[reconstruction ratio 1/2, n = {n_min}..{n_max}]"
        ),
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="Digamma_1/2(n) : reste apres extraction de P(n)"
                + (f"  (echelle {scale})" if scale != "linear" else ""),
        points=pts,
        formula=(
            "digamma_1/2(n) = SB(n) - 64 * P(n)  "
            "avec 64 = 128/2 (constante Savard specifique au ratio 1/2). "
            "Reconstruction : P(n) = (SB(n) - digamma_1/2(n)) / 64."
        ),
        axis_legend={
            "n": "indice de position (n=1 pour p1=2, n=2 pour p2=3, ...)",
            "Digamma_1/2(n)": "residu SB(n) - 64.P(n) specifique au RATIO 1/2 (pas 1/3, 1/4, ...)",
        },
        critical_summary=(
            "GRAPHIQUE : trace la fonction Digamma_1/2(n) = SB(n) - 64.P(n), "
            "ATTENTION SPECIFIQUE AU RATIO 1/2 (constante 64 = 128/2). Pour un ratio "
            "1/3 la constante serait differente, la courbe donc AUSSI. "
            "L'axe horizontal est l'indice n. L'axe vertical est le residu obtenu "
            "en soustrayant a SB(n) la contribution du n-ieme premier P(n) ponderee "
            "par 64. Ce residu est CE QUI RESTE une fois le premier extrait, permet "
            "de RECONSTRUIRE P(n) = (SB(n) - digamma) / 64. "
            "NE MONTRE PAS le ratio spectral (voir RATIO) ni les primes bruts (voir PRIME). "
            "Source : methode_spectral.thy::reconstruction_1_2."
        ),
    )


def _compute_invariant(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    """D(n,P) = SB - SA - 1/2 * P  (invariant theorique pour le ratio 1/2)."""
    pts = []
    for n in range(n_min, n_max + 1):
        prime = core.get_prime_at_position(n)
        if prime is None:
            continue
        d_x8 = core._SB_scaled_x8(n) - core._SA_scaled_x8(n) - 4 * prime
        d_val = d_x8 / 8.0
        pts.append(CurvePoint(n=n, y_exact=d_x8, y_float=_project(d_val, scale),
                              prime=prime,
                              extra={"D_exact_x8": d_x8, "D_value": d_val}))
    return CurveData(
        kind=CurveKind.INVARIANT, primary_label="D(n,P) : invariant", n_min=n_min, n_max=n_max, scale=scale,
        title=f"Invariant spectral D(n,P) = SB(n) - SA(n) - (1/2).P(n)   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="D(n,P) : invariant theorique" + (f"  ({scale})" if scale != "linear" else ""),
        points=pts,
        formula="D(n,P) = SB(n) - SA(n) - (1/2) * P(n)  (calcule en entier scale x8 pour exactitude)",
        axis_legend={
            "n": "indice de position dans la table des premiers",
            "D(n,P)": "SB(n) - SA(n) - (1/2).P(n) : doit etre regulier si le ratio 1/2 est valide",
        },
        critical_summary=(
            "GRAPHIQUE : trace l'invariant D(n,P) = SB(n) - SA(n) - (1/2).P(n). "
            "Test de coherence de la Methode Spectrale 1/2 : si le ratio 1/2 est "
            "correct, D doit etre regulier (nul ou lineaire). Un ecart signale une "
            "possible anomalie theorique. Calcul en entier x8 (scale multiplicatif) "
            "pour garantir l'exactitude. "
            "NE MONTRE PAS l'origine causale d'eventuels ecarts."
        ),
    )


def _compute_ratio(core: SpectralMethodCore, n_min: int, n_max: int) -> CurveData:
    """SA/SB en lineaire (toujours)."""
    pts = []
    for n in range(n_min, n_max + 1):
        sa_x8 = core._SA_scaled_x8(n)
        sb_x8 = core._SB_scaled_x8(n)
        if sb_x8 == 0:
            continue
        ratio = sa_x8 / sb_x8
        pts.append(CurvePoint(n=n, y_exact=ratio, y_float=ratio,
                              prime=core.get_prime_at_position(n),
                              extra={"SA_x8": sa_x8, "SB_x8": sb_x8}))
    return CurveData(
        kind=CurveKind.RATIO_SA_SB, primary_label="Rapport SA(n)/SB(n)", n_min=n_min, n_max=n_max, scale="linear",
        title=f"Rapport spectral SA(n) / SB(n) - Convergence asymptotique vers 1/2   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="Rapport SA(n) / SB(n)  (sans unite)",
        points=pts,
        target_line=0.5,
        target_label="Cible asymptotique 1/2",
        formula="SA(n)/SB(n) -> 1/2 quand n -> infini",
        axis_legend={
            "n": "indice de position dans la table des premiers",
            "SA/SB": "rapport spectral (adimensionnel), doit tendre vers 0.5",
            "ligne verte pointillee": "cible asymptotique 1/2",
        },
        critical_summary=(
            "GRAPHIQUE : trace le rapport spectral SA(n) / SB(n) qui, selon la Methode "
            "Spectrale 1/2 de Savard, converge vers 1/2 quand n -> infini. La ligne "
            "verte pointillee marque la cible asymptotique. Les annotations montrent "
            "les valeurs aux extremums et le point de plus grande divergence. "
            "NE MONTRE PAS d'autres ratios (1/3, 1/4, ...). "
            "Source : methode_spectral.thy::preuve_rapport_spectral_limite_savard."
        ),
    )


def _compute_gap(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    """Gap = p(n+1) - p(n) en fonction de n."""
    pts = []
    for n in range(n_min, n_max + 1):
        p1 = core.get_prime_at_position(n)
        p2 = core.get_prime_at_position(n + 1)
        if p1 is None or p2 is None:
            continue
        gap = p2 - p1
        pts.append(CurvePoint(n=n, y_exact=gap, y_float=_project(gap, scale),
                              prime=p1, extra={"prime_next": p2}))
    return CurveData(
        kind=CurveKind.GAP, primary_label="Delta_p(n) : ecart consecutif", n_min=n_min, n_max=n_max, scale=scale,
        title=f"Ecarts consecutifs entre premiers : Delta_p(n) = P(n+1) - P(n)   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="Delta_p(n) : ecart entre P(n+1) et P(n)"
                + (f"  ({scale})" if scale != "linear" else ""),
        points=pts,
        formula="Delta_p(n) = P(n+1) - P(n)",
        axis_legend={
            "n": "indice de position dans la table des premiers",
            "Delta_p(n)": "difference entre le (n+1)-ieme et le n-ieme premier",
        },
        critical_summary=(
            "GRAPHIQUE : trace les ecarts consecutifs Delta_p(n) = P(n+1) - P(n) "
            "entre premiers successifs. Utile pour visualiser l'irregularite de "
            "leur distribution (ecarts pairs a l'exception de 3-2=1). "
            "L'axe horizontal est l'indice de position n. L'axe vertical est "
            "l'ecart en unites entieres. "
            "NE MONTRE PAS de tendance moyenne (voir loi de Cramer / conjectures)."
        ),
    )


def _compute_prime(core: SpectralMethodCore, n_min: int, n_max: int, scale: str) -> CurveData:
    pts = []
    for n in range(n_min, n_max + 1):
        p = core.get_prime_at_position(n)
        if p is None:
            continue
        pts.append(CurvePoint(n=n, y_exact=p, y_float=_project(p, scale), prime=p))
    return CurveData(
        kind=CurveKind.PRIME, primary_label="P(n) : n-ieme premier", n_min=n_min, n_max=n_max, scale=scale,
        title=f"Croissance des nombres premiers : P(n) fonction de n   [n = {n_min}..{n_max}]",
        x_label=f"n : indice de position dans la table des 1000 premiers ({n_min} <= n <= {n_max})",
        y_label="P(n) : valeur du n-ieme premier"
                + (f"  ({scale})" if scale != "linear" else ""),
        points=pts,
        formula="P(n) = n-ieme nombre premier (1..1000)",
        axis_legend={
            "n": "indice de position (n=1 pour p1=2)",
            "P(n)": "valeur du n-ieme nombre premier (2, 3, 5, 7, 11, ...)",
        },
        critical_summary=(
            "GRAPHIQUE : trace la croissance des nombres premiers P(n) en fonction "
            "de leur indice de position n. Suit approximativement P(n) ~ n * ln(n) "
            "(theoreme des nombres premiers). L'axe horizontal est n, l'axe vertical "
            "est la valeur reelle du n-ieme premier. "
            "NE MONTRE PAS la structure spectrale (voir SA, SB, RATIO). "
            "Source : table des 1000 premiers embarquee dans SpectralMethodCore."
        ),
    )


# --------------------------------------------------------------------------
# API publique
# --------------------------------------------------------------------------


def compute_curve(
    core: SpectralMethodCore,
    kind: str | CurveKind,
    n_min: int,
    n_max: int,
    scale: Optional[str] = None,
) -> CurveData:
    """Calcule une courbe pour le type demande.

    Args:
        core: SpectralMethodCore initialise.
        kind: "SA" | "SB" | "SA_SB" | "digamma" | "invariant" | "ratio" | "gap" | "prime".
        n_min, n_max: bornes (1..1000).
        scale: "linear" | "log10" | "log2" | "auto" (defaut : choix auto selon donnees).

    Returns:
        CurveData prete a etre rendue.
    """
    # Validation bornes
    if n_min < 1:
        raise ValueError(f"n_min doit etre >= 1 (recu {n_min})")
    max_pos = len(core.prime_list)
    if n_max > max_pos:
        raise ValueError(f"n_max={n_max} > taille table primes ({max_pos})")
    if n_max < n_min:
        raise ValueError(f"n_max ({n_max}) < n_min ({n_min})")

    # Normalisation kind
    try:
        k = CurveKind(kind) if isinstance(kind, str) else kind
    except ValueError:
        raise ValueError(f"Kind inconnu : '{kind}'. Choix : {list_supported_kinds()}")

    # Auto-scale : log si valeurs toutes positives ET amplitude > 100x
    requested = scale or "auto"
    if requested == "auto":
        eff_scale = _auto_scale(core, k, n_min, n_max)
    else:
        eff_scale = requested

    if eff_scale not in {"linear", "log10", "log2"}:
        raise ValueError(f"Scale invalide : '{eff_scale}' (linear|log10|log2|auto)")

    if k == CurveKind.SA:
        return _compute_SA(core, n_min, n_max, eff_scale)
    if k == CurveKind.SB:
        return _compute_SB(core, n_min, n_max, eff_scale)
    if k == CurveKind.SA_SB:
        return _compute_SA_SB(core, n_min, n_max, eff_scale)
    if k == CurveKind.DIGAMMA:
        return _compute_digamma(core, n_min, n_max, eff_scale)
    if k == CurveKind.INVARIANT:
        return _compute_invariant(core, n_min, n_max, eff_scale)
    if k == CurveKind.RATIO_SA_SB:
        return _compute_ratio(core, n_min, n_max)  # toujours linear
    if k == CurveKind.GAP:
        return _compute_gap(core, n_min, n_max, eff_scale)
    if k == CurveKind.PRIME:
        return _compute_prime(core, n_min, n_max, eff_scale)
    raise ValueError(f"Kind {k} non implemente")


def _auto_scale(core: SpectralMethodCore, k: CurveKind, n_min: int, n_max: int) -> str:
    """Choix automatique d'echelle selon les donnees.

    Regle :
      - Si toutes les valeurs > 0 ET max/min > 100 -> log10
      - Sinon -> linear (pour conserver les zeros/negatifs visibles)
    """
    if k == CurveKind.RATIO_SA_SB:
        return "linear"
    # On echantillonne quelques valeurs pour decider
    sample_ns = [n_min, (n_min + n_max) // 2, n_max]
    vals: list[float] = []
    for n in sample_ns:
        try:
            if k == CurveKind.SA:
                vals.append(float(core._SA_int(n)))
            elif k == CurveKind.SB:
                vals.append(float(core._SB_int(n)))
            elif k == CurveKind.SA_SB:
                vals.append(float(core._SA_int(n)))
                vals.append(float(core._SB_int(n)))
            elif k == CurveKind.DIGAMMA:
                d = core.reconstruct_prime_1_2(n)
                if d:
                    vals.append(float(d.digamma))
            elif k == CurveKind.INVARIANT:
                p = core.get_prime_at_position(n)
                if p:
                    vals.append((core._SB_scaled_x8(n) - core._SA_scaled_x8(n) - 4 * p) / 8.0)
            elif k == CurveKind.GAP:
                p1 = core.get_prime_at_position(n)
                p2 = core.get_prime_at_position(n + 1)
                if p1 and p2:
                    vals.append(float(p2 - p1))
            elif k == CurveKind.PRIME:
                p = core.get_prime_at_position(n)
                if p:
                    vals.append(float(p))
        except Exception:
            continue
    if not vals:
        return "linear"
    if any(v <= 0 for v in vals):
        return "linear"
    pos_vals = [v for v in vals if v > 0]
    if not pos_vals:
        return "linear"
    ratio = max(pos_vals) / min(pos_vals)
    return "log10" if ratio > 100 else "linear"


def list_supported_kinds() -> list[str]:
    """Retourne la liste des courbes supportees (pour aide CLI)."""
    return [k.value for k in CurveKind]

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
