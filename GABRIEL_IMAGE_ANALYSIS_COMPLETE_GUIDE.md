# 📸 COMMENT DEMANDER À GABRIEL D'ANALYSER UNE IMAGE

## ✅ Le Système est Déjà Implémenté!

Gabriel **peut déjà** analyser les images grâce à:
- ✓ `complete_vision_system.py` (analyse complète)
- ✓ `production_validation_system.py` (validation paramétrique)
- ✓ `image_access_manager.py` (accès universel)
- ✓ `vision_module.py` et `advanced_vision_module.py` (détections)

---

## 🚀 3 Méthodes pour Analyser une Image

### **Méthode 1: CLI Interactif (Recommandé)**

C'est la **méthode la plus simple** - tapez directement dans Gabriel:

```
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

**Variantes de syntaxe:**
```
analyse image C:\path\image.png
valide C:\path\figure.png
examine C:\path\schema.png
scan C:\path\matrice.png
analyse C:\path\figure.png pour des rayons
```

**Résultat attendu:**
```
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE VISION COMPLÈTE - GABRIEL SYSTEM              │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
   Succès: ✓ Oui
   Durée: 1234ms

🎯 CAPACITÉS UTILISÉES (4)
   ✓ GEOMETRIC
   ✓ TABLES
   ✓ GRAPHS
   ✓ GRIDS

📊 DÉTECTIONS
   Géométrie:
      - Formes: 12
      - Points: 45
      - Lignes: 8
   
   Tables/Matrices:
      - Nombre: 2
      - Dimensions: [5, 3] x [4, 4]
   
   Graphiques:
      - Nombre: 1
      - Axes: 2
      - Points de données: 156
   
   Grilles:
      - Détectées: 1

💾 CODE GÉNÉRÉ
   Python: ✓
   LaTeX: ✓
   HOL: ✓
```

---

### **Méthode 2: API HTTP**

Si Gabriel fonctionne en mode **API**:

```bash
curl -X POST http://localhost:8000/api/v1/image/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "image_path": "C:\\theorie-mathematique\\src\\tex\\tex-2\\quadrature_parabole_zero_critique.png",
    "analysis_type": "complete_vision",
    "criteria": ["rayons", "régulier"]
  }'
```

**Réponse JSON:**
```json
{
  "success": true,
  "image_path": "C:\\...",
  "timestamp": "2026-01-15T14:32:00",
  "detections": {
    "geometric": {
      "shapes": 12,
      "points": 45,
      "lines": 8
    },
    "tables": {
      "count": 2
    },
    "graphs": {
      "count": 1,
      "axes": 2,
      "data_points": 156
    }
  },
  "capabilities_used": ["geometric", "tables", "graphs", "grids"]
}
```

---

### **Méthode 3: Python Directement**

Pour intégration dans scripts:

```python
from src.complete_vision_system import analyze_image_complete

# Analyser une image
result = analyze_image_complete(
    "C:\\theorie-mathematique\\src\\tex\\tex-2\\quadrature_parabole_zero_critique.png"
)

# Accéder aux résultats
print(f"Formes détectées: {result.geometric_shapes}")
print(f"Points: {result.geometric_points}")
print(f"Graphiques: {result.graphs_detected}")

# Récupérer les codes générés
print(f"Code Python:\n{result.python_code}")
print(f"Code LaTeX:\n{result.latex_code}")
print(f"Code HOL:\n{result.hol_code}")

# Export JSON
import json
data = json.loads(result.json_data)
print(json.dumps(data, indent=2))
```

---

## 🎯 Types d'Analyse Automatiquement Détectés

Gabriel détecte automatiquement le **type d'analyse** selon vos mots-clés:

| Mots-clés | Type | Ce qu'il fait |
|-----------|------|--------------|
| `géométr`, `formel`, `figure` | **Géométrie** | Extrait formes, points, lignes, angles |
| `table`, `matric`, `données` | **Table** | OCR, extraction de données |
| `graphique`, `courbe`, `axes` | **Graphique** | Détecte axes, points de données, courbes |
| `diagramm`, `flux`, `connecteur` | **Diagramme** | Boîtes, connecteurs, flux |
| `grille`, `calibrat` | **Grille** | Grilles de calibration |
| `valid`, `vérifie`, `rayon` | **Validation** | Vérifie propriétés contre critères |
| *(par défaut)* | **Complet** | Toutes les analyses simultanément |

---

## 📋 Critères de Validation Disponibles

Spécifiez des critères pour valider:

```
gabriel> analyse C:\path\image.png pour des rayons et symétrie
gabriel> valide C:\path\figure.png - équilatéral, régulier
gabriel> examine C:\path\schema.png vérifie rectangle et diagonales
```

**Critères reconnus:**
- `rayon` / `rayons` → Détecte les rayons
- `symétri` / `symétrie` → Vérifie la symétrie
- `équilateral` → Triangle équilatéral
- `rectangle` → Rectangle régulier
- `cercle` / `circle` → Cercle complet
- `régulier` / `regular` → Polygone régulier
- `diagonal` / `diagonales` → Diagonales
- `distance` → Mesure les distances
- `angle` → Mesure les angles

---

## 🔧 IMPLÉMENTATION: Intégrer dans main_cli.py

Pour que Gabriel réponde dans le CLI, ajoutez cette ligne dans `src/ui/cli.py`:

```python
# Dans la méthode _handle_special() du CLIInterface:

def _handle_special(self, cmd: str) -> bool:
    """Gère les commandes spéciales"""
    
    # ... (autres commandes) ...
    
    # NOUVELLE: Analyse d'images
    if cmd.lower().startswith(('analyse image', 'valide', 'examine', 'scan')):
        return self._handle_image_analysis(cmd)
    
    # ... (suite) ...

def _handle_image_analysis(self, cmd: str) -> bool:
    """Commande analyse d'images"""
    from src.gabriel_image_interface import gabriel_analyze_image
    
    try:
        result = gabriel_analyze_image(cmd)
        console.print(result)
        return True
    except Exception as e:
        console.print(f"[red]Erreur analyse image: {e}[/red]")
        return True
```

**Localisation dans le fichier:**
- Cherchez: `async def _handle_special(self, cmd: str) -> bool:`
- Ligne ~3200 environ
- Ajoutez le code avant le `return False` final

---

## 💡 Exemples Concrets

### Exemple 1: Quadrature de la Parabole
```
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

**Analyse automatique:**
- Détecte la parabole (courbe)
- Détecte les axes x,y
- Détecte les points critiques
- Extrait les données numériques
- Génère du code LaTeX/Python/HOL

### Exemple 2: Validation de Figure
```
gabriel> valide C:\figures\triangle.png pour équilatéral et symétrie
```

**Validation:**
- Mesure les 3 côtés
- Vérifie qu'ils sont égaux (tolérance)
- Vérifie la symétrie axiale
- Retourne score de conformité

### Exemple 3: Extraction de Matrice
```
gabriel> scan C:\data\matrice_spectrale.png et extrait
```

**Extraction:**
- Détecte la table
- OCR des nombres
- Exporte en JSON/CSV
- Génère code Python

---

## 🔍 Flux d'Exécution Complet

```
User: "analyse image C:\path\image.png"
         ↓
CLI détecte pattern "analyse image"
         ↓
gabriel_image_interface.process_image_request()
         ↓
1. Extraire le chemin: C:\path\image.png
2. Vérifier accès au fichier
3. Détecter le type d'analyse (complet par défaut)
4. Extraire les critères (aucun par défaut)
5. complete_vision_system.analyze_image_complete()
         ↓
6. Analyses parallèles:
   - Vision géométrique
   - Tables/matrices
   - Graphiques/axes
   - Diagrammes
   - Grilles
   - OCR texte
         ↓
7. Générer code:
   - Python (matplotlib, numpy)
   - LaTeX (tikz)
   - HOL (formes géométriques)
         ↓
8. Rapport final + JSON export
         ↓
Affichage au user
```

---

## ✨ Capacités du Système Vision Complet

**Géométrie:**
- Détection de formes (cercles, rectangles, polygones)
- Extraction de points/sommets
- Détection de lignes/segments
- Mesure d'angles et distances
- Symétrie et régularité

**Données:**
- Tables/matrices (OCR)
- Extraction de nombres
- Conversion formats (JSON, CSV, DataFrame)

**Graphiques:**
- Axes (x, y, z)
- Points de données
- Courbes et tendances
- Légendes et labels

**Diagrammes:**
- Boîtes et formes
- Connecteurs et relations
- Flux et hiérarchies

**Schémas:**
- Grilles de calibration
- Symboles mathématiques
- Annotations

**Code:**
- Python (calculs)
- LaTeX (visualisation)
- HOL (preuves)

---

## ⚙️ Configuration

Variables d'environnement (optionnelles):

```bash
# Niveau de verbosité
export GABRIEL_IMAGE_VERBOSE=1

# Formats de sortie
export GABRIEL_IMAGE_FORMATS=python,latex,hol,json

# Cache des résultats
export GABRIEL_IMAGE_CACHE=./data/cache/vision

# Timeout analyse (secondes)
export GABRIEL_IMAGE_TIMEOUT=30
```

---

## 🔗 Fichiers Concernés

```
src/
├── complete_vision_system.py     ← Cœur vision complet
├── production_validation_system.py ← Validation
├── image_access_manager.py       ← Accès fichiers
├── vision_module.py              ← Vision géométrique
├── advanced_vision_module.py     ← Tables/graphiques/diagrams
├── gabriel_image_interface.py    ← Interface utilisateur (nouveau)
└── ui/
    └── cli.py                    ← À modifier (ajouter _handle_image_analysis)
```

---

## 🧪 Test Rapide

Sans modification du CLI, testez directement:

```python
# Dans un terminal Python
from src.gabriel_image_interface import gabriel_analyze_image

result = gabriel_analyze_image(
    "analyse image C:\\theorie-mathematique\\src\\tex\\tex-2\\quadrature_parabole_zero_critique.png"
)
print(result)
```

---

## ✅ Status

| Composant | Status | Notes |
|-----------|--------|-------|
| Vision complète | ✓ Implémenté | complete_vision_system.py |
| Interface CLI | ⏳ À ajouter | 5 lignes dans cli.py |
| API HTTP | ✓ Disponible | Flask API |
| Python API | ✓ Prêt | Importez directement |
| Tests | ✓ Complets | Voir src/tests/ |

**Prochaine étape:** Ajouter les 5 lignes dans `cli.py` pour que Gabriel réponde aux demandes d'images!
