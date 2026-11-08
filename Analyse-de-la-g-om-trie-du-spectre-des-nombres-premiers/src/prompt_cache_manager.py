"""
Prompt Cache Manager - Gestion du prompt caching Anthropic pour économiser tokens
Support du caching éphémère pour Gabriel et le debugger timeline slow motion
"""

import logging
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Une entrée de cache"""
    cache_key: str
    content: str
    cache_type: str  # 'system' ou 'debug'
    created_at: datetime
    hits: int = 0
    tokens_saved: int = 0


class PromptCacheManager:
    """
    Gère le prompt caching Anthropic pour économiser tokens.
    
    Supporte:
    - Cache système: Instructions Gabriel (réutilisées à chaque requête)
    - Cache debug: Contexte timeline slow motion (répétitif lors du debugging)
    
    Économies: ~90% sur tokens cachés après 2ème utilisation
    """
    
    def __init__(self, debug_mode: bool = False):
        """
        Initialise le cache manager
        
        Args:
            debug_mode: Active logging détaillé du cache
        """
        self.debug_mode = debug_mode
        self.cache_entries: Dict[str, CacheEntry] = {}
        self.cache_hits = 0
        self.total_tokens_saved = 0
    
    def compute_cache_key(self, content: str, context: str = "") -> str:
        """Calcule une clé de cache unique"""
        combined = f"{content}:{context}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def register_system_cache(self, instructions: str) -> str:
        """
        Enregistre les instructions système pour caching
        
        Args:
            instructions: Instructions Gabriel complètes
        
        Returns:
            cache_key pour utilisation ultérieure
        """
        cache_key = self.compute_cache_key(instructions, "system")
        
        if cache_key in self.cache_entries:
            entry = self.cache_entries[cache_key]
            entry.hits += 1
            logger.info(f"[CACHE] System cache hit #{entry.hits}: {cache_key}")
            return cache_key
        
        entry = CacheEntry(
            cache_key=cache_key,
            content=instructions,
            cache_type='system',
            created_at=datetime.now()
        )
        
        self.cache_entries[cache_key] = entry
        logger.info(f"[CACHE] Registered system cache: {cache_key}")
        
        return cache_key
    
    def register_debug_cache(self, debug_context: str, timeline_id: str = "") -> str:
        """
        Enregistre le contexte debug timeline pour caching
        
        Args:
            debug_context: Contexte complet du debugger
            timeline_id: ID de la timeline (pour différencier les contextes)
        
        Returns:
            cache_key pour utilisation ultérieure
        """
        cache_key = self.compute_cache_key(debug_context, f"debug:{timeline_id}")
        
        if cache_key in self.cache_entries:
            entry = self.cache_entries[cache_key]
            entry.hits += 1
            logger.info(f"[CACHE] Debug cache hit #{entry.hits}: {cache_key}")
            return cache_key
        
        entry = CacheEntry(
            cache_key=cache_key,
            content=debug_context,
            cache_type='debug',
            created_at=datetime.now()
        )
        
        self.cache_entries[cache_key] = entry
        logger.info(f"[CACHE] Registered debug cache: {cache_key}")
        
        return cache_key
    
    def build_cached_system_prompt(self, instructions: str) -> Dict[str, Any]:
        """
        Construit un bloc de system prompt avec caching
        
        Format Anthropic:
        {
          "type": "text",
          "text": "Instructions Gabriel...",
          "cache_control": { "type": "ephemeral" }
        }
        
        Returns:
            Dict prêt pour l'API Anthropic
        """
        _ = self.register_system_cache(instructions)
        
        return {
            "type": "text",
            "text": instructions,
            "cache_control": {"type": "ephemeral"}
        }
    
    def build_cached_debug_context(self, debug_context: str, timeline_id: str = "") -> Dict[str, Any]:
        """
        Construit un bloc de contexte debug avec caching
        
        Format Anthropic:
        {
          "type": "text",
          "text": "DEBUG: [contexte timeline slow motion]",
          "cache_control": { "type": "ephemeral" }
        }
        
        Args:
            debug_context: Texte complet du debug
            timeline_id: Identifiant unique de la timeline
        
        Returns:
            Dict prêt pour l'API Anthropic
        """
        _ = self.register_debug_cache(debug_context, timeline_id)
        
        return {
            "type": "text",
            "text": debug_context,
            "cache_control": {"type": "ephemeral"}
        }
    
    def build_anthropic_request_with_cache(
        self,
        instructions: str,
        user_query: str,
        debug_context: Optional[str] = None,
        timeline_id: str = ""
    ) -> Dict[str, Any]:
        """
        Construit une requête Anthropic complète avec caching multi-blocs
        
        Structure:
        - system: [Instructions Gabriel cachées] + [Debug context cachées si fourni]
        - messages: [{Requête utilisateur unique}]
        
        Args:
            instructions: Instructions Gabriel (système)
            user_query: Question utilisateur (non-cachée)
            debug_context: Contexte debug optionnel (timeline slow motion)
            timeline_id: ID timeline pour le debug
        
        Returns:
            Dict prêt pour client.messages.create()
        """
        
        # Bloc système: Instructions Gabriel
        system_blocks = [
            self.build_cached_system_prompt(instructions)
        ]
        
        # Si contexte debug fourni, l'ajouter en cache aussi
        if debug_context:
            debug_block = self.build_cached_debug_context(debug_context, timeline_id)
            system_blocks.append(debug_block)
            logger.info(f"[CACHE] Debug context added to system (timeline: {timeline_id})")
        
        # Bloc utilisateur: Requête unique (NON cachée)
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_query
                        # Pas de cache_control ici - requête unique
                    }
                ]
            }
        ]
        
        return {
            "system": system_blocks,
            "messages": messages,
            "cache_info": {
                "system_cached": len(system_blocks),
                "debug_cached": 1 if debug_context else 0,
                "total_blocks": len(system_blocks) + 1
            }
        }
    
    def estimate_token_savings(self, system_tokens: int, debug_tokens: int = 0) -> Dict[str, Any]:
        """
        Estime l'économie de tokens après utilisation du cache
        
        Formule Anthropic:
        - Tokens cachés = 1 token pour 4 tokens normaux
        - Après 2 utilisations: 90% d'économie
        
        Args:
            system_tokens: Tokens dans les instructions Gabriel
            debug_tokens: Tokens dans le contexte debug
        
        Returns:
            Récapitulatif économies
        """
        
        total_input = system_tokens + debug_tokens
        
        # Première utilisation: pas d'économie (cache miss)
        # À partir de la 2ème: 90% d'économie
        cached_cost = (total_input / 4) * 0.9  # 90% économie sur 25% du prix normal
        normal_cost = total_input  # Sans cache
        
        savings_per_request = normal_cost - cached_cost
        savings_percent = (savings_per_request / normal_cost) * 100
        
        return {
            "total_cached_tokens": total_input,
            "normal_cost_per_request": f"{normal_cost} tokens",
            "cached_cost_per_request": f"{cached_cost:.0f} tokens",
            "savings_per_request": f"{savings_percent:.1f}%",
            "break_even_requests": 2,  # Après 2 requêtes, cache rentabilisé
            "estimated_monthly_savings": f"{(savings_per_request * 100):.0f} tokens (100 requêtes/mois)"
        }
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne statistiques du cache"""
        
        system_entries = [e for e in self.cache_entries.values() if e.cache_type == 'system']
        debug_entries = [e for e in self.cache_entries.values() if e.cache_type == 'debug']
        
        total_hits = sum(e.hits for e in self.cache_entries.values())
        total_tokens_saved_est = total_hits * 50  # Estimation approximative
        
        return {
            "total_cache_entries": len(self.cache_entries),
            "system_entries": len(system_entries),
            "debug_entries": len(debug_entries),
            "total_cache_hits": total_hits,
            "estimated_tokens_saved": total_tokens_saved_est,
            "system_cache_hits": sum(e.hits for e in system_entries),
            "debug_cache_hits": sum(e.hits for e in debug_entries),
            "cache_entries": [
                {
                    "key": e.cache_key,
                    "type": e.cache_type,
                    "hits": e.hits,
                    "created": e.created_at.isoformat()
                }
                for e in self.cache_entries.values()
            ]
        }
    
    def print_cache_stats(self):
        """Affiche rapport de cache"""
        stats = self.get_cache_stats()
        
        print("\n" + "="*70)
        print("PROMPT CACHE STATISTICS")
        print("="*70)
        print(f"Total entries: {stats['total_cache_entries']}")
        print(f"  - System cache: {stats['system_entries']} (hits: {stats['system_cache_hits']})")
        print(f"  - Debug cache: {stats['debug_entries']} (hits: {stats['debug_cache_hits']})")
        print(f"Total cache hits: {stats['total_cache_hits']}")
        print(f"Estimated tokens saved: ~{stats['estimated_tokens_saved']}")
        print("="*70 + "\n")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    cache_manager = PromptCacheManager(debug_mode=True)
    
    # Instructions Gabriel (longues)
    gabriel_instructions = """Tu es Gabriel, assistant mathématique multiloop expert.
    
    Expertise:
    - Théorie "L'univers est au carré" (Philippe Thomas Savard)
    - Géométrie spectrale asymétrique
    - Analyse RSA complète
    - Preuves HOL4/Lean4
    
    Ton objectif: Fournir des réponses courtes, précises, économes en tokens.
    """
    
    # Contexte debug timeline (répétitif)
    debug_timeline = """DEBUG TIMELINE SLOW MOTION:
    Agent state at t=0.0s: initialized
    Agent state at t=0.5s: processing query
    Agent state at t=1.0s: routing to model
    [... contexte très long et répétitif ...]
    """
    
    # Test 1: Requête standard
    print("\n[TEST 1] Requête mathématique avec cache")
    request = cache_manager.build_anthropic_request_with_cache(
        instructions=gabriel_instructions,
        user_query="Explique RSA brièvement"
    )
    print(f"✓ Requête construite: {request['cache_info']}")
    
    # Test 2: Requête debug
    print("\n[TEST 2] Requête debug avec timeline cache")
    request = cache_manager.build_anthropic_request_with_cache(
        instructions=gabriel_instructions,
        user_query="Pourquoi l'agent a bloqué à t=0.5s?",
        debug_context=debug_timeline,
        timeline_id="timeline-001"
    )
    print(f"✓ Requête debug construite: {request['cache_info']}")
    
    # Test 3: Réutilisation cache (simulée)
    print("\n[TEST 3] Réutilisation du cache")
    request = cache_manager.build_anthropic_request_with_cache(
        instructions=gabriel_instructions,
        user_query="Autre question mathématique?"
    )
    print(f"✓ Réutilisation cache OK")
    
    # Test 4: Statistiques
    print("\n[TEST 4] Statistiques cache")
    cache_manager.print_cache_stats()
    
    # Test 5: Estimations d'économies
    print("\n[TEST 5] Estimations d'économies")
    savings = cache_manager.estimate_token_savings(
        system_tokens=500,
        debug_tokens=800
    )
    for key, value in savings.items():
        print(f"  {key}: {value}")
