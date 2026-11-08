# Guide des commandes Gabriel — Agent Multi-Loop Local

**Version : 2.2** &nbsp;|&nbsp; **Date : 15 février 2026** &nbsp;|&nbsp; **Tests : 230/230 ✅**

Ce document liste **toutes les commandes** disponibles pour interagir avec Gabriel,
votre agent multi-loop local dédié à la **Méthode Spectrale** (reconstruction de
primes via les suites SA / SB / digamma).

Gabriel se lance via le script `start-agent.ps1` (Windows) ou directement par
`python main_cli.py` à la racine du projet. Une fois lancé, vous tapez les
commandes ci-dessous directement dans le prompt `Philippe >`.

---

## 🌟 Démarrage rapide

Quand vous ouvrez Gabriel, vous verrez :

```
+============================================================+
|     MULTI-LOOP MATH AGENT  -  Philippe Thomas Savard       |
|       Methode Spectrale  *  Isabelle/HOL  *  Multi-Loop    |
+============================================================+

  Verification de la suite de tests (pytest local)...
  Statut CI Gabriel : 230/230 OK (pytest local, 1.7s - tapez 'ci' pour le rapport detaille)

  Agent Multi-Loop pret. Bonjour Philippe !
  Tapez 'aide' pour les commandes, 'quitter' pour sortir.
  --------------------------------------------------------
Philippe >
```

À partir d'ici, vous avez **3 façons** d'utiliser Gabriel :

1. **Commandes explicites** (déterministes, rapides, citables) — listées ci-dessous
2. **Questions en langage naturel** (LLM multiloop avec garde-fous mathématiques)
3. **Auto-trigger visualisation** — Gabriel détecte automatiquement les demandes de graphique et y répond sans LLM

---

## 📋 Table des matières

1. [Commandes générales](#1-commandes-générales)
2. [Corpus & nombres premiers](#2-corpus--nombres-premiers)
3. [Calculs déterministes (sans LLM)](#3-calculs-déterministes-sans-llm)
4. [Visualisations & graphiques](#4-visualisations--graphiques)
5. [Validation & vérification mathématique](#5-validation--vérification-mathématique)
6. [Audit & citations scientifiques](#6-audit--citations-scientifiques)
7. [Mode debugger pédagogique](#7-mode-debugger-pédagogique)
8. [Tests & CI](#8-tests--ci)
9. [Questions en langage naturel](#9-questions-en-langage-naturel-multi-loop)
10. [Auto-trigger visualisation](#10-auto-trigger-visualisation)

---

## 1. Commandes générales

| Commande | Description |
|---|---|
| `aide` (`h`, `?`) | Affiche l'aide rapide |
| `commandes` (`cmd`, `commands`) | **Affiche la liste complète des commandes + raccourcis clavier dans le terminal** |
| `version` | Affiche la version de Gabriel |
| `contexte` | Affiche le contexte mathématique actuel |
| `memoire` | Affiche les échanges en mémoire (historique session) |
| `quitter` | Ferme Gabriel proprement |

> 💡 **Astuce** : tapez `commandes` à tout moment dans Gabriel pour obtenir cette même fiche directement dans votre terminal, sans quitter la session.

---

## 2. Corpus & nombres premiers

Gabriel charge un corpus Isabelle/HOL (fichiers `.thy`) au démarrage et dispose d'une table de **1000 nombres premiers exacts**.

| Commande | Description | Exemple |
|---|---|---|
| `corpus` | Résumé des fichiers `.thy` chargés | `corpus` |
| `corpus detail` | Vue détaillée : sections, definitions, lemmes par fichier | `corpus detail` |
| `primes` | Statut de la table des nombres premiers (1..1000) | `primes` |
| `prime <N>` | Donne le N-ième nombre premier | `prime 26` → 101 |

**Exemples** :
```
Philippe > prime 1
2

Philippe > prime 100
541

Philippe > prime 1000
7919
```

---

## 3. Calculs déterministes (sans LLM)

Ces commandes utilisent uniquement le **SpectralMethodCore** (entiers exacts Python) et ne consomment **aucun token LLM**. Résultats 100 % reproductibles, citables scientifiquement.

### 3.1 Écarts spectraux (gaps)

| Commande | Description | Exemple |
|---|---|---|
| `gap <v1> <v2>` | Écart spectral entre 2 positions ou 2 nombres premiers (auto-détecte les 3 cas : `(+,+)`, `(−,−)`, `(−,+)`) | `gap 26 56` |

**Exemples** :
```
Philippe > gap 26 56
# Écart entre la 26ème et la 56ème position du spectre des primes

Philippe > gap 101 263
# Écart entre les primes 101 et 263 (résolu directement)
```

### 3.2 Rapports spectraux

Gabriel sait calculer 4 types de rapports spectraux :

- **1×1** : un seul couple (a, b)
- **n×n symétrique** : matrice symétrique
- **chaotique** : asymétrique chaotique
- **ordonnée** : asymétrique ordonnée

| Commande | Description | Exemple |
|---|---|---|
| `rsp <A> <B>` | Rapport spectral direct (auto-détecte la configuration) | `rsp 2 3` |
| `rsp-test <config> <N>` | Lance N tests aléatoires d'une configuration<br/>`config` ∈ `1x1` \| `sym2` \| `sym3` \| `sym5` \| `chaos` \| `ord` | `rsp-test sym3 100` |

**Exemples** :
```
Philippe > rsp 2 3
# Rapport spectral direct entre p=2 et p=3

Philippe > rsp-test sym2 50
# 50 tests aléatoires en configuration symétrique 2x2

Philippe > rsp-test chaos 200
# 200 tests aléatoires en asymétrique chaotique
```

---

## 4. Visualisations & graphiques

Gabriel propose **3 formats de sortie combinés** : ASCII (toujours), Rich Table (`--table`), PNG citable (`--png`).

### 4.1 Courbe RsP en fonction de k (ASCII rapide)

| Commande | Description |
|---|---|
| `rsp-courbe <config> [kmax]` | Trace en ASCII la courbe du rapport spectral en fonction de k<br/>`config` ∈ `1x1` \| `sym` \| `chaos` \| `ord`<br/>`kmax` (optionnel) = limite supérieure de k |

```
Philippe > rsp-courbe sym 50
Philippe > rsp-courbe chaos
```

### 4.2 Commande universelle `courbe` (ASCII + Table + PNG)

**Syntaxe complète** :
```
courbe <type> <n_min>..<n_max> [--table] [--png] [--scale=auto|linear|log10|log2]
```

**Types disponibles** :

| Type | Description | Échelle auto |
|---|---|---|
| `SA` | Suite alternée A : `SA(n) = (13·2^n)/8 − 2` | log10 |
| `SB` | Suite alternée B : `SB(n) = (13·2^n)/4 − 66` | log10 |
| `SA_SB` | Superposition SA et SB sur le même graphique | log10 |
| `digamma` | `digamma(n) = SB(n) − 64·P(n)` (reconstruction 1/2) | auto |
| `invariant` | `D(n,P) = SB − SA − (1/2)·P` (invariant spectral) | auto |
| `ratio` | `SA(n) / SB(n)` (converge vers 1/2) | linear |
| `gap` | `Δp(n) = P(n+1) − P(n)` (écarts consécutifs) | linear |
| `prime` | `P(n)` (croissance des nombres premiers) | log10 |

**Flags** :

| Flag | Effet |
|---|---|
| `--table` | Ajoute un tableau Rich avec les valeurs exactes |
| `--png` | Exporte un fichier PNG haute résolution (150 dpi) dans `data/graphs/` |
| `--scale=X` | Force l'échelle : `linear`, `log10`, `log2` ou `auto` (défaut) |

**Exemples** :
```
Philippe > courbe ratio 1..50
# ASCII : convergence visible vers 1/2

Philippe > courbe SA_SB 1..50 --table
# ASCII + tableau Rich avec SA et SB côte à côte

Philippe > courbe digamma 1..30 --png
# ASCII + PNG haute résolution pour article scientifique

Philippe > courbe ratio 1..200 --table --png
# Combo complet : ASCII + tableau + PNG + audit JSON citable

Philippe > courbe SA 1..100 --scale=log10
# Force l'échelle log10 (utile pour voir l'allure 2^n)
```

**Sortie typique** : à chaque visualisation, Gabriel crée automatiquement un **audit JSON signé** dans `data/audits/`, vous donnant un `id` pour citation scientifique (voir section 6).

---

## 5. Validation & vérification mathématique

| Commande | Description | Quand l'utiliser |
|---|---|---|
| `verifier <N>` | Validation toolkit (sympy/mpmath/z3) + création d'audit citable (rapport 1/2) | Quand vous voulez une preuve formelle d'un calcul |
| `valider <N>` | Boucle complète Wolfram ↔ Gabriel ↔ Isabelle (`.thy` auto-compile) | Quand vous voulez croiser 3 sources mathématiques |

**Exemples** :
```
Philippe > verifier 26
# Validation formelle de la reconstruction du 26ème prime (=101)
# via sympy + mpmath + z3 → crée un audit JSON signé

Philippe > valider 42
# Boucle Wolfram <-> Gabriel <-> Isabelle pour le 42ème prime
# Compile dynamiquement un fichier .thy si Isabelle est activé
```

> ⚠️ La commande `valider` nécessite que le profil Docker `WithIsabelle` soit actif
> (option `-WithIsabelle` au démarrage via `start-agent.ps1`) pour la compilation `.thy`.

---

## 6. Audit & citations scientifiques

Chaque calcul important crée un **audit JSON signé** (SHA-256) dans `data/audits/`. Ces audits sont **citables dans vos articles**.

| Commande | Description | Exemple |
|---|---|---|
| `historique` | Liste les 20 derniers audits | `historique` |
| `audit <id>` | Affiche le contenu complet d'un audit (JSON) | `audit aa41c24a` |
| `citer <id> [fmt]` | Génère une citation scientifique<br/>`fmt` ∈ `markdown` \| `latex` \| `text` (défaut : markdown) | `citer aa41c24a latex` |

**Exemple de flux complet** :
```
Philippe > courbe ratio 1..100 --png
[...]
_Audit citable cree : id=aa41c24a_

Philippe > citer aa41c24a latex
% Citation LaTeX prête à insérer dans votre article
\bibitem{gabriel-aa41c24a}
  Gabriel Multi-Loop Agent (2026). Audit aa41c24a :
  "Visualisation auto-declenchee : courbe ratio sur n=1..100".
  Formule : SA(n)/SB(n) -> 1/2 quand n -> infini.
  Hash SHA-256 : ...

Philippe > audit aa41c24a
# Affiche le JSON complet (intervention_type, citations_thy, toolkit_reports, hash...)
```

---

## 7. Mode debugger pédagogique

Gabriel possède un **Slow-Motion Debugger** : un mode interactif où vous décomposez une question étape par étape, avec bypass LLM et commentaires manuels.

| Commande | Description |
|---|---|
| `debug "<question>"` | Lance le mode debugger sur une question (les guillemets sont obligatoires) |

**Exemple** :
```
Philippe > debug "Reconstruis le 42ième nombre premier"
# Ouvre une session interactive :
#   - décomposition étape par étape
#   - bypass possible vers le CertaintyKernel (formules hardcodées)
#   - ajout de commentaires manuels (sauvegardés dans l'audit)
#   - validation par toolkit sympy/mpmath/z3
```

---

## 8. Tests & CI

| Commande | Description |
|---|---|
| `ci` (alias : `tests`, `pytest`) | Lance localement la suite pytest (230 tests) et affiche le rapport détaillé |

**Note** : le statut CI s'affiche aussi automatiquement à chaque ouverture de Gabriel dans la bannière (`Statut CI Gabriel : 230/230 OK`).

GitHub Actions exécute également ces 230 tests automatiquement à chaque push/PR sur `main` (voir `.github/workflows/tests.yml`).

---

## 9. Questions en langage naturel (multi-loop)

Vous pouvez aussi poser **n'importe quelle question mathématique** en langage naturel. Gabriel :

1. **Détecte un éventuel calcul exact** (gap, prime, visualisation) → réponse immédiate
2. **Sinon** : lance le pipeline multi-loop avec :
   - 7 moteurs cognitifs
   - Boucle de raffinement multi-critique
   - Garde-fous CertaintyKernel (formules hardcodées)
   - Mode Silent Audit + Slow Motion Debugger automatique

**Exemples** :
```
Philippe > Reconstruis le 42ème nombre premier
# Gabriel répond avec calcul exact + audit citable

Philippe > Quel est l'écart spectral entre 26 et 56 ?
# Gabriel détecte un gap (+,+) et résout sans LLM

Philippe > Explique-moi la convergence du ratio SA/SB
# Pipeline multi-loop avec garde-fous mathématiques

Philippe > Quelle est la signification du plan trifocal FZg/HyRi/MsP ?
# Pipeline multi-loop + corpus Isabelle
```

---

## 10. Auto-trigger visualisation

**Nouveauté v2.2** : Gabriel détecte automatiquement les demandes de graphique dans vos questions en langage naturel et y répond **sans LLM** (100 % déterministe).

**Mots-clés déclencheurs** :
- *Verbes* : `trace`, `dessine`, `illustre`, `visualise`, `affiche`, `évolue`, `converge`, `comportement`, `représente`, `montre`...
- *Types* : `SA`, `SB`, `digamma`, `ψ`, `psi`, `ratio`, `rapport`, `gap`, `écart`, `invariant`, `D(n,P)`, `prime(s)`...
- *Intervalles* : `n=1..50`, `de 1 à 100`, `entre 5 et 25`, `[1,200]`, `les 100 premiers`...
- *PNG* : `article scientifique`, `exporte`, `image`, `fichier`, `PDF`, `citable`...

**Exemples de questions reconnues automatiquement** :
```
Philippe > Trace la courbe de SA pour n=1..50
Philippe > Peux-tu illustrer la convergence du ratio SA/SB sur 1..100 ?
Philippe > Comment évolue digamma sur les 30 premiers ?
Philippe > Dessine les écarts entre primes consécutifs entre 1 et 200
Philippe > Visualise SA et SB ensemble et exporte un PNG pour mon article scientifique
```

Pour chaque détection, Gabriel produit : ASCII + résumé statistique + (PNG si demandé) + audit JSON citable.

---

## ⌨️ Raccourcis clavier interactifs

Gabriel active automatiquement les raccourcis clavier du module `readline` à chaque démarrage. **Historique persistant** entre sessions dans `data/.gabriel_history`.

### Navigation dans l'historique

| Raccourci | Action |
|---|---|
| `↑` / `↓` | Naviguer dans les commandes précédentes/suivantes |
| `Ctrl + R` | Recherche inversée (commencez à taper, `Ctrl+R` à nouveau pour suivant) |
| `Ctrl + S` | Recherche avant (rare ; nécessite parfois `stty -ixon`) |
| `Ctrl + G` | Annuler une recherche `Ctrl+R` |

### Auto-complétion

| Raccourci | Action |
|---|---|
| `Tab` | Complète la commande en cours (ex : `cou<Tab>` → `courbe`) |
| `Tab Tab` | Affiche toutes les complétions possibles si ambigu |

Les commandes proposées sont : toutes celles listées dans `aide` + les types de `courbe`.

### Édition de la ligne courante

| Raccourci | Action |
|---|---|
| `Ctrl + A` | Aller en début de ligne |
| `Ctrl + E` | Aller en fin de ligne |
| `Alt + B` | Reculer d'un mot |
| `Alt + F` | Avancer d'un mot |
| `Ctrl + W` | Effacer le mot précédent |
| `Ctrl + U` | Effacer toute la ligne (vers la gauche) |
| `Ctrl + K` | Effacer toute la ligne (vers la droite) |
| `Ctrl + Y` | Coller le dernier texte coupé (yank) |
| `Ctrl + T` | Inverser les 2 caractères autour du curseur |

### Contrôle du terminal

| Raccourci | Action |
|---|---|
| `Ctrl + L` | Effacer l'écran (sans perdre la session) |
| `Ctrl + C` | Interrompre la commande en cours |
| `Ctrl + D` | Quitter Gabriel (envoie EOF) |

> 💡 **Sur Windows hors Docker** : si vous lancez Gabriel directement avec Python sur Windows (pas via Docker), installez `pyreadline3` (`pip install pyreadline3`) pour activer ces raccourcis. Dans Docker (cas par défaut), readline est natif et tout fonctionne.

---

## 🛠️ Astuces & raccourcis

| Astuce | Commande |
|---|---|
| Voir l'historique de vos audits | `historique` |
| Récupérer une citation pour LaTeX | `citer <id> latex` |
| Forcer une échelle log sur une courbe | `courbe SA 1..100 --scale=log10` |
| Combiner table + PNG + audit en une commande | `courbe ratio 1..50 --table --png` |
| Vérifier que tous les tests passent | `ci` |
| Lancer Gabriel avec Isabelle | `.\start-agent.ps1 -WithIsabelle` |
| Quitter Gabriel | `quitter` ou `Ctrl+D` |

---

## 📂 Fichiers générés par Gabriel

| Dossier | Contenu |
|---|---|
| `data/audits/` | Audits JSON signés (SHA-256), citables scientifiquement |
| `data/graphs/` | PNG haute résolution (150 dpi) exportés via `--png` |

**Note** : ces dossiers sont **ignorés** par git (`.gitignore`) pour éviter de polluer le dépôt. Vos audits restent locaux par défaut.

---

## 📚 Pour aller plus loin

- **Documentation Méthode Spectrale** : voir `README.md` à la racine du projet
- **Architecture du code** : voir `src/` (8 modules : `core`, `engines`, `multiloop`, `spectral`, `visualization`, `audit`, `learning`, `ui`)
- **Tests** : voir `tests/` (230 tests Pytest, structure cohérente)
- **Intégrations Isabelle** : voir `theories/*.thy` et `src/adapters/hol_isabelle.py`

---

**Bon travail avec Gabriel ! 🎯**

_Document généré automatiquement le 15 février 2026 — version 2.2_
