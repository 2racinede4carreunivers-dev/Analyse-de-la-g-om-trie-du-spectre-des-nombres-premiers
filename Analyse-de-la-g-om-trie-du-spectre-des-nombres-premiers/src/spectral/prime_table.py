"""
Table des nombres premiers indexes par position (1-based).
Pour rapport 1/2 : n = position = quantite de termes dans A et B.

PRIMES[n-1] = n-ieme nombre premier.
Table genere via sieve d Eratosthene, contient 1000 premiers (2 a 7919).
"""
from __future__ import annotations

from ._primes_data import PRIMES_RAW


PRIMES: list[int] = list(PRIMES_RAW)


def nth_prime(n: int) -> int | None:
    """Retourne le n-ieme nombre premier (1-indexed). 2 = 1er, 3 = 2e, etc."""
    if n < 1 or n > len(PRIMES):
        return None
    return PRIMES[n - 1]


def prime_position(p: int) -> int | None:
    """Retourne la position (1-indexed) du nombre premier p, ou None s'il n'est pas dans la table."""
    try:
        return PRIMES.index(p) + 1
    except ValueError:
        return None


def is_known_prime(p: int) -> bool:
    return p in PRIMES


def max_position() -> int:
    """Position max disponible dans la table."""
    return len(PRIMES)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
