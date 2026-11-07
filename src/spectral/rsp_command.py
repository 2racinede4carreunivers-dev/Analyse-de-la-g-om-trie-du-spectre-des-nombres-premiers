"""
CLI command 'rsp' — Rapport spectral direct pour toute combinaison
de premiers/positions dans l'intervalle 1..1000.

Syntaxes acceptees :
    rsp 7,23,2 29,17,13           -> tuples par virgules
    rsp (7,23,2) (29,17,13)       -> tuples parentheses
    rsp 2 3                        -> 1x1 (deux valeurs simples)
    rsp 7,23 29,17,13              -> asymetrique chaotique
    rsp-test sym 100               -> 100 tests aleatoires symetriques nxn
    rsp-test chaos 100             -> 100 tests aleatoires asym chaotiques
    rsp-test ord 100               -> 100 tests aleatoires asym ordonnees
    rsp-test 1x1 1000              -> 1000 tests aleatoires 1x1
"""
from __future__ import annotations

import random
import re
from typing import Optional

from ..core.spectral_core import SpectralMethodCore


_TUPLE_PAREN_RE = re.compile(r"\(([^)]+)\)")
_NUM_RE = re.compile(r"-?\d+")


def parse_rsp_args(raw: str) -> tuple[list[int], list[int]] | None:
    """
    Parse une chaine 'rsp 7,23,2 29,17,13' ou 'rsp (7,23,2) (29,17,13)'
    et retourne (A, B) ou None si parsing impossible.
    """
    raw = raw.strip()
    # Cas 1 : parentheses
    parens = _TUPLE_PAREN_RE.findall(raw)
    if len(parens) >= 2:
        a = [int(n) for n in _NUM_RE.findall(parens[0])]
        b = [int(n) for n in _NUM_RE.findall(parens[1])]
        return (a, b) if a and b else None
    # Cas 2 : deux groupes separes par espace, chaque groupe = csv de chiffres
    parts = raw.split()
    if len(parts) >= 2:
        # Chercher 2 groupes contenant chacun un ou plusieurs nombres
        # Strategie : recoller, puis splitter sur 'espace entre nombres et virgules'
        # On accepte aussi 'rsp 7,23,2 29,17,13'
        groups: list[list[int]] = []
        for part in parts:
            nums = [int(n) for n in _NUM_RE.findall(part)]
            if nums:
                groups.append(nums)
        if len(groups) >= 2:
            return groups[0], groups[1]
    return None


def random_combo(core: SpectralMethodCore, config: str, max_position: int = 1000) -> tuple[list[int], list[int]]:
    """
    Genere une combinaison aleatoire de primes pour une config donnee.
    config in : '1x1', 'sym2', 'sym3', 'sym5', 'chaos', 'ord'
    """
    primes = core.prime_list[:max_position]
    if config == "1x1":
        a, b = random.sample(primes, 2)
        return [a], [b]
    if config in ("sym2", "sym3", "sym5"):
        n = int(config[3:])
        chosen = random.sample(primes, 2 * n)
        return chosen[:n], chosen[n:]
    if config == "ord":
        # asymetrique ordonnee : indices strict croissants + max(A) < min(B), |B|=|A|+1
        size_a = random.randint(2, 4)
        size_b = size_a + 1
        # On veut size_a positions <= cut et size_b positions > cut, avec
        # cut tel que ces tailles sont realisables sans recouvrement
        cut = random.randint(size_a + 1, max_position - size_b - 1)
        a_pos = sorted(random.sample(range(1, cut + 1), size_a))
        b_pos = sorted(random.sample(range(cut + 1, max_position + 1), size_b))
        # On retourne les PRIMES (pas les positions) pour rester coherent avec
        # la convention "l'utilisateur ecrit des primes"
        return [core.prime_list[p - 1] for p in a_pos], [core.prime_list[p - 1] for p in b_pos]
    if config == "chaos":
        size_a = random.randint(2, 5)
        size_b = random.randint(2, 5)
        while size_b == size_a:
            size_b = random.randint(2, 5)
        a = random.sample(primes, size_a)
        b = random.sample(primes, size_b)
        return a, b
    raise ValueError(f"Config inconnue : {config}")

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
