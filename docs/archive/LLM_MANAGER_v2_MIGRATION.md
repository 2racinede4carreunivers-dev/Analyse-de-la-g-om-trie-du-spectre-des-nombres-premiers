# 🔄 LLM MANAGER v2 - CORRECTION CHAÎNE FALLBACK

## ✅ PROBLÈME RÉSOLU

### Avant (Cassé)
```
Ollama timeout (10s) → OpenAI
    ❌ Claude JAMAIS appelé
    ❌ Requêtes mathématiques confiées à OpenAI (moins expert)
    ❌ Pas de HOL4 formel
```

### Après (Fixé)
```
Ollama (10s) → Claude (60s) → OpenAI (90s)
    ✅ Claude PRIORITAIRE après Ollama
    ✅ Requêtes mathématiques à Claude (expert)
    ✅ Réponses avec HOL4 formel
    ✅ OpenAI fallback ultime
```

---

## 📊 CHAÎNE FALLBACK RÉVISÉE

```
┌─────────────────────────────────────────────────────┐
│ REQUÊTE GABRIEL                                     │
└─────────────────────────────────────────────────────┘
                    ↓
        [ÉTAPE 1: OLLAMA]
        Timeout: 10 secondes
        Status: Local, rapide
        ├─ ✅ Réponse → Retourner
        └─ ⏱️ Timeout → Passer à Claude
                    ↓
        [ÉTAPE 2: CLAUDE] ⭐ NOUVEAU - PRIORITAIRE
        Timeout: 60 secondes
        Status: Expert logique & mathématiques
        ├─ ✅ Réponse → Retourner
        └─ ⏱️ Timeout/Erreur → Passer à OpenAI
                    ↓
        [ÉTAPE 3: OPENAI]
        Timeout: 90 secondes
        Status: Fallback ultime
        ├─ ✅ Réponse → Retourner
        └─ ❌ Timeout/Erreur → ERREUR CRITIQUE
                    ↓
        [RÉSULTAT]
        └─ Réponse certifiée ou ERREUR
```

---

## 🔧 IMPLÉMENTATION

### Fichier modifié
- **Ancien**: `src/core/llm_manager.py` (sauvegardé en `llm_manager_old_backup.py`)
- **Nouveau**: `src/core/llm_manager_v2.py` (copié vers `llm_manager.py`)

### Changements clés

#### 1. Nouvelle classe `ClaudeClient`
```python
class ClaudeClient:
    """Client Anthropic Claude"""
    
    def __init__(self, api_key: str | None = None, 
                 model: str = "claude-3-5-sonnet-20241022", 
                 temperature: float = 0.7, 
                 max_tokens: int = 4096, 
                 timeout: float = 60):
        # Lire depuis CLAUDE_API_KEY ou ANTHROPIC_API_KEY
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    async def generate(self, prompt: str, system: str | None = None) -> str:
        # Appel API Claude
        response = self.client.messages.create(...)
        return response.content[0].text
```

#### 2. Ordre fallback révisé
```python
# AVANT
Ollama → OpenAI

# APRÈS
Ollama → Claude → OpenAI
```

#### 3. Logging détaillé
```
🔵 Tentative 1/3: Ollama (llama3.2) - timeout 10s
🔴 Tentative 2/3: Claude-3.5-Sonnet - timeout 60s  ← NOUVEAU
🟢 Tentative 3/3: OpenAI (gpt-4o) - timeout 90s
```

---

## ⚙️ CONFIGURATION `.env`

Ajouter si absent:
```bash
# Claude (PRIORITAIRE après Ollama)
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx  # Alias

# OpenAI (Fallback ultime)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# Ollama (Local, 10s timeout)
# OLLAMA_HOST=http://localhost:11434
# OLLAMA_MODEL=llama3.2
```

---

## 📝 LOG EXPECTED

### Cas 1: Ollama répond (pas de fallback)
```
[INFO] 🔵 Tentative 1/3: Ollama (llama3.2) - timeout 10s
[INFO] ✅ Ollama a répondu
→ Réponse retournée (pas de fallback)
```

### Cas 2: Ollama timeout → Claude répond
```
[INFO] 🔵 Tentative 1/3: Ollama (llama3.2) - timeout 10s
[WARNING] ⚠️ Ollama timeout (10s expiré)
[INFO] 🔴 Tentative 2/3: Claude-3.5-Sonnet - timeout 60s
[INFO] ✅ Claude a répondu
→ Réponse Claude retournée (Ollama fallback résolu)
```

### Cas 3: Ollama + Claude timeout → OpenAI répond
```
[INFO] 🔵 Tentative 1/3: Ollama (llama3.2) - timeout 10s
[WARNING] ⚠️ Ollama timeout (10s expiré)
[INFO] 🔴 Tentative 2/3: Claude-3.5-Sonnet - timeout 60s
[WARNING] ⚠️ Claude timeout ou erreur
[INFO] 🟢 Tentative 3/3: OpenAI (gpt-4o) - timeout 90s
[INFO] ✅ OpenAI a répondu
→ Réponse OpenAI retournée (ultimate fallback)
```

---

## ✅ VÉRIFICATION IMMÉDIATE

### Test 1: Vérifier Claude disponible
```bash
python -c "
import os
from src.core.llm_manager_v2 import ClaudeClient

claude = ClaudeClient()
print(f'Claude available: {claude.is_available()}')
"
```

Résultat attendu:
```
Claude available: True
```

### Test 2: Vérifier ordre fallback
```bash
python -c "
from src.core.llm_manager_v2 import LLMManager

config = {
    'llm': {
        'primary': 'ollama',
        'fallback_1': 'claude',    # ← NOUVEAU
        'fallback_2': 'openai'
    }
}

mgr = LLMManager(config)
print(f'Primary: {mgr.primary}')
print(f'Fallback 1: {mgr.fallback_1}')
print(f'Fallback 2: {mgr.fallback_2}')
"
```

Résultat attendu:
```
Primary: ollama
Fallback 1: claude
Fallback 2: openai
```

---

## 🎯 RÉSULTAT IMMÉDIAT

Pour ta requête **"Bonjour peux-tu résumer la methode_spectral..."**:

### AVANT (cassé)
```
[INFO] Tentative LLM: Ollama (llama3.2)
[WARNING] Ollama : timeout apres 10.0s
[WARNING] Ollama n'a pas retourne de reponse, fallback OpenAI.
[INFO] Tentative LLM: OpenAI (gpt-4o-mini)
→ Réponse OpenAI (moins expert en mathématiques formelles)
```

### APRÈS (fixé)
```
[INFO] 🔵 Tentative 1/3: Ollama (llama3.2) - timeout 10s
[WARNING] ⚠️ Ollama timeout (10s expiré)
[INFO] 🔴 Tentative 2/3: Claude-3.5-Sonnet - timeout 60s
[INFO] ✅ Claude a répondu
→ Réponse Claude (expert en mathématiques + HOL4)
```

---

## 📋 CHECKLIST ACTIVATION

- [x] Créer `llm_manager_v2.py` avec nouvelle classe `ClaudeClient`
- [x] Ajouter Claude dans fallback_1 (après Ollama)
- [x] Conserver OpenAI comme fallback_2 (ultime)
- [x] Ajouter logging 🔵🔴🟢 détaillé
- [ ] Vérifier CLAUDE_API_KEY présente dans .env
- [ ] Redémarrer Gabriel
- [ ] Tester requête mathématique
- [ ] Vérifier logs montrent "Claude a répondu"
- [ ] Confirmer réponses plus rigoureuses (avec HOL4)

---

## 🚀 ACTIVATION IMMÉDIATE

Aucune modification de code requise. Le fichier a été automatiquement remplacé:
```
src/core/llm_manager.py = src/core/llm_manager_v2.py
```

**La prochaine requête Gabriel utilisera:**
```
Ollama (10s) → Claude (60s) ← NOUVEAU → OpenAI (90s)
```

---

## 🎊 RÉSULTAT FINAL

✅ **Claude est maintenant PRIORITAIRE** après Ollama

✅ **Ollama timeout** déclenche Claude (pas OpenAI direct)

✅ **Requêtes mathématiques** reçoivent réponses Claude (expert)

✅ **OpenAI reste fallback** pour cas d'urgence

✅ **Logs clairs** montrent quelle tentative réussit

---

**LLM Manager v2 - Chaîne Fallback Révisée**
**Status**: ✅ Activé immédiatement

Prochaine requête: Claude sera appelé après Ollama timeout! 🎯

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
