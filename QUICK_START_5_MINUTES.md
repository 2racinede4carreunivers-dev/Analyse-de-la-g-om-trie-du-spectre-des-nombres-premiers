# 🚀 DÉMARRAGE RAPIDE: ANALYSER UNE IMAGE

**Durée totale: 5 minutes**

---

## ✅ Étape 1: Vérifier que le système fonctionne (2 min)

Ouvrez Python et testez:

```python
from src.complete_vision_system import analyze_image_complete

result = analyze_image_complete(
    r"C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png"
)
print(f"✓ Formes: {result.geometric_shapes}")
print(f"✓ Points: {result.geometric_points}")
print(f"✓ Graphiques: {result.graphs_detected}")
```

**Résultat attendu:** Affiche des nombres > 0

Si ça marche → Passez à l'étape 2 ✓

---

## 🔧 Étape 2: Intégrer dans le CLI (2 min)

### 2a. Ouvrir le fichier
```
src/ui/cli.py
```

### 2b. Chercher (Ctrl+F)
```
if cmd.lower().startswith("cognitive"):
```

### 2c. Ajouter juste AVANT `return False` (dans la même fonction):
```python
        if cmd.lower().startswith(('analyse image', 'valide', 'examine', 'scan')):
            return self._handle_image_analysis(cmd)
```

### 2d. Ajouter cette nouvelle méthode (fin de la classe CLIInterface):
```python
    def _handle_image_analysis(self, cmd: str) -> bool:
        try:
            from src.gabriel_image_interface import gabriel_analyze_image
            result = gabriel_analyze_image(cmd)
            console.print(result)
        except Exception as e:
            console.print(f"[red]Erreur: {e}[/red]")
        return True
```

### 2e. Sauvegarder

---

## ▶️ Étape 3: Redémarrer Gabriel (1 min)

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
python main_cli.py
```

---

## 🎉 Étape 4: Utiliser! (30 sec)

Dans Gabriel:

```
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

**Attendu:**
```
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE VISION COMPLÈTE - GABRIEL SYSTEM              │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: C:\theorie-mathematique\src\tex\tex-2\...
   Succès: ✓ Oui
   Durée: 1234ms

🎯 CAPACITÉS UTILISÉES (5)
   ✓ GEOMETRIC
   ✓ TABLES
   ✓ GRAPHS
   ✓ DIAGRAMS
   ✓ GRIDS

📊 DÉTECTIONS
   Formes: 12
   Points: 45
   Lignes: 8
   ...
```

---

## 🧪 Tester d'autres commandes

```
gabriel> valide C:\path\figure.png

gabriel> examine C:\path\schema.png pour des rayons

gabriel> scan C:\path\matrice.png et extrait

gabriel> aide
  → Voir la nouvelle section "VISION & ANALYSE D'IMAGES"
```

---

## 📋 Checklist

- [ ] Test Python (Étape 1) ✓
- [ ] Modifications dans src/ui/cli.py (Étape 2) ✓
- [ ] Redémarrage Gabriel (Étape 3) ✓
- [ ] Test premier analyse (Étape 4) ✓
- [ ] Essai d'autres commandes (Étape 4)

---

## 🆘 Dépannage

**Erreur: "Module vision non disponible"**
- Vérifiez l'import dans `_handle_image_analysis`

**Erreur: "Fichier non trouvé"**
- Vérifiez le chemin: `C:\chemin\vers\image.png`

**Pas de résultats**
- Assurez-vous que le format est `.png`, `.jpg` ou `.bmp`

**Toujours `return False` après taper la commande**
- Vérifiez que vous avez bien retourné `True` dans `_handle_image_analysis()`

---

## 🎯 Prochaines Étapes

Après validation, vous pouvez:

1. **Analyser vos images réelles**
   ```
   gabriel> analyse image C:\mes-figures\figure-1.png
   ```

2. **Valider des propriétés**
   ```
   gabriel> valide C:\mes-figures\triangle.png - équilatéral, régulier
   ```

3. **Extraire des données**
   ```
   gabriel> scan C:\data\matrice-spectrale.png et extrait
   ```

4. **Générer du code**
   → Le code Python/LaTeX/HOL est inclus dans la sortie!

---

## 📞 Support

- **Documentation complète:** `GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md`
- **Réponse directe:** `IMAGE_ANALYSIS_ANSWER_DIRECT.md`
- **Code prêt:** `COPIER_COLLER_DIRECT.py`

---

**C'est tout! Vous êtes maintenant équipé pour analyser vos images avec Gabriel! 🎉**
