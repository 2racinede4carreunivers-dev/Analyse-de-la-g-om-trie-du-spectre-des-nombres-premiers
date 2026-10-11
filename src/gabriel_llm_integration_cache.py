"""
Gabriel LLM Integration - Version SAFE BUDGET avec PROMPT CACHING
Intègre Cost Manager + Prompt Cache Manager pour économiser énormément de tokens
"""

import logging
from typing import Dict, Any, Optional

from src.llm_router import LLMRouter, TaskType
from src.prompt_injector import PromptInjector
from src.cost_manager import ClaudeBudgetManager
from src.prompt_cache_manager import PromptCacheManager

logger = logging.getLogger(__name__)

class GabrielLLMIntegrationSafeBudgetWithCache:
    """Gabriel avec gestion budget Claude + Prompt Caching - version sûre et économique"""
    
    def __init__(self, monthly_budget_usd: float = 7.0, enable_cache: bool = True):
        """
        Initialise Gabriel avec budget protection + prompt caching
        
        Args:
            monthly_budget_usd: Budget mensuel en USD (défaut 7$)
            enable_cache: Activer prompt caching éphémère (défaut True)
        """
        self.router = LLMRouter()
        self.injector = PromptInjector()
        self.budget_manager = ClaudeBudgetManager(monthly_budget_usd=monthly_budget_usd)
        self.cache_manager = PromptCacheManager(debug_mode=False) if enable_cache else None
        self.response_cache = {}
        self.enable_cache = enable_cache
    
    def query_intelligent(self, 
                         question: str,
                         task_type: Optional[TaskType] = None,
                         use_theory_context: bool = True,
                         force_openai_if_budget_low: bool = True,
                         debug_context: Optional[str] = None,
                         timeline_id: str = "") -> Dict[str, Any]:
        """
        Requête intelligente avec protection budget + prompt caching
        
        Args:
            question: Question utilisateur
            task_type: Type de tâche (auto-détecté si None)
            use_theory_context: Injecter axiomes Savard
            force_openai_if_budget_low: Basculer OpenAI si budget proche limite
            debug_context: Contexte debug timeline slow motion (optionnel)
            timeline_id: ID unique pour le contexte debug
        
        Returns:
            Réponse complète avec métadonnées + économies cache
        """
        
        logger.info(f"[Gabriel] Requête: {question[:50]}...")
        
        # 🛡️ VÉRIFIER BUDGET AVANT REQUÊTE
        budget_ok = self.budget_manager.check_budget()
        
        if not budget_ok:
            logger.warning("⚠️ Budget Claude atteint - Utiliser OpenAI seul")
            use_claude = False
        else:
            use_claude = True
        
        # Classifier si nécessaire
        if task_type is None:
            task_type = self.router.classify_task(question)
            logger.info(f"  → Tâche classifiée: {task_type.value}")
        
        # Injecter contexte théorique si applicable
        if use_theory_context:
            injected = self.injector.inject_for_ollama(question, str(task_type.value))
            prompt = injected
        else:
            prompt = question
        
        # Décider modèle
        decision = self.router.decide_model(task_type)
        
        # BUDGET CHECK: Si budget bas et tâche non-critique, utiliser OpenAI
        report = self.budget_manager.get_monthly_report()
        token_usage_percent = report['tokens']['percent_used']
        
        if token_usage_percent > 80 and force_openai_if_budget_low:
            logger.info(f"  ⚠️ Budget à {token_usage_percent:.0f}% - Utiliser OpenAI au lieu de Claude")
            decision.selected_model = 'openai'
        
        logger.info(f"  → Modèle sélectionné: {decision.selected_model.upper()}")
        logger.info(f"  → Budget utilisé: {token_usage_percent:.1f}%")
        
        # System prompt adapté
        system_prompt = self._build_system_prompt(task_type)
        
        try:
            # 🚀 CONSTRUIRE REQUÊTE AVEC CACHE SI ENABLED
            cache_info = {}
            
            if self.enable_cache and decision.selected_model == 'claude':
                # Utiliser prompt caching pour Claude
                request_with_cache = self.cache_manager.build_anthropic_request_with_cache(
                    instructions=system_prompt,
                    user_query=prompt,
                    debug_context=debug_context,
                    timeline_id=timeline_id
                )
                
                # Extraire info cache
                cache_info = request_with_cache.get('cache_info', {})
                logger.info(f"  🔄 Prompt caching activé: {cache_info}")
                
                # Passer au routeur pour utiliser avec cache
                response_text, metadata = self.router.query_with_cache(
                    request_with_cache=request_with_cache,
                    task_type=task_type,
                    model='claude'
                )
            else:
                # Requête standard sans cache (OpenAI ou Claude sans caching)
                response_text, metadata = self.router.query(
                    prompt=prompt,
                    task_type=task_type,
                    system_prompt=system_prompt
                )
            
            # 📊 ENREGISTRER USAGE
            input_tokens = metadata.get('input_tokens', 0)
            output_tokens = metadata.get('output_tokens', 0)
            cache_creation_input_tokens = metadata.get('cache_creation_input_tokens', 0)
            cache_read_input_tokens = metadata.get('cache_read_input_tokens', 0)
            
            self.budget_manager.record_usage(input_tokens, output_tokens)
            
            logger.info(f"  ✓ Requête complète")
            logger.info(f"    Tokens: {input_tokens + output_tokens} (input={input_tokens}, output={output_tokens})")
            
            # Estimer économies cache
            cache_savings = 0
            if cache_read_input_tokens > 0:
                # Tokens lus du cache = 90% moins chers
                cache_savings = int(cache_read_input_tokens * 0.9)
                logger.info(f"    🔄 Cache: {cache_read_input_tokens} tokens lus (économie ~{cache_savings} tokens!)")
            
            # Retourner avec métadonnées budget + cache
            result = {
                'response': response_text,
                'model': metadata['model'],
                'task_type': task_type.value,
                'tokens': {
                    'total': input_tokens + output_tokens,
                    'input': input_tokens,
                    'output': output_tokens,
                    'cache_creation': cache_creation_input_tokens,
                    'cache_read': cache_read_input_tokens
                },
                'cache': {
                    'enabled': self.enable_cache,
                    'savings': {
                        'tokens_saved': cache_savings,
                        'percent_saved': f"{(cache_savings / (input_tokens + output_tokens + cache_savings) * 100):.1f}%" if (input_tokens + output_tokens + cache_savings) > 0 else "0%"
                    },
                    'info': cache_info
                },
                'budget': {
                    'tokens_used_this_month': self.budget_manager.tokens_used_this_month,
                    'tokens_budget': self.budget_manager.monthly_token_budget,
                    'tokens_remaining': max(0, self.budget_manager.monthly_token_budget - self.budget_manager.tokens_used_this_month),
                    'cost_this_month': f"${self.budget_manager.cost_this_month:.2f}",
                    'cost_budget': f"${self.budget_manager.monthly_budget_usd:.2f}",
                    'percent_used': (self.budget_manager.tokens_used_this_month / self.budget_manager.monthly_token_budget) * 100
                }
            }
            
            return result
        
        except Exception as e:
            logger.error(f"  ✗ Erreur requête: {e}")
            return {
                'response': None,
                'error': str(e),
                'model': decision.selected_model
            }
    
    def query_debug_timeline(self, 
                            question: str,
                            timeline_context: str,
                            timeline_id: str = "debug-001") -> Dict[str, Any]:
        """
        Requête spécialisée pour debugging avec timeline slow motion
        
        Utilise prompt caching pour le contexte repetitif de la timeline
        Économise énormément de tokens pour les sessions debug interactives
        
        Args:
            question: Question sur le debug
            timeline_context: Contexte timeline complet (slow motion)
            timeline_id: ID unique de la timeline
        
        Returns:
            Réponse debug avec économies cache
        """
        
        logger.info(f"[Gabriel DEBUG] Requête debug timeline: {timeline_id}")
        
        # Utiliser type de tâche approprié pour debug
        task_type = TaskType.LOGICAL_STRUCTURE  # Debug = structure logique
        
        # Construire system prompt pour debug
        system_prompt = """Tu es Gabriel en mode DEBUG.

Ton rôle: Analyser la timeline slow motion de l'agent et identifier:
1. Où l'agent a bloqué
2. Pourquoi le blocage s'est produit
3. Comment le reformuler pour générer une réponse probable

Sois DIRECT et CONCIS."""
        
        # Utiliser cache pour la timeline (très répétitive)
        return self.query_intelligent(
            question=question,
            task_type=task_type,
            use_theory_context=False,
            debug_context=timeline_context,
            timeline_id=timeline_id
        )
    
    def _build_system_prompt(self, task_type: TaskType) -> str:
        """Construit system prompt adapté à la tâche"""
        
        base_prompt = """Tu es Gabriel, un assistant mathématique multiloop de haut niveau.

Ton expertise couvre:
- Théorie personnelle "L'univers est au carré" (Philippe Thomas Savard)
- Géométrie spectrale asymétrique des nombres premiers
- Analyse RSA (Rapport Spectral Asymétrique Ordonné)
- Preuves formelles en HOL4/Lean4
- Validation de structures mathématiques rigoureuses

IMPORTANT: Réponses COURTES et DIRECTES (≤ 150 mots si possible)
pour optimiser utilisation tokens.

NOTE: Cette instruction est en CACHE EPHEMERE - réutilisée entre requêtes
pour économiser ~90% des tokens système."""
        
        if task_type == TaskType.MATHEMATICAL_REASONING:
            return base_prompt + "\nFOCUS: Raisonnement clair, structuré, économe."
        elif task_type == TaskType.CODE_VALIDATION:
            return base_prompt + "\nFOCUS: Validation code HOL4/Lean4 concise."
        elif task_type == TaskType.HOL_PROOF_GENERATION:
            return base_prompt + "\nFOCUS: Preuves complètes mais sans verbosité."
        elif task_type == TaskType.RIEMANN_ANALYSIS:
            return base_prompt + "\nFOCUS: Analyse géométrie spectrale directe."
        elif task_type == TaskType.LOGICAL_STRUCTURE:
            return base_prompt + "\nFOCUS: Structures logiques et déductions."
        else:
            return base_prompt
    
    def print_budget_report(self):
        """Affiche rapport budget courant"""
        self.budget_manager.print_budget_report()
    
    def print_cache_stats(self):
        """Affiche statistiques cache"""
        if self.cache_manager:
            self.cache_manager.print_cache_stats()
        else:
            print("❌ Cache manager non activé")
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Retourne statut budget sans rapport complet"""
        
        report = self.budget_manager.get_monthly_report()
        cache_stats = self.cache_manager.get_cache_stats() if self.cache_manager else {}
        
        return {
            'tokens_percent': report['tokens']['percent_used'],
            'cost_percent': report['cost']['percent_used'],
            'tokens_remaining': report['tokens']['remaining'],
            'cost_remaining': report['cost']['remaining'],
            'requests_count': report['requests'],
            'cache_stats': cache_stats
        }


if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("="*70)
    print("GABRIEL LLM INTEGRATION - SAFE BUDGET + PROMPT CACHING")
    print("="*70)
    
    # Initialiser avec budget safe + caching enabled
    gabriel = GabrielLLMIntegrationSafeBudgetWithCache(
        monthly_budget_usd=7.0,
        enable_cache=True
    )
    
    # Test 1: Requête standard mathématique
    print("\n[TEST 1] Requête mathématique avec cache")
    result = gabriel.query_intelligent(
        "Explique brièvement RSA et sa convergence vers 0.5"
    )
    
    if result.get('response'):
        print(f"✓ Réponse obtenue ({result['tokens']['total']} tokens)")
        print(f"  Modèle: {result['model'].upper()}")
        print(f"  Budget: {result['budget']['percent_used']:.1f}% utilisé")
        if result['cache']['savings']['tokens_saved'] > 0:
            print(f"  🔄 Cache économies: {result['cache']['savings']['tokens_saved']} tokens!")
    
    # Test 2: Requête debug timeline (réutilise cache)
    print("\n[TEST 2] Requête debug timeline (réutilise cache)")
    timeline_debug = """DEBUG TIMELINE SLOW MOTION (timeline-001):
    t=0.0s: Agent initialisation Gabriel
    t=0.5s: Traitement requête mathématique
    t=1.0s: Classification tâche → MATHEMATICAL_REASONING
    t=1.5s: Routage vers Claude
    t=2.0s: Construction system prompt
    [... contexte très long et répétitif ...]
    """
    
    result2 = gabriel.query_debug_timeline(
        question="Pourquoi le blocage à t=1.5s?",
        timeline_context=timeline_debug,
        timeline_id="timeline-001"
    )
    
    if result2.get('response'):
        print(f"✓ Réponse debug obtenue ({result2['tokens']['total']} tokens)")
        if result2['cache']['savings']['tokens_saved'] > 0:
            print(f"  🔄 Cache économies: {result2['cache']['savings']['tokens_saved']} tokens!")
    
    # Afficher rapports
    print("\n[BUDGET REPORT]")
    gabriel.print_budget_report()
    
    print("\n[CACHE STATS]")
    gabriel.print_cache_stats()
