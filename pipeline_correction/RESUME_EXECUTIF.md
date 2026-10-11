# 🎯 RÉSUMÉ EXÉCUTIF — PIPELINE DE CORRECTION GABRIEL

## C'est quoi ?

Le **Pipeline de Correction** est une **transmission mécanique** qui transforme vos intentions de correction en modifications précises, vérifiées et restaurables dans le code Gabriel.

---

## Les 3 mots-clés

### 1️⃣ **SCANNER**
- Parcourt tout le dépôt (234 fichiers)
- Crée une cartographie SQLite
- Index : fichiers + rôles + keywords + imports

### 2️⃣ **CHERCHER**
- Retrouve les fichiers par mots-clés
- Propage via le réseau d'imports
- Retourne TOUTES les adresses affectées

### 3️⃣ **APPLIQUER**
- Applique les modifications
- Vérifie la syntaxe
- Sauvegarde l'état original (snapshot)
- Permet le rollback

---

## Cœur du pipeline

**`orchestrator_main.py`** — Le directeur d'orchestre unique

```python
# 1. Scanning
RepoOrchestrator(repo_root, db_path).scan_repo()
RepoOrchestrator(...).build_database()

# 2. Application
VariateurMecanique(repo_root, db_path).executer_contrat(patch.json)

# 3. Restauration
VariateurMecanique(...).restaurer_snapshot(snapshot_id)
```

**`archiviste.py`** — La transmission (cherche dans le réseau)

```python
ArchivisteCorrection(db_path, repo_root).reseau_de_correction(
    mots=["spectral"],
    profondeur=2
)  # → retourne adresses
```

---

## Cas d'usage

### ✅ Corriger un bug partout

Utiliser **propager_texte** :

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral"],
  "profondeur": 2,
  "operation": {"op": "remplacer_texte", ...}
}
```

→ Applique la correction à TOUS les fichiers du réseau.

### ✅ Ajouter une fonction

Utiliser **creer_fichier** :

```json
{"op": "creer_fichier", "cible": "src/utils/new.py", "contenu": "..."}
```

### ✅ Corriger un fichier spécifique

Utiliser **remplacer_texte** :

```json
{"op": "remplacer_texte", "cible": "src/core/spectral_core.py", "ancien_texte": "...", "nouveau_texte": "..."}
```

---

## Workflow standard (10 min)

```
1. Générer DB        : python orchestrator_main.py
2. Créer patch       : mon_patch.json
3. Tester            : --apply-dry-run
4. Appliquer         : --apply mon_patch.json
5. Vérifier Gabriel  : python src/ui/cli.py
6. Committer         : git add -A && git commit
7. Problème ?        : --rollback (retour instantané)
```

---

## 8 types d'opérations

| Type | Cible | Utilité |
|------|------|---------|
| remplacer_texte | 1 fichier | Corriger du code |
| inserer_lignes | 1 fichier | Ajouter à position N |
| supprimer_lignes | 1 fichier | Supprimer lignes N-M |
| ajouter_a_la_fin | 1 fichier | Append à la fin |
| creer_fichier | nouveau | Créer nouveau fichier |
| deployer_fichier | copier | Copier depuis source |
| executer_python | N/A | Lancer script |
| **propager_texte** ⭐ | **TOUS** | Appliquer à TOUS les fichiers du réseau |

---

## Architecture

### Tables SQLite

```
files (234 lignes)
├── rel_path : "src/core/spectral_core.py"
├── role : "spectral"
├── score : 11.8
├── keywords : ["spectral", "core", "python"]
└── imports : ["numpy", "src.utils"]

file_edges (450 lignes)
├── src_path → dst_path : "src/core/orchestrator.py" → "src/core/spectral_core.py"
├── relation : "import" (weight=2.0) ou "role_cluster" (weight=0.7)
└── ...
```

### Snapshots

```
.gabriel_variateur/snapshots/
├── 20260902T150322Z_mon_patch/
│   ├── manifeste.json
│   └── fichiers/
│       ├── a1b2c3d_spectral_core.py.bak
│       └── ...
└── 20260902T140115Z_autre_patch/
    └── ...
```

---

## Fichiers du pipeline

```
pipeline_correction/
├── INDEX.md                    ← Vous êtes ici / Centre de commandes
├── DEMARRAGE_RAPIDE.md         ← 10 minutes pour démarrer
├── GUIDE_UTILISATEUR.md        ← Guide complet avec exemples
├── ANALYSE_APPROFONDIE.md      ← Fonctionnement interne
├── README_PIPELINE.md          ← Référence technique
│
├── orchestrator_main.py        ← CŒUR (56 KB)
│   ├── RepoOrchestrator (scanner)
│   └── VariateurMecanique (application + rollback)
│
├── archiviste.py              ← TRANSMISSION (16 KB)
│   └── ArchivisteCorrection (cherche dans réseau)
│
├── config.py                  ← Configuration
├── __main__.py                ← Entrypoint
├── __init__.py                ← Package Python
│
└── data/
    ├── gabriel_repo_map.db    ← Base SQLite (49 MB)
    └── snapshots/             ← Sauvegardes
```

---

## Commandes essentielles

```bash
# Générer DB (une fois)
python orchestrator_main.py

# Appliquer patch
python orchestrator_main.py --apply mon_patch.json

# Tester sans modifier
python orchestrator_main.py --apply mon_patch.json --apply-dry-run

# Lister snapshots
python orchestrator_main.py --list-snapshots

# Rollback
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# Aide
python orchestrator_main.py --help
```

---

## Garanties

✅ **Sauvegarde automatique** — Snapshot créé avant chaque modification

✅ **Vérification syntaxe** — .py compilé, .json parsé, .yaml validé

✅ **Rollback instantané** — Retour à l'état exact d'avant

✅ **Propagation réseau** — Corrige TOUS les fichiers affectés

✅ **Transparence** — Rapport détaillé de chaque opération

---

## Résolution de cible (comment trouver le fichier)

### Méthode 1 : Chemin explicit

```json
{"cible": "src/core/spectral_core.py"}
```

### Méthode 2 : Keywords + rôle

```json
{"mots_cles": ["spectral"], "role": "core"}
```

Cherche dans la DB les fichiers où keywords contiennent "spectral" ET rôle="core".

### Méthode 3 : Réseau (propager_texte uniquement)

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral"],
  "profondeur": 2
}
```

Cherche les fichiers, puis propage via imports jusqu'à profondeur 2.

---

## Opération puissante : propager_texte

Applique une modification à **TOUS les fichiers du réseau** :

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral", "reconstruction"],
  "role": "core",
  "profondeur": 2,
  "operation": {
    "op": "remplacer_texte",
    "ancien_texte": "OLD_CODE",
    "nouveau_texte": "NEW_CODE"
  }
}
```

**Processus** :

1. Archiviste cherche par mots-clés → trouve 2 fichiers
2. Propage via imports jusqu'à profondeur 2 → trouve 5 fichiers supplémentaires
3. Applique modification à TOUS les 7 fichiers
4. Retourne rapport avec tous les fichiers touchés

---

## Bonnes pratiques

✅ **TOUJOURS** tester avec `--apply-dry-run`

✅ **TOUJOURS** vérifier Gabriel après patch

✅ **TOUJOURS** garder les snapshots

✅ **Utiliser propager_texte** pour corrections globales

✅ **Committer après succès** : `git add -A && git commit`

---

## Pièges à éviter

❌ Appliquer sans tester d'abord

❌ Supprimer `.gabriel_variateur` (contient snapshots)

❌ Modifier la DB à la main

❌ Appliquer plusieurs patchs en même temps

---

## 🚀 Pour commencer

1. Lire **DEMARRAGE_RAPIDE.md** (5 min)
2. Générer la DB : `python orchestrator_main.py`
3. Créer votre patch : `mon_patch.json`
4. Tester : `--apply-dry-run`
5. Appliquer : `--apply mon_patch.json`
6. Vérifier Gabriel

---

## 🆘 En cas de problème

```bash
# Voir la situation
python orchestrator_main.py --list-snapshots

# Restaurer instantanément
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# Vérifier Gabriel
python ../src/ui/cli.py

# Lire le guide
cat GUIDE_UTILISATEUR.md
```

---

## Statut

✅ **Production-ready**

- Cœur implémenté : orchestrator_main.py
- Transmission implémentée : archiviste.py
- Base SQLite operationnelle
- 8 types d'opérations
- Snapshots + rollback
- Documentation complète

---

## Documentation par niveau

| Niveau | Document | Temps |
|--------|----------|-------|
| **Débutant** | DEMARRAGE_RAPIDE.md | 5 min |
| **Utilisateur** | GUIDE_UTILISATEUR.md | 20 min |
| **Contributeur** | ANALYSE_APPROFONDIE.md | 30 min |
| **Référence** | README_PIPELINE.md | 60 min |

---

**Pipeline de Correction v1.0 — orchestrator_main.py + archiviste.py + DB SQLite**

© 2026 Gabriel Pipeline Team
