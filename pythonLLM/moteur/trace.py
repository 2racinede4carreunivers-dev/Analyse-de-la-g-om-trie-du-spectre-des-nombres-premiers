# -*- coding: utf-8 -*-
"""
moteur/trace.py — trace de derivation chainee par SHA-256.

Chaque etape du pipeline produit un TraceEtape dont l'empreinte est
``SHA-256(empreinte_precedente + donnee)``. La chaine est inalterable :
modifier une etape invalide toutes les empreintes suivantes. L'empreinte
initiale est une constante de genese (64 zeros), comme un bloc genesis.
"""
from __future__ import annotations

import hashlib

from ..modele.entites import TraceEtape

GENESE = "0" * 64


class Tracer:
    """Accumule les etapes et maintient l'empreinte courante."""

    def __init__(self) -> None:
        self._empreinte_courante = GENESE
        self._etapes: list[TraceEtape] = []

    def ajouter(self, nom: str, donnee: str) -> TraceEtape:
        """Ajoute une etape et retourne le TraceEtape cree."""
        ordre = len(self._etapes)
        materiaux = (self._empreinte_courante + donnee).encode("utf-8")
        empreinte = hashlib.sha256(materiaux).hexdigest()
        etape = TraceEtape(
            ordre=ordre,
            nom=nom,
            donnee=donnee,
            empreinte_precedente=self._empreinte_courante,
            empreinte=empreinte,
        )
        self._etapes.append(etape)
        self._empreinte_courante = empreinte
        return etape

    @property
    def empreinte_finale(self) -> str:
        return self._empreinte_courante

    def etapes(self) -> tuple[TraceEtape, ...]:
        return tuple(self._etapes)
