# GABRIEL VISION MODULE - Documentation Complète

## 🎯 Capacités principales

Gabriel peut maintenant:

### 1. **Accéder aux images depuis n'importe où**
   - ✅ Chemins locaux absolus: `C:\Users\Philippe\Pictures\figure.png`
   - ✅ Chemins relatifs: `./images/schema.jpg`
   - ✅ Partages réseau (UNC): `\\serveur\partage\diagram.png`
   - ✅ Partages réseau (SMB): `smb://serveur/partage/fichier.png`
   - ✅ URL HTTP/HTTPS: `https://example.com/image.png`

### 2. **Analyser les images**
   - ✅ Détecter les points (vertices, intersections, extremums)
   - ✅ Détecter les lignes (droites, courbes, pointillées)
   - ✅ Détecter les formes géométriques (triangles, rectangles, polygones)
   - ✅ Extraire les coordonnées précises

### 3. **Valider les figures**
   - ✅ Vérifier la cohérence entre points et figure
   - ✅ Calculer l'aire et le périmètre
   - ✅ Vérifier les propriétés géométriques (parallèles, perpendiculaires)
   - ✅ Générer un score de cohérence

### 4. **Générer du code paramétrique**
   - ✅ Code Python (matplotlib, numpy)
   - ✅ Code LaTeX TikZ
   - ✅ Code Isabelle/HOL formalisé
   - ✅ Coordonnées JSON

---

## 📖 Exemples d'utilisation

### Exemple 1: Analyser une image locale
```python
from gabriel_vision_integration import analyze_image

# Chemins locaux
result = analyze_image("C:/Users/Philippe/Pictures/geometrie.png")
result = analyze_image("./data/figures/triangle.jpg")
result = analyze_image("/home/user/images/schema.png")

if result.success:
    print(result.report)  # Rapport complet
    print(result.python_code)  # Code Python généré
    print(result.hol_code)  # Code HOL formalisé
```

### Exemple 2: Analyser une image depuis une URL
```python
result = analyze_image("https://example.com/my-figure.png")

if result.success:
    # L'image est automatiquement téléchargée et mise en cache
    print(f"Points détectés: {result.points_detected}")
    print(f"Formes détectées: {result.shapes_detected}")
```

### Exemple 3: Accéder via réseau
```python
# Partage Windows UNC
result = analyze_image("\\\\serveur-local\\documents\\figures\\schema.png")

# Partage SMB
result = analyze_image("smb://192.168.1.100/shared/diagram.png")
```

### Exemple 4: Valider que les points correspondent à la figure
```python
from gabriel_vision_integration import get_vision_integration

vision = get_vision_integration()

# Points fournis par l'utilisateur
user_points = [(100, 50), (200, 150), (150, 200)]

# Valider
validation = vision.validate_points_with_figure(
    "C:/path/to/triangle.png",
    user_points
)

if validation['valid']:
    print("✓ Points cohérents avec la figure")
else:
    print("✗ Points incohérents")
    for check in validation['checks']:
        print(f"  - {check['issues']}")
```

### Exemple 5: Générer du code paramétrique
```python
# Générer du code Python
python_code = vision.generate_parametric_code("image.png", language='python')

# Générer du code LaTeX TikZ
latex_code = vision.generate_parametric_code("image.png", language='latex')

# Générer du code Isabelle/HOL
hol_code = vision.generate_parametric_code("image.png", language='hol')
```

---

## 🏗️ Architecture

### Modules inclus

#### 1. **image_access_manager.py**
Gère l'accès universel aux images
- Détecte le type de source (local, URL, réseau)
- Résout les chemins
- Télécharge depuis HTTP/HTTPS
- Gère le cache local
- Support complet des chemins Windows/Linux

**Classes principales:**
- `ImageAccessManager`: Gestionnaire universel
- `ImageSource`: Représentation d'une source
- `ImageSourceType`: Énumération des types

#### 2. **vision_module.py**
Analyse visuelle et extraction de formes
- Détection de points (corner detection)
- Détection de lignes (Hough transform)
- Détection de formes (contour analysis)
- Calcul géométrique (aire, périmètre, centre)
- Génération de code paramétrique

**Classes principales:**
- `ImageVisionAnalyzer`: Analyseur visuel
- `Point`: Représente un point
- `Line`: Représente une ligne
- `Shape`: Représente une forme géométrique

#### 3. **gabriel_vision_integration.py**
Intégrateur principal pour Gabriel
- Point d'entrée unique
- Orchestration des modules
- Résultats structurés
- Gestion des erreurs
- Cache des analyses

**Classes principales:**
- `GabrielVisionIntegration`: Intégrateur
- `AnalysisResult`: Résultat complet

---

## ⚙️ Configuration

### Variables d'environnement
```bash
# Chemin du cache des images
GABRIEL_IMAGE_CACHE=/tmp/gabriel_image_cache

# Durée de vie du cache (heures)
GABRIEL_CACHE_TTL_HOURS=24

# Timeout pour téléchargement (secondes)
GABRIEL_IMAGE_DOWNLOAD_TIMEOUT=30
```

### Racines de recherche personnalisées
```python
vision = get_vision_integration()

# Ajouter une racine de recherche
vision.add_search_root("C:/MesDocuments/Figures")
vision.add_search_root("/mnt/shared/diagrams")

# Maintenant les chemins relatifs seront cherchés aussi dans ces dossiers
result = analyze_image("schema.png")  # Cherche dans MesDocuments aussi
```

---

## 📊 Résultat d'analyse

### Structure de `AnalysisResult`

```python
@dataclass
class AnalysisResult:
    success: bool  # Analyse réussie?
    timestamp: datetime
    image_path: str  # Chemin/URL original
    source: ImageSource  # Source accessible
    
    # Détections
    points_detected: int
    lines_detected: int
    shapes_detected: int
    
    # Validation
    is_valid: bool
    consistency_score: float  # 0-1
    validation_errors: list[str]
    validation_warnings: list[str]
    
    # Générations
    report: str  # Rapport complet
    python_code: str  # Code Python
    latex_code: str  # Code LaTeX
    hol_code: str  # Code HOL
    
    # Métadonnées
    coordinates: Dict  # Points, lignes, formes extraites
    analysis_duration_ms: float
    error_message: Optional[str]
```

---

## 🔄 Flux de travail recommandé

### Pour Gabriel dans une conversation

1. **Utilisateur fournit une image**
   ```
   "Analysez cette figure: C:/Users/Me/Desktop/triangle.png"
   ```

2. **Gabriel accède l'image**
   ```python
   result = analyze_image("C:/Users/Me/Desktop/triangle.png")
   ```

3. **Gabriel rapporte les détections**
   ```
   - Points détectés: 3
   - Formes: triangle
   - Aire: 1500 px²
   - Cohérence: 95%
   ```

4. **Gabriel génère du code si demandé**
   ```python
   # Code Python pour reproduire la figure
   # Code HOL pour la formaliser
   ```

5. **Gabriel valide les propriétés**
   ```
   - Triangle équilatéral? Calcul de distances...
   - Points alignés? Vérification des pentes...
   ```

---

## 🎨 Types d'images supportées

| Format | Support | Notes |
|--------|---------|-------|
| PNG | ✅ | Recommandé |
| JPG/JPEG | ✅ | Qualité acceptable |
| GIF | ✅ | Static GIF OK |
| BMP | ✅ | Non compressé |
| TIFF | ✅ | Haute qualité |
| SVG | ⚠️ | Conversion nécessaire |
| PDF | ⚠️ | Pages rasterisées |

---

## 🔧 Dépendances optionnelles

### Pour la détection avancée
```bash
pip install opencv-python  # Détection de coins, contours
pip install numpy  # Calculs matriciels
pip install pillow  # Traitement d'images
pip install requests  # Téléchargement URL
```

### Pour la génération LaTeX
```bash
pip install numpy matplotlib  # Visualisation
```

---

## ⚡ Performance

### Temps de traitement typique

| Opération | Temps | Notes |
|-----------|-------|-------|
| Détection points | 100-500ms | Dépend de la taille |
| Détection lignes | 150-600ms | Hough transform |
| Détection formes | 200-800ms | Contour analysis |
| Génération code | 50-200ms | Rapide |
| **Total** | **500-2000ms** | Image 500×500px |

### Cache

- Images en cache: 24h par défaut
- Réutilisé automatiquement
- Économise bande passante réseau/URL

---

## 🐛 Dépannage

### Image non trouvée
```
Chemin original: C:/Users/Philippe/Figures/schema.png
Erreur: Impossible d'accéder à l'image

Solutions:
1. Vérifier le chemin exact
2. Vérifier les permissions d'accès
3. Vérifier le format du chemin (slashes)
```

### Détection faible
```
Points détectés: 0
Lignes détectées: 0

Solutions:
1. Augmenter le contraste de l'image
2. Vérifier la résolution (min 100px)
3. Vérifier les formats (PNG/JPG recommandés)
```

### URL non accessible
```
Erreur: requests non disponible

Solution: pip install requests
```

---

## 📝 Exemples complets

### Exemple: Analyser un triangle
```python
from gabriel_vision_integration import get_vision_integration

vision = get_vision_integration()

# Analyser
result = vision.analyze_image("triangle.png")

# Rapport
print(result.report)

# Points détectés
for pt in result.coordinates['points']:
    print(f"  Point: ({pt['x']:.1f}, {pt['y']:.1f})")

# Générer Python
with open("triangle_param.py", "w") as f:
    f.write(result.python_code)

# Générer HOL
with open("triangle_formal.thy", "w") as f:
    f.write(result.hol_code)
```

### Exemple: Validation interactive
```python
def validate_figure_interactive():
    vision = get_vision_integration()
    
    image_path = input("Chemin de l'image: ")
    result = vision.analyze_image(image_path)
    
    if not result.success:
        print(f"Erreur: {result.error_message}")
        return
    
    print(f"Formes détectées: {result.shapes_detected}")
    
    if result.shapes_detected > 0:
        # Demander les points
        coords = input("Coordonnées points (x1,y1 x2,y2...): ")
        points = []
        for coord_pair in coords.split():
            x, y = map(float, coord_pair.split(','))
            points.append((x, y))
        
        # Valider
        validation = vision.validate_points_with_figure(image_path, points)
        
        if validation['valid']:
            print("✓ Figure valide!")
        else:
            print("✗ Problèmes détectés:")
            for check in validation['checks']:
                for issue in check['issues']:
                    print(f"  - {issue}")
```

---

## 🚀 Activation dans Gabriel

Dans `main_cli.py` ou `ask_gabriel.py`, ajouter:

```python
from gabriel_vision_integration import get_vision_integration

# Commande pour analyser une image
if user_input.startswith("analyser image"):
    image_path = user_input.replace("analyser image", "").strip()
    vision = get_vision_integration()
    result = vision.analyze_image(image_path)
    
    if result.success:
        print(result.report)
        if "code" in user_input.lower():
            if "python" in user_input.lower():
                print(result.python_code)
            elif "hol" in user_input.lower():
                print(result.hol_code)
            elif "latex" in user_input.lower():
                print(result.latex_code)
    else:
        print(f"Erreur: {result.error_message}")
```

---

## 📞 Support

Pour les problèmes:
1. Vérifier les logs: `logger.info()`
2. Vérifier le cache: `vision.cache_stats()`
3. Nettoyer le cache: `vision.clear_cache()`
4. Consulter ce guide
