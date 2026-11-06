"""MODELE CONFIRME DES 4 BRANCHES (derive analytique, verifie sur 676k ancres).

S_A(10) = k^10 + k^9 + k^6 + k^5 + k^4 + k^3 + k^2 + k
S_B(10) = k^11 + k^10 + k^7 + k^5 + k^4 + k^3 + k^2 + k
S_B - S_A = k^11 - k^9 + k^7 - k^6

P = (S_B - Digamma)/k^6,  Digamma = S_A + signe * k^pos

D'ou :
  A(8)-  (pos 8, signe -)  ->  P = B0 + k^2
  A(8)+  (pos 8, signe +)  ->  P = B0 - k^2
  A(7)+  (pos 7, signe +)  ->  P = B0 - k
  A(7)-  (pos 7, signe -)  ->  P = B0 + k
avec B0 = k^5 - k^3 + k - 1.

ATTENTION : le script _scan_regle_branche.py (ancien) inversait les signes
A(7)+ / A(7)- ; le mapping ci-dessous est le bon (verifie numeriquement).
"""

BRANCHES = ["A(8)-", "A(8)+", "A(7)+", "A(7)-"]
# coefficient de k^2 / k dans B0 + signe_effectif * (k^2 ou k)
SPEC = {
    "A(8)-": ("k2", +1),
    "A(8)+": ("k2", -1),
    "A(7)+": ("k", -1),
    "A(7)-": ("k", +1),
}


def B0(k: int) -> int:
    return k ** 5 - k ** 3 + k - 1


def candidate(k: int, branche: str) -> int:
    genre, mult = SPEC[branche]
    return B0(k) + mult * (k * k if genre == "k2" else k)


def candidats(k: int):
    """Les 4 candidats dans l'ordre BRANCHES."""
    return tuple(candidate(k, b) for b in BRANCHES)
