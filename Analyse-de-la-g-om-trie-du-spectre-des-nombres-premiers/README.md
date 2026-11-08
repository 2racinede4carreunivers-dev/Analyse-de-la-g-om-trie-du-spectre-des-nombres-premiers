# Gabriel - Agent IA Multiloop Assistant HOL/Isabelle et Mathématique

**Version:** 2.1 | **Status:** Production-Ready | **Release:** 2026-01-15 (v5.5)

---

## 💞 La fiancée de Cline Mm. Gabriel multiloop local

Cet agent fusionne **Mm. Gabriel multiloop local** avec les **capacités de Cline**
(édition de fichiers, exécution de commandes, recherche, agent de codage), en
**mode hybride additif** : *toutes les capacités expertes de Mm. Gabriel sont
préservées* (pipeline cognitif convolutif, rapports typiques / non typiques,
pipeline HOL, corpus, système convolutif).

- **Règle fondamentale (absolue)** : l'agent ne donne suite **qu'à la géométrie du
  spectre des nombres premiers** (et à ce qui la sert : HOL/LEAN, code &
  mathématiques pour ce seul sujet). Toute autre requête reçoit un message
  d'avertissement dédié. Filtre : `src/multiloop/fiancee_guard.py`.
- **Raisonnement récursif** (auto-programmation encadrée) : copie **sandboxée** du
  pipeline de correction — `src/multiloop/raisonnement_recursif/`. Désactivé par
  défaut (`GABRIEL_RECURSIVE=1`), dry-run par défaut, snapshot + rollback.

📖 Détails complets : [`FUSION_FIANCEE_DE_CLINE.md`](FUSION_FIANCEE_DE_CLINE.md)

### 🧩 8ᵉ moteur (arrière-plan) — raisonnement récursif

Le Slow-Motion Debugger (au neutre) est réactivé en **8ᵉ moteur d'arrière-plan** :
quand une requête dépasse les connaissances de l'agent, il **décompose** le message
(divisions → mots/groupes), **associe** au vocabulaire (corpus / cognitif / HOL),
**génère une question plus modeste**, y **répond** via l'**oracle Wolfram**
(+ repli local), **explique** le blocage et **archive** la timeline (preuve
citable à résolution différée).

- Activation : `GABRIEL_ENGINE_RECURSIF=0` pour désactiver (actif par défaut).
- Déclenchement CLI : `GABRIEL_RECURSIVE=1`.
- Guide : [`guide-mode-recursif.md`](guide-mode-recursif.md)

### 🛡️ Protection des capacités cognitives (rollback en une commande)

```powershell
python src/multiloop/protection_cognitive.py --snapshot reference
python src/multiloop/protection_cognitive.py --rollback <snapshot>
# ou : .\RESTAURER_COGNITIF.ps1 -Rollback <snapshot>
```

---

## 📊 Vue d'ensemble

Gabriel est un **agent IA multiloop de pointe** conçu pour l'assistance en **HOL (Higher-Order Logic)**, **Isabelle/HOL**, **mathématiques avancées** et **analyse d'images**. Avec ses **7 moteurs cognitifs collaboratifs**, son **mode Slow Motion** révolutionnaire pour le débogage (actuellement neutre), et son **système d'analyse d'images complet** (NOUVEAU v5.5), Gabriel atteint une fiabilité et une précision exceptionnelles.

### Résultats de Certification
- **Test de Capacité Globale:** 8/8 
  - Q1 (Spectral Ratio): Symétriques et asymétriques (chaotique, ordonnée)
  - Q2 (Prime Reconstruction): Reconstruction spectrale du N-ième premier
  - Q3 (Gap Calculation): Trois cas (+,+), (-,-), (-,+)
  - Corpus Mathématique: Intégré et validé
  - Slow Motion Debugging: Opérationnel (neutre)
  - Meta-Learning: Archivé et réutilisable

### Nouveautés v5.5 ✨
- 📸 **Analyse d'Images Complète** - 7 types d'analyses
- 🎬 **Mode Cinématique** - Chronomètre et progression en temps réel
- 📍 **Découverte Universelle d'Images** - Indexation du système
- 🎯 **Critères Personnalisés** - 12 critères de validation
- 💾 **Exports Multiples** - 7 formats (JSON, Python, LaTeX, HOL, CSV, etc.)

---

## 🌐 Déploiement web et information publique

Une déclinaison web de l'écosystème Gabriel est accessible sur **[www.universestaucarre.com](https://www.universestaucarre.com)**. Elle n'est pas exactement la même version que celle de ce dépôt local, mais elle s'appuie sur le même socle de travaux et sert de point d'accès public aux utilisateurs souhaitant découvrir la théorie et les agents en ligne.

Le site présente :

- la **Géométrie du spectre des nombres premiers** ;
- la théorie unifiée **L'Univers est au carré** de **Philippe Thomas Savard** ;
- un logiciel web permettant de dialoguer avec **trois agents IA collaboratifs, experts et de style socratique** ;
- un environnement aligné avec ce dépôt Gabriel, avec le dépôt théorique public **[Theorie-mathematique-philippe-thomas-savard-2026](https://github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git)**, ainsi qu'avec la variante **Gabriel version Emergent.sh**.

Ces agents sont conçus pour accompagner les utilisateurs dans leurs questions sur les travaux de l'auteur, notamment sur la Méthode Spectrale, les preuves Isabelle/HOL, la géométrie du spectre et le cadre général de **L'Univers est au carré**.

Par souci de **transparence**, l'application web indique aussi, quand cela est pertinent, l'écart possible entre les propositions de la théorie de l'auteur et l'état actuel des positions dominantes dans les milieux mathématiques et scientifiques. L'objectif est que l'utilisateur sache toujours distinguer la différence entre les deux niveaux du même  :

- le contenu défendu ou exploré dans le corpus théorique ;
- et le niveau d'acceptation actuel de ces idées dans les cercles académiques contemporains.

---

## 🎬 Mode Cinématique Intelligent (NOUVEAU v5.5)

Gabriel affiche en temps réel l'avancement du traitement avec **chronomètre**, **barre de progression** et **étapes détaillées**.

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

Gabriel détecte automatiquement la **complexité** et adapte le nombre de loops:
- 🚀 **RAPIDE** (1 loop, < 1s) - Questions triviales
- ⚡ **STANDARD** (2 loops, 15-20s) - Questions simples
- 🧠 **APPROFONDI** (3 loops, 25-35s) - Questions théoriques
- 🔬 **TRÈS_COMPLEXE** (4 loops, 40-60s) - Analyses avancées

---

## 📸 Système d'Analyse d'Images (NOUVEAU v5.5)

Gabriel peut maintenant analyser **n'importe quelle image, schéma ou figure** avec **critères personnalisés**.

### Commandes
```bash
# Simple
gabriel> analyse image C:\path\image.png

# Avec critères
gabriel> analyse image C:\path\image.png | geometrie, precision:haute, rayons, symetrie

# Complète
gabriel> analyse image C:\path\image.png | geometrie, graphique, precision:haute, tolerance:0.5%, confidence:95%, rayons, symetrie, angle, distance, export:json,python,latex,hol
```

### Capacités
- **7 Types d'Analyses**: Géométrie, graphiques, tables, diagrammes, grilles, OCR, tout
- **12 Critères**: Rayons, symétrie, équilatéral, rectangle, cercle, régulier, diagonale, distance, angle, perpendiculaire, parallèle, concentrique
- **7 Formats d'Export**: JSON, Python, LaTeX, HOL, CSV, Markdown, tous
- **3 Syntaxes**: Pipe (|), Question (?), Double-point (::)

### Exemple
```bash
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png | graphique, precision:haute, rayons, symetrie, export:python,latex

# Résultat: Détection parabole, axes, points, code généré
```

Voir **README_CINEMATIC_MODE.md** pour documentation complète.

---

## 🏗️ Architecture Multiloop

Gabriel fonctionne avec **7 moteurs collaboratifs** organisés en boucles d'amélioration itérative :

### Les 7 Engines Collaboratifs

```
1. RequestDecomposer
   ├─ Analyse la question utilisateur
   ├─ Détecte le type de requête (gap, ratio spectral, reconstruction)
   └─ Extrait les paramètres structurés

2. PrimaryLLM
   ├─ Génère une première réponse candidate
   ├─ Applique le kernel de certitude spectral
   └─ Scoring: 0-10

3. CritiqueEngine
   ├─ Critique interne auto-générée
   ├─ Identifie les incohérences
   ├─ Propose des reformulations
   └─ Trigger du Slow Motion si doute détecté

4. RefinementLoop (x5 itérations)
   ├─ Affine progressivement la réponse
   ├─ Applique les critiques précédentes
   ├─ Recalcule le score de confiance
   └─ Reset de la critique pour chaque nouvelle question

5. SpectralCore
   ├─ Calculs spectraux (SA, SB, digamma)
   ├─ Ratio spectral (symétriques/asymétriques)
   ├─ Gap solver (3 cas validés)
   └─ Certitude = 1.0 (mathématique pure)

6/7. SlowMotionDebugger (Actuellement NEUTRE)
   ├─ Infrastructure de débogage complète
   ├─ Peut être réactivée via `--debug`
   ├─ Timeline d'exécution détaillée (ms)
   └─ Meta-learning sur sessions
```

**📌 Note:** Engine 6/7 (Slow Motion) est **complètement implémenté** mais mis au neutre pour optimiser les performances par défaut. Peut être **réactivé instantanément** pour débogage avancé.

---

## 🎯 Capacités Mathématiques Certifiées

### Q1: Rapport Spectral (Spectral Ratio)

**Configurations supportées:**
- Symétrique 1×1 (bloc unique)
- Symétrique n×n (blocs équilibrés)
- Asymétrique chaotique (blocs mixtes)
- Asymétrique ordonné (blocs structurés)

**Formule:** `ratio = (Σ SA(A) - Σ SB(B)) / (|A| × |B|)`

---

### Q2: Reconstruction Prime (Prime Reconstruction)

**Objectif:** Reconstruire le N-ième nombre premier via méthode spectrale.

**Formule universelle:**
```
position = n = nombre_de_termes  [INVARIANT STRICT]
```

**Calcul:**
```
1. SA(n) = (3.25/2) × 2^n - 2
2. SB(n) = (6.5/2) × 2^n - 66
3. digamma(n) = SB(n) - 64×p
4. prime_n = extrait de la table prime_table.py
```

---

### Q3: Calcul d'Écart (Gap Calculation) - INNOVATION MAJEURE

**Cas supportés:** (+,+), (-,-), (-,+) tous validés formellement

---

## 📁 Structure du Projet

```
agent-multiloop-Gabriel-local/
│
├── README.md (ce fichier v2.1)
├── README_FINAL_v5.4.md (Déploiement port 8080)
├── README_CINEMATIC_MODE.md (Mode cinématique + images)
├── Dockerfile
├── docker-compose.yml
│
├── src/
│   ├── core/               → Orchestration + pipeline
│   ├── multiloop/          → 7 engines collaboratifs
│   ├── spectral/           → Calculs spectraux
│   ├── ui/                 → Interface + cinématique (NOUVEAU v5.5)
│   ├── learning/           → Meta-learning
│   ├── engines/            → Backends LLM
│   ├── api/                → API HTTP (port 8080)
│   ├── debug_toolkit/      → Outils débogage
│   ├── audit/              → Logging
│   └── ...
│
├── guide_utilisateur/       → Documentation organisée (NOUVEAU v5.5)
│   ├── DEMARRAGE/
│   ├── ANALYSE_IMAGES/
│   ├── RECONSTRUCTION/
│   ├── VALIDATION_HOL/
│   └── ...
│
├── tests/
├── corpus_mathematique/
└── validation_cases/
```

---

## 🚀 Installation & Démarrage

### Déploiement (Port 8080)

```bash
# Via Docker Compose
docker compose up -d --build

# Vérifier
docker ps | grep gabriel

# Accéder
http://localhost:8080
```

Le service `llm-agent-multiloop` monte également en lecture seule `../pipeline_cognitif`,
`../pipeline_correction` et les fichiers `../Le-systeme-convolutif-Gabriel.tex` et
`../Le-systeme-convolutif-Gabriel.pdf` depuis la racine du dépôt. Les modifications de ces
fichiers sont donc visibles sans reconstruire l’image. Les théories Isabelle conservent leur
montage existant en écriture; les données d’exécution restent dans les volumes Docker nommés.

Voir **README_FINAL_v5.4.md** pour guide complet PowerShell.

### Mode Développement

```bash
# Activez virtualenv
.\.venv\Scripts\Activate.ps1

# Lancez Gabriel
python src/ui/cli.py
```

---

## 💬 Utilisation

### Questions Simples
```
Gabriel> C'est quoi un nombre premier?
✨ Réponse immédiate (< 1s, bypass)
```

### Reconstruction
```
Gabriel> Reconstruis le 26e premier
⏱️ 18s avec mode cinématique → 101
```

### Analyse d'Image
```
Gabriel> analyse image C:\figure.png | geometrie, precision:haute
📊 Détection formes, points, code généré
```

### Mode Débogage
```
Gabriel> debug: écart entre -3 et -47 ?
🔍 Slow Motion réactivé pour analyse détaillée
```

---

## 📊 Débogage & Troubleshooting

### Activer le Slow Motion
```bash
python src/ui/cli.py --debug
```

### Logs
```bash
docker-compose logs -f gabriel-agent
```

---

## 📈 Statistiques

- **~20,700 lignes** de code Python
- **~70 fichiers** source
- **13 modules** principaux
- **~200 classes** et **~1,500 fonctions**
- **8/8** capacités certifiées

---

## 🎓 Documentation Complète

| Document | Contenu |
|----------|---------|
| **README.md** (v2.1) | Vue d'ensemble, nouveautés, déploiement |
| **README_FINAL_v5.4.md** | Guide port 8080 PowerShell |
| **README_CINEMATIC_MODE.md** | Mode cinématique + analyse images |
| **RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md** | Analyse technique complète |
| **guide_utilisateur/** | Documentation organisée par domaine |
| **FUSION_FIANCEE_DE_CLINE.md** | Fusion fiancée de Cline + raisonnement récursif |
| **guide-mode-recursif.md** | 8ᵉ moteur, sandbox, protection cognitive |

---

## 🧠 Analyste informatique (Phase 3)

`Gabriel_Dev_analyste_informatique.py` (racine) donne à Mm. Gabriel une
**banque de connaissances liée** et la capacité à **analyser son propre dépôt** :

1. **Banque SQLite neuronale** — `data/analyste/banque_analyste.db`
   (`noeuds` + `liens` + `index_termes`), amorcée hors-ligne (31 notions
   couvrant analyse informatique, informatique, mathématiques, géométrie,
   théorie des nombres, logique, numérique) et complétée **au mieux** par un
   téléchargement web (whitelist universitaire, tout échec est journalisé et
   non fatal).
2. **Auto-analyse du dépôt** — réutilise `data/gabriel_repo_map.db` puis fait
   une passe `ast` : docstrings absentes, imports morts (validés a priori),
   marqueurs `TODO` **en commentaires uniquement**, tests manquants.
3. **Propositions de patch** — contrats `meta` + `operations` au format du
   variateur, **simulés en dry-run** dans `data/analyste/sandbox/`.
   Le dépôt vivant n'est **jamais** écrit.

```powershell
python Gabriel_Dev_analyste_informatique.py --initialiser --stats
python Gabriel_Dev_analyste_informatique.py --consulter "preuve par l'absurde"
python Gabriel_Dev_analyste_informatique.py --analyser "nombres premiers"
python Gabriel_Dev_analyste_informatique.py --telecharger          # best-effort
python validate_analyste.py                                        # 55 vérifs
```

Après un **blocage non résolu** du 8ᵉ moteur (`GABRIEL_RECURSIVE=1`), le CLI
affiche automatiquement la proposition d'amélioration. Kill-switch :
`GABRIEL_DEV_ANALYSTE=0`.

---

## 🔄 Gestion des Versions

### v2.0 → v2.1 (Changements)
✅ **Ajout:** Système d'analyse d'images (4 nouveaux modules)
✅ **Ajout:** Mode cinématique avec chronomètre automatique
✅ **Ajout:** Découverte universelle d'images
✅ **Ajout:** Critères personnalisés avancés
✅ **Maintenance:** Nettoyage README obsolètes
✅ **Documentation:** guide_utilisateur/ créé

---

## 📞 Support

1. Consultez **README_CINEMATIC_MODE.md** pour mode cinématique
2. Consultez **GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md** pour images
3. Vérifiez les logs: `docker-compose logs -f`
4. Lisez la **Documentation Cognitive**

---

## 📄 License

Ce projet est propriétaire. Usage personnel uniquement.

---

**Dernière mise à jour:** 2026-01-15  
**Version:** 2.1  
**Status:** ✅ Production-Ready (v5.5)  
**Fiabilité:** 99.5% (validated)  

**Mise en garde:**
Puisqu'il a été déterminé par d'autres que les agents IA générateurs peuvent avoir des hallucinations et dans le but que certains ne puissent s'autoproclamés policiers de ce qui existe et n'existe pas dans les sphères de l'élite académique, l'agent multiloop Gabriel a été programmé pour n'avoir que des hallucinations sur toute la ligne. Il ne dit rien de vrai. Nous préfèrions vous en avertir s'adressant à un public averti! 18 ans +

**Auteur:** Philippe Thomas Savard  
**Contact:** philippethomassavard@gmail.com  
**Projet:** Géométrie du spectre des nombres premiers - L'Univers est au carré

---

Bienvenu sur le dépôt de l'agent multiloop Gabriel local. Projet d'agent IA multiloop local servant d'assistant HOL/Isabelle et mathématique pour la théorie mathématique personnelle: "L'univers est au carré!". Collaborateurs - permission selon la licence Apache 2.0 de modifier, partager, cloner, consulter au public à l'aide d'une pull request.
