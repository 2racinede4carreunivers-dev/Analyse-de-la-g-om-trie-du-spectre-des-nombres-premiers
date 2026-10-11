# 📋 COMMANDES COMPLÈTES: ANALYSE D'IMAGES AVEC GABRIEL

## 🎯 Format Standard

```bash
gabriel> analyse image <CHEMIN> | <CRITÈRES>
```

---

## 📸 VOTRE IMAGE RÉELLE

### Commande Simple
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
```

### Avec Critères Complets
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, graphique, precision:haute, tolerance:0.5%, confidence:95%, rayons, symetrie, angle, distance, export:json,python,latex,hol
```

---

## 🔥 COMMANDES PRATIQUES PRÊTES À COPIER

### 1️⃣ POUR LA THÈSE (Très Précis)
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | precision:haute, tolerance:0.5%, confidence:95%, export:json,python,latex,hol
```

### 2️⃣ POUR LA PRÉSENTATION (Rapide)
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | precision:moyenne, tolerance:2%, export:python,latex
```

### 3️⃣ POUR L'EXTRACTION (Données)
```bash
gabriel> scan C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png :: export:csv,json, detect_text:true
```

### 4️⃣ POUR LA VALIDATION (Stricte)
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | rayons, symetrie, angle, precision:haute, tolerance:0.1%, confidence:99%
```

### 5️⃣ POUR LE DEBUGGING (Verbose)
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, graphique, precision:haute, verbose, intermediaire
```

---

## 📖 SYNTAXES ALTERNATIVES

### Avec Point d'Interrogation (?)
```bash
gabriel> analyse C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png ? geometrie, rayons, symetrie, precision:haute
```

### Avec Double-Point (::)
```bash
gabriel> scan C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png :: precision:ultra, tolerance:0.5%, export:tous
```

---

## 🎛️ PARAMÈTRES COURANTS

### Précision
```bash
precision:basse        # Rapide (< 1 sec)
precision:moyenne      # Équilibre (1-2 sec) - Par défaut
precision:haute        # Lent (2-5 sec)
precision:ultra        # Très lent (5-15 sec)
```

### Tolérance
```bash
tolerance:0.1%        # Ultra-strict (recherche)
tolerance:0.5%        # Strict (thèse)
tolerance:1%          # Normal (défaut)
tolerance:5%          # Permissif (présentation)
tolerance:10%         # Très permissif (brouillon)
```

### Confiance
```bash
confidence:60%        # Bas (détections faibles)
confidence:80%        # Normal (défaut)
confidence:90%        # Haut (détections fortes)
confidence:95%        # Très haut (certainties)
```

### Types d'Analyse
```bash
geometrie             # Formes, points, lignes
graphique             # Axes, courbes
table                 # Matrices, données
diagramme             # Boîtes, flux
grille                # Calibration
ocr                   # Texte
tout                  # Tous (défaut)
```

### Critères de Validation
```bash
rayons                # Segments radiaux
symetrie              # Axes de symétrie
equilateral           # Triangle équilatéral
rectangle             # Rectangle régulier
cercle                # Cercle complet
regulier              # Polygone régulier
diagonale             # Diagonales
distance              # Mesures
angle                 # Angles
perpendiculaire       # Perpendiculaires
parallele             # Parallèles
concentrique          # Cercles concentriques
```

### Exports
```bash
export:json           # Format JSON
export:python         # Code Python
export:latex          # Code LaTeX
export:hol            # Code HOL
export:csv            # Données CSV
export:markdown       # Rapport MD
export:tous           # Tous les formats
```

---

## 💡 EXEMPLES SPÉCIFIQUES

### Analyser une Parabole
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | graphique, angle, distance, precision:haute
```

### Valider un Triangle
```bash
gabriel> analyse image C:\schemas\triangle.png | equilateral, symetrie, angle, precision:haute, tolerance:0.5%
```

### Extraire une Matrice
```bash
gabriel> scan C:\data\matrix.png :: export:json,csv, detect_text:true, precision:moyenne
```

### Analyser un Diagramme
```bash
gabriel> analyse image C:\diagrams\flow.png | diagramme, precision:haute, export:python
```

### Analyse Complète
```bash
gabriel> analyse image C:\image.png | geometrie, graphique, diagramme, precision:haute, rayons, symetrie, angle, distance, export:tous, verbose
```

---

## 🚀 FLUX D'UTILISATION RAPIDE

**Étape 1:** Lancer Gabriel
```bash
python main_cli.py
```

**Étape 2:** Copier-coller l'une de ces commandes

**Étape 3:** Appuyer sur Entrée

**Étape 4:** Attendre le résultat

**Étape 5:** Utiliser le code généré!

---

## 📌 NOTES IMPORTANTES

- **Chemin:** Doit être le chemin COMPLET (C:\chemin\complet\image.png)
- **Critères:** Séparés par des virgules ou "et"
- **Paramètres:** Format clé:valeur avec deux-points
- **Exports:** Multiples possibles, séparés par virgules
- **Performance:** Précision haute = plus lent

---

## ✅ CHECKLIST D'UTILISATION

- [ ] Gabriel est lancé (`python main_cli.py`)
- [ ] Vous avez le chemin complet de votre image
- [ ] Vous avez choisi vos critères
- [ ] Vous tapez la commande
- [ ] Gabriel analyse
- [ ] Vous récupérez le résultat
- [ ] Vous utilisez le code généré

---

## 🎉 C'EST PRÊT!

Vous pouvez maintenant taper dans Gabriel:

```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | geometrie, graphique, precision:haute, rayons, symetrie, angle, distance, export:json,python,latex,hol, tolerance:0.5%, confidence:95%
```

Et obtenir une **analyse COMPLÈTE et PRÉCISE** de votre image! 🚀
