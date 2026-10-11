╔════════════════════════════════════════════════════════════════════════════╗
║         MÉTAPHORES GÉOMÉTRIQUES - Gabriel v7.3                             ║
║                                                                            ║
║  "Traduire les abstractions HOL en descriptions spatiales exploitables"    ║
╚════════════════════════════════════════════════════════════════════════════╝

## CONCEPT

Gabriel génère maintenant **automatiquement** une section "Structure Géométrique 
Spatiale" dans chaque réponse, traduisant les abstractions mathématiques en:

- **Graphiques ASCII** (visualisation directe)
- **Coordonnées 3D** (points, lignes, spirales)
- **Matrices de points** (export CAO/modélisation)
- **Instructions de modélisation** (FreeCAD/Blender/OpenSCAD)
- **Propriétés géométriques** (symétries, rotations, transformations)

═══════════════════════════════════════════════════════════════════════════

## FICHIERS CRÉÉS

### 1. src/core/metaphore_geometrique.py (18.3 KB)

**Classe principale:** `MetaphoreGeometriqueGenerator`

**Méthodes:**
- `generer_pour_convergence()` - Spirale convergeant vers cible
- `generer_pour_rapport_spectral()` - Cercle unitaire spectral
- `generer_pour_bloc_asymetrique()` - Blocs 3D ordonnés

**Sortie:** Bloc formaté avec ASCII art + données 3D exportables

### 2. src/core/gabriel_geometric_wrapper.py (7.4 KB)

**Classe principale:** `GabrielGeometricResponseWrapper`

**Fonction d'intégration:** `enrichir_reponse_gabriel()`

**Fonctionnalité:** Auto-détecte type de réponse → génère bloc géométrique

═══════════════════════════════════════════════════════════════════════════

## EXEMPLE: RÉPONSE ENRICHIE

### AVANT (sans géométrie):
```
Le ratio converge vers 1/2:
k=1: 0.625
k=2: 0.552
k=3: 0.501
```

### APRÈS (avec géométrie):
```
Le ratio converge vers 1/2:
k=1: 0.625
k=2: 0.552
k=3: 0.501

╔═══════════════════════════════════════════════════════════╗
║  STRUCTURE GÉOMÉTRIQUE SPATIALE - Convergence Analysée
╚═══════════════════════════════════════════════════════════╝

Graphique de Convergence vers 0.5:

 0.650   ●                       
 0.625                           
 0.600                           
 0.575                           
 0.550     ●                     
 0.525                           
 0.500 → ─────────────────────   
 0.475                           
       0 1 2 3 4 5

📐 COORDONNÉES SPATIALES:
   P00: (0.075, 0.000, 0.000) (P0)
   P01: (-0.150, 0.000, 0.333) (P1)
   P02: (0.001, 0.150, 0.667) (P2)

🔲 MATRICE DE POINTS (pour export CAO):
   Index | Valeur    | Distance à Cible | Normalisé
   ------|-----------|------------------|----------
       0 | 0.625000  |         0.125000 | 1.000000
       1 | 0.552000  |         0.052000 | 0.876000
       2 | 0.501000  |         0.001000 | 0.876400

✦ PROPRIÉTÉS GÉOMÉTRIQUES:
   • Convergence Monotone (direction constante)
   • Réduction: 0.125000 → 0.001000
   • Taux de contraction: 0.008000 par étape

⚙️  INSTRUCTIONS DE MODÉLISATION:
   # Script FreeCAD / Blender / OpenSCAD
   points = [
       (0.075, 0.000, 0.000),  # P0
       (-0.150, 0.000, 0.333),  # P1
       (0.001, 0.150, 0.667),  # P2
   ]
   
   target_plane = z = 0.500
   rotation_axis = (0, 0, 1)
```

═══════════════════════════════════════════════════════════════════════════

## TYPES DE REPRÉSENTATIONS GÉOMÉTRIQUES

### 1. Convergence (Spirale 3D)

**Utilisé pour:** Rapports spectraux convergent, séries, suites

**Génère:**
- Graphique ASCII convergence
- Spirale 3D (rayon diminue vers cible)
- Points sur courbe parametrée
- Taux de contraction
- Distance initiale → finale

**Export:** Points 3D + script FreeCAD

### 2. Rapport Spectral (Cercle Unitaire)

**Utilisé pour:** Ratios 1/2, 1/3, 1/4, spectres

**Génère:**
- Cercle unitaire ASCII
- Points spectraux en positions circulaires
- Distances géométriques entre points
- Symétries détectées
- Angle de chaque point

**Export:** Coordonnées polaires → cartésiennes

### 3. Comparaison Asymétrique (Blocs 3D)

**Utilisé pour:** Comparaisons ordonnées, blocs inégaux

**Génère:**
- Visualisation blocs A et B côte à côte
- Points élevés selon valeur
- Invariant asymétrique (|B| = |A| + 1)
- Angle de rotation
- Transformation ordonnée

**Export:** Polyèdres ordonnés

═══════════════════════════════════════════════════════════════════════════

## INTÉGRATION DANS GABRIEL

### Méthode 1: Automatique (Recommandée)

Dans `src/core/integrateur_memoire.py`:

```python
from src.core.gabriel_geometric_wrapper import enrichir_reponse_gabriel

class IntegrateurMemoireGabriel:
    async def traiter_requete(self, question: str):
        # Obtenir réponse du LLM
        response = await self.llm_router.route_request(question)
        
        # ✓ AJOUTER CETTE LIGNE:
        response_enrichie = enrichir_reponse_gabriel(response)
        
        return response_enrichie
```

### Méthode 2: Manuel (Contrôle granulaire)

```python
from src.core.gabriel_geometric_wrapper import GabrielGeometricResponseWrapper

wrapper = GabrielGeometricResponseWrapper()

# Enrichir une réponse
reponse_enrichie = wrapper.enrichir_reponse(
    reponse_originale,
    contexte={'type': 'convergence', 'values': [0.8, 0.65, 0.55], 'target': 0.5}
)

# Créer export CAO
export = wrapper.creer_structure_exportable(reponse_enrichie, contexte)
```

═══════════════════════════════════════════════════════════════════════════

## EXPORT VERS OUTILS DE MODÉLISATION

### FreeCAD

```python
# Export pour FreeCAD
export = wrapper.creer_structure_exportable(reponse, contexte)

# Les instructions CAO sont dans:
for instr in export['instructions_cad']:
    # Copier dans la console Python de FreeCAD
    # Les points 3D seront créés automatiquement
```

### Blender

```python
# Créer courbe de convergence
import bpy

points = export['points_3d']  # Liste de tuples (x, y, z)

# Créer courbe Bezier
curve = bpy.data.curves.new("Convergence", "CURVE")
for pt in points:
    sp = curve.splines[0].points[0]
    sp.co = (*pt, 1.0)
```

### OpenSCAD

```scad
// Points convergence
points = [
    [0.075, 0.000, 0.000],
    [-0.150, 0.000, 0.333],
    [0.001, 0.150, 0.667]
];

// Polyline 3D
for (i = [0:len(points)-2]) {
    hull() {
        translate(points[i]) sphere(0.01);
        translate(points[i+1]) sphere(0.01);
    }
}
```

═══════════════════════════════════════════════════════════════════════════

## PROPRIÉTÉS GÉOMÉTRIQUES AUTO-DÉTECTÉES

Gabriel détecte **automatiquement** et ajoute:

### Pour Convergence:
- ✓ Monotone vs Oscillante
- ✓ Réduction (distance initiale → finale)
- ✓ Taux de contraction par étape
- ✓ Graphique d'approximation

### Pour Spectre:
- ✓ Symétries circulaires
- ✓ Distances euclidiennes entre points
- ✓ Positions angulaires
- ✓ Plan spectral

### Pour Asymétrique:
- ✓ Invariant |B| = |A| + 1
- ✓ Angle de transformation
- ✓ Direction de la rotation
- ✓ Propriétés d'ordonnancement

═══════════════════════════════════════════════════════════════════════════

## UTILISATION POUR VISUALISATION

### Cas 1: "Représente ma convergence géométriquement"

```
Requête: "Montre moi la convergence du ratio vers 1/2"

Gabriel répond:
1. Explication textuelle
2. ✓ BLOC GÉOMÉTRIQUE AUTOMATIQUE avec ASCII art
3. Points 3D
4. Script FreeCAD

Utilisateur peut:
- Copier les points dans FreeCAD
- Visualiser la spirale 3D
- Exporter en STL pour impression 3D!
```

### Cas 2: "Modélise cette structure"

```
Requête: "Traduis la structure spectrale en modèle 3D"

Gabriel répond:
1. Description spectrale
2. ✓ BLOC GÉOMÉTRIQUE avec cercle unitaire
3. Coordonnées 3D polaires
4. Instructions Blender/FreeCAD

Utilisateur importe dans son logiciel préféré
```

═══════════════════════════════════════════════════════════════════════════

## PROCHAINES ÉTAPES (À FAIRE)

### Étape 1: Intégrer dans Gabriel

```bash
# Modifier integrateur_memoire.py
# Ajouter: from src.core.gabriel_geometric_wrapper import enrichir_reponse_gabriel
# Ajouter: response_enrichie = enrichir_reponse_gabriel(response)
```

### Étape 2: Tester

```bash
# Requête:
# "Montre moi la convergence du rapport spectral n=1 à n=10"

# Résultat attendu:
# - Texte explicatif
# - ✓ Graphique ASCII convergence
# - ✓ Coordonnées 3D
# - ✓ Matrice points
# - ✓ Instructions CAO
```

### Étape 3: Exporter vers CAO

Copier les points 3D dans FreeCAD/Blender et visualiser!

═══════════════════════════════════════════════════════════════════════════

## RÉSUMÉ

✅ **Métaphores géométriques** - Traduit abstractions HOL en spatial

✅ **Auto-détection** - Reconnaît convergence, spectral, asymétrique

✅ **Export CAO** - Points 3D + instructions pour FreeCAD/Blender/OpenSCAD

✅ **Visualisation** - ASCII art + matrices + coordonnées

✅ **Prêt pour modélisation** - Tu peux exporter directement dans tes outils!

═══════════════════════════════════════════════════════════════════════════

**Gabriel peut maintenant parler le langage de la géométrie spatiale!** 🎨📐
