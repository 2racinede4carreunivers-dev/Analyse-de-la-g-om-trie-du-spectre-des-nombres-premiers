"""Client async pour OpenAI (fallback)."""
from __future__ import annotations

import logging
import os

from openai import AsyncOpenAI


logger = logging.getLogger(__name__)


class OpenAIClient:
    """Client async pour l'API OpenAI."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-5.4",
        temperature: float = 0.2,
        max_tokens: int = 4096,
        timeout: float = 90.0,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        # Detection des placeholders d'un .env non rempli -> on neutralise
        if self.api_key:
            placeholders = ("COLLEZ", "VOTRE", "PLACEHOLDER", "sk-VOTRE", "sk-[")
            if any(self.api_key.upper().startswith(p.upper()) for p in placeholders):
                self.api_key = None
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self._client: AsyncOpenAI | None = None

    def _get_client(self) -> AsyncOpenAI:
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY absent : impossible d'utiliser le fallback OpenAI."
            )
        if self._client is None:
            self._client = AsyncOpenAI(api_key=self.api_key, timeout=self.timeout)
        return self._client

    def is_available(self) -> bool:
        return bool(self.api_key)

    async def generate(self, prompt: str, system: str | None = None, temperature: float | None = None) -> str | None:
        """Generation simple par completion via chat.completions."""
        messages: list[dict] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return await self.chat(messages, temperature=temperature)

    async def chat(self, messages: list[dict], temperature: float | None = None) -> str | None:
        """Chat multi-tours."""
        try:
            client = self._get_client()
            resp = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=self.max_tokens,
            )
            return (resp.choices[0].message.content or "").strip() or None
        except Exception as exc:
            logger.error("OpenAI erreur : %s", exc)
            return None
