# pipeline_correction_HOL

Boite a outils de sante et de correction pour les sessions **Isabelle / HOL**
de validation mathematique. Reutilisable sur tout projet Isabelle, sans
dependance specifique a la session `Geometrie_Spectre_Premier_Philippe_Thomas_Savard`.

Auteur : Philippe Thomas Savard - Licence Apache 2.0.

## Contenu

| Fichier | Role |
|---|---|
| `Healthcheck_HOL_correction.py` | Analyseur + correcteur (7 passes P0-P6) |
| `healthcheck_rapport.json` | Dernier rapport produit sur la session geometrie du spectre |
| `DEVIS_NETTOYAGE_HOL.md` | Devis d'allegement de la validation principale et des contre-validations |

## Utilisation

Toujours lancer depuis la racine du depot (`C:\agent-multiloop-Gabriel-local`).

```sh
# 1. Analyse rapide (0,4 s) -- ne lance pas Isabelle
python pipeline_correction_HOL\Healthcheck_HOL_correction.py ^
    --theories-dir agent-multiloop-Gabriel-local/theories --offline

# 2. Analyse complete : interroge Isabelle/Cygwin (version, ML_OPTIONS, ML_PLATFORM)
python pipeline_correction_HOL\Healthcheck_HOL_correction.py ^
    --theories-dir <TON_REPERTOIRE>\theories ^
    --isabelle-home "C:\Users\isabelle\Isabelle2025-2" ^
    --patch-out rapport.json

# 3. Generer ET appliquer le patch de correction
python pipeline_correction_HOL\Healthcheck_HOL_correction.py ^
    --theories-dir <TON_REPERTOIRE>\theories --fix
```

### Options

| Option | Effet |
|---|---|
| `--theories-dir DIR` | **obligatoire** - dossier contenant `ROOT` et les `.thy` |
| `--fix` | applique les corrections automatiques (BOM, CR isoles, nom de theorie, Unicode) |
| `--offline` | saute l'introspection Isabelle/Cygwin : analyse `.thy` seule, ~0,4 s |
| `--patch-out F` | ecrit le rapport + le patch de correction en JSON |
| `--json` | imprime le rapport complet sur stdout |
| `--strict` | retourne un code non nul siwarning** en plus des erreurs |
| `-q` / `--quiet` | une seule ligne de resume |

Code de sortie : `0` = aucune erreur, `1` = erreurs detectees, `2` = mauvais `--theories-dir`.

## Les 7 passes

| Passe | Controle | Regle source |
|---|---|---|
| **P0-env** | `Cygwin-Terminal.bat` (HOME/PATH/LANG/CHERE/bash), `isabelle version`, `isabelle build -h`, `isabelle getenv ML_OPTIONS ML_PLATFORM` | contenu reel du lanceur + `isabelle build -h` |
| **P1-session** | `session NOM = HOL +`, theories declarees mais absentes (= echec build), theories presentes non declarees (= ignorees), doublons | syntaxe outer Isar |
| **P2-header** | `theory NOM` aligne sur le nom de fichier, imports resolus, cycles, ordre fragile | grammaire `theory`/`imports` |
| **P3-structure** | **analyse a pile** des blocs imbriques `begin/end`, `proof/qed`, `\<open>/\<close>` | grammaire Isar reelle |
| **P4-encoding** | UTF-8 strict, BOM, CR isoles, fins de ligne melangees | comportement du chargeur |
| **P5-unicode** | delegue a `verify_thy_structure.py` s'il est dans le dossier (sinon table Unicode integree) | verificateur du projet |
| **P6-memoire** | pese `by eval`, Pocklington, `mod_exp`, `prime >= 10^7`, `sorry` ; compare le cout cumule au plafond de `ML_PLATFORM` | `contrib/polyml-5.9.2-2/src/libpolyml/heapsizing.cpp` (`MAXIMUMADDRESS`) |

## Limites

* Analyse **statique** : garantit qu'Isabelle *parse* la session (donc pas de
  `Outer syntax error`). Seul `isabelle build` peut dire si les **preuves** passent.
* P6 est une **prevision de cout** basee sur des motifs, pas une mesure.
* Le decoupage d'une session en plusieurs fichiers `.thy` **ne reduit pas** le pic
  memoire : une session = un seul tas ML partage. Pour baisser le pic, il faut
  extraire les certificats lourds dans une session annexe ou les axiomatiser.