"""
PRE-RAISONNEUR GABRIEL (v3.34)
================================================================================
Moteur de pre-raisonnement inject en T0 du Pipeline. Analyse la requete AVANT
la chaine complete (abstraction / meta / navigation / spectral / multiloop /
slow-motion / audit) et produit un ReasoningPlan qui indique :
  - le mode de traitement (INSTANTANE / RAPIDE / STANDARD / APPROFONDI / TRES_COMPLEXE)
  - le nombre d'iterations de raffinement a executer (0 / 1 / 2 / 3 / 4)
  - les etages du pipeline a court-circuiter (spectral_compute, slow-motion,
    audit silencieux, generation HOL)
  - une estimation de la duree (secondes) pour le timer temps reel du CLI
  - une justification lisible (audit)

Cinq modes :
  - INSTANTANE     : 0 loop, reponse template pre-compilee (bonjour, oui, non,
                     continue, reformule, merci, au revoir). Aucun LLM appele.
  - RAPIDE         : 1 loop, requete verbale/discursive sur la Methode Spectrale
                     ou sur une section Isabelle (ex : "resume la Section XIII",
                     "compare ces deux lemmes", "cette preuve tient-elle ?").
                     Skip spectral_compute + slow-motion + audit silencieux.
  - STANDARD       : 2 loops, calcul simple (RsP unique, gap, position d'un
                     premier). Le calcul spectral s'execute mais slow-motion
                     et audit restent tolerants.
  - APPROFONDI     : 3 loops, requete de configuration (ratio_spectral_nxn,
                     bloc A/B, comparaison chaotique/ordonnee).
  - TRES_COMPLEXE  : 4 loops, requete multi-objectifs / theorie avancee
                     (Section XIII, Pont Savard, zeta, Chebyshev, hypothese
                     de Riemann, plusieurs demandes chainees).

Un override utilisateur (via commandes CLI /rapide /standard /approfondi
/complet ou parametre `force_mode`) est possible et bypasse la detection
automatique tout en conservant l'audit du choix force.

Author: Philippe Thomas Savard (Methode Spectrale)
License: Apache License 2.0
================================================================================
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class RequestMode(Enum):
    """Modes de traitement decides par le pre-raisonneur."""
    INSTANTANE = "instantane"        # 0 loop, template
    RAPIDE = "rapide"                 # 1 loop, verbal Isabelle/theorie
    STANDARD = "standard"             # 2 loops, calcul simple
    APPROFONDI = "approfondi"         # 3 loops, configuration/nxn
    TRES_COMPLEXE = "tres_complexe"   # 4 loops, multi-obj / theorie avancee


@dataclass
class ReasoningPlan:
    """Plan de raisonnement produit par le PreReasoner."""
    mode: RequestMode
    n_iterations: int                 # 0, 1, 2, 3 ou 4
    skip_spectral_compute: bool
    skip_slowmotion: bool
    skip_silent_audit: bool
    skip_hol_generation: bool
    estimated_duration_sec: int
    reason: str
    detected_categories: list[str] = field(default_factory=list)
    is_forced: bool = False
    template_response: Optional[str] = None
    confidence: float = 0.85

    def as_dict(self) -> dict:
        return {
            "mode": self.mode.value,
            "n_iterations": self.n_iterations,
            "skip_spectral_compute": self.skip_spectral_compute,
            "skip_slowmotion": self.skip_slowmotion,
            "skip_silent_audit": self.skip_silent_audit,
            "skip_hol_generation": self.skip_hol_generation,
            "estimated_duration_sec": self.estimated_duration_sec,
            "reason": self.reason,
            "detected_categories": list(self.detected_categories),
            "is_forced": self.is_forced,
            "confidence": self.confidence,
        }


# ============================================================================
# TABLES DE DETECTION
# ============================================================================

# INSTANTANE : messages ultra-courts / discours pur (aucun LLM necessaire)
_INSTANTANE_TEMPLATES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^\s*(?:bonjour|salut|coucou|bonsoir|hello|hey|allo|hi)\s*[!?.]*\s*$", re.I),
     "Bonjour ! Je suis Gabriel, agent multiloop dédié à la Méthode Spectrale. "
     "Que puis-je faire pour toi ?"),
    (re.compile(r"^\s*(?:merci|thanks|thx|merci beaucoup|super merci)\s*[!?.]*\s*$", re.I),
     "Avec plaisir. Dis-moi si tu veux explorer un autre lemme ou une nouvelle configuration."),
    (re.compile(r"^\s*(?:au revoir|bye|à\s+plus|a\s+plus|à\s+bientôt|a\s+bientot|ciao)\s*[!?.]*\s*$", re.I),
     "À bientôt. Je garde le fil en mémoire pour la prochaine session."),
    (re.compile(r"^\s*(?:ok|oui|d'accord|d\s*accord|ouais|yes|yep|ya|correct|exact)\s*[!?.]*\s*$", re.I),
     "Compris. Souhaites-tu que je continue ou que je détaille un point précis ?"),
    (re.compile(r"^\s*(?:non|nope|pas vraiment|no)\s*[!?.]*\s*$", re.I),
     "D'accord. Reformule ta demande ou pointe-moi la partie à corriger."),
    (re.compile(r"^\s*(?:continue|poursui[st]|va[- ]?y|enchaîne|enchaine|encore|suite)\s*[!?.]*\s*$", re.I),
     "Je reprends le fil. (Astuce : précise la Section ou le lemme pour un ancrage optimal.)"),
    (re.compile(r"^\s*(?:comment (?:ça |ca )?vas?(?:[- ]?tu)?|comment tu vas|ça\s*va|ca\s*va)\s*[!?.]*\s*$", re.I),
     "Tout va bien côté kernel : 1568 pytests verts, Isabelle compile sans erreur. "
     "De ton côté, sur quoi veux-tu qu'on travaille ?"),
]

# RAPIDE : requetes verbales / discursives sur Isabelle, sections, lemmes,
# theoremes, sans besoin de calcul numerique.
_VERBAL_ISABELLE_PATTERNS = [
    # Meta-analyse d'une section / preuve / lemme
    r"\b(?:cette|cet|ce|la|le)\s+(?:section|preuve|lemme|theoreme|théorème|axiome|definition|démonstration|demonstration)\b",
    r"\b(?:section\s+(?:xi{1,3}|1[0-3]|13|12|11|10|[1-9]))\b",
    r"\b(?:pont\s+savard|savard\s+bridge)\b",
    # Verbes discursifs
    r"\b(?:resume|résume|résumer|resumer|synthese|synthèse|synthétise|synthetise)\b",
    r"\b(?:compare[rs]?|comparer|comparaison|différence|difference|distingue[rs]?)\s+(?:ces|les|entre|ce)",
    r"\b(?:commente[rs]?|commenter|commentaire|analyse[rs]?|analyser)\s+(?:cette|ce|cet|la|le|ma|mon|mes)",
    r"\b(?:relis|relire|verifie|vérifie|regarde|regarder|examine[rs]?)\s+(?:cette|ce|cet|la|le|ma|mon|mes)",
    r"\b(?:reformule[rs]?|reformuler|clarifie[rs]?|clarifier|simplifie[rs]?|simplifier)\b",
    r"\b(?:que penses[- ]?tu|qu'en penses[- ]?tu|ton avis|ton opinion|selon toi|crois[- ]?tu)\b",
    r"\b(?:tient[- ]?elle|tient[- ]?il|est[- ]?ce (?:que|bien)|est[- ]?elle|est[- ]?il)\s+(?:valide|correct|coherent|cohérent|bien|juste|exact|bon)",
    r"\b(?:bien\s+(?:formatee?|formatée?|ecrite?|écrite?|redigee?|rédigée?|structuree?|structurée?)|lisible|clair|claire|coherent|cohérent)\b",
    r"\b(?:liste[rs]?|lister|enumere[rs]?|énumère?[rs]?|enumerer|énumérer|nomme[rs]?|nommer)\s+(?:les|toutes?|tous|mes|ses|ces)",
    r"\b(?:explique[- ]?moi|expliquer|explication)\b",
    r"\b(?:parle[- ]?moi|dis[- ]?moi|raconte[- ]?moi|montre[- ]?moi)\b",
    r"\b(?:qu'est[- ]?ce que|c'est quoi|c'est qui|kesako)\b",
    r"\b(?:pourquoi|comment)\b.{0,80}\?",
    r"\b(?:aide[- ]?moi|assiste[- ]?moi|guide[- ]?moi|conseille[- ]?moi)\b",
    r"\b(?:documente[rs]?|documenter|rédige[rs]?|redige[rs]?|écris[- ]?moi|ecris[- ]?moi)\b",
    r"\b(?:que fais[- ]?tu|que peux[- ]?tu|à quoi (?:tu\s+)?sers|qui es[- ]?tu)\b",
]

# TRES_COMPLEXE : marqueurs de theorie avancee / multi-objectifs
_VERY_HIGH_PATTERNS = [
    r"\b(?:zeta|zêta|z[eé]ta|riemann|hypothèse\s+de\s+riemann)\b",
    r"\b(?:chebyshev|tchebychev|psi[- _]?savard|psi\s*\(\s*savard)\b",
    r"\b(?:section\s+(?:xiii|13)|pont\s+savard|savard\s+bridge)\b(?:.*?)(?:calcul|verifie|prouve|démontre|demontre)",
    r"\b(?:plusieurs|multi(?:ple)?)\b.{0,60}\b(?:objectifs?|calculs?|demandes?)\b",
    r"\b(?:reconstruis|calcule).*\bet\s+(?:aussi\s+)?(?:reconstruis|calcule|compare|vérifie|verifie)\b",
    r"\b(?:droite\s+critique|zeros?\s+de\s+zeta|zéros?\s+de\s+zêta)\b",
]

# APPROFONDI : configurations nxn / blocs A/B / comparaisons chaotique-ordonnee
_HIGH_PATTERNS = [
    r"\b(?:sym[eé]trique|asym[eé]trique)\s*\d+\s*[x*]\s*\d+\b",
    r"\bconfiguration\s+\d+\s*[x*]\s*\d+\b",
    r"\bbloc\s*[ab]\s*=",
    r"\b(?:chaotique|ordonn[eé]e?)\b.{0,40}\b(?:asym[eé]trique|sym[eé]trique|bloc)\b",
    r"\brapport\s+spectral\s+(?:sym[eé]trique|asym[eé]trique)\b",
    r"\bcomparaison\s+(?:asym[eé]trique|sym[eé]trique)\b",
]

# STANDARD : calculs simples (un seul objectif numerique)
_MEDIUM_PATTERNS = [
    r"\bRsP\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)",
    r"\b(?:calcule[rs]?|calculer)\s+(?:le\s+)?(?:rapport|ratio|gap|écart|ecart)\b",
    r"\breconstrui[rs]\s+(?:le\s+)?\d+",
    r"\b(?:position|rang|index)\s+(?:du\s+)?(?:premier|nombre)\s+\d+",
    r"\bgap\s+entre\s+-?\d+\s+et\s+-?\d+",
    r"\bécart\s+entre\s+-?\d+\s+et\s+-?\d+",
    r"\becart\s+entre\s+-?\d+\s+et\s+-?\d+",
    r"\b(?:le\s+)?\d+\s*(?:eme|ième|ème|ieme|e)\s+(?:nombre\s+)?premier\b",
    r"\b(?:verif|vérif|check|valide)\w*\b.*\b(?:premier|prime|equation|équation)\b",
]

# Marqueurs qui *empechent* le classement INSTANTANE / RAPIDE
# (ces mots impliquent presque toujours du calcul)
_CALCULATION_MARKERS = [
    r"\bRsP\s*\(", r"\bSA\s*=", r"\bSB\s*=",
    r"\bcalcule[rs]?\b", r"\bcompute\b",
    r"\breconstrui[rs]\b", r"\bgap\s+\d",
    r"\bbloc\s*[ab]\s*=",
    r"-?\d+\s*[+\-*/=]\s*-?\d+",
]


class PreReasoner:
    """Moteur de pre-raisonnement de Gabriel.

    Il decide, avant que le Pipeline n'engage la chaine complete, du mode de
    traitement optimal (INSTANTANE / RAPIDE / STANDARD / APPROFONDI / TRES_COMPLEXE)
    et produit un ReasoningPlan qui pilote finement le pipeline.
    """

    # Durees moyennes en secondes par mode (calibrees sur les traces reelles)
    _DURATION_TABLE = {
        RequestMode.INSTANTANE: 1,
        RequestMode.RAPIDE: 9,
        RequestMode.STANDARD: 18,
        RequestMode.APPROFONDI: 32,
        RequestMode.TRES_COMPLEXE: 55,
    }

    _ITERATIONS_TABLE = {
        RequestMode.INSTANTANE: 0,
        RequestMode.RAPIDE: 1,
        RequestMode.STANDARD: 2,
        RequestMode.APPROFONDI: 3,
        RequestMode.TRES_COMPLEXE: 4,
    }

    def __init__(self) -> None:
        self._verbal_re = [re.compile(p, re.I) for p in _VERBAL_ISABELLE_PATTERNS]
        self._very_high_re = [re.compile(p, re.I) for p in _VERY_HIGH_PATTERNS]
        self._high_re = [re.compile(p, re.I) for p in _HIGH_PATTERNS]
        self._medium_re = [re.compile(p, re.I) for p in _MEDIUM_PATTERNS]
        self._calc_marker_re = [re.compile(p, re.I) for p in _CALCULATION_MARKERS]

    # ----------------------------------------------------------------- API
    def plan(
        self,
        question: str,
        force_mode: Optional[RequestMode] = None,
    ) -> ReasoningPlan:
        """Produit un plan de raisonnement pour la question donnee."""
        q = (question or "").strip()

        # 1. Override utilisateur explicite
        if force_mode is not None:
            plan = self._build_plan_for_mode(
                force_mode,
                reason=f"Mode forcé par l'utilisateur ({force_mode.value}).",
                categories=[f"forced:{force_mode.value}"],
                is_forced=True,
            )
            logger.info("PreReasoner: plan forcé = %s (%d itérations)",
                        plan.mode.value, plan.n_iterations)
            return plan

        # 2. Question vide -> INSTANTANE avec message d'invite
        if not q:
            return self._build_plan_for_mode(
                RequestMode.INSTANTANE,
                reason="Requête vide.",
                categories=["empty"],
                template="Je suis prêt. Pose-moi une question sur la Méthode Spectrale.",
            )

        # 3. Detection INSTANTANE (templates) - seulement si pas de marqueur calcul
        if not self._has_calculation_marker(q):
            for pattern, template in _INSTANTANE_TEMPLATES:
                if pattern.match(q):
                    return self._build_plan_for_mode(
                        RequestMode.INSTANTANE,
                        reason="Message court détecté (small-talk / continuation).",
                        categories=["instantane_template"],
                        template=template,
                    )

        # 4. Scores par categorie
        very_high_hits = self._count_hits(q, self._very_high_re)
        high_hits = self._count_hits(q, self._high_re)
        medium_hits = self._count_hits(q, self._medium_re)
        verbal_hits = self._count_hits(q, self._verbal_re)
        has_calc = self._has_calculation_marker(q)

        detected: list[str] = []
        if very_high_hits > 0:
            detected.append(f"tres_complexe:{very_high_hits}")
        if high_hits > 0:
            detected.append(f"approfondi:{high_hits}")
        if medium_hits > 0:
            detected.append(f"standard:{medium_hits}")
        if verbal_hits > 0:
            detected.append(f"verbal:{verbal_hits}")
        if has_calc:
            detected.append("calc_marker")

        # 5. Regles de decision (du plus complexe au plus simple)
        # 5a. TRES_COMPLEXE : theorie avancee ou multi-objectifs
        if very_high_hits >= 1:
            return self._build_plan_for_mode(
                RequestMode.TRES_COMPLEXE,
                reason=f"Théorie avancée / multi-objectifs détectés ({very_high_hits} marqueur(s)).",
                categories=detected,
            )

        # 5b. APPROFONDI : configuration nxn / blocs
        if high_hits >= 1:
            return self._build_plan_for_mode(
                RequestMode.APPROFONDI,
                reason=f"Configuration complexe détectée ({high_hits} marqueur(s) n×n / bloc).",
                categories=detected,
            )

        # 5c. RAPIDE : requete verbale/discursive sans marqueur de calcul
        if verbal_hits >= 1 and not has_calc:
            return self._build_plan_for_mode(
                RequestMode.RAPIDE,
                reason=(f"Requête verbale/discursive détectée ({verbal_hits} marqueur(s)) "
                        f"— aucun calcul spectral nécessaire."),
                categories=detected,
            )

        # 5d. STANDARD : calcul simple
        if medium_hits >= 1 or has_calc:
            return self._build_plan_for_mode(
                RequestMode.STANDARD,
                reason=f"Calcul simple détecté ({medium_hits} marqueur(s) numérique).",
                categories=detected,
            )

        # 5e. Fallback : mixte (question ouverte sans marqueur) -> STANDARD prudent
        # sauf si tres court -> RAPIDE
        if len(q.split()) <= 10:
            return self._build_plan_for_mode(
                RequestMode.RAPIDE,
                reason="Question courte sans marqueur mathématique — traitement rapide.",
                categories=detected + ["fallback_short"],
                confidence=0.60,
            )

        return self._build_plan_for_mode(
            RequestMode.STANDARD,
            reason="Aucun marqueur fort détecté — mode standard par défaut.",
            categories=detected + ["fallback_default"],
            confidence=0.60,
        )

    # ----------------------------------------------------------- helpers
    def _count_hits(self, q: str, regexes: list[re.Pattern]) -> int:
        return sum(1 for r in regexes if r.search(q))

    def _has_calculation_marker(self, q: str) -> bool:
        return any(r.search(q) for r in self._calc_marker_re)

    def _build_plan_for_mode(
        self,
        mode: RequestMode,
        reason: str,
        categories: list[str],
        is_forced: bool = False,
        template: Optional[str] = None,
        confidence: float = 0.85,
    ) -> ReasoningPlan:
        n_iter = self._ITERATIONS_TABLE[mode]
        duration = self._DURATION_TABLE[mode]

        # Politique des bypasses
        if mode == RequestMode.INSTANTANE:
            skip_spectral = True
            skip_slow = True
            skip_audit = True
            skip_hol = True
        elif mode == RequestMode.RAPIDE:
            # Verbal Isabelle : on saute tout ce qui est numerique
            skip_spectral = True
            skip_slow = True
            skip_audit = True
            skip_hol = True
        elif mode == RequestMode.STANDARD:
            # Calcul simple : on execute mais on reste tolerant
            skip_spectral = False
            skip_slow = False
            skip_audit = False
            skip_hol = False
        else:  # APPROFONDI / TRES_COMPLEXE
            skip_spectral = False
            skip_slow = False
            skip_audit = False
            skip_hol = False

        return ReasoningPlan(
            mode=mode,
            n_iterations=n_iter,
            skip_spectral_compute=skip_spectral,
            skip_slowmotion=skip_slow,
            skip_silent_audit=skip_audit,
            skip_hol_generation=skip_hol,
            estimated_duration_sec=duration,
            reason=reason,
            detected_categories=categories,
            is_forced=is_forced,
            template_response=template,
            confidence=confidence,
        )


# ============================================================================
# HELPERS POUR PARSER LES COMMANDES CLI D'OVERRIDE
# ============================================================================

_CLI_MODE_ALIASES: dict[str, RequestMode] = {
    "/rapide": RequestMode.RAPIDE,
    "/standard": RequestMode.STANDARD,
    "/approfondi": RequestMode.APPROFONDI,
    "/complet": RequestMode.TRES_COMPLEXE,
    "/tres_complexe": RequestMode.TRES_COMPLEXE,
    "/instantane": RequestMode.INSTANTANE,
}


def parse_cli_force_mode(user_input: str) -> tuple[Optional[RequestMode], str]:
    """Analyse une entree utilisateur pour extraire un override /rapide, /standard...

    Retourne (mode_ou_None, entree_nettoyee_sans_la_commande).
    L'override doit etre place en debut de ligne.
    """
    if not user_input:
        return None, user_input
    stripped = user_input.lstrip()
    lower = stripped.lower()
    for alias, mode in _CLI_MODE_ALIASES.items():
        if lower.startswith(alias):
            # Retirer la commande et espace suivant
            remainder = stripped[len(alias):].lstrip()
            return mode, remainder
    return None, user_input


__all__ = [
    "RequestMode",
    "ReasoningPlan",
    "PreReasoner",
    "parse_cli_force_mode",
]
