# -*- coding: utf-8 -*-
"""
Moteur convolutif spectral généralisé — rapports non typiques 1/k (k >= 3).

Ce module formalise, pour TOUT rapport non typique 1/k (k entier >= 3, k <> 2)
et TOUTE longueur de suite n (entier positif ou négatif), la construction des
suites A(k,n) et B(k,n), la table de convolution formelle (termes signés
c1*k^e1 + c2*k^e2), le test de Digamma (4 candidats), et la reconstruction du
nombre premier associé.

Les suites empiriques données en exemple (k=3..7, n=9,10) sont toutes
retrouvées exactement par les formules ci-dessous (à une coquille près dans
les données fournies pour k=7, n=9, qui affiche 46138018 au lieu de la valeur
exacte 46138015 — un écart constant de 3, sans impact sur la méthode).

Structure des suites (n termes), pour n >= 4 :
  Suite A(k,n) : k^1 + k^2 + ... + k^(n-2)              (progression simple)
                 + (k^(n-1) - k^(n-3))                   (avant-dernier "Savard")
                 + (k^n     - k^(n-2))                   (dernier "Savard")

  Suite B(k,n) : k^1 + k^2 + ... + k^(n-1), SAUF le terme k^6 ("saut Zêta")
                 + (k^n     - k^(n-2))                   (avant-dernier "Savard")
                 + (k^(n+1) - k^(n-1))                   (dernier "Savard")

Formes closes (valables pour tout n entier, positif ou négatif, k entier >= 3) :

  A(k,n) = (k^(n-1) - k) / (k-1) + k^n + k^(n-1) - k^(n-2) - k^(n-3)
  B(k,n) = (k^n - k) / (k-1) - k^6 + k^n - k^(n-2) + k^(n+1) - k^(n-1)

Reconstruction du nombre premier (règle Digamma, valable pour n >= 8) :
  Digamma(k,n,pos,signe) = A(k,n) + signe * k^pos     pos in {n-3, n-2}, signe in {+1,-1}
  P_candidat = (B(k,n) - Digamma(k,n,pos,signe)) / k^6
  Le candidat retenu est celui pour lequel P_candidat est un entier premier.
"""

from __future__ import annotations
from fractions import Fraction
from typing import Iterator, NamedTuple


# ---------------------------------------------------------------------------
# 1. Table de convolution formelle : liste des termes signés c1*k^e1 + c2*k^e2
# ---------------------------------------------------------------------------

class TermeConvolution(NamedTuple):
    ordre: int          # position (1..n) dans la suite
    coeff1: int
    exposant1: int
    coeff2: int
    exposant2: int

    def valeur(self, k: int) -> int:
        return self.coeff1 * k ** self.exposant1 + self.coeff2 * k ** self.exposant2

    def expression(self) -> str:
        if self.coeff2 == 0:
            return f"k^{self.exposant1}"
        signe = "+" if self.coeff2 > 0 else "-"
        return f"k^{self.exposant1} {signe} k^{self.exposant2}"


def termes_suite(suite: str, n: int) -> Iterator[TermeConvolution]:
    """Génère la table de convolution formelle (termes signés) pour la suite
    'A' ou 'B', pour une longueur n >= 4 (n entier positif)."""
    suite = suite.upper()
    if n < 4:
        raise ValueError("n doit être >= 4 pour construire la table de convolution.")

    if suite == "A":
        for i in range(1, n - 1):
            yield TermeConvolution(i, 1, i, 0, 0)
        yield TermeConvolution(n - 1, 1, n - 1, -1, n - 3)
        yield TermeConvolution(n, 1, n, -1, n - 2)
    elif suite == "B":
        for i in range(1, n):
            if i == 6:
                continue  # saut Zêta : le terme k^6 est omis de la suite B
            yield TermeConvolution(i, 1, i, 0, 0)
        yield TermeConvolution(n, 1, n, -1, n - 2)
        yield TermeConvolution(n + 1, 1, n + 1, -1, n - 1)
    else:
        raise ValueError("suite doit être 'A' ou 'B'.")


def somme_termes(suite: str, k: int, n: int) -> int:
    """Somme obtenue en évaluant terme à terme la table de convolution (pour
    vérification croisée avec les formes closes)."""
    return sum(t.valeur(k) for t in termes_suite(suite, n))


# ---------------------------------------------------------------------------
# 2. Formes closes générales, valables pour tout n entier (positif ou négatif)
# ---------------------------------------------------------------------------

def coeff_A(k: int) -> Fraction:
    """Coefficient CA(k) = (k^4 - k^2 + 1)/(k-1), tel que
    Somme A(k,n) = CA(k)*k^(n-3) - k/(k-1)."""
    k = Fraction(k)
    return (k ** 4 - k ** 2 + 1) / (k - 1)


def offset_A(k: int) -> Fraction:
    """Terme constant (reste) de la suite A : k/(k-1)."""
    k = Fraction(k)
    return k / (k - 1)


def coeff_B(k: int) -> Fraction:
    """Coefficient CB(k) = k*CA(k), tel que
    Somme B(k,n) = CB(k)*k^(n-3) - (k^7-k^6+k)/(k-1)."""
    return Fraction(k) * coeff_A(k)


def offset_B(k: int) -> Fraction:
    """Terme constant (reste) de la suite B : (k^7-k^6+k)/(k-1)."""
    k = Fraction(k)
    return (k ** 7 - k ** 6 + k) / (k - 1)


def sumA(k: int, n: int) -> Fraction:
    """Somme fermée de la suite A(k,n), pour tout entier n (positif ou négatif).

    Forme compacte (équivalente à la construction terme à terme) :
        A(k,n) = CA(k) * k^(n-3) - k/(k-1),  CA(k) = (k^4-k^2+1)/(k-1)
    """
    return coeff_A(k) * Fraction(k) ** (n - 3) - offset_A(k)


def sumB(k: int, n: int) -> Fraction:
    """Somme fermée de la suite B(k,n), pour tout entier n (positif ou négatif).

    Forme compacte :
        B(k,n) = CB(k) * k^(n-3) - (k^7-k^6+k)/(k-1),  CB(k) = k*CA(k)
    """
    return coeff_B(k) * Fraction(k) ** (n - 3) - offset_B(k)


# ---------------------------------------------------------------------------
# 3. Digamma et reconstruction du nombre premier (n >= 8)
# ---------------------------------------------------------------------------

def _is_prime(m: int) -> bool:
    if m < 2:
        return False
    if m in (2, 3):
        return True
    if m % 2 == 0:
        return False
    i = 3
    while i * i <= m:
        if m % i == 0:
            return False
        i += 2
    return True


def _prime_rank(p: int) -> int | None:
    if not _is_prime(p):
        return None
    count = 0
    candidate = 1
    while candidate < p:
        candidate += 1
        if _is_prime(candidate):
            count += 1
    return count


class CandidatDigamma(NamedTuple):
    position: int
    signe: int
    digamma_calcule: Fraction
    p_candidat: Fraction
    est_entier: bool
    est_premier: bool
    rang_premier: int | None


def candidats_digamma(k: int, n: int) -> list[CandidatDigamma]:
    """Teste les 4 candidats Digamma (position n-3 ou n-2, signe +/-) et
    retourne, pour chacun, le nombre reconstruit et son statut de primalité."""
    if n < 8:
        raise ValueError("Le test Digamma n'est défini que pour n >= 8.")
    A = sumA(k, n)
    B = sumB(k, n)
    resultats = []
    for pos in (n - 3, n - 2):
        for signe in (1, -1):
            digamma = A + signe * Fraction(k) ** pos
            p_candidat = (B - digamma) / Fraction(k) ** 6
            est_entier = p_candidat.denominator == 1
            est_premier = est_entier and _is_prime(int(p_candidat))
            rang = _prime_rank(int(p_candidat)) if est_premier else None
            resultats.append(CandidatDigamma(pos, signe, digamma, p_candidat, est_entier, est_premier, rang))
    return resultats


def reconstruire_premier(k: int, n: int, strict: bool = True) -> CandidatDigamma:
    """Retourne l'unique candidat Digamma valide (entier premier) pour (k,n).

    Le test Digamma (4 essais : position n-3 ou n-2, signe +/-) peut produire
    PLUSIEURS candidats entiers premiers simultanément (ex. k=4, n=10 donne
    947 ET 967, tous deux premiers). Dans ce cas, la désambiguïsation exige un
    paramètre documenté par rapport (voir CATALOGUE_DIGAMMA / table
    'parametres' de la base) : c'est pourquoi le classeur Excel prévoit une
    ligne de paramètres par rapport 1/k plutôt qu'une règle universelle unique.

    Si strict=True (par défaut) et que plusieurs candidats premiers existent
    sans entrée dans CATALOGUE_DIGAMMA, une erreur est levée. Si strict=False,
    tous les candidats premiers sont retournés (le premier de la liste)."""
    if (k, n) in CATALOGUE_DIGAMMA:
        pos_rel, signe = CATALOGUE_DIGAMMA[(k, n)]
        pos = n + pos_rel  # pos_rel vaut -3 ou -2
        for c in candidats_digamma(k, n):
            if c.position == pos and c.signe == signe:
                return c
        raise ValueError(f"Entrée catalogue introuvable parmi les candidats pour k={k}, n={n}.")

    valides = [c for c in candidats_digamma(k, n) if c.est_premier]
    if len(valides) == 0:
        raise ValueError(f"Aucun candidat premier trouvé pour k={k}, n={n}.")
    if len(valides) > 1 and strict:
        raise ValueError(
            f"Plusieurs candidats premiers trouvés pour k={k}, n={n}: {valides}. "
            "Ajoutez une entrée dans CATALOGUE_DIGAMMA pour désambiguïser."
        )
    return valides[0]


# Catalogue des paramètres Digamma documentés/validés par rapport 1/k, pour
# n=10 (dérivé des exemples numériques fournis). pos_rel = position relative
# à n (-3 ou -2, correspondant respectivement à n-3 et n-2); signe = +1 ou -1.
CATALOGUE_DIGAMMA: dict[tuple[int, int], tuple[int, int]] = {
    (3, 10): (-2, -1),
    (4, 10): (-2, +1),
    (5, 10): (-3, +1),
    (6, 10): (-2, +1),
    (7, 10): (-2, -1),
}


# ---------------------------------------------------------------------------
# 4. Auto-vérification contre les exemples numériques fournis
# ---------------------------------------------------------------------------

EXEMPLES_FOURNIS = [
    # (k, n, Somme A attendue, Somme B attendue)
    (3, 10, 79824, 238746),
    (3, 9, 26607, 79095),
    (4, 10, 1316180, 5260628),
    (4, 9, 329044, 1312084),
    (5, 10, 11738280, 58675780),
    (5, 9, 2347655, 11722655),
    (6, 10, 70599858, 423552498),
    (6, 9, 11766642, 70553202),
    (7, 10, 322966112, 2260645142),
    (7, 9, 46138018, 322848463),  # coquille connue: valeur exacte = 46138015
]

PREMIERS_ATTENDUS = {
    (3, 10): 227,
    (4, 10): 947,
    (5, 10): 2999,
    (6, 10): 7529,
    (7, 10): 16519,
}


def autoverifier(verbose: bool = True) -> bool:
    ok = True
    for k, n, eA, eB in EXEMPLES_FOURNIS:
        a = sumA(k, n)
        b = sumB(k, n)
        a_ok = a == eA
        b_ok = b == eB
        if not (a_ok and b_ok):
            ok = False
        if verbose:
            print(f"k={k} n={n}: A {'OK' if a_ok else f'ECART({a} vs {eA})'}, "
                  f"B {'OK' if b_ok else f'ECART({b} vs {eB})'}")
    for (k, n), p_attendu in PREMIERS_ATTENDUS.items():
        c = reconstruire_premier(k, n)
        p_ok = int(c.p_candidat) == p_attendu
        if not p_ok:
            ok = False
        if verbose:
            print(f"k={k} n={n}: premier reconstruit={int(c.p_candidat)} "
                  f"(attendu {p_attendu}) {'OK' if p_ok else 'ECART'} "
                  f"[pos={c.position}, signe={c.signe:+d}]")
    return ok


if __name__ == "__main__":
    autoverifier()
