#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUITES GEOMETRIQUES NIVEAU 2 - Pipeline Cognitif Gabriel v7.5
==============================================================

Implementation unifiee des NIVEAUX 1 et 2 du systeme convolutif spectral,
conforme :
  - aux exemples du rapport (1/k = 1/7 entier, et niveau geometrique n=10) ;
  - aux REGLES SAVARD formalisees (sections XI et XII, sans tactique ring) :
      raison spectrale        r = x2 / x1 = k
      progression simple      terme_i = a1 * r^(i-1)
      avant-dernier (A)       (r - 1/r) * a1 * r^(n-3)     [position n-1]
      dernier       (A)       avant-dernier * r            [position n]
      saut Zeta     (B)       position 6 = a1 * r^6
      positions suivantes(B)  a1 * r^i  (decalage +1 du a la substitution)
      avant-dernier (B)       (r - 1/r) * a1 * r^(n-2)     [position n-1]
      dernier       (B)       avant-dernier * r            [position n]

NIVEAU 1 - termes entiers (a1 = r = k) - exemple 1/k = 1/7, n=10 :
  Suite A : k^1+...+k^8+(k^9-k^7)+(k^10-k^8)                 = 322966112
  Suite B : k^1+...+k^5+k^7+k^8+k^9+(k^10-k^8)+(k^11-k^9)    = 2260645142
  Digamma  : Somme_A - k^8                                    = 317201321
  Premier  : (Somme_B - Digamma) / k^6 = 1943443821/117649      = 16519

NIVEAU 2 - termes geometriques sqrt(a^2+b^2) (a1 = sqrt(1+k^2), r = k) :
  Suite A : a1 + a1*k + ... + (k^(n-2)-k^(n-4))*a1 + (k^(n-1)-k^(n-3))*a1
  Suite B : a1 + a1*k + ... + a1*k^6 + ... (meme structure que le niveau 1)
  Les positions 7 et 8 de la suite A sont a1*k^6 et a1*k^7 : les 4 Digamma,
  le diviseur k^6, les coefficients et les equations generalisees ont donc
  EXACTEMENT LES MEMES UTILITES que pour le niveau 1.

FORMES FERMEES UNIVERSELLES (section XII) :
  C_k = k^4 - k^2 + 1        (ecart des suites A -> 13, 73, 601, 1261, 2353)
  m_k = k^6 - k^5 + 1        (facteur du reste B -> 33, 487, 12501, 38881, 100843)
  S_A(n) = C_k*k^(n-3)/(k-1) - k/(k-1)
  S_B(n) = C_k*k^(n-2)/(k-1) - m_k*k/(k-1)

  Coefficient A = C_k/k^2     Coefficient B = C_k/k     x = k*(k-1)
  Reste A = k/(k-1)          Reste B = m_k*k/(k-1) = m_k * Reste A
  Equation A (n>0) : (Coefficient A / x)*k^n - Reste A = Somme suite A
  Equation B (n>0) : (Coefficient B / x)*k^n - Reste B = Somme suite B
  Equation A (n<0) : Coefficient A * k^n - Reste A      = Somme suite A

CONVENTIONS VERROUILLEES (methode spectrale / systeme convolutif) :
  - n est TOUJOURS un entier strictement positif (n >= 1). n=0 et toute
    valeur non entiere sont rejetes (ValueError). Le chemin n<0 / premiers
    negatifs existe dans le code mais est INACTIF et non requis pour l'heure.
  - Tout ancrage a n=10 correspond a la POSITION d'un nombre premier dans P.
  - Equation spectrale : (Somme suite B - Digamma calcule)
    / (6eme position suite A zeta) = Nombre premier a la position n.
  - PREUVE PAR L'ABSURDE (exclusion des composites C) : supposer C=Ci avec
    Ci=Pi ; un composite n'est jamais premier, donc les C sont exclus.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple, Union


# ============================================================
# GARDE-FOUS n (ENTIER STRICTEMENT POSITIF)
# ============================================================

def valider_n(n) -> int:
    """Garde-fou : n doit etre un entier strictement positif (n >= 1).

    n = 0, les valeurs negatives et non entieres sont rejetees (ValueError).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError(f"n doit etre un entier strictement positif, recu : {n!r}")
    if n < 1:
        raise ValueError(
            f"n doit etre un entier strictement positif (n >= 1), recu : {n}"
        )
    return n


def est_premier(m: int) -> bool:
    """Test de primalite deterministe (divisions impaires jusqu'a sqrt(m))."""
    if m < 2:
        return False
    if m == 2:
        return True
    if m % 2 == 0:
        return False
    for i in range(3, math.isqrt(m) + 1, 2):
        if m % i == 0:
            return False
    return True


def preuve_absurde_generique(k: int, somme_B: int, digamma: int,
                             pos6: int, verbose: bool = False) -> dict:
    """Preuve par l'absurde : seul un quotient entier PREMIER passe.

    Hypothese : C = Ci avec Ci = Pi. Si (Somme_B - Digamma)/pos6 = Ci = Pi
    alors Ci = C <> P, ce qui est impossible car un composite n'est jamais
    premier : les composites C sont donc exclus de la methode spectrale,
    pour tout nombre premier P.
    """
    quotient = Fraction(somme_B - digamma, pos6)
    est_entier = ((somme_B - digamma) % pos6 == 0)
    P = (somme_B - digamma) // pos6 if est_entier else None
    P_premier = est_premier(P) if P is not None else False
    tenable = bool(est_entier and P_premier)
    conclusion = (
        "Preuve par l'absurde OK : quotient entier PREMIER ; C exclus."
        if tenable else
        "Contradiction : quotient non premier -> C exclu."
    )
    if verbose:
        print(f"  [Absurde k=1/{k}] (S_B-Digamma)/pos6 = {quotient} -> {conclusion}")
    return {"k": k, "quotient": quotient, "entier": est_entier,
            "P": P, "P_premier": P_premier,
            "hypothese_Ci_eq_Pi_tenable": tenable, "conclusion": conclusion}


# ============================================================
# STRUCTURES DE DONNEES
# ============================================================

@dataclass
class ResultatNiveau1Entiers:
    """Resultat du calcul niveau 1 - suites A et B a termes entiers."""
    k: int
    n: int
    somme_A: int
    somme_B: int
    termes_A: List[int] = field(default_factory=list)
    termes_B: List[int] = field(default_factory=list)
    premier_reconstruit: Optional[int] = None

    def __repr__(self):
        return (f"ResultatN1(k=1/{self.k}, n={self.n}, "
                f"S_A={self.somme_A}, S_B={self.somme_B})")


@dataclass
class ResultatNiveau2Geometrique:
    """Resultat du calcul niveau 2 - suites A et B geometriques."""
    k: Union[int, float]
    n: int
    t: float
    somme_A: float
    somme_B: float
    termes_A: List[float] = field(default_factory=list)
    termes_B: List[float] = field(default_factory=list)
    coefficient_A: Optional[Any] = None
    coefficient_B: Optional[Any] = None
    equation_A_positif: Optional[str] = None
    equation_B_positif: Optional[str] = None
    equation_A_negatif: Optional[str] = None
    equation_B_negatif: Optional[str] = None
    premiers_trouves: List[int] = field(default_factory=list)

    def __repr__(self):
        return (f"ResultatN2(k=1/{self.k}, n={self.n}, "
                f"S_A={self.somme_A:.6f}, S_B={self.somme_B:.6f})")


# ============================================================
# REGLES SAVARD (SECTION XI) - CONSTRUCTION DES SUITES A ET B
# ============================================================

# Ordre d'ancrage des 4 possibilites Digamma (positions 8 puis 7 de la suite A).
# Section XIV.5 : l'ancrage retenu a n=10 est le premier candidat entier premier
# dans cet ordre. Les DEUX niveaux (entier et geometrique) partagent le meme
# ordre : la verification numerique montre que l'ordre 8- puis 8+ puis 7+ puis
# 7- reproduit les HUIT ancrages du tableau XIV.6.
ORDRE_DIGAMMA = ((8, -1), (8, +1), (7, +1), (7, -1))
ORDRE_DIGAMMA_NIVEAU_1 = ORDRE_DIGAMMA
ORDRE_DIGAMMA_NIVEAU_2 = ORDRE_DIGAMMA

#: Ancrages du systeme convolutif (section XIV.6) : pour chaque rapport 1/k,
#: (rang du premier dans la table P, premier d'ancrage a n=10).
#:   rang_base_k  : rang du premier d'ancrage
#:   premier_base : premier reconstruit a n=10 (les 4 essais Digamma)
ANCRAGES_XIV = {
    2: {'rang': 10,    'premier': 29},
    3: {'rang': 49,    'premier': 227},
    4: {'rang': 161,   'premier': 947},
    5: {'rang': 430,   'premier': 2999},
    6: {'rang': 954,   'premier': 7529},
    7: {'rang': 1913,  'premier': 16519},
    8: {'rang': 3468,  'premier': 32327},
    9: {'rang': 5906,  'premier': 58337},
}


def nieme_premier(rang: int) -> int:
    """Rang-ième nombre premier (rang entier >= 1)."""
    if rang < 1:
        raise ValueError(f"rang doit etre un entier >= 1, recu : {rang}")
    compteur = 0
    candidat = 1
    while compteur < rang:
        candidat += 1
        if est_premier(candidat):
            compteur += 1
    return candidat


def rang_cible(k: int, n: int) -> int:
    """Section XIV.6 : rang cible = rang base + n - 10."""
    n = valider_n(n)
    if k not in ANCRAGES_XIV:
        raise ValueError(f"aucun ancrage connu pour k={k} (table XIV.6)")
    return ANCRAGES_XIV[k]['rang'] + n - 10


def premier_cible(k: int, n: int) -> int:
    """Section XIV.6 : P_cible(n) = tblPremiers[rang_cible(n)]."""
    return nieme_premier(rang_cible(k, n))


def digamma_calcule(k: int, n: int, somme_B: Optional[int] = None) -> int:
    """Section XIV.6 : Digamma(k,n) = Somme_B(k,n) - P_cible(n) * k^6."""
    n = valider_n(n)
    if somme_B is None:
        somme_B = CalculateurNiveau1Entiers(k=k).calculer(n).somme_B
    return somme_B - premier_cible(k, n) * k ** 6


def construire_termes_savard(a1, r, n):
    """Section XI : construit les n termes des suites A et B.

    a1 : premier terme (k pour le niveau 1 entier, sqrt(1+k^2) pour le
         niveau 2 geometrique).
    r  : raison spectrale (x2/x1 = k).
    n  : nombre de termes (entier strictement positif).

    Retourne le couple (termes_A, termes_B). Pour n < 8 les deux suites
    coincident avec la progression simple : la condition terminale et le saut
    Zeta ne s'appliquent qu'a partir de 8 termes (section XI.6).
    """
    n = valider_n(n)

    if n < 8:
        base = [a1 * r ** (i - 1) for i in range(1, n + 1)]
        return base, list(base)

    # --- Suite A : progression simple (positions 1 a n-2) puis terminale ---
    termes_A = [a1]
    termes_A += [a1 * r ** (i - 1) for i in range(2, n - 1)]
    avant_dernier_A = (r - 1 / r) * (a1 * r ** (n - 3))
    termes_A += [avant_dernier_A, avant_dernier_A * r]

    # --- Suite B : saut Zeta en position 6 puis decalage (+1) des positions
    termes_B = [a1]
    termes_B += [a1 * r ** (i - 1) for i in range(2, 6)]
    termes_B += [a1 * r ** 6]
    termes_B += [a1 * r ** i for i in range(7, n - 1)]
    avant_dernier_B = (r - 1 / r) * (a1 * r ** (n - 2))
    termes_B += [avant_dernier_B, avant_dernier_B * r]

    return termes_A, termes_B


# ============================================================
# CALCULATEUR NIVEAU 1 - SUITES A ET B ENTIERS (ex: 1/7)
# ============================================================

class CalculateurNiveau1Entiers:
    """Suites A et B a termes entiers pour le rapport 1/k (a1 = r = k).

    Exemple 1/k = 1/7, n=10 :
      Suite A : 7^1+7^2+...+7^8+(7^9-7^7)+(7^10-7^8)                 = 322966112
      Suite B : 7^1+7^2+7^3+7^4+7^5+7^7+7^8+7^9+(7^10-7^8)+(7^11-7^9) = 2260645142

    Pour n=9 (reference 16511) :
      Suite A : 7^1+...+7^7+(7^8-7^6)+(7^9-7^7)                      = 46138018
      Suite B : 7^1+...+7^5+7^7+7^8+(7^9-7^7)+(7^10-7^8)             = 322848463

    Formes fermees (section XII) :
      S_A(n) = C*k^(n-3)/(k-1) - k/(k-1)
      S_B(n) = C*k^(n-2)/(k-1) - m*k/(k-1),  C = k^4-k^2+1, m = k^6-k^5+1
    """

    def __init__(self, k: int):
        k = int(k)
        if k < 2:
            raise ValueError("k doit etre un entier >= 2")
        self.k = k
        self.t = Fraction(1, k)
        self.C = k ** 4 - k ** 2 + 1              # ecart des suites A
        self.m = k ** 6 - k ** 5 + 1              # facteur du reste de B
        self.x = k * (k - 1)                      # bloc A de (Reste + x)
        self.coefficient_A = Fraction(self.C, k ** 2)
        self.coefficient_B = Fraction(self.C, k)
        self.reste_A = Fraction(k, k - 1)
        self.reste_B = Fraction(self.m * k, k - 1)

    # --- generation des termes (section XI) --------------------------
    def generer_suite_A_termes(self, n: int) -> List[int]:
        n = valider_n(n)
        termes, _ = construire_termes_savard(Fraction(self.k), Fraction(self.k), n)
        return [int(t) for t in termes]

    def generer_suite_B_termes(self, n: int) -> List[int]:
        n = valider_n(n)
        _, termes = construire_termes_savard(Fraction(self.k), Fraction(self.k), n)
        return [int(t) for t in termes]

    # --- formes fermees (XIV.2) --------------------------------------
    #: Domaine de validite des formes fermees convolutives (XIV.2) : elles
    #: coincident exactement avec la construction terme a terme (XIV.4) a
    #: partir de n = 8, seuil auquel les deux termes terminaux Savard et le
    #: saut Zeta de la suite B s'appliquent (XIV.4 : « Pour n <= 7 :
    #: terme_b = terme_a », c'est-a-dire progression simple sans condition
    #: terminale). En dessous de ce seuil, XIV.2 et XIV.4 divergent : la
    #: construction XIV.4 fait foi et est retournee telle quelle.
    SEUIL_FORMES_FERMEES = 8

    def somme_A_formelle(self, n: int) -> Fraction:
        """S_A(n) = C*k^(n-3)/(k-1) - k/(k-1)  (forme fermee XIV.2, n >= 8)."""
        n = valider_n(n)
        if n < self.SEUIL_FORMES_FERMEES:
            return Fraction(sum(self.generer_suite_A_termes(n)))
        return Fraction(self.C * self.k ** (n - 3), self.k - 1) - self.reste_A

    def somme_B_formelle(self, n: int) -> Fraction:
        """S_B(n) = C*k^(n-2)/(k-1) - m*k/(k-1)  (forme fermee XIV.2, n >= 8)."""
        n = valider_n(n)
        if n < self.SEUIL_FORMES_FERMEES:
            return Fraction(sum(self.generer_suite_B_termes(n)))
        return Fraction(self.C * self.k ** (n - 2), self.k - 1) - self.reste_B

    def calculer(self, n: int = 10) -> ResultatNiveau1Entiers:
        """Calcule les suites A et B entieres pour n termes."""
        n = valider_n(n)
        termes_A = self.generer_suite_A_termes(n)
        termes_B = self.generer_suite_B_termes(n)
        return ResultatNiveau1Entiers(
            k=self.k, n=n, somme_A=sum(termes_A), somme_B=sum(termes_B),
            termes_A=termes_A, termes_B=termes_B,
        )

    def equations_generalisees(self) -> Dict[str, str]:
        """Equations reconstruites pour n entier strictement positif."""
        k, x = self.k, self.x
        return {
            'equation_A_positif': (
                f"({self.coefficient_A}/{x} * {k}^n) - {self.reste_A}"
                f" = Somme suite A (n > 0)"
            ),
            'equation_B_positif': (
                f"({self.coefficient_B}/{x} * {k}^n) - {self.reste_B}"
                f" = Somme suite B (n > 0)"
            ),
            'equation_A_negatif': (
                f"{self.coefficient_A} * {k}^(-n) - {self.reste_A}"
                f" = Somme suite A (n < 0)"
            ),
            'equation_B_negatif': (
                f"{self.coefficient_B} * {k}^(-n) - {self.reste_B}"
                f" = Somme suite B (n < 0)"
            ),
        }


# ============================================================
# METHODE DIGAMMA - NIVEAU 1 (termes entiers)
# ============================================================

class MethodeDigamma:
    """4 possibilites Digamma sur la suite A entiere (positions 8 et 7).

      1. Digamma = Somme_A + position_8
      2. Digamma = Somme_A - position_8
      3. Digamma = Somme_A + position_7
      4. Digamma = Somme_A - position_7

    Puis : P_candidat = (Somme_B - Digamma) / k^6 (6eme position de la suite A
    zeta). Les 4 possibilites determinent la valeur du Digamma calcule.

    Exemple 1/7 : Digamma = 322966112 - 7^8 = 317201321
                  P = (2260645142 - 317201321)/7^6 = 16519 (premier)
    Exemple 1/5 : Digamma = 11738280 + 5^7 = 11816405
                  P = (58675780 - 11816405)/5^6 = 2999 (premier)
    Exemple 1/6 : Digamma = 70599858 + 6^7 = 72279474
                  P = (423552498 - 72279474)/6^6 = 7529 (premier)
    """

    ORDRE = ORDRE_DIGAMMA_NIVEAU_1

    def __init__(self, k: int, n: int = 10):
        self.k = int(k)
        self.n = n
        self.position_7 = self.k ** 7 if n >= 7 else None
        self.position_8 = self.k ** 8 if n >= 8 else None
        self.k_pow_6 = self.k ** 6

    @staticmethod
    def _est_premier(m: int) -> bool:
        return est_premier(m)

    def generer_digamma_possibilities(self, somme_A: int) -> List[Dict]:
        """Genere les 4 possibilites Digamma dans l'ordre d'ancrage."""
        possibilites = []
        termes_pos = {8: self.position_8, 7: self.position_7}
        # Ordre d'ancrage declare (ORDRE_DIGAMMA), identique aux niveaux 1 et 2.
        for position, signe in self.ORDRE:
            terme = termes_pos[position]
            if terme is None:
                continue
            possibilites.append({
                'position': position,
                'signe': signe,
                'digamma_calcule': somme_A + signe * terme,
                'P_candidat': None,
                'est_premier': False,
                'description': (
                    f"{'+' if signe > 0 else '-'} position {position} "
                    f"(k^{position}={terme})"
                ),
            })
        return possibilites

    def reconstruire_premier(self, somme_A: int, somme_B: int,
                             verbose: bool = True) -> Tuple[Optional[int], List[Dict]]:
        """Tente de reconstruire le nombre premier via les 4 Digamma."""
        possibilites = self.generer_digamma_possibilities(somme_A)
        resultats: List[Dict] = []
        premier_trouve: Optional[int] = None

        for poss in possibilites:
            numerateur = somme_B - poss['digamma_calcule']
            if numerateur % self.k_pow_6 == 0:
                P = numerateur // self.k_pow_6
                poss['P_candidat'] = P
                poss['est_premier'] = est_premier(P)
                if poss['est_premier'] and premier_trouve is None:
                    premier_trouve = P
            else:
                poss['P_candidat'] = Fraction(numerateur, self.k_pow_6)
                poss['est_premier'] = False
            resultats.append(poss)

            if verbose:
                premier_str = " PREMIER" if poss['est_premier'] else ""
                print(f"  Digamma [{poss['description']}]: "
                      f"digamma={poss['digamma_calcule']}, "
                      f"P={poss['P_candidat']}{premier_str}")

        return premier_trouve, resultats


# ============================================================
# NIVEAU 2 - CONSTRUCTION GEOMETRIQUE + METHODE SPECTRALE
# ============================================================
# Meme methode que le niveau 1, en forme geometrique : a1 = sqrt(1+k^2),
# r = k (t = k). Les composantes (a, b) de chaque terme sont en progression
# spectrale ; comme tous les radicaux sont des carres (a^2+b^2 = a^2(1+r^2)),
# chaque terme geometrique vaut exactement sqrt(1+k^2) fois le terme entier
# correspondant. Exemple n=10 (t = k) :
#   suite A = sqrt(1^2+t^2), sqrt(t^2+t^4), ..., sqrt((t^8-t^6)^2+(t^9-t^7)^2),
#             sqrt((t^9-t^7)^2+(t^10-t^8)^2)
#   suite B = idem avec le saut Zeta en position 6 (t^6 -> t^7), decalage +1.

def construire_termes_savard_geometrique(k, n):
    """Section XI en forme geometrique : termes sqrt(a^2 + b^2).

    Correspondance exacte avec le niveau 1 : le terme entier correspondant joue
    le role de la composante a et b = k * a, de sorte que

        (a^2 + b^2)^(1/2) = a * sqrt(1 + k^2)

    Exemple n=10, k=7 : sqrt(1^2+t^2), sqrt(t^2+t^4), ...,
    sqrt((t^8-t^6)^2 + (t^9-t^7)^2), sqrt((t^9-t^7)^2 + (t^10-t^8)^2)
    pour la suite A (t = k), et la meme progression avec le saut Zeta en
    position 6 et le decalage (+1) pour la suite B.

    Retourne le couple (termes_A, termes_B) en flottants.
    """
    k = int(k)
    n = valider_n(n)
    t = float(k)

    def terme(terme_entier):
        """Radical sqrt(a^2+b^2) avec a = terme_entier et b = k * terme_entier."""
        a = float(terme_entier)
        return math.hypot(a, t * a)

    termes_A_int, termes_B_int = construire_termes_savard(k, k, n)
    return ([terme(v) for v in termes_A_int],
            [terme(v) for v in termes_B_int])


def ecart_spectral(somme_A_n1, somme_A_n2, k: int, exposant: int = 8):
    """Ecart spectral normalise : (S_A(n1) - S_A(n2)) / k^exposant."""
    return Fraction(somme_A_n1 - somme_A_n2, k ** exposant)


# ============================================================
# METHODE DIGAMMA - NIVEAU 2 (termes geometriques)
# ============================================================

class MethodeDigammaGeometrique:
    """4 possibilites Digamma sur la suite A GEOMETRIQUE (meme regle).

      1. Digamma = Somme_A + position_8   (position 8 = a1*k^7)
      2. Digamma = Somme_A - position_8
      3. Digamma = Somme_A + position_7   (position 7 = a1*k^6)
      4. Digamma = Somme_A - position_7

    Puis : P_candidat = (Somme_B - Digamma) / (6eme position suite A zeta)

    La 6eme position de la suite A vaut a1*k^5 (a1 = sqrt(1+k^2)) mais, selon
    la regle du niveau 1, le diviseur spectral est k^6 : les deux niveaux ont
    donc EXACTEMENT les memes utilites (les radicaux ne sont pas des carres
    parfaits, on conserve donc la valeur entiere k^6 comme au niveau 1).

    Exemple k=7 : (- position 8) -> 16519 ; (+ position 8) -> 16421 ;
    (- position 7) -> 16477 : trois nombres premiers, conformement a la
    propriete des 4 possibilites du Digamma.
    """

    def __init__(self, k: int, n: int = 10, ordre=None):
        k = int(k)
        if k < 2:
            raise ValueError("k doit etre un entier >= 2")
        self.k = k
        self.n = valider_n(n)
        self.ordre = ordre if ordre is not None else ORDRE_DIGAMMA_NIVEAU_2
        self.k_pow_6 = k ** 6
        self.calc_entiers = CalculateurNiveau1Entiers(k=k)

    @property
    def facteur(self) -> float:
        """Facteur geometrique a1 = sqrt(1 + k^2)."""
        return math.sqrt(1.0 + self.k ** 2)

    def _resoudre_n(self, res, n) -> int:
        """Determine n depuis (n explicite, resultat geometrique, n par defaut)."""
        if n is not None:
            return valider_n(n)
        if res is not None and getattr(res, 'n', None) is not None:
            return valider_n(res.n)
        return self.n

    def composantes_zeta(self, n: Optional[int] = None):
        """Composantes zeta entieres : (termes_A, termes_B, somme_A, somme_B).

        Chaque terme geometrique est exactement `facteur * composante_zeta` :
        les composantes zeta sont les termes entiers du niveau 1, ce qui permet
        de calculer le Digamma en arithmetique entiere EXACTE.
        """
        n = self.n if n is None else valider_n(n)
        res_int = self.calc_entiers.calculer(n)
        return res_int.termes_A, res_int.termes_B, res_int.somme_A, res_int.somme_B

    def generer_digamma_possibilities(self, res=None,
                                      n: Optional[int] = None) -> List[Dict]:
        """Genere les 4 possibilites Digamma (positions 8 et 7 de la suite A).

        Le parametre `res` (resultat geometrique) reste accepte pour
        compatibilite, mais le calcul s'effectue toujours sur les composantes
        zeta entieres exactes afin d'eviter toute erreur d'arrondi flottant.
        """
        n = self._resoudre_n(res, n)
        termes_A, _, somme_A, _ = self.composantes_zeta(n)
        if len(termes_A) < 8:
            return []

        facteur = self.facteur
        possibilites = []
        for position, signe in self.ordre:
            composante = termes_A[position - 1]
            possibilites.append({
                'position': position,
                'signe': signe,
                'composante_zeta': composante,
                'terme_geo': facteur * composante,
                'digamma_calcule': somme_A + signe * composante,
                'P_candidat': None,
                'est_premier': False,
                'description': (
                    f"{'+' if signe > 0 else '-'} position {position} "
                    f"(composante zeta = {composante})"
                ),
            })
        return possibilites

    def reconstruire_premier(self, res=None, verbose: bool = True,
                             n: Optional[int] = None
                             ) -> Tuple[Optional[int], List[Dict]]:
        """Tente de reconstruire le premier via les 4 Digamma geometriques.

        Les sommes geometriques valant exactement `facteur` fois les sommes
        entieres, le facteur s'annule dans (Somme_B - Digamma)/k^6 : le premier
        obtenu est donc exactement celui du niveau 1 (memes utilites).
        """
        n = self._resoudre_n(res, n)
        possibilites = self.generer_digamma_possibilities(n=n)
        # Reconstruction exacte (arithmetique entiere) sur les composantes zeta.
        _, _, somme_A_int, somme_B_int = self.composantes_zeta(n)
        resultats: List[Dict] = []
        premier_trouve: Optional[int] = None
        for poss in possibilites:
            numerateur = somme_B_int - poss['digamma_calcule']
            if numerateur % self.k_pow_6 == 0:
                P = numerateur // self.k_pow_6
                poss['P_candidat'] = P
                poss['est_premier'] = est_premier(P)
                if poss['est_premier'] and premier_trouve is None:
                    premier_trouve = P
            else:
                poss['P_candidat'] = Fraction(numerateur, self.k_pow_6)
                poss['est_premier'] = False
            resultats.append(poss)

            if verbose:
                tag = " PREMIER" if poss['est_premier'] else ""
                print(f"  Digamma [{poss['description']}]: "
                      f"digamma={poss['digamma_calcule']}, "
                      f"P={poss['P_candidat']}{tag}")

        return premier_trouve, resultats


class CalculateurNiveau2Geometrique:
    """Suites A et B geometriques : termes sqrt(a^2 + b^2).

    a1 = sqrt(1 + k^2) et r = k : les termes conservent la valeur numerique du
    terme entier correspondant du niveau 1, multipliee par le facteur
    sqrt(1 + k^2) (les deux composantes a et b etant en progression spectrale).

    EXEMPLE n=10 :
      Suite A : sqrt(1^2+t^2) + ... + sqrt((t^8-t^6)^2+(t^9-t^7)^2)
                + sqrt((t^9-t^7)^2+(t^10-t^8)^2)
      Suite B : idem avec le saut Zeta en position 6 et le decalage (+1).

    MEMES UTILITES QUE LE NIVEAU 1 (meme methode que le rapport 1/7) :
      positions 7 et 8 de la suite A : a1*k^6 et a1*k^7 -> 4 Digamma
      diviseur : 6eme position de la suite A zeta (k^6)
      Coefficient A = C/k^2    Coefficient B = C/k    C = k^4-k^2+1
      x = k*(k-1) (bloc A)     Reste A = k/(k-1)      (bloc B)
    """

    def __init__(self, k: Union[int, float]):
        k = int(k) if float(k) == int(k) else float(k)
        if k < 2:
            raise ValueError("k doit etre >= 2")
        self.k = k
        self.k_int = int(k)
        self.t = float(k)                        # base de la progression
        self.facteur = math.sqrt(1.0 + float(k) ** 2)
        self.C = self.k_int ** 4 - self.k_int ** 2 + 1
        self.m = self.k_int ** 6 - self.k_int ** 5 + 1
        self.x = self.k_int * (self.k_int - 1)
        self.coefficient_A = Fraction(self.C, self.k_int ** 2)
        self.coefficient_B = Fraction(self.C, self.k_int)
        self.reste_A = Fraction(self.k_int, self.k_int - 1)
        self.reste_B = Fraction(self.m * self.k_int, self.k_int - 1)
        self.digamma = MethodeDigammaGeometrique(self.k_int, n=10)

    def _calc_terme_geo(self, a: float, b: float) -> float:
        """Calcule sqrt(a^2 + b^2)."""
        return math.hypot(a, b)

    # --- generation des termes (section XI) --------------------------
    def generer_suite_A_termes(self, n: int) -> List[float]:
        n = valider_n(n)
        termes, _ = construire_termes_savard_geometrique(self.k_int, n)
        return termes

    def generer_suite_B_termes(self, n: int) -> List[float]:
        n = valider_n(n)
        _, termes = construire_termes_savard_geometrique(self.k_int, n)
        return termes

    def calculer(self, n: int = 10) -> ResultatNiveau2Geometrique:
        """Calcule les suites A et B geometriques pour n termes."""
        n = valider_n(n)
        termes_A = self.generer_suite_A_termes(n)
        termes_B = self.generer_suite_B_termes(n)
        return ResultatNiveau2Geometrique(
            k=self.k, n=n, t=self.t,
            somme_A=sum(termes_A), somme_B=sum(termes_B),
            termes_A=termes_A, termes_B=termes_B,
        )

    # --- ecart et coefficients (section XII) -------------------------
    def ecart_geo(self, n1: int = 10, n2: int = 9) -> float:
        """Ecart geometrique : (S_A(n1) - S_A(n2)) / k^6 = C*sqrt(1+k^2)."""
        n1 = valider_n(n1)
        n2 = valider_n(n2)
        return ((self.calculer(n1).somme_A - self.calculer(n2).somme_A)
                / self.k_int ** 6)

    def calculer_coefficients(self, n1: int = 10,
                              n2: int = 9) -> Tuple[Fraction, Fraction]:
        """Coefficients A et B du rapport 1/k (section XII).

        Coefficient A = (S_A(10) - S_A(9))/k^8 = C/k^2
        Coefficient B = (S_B(10) - S_B(9))/k^8 = C/k

        L'ecart geometrique (S_A(10)-S_A(9))/k^6 est verifie contre la forme
        fermee C*sqrt(1+k^2) : les deux niveaux partagent exactement la meme
        structure, au facteur geometrique sqrt(1+k^2) pres.
        """
        ecart = self.ecart_geo(n1, n2)
        attendu = self.C * self.facteur
        if abs(ecart - attendu) > 1e-6 * max(1.0, abs(attendu)):
            raise ArithmeticError(
                f"Incoherence niveau 2 (k={self.k}) : ecart={ecart} != "
                f"C*sqrt(1+k^2)={attendu}"
            )
        return self.coefficient_A, self.coefficient_B

    def reconstruire_equations_generales(self, verbose: bool = False,
                                         n1: int = 10, n2: int = 9) -> Dict[str, Any]:
        """Reconstruit les equations generalisees (n > 0) des suites A et B.

        (Coefficient)/((Somme)/k^10) = Reste + x -> bloc A = partie entiere (x),
        bloc B = partie decimale (< 1). L'equation reconstruite est ensuite
        generalisee pour tout n entier strictement positif :

            (Coefficient A / x) * k^n - Reste A = Somme suite A
            (Coefficient B / x) * k^n - Reste B = Somme suite B
        """
        k = self.k_int
        res: Dict[str, Any] = {
            'k': self.k, 't': self.t,
            'facteur_geometrique': self.facteur,
            'coefficient_A': self.coefficient_A,
            'coefficient_B': self.coefficient_B,
            'coefficient_A_geo': self.coefficient_A * self.facteur,
            'coefficient_B_geo': self.coefficient_B * self.facteur,
            'C': self.C, 'm': self.m, 'x': self.x,
            'ecart_A_geo': self.ecart_geo(n1, n2),
        }

        for nom, coeff, reste in (('A', self.coefficient_A, self.reste_A),
                                  ('B', self.coefficient_B, self.reste_B)):
            r_n1 = self.calculer(n1)
            somme_n1 = r_n1.somme_A if nom == 'A' else r_n1.somme_B
            # (Reste + x) = Coefficient / (Somme / k^n1) -> blocs A et B
            reste_plus_x = (coeff * k ** n1) / Fraction(somme_n1)
            x_calcul = int(reste_plus_x)          # bloc A : partie entiere
            bloc_B = reste_plus_x - x_calcul      # bloc B : partie < 1
            res[f'x_{nom}'] = x_calcul
            res[f'reste_plus_x_{nom}'] = reste_plus_x
            res[f'bloc_B_{nom}'] = bloc_B
            res[f'reste_{nom}'] = reste
            res[f'equation_{nom}_positif'] = (
                f"({coeff}/{self.x} * {k}^n) - {reste} = Somme suite {nom} (n > 0)"
            )
            res[f'equation_{nom}_negatif'] = (
                f"{coeff} * {k}^(-n) - {reste} = Somme suite {nom} (n < 0)"
            )
            if verbose:
                print(f"\n  === Suite {nom} (niveau 2 geometrique) ===")
                print(f"  Coefficient {nom} = {coeff} = {float(coeff):.10f}")
                print(f"  (Coefficient/(Somme/k^{n1})) = Reste + x = {float(reste_plus_x):.10f}")
                print(f"  Bloc A (partie entiere) : x = {x_calcul} (theorique : {self.x})")
                print(f"  Bloc B (partie decimale) : {float(bloc_B):.12f}")
                print(f"  Reste {nom} = {reste}")
                print(f"  Equation ({nom}) n > 0 : {res[f'equation_{nom}_positif']}")

        return res

    # --- reconstruction du premier (meme methode que le niveau 1) -----
    def reconstruire_premier(self, n: int = 10, verbose: bool = True
                             ) -> Tuple[Optional[int], List[Dict]]:
        """Reconstruit le premier au niveau 2 geometrique (4 Digamma)."""
        n = valider_n(n)
        res = self.calculer(n)
        return self.digamma.reconstruire_premier(res, verbose=verbose)

    # NB : les methodes ecart_geo / calculer_coefficients /
    # reconstruire_equations_generales / reconstruire_premier sont definies
    # ci-dessus (une seule implementation, aucune duplication).

# ============================================================
# PIPELINE NIVEAU 2 - COORDINATION DES DEUX NIVEAUX
# ============================================================

class PipelineNiveau2Geometrique:
    """Pipeline cognitif niveau 2 : geometrique (sqrt(a^2+b^2)) + spectral.

    Applique aux DEUX niveaux exactement la meme methode generalisee que le
    rapport 1/7 :

      niveau 1 (entiers)      : suites A/B k^i, 4 Digamma, P, coefficients
      niveau 2 (geometriques) : suites A/B sqrt(a^2+b^2) (meme regle avec
                                a1 = sqrt(1+k^2) et r = k), 4 Digamma
                                geometriques, P, coefficients et equations

    Les suites geometriques conservent les MEMES UTILITES que les suites
    entieres : positions 7 et 8 pour le Digamma, 6eme position zeta comme
    diviseur, coefficients C/k^2 et C/k, x = k*(k-1), Reste k/(k-1).
    """

    def __init__(self, k: Union[int, float] = 2):
        k = int(k) if float(k) == int(k) else float(k)
        self.k = k
        self.k_int = int(k)
        self.calc_geo = CalculateurNiveau2Geometrique(k=k)
        self.calc_entiers = CalculateurNiveau1Entiers(k=self.k_int)
        self.methode_entiers = MethodeDigamma(k=self.k_int)

    def calculer_tout(self, n: int = 10, verbose: bool = True) -> Dict[str, Any]:
        """Calcule tout le pipeline niveau 2 pour un n donne."""
        n = valider_n(n)
        if verbose:
            print(f"\n{'=' * 70}")
            print(f"  PIPELINE COGNITIF NIVEAU 2 - k = 1/{self.k}, n = {n}")
            print(f"{'=' * 70}")

        # --- niveau 1 : suites entieres + 4 Digamma ------------------
        res_entiers = self.calc_entiers.calculer(n=n)
        premier_n1, cands_n1 = self.methode_entiers.reconstruire_premier(
            res_entiers.somme_A, res_entiers.somme_B, verbose=verbose
        )

        # --- niveau 2 : suites geometriques + 4 Digamma --------------
        res_geo = self.calc_geo.calculer(n=n)
        if verbose:
            print(f"\n  Suite A (geometrique) : Somme = {res_geo.somme_A:.6f}")
            print(f"  Suite B (geometrique) : Somme = {res_geo.somme_B:.6f}")
        premier_n2, cands_n2 = self.calc_geo.reconstruire_premier(
            n=n, verbose=verbose
        )

        # --- coefficients et equations (niveau 2) --------------------
        equations = self.calc_geo.reconstruire_equations_generales(
            verbose=verbose, n1=10, n2=9
        )

        resultat: Dict[str, Any] = {
            'n': n, 'k': self.k,
            'typique': self.k == 2,
            'somme_A_geo': res_geo.somme_A,
            'somme_B_geo': res_geo.somme_B,
            'terme_7_A': res_geo.termes_A[6] if len(res_geo.termes_A) >= 7 else None,
            'terme_8_A': res_geo.termes_A[7] if len(res_geo.termes_A) >= 8 else None,
            'diviseur_zeta_6e_position': self.k_int ** 6,
            'somme_A_entiers': res_entiers.somme_A,
            'somme_B_entiers': res_entiers.somme_B,
            'coefficient_A': self.calc_geo.coefficient_A,
            'coefficient_B': self.calc_geo.coefficient_B,
            'x': self.calc_geo.x,
            'reste_A': self.calc_geo.reste_A,
            'reste_B': self.calc_geo.reste_B,
            'equations': equations,
            'premier_niveau_1': premier_n1,
            'premier_niveau_2': premier_n2,
            'premier_reconstruit': premier_n2 if premier_n2 else premier_n1,
            'candidats_digamma_entiers': cands_n1,
            'candidats_digamma_geometriques': cands_n2,
        }

        if verbose:
            print(f"\n{'=' * 70}")
            print(f"  Premier reconstruit (niveau 2) : {premier_n2}")
            print(f"  Premier reconstruit (niveau 1) : {premier_n1}")
            print(f"{'=' * 70}")

        return resultat

    def rapport_complet(self, n: int = 10) -> str:
        """Rapport complet niveau 2 (n entier strictement positif)."""
        n = valider_n(n)
        data = self.calculer_tout(n=n, verbose=False)
        geo = self.calc_geo
        lignes = [
            "=" * 70,
            f"  RAPPORT NIVEAU 2 - RAPPORT NON TYPIQUE 1/k = 1/{self.k} (n={n})",
            "=" * 70,
            "",
            f"  Suite A (geometrique) = {data['somme_A_geo']:.6f}",
            f"  Suite B (geometrique) = {data['somme_B_geo']:.6f}",
            f"  7eme position suite A = {data['terme_7_A']}",
            f"  8eme position suite A = {data['terme_8_A']}",
            f"  6eme position zeta (diviseur) = k^6 = {data['diviseur_zeta_6e_position']}",
            "",
            f"  Digamma calcule (- 8eme position) = "
            f"{data['somme_A_geo'] - (data['terme_8_A'] or 0):.6f}",
            f"  P = (Somme B - Digamma) / k^6 = {data['premier_niveau_2']}",
            "",
            f"  Coefficient A = {geo.coefficient_A} = C/k^2  (C = k^4-k^2+1 = {geo.C})",
            f"  Coefficient B = {geo.coefficient_B} = C/k",
            f"  x (bloc A) = {geo.x}     Reste A (bloc B) = {geo.reste_A}",
            f"  Reste B = {geo.reste_B} = m * Reste A  (m = k^6-k^5+1 = {geo.m})",
            "",
            f"  Equation A (n>0) : {data['equations']['equation_A_positif']}",
            f"  Equation B (n>0) : {data['equations']['equation_B_positif']}",
        ]
        rapport = "\n".join(lignes)
        print(rapport)
        return rapport


# ============================================================
# DEMO / TEST AUTONOME
# ============================================================

#: Reference a n=10 pour chaque rapport non typique 1/k (section XII).
PREMIERS_REFERENCE = {2: 29, 3: 227, 5: 2999, 6: 7529, 7: 16519}


def demo():
    """Niveaux 1 et 2 : reconstruction du premier a n=10, pour chaque 1/k."""
    print("=" * 78)
    print("  PIPELINE COGNITIF GABRIEL v7.5 - NIVEAUX 1 ET 2 (n entier > 0)")
    print("=" * 78)

    print("\n  --- NIVEAU 1 (entiers, 4 Digamma sur k^7 et k^8) ---")
    for k, attendu in PREMIERS_REFERENCE.items():
        calc = CalculateurNiveau1Entiers(k=k)
        r10 = calc.calculer(10)
        r9 = calc.calculer(9)
        P, _ = MethodeDigamma(k=k, n=10).reconstruire_premier(
            r10.somme_A, r10.somme_B, verbose=False)
        eq = calc.equations_generalisees()
        statut = "OK" if P == attendu else "ECHEC"
        print(f"    [{statut}] k=1/{k} : S_A(10)={r10.somme_A}, S_B(10)={r10.somme_B} "
              f"-> P={P} (attendu {attendu})")
        print(f"           C={calc.C}, CoeffA={calc.coefficient_A}, "
              f"CoeffB={calc.coefficient_B}, x={calc.x}")
        print(f"           S_A(9)={r9.somme_A}, S_B(9)={r9.somme_B}")
        print(f"           {eq['equation_A_positif']}")
        print(f"           {eq['equation_B_positif']}")

    print("\n  --- NIVEAU 2 (geometriques sqrt(a^2+b^2), memes utilites) ---")
    for k, attendu in PREMIERS_REFERENCE.items():
        calc = CalculateurNiveau2Geometrique(k=k)
        r10 = calc.calculer(10)
        P, cands = calc.reconstruire_premier(n=10, verbose=False)
        statut = "OK" if P == attendu else "ECHEC"
        print(f"    [{statut}] k=1/{k} : facteur=sqrt(1+k^2)={calc.facteur:.10f}")
        print(f"           S_A(10)={r10.somme_A:.6f} = facteur * {r10.somme_A / calc.facteur:.6f}")
        print(f"           S_B(10)={r10.somme_B:.6f} = facteur * {r10.somme_B / calc.facteur:.6f}")
        print(f"           ecart (S_A10-S_A9)/k^6 = {calc.ecart_geo():.6f} "
              f"(= C*sqrt(1+k^2) = {calc.C * calc.facteur:.6f})")
        print(f"           C={calc.C}, CoeffA={calc.coefficient_A}, "
              f"CoeffB={calc.coefficient_B}, x={calc.x}, ResteA={calc.reste_A}")
        for c in cands:
            tag = " PREMIER" if c['est_premier'] else ""
            print(f"           Digamma [{c['description']}] -> P={c['P_candidat']}{tag}")

    print("\n  --- RAPPORT COMPLET 1/7 (niveau 2) ---")
    PipelineNiveau2Geometrique(k=7).rapport_complet(n=10)

    print("\n  --- GARDE-FOU n (entier strictement positif) ---")
    for mauvais in (0, -1, 2.5):
        try:
            valider_n(mauvais)
            print(f"    ECHEC : n={mauvais} aurait du etre rejete")
        except ValueError as exc:
            print(f"    OK : n={mauvais} rejete ({exc})")


if __name__ == "__main__":
    import sys as _sys
    import io as _io
    try:
        _sys.stdout = _io.TextIOWrapper(_sys.stdout.buffer, encoding="utf-8",
                                       errors="replace")
    except Exception:
        pass
    demo()

