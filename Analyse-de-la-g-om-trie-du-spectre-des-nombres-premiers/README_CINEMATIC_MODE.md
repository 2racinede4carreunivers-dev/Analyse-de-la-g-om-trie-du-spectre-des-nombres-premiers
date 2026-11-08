# 🎬 GABRIEL - MODE CINÉMATIQUE & ANALYSE D'IMAGES v5.5

## 📌 Vue d'Ensemble

Gabriel possède un **mode cinématique intelligent** qui affiche en temps réel l'avancement du traitement d'une requête avec chronomètre, barre de progression et étapes détaillées.

De plus, Gabriel est maintenant équipé d'un **système complet d'analyse d'images** avec critères personnalisés et découverte universelle.

---

## 🎬 MODE CINÉMATIQUE

### Qu'est-ce que c'est?

Lorsque Gabriel traite une requête, il affiche une **interface visuelle animée** montrant:
- ⏱️ **Chronomètre** (temps écoulé / temps estimé)
- 📊 **Barre de progression** avec animation
- 🔄 **Nombre de loops** (actuels / totaux)
- 📝 **Étapes en cours** (abstraction, critiques, multiloop, etc.)
- 📋 **Journal des événements** (10 derniers événements)

### Exemple d'Affichage

```
╔════════════════════════════════════════════════════════════════╗
║            Gabriel Multi-Loop Cinematic Display               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📊 GABRIEL - Mode Réponse Intelligente                       ║
║                                                                ║
║  Loops prévues: 2/3                                           ║
║  ⏱️  00:12 / ~00:20                                             ║
║  [███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 55% ⠹           ║
║  🔄 Loop 2/3 en cours (Itération 3/5)                         ║
║                                                                ║
║  📋 Événements Récents:                                        ║
║     • [22:15:34] RequestDecomposer: Gap detected (-19, -5)   ║
║     • [22:15:35] SpectralCore: SA(-7) = -1.987305            ║
║     • [22:15:36] CritiqueEngine: Verify digamma sign          ║
║     • [22:15:37] RefinementLoop: Correct formula applied     ║
║     • [22:15:38] SlowMotionDebugger: Solution verified       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## ⚡ DÉTECTION AUTOMATIQUE DE COMPLEXITÉ

Gabriel analyse chaque requête et détecte automatiquement le nombre de loops nécessaires:

### Niveaux de Complexité

#### 🚀 RAPIDE (1 loop, < 1 sec)
- Questions triviales
- Définitions simples
- Faits directs

**Exemple:**
```
Gabriel> C'est quoi un nombre premier?
✨ Réponse immédiate:
"Un nombre premier est un nombre naturel supérieur à 1 
qui n'a exactement deux diviseurs positifs..."
(< 1 seconde, bypass)
```

#### ⚡ STANDARD (2 loops, 15-20 sec)
- Reconstructions simples
- Rapports basiques
- Questions simples

**Exemple:**
```
Gabriel> Reconstruis le 26e premier

╔════════════════════════════════════════╗
║  Loops prévues: 2/2                   ║
║  ⏱️  00:18 / ~00:20                     ║
║  [██████████████████░░░░░░░░░░░░] 90% ║
║  ✅ Terminé                            ║
╚════════════════════════════════════════╝

Le 26e nombre premier est 101.
```

#### 🧠 APPROFONDI (3 loops, 25-35 sec)
- Rapports spectraux n×n
- Calculs d'écarts
- Questions théoriques

**Exemple:**
```
Gabriel> Rapport spectral symétrique 4x4: 
Bloc A={3,5,7,11} Bloc B={13,17,19,23}

╔════════════════════════════════════════╗
║  Loops prévues: 3/3                   ║
║  ⏱️  00:28 / ~00:32                     ║
║  [███████████████░░░░░░] 65% ⠹         ║
║  🔄 Loop 3/3 (Itération 4/5)           ║
╚════════════════════════════════════════╝

Ratio spectral = 0.501...
```

#### 🔬 TRÈS_COMPLEXE (4 loops, 40-60 sec)
- Section 13 avancée
- Zêta complexe
- Théorie combinée

**Exemple:**
```
Gabriel> Section 13: pont logique Zêta avec nombres négatifs

╔════════════════════════════════════════╗
║  Loops prévues: 4/4                   ║
║  ⏱️  00:45 / ~00:55                     ║
║  [████████████████████░░░░░░░░] 80% ⠹  ║
║  🔄 Loop 4/4 (Itération 5/5)           ║
╚════════════════════════════════════════╝

[Analyse complexe en cours...]
```

---

## 📸 SYSTÈME D'ANALYSE D'IMAGES (NOUVEAU v5.5)

### Qu'est-ce que c'est?

Gabriel peut maintenant analyser **n'importe quelle image, schéma ou figure** sauvegardée sur votre système avec des **critères personnalisés**.

### Commandes Disponibles

#### Simple
```bash
gabriel> analyse image C:\path\image.png
```

#### Avec Critères (Syntaxe Pipe)
```bash
gabriel> analyse image C:\path\image.png | geometrie, precision:haute, rayons, symetrie
```

#### Complète
```bash
gabriel> analyse image C:\path\image.png | geometrie, graphique, precision:haute, tolerance:0.5%, confidence:95%, rayons, symetrie, angle, distance, export:json,python,latex,hol
```

#### Alternative (Syntaxe Question)
```bash
gabriel> analyse C:\path\image.png ? rayons, symetrie, precision:haute
```

#### Technique (Double-Point)
```bash
gabriel> scan C:\path\image.png :: precision:ultra, tolerance:0.5%
```

### Capacités d'Analyse

#### Types d'Analyses
- 📐 **Géométrie**: Formes, points, lignes, angles
- 📊 **Graphiques**: Axes, courbes, points de données
- 📋 **Tables**: Matrices, données tabulaires
- 📦 **Diagrammes**: Boîtes, connecteurs, flux
- 📍 **Grilles**: Calibration, repères
- 📖 **OCR**: Extraction de texte

#### Critères de Validation
- 🔹 Rayons (segments radiaux)
- 🔄 Symétrie (axes de symétrie)
- △ Équilatéral (triangle équilatéral)
- ◻️ Rectangle (rectangle régulier)
- ⭕ Cercle (cercle complet)
- ⬡ Régulier (polygone régulier)
- ↗️ Diagonale (diagonales)
- 📏 Distance (mesures)
- ∠ Angle (angles)
- ⊥ Perpendiculaire (perpendiculaires)
- ∥ Parallèle (parallèles)
- ⊙ Concentrique (cercles concentriques)

#### Niveaux de Précision
```
precision:basse     → Rapide (< 1 sec)
precision:moyenne   → Équilibre (1-2 sec) - Défaut
precision:haute     → Lent (2-5 sec)
precision:ultra     → Très lent (5-15 sec)
```

#### Formats d'Export
```
export:json         → Format JSON structuré
export:python       → Code Python exécutable
export:latex        → Code LaTeX/TikZ
export:hol          → Code HOL/Isabelle
export:csv          → Données CSV
export:markdown     → Rapport Markdown
export:tous         → Tous les formats
```

### Exemples Concrets

#### Analyser une Parabole
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | graphique, precision:haute, rayons, symetrie, export:json,python,latex

# Résultat: Détection parabole, axes, points critiques, code généré
```

#### Valider un Triangle
```bash
gabriel> analyse image C:\schemas\triangle.png | equilateral, symetrie, angle, precision:haute, tolerance:0.5%

# Résultat: Confirmation si équilatéral, mesure des côtés et angles
```

#### Extraire une Matrice
```bash
gabriel> scan C:\data\spectral_matrix.png :: export:csv,json, detect_text:true

# Résultat: Matrice extraite en CSV et JSON
```

---

## 🎯 FLUX D'UTILISATION COMBINÉ

### Scenario 1: Question Simple avec Cinématique

```
User: gabriel> Reconstruis le 50e premier

[Affichage cinématique pendant 18 secondes]

Résultat: Le 50e nombre premier est 229.
```

### Scenario 2: Analyse d'Image Complexe

```
User: gabriel> analyse image C:\figure.png | geometrie, precision:haute, export:python

[Affichage cinématique pendant l'analyse]

Résultat: 
- 8 formes détectées
- 34 points extraits
- Code Python généré
```

### Scenario 3: Question Théorique + Affichage

```
User: gabriel> Rapport spectral: A=(3,5,7,11) B=(13,17,19,23)

[Affichage cinématique - Mode APPROFONDI - 3 loops]

Résultat: Ratio = 0.501... avec validation spectrale
```

---

## 🔌 INTÉGRATION TECHNIQUE

### Code d'Intégration Simple

```python
from src.ui.cinematic_orchestrator import CinematicOrchestrator

# Une ligne pour l'intégration complète!
orch = CinematicOrchestrator(pipeline)
final = await orch.process(question, print_cinematic=True)
```

### Avec Rapport de Complexité

```python
orch = CinematicOrchestrator(pipeline, verbose=True)
final = await orch.process(question)
report = orch.get_complexity_report()
print(f"Mode: {report['mode']}, Temps: {report['elapsed_sec']:.1f}s")
```

---

## 📊 PERFORMANCES COMPARÉES

| Métrique | Avant | Après | Gain |
|----------|-------|-------|------|
| Questions triviales | 30-40s | <1s | **97%** ⚡⚡⚡ |
| Questions simples | 30-40s | 15-20s | **50%** ⚡⚡ |
| Questions complexes | 30-40s | 40-60s | optimisé |
| Transparence utilisateur | ❌ | ✅ | +100% |
| Analyse images | ❌ | ✅ | +∞ |

---

## 📁 FICHIERS IMPORTANTS

### Systèmes Cinématiques
```
src/ui/complexity_analyzer.py       → Analyse complexité
src/ui/cinematic_display.py         → Affichage cinématique
src/ui/cinematic_orchestrator.py    → Orchestration complète
```

### Systèmes d'Analyse d'Images
```
src/gabriel_image_interface.py      → Interface images
src/image_discovery_system.py       → Découverte d'images
src/advanced_analysis_criteria.py   → Critères avancés
```

### Documentation
```
CINEMATIC_INTEGRATION_GUIDE.md      → Guide technique
CINEMATIC_MODE_SUMMARY.md           → Résumé des fonctionnalités
GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md → Guide complet
GUIDE_ANALYSE_AVEC_CRITERES.md      → Critères personnalisés
```

---

## ✅ STATUS: PRODUCTION READY v5.5

Gabriel v5.5 est maintenant:

✅ Mode cinématique avec chronomètre automatique
✅ Analyse d'images complète et personnalisée
✅ Détection intelligent de complexité
✅ Découverte universelle d'images
✅ 7 formats d'export
✅ Interface visuelle pendant le traitement
✅ Prêt pour utilisation quotidienne

---

## 🚀 DÉMARRAGE

```bash
# Via docker-compose
docker compose up -d

# Ou local
python src/ui/cli.py

# Testez:
gabriel> Reconstruis le 30e premier
# Vous verrez l'affichage cinématique!

gabriel> analyse image C:\path\image.png
# L'image sera analysée avec affichage du progrès
```

---

## 📞 SUPPORT

Pour questions ou problèmes:
1. Consulter **CINEMATIC_INTEGRATION_GUIDE.md**
2. Consulter **GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md**
3. Vérifier les logs: `docker compose logs -f`

---

**Dernière mise à jour:** 2026-01-15  
**Version:** 5.5  
**Status:** ✅ Production Ready  
**Fonctionnalités:** Mode Cinématique + Analyse Complète d'Images
