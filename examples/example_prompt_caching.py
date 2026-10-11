#!/usr/bin/env python3
"""
GUIDE D'IMPLÉMENTATION - Prompt Caching pour Agent Gabriel
Économiser jusqu'à 90% de tokens pour les requêtes répétitives
"""

import logging
from pathlib import Path
import sys

# Setup
_ROOT = Path(__file__).parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.prompt_cache_manager import PromptCacheManager
from src.gabriel_llm_integration_cache import GabrielLLMIntegrationSafeBudgetWithCache

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_basic_cache():
    """Exemple 1: Utilisation basique du caching"""
    print("\n" + "="*70)
    print("EXEMPLE 1: UTILISATION BASIQUE DU CACHING")
    print("="*70)
    
    # Initialiser Gabriel avec cache
    gabriel = GabrielLLMIntegrationSafeBudgetWithCache(
        monthly_budget_usd=7.0,
        enable_cache=True
    )
    
    # Première requête (cache miss)
    print("\n[1ère requête] Cache MISS - Instructions Gabriel créées dans le cache")
    result1 = gabriel.query_intelligent(
        "Explique la théorie RSA en 50 mots",
        use_theory_context=True
    )
    
    if result1.get('response'):
        print(f"✓ Réponse 1: {result1['response'][:100]}...")
        print(f"  Tokens: {result1['tokens']['total']}")
        print(f"  Cache créé: {result1['cache']['info'].get('system_cached')} blocs")
    
    # Deuxième requête (cache hit)
    print("\n[2ème requête] Cache HIT - Instructions réutilisées (~90% d'économie)")
    result2 = gabriel.query_intelligent(
        "Explique la convergence RSA vers 0.5 en 50 mots",
        use_theory_context=True
    )
    
    if result2.get('response'):
        print(f"✓ Réponse 2: {result2['response'][:100]}...")
        print(f"  Tokens: {result2['tokens']['total']}")
        print(f"  Cache lus: {result2['tokens'].get('cache_read', 0)} tokens")
        print(f"  Économies: {result2['cache']['savings']['tokens_saved']} tokens!")


def example_debug_timeline():
    """Exemple 2: Debugging avec timeline slow motion et caching"""
    print("\n" + "="*70)
    print("EXEMPLE 2: DEBUGGING AVEC TIMELINE SLOW MOTION")
    print("="*70)
    
    gabriel = GabrielLLMIntegrationSafeBudgetWithCache(
        monthly_budget_usd=7.0,
        enable_cache=True
    )
    
    # Contexte debug timeline (très long et répétitif)
    timeline_context = """
DEBUG TIMELINE SLOW MOTION - timeline-debug-001:

t=0.000s: [INIT] Agent Gabriel démarré
  - Config: safe_budget=7.0, cache=enabled
  - Models: Claude (prioritaire), OpenAI (fallback)

t=0.005s: [CONFIG] Chargement configuration
  - Budget manager: OK
  - Cache manager: OK
  - LLM router: OK

t=0.010s: [QUERY] Requête utilisateur reçue
  - Contenu: "Explique RSA"
  - Longueur: 12 tokens

t=0.015s: [CLASSIFY] Classification de la tâche
  - Mots-clés détectés: ['rsa', 'explique']
  - Task type: MATHEMATICAL_REASONING (Claude★★★★★)

t=0.020s: [INJECT] Injection contexte théorique
  - Axiomes Savard injectés
  - Contexte: géométrie spectrale

t=0.025s: [ROUTE] Décision routage
  - Modèle sélectionné: claude
  - Raison: Expert en structures mathématiques
  - Budget: 45.3% utilisé

t=0.030s: [BUDGET_CHECK] Vérification budget
  - Budget mensuel: 500,000 tokens
  - Utilisés: 226,500 tokens
  - Statut: OK (budget restant ample)

t=0.050s: [CACHE] Construction requête avec cache
  - System blocks cachés: 1 (instructions Gabriel)
  - Debug blocks cachés: 0 (pas de debug cette fois)
  - User query (non-cachée): "Explique RSA"

t=0.100s: [ANTHROPIC] Envoi requête à l'API Anthropic
  - Endpoint: https://api.anthropic.com/v1/messages
  - Model: claude-sonnet-4-5-20250929
  - Max tokens: 1500

t=0.150s: [CACHE_HIT] Cache des instructions réutilisé!
  - Cache creation tokens: 0 (réutilisé du cache)
  - Cache read tokens: 450 (instructions lues du cache)
  - Économie: 450 * 0.9 = 405 tokens économisés!

t=0.200s: [GENERATION] Claude génère la réponse
  - Tokens générés: 120
  - Status: COMPLETE

t=0.250s: [RESPONSE] Réponse reçue de Anthropic
  - Contenu: "RSA est un rapport spectral asymétrique..."
  - Tokens totaux utilisés: 120 (output) + 51 (input avec cache)
  - Vrai coût: ~50% du normal grâce au cache!

t=0.300s: [BUDGET_UPDATE] Mise à jour du budget
  - Tokens utilisés: 171 (au lieu de ~600 sans cache)
  - Budget restant: 226,329 tokens
  - Économie totale: 429 tokens!

t=0.310s: [SUCCESS] Requête complète avec succès
  - Durée: 310ms
  - Cache économies: 90% sur bloc système
  - Statut: READY pour prochaine requête
"""
    
    # Question debug 1
    print("\n[DEBUG 1] Première question sur la timeline")
    result1 = gabriel.query_debug_timeline(
        question="Pourquoi le cache hit s'est produit à t=0.150s?",
        timeline_context=timeline_context,
        timeline_id="timeline-debug-001"
    )
    
    if result1.get('response'):
        print(f"✓ Réponse debug 1: {result1['response'][:150]}...")
        print(f"  Tokens utilisés: {result1['tokens']['total']}")
        print(f"  Cache lus: {result1['tokens'].get('cache_read', 0)} tokens")
    
    # Question debug 2 - réutilise le cache
    print("\n[DEBUG 2] Deuxième question (réutilise cache timeline)")
    result2 = gabriel.query_debug_timeline(
        question="Comment Gabriel a économisé 429 tokens?",
        timeline_context=timeline_context,
        timeline_id="timeline-debug-001"  # Même timeline ID = cache réutilisé
    )
    
    if result2.get('response'):
        print(f"✓ Réponse debug 2: {result2['response'][:150]}...")
        print(f"  Tokens utilisés: {result2['tokens']['total']}")
        print(f"  Cache lus: {result2['tokens'].get('cache_read', 0)} tokens")
        print(f"  🔄 ECONOMIES: {result2['cache']['savings']['tokens_saved']} tokens!")


def example_direct_cache_manager():
    """Exemple 3: Utilisation directe du PromptCacheManager"""
    print("\n" + "="*70)
    print("EXEMPLE 3: UTILISATION DIRECTE DU PROMPT CACHE MANAGER")
    print("="*70)
    
    cache_mgr = PromptCacheManager(debug_mode=True)
    
    # Instructions Gabriel
    gabriel_instructions = """Tu es Gabriel, assistant mathématique multiloop expert.

EXPERTISE:
- Théorie "L'univers est au carré" (Philippe Thomas Savard)
- Géométrie spectrale asymétrique des nombres premiers
- Analyse RSA (Rapport Spectral Asymétrique Ordonné)
- Preuves formelles en HOL4/Lean4
- Validation structures mathématiques rigoureuses

DIRECTIVES:
1. Réponses COURTES et DIRECTES (≤150 mots)
2. Économiser tokens (prompt caching activé)
3. Structure logique claire
4. Pas de verbosité inutile"""
    
    # Enregistrer cache système
    print("\n[1] Enregistrement instructions Gabriel en cache")
    system_key = cache_mgr.register_system_cache(gabriel_instructions)
    print(f"✓ Clé cache système: {system_key}")
    
    # Réutiliser le cache
    print("\n[2] Réutilisation du cache (hit)")
    system_key2 = cache_mgr.register_system_cache(gabriel_instructions)
    print(f"✓ Cache hit! Même clé: {system_key2}")
    
    # Construire requête avec cache
    print("\n[3] Construction requête Anthropic avec cache")
    request = cache_mgr.build_anthropic_request_with_cache(
        instructions=gabriel_instructions,
        user_query="Explique RSA brièvement"
    )
    
    print(f"✓ Requête construite:")
    print(f"  - System blocks: {request['cache_info']['system_cached']}")
    print(f"  - Messages: {len(request['messages'])}")
    print(f"  - Cache enabled: Yes")
    
    # Estimer économies
    print("\n[4] Estimation d'économies")
    savings = cache_mgr.estimate_token_savings(
        system_tokens=len(gabriel_instructions.split()),
        debug_tokens=0
    )
    
    for key, value in savings.items():
        print(f"  {key}: {value}")
    
    # Statistiques
    print("\n[5] Statistiques du cache")
    cache_mgr.print_cache_stats()


def main():
    """Lance tous les exemples"""
    
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  GUIDE D'IMPLÉMENTATION - PROMPT CACHING POUR GABRIEL".center(68) + "█")
    print("█" + "  Économiser jusqu'à 90% de tokens!".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    try:
        # Exemple 1: Caching basique
        example_basic_cache()
        
        # Exemple 2: Debug timeline
        example_debug_timeline()
        
        # Exemple 3: Direct cache manager
        example_direct_cache_manager()
        
    except Exception as e:
        logger.error(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Résumé final
    print("\n" + "="*70)
    print("RÉSUMÉ - IMPLÉMENTATION PROMPT CACHING")
    print("="*70)
    print("""
✓ Caching activé automatiquement pour Gabriel
✓ Instructions système cachées = ~90% d'économie après 2ème requête
✓ Debug timeline cachée = économies massives pour sessions debugging
✓ Budget mensuel 7$ = ~1000 requêtes (vs ~110 sans cache!)

POINTS-CLÉS:
1. Cache éphémère = disponible 5 minutes dans la session
2. 90% d'économie sur tokens cachés après réutilisation
3. Support multi-blocs: système + debug context
4. Intégration transparente dans gabriel_llm_integration_cache.py

FICHIERS CRÉÉS:
- src/prompt_cache_manager.py (gestion cache)
- src/gabriel_llm_integration_cache.py (Gabriel avec cache)
- src/llm_router_cache_extension.py (extension LLMRouter)
- examples/example_prompt_caching.py (ce fichier)

PROCHAINES ÉTAPES:
1. Importer: from src.gabriel_llm_integration_cache import GabrielLLMIntegrationSafeBudgetWithCache
2. Utiliser: gabriel = GabrielLLMIntegrationSafeBudgetWithCache(enable_cache=True)
3. Requête: result = gabriel.query_intelligent("question", debug_context="timeline...")
4. Résultat: Économies de tokens affichées dans result['cache']['savings']
    """)
    
    return 0


if __name__ == '__main__':
    exit(main())
