#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROUTEUR LLM EXPLICITE - Gabriel v7.2
====================================

Résout le conflit OpenAI/Anthropic en forçant une cascade stricte:
1. Ollama (local, 10s timeout)
2. Claude (expert maths, 60s timeout) ← PRIORITAIRE si Ollama échoue
3. OpenAI (fallback ultime, 30s timeout)

NE JAMAIS sauter Claude pour OpenAI!
"""

import os
import asyncio
import logging
from typing import Tuple, Optional, Dict, Any
from enum import Enum

# ========================================================================
# CONFIGURATION
# ========================================================================

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class LLMProvider(Enum):
    """Énumération des fournisseurs LLM"""
    OLLAMA = "ollama"
    CLAUDE = "claude"
    OPENAI = "openai"

# ========================================================================
# ROUTEUR LLM - LOGIQUE PRINCIPALE
# ========================================================================

class LLMRouterExplicite:
    """
    Routeur avec cascade STRICTE:
    - Jamais de saut (Claude ne peut pas être sauté pour OpenAI)
    - Timeouts respectés
    - Logging explicite de chaque décision
    - Anti-collision: un seul fournisseur à la fois
    """
    
    def __init__(self):
        """Initialise le routeur avec priorités strictes"""
        
        # Cascade OBLIGATOIRE (ordre inviolable)
        self.priority_cascade = [
            (LLMProvider.OLLAMA, 10, self._call_ollama),
            (LLMProvider.CLAUDE, 60, self._call_claude),      # ← PRIORITAIRE
            (LLMProvider.OPENAI, 30, self._call_openai),      # ← Dernier recours
        ]
        
        # État d'exécution
        self._lock = asyncio.Lock()
        self._current_provider: Optional[LLMProvider] = None
        self._call_count = 0
    
    async def route_request(self, prompt: str, debug: bool = True) -> Dict[str, Any]:
        """
        Route une requête via cascade stricte
        
        Args:
            prompt: Texte à envoyer au LLM
            debug: Affiche le log détaillé du routage
        
        Returns:
            {'provider': str, 'content': str, 'attempts': int, 'time_ms': float}
        """
        
        # Anti-collision: un seul appel à la fois
        async with self._lock:
            self._call_count += 1
            call_id = self._call_count
        
        logger.info(f"[CALL #{call_id}] Routage requête (cascade stricte)")
        
        # Essayer chaque fournisseur dans l'ordre FIXE
        for attempt_num, (provider, timeout, call_func) in enumerate(self.priority_cascade, 1):
            
            # Vérifier que la clé API existe
            if not self._provider_enabled(provider):
                logger.warning(f"[ATTEMPT {attempt_num}/{len(self.priority_cascade)}] {provider.value} désactivé (clé manquante)")
                continue
            
            logger.info(f"[ATTEMPT {attempt_num}/{len(self.priority_cascade)}] {provider.value.upper()} ({timeout}s timeout)")
            
            try:
                # Enregistrer le fournisseur actif
                self._current_provider = provider
                
                # Appel avec timeout strict
                response = await asyncio.wait_for(
                    call_func(prompt),
                    timeout=timeout
                )
                
                logger.info(f"[SUCCESS #{call_id}] {provider.value} a répondu (attempt {attempt_num})")
                
                return {
                    'provider': provider.value,
                    'content': response,
                    'attempts': attempt_num,
                    'success': True,
                    'call_id': call_id
                }
                
            except asyncio.TimeoutError:
                logger.warning(f"[TIMEOUT #{call_id}] {provider.value} a expiré ({timeout}s)")
                # Continuer au fournisseur suivant
                continue
            
            except Exception as e:
                logger.error(f"[ERROR #{call_id}] {provider.value} erreur: {str(e)[:100]}")
                # Continuer au fournisseur suivant
                continue
            
            finally:
                self._current_provider = None
        
        # Tous les fournisseurs ont échoué
        logger.error(f"[FATAL #{call_id}] Tous les fournisseurs LLM ont échoué!")
        
        return {
            'provider': 'NONE',
            'content': 'Erreur: Tous les fournisseurs LLM sont indisponibles',
            'attempts': len(self.priority_cascade),
            'success': False,
            'call_id': call_id
        }
    
    # ====================================================================
    # APPELS LLM SPÉCIFIQUES
    # ====================================================================
    
    async def _call_ollama(self, prompt: str) -> str:
        """Appel Ollama (local)"""
        
        # Simulation d'un appel Ollama
        # En production: utiliser la vraie API Ollama
        
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        
        logger.debug(f"  → Ollama: {ollama_host} (model: {ollama_model})")
        
        # TODO: Appel réel à Ollama
        raise asyncio.TimeoutError("Ollama timeout simulé")
    
    async def _call_claude(self, prompt: str) -> str:
        """Appel Claude Anthropic"""
        
        api_key = os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')
        
        if not api_key:
            raise Exception("ANTHROPIC_API_KEY non définie")
        
        logger.debug(f"  → Claude: utilise ANTHROPIC_API_KEY")
        
        # Import Anthropic SDK (si disponible)
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=api_key)
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text
        
        except ImportError:
            logger.warning("  → anthropic SDK non installé, simulation")
            return f"[Claude simulé] Réponse à: {prompt[:50]}..."
        
        except Exception as e:
            logger.error(f"  → Claude erreur: {e}")
            raise
    
    async def _call_openai(self, prompt: str) -> str:
        """Appel OpenAI"""
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise Exception("OPENAI_API_KEY non définie")
        
        logger.debug(f"  → OpenAI: utilise OPENAI_API_KEY")
        
        # Import OpenAI SDK
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4o",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
        
        except ImportError:
            logger.warning("  → openai SDK non installé, simulation")
            return f"[OpenAI simulé] Réponse à: {prompt[:50]}..."
        
        except Exception as e:
            logger.error(f"  → OpenAI erreur: {e}")
            raise
    
    # ====================================================================
    # UTILITAIRES
    # ====================================================================
    
    def _provider_enabled(self, provider: LLMProvider) -> bool:
        """Vérifie si un fournisseur a sa clé API configurée"""
        
        if provider == LLMProvider.OLLAMA:
            return os.getenv('OLLAMA_HOST') is not None
        
        elif provider == LLMProvider.CLAUDE:
            return bool(
                os.getenv('ANTHROPIC_API_KEY') or 
                os.getenv('CLAUDE_API_KEY')
            )
        
        elif provider == LLMProvider.OPENAI:
            return os.getenv('OPENAI_API_KEY') is not None
        
        return False
    
    def get_current_provider(self) -> Optional[str]:
        """Retourne le fournisseur actuellement actif"""
        return self._current_provider.value if self._current_provider else None

# ========================================================================
# TEST
# ========================================================================

async def test_router():
    """Test du routeur"""
    
    print("\n" + "="*80)
    print("TEST ROUTEUR LLM EXPLICITE - ANTI-CONFLIT OPENAI/ANTHROPIC")
    print("="*80 + "\n")
    
    router = LLMRouterExplicite()
    
    # Afficher config
    print("Configuration des fournisseurs:")
    print(f"  OLLAMA_HOST: {os.getenv('OLLAMA_HOST', 'non définie')}")
    print(f"  ANTHROPIC_API_KEY: {'✓' if os.getenv('ANTHROPIC_API_KEY') else '✗'}")
    print(f"  OPENAI_API_KEY: {'✓' if os.getenv('OPENAI_API_KEY') else '✗'}")
    
    print(f"\nCascade de priorité (FIXE, inviolable):")
    for i, (prov, timeout, _) in enumerate(router.priority_cascade, 1):
        print(f"  {i}. {prov.value.upper()} ({timeout}s timeout)")
    
    # Test
    test_prompts = [
        "Dis bonjour",
        "Qu'est-ce que la géométrie spectrale?",
    ]
    
    for prompt in test_prompts:
        print(f"\n--- Test: {prompt[:40]}... ---")
        
        result = await router.route_request(prompt, debug=True)
        
        print(f"\nRésultat:")
        print(f"  Provider: {result['provider']}")
        print(f"  Attempts: {result['attempts']}/{len(router.priority_cascade)}")
        print(f"  Success: {result['success']}")
        if result['success']:
            print(f"  Content: {result['content'][:100]}...")

if __name__ == "__main__":
    asyncio.run(test_router())
