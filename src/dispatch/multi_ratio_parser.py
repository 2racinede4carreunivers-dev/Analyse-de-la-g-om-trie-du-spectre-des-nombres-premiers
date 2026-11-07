#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
multi_ratio_parser.py — Parsing formel GENERALISE des requetes multi-rapports 1/k.
================================================================================
NE TOUCHE A AUCUN CALCUL : uniquement extraction (k_debut, k_fin, n) depuis
le texte libre francais, avec limite de commodite agent K_MAX_AGENT = 1_000_000.

Formes acceptees (generalisees, pas seulement 1/2 -> 1/111) :
  - "1/k=1/2 a 1/111", "1/2 a 1/111", "1/2 .. 1/111", "de 1/2 a 1/111"
  - "rapports multiples typiques et non typiques 1/2 a 1/111"
  - "k=2..111", "k 2 a 111", "k_debut=2 k_fin=111"
  - ratio unique "1/7" -> (7, 7, n)
  - n commun : "n=10", "n commune n=10", "pour n=10", defaut n=10

Limites :
  k >= 2, k_fin <= 1_000_000 (commodite agent, pipeline supporte jusqu'a 1e13).
  Si k_fin > limite -> ValueError explicite (pas de troncature silencieuse).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

K_MIN = 2
K_MAX_AGENT = 1_000_000  # limite de commodite fixee pour l'agent
N_DEFAUT = 10

_RE_N = re.compile(r"n\s*(?:commune?)?\s*=\s*(\d{1,3})", re.IGNORECASE)
_RE_N_ALT = re.compile(r"pour\s+n\s+(\d{1,3})", re.IGNORECASE)
# plages : 1/2 a 1/111, 1/k=1/2 a 1/k=1/111, 1/2..1/111, 1/2-1/111
_RE_PLAGE = re.compile(
    r"1\s*/\s*(?:k\s*=\s*)?(\d{1,7})\s*(?:a|à|-|–|\.{2,}|->|jusqu['’]?\s*a)\s*1\s*/\s*(?:k\s*=\s*)?(\d{1,13})",
    re.IGNORECASE,
)
# formes k=2..111 / k 2 a 111
_RE_K_PLAGE = re.compile(
    r"\bk\s*(?:=|de|entre)?\s*(\d{1,7})\s*(?:a|à|-|–|\.{2,}|->|et)\s*(\d{1,13})",
    re.IGNORECASE,
)
_RE_UNIQUE = re.compile(r"1\s*/\s*(\d{1,13})")


@dataclass(frozen=True)
class SpecMultiRatio:
    k_debut: int
    k_fin: int
    n: int
    multi: bool

    @property
    def taille(self) -> int:
        return self.k_fin - self.k_debut + 1


def _extraire_n(texte: str) -> int:
    m = _RE_N.search(texte)
    if m:
        return int(m.group(1))
    m = _RE_N_ALT.search(texte)
    if m:
        return int(m.group(1))
    return N_DEFAUT


def parser_multi_ratio(texte: str) -> SpecMultiRatio:
    """Parse generalise -> SpecMultiRatio. Lève ValueError si hors limites."""
    n = _extraire_n(texte)
    if n < 1:
        raise ValueError(f"n={n} invalide (n >= 1 requis).")

    m = _RE_PLAGE.search(texte)
    if m:
        kd, kf = int(m.group(1)), int(m.group(2))
        if kd > kf:
            kd, kf = kf, kd
        _valider_bornes(kd, kf)
        return SpecMultiRatio(k_debut=kd, k_fin=kf, n=n, multi=True)

    m = _RE_K_PLAGE.search(texte)
    if m:
        kd, kf = int(m.group(1)), int(m.group(2))
        if kd > kf:
            kd, kf = kf, kd
        _valider_bornes(kd, kf)
        return SpecMultiRatio(k_debut=kd, k_fin=kf, n=n, multi=True)

    m = _RE_UNIQUE.search(texte)
    if m:
        k = int(m.group(1))
        _valider_bornes(k, k)
        return SpecMultiRatio(k_debut=k, k_fin=k, n=n, multi=False)

    raise ValueError(f"Aucun ratio 1/k trouve dans : {texte!r}")


def _valider_bornes(kd: int, kf: int) -> None:
    if kd < K_MIN:
        raise ValueError(f"k_debut={kd} invalide (k >= {K_MIN} requis).")
    if kf > K_MAX_AGENT:
        raise ValueError(
            f"k_fin={kf} depasse la limite agent K_MAX_AGENT={K_MAX_AGENT:,}. "
            "Reformulez en sous-plages (ex. 1/2 a 1/1000000). "
            "Le pipeline supporte jusqu'a 1e13, l'agent plafonne a 1 million par commodite."
        )


def est_requete_multi(texte: str) -> bool:
    """True si le texte contient une plage multi-rapports."""
    return bool(_RE_PLAGE.search(texte) or _RE_K_PLAGE.search(texte))


if __name__ == "__main__":
    for t in [
        "Reconstruit les premiers pour 1/k=1/2 a 1/111 pour n commune n=10",
        "rapports multiples 1/2..1/20 n=10",
        "k=2..1000000 n=10",
        "le rapport 1/7 n=10",
    ]:
        print(t, "->", parser_multi_ratio(t))
