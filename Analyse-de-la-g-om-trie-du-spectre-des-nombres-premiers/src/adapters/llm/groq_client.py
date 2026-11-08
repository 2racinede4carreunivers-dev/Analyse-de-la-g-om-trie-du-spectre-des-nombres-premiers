"""Client async pour l'API compatible OpenAI de Groq."""
from __future__ import annotations

import logging
import os

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class GroqClient:
    """Client Groq utilise comme fallback cloud apres Ollama."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        timeout: float = 60.0,
        base_url: str = "https://api.groq.com/openai/v1",
    ):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if self.api_key and self.api_key.strip().upper() in {
            "VOTRE_CLE_GROQ_ICI",
            "YOUR_GROQ_API_KEY",
        }:
            self.api_key = None
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.base_url = base_url
        self._client: AsyncOpenAI | None = None

    def is_available(self) -> bool:
        return bool(self.api_key)

    def _get_client(self) -> AsyncOpenAI:
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY absent : impossible d'utiliser Groq.")
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                timeout=self.timeout,
            )
        return self._client

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float | None = None,
    ) -> str | None:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return await self.chat(messages, temperature=temperature)

    async def chat(
        self,
        messages: list[dict],
        temperature: float | None = None,
    ) -> str | None:
        try:
            response = await self._get_client().chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=self.max_tokens,
            )
            return (response.choices[0].message.content or "").strip() or None
        except Exception as exc:
            logger.error("Groq erreur : %s", exc)
            return None
