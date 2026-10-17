# -*- coding: utf-8 -*-
"""
moteur/banque.py — acces en lecture a la base SQLite du corpus.

La base est chargee une fois en memoire (tables transformees en ensembles et
dictionnaires) pour que la reconnaissance soit une simple appartenance
ensembliste, sans requete par terme. Si la base n'existe pas, elle est
construite automatiquement depuis le corpus encode.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, FrozenSet, Optional, Tuple

from ..modele.entites import ChampConnaissance, Institution, Notion, Invariant, RegleIntention

_CHEMIN_DEFAUT = (
    Path(__file__).resolve().parents[1] / "corpus" / "corpus_computationnel.db"
)


class Banque:
    """Vue en lecture du corpus, chargee en memoire.

    Attributs principaux :
    - ``lemmes`` : ensemble fige des termes reconnus (appartenance O(1)) ;
    - ``notions`` : dict lemme -> Notion ;
    - ``champs`` : dict code -> ChampConnaissance, ordonne par poids ;
    - ``regles`` : regles d'intention triees par priorite croissante.
    """

    def __init__(self, chemin: Optional[Path] = None) -> None:
        self.chemin = Path(chemin) if chemin else _CHEMIN_DEFAUT
        if not self.chemin.exists():
            # Construction paresseuse depuis le corpus encode.
            from ..corpus.construire_db import construire
            construire(self.chemin)
        self._charger()

    def _charger(self) -> None:
        conn = sqlite3.connect(str(self.chemin))
        conn.row_factory = sqlite3.Row
        try:
            self.champs: Dict[str, ChampConnaissance] = {
                r["code"]: ChampConnaissance(
                    r["code"], r["libelle"], r["poids"], r["description"] or ""
                )
                for r in conn.execute("SELECT * FROM champs ORDER BY poids")
            }
            self.institutions: Dict[str, Institution] = {
                r["identifiant"]: Institution(
                    r["identifiant"], r["nom"], r["type_institution"],
                    r["autorite"], r["perimetre"] or ""
                )
                for r in conn.execute("SELECT * FROM institutions ORDER BY autorite")
            }
            self.notions: Dict[str, Notion] = {}
            for r in conn.execute("SELECT * FROM notions"):
                self.notions[r["lemme"]] = Notion(
                    r["lemme"], r["champ_code"], r["source_id"],
                    bool(r["graphe"]), r["definition"] or ""
                )
            self.lemmes: FrozenSet[str] = frozenset(self.notions.keys())
            self.invariants: Tuple[Invariant, ...] = tuple(
                Invariant(r["code"], r["champ_code"], r["enonce"], r["severite"])
                for r in conn.execute("SELECT * FROM invariants ORDER BY code")
            )
            self.regles: Tuple[RegleIntention, ...] = tuple(
                RegleIntention(
                    r["priorite"], r["intention"], r["condition"],
                    r["champ_requis"], tuple((r["mots_declencheurs"] or "").split())
                )
                for r in conn.execute("SELECT * FROM regles_intention ORDER BY priorite")
            )
        finally:
            conn.close()

    def champ_ordre(self) -> Tuple[str, ...]:
        """Codes de champ dans l'ordre de poids croissant (ordre total)."""
        return tuple(c.code for c in sorted(self.champs.values(), key=lambda c: c.poids))

    def invariants_de(self, severite: Optional[str] = None) -> Tuple[Invariant, ...]:
        if severite is None:
            return self.invariants
        return tuple(v for v in self.invariants if v.severite == severite)
