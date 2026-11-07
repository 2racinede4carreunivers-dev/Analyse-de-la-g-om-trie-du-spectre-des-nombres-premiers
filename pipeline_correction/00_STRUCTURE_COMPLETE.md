# 📁 STRUCTURE COMPLÈTE DU PIPELINE DE CORRECTION

```
agent-multiloop-Gabriel-local/
└── pipeline_correction/                    ← CENTRE DE COMMANDES
    │
    ├── 📘 DOCUMENTATION
    │   ├── INDEX.md                        ← 📍 VOUS ÊTES ICI (navigation principale)
    │   ├── DEMARRAGE_RAPIDE.md             ← ⚡ 10 minutes pour démarrer
    │   ├── GUIDE_UTILISATEUR.md            ← 📖 Guide complet avec cas d'usage
    │   ├── RESUME_EXECUTIF.md              ← 🎯 Vue d'ensemble (cette fiche)
    │   ├── ANALYSE_APPROFONDIE.md          ← 🔬 Fonctionnement interne
    │   └── README_PIPELINE.md              ← 📚 Référence technique
    │
    ├── 🔧 CODE PRINCIPAL
    │   ├── orchestrator_main.py            ← ⭐ CŒUR DU PIPELINE (56 KB)
    │   │                                      RepoOrchestrator (scanning)
    │   │                                      VariateurMecanique (application)
    │   │
    │   ├── archiviste.py                   ← 🔗 TRANSMISSION (16 KB)
    │   │                                      ArchivisteCorrection (recherche réseau)
    │   │
    │   ├── config.py                       ← ⚙️ Configuration centralisée
    │   ├── __main__.py                     ← 🚀 Entrypoint du package
    │   └── __init__.py                     ← 📦 Package Python
    │
    └── 📊 DONNÉES
        └── data/
            ├── gabriel_repo_map.db         ← 🗄️ Base SQLite (49 MB)
            │                                  - Table 'files' (234 fichiers)
            │                                  - Table 'file_edges' (450 relations)
            │                                  - Cartographie complète du dépôt
            │
            ├── snapshots/                  ← 💾 Sauvegardes (rollback)
            │   ├── 20260902T150322Z_mon_patch/
            │   │   ├── manifeste.json
            │   │   ├── fichiers/
            │   │   │   ├── a1b2c3d_spectral_core.py.bak
            │   │   │   └── ...
            │   │   └── exec/
            │   │       └── op_7.py
            │   └── 20260902T140115Z_autre_patch/
            │       └── ...
            │
            └── logs/                       ← 📝 Journaux d'opérations
                └── ...
```

---

## 📍 NAVIGATION RAPIDE

### Pour **débuter** (5-10 minutes)

```
1. Vous êtes nouveau ?
   → Lire : DEMARRAGE_RAPIDE.md

2. Besoin du mode d'emploi ?
   → Lire : GUIDE_UTILISATEUR.md

3. Où commencer ?
   → Lire : INDEX.md (vous êtes ici)
```

### Pour **comprendre** le fonctionnement

```
1. Vue d'ensemble ?
   → Lire : RESUME_EXECUTIF.md

2. Fonctionnement interne ?
   → Lire : ANALYSE_APPROFONDIE.md

3. Référence complète ?
   → Lire : README_PIPELINE.md
```

### Pour **utiliser** le pipeline

```
1. Générer la cartographie
   $ python orchestrator_main.py

2. Créer un patch
   $ Éditer mon_patch.json

3. Tester sans risque
   $ python orchestrator_main.py --apply mon_patch.json --apply-dry-run

4. Appliquer
   $ python orchestrator_main.py --apply mon_patch.json

5. Restaurer en cas de problème
   $ python orchestrator_main.py --list-snapshots
   $ python orchestrator_main.py --rollback <SNAPSHOT_ID>
```

---

## 🎯 LES 3 FICHIERS CLÉS

### 1. orchestrator_main.py (56 KB) ⭐

**Le cœur du pipeline**

- Classe `RepoOrchestrator` : Scanner du dépôt
- Classe `VariateurMecanique` : Application des patches
- Crée et utilise `gabriel_repo_map.db`
- Point d'entrée principal

### 2. archiviste.py (16 KB) 🔗

**La transmission (recherche dans le réseau)**

- Classe `ArchivisteCorrection` : Moteur de recherche
- Consulte `gabriel_repo_map.db` (tables `files`, `file_edges`)
- Cherche par mots-clés
- Propage via réseau d'imports
- Retourne TOUTES les adresses affectées

### 3. data/gabriel_repo_map.db (49 MB) 🗄️

**La base de données (cartographie du dépôt)**

```sql
-- 234 fichiers avec métadonnées
SELECT * FROM files LIMIT 3;

-- 450 relations (import, rôle_cluster)
SELECT * FROM file_edges LIMIT 3;

-- Historique
SELECT * FROM snapshots;
```

---

## 🔄 FLUX DE DONNÉES

```
1. SCANNER
   orchestrator_main.py
   └── RepoOrchestrator.scan_repo()
       ├── Parcourt 234 fichiers
       ├── Détecte rôles, keywords, imports
       ├── Calcule scores
       └── → list[FileScanResult]

2. INDEXATION
   orchestrator_main.py
   └── RepoOrchestrator.build_database()
       ├── Crée Table 'files' (234 lignes)
       ├── Crée Table 'file_edges' (450 relations)
       └── → gabriel_repo_map.db

3. RECHERCHE (optionnel)
   archiviste.py
   └── ArchivisteCorrection.reseau_de_correction()
       ├── Cherche par mots-clés dans 'files'
       ├── Propage via 'file_edges' (profondeur)
       └── → list[adresses]

4. APPLICATION
   orchestrator_main.py
   └── VariateurMecanique.executer_contrat()
       ├── Lit patch JSON
       ├── Résout les cibles
       ├── Crée snapshot
       ├── Applique opérations
       ├── Vérifie syntaxe
       └── → Rapport + Snapshot

5. RESTAURATION (en cas de problème)
   orchestrator_main.py
   └── VariateurMecanique.restaurer_snapshot()
       ├── Lit manifeste.json
       ├── Restaure fichiers sauvegardés
       └── → État exact d'avant
```

---

## 📊 CONTENU DE LA BASE SQLite

### Table `files`

```
id  | rel_path | role | score | keywords | imports | file_type
----|----------|------|-------|----------|---------|----------
1   | src/core/spectral_core.py | spectral | 11.8 | ["spectral","core"] | ["numpy"] | python
2   | src/core/reconstruct.py | core | 9.2 | ["core"] | ["spectral_core"] | python
3   | tests/test_spectral.py | test | 4.5 | ["test"] | ["spectral_core"] | python
... | ... | ... | ... | ... | ... | ...
```

**234 lignes** (1 par fichier)

### Table `file_edges`

```
src_path | dst_path | relation | weight
---------|----------|----------|-------
src/core/orchestrator.py | src/core/spectral_core.py | import | 2.0
src/core/spectral_core.py | src/core/reconstruct.py | role_cluster | 0.7
... | ... | ... | ...
```

**450 lignes** (relations entre fichiers)

---

## 💾 STRUCTURE D'UN SNAPSHOT

```
.gabriel_variateur/snapshots/
└── 20260902T150322Z_mon_patch/
    │
    ├── manifeste.json
    │   {
    │     "version": "1.0",
    │     "horodatage": "2026-09-02T15:03:22Z",
    │     "contrat": "/path/to/mon_patch.json",
    │     "repo_root": "/path/to/agent-multiloop-Gabriel-local",
    │     "fichiers": [
    │       {"rel": "src/core/spectral_core.py", "existed_before": true, 
    │        "backup_relatif": "fichiers/a1b2c3d_spectral_core.py.bak"},
    │       ...
    │     ]
    │   }
    │
    ├── fichiers/
    │   ├── a1b2c3d_spectral_core.py.bak      ← État original
    │   ├── x9y8z7w6_reconstruct.py.bak       ← État original
    │   └── ...
    │
    └── exec/
        └── op_7.py                            ← Scripts exécutés (si executer_python)
```

---

## 🚀 COMMANDES PRINCIPALES

```bash
# Générer la cartographie (une fois)
$ python orchestrator_main.py

# Appliquer un patch
$ python orchestrator_main.py --apply mon_patch.json

# Tester sans modifier (RECOMMANDÉ)
$ python orchestrator_main.py --apply mon_patch.json --apply-dry-run

# Mode strict (échoue à première erreur)
$ python orchestrator_main.py --apply mon_patch.json --apply-strict

# Lister les snapshots
$ python orchestrator_main.py --list-snapshots

# Restaurer un snapshot
$ python orchestrator_main.py --rollback <SNAPSHOT_ID>

# Aide complète
$ python orchestrator_main.py --help
```

---

## 📚 DOCUMENTATION PAR CAS D'USAGE

| Cas | Document | Étapes |
|-----|----------|--------|
| **Je veux démarrer rapidement** | DEMARRAGE_RAPIDE.md | 10 min |
| **Je veux comprendre l'outil** | GUIDE_UTILISATEUR.md | 20 min |
| **Je veux voir les exemples** | GUIDE_UTILISATEUR.md (cas complets) | 15 min |
| **Je veux comprendre l'architecture** | ANALYSE_APPROFONDIE.md | 30 min |
| **Je veux la référence technique** | README_PIPELINE.md | 60 min |
| **Je veux un résumé** | RESUME_EXECUTIF.md | 5 min |

---

## ✅ CHECKLIST D'INSTALLATION

- [ ] Dossier `pipeline_correction/` créé
- [ ] Fichiers Python présents : orchestrator_main.py, archiviste.py, config.py
- [ ] Documentation présente : tous les .md
- [ ] Dossier `data/` créé
- [ ] Base SQLite générée : `python orchestrator_main.py`

---

## 🎓 CONCEPTS CLÉS

### Scanner (RepoOrchestrator)
Analyse chaque fichier : role, keywords, imports, score.

### Base SQLite
Stocke fichiers + relations (imports, rôles).

### Archiviste (ArchivisteCorrection)
Cherche dans la base par mots-clés, propage via réseau.

### Variateur (VariateurMecanique)
Applique patches, crée snapshots, fait rollback.

### Propagation (propager_texte)
Opération unique qui applique à TOUS les fichiers du réseau.

### Snapshot
Sauvegarde automatique de l'état avant modification.

---

## 🔐 Sécurité

✅ **Snapshots automatiques** — Rollback toujours possible

✅ **Vérification syntaxe** — .py, .json, .yaml validés

✅ **Backup avant modification** — État original préservé

✅ **Manifeste** — Trace complète de ce qui a changé

✅ **Checksum** — Intégrité vérifiée lors du rollback

---

## 🏆 Avantages

✅ Corrections globales en 1 clic (propager_texte)

✅ Automatisation totale (pas d'erreurs manuelles)

✅ Rollback instantané (pas de panique)

✅ Traçabilité complète (snapshots + manifestes)

✅ Vérification systématique (pas de bogue)

---

## 📞 SUPPORT

```
Problème ? → Consulter DEMARRAGE_RAPIDE.md
Besoin d'aide ? → Consulter GUIDE_UTILISATEUR.md
Ça ne marche pas ? → Lire ANALYSE_APPROFONDIE.md
Urgent ? → python orchestrator_main.py --rollback <SNAPSHOT>
```

---

**🎯 Vous êtes prêt ! Allez à DEMARRAGE_RAPIDE.md ou GUIDE_UTILISATEUR.md**

© 2026 Gabriel Pipeline Team
