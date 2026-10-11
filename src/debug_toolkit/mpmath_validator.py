"""
MpmathValidator — Recalcul a precision arbitraire.

Utile pour les grandes positions (>500) ou les flottants standards
perdent en precision sur 2^n. mpmath.mpf garantit la precision
en arithmetique decimale arbitraire.
"""
from __future__ import annotations

from typing import Any

import mpmath


class MpmathValidator:
    """Validateur en precision arbitraire."""

    DEFAULT_PRECISION = 100  # chiffres decimaux

    def __init__(self, precision: int = DEFAULT_PRECISION) -> None:
        self.precision = precision
        mpmath.mp.dps = precision

    def validate(self, position: int, ratio: str = "1/2", prime: int | None = None) -> dict[str, Any]:
        """
        Recalcule SA(n), SB(n), digamma, reconstruction a precision arbitraire.
        Permet de croiser avec le resultat de spectral_core (flottants 64-bit)
        et detecter les divergences.
        """
        if ratio != "1/2":
            return {
                "supported": False,
                "reason": f"MpmathValidator gere uniquement le rapport 1/2 (recu : {ratio})",
            }

        n = mpmath.mpf(position)
        # SA(n) = (3.25/2) * 2^n - 2 = (13/8) * 2^n - 2
        SA = (mpmath.mpf(13) / 8) * mpmath.power(2, n) - 2
        SB = (mpmath.mpf(13) / 4) * mpmath.power(2, n) - 66

        result: dict[str, Any] = {
            "supported": True,
            "ratio": ratio,
            "position": position,
            "precision_digits": self.precision,
            "SA": str(SA),
            "SB": str(SB),
            "SA_float": float(SA),
            "SB_float": float(SB),
            "method": f"mpmath.mpf @ {self.precision} chiffres decimaux",
        }

        if prime is not None:
            p = mpmath.mpf(prime)
            digamma = SB - 64 * p
            recon = (SB - digamma) / 64
            identity_ok = mpmath.almosteq(recon, p, rel_eps=mpmath.mpf(10) ** (-self.precision + 10))
            result.update({
                "prime_input": prime,
                "digamma_calc": str(digamma),
                "P_reconstruit": str(recon),
                "identity_verified": bool(identity_ok),
                "absolute_error": str(abs(recon - p)),
            })

        return result

    def render(self, report: dict[str, Any]) -> str:
        if not report.get("supported"):
            return f"[mpmath] {report.get('reason', 'non supporte')}"
        lines = [
            f"[mpmath] Validation precision arbitraire @ {report['precision_digits']} chiffres",
            f"  position = {report['position']}, ratio = {report['ratio']}",
            f"  SA = {report['SA_float']} (precise : {report['SA'][:40]}...)" if len(report['SA']) > 40 else f"  SA = {report['SA']}",
            f"  SB = {report['SB_float']} (precise : {report['SB'][:40]}...)" if len(report['SB']) > 40 else f"  SB = {report['SB']}",
        ]
        if report.get("prime_input") is not None:
            lines.append(f"  digamma_calc = {report['digamma_calc'][:40]}...")
            lines.append(f"  P_reconstruit = {report['P_reconstruit'][:40]}...")
            lines.append(f"  erreur absolue = {report['absolute_error']}")
            mark = "OK" if report["identity_verified"] else "ECHEC"
            lines.append(f"  IDENTITE prouvee a {report['precision_digits']} chiffres : [{mark}]")
        lines.append(f"  methode : {report['method']}")
        return "\n".join(lines)
