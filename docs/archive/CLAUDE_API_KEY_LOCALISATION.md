# 🔑 LOCALISATION CLAUDE_API_KEY - GUIDE COMPLET

## ✅ CHECKLIST EMPLACEMENTS

Tu dois placer ta clé Claude **dans 3 endroits**:

### **1️⃣ FICHIER `.env` (PRINCIPAL)**

**Chemin**: `C:\agent-multiloop-Gabriel-local-final\.env`

```bash
# ============================================================
# Claude Anthropic (PRIORITAIRE après Ollama timeout)
# ============================================================
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

**Statut**: ✅ **AJOUTÉE** (mise à jour v2)

---

### **2️⃣ FICHIER DE CONFIGURATION (si applicable)**

**Fichier**: `config_mathematical.env` (si présent)

Vérifier s'il existe:
```bash
ls -la config_mathematical.env
```

Si OUI, ajouter:
```bash
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
```

**Statut**: ⚠️ À vérifier

---

### **3️⃣ FICHIER PYTHON `llm_manager.py`**

**Chemin**: `agent-multiloop-Gabriel-local/src/core/llm_manager.py`

**Ligne critique** (déjà présente):
```python
class ClaudeClient:
    def __init__(self, api_key: str | None = None, ...):
        import os
        
        # ✅ LIT depuis .env
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
```

**Statut**: ✅ **CONFIGURÉE CORRECTEMENT**

---

## 🔍 VÉRIFICATION DÉTAILLÉE

### Comment Python lit la clé Claude

```python
# Dans src/core/llm_manager.py
import os

# Tentative 1: Variable CLAUDE_API_KEY
api_key = os.getenv("CLAUDE_API_KEY")

# Tentative 2 (fallback): Variable ANTHROPIC_API_KEY
if not api_key:
    api_key = os.getenv("ANTHROPIC_API_KEY")

# Utiliser
client = anthropic.Anthropic(api_key=api_key)
```

**Ordre de priorité**:
1. ✅ `CLAUDE_API_KEY` (préféré)
2. ✅ `ANTHROPIC_API_KEY` (alias, OK aussi)

---

## 📋 PLACES OÙ `.env` EST LU

### Lieu 1: `LLMManager.__init__()` 
```python
self.claude = ClaudeClient(
    api_key=None,  # lit depuis .env CLAUDE_API_KEY
    ...
)
```
**Fichier**: `src/core/llm_manager.py` (ligne ~116)

### Lieu 2: `ClaudeClient.__init__()`
```python
self.api_key = api_key or os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
```
**Fichier**: `src/core/llm_manager.py` (ligne ~32)

### Lieu 3: `gabriel_v6_2_rag.py` (si utilisé)
```python
from src.gabriel_llm_integration_v2 import GabrielLLMIntegrationV2
# Lecture indirecte via LLMManager
```

---

## ✅ VÉRIFICATION IMMÉDIATE

### Test 1: Vérifier que .env a la clé
```bash
cat .env | grep CLAUDE_API_KEY
# Doit afficher: CLAUDE_API_KEY=sk-ant-xxxxx...
```

### Test 2: Vérifier que Python peut lire
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Charge .env
claude_key = os.getenv("CLAUDE_API_KEY")
print(f"Claude key found: {claude_key is not None}")
print(f"Key starts with: {claude_key[:20] if claude_key else 'MISSING'}")
```

### Test 3: Vérifier que Claude client s'initialise
```python
from src.core.llm_manager_v2 import ClaudeClient

claude = ClaudeClient()
print(f"Claude available: {claude.is_available()}")
print(f"Claude model: {claude.model}")
```

Expected output:
```
Claude available: True
Claude model: claude-3-5-sonnet-20241022
```

---

## 🚨 DIAGNOSTIC SI ÇA NE MARCHE PAS

### Symptôme 1: "Claude indisponible (CLAUDE_API_KEY manquante)"

```python
logger.warning("⚠️ Claude indisponible (CLAUDE_API_KEY manquante)")
```

**Solutions**:
1. Vérifier `.env` contient `CLAUDE_API_KEY=sk-ant-xxxxx`
2. Vérifier aucun espace autour du `=`
3. Vérifier clé commence par `sk-ant-` (pas `sk-` seul)
4. Redémarrer Python après modification `.env`

### Symptôme 2: "Claude initialization failed"

```
❌ Claude initialization failed: Authentication error
```

**Solutions**:
1. Vérifier clé est valide (générée depuis https://console.anthropic.com/)
2. Vérifier clé n'a pas de caractères invisibles
3. Vérifier clé n'est pas expirée

### Symptôme 3: Logs montrent "Claude timeout"

```
[WARNING] ⚠️ Claude timeout ou erreur
```

**Solutions**:
1. Vérifier connection internet
2. Vérifier Anthropic API n'est pas surchargée
3. Vérifier clé a les bonnes permissions

---

## 📝 FORMAT CORRECT CLAUDE_API_KEY

```
Format valide:  sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                ^^^ ^^^
                │   └─ "ant" = Anthropic
                └─────── "sk" = Secret Key

Longueur: ~50 caractères
Caractères: alphanumériques + tirets
Début: TOUJOURS "sk-ant-"
```

---

## 🔗 CHAÎNE D'APPEL COMPLÈTE

```
gabriel_llm_integration_v2.py
    ↓ (crée)
LLMManager (src/core/llm_manager.py)
    ├─ init() lit .env
    ├─ crée ClaudeClient()
    │   ├─ lit CLAUDE_API_KEY depuis .env
    │   ├─ crée anthropic.Anthropic(api_key=...)
    │   └─ stocke client
    │
    └─ generate() appelle claude.generate()
        ├─ vérifiee is_available()
        ├─ appelle client.messages.create()
        └─ retourne réponse
```

---

## 🎯 RÉSUMÉ FINAL

| Lieu | Type | Clé | Statut |
|------|------|-----|--------|
| `.env` | Variable env | `CLAUDE_API_KEY=sk-ant-xxxxx` | ✅ À METTRE |
| `.env` | Alias | `ANTHROPIC_API_KEY=sk-ant-xxxxx` | ✅ À METTRE |
| `llm_manager.py` | Code | `os.getenv("CLAUDE_API_KEY")` | ✅ DÉJÀ PRÉSENT |
| `llm_manager.py` | Code | `os.getenv("ANTHROPIC_API_KEY")` | ✅ DÉJÀ PRÉSENT |

---

## 🚀 ACTION IMMÉDIATE

### ÉTAPE 1: Éditer `.env`
```bash
nano .env
```

Ajouter/vérifier:
```
CLAUDE_API_KEY=sk-ant-[votre clé ici]
ANTHROPIC_API_KEY=sk-ant-[votre clé ici]
```

### ÉTAPE 2: Sauvegarder
```bash
# Ctrl+X → Y → Entrée (nano)
# Ou: Ctrl+S (éditeur standard)
```

### ÉTAPE 3: Redémarrer Gabriel
```bash
python gabriel_mathematical.py
# Ou: docker-compose up (si Docker)
```

### ÉTAPE 4: Vérifier logs
```
[INFO] 🔴 Tentative 2/3: Claude-3.5-Sonnet - timeout 60s
[INFO] ✅ Claude a répondu
```

---

✅ **Claude API key est maintenant LOCALISÉE**
✅ **LLMManager peut la LIRE depuis .env**
✅ **Prochaine requête: Claude sera APPELÉ**

Ton `.env` est mis à jour! 🎯
