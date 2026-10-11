# 🔧 GUIDE: RECONSTRUIRE/REDÉMARRER GABRIEL AVEC LES NOUVELLES FONCTIONNALITÉS

## ❓ Devez-vous Reconstruire?

**NON!** Vous n'avez besoin que de:
- ✅ Redémarrer Gabriel
- ✅ (Optionnel) Ajouter 2-3 lignes dans le CLI

---

## 🚀 OPTION 1: REDÉMARRAGE SIMPLE (Recommandé)

### Étape 1: Arrêter Gabriel (s'il est en cours d'exécution)

```bash
# Dans le terminal Gabriel:
gabriel> quitter

# Ou fermez simplement la fenêtre
```

### Étape 2: Double-cliquez sur

```
C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\START_GABRIEL.bat
```

### Étape 3: Attendre l'initialisation

```
============================================================
     Gabriel Multi-Loop Mathematical Agent v5.4
============================================================

Demarrage de Gabriel sur port 8080...
Chargement de la Methode Spectrale...
Verification de la suite de tests...
[OK] Initialisation terminée
gabriel> _
```

**C'est tout!** Gabriel redémarre avec:
- ✅ Toutes les nouvelles fonctionnalités
- ✅ Système d'analyse d'images
- ✅ Système de découverte d'images
- ✅ Système de critères avancés

---

## 🔌 OPTION 2: REDÉMARRAGE PAR TERMINAL

### Windows PowerShell

```powershell
cd "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
python main_cli.py
```

### Linux/Mac

```bash
cd ~/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local
python main_cli.py
```

---

## 🛠️ OPTION 3: INTÉGRATION DES NOUVELLES FONCTIONNALITÉS (Optionnel)

Si vous voulez les **commandes dans le CLI** (recommandé), modifiez `src/ui/cli.py`:

### Étape 1: Ouvrir le fichier

```
src/ui/cli.py
```

### Étape 2: Chercher (ligne ~3215)

```python
async def _handle_special(self, cmd: str) -> bool:
    """Gère les commandes spéciales"""
    
    if cmd.lower().startswith("cognitive"):
        return await self._handle_cognitive(cmd)
    
    # ← AJOUTER ICI, AVANT "return False"
    
    return False
```

### Étape 3: Ajouter le code d'intégration

Ajoutez AVANT `return False`:

```python
        # Analyse d'images avec critères avancés (v5.5)
        if cmd.lower().startswith(('analyse image', 'valide', 'examine', 'scan')):
            return self._handle_image_analysis_advanced(cmd)
```

### Étape 4: Ajouter la nouvelle méthode

Cherchez la fin de la classe `CLIInterface` et ajoutez:

```python
    def _handle_image_analysis_advanced(self, cmd: str) -> bool:
        """Analyse d'images avec critères personnalisés"""
        try:
            from src.advanced_analysis_criteria import analyze_with_criteria
            from src.gabriel_image_interface import gabriel_analyze_image
            
            # Essayer d'abord le parser avancé
            try:
                result = analyze_with_criteria(cmd)
                if result.get('success'):
                    console.print(result.get('report', ''))
                    return True
            except Exception as e:
                logger.debug(f"Parser avancé: {e}")
            
            # Fallback au parser simple
            result = gabriel_analyze_image(cmd)
            console.print(result)
            
        except ImportError as e:
            console.print(f"[red]Module non disponible: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
        
        return True
```

### Étape 5: Sauvegarder et redémarrer

Sauvegardez le fichier et redémarrez Gabriel.

---

## ✅ VÉRIFICATION POST-REDÉMARRAGE

### Test 1: Gabriel Démarre Correctement

```bash
C:\> START_GABRIEL.bat

# Attendez 10 secondes
# Vous devriez voir:
#   [OK] Initialisation terminée
#   gabriel> _
```

### Test 2: Commande Simple

```bash
gabriel> aide
# Doit afficher l'aide complète
```

### Test 3: Analyse d'Image Simple

```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
# Doit analyser l'image
```

### Test 4: Analyse avec Critères

```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, precision:haute
# Doit analyser avec critères
```

---

## 🐛 DÉPANNAGE

### Problème: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
# Puis redémarrer Gabriel
```

### Problème: Port 8080 déjà utilisé

**Solution:**
```bash
# Fermer tous les processus Gabriel
taskkill /F /IM python.exe

# Ou changer le port dans main_cli.py
export GABRIEL_HTTP_PORT=8001
python main_cli.py
```

### Problème: "advanced_analysis_criteria not found"

**Solution:**
```bash
# Vérifier que le fichier existe:
ls src/advanced_analysis_criteria.py

# Si absent, copier le fichier créé plus tôt
# Puis redémarrer Gabriel
```

### Problème: Fenêtre ne s'affiche pas

**Solution:**
```bash
# Lancer manuellement depuis PowerShell:
cd "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
python main_cli.py

# Ou utiliser:
python -m src.ui.cli
```

---

## 📊 ÉTAT DU SYSTÈME

### Fichiers Existants ✅
- ✅ `main_cli.py` - Point d'entrée CLI
- ✅ `src/ui/cli.py` - Interface utilisateur
- ✅ `src/complete_vision_system.py` - Vision complète
- ✅ `src/gabriel_image_interface.py` - Interface images
- ✅ `src/image_discovery_system.py` - Découverte images

### Fichiers Créés Aujourd'hui ✅
- ✅ `src/advanced_analysis_criteria.py` - Critères avancés
- ✅ `GUIDE_ANALYSE_AVEC_CRITERES.md` - Guide
- ✅ `COMMANDES_PRATIQUES_ANALYSE.md` - Commandes
- ✅ `GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` - Guide complet

### À Modifier (Optionnel)
- ⏳ `src/ui/cli.py` - Ajouter 2-3 lignes

---

## 🚀 FLUX COMPLET

### Pour Utilisation Immédiate (5 min)

```bash
1. Double-cliquez START_GABRIEL.bat
2. Attendez l'initialisation
3. Tapez une commande
4. C'est prêt!
```

### Pour Intégration Complète (10 min)

```bash
1. Ouvrir src/ui/cli.py
2. Ajouter 2-3 lignes de code
3. Sauvegarder
4. Double-cliquez START_GABRIEL.bat
5. Redémarrer Gabriel
6. Utiliser les commandes avancées
```

---

## 📋 CHECKLIST

- [ ] Gabriel est arrêté (s'il était en cours)
- [ ] Fichiers créés sont présents dans `src/`
- [ ] Double-cliquez `START_GABRIEL.bat`
- [ ] Attendez "Initialisation terminée"
- [ ] Testez une commande simple
- [ ] (Optionnel) Modifiez `src/ui/cli.py`
- [ ] (Optionnel) Redémarrez Gabriel
- [ ] Testez avec critères
- [ ] Vous êtes prêt! 🎉

---

## 💡 VOUS N'AVEZ BESOIN QUE DE:

✅ **Redémarrer Gabriel** - C'est tout pour une utilisation basique!

❌ Vous n'avez **PAS** besoin de:
- Réinstaller Python
- Recréer l'environnement virtuel
- Recompiler le projet
- Modifier les dépendances
- Faire une "clean build"

---

## 🎯 RÉSUMÉ

**Question:** Dois-je reconstruire Gabriel?

**Réponse:** NON! Juste redémarrer.

**Procédure:**
1. Double-cliquez `START_GABRIEL.bat`
2. Attendre l'initialisation
3. Utiliser normalement

**C'est aussi simple que ça!** ✅

---

## 🆘 BESOIN D'AIDE?

Si Gabriel ne démarre pas:

```bash
# Essayer en ligne de commande
cd "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
python main_cli.py

# Si erreur, consulter les logs:
cat logs/agent_cli.log

# Ou en PowerShell:
Get-Content logs/agent_cli.log | Select-Object -Last 50
```

---

## ✨ Résultat Final

Après redémarrage, Gabriel a:
- ✅ Analyse d'images complète
- ✅ Système de découverte d'images
- ✅ Critères personnalisés
- ✅ 3 syntaxes de commande
- ✅ 7 formats d'export
- ✅ Toutes les nouvelles fonctionnalités

**À utiliser avec:**
```bash
gabriel> analyse image C:\path\image.png | geometrie, precision:haute, export:json,python,latex
```

**C'est prêt!** 🚀
