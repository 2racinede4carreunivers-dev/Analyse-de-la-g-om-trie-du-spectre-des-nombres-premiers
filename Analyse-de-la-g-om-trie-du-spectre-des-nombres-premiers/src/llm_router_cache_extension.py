"""
Extension LLM Router - Méthode query_with_cache pour prompt caching
À intégrer dans src/llm_router.py
"""

from typing import Dict, Any, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def query_with_cache_extension(self, request_with_cache: Dict[str, Any], task_type, model: str = 'claude') -> Tuple[str, Dict]:
    """
    Requête avec prompt caching activé (Anthropic)
    
    À ajouter à la classe LLMRouter
    
    Args:
        request_with_cache: Dict construit par PromptCacheManager.build_anthropic_request_with_cache()
        task_type: Type de tâche TaskType
        model: Modèle à utiliser (doit être 'claude')
    
    Returns:
        (response_text, metadata avec info cache)
    """
    
    if model != 'claude':
        raise ValueError("Prompt caching disponible uniquement avec Claude (Anthropic)")
    
    if not self.claude_client:
        raise ValueError("Claude client non initialisé")
    
    # Déconstruire la requête construite avec cache
    system = request_with_cache.get('system')
    messages = request_with_cache.get('messages')
    
    if not system or not messages:
        raise ValueError("Requête avec cache mal formée")
    
    try:
        # Appel Anthropic avec cache_control ephemeral dans system
        response = self.claude_client.messages.create(
            model=self.claude_config.model_id,
            max_tokens=self.claude_config.max_tokens,
            system=system,  # Déjà avec cache_control: { "type": "ephemeral" }
            messages=messages,
            temperature=self.claude_config.temperature
        )
        
        text = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        
        # Extraire info cache si disponible
        cache_creation_tokens = getattr(response.usage, 'cache_creation_input_tokens', 0)
        cache_read_tokens = getattr(response.usage, 'cache_read_input_tokens', 0)
        
        # Mettre à jour tracking
        self.rate_limit_tracking['claude']['requests'] += 1
        self.rate_limit_tracking['claude']['tokens'] += tokens
        
        logger.info(f"[CACHE INFO] Creation: {cache_creation_tokens}, Read: {cache_read_tokens}")
        
        return text, {
            'model': 'claude',
            'tokens_used': tokens,
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens,
            'cache_creation_input_tokens': cache_creation_tokens,
            'cache_read_input_tokens': cache_read_tokens
        }
    
    except Exception as e:
        logger.error(f"Erreur requête cache Claude: {e}")
        raise


# INSTRUCTIONS D'INTÉGRATION
"""
Pour ajouter prompt caching au LLMRouter:

1. Ajouter cette méthode à la classe LLMRouter dans src/llm_router.py:
   
   def query_with_cache(self, request_with_cache: Dict[str, Any], 
                       task_type, model: str = 'claude') -> Tuple[str, Dict]:
       # Code de query_with_cache_extension ci-dessus
   
2. Utilisation dans gabriel_llm_integration_cache.py:
   
   if self.enable_cache and decision.selected_model == 'claude':
       request_with_cache = self.cache_manager.build_anthropic_request_with_cache(...)
       response_text, metadata = self.router.query_with_cache(
           request_with_cache=request_with_cache,
           task_type=task_type,
           model='claude'
       )
"""
