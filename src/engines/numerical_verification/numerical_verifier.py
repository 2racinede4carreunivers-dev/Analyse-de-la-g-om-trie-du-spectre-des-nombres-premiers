"""
6e moteur cognitif : Verification Numerique Independante via Wolfram|Alpha.

Verifie les resultats spectraux du Python contre Wolfram :
- prime_check : confirme la primalite d'un nombre reconstruit
- value_comparison : compare un calcul Python a Wolfram
- equality_check : verifie une egalite mathematique

Si Wolfram n'est pas configure (pas d'App ID), le moteur retourne
gracieusement 'skipped' sans casser le pipeline.
"""
from __future__ import annotations

import logging
from typing import Any

from ...adapters.wolfram import (
    WolframClient,
    WolframError,
    WolframInvalidAppIDError,
    WolframNoResultError,
    WolframTimeoutError,
)


logger = logging.getLogger(__name__)


class NumericalVerifier:
    """6e moteur : verification numerique via Wolfram|Alpha."""

    def __init__(self, wolfram_client: WolframClient | None = None):
        self.wolfram = wolfram_client or WolframClient()

    @property
    def is_available(self) -> bool:
        return self.wolfram.is_available()

    async def verify_prime(self, n: int) -> dict[str, Any]:
        """Verifie si n est premier selon Wolfram."""
        if not self.is_available:
            return self._skipped("prime_check", n)
        try:
            qr = await self.wolfram.query_full_results(f"is {n} prime")
            text = (WolframClient.extract_primary_plaintext(qr) or "").lower()
            if "prime" in text and "not" not in text and "composite" not in text:
                return {"outcome": "verified", "message": f"Wolfram confirme : {n} est premier.", "raw_text": text}
            if "composite" in text or "not prime" in text:
                return {"outcome": "contradicted", "message": f"Wolfram : {n} n'est PAS premier.", "raw_text": text}
            return {"outcome": "inconclusive", "message": f"Reponse ambigue : {text[:100]}", "raw_text": text}
        except WolframTimeoutError:
            return {"outcome": "timeout", "message": "Wolfram timeout"}
        except (WolframError, WolframNoResultError, WolframInvalidAppIDError) as exc:
            return {"outcome": "error", "message": str(exc)}

    async def verify_equality(self, expr_left: str, expr_right: str) -> dict[str, Any]:
        """Verifie si expr_left == expr_right via Wolfram."""
        if not self.is_available:
            return self._skipped("equality_check", f"{expr_left} == {expr_right}")
        try:
            qr = await self.wolfram.query_full_results(f"({expr_left}) == ({expr_right})")
            text = (WolframClient.extract_primary_plaintext(qr) or "").lower()
            if "true" in text and "false" not in text:
                return {"outcome": "verified", "message": f"Wolfram confirme : {expr_left} == {expr_right}", "raw_text": text}
            if "false" in text:
                return {"outcome": "contradicted", "message": f"Wolfram refute : {expr_left} != {expr_right}", "raw_text": text}
            return {"outcome": "inconclusive", "message": f"Reponse ambigue : {text[:100]}", "raw_text": text}
        except WolframTimeoutError:
            return {"outcome": "timeout", "message": "Wolfram timeout"}
        except (WolframError, WolframNoResultError, WolframInvalidAppIDError) as exc:
            return {"outcome": "error", "message": str(exc)}

    async def verify_value(self, expression: str, expected_value: float, tolerance: float = 1e-6) -> dict[str, Any]:
        """Calcule expression via Wolfram et compare a expected_value."""
        if not self.is_available:
            return self._skipped("value_comparison", expression)
        try:
            qr = await self.wolfram.query_full_results(expression)
            text = (WolframClient.extract_primary_plaintext(qr) or "").strip()
            try:
                wolfram_val = float(text.split()[0].replace(",", ""))
                diff = abs(wolfram_val - expected_value)
                if diff < tolerance:
                    return {"outcome": "verified", "message": f"Wolfram = {wolfram_val}, ecart {diff}", "wolfram_value": wolfram_val}
                return {"outcome": "contradicted", "message": f"Wolfram = {wolfram_val} vs attendu {expected_value} (ecart {diff})", "wolfram_value": wolfram_val}
            except (ValueError, IndexError):
                return {"outcome": "inconclusive", "message": f"Resultat non-numerique : {text[:100]}", "raw_text": text}
        except WolframTimeoutError:
            return {"outcome": "timeout", "message": "Wolfram timeout"}
        except (WolframError, WolframNoResultError, WolframInvalidAppIDError) as exc:
            return {"outcome": "error", "message": str(exc)}

    @staticmethod
    def _skipped(kind: str, target: Any) -> dict[str, Any]:
        return {
            "outcome": "skipped",
            "message": f"Verification {kind} pour {target} non effectuee (WOLFRAM_APP_ID absent).",
        }
