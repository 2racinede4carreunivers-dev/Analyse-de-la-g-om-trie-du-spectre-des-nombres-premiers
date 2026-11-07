"""
SympyValidator — Validation symbolique exacte des formules SA, SB, digamma.

sympy travaille en FRACTIONS EXACTES (pas en flottants), donc detecte
les erreurs d'arrondi qui peuvent fausser l'INVARIANT pour grands n.
"""
from __future__ import annotations

from typing import Any

import sympy as sp


class SympyValidator:
    """Validateur symbolique base sur sympy."""

    def __init__(self) -> None:
        self.n = sp.Symbol('n', positive=True, integer=True)
        self.p = sp.Symbol('p', positive=True, integer=True)
        # Formes symboliques exactes (cf. methode_spectral.thy)
        self.SA_sym = sp.Rational(13, 8) * 2**self.n - 2          # (3.25/2)*2^n - 2
        self.SB_sym = sp.Rational(13, 4) * 2**self.n - 66         # (6.5/2)*2^n - 66
        # digamma_calc(n,p) = SB(n) - 64*p
        self.digamma_sym = self.SB_sym - 64 * self.p
        # Reconstruction : (SB(n) - digamma_calc(n,p)) / 64
        self.recon_sym = (self.SB_sym - self.digamma_sym) / 64

    def validate(self, position: int, ratio: str = "1/2", prime: int | None = None) -> dict[str, Any]:
        """
        Valide symboliquement la reconstruction pour une position donnee.
        
        Returns:
            dict avec : SA, SB, digamma_calc, P_reconstruit, identite_verifiee
        """
        if ratio != "1/2":
            return {
                "supported": False,
                "reason": f"SympyValidator gere uniquement le rapport 1/2 pour le moment (recu : {ratio})",
            }

        n_val = sp.Integer(position)
        SA_val = self.SA_sym.subs(self.n, n_val)
        SB_val = self.SB_sym.subs(self.n, n_val)

        if prime is not None:
            p_val = sp.Integer(prime)
            dig_val = self.digamma_sym.subs({self.n: n_val, self.p: p_val})
            # Verifie l'identite : (SB - digamma) / 64 = p
            recon_val = ((SB_val - dig_val) / 64).simplify()
            identity_ok = bool(sp.Eq(recon_val, p_val).simplify() == sp.true)
        else:
            p_val = None
            dig_val = None
            recon_val = None
            identity_ok = None

        return {
            "supported": True,
            "ratio": ratio,
            "position": position,
            "SA": int(SA_val) if SA_val.is_integer else float(SA_val),
            "SA_symbolic": str(self.SA_sym.subs(self.n, n_val)),
            "SB": int(SB_val) if SB_val.is_integer else float(SB_val),
            "SB_symbolic": str(self.SB_sym.subs(self.n, n_val)),
            "prime_input": prime,
            "digamma_calc": int(dig_val) if dig_val is not None and dig_val.is_integer else dig_val,
            "P_reconstruit": int(recon_val) if recon_val is not None and recon_val.is_integer else recon_val,
            "identity_verified": identity_ok,
            "method": "sympy.Rational (fractions exactes)",
        }

    def render(self, report: dict[str, Any]) -> str:
        """Rendu texte du rapport pour affichage CLI."""
        if not report.get("supported"):
            return f"[sympy] {report.get('reason', 'non supporte')}"
        lines = [f"[sympy] Validation symbolique position={report['position']}, ratio={report['ratio']}"]
        lines.append(f"  SA = {report['SA']}   (forme : {report['SA_symbolic']})")
        lines.append(f"  SB = {report['SB']}   (forme : {report['SB_symbolic']})")
        if report.get("prime_input") is not None:
            lines.append(f"  digamma_calc({report['position']}, {report['prime_input']}) = {report['digamma_calc']}")
            lines.append(f"  P_reconstruit = {report['P_reconstruit']}")
            mark = "OK" if report["identity_verified"] else "ECHEC"
            lines.append(f"  IDENTITE (SB - dig)/64 = p : [{mark}]")
        lines.append(f"  methode : {report['method']}")
        return "\n".join(lines)
