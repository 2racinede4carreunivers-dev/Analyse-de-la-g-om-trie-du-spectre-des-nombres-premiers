# 🎯 PIPELINE DE CORRECTION GABRIEL — CENTRE DE COMMANDES

## 📍 Vous êtes ici

```
agent-multiloop-Gabriel-local/
└── pipeline_correction/          ← VOUS ÊTES ICI
    ├── 📘 GUIDE_UTILISATEUR.md   ← COMMENCEZ ICI (guide complet)
    ├── 🔬 ANALYSE_APPROFONDIE.md ← Comprendre le fonctionnement
    ├── 📖 README_PIPELINE.md     ← Documentation technique
    ├── orchestrator_main.py       ← CŒUR (répertoire + variateur)
    ├── archiviste.py             ← TRANSMISSION (réseau)
    ├── config.py                 ← Configuration
    ├── __main__.py               ← Entrypoint
    ├── __init__.py               ← Package Python
    └── data/
        ├── gabriel_repo_map.db   ← Base SQLite (cartographie)
        └── snapshots/            ← Sauvegardes
```

---

## ⚡ COMMANDES RAPIDES

### 🔧 Générer la cartographie (première fois)

```bash
cd pipeline_correction
python orchestrator_main.py
```

### 🎯 Appliquer un patch

```bash
python orchestrator_main.py --apply mon_patch.json
```

### 🧪 Tester sans modifier

```bash
python orchestrator_main.py --apply mon_patch.json --apply-dry-run
```

### 📋 Lister les sauvegardes

```bash
python orchestrator_main.py --list-snapshots
```

### ↩️ Restaurer une sauvegarde

```bash
python orchestrator_main.py --rollback <SNAPSHOT_ID>
```

---

## 📚 DOCUMENTATION

| Document | Contenu | Pour qui ? |
|----------|---------|-----------|
| **GUIDE_UTILISATEUR.md** | Guide pratique complet + exemples | Utilisateurs (start here) |
| **ANALYSE_APPROFONDIE.md** | Fonctionnement interne détaillé | Développeurs |
| **README_PIPELINE.md** | Référence technique | Contributeurs |

---

## 🏗️ ARCHITECTURE

### Trois composantes

1. **RepoOrchestrator** (orchestrator_main.py)
   - Scanne le dépôt
   - Indexe fichiers, rôles, keywords, imports
   - Crée la DB SQLite

2. **ArchivisteCorrection** (archiviste.py)
   - Cherche dans la DB par mots-clés
   - Propage via réseau d'imports
   - Retourne tous les fichiers affectés

3. **VariateurMécanique** (orchestrator_main.py)
   - Applique les patches
   - Sauvegarde états (snapshots)
   - Restaure en rollback

### Base de données

**gabriel_repo_map.db** (SQLite) :
- Table `files` : 234 fichiers indexés
- Table `file_edges` : 450 relations (import, rôle_cluster)
- Table `snapshots` : historique des opérations

---

## 🚀 WORKFLOW COMPLET

```
1. SCANNER (une fois)
   python orchestrator_main.py
   → Crée data/gabriel_repo_map.db

2. CRÉER PATCH
   Fichier mon_patch.json avec mots-clés / cible

3. TESTER
   python orchestrator_main.py --apply mon_patch.json --apply-dry-run
   → Montre ce qui sera modifié

4. APPLIQUER
   python orchestrator_main.py --apply mon_patch.json
   → Applique réellement + crée snapshot

5. VÉRIFIER
   python src/ui/cli.py
   → Gabriel fonctionne ?

6. PROBLÈME ?
   python orchestrator_main.py --list-snapshots
   python orchestrator_main.py --rollback <SNAPSHOT>
   → Retour à l'état antérieur
```

---

## 🔑 CONCEPTS CLÉS

### **Cible d'une opération**

Deux façons de spécifier **QUEL fichier modifier** :

1. **Chemin explicite** :
   ```json
   {"cible": "src/core/spectral_core.py"}
   ```

2. **Mots-clés + rôle** (cherche dans la DB) :
   ```json
   {"mots_cles": ["spectral"], "role": "core"}
   ```

### **Propagation (propager_texte)**

L'opération la plus puissante : applique une modification à **TOUS les fichiers du réseau** :

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral", "reconstruction"],
  "profondeur": 2,
  "operation": {
    "op": "remplacer_texte",
    "ancien_texte": "old",
    "nouveau_texte": "new"
  }
}
```

Processus :
1. Archiviste cherche par mots-clés
2. Propage via imports jusqu'à profondeur 2
3. Applique modification à TOUS les fichiers trouvés
4. Retourne rapport avec fichiers touchés

### **Snapshot (sauvegarde)**

Avant chaque application, tous les fichiers modifiés sont sauvegardés :

```
.gabriel_variateur/snapshots/
└── 20260902T150322Z_mon_patch/
    ├── manifeste.json              ← Métadonnées
    └── fichiers/
        ├── a1b2c3d_spectral_core.py.bak
        └── ...
```

Permet de restaurer l'état exact avec `--rollback`.

---

## ✅ AVANT D'UTILISER

- [ ] Avez-vous lu **GUIDE_UTILISATEUR.md** ?
- [ ] Avez-vous généré la DB ? (`python orchestrator_main.py`)
- [ ] Avez-vous testé le patch ? (`--apply-dry-run`)
- [ ] Gabriel fonctionnait avant le patch ?
- [ ] Vous avez un snapshot de secours ?

---

## ❌ SI QUELQUE CHOSE NE VA PAS

```bash
# 1. Voir les snapshots
python orchestrator_main.py --list-snapshots

# 2. Restaurer
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# 3. Vérifier Gabriel
python src/ui/cli.py
```

---

## 📞 RÉSUMÉ DES COMMANDES

```bash
# Générer la cartographie
python orchestrator_main.py

# Appliquer un patch
python orchestrator_main.py --apply <patch.json>

# Tester sans modifier
python orchestrator_main.py --apply <patch.json> --apply-dry-run

# Mode strict (échoue à première erreur)
python orchestrator_main.py --apply <patch.json> --apply-strict

# Lister les snapshots
python orchestrator_main.py --list-snapshots

# Restaurer un snapshot
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# Aide
python orchestrator_main.py --help
```

---

## 🎓 CAS D'USAGE TYPIQUES

### Corriger un bug partout

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral"],
  "profondeur": 2,
  "operation": {
    "op": "remplacer_texte",
    "ancien_texte": "BUG",
    "nouveau_texte": "FIXED"
  }
}
```

### Ajouter une fonction

```json
{
  "op": "creer_fichier",
  "cible": "src/utils/new_util.py",
  "contenu": "def new_function():\n    pass"
}
```

### Ajouter un test partout

```json
{
  "op": "propager_texte",
  "mots_cles": ["test"],
  "operation": {
    "op": "ajouter_a_la_fin",
    "contenu": "\n\ndef test_new():\n    assert True"
  }
}
```

---

## 🔬 POUR LES DÉVELOPPEURS

Voir **ANALYSE_APPROFONDIE.md** pour :
- Architecture interne
- Classes (RepoOrchestrator, VariateurMecanique, ArchivisteCorrection)
- Tables SQLite
- Flux de données

---

## 📄 FICHIERS DU PIPELINE

```
orchestrator_main.py (56 KB)
  ├── RepoOrchestrator
  │   ├── scan_repo() → indexation
  │   └── build_database() → création DB
  └── VariateurMecanique
      ├── charger_contrat() → parse patch JSON
      ├── executer_contrat() → applique opérations
      └── restaurer_snapshot() → rollback

archiviste.py (16 KB)
  ├── ArchivisteCorrection
  │   ├── chercher_par_mots() → recherche lexicale
  │   ├── voisinage() → propagation réseau
  │   └── reseau_de_correction() → adresses complètes

config.py (6 KB)
  └── Configuration centralisée

data/
  ├── gabriel_repo_map.db (49 MB) ← Base SQLite
  └── snapshots/ ← Sauvegardes des états
```

---

**🚀 Prêt à corriger Gabriel ? Allez à GUIDE_UTILISATEUR.md**

© 2026 Gabriel Pipeline Team
