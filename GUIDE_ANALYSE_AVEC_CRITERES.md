# 🎯 GUIDE: ANALYSE AVEC CRITÈRES PERSONNALISÉS

## Vue d'Ensemble

Vous pouvez maintenant demander à Gabriel d'analyser une image **exactement selon vos besoins** en ajoutant des **critères spécifiques**.

Au lieu de:
```
gabriel> analyse image C:\image.png
```

Vous pouvez demander:
```
gabriel> analyse image C:\image.png | geometrie, precision:haute, rayons, export:json,python,latex
```

---

## 🔧 SYNTAXES SUPPORTÉES

### Syntaxe 1: Pipe (|) - Recommandée

```bash
gabriel> analyse image <CHEMIN> | <CRITÈRES>
```

**Format des critères:**
```
type1, type2 | precision:value | criteria1, criteria2 | export:format1,format2
```

**Exemples:**
```bash
# Analyse simple avec précision haute
gabriel> analyse image C:\path\image.png | precision:haute

# Avec critères de validation
gabriel> analyse image C:\path\image.png | geometrie, rayons, symetrie

# Complet
gabriel> analyse image C:\path\image.png | geometrie, precision:haute, rayons, symetrie, export:json,python,latex
```

---

### Syntaxe 2: Question (?) - Intuitive

```bash
gabriel> analyse <CHEMIN> ? <CRITÈRES>
```

Utilise le point d'interrogation pour "demander" une analyse spécifique.

**Exemples:**
```bash
# Quels sont les rayons et la symétrie?
gabriel> analyse C:\path\image.png ? rayons, symetrie

# Quelles formes, points et lignes détectes-tu?
gabriel> analyse C:\path\image.png ? formes, points, lignes

# Valide et exporte en JSON
gabriel> analyse C:\path\image.png ? validation:strict, export:json
```

---

### Syntaxe 3: Double-Colon (::) - Précise

```bash
gabriel> scan <CHEMIN> :: <CRITÈRES>
```

Utilise `::` pour les critères techniques très précis.

**Exemples:**
```bash
# Avec paramètres d'exécution
gabriel> scan C:\path\image.png :: precision:ultra, tolerance:0.5%, confidence:90%

# Extraction de données
gabriel> scan C:\path\matrix.png :: export:csv,json, detect_text:true

# Multi-validation
gabriel> scan C:\path\polygon.png :: rayons=5, symetrie=axiale, precision=haute
```

---

## 📋 CRITÈRES DISPONIBLES

### A. Types d'Analyses

Spécifiez **quoi analyser**:

```bash
geometrie          # Formes, points, lignes (par défaut)
graphique          # Axes, courbes, points de données
table              # Matrices, données tabulaires
diagramme          # Boîtes, connecteurs, flux
grille             # Calibration, repères
ocr                # Extraction de texte
tout               # Tous les types (par défaut)
```

**Exemples:**
```bash
gabriel> analyse image C:\fig.png | geometrie
gabriel> analyse image C:\curve.png | graphique
gabriel> analyse image C:\matrix.png | table
gabriel> analyse image C:\complex.png | geometrie, graphique, table
```

---

### B. Critères de Validation

Spécifiez **ce qu'il faut valider**:

```bash
rayons             # Segments radiaux
symetrie           # Axes de symétrie
equilateral        # Triangle équilatéral
rectangle          # Rectangle régulier
cercle             # Cercle complet
regulier           # Polygone régulier
diagonale          # Diagonales
distance           # Mesures
angle              # Angles
perpendiculaire    # Perpendiculaires
parallele          # Parallèles
concentrique       # Cercles concentriques
```

**Exemples:**
```bash
# Valider un triangle
gabriel> analyse image C:\triangle.png | equilateral, symetrie

# Valider un rectangle
gabriel> analyse image C:\rectangle.png | rectangle, parallele, perpendiculaire

# Mesurer les angles
gabriel> analyse image C:\polygon.png | angle, distance, regulier

# Complet
gabriel> analyse image C:\shape.png | rayons, symetrie, angle, distance
```

---

### C. Paramètres de Précision

Contrôlez la **qualité de l'analyse**:

```bash
precision:basse    # Rapide, moins précis (< 1 sec)
precision:moyenne  # Équilibre (1-2 sec) - Défaut
precision:haute    # Lent, très précis (2-5 sec)
precision:ultra    # Très lent, extrêmement précis (5-15 sec)
```

**Exemples:**
```bash
# Analyse rapide (pour preview)
gabriel> analyse image C:\image.png | precision:basse

# Analyse précise (pour publication)
gabriel> analyse image C:\image.png | precision:haute

# Analyse complète (pour recherche)
gabriel> analyse image C:\image.png | precision:ultra
```

---

### D. Paramètres de Tolérance

Contrôlez l'**acceptabilité des mesures**:

```bash
tolerance:0.5%    # Très strict (±0.5%)
tolerance:1%      # Strict (±1%) - Défaut
tolerance:5%      # Normal (±5%)
tolerance:10%     # Permissif (±10%)
```

**Exemples:**
```bash
# Pour une thèse (strict)
gabriel> analyse image C:\thesis_figure.png | precision:haute, tolerance:0.5%

# Pour une présentation (normal)
gabriel> analyse image C:\presentation.png | tolerance:5%

# Pour un brouillon (permissif)
gabriel> analyse image C:\draft.png | tolerance:10%, precision:basse
```

---

### E. Confiance Minimale

Contrôlez le **niveau de confiance exigé**:

```bash
confidence:60%     # Bas (détections faibles acceptées)
confidence:80%     # Normal - Défaut
confidence:90%     # Haut (détections fortes uniquement)
confidence:95%     # Très haut (uniquement certitudes)
```

**Exemples:**
```bash
# Accepter les détections floues
gabriel> analyse image C:\blurry.png | confidence:60%

# Haute confiance
gabriel> analyse image C:\clear.png | confidence:95%
```

---

### F. Formats d'Export

Spécifiez les **formats de sortie**:

```bash
export:json        # Format JSON structuré
export:python      # Code Python exécutable
export:latex       # Code LaTeX/TikZ
export:hol         # Code HOL/Isabelle
export:csv         # Données CSV (pour tables)
export:markdown    # Rapport Markdown
export:tous        # Tous les formats
```

**Exemples:**
```bash
# Export JSON uniquement
gabriel> analyse image C:\image.png | export:json

# Export code (Python et LaTeX)
gabriel> analyse image C:\image.png | export:python,latex

# Export tout
gabriel> analyse image C:\image.png | export:tous

# Export structuré pour intégration
gabriel> analyse image C:\matrix.png | export:json,csv
```

---

## 🎯 EXEMPLES COMPLETS RÉALISTES

### Exemple 1: Analyse Précise d'une Figure Théorique

**Situation:** Vous avez une figure pour votre thèse et voulez une analyse très précise

```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, graphique, precision:haute, tolerance:0.5%, confidence:95%, export:json,python,latex
```

**Ce que Gabriel fera:**
1. ✓ Analyse géométrique de haute précision
2. ✓ Détecte la parabole et les axes
3. ✓ Tolérance très stricte (±0.5%)
4. ✓ Accepte uniquement les détections très confiantes (95%)
5. ✓ Exporte en JSON, Python et LaTeX
6. ✓ Génère un rapport détaillé

**Durée:** ~5 secondes

**Résultat:** Vous obtenez du code prêt pour votre thèse!

---

### Exemple 2: Validation d'une Construction Géométrique

**Situation:** Vous avez dessiné un hexagone régulier et voulez le valider

```bash
gabriel> analyse image C:\schemas\hexagone_regulier.png ? regulier, symetrie, distance, angle, tolerance:1%
```

**Gabriel validera:**
- ✓ Tous les côtés égaux (régulier)
- ✓ Tous les axes de symétrie (6)
- ✓ Toutes les distances équidistantes
- ✓ Tous les angles = 120°
- ✓ Tolérance: ±1%

**Rapport:**
```
✓ VALIDATION GÉOMÉTRIQUE - HEXAGON RÉGULIER

Critères validés:
  ✓ Régularité: Confirmée (6 côtés égaux, tolérance 1%)
  ✓ Symétrie: 6 axes détectés
  ✓ Distance: Toutes égales (±1%)
  ✓ Angle: 6 × 120° (±1%)

Score conformité: 99.7%
```

---

### Exemple 3: Extraction Rapide de Données

**Situation:** Vous avez une matrice spectrale et voulez juste les données

```bash
gabriel> scan C:\data\matrice_spectrale_50x50.png :: precision:basse, export:csv,json, detect_text:true
```

**Gabriel fera:**
1. ✓ Détection rapide (basse précision = rapide)
2. ✓ Extraction OCR du texte
3. ✓ Export en CSV et JSON
4. ✓ Prêt en < 2 secondes

**Résultat:** Vous obtenez les données extraites immédiatement!

---

### Exemple 4: Analyse Complète Multi-Critères

**Situation:** Vous avez un schéma complexe et voulez tout analyser

```bash
gabriel> analyse image C:\schemas\spectral_diagram_complex.png | geometrie, graphique, diagramme, precision:haute, rayons, symetrie, angle, distance, export:tous, verbose
```

**Gabriel fera:**
1. ✓ Détecte toutes les formes géométriques
2. ✓ Extrait tous les graphiques/courbes
3. ✓ Reconnaît la structure du diagramme
4. ✓ Valide rayons, symétrie, angles, distances
5. ✓ Exporte en tous les formats
6. ✓ Affiche les détails de chaque étape (verbose)

**Rapport Complet:** Vous avez une analyse exhaustive!

---

### Exemple 5: Validation Sélective

**Situation:** Vous ne voulez valider que certains critères

```bash
gabriel> analyse image C:\triangle.png ? rayons, angle
```

**Gabriel validera UNIQUEMENT:**
- ✓ Les rayons (s'il y en a)
- ✓ Les angles
- ✗ Pas de vérification de symétrie
- ✗ Pas de vérification d'égalité des côtés

**Résultat:** Analyse ciblée et rapide!

---

## 📊 COMBINAISONS UTILES

### Pour la Recherche (Très Précis)
```bash
gabriel> analyse image C:\image.png | precision:ultra, tolerance:0.1%, confidence:99%, export:tous
```

### Pour l'Enseignement (Équilibré)
```bash
gabriel> analyse image C:\image.png | precision:haute, tolerance:2%, export:python,latex
```

### Pour la Production Rapide (Léger)
```bash
gabriel> analyse image C:\image.png | precision:basse, tolerance:5%, export:json
```

### Pour Validation Stricte
```bash
gabriel> analyse image C:\image.png | rayons, symetrie, angle, precision:haute, tolerance:0.5%, confidence:95%
```

### Pour Extraction de Données
```bash
gabriel> scan C:\data.png :: export:csv,json, detect_text:true, precision:moyenne
```

---

## 🔄 FLUX COMPLET D'UTILISATION

### Étape 1: Lancer Gabriel
```bash
C:\> python main_cli.py
gabriel> _
```

### Étape 2: Taper la commande avec critères
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, graphique, precision:haute, rayons, symetrie, export:json,python,latex,hol, tolerance:0.5%
```

### Étape 3: Gabriel analyse
```
[*] Parsing critères...
[*] Accès au fichier...
[*] Lecture image (1500×1000 px)...
[*] Analyse géométrique (précision: haute)...
[*] Détection des rayons...
[*] Validation symétrie...
[*] Génération code Python...
[*] Génération code LaTeX...
[*] Génération code HOL...
[*] Compilation rapport...
```

### Étape 4: Résultats affichés
```
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE AVANCÉE - GABRIEL MULTILOOP SYSTEM            │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE: quadrature_parabole_zero_critique.png

⚙️  CRITÈRES D'ANALYSE
   Types: geometrie, graphique
   Validation: rayons, symetrie
   Précision: haute
   Tolérance: 0.5%
   Export: json, python, latex, hol

📊 RÉSULTATS
   ✓ Rayons: 3 détectés
   ✓ Symétrie: 1 axe détecté
   ✓ Parabole: Détectée
   ✓ Points: 8 détectés
   
💾 EXPORTS GÉNÉRÉS
   ✓ JSON
   ✓ PYTHON (matplotlib)
   ✓ LATEX (tikz)
   ✓ HOL (isabelle)
```

### Étape 5: Utiliser les résultats
```bash
# Code Python prêt à exécuter
# Code LaTeX prêt pour votre document
# Code HOL prêt pour votre preuve formelle
# Données JSON pour intégration
```

---

## ✨ FONCTIONNALITÉS SPÉCIALES

### Mode Verbose (Détailed)
```bash
gabriel> analyse image C:\image.png | precision:haute, verbose
```

Affiche chaque étape de l'analyse en détail.

---

### Détection de Texte (OCR)
```bash
gabriel> analyse image C:\image.png | ocr, export:json
```

Extrait aussi le texte/labels de l'image.

---

### Sauvegarde Intermédiaire
```bash
gabriel> analyse image C:\image.png | intermediaire
```

Sauvegarde les étapes intermédiaires pour débogage.

---

### Génération Automatique de Rapport
```bash
gabriel> analyse image C:\image.png | rapport
```

Génère un rapport Markdown exportable.

---

## 🆘 DÉPANNAGE

### "Critères invalides"
Vérifiez la syntaxe:
```bash
# ❌ Mauvais (typo)
gabriel> analyse image C:\image.png | precisio:haute

# ✓ Bon
gabriel> analyse image C:\image.png | precision:haute
```

### "Fichier non trouvé"
Vérifiez le chemin:
```bash
# ❌ Mauvais (chemin incomplet)
gabriel> analyse image C:\image.png

# ✓ Bon (chemin complet)
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature.png
```

### Analyse trop lente
Réduisez la précision:
```bash
# Au lieu de
gabriel> analyse image C:\image.png | precision:ultra

# Utilisez
gabriel> analyse image C:\image.png | precision:moyenne
```

---

## 📝 RÉSUMÉ DES SYNTAXES

| Syntaxe | Usage | Exemple |
|---------|-------|---------|
| Pipe (\|) | Recommandée | `analyse image C:\path\img.png \| geometrie, precision:haute` |
| Question (?) | Intuitive | `analyse C:\path\img.png ? rayons, symetrie` |
| Double-Colon (::) | Technique | `scan C:\path\img.png :: precision:ultra, tolerance:0.5%` |

---

## 🎉 VOUS ÊTES PRÊT!

Vous pouvez maintenant:
- ✅ Analyser des images avec **précision contrôlée**
- ✅ Valider des **critères spécifiques**
- ✅ Exporter dans **n'importe quel format**
- ✅ Adapter Gabriel à vos **besoins exacts**

**Commencez avec:**
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, precision:haute, rayons, symetrie, export:json,python,latex
```

Vous obtenez une analyse **complète, précise et prête à utiliser**! 🚀
