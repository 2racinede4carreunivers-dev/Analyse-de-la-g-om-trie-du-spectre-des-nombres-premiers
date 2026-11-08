"""
scorer.py  —  Évaluateur de qualité de réponse Gabriel
═══════════════════════════════════════════════════════
CORRECTION appliquée (DEF-06) :
  • Ajout du critère ratio_coherence (poids 30%), BLOQUANT
  • Pénalité : score plafonné à 4.9 si model != ratio demandé
  • Un score >= seuil est impossible si ratio_coherence échoue
═══════════════════════════════════════════════════════
"""

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("gabriel.scorer")

SCORE_THRESHOLD = 7.0


@dataclass
class ScoreDetails:
    ratio_coherence:      float = 0.0   # CORRECTION DEF-06
    formula_match:        float = 0.0
    invariant_check:      float = 0.0
    hol_coherence:        float = 0.0
    numeric_plausibility: float = 0.0
    total:                float = 0.0
    passed:               bool  = False
    blocking_reason:      Optional[str] = None


class Scorer:
    """
    Évalue la réponse de SpectralCore sur 5 critères pondérés.
    CORRECTION DEF-06 : ratio_coherence est BLOQUANT (poids 30%).
    """

    WEIGHTS = {
        "ratio_coherence":      0.30,   # nouveau — était absent avant correction
        "formula_match":        0.25,
        "invariant_check":      0.20,
        "hol_coherence":        0.15,
        "numeric_plausibility": 0.10,
    }

    def evaluate(self, response: dict, request_params: dict) -> ScoreDetails:
        details = ScoreDetails()
        ratio_demandé  = request_params.get("ratio_str", "UNKNOWN")
        model_retourné = response.get("model", "UNKNOWN")
        k              = request_params.get("k", 0)

        # ── 1. ratio_coherence (BLOQUANT) ─────────────────
        if model_retourné == ratio_demandé:
            details.ratio_coherence = 10.0
            logger.info("ratio_coherence OK : model=%r == ratio=%r",
                        model_retourné, ratio_demandé)
        else:
            details.ratio_coherence = 0.0
            details.blocking_reason = (
                f"ratio_coherence ÉCHOUE : "
                f"model={model_retourné!r} != ratio={ratio_demandé!r}"
            )
            logger.error("BLOQUANT — %s", details.blocking_reason)

        # ── 2. formula_match ──────────────────────────────
        SA = response.get("SA", 0.0)
        if k > 0 and SA > (k ** 20):
            details.formula_match = 10.0
        else:
            details.formula_match = 0.0
            logger.warning("formula_match : SA=%.2e trop petit pour k=%d", SA, k)

        # ── 3. invariant_check ────────────────────────────
        invariant = response.get("invariant", "")
        if k == 2 and "position = n" in invariant:
            details.invariant_check = 10.0
        elif k != 2 and ("position != n" in invariant or "asymetrique" in invariant.lower()):
            details.invariant_check = 10.0
        elif k != 2 and "ratio 1/2" in invariant:
            details.invariant_check = 0.0
            logger.warning("invariant_check : invariant 1/2 appliqué pour k=%d", k)
        else:
            details.invariant_check = 5.0

        # ── 4. hol_coherence ──────────────────────────────
        hol = response.get("hol_fragment", "")
        if hol and f"ratio{k}" in hol and f"SA_k{k}_def" in hol:
            details.hol_coherence = 10.0
        elif hol and "2^n" in hol and k != 2:
            details.hol_coherence = 0.0
        else:
            details.hol_coherence = 5.0

        # ── 5. numeric_plausibility ───────────────────────
        SB = response.get("SB", 0.0)
        details.numeric_plausibility = 10.0 if (SA > 0 and SB > SA) else 0.0

        # ── Score total ───────────────────────────────────
        raw = sum(
            getattr(details, c) * w
            for c, w in self.WEIGHTS.items()
        )

        # CORRECTION DEF-06 : plafonnement si ratio_coherence échoue
        if details.blocking_reason:
            raw = min(raw, 4.9)
            logger.error(
                "Score plafonné à 4.9 (seuil=%.1f) — ratio_coherence échoué.",
                SCORE_THRESHOLD,
            )

        details.total  = round(raw, 2)
        details.passed = (details.total >= SCORE_THRESHOLD)
        logger.info("Score %.2f/10  passed=%s", details.total, details.passed)
        return details


# ─────────────────────────────────────────────────────────
#  TESTS UNITAIRES
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tests scorer ===")
    scorer = Scorer()

    # Test 1 : réponse Gabriel erronée (model=1/2 pour ratio=1/4)
    bad = scorer.evaluate(
        response={"model": "1/2", "SA": 13631486.0, "SB": 27262910.0,
                  "invariant": "INVARIANT (ratio 1/2): position = n = 23",
                  "hol_fragment": "SA(n)=(3.25/2)*2^n-2"},
        request_params={"ratio_str": "1/4", "k": 4},
    )
    assert bad.total <= 4.9, f"Score devrait être <= 4.9, obtenu {bad.total}"
    assert not bad.passed
    print(f"  OK  réponse erronée Gabriel : score={bad.total}/10 passed={bad.passed}")

    # Test 2 : réponse correcte (model=1/4)
    good = scorer.evaluate(
        response={"model": "1/4", "SA": 8.83e13, "SB": 3.53e14,
                  "invariant": "INVARIANT (ratio 1/4): n=terms [position != n]",
                  "hol_fragment": "theory verif_p1097_n23_ratio4  SA_k4_def"},
        request_params={"ratio_str": "1/4", "k": 4},
    )
    assert good.total >= SCORE_THRESHOLD, f"Score devrait être >= {SCORE_THRESHOLD}"
    assert good.passed
    print(f"  OK  réponse correcte         : score={good.total}/10 passed={good.passed}")

    print("\nTous les tests scorer : OK")
