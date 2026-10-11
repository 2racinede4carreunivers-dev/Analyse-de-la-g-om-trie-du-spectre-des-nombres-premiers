"""question_graphs.py — Auto-generation contextuelle des graphiques Gabriel.

Mapping :  question canonique (Q1.a, Q1.b, Q1.c, Q1.d, Q2, Q3.a/b/c)
         -> graphique(s) PNG specifique(s) genere(s) dans data/graphs/.

Regle essentielle :  un seul graphique pour la bonne question, pas tous.
                     Q2 (reconstruction) en genere 2 (SA+SB et Digamma).

Tous les graphiques :
  - PNG haute resolution (matplotlib 150 dpi) dans data/graphs/
  - Nommes <Qcode>_<contexte>_<timestamp>.png
  - Annotates : titre + sous-titre dynamique + footer citable

Utilisation typique :
    from src.engines.question_graphs import generate_graphs_for_question
    paths = generate_graphs_for_question(
        question="Q2", core=core, params={"n": 26}, output_dir=Path("data/graphs"),
    )
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..core.spectral_core import SpectralMethodCore
from ..spectral.rsp_curve import compute_rsp_curve
from ..spectral.ratios import build_chaos_savard_blocks
from ..visualization.curves import (
    CurveData, CurveKind, CurvePoint, compute_curve,
)
from ..visualization.png_renderer import (
    MATPLOTLIB_AVAILABLE, render_png,
)


# =============================================================================
# Mapping Question -> Configuration de graphique
# =============================================================================
@dataclass(frozen=True)
class GraphSpec:
    """Specification d'un graphique a generer pour une question."""
    question: str           # "Q1.a", "Q1.b", "Q1.c", "Q1.d", "Q2", "Q3.a/b/c"
    label: str              # ex: "Suites SA et SB", "Digamma", "Courbe rsp-chaos-savard"
    kind: str               # "rsp_curve" | "curve_kind"
    curve_kind: CurveKind | None = None    # si kind == "curve_kind"
    rsp_config: str | None = None          # si kind == "rsp_curve" : 1x1|sym|chaos-savard|ord
    n_range: tuple[int, int] = (1, 100)
    target_line: float | None = 0.5         # ligne cible 1/2 si applicable


QUESTION_GRAPH_MAP: dict[str, list[GraphSpec]] = {
    "Q1.a": [
        GraphSpec(
            question="Q1.a", label="Courbe RsP 1x1",
            kind="rsp_curve", rsp_config="1x1", n_range=(1, 50),
        ),
    ],
    "Q1.b": [
        GraphSpec(
            question="Q1.b", label="Courbe RsP n*n symetrique",
            kind="rsp_curve", rsp_config="sym", n_range=(1, 50),
        ),
    ],
    "Q1.c": [
        GraphSpec(
            question="Q1.c", label="Courbe RsP chaos-Savard (convention alternee)",
            kind="rsp_curve", rsp_config="chaos-savard", n_range=(1, 15),
        ),
    ],
    "Q1.d": [
        GraphSpec(
            question="Q1.d", label="Courbe RsP asymetrique ordonnee",
            kind="rsp_curve", rsp_config="ord", n_range=(1, 50),
        ),
    ],
    "Q2": [
        GraphSpec(
            question="Q2", label="Suites SA et SB",
            kind="curve_kind", curve_kind=CurveKind.SA_SB,
            n_range=(1, 100), target_line=None,
        ),
        GraphSpec(
            question="Q2", label="Digamma calcule",
            kind="curve_kind", curve_kind=CurveKind.DIGAMMA,
            n_range=(1, 100), target_line=None,
        ),
    ],
    "Q3.a": [
        GraphSpec(
            question="Q3.a", label="Ecarts (+,+) consecutifs",
            kind="curve_kind", curve_kind=CurveKind.GAP,
            n_range=(1, 100), target_line=None,
        ),
    ],
    "Q3.b": [
        GraphSpec(
            question="Q3.b", label="Ecarts (-,-) consecutifs",
            kind="curve_kind", curve_kind=CurveKind.GAP,
            n_range=(1, 100), target_line=None,
        ),
    ],
    "Q3.c": [
        GraphSpec(
            question="Q3.c", label="Ecarts (-,+) consecutifs",
            kind="curve_kind", curve_kind=CurveKind.GAP,
            n_range=(1, 100), target_line=None,
        ),
    ],
}


# =============================================================================
# Construction CurveData pour une courbe RsP (1x1/sym/chaos-savard/ord)
# =============================================================================
def _build_rsp_curve_data(
    core: SpectralMethodCore,
    config: str,
    k_min: int,
    k_max: int,
) -> CurveData:
    """Convertit le resultat compute_rsp_curve en CurveData pour rendu PNG.

    Une serie de points (k, RsP_decimal), ligne cible 1/2.
    """
    raw = compute_rsp_curve(core, config, k_max=k_max)
    pts: list[CurvePoint] = []
    for entry in raw:
        if entry.get("error"):
            continue
        k = entry["k"]
        if k < k_min:
            continue
        rsp = entry.get("RsP_decimal", float("nan"))
        pts.append(CurvePoint(n=k, y_exact=rsp, y_float=rsp))
    # v3.36 : ajuste k_max effectif au dernier k valide (utile quand la table
    # de premiers limite le calcul, ex: 'ord' plafonne a k=499 pour 1000 primes)
    effective_k_max = pts[-1].n if pts else k_max
    # Lib subtitle
    titles = {
        "1x1":           "Rapport spectral 1x1 — convergence vers 1/2",
        "sym":           "Rapport spectral symetrique n*n — convergence vers 1/2",
        "chaos-savard":  "Rapport spectral chaos-Savard (convention alternee)",
        "ord":           "Rapport spectral asymetrique ordonne — convergence vers 1/2",
        "chaos":         "Rapport spectral asymetrique chaotique",
    }
    formulas = {
        "1x1":           "RsP = (SA(n+1)-SA(n)) / (SB(n+1)-SB(n))",
        "sym":           "RsP = (sum_SA(A)-sum_SA(B)) / (sum_SB(A)-sum_SB(B))  avec |A|=|B|=k",
        "chaos-savard":  "RsP = (alt_SA(A)-alt_SA(B)) / (alt_SB(A)-alt_SB(B)) "
                         "avec A=[p_{k+1}..p_{2k}], B=[p_{2k+1},p_1..p_k]",
        "ord":           "RsP = (sum_SA(A)-sum_SA(B)) / (sum_SB(A)-sum_SB(B))  asymetrie ordonnee |B|=|A|+1",
        "chaos":         "RsP = (sum_SA(A)-sum_SA(B)) / (sum_SB(A)-sum_SB(B))  chaotique simple",
    }
    # v3.36 : titre reflete le k_max effectif (peut differer du k_max demande
    # quand la table de primes limite le calcul). Titre multi-lignes si limite.
    title_line1 = titles.get(config, config)
    title_line2 = f"k={k_min}..{effective_k_max}"
    if effective_k_max < k_max:
        primes_needed = 2 * effective_k_max + 1
        title_line2 += f"  (demande k_max={k_max} — limite : {primes_needed} primes utilises)"
    full_title = f"{title_line1}\n{title_line2}"
    return CurveData(
        kind=CurveKind.RATIO_SA_SB,   # reutilise le rendu ratio
        n_min=k_min, n_max=effective_k_max, scale="linear",
        title=full_title,
        x_label="k (taille du bloc / index de la courbe)",
        y_label="RsP",
        points=pts,
        target_line=0.5,
        target_label="cible 1/2",
        formula=formulas.get(config, f"config={config}"),
        # v3.36 : active l'echelle adaptative pour toutes les courbes RsP.
        # Utile surtout pour 'ord' et 'chaos-savard' qui divergent a petit k.
        adaptive_scale=True,
        zoom_y_window=0.02,
    )


# =============================================================================
# API publique
# =============================================================================
def generate_graphs_for_question(
    question: str,
    core: SpectralMethodCore,
    params: dict[str, Any] | None = None,
    output_dir: Path | str = "data/graphs",
    dpi: int = 150,
) -> list[Path]:
    """Genere les graphiques specifiques a une question canonique.

    Args:
        question : code de la question ("Q1.a", "Q1.b", ..., "Q3.c").
        core     : SpectralMethodCore initialise.
        params   : parametres specifiques (ex: {"n": 26} pour Q2, {"k_max": 50}).
        output_dir : repertoire de sortie (cree si absent).
        dpi      : resolution PNG.

    Returns:
        Liste des chemins PNG generes (vide si matplotlib absent ou erreur).
    """
    if not MATPLOTLIB_AVAILABLE:
        return []
    params = params or {}
    specs = QUESTION_GRAPH_MAP.get(question, [])
    if not specs:
        return []
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paths: list[Path] = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")

    for spec in specs:
        try:
            # Determine plage n / k
            n_min, n_max = spec.n_range
            # Si caller a specifie un k_max sur Q1.x, on l'utilise
            if spec.kind == "rsp_curve" and "k_max" in params:
                n_max = int(params["k_max"])
            # Q2 : si n est specifie et < 100, on garde 100 par defaut
            # (Philippe veut toujours n=1..100 pour SA/SB/digamma)

            # Build CurveData
            if spec.kind == "rsp_curve":
                curve = _build_rsp_curve_data(
                    core, spec.rsp_config or "1x1", n_min, n_max,
                )
            else:
                curve = compute_curve(
                    core, spec.curve_kind, n_min, n_max,
                )

            # Filename : Q1c_chaos-savard_k15_TIMESTAMP.png
            qslug = spec.question.replace(".", "")
            ctx = (spec.rsp_config or (spec.curve_kind.value if spec.curve_kind else "x"))
            filename = f"{qslug}_{ctx}_n{n_min}-{n_max}_{ts}"

            path = render_png(curve, output_dir, dpi=dpi, filename=filename)
            paths.append(path)
        except Exception as exc:
            # Logue silencieusement ; ne casse pas la commande utilisateur
            import logging
            logging.getLogger(__name__).warning(
                "generate_graphs_for_question(%s) : echec spec %s : %s",
                question, spec.label, exc,
            )
            continue
    return paths


def list_questions() -> list[str]:
    """Retourne les codes de question supportes."""
    return sorted(QUESTION_GRAPH_MAP.keys())


def graph_count_for(question: str) -> int:
    """Combien de graphiques sont generes pour cette question ?"""
    return len(QUESTION_GRAPH_MAP.get(question, []))


def detect_gap_question(p1: int, p2: int) -> str:
    """Detecte Q3.a/b/c selon signes de p1 et p2.

       p1 > 0 et p2 > 0 -> Q3.a (+,+)
       p1 < 0 et p2 < 0 -> Q3.b (-,-)
       sinon (signes melanges) -> Q3.c (-,+)
    """
    if p1 > 0 and p2 > 0:
        return "Q3.a"
    if p1 < 0 and p2 < 0:
        return "Q3.b"
    return "Q3.c"


def detect_rsp_question(case: str) -> str:
    """Detecte Q1.b/c/d selon le cas de configuration.

      'nxn_symetrique' / 'sym' -> Q1.b
      'asym_chaotique' / 'chaos' / 'chaos-savard' -> Q1.c
      'asym_ordonnee' / 'ord' -> Q1.d
    """
    norm = case.lower().strip()
    if norm in ("sym", "nxn_symetrique", "1x1"):
        return "Q1.b" if norm != "1x1" else "Q1.a"
    if norm in ("ord", "asym_ordonnee"):
        return "Q1.d"
    # Tout ce qui ressemble a chaotique -> Q1.c
    return "Q1.c"

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
