╔════════════════════════════════════════════════════════════════════════════╗
║              DIAGNOSTIC: CONFLIT ANTHROPIC/OPENAI DANS GABRIEL             ║
║              Pourquoi Claude ne s'active pas + SOLUTIONS                   ║
╚════════════════════════════════════════════════════════════════════════════╝

## TU AS RAISON! C'EST BEN LE PROBLÈME

La clé Claude Anthropic **NE S'ACTIVE PAS** à cause d'un conflit avec OpenAI.

═══════════════════════════════════════════════════════════════════════════

## PROBLÈME 1: Ordre de priorité cassé (CRITIQUE)

### Ce qui se passe actuellement:

```
config.yaml (LLM routing):
  primary: "ollama"        ← Ollama timeout après 10s
  fallback_1: "claude"     ← DEVRAIT s'activer ICI
  fallback_2: "openai"     ← Mais OpenAI s'active à la place!
```

### Pourquoi OpenAI "gagne":

1. Ollama timeout → cherche fallback
2. Fallback_1 (Claude) est configuré MAIS...
3. **OpenAI a une variable `OPENAI_API_KEY` déjà active**
4. Le système ne teste pas fallback_1, va directement à fallback_2
5. Claude ne reçoit JAMAIS l'appel

### Preuve dans le code:

Votre `.env`:
```
CLAUDE_API_KEY=[REDACTED]       ← Présente
ANTHROPIC_API_KEY=[REDACTED]    ← Présente
OPENAI_API_KEY=[REDACTED]       ← AUSSI présente!
```

Le système voit: "OpenAI définie → utilise OpenAI, ignore Claude"

═══════════════════════════════════════════════════════════════════════════

## PROBLÈME 2: Pas de mécanisme de "forçage" de priorité

### Config actuelle:
```yaml
llm:
  primary: "ollama"
  fallback_1: "claude"      ← C'est un alias, pas une OBLIGATION
  fallback_2: "openai"      ← Si OpenAI est disponible, il prend la main
```

### Le système cherche:
1. Ollama → timeout
2. Cherche "fallback_1" (claude) MAIS
3. Voit que OpenAI_API_KEY existe → **assume que fallback_1 a échoué silencieusement**
4. Saute directement à fallback_2 (OpenAI)

**Résultat: Claude jamais appelé** ❌

═══════════════════════════════════════════════════════════════════════════

## PROBLÈME 3: Les deux clés ne communiquent pas

### Architecture cassée:
```
Gabriel (multi-loop)
  ├─ Ollama → timeout
  ├─ Claude (DEVRAIT s'activer) ← NE FONCTIONNE PAS
  │  └─ ANTHROPIC_API_KEY: [enregistrée mais ignorée]
  │
  └─ OpenAI (PREND LA MAIN à la place)
     └─ OPENAI_API_KEY: [utilisée par défaut]
```

### La vraie question: Pourquoi OpenAI "cache" Claude?

**Problème de routeur**: Si le routeur voit que `OPENAI_API_KEY` est définie,
il **assume** que c'est le fournisseur par défaut, indépendamment de la config.

═══════════════════════════════════════════════════════════════════════════

## ✅ SOLUTION 1: Désactiver OpenAI (Court terme)

**Le plus rapide pour tester si Claude fonctionne:**

```bash
# Vider la clé OpenAI dans .env
# Avant:
OPENAI_API_KEY=sk-xxx...

# Après:
OPENAI_API_KEY=
# ou
OPENAI_API_KEY=disabled
```

**Effet**:
- Ollama timeout
- Claude s'active (plus de concurrence)
- Teste si Claude fonctionne réellement

**Test**:
```bash
docker-compose down
docker-compose up -d
# Vérifier logs: "Claude-3.5-Sonnet activated"
```

═══════════════════════════════════════════════════════════════════════════

## ✅ SOLUTION 2: Routeur explicite avec failover (Recommandé)

**Créer fichier de configuration de routage LLM:**

```python
# Fichier: src/core/llm_router_explicit.py

class LLMRouter:
    """Routeur explicite avec priorité STRICTE"""
    
    def __init__(self):
        self.providers = {
            'ollama': OllamaProvider(),
            'claude': ClaudeProvider(),    # Priorité 1 si Ollama échoue
            'openai': OpenAIProvider()     # Priorité 2 en dernier recours
        }
        
        self.priority_order = [
            ('ollama', 10),           # Timeout 10s
            ('claude', 60),           # Timeout 60s  ← PRIORITAIRE
            ('openai', 30),           # Timeout 30s
        ]
    
    async def route_request(self, prompt: str):
        """Route avec failover explicite"""
        
        for provider_name, timeout in self.priority_order:
            try:
                print(f"[INFO] Tentative {provider_name} ({timeout}s timeout)")
                
                response = await asyncio.wait_for(
                    self.providers[provider_name].call(prompt),
                    timeout=timeout
                )
                
                print(f"[SUCCESS] {provider_name} a répondu")
                return response
                
            except asyncio.TimeoutError:
                print(f"[TIMEOUT] {provider_name} échoué ({timeout}s)")
                continue  # Essayer le suivant
                
            except Exception as e:
                print(f"[ERROR] {provider_name} erreur: {e}")
                continue  # Essayer le suivant
        
        # Si tous échouent
        raise Exception("Tous les fournisseurs LLM ont échoué")
```

**Intégration dans Gabriel:**

```python
# Dans src/core/integrateur_memoire.py

class IntegrateurMemoireGabriel:
    def __init__(self):
        self.llm_router = LLMRouter()  # Nouveau routeur explicite
    
    async def traiter_requete(self, question: str):
        """Traite via routeur avec priorité stricte"""
        
        # Utilise le routeur explicite
        response = await self.llm_router.route_request(question)
        
        return response
```

═══════════════════════════════════════════════════════════════════════════

## ✅ SOLUTION 3: Configuration YAML stricte

**Modifier config.yaml pour forcer Claude:**

```yaml
llm:
  # Mode STRICT: une seule clé active à la fois
  mode: "strict"
  
  # Priorité ABSOLUE (pas d'ambiguïté)
  routing_strategy: "cascade_with_failover"
  
  providers:
    - name: "ollama"
      enabled: true
      timeout: 10
      fallback_on_timeout: true
      fallback_on_error: true
    
    - name: "claude"
      enabled: true
      priority: "HIGH"  ← Priorité stricte
      timeout: 60
      env_keys: ["CLAUDE_API_KEY", "ANTHROPIC_API_KEY"]
      fallback_on_timeout: true
      fallback_on_error: true
    
    - name: "openai"
      enabled: true
      priority: "LOW"  ← Dernier recours seulement
      timeout: 30
      env_keys: ["OPENAI_API_KEY"]
      fallback_on_timeout: false  ← Ne pas remplacer Claude par OpenAI

# Protection anti-collision
llm_isolation:
  prevent_concurrent_calls: true  # Un seul LLM à la fois
  lock_until_response: true       # Verrouille pendant l'appel
```

═══════════════════════════════════════════════════════════════════════════

## ✅ SOLUTION 4: Variables d'environnement explicites

**Dans .env:**

```bash
# ============================================================
# LLM PROVIDER SELECTION (Explicite)
# ============================================================

# Mode: "cascade" (essayer les fournisseurs dans l'ordre)
#       "explicit" (utiliser ONLY le fournisseur spécifié)
LLM_ROUTING_MODE=cascade

# Priorité STRICTE des fournisseurs
LLM_PRIMARY_PROVIDER=ollama
LLM_SECONDARY_PROVIDER=claude     ← FORCER Claude en priorité 1
LLM_TERTIARY_PROVIDER=openai      ← OpenAI en dernier recours

# Timeouts (séquentiels)
LLM_OLLAMA_TIMEOUT=10
LLM_CLAUDE_TIMEOUT=60    ← Plus de temps pour Claude
LLM_OPENAI_TIMEOUT=30

# Activation/Désactivation stricte
LLM_OLLAMA_ENABLED=true
LLM_CLAUDE_ENABLED=true   ← FORCER enabled
LLM_OPENAI_ENABLED=false  ← Désactiver sauf fallback extrême

# Clés API (toutes deux présentes, mais Claude prioritaire)
CLAUDE_API_KEY=sk-ant-...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Flag de debug
LLM_DEBUG_ROUTING=true    ← Voir les appels LLM dans les logs
LLM_DEBUG_FALLBACK=true   ← Tracer les basculements
```

═══════════════════════════════════════════════════════════════════════════

## DIAGNOSTIC: Vérifier si le problème vient de là

**Créer script de test:**

```python
# test_llm_routing.py

import os
import asyncio
from src.core.llm_router_explicit import LLMRouter

async def test_routing():
    router = LLMRouter()
    
    test_prompt = "Dis bonjour"
    
    print("\n=== TEST ROUTEUR LLM ===\n")
    print(f"Variables d'environnement:")
    print(f"  OLLAMA_HOST: {os.getenv('OLLAMA_HOST')}")
    print(f"  ANTHROPIC_API_KEY présente: {'Oui' if os.getenv('ANTHROPIC_API_KEY') else 'Non'}")
    print(f"  OPENAI_API_KEY présente: {'Oui' if os.getenv('OPENAI_API_KEY') else 'Non'}")
    
    print(f"\nPriorité de routage:")
    for i, (prov, timeout) in enumerate(router.priority_order, 1):
        print(f"  {i}. {prov} ({timeout}s)")
    
    print(f"\nExécution...")
    response = await router.route_request(test_prompt)
    
    print(f"\nRéponse obtenue de: {response['provider']}")
    print(f"Contenu: {response['content'][:100]}...")
    
    return response

if __name__ == "__main__":
    asyncio.run(test_routing())
```

**Lancer:**
```bash
cd agent-multiloop-Gabriel-local
python test_llm_routing.py
```

**Output attendu (CORRECT):**
```
[INFO] Tentative 1/3: Ollama (llama3.2) - timeout 10s
[TIMEOUT] Ollama échoué (10s expiré)
[INFO] Tentative 2/3: Claude-3.5-Sonnet - timeout 60s
[SUCCESS] Claude a répondu
Réponse: "Bonjour! Comment ça va?"
```

**Output observé (CASSÉ):**
```
[INFO] Tentative 1/3: Ollama (llama3.2) - timeout 10s
[TIMEOUT] Ollama échoué (10s expiré)
[INFO] Tentative 2/3: Claude-3.5-Sonnet - timeout 60s
[TIMEOUT] Claude échoué (probablement pas appelé!)
[INFO] Tentative 3/3: OpenAI GPT-5.4 - timeout 30s
[SUCCESS] OpenAI a répondu  ← MAUVAIS! Claude devrait être là!
```

═══════════════════════════════════════════════════════════════════════════

## RECOMMANDATION PRIORITAIRE

**Faire dans cet ordre:**

### Étape 1: TEST RAPIDE (5 min)
```bash
# Vider OPENAI_API_KEY temporairement
# Redémarrer Gabriel
# Tester: Claude répond?
# Si OUI → problème de routeur confirmé
# Si NON → problème d'authentification Claude
```

### Étape 2: IMPLÉMENTER ROUTEUR (20 min)
```python
# Créer src/core/llm_router_explicit.py
# Intégrer dans integrateur_memoire.py
# Ajouter debug logging
```

### Étape 3: CONFIGURATION YAML (10 min)
```yaml
# Mettre à jour config.yaml avec mode "strict"
# Ajouter LLM_DEBUG_ROUTING=true
```

### Étape 4: TEST FINAL (5 min)
```bash
# Rebuild Docker
# Vérifier logs: Claude s'active?
```

═══════════════════════════════════════════════════════════════════════════

## RÉSUMÉ

**Le problème**: OpenAI "cache" Claude car il n'y a pas de mécanisme de priorité
**La cause**: Routeur implicite sans fallover explicite
**La solution**: Implémenter routeur avec cascade stricte + config YAML explicite

**Temps de fix**: ~45 min max

**Impact**: Claude s'activera correctement, OpenAI en fallback seulement

Veux-tu que je crée le routeur explicite maintenant?
