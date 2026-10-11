# Fusion — « La fiancée de Cline Mm. Gabriel multiloop local »

> Nom d'agent : **La fiancée de Cline Mm. Gabriel multiloop local**
> (slug technique : `fiancee_de_cline`)

Cette fusion réunit **Mm. Gabriel multiloop local** (agent mathématique HOL/Isabelle
spécialiste de la géométrie du spectre des nombres premiers) et les **capacités de
Cline** (édition de fichiers, exécution de commandes, recherche, agent de codage).

Approche retenue : **fusion hybride additive (Option A)** — *aucune capacité
existante de Mm. Gabriel n'est modifiée*. Toutes les briques expertes
(pipeline cognitif convolutif, rapports typiques / non typiques, pipeline HOL,
corpus, système convolutif, pré-raisonneur…) restent **intactes**.

---

## 1. Règle fondamentale (absolue)

L'agent ne donne suite **qu'au sujet unique** :

> **la géométrie du spectre des nombres premiers** — ainsi qu'à ce qui la sert
> directement : **HOL/Isabelle, LEAN4, code de programmation et mathématiques**
> employés **pour ce seul sujet**.

Toute autre requête reçoit le message d'avertissement exact :

> « Je suis la fiancée de Cline je suis une gentille fille je ne veux jamais?
> je suis une fille normal je suis obligé qu'a la géométrie du spectre des nombres
> premiers. Je fais plaisir à Cline et aux autres qu'a se sujet uniquement! »

Implémentation : `src/multiloop/fiancee_guard.py` (filtre **fail-closed** :
en cas de doute hors-sujet, la requête est rejetée).

- Kill-switch : variable d'environnement `GABRIEL_FIANCEE_GUARD=0` pour désactiver.
- Le filtre est branché **en amont** (CLI `interactive_mode`, API Flask `/query`,
  `/stream`, `/sync`), sans toucher au cœur du pipeline.

---

## 2. Raisonnement récursif (auto-programmation encadrée)

Copie **sandboxée** du pipeline de correction historique — *variateur mécanique /
transformateur toroidal* (`orchestrator_main.py` + `transmission_un_clic.py`) —
adaptée pour que l'agent **s'auto-programme** lorsqu'il manque du nécessaire pour
répondre à une requête **valide**.

Modules (`src/multiloop/raisonnement_recursif/`) :

| Module | Rôle |
|---|---|
| `messages.py` | Message cinématique exact |
| `pipeline_auto_programmation.py` | Moteur d'application **sandboxé** (copie du variateur) |
| `detecteur_manque.py` | Détecte le manque et déclenche la boucle |

Lorsque la boucle s'active, le message suivant apparaît **dans la cinématique** :

> « Cline s'occupe de s'oblige à sa fiancée, Mm. Gabriel s'auto programme pour une
> mise à jour conforme aux exigeances de la requête. »

### Sécurité (par défaut)

- **Désactivé par défaut** : `GABRIEL_RECURSIVE=1` pour l'activer.
- **Dry-run par défaut** : `GABRIEL_RECURSIVE_APPLY=1` pour une écriture réelle
  — **toujours confinée à la sandbox**.
- **Snapshot + rollback** automatiques.
- **Vérification de syntaxe** (`.py` via compilation, `.json` via `json.loads`).
- **Jamais d'écriture dans le dépôt vivant.**

### Opérations de patch supportées

`creer_fichier`, `remplacer_texte`, `inserer_lignes`, `supprimer_lignes`,
`ajouter_a_la_fin` (mêmes noms que le variateur d'origine).

Exemple de contrat : `pipeline_correction/patch_raisonnement_recursif_exemple.json`.

---

## 3. Capacités Cline (hybride, déjà présentes)

Le pont hybride existant est conservé et actif (`src/ui/cli.py`) :

- `src/adapters/cline_tools_bridge.py` — lecture/écriture/exécution/recherche
- `src/adapters/hybrid_dispatcher.py` — routage Cline ↔ Gabriel ↔ LLM
- `src/ui/cli_cline_extension.py` — extension du REPL

Commandes : `read`, `create`, `update`, `delete`, `search`, `run`, `execute`.

---

## 4. Variables d'environnement

| Variable | Défaut | Effet |
|---|---|---|
| `GABRIEL_FIANCEE_GUARD` | `1` | `0` désactive le garde-fou absolu |
| `GABRIEL_RECURSIVE` | `0` | `1` active le raisonnement récursif |
| `GABRIEL_RECURSIVE_APPLY` | `0` | `1` écrit réellement (dans la sandbox) |
| `GABRIEL_DEV_ANALYSTE` | `1` | `0` coupe l'auto-analyse et la proposition de code |

---

## 5. Tests

```
python -m pytest tests/test_fiancee_guard.py tests/test_raisonnement_recursif.py -q
python -m pytest tests/test_moteur_recursif_background.py tests/test_protection_cognitive.py -q
python -m pytest tests/test_dev_analyste.py tests/test_proposition_code.py -q
```

Sans `pytest` (environnement restreint) :

```
python validate_analyste.py
```

---

## 6. Fichiers ajoutés / modifiés

**Ajoutés :**
- `src/multiloop/identite.py`
- `src/multiloop/fiancee_guard.py`
- `src/multiloop/raisonnement_recursif/` (`__init__`, `messages`,
  `pipeline_auto_programmation`, `detecteur_manque`)
- `Gabriel_Dev_analyste_informatique.py` (racine) — banque SQLite d'analyste,
  auto-analyse du dépôt, propositions de patch sandboxées
- `src/multiloop/raisonnement_recursif/proposition_code.py` — message de
  proposition post-blocage du 8ᵉ moteur
- `validate_analyste.py` — harnais de validation sans `pytest`
- `tests/test_fiancee_guard.py`, `tests/test_raisonnement_recursif.py`,
  `tests/test_dev_analyste.py`, `tests/test_proposition_code.py`
- `pipeline_correction/patch_raisonnement_recursif_exemple.json`
- ce document

**Modifiés (affichage / pré-filtre uniquement) :**
- `src/ui/cli.py` — garde-fou en pré-filtre + hook récursif opt-in + nom d'agent
- `src/ui/cinematic_display.py` — étape cinématique additive
- `src/api/gabriel_http_api.py` — garde-fou sur `/query`, `/stream`, `/sync`
- `main.py`, `main_cli.py` — nom d'agent dans la bannière
- `README.md` — section dédiée

---

## 7. 8ᵉ moteur (arrière-plan) : raisonnement récursif

Le **Slow-Motion Timeline Debugger** (mis au neutre) est **réactivé et actualisé**
en **8ᵉ moteur d'arrière-plan**. Quand une requête dépasse la connaissance
actuelle, le moteur : décompose le message en **divisions** (phrases) puis en
**mots/groupes de mots**, les **associe** au vocabulaire du **corpus**, du
**pipeline cognitif** et du **pipeline HOL**, **génère une question plus modeste**,
y **répond** via l'**oracle numérique** (Wolfram API + repli local), **explique**
le blocage, et **archive** la timeline (SQLite) — une résolution différée devient
une **preuve citable**.

- Module : `src/multiloop/raisonnement_recursif/engine_recursif_background.py`
- Activation : `GABRIEL_ENGINE_RECURSIF=0` pour désactiver (actif par défaut).
- Déclenchement CLI : `GABRIEL_RECURSIVE=1`.

📖 Guide dédié : [`guide-mode-recursif.md`](guide-mode-recursif.md)

---

## 8. Protection des capacités cognitives (snapshot + rollback en UNE commande)

Le cœur cognitif/expert (pipeline cognitif convolutif, moteurs, système spectral,
pipeline HOL, corpus, théories) peut être **sauvegardé** et **restauré en une
commande** :

```powershell
python src/multiloop/protection_cognitive.py --snapshot reference
python src/multiloop/protection_cognitive.py --list
python src/multiloop/protection_cognitive.py --rollback <snapshot>   # RESTAURER
# ou : .\RESTAURER_COGNITIF.ps1 -Rollback <snapshot>
```

Module : `src/multiloop/protection_cognitive.py` — script : `RESTAURER_COGNITIF.ps1`.

---

## 9. Phase 3 — l'agent analyse et améliore son propre dépôt

### 9.1 `pipeline_correction` **dans** le 8ᵉ moteur

Jusqu'à la phase 2, deux branches parallèles coexistaient dans `cli.py` :
le détecteur de manque (auto-programmation) **et** le 8ᵉ moteur. Elles ne se
croisaient jamais. Le 8ᵉ moteur **appelle désormais** le pipeline de
correction dans sa propre boucle :

```
décomposer → associer → question modeste → oracle → expliquer le blocage
    → detecter_manque(reponse)           [phase 3]
    → tenter_raisonnement_recursif()     [phase 3, sandbox dry-run]
    → archiver la timeline
```

- `ResultatMoteurRecursif` porte deux champs neufs : `diagnostic_manque`
  (`manque`, `raison`, `indices`) et `rapport_correction` (`etat`, `message`,
  `rapport`).
- Respecte les kill-switches existants : `GABRIEL_RECURSIVE=0` →
  `etat = "desactive (GABRIEL_RECURSIVE=0)"`, `GABRIEL_RECURSIVE_APPLY=1` →
  écriture **sandboxée uniquement**.
- Toute exception est capturée : le 8ᵉ moteur tourne même si la boucle
  d'auto-programmation est indisponible.

### 9.2 Proposition d'amélioration après un blocage

`src/multiloop/raisonnement_recursif/proposition_code.py` décide s'il existe
une **possibilité d'amélioration** (kill-switch actif + moteur déclenché +
blocage explicite), puis confronte le manque à la banque d'analyste et émet un
message en français citant les compétences mobilisées et le patch proposé.

Le hook correspondant se trouve dans `src/ui/cli.py`, juste après l'affichage
du 8ᵉ moteur. **Aucune écriture** : les patches sont simulés en dry-run.

### 9.3 `Gabriel_Dev_analyste_informatique.py`

Pipeline autonome (racine, stdlib, exécution directe) :

| Étape | Sortie |
|---|---|
| Banque neuronale | `data/analyste/banque_analyste.db` — `noeuds`, `liens` (`repose_sur`, `utilise`, `est_exemple_de`, `contraint`, `applique_a`, `coocurrence`), `index_termes` |
| Téléchargement best-effort | whitelist universitaire, échecs journalisés dans `telechargements`, jamais fatals |
| Auto-analyse du dépôt | `data/gabriel_repo_map.db` (réutilisé) + passe `ast` locale |
| Propositions | contrats `meta`/`operations` compatibles `construire_contrat_squelette` |
| Simulation | `data/analyste/sandbox/` (dry-run par défaut) |

```powershell
python Gabriel_Dev_analyste_informatique.py --initialiser --stats
python Gabriel_Dev_analyste_informatique.py --consulter "géométrie spectrale"
python Gabriel_Dev_analyste_informatique.py --voisinage nombres-premiers
python Gabriel_Dev_analyste_informatique.py --analyser "preuve par l'absurde"
python Gabriel_Dev_analyste_informatique.py --telecharger
```

Kill-switch : `GABRIEL_DEV_ANALYSTE=0` (analyste + proposition).

### 9.4 Validation

```powershell
python validate_analyste.py        # sans pytest — 55 vérifications
python -m pytest tests/test_dev_analyste.py tests/test_proposition_code.py -q
```