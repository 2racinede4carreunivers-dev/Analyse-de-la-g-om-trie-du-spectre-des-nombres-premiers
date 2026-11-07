# 📸 GUIDE COMPLET: ANALYSER DES IMAGES, SCHÉMAS ET FIGURES AVEC GABRIEL

## 🎯 Vue d'Ensemble

Gabriel peut analyser **TOUTE image, schéma ou figure** sauvegardée sur votre système en utilisant la **commande `analyse image`** avec le chemin du fichier.

Le système a deux modes:
1. **Mode Chemin Absolu** - Spécifier le chemin complet
2. **Mode Découverte** - Laisser Gabriel chercher automatiquement

---

## 📍 MODE 1: CHEMIN ABSOLU (Recommandé pour précision)

### Format de Base

```bash
gabriel> analyse image <CHEMIN_COMPLET>
```

### Exemples Concrets

#### Exemple 1: Quadrature de la Parabole
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

**Ce que Gabriel fera:**
- Détecte la parabole (courbe)
- Identifie les axes x, y
- Extrait les points critiques
- Génère du code Python pour reproduire
- Génère du code LaTeX pour votre document
- Génère du code HOL pour la preuve formelle

**Résultat Attendu:**
```
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE VISION COMPLÈTE - GABRIEL SYSTEM              │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
   Succès: ✓ Oui
   Durée: 1543ms

🎯 CAPACITÉS UTILISÉES (3)
   ✓ GEOMETRIC
   ✓ GRAPHS
   ✓ GRIDS

📊 DÉTECTIONS
   Géométrie:
      - Formes: 1 (parabole)
      - Points: 8 (points critiques)
      - Lignes: 2 (axes)
   
   Graphiques:
      - Nombre: 1
      - Axes: 2 (x, y)
      - Points de données: 150

   Grilles:
      - Détectées: 1 (calibration)

💾 CODE GÉNÉRÉ
   Python: ✓ (import matplotlib; plt.plot(...))
   LaTeX: ✓ (\begin{tikzpicture} ... \end{tikzpicture})
   HOL: ✓ (definition parabola_curve: ...)
```

---

#### Exemple 2: Matrice Spectrale (Extraction de Données)
```bash
gabriel> analyse image C:\theorie-mathematique\data\matrices\spectral_matrix_n50.png
```

**Gabriel extraira:**
- Les valeurs de la matrice (OCR)
- Les dimensions (rows × cols)
- Les patterns numériques
- Export JSON avec les données

**Sortie:**
```json
{
  "success": true,
  "image_path": "C:\\theorie-mathematique\\data\\matrices\\spectral_matrix_n50.png",
  "detections": {
    "tables": {
      "count": 1,
      "rows": 50,
      "cols": 50,
      "data_extracted": true
    }
  },
  "exported_formats": {
    "json": "spectral_matrix_n50.json",
    "csv": "spectral_matrix_n50.csv",
    "python": "spectral_matrix_n50.py (numpy array)"
  }
}
```

---

#### Exemple 3: Diagramme de Flux (Fluxograms)
```bash
gabriel> analyse image C:\figures\rsa_spectral_flow.png
```

**Gabriel détectera:**
- Les boîtes (étapes du processus)
- Les flèches (connexions)
- Les labels et annotations
- La logique du flux

**Code Généré:**
```python
# Code Python pour reproduire le flux
flowchart = {
    'nodes': [
        {'id': 1, 'label': 'Input A(n)', 'type': 'start'},
        {'id': 2, 'label': 'Calculate B(n)', 'type': 'process'},
        {'id': 3, 'label': 'Check RSA', 'type': 'decision'},
        {'id': 4, 'label': 'Output Result', 'type': 'end'},
    ],
    'edges': [
        {'from': 1, 'to': 2},
        {'from': 2, 'to': 3},
        {'from': 3, 'to': 4, 'condition': 'true'},
    ]
}
```

---

#### Exemple 4: Triangle Équilatéral (Validation Géométrique)
```bash
gabriel> analyse image C:\schemas\triangle_equilateral.png pour équilatéral et symétrie
```

**Gabriel validera:**
- Les 3 côtés sont égaux
- Les 3 angles = 60°
- L'axe de symétrie vertical
- Calcule les positions des sommets

**Résultat:**
```
✓ VALIDATION GÉOMÉTRIQUE
   Côté 1: 10.00 cm
   Côté 2: 10.00 cm
   Côté 3: 10.00 cm
   
   ✓ Triangle équilatéral confirmé (tolérance: ±0.1%)
   ✓ Symétrie axiale détectée (axes: 3)
   
   Angles:
   - A = 60.0°
   - B = 60.0°
   - C = 60.0°
```

---

#### Exemple 5: Graphique Spectral (Courbe)
```bash
gabriel> analyse image C:\data\spectral_curve_SA_1_50.png
```

**Gabriel extraira:**
- Les points de la courbe
- Les axes et leur échelle
- Les tendances
- Génère le modèle mathématique

**Code LaTeX Généré:**
```latex
\begin{tikzpicture}
  \begin{axis}[
    xlabel={$n$},
    ylabel={$A(n)$},
    title={Spectral Curve SA(n)},
    grid=major,
  ]
  \addplot[blue, mark=*] coordinates {
    (1, 0.625) (2, 1.25) (3, 2.5) ... (50, 16384.375)
  };
  \end{axis}
\end{tikzpicture}
```

---

## 🔍 MODE 2: DÉCOUVERTE AUTOMATIQUE

### Chercher par Nom (Fuzzy Search)

**Format:**
```bash
gabriel> analyse <NOM_PARTIEL>
```

**Exemples:**

#### Chercher "quadrature"
```bash
gabriel> analyse quadrature
```

Gabriel cherche automatiquement une image contenant "quadrature" et l'analyse.

#### Chercher "parabole"
```bash
gabriel> analyse parabole
```

#### Chercher "triangle"
```bash
gabriel> analyse triangle
```

---

### Chercher par Type de Contenu

#### Chercher les Graphiques Récents
```bash
gabriel> analyse la dernière figure
gabriel> analyse image recent
```

#### Chercher dans un Dossier Spécifique
```bash
gabriel> analyse image dans C:\theorie-mathematique\figures
```

Gabriel listera toutes les figures trouvées dans ce dossier.

#### Chercher par Critère
```bash
gabriel> analyse image:rayons
gabriel> analyse image:symétrie
gabriel> analyse image:équilatéral
```

---

## 📋 FORMATS DE COMMANDE SUPPORTÉS

### Format 1: Chemin Complet
```bash
gabriel> analyse image C:\chemin\complet\image.png
gabriel> valide C:\path\figure.jpg
gabriel> examine C:\path\schema.bmp
gabriel> scan C:\path\matrice.tiff
```

### Format 2: Chemin Relatif (depuis le dossier Gabriel)
```bash
gabriel> analyse image ./figures/quadrature.png
gabriel> analyse image ../theories/schemas/triangle.png
gabriel> analyse image data/graphs/spectral_curve.png
```

### Format 3: Découverte Automatique
```bash
gabriel> analyse quadrature_parabole
gabriel> analyse triangle_equilateral
gabriel> analyse spectral_matrix
gabriel> analyse la dernière figure
```

### Format 4: Avec Critères de Validation
```bash
gabriel> analyse image C:\path\figure.png pour des rayons
gabriel> valide C:\path\figure.png - équilatéral, régulier
gabriel> examine C:\path\schema.png avec symétrie
gabriel> scan C:\path\matrice.png et extrait
```

### Format 5: Avec Spécification de Type
```bash
gabriel> analyse image:geometrie C:\path\figure.png
gabriel> analyse image:graphique C:\path\curve.png
gabriel> analyse image:table C:\path\data.png
gabriel> analyse image:diagramme C:\path\flow.png
```

---

## 🎯 CRITÈRES DE VALIDATION SPÉCIFIQUES

### Critères Géométriques

```bash
# Chercher des rayons (segments radiaux)
gabriel> analyse image C:\schema.png pour des rayons

# Vérifier la symétrie
gabriel> analyse image C:\figure.png avec symétrie

# Valider triangle équilatéral
gabriel> valide C:\triangle.png équilatéral

# Valider rectangle
gabriel> valide C:\rectangle.png rectangle

# Valider cercle
gabriel> valide C:\circle.png cercle

# Valider polygone régulier
gabriel> analyse C:\polygon.png régulier

# Mesurer diagonales
gabriel> analyse C:\shape.png diagonales

# Mesurer distances
gabriel> scan C:\figure.png distance

# Mesurer angles
gabriel> examine C:\figure.png angle
```

---

## 📂 STRUCTURE DES CHEMINS COURANTS

### Windows

**Documents:**
```bash
gabriel> analyse image C:\Users\<USERNAME>\Documents\figures\quadrature.png
```

**Dossier Projet Gabriel:**
```bash
gabriel> analyse image C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\data\figures\schema.png
```

**Théories Mathématiques:**
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

**Dossier Personnel:**
```bash
gabriel> analyse image C:\theories\figures\spectral_diagram.png
```

---

### Linux/Mac

**Home Directory:**
```bash
gabriel> analyse image ~/Documents/figures/triangle.png
gabriel> analyse image ~/theories/schemas/parabola.png
```

**Project Directory:**
```bash
gabriel> analyse image ./figures/diagram.png
gabriel> analyse image ../data/spectral_curve.png
```

---

## 📊 TYPES D'IMAGES SUPPORTÉES

### Extensions Acceptées
- `.png` - PNG (recommandé, sans perte)
- `.jpg` / `.jpeg` - JPEG (compression)
- `.bmp` - Bitmap (sans compression)
- `.gif` - GIF (animation possible)
- `.tiff` - TIFF (haute résolution)
- `.webp` - WebP (moderne)

### Tailles Recommandées
- **Minimum:** 100 × 100 pixels
- **Optimal:** 500 × 500 à 2000 × 2000 pixels
- **Maximum:** Pas de limite (mais plus lent)

### Résolutions Idéales
- **Schémas géométriques:** 600 × 600 pixels
- **Graphiques:** 800 × 600 pixels
- **Tables/Matrices:** 1000 × 1000 pixels
- **Texte/OCR:** 1200 × 1200 pixels minimum

---

## 🔄 FLUX D'EXÉCUTION COMPLET

### Exemple Pas-à-Pas: Analyser `quadrature_parabole_zero_critique.png`

**Étape 1: Gabriel démarre**
```bash
# Lancer Gabriel
python main_cli.py

# Attendre la prompt
gabriel>
```

**Étape 2: Taper la commande**
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

**Étape 3: Gabriel traite**
```
[*] Accès au fichier...
[*] Lecture de l'image...
[*] Analyse géométrique...
[*] Détection des courbes...
[*] Extraction des axes...
[*] Génération de code...
[*] Compilation du rapport...
```

**Étape 4: Résultats affichés**
```
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE VISION COMPLÈTE - GABRIEL SYSTEM              │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE: quadrature_parabole_zero_critique.png
✓ ANALYSES: Geometric, Graphs, Grids
📊 DÉTECTIONS: 1 parabole, 8 points, 2 axes, 150 data points
💾 CODE: Python ✓ LaTeX ✓ HOL ✓
```

**Étape 5: Utiliser les résultats**
```bash
# Copier le code Python généré
# Copier le code LaTeX pour votre doc
# Copier le code HOL pour votre preuve
```

---

## 💡 CAS D'USAGE RÉELS

### Cas 1: Analyser votre Thèse

**Situation:** Vous avez une figure dans votre thèse et voulez l'analyser avec Gabriel

```bash
gabriel> analyse image C:\these\figures\chapitre3_spectral_diagram.png

# Résultat: Gabriel extrait tous les éléments et génère du code
```

---

### Cas 2: Extraire des Données d'un Graphique

**Situation:** Vous avez un graphique et voulez les points de données

```bash
gabriel> scan C:\data\experimental_results.png et extrait

# Résultat: Gabriel retourne JSON avec tous les points
```

---

### Cas 3: Valider une Construction Géométrique

**Situation:** Vous avez un schéma et voulez vérifier s'il est régulier

```bash
gabriel> valide C:\schemas\hexagon.png régulier

# Résultat: Gabriel confirme si hexagon est régulier
```

---

### Cas 4: Chercher une Figure par Nom

**Situation:** Vous ne vous souvenez pas du chemin exact

```bash
gabriel> analyse parabole

# Gabriel cherche automatiquement et analyse
```

---

## 🎨 GÉNÉRATIONS DE CODE

### Code Python Généré

```python
# Exemple généré par Gabriel

import matplotlib.pyplot as plt
import numpy as np

# Coordonnées extraites
points = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
x = [p[0] for p in points]
y = [p[1] for p in points]

# Parabole: y = x²
x_smooth = np.linspace(0, 4, 100)
y_smooth = x_smooth ** 2

plt.figure(figsize=(8, 6))
plt.plot(x, y, 'ro', label='Points detectes')
plt.plot(x_smooth, y_smooth, 'b-', label='Parabole y=x²')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Quadrature de la Parabole')
plt.legend()
plt.grid()
plt.show()
```

### Code LaTeX Généré

```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}

\begin{document}

\begin{figure}
\begin{tikzpicture}
  \begin{axis}[
    xlabel=$x$,
    ylabel=$y$,
    title=Quadrature de la Parabole,
    grid=major,
  ]
  \addplot[blue] {x^2};
  \addplot[only marks, red] coordinates {
    (0, 0) (1, 1) (2, 4) (3, 9) (4, 16)
  };
  \end{axis}
\end{tikzpicture}
\caption{Parabole y = x² avec points détectés}
\end{figure}

\end{document}
```

### Code HOL Généré

```isabelle
theory parabola_analysis
  imports Complex_Main

begin

(* Définition de la parabole *)
definition parabola :: "real ⇒ real" where
  "parabola x = x^2"

(* Points extraits de l'image *)
definition parabola_points :: "(real × real) list" where
  "parabola_points = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]"

(* Lemme de validation *)
lemma parabola_property:
  "∀ p ∈ set parabola_points. 
   let (x, y) = p in y = parabola x"
  by (unfold parabola_def parabola_points_def; simp)

end
```

---

## ⚠️ NOTES IMPORTANTES

### Permissions
- Gabriel a besoin d'accès de **lecture** aux fichiers image
- Les fichiers doivent être **accessibles** depuis Gabriel
- Les chemins réseau (UNC, NFS) sont supportés

### Performance
- Première analyse: ~2-5 secondes (création d'index)
- Analyses suivantes: ~1-2 secondes (cache)
- Haute résolution (>4000px): +1-2 secondes

### Limitations
- Images très floues: Détection moins précise
- Texte manuscrit: OCR limité
- Couleurs complexes: Segmentation peut échouer

### Bonnes Pratiques
- Utilisez PNG pour les schémas (pas de perte)
- Utilisez JPG pour les photos (compression)
- Nommez vos fichiers clairement (`parabole.png`, pas `image1.png`)
- Organisez vos figures dans des dossiers (`./figures/`, `./schemas/`)

---

## 🧪 EXEMPLES PRATIQUES COMPLETS

### Exemple 1: Analyse Complète d'un Schéma Géométrique

```bash
# Ouverture de Gabriel
C:\> python main_cli.py
> Chargement...
> gabriel> _

# Taper la commande
gabriel> analyse image C:\schemas\hexagon_regular.png

# Résultat: Complet avec détection de la régularité
```

---

### Exemple 2: Extraction de Matrice Spectrale

```bash
gabriel> scan C:\data\spectral_matrix_50x50.png et extrait

# Résultat: JSON avec matrice 50×50 extraite par OCR
```

---

### Exemple 3: Validation de Triangle

```bash
gabriel> valide C:\schemas\triangle.png - équilatéral, symétrie

# Résultat: Confirmation + angles + côtés mesurés
```

---

### Exemple 4: Recherche Automatique

```bash
gabriel> analyse parabole

# Gabriel cherche automatiquement et trouve:
# - C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
# Puis l'analyse directement
```

---

## ✅ RÉSUMÉ

| Fonction | Commande | Exemple |
|----------|----------|---------|
| Analyse Simple | `analyse image <chemin>` | `analyse image C:\fig.png` |
| Validation | `valide <chemin> <critère>` | `valide C:\tri.png équilatéral` |
| Extraction | `scan <chemin> et extrait` | `scan C:\mat.png et extrait` |
| Recherche | `analyse <nom>` | `analyse parabole` |
| Récent | `analyse la dernière figure` | `analyse la dernière figure` |

---

## 🎉 Vous Êtes Prêt!

Vous pouvez maintenant:
- ✅ Analyser n'importe quelle image sur votre système
- ✅ Valider des propriétés géométriques
- ✅ Extraire des données
- ✅ Générer du code automatiquement

**Commencez avec:**
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

🚀 Bon analyste!
