"""Prompt Injector Enhanced - injection structuree pour Gabriel v5.2 / v6.2.

Detecte le type de requete (HOL, RSA, Riemann, etc.), injecte les specifications
formelles correspondantes dans le prompt Claude, et valide la conformite de la
reponse LLM aux contraintes attendues.

Complement du `AdaptateurCognitifSpectral` (qui detecte les regimes mathematiques).
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Resultat de validation d'une reponse LLM."""
    is_compliant: bool
    score: float
    findings: list[str]
    missing: list[str]


# Specifications HOL/Isabelle/Lean strictes pour injection
HOL_STRICT_SPEC = """SPÉCIFICATIONS HOL4/ISABELLE/LEAN4 FORMELLES STRICTES :

OBLIGATIONS DE SYNTAXE :
  - Toute fonction declaree par `definition <nom> :: "<type>" where`
  - Types Isabelle : nat, real, int (jamais "number" ou "float")
  - Operations : `*` (multiplication), `^` (puissance entiere), `powr` (puissance reelle)
  - Fractions : utiliser `/` (jamais division flottante 0.5 mais `1 / 2`)

DEFINITIONS REQUISES (regime 1/2) :
  definition A :: "nat => real" where
    "A n = (13 / 8) * (2 ^ n) - 2"
  definition B :: "nat => real" where
    "B n = (13 / 4) * (2 ^ n) - 66"
  definition digamma :: "nat => nat => real" where
    "digamma n p = B n - 64 * real p"
  definition reconstruct :: "nat => nat => real" where
    "reconstruct n p = (B n - digamma n p) / 64"

LEMMES INDISPENSABLES :
  - reconstruct_correct : "reconstruct n p = real p"
  - ratio_one_half : "(A n1 - A n2) / (B n1 - B n2) = 1 / 2"

STRUCTURE ATTENDUE :
  theory Spectral_Primes
  imports Main HOL.Real
  begin
    <definitions>
    <theorems>
  end

INTERDICTIONS ABSOLUES :
  - Pas de "fun" pour les definitions (utiliser "definition")
  - Pas de "(3.25 / 2)" ou autre arithmetique flottante : utiliser "(13 / 8)"
  - Pas de "pow" : utiliser "^" (entiere) ou "powr" (reelle)
  - Pas de "digamma_calcule" : utiliser exactement "digamma"
"""

RSA_SPEC = """SPECIFICATIONS RSA / RAPPORT SPECTRAL :

  - RSA designe le rapport spectral RsP = 1/n (n=2,3,4)
  - Formule par DIFFERENCES : (A(n1) - A(n2)) / (B(n1) - B(n2))
  - JAMAIS par SOMMES seules (ne converge pas)
  - Pour bloc nxn symetrique : ratio EXACT
  - Pour bloc asymetrique : convergence asymptotique
"""

RIEMANN_SPEC = """SPECIFICATIONS HYPOTHESE DE RIEMANN :

  - Les zeros non triviaux ont Re(s) = 1/2 (ligne critique)
  - Lien Methode Spectrale -> Riemann via plan trifocal FZg/HyRi/MsP
  - Validation epipolaire requise pour toute conjecture
  - Toute affirmation sans preuve formelle = CONJECTURE explicite
"""


class PromptInjector:
    """Injecteur de prompt structure pour Gabriel.

    Detecte le type de requete et injecte les specifications formelles
    correspondantes pour guider Claude vers une reponse conforme HOL/HOL4/Lean4.
    """

    # Patterns de detection du TYPE de requete (different du REGIME mathematique)
    TYPE_PATTERNS: dict[str, list[str]] = {
        "hol": [
            r"\bHOL\b", r"\bIsabelle\b", r"\bLean\b", r"\btheory\b",
            r"\bgenere?z?\s+(?:la\s+)?th[eé]orie\b",
            r"\bg[eé]n[eé]re?z?\s+.*\s+(?:HOL|Isabelle)\b",
            r"\bpreuve\s+formelle\b", r"\btheorem\b",
        ],
        "rsa": [
            r"\bRSA\b", r"\brapport\s+spectral\b",
            r"\bRsP\b", r"\bratio\s+1/[234]\b",
        ],
        "riemann": [
            r"\bRiemann\b", r"\bz[eé]ros?\s+(non\s+)?triviaux?\b",
            r"\bhypoth[eè]se\s+de\s+Riemann\b", r"\bHypR\b",
            r"\bligne\s+critique\b",
        ],
        "reconstruction": [
            r"\breconstru[ic][rt]\b", r"\bN-?[ie]me\s+premier\b",
            r"\bN-?[ie]me\s+nombre\s+premier\b",
        ],
        "gap": [
            r"\b[eé]cart\b", r"\bgap\b",
            r"\b(?:nombres?\s+)?entre\s+-?\d+\s+et\s+-?\d+\b",
        ],
    }

    # Mots-cles obligatoires par type de validation
    VALIDATION_KEYWORDS = {
        "hol_proof_generation": {
            "required": [
                "definition", "where", "theorem", "begin", "end",
            ],
            "forbidden": [
                "fun ", "3.25 / 2", "6.5 / 2", "digamma_calcule",
                "(2 pow ", "math.pow",
            ],
            "preferred": [
                "(13 / 8)", "(13 / 4)", "nat", "real",
                "A n =", "B n =", "digamma n p",
            ],
        },
    }

    def detect_query_type(self, text: str) -> str:
        """Detecte le type principal de la requete.

        Returns:
            Type detecte ("hol", "rsa", "riemann", "reconstruction", "gap")
            ou "general" si aucun match.
        """
        if not text:
            return "general"
        scores: dict[str, int] = {}
        for type_name, patterns in self.TYPE_PATTERNS.items():
            count = sum(1 for p in patterns if re.search(p, text, re.IGNORECASE))
            if count > 0:
                scores[type_name] = count
        if not scores:
            return "general"
        # Retourne le type avec le plus de matches
        return max(scores, key=scores.get)

    def inject_for_claude_hol(self, question: str) -> str:
        """Injecte les specifications HOL strictes dans le prompt."""
        return (
            f"{HOL_STRICT_SPEC}\n\n"
            f"=== REQUETE UTILISATEUR ===\n{question}\n\n"
            "REPONSE ATTENDUE : Code Isabelle/HOL FORMEL conforme aux specifications "
            "ci-dessus, encadre par `theory ... begin ... end`."
        )

    def inject_for_claude_rsa(self, question: str) -> str:
        return f"{RSA_SPEC}\n\n=== REQUETE ===\n{question}"

    def inject_for_claude_riemann(self, question: str) -> str:
        return f"{RIEMANN_SPEC}\n\n=== REQUETE ===\n{question}"

    def inject(self, question: str) -> tuple[str, str]:
        """Detecte le type et retourne (type, prompt_augmente)."""
        qtype = self.detect_query_type(question)
        if qtype == "hol":
            return qtype, self.inject_for_claude_hol(question)
        if qtype == "rsa":
            return qtype, self.inject_for_claude_rsa(question)
        if qtype == "riemann":
            return qtype, self.inject_for_claude_riemann(question)
        # reconstruction, gap, general : pas de specs additionnelles
        return qtype, question

    def validate_llm_response(
        self,
        response: str,
        query_type: str = "hol_proof_generation",
    ) -> dict:
        """Valide la conformite d'une reponse LLM aux specifications attendues.

        Args:
            response: Texte de la reponse generee par le LLM.
            query_type: Type de validation a appliquer (cle de VALIDATION_KEYWORDS).

        Returns:
            Dict avec is_compliant (bool), score (float 0..1), findings, missing.
        """
        spec = self.VALIDATION_KEYWORDS.get(query_type)
        if not spec:
            return {
                "is_compliant": True, "score": 1.0,
                "findings": [], "missing": [],
            }

        required = spec.get("required", [])
        forbidden = spec.get("forbidden", [])
        preferred = spec.get("preferred", [])

        findings: list[str] = []
        missing: list[str] = []

        # Penalisations
        forbidden_found = [kw for kw in forbidden if kw in response]
        for kw in forbidden_found:
            findings.append(f"INTERDIT trouve : '{kw}'")

        # Required
        required_found = sum(1 for kw in required if kw in response)
        missing_required = [kw for kw in required if kw not in response]
        missing.extend(missing_required)

        # Preferred (bonus)
        preferred_found = sum(1 for kw in preferred if kw in response)

        # Score : 70% required, 30% preferred, -50% par forbidden
        req_ratio = required_found / max(1, len(required))
        pref_ratio = preferred_found / max(1, len(preferred))
        penalty = 0.5 * len(forbidden_found)
        score = max(0.0, min(1.0, 0.7 * req_ratio + 0.3 * pref_ratio - penalty))

        is_compliant = (
            score >= 0.5
            and not forbidden_found
            and len(missing_required) <= max(1, len(required) // 4)
        )

        return {
            "is_compliant": is_compliant,
            "score": round(score, 3),
            "findings": findings,
            "missing": missing,
            "required_found": required_found,
            "required_total": len(required),
            "preferred_found": preferred_found,
            "forbidden_found": forbidden_found,
        }
