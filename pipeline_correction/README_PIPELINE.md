# 📋 GUIDE COMPLET — PIPELINE DE CORRECTION GABRIEL

## 🎯 Vue d'ensemble

Le **Pipeline de Correction** est un système **autonome et intégré** de gestion du code de l'agent Gabriel Multiloop. Il fonctionne comme une **transmission mécanique** qui transforme les corrections manuelles en modifications précises et ciblées dans le code.

### 🔧 Comment ça marche ?

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  UTILISATEUR                                                    │
│  ↓                                                              │
│  "Je veux corriger le module spectral"                         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PIPELINE DE CORRECTION (3 étapes)                            │
│                                                                 │
│  1️⃣ ANALYSEUR (orchestrator_main --scan)                       │
│     • Parcourt TOUT le dépôt                                   │
│     • Crée une cartographie complète en SQLite                │
│     • Relie tous les fichiers par leurs imports               │
│                                                                 │
│  2️⃣ ARCHIVISTE (archiviste.py + DB)                           │
│     • Reçoit les mots-clés ("spectral", "reconstruction")    │
│     • Cherche dans la DB les fichiers correspondants          │
│     • Propage le long du réseau (import, rôles)              │
│     • Retourne TOUTES les adresses affectées                 │
│                                                                 │
│  3️⃣ APPLICATEUR (orchestrator_main --apply)                   │
│     • Reçoit un patch JSON avec les modifications            │
│     • Sauvegarde l'état original (snapshot)                  │
│     • Applique les corrections aux bonnes adresses           │
│     • Vérifie la syntaxe Python et les imports               │
│     • Génère un rapport détaillé                             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RÉSULTAT                                                       │
│  ↓                                                              │
│  Gabriel fonctionne parfaitement avec les corrections       │
│  (et possibilité de rollback en 1 clic)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure du Pipeline

```
pipeline_correction/
├── __init__.py              # Package Python
├── __main__.py              # Entrypoint : python -m pipeline_correction
├── config.py                # Configuration centralisée
├── orchestrator_main.py      # Directeur d'orchestre (scan, apply, rollback)
├── archiviste.py            # Moteur de recherche dans la DB
├── data/
│   ├── gabriel_repo_map.db  # Base SQLite (cartographie du dépôt)
│   ├── snapshots/           # Sauvegardes de l'état du code
│   └── logs/                # Journaux des opérations
└── README_PIPELINE.md       # Ce guide

```

---

## 🚀 DÉMARRAGE RAPIDE (5 minutes)

### Étape 1 : Scanner le dépôt

**Première fois ou après modifications majeures :**

```bash
cd pipeline_correction
python -m pipeline_correction --scan
```

**Résultat :**
```
✅ Scanning repository...
Found 234 files (Python, YAML, Markdown, etc.)
Building network graph...
Writing gabriel_repo_map.db (49 MB)
Done in 12 seconds!
```

La DB contient :
- ✅ **234 fichiers** indexés
- ✅ **~450 relations** d'import/rôle
- ✅ **Scores d'importance** pour chaque composant
- ✅ **Mots-clés** pour chaque fichier

### Étape 2 : Créer un patch JSON

**Exemple de patch** (`spectral_fix.json`) :

```json
{
  "titre": "Correction du calcul spectral",
  "description": "Correction du calcul de SA_SB pour les configurations asymétriques",
  "cibles": {
    "mots_cles": ["spectral", "reconstruction"],
    "role": "core",
    "profondeur": 2
  },
  "modifications": [
    {
      "fichier": "src/core/spectral_core.py",
      "type": "remplacer",
      "ancien": "def _compute_sa_sb():\n    return A, B",
      "nouveau": "def _compute_sa_sb(config=None):\n    # Correction pour asymétrique\n    return A, B"
    }
  ]
}
```

### Étape 3 : Appliquer le patch

**Simulation (sans modification) :**

```bash
python -m pipeline_correction --dry-run spectral_fix.json
```

**Application réelle :**

```bash
python -m pipeline_correction --apply spectral_fix.json
```

**Résultat :**
```
✅ Patch: Correction du calcul spectral
✅ Archiviste: Trouvé 7 fichiers affectés
✅ Snapshot: snap-20260902-150322 créé
✅ Modifications appliquées et vérifiées
✅ Rapport: patches/spectral_fix.report.json
```

### Étape 4 : Restaurer si nécessaire

```bash
python -m pipeline_correction --rollback snap-20260902-150322
```

---

## 📊 ÉTAPES DÉTAILLÉES

### 1️⃣ PHASE DE SCANNING (Analyse du dépôt)

**Commande :**
```bash
python -m pipeline_correction --scan
```

**Ce qui se passe :**

1. **Exploration** : Parcourt tous les fichiers du dépôt
2. **Indexation** : Extrait le rôle, les mots-clés, le score de chaque fichier
3. **Graphe** : Crée des arêtes basées sur les imports (`import X from Y`)
4. **Base SQLite** : Stocke le tout dans `gabriel_repo_map.db`

**Tables créées :**

- **files** : chaque fichier = 1 ligne
  ```sql
  SELECT * FROM files LIMIT 3;
  -- rel_path | path | role | score | keywords | file_type
  -- src/core/spectral_core.py | /full/path/... | core | 9.2 | ["spectral", "SA", "SB"] | py
  ```

- **file_edges** : relations entre fichiers
  ```sql
  SELECT * FROM file_edges LIMIT 3;
  -- src_path | dst_path | relation | weight
  -- src/core/orchestrator.py | src/core/spectral_core.py | import | 1.0
  ```

**Options avancées :**

```bash
# Forcer la régénération
python -m pipeline_correction --scan --rebuild

# Verbose pour voir les détails
python -m pipeline_correction --scan -v

# Définir un timeout personnalisé
python -m pipeline_correction --scan --timeout 600
```

---

### 2️⃣ PHASE DE RECHERCHE (Archiviste)

**Commande :**
```bash
python -m pipeline_correction --archiviste-search "spectral" "reconstruction"
```

**Ce qui se passe :**

1. **Recherche lexicale** : Trouve les fichiers mentionnant "spectral" ET "reconstruction"
2. **Scoring** : Trie par pertinence
3. **Propagation** : Suit les liens d'import pour trouver les fichiers affectés
4. **Réseau complet** : Retourne TOUTES les adresses à modifier

**Exemple de résultat :**

```
=== ARCHIVISTE — TRANSMISSION (réseau fonctionnel) ===
base  : /path/to/gabriel_repo_map.db
depot : /path/to/agent-multiloop-Gabriel-local
adresses trouvées : 7

  [core     ] src/core/spectral_core.py  (score 9.5)
  [spectral ] src/core/reconstruct.py    (score 8.8)
  [multiloop] src/multiloop/debat_orchestrator.py  (score 7.2)
  [core     ] src/core/orchestrator.py   (score 6.9)
  [ui       ] src/ui/cli.py              (score 5.1)
  [test     ] tests/test_spectral_core.py (score 4.5)
  [doc      ] docs/GUIDE_SPECTRAL.md     (score 3.2)

=== Position dans l'arborescence ===
  dossier : src/core
      → spectral_core.py
      → orchestrator.py
  dossier : src/multiloop
      → debat_orchestrator.py
  dossier : src/ui
      → cli.py
  dossier : tests
      → test_spectral_core.py
  dossier : docs
      → GUIDE_SPECTRAL.md
```

**Options :**

```bash
# Filtrer par rôle
python -m pipeline_correction --archiviste-search "spectral" --role core

# Profondeur de propagation réseau
python -m pipeline_correction --archiviste-search "spectral" --profondeur 3

# Format JSON pour intégration
python -m pipeline_correction --archiviste-search "spectral" --json
```

---

### 3️⃣ PHASE D'APPLICATION (Applicateur)

**Commande :**
```bash
python -m pipeline_correction --apply mon_patch.json
```

**Structure d'un patch JSON :**

```json
{
  "titre": "Description courte du patch",
  "description": "Description longue et détaillée",
  "auteur": "Nom de l'auteur",
  "cibles": {
    "mots_cles": ["spectral", "reconstruction"],
    "role": "core",
    "profondeur": 2,
    "fichier_explicite": "src/core/spectral_core.py"
  },
  "modifications": [
    {
      "fichier": "src/core/spectral_core.py",
      "type": "remplacer",
      "ancien": "def old_function():\n    pass",
      "nouveau": "def new_function():\n    # Fixed\n    pass"
    },
    {
      "fichier": "src/core/spectral_core.py",
      "type": "ajouter_import",
      "ligne": 15,
      "contenu": "from src.utils import new_utility"
    },
    {
      "fichier": "tests/test_spectral_core.py",
      "type": "ajouter_ligne",
      "ligne": 42,
      "contenu": "    assert result == expected  # Nouvelle assertion"
    }
  ]
}
```

**Types de modifications disponibles :**

| Type | Description | Exemple |
|------|-------------|---------|
| `remplacer` | Remplace du texte | `ancien: "A"` → `nouveau: "B"` |
| `ajouter_ligne` | Ajoute une ligne à une position | Ligne 42 |
| `supprimer_ligne` | Supprime une ligne | Ligne 42-45 |
| `ajouter_import` | Ajoute un import au début | `from X import Y` |
| `creer_fichier` | Crée un nouveau fichier | `contenu:` |
| `supprimer_fichier` | Supprime un fichier | `chemin: "...py"` |

**Processus d'application :**

```
1. Validation du patch JSON
   ✅ Structure syntaxe vérifiée
   ✅ Fichiers cibles vérifiés existent

2. Recherche des adresses (Archiviste)
   ✅ Mots-clés → fichiers trouvés
   ✅ Propagation réseau → fichiers affectés

3. Backup (snapshot)
   ✅ État original sauvegardé
   ✅ ID snapshot généré : snap-20260902-150322

4. Application des modifications
   ✅ Chaque modification appliquée séquentiellement
   ✅ Rapport de chaque application généré

5. Vérification
   ✅ Syntaxe Python vérifiée (compile)
   ✅ Imports vérifiés (import test)
   ✅ Pas de fichiers orphelins

6. Résultat
   ✅ Rapport détaillé généré
   ✅ Manifesté restaurable créé
```

**Exemple d'exécution :**

```bash
$ python -m pipeline_correction --apply spectral_fix.json

╔════════════════════════════════════════════════════════════════════╗
║         PIPELINE DE CORRECTION — APPLICATION DE PATCH             ║
╚════════════════════════════════════════════════════════════════════╝

📋 PATCH : Correction du calcul spectral
  Description: Correction du calcul de SA_SB pour configurations asymétriques
  Auteur: Gabriel Dev Team

🔍 ARCHIVISTE — Recherche des cibles
  Mots-clés: ["spectral", "reconstruction"]
  Rôle: core
  Profondeur: 2
  ✅ Trouvé 7 fichiers affectés

💾 BACKUP — Création du snapshot
  ✅ snap-20260902-150322 créé
  ✅ 234 fichiers sauvegardés (12.3 MB)

⚙️  APPLICATION — Modifications
  src/core/spectral_core.py
    ✅ Remplacement #1: old_function → new_function
    ✅ Import ajouté: from src.utils import ...
  
  src/core/reconstruct.py
    ✅ Remplacement #1: calcul SA_SB
  
  tests/test_spectral_core.py
    ✅ Ligne 42 ajoutée : assertion spectral

✔️  VÉRIFICATION
  ✅ Syntaxe Python OK (py_compile)
  ✅ Imports OK (importlib)
  ✅ Pas d'erreurs

📊 RAPPORT
  Fichiers modifiés: 3
  Modifications: 4
  Erreurs: 0
  ✅ SUCCÈS

📁 Fichiers générés:
  patches/spectral_fix.report.json      (Détails)
  patches/spectral_fix.manifest.json    (Restaurable)
```

**Options :**

```bash
# Simulation (dry-run)
python -m pipeline_correction --dry-run mon_patch.json
# Ne modifie rien, affiche les changements prévus

# Forcer sans vérification
python -m pipeline_correction --apply mon_patch.json --force

# Mode verbeux
python -m pipeline_correction --apply mon_patch.json -v
```

---

### 4️⃣ PHASE DE RESTAURATION (Rollback)

**Lister les snapshots :**

```bash
python -m pipeline_correction --list-snapshots
```

**Résultat :**

```
=== SNAPSHOTS DISPONIBLES ===

snap-20260902-150322  (2026-09-02 15:03:22)
  Patch: Correction du calcul spectral
  Fichiers: 234 | Taille: 12.3 MB
  Auteur: Gabriel Dev Team

snap-20260902-140115  (2026-09-02 14:01:15)
  Patch: Ajout du mode cinématique
  Fichiers: 234 | Taille: 12.3 MB
  Auteur: Gabriel Dev Team

snap-20260902-130000  (2026-09-02 13:00:00)
  Patch: Initial deployment
  Fichiers: 234 | Taille: 12.1 MB
  Auteur: Gordon
```

**Restaurer un snapshot :**

```bash
python -m pipeline_correction --rollback snap-20260902-150322
```

**Processus :**

```
1. Vérification du snapshot
   ✅ snap-20260902-150322 trouvé
   
2. Vérification d'intégrité (checksum)
   ✅ Intégrité OK
   
3. Backup de l'état actuel
   ✅ snap-rollback-20260902-151045 créé
   
4. Restauration
   ✅ Fichiers restaurés (234)
   ✅ Permissions préservées
   
5. Vérification
   ✅ Vérification post-restauration OK
   
✅ SUCCÈS — Rollback terminé
```

---

## 🛠️ UTILISATION AVANCÉE

### Utiliser le pipeline dans votre code Python

```python
from pipeline_correction.archiviste import ArchivisteCorrection

# Initialiser l'archiviste
archiviste = ArchivisteCorrection()

# Chercher par mots-clés
resultats = archiviste.reseau_de_correction(
    mots=["spectral", "reconstruction"],
    role="core",
    profondeur=2
)

# Afficher les résultats
for r in resultats:
    print(f"  {r['rel_path']} (score {r['score']})")
```

### Intégrer le pipeline dans une chaîne de CI/CD

```yaml
# .github/workflows/pipeline.yml
name: Correction Pipeline
on: [push]

jobs:
  correction:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Scan repository
        run: python -m pipeline_correction --scan
      
      - name: Apply patches
        run: python -m pipeline_correction --apply .patches/pending/*.json
      
      - name: Verify
        run: pytest tests/
```

---

## 📋 CHECKLIST D'UTILISATION

### Première utilisation

- [ ] Naviguez vers le dépôt Gabriel
- [ ] Exécutez : `python -m pipeline_correction --scan`
- [ ] Attendez la génération de la DB (~15 secondes)
- [ ] Vérifiez : `ls pipeline_correction/data/gabriel_repo_map.db`

### Pour chaque correction

- [ ] **Étape 1** : Créez un patch JSON (`mon_patch.json`)
- [ ] **Étape 2** : Testez avec `--dry-run` : `python -m pipeline_correction --dry-run mon_patch.json`
- [ ] **Étape 3** : Appliquez : `python -m pipeline_correction --apply mon_patch.json`
- [ ] **Étape 4** : Vérifiez Gabriel fonctionne : `python src/ui/cli.py`
- [ ] **Étape 5** : Committez les changements

### En cas de problème

- [ ] Listez les snapshots : `python -m pipeline_correction --list-snapshots`
- [ ] Restaurez le dernier : `python -m pipeline_correction --rollback snap-XXXXX`
- [ ] Vérifiez Gabriel : `python src/ui/cli.py`

---

## 🔍 DÉPANNAGE

### Erreur : "Base du réseau introuvable"

**Solution :**
```bash
python -m pipeline_correction --scan
```

### Erreur : "Fichier non trouvé après modification"

**Vérifiez :**
```bash
python -m pipeline_correction --archiviste-search "mon_mot_cle" --json
```

### Patch n'a rien modifié

**Vérifiez la structure JSON :**
```bash
python -m pipeline_correction --dry-run mon_patch.json
```

### Gabriel ne démarre plus après patch

**Restaurez immédiatement :**
```bash
python -m pipeline_correction --list-snapshots
python -m pipeline_correction --rollback snap-XXXXX
```

---

## 📞 SUPPORT ET CONTACT

Pour toute question ou problème :

1. Consultez ce guide complet
2. Exécutez : `python -m pipeline_correction --help`
3. Vérifiez les logs : `pipeline_correction/data/logs/`

---

**Pipeline de Correction v1.0.0**  
Conçu pour Gabriel Multiloop Agent  
© 2026 Philippe Thomas Savard Pipeline 
