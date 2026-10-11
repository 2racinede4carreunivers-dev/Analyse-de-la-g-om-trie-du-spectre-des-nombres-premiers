"""Client async pour Ollama (LLM local primaire) - AVEC SANITIZATION UTF-8."""
from __future__ import annotations

import logging
import os

import httpx

from .utf8_sanitizer import UTF8Sanitizer


logger = logging.getLogger(__name__)


class OllamaClient:
    """Client async pour l'API Ollama avec correction UTF-8."""

    def __init__(self, base_url: str | None = None, model: str = "llama3.2", timeout: float = 10.0):
        self.base_url = (base_url or os.environ.get("OLLAMA_HOST", "http://ollama:11434")).rstrip("/")
        self.model = model
        self.timeout = timeout
        self.sanitizer = UTF8Sanitizer()

    async def is_available(self) -> bool:
        """Verifie si Ollama est joignable et que le modele est present."""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                if resp.status_code != 200:
                    return False
                data = resp.json()
                models = [m.get("name", "") for m in data.get("models", [])]
                # Tolere les variantes :latest
                return any(self.model in name for name in models)
        except Exception as exc:
            logger.warning("Ollama indisponible : %s", exc)
            return False

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.2,
    ) -> str | None:
        """Genere une reponse via /api/generate. Retourne None si echec.
        
        NOUVEAU: Nettoie le prompt UTF-8 avant envoi.
        """
        # SANITIZE prompt
        prompt_clean = self.sanitizer.sanitize(prompt)
        system_clean = self.sanitizer.sanitize(system) if system else None
        
        payload: dict = {
            "model": self.model,
            "prompt": prompt_clean,
            "stream": False,
            "options": {"temperature": temperature},
        }
        if system_clean:
            payload["system"] = system_clean
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(f"{self.base_url}/api/generate", json=payload)
                if resp.status_code != 200:
                    logger.warning("Ollama HTTP %s : %s", resp.status_code, resp.text[:200])
                    return None
                data = resp.json()
                response = data.get("response", "").strip() or None
                
                # Sanitize la réponse aussi
                if response:
                    response = self.sanitizer.sanitize(response)
                
                return response
        except httpx.TimeoutException:
            logger.warning("Ollama : timeout apres %ss", self.timeout)
            return None
        except Exception as exc:
            logger.error(f"Ollama : erreur {exc}")
            return None

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
    ) -> str | None:
        """Chat multi-tours via /api/chat. messages = [{role, content}, ...]
        
        NOUVEAU: Nettoie tous les messages UTF-8 avant envoi.
        """
        # Sanitize tous les messages
        messages_clean = []
        for msg in messages:
            msg_clean = {
                "role": msg.get("role", "user"),
                "content": self.sanitizer.sanitize(msg.get("content", ""))
            }
            messages_clean.append(msg_clean)
        
        payload = {
            "model": self.model,
            "messages": messages_clean,
            "stream": False,
            "options": {"temperature": temperature},
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(f"{self.base_url}/api/chat", json=payload)
                if resp.status_code != 200:
                    logger.warning("Ollama HTTP %s", resp.status_code)
                    return None
                data = resp.json()
                response = (data.get("message", {}).get("content") or "").strip() or None
                
                # Sanitize la réponse aussi
                if response:
                    response = self.sanitizer.sanitize(response)
                
                return response
        except Exception as exc:
            logger.error(f"Ollama chat : erreur {exc}")
            return None
