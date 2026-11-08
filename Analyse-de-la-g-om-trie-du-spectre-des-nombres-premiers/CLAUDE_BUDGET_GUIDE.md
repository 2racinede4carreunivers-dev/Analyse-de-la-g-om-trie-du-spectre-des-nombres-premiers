# 💰 CLAUDE API BUDGET GUIDE - Rester dans les 5-10$/mois

## ⚠️ TA SITUATION

- **Clé acquise**: $35 USD
- **Goal**: Utiliser ~$5-10/mois
- **Risque**: Dépassement si Gabriel utilisé intensivement

---

## 🔢 TARIFS CLAUDE-3.5-SONNET (ACTUELS)

```
Input tokens:  $3 par million        ($0.000003 par token)
Output tokens: $15 par million       ($0.000015 par token)
```

### Exemple de coût réaliste:

```
Requête typique:
  Input:  1000 tokens × $0.000003 = $0.003
  Output: 500 tokens × $0.000015 = $0.0075
  TOTAL:  $0.0105 par requête

10 requêtes/jour:
  Daily:   ~$0.10
  Monthly: ~$3 USD ✓ (dans budget)

50 requêtes/jour:
  Daily:   ~$0.50
  Monthly: ~$15 USD ⚠️ (DÉPASSE budget!)
```

---

## 🛡️ STRATÉGIE POUR RESTER DANS BUDGET

### ✅ IMPLÉMENTÉE: Limites dans llm_router.py

```python
# max_tokens réduit de 4096 à 1500
max_tokens: int = 1500

# Budget tracking
monthly_token_budget: int = 500000  # ~$5-7 USD
```

### ✅ IMPLÉMENTÉE: Budget Manager (cost_manager.py)

```python
manager = ClaudeBudgetManager(monthly_budget_usd=7.0)

# Utilisation
manager.record_usage(input_tokens=1000, output_tokens=500)
manager.print_budget_report()
```

---

## 📋 3 NIVEAUX DE GESTION

### NIVEAU 1: AUTOMATIQUE (Actuellement activé)

- ✅ Max 1500 tokens par réponse (vs 4096)
- ✅ Budget mensuel: 500K tokens (~$5-7)
- ✅ Alertes à 80% d'utilisation
- ✅ Fallback automatique à OpenAI si limite

**Résultat**: ~$5-7/mois même usage intensif

### NIVEAU 2: INTELLIGENTE (Router actif)

```
Tâche mathématique → Claude  (plus cher, excellent)
Tâche fluide → OpenAI       (moins cher, ~$0.002/K tokens)

Distribution: 40% Claude + 60% OpenAI
Coût estimé: $3-5/mois
```

### NIVEAU 3: CONSERVATRICE (Mode sûr)

```
Limiter à 5 requêtes/jour max
Utiliser uniquement pour tâches critiques
Réserver OpenAI pour interactif

Coût: < $2/mois (très sûr)
```

---

## 🎯 UTILISATION RECOMMANDÉE

### Pour Gabriel quotidiennement:

```python
from src.cost_manager import ClaudeBudgetManager
from src.gabriel_llm_integration import GabrielLLMIntegration

# Initialiser avec limite
budget_mgr = ClaudeBudgetManager(monthly_budget_usd=7.0)

gabriel = GabrielLLMIntegration()

# Avant chaque requête
if not budget_mgr.check_budget():
    print("Budget atteint pour ce mois - utiliser OpenAI seul")
    # Basculer à OpenAI uniquement

# Après chaque requête
result = gabriel.query_intelligent("Ma question")
budget_mgr.record_usage(
    input_tokens=result['tokens_detail']['input'],
    output_tokens=result['tokens_detail']['output']
)

# Afficher rapport
budget_mgr.print_budget_report()
```

---

## 🚨 ALERTES À MONITORER

### ⚠️ ROUGE (Agir immédiatement):

```
- Utilisation > 100% du budget token
- Coût > 100% du budget USD
- Action: ARRÊTER requêtes Claude, utiliser OpenAI seul
```

### 🟡 ORANGE (Réduire utilisation):

```
- Utilisation > 80% du budget token
- Coût > 80% du budget USD
- Action: Réduire requêtes, favoriser OpenAI
```

### 🟢 VERT (Utilisation normale):

```
- Utilisation < 80%
- Coût < 80%
- Action: Continuer utilisation normale
```

---

## 📊 BUDGET PAR USAGE LEVEL

| Usage | Requêtes/jour | Coût/mois |
|-------|--------------|-----------|
| Léger | 5 | $1-2 |
| Normal | 15 | $3-5 |
| Actif | 30 | $6-8 |
| Intensif | 50+ | $12-15+ ⚠️ |

**Recommandation**: Rester ≤ 15 requêtes/jour = $3-5/mois confortable

---

## ✅ VÉRIFICATIONS MENSUELLES

**1er du mois**: Réinitialiser compteurs

```python
manager._reset_month()
manager.print_budget_report()
```

**Chaque semaine**: Afficher rapport

```python
manager.print_budget_report()
```

**Si alerte**: Réduire utilisation

```
Si > 80%:
  - Réduire requêtes/jour
  - Augmenter usage OpenAI
  - Réserver Claude pour math critique
```

---

## 🔐 PROTECTION CONTRE DÉPASSEMENT

### Automatique (déjà en place):

```python
# Dans llm_router.py
if self._is_rate_limited('claude') or monthly_exceeded:
    selected = 'openai'  # Fallback auto
```

### Manuel (à vérifier):

Aller sur https://console.anthropic.com/usage régulièrement

---

## 📈 PROJECTION RÉALISTE

**Avec configuration actuelle** (1500 max tokens, 500K budget):

```
Cas 1: Gabriel peu utilisé (3 requêtes/jour)
  Monthly: ~$1-2 ✓ très safe

Cas 2: Gabriel utilisé activement (15 requêtes/jour)
  Monthly: ~$4-6 ✓ safe

Cas 3: Gabriel utilisé intensivement (30 requêtes/jour)
  Monthly: ~$7-10 ⚠️ limite

Cas 4: Gabriel utilisé sans limite (100 requêtes/jour)
  Monthly: ~$20-25 ❌ DÉPASSE
```

**Conclusion**: Tant que ≤ 30 requêtes/jour, tu restes confortable dans budget 5-10$

---

## 💡 CONSEILS D'ÉCONOMIE

1. **Utiliser OpenAI pour contenu** (non-math)
   - Économie: 60% du coût

2. **Réduire max_tokens si possible**
   - Actuellement: 1500 tokens
   - Économie additionnelle: 30%

3. **Utiliser Claude seulement pour math critique**
   - Réserver pour: HOL4, preuves, Riemann
   - Utiliser OpenAI pour: descriptions, web, contenu

4. **Monitorer mensuel**
   - Ajuster si approche limite
   - Prévient dépassement

---

## 🎯 RÉSUMÉ

✅ **Automatiquement protégé** contre dépassement
✅ **Budget manager** en place pour monitoring
✅ **Alertes** à 80% utilisation
✅ **Fallback** automatique à OpenAI
✅ **Coût réaliste**: $5-10/mois pour usage normal

**Ton $35 USD**: 3-6 mois d'utilisation normale ✓

---

## 🔧 ACTIVATION

```python
# Importer et initialiser
from src.cost_manager import ClaudeBudgetManager

manager = ClaudeBudgetManager(monthly_budget_usd=7.0)

# Avant requête
if manager.check_budget():
    # Requête OK
    pass

# Après requête
manager.record_usage(input_tokens, output_tokens)

# Rapport
manager.print_budget_report()
```

**Fichiers impliqués**:
- `src/llm_router.py` - Limites tokens implémentées
- `src/cost_manager.py` - Budget tracking
- `src/gabriel_llm_integration.py` - Utiliser cost_manager

---

**Conclusion**: Ton budget de $35 USD devrait te durer 3-6 mois avec utilisation normale. Les limites sont en place, les alertes sont configurées, et le fallback automatique à OpenAI prevent les dépassements.
