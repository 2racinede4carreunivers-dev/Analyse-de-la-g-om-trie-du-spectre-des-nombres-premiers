# GABRIEL + CLINE FUSION - Guide d'Activation
## Option 2: Fusion Hybride (Recommandée)

---

## ✅ Qu'est-ce qui a été fait ?

Trois nouveaux modules ont été créés pour fusionner Gabriel et Cline :

### 1. **cline_tools_bridge.py** (`src/adapters/`)
   - Adapte les outils Cline (file edit, command exec, search)
   - Crée une interface uniforme via `ClineToolDispatcher`
   - **Capacités** :
     - File operations: `read`, `create`, `update`, `delete`
     - Command execution: `run`, `execute`
     - File search: `search`, `grep`, `find`

### 2. **hybrid_dispatcher.py** (`src/adapters/`)
   - Dispatcher unifié **Gabriel + Cline**
   - Détecte automatiquement le type de commande :
     - Commandes Cline → routing vers `ClineToolDispatcher`
     - Requêtes Gabriel → routing vers les modules Gabriel (math, vision, etc.)
     - Autres → LLM routing
   - Support 6 catégories : `CLINE_FILE`, `CLINE_EXEC`, `CLINE_SEARCH`, `GABRIEL_MATH`, `GABRIEL_VISION`, `LLM_ROUTING`

### 3. **cli_cline_extension.py** (`src/ui/`)
   - Extension du CLI Gabriel avec support Cline
   - Intègre les commandes Cline dans la boucle REPL existante
   - Affichage formaté (Rich panels, syntax highlighting)
   - Fonction `integrate_cline_in_cli()` pour patcher dynamiquement le CLI

---

## 🚀 Activation (3 étapes)

### Étape 1: Modifier le fichier CLI principal

Ouvre `src/ui/cli.py` et ajoute ceci **à la fin du fichier** :

```python
# ═══════════════════════════════════════════════════════════════════════════
# CLINE INTEGRATION (Option 2 - Hybrid Fusion)
# ═══════════════════════════════════════════════════════════════════════════
from .cli_cline_extension import integrate_cline_in_cli

# Intégrer l'extension Cline à la classe CLIInterface
# (cet appel doit se faire AVANT qu'une instance soit créée)
integrate_cline_in_cli(CLIInterface)
```

### Étape 2: Tester les modules

Exécute les tests unitaires pour vérifier l'intégration :

```bash
# Terminal PowerShell

# Test 1: Cline bridge
cd C:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local
python src/adapters/cline_tools_bridge.py

# Test 2: Hybrid dispatcher
python src/adapters/hybrid_dispatcher.py

# Test 3: CLI extension
python src/ui/cli_cline_extension.py
```

### Étape 3: Démarrer Gabriel avec Cline activé

```bash
cd C:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local
python main_cli.py
```

Tapez `aide` pour voir les nouvelles commandes Cline 👇

---

## 📝 Commandes Disponibles (après activation)

### **CLINE TOOLS** (Fichiers & Exécution)

```bash
gabriel> read src/ui/cli.py
gabriel> create exemple.txt Bonjour le monde
gabriel> update exemple.txt Contenu modifié
gabriel> delete exemple.txt
gabriel> search *.py in src/
gabriel> run powershell -Command "Get-ChildItem"
gabriel> execute python main_cli.py --help
```

### **GABRIEL NATIVE** (Toujours disponible)

```bash
gabriel> ratio 1/2 spectral
gabriel> analyse image C:\path\image.png
gabriel> validation HOL reconstruct 101
gabriel> cognitive multiloop think about Riemann hypothesis
gabriel> debat --persona=logicien --tours=5 La preuve existe-t-elle?
```

### **LLM ROUTING** (Reste du texte → LLM)

```bash
gabriel> What is the meaning of life?
gabriel> Explain the Riemann hypothesis to a 10-year-old
```

---

## 🔍 Architecture de Fusion

```
USER INPUT
    ↓
HybridDispatcher.dispatch()
    ├─→ Pattern Cline ? (read, run, search...)
    │   └─→ ClineToolDispatcher → File/Command Ops
    │
    ├─→ Pattern Gabriel ? (ratio, image, HOL...)
    │   └─→ Gabriel modules (ratio_dispatcher, vision, etc.)
    │
    └─→ Default
        └─→ LLM Routing
```

---

## ⚙️ Configuration (Optionnel)

Si tu veux personnaliser les patterns reconnus, édite `hybrid_dispatcher.py` :

```python
# Dans la classe HybridDispatcher.__init__()

self.cline_patterns = {
    r"^(read|cat)\s+": CommandCategory.CLINE_FILE,
    # Ajoute tes propres patterns ici
    r"^(my_command)\s+": CommandCategory.CLINE_EXEC,
}
```

---

## 🛠️ Débogage

### Si une commande Cline n'est pas reconnue :

```bash
gabriel> run python -c "from src.adapters.hybrid_dispatcher import HybridDispatcher; print(HybridDispatcher().detect_category('ta_commande'))"
```

### Si le CLI plante lors de l'import :

```bash
cd C:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local
python -c "from src.ui.cli_cline_extension import integrate_cline_in_cli; print('✓ Import OK')"
```

### Activer le logging détaillé :

```python
# Ajoute dans main_cli.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## ✨ Prochaines Étapes (Après Activation)

1. **Valider l'intégration** :
   ```bash
   gabriel> read QUICKSTART.md
   gabriel> aide
   ```

2. **Tester une commande Cline** :
   ```bash
   gabriel> create test_fusion.txt Test Gabriel+Cline
   gabriel> read test_fusion.txt
   gabriel> delete test_fusion.txt
   ```

3. **Combiner Gabriel + Cline** (cas avancé) :
   ```bash
   gabriel> run python -m pytest tests/
   # Puis : gabriel> read test_reports/result.json
   ```

4. **Sauvegarder les modifications** :
   ```bash
   git add src/adapters/cline_tools_bridge.py
   git add src/adapters/hybrid_dispatcher.py
   git add src/ui/cli_cline_extension.py
   git commit -m "feat: Gabriel + Cline hybrid fusion (Option 2)"
   ```

---

## 📂 Fichiers Créés

```
src/
├── adapters/
│   ├── cline_tools_bridge.py        ← NEW (13 KB)
│   └── hybrid_dispatcher.py         ← NEW (11 KB)
└── ui/
    └── cli_cline_extension.py       ← NEW (9 KB)
```

---

## ❓ FAQ

**Q: Est-ce que Gabriel fonctionne toujours seul sans Cline ?**  
R: Oui ! L'extension est optionnelle. Sans l'appel `integrate_cline_in_cli()`, Gabriel fonctionne normalement.

**Q: Puis-je désactiver Cline facilement ?**  
R: Oui, enlève simplement l'import et l'appel `integrate_cline_in_cli()` du `cli.py`.

**Q: Les commandes Cline fonctionnent-elles aussi depuis la ligne de commande ?**  
R: Non, seulement dans la boucle REPL du CLI Gabriel.

**Q: Est-ce que ça ralentit Gabriel ?**  
R: Non, l'overhead est minimal (simples regex patterns).

---

## 🔄 Rollback (Retourner à Gabriel Original)

Si tu veux revenir à Gabriel sans Cline :

```bash
# Supprimer les 3 fichiers d'intégration
rm src/adapters/cline_tools_bridge.py
rm src/adapters/hybrid_dispatcher.py
rm src/ui/cli_cline_extension.py

# Enlever l'import du cli.py
# (reverser à la dernière version sans CLINE INTEGRATION)

# Redémarrer Gabriel
python main_cli.py
```

Ou utilise ta sauvegarde :
```bash
Copy-Item -Path "agent-multiloop-Gabriel-local_BACKUP_20260922_193142" -Destination "agent-multiloop-Gabriel-local-restored" -Recurse
```

---

## 📞 Support

Si tu rencontres des problèmes :

1. Vérife que les 3 fichiers sont bien créés
2. Teste chaque module individuellement (étape 2)
3. Regarde les logs : `logging.DEBUG`
4. Compare avec la sauvegarde si besoin

---

**Fusion réussie ! Gabriel + Cline fusionnés en Option 2 (Hybride). 🎉**
