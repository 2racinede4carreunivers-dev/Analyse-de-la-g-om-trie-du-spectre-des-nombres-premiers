"""
Moteur de Generalisation.
Etend les patterns 1/2 -> 1/3 -> 1/4 -> 1/k, et positif -> negatif -> mixte.
"""
from __future__ import annotations

from typing import Any


class PatternMatcher:
    """Detecte les patterns spectraux dans une question."""

    GENERIC_PATTERNS = {
        "ratio_1_k": "Pour tout k entier >= 2, rapport spectral 1/k existe avec formules analogues.",
        "positive_to_negative": "Toute formule positive a son pendant negatif via axiomatisation.",
        "single_to_block": "Toute identite 1x1 se generalise en n*n via sommes de blocs.",
    }

    def match(self, ctx: dict[str, Any]) -> list[str]:
        patterns = []
        if ctx.get("model") in {"1/2", "1/3", "1/4"}:
            patterns.append("ratio_1_k")
        if ctx.get("intent") == "ratio":
            patterns.append("single_to_block")
        if "negatif" in (ctx.get("question") or "").lower():
            patterns.append("positive_to_negative")
        return patterns


REGLE_DEUX_NIVEAUX = (
    "Critères convolutifs obligatoires (niveaux 1 et 2) : (1) exposer d'abord le "
    "NIVEAU 1 — ENTIER (suites A et B à termes entiers) et ses QUATRE "
    "possibilités Digamma (positions n-3 et n-2, signes ±), avec le candidat et "
    "son statut premier/composé pour chacune ; (2) si le niveau 1 ne retourne "
    "AUCUN premier, donner la démarche de niveau 1 qui n'aboutit pas, PUIS "
    "déterminer le NIVEAU 2 — GÉOMÉTRIQUE (exactement la même démarche, mais les "
    "suites A et B sont composées de termes géométriques "
    "sqrt((k^(i-1))^2 + (k^i)^2)) ; (3) si aucun des deux niveaux ne retourne "
    "d'ancrage, énoncer explicitement que, pour ce rapport 1/k non typique, le "
    "système convolutif ne retourne aucun ancrage pour un premier."
)


class Generalizer:
    """Genere des templates a partir de cas particuliers."""

    def __init__(self):
        self.matcher = PatternMatcher()

    def generalize(self, computation_result: dict[str, Any], ctx: dict[str, Any]) -> dict[str, Any]:
        """Produit une description generale de la solution calculee."""
        patterns = self.matcher.match(ctx)
        return {
            "patterns_detected": patterns,
            "general_form": self._build_general_form(computation_result, ctx),
            "extension_hint": self._extension_hint(ctx),
        }

    def _build_general_form(self, result: dict[str, Any], ctx: dict[str, Any]) -> str:
        intent = ctx.get("intent")
        if intent == "reconstruction":
            model = str(result.get("model") or ctx.get("model") or "1/2")
            if model != "1/2":
                equation_a = result.get("equation_A", {})
                equation_b = result.get("equation_B", {})
                return (
                    f"Rapport non-typique {model}. Utilise exclusivement les équations "
                    f"calculées : {equation_a.get('forme', 'A(n) inconnue')} ; "
                    f"{equation_b.get('forme', 'B(n) inconnue')}. "
                    "Ne pas appliquer la formule du rapport 1/2, ne pas employer le "
                    "facteur 64, et ne pas affirmer que n est la position du premier. "
                    + REGLE_DEUX_NIVEAUX +
                    " Les clés `niveau_1`, `niveau_2`, `point_1_niveau_1`, "
                    "`point_2_niveau_2` et `point_3_verdict` fournissent ces points "
                    "textuellement. Les listes `suite_Ai` et `suite_Bi` exposent les "
                    "composantes réelles par position; ne jamais les remplacer par "
                    "des valeurs inventées."
                )
            return (
                "Rapport typique 1/2 : pour tout p premier et n suffisant, "
                "prime_equation(n, p) = (SB(n) - digamma_calc(n, p)) / 64 = p, "
                "avec n égal à la position du premier. "
                + REGLE_DEUX_NIVEAUX
            )
        if intent == "ratio":
            return (
                "Forme generale : RsP(A_indices, B_indices) -> 1/k selon le modele. "
                "Independant des indices choisis tant que la configuration est valide."
            )
        if intent == "gap":
            return (
                "Forme generale : gap_equation(A_next, B_high, D_high, D_low) / factor = p_low - p_high. "
                "Vrai pour les 3 cas (+,+), (-,-), (-,+) avec adaptation du diviseur."
            )
        return "Pas de generalisation specifique."

    def _extension_hint(self, ctx: dict[str, Any]) -> str:
        return (
            "Extensions possibles : rapport 1/5, 1/6 (analogues), suites a coefficients differents, "
            "et passage explicite a la concordance Riemann-Savard via le plan trifocal."
        )

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
