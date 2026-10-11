# 👋 BIENVENUE DANS LE PIPELINE DE CORRECTION GABRIEL

## 🎯 Vous avez un pipeline puissant et complet

Vous tenez entre les mains un système professionnel de gestion du code de Gabriel.

---

## ⚡ EN 5 SECONDES

**Le Pipeline = Scanner + Applicateur + Transmission**

1. **Scanner** : Cartographie le dépôt (orchestrator_main.py)
2. **Applicateur** : Applique les patchs (orchestrator_main.py)
3. **Transmission** : Cherche les fichiers affectés (archiviste.py)

**Résultat** : Corrections sûres, vérifiées, restaurables

---

## 🚀 COMMENCER EN 10 MINUTES

```bash
# 1. Générer la DB (15 secondes)
cd pipeline_correction
python orchestrator_main.py

# 2. Lire le guide (5 minutes)
cat DEMARRAGE_RAPIDE.md

# 3. Créer votre premier patch (3 minutes)
echo '{"meta":{"nom":"Test"},"operations":[...]}' > mon_patch.json

# 4. Tester
python orchestrator_main.py --apply mon_patch.json --apply-dry-run

# 5. Appliquer
python orchestrator_main.py --apply mon_patch.json
```

✅ **Vous avez terminé !**

---

## 📚 DOCUMENTATION

| Document | Pour qui | Durée |
|----------|----------|-------|
| **DEMARRAGE_RAPIDE.md** | Tout le monde | 10 min |
| **GUIDE_UTILISATEUR.md** | Utilisateurs quotidiens | 30 min |
| **ANALYSE_APPROFONDIE.md** | Développeurs | 45 min |
| **RESUME_EXECUTIF.md** | Cadres | 5 min |
| **INDEX.md** | Navigation | - |

---

## 🎯 CAS TYPIQUE

**Vous trouvez un bug dans spectral_core.py**

```bash
# 1. Créer un patch (utiliser propager_texte pour toucher TOUS les fichiers)
cat > spectral_fix.json << 'EOF'
{
  "meta": {"nom": "Correction spectral", "version": "1.0"},
  "operations": [
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
  ]
}
EOF

# 2. Tester sans modifier
python orchestrator_main.py --apply spectral_fix.json --apply-dry-run

# 3. Appliquer (crée snapshot automatiquement)
python orchestrator_main.py --apply spectral_fix.json

# 4. Vérifier
python ../src/ui/cli.py

# 5. Si problème : rollback instantané
python orchestrator_main.py --list-snapshots
python orchestrator_main.py --rollback <SNAPSHOT>
```

✅ **Le bug est fixé partout !**

---

## ✨ CE QUE VOUS OBTENEZ

✅ **Automatisation** — Corrections appliquées automatiquement  
✅ **Sécurité** — Snapshots + rollback en cas de problème  
✅ **Traçabilité** — Rapport détaillé de chaque modification  
✅ **Propagation** — Corriger tous les fichiers affectés en 1 clic  
✅ **Vérification** — Syntaxe Python/JSON vérifiée automatiquement  

---

## 🔐 GARANTIES

✅ **Avant chaque modification** : Snapshot créé automatiquement  
✅ **Après chaque modification** : Syntaxe vérifiée  
✅ **En cas de problème** : Rollback instantané  
✅ **Trace complète** : Manifeste JSON de chaque opération  

---

## 📊 LES 3 COMPOSANTES

### 1. Scanner (RepoOrchestrator)
```python
orchestrator_main.py → scan_repo()
# Parcourt 234 fichiers
# Crée gabriel_repo_map.db
# Index : rôles, keywords, imports, scores
```

### 2. Applicateur (VariateurMecanique)
```python
orchestrator_main.py → executer_contrat(patch.json)
# Charge le patch
# Résout les cibles
# Crée snapshot
# Applique opérations
# Vérifie syntaxe
```

### 3. Transmission (ArchivisteCorrection)
```python
archiviste.py → reseau_de_correction(mots_cles, profondeur)
# Cherche par keywords
# Propage via imports
# Retourne TOUTES les adresses
```

---

## 8️⃣ TYPES D'OPÉRATIONS

| Type | Utilité |
|------|---------|
| **remplacer_texte** | Corriger du code |
| **inserer_lignes** | Ajouter à position N |
| **supprimer_lignes** | Supprimer lignes N-M |
| **ajouter_a_la_fin** | Append à la fin |
| **creer_fichier** | Créer nouveau fichier |
| **deployer_fichier** | Copier depuis source |
| **executer_python** | Lancer script |
| **propager_texte** ⭐ | Appliquer à TOUS les fichiers |

**propager_texte est la plus puissante** : elle applique à TOUS les fichiers du réseau

---

## 🎓 EXEMPLE COMPLET

**Scénario** : Corriger un bug + ajouter un test

```json
{
  "meta": {
    "nom": "Correction + test",
    "description": "Corrige le bug et ajoute un test partout",
    "version": "1.0"
  },
  "operations": [
    {
      "op": "propager_texte",
      "mots_cles": ["spectral"],
      "profondeur": 2,
      "operation": {
        "op": "remplacer_texte",
        "ancien_texte": "def old_function():",
        "nouveau_texte": "def new_function():  # FIXED"
      }
    },
    {
      "op": "propager_texte",
      "mots_cles": ["test", "spectral"],
      "operation": {
        "op": "ajouter_a_la_fin",
        "contenu": "\n\ndef test_new_fix():\n    assert True"
      }
    }
  ]
}
```

**Résultat** : 7 fichiers corrigés et testés en 1 clic

---

## ❌ PIÈGES À ÉVITER

❌ Appliquer sans `--apply-dry-run`  
❌ Supprimer `.gabriel_variateur`  
❌ Modifier la DB à la main  
❌ Appliquer plusieurs patchs ensemble

---

## ✅ BONNES PRATIQUES

✅ TOUJOURS tester avec `--apply-dry-run`  
✅ TOUJOURS vérifier Gabriel après  
✅ Utiliser `propagar_texte` pour corrections globales  
✅ Committer après succès  

---

## 🆘 AIDE RAPIDE

```bash
# Problème ?
python orchestrator_main.py --list-snapshots
python orchestrator_main.py --rollback <SNAPSHOT>

# Questions ?
cat INDEX.md

# Besoin du mode d'emploi ?
cat GUIDE_UTILISATEUR.md
```

---

## 🎯 PROCHAINES ÉTAPES

1. **Maintenant** : Lire `DEMARRAGE_RAPIDE.md` (5 min)
2. **Ensuite** : Générer la DB (`python orchestrator_main.py`)
3. **Puis** : Créer votre premier patch
4. **Enfin** : Tester et appliquer

---

## 📞 RESSOURCES

```
Rapide (5 min)      → DEMARRAGE_RAPIDE.md
Complet (30 min)    → GUIDE_UTILISATEUR.md
Technique (45 min)  → ANALYSE_APPROFONDIE.md
Référence (60 min)  → README_PIPELINE.md
Navigation          → INDEX.md
Résumé             → RESUME_EXECUTIF.md
```

---

## 🚀 LET'S GO !

**Allez à : `pipeline_correction/DEMARRAGE_RAPIDE.md`**

⏱️ 10 minutes et vous êtes 100% opérationnel

---

**Pipeline de Correction Gabriel v1.0**

Cœur : orchestrator_main.py  
Transmission : archiviste.py  
Base : gabriel_repo_map.db

© 2026 Gabriel Pipeline Team

**Bon travail ! 🎉**
