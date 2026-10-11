r"""Axe 3 - Ontologie des regimes spectraux.

Definit la hierarchie ontologique des regimes :
  Univers Spectral
    \_ Modeles (1/2, 1/3, 1/4)
        \_ Regimes (positif, negatif, mixte, asymetrique, ...)
            \_ Sous-cas particuliers

Et les relations entre regimes (specialisation, extension, generalisation).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RegimeRelation(str, Enum):
    """Types de relations entre regimes."""
    SPECIALISATION = "specialisation"  # B est un cas particulier de A
    EXTENSION = "extension"            # B etend A (e.g. 1/4 etend 1/2)
    GENERALISATION = "generalisation"  # B generalise A
    DUAL = "dual"                      # B est le dual de A (e.g. positif <-> negatif)
    COMPATIBLE = "compatible"          # B peut coexister avec A
    INCOMPATIBLE = "incompatible"      # B et A s'excluent mutuellement


@dataclass
class RegimeEntity:
    """Une entite ontologique : regime, modele ou univers."""
    nom: str
    niveau: str  # "univers" | "modele" | "regime" | "sous-cas"
    parent: Optional[str] = None
    description: str = ""


# Hierarchie ontologique officielle (conforme methode_spectral.thy)
ONTOLOGIE: dict[str, RegimeEntity] = {
    "univers_spectral": RegimeEntity(
        nom="univers_spectral", niveau="univers",
        description="Univers complet de la Methode Spectrale Savard",
    ),
    "modele_1_2": RegimeEntity(
        nom="modele_1_2", niveau="modele", parent="univers_spectral",
        description="Modele quadratique (base 2, factor 64)",
    ),
    "modele_1_3": RegimeEntity(
        nom="modele_1_3", niveau="modele", parent="univers_spectral",
        description="Modele cubique (base 3, factor 729)",
    ),
    "modele_1_4": RegimeEntity(
        nom="modele_1_4", niveau="modele", parent="univers_spectral",
        description="Modele quartique (base 4, factor 4096)",
    ),
    "regime_positif": RegimeEntity(
        nom="regime_positif", niveau="regime", parent="modele_1_2",
        description="Indices n positifs uniquement",
    ),
    "regime_negatif": RegimeEntity(
        nom="regime_negatif", niveau="regime", parent="modele_1_2",
        description="Indices n negatifs (powr)",
    ),
    "regime_mixte": RegimeEntity(
        nom="regime_mixte", niveau="regime", parent="modele_1_2",
        description="Indices traversant zero",
    ),
    "bloc_symetrique": RegimeEntity(
        nom="bloc_symetrique", niveau="sous-cas", parent="regime_positif",
        description="|A_pos| == |B_pos|, ratio exact",
    ),
    "bloc_chaotique": RegimeEntity(
        nom="bloc_chaotique", niveau="sous-cas", parent="regime_positif",
        description="|A_pos| != |B_pos|, ordre arbitraire, convergence",
    ),
    "bloc_ordonne": RegimeEntity(
        nom="bloc_ordonne", niveau="sous-cas", parent="regime_positif",
        description="|A_pos| != |B_pos|, ordre croissant, convergence",
    ),
}


# Relations explicites
RELATIONS: list[tuple[str, RegimeRelation, str]] = [
    ("modele_1_4", RegimeRelation.EXTENSION, "modele_1_2"),
    ("modele_1_3", RegimeRelation.EXTENSION, "modele_1_2"),
    ("regime_positif", RegimeRelation.DUAL, "regime_negatif"),
    ("regime_mixte", RegimeRelation.GENERALISATION, "regime_positif"),
    ("regime_mixte", RegimeRelation.GENERALISATION, "regime_negatif"),
    ("bloc_symetrique", RegimeRelation.SPECIALISATION, "regime_positif"),
    ("bloc_chaotique", RegimeRelation.SPECIALISATION, "regime_positif"),
    ("bloc_ordonne", RegimeRelation.SPECIALISATION, "regime_positif"),
    ("bloc_symetrique", RegimeRelation.INCOMPATIBLE, "bloc_chaotique"),
]


class RegimeOntology:
    """API d'interrogation de l'ontologie des regimes spectraux."""

    def __init__(self):
        self.entities = ONTOLOGIE
        self.relations = RELATIONS

    def get(self, nom: str) -> RegimeEntity:
        if nom not in self.entities:
            raise ValueError(f"Entite inconnue : '{nom}'")
        return self.entities[nom]

    def ancestors(self, nom: str) -> list[str]:
        """Liste des ancetres dans la hierarchie."""
        result: list[str] = []
        current = self.entities.get(nom)
        while current and current.parent:
            result.append(current.parent)
            current = self.entities.get(current.parent)
        return result

    def relations_of(self, nom: str) -> list[tuple[RegimeRelation, str]]:
        """Toutes les relations sortantes d'un noeud."""
        return [(rel, target) for (src, rel, target) in self.relations if src == nom]

    def is_compatible(self, a: str, b: str) -> bool:
        """Verifie si deux regimes sont compatibles (pas incompatibles explicitement)."""
        for (src, rel, target) in self.relations:
            if rel == RegimeRelation.INCOMPATIBLE and (
                (src == a and target == b) or (src == b and target == a)
            ):
                return False
        return True

    def list_by_level(self, niveau: str) -> list[str]:
        """Liste toutes les entites d'un niveau donne."""
        return [
            nom for nom, e in self.entities.items() if e.niveau == niveau
        ]
