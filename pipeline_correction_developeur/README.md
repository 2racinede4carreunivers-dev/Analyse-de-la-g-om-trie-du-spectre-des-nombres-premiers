# pipeline_correction_developeur — Double developpeur (usage manuel du developpeur)

Ce dossier est un **double** du pipeline de correction, reserve a l'usage du
developpeur (Philippe Thomas Savard) pour appliquer lui-meme des corrections de
masse au code de programmation de l'Agent.

## Coexistence des deux pipelines sur `main`

| Dossier | Role | Fichiers |
|---|---|---|
| `pipeline_correction/` | Version integrant la fusion Cline/Gabriel (moteur recursif, garde-fou) — **INCHANGEE** | complete (~41) |
| `pipeline_correction_developeur/` (ce dossier) | Version developpeur pure, pour corriger l'Agent a la main | 13 fichiers de base |

Les deux dossiers portent des **noms distincts** : aucun conflit.

## Contenu (13 fichiers developpeur)

- `gabriel_01_pipeline_trace.py` — reconstruction du pipeline soumission -> reponse
- `gabriel_02_engine_audit.py` — audit du moteur et des defaillances
- `gabriel_03_corrector.py` — generation des fichiers corriges prets a deployer
- `variateur_mecanique.py` — application des patchs JSON (variateur de correction)
- `defaillances.json`, `patch_*.json`, `rapport_*.txt/json` — donnees et patchs

## Note

Le **moteur recursif** et la **fusion avec le code de Cline** (dans
`pipeline_correction/` et `src/`) ne sont **pas** modifies par ce dossier.

> Ajoute le : 2026-10-11
