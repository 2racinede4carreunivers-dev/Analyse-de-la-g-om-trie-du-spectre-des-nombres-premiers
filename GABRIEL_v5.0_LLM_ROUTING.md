# 🧠 GABRIEL v5.0 - ROUTAGE INTELLIGENT LLM (Claude → OpenAI)

## ✨ CAPACITÉ STRATÉGIQUE AJOUTÉE

Un **système de routage intelligent** qui:
- ✅ **Claude prioritaire** - "Cerveau logique" pour mathématiques rigoreuses
- ✅ **OpenAI fallback** - Tâches fluides et génération rapide
- ✅ **Détection automatique** - Classe les tâches optimalement
- ✅ **Gestion rate limits** - Bascule auto en cas de limitation
- ✅ **Validation conformité** - Réponses adaptées théorie Savard

---

## 🎯 ARCHITECTURE DÉCISIONS

### Claude-3-5-Sonnet: Cerveau Logique (Prioritaire)

**Excelle dans**:
- 🧮 Raisonnement mathématique rigoureux
- 📝 Validation code HOL4/Lean4
- 🏛️ Génération preuves formelles
- 🔗 Structures logiques complexes
- 🌀 Analyse géométrie spectrale Savard
- ✓ **Tâches**: MATHEMATICAL_REASONING, CODE_VALIDATION, HOL_PROOF_GENERATION, LOGICAL_STRUCTURE, RIEMANN_ANALYSIS, FORMAL_VERIFICATION

**Modèle**: `claude-3-5-sonnet-20241022`
**Rate limit**: 3500 RPM / 90000 TPM
**Température**: 0.7 (équilibre créativité/rigueur)

### GPT-4o: Tâches Fluides (Fallback)

**Excelle dans**:
- 📄 Génération contenu fluide
- 💻 Web scripting rapide
- ⚡ Optimisation textuelle
- 🎨 Descriptions éloquentes
- **Tâches**: CONTENT_GENERATION, WEB_SCRIPTING, QUICK_OPTIMIZATION, TEXT_FLUENCY

**Modèle**: `gpt-4o`
**Rate limit**: 10000 RPM / 2000000 TPM
**Température**: 0.7 (expressivité naturelle)

---

## 📦 MODULES CRÉÉS

### 1. **`src/llm_router.py`** (15.8 KB)

Routeur principal:

```python
from src.llm_router import LLMRouter, TaskType

router = LLMRouter()

# Classification auto
task = router.classify_task("Explique RSA")  
# → TaskType.RIEMANN_ANALYSIS

# Décision routage
decision = router.decide_model(task)
# → RoutingDecision(selected='claude', reason='Expert...')

# Requête avec fallback auto
response, metadata = router.query(
    prompt="Ma requête",
    task_type=task
)
# Claude OU OpenAI selon situation + rate limits
```

**Capacités**:
- ✓ Classification 8 types tâches
- ✓ Détection rate limits
- ✓ Fallback automatique
- ✓ Tracking usage
- ✓ Support API Claude + OpenAI

### 2. **`src/gabriel_llm_integration.py`** (8.5 KB)

Intégration Gabriel:

```python
from src.gabriel_llm_integration import GabrielLLMIntegration

gabriel = GabrielLLMIntegration()

# Requête intelligente complète
result = gabriel.query_intelligent(
    question="Analyse la géométrie du spectre",
    use_theory_context=True,     # Injecte axiomes Savard
    validate_response=True        # Vérifie conformité
)

# Retourne:
# {
#   'response': str,
#   'model': 'claude' ou 'openai',
#   'task_type': 'riemann_analysis',
#   'routing_decision': {...},
#   'validation': {...},
#   'tokens_used': int
# }
```

**Intégration**:
- ✓ Injection axiomes théorie Savard
- ✓ Validation conformité auto
- ✓ System prompts adaptés par tâche
- ✓ Correction réponses non-conformes
- ✓ Statistiques routage

---

## 🔄 FLUX ROUTAGE COMPLET

```
REQUÊTE UTILISATEUR
    ↓
[1] Classification automatique
    → "Explique RSA" → TaskType.RIEMANN_ANALYSIS
    
    ↓
[2] Injection contexte (optionnel)
    → Axiomes théorie Savard injectés
    → Sr2=1.5, RSA formules, etc.
    
    ↓
[3] Décision routage
    → TaskType.RIEMANN_ANALYSIS → Claude
    → Vérifier rate limits
    → Si Claude saturé → OpenAI fallback
    
    ↓
[4] Requête LLM
    → Claude-3-5-Sonnet (prioritaire)
    ↓ (si timeout/rate-limit)
    → GPT-4o (fallback)
    
    ↓
[5] Validation (optionnel)
    → Vérifier conformité axiomes Savard
    → Corriger si nécessaire
    
    ↓
RÉPONSE FINALE (fiable, conforme, optimal)
```

---

## 📊 CLASSIFICATION TÂCHES AUTOMATIQUES

| Requête contient | Task Type | Modèle | Raison |
|-----------------|-----------|--------|--------|
| "math", "équation", "théorème" | MATHEMATICAL_REASONING | Claude | Expert raisonnement |
| "hol4", "isabelle", "proof" | HOL_PROOF_GENERATION | Claude | Spécialiste preuves |
| "RSA", "spectre", "riemann" | RIEMANN_ANALYSIS | Claude | Géométrie spectrale |
| "web", "javascript", "html" | WEB_SCRIPTING | OpenAI | Scripting rapide |
| "article", "contenu", "description" | CONTENT_GENERATION | OpenAI | Fluidité textuelle |
| Autre | GENERAL | Claude | Défaut prioritaire |

**Détection automatique** - pas besoin spécifier!

---

## ⚡ RATE LIMIT MANAGEMENT

```
[Requête normale]
    ↓
Claude (90% limit not reached)
    → Envoyer
    
[Après 3500 requêtes/minute Claude]
    ↓
Claude (90% limit reached)
    → Détecté automatiquement
    → Basculer à OpenAI
    → Continuer sans interruption
    
[Après 60 secondes]
    ↓
Compteur réinitialisé
    → Rebasculer à Claude prioritaire
```

**Avantage**: Aucune interruption calculs même si Claude surchargé!

---

## 💻 UTILISATION

### Mode 1: Simple query

```python
from src.llm_router import LLMRouter

router = LLMRouter()
response, metadata = router.query("Ma requête math")
print(response)
```

### Mode 2: Avec classification

```python
from src.llm_router import LLMRouter, TaskType

router = LLMRouter()

task = router.classify_task("Analyse RSA")
response, metadata = router.query(
    "Ma requête",
    task_type=task
)
print(f"Modèle: {metadata['model']}")
```

### Mode 3: Gabriel intégration (recommended)

```python
from src.gabriel_llm_integration import GabrielLLMIntegration

gabriel = GabrielLLMIntegration()

# Requête complète avec contexte + validation
result = gabriel.query_intelligent(
    "Explique la géométrie du spectre",
    use_theory_context=True,  # Injecte axiomes
    validate_response=True     # Vérifie conformité
)

print(result['response'])
print(f"Modèle: {result['model']}")
print(f"Validation: {result['validation']}")
```

---

## 📋 CONFIGURATION .env

```bash
# CLAUDE (Prioritaire)
CLAUDE_API_KEY=sk-ant-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx

# OPENAI (Fallback)
OPENAI_API_KEY=sk-xxxxx

# Routage
LLM_PRIMARY_MODEL=claude
LLM_FALLBACK_MODEL=openai
LLM_ENABLE_ROUTING=true
LLM_RATE_LIMIT_TRACKING=true
```

---

## 📈 STATISTIQUES ROUTAGE

```python
# Voir rapport complet
stats = router.get_routing_stats()

print(f"Claude requests: {stats['claude_requests']}")
print(f"OpenAI requests: {stats['openai_requests']}")
print(f"Claude percentage: {stats['claude_percentage']:.1f}%")
print(f"Claude tokens: {stats['claude_tokens']}")
print(f"OpenAI tokens: {stats['openai_tokens']}")
```

**Attendu pour mathématiques**:
- ✓ Claude: ~85-90% requêtes (priorité mathématique)
- ✓ OpenAI: ~10-15% requêtes (fallback + contenu)

---

## ✅ INTÉGRATION GABRIEL COMPLÈTE

En `gabriel_mathematical.py`:

```python
from src.gabriel_llm_integration import GabrielLLMIntegration

class GabrielMathematicalAssistant:
    def __init__(self):
        self.llm = GabrielLLMIntegration()
    
    def process_query(self, query):
        # Requête intelligente avec routage
        result = self.llm.query_intelligent(
            question=query,
            use_theory_context=True,
            validate_response=True
        )
        
        return result['response']
```

---

## 🎯 RÉSULTATS ATTENDUS

### Requête mathématique:
```
Input: "Analyse la convergence RSA vers 0.5"
→ Classification: RIEMANN_ANALYSIS
→ Routage: Claude-3-5-Sonnet (expert)
→ Response: Explication rigoureuse avec formules
→ Validation: Conforme axiomes Savard ✓
```

### Requête contenu:
```
Input: "Écris description YouTube sur géométrie spectrale"
→ Classification: CONTENT_GENERATION
→ Routage: GPT-4o (fluidité)
→ Response: Description éloquente et engageante
→ Validation: Texte fluide ✓
```

### Rate limit:
```
Claude atteint 90% RPM
→ Automatically fallback à OpenAI
→ Requête suivante: OpenAI
→ 60 sec après: Rebasculer Claude
→ Aucune interruption utilisateur ✓
```

---

## ✅ CHECKLIST v5.0

- [x] LLM Router implémenté (Claude + OpenAI)
- [x] Classification automatique 8 types tâches
- [x] Gestion rate limits avec fallback
- [x] Gabriel integration complète
- [x] Injection axiomes Savard
- [x] Validation conformité réponses
- [x] .env.example mise à jour
- [x] Statistiques routage
- [x] System prompts adaptés par tâche

---

## 🚀 ACTIVATION

### Step 1: Ajouter clés .env

```bash
CLAUDE_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
```

### Step 2: Utiliser dans Gabriel

```python
from src.gabriel_llm_integration import GabrielLLMIntegration

gabriel = GabrielLLMIntegration()
result = gabriel.query_intelligent("Requête math")
```

### Step 3: Monitorer

```python
gabriel.print_routing_stats()
# Voir Claude vs OpenAI usage
```

---

## 📊 STATUS v5.0

```
Gabriel v5.0 - Intelligent LLM Routing
✅ Claude-3-5-Sonnet prioritaire (mathématiques)
✅ GPT-4o fallback (tâches fluides)
✅ Classification automatique
✅ Rate limit management
✅ Théorie Savard intégrée
✅ Validation conformité
✅ Statistiques tracking

Status: ✅ PRODUCTION READY
```

---

**Gabriel v5.0 - Intelligent LLM Routing**
**Date**: 2024
**Status**: ✅ Production Ready

Claude gère les mathématiques, OpenAI prend le relais. Optimal! 🧠⚡
