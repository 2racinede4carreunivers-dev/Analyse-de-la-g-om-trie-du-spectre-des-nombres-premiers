# -*- coding: utf-8 -*-
"""
Restitution MULTI-RAPPORTS - couche reponse de l'agent Gabriel
==============================================================

Relie la COUCHE REPONSE de l'agent (orchestrator / LLM / HTTP / CLI)
au dispatcher deterministe du pipeline cognitif SANS modifier :
  - les equations du systeme convolutif,
  - src/core/pipeline.py,
  - pipeline_cognitif/ (utilise en LECTURE SEULE via requete_multi_k).

Quand l'utilisateur demande PLUSIEURS rapports 1/k (plage « 1/2 a 1/111 »,
lots « 1/2-1/10, 1/11-1/20 », liste « 1/3, 1/5, 1/7 », « tous les rapports »),
la couche reponse :
  1. detecte la requete multi-rapports dans la question ;
  2. genere le tableau deterministe complet (format identique aux fichiers
     Liste_Premier_Multi_Rapports_K/liste_k*_n*.txt) en reutilisant les
     fichiers precalcules quand la plage est couverte, sinon en appelant
     MultiRatioDispatcher.requete() ;
  3. append le tableau + statistiques a answer_text (marqueur idempotent) ;
  4. fournit une consigne de formulation PAR LOTS pour le prompt LLM
     (llama3.2 ne resume pas : il decrit les lots, le tableau exhaustif
     etant append deterministe apres sa prose).

Aucun jeton LLM n'est consomme pour le tableau : il est 100% deterministe.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Marqueur idempotent d'append dans answer_text
MARQUEUR_MULTI_RATIO = (
    "### Reconstruction multi-rapports 1/k (deterministe - pipeline cognitif)"
)

# Dossier des fichiers precalcules (racine du depot)
_RACINE_DEPOT = Path(__file__).resolve().parents[2]
_DOSSIER_LISTES = "Liste_Premier_Multi_Rapports_K"

# Gardiens (surchargeables via config.yaml > multi_ratio_reponse)
VALEURS_DEFAUT = {
    "enabled": True,
    # k max calcules a la volee sans fichier precalcule
    "max_k_calcul_direct": 2000,
    # k max rendus en ligne (au-dela : extrait)
    "max_k_inline": 5000,
    # taille des lots annoncee dans la consigne LLM
    "lots_lignes": 10,
    # inclure le tableau comparatif large (Digamma, branches)
    "tableau_comparatif": True,
}


# =============================================================================
# DETECTION DE LA REQUETE MULTI-RAPPORTS
# =============================================================================

@dataclass
class RequeteMultiRapports:
    """Plage/liste de rapports 1/k demandee + valeur de n."""
    n: int
    k_debut: int
    k_fin: int
    liste_k: list[int]
    lots: list[tuple[int, int]]     # sous-plages signalees par l'utilisateur
    source: str                     # "plage" | "liste" | "tous" | "lots"

    @property
    def nb_rapports(self) -> int:
        return len(self.liste_k)

    def resume(self) -> str:
        return (
            f"1/{self.k_debut} a 1/{self.k_fin} "
            f"(n={self.n}, {self.nb_rapports} rapports)"
        )


# Plage de ratios : 1/2 à 1/111, 1/2-1/111, 1/2 -> 1/111, 1/2 .. 1/111
_RE_PLAGE_RATIOS = re.compile(
    r"1\s*/\s*(\d{1,12})\s*"
    r"(?:jusqu\s*['’]\s*à|jusqu\s*['’]\s*a|->|→|au|à|a|\.\.|–|-)\s*"
    r"1\s*/\s*(\d{1,12})",
    re.IGNORECASE,
)
# Plage sous forme k : k=2..111, k de 2 a 111, k 2-111
_RE_PLAGE_K = re.compile(
    r"\bk\s*(?:=|\s*de\s*)?\s*(\d{1,12})\s*"
    r"(?:\.\.|->|à|a|au|–|-)\s*(\d{1,12})\b",
    re.IGNORECASE,
)
# Liste explicite : 1/3, 1/5, 1/7
_RE_LISTE_RATIOS = re.compile(r"1\s*/\s*(\d{1,12})")
# n commun : n=10, n 12 ...
_RE_N = re.compile(r"\bn\s*=\s*(\d{1,6})")

# Mots-cles contextuels requis pour eviter les faux positifs
# (« calcule 1/2 - 1/3 » n'est PAS une requete multi-rapports).
_CTX = re.compile(
    r"rapport|1\s*/\s*k|reconstru|premier|ancrage|liste|tous\s+les|multi[-_ ]?r",
    re.IGNORECASE,
)
_CTX_TOUS = re.compile(r"tous\s+les\s+rapports|multi[-_ ]?r", re.IGNORECASE)


def _plage(k_debut: int, k_fin: int) -> list[int]:
    if k_fin < k_debut:
        k_debut, k_fin = k_fin, k_debut
    return list(range(max(2, k_debut), k_fin + 1))


def detecter_requete_multi_rapports(
    texte: str, n_defaut: int = 10
) -> Optional[RequeteMultiRapports]:
    """Detecte plage/liste/lots de rapports 1/k dans une question.

    Retourne None si la question est MONO-rapport (le pipeline normal
    deja gere ce cas) ou hors contexte.
    """
    if not texte or not _CTX.search(texte):
        return None

    m_n = _RE_N.search(texte)
    n = int(m_n.group(1)) if m_n else n_defaut

    # 1) Plages explicites (toutes les sous-plages signalees = « lots »)
    lots = [
        (int(a), int(b))
        for a, b in _RE_PLAGE_RATIOS.findall(texte)
        if int(a) >= 2 and int(b) >= 2
    ]
    if not lots:
        lots = [
            (int(a), int(b))
            for a, b in _RE_PLAGE_K.findall(texte)
            if int(a) >= 2 and int(b) >= 2
        ]

    if lots:
        tous_k: set[int] = set()
        for a, b in lots:
            tous_k.update(_plage(a, b))
        liste_k = sorted(tous_k)
        if len(liste_k) < 2:
            return None
        source = "plage" if len(lots) == 1 else "lots"
        return RequeteMultiRapports(
            n=n, k_debut=liste_k[0], k_fin=liste_k[-1],
            liste_k=liste_k, lots=lots, source=source,
        )

    # 2) Liste explicite de >= 2 rapports distincts (1/3, 1/5, 1/7)
    valeurs = sorted({int(v) for v in _RE_LISTE_RATIOS.findall(texte) if int(v) >= 2})
    if len(valeurs) >= 2:
        return RequeteMultiRapports(
            n=n, k_debut=valeurs[0], k_fin=valeurs[-1],
            liste_k=valeurs, lots=[(valeurs[0], valeurs[-1])], source="liste",
        )

    # 3) « tous les rapports 1/k » sans bornes -> catalogue K_TOUS (2..9)
    if _CTX_TOUS.search(texte):
        liste_k = list(range(2, 10))
        return RequeteMultiRapports(
            n=n, k_debut=2, k_fin=9, liste_k=liste_k,
            lots=[(2, 9)], source="tous",
        )

    return None


# =============================================================================
# GENERATION DU TABLEAU DETERMINISTE
# =============================================================================

def _fichier_couvrant(k_debut: int, k_fin: int, n: int) -> Optional[Path]:
    """Cherche un fichier precalcule liste_kA_kB_nN.txt couvrant [k_debut, k_fin]."""
    for racine in (_RACINE_DEPOT, Path.cwd()):
        dossier = racine / _DOSSIER_LISTES
        if not dossier.is_dir():
            continue
        for f in dossier.glob(f"liste_k*_k*_n{n}.txt"):
            m = re.fullmatch(r"liste_k(\d+)_k(\d+)_n(\d+)\.txt", f.name)
            if not m:
                continue
            a, b = int(m.group(1)), int(m.group(2))
            if a <= k_debut and k_fin <= b:
                return f
    return None


def _extraire_plage_du_fichier(
    fichier: Path, k_debut: int, k_fin: int, n: int
) -> Optional[str]:
    """Extrait les blocs 1/k (ligne + Note associee) pour la plage demandee."""
    try:
        brut = fichier.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("Lecture fichier impossible (%s): %s", fichier, exc)
        return None

    voulus = set(range(k_debut, k_fin + 1))
    blocs: dict[int, list[str]] = {}
    courant: Optional[int] = None
    for ligne in brut.splitlines():
        m = re.match(r"^\s{2}1/(\d+)\b", ligne)
        if m:
            courant = int(m.group(1))
            if courant in voulus:
                blocs.setdefault(courant, []).append(ligne)
        elif courant in voulus and ligne.startswith("    Note:"):
            blocs[courant].append(ligne)
        elif ligne.startswith("===="):
            courant = None

    if len(blocs) != len(voulus):
        return None  # couverture partielle -> calculer

    sep = "=" * 80
    lignes = [
        sep,
        f" REQUETE MULTI-RATIO | n={n} | {len(blocs)} rapport(s) 1/k"
        f" | k_min={k_debut} k_max={k_fin}",
        sep,
    ]
    succes = 0
    for k in sorted(blocs):
        for l in blocs[k]:
            lignes.append(l)
            if "[PREMIER TROUVE]" in l:
                succes += 1
    lignes.append(sep)
    global_ = "OUI" if succes == len(voulus) else "PARTIEL/ECHEC"
    lignes.append(f" Succes : {succes}/{len(voulus)} | Global : {global_}")
    lignes.append(sep)
    lignes.append(f" (source : fichier precalcule {fichier.name})")
    return "\n".join(lignes)


def _import_dispatcher():
    """Import paresseux du dispatcher (sympy) avec repli sys.path."""
    try:
        from pipeline_cognitif.multi_ratio_dispatcher import requete_multi_k  # type: ignore
        return requete_multi_k
    except ImportError:
        import sys
        racine = str(_RACINE_DEPOT)
        if racine not in sys.path:
            sys.path.insert(0, racine)
        from pipeline_cognitif.multi_ratio_dispatcher import requete_multi_k  # type: ignore
        return requete_multi_k


def _stats_depuis_texte(texte: str, req: RequeteMultiRapports) -> dict[str, Any]:
    succes = texte.count("[PREMIER TROUVE]")
    echecs = texte.count("[ECHEC]")
    return {
        "multi_ratio_k_debut": req.k_debut,
        "multi_ratio_k_fin": req.k_fin,
        "multi_ratio_n": req.n,
        "multi_ratio_nb": req.nb_rapports,
        "multi_ratio_succes": succes,
        "multi_ratio_echecs": echecs,
    }


def generer_tableau_multi_rapports(
    req: RequeteMultiRapports, config: Optional[dict] = None
) -> tuple[str, dict[str, Any]]:
    """Genere le tableau deterministe complet + statistiques.

    Retourne (texte_du_tableau, stats_scalaires).
    Priorite : fichier precalcule -> calcul direct (garde-fous config).
    """
    cfg = {**VALEURS_DEFAUT, **(config or {})}
    k_debut, k_fin, n = req.k_debut, req.k_fin, req.n

    # 1) Fichier precalcule couvrant la plage (format canonique, instantane)
    fichier = _fichier_couvrant(k_debut, k_fin, n)
    if fichier is not None:
        texte = _extraire_plage_du_fichier(fichier, k_debut, k_fin, n)
        if texte is not None:
            stats = _stats_depuis_texte(texte, req)
            stats["multi_ratio_source"] = f"fichier:{fichier.name}"
            return texte, stats

    # 2) Calcul direct via le dispatcher (lecture seule)
    nb_a_calculer = req.nb_rapports
    if nb_a_calculer > int(cfg["max_k_calcul_direct"]):
        message = (
            f"Plage trop large pour un calcul direct "
            f"({nb_a_calculer} rapports > max_k_calcul_direct="
            f"{cfg['max_k_calcul_direct']}).\n"
            f"  - Soit demander une plage couverte par un fichier precalcule "
            f"(2..1001, 1002..10001, 10002..100001 existants) ;\n"
            f"  - Soit generer le fichier : python pipeline_cognitif/"
            f"generer_reconstruction_1k.py --n {n} --k-debut {k_debut} "
            f"--k-fin {k_fin} --out "
            f"{_DOSSIER_LISTES}/liste_k{k_debut}_k{k_fin}_n{n}.txt"
        )
        stats = _stats_depuis_texte("", req)
        stats["multi_ratio_source"] = "refus"
        return message, stats

    requete_multi_k = _import_dispatcher()
    res = requete_multi_k(n=n, liste_k=list(req.liste_k))
    texte = res.rapport_texte()
    if cfg["tableau_comparatif"] and nb_a_calculer <= 200:
        texte += "\n\n" + res.tableau_texte()

    stats = _stats_depuis_texte(texte, req)
    stats["multi_ratio_succes"] = res.nb_succes
    stats["multi_ratio_total"] = len(res.liste_k)
    stats["multi_ratio_source"] = "dispatcher"
    return texte, stats


# =============================================================================
# ENRICHISSEMENT DE LA REPONSE FINALE (append idempotent)
# =============================================================================

def enrichir_reponse_multi_rapports(
    question: str,
    answer: Any,                    # FinalAnswer (pydantic) - typé en Any pour
    config: Optional[dict] = None,  # rester importable sans pydantic
) -> bool:
    """Append le tableau deterministe a answer.answer_text si requis.

    - Idempotent (marqueur deja present -> rien).
    - Ajoute les stats scalaires a answer.structured_data (panel
      « Chiffres calcules » de la CLI).
    - Ne leve JAMAIS : la reponse LLM reste servie telle quelle en cas de
      souci du dispatcher.
    """
    cfg = {**VALEURS_DEFAUT, **(config or {})}
    if not cfg.get("enabled", True):
        return False

    texte_courant = getattr(answer, "answer_text", "") or ""
    if MARQUEUR_MULTI_RATIO in texte_courant:
        return False

    try:
        req = detecter_requete_multi_rapports(question)
        if req is None:
            return False
        tableau, stats = generer_tableau_multi_rapports(req, cfg)
    except Exception as exc:  # garde-fou : jamais de rupture de reponse
        logger.warning("Restitution multi-rapports impossible: %s", exc)
        return False

    # Garde-fou inline : au-dela de max_k_inline, extrait tete/queue
    lignes = tableau.splitlines()
    max_inline = int(cfg["max_k_inline"])
    if len(lignes) > max_inline:
        tete = max_inline // 2
        queue = max_inline - tete
        tableau = (
            "\n".join(lignes[:tete])
            + f"\n    [... extrait : {len(lignes)} lignes au total - "
            f"plage 1/{req.k_debut}..1/{req.k_fin}] ...\n"
            + "\n".join(lignes[-queue:])
        )

    bloc = (
        f"{MARQUEUR_MULTI_RATIO}\n"
        f"Demande : {req.resume()} | source lots : {req.source}\n"
        f"Succes : {stats.get('multi_ratio_succes', '?')}/{req.nb_rapports}\n"
        f"{tableau}"
    )
    answer.answer_text = (texte_courant.rstrip() + "\n\n" + bloc)

    sd = dict(getattr(answer, "structured_data", None) or {})
    sd.update(stats)
    try:
        answer.structured_data = sd
    except Exception:  # pragma: no cover - modele non mutable
        pass
    return True


# =============================================================================
# CONSIGNE DE FORMULATION PAR LOTS (prompt LLM, couche reponse)
# =============================================================================

def consigne_prompt_multi_rapports(prompt: str) -> str:
    """Append une consigne courte au prompt LLM si requete multi-rapports.

    Evite que llama3.2 ne resume « a un seul ancre » : il decrit les lots
    (1/2-1/10, 1/11-1/20, ...), le tableau exhaustif etant append
    deterministiquement APRES sa prose (aucun risque d'invention).
    """
    if not prompt or MARQUEUR_MULTI_RATIO in prompt:
        return prompt
    try:
        req = detecter_requete_multi_rapports(prompt)
    except Exception:
        return prompt
    if req is None:
        return prompt

    pas = max(2, int(VALEURS_DEFAUT["lots_lignes"]))
    bornes = [
        (k, min(k + pas - 1, req.k_fin))
        for k in range(req.k_debut, req.k_fin + 1, pas)
    ]
    lots_txt = ", ".join(f"1/{a}-1/{b}" for a, b in bornes[:12])
    suffixe = ", ..." if len(bornes) > 12 else ""
    return (
        prompt
        + "\n\n[CONSIGNE MULTI-RAPPORTS]\n"
        + f"La question porte sur {req.resume()}.\n"
        + f"- Structure ta reponse PAR LOTS contigus de {pas} rapports "
        + f"({lots_txt}{suffixe}).\n"
        + "- Pour chaque lot : ancre n=10, premier reconstruit, statut "
        + "[PREMIER TROUVE] / [ECHEC] (4 essais Digamma sans ancrage).\n"
        + "- NE RESUME PAS a un seul rapport et NE INVENTE aucun premier : "
        + "le tableau exhaustif deterministe est append automatiquement "
        + "APRES ta reponse, il fait foi.\n"
        + "- Conclus par le taux de succes global."
    )



