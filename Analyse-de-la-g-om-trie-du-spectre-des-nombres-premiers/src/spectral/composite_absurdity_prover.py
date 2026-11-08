"""
Preuve par l'absurde : la Methode Spectrale exclut strictement les composes.

Idee originale de Philippe Thomas Savard (2026-07-02) : l'echec systematique
de prime_position(C) pour un compose C constitue une preuve empirique par
l'absurde de la validite de la Methode Spectrale sur l'ensemble ℙ des
premiers.

Ce module transforme cette observation en un rapport pedagogique structure
retourne a l'utilisateur, en complement de la formalisation Isabelle/HOL
(theorem composite_not_prime_i dans theories/methode_spectral.thy autour
de la ligne 1490).

Cas emblematiques couverts (correspondent aux lemmes .thy) :
  - 4   = 2 * 2
  - 9   = 3 * 3
  - 15  = 3 * 5
  - 51  = 3 * 17   (cas rapporte par Philippe)
  - 91  = 7 * 13
  - 121 = 11 * 11
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .prime_table import PRIMES, nth_prime, prime_position


# Ensemble des premiers < 1000 pour tests rapides
_PRIME_SET: frozenset[int] = frozenset(PRIMES)


def is_prime(n: int) -> bool:
    """Verifie si |n| est premier (table interne, 1000 premiers indexes).

    Convention Methode Spectrale : les entiers negatifs -p (avec p premier
    positif) sont consideres comme des "premiers spectraux negatifs". Donc
    -7 est premier, -8 ne l'est pas, +51 = 3*17 ne l'est pas non plus.
    """
    abs_n = abs(int(n))
    if abs_n < 2:
        return False
    if abs_n in _PRIME_SET:
        return True
    # Fallback pour |n| > 1000 : test naif
    if abs_n > PRIMES[-1]:
        return _naive_prime_check(abs_n)
    return False


def _naive_prime_check(n: int) -> bool:
    """Test de primalite pour |n| au-dela de la table (n > 7919)."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def factorize(n: int) -> list[int]:
    """Retourne la decomposition en facteurs premiers de |n| (multiplicites).

    Exemples :
        factorize(51)  -> [3, 17]
        factorize(4)   -> [2, 2]
        factorize(121) -> [11, 11]
        factorize(-51) -> [3, 17]  (signe ignore)
    """
    n = abs(int(n))
    if n < 2:
        return []
    factors: list[int] = []
    for p in PRIMES:
        if p * p > n:
            break
        while n % p == 0:
            factors.append(p)
            n //= p
    if n > 1:
        factors.append(n)
    return factors


def nearest_primes(n: int) -> tuple[Optional[int], Optional[int]]:
    """Retourne (premier_inferieur, premier_superieur) autour de |n|.

    Utile pour suggerer une correction pedagogique :
        « 51 n'est pas premier ; voisins premiers : 47 (avant), 53 (apres) »
    """
    abs_n = abs(int(n))
    inf: Optional[int] = None
    sup: Optional[int] = None
    for p in PRIMES:
        if p < abs_n:
            inf = p
        elif p > abs_n and sup is None:
            sup = p
            break
        elif p == abs_n:
            # abs_n est premier lui-meme, cas non pedagogique ici
            return p, p
    return inf, sup


# ---------------------------------------------------------------------------
# Rapport pedagogique
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CompositeRejection:
    """Rapport pedagogique pour un entier compose soumis a Gabriel."""

    value: int
    factors: list[int]
    is_negative: bool
    nearest_prime_below: Optional[int]
    nearest_prime_above: Optional[int]
    thy_reference: str  # nom du lemme Isabelle/HOL correspondant si canonique

    @property
    def decomposition_str(self) -> str:
        """Ex : '51 = 3 x 17', '121 = 11 x 11', '-51 = -(3 x 17)'."""
        abs_val = abs(self.value)
        core = " x ".join(str(f) for f in self.factors) if self.factors else "?"
        if self.is_negative:
            return f"{self.value} = -({core}) = -{abs_val}"
        return f"{self.value} = {core}"

    def to_pedagogical_text(self) -> str:
        """Rend un message pedagogique complet, destine a etre affiche a
        l'utilisateur dans le CLI Gabriel."""
        lines: list[str] = []
        lines.append(
            f"[ARRET] {self.value} n'est pas un nombre premier."
        )
        lines.append("")
        lines.append("=== Preuve par l'absurde ===")
        lines.append(f"Decomposition factorielle : {self.decomposition_str}")
        lines.append("")
        lines.append(
            "La Methode Spectrale requiert un nombre premier. Elle ne s'applique"
        )
        lines.append(
            "qu'aux elements de ℙ. Cette contrainte n'est pas une lacune : elle"
        )
        lines.append(
            "est une CARACTERISATION AXIOMATIQUE stricte de ℙ, formalisee dans"
        )
        lines.append(
            "theories/methode_spectral.thy sous les theoremes :"
        )
        lines.append(f"  - composite_not_prime_i (theoreme principal - ecarts)")
        lines.append(
            f"  - spectral_method_exclusively_for_primes (corollaire - ecarts)"
        )
        lines.append(
            f"  - composite_no_reconstruction_position (extension - reconstruction)"
        )
        lines.append(
            f"  - composite_pair_no_rsp_positions (extension - rapport spectral RsP)"
        )
        if self.thy_reference:
            lines.append(f"  - {self.thy_reference} (cas concret)")
        lines.append("")
        if self.nearest_prime_below or self.nearest_prime_above:
            below = self.nearest_prime_below
            above = self.nearest_prime_above
            sign = "-" if self.is_negative else ""
            hints = []
            if below is not None:
                hints.append(f"{sign}{below}")
            if above is not None:
                hints.append(f"{sign}{above}")
            lines.append(
                "Voulez-vous plutot travailler avec un premier voisin ? "
                f"Candidats : {' ou '.join(hints)}."
            )
        return "\n".join(lines)


def _canonical_thy_reference(abs_value: int) -> str:
    """Retourne le nom du theoreme .thy specifique si le compose est
    canonique (4, 9, 15, 51, 91, 121), sinon ''."""
    canonical = {
        4: "no_spectral_position_for_4",
        9: "no_spectral_position_for_9",
        15: "no_spectral_position_for_15",
        51: "no_spectral_position_for_51",
        91: "no_spectral_position_for_91",
        121: "no_spectral_position_for_121",
    }
    return canonical.get(abs_value, "")


def build_composite_rejection(n: int) -> Optional[CompositeRejection]:
    """Construit un rapport de rejet si n est un entier compose (|n| > 1 non premier).

    Retourne None si n est premier ou si |n| < 2 (cas d'entree invalide).
    """
    abs_n = abs(int(n))
    if abs_n < 2:
        return None
    if is_prime(abs_n):
        return None
    factors = factorize(abs_n)
    below, above = nearest_primes(abs_n)
    if below == abs_n or above == abs_n:
        # abs_n est premier lui-meme (guard supplementaire)
        return None
    return CompositeRejection(
        value=int(n),
        factors=factors,
        is_negative=(n < 0),
        nearest_prime_below=below,
        nearest_prime_above=above,
        thy_reference=_canonical_thy_reference(abs_n),
    )


def detect_composite_in_gap_request(
    numbers: list[int],
) -> list[CompositeRejection]:
    """Retourne la liste des rejets pour les composes dans une requete d'ecart.

    Exemples :
        detect_composite_in_gap_request([-7, -51])   -> [rejet pour -51]
        detect_composite_in_gap_request([15, 51])    -> [rejet pour 15, rejet pour 51]
        detect_composite_in_gap_request([-7, -5])    -> []
    """
    rejections: list[CompositeRejection] = []
    for n in numbers:
        rej = build_composite_rejection(n)
        if rej is not None:
            rejections.append(rej)
    return rejections


__all__ = [
    "CompositeRejection",
    "build_composite_rejection",
    "detect_composite_in_gap_request",
    "factorize",
    "is_prime",
    "nearest_primes",
]

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
