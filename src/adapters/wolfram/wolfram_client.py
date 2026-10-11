"""
Client async pour Wolfram|Alpha Full Results API.

Utilise comme oracle de verification numerique independant.
L'App ID est lu depuis WOLFRAM_APP_ID dans .env
Obtenir un App ID gratuit : https://developer.wolframalpha.com/access
"""
from __future__ import annotations

import logging
import os
from typing import Any

import httpx


logger = logging.getLogger(__name__)

WOLFRAM_API_BASE_URL = "https://api.wolframalpha.com/v2/query"


class WolframError(Exception):
    """Erreur generique Wolfram."""


class WolframTimeoutError(WolframError):
    """Timeout d'une requete Wolfram."""


class WolframInvalidAppIDError(WolframError):
    """AppID invalide."""


class WolframNoResultError(WolframError):
    """Wolfram n'a pas pu interpreter la requete."""


class WolframClient:
    """Client asynchrone Wolfram|Alpha (verification numerique independante)."""

    def __init__(
        self,
        app_id: str | None = None,
        timeout: float = 15.0,
        client: httpx.AsyncClient | None = None,
    ):
        self.app_id = app_id or os.environ.get("WOLFRAM_APP_ID", "")
        self.timeout = timeout
        self._external_client = client

    def is_available(self) -> bool:
        if not self.app_id:
            return False
        # Detection des placeholders connus (.env non rempli)
        placeholders = ("VOTRE-WOLFRAM", "COLLEZ-VOTRE", "COLLEZ_VOTRE",
                        "VOTRE_WOLFRAM", "PLACEHOLDER")
        return not any(self.app_id.upper().startswith(p.upper())
                       for p in placeholders)

    async def query_full_results(self, input_text: str) -> dict[str, Any]:
        """Appelle l'API Full Results. Retourne le queryresult ou leve une exception."""
        if not self.is_available():
            raise WolframInvalidAppIDError("WOLFRAM_APP_ID absent ou non configure dans .env")

        params = {
            "appid": self.app_id,
            "input": input_text,
            "format": "plaintext",
            "output": "json",
        }

        timeout_cfg = httpx.Timeout(self.timeout, connect=5.0)

        try:
            if self._external_client is not None:
                response = await self._external_client.get(
                    WOLFRAM_API_BASE_URL, params=params, timeout=timeout_cfg
                )
            else:
                async with httpx.AsyncClient(timeout=timeout_cfg) as client:
                    response = await client.get(WOLFRAM_API_BASE_URL, params=params)
        except httpx.TimeoutException as exc:
            raise WolframTimeoutError(f"Timeout apres {self.timeout}s") from exc
        except httpx.RequestError as exc:
            raise WolframError(f"Erreur reseau Wolfram : {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise WolframError("Reponse Wolfram non-JSON") from exc

        queryresult = data.get("queryresult")
        if not queryresult:
            raise WolframError("Reponse Wolfram malformee : pas de queryresult")

        if queryresult.get("error"):
            err = queryresult.get("error", {})
            msg = err.get("msg") or "Erreur inconnue"
            code = err.get("code")
            if "Invalid appid" in str(msg) or code == 1 or code == "1":
                raise WolframInvalidAppIDError(f"AppID invalide : {msg}")
            raise WolframError(f"Erreur Wolfram : {msg} (code={code})")

        if not queryresult.get("success", False):
            raise WolframNoResultError("Wolfram n'a pas pu interpreter la requete")

        return queryresult

    @staticmethod
    def extract_primary_plaintext(queryresult: dict[str, Any]) -> str | None:
        """Extrait le plaintext du pod primaire (ou du premier pod)."""
        pods = queryresult.get("pods", [])
        for pod in pods:
            if pod.get("primary"):
                for subpod in pod.get("subpods", []):
                    if subpod.get("plaintext"):
                        return subpod["plaintext"]
        if pods:
            for subpod in pods[0].get("subpods", []):
                if subpod.get("plaintext"):
                    return subpod["plaintext"]
        return None
