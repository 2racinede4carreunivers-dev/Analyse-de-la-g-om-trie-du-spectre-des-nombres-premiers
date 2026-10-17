# -*- coding: utf-8 -*-
"""
moteur/normalisation.py — normalisation deterministe d'une requete.

Aucune approximation : la normalisation est une fonction pure. On applique
NFKC (forme de compatibilite Unicode), on retire les accents par table de
correspondance explicite (pas de translitteration floue), on minusculise, et
on decoupe en tokens alphanumeriques. Le resultat est un tuple reproductible.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Tuple

# Table de suppression d'accents explicite (decomposition NFD + retrait des
# marques combinantes). Deterministe, couvre l'ensemble du repertoire Unicode.
_TOKEN_RE = re.compile(r"[0-9a-z]+")


def normaliser(texte: str) -> Tuple[str, ...]:
    """Retourne le tuple de tokens normalises d'une chaine.

    - decomposition NFD puis suppression des marques combinantes (accents) ;
    - minuscule ;
    - decoupe sur ``[0-9a-z]+`` (les separateurs deviennent des frontieres).

    Exemple : ``"L'Arbre de Cayley !"`` -> ``('l', 'arbre', 'de', 'cayley')``.
    """
    if not texte:
        return ()
    # Decomposition canonique + suppression des diacritiques.
    decompose = unicodedata.normalize("NFD", texte)
    sans_accents = "".join(
        ch for ch in decompose if not unicodedata.combining(ch)
    )
    minuscule = sans_accents.lower()
    return tuple(_TOKEN_RE.findall(minuscule))


def rejoindre(tokens: Tuple[str, ...]) -> str:
    """Reforme une phrase simple depuis des tokens (utile aux traces)."""
    return " ".join(tokens)
