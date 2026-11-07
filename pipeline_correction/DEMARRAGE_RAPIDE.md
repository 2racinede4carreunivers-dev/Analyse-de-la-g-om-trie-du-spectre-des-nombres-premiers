# ⚡ DÉMARRAGE EN 10 MINUTES

**Vous voulez corriger Gabriel avec le pipeline ? Suivez ceci.**

---

## 📋 ÉTAPE 0 : Où suis-je ?

```
agent-multiloop-Gabriel-local/
└── pipeline_correction/  ← Vous êtes ici
```

---

## 🚀 ÉTAPE 1 : Générer la cartographie (2 minutes)

C'est à faire UNE SEULE FOIS ou quand Gabriel change beaucoup.

```bash
cd pipeline_correction
python orchestrator_main.py
```

**Attendez ~15 secondes...**

```
=== Gabriel repository orchestrator ===
repo root : ...
total files : 234
total edges : 450

Top roles:
  - core: 45
  - test: 38
  ...

DB SQLite created: data/gabriel_repo_map.db
Summary JSON created: data/gabriel_repo_summary.json

Next step: python orchestrator_main.py --apply <contrat.json>
```

✅ **La DB est créée !**

---

## 🎯 ÉTAPE 2 : Créer votre patch (3 minutes)

Créez un fichier `mon_patch.json` avec vos modifications.

**Exemple simple** (remplacer du texte) :

```json
{
  "meta": {
    "nom": "Correction du calcul",
    "description": "Corrige le bug dans spectral_core.py",
    "version": "1.0"
  },
  "operations": [
    {
      "op": "remplacer_texte",
      "cible": "src/core/spectral_core.py",
      "ancien_texte": "def old_function():\n    return A, B",
      "nouveau_texte": "def new_function():\n    return A, B  # FIXED",
      "message": "Correction appliquée"
    }
  ]
}
```

**Exemple avancé** (propager dans TOUS les fichiers du réseau) :

```json
{
  "meta": {
    "nom": "Correction globale spectral",
    "version": "1.0"
  },
  "operations": [
    {
      "op": "propager_texte",
      "mots_cles": ["spectral", "reconstruction"],
      "role": "core",
      "profondeur": 2,
      "operation": {
        "op": "remplacer_texte",
        "ancien_texte": "bug_code",
        "nouveau_texte": "fixed_code"
      },
      "message": "Bug corrigé partout"
    }
  ]
}
```

---

## 🧪 ÉTAPE 3 : Tester (2 minutes)

**SANS MODIFIER RIEN** (simulation) :

```bash
python orchestrator_main.py --apply mon_patch.json --apply-dry-run
```

**Résultat :**

```
=== Variateur : rapport d'application ===
  mode      : SIMULATION (dry-run)
  ok        : 1
  simulees  : 1
  echouees  : 0
    [simule] #1 remplacer_texte -> src/core/spectral_core.py
```

✅ **Ça va marcher !**

Si `[echouee]` apparaît, lisez l'erreur et corrigez le patch.

---

## ✅ ÉTAPE 4 : Appliquer pour de vrai (1 minute)

**ATTENTION : À partir d'ici, ça modifie réellement les fichiers.**

```bash
python orchestrator_main.py --apply mon_patch.json
```

**Résultat :**

```
=== Variateur : rapport d'application ===
  mode      : APPLICATION RELLE
  ok        : 1
  simulees  : 0
  echouees  : 0
  manifeste : /path/to/.gabriel_variateur/snapshots/20260902T150322Z_mon_patch/manifeste.json
    [ok] #1 remplacer_texte -> src/core/spectral_core.py
```

✅ **Appliqué !**

Un snapshot a été créé (pour rollback si besoin).

---

## 🔍 ÉTAPE 5 : Tester Gabriel (1 minute)

```bash
cd ..
python src/ui/cli.py
```

**Gabriel doit fonctionner !**

Si quelque chose ne va pas, allez à l'étape ROLLBACK (ci-dessous).

---

## ❌ ÉTAPE 6 : Rollback (si problème) (1 minute)

Gabriel ne fonctionne pas ? Restaurez l'état d'avant !

```bash
cd pipeline_correction

# Voir les sauvegardes
python orchestrator_main.py --list-snapshots

# Restaurer le dernier bon état
python orchestrator_main.py --rollback 20260902T150322Z_mon_patch
```

**Vérifiez :**

```bash
cd ..
python src/ui/cli.py
```

✅ **Gabriel fonctionne à nouveau !**

---

## 📊 RÉSUMÉ DES COMMANDES

```bash
# Dans le dossier pipeline_correction:

# Générer la DB (une fois)
python orchestrator_main.py

# Tester le patch (avec --apply-dry-run)
python orchestrator_main.py --apply mon_patch.json --apply-dry-run

# Appliquer (pour de vrai)
python orchestrator_main.py --apply mon_patch.json

# Voir les snapshots
python orchestrator_main.py --list-snapshots

# Rollback d'urgence
python orchestrator_main.py --rollback <SNAPSHOT_ID>
```

---

## 🎓 TYPES D'OPÉRATIONS (8 types)

| Type | Exemple | Use case |
|------|---------|----------|
| **remplacer_texte** | Remplacer du code | Corriger un bug |
| **inserer_lignes** | Ajouter à la ligne 42 | Ajouter une assertion |
| **supprimer_lignes** | Supprimer lignes 10-20 | Nettoyer du code |
| **ajouter_a_la_fin** | Append au fichier | Ajouter une fonction |
| **creer_fichier** | Créer nouveau fichier | Ajouter un module |
| **deployer_fichier** | Copier depuis source | Déployer correction |
| **executer_python** | Exécuter script | Task custom |
| **propager_texte** ⭐ | Appliquer à TOUS | Corriger partout |

Le type **propager_texte** est le plus puissant : il applique la modification à TOUS les fichiers du réseau.

---

## 🏆 WORKFLOW COMPLET (10 min)

```
1. Générer la DB
   python orchestrator_main.py
   ⏱️ 15 secondes

2. Créer mon_patch.json
   ⏱️ 3 minutes

3. Tester
   python orchestrator_main.py --apply mon_patch.json --apply-dry-run
   ⏱️ 1 minute
   Vérifier : [simule] ou [echouee] ?

4. Appliquer
   python orchestrator_main.py --apply mon_patch.json
   ⏱️ 1 minute
   Vérifier : [ok] ?

5. Tester Gabriel
   python ../src/ui/cli.py
   ⏱️ 1 minute
   Fonctionne ?

6. Si problème : Rollback
   python orchestrator_main.py --rollback <SNAPSHOT>
   ⏱️ 1 minute
   Gabriel OK ?

Total : ~10-15 minutes
```

---

## ⚠️ PIÈGES À ÉVITER

❌ **NE PAS** appliquer sans tester avec `--apply-dry-run` d'abord

❌ **NE PAS** supprimer le dossier `.gabriel_variateur` (ça contient les snapshots)

❌ **NE PAS** modifier la DB `data/gabriel_repo_map.db` à la main

❌ **NE PAS** appliquer plusieurs patchs à la fois (risque de conflit)

---

## ✅ BONNES PRATIQUES

✅ **TOUJOURS** tester avec `--apply-dry-run` d'abord

✅ **TOUJOURS** committer les changements après succès

✅ **TOUJOURS** garder les snapshots (rollback possible)

✅ **TOUJOURS** vérifier Gabriel fonctionne après patch

✅ **Utiliser propager_texte** pour corriger partout

---

## 🚨 AIDE D'URGENCE

**Quelque chose ne va pas ?**

```bash
# 1. Restaurer immédiatement
python orchestrator_main.py --list-snapshots
python orchestrator_main.py --rollback <SNAPSHOT_ID>

# 2. Vérifier Gabriel
python ../src/ui/cli.py

# 3. Consulter le guide complet
cat GUIDE_UTILISATEUR.md
```

---

## 📚 POUR EN SAVOIR PLUS

- **Guide complet** : `GUIDE_UTILISATEUR.md`
- **Fonctionnement interne** : `ANALYSE_APPROFONDIE.md`
- **Référence technique** : `README_PIPELINE.md`
- **Index principal** : `INDEX.md`

---

**🎉 Vous êtes prêt ! Suivez les 6 étapes ci-dessus et c'est bon.**

© 2026 Gabriel Pipeline Team
