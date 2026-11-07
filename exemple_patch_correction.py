#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLE DE PATCH — Correction de programmation de l'agent (format variateur)

Ce fichier décrit UNE correction, mise à jour ou modification à apporter au
code de programmation de l'agent Gabriel MULTILOOP, de façon AUTONOME.

La variable PATCH (dict) contient :
  - meta           : nom + description de la correction
  - mots_cles      : les mots-clés que l'archiviste (transmission) utilisera
                     pour retrouver les adresses des fichiers impliqués
                     dans le réseau (base gabriel_repo_map.db).
  - role           : (facultatif) filtre par rôle fonctionnel.
  - profondeur     : profondeur de propagation du réseau (combien d'arêtes).
  - operation      : l'opération d'édition à appliquer à CHAQUE fichier du réseau.
       * op = "remplacer_texte"   (ancien_texte → nouveau_texte)
       * op = "inserer_lignes"    (ligne_insertion + contenu)
       * op = "supprimer_lignes"  (ligne_debut + ligne_fin)
       * op = "ajouter_a_la_fin"  (contenu)
       * op = "creer_fichier"     (nom_fichier + contenu)

Exécution un clic :
  python transmission_un_clic.py --patch exemple_patch_correction.py
  python transmission_un_clic.py --patch exemple_patch_correction.py --dry-run
"""

PATCH = {
    "meta": {
        "nom": "exemple_ajout_constante_spectrale",
        "description": "Ajoute un en-tête de version spectral aux fichiers du réseau spectral.",
    },
    # ── Critères de recherche dans la base (réseau neuronal) ──────────────
    "mots_cles": ["spectral"],
    "role": "core",
    "profondeur": 1,
    # ── Opération appliquée à tous les fichiers trouvés ───────────────────
    "operation": {
        "op": "ajouter_a_la_fin",
        "contenu": "\n# [VARIATEUR] Constante spectrale globale\nSPECTRAL_VERSION = \"1.0\"",
    },
}

if __name__ == "__main__":
    import json
    print(json.dumps(PATCH, indent=2, ensure_ascii=False))