# pipeline_correction_dev — Double developpeur du pipeline de correction

Ce dossier est un **double** du pipeline de correction, reserve a l'usage du
developpeur (Philippe Thomas Savard) pour appliquer des corrections de masse
au code de programmation de l'Agent, par le developpeur et pour le developpeur.

## Difference avec `pipeline_correction/` (version principale)

| | `pipeline_correction/` (main) | `pipeline_correction_dev/` (cette branche) |
|---|---|---|
| Role | Version integrant la fusion Cline/Gabriel (moteur recursif, garde-fou, etc.) | Version developpeur pure, utilisee manuellement par le developpeur |
| Fichiers | complete (patchs etendus, orchestrator_main, archiviste, config, __main__) | les 13 fichiers de base : gabriel_01/02/03, variateur_mecanique, patchs de base |
| __init__.py | contenu complet | version locale du developpeur |

## Contenu (13 fichiers developpeur)

- `gabriel_01_pipeline_trace.py` — reconstruction du pipeline soumission -> reponse
- `gabriel_02_engine_audit.py` — audit du moteur et des defaillances
- `gabriel_03_corrector.py` — generation des fichiers corriges prets a deployer
- `variateur_mecanique.py` — application des patchs JSON (variateur de correction)
- `defaillances.json`, `patch_*.json`, `rapport_*.txt/json` — donnees et patchs

## Note importante

Le **moteur recursif** et la **fusion avec le code de Cline** ne sont PAS
modifies ici. Cette branche sert uniquement a conserver et utiliser la version
developpeur du pipeline de correction, en parallele de la version principale.

> Branche : `pipeline-correction-dev`
> Creee le : 2026-10-11
