#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple de PATCH GÉNÉRIQUE — mise à jour d'un script HOL/Isabelle (.thy).

Ce patch illustre que le pipeline peut modifier TOUT fichier du dépôt, y
compris les scripts de preuve Isabella/HOL (le coeur de la validation de
Gabriel). Ici : on ajoute un commentaire de version dans methode_spectral.thy.
"""
from pathlib import Path

PATCH = {
    "meta": {
        "nom": "exemple_generique_hol",
        "description": "Ajoute un marqueur de version dans un script HOL/Isabelle (.thy) "
                       "— preuve que le pipeline couvre les validations HOL.",
        "version": "1.0",
    },
    "operations": [
        {
            "op": "remplacer_texte",
            "cible": "theories/methode_spectral.thy",
            "ancien_texte": "theory methode_spectral\n  imports Complex_Main",
            "nouveau_texte": "(* [VARIATEUR] mis-a-jour HOL : exemple generique *)\ntheory methode_spectral\n  imports Complex_Main",
            "toutes": False,
            "message": "Mise à jour générique d'un script HOL/Isabelle",
        },
    ],
}