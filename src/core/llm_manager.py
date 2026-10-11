"""
LLM Manager v3 - Avec système de mémoire Gabriel intégré
Chaîne de fallback: Ollama → Claude → OpenAI + RAG sémantique/syntaxique
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

from ..adapters.llm.ollama_client import OllamaClient
from ..adapters.llm.openai_client import OpenAIClient
from ..adapters.llm.utf8_sanitizer import UTF8Sanitizer
from .conversational_memory import (
    ConversationalMemory,
    merge_context_into_prompt,
)

logger = logging.getLogger(__name__)

# Nouvelles imports Claude
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

# ========================================================================
# INTÉGRATION MÉMOIRE GABRIEL
# ========================================================================

INTEGRATEUR_MEMOIRE = None
try:
    # Importer l'intégrateur de mémoire
    sys.path.insert(0, str(Path(__file__).parent))
    from integrateur_memoire import IntegrateurMemoireGabriel
    INTEGRATEUR_MEMOIRE = IntegrateurMemoireGabriel()
    logger.info("✅ Système de mémoire Gabriel activé (RAG sémantique + syntaxique)")
except Exception as e:
    logger.warning(f"⚠️ Système de mémoire désactivé: {e}")
    INTEGRATEUR_MEMOIRE = None


class ClaudeClient:
    """Client Anthropic Claude - nouveau dans v2"""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: float = 60,
    ):
        # Modèle : argument explicite > variable d'env > par défaut Sonnet 4.5
        self.api_key = (
            api_key
            or os.getenv("CLAUDE_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
        )

        # Détection des placeholders d'un .env non rempli -> on neutralise
        if self.api_key:
            placeholders = ("COLLEZ", "VOTRE", "PLACEHOLDER", "sk-ant-[")
            if any(self.api_key.upper().startswith(p.upper()) for p in placeholders):
                # SÉCURITÉ: Utiliser secrets pour un masquage sécurisé (non-réversible)
                # au lieu de SHA256 qui est faible pour les données sensibles (API keys)
                # Refs: OWASP CWE-327, CWE-328, CWE-916
                import secrets
                # Générer un token aléatoire pour masquer la clé (pas une hash)
                masked = secrets.token_hex(4)  # 8 caractères hexadécimaux aléatoires
                logger.warning(
                    "CLAUDE_API_KEY semble invalide (token=%s). Claude désactivé jusqu'à saisie d'une clé réelle.",
                    masked,
                )
                self.api_key = None

        self.model = (
            model
            or os.getenv("CLAUDE_MODEL")
            or "claude-sonnet-4-5-20250929"
        )
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

        self.client = None
        if self.api_key:
            if not CLAUDE_AVAILABLE:
                logger.error(
                    "❌ Module 'anthropic' non installé dans le container Docker.\n"
                    "   -> Vérifier que requirements.txt contient : anthropic>=0.40.0\n"
                    "   -> Puis rebuild l'image : docker-compose down && docker-compose up --build"
                )
            else:
                try:
                    self.client = anthropic.Anthropic(api_key=self.api_key)
                    logger.info(f"✅ Claude client initialized: model={self.model}")
                except Exception as e:
                    logger.error(f"❌ Claude initialization failed: {e}")

    def is_available(self) -> bool:
        """Vérifie si Claude est disponible"""
        return self.client is not None and self.api_key is not None

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float | None = None,
    ) -> str:
        """Génère réponse via Claude API"""

        if not self.is_available():
            return ""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system
                or "Tu es Gabriel, un expert en mathématiques et géométrie spectrale.",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature or self.temperature,
                timeout=self.timeout,
            )

            return response.content[0].text

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            return ""
        except Exception as e:
            logger.error(f"Claude generation error: {e}")
            return ""

    async def chat(
        self,
        messages: list[dict],
        temperature: float | None = None,
    ) -> str:
        """Chat multi-tours avec Claude"""

        if not self.is_available():
            return ""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=messages,
                temperature=temperature or self.temperature,
                timeout=self.timeout,
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude chat error: {e}")
            return ""


class LLMManager:
    """
    LLM Manager v3 - Avec système de mémoire Gabriel

    NOUVELLE PRIORITÉ:
    1. Ollama (10s timeout) - local, rapide
    2. Claude (60s timeout) - expert logique, tâches complexes
    3. OpenAI (90s timeout) - fallback ultime

    + RAG sémantique/syntaxique + cache d'erreurs persistent
    """

    def __init__(self, config: dict[str, Any]):
        llm_cfg = config.get("llm", {})
        ollama_cfg = llm_cfg.get("ollama", {})
        claude_cfg = llm_cfg.get("claude", {})
        openai_cfg = llm_cfg.get("openai", {})

        # Configuration primaire/fallbacks
        self.primary = llm_cfg.get("primary", "ollama")
        self.fallback_1 = llm_cfg.get("fallback_1", "claude")
        self.fallback_2 = llm_cfg.get("fallback_2", "openai")

        # Initialiser clients
        self.ollama = OllamaClient(
            base_url=ollama_cfg.get("base_url"),
            model=ollama_cfg.get("model", "llama3.2"),
            timeout=float(ollama_cfg.get("timeout_seconds", 10)),
        )

        self.claude = ClaudeClient(
            api_key=None,
            model=claude_cfg.get("model") or None,
            temperature=float(claude_cfg.get("temperature", 0.7)),
            max_tokens=int(claude_cfg.get("max_tokens", 4096)),
            timeout=float(
                os.environ.get("CLAUDE_TIMEOUT_SECONDS")
                or claude_cfg.get("timeout_seconds")
                or 60  # augmente de 20s -> 60s (2026-06-28, éviter timeouts Sonnet 4.5)
            ),
        )

        self.openai = OpenAIClient(
            api_key=None,
            model=openai_cfg.get("model", "gpt-4o"),
            temperature=float(openai_cfg.get("temperature", 0.2)),
            max_tokens=int(openai_cfg.get("max_tokens", 4096)),
            timeout=float(
                os.environ.get("OPENAI_TIMEOUT_SECONDS")
                or openai_cfg.get("timeout_seconds")
                or 45  # augmente de 30s -> 45s en cohérence avec Claude 60s
            ),
        )

        self._ollama_available: bool | None = None

        # === Mémoire conversationnelle courte (P1) ===
        conv_cfg = (config.get("conversation", {}) or {}) if config else {}
        conv_max_turns = int(conv_cfg.get("max_turns", 3))
        conv_max_chars = int(conv_cfg.get("max_chars_per_field", 1500))
        self.conversation_memory = ConversationalMemory(
            max_turns=conv_max_turns,
            max_chars_per_field=conv_max_chars,
        )

        logger.info("✅ LLM Manager v3 Initialized")
        logger.info(
            "   Chaîne fallback: Ollama (%.0fs) → %s (%.0fs) → OpenAI %s (%.0fs)",
            self.ollama.timeout,
            getattr(self.claude, "model", "Claude"),
            getattr(self.claude, "timeout", 30),
            getattr(self.openai, "model", "gpt"),
            getattr(self.openai, "timeout", 30),
        )
        if INTEGRATEUR_MEMOIRE:
            logger.info("   Mémoire: Activée (RAG + cache erreurs)")
        logger.info(
            "   Mémoire conversationnelle: %d derniers tours (max %d chars/champ)",
            conv_max_turns,
            conv_max_chars,
        )

    async def _check_ollama(self) -> bool:
        if self._ollama_available is None:
            self._ollama_available = await self.ollama.is_available()
        return self._ollama_available

    def _augmenter_prompt_avec_memoire(
        self,
        prompt: str,
        domaine: str = "general",
    ) -> str:
        """Augmente le prompt avec contexte de mémoire (RAG sémantique Gabriel)."""
        if not INTEGRATEUR_MEMOIRE:
            return prompt

        try:
            return INTEGRATEUR_MEMOIRE.augmenter_prompt(prompt, domaine=domaine)
        except Exception as e:
            logger.warning(f"⚠️ Erreur injection mémoire: {e}")
            return prompt

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        temperature: float = 0.2,
        domaine: str = "general",
        include_conversation: bool = False,
    ) -> str:
        """
        Génère avec mémoire intégrée
        """

        # Sanitization UTF-8
        prompt = UTF8Sanitizer.sanitize(prompt) if prompt else prompt
        if system:
            system = UTF8Sanitizer.sanitize(system)

        # Augmenter le prompt avec mémoire
        prompt_augmente = self._augmenter_prompt_avec_memoire(prompt, domaine)

        # Préfixer avec le contexte conversationnel court (P1)
        if include_conversation and not self.conversation_memory.is_empty():
            ctx_block = self.conversation_memory.build_context_block()
            prompt_augmente = merge_context_into_prompt(
                prompt_augmente,
                ctx_block,
            )
            logger.info(
                "🧠 Contexte conversationnel injecté : %d tours (%d chars)",
                len(self.conversation_memory),
                len(ctx_block),
            )

        # ========== ÉTAPE 1: OLLAMA ==========
        if self.primary == "ollama" and await self._check_ollama():
            logger.info("🔵 Tentative 1/3: Ollama (llama3.2) - timeout 10s")
            result = await self.ollama.generate(
                prompt_augmente,
                system=system,
                temperature=temperature,
            )
            if result and len(result.strip()) > 0:
                logger.info("✅ Ollama a répondu")
                return result
            logger.warning("⚠️ Ollama timeout ou réponse vide (10s expiré)")
        elif self.primary == "ollama":
            logger.warning("⚠️ Ollama indisponible (daemon non détecté)")

        # ========== ÉTAPE 2: CLAUDE ==========
        if self.claude.is_available():
            logger.info(
                "🔴 Tentative 2/3: %s - timeout %.0fs",
                getattr(self.claude, "model", "Claude"),
                getattr(self.claude, "timeout", 30),
            )
            result = await self.claude.generate(
                prompt_augmente,
                system=system,
                temperature=temperature,
            )
            if result and len(result.strip()) > 0:
                logger.info("✅ Claude a répondu (avec mémoire injectée)")
                return result
            logger.warning("⚠️ Claude timeout ou erreur")
        else:
            logger.warning("⚠️ Claude indisponible (CLAUDE_API_KEY manquante)")

        # ========== ÉTAPE 3: OPENAI ==========
        if self.openai.is_available():
            logger.info(
                "🟢 Tentative 3/3: OpenAI (%s) - timeout %.0fs",
                getattr(self.openai, "model", "gpt"),
                getattr(self.openai, "timeout", 30),
            )
            result = await self.openai.generate(
                prompt_augmente,
                system=system,
                temperature=temperature,
            )
            if result and len(result.strip()) > 0:
                logger.info("✅ OpenAI a répondu (fallback)")
                return result
            logger.error("❌ OpenAI timeout ou erreur")
        else:
            logger.error("❌ OpenAI indisponible (OPENAI_API_KEY manquante)")

        # ========== ERREUR CRITIQUE ==========
        logger.critical("❌ TOUS LES LLM ONT ÉCHOUÉ")
        return "[ERREUR LLM] Ollama, Claude ET OpenAI sont inaccessibles."

    async def chat(
        self,
        messages: list[dict],
        temperature: float = 0.2,
        domaine: str = "general",
    ) -> str:
        """Chat multi-tours avec mémoire"""

        # Sanitization UTF-8
        sanitized: list[dict] = []
        for msg in messages:
            new_msg = dict(msg)
            if isinstance(new_msg.get("content"), str):
                new_msg["content"] = UTF8Sanitizer.sanitize(new_msg["content"])
            sanitized.append(new_msg)
        messages = sanitized

        # Augmenter dernier message avec mémoire
        if messages and messages[-1].get("role") == "user":
            messages[-1]["content"] = self._augmenter_prompt_avec_memoire(
                messages[-1]["content"],
                domaine,
            )

        # OLLAMA
        if self.primary == "ollama" and await self._check_ollama():
            logger.info("🔵 Chat Ollama")
            result = await self.ollama.chat(messages, temperature=temperature)
            if result:
                return result
            logger.warning("⚠️ Ollama chat vide, fallback Claude")

        # CLAUDE
        if self.claude.is_available():
            logger.info("🔴 Chat Claude (mémoire injectée)")
            result = await self.claude.chat(messages, temperature=temperature)
            if result:
                return result
            logger.warning("⚠️ Claude chat vide, fallback OpenAI")

        # OPENAI
        if self.openai.is_available():
            logger.info("🟢 Chat OpenAI (fallback)")
            result = await self.openai.chat(messages, temperature=temperature)
            if result:
                return result
            logger.error("❌ OpenAI chat vide")

        return "[ERREUR LLM] Chat indisponible"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("\n" + "=" * 70)
    print("LLM MANAGER v3 - AVEC SYSTÈME DE MÉMOIRE GABRIEL")
    print("=" * 70)

    print(
        """
    CHAÎNE DE FALLBACK + MÉMOIRE:

    1️⃣ OLLAMA (llama3.2)
       └─ Timeout: 10s
       └─ + Injection mémoire (RAG sémantique)

    2️⃣ CLAUDE (claude-3-5-sonnet) ⭐ PRIORITAIRE
       └─ Timeout: 60s
       └─ + Injection mémoire (RAG sémantique + syntaxique)

    3️⃣ OPENAI (gpt-4o)
       └─ Timeout: 90s
       └─ + Injection mémoire (fallback)

    SYSTÈME DE MÉMOIRE:
    ✅ RAG sémantique (axiomes, définitions)
    ✅ RAG syntaxique (patterns, lemmes)
    ✅ Cache d'erreurs persistent
    ✅ Stratégie d'évitement (pas 3x même erreur)
    ✅ Apprentissage continu
    """
    )

    print("=" * 70)
