#!/usr/bin/env python3
"""
GABRIEL v6.0 - QUICK START
Claude PRIORITAIRE + Effort Cognitif
Déploiement immédiat
"""

import sys
from pathlib import Path

# Setup
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Deploy Gabriel v6.0"""
    
    print("\n" + "="*70)
    print("GABRIEL v6.0 - DEPLOYMENT RAPIDE")
    print("="*70)
    
    print("\n[STEP 1] Vérifier .env")
    print("─" * 70)
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    claude_key = os.getenv('CLAUDE_API_KEY')
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if claude_key:
        print(f"  ✅ CLAUDE_API_KEY trouvée (sk-ant-{claude_key[-8:]}...)")
    else:
        print(f"  ❌ CLAUDE_API_KEY manquante")
        print("\n   Action: Ajouter à .env:")
        print("   CLAUDE_API_KEY=sk-ant-xxxxx")
        return False
    
    if openai_key:
        print(f"  ✅ OPENAI_API_KEY trouvée (sk-{openai_key[-8:]}...)")
    else:
        print(f"  ⚠️ OPENAI_API_KEY optionnelle (fallback seulement)")
    
    print("\n[STEP 2] Initialiser Gabriel v6.0")
    print("─" * 70)
    
    try:
        from src.gabriel_llm_integration_v2 import GabrielLLMIntegrationV2
        
        gabriel = GabrielLLMIntegrationV2()
        print("  ✅ Gabriel initialized")
        print("     - Claude: PRIORITAIRE")
        print("     - OpenAI: Fallback")
        print("     - Ollama: DISABLED")
        print("     - Split: 75/25 available")
    
    except Exception as e:
        print(f"  ❌ Initialization failed: {e}")
        return False
    
    print("\n[STEP 3] Test requête difficile")
    print("─" * 70)
    
    try:
        print("  🔄 Requête: 'Analyse RSA et convergence'")
        result = gabriel.query_intelligent(
            "Analyse la convergence du rapport spectral asymétrique vers 0.5"
        )
        
        if result.get('response'):
            print(f"  ✅ Réponse obtenue")
            print(f"     - Model: {result['model'].upper()}")
            print(f"     - Effort: {result['cognitive_effort']}")
            print(f"     - Tokens: {result['tokens']}")
            print(f"     - Réponse: {result['response'][:100]}...")
        else:
            print(f"  ❌ Erreur: {result.get('error')}")
            return False
    
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        return False
    
    print("\n[STEP 4] Afficher statistiques")
    print("─" * 70)
    
    gabriel.print_routing_stats()
    
    print("\n[STEP 5] Architecture Final")
    print("─" * 70)
    
    print("""
    FLUX AUTOMATIQUE:
    
    Query → [Classify] → [Analyze Effort]
                              ↓
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
                 LOW      MEDIUM      HIGH
                    ↓         ↓         ↓
                 OpenAI    SPLIT     Claude
                          75/25
    
    PRIORITÉ:
    1️⃣ Claude (tâches logiques)
    2️⃣ OpenAI (tâches simples)
    3️⃣ SPLIT (effort mixte)
    
    OLLAMA: DÉSACTIVÉ ❌
    """)
    
    print("\n[SUCCÈS] Gabriel v6.0 est opérationnel!")
    print("="*70)
    
    print("""
    UTILISATION:
    
    from src.gabriel_llm_integration_v2 import GabrielLLMIntegrationV2
    
    gabriel = GabrielLLMIntegrationV2()
    result = gabriel.query_intelligent("Analyse RSA")
    print(result['response'])
    
    """)
    
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        sys.exit(1)
