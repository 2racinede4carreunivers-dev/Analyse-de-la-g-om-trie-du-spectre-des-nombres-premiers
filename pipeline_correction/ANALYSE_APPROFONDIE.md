# 🔬 ANALYSE APPROFONDIE DU PIPELINE DE CORRECTION GABRIEL

## 📌 LE PIPELINE RÉEL EN 4 PHASES

### **PHASE 1 : SCANNING DES FICHIERS (RepoOrchestrator.scan_repo)**

```python
class RepoOrchestrator:
    def scan_repo() -> list[FileScanResult]:
```

**Objectif** : Parcourir TOUT le dépôt et créer une liste de fichiers avec leurs métadonnées.

**Processus :**

1. **Itération récursive** (`_iter_files`)
   - Parcourt tous les fichiers du dépôt
   - Exclut les répertoires (.git, __pycache__, .venv, etc.)
   - Ignore les extensions binaires (.pyc, .png, .jpg, .pdf, etc.)

2. **Détection de rôle** (`_detect_role`)
   - Analyse le chemin et le nom du fichier
   - Cherche des keywords : "spectral", "multiloop", "core", "hol", "ui", etc.
   - Affecte un rôle : core, spectral, multiloop, hol, ui, memory, vision, test, doc, data

3. **Extraction de mots-clés** (`_extract_keywords`)
   - Parcourt le chemin du fichier
   - Extrait tous les mots-clés pertinents
   - Chaque fichier peut avoir plusieurs mots-clés

4. **Extraction des imports Python** (`_extract_python_imports`)
   - Parse l'AST des fichiers `.py`
   - Extrait tous les imports (`import X`, `from Y import Z`)
   - Crée une liste d'imports pour chaque fichier

5. **Calcul du score** (`_compute_score`)
   - Score de base : 1.0
   - +4.0 si dans "src" ou "core"
   - +5.5 si contient "spectral", "multiloop", "hol"
   - +7.0 si "main.py", "pipeline", "orchestr"
   - +1.5 si test
   - +0.7 si markdown
   - +0.6 * nombre de keywords
   - +0.25 * nombre d'imports

**Résultat** : `list[FileScanResult]` avec ~234 fichiers

```
FileScanResult(
    path="/full/path/src/core/spectral_core.py",
    rel_path="src/core/spectral_core.py",
    extension=".py",
    file_type="python",
    role="spectral",
    size_bytes=45236,
    modified_iso="2026-08-30T14:32:00Z",
    keywords=["spectral", "core", "python"],
    imports=["numpy", "src.utils", "src.core.reconstruct"],
    score=11.8
)
```

---

### **PHASE 2 : CONSTRUCTION DE LA BASE SQLite (build_database)**

```python
def build_database(files: list[FileScanResult]) -> dict:
```

**Objectif** : Créer une base SQLite avec les fichiers ET les relations entre eux.

**Processus :**

#### **Table 1 : `files`**

Stocke chaque fichier indexé :

```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY,
    path TEXT UNIQUE,
    rel_path TEXT,
    extension TEXT,
    file_type TEXT,
    role TEXT,
    size_bytes INTEGER,
    modified_iso TEXT,
    keywords TEXT (JSON),
    imports TEXT (JSON),
    score REAL,
    created_at TEXT
)
```

**Exemple** :

```
| id | rel_path | role | score | keywords | imports |
|----|----------|------|-------|----------|---------|
| 1 | src/core/spectral_core.py | spectral | 11.8 | ["spectral","core","python"] | ["numpy","src.utils"] |
| 2 | src/core/reconstruct.py | core | 9.2 | ["core","python"] | ["src.core.spectral_core"] |
| 234 | tests/test_spectral.py | test | 4.5 | ["test","python"] | ["src.core.spectral_core","pytest"] |
```

#### **Table 2 : `file_edges`**

Crée des RELATIONS entre fichiers (le cœur du réseau) :

```sql
CREATE TABLE file_edges (
    id INTEGER PRIMARY KEY,
    src_path TEXT,
    dst_path TEXT,
    relation TEXT,        -- "import" ou "role_cluster"
    weight REAL,           -- 2.0 pour import, 0.7 pour role_cluster
    created_at TEXT
)
```

**Deux types de relations** :

1. **"import"** (weight=2.0) : src_path importe dst_path
   ```
   src/core/orchestrator.py → src/core/spectral_core.py (import)
   src/multiloop/debat.py → src/core/spectral_core.py (import)
   ```

2. **"role_cluster"** (weight=0.7) : fichiers du même rôle
   ```
   src/core/spectral_core.py ↔ src/core/reconstruct.py (rôle=core)
   src/core/orchestrator.py ↔ src/core/spectral_core.py (rôle=core)
   ```

**Résultat** : ~450 relations créées

---

### **PHASE 3 : RECHERCHE DES FICHIERS (Archiviste + Transmission)**

Quand l'utilisateur veut corriger "spectral reconstruction", le pipeline utilise `archiviste.py` :

```python
archiviste = ArchivisteCorrection(db_path, repo_root)
resultats = archiviste.reseau_de_correction(
    mots=["spectral", "reconstruction"],
    role="core",
    profondeur=2
)
```

**Processus (3 étapes) :**

#### **Étape 1 : Recherche lexicale dans la DB**

Cherche les fichiers dont le chemin/rôle/keywords contiennent "spectral" ET "reconstruction" :

```sql
SELECT * FROM files 
WHERE keywords LIKE '%spectral%' OR keywords LIKE '%reconstruction%'
ORDER BY score DESC
```

Trouvé : `src/core/spectral_core.py`, `src/core/reconstruct.py`

#### **Étape 2 : Propagation du réseau (BFS)**

Pour chaque fichier trouvé, remonte les relations d'import jusqu'à profondeur 2 :

```
src/core/spectral_core.py (trouvé)
  ↓ (import relation)
src/multiloop/debat_orchestrator.py (profondeur 1)
  ↓ (import relation)
src/ui/cli.py (profondeur 2)
  ↓ (role_cluster relation)
src/core/reconstruct.py (profondeur 1)
```

Résultat : 7 fichiers affectés

#### **Étape 3 : Retour des adresses**

```python
[
    {"rel_path": "src/core/spectral_core.py", "type": "correspondance", "score": 11.8},
    {"rel_path": "src/core/reconstruct.py", "type": "correspondance", "score": 9.2},
    {"rel_path": "src/multiloop/debat_orchestrator.py", "type": "voisin_réseau", "score": 7.1},
    {"rel_path": "src/core/orchestrator.py", "type": "voisin_réseau", "score": 6.9},
    ...
]
```

---

### **PHASE 4 : APPLICATION DU PATCH (VariateurMecanique)**

Le patch JSON décrit les modifications. Le Variateur les applique :

```python
variateur = VariateurMecanique(repo_root, db_path)
rapport = variateur.executer_contrat(
    Path("mon_patch.json"),
    dry_run=False,
    strict=False
)
```

#### **Processus d'exécution** :

```
Pour chaque opération dans le patch :

1. NORMALISATION
   - Alias anglais → français (replace_text → remplacer_texte)
   - Validation de la structure

2. RÉSOLUTION DE CIBLE
   - Si cible donnée : cherche le fichier complet chemin
   - Si mots-clés donnés : appelle l'archiviste (réseau)
   - Résultat : Path exacte du fichier

3. SAUVEGARDE (snapshot)
   - Copie l'état original → .gabriel_variateur/snapshots/<id>/fichiers/
   - Crée un manifeste JSON restaurable

4. ÉDITION
   Selon le type d'opération :
   - remplacer_texte : replace() sur le contenu
   - inserer_lignes : insère lignes à position N
   - supprimer_lignes : supprime lignes N à M
   - ajouter_a_la_fin : append() à la fin
   - creer_fichier : crée nouveau fichier
   - deployer_fichier : copie depuis source
   - propager_texte : applique à TOUS les fichiers du réseau
   - executer_python : lance un script Python

5. VÉRIFICATION
   - py_compile pour .py (syntaxe Python)
   - json.loads pour .json (syntaxe JSON)
   - yaml.safe_load pour .yaml (optionnel)

6. RAPPORT
   - Logs de chaque opération
   - Statut : ok / simule / echouee
   - Manifeste pour rollback
```

#### **Le type d'opération CRUCIAL : "propager_texte"**

C'est l'opération qui fait la **TRANSMISSION** :

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral", "reconstruction"],
  "role": "core",
  "profondeur": 2,
  "operation": {
    "op": "remplacer_texte",
    "ancien_texte": "def old_func():",
    "nouveau_texte": "def new_func():"
  }
}
```

**Processus** :

1. Appelle l'archiviste : `reseau_de_correction(["spectral", "reconstruction"])`
2. Reçoit 7 fichiers affectés
3. Applique l'opération "remplacer_texte" à CHACUN des 7 fichiers
4. Retourne rapport avec tous les fichiers touchés

---

## 🎯 LES 3 COMPOSANTES PRINCIPALES

### **1. RepoOrchestrator (Classe)**

**Responsabilité** : Scander et indexer

```python
RepoOrchestrator(repo_root, db_path)
  ├── scan_repo() → list[FileScanResult]
  ├── build_database(files) → gabriel_repo_map.db
  └── print_summary()
```

### **2. ArchivisteCorrection (Classe dans archiviste.py)**

**Responsabilité** : Chercher et propager

```python
ArchivisteCorrection(db_path, repo_root)
  ├── chercher_par_mots(mots, role) → list[fichiers]
  ├── voisinage(fichier, profondeur) → list[fichiers voisins]
  └── reseau_de_correction(mots, role, profondeur) → list[adresses]
```

### **3. VariateurMecanique (Classe)**

**Responsabilité** : Appliquer et restaurer

```python
VariateurMecanique(repo_root, db_path)
  ├── charger_contrat(patch.json) → dict
  ├── executer_contrat() → rapport (OK/échouée)
  ├── restaurer_snapshot() → rollback
  └── lister_snapshots() → list[snapshots]
```

---

## 🔄 LE FLUX COMPLET

```
UTILISATEUR
    ↓
"Je veux corriger le spectral"
    ↓
ORCHESTRATOR_MAIN.PY (main())
    ↓
┌─ Mode 1 : SCANNER
│  $ python orchestrator_main.py
│  → RepoOrchestrator.scan_repo()
│  → RepoOrchestrator.build_database()
│  → Crée gabriel_repo_map.db
│
├─ Mode 2 : APPLIQUER
│  $ python orchestrator_main.py --apply mon_patch.json
│  → VariateurMecanique.executer_contrat()
│  → Pour chaque opération :
│    ├── _resoudre_cible() (cherche le fichier)
│    ├── _sauvegarder_fichier() (backup)
│    ├── _editer_fichier() (applique la modification)
│    └── _verifier_syntaxe() (vérifie)
│  → Retourne rapport
│
├─ Mode 3 : PROPAGATION (propager_texte)
│  → VariateurMecanique._executer_propagation()
│  → Appelle ArchivisteCorrection.reseau_de_correction()
│  → Applique modification à TOUS les fichiers du réseau
│
└─ Mode 4 : RESTAURATION
   $ python orchestrator_main.py --rollback snap-XXX
   → VariateurMecanique.restaurer_snapshot()
   → Restaure l'état d'avant le patch

GABRIEL FONCTIONNE CORRECTEMENT ✅
```

---

## 📊 LES FICHIERS DU PIPELINE

```
pipeline_correction/
├── orchestrator_main.py     ← CŒUR (RepoOrchestrator + VariateurMecanique)
├── archiviste.py            ← TRANSMISSION (cherche dans le réseau)
├── config.py                ← Configuration centralisée
├── __main__.py              ← Entrypoint
├── __init__.py              ← Package Python
├── data/
│   ├── gabriel_repo_map.db  ← La cartographie (base SQLite)
│   ├── snapshots/           ← Sauvegardes du variateur
│   └── logs/                ← Journaux
└── README_PIPELINE.md       ← Ce guide
```

---

## ✅ RÉSUMÉ

| Composante | Fichier | Classe | Rôle |
|-----------|---------|--------|------|
| **Orchestrator Principal** | orchestrator_main.py | RepoOrchestrator | Scanner : crée la DB |
| **Variateur Mécanique** | orchestrator_main.py | VariateurMecanique | Applique patches + restaure |
| **Transmission** | archiviste.py | ArchivisteCorrection | Cherche fichiers dans le réseau |
| **Base de données** | data/gabriel_repo_map.db | SQLite | Stocke fichiers + relations |
| **Snapshots** | .gabriel_variateur/snapshots/ | JSON + fichiers | Sauvegarde états antérieurs |

---

**Ce pipeline est une "transmission mécanique" : il transforme les intentions de correction en modifications précises, ciblées et vérifiées.**

