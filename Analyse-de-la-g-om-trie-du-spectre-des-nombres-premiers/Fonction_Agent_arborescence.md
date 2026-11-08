# Gabriel — arborescence des composants et test de continuité

## Périmètre

Cette carte décrit les principaux dossiers du dépôt
`Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers`. Elle montre les
liaisons fonctionnelles, pas l'inventaire des fichiers. Les simulations
suivent les chemins du code local; elles ne constituent pas une validation
mathématique indépendante ni un test complet de déploiement.

## Arborescence fonctionnelle

```text
Dépôt Gabriel
│
├── main_cli.py / main.py
│   └── démarrage de l'agent
│       ↓
├── src/ui/
│   ├── interaction en ligne de commande
│   └── routage des commandes, notamment image et corpus
│       ↓
├── src/core/
│   ├── orchestrateur et pipeline de question-réponse
│   ├── planification, configuration et mémoire
│   └── raccordement calcul spectral, corpus et réponse finale
│       ↓
├── src/multiloop/
│   ├── décomposition et pré-raisonnement
│   ├── critique, vérification et raffinement
│   └── raisonnement récursif d'arrière-plan (optionnel)
│
├── src/cognitive/
│   └── traces, provenance et méta-raisonnement
│
├── src/engines/
│   ├── abstraction
│   ├── méta-raisonnement et planification de preuve
│   ├── navigation conceptuelle
│   ├── généralisation
│   ├── découverte de théorèmes
│   └── vérification numérique
│
├── src/spectral/
│   └── modèles spectraux, suites, rapports, reconstruction et Digamma
│       ↓
├── pipeline_cognitif/
│   └── calcul convolutif déterministe et dispatcher multi-rapports
│
├── src/adapters/
│   ├── corpus/       → chargement et indexation de théories
│   ├── hol_isabelle/ → liaison avec Isabelle/HOL
│   ├── llm/          → fournisseur de langage
│   └── wolfram/      → vérification numérique externe
│       ↓
├── theories/
│   └── sources formelles Isabelle/HOL
│
├── backend/ et src/api/
│   └── interfaces de service
├── frontend/
│   └── interface Web
├── config/ et scripts/
│   └── réglages, démarrage et intégrations
└── tests/
    └── tests unitaires et de routage
```

### Les huit moteurs : correspondance prudente

Le pipeline instancie explicitement les moteurs d'abstraction, d'analyse des
objectifs/planification, de navigation, de généralisation, de découverte de
théorèmes et de vérification numérique; il raccorde aussi Isabelle/HOL. Le
raisonnement récursif est appelé « 8e moteur » dans le code et fonctionne en
arrière-plan. Cette liste est une correspondance des composants, pas un
registre officiel stable numéroté de 1 à 8. Le moteur numérique dépend d'un
vérificateur optionnel et le moteur récursif peut être désactivé par variable
d'environnement ou indisponible à l'import.

## Suivi des trois questions

### 1. Reconstruction pour n=10, rapports 1/2 à 1/19

```text
Question utilisateur
  ↓
UI / CLI → Orchestrator.ask
  ↓
Pipeline → calculs et réponse de base
  ↓
Enrichissement multi-rapports
  ↓
pipeline_cognitif / dispatcher ou catalogue pré-calculé
  ↓
Tableau et statistiques ajoutés à la réponse
```

- Le parseur reconnaît la plage comme 18 rapports et la couche de réponse
  trouve le catalogue pré-calculé `n=10`.
- Le catalogue annonce 16/18 résultats; `1/11` et `1/14` restent sans premier.
- **Continuité incertaine :** le calcul direct donne 13/18, et signale des
  ancrages ambigus notamment pour `1/10`, `1/12` et `1/16`, alors que le
  catalogue choisit un ancrage pour ces rapports. Le catalogue et le calcul
  direct ne sont donc pas équivalents; la réponse dépend de la voie choisie.
- Le chemin de restitution multi-rapports est testé; cela ne résout pas la
  divergence entre ses deux sources.

### 2. Résumé exhaustif du spectre, des thèmes HOL/Isabelle et du convolutif

```text
Question discursive
  ↓
UI / CLI → Orchestrator.ask → pré-raisonnement et pipeline
  ↓
moteurs cognitifs → prompt LLM → critique / audit → réponse

Voie HOL distincte :
théories .thy → chargeur de corpus → commande « corpus detail »
                                     (consultation manuelle)
Calcul nécessitant une preuve → générateur HOL → adaptateur Isabelle
```

- Le dossier de théories est chargé à l'initialisation; le chargeur indexe les
  sections et déclarations des fichiers `.thy` directement présents dans ce
  dossier. Le dépôt local en compte 25 à ce niveau.
- La commande de détail du corpus est une voie CLI séparée. Le pipeline de
  réponse libre ne transmet pas automatiquement le contenu complet de toutes
  les théories au prompt.
- Une demande de résumé ne garantit donc ni une revue exhaustive de toutes les
  théories, ni une session Isabelle exécutée. La génération HOL est un chemin
  conditionnel lié aux objectifs de preuve et aux faits calculés.
- **Chemin incomplet pour l'exhaustivité demandée :** aucune liaison unique
  n'assure le parcours complet du corpus puis la synthèse de tous ses thèmes.

### 3. Analyse de l'image `C:\theorie-mathematique\assets\images\quadrature_parabole_zero_critique.png`

```text
Commande « image <chemin> [question] »
  ↓
interception prioritaire par l'UI
  ↓
accès filesystem → résolution du chemin → lecture de l'image
  ↓
analyse Claude Vision (clé et SDK requis)
```

- Le fichier existe sur l'hôte et s'ouvre localement comme PNG de 1242 × 789.
  La résolution du chemin Windows fonctionne dans l'environnement natif.
- **Chemin Docker incomplet :** le volume correspondant au lecteur `C:` et au
  dossier `C:\theorie-mathematique` n'apparaît pas dans la configuration
  Compose. Depuis le conteneur, il faut un volume ou un `WINDOWS_MOUNT_MAP`
  approprié.
- Les tests vérifient le routage de l'alias et des chemins Windows avec des
  images de test. L'analyse sémantique de cette image précise n'a pas été
  envoyée à un service externe et n'est donc pas validée ici.

## Continuité transversale et points à corriger

- **Debugger slow-motion : liaison interrompue.** Le pipeline crée le détecteur
  et le debugger, puis calcule un score de cohérence; la branche censée déclencher
  le debugger se termine toutefois par une instruction vide. Le mode activé
  dans la configuration ne suffit pas à exécuter le débogage pas à pas.
- **Tests ciblés :** 38 tests multi-rapports et image réussissent. Sur l'ensemble
  incluant les tests des critères convolutifs, 5 tests échouent sur 51 :
  deux résultats du rapport typique n'ont pas la clé `niveau_1`, et trois appels
  non typiques passent un argument `n` refusé par la méthode sous-jacente.
  Ces échecs signalent une rupture de contrat entre la couche spectrale et ses
  correctifs/tests.
- **Bilan :** l'entrée CLI, la restitution multi-rapports et le routage image
  sont présents; la cohérence catalogue/calcul direct, la synthèse exhaustive
  HOL, le montage de cette image en conteneur et le déclenchement slow-motion
  ne sont pas établis comme continus de bout en bout.
