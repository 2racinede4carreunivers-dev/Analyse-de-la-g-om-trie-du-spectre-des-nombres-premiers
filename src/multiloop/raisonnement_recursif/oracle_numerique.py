"""oracle_numerique.py - Oracle numerique du 8e moteur (Wolfram + repli local).

Utilise le package Wolfram (Wolfram|Alpha Full Results API, deja presente dans le
depot : src/adapters/wolfram/wolfram_client.py) comme oracle independant pour
repondre a une question modeste. Si Wolfram n'est pas configure (WOLFRAM_APP_ID
absent) ou si httpx est indisponible, on retombe proprement sur un repli local
deterministe (primalite, petit n-ieme premier) et on EXPLIQUE le blocage.

ADDITIF : tous les imports lourds sont paresseux (au moment de l'appel).
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Optional


@dataclass
class ResultatOracle:
    outcome: str        # verified | contradicted | inconclusive | indisponible | error
    message: str
    source: str         # wolfram | local | aucun
    valeur: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "outcome": self.outcome,
            "message": self.message,
            "source": self.source,
            "valeur": self.valeur,
        }


def _est_premier(n: int) -> bool:
    """Test de primalite deterministe simple (stdlib)."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def _nieme_premier(n: int) -> Optional[int]:
    """Retourne le n-ieme nombre premier (n>=1) si n raisonnable."""
    if n < 1 or n > 100000:
        return None
    compte, candidat = 0, 1
    while compte < n:
        candidat += 1
        if _est_premier(candidat):
            compte += 1
    return candidat


class OracleNumerique:
    """Oracle numerique : Wolfram|Alpha si disponible, sinon repli local."""

    def __init__(self, app_id: Optional[str] = None, timeout: float = 15.0):
        self._app_id = app_id
        self._timeout = timeout
        self._client = None

    # ── disponibilite ──────────────────────────────────────────────────────
    def _charger_client(self):
        if self._client is not None:
            return self._client
        try:
            from ...adapters.wolfram.wolfram_client import WolframClient
            self._client = WolframClient(app_id=self._app_id, timeout=self._timeout)
        except Exception:
            self._client = False  # marqueur : indisponible
        return self._client

    def disponible(self) -> bool:
        client = self._charger_client()
        try:
            return bool(client) and client.is_available()
        except Exception:
            return False

    # ── interrogation ──────────────────────────────────────────────────────
    async def interroger(self, question: str) -> ResultatOracle:
        """Interroge Wolfram ; repli local ; explique si indisponible."""
        client = self._charger_client()
        if client:
            try:
                qr = await client.query_full_results(question)
                texte = client.extract_primary_plaintext(qr)
                if texte:
                    return ResultatOracle("verified", texte[:500], "wolfram", valeur=texte[:200])
                return ResultatOracle("inconclusive", "Wolfram n'a pas retourne de texte.",
                                      "wolfram")
            except Exception as exc:  # timeout, appid, reseau, import httpx...
                local = self._repli_local(question)
                if local is not None:
                    return local
                return ResultatOracle(
                    "indisponible",
                    f"Oracle Wolfram indisponible ({exc}). Repli local impossible pour "
                    f"cette question.",
                    "aucun",
                )
        local = self._repli_local(question)
        if local is not None:
            return local
        return ResultatOracle(
            "indisponible",
            "Oracle numerique indisponible (WOLFRAM_APP_ID absent / package non "
            "installe). La question modeste sera presentee a l'utilisateur.",
            "aucun",
        )

    def interroger_sync(self, question: str) -> ResultatOracle:
        """Version synchrone (utilisable hors boucle asyncio)."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            # Deja dans une boucle : on ne peut pas run_until_complete.
            return self._repli_local(question) or ResultatOracle(
                "indisponible", "Appel synchrone impossible dans une boucle asyncio.",
                "aucun",
            )
        return asyncio.run(self.interroger(question))

    # ── repli local deterministe ───────────────────────────────────────────
    def _repli_local(self, question: str) -> Optional[ResultatOracle]:
        import re
        q = question.lower()
        # "est <n> premier" / "is <n> prime"
        m = re.search(r"(?:est|is)\s+(\d+)\s+(?:premier|prime)", q)
        if m:
            n = int(m.group(1))
            ok = _est_premier(n)
            return ResultatOracle(
                "verified", f"{n} est premier : {'oui' if ok else 'non'} (repli local).",
                "local", valeur=str(ok),
            )
        # "n-ieme nombre premier"
        m2 = re.search(r"(\d+)\s*(?:e|eme|ieme|ième|th)?\s*(?:nombre\s+)?(?:premier|prime)", q)
        if m2:
            n = int(m2.group(1))
            p = _nieme_premier(n)
            if p is not None:
                return ResultatOracle(
                    "verified", f"Le {n}e nombre premier est {p} (repli local).",
                    "local", valeur=str(p),
                )
        return None


__all__ = ["ResultatOracle", "OracleNumerique", "_est_premier", "_nieme_premier"]