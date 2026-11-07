# 📘 GUIDE UTILISATEUR COMPLET — PIPELINE DE CORRECTION GABRIEL

**Version Corrigée basée sur analyse approfondie d'orchestrator_main.py**

---

## 🎯 QU'EST-CE QUE LE PIPELINE ?

Le **Pipeline de Correction** est une **transmission mécanique** de programmation qui :

1. **SCANNE** le dépôt complet → crée une cartographie SQLite
2. **CHERCHE** les fichiers affectés par les mots-clés → retrouve toutes les adresses
3. **APPLIQUE** les modifications aux bons fichiers → vérification syntaxe + backup
4. **RESTAURE** en cas de problème → rollback automatique

**Cœur du pipeline** : `orchestrator_main.py`

---

## 🚀 DÉMARRAGE RAPIDE (5 minutes)

### Étape 1 : Générer la base SQLite

**Première fois ou après modifications majeures du code :**

```bash
cd pipeline_correction
python orchestrator_main.py
```

**Qu'il se passe :**

```
RepoOrchestrator.scan_repo()
  → Parcourt 234 fichiers
  → Détecte rôles, keywords, imports
  → Score calculé pour chaque fichier

RepoOrchestrator.build_database()
  → Crée table 'files' (234 lignes)
  → Crée table 'file_edges' (450 relations)
  → Enregistre dans sqlite3

Résultat : data/gabriel_repo_map.db (49 MB)
```

**Résultat affichage :**

```
=== Gabriel repository orchestrator ===
repo root : /path/to/agent-multiloop-Gabriel-local
total files : 234
total edges : 450

Top roles:
  - core: 45
  - test: 38
  - multiloop: 32
  - spectral: 28
  - ui: 18
  ...

Top files:
  - src/core/orchestrator.py [core] score=12.5
  - src/core/spectral_core.py [spectral] score=11.8
  ...
```

### Étape 2 : Créer un patch JSON

**Fichier `mon_patch.json` :**

```json
{
  "meta": {
    "nom": "Correction du calcul spectral",
    "description": "Corrige le calcul de SA_SB pour configurations asymétriques",
    "version": "1.0"
  },
  "operations": [
    {
      "op": "remplacer_texte",
      "cible": "src/core/spectral_core.py",
      "ancien_texte": "def _compute_sa_sb():\n    return A, B",
      "nouveau_texte": "def _compute_sa_sb(config=None):\n    # Correction pour asymétrique\n    return A, B",
      "message": "Ajout du paramètre config"
    }
  ]
}
```

### Étape 3 : Tester le patch

**Simulation (sans modifier):**

```bash
python orchestrator_main.py --apply mon_patch.json --apply-dry-run
```

**Résultat :**

```
=== Variateur : rapport d'application ===
  contrat   : /path/to/mon_patch.json
  mode      : SIMULATION (dry-run)
  ok        : 1
  simulees  : 1
  echouees  : 0
  manifeste : None
    [simule] #1 remplacer_texte -> src/core/spectral_core.py
```

### Étape 4 : Appliquer le patch

**Application réelle (modifie les fichiers):**

```bash
python orchestrator_main.py --apply mon_patch.json
```

**Résultat :**

```
=== Variateur : rapport d'application ===
  contrat   : /path/to/mon_patch.json
  mode      : APPLICATION RELLE
  ok        : 1
  simulees  : 0
  echouees  : 0
  manifeste : /path/to/.gabriel_variateur/snapshots/20260902T150322Z_mon_patch/manifeste.json
    [ok] #1 remplacer_texte -> src/core/spectral_core.py
```

### Étape 5 : Tester Gabriel

```bash
python src/ui/cli.py
# Gabriel doit fonctionner sans erreur
```

---

## 📋 TYPES D'OPÉRATIONS

### **1. remplacer_texte**

Remplace du texte dans un fichier :

```json
{
  "op": "remplacer_texte",
  "cible": "src/core/spectral_core.py",
  "ancien_texte": "# ANCIEN CODE",
  "nouveau_texte": "# NOUVEAU CODE",
  "toutes": false,
  "message": "Description de la modification"
}
```

### **2. inserer_lignes**

Insère des lignes à une position :

```json
{
  "op": "inserer_lignes",
  "cible": "tests/test_spectral.py",
  "ligne_insertion": 42,
  "contenu": "    # Nouvelle vérification\n    assert result == expected",
  "message": "Ajout assertion spectrale"
}
```

### **3. supprimer_lignes**

Supprime lignes de N à M :

```json
{
  "op": "supprimer_lignes",
  "cible": "src/core/old_module.py",
  "ligne_debut": 10,
  "ligne_fin": 20,
  "message": "Suppression du code obsolète"
}
```

### **4. ajouter_a_la_fin**

Ajoute du contenu à la fin du fichier :

```json
{
  "op": "ajouter_a_la_fin",
  "cible": "src/core/spectral_core.py",
  "contenu": "\n\ndef new_function():\n    pass",
  "message": "Ajout d'une nouvelle fonction"
}
```

### **5. creer_fichier**

Crée un nouveau fichier :

```json
{
  "op": "creer_fichier",
  "cible": "src/utils/new_util.py",
  "contenu": "#!/usr/bin/env python3\n# Nouveau module\n\ndef new_function():\n    pass",
  "message": "Création d'un nouveau module utilitaire"
}
```

### **6. deployer_fichier**

Copie un fichier source vers une cible :

```json
{
  "op": "deployer_fichier",
  "source": "../corrections/src/core/spectral_core.py",
  "cible": "src/core/spectral_core.py",
  "message": "Déploiement du fichier corrigé"
}
```

### **7. executer_python**

Exécute un script Python :

```json
{
  "op": "executer_python",
  "contenu": "import sys\nprint('Patch executed')\nsys.exit(0)",
  "message": "Exécution d'une tâche personnalisée"
}
```

### **8. propager_texte ⭐ (LE PLUS PUISSANT)**

**Applique une modification à TOUS les fichiers du réseau** :

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral", "reconstruction"],
  "role": "core",
  "profondeur": 2,
  "operation": {
    "op": "remplacer_texte",
    "ancien_texte": "old_formula",
    "nouveau_texte": "new_formula"
  },
  "message": "Correction du calcul spectral dans TOUS les fichiers impliqués"
}
```

**Processus de propager_texte :**

1. Appelle `ArchivisteCorrection.reseau_de_correction(["spectral", "reconstruction"], role="core", profondeur=2)`
2. Reçoit : `src/core/spectral_core.py`, `src/core/reconstruct.py`, `src/multiloop/debat.py`, etc. (7 fichiers)
3. Applique l'opération "remplacer_texte" à CHACUN des 7 fichiers
4. Retourne rapport avec tous les fichiers touchés

---

## 🔍 RÉSOLUTION DES CIBLES

### **Méthode 1 : Cible explicite (chemin complet)**

```json
{"op": "...", "cible": "src/core/spectral_core.py"}
```

VariateurMecanique cherche le fichier par chemin. **Doit exister.**

### **Méthode 2 : Mots-clés + rôle**

```json
{
  "op": "...",
  "mots_cles": ["spectral", "reconstruction"],
  "role": "core"
}
```

VariateurMecanique :
1. Charge la DB (`files` table)
2. Cherche les fichiers où keywords contiennent "spectral" ET "reconstruction"
3. Filtre par rôle="core"
4. Retourne le fichier avec le score le plus élevé

**Avantage** : Pas besoin de connaître le chemin exact !

### **Méthode 3 : Archiviste + réseau (propager_texte uniquement)**

```json
{
  "op": "propager_texte",
  "mots_cles": ["spectral"],
  "profondeur": 2
}
```

ArchivisteCorrection :
1. Cherche les fichiers par mots-clés
2. Propage via les relations d'import jusqu'à profondeur 2
3. Retourne TOUS les fichiers affectés (~7 fichiers)
4. Applique la modification à CHACUN

---

## 💾 SNAPSHOTS ET ROLLBACK

### **Lister les snapshots**

```bash
python orchestrator_main.py --list-snapshots
```

**Résultat :**

```
=== Snapshots du variateur ===
  - 20260902T150322Z_mon_patch  (/path/to/.gabriel_variateur/snapshots/20260902T150322Z_mon_patch)
  - 20260902T140115Z_autre_patch  (...)
  - 20260902T130000Z_initial  (...)
```

### **Restaurer un snapshot**

```bash
python orchestrator_main.py --rollback /path/to/.gabriel_variateur/snapshots/20260902T150322Z_mon_patch
```

**Ou plus court :**

```bash
python orchestrator_main.py --rollback 20260902T150322Z_mon_patch
```

**Processus de rollback :**

1. Lit le manifeste du snapshot
2. Restaure chaque fichier sauvegardé
3. Supprime les fichiers créés par le patch
4. Vérifie les checksums

**Résultat :**

```
=== Rollback 20260902T150322Z_mon_patch ===
  restaures : 3
  supprimes : 1
  manquants : 0
  dry_run : False
```

---

## 🛠️ CAS D'USAGE COMPLETS

### **CAS 1 : Corriger un calcul dans tous les fichiers concernés**

```bash
# 1. Créer le patch avec propager_texte
cat > spectral_fix.json << 'EOF'
{
  "meta": {
    "nom": "Correction calcul spectral global",
    "description": "Corrige le calcul de SA_SB partout où il est utilisé",
    "version": "1.0"
  },
  "operations": [
    {
      "op": "propager_texte",
      "mots_cles": ["spectral"],
      "role": "core",
      "profondeur": 2,
      "operation": {
        "op": "remplacer_texte",
        "ancien_texte": "def _compute_sa_sb():",
        "nouveau_texte": "def _compute_sa_sb(config=None):  # CORRIGÉ"
      },
      "message": "Correction appliquée globalement"
    }
  ]
}
EOF

# 2. Tester
python orchestrator_main.py --apply spectral_fix.json --apply-dry-run

# 3. Appliquer
python orchestrator_main.py --apply spectral_fix.json

# 4. Vérifier
python src/ui/cli.py
```

### **CAS 2 : Ajouter un test partout où c'est pertinent**

```bash
cat > add_test.json << 'EOF'
{
  "meta": {"nom": "Ajout tests spectral", "version": "1.0"},
  "operations": [
    {
      "op": "propager_texte",
      "mots_cles": ["test", "spectral"],
      "profondeur": 1,
      "operation": {
        "op": "ajouter_a_la_fin",
        "contenu": "\n\ndef test_spectral_consistency():\n    \"\"\"Vérification nouvelle.\"\"\"\n    assert True"
      },
      "message": "Ajout test spectral"
    }
  ]
}
EOF

python orchestrator_main.py --apply add_test.json
```

### **CAS 3 : Rollback rapide après erreur**

```bash
# Oups, le patch a cassé quelque chose !

# 1. Voir les snapshots
python orchestrator_main.py --list-snapshots

# 2. Restaurer le dernier bon état
python orchestrator_main.py --rollback 20260902T150322Z_mon_patch

# 3. Tester Gabriel
python src/ui/cli.py

# ✅ Gabriel fonctionne à nouveau !
```

---

## ⚠️ CHECKLIST AVANT D'APPLIQUER UN PATCH

- [ ] Patch JSON valide (vérifier la syntaxe)
- [ ] La cible existe OU les mots-clés trouvent quelque chose
- [ ] Tester avec `--apply-dry-run`
- [ ] Lire le rapport dry-run
- [ ] Si satisfait, appliquer avec `--apply`
- [ ] Tester Gabriel : `python src/ui/cli.py`
- [ ] Si problème : rollback immédiat
- [ ] Committer les changements : `git add -A && git commit -m "..."`

---

## 🔍 DÉPANNAGE

### **Erreur : "Cible introuvable et introuvable dans la DB"**

**Solution** :
```bash
# 1. Régénérer la DB
python orchestrator_main.py

# 2. Vérifier le chemin exact
grep "mon_fichier" ../data/gabriel_repo_map.db  # (SQLite CLI)
```

### **Erreur : "Aucun fichier résolu pour mots_cles"**

**Solution** :
- Les mots-clés ne correspondent à aucun fichier
- Regénérer la DB
- Chercher des keywords différents

### **Erreur : "verification syntaxe ... SyntaxError"**

**Solution** :
- Le fichier n'est pas valide Python après modification
- Vérifier l'ancien/nouveau texte du patch
- Tester la modification manuellement

### **Gabriel ne démarre pas après patch**

**Solution d'urgence** :
```bash
# 1. Lister les snapshots
python orchestrator_main.py --list-snapshots

# 2. Rollback au dernier bon
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# 3. Tester Gabriel
python src/ui/cli.py

# ✅ Récupéré !
```

---

## 📊 FICHIERS GÉNÉRÉS PAR LE PIPELINE

```
.gabriel_variateur/
├── snapshots/
│   ├── 20260902T150322Z_mon_patch/
│   │   ├── manifeste.json           ← Métadonnées + liste fichiers
│   │   ├── fichiers/
│   │   │   ├── a1b2c3d4e_spectral_core.py.bak
│   │   │   ├── x9y8z7w6v_reconstruct.py.bak
│   │   │   └── ...
│   │   └── exec/
│   │       └── op_7.py              ← Script exécuté si op=executer_python
│   └── 20260902T140115Z_autre_patch/
│       └── ...
└── logs/
    └── ...
```

**Manifeste (manifeste.json)** :

```json
{
  "version": "1.0",
  "horodatage": "2026-09-02T15:03:22Z",
  "contrat": "/path/to/mon_patch.json",
  "repo_root": "/path/to/agent-multiloop-Gabriel-local",
  "dossier_sauvegarde": "/path/to/.gabriel_variateur/snapshots/20260902T150322Z_mon_patch",
  "fichiers": [
    {
      "rel": "src/core/spectral_core.py",
      "existed_before": true,
      "backup_relatif": "fichiers/a1b2c3d4e_spectral_core.py.bak"
    }
  ]
}
```

---

## 📞 RÉCAPITULATIF DES COMMANDES

```bash
# SCANNER (créer la DB)
python orchestrator_main.py

# APPLIQUER UN PATCH
python orchestrator_main.py --apply mon_patch.json

# TESTER SANS MODIFIER
python orchestrator_main.py --apply mon_patch.json --apply-dry-run

# STRICT (échoue à la première erreur)
python orchestrator_main.py --apply mon_patch.json --apply-strict

# LISTER LES SNAPSHOTS
python orchestrator_main.py --list-snapshots

# RESTAURER UN SNAPSHOT
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# AIDE
python orchestrator_main.py --help
```

---

**Pipeline de Correction v1.0**  
Cœur : orchestrator_main.py  
Transmission : archiviste.py  
Base : data/gabriel_repo_map.db

© 2026 Gabriel Pipeline Team
