# Configuration Gabriel Vision - Activation complète
# ====================================================

## Import principal dans main_cli.py ou ask_gabriel.py

```python
from complete_vision_system import (
    get_complete_vision_system,
    analyze_image_complete,
    CompleteAnalysisResult,
)

# Initialiser une seule fois
vision_system = get_complete_vision_system()
```

## Utilisation dans les commandes Gabriel

### Commande: "analyser image"
```python
if user_input.startswith("analyser image"):
    image_path = user_input.replace("analyser image", "").strip()
    result = vision_system.analyze_image_complete(image_path)
    
    if result.success:
        print(result.full_report)
        print(f"\n📊 JSON Export:\n{result.json_data}")
        
        # Demander le type de code si applicable
        if "code" in user_input.lower():
            if "python" in user_input.lower():
                print(result.python_code)
            elif "latex" in user_input.lower():
                print(result.latex_code)
            elif "hol" in user_input.lower():
                print(result.hol_code)
    else:
        print(f"❌ Erreur: {result.error_message}")
```

### Commande: "analyser table"
```python
if user_input.startswith("analyser table"):
    image_path = user_input.replace("analyser table", "").strip()
    result = vision_system.analyze_image_complete(
        image_path,
        analyze_geometric=False,
        analyze_graphs=False,
        analyze_diagrams=False,
        analyze_grids=False,
    )
    
    if result.tables_detected > 0:
        print(f"✓ {result.tables_detected} table(s) détectée(s)")
        print(f"Dimensions: {result.table_rows} x {result.table_cols}")
        print(result.full_report)
```

### Commande: "analyser graphique"
```python
if user_input.startswith("analyser graphique"):
    image_path = user_input.replace("analyser graphique", "").strip()
    result = vision_system.analyze_image_complete(
        image_path,
        analyze_geometric=False,
        analyze_tables=False,
        analyze_diagrams=False,
        analyze_grids=False,
    )
    
    if result.graphs_detected > 0:
        print(f"✓ Graphique détecté")
        print(f"  Axes: {result.graph_axes}")
        print(f"  Points de données: {result.graph_points}")
        print(result.full_report)
```

### Commande: "analyser diagramme"
```python
if user_input.startswith("analyser diagramme"):
    image_path = user_input.replace("analyser diagramme", "").strip()
    result = vision_system.analyze_image_complete(
        image_path,
        analyze_geometric=False,
        analyze_tables=False,
        analyze_graphs=False,
        analyze_grids=False,
    )
    
    if result.diagram_boxes > 0:
        print(f"✓ Diagramme détecté")
        print(f"  Boîtes: {result.diagram_boxes}")
        print(f"  Connecteurs: {result.diagram_connectors}")
        print(result.full_report)
```

## Dépendances requises

### Obligatoires
```bash
pip install pillow numpy
```

### Optionnels mais très recommandés
```bash
pip install opencv-python  # Pour détection avancée
pip install pytesseract    # Pour OCR (tables)
pip install requests       # Pour accès URL
```

### Pour OCR (Windows)
```
Télécharger Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
Installer à: C:\Program Files\Tesseract-OCR
Ajouter au code:
    import pytesseract
    pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Configuration du cache

```python
from pathlib import Path
from complete_vision_system import get_complete_vision_system

# Personnaliser le répertoire de cache
vision_system = get_complete_vision_system(
    cache_dir="C:/Gabriel/image_cache"
)
```

## Exemples d'utilisation complète

### Exemple 1: Figure géométrique avec code généré
```python
result = vision_system.analyze_image_complete(
    "C:/Users/Philippe/Desktop/triangle.png"
)

if result.success:
    print(result.full_report)
    print("\n=== CODE PYTHON ===")
    print(result.python_code)
```

### Exemple 2: Table de données
```python
result = vision_system.analyze_image_complete(
    "https://example.com/data_table.png",
    analyze_tables=True,
    analyze_geometric=False,
)

# Accéder via image_access_manager
if result.source:
    print(f"Table téléchargée: {result.source.resolved_path}")
```

### Exemple 3: Graphique avec analyse
```python
result = vision_system.analyze_image_complete(
    "\\serveur\documents\graph.png",
    analyze_graphs=True,
)

print(f"Détecté: {result.graph_points} points de données")
print(f"Axes: {result.graph_axes}")
```

### Exemple 4: Analyse complète multi-modalités
```python
# Analyser TOUS les types d'éléments
result = vision_system.analyze_image_complete(
    "complex_diagram.png",
    analyze_geometric=True,
    analyze_tables=True,
    analyze_graphs=True,
    analyze_diagrams=True,
    analyze_grids=True,
    generate_code=True,
)

print(f"✓ Capacités utilisées: {', '.join(result.capabilities_used)}")
print(f"✓ Durée: {result.analysis_duration_ms:.0f}ms")
print(result.full_report)

# Export JSON pour post-traitement
with open("analysis.json", "w") as f:
    f.write(result.json_data)
```

## Structure des modules

```
src/
├── image_access_manager.py       # Accès universel aux images
├── vision_module.py              # Figures géométriques
├── advanced_vision_module.py     # Tables, graphiques, diagrammes
├── gabriel_vision_integration.py # Intégrateur simple
└── complete_vision_system.py     # Intégrateur COMPLET (← UTILISER)
```

## Capacités par module

### complete_vision_system.py (PRINCIPAL)
✓ Orchestration complète
✓ Analyse multi-modalités
✓ Rapports unifiés
✓ Export JSON
✓ Génération de code

### advanced_vision_module.py
✓ Tables et matrices (OCR)
✓ Graphiques avec axes (détection d'axes, points)
✓ Diagrammes (boîtes, connecteurs, flux)
✓ Schémas (symboles, flèches)
✓ Grilles et calibration

### vision_module.py
✓ Figures géométriques (triangle, rectangle, cercle, polygon)
✓ Points, lignes, formes
✓ Validation de cohérence
✓ Calcul d'aire et périmètre

### image_access_manager.py
✓ Accès: chemin local, URL, réseau UNC/SMB
✓ Cache local
✓ Téléchargement HTTP/HTTPS

## Dépannage

### "Module not found: advanced_vision_module"
→ Vérifier que le fichier est dans src/
→ Vérifier les imports dans complete_vision_system.py

### "OpenCV not available"
→ pip install opencv-python

### "Tesseract not found"
→ Installer Tesseract OCR (voir section dépendances)

### "Image not accessible"
→ Vérifier le chemin/URL
→ Vérifier les permissions
→ Vérifier la connectivité réseau

## Performance

Temps de traitement typique (image 500×500px):
- Détection géométrique: 100-300ms
- Détection tables: 200-500ms
- Détection graphiques: 150-400ms
- Détection diagrammes: 200-600ms
- Génération code: 50-150ms
- **TOTAL: 500-2000ms**

Avec cache (réutilisation):
- Immédiat (0-50ms)

## Limitations connues

- OCR nécessite Tesseract installé
- Détection de graphiques fonctionne mieux avec grilles visibles
- Tables rectilignes uniquement (pas de tables fusionnées)
- Schémas détectés mais pas de reconnaissance de symboles spécifiques
- Texte dans images: OCR basique uniquement

## Évolutions possibles

- [ ] Reconnaissance de symboles (circuits électriques, chimie)
- [ ] Reconnaissance d'équations mathématiques
- [ ] Détection de texte avec positionnement précis
- [ ] Analyse de couleurs et motifs
- [ ] Détection de cadran/jauge
- [ ] Extraction d'histogrammes
- [ ] Analyse de réseau/graphe (nœuds, arêtes)
