# Guide — Mode récursif de « La fiancée de Cline Mm. Gabriel multiloop local »

> Ce guide décrit le **mode récursif** de l'agent fusionné : son rôle de **8ᵉ moteur
> d'arrière-plan**, sa protection (snapshots + rollback en une commande) et son
> usage pour produire, au fil des sessions, des **preuves citables** contribuant à
> valider la géométrie du spectre des nombres premiers.

---

## 1. Qu'est-ce que le mode récursif ?

Historiquement, l'agent possédait un **Slow-Motion Timeline Debugger** (mis « au
neutre » en juillet 2026 car trop coûteux : 25+ itérations, scores bas). Le mode
récursif **réactive cette fonction de debugger en l'actualisant** : au lieu de
relancer aveuglément le multiloop, l'agent, **lorsqu'une requête lui demande plus
qu'il ne sait répondre**, va :

1. **Décomposer** le message de la requête en **divisions** (phrases/clauses), puis
   en **mots** et **groupes de mots** ;
2. **Associer** ces éléments au **vocabulaire** du **corpus**, du **pipeline
   cognitif** et du **pipeline HOL/Isabelle/LEAN** ;
3. **Générer une question plus modeste** à partir de ces associations ;
4. **Tenter d'y répondre** à l'aide d'un **oracle numérique** (package **Wolfram
   API** inclus, + repli local déterministe) ;
5. **Expliquer** ce qui l'empêche de répondre adéquatement à la requête initiale ;
6. **Archiver** la timeline (persistance SQLite) pour les **sessions futures**.

> Avantage clé : une question non résolue aujourd'hui, si elle est **résolue
> indirectement** plus tard (dans une autre session), **devient une preuve
> citable** qui contribue à valider la géométrie du spectre — notamment pour la
> **preuve par l'absurde** sur l'**exclusivité de P premier**, section critique de
> `methode_spectral.thy`.

---

## 2. Le 8ᵉ moteur d'arrière-plan

| | |
|---|---|
| **Nom** | `MoteurRecursifBackground` — « 8ᵉ moteur (arrière-plan) : raisonnement récursif » |
| **Module** | `src/multiloop/raisonnement_recursif/engine_recursif_background.py` |
| **Statut** | **Activé** par défaut (`GABRIEL_ENGINE_RECURSIF=0` pour le désactiver) |
| **Exécution** | En **arrière-plan** (n'altère pas la réponse principale) |
| **Dépendances** | stdlib au chargement ; Wolfram chargé paresseusement |

### Sous-modules

| Module | Rôle |
|---|---|
| `decomposeur_lexical.py` | Divisions → tokens → associations (corpus / cognitif / HOL) |
| `generateur_question_modeste.py` | Construit la/les question(s) simplifiée(s) |
| `oracle_numerique.py` | Oracle Wolfram|Alpha + repli local (primalité, n-ième premier) |
| `archiveur_timeline.py` | Persistance SQLite des timelines (réutilisation inter-session) |
| `engine_recursif_background.py` | Orchestrateur du 8ᵉ moteur |
| `messages.py` | Message cinématique exact |
| `pipeline_auto_programmation.py` / `detecteur_manque.py` | Auto-programmation sandboxée (voir §5) |

---

## 3. Ce que voit l'utilisateur (cinématique)

Lorsque le mode récursif est actif et qu'un manque est détecté, la cinématique
affiche exactement :

> « **Cline s'occupe de s'oblige à sa fiancée, Mm. Gabriel s'auto programme pour
> une mise à jour conforme aux exigeances de la requête.** »

Puis, en complément :

- le nombre de **divisions** analysées et d'**ancres spectrales** ;
- la **couverture** lexicale (%) ;
- la **question plus modeste** proposée ;
- la **réponse modeste** (si l'oracle a répondu) ;
- une **explication du blocage** de la requête initiale ;
- l'**identifiant de la timeline archivée** (et la mention **CITABLE** si résolue).

Étape cinématique dédiée : `moteur_recursif` — « 🧩 8e moteur : raisonnement
récursif (divisions → question modeste → oracle) ».

---

## 4. Activation

Le mode récursif se compose de deux niveaux :

| Variable d'environnement | Défaut | Effet |
|---|---|---|
| `GABRIEL_ENGINE_RECURSIF` | `1` | instancie le 8ᵉ moteur en arrière-plan |
| `GABRIEL_RECURSIVE` | `0` | **déclenche** la boucle d'auto-programmation/récursive dans le CLI |
| `GABRIEL_RECURSIVE_APPLY` | `0` | écriture réelle (sandbox uniquement) au lieu du dry-run |
| `GABRIEL_FIANCEE_GUARD` | `1` | garde-fou de domaine absolu (`0` = désactivé) |

Exemple (PowerShell) :

```powershell
cd C:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local
$env:GABRIEL_RECURSIVE="1"        # déclenche le mode récursif
python main_cli.py
```

---

## 5. Sécurité : le mode récursif ne casse rien

1. **Garde-fou de domaine absolu** (fail-closed) en amont : seules les requêtes du
   sujet spectral (et ce qui le sert) sont traitées.
2. **Auto-programmation sandboxée** : patchs `.json` appliqués dans un **dossier
   temporaire isolé**, **dry-run par défaut**, jamais le dépôt vivant.
3. **Snapshot + rollback** : voir §6.
4. **Imports lourds paresseux** : l'agent démarre même sans `httpx`/Wolfram.

---

## 6. Protection des capacités cognitives (snapshot + rollback en UNE commande)

Lorsqu'une modification touche le **cœur cognitif/expert** (pipeline cognitif
convolutif, moteurs, système spectral, pipeline HOL, corpus, théories), un
**snapshot** peut être pris avant toute écriture, et le retour à l'ancienne version
se fait en **une seule commande**.

**Module :** `src/multiloop/protection_cognitive.py`
**Script un clic :** `RESTAURER_COGNITIF.ps1`

### Commandes

```powershell
# 1) Créer un snapshot de référence du cœur cognitif
python src/multiloop/protection_cognitive.py --snapshot reference
#    (ou)   .\RESTAURER_COGNITIF.ps1 -Snapshot mon_label

# 2) Lister les snapshots
python src/multiloop/protection_cognitive.py --list

# 3) RESTAURER l'ancienne version (UNE COMMANDE)
python src/multiloop/protection_cognitive.py --rollback <nom_snapshot>
#    (ou)   .\RESTAURER_COGNITIF.ps1 -Rollback <nom_snapshot>

# 4) Simulation (aucune écriture)
python src/multiloop/protection_cognitive.py --rollback <nom_snapshot> --dry-run

# 5) Vérifier l'intégrité (ce qui a changé depuis le snapshot)
python src/multiloop/protection_cognitive.py --verifier <nom_snapshot>
```

Les snapshots sont stockés dans `.gabriel_cognitif/snapshots/` (ignoré par git).
Chaque snapshot contient un `manifeste.json` (chemins + empreintes SHA-256).

### Périmètre protégé (`MOTIFS_PROTEGES`)

`src/core/*.py`, `src/multiloop/*.py`, `src/multiloop/raisonnement_recursif/*.py`,
`src/spectral/*.py`, `src/engines/**/*.py`, `src/adapters/hol_isabelle/*.py`,
`src/adapters/wolfram/*.py`, `pipeline_cognitif/*.py`,
`theories/methode_spectral.thy`, `theories/validation_hol_unifiee.thy`,
`theories/geometrie_spectre_premier.thy`, `corpus/*`.

---

## 7. Preuves citables (résolution différée)

- Chaque déclenchement archive une ligne dans
  `data/learning/timelines_recursives.db` (table `timelines`).
- Une timeline **non résolue** reste disponible pour les **sessions futures**.
- Quand une timeline est **résolue** (aujourd'hui via l'oracle, ou plus tard de
  façon indirecte), elle passe à `resolue=1` / `citable=1` :
  elle devient une **preuve citable**.
- Le moteur **réutilise** les timelines citables similaires (inter-session).

### API rapide

```python
from src.multiloop.raisonnement_recursif import MoteurRecursifBackground
moteur = MoteurRecursifBackground()
res = moteur.traiter("Comment reconstruire le 137e nombre premier (rapport 1/2) ?")
print(res.divisions, res.ancres, res.question_modeste, res.reponse_modeste)
print(res.blocage)
print(moteur.statistiques())     # total / resolues / non_resolues / citables
```

---

## 8. Limites honnêtes

- La « compréhension » est **programmatique** (décomposition + associations +
  oracle), pas une conscience : c'est une **auto-correction encadrée**.
- Sans `WOLFRAM_APP_ID` (ou sans `httpx`), l'oracle tombe sur un **repli local**
  limité (primalité, petits n-ièmes premiers) ; la question modeste reste
  néanmoins présentée à l'utilisateur.
- Aucun filtre textuel n'est mathématiquement inviolable ; le garde-fou est
  **fail-closed** mais reste un filtre robuste, pas une preuve formelle.

---

## 9. Fichiers concernés

**Ajoutés :** `src/multiloop/protection_cognitive.py`, `RESTAURER_COGNITIF.ps1`,
`guide-mode-recursif.md`, et sous `src/multiloop/raisonnement_recursif/` :
`decomposeur_lexical.py`, `generateur_question_modeste.py`, `oracle_numerique.py`,
`archiveur_timeline.py`, `engine_recursif_background.py`.

**Modifiés (additif) :** `src/core/pipeline.py` (enregistrement du 8ᵉ moteur),
`src/ui/cli.py` (affichage cinématique du 8ᵉ moteur),
`src/ui/cinematic_display.py` (nouvelle étape), `.gitignore`.

**Prérequis :** `GABRIEL_RECURSIVE=1` pour déclencher la boucle dans le CLI.

---

## 10. Phase 3 : améliorer son propre code après un blocage

### 10.1 Ce qui a changé dans le 8ᵉ moteur

Le moteur n'a plus besoin du hook CLI pour déclencher le pipeline de
correction : il l'intègre lui-même, entre l'explication du blocage et
l'archivage.

| Champ | Contenu |
|---|---|
| `diagnostic_manque` | `DiagnosticManque(manque, raison, indices)` issu de `detecter_manque()` |
| `rapport_correction` | `{"etat", "message", "rapport"}` issu de `tenter_raisonnement_recursif()` |

`etat` vaut `"desactive (GABRIEL_RECURSIVE=0)"` par défaut, et
`"applique (sandbox)"` quand `GABRIEL_RECURSIVE=1` — avec `dry_run=True` sauf
`GABRIEL_RECURSIVE_APPLY=1`.

### 10.2 Perception d'une possibilité d'amélioration

`proposition_code.evaluer_possibilite()` répond **oui** seulement si :

1. `GABRIEL_DEV_ANALYSTE` n'est pas `0` ;
2. le 8ᵉ moteur s'est déclenché ;
3. un blocage est explicitement expliqué.

`reponse_modeste` et `citable` sont reportés dans la raison **à titre de
contexte, jamais comme bloquants** : l'oracle répond presque toujours à la
question modeste (repli local), ce qui ne résout pas la requête d'origine —
le bloquer sur ce critère rendrait la proposition quasi jamais déclenchée.

Sinon, un motif factuel est journalisé en `debug` (aucun bruit à l'écran).

### 10.3 Ce que voit l'utilisateur

```text
Mm. Gabriel a percu une POSSIBILITE d'ameliorer son propre code apres le
blocage du 8e moteur (timeline #42) :
  2 point(s), 2 patch(s), 2 simulation(s) propre(s) en sandbox
  (dry-run, depot vivant intact).
  1. [inserer_lignes] src/foo.py:1 — Module sans docstring
     competences : documentation-technique, revue-de-code
  2. [supprimer_lignes] src/bar.py:12 — Import inutilise : math
     competences : revue-de-code, architecture-logicielle
  Aucune ecriture n'a eu lieu. Pour appliquer en sandbox :
  GABRIEL_RECURSIVE_APPLY=1 (dossier data/analyste/sandbox).
```

Une catégorie `marqueur_todo` est volontairement **sans patch** : remplacer un
`TODO` par une implémentation supposée serait une affirmation non vérifiée —
le point est signalé pour arbitrage humain.

### 10.4 Garde-fous rappelés

- Le dépôt vivant n'est **jamais** écrit ; seuls `data/analyste/**` le sont.
- Chaque `supprimer_lignes` est validé **a priori** (la ligne retirée doit
  laisser un module `ast.parse`-able) et **a posteriori** (la sandbox vérifie
  la syntaxe du résultat).
- Les imports étalés sur plusieurs lignes ne sont jamais proposés à la
  suppression.
- `GABRIEL_DEV_ANALYSTE=0` coupe analyste **et** proposition.