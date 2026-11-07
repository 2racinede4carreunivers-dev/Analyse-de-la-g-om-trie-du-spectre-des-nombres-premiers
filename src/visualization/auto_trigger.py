"""Detecteur d'intention de visualisation pour Gabriel.

Analyse une question en francais (sans LLM) et determine si l'utilisateur
demande implicitement un graphique. Si oui, identifie :
  - le type de courbe (SA, SB, digamma, ratio, gap, etc.)
  - l'intervalle [n_min, n_max]
  - le souhait d'export PNG

Approche : 100% deterministe (regex + mots-cles). Aucun appel LLM,
zero hallucination, latence quasi nulle.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Optional

from .curves import CurveKind


@dataclass
class VisualizationIntent:
    """Resultat de la detection d'intention de visualisation."""
    kind: CurveKind
    n_min: int
    n_max: int
    want_png: bool = False
    confidence: float = 1.0  # 0..1
    reasoning: str = ""      # Pourquoi cette detection (pour audit)
    matched_keywords: list[str] = None  # type: ignore
    # Si non-None, la visualisation utilise une courbe RsP (config 1x1/sym/chaos-savard/ord)
    # au lieu d'une CurveKind classique. Le champ kind est alors utilise comme placeholder
    # (typiquement CurveKind.RATIO_SA_SB) et le calcul passe par compute_rsp_curve.
    rsp_config: Optional[str] = None

    def __post_init__(self):
        if self.matched_keywords is None:
            self.matched_keywords = []


# =============================================================
# Patterns RsP-config : detection PRIORITAIRE des configs specifiques
# avant le fallback generique "rapport spectral" -> RATIO_SA_SB.
# Ordre : du plus specifique au moins specifique.
# =============================================================
_RSP_CONFIG_PATTERNS: list[tuple[str, list[str]]] = [
    # chaos-savard : convention alternee Philippe Thomas Savard
    ("chaos-savard", [
        r"chaos[\s\-_]?savard",
        r"chaotique[\s\-_]?savard",
        r"savard[\s\-_]?chaos",
        r"convention\s+alternee",
        r"formule\s+alternee",
        r"asymetri\w*\s+chaotique",        # "asymetrique chaotique" / "asymetrie chaotique"
        r"chaotique\s+asymetri\w*",
        r"comparaison\s+chaotique",
        r"\bchaotique\b",                   # standalone (en dernier des patterns chaos)
    ]),
    # asymetrique ordonnee
    ("ord", [
        r"asymetri\w*\s+ordonn\w*",
        r"ordonn\w*\s+asymetri\w*",
        r"comparaison\s+ordonn\w*",
        r"\bordonn\w*\b",                   # standalone
    ]),
    # n×n symetrique
    ("sym", [
        r"n\s*\*\s*n\s+symetri\w*",
        r"symetri\w*\s+n\s*\*\s*n",
        r"symetri\w*\s+n\s*x\s*n",
        r"n\s*x\s*n\s+symetri\w*",
        r"comparaison\s+symetri\w*",
        r"\bsymetri\w*\b",
    ]),
    # 1x1
    ("1x1", [
        r"1\s*x\s*1",
        r"rapport\s+1\s*x\s*1",
    ]),
]


def _detect_rsp_config(qnorm: str) -> tuple[Optional[str], list[str]]:
    """Identifie une config RsP specifique. Retourne (config, mots-cles)."""
    matched: list[str] = []
    for cfg, patterns in _RSP_CONFIG_PATTERNS:
        for pat in patterns:
            m = re.search(pat, qnorm, re.IGNORECASE)
            if m:
                matched.append(m.group(0).strip())
                return cfg, matched
    return None, matched


# --------------------------------------------------------------------------
# Mots-cles
# --------------------------------------------------------------------------
# Verbes/noms qui signalent une volonte de visualisation.
# Liste volontairement stricte pour eviter les faux positifs
# (ex: "montre", "voir", "schema" dans une discussion conceptuelle).
# Marqueurs conversationnels/theoriques qui BLOQUENT l'auto-trigger visualisation
# (Philippe 2026-02) : quand la question est une DISCUSSION conceptuelle et non
# une demande de graphique, la presence isolee de "sa"/"voir"/"schema" ne doit
# PAS declencher la visualisation SA/SB. Ces marqueurs suggerent :
#  - une reference a d'autres theories (Archimede, parabole, quadrature)
#  - une explication conceptuelle ("il s'agit", "laisse-moi te", "en soit")
#  - une description d'un schema NON-spectral fournit par l'utilisateur
_CONVERSATIONAL_ANTI_PATTERNS: set[str] = {
    # Autres theories mathematiques classiques
    "archimede", "parabole", "quadrature", "trifocal", "trifocale",
    "pythagore", "euclide", "descartes", "riemann", "galois", "hilbert",
    # Marqueurs de discussion / reformulation
    "il s'agit", "il s agit", "laisse moi", "laisse-moi",
    "je t'explique", "je vais t'expliquer", "je vais te faire",
    "en soit", "en soi", "en realite", "en fait", "en somme",
    "d'abord", "d abord", "ensuite", "par ailleurs", "toutefois",
    "cependant", "neanmoins", "en definitive",
    # Metadiscours sur un schema fourni par l'utilisateur
    "sur mon schema", "sur ce schema", "dans mon schema", "mon dessin",
    "l'image", "cette image", "la figure", "cette figure",
    "annotation", "annotations", "annote",
    # Descriptions geometriques generales (non spectrales)
    "aire", "aires", "surface", "surfaces", "perimetre", "perimeter",
    "triangle", "triangles", "carre", "carres", "rectangle", "rectangles",
    "cercle", "cercles", "polygone", "polygones",
    "peser", "peser theorique", "pesee", "balancier",
    # v3.30 (Philippe 2026-02) : marqueurs d'OPINION / DISCUSSION EXPERTE.
    # Une question qui sollicite un jugement, une opinion, un avis expert
    # sur la theorie/methode n'est PAS une demande de graphique meme si
    # elle contient des mots-cles isoles (voir, sa, schema...).
    "ton opinion", "ton avis", "ton point de vue", "ton jugement",
    "quel est ton", "penses-tu", "penses tu", "que penses",
    "qu'en penses", "qu en penses", "selon toi", "d'apres toi", "d apres toi",
    "assistant expert", "expert de la", "experts de la",
    "analyse d'expert", "analyse d expert", "avis d'expert", "avis d expert",
    "theorie geometrique", "theorie des nombres", "geometrie du spectre",
    "merite d'etre", "merite d etre", "merite-t-elle", "merite t elle",
    "peut-elle", "peut elle", "est-elle", "est elle",
    "avenir", "futur", "suite logique",
    "archives", "publication scientifique", "soumise", "soumettre",
    "opinion", "jugement",
    # Cas particulier (Philippe 2026-02) : "savoir" en tant que verbe
    # d'interrogation ("le premier point est A SAVOIR...", "il faut savoir")
    "a savoir", "il faut savoir", "faut-il savoir", "sans savoir",
    # Marqueur du nom propre "Savard" (Philippe Thomas Savard) - la mention
    # de l'auteur signale une discussion sur son oeuvre, pas une demande de
    # visualisation. On l'ajoute en anti-pattern (compte pour 1 hit).
    "savard",
}


def _has_conversational_context(qnorm: str, question_len: int) -> tuple[bool, list[str]]:
    """
    v3.28 : Detecte si la question est une DISCUSSION conceptuelle plutot
    qu'une demande de visualisation spectrale.

    Regle : si >= 2 anti-patterns detectes OU si question > 300 chars avec
    >= 1 anti-pattern, on considere que c'est une conversation et on
    BLOQUE l'auto-trigger visualisation.

    Args:
        qnorm: question normalisee (accents retires, lowercase).
        question_len: longueur brute de la question originale.

    Returns:
        (is_conversational, hits) : True si contexte conversationnel detecte,
        et la liste des anti-patterns matches (pour le reasoning).
    """
    hits = [p for p in _CONVERSATIONAL_ANTI_PATTERNS if p in qnorm]
    if len(hits) >= 2:
        return True, hits
    if question_len > 300 and len(hits) >= 1:
        return True, hits
    return False, hits


_VIZ_KEYWORDS = {
    "courbe", "courbes", "graphique", "graphiques", "graphe", "graphes",
    "montre", "montrer", "montre-moi",
    "trace", "tracer", "traces", "tracerais",
    "dessine", "dessiner", "dessines",
    "illustre", "illustrer", "illustres", "illustrant",
    "visualise", "visualiser", "visualises",
    "evolution", "evolue", "evoluent", "evoluer",
    "comporte", "comportement",
    "convergence", "converge", "convergent",
    "represente", "representer", "represente",
    "affiche", "afficher", "affichant",
    "diagramme", "plot",
}

# Mots/expressions qui indiquent qu'on demande une explication d'un
# graphique deja affiche (et non la generation d'un nouveau graphique).
_EXPLANATION_KEYWORDS = {
    "explique", "expliquer", "explication", "detail", "details",
    "interpreter", "interpretation", "analyse", "analyser",
    "pourquoi", "axe", "axes", "legende", "legendes",
    "dernier graphique", "dernier graphe", "ce graphique", "ce graphe",
}

# Verbes de generation explicite : s'ils sont presents, on garde l'auto-trigger.
_VIZ_GENERATION_KEYWORDS = {
    "trace", "tracer", "dessine", "dessiner", "visualise", "visualiser",
    "genere", "generer", "produis", "produire", "exporte", "exporter",
    "plot",
}

# Mots qui suggerent l'export PNG (article scientifique, etc.)
_PNG_KEYWORDS = {
    "png", "image", "fichier", "pdf",
    "article", "scientifique", "publication", "papier",
    "exporte", "exporter", "exportation", "sauvegarde", "sauvegarder",
    "citer", "citable", "cite",
    "rapport", "document",
}

# Mots qui suggerent un tableau de donnees
_TABLE_KEYWORDS = {
    "tableau", "table", "tableaux", "tabule", "tabuler",
    "valeurs", "chiffres", "donnees",
}

# Map mots-cles -> CurveKind
# L'ordre importe : on cherche les expressions composees en premier.
# Chaque pattern peut etre :
#   - une string -> matched as 'word' avec bornes \b (regex)
#   - une string finissant par espace = matche comme substring brut (pour compatibilite)
_KIND_PATTERNS: list[tuple[CurveKind, list[str]]] = [
    # SA_SB doit etre teste AVANT SA et SB seuls
    (CurveKind.SA_SB, [
        r"sa\s+et\s+sb", r"sb\s+et\s+sa", r"sa\s*\+\s*sb",
        r"suites?\s+a\s+et\s+b", r"suite\s+a\s+et\s+suite\s+b",
        r"sommes?\s+a\s+et\s+b", r"sa\s+puis\s+sb",
        r"superposer?\s+sa\s+sb",
    ]),
    (CurveKind.RATIO_SA_SB, [
        r"ratio\s+sa\s*/\s*sb", r"ratio\s+sa\s+sb",
        r"rapport\s+sa\s*/\s*sb", r"rapport\s+sa\s+sb",
        r"\bratio\b", r"rapport\s+spectral", r"rapport\s+asymptotique",
        r"\bsa\s*/\s*sb\b", r"convergence\s+vers\s+1\s*/\s*2",
        r"convergence\s+asymptotique",
    ]),
    (CurveKind.SA, [
        r"\bsa\s*\(\s*n\s*\)", r"\bsa\s+de\s+n", r"somme\s+alternee\s+a",
        r"\bsomme\s+a\b", r"suite\s+alternee\s+a", r"\bsuite\s+a\b",
        r"\bsa\b",
    ]),
    (CurveKind.SB, [
        r"\bsb\s*\(\s*n\s*\)", r"\bsb\s+de\s+n", r"somme\s+alternee\s+b",
        r"\bsomme\s+b\b", r"suite\s+alternee\s+b", r"\bsuite\s+b\b",
        r"\bsb\b",
    ]),
    (CurveKind.DIGAMMA, [
        r"\bdigamma\b", r"\bpsi\b", r"ψ", r"fonction\s+psi",
        r"fonction\s+digamma",
    ]),
    (CurveKind.INVARIANT, [
        r"\binvariant\b", r"d\s*\(\s*n\s*,\s*p\s*\)", r"d\s+de\s+n",
        r"sb\s*-\s*sa\s*-\s*z\s*\*\s*p", r"\bsb\s*-\s*sa\b",
        r"ecart\s+structurel",
    ]),
    (CurveKind.GAP, [
        r"\bgap\b", r"\bgaps\b", r"\becart\b", r"\becarts\b", r"\becartement\b",
        r"delta[_\s]p", r"p\s*\(\s*n\s*\+\s*1\s*\)\s*-\s*p\s*\(\s*n\s*\)",
        r"premiers\s+consecutifs", r"primes\s+consecutifs",
    ]),
    (CurveKind.PRIME, [
        r"\bpremiers\b", r"\bprimes\b", r"\bp\s*\(\s*n\s*\)",
        r"nombres?\s+premiers?", r"croissance\s+des\s+premiers",
        r"n[-\s]ieme\s+premier",
    ]),
]

# Patterns d'intervalle (regex). Tous capturent (n_min, n_max).
# On teste du plus specifique au moins specifique.
_RANGE_PATTERNS = [
    # "n=1..50" / "n=1 a 50" / "1..1000"
    re.compile(r"n\s*=\s*(\d+)\s*(?:\.\.|a|à|jusqu['e]\s*a|jusqu['e]\s*à)\s*(?:n\s*=\s*)?(\d+)", re.IGNORECASE),
    re.compile(r"(?<!\d)(\d{1,4})\s*\.\.\s*(\d{1,4})(?!\d)"),
    # "de 1 a 50" / "de 1 à 50"
    re.compile(r"de\s+(\d+)\s+(?:a|à)\s+(\d+)", re.IGNORECASE),
    # "entre 1 et 50"
    re.compile(r"entre\s+(\d+)\s+et\s+(\d+)", re.IGNORECASE),
    # "n entre 1 et 50"
    re.compile(r"n\s+entre\s+(\d+)\s+et\s+(\d+)", re.IGNORECASE),
    # "sur l'intervalle [1, 50]" / "[1,50]"
    re.compile(r"\[\s*(\d+)\s*[,;]\s*(\d+)\s*\]"),
    # "sur 1..50"
    re.compile(r"sur\s+(\d+)\s*\.\.\s*(\d+)", re.IGNORECASE),
    # "pour les N premiers" / "premiers 100 termes" -> 1..N
]

# Pattern "premiers N" / "N premiers" -> 1..N
_FIRST_N_PATTERNS = [
    re.compile(r"(?:les\s+)?(\d+)\s+(?:premiers|premieres|premiers\s+termes|premiers\s+nombres)", re.IGNORECASE),
    re.compile(r"premiers?\s+(\d+)", re.IGNORECASE),
]

# Limites strictes
_N_MIN_ABS = 1
_N_MAX_ABS = 1000
_DEFAULT_N_MIN = 1
_DEFAULT_N_MAX = 50  # Defaut raisonnable si pas d'intervalle precise


def _strip_accents(s: str) -> str:
    """Retire les accents pour faciliter le matching."""
    nfd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _normalize(question: str) -> str:
    """Normalise : minuscules + sans accents + espaces simples."""
    q = _strip_accents(question.lower())
    q = re.sub(r"\s+", " ", q).strip()
    return q


def _detect_kind(qnorm: str, original: str = "") -> tuple[Optional[CurveKind], list[str]]:
    """Identifie le type de courbe demande, retourne (kind, mots-cles matches).

    v3.30 (Philippe 2026-02) : quand seul le pattern generique `\\bsa\\b` ou
    `\\bsb\\b` matche (pronom possessif francais 'sa'/'sb'), on exige que le
    token soit ecrit en MAJUSCULES dans le texte ORIGINAL pour eviter les
    faux positifs sur 'sa place', 'sa suite logique', etc.
    """
    matched: list[str] = []
    # Patterns "ambigus" (matchent aussi des mots courants francais)
    _AMBIGUOUS_STANDALONE = {r"\bsa\b", r"\bsb\b"}
    for kind, patterns in _KIND_PATTERNS:
        for pat in patterns:
            m = re.search(pat, qnorm, re.IGNORECASE)
            if m:
                # Si c'est un pattern ambigu ET qu'on a le texte original,
                # exiger la casse MAJUSCULE dans l'original.
                if pat in _AMBIGUOUS_STANDALONE and original:
                    token = m.group(0).strip()
                    # Chercher SA ou SB en majuscules dans l'original
                    upper_re = r"\b" + token.upper() + r"\b"
                    if not re.search(upper_re, original):
                        continue  # pronom francais, on ignore
                matched.append(m.group(0).strip())
                return kind, matched
    return None, matched


def _detect_range(qnorm: str) -> Optional[tuple[int, int]]:
    """Extrait [n_min, n_max] depuis la question. Retourne None si non trouve."""
    # Patterns "n_min..n_max"
    for pat in _RANGE_PATTERNS:
        m = pat.search(qnorm)
        if m:
            try:
                a, b = int(m.group(1)), int(m.group(2))
                if a > b:
                    a, b = b, a
                a = max(_N_MIN_ABS, a)
                b = min(_N_MAX_ABS, b)
                if a <= b:
                    return (a, b)
            except (ValueError, IndexError):
                continue
    # Pattern "N premiers" -> 1..N
    for pat in _FIRST_N_PATTERNS:
        m = pat.search(qnorm)
        if m:
            try:
                n = int(m.group(1))
                if 2 <= n <= _N_MAX_ABS:
                    return (1, n)
            except (ValueError, IndexError):
                continue
    return None


def _detect_png_intent(qnorm: str) -> bool:
    """Detecte si l'utilisateur souhaite un PNG citable."""
    for kw in _PNG_KEYWORDS:
        if kw in qnorm:
            return True
    return False


def _is_explanation_followup(qnorm: str) -> tuple[bool, list[str]]:
    """Detecte une demande d'explication d'un graphique deja produit.

    Regle:
      - il faut une reference au graphique/courbe
      - il faut au moins 1 marqueur d'explication
      - il ne faut PAS de verbe explicite de generation de nouveau graphique
    """
    references = [kw for kw in {"graphique", "graphe", "courbe", "diagramme", "plot"} if kw in qnorm]
    if not references:
        return False, []

    expl_hits = [kw for kw in _EXPLANATION_KEYWORDS if kw in qnorm]
    if not expl_hits:
        return False, []

    has_generation = any(kw in qnorm for kw in _VIZ_GENERATION_KEYWORDS)
    if has_generation:
        return False, []

    return True, expl_hits


def detect_visualization_intent(question: str) -> Optional[VisualizationIntent]:
    """Analyse une question et retourne un VisualizationIntent si une visualisation est demandee.

    Args:
        question: question utilisateur en francais (peut contenir accents).

    Returns:
        VisualizationIntent si une visualisation est detectee, None sinon.
    """
    if not question or not question.strip():
        return None
    qnorm = _normalize(question)
    question_len = len(question)

    # 0) GARDE-FOU v3.28 (Philippe 2026-02) : detecter le contexte conversationnel
    # AVANT toute detection viz. Si l'utilisateur discute d'un concept, d'un
    # schema fourni, ou d'autres theories (Archimede, quadrature, etc.), on
    # ne doit PAS auto-declencher un graphique SA/SB, meme si des mots-cles
    # isoles matchent (comme "sa" dans "sa longueur" ou "voir" dans "tu peux voir").
    is_conversational, conv_hits = _has_conversational_context(qnorm, question_len)
    if is_conversational:
        return None

    # 1) Verifier qu'il y a un mot-cle de visualisation
    # v3.30 (Philippe 2026-02) : matching MOT-ENTIER (regex \b...\b) pour
    # eviter que "savoir" (present dans "a savoir", "il faut savoir")
    # matche "voir" en sous-chaine.
    viz_hits: list[str] = []
    for kw in _VIZ_KEYWORDS:
        if re.search(r"\b" + re.escape(kw) + r"\b", qnorm):
            viz_hits.append(kw)
    if not viz_hits:
        return None

    # 1.bis) Si l'utilisateur demande surtout une explication du graphique
    # precedent (axes, interpretation, pourquoi...), on ne doit pas regenirer.
    is_explaining, _expl_hits = _is_explanation_followup(qnorm)
    if is_explaining:
        return None

    # 2) PRIORITE : detecter une config RsP specifique (chaos-savard, ord, sym, 1x1)
    rsp_cfg, rsp_matches = _detect_rsp_config(qnorm)

    # 3) Identifier le type de courbe (CurveKind classique)
    kind, kind_matches = _detect_kind(qnorm, original=question)

    # Si on a une config RsP, on force kind=RATIO_SA_SB (placeholder pour le rendu)
    if rsp_cfg is not None:
        kind = CurveKind.RATIO_SA_SB
        kind_matches = rsp_matches + kind_matches

    if kind is None:
        return None

    # 4) Identifier l'intervalle (defaut 1..50)
    rng = _detect_range(qnorm)
    if rng is None:
        # Pour chaos-savard, defaut 1..15 (au-dela c'est tres proche de 1/2)
        if rsp_cfg == "chaos-savard":
            n_min, n_max = 1, 15
            range_source = "defaut chaos-savard (1..15)"
        else:
            n_min, n_max = _DEFAULT_N_MIN, _DEFAULT_N_MAX
            range_source = "defaut (1..50)"
    else:
        n_min, n_max = rng
        range_source = f"detecte ({n_min}..{n_max})"

    # 5) Detection PNG
    want_png = _detect_png_intent(qnorm)
    # AMELIORATION (Philippe 2026-07-03) : quand une config RsP specifique
    # est detectee (chaos-savard, ord, sym, 1x1), on force want_png=True
    # par defaut car ces graphiques sont typiquement destines aux articles
    # scientifiques et au corpus PDF. L'utilisateur ne devrait pas avoir a
    # ecrire "png" ou "exporter" explicitement pour ces cas emblematiques.
    if rsp_cfg is not None and not want_png:
        want_png = True

    # 6) Confidence (heuristique simple)
    # +0.4 pour mot-cle viz, +0.4 pour type identifie, +0.2 si intervalle explicite
    confidence = 0.4 + 0.4 + (0.2 if rng is not None else 0.0)

    matched = viz_hits[:3] + kind_matches[:2]
    reasoning_parts = [
        f"Mots-cles visualisation : {', '.join(viz_hits[:3])}.",
        f"Type identifie : {kind.value} (matches : {', '.join(kind_matches[:2])}).",
    ]
    if rsp_cfg is not None:
        reasoning_parts.append(f"Config RsP detectee : {rsp_cfg}.")
    reasoning_parts.append(f"Intervalle : {range_source}.")
    reasoning_parts.append(f"PNG demande : {'oui' if want_png else 'non'}.")
    reasoning = " ".join(reasoning_parts)

    return VisualizationIntent(
        kind=kind,
        n_min=n_min,
        n_max=n_max,
        want_png=want_png,
        confidence=confidence,
        reasoning=reasoning,
        matched_keywords=matched,
        rsp_config=rsp_cfg,
    )

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
