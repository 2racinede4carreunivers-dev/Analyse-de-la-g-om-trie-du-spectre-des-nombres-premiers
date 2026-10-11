# GABRIEL v6.0 - QUICK REFERENCE

## 🎯 TL;DR

**Problème**: Claude API jamais utilisée (même si clé dans .env), Ollama timeout constant, OpenAI par défaut (pas optimal pour logique)

**Solution**: 
- Ollama DÉSACTIVÉ ❌
- Claude PRIORITAIRE automatiquement ✅
- Effort cognitif ANALYSÉ ✅
- OpenAI pour tâches simples ✅
- SPLIT 75/25 pour mixte ✅

---

## 🚀 DÉMARRAGE RAPIDE

### 1. Mettre à jour .env
```bash
CLAUDE_API_KEY=sk-ant-xxxxx     # OBLIGATOIRE
OPENAI_API_KEY=sk-xxxxx        # OPTIONNEL
```

### 2. Importer Gabriel v6.0
```python
from src.gabriel_llm_integration_v2 import GabrielLLMIntegrationV2

gabriel = GabrielLLMIntegrationV2()
```

### 3. Utiliser
```python
# Tâche logique → Claude automatiquement
result = gabriel.query_intelligent("Analyse RSA")
print(result['model'])  # 'claude'

# Tâche simple → OpenAI
result = gabriel.query_intelligent("Écris texte")
print(result['model'])  # 'openai'

# Tâche mixte → SPLIT
result = gabriel.query_intelligent("Analyse et explique")
print(result['model'])  # 'split'
```

---

## 📊 TABLE ROUTAGE

| Query | Effort | Model | Raison |
|-------|--------|-------|--------|
| Analyse RSA convergence | VERY_HIGH | Claude | Expertise logique |
| Théorie Isabelle HOL | HIGH | Claude | Preuves formelles |
| Analyse + explique | MEDIUM | SPLIT 75/25 | Mixte |
| Écris article | LOW | OpenAI | Fluidité textuelle |

---

## 🧠 EFFORT COGNITIF

### Mots "DURS" → HIGH/VERY_HIGH → Claude

```
mathématique, riemann, zéro, spectre, rsa,
hol4, isabelle, lean, proof, théorème, preuve,
convergence, géométrie, spectral, axiome
```

### Mots "FACILES" → LOW → OpenAI

```
texte, article, web, javascript, poème,
explication simple, résumé, description
```

---

## 💻 API PRINCIPALE

### Initialize

```python
gabriel = GabrielLLMIntegrationV2(monthly_budget_usd=7.0)
```

### Query

```python
result = gabriel.query_intelligent(
    question="Analyse RSA",
    task_type=None,           # Auto-détecté
    use_theory_context=True,  # Injecte axiomes Savard
    validate_response=True,   # Valide conformité
    force_model=None,         # 'claude', 'openai', 'split', or None
    analyze_split=True        # Détecte auto split 75/25
)

# Métadonnées retournées:
# - response: str (réponse)
# - model: str ('claude', 'openai', 'split')
# - cognitive_effort: str ('low', 'medium', 'high', 'very_high')
# - tokens: int (total)
# - split_info: dict (si split mode)
```

### Stats

```python
gabriel.print_routing_stats()
# Affiche: Total, Claude%, OpenAI%, Split%, tokens
```

---

## 🔄 MODE SPLIT 75/25

**Auto-détecté** quand:
- Effort = MEDIUM
- Query contient 75% mots "durs" + 25% mots "faciles"

**Exemple**:
```
Query: "Analyse mathématiquement la géométrie spectrale
        et explique simplement pour un enfant"
        ↓
Effort: MEDIUM (mix détecté)
        ↓
Split: 75% Claude (analyse math) + 25% OpenAI (simplification)
```

---

## ⚙️ CONFIGURATION

### .env (OBLIGATOIRE)

```bash
CLAUDE_API_KEY=sk-ant-xxxxx
# OPENAI_API_KEY=sk-xxxxx  (optionnel)
```

### Force Model

```python
# Force Claude
gabriel.query_intelligent(query, force_model='claude')

# Force OpenAI
gabriel.query_intelligent(query, force_model='openai')

# Force Split
gabriel.query_intelligent(query, force_model='split')
```

---

## 📈 RÉSULTATS ATTENDUS

### Tâche Math (logique)

```
Input: "Analyse la convergence RSA vers 0.5"
  ↓
Detected Effort: VERY_HIGH
  ↓
Selected Model: Claude ✅
  ↓
Output: [Analyse rigoureuse mathématique]
```

### Tâche Web (simple)

```
Input: "Crée un site avec HTML5"
  ↓
Detected Effort: LOW
  ↓
Selected Model: OpenAI ✅
  ↓
Output: [Code HTML fluide]
```

### Tâche Mixte

```
Input: "Analyse RSA et explique simplement"
  ↓
Detected Effort: MEDIUM (mix)
  ↓
Selected Mode: SPLIT 75% Claude / 25% OpenAI ✅
  ↓
Output: [Analyse math (Claude) + explication simple (OpenAI)]
```

---

## 🧪 TESTS

### Test rapide

```python
gabriel = GabrielLLMIntegrationV2()

# Test 1: Tâche difficile → Claude
r1 = gabriel.query_intelligent("Analyse RSA convergence")
assert r1['model'] == 'claude'

# Test 2: Tâche simple → OpenAI
r2 = gabriel.query_intelligent("Écris article web")
assert r2['model'] == 'openai'

# Test 3: Afficher stats
gabriel.print_routing_stats()

print("✅ All tests passed!")
```

### Test complet

```bash
python deploy_gabriel_v6.py
# Automatise tous les tests + deployment
```

---

## 💰 BUDGET

### Avant (Cassé)

```
OpenAI par défaut pour TOUT
→ $15-20/mois (cher)
→ Qualité math: BASSE
```

### Après (Optimisé)

```
Claude pour logique (~70%)
OpenAI pour simple (~25%)
Split pour mixte (~5%)
→ $6-8/mois (60% économie!)
→ Qualité math: EXCELLENTE
```

---

## 📋 CHECKLIST

- [ ] .env with CLAUDE_API_KEY
- [ ] Import GabrielLLMIntegrationV2
- [ ] Initialize gabriel
- [ ] Test math query → Claude
- [ ] Test simple query → OpenAI
- [ ] Check stats
- [ ] Deploy ✅

---

## 🎯 KEY FEATURES

✅ Claude PRIORITAIRE automatique
✅ Ollama DISABLED (fini les timeouts)
✅ Effort cognitif ANALYSÉ smart
✅ SPLIT 75/25 pour mixte
✅ Fallback automatique
✅ Budget optimisé (-60%)
✅ Qualité mathématique EXCELLENTE

---

## 📞 HELP

| Problem | Solution |
|---------|----------|
| Claude not found? | Add CLAUDE_API_KEY to .env |
| OpenAI not used? | Add OPENAI_API_KEY (optionnel) |
| Rate limit? | Auto fallback, wait 60s |
| Wrong model selected? | Check query keywords |

---

## 🚀 DEPLOY NOW

```bash
python deploy_gabriel_v6.py
```

**That's it! Claude is now primary. Enjoy optimal routing!** 🎊
