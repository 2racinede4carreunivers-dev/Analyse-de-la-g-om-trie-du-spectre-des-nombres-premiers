# GUIDE UTILISATEUR — TRANSMISSION / VARIATEUR MÉCANIQUE DE CORRECTION

> **But** : corriger, modifier ou mettre à jour le code de programmation de
> l'agent **Gabriel MULTILOOP** en **un seul clic** via le pipeline de
> correction autonome à variateur mécanique, sur l'ensemble du dépôt local.

---

## 1. Vue d'ensemble du pipeline (la transmission)

```
  [1] ANALYSEUR         gabriel_repo_mapper.py / orchestrator_main.py --rebuild
       → scanne TOUT le dépôt → base gabriel_repo_map.db (réseau neuronal :
         fichiers, fonctions, dossiers, adresses, imports, rôles, scores)

  [2] ARCHIVISTE        archiviste.py
       → la « transmission » (boîte d'engrenage) : à partir des mots-clés d'un
         patch, retrouve dans la base les ADRESSES des fichiers concernés et
         PROPAGE le long du réseau (imports + rôles) pour couvrir tous les
         fichiers impliqués.

  [3] ORCHESTRATEUR     orchestrator_main.py --apply <contrat>
       → le chef d'orchestre : écrit la correction dans chaque fichier résolu,
         SAUVEGARDE l'état d'origine (.gabriel_variateur/snapshots/), vérifie
         la syntaxe (py_compile / json), écrit le manifeste restaurable.

  [4] UN CLIC           transmission_un_clic.py --patch <fichier_patch.py>
       → point d'entrée unique : charge le PATCH (décrit en Python), appelle
         l'archiviste, construit le contrat, lance l'orchestrateur.
```

Le tout forme un **variateur mécanique** : le patch est la « vitesse » saisie,
l'archiviste est la **transmission** qui sélectionne les bons engrenages
(fichiers), et l'orchestrateur est l'**arbre de sortie** qui applique la
rotation (la correction) à toute la mécanique du dépôt.

---

## 2. Fichiers du pipeline

| Fichier | Rôle |
|---|---|
| `orchestrator_main.py` | Analyseur + variateur d'application (`--apply`, `--rollback`) |
| `archiviste.py` | Transmission : recherche + propagation réseau (base SQLite) |
| `transmission_un_clic.py` | Lanceur un-clic (`--patch fichier.py`) |
| `VARIATEUR_UN_CLIC.ps1` | Script PowerShell qui enchaîne analyseur + transmission |
| `exemple_patch_correction.py` | Exemple de patch au format PATCH |
| `patch_rapports_non_typiques.py` | **Patch des rapports non-typiques 1/k<>1/2** |
| `src/spectral/rapports_non_typiques.py` | Module exclusif de la méthode 1/k<>1/2 |
| `.gabriel_variateur/snapshots/` | Snapshots (sauvegardes) pour `--rollback` |
| `data/gabriel_repo_map.db` | Base du réseau neuronal (créée par l'analyseur) |

---

## 3. FORMAT D'UN PATCH

Deux formats acceptés par `transmission_un_clic.py` :

### Format 1 — propagation réseau (une opération appliquée à tous les fichiers trouvés)

```python
PATCH = {
    "meta": {"nom": "...", "description": "...", "version": "1.0"},
    "mots_cles": ["spectral"],          # l'archiviste cherche ces mots
    "role": "core",                      # filtre par rôle (optionnel)
    "profondeur": 1,                     # profondeur de propagation réseau
    "operation": {
        "op": "ajouter_a_la_fin",
        "contenu": "\n# Mon ajout",
    },
}
```

### Format 2 — liste d'opérations (contrat direct multi-fichiers)

```python
PATCH = {
    "meta": {...},
    "operations": [
        {"op": "creer_fichier", "cible": "src/xxx.py", "contenu": "..."},
        {"op": "remplacer_texte", "cible": "src/yyy.py",
         "ancien_texte": "...", "nouveau_texte": "...", "toutes": False},
        {"op": "propager_texte", "mots_cles": [...], "operation": {...}},
    ],
}
```

### Opérations disponibles

| op | Champs clés | Effet |
|---|---|---|
| `remplacer_texte` | `ancien_texte`, `nouveau_texte`, `toutes` | Remplace le texte (1re ou toutes les occurrences) |
| `inserer_lignes` | `ligne_insertion`, `contenu` | Insère des lignes à une position |
| `supprimer_lignes` | `ligne_debut`, `ligne_fin` | Supprime un intervalle de lignes |
| `ajouter_a_la_fin` | `contenu` | Ajoute du texte en fin de fichier |
| `creer_fichier` | `cible`, `contenu` | Crée un fichier |
| `deployer_fichier` | `source` | Déploie un fichier depuis un dossier `corrections/` |
| `executer_python` | `contenu` | Exécute un script Python de correction |
| `propager_texte` | `mots_cles`, `role`, `profondeur`, `operation` | Applique une opération à **tous** les fichiers du réseau résolu par l'archiviste |

---

## 4. Procédure exacte — Terminal PowerShell

### Étape 0 — Ouvrir PowerShell dans le dépôt

```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
```

### Étape 1 — (Re)construire la base du réseau neuronal (analyseur)

```powershell
python orchestrator_main.py --rebuild
```

> Génère / rafraîchit `data/gabriel_repo_map.db` (fichiers + liens) et
> `data/gabriel_repo_summary.json`.

### Étape 2 — Interroger l'archiviste (facultatif — aperçu du réseau)

```powershell
python archiviste.py --mots spectral --role core
python archiviste.py --mots "1/3" --json
```

### Étape 3 — Appliquer un patch (SIMULATION d'abord, toujours !)

```powershell
python transmission_un_clic.py --patch patch_rapports_non_typiques.py --dry-run
```

> Mode sec : aucune modification, rapport complet des opérations.

### Étape 4 — Appliquer le patch (EXÉCUTION RÉELLE)

```powershell
python transmission_un_clic.py --patch patch_rapports_non_typiques.py
```

> - Chaque fichier touché est sauvegardé dans
>   `.gabriel_variateur/snapshots/<horodatage>_<contrat>/`.
> - Un `manifeste.json` permet la restauration exacte.
> - La syntaxe de chaque fichier modifié est vérifiée.

### Étape 5 — Vérifier

```powershell
python -m py_compile src/core/spectral_core.py src/spectral/rapports_non_typiques.py
python -c "from src.core.spectral_core import SpectralMethodCore; c=SpectralMethodCore(); print(c.reconstruire_rapport_non_typique('1/3', n=10))"
```

### Annuler (ROLLBACK) si besoin

```powershell
python orchestrator_main.py --list-snapshots
python orchestrator_main.py --rollback <dossier_snapshot>
```

---
Le pipeline de correction n’est pas limité au patch des rapports non‑typiques.
Il est conçu comme un variateur mécanique général, capable d’appliquer des corrections, des mises à jour, des ajouts ou des suppressions sur l’ensemble du dépôt Gabriel MULTILOOP, incluant :

les modules Python (src/core, src/multiloop, src/spectral, etc.)

les scripts HOL Isabelle (theories/*.thy)

les fichiers de configuration (.json, .yaml)

les guides (.md)

les fichiers utilitaires

les nouveaux modules à créer

Les 8 opérations du pipeline sont entièrement génériques :

remplacer_texte

inserer_lignes

supprimer_lignes

ajouter_a_la_fin

creer_fichier

deployer_fichier

executer_python

propager_texte

Elles permettent de :

corriger un bug dans un module Python

ajouter une nouvelle fonction dans un fichier spectral

modifier un script HOL Isabelle

créer un nouveau module complet

propager une correction dans plusieurs fichiers liés

exécuter un script de migration ou de reconstruction

déployer un fichier préparé dans corrections/

mettre à jour la logique interne de Gabriel MULTILOOP

corriger ou étendre les validations Isabelle/HOL

appliquer des mises à jour générales du dépôt

Exemple de patch général (HOL)
python
PATCH = {
    "meta": {"nom": "maj_hol", "description": "Mise à jour d'un script HOL"},
    "operations": [
        {
            "op": "remplacer_texte",
            "cible": "theories/methode_spectral.thy",
            "ancien_texte": "lemma old_version",
            "nouveau_texte": "lemma new_version",
            "toutes": False
        }
    ]
}
Exemple de patch général (Python)
python
PATCH = {
    "meta": {"nom": "maj_core", "description": "Ajout d'une méthode dans SpectralMethodCore"},
    "operations": [
        {
            "op": "ajouter_a_la_fin",
            "cible": "src/core/spectral_core.py",
            "contenu": "\n    def nouvelle_methode(self):\n        return 'OK'"
        }
    ]
}
Conclusion
Le patch des rapports non‑typiques n’est qu’un exemple.
Le pipeline est un système général, conçu pour toutes les mises à jour du dépôt Gabriel MULTILOOP, y compris les validations Isabelle/HOL.
## 7. Bonnes pratiques

- **Toujours tester en `--dry-run`** avant l'application réelle.
- Un patch doit être **idempotent** : ne pas s'appliquer deux fois de suite
  sans contrôle (les `remplacer_texte` doivent cibler un texte qui
  n'existe plus après application).
- Conserver les **snapshots** tant que la correction n'est pas validée.
- Après application, lancer les tests du dépôt :
  `python -m pytest tests/ -x -q` (si pytest disponible).
- L'archiviste sert d'**aperçu** : utilisez-le pour connaître les fichiers
  qui seront touchés avant de lancer le patch.

---

## 8. Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| `Cible inexistante` | Fichier absent de la base | Refaire `python orchestrator_main.py --rebuild` |
| `ancien texte introuvable` | Patch déjà appliqué (non idempotent) | Restaurer via snapshot ou adapter `ancien_texte` |
| Table `fichiers` illisible | Base trop ancienne | Reconstruire la base (`--rebuild`) |
| SyntaxError import `src.spectral` | `non_typical_ratios.py` non corrigé | Le patch op. 6 corrige l'encodage UTF-8 |
| Rollback « manquants » | Anciens snapshots au chemin doublé | Utiliser la version corrigée d'`orchestrator_main.py` |

---

*Pipeline de correction autonome — Transmission / Variateur mécanique de
programmation de l'agent Gabriel MULTILOOP.*