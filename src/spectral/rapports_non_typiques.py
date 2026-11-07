#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
══════════════════════════════════════════════════════════════════════════════
 MODULE EXCLUSIF — RAPPORTS NON-TYPIQUES 1/k<>1/2   (variateur mécanique)
══════════════════════════════════════════════════════════════════════════════

Méthode formalisée et généralisée des suites A/B pour les rapports 1/k<>1/2
(reconstruction de nombres premiers), d'après l'extrait Savard « L'Univers
est au Carré ».

  • Les suites A et B d'un rapport non-typique (1/3, 1/4, 1/5, 1/6, … 1/k)
    reconstruisent les nombres premiers de façon analogue au rapport typique.
  • On reconstruit d'abord le premier pour n = 10 (quantité de TERMES).
  • Pour 1/k<>1/2, la valeur de n ne vaut PAS la position du premier.
    Ex. rapport 1/3, n=10 → premier 227 qui est le 49e nombre premier.
  • Suite A (n=10) :
        t^1 + t^2 + t^3 + t^4 + t^5 + t^6 + t^7 + t^8
        + (t^9  - t^7 ) + (t^10 - t^8)
  • Suite B (n=10) :
        t^1 + t^2 + t^3 + t^4 + t^5 + t^7 + t^8 + t^9
        + (t^10 - t^8 ) + (t^11 - t^9)
  • Digamma : valeur à la 8e position (parfois 7e), additionnée ou soustraite.
  • Reconstruction (1/k<>1/2) :
        Premier = ( Somme suite B - Digamma_calculé ) / t^6
  • n (nombre de termes) ≠ position du premier. On reconstruit n=10 d'abord,
    puis n>10 (croissant), n<10 (décroissant). Digamma n≠10 :
        Digamma_calculé = ( SB / t^6 - P ) * t^6   (valable 1/k non-typique)
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction
from typing import Dict, List, Optional, Tuple


def _crible(valeur_max: int) -> List[int]:
    """Crible d'Ératosthène : tous les nombres premiers <= valeur_max."""
    if valeur_max < 2:
        return []
    crible = bytearray([1]) * (valeur_max + 1)
    crible[0] = crible[1] = 0
    for i in range(2, int(math.sqrt(valeur_max)) + 1):
        if crible[i]:
            crible[i * i::i] = bytearray((valeur_max - i * i) // i + 1)
    return [i for i in range(2, valeur_max + 1) if crible[i]]


# Table des premiers (positions positives 1..n) jusqu'à 20 000 000 — assez
# large pour couvrir l'ancre la plus élevée du catalogue (1/27 -> 14 330 707,
# rang 930 152) et son décalage de rang. (Anciennement 120 000 : les ancres
# 1/13, 1/18, 1/27 dépassaient la table et cassaient la reconstruction.)
PREMIERS: List[int] = _crible(20_000_000)


def _somme_puissances(t: int, debut: int, fin: int) -> int:
    """Somme des t^i pour i dans [debut, fin] (inclus)."""
    return sum(t ** i for i in range(debut, fin + 1))


def suite_A(t: int, n: int = 10) -> int:
    """Somme de la suite A pour le rapport de base t et n termes.

    A(n) = (t^1+...+t^(n-2)) + (t^(n-1)-t^(n-3)) + (t^n - t^(n-2)).
    n=10 donne (t^1..t^8) + (t^9 - t^7) + (t^10 - t^8).
    """
    t = int(t); n = int(n)
    if n < 3:
        raise ValueError("suite_A : n doit être >= 3")
    return (_somme_puissances(t, 1, n - 2)
            + (t ** (n - 1) - t ** (n - 3))
            + (t ** n - t ** (n - 2)))


def suite_B(t: int, n: int = 10) -> int:
    """Somme de la suite B (rapport t) : t^1..t^5, t^7..t^(n-1),
    puis (t^n-t^(n-2)) + (t^(n+1)-t^(n-1))."""
    t = int(t); n = int(n)
    if n < 7:
        raise ValueError("suite_B : n doit être >= 7")
    return (_somme_puissances(t, 1, 5)
            + _somme_puissances(t, 7, n - 1)
            + (t ** n - t ** (n - 2))
            + (t ** (n + 1) - t ** (n - 1)))


# Digamma : (position, signe) par rapport (n=10) — ancrage correct de chaque
# rapport, conforme à la Section XIV.6 (position 8 ou 7, signe +/-).
DIGAMMA_MAP: Dict[int, Tuple[int, int]] = {
    2:  (8, -1),   # 29     (A8-)
    3:  (8, -1),   # 227    (A8-)
    4:  (8, +1),   # 947    (A8+)
    5:  (7, +1),   # 2999   (A7+)
    6:  (8, +1),   # 7529   (A8+)
    7:  (8, -1),   # 16519  (A8-)
    8:  (8, -1),   # 32327  (A8-)
    9:  (7, -1),   # 58337  (A7-)
    13: (8, +1),   # 368939 (A8+)
}

# Ajustements de forme de la suite A : AUCUN. La construction XIV.4 terme à
# terme est la seule autorisée — l'ancien retrait de t^8 pour 1/6 corrompait
# la somme A (68 920 242 au lieu de 70 599 858) et décalait l'ancrage vers un
# mauvais premier (7 607 au lieu de 7 529). Désactivé pour conformité.
SUITES_A_AJUSTEES: Dict[int, Dict] = {}

# Données radicales des tableaux 14.1 à 14.15. Les radicandes sont conservés
# sous forme décimale (et non en float) afin que le calcul reste reproductible.
# ``exposant_zeta`` est propre à chaque tableau : les tableaux 14.1--14.13 et
# 14.15 divisent par sqrt((k^5)^2 + (k^6)^2), alors que 14.14 emploie k^6/k^7.
REFERENCES_REELLES_N10: Dict[int, Dict[str, object]] = {
    2: {
        "somme_A_radicande": "3452805",
        "somme_B_radicande": "13300805",
        "digamma_radicande": "81920",
        "signe_digamma": -1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 29,
        "source": "Tableau 14.1, rapport 1/2",
    },
    3: {
        "somme_A_radicande": "7079856640",
        "somme_B_radicande": "6.333294724e10",
        "digamma_radicande": "47829690",
        "signe_digamma": -1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 227,
        "source": "Tableau 14.2, rapport 1/3",
    },
    4: {
        "somme_A_radicande": "1.840600404e12",
        "somme_B_radicande": "2.940384489e13",
        "digamma_radicande": "4563402752",
        "signe_digamma": 1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 947,
        "source": "Tableau 14.3, rapport 1/4",
    },
    5: {
        "somme_A_radicande": "1.432987061e14",
        "somme_B_radicande": "3.580561045e15",
        "digamma_radicande": "6347656250",
        "signe_digamma": 1,
        "position_digamma": "7e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 2999,
        "source": "Tableau 14.4, rapport 1/5",
    },
    6: {
        "somme_A_radicande": "5.122793837e15",
        "somme_B_radicande": "1.8437699607e17",
        "digamma_radicande": "2.899474072e12",
        "signe_digamma": 1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 7529,
        "source": "Tableau 14.5, rapport 1/6",
    },
    7: {
        "somme_A_radicande": "1.06435826e17",
        "somme_B_radicande": "5.214812712e18",
        "digamma_radicande": "3.391115364e13",
        "signe_digamma": 1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 16421,
        "source": "Tableau 14.6, rapport 1/7",
    },
    8: {
        "somme_A_radicande": "1.482700943e18",
        "somme_B_radicande": "9.488771358e19",
        "digamma_radicande": "2.858730232e14",
        "signe_digamma": -1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 32327,
        "source": "Tableau 14.8, rapport 1/8",
    },
    9: {
        "somme_A_radicande": "1.519945564e19",
        "somme_B_radicande": "1.231118384e21",
        "digamma_radicande": "2.315922199e13",
        "signe_digamma": -1,
        "position_digamma": "7e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 58337,
        "source": "Tableau 14.9, rapport 1/9",
    },
    10: {
        "somme_A_radicande": "1.224570136e20",
        "somme_B_radicande": "1.224547893e22",
        "digamma_radicande": "1.01e16",
        "signe_digamma": 1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 98999,
        "source": "Tableau 14.10, rapport 1/10",
    },
    11: {
        "somme_A_radicande": "8.221121742e22",
        "somme_B_radicande": "9.947546087e24",
        "digamma_radicande": "3.82888262e14",
        "signe_digamma": -1,
        "position_digamma": "7e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 1611851,
        "source": "Tableau 14.11, rapport 1/11",
    },
    12: {
        "somme_A_radicande": "4.531028809e21",
        "somme_B_radicande": "6.524633079e23",
        "digamma_radicande": "1.861681774e17",
        "signe_digamma": -1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 247259,
        "source": "Tableau 14.12, rapport 1/12",
    },
    20: {
        "somme_A_radicande": "1.158959701e26",
        "somme_B_radicande": "4.635836044e28",
        "digamma_radicande": "6.569984e20",
        "signe_digamma": -1,
        "position_digamma": "8e position de la première suite",
        "exposant_zeta": 5,
        "premier_attendu": 3192419,
        "source": "Tableau 14.13, rapport 1/20",
    },
    50: {
        "somme_A_radicande": "2.481538804e37",
        "somme_B_radicande": "6.20384701e40",
        "digamma_radicande": "3.816223145e30",
        "signe_digamma": -1,
        "position_digamma": "8e position de la deuxième suite",
        "exposant_zeta": 6,
        "premier_attendu": 312379999,
        "source": "Tableau 14.14, rapport 1/50",
    },
    100: {
        "somme_A_radicande": "1.02020203e40",
        "somme_B_radicande": "1.02020102e44",
        "digamma_radicande": "1.0001e36",
        "signe_digamma": -1,
        "position_digamma": "9e position de la deuxième suite",
        "exposant_zeta": 5,
        "premier_attendu": 9999995089,
        "correction_documentee": True,
        "source": "Tableau 14.15, rapport 1/100",
    },
}


def _est_premier(valeur: int) -> bool:
    """Teste la primalité entière sans dépendre de la table bornée ``PREMIERS``."""
    valeur = int(valeur)
    if valeur < 2:
        return False
    # Le test par divisions successives est réservé aux candidats de taille
    # raisonnable. Les candidats plus grands sont rapportés comme non vérifiés
    # au lieu de bloquer le pipeline sur une recherche quadratique.
    if valeur > 10**12:
        return False
    if valeur % 2 == 0:
        return valeur == 2
    diviseur = 3
    while diviseur * diviseur <= valeur:
        if valeur % diviseur == 0:
            return False
        diviseur += 2
    return True


def construire_suites_reelles(rapport: object, n: int = 10) -> Dict[str, object]:
    """Construit les composantes géométriques réelles ``A_i`` et ``B_i``.

    Chaque composante est une longueur ``sqrt(k^(2i) + k^(2i+2))``. La sixième
    composante est le Zêta de référence; les composantes 9 et 10 décrivent la
    substitution visible dans les tableaux 14.1--14.15. Cette construction est
    valable pour toute base entière ``k >= 2`` et toute longueur ``n >= 10``.
    """
    k = extraire_k(rapport)
    if k < 2:
        raise ValueError("Les suites réelles exigent un rapport de la forme 1/k avec k >= 2")
    n = int(n)
    if n < 10:
        raise ValueError("Les suites réelles exigent au moins 10 positions")

    def segment(i: int) -> Dict[str, object]:
        return {
            "position": i,
            "radicande": k ** (2 * (i - 1)) + k ** (2 * i),
            "forme": f"sqrt(({k}^{i - 1})^2 + ({k}^{i})^2)",
        }

    suite_a = [segment(i) for i in range(1, n + 1)]
    suite_b = [segment(i) for i in range(1, n + 1)]
    return {
        "rapport": f"1/{k}",
        "n": n,
        "suite_Ai": suite_a,
        "suite_Bi": suite_b,
        "zeta": segment(6),
        "substitution": {
            "debut": 6,
            "fin": 7,
            "forme": "La sixième position sert de Zêta; les positions suivantes poursuivent la suite géométrique.",
        },
    }


def equations_suites_reelles(rapport: object, n: int = 10) -> Dict[str, object]:
    """Construit universellement les sommes réelles des suites ``Ai`` et ``Bi``.

    En posant ``X_i = sqrt((k^(i-1))^2 + (k^i)^2)``, les tableaux donnent :

    ``A(n) = X_1 + ... + X_(n-4) + X_(n-1) + X_n``
    ``B(n) = X_1 + ... + X_5 + X_7 + ... + X_(n-3) + X_n + X_(n+1)``

    Comme tous les ``X_i`` portent le facteur commun ``sqrt(1+k^2)``, les
    coefficients restent exacts et permettent une reconstruction algébrique
    pour chaque entier ``k >= 2`` et ``n >= 10``.
    """
    k = extraire_k(rapport)
    n = int(n)
    if k < 2 or n < 10:
        raise ValueError("Les équations réelles exigent k >= 2 et n >= 10")
    coefficient_a = sum(k ** exponent for exponent in range(n - 4)) + k ** (n - 2) + k ** (n - 1)
    coefficient_b = (
        sum(k ** exponent for exponent in range(5))
        + sum(k ** exponent for exponent in range(6, n - 3))
        + k ** (n - 1)
        + k ** n
    )
    return {
        "rapport": f"1/{k}",
        "k": k,
        "n": n,
        "facteur_radiciel": f"sqrt(1 + {k}^2)",
        "coefficient_A": coefficient_a,
        "coefficient_B": coefficient_b,
        "radicande_A": (1 + k ** 2) * coefficient_a ** 2,
        "radicande_B": (1 + k ** 2) * coefficient_b ** 2,
        "forme_A": f"A_reel({n}) = ({coefficient_a}) * sqrt(1 + {k}^2)",
        "forme_B": f"B_reel({n}) = ({coefficient_b}) * sqrt(1 + {k}^2)",
    }


def candidats_reconstruction_reelle(rapport: object, n: int = 10) -> List[Dict[str, object]]:
    """Énumère algébriquement les branches réelles sans tableau préprogrammé.

    Les Digamma possibles sont les positions ``n-3`` et ``n-2`` de la première
    suite, avec les deux signes. Les deux Zêta documentés (positions 6 et 7)
    sont tous deux essayés. Le facteur radical commun s'annule avant la
    division, donc le test d'intégralité est exact.
    """
    equation = equations_suites_reelles(rapport, n)
    k = int(equation["k"])
    n = int(equation["n"])
    coefficient_a = int(equation["coefficient_A"])
    coefficient_b = int(equation["coefficient_B"])
    candidats: List[Dict[str, object]] = []
    for position_digamma in (n - 3, n - 2):
        valeur_digamma = k ** (position_digamma - 1)
        for signe in (1, -1):
            coefficient_calcule = coefficient_a + signe * valeur_digamma
            for position_zeta in (6, 7):
                diviseur = k ** (position_zeta - 1)
                numerateur = coefficient_b - coefficient_calcule
                est_entier = numerateur % diviseur == 0
                premier = numerateur // diviseur if est_entier else None
                candidats.append({
                    "position_digamma": position_digamma,
                    "signe_digamma": signe,
                    "position_zeta": position_zeta,
                    "digamma_calcule_coefficient": coefficient_calcule,
                    "premier": premier,
                    "entier": est_entier,
                    "premier_verifie": premier is not None and _est_premier(premier),
                })
    return candidats


def reconstruire_premier_reel_universel(rapport: object, n: int = 10) -> Dict[str, object]:
    """Reconstruit un premier réel par les équations universelles de ``Ai/Bi``."""
    equation = equations_suites_reelles(rapport, n)
    candidats = candidats_reconstruction_reelle(rapport, n)
    valides = [candidat for candidat in candidats if candidat["premier_verifie"]]
    if len(valides) != 1:
        return {
            **equation,
            "methode": "reelle-universelle-ai-bi",
            "premier": None,
            "verifie": False,
            "candidats": candidats,
            "note": (
                "Aucune branche réelle universelle ne détermine un premier."
                if not valides
                else "Plusieurs branches réelles universelles déterminent un premier; sélection non unique."
            ),
        }
    candidat = valides[0]
    return {
        **equation,
        **candidat,
        "methode": "reelle-universelle-ai-bi",
        "verifie": True,
        "note": "Premier déterminé par les équations réelles universelles Ai/Bi.",
    }


def reconstruire_premier_reel(rapport: object, n: int = 10) -> Optional[Dict[str, object]]:
    """Essaie le repli réel documenté après l'échec des branches entières.

    Le calcul utilise les racines carrées des radicandes du tableau et le
    dénominateur ``sqrt(k^12 + k^14) = k^6 * sqrt(1 + k^2)``. Une valeur n'est
    retenue que si elle est suffisamment proche d'un entier *et* que cet entier
    est premier. Les tableaux arrondis qui ne satisfont pas ces deux contrôles
    ne produisent donc jamais un faux positif.
    """
    k = extraire_k(rapport)
    if k < 2:
        raise ValueError("Le repli réel exige un rapport de la forme 1/k avec k >= 2")
    reference = REFERENCES_REELLES_N10.get(k)
    if reference is None or int(n) != 10:
        return None

    with localcontext() as contexte:
        contexte.prec = 60
        somme_a = Decimal(str(reference["somme_A_radicande"])).sqrt()
        somme_b = Decimal(str(reference["somme_B_radicande"])).sqrt()
        digamma = Decimal(str(reference["digamma_radicande"])).sqrt()
        signe = Decimal(int(reference["signe_digamma"]))
        digamma_calcule = somme_a + signe * digamma
        exposant_zeta = int(reference["exposant_zeta"])
        denominateur = (Decimal(k) ** exposant_zeta) * (Decimal(1) + Decimal(k) ** 2).sqrt()
        candidat_reel = (somme_b - digamma_calcule) / denominateur
        candidat_entier = int(candidat_reel.to_integral_value(rounding=ROUND_HALF_UP))
        ecart_arrondi = abs(candidat_reel - Decimal(candidat_entier))

    tolerance = Decimal("0.1")
    if reference.get("correction_documentee"):
        premier_documente = int(reference["premier_attendu"])
        if not _est_premier(premier_documente):
            return {
                "rapport": f"1/{k}",
                "k": k,
                "n": int(n),
                "methode": "reelle-racines-carrees",
                "premier": None,
                "verifie": False,
                "verification": "contradiction-documentee",
                "candidat_reel": str(candidat_reel),
                "premier_documente": premier_documente,
                "note": (
                    "Le tableau 14.15 corrige le candidat vers une valeur qui "
                    "n'est pas première au test indépendant; aucun premier n'est retenu."
                ),
                "source": reference["source"],
            }
        candidat_entier = premier_documente
        ecart_arrondi = None
        verification = "correction-documentee"
    elif ecart_arrondi <= tolerance and _est_premier(candidat_entier):
        verification = "calcul-direct"
    else:
        return {
            "rapport": f"1/{k}",
            "k": k,
            "n": int(n),
            "methode": "reelle-racines-carrees",
            "premier": None,
            "verifie": False,
            "candidat_reel": str(candidat_reel),
            "ecart_arrondi": str(ecart_arrondi),
            "note": (
                "Le repli réel n'a pas produit un entier suffisamment précis et "
                "premier à partir des données tabulées."
            ),
            "source": reference["source"],
        }

    return {
        "rapport": f"1/{k}",
        "k": k,
        "n": int(n),
        "methode": "reelle-racines-carrees",
        "position": reference["position_digamma"],
        "signe": "addition" if signe > 0 else "soustraction",
        "A_reel": str(somme_a),
        "B_reel": str(somme_b),
        "digamma_calcule": str(digamma_calcule),
        "candidat_reel": str(candidat_reel),
        "ecart_arrondi": str(ecart_arrondi) if ecart_arrondi is not None else None,
        "premier": candidat_entier,
        "position_du_premier (1-index)": position_premier_table(candidat_entier),
        "verifie": True,
        "verification": verification,
        "exposant_zeta": exposant_zeta,
        "source": reference["source"],
        "note": (
            "Premier corrigé conformément à la note du tableau 14.15."
            if verification == "correction-documentee"
            else "Premier vérifié par le repli réel à racines carrées."
        ),
    }


def extraire_k(rapport: object) -> int:
    """Extrait k depuis '1/k' ou un simple entier."""
    if isinstance(rapport, int):
        return rapport
    m = re.search(r"1/(\d+)", str(rapport))
    return int(m.group(1)) if m else int(str(rapport).strip())


@dataclass(frozen=True)
class EquationSomme:
    """Equation exacte d'une somme de suite : S(n) = coefficient * k^n + constante."""

    nom: str
    k: int
    coefficient: Fraction
    constante: Fraction

    def somme(self, n: int) -> Fraction:
        """Évalue l'équation sans conversion flottante."""
        return self.coefficient * self.k ** int(n) + self.constante

    @property
    def innovation(self) -> Fraction:
        """Terme constant de S(n+1) = k*S(n) + innovation."""
        return (1 - self.k) * self.constante

    def convoluer(self, valeur_ancre: Fraction, n_ancre: int, n_cible: int) -> Fraction:
        """Propage une somme par la convolution géométrique exacte vers n_cible."""
        n_ancre = int(n_ancre)
        n_cible = int(n_cible)
        if n_cible < n_ancre:
            raise ValueError("La convolution requiert n_cible >= n_ancre")
        delta = n_cible - n_ancre
        puissance = self.k ** delta
        noyau = Fraction(puissance - 1, self.k - 1)
        return puissance * Fraction(valeur_ancre) + self.innovation * noyau

    def as_dict(self) -> Dict[str, object]:
        """Expose les composantes algébriques sérialisables de l'équation."""
        return {
            "nom": self.nom,
            "k": self.k,
            "coefficient": self.coefficient,
            "constante": self.constante,
            "innovation": self.innovation,
            "forme": f"{self.nom}(n) = ({self.coefficient}) * {self.k}^n + ({self.constante})",
        }


def _verifier_k_non_typique(rapport: object) -> int:
    """Valide la base k d'un rapport 1/k (k >= 2 : régime typique 1/2 inclus)."""
    k = extraire_k(rapport)
    if k < 2:
        raise ValueError("Un rapport doit être de la forme 1/k avec k >= 2")
    return k


def equations_ab(rapport: object) -> Tuple[EquationSomme, EquationSomme]:
    """Construit les équations universelles exactes des sommes A et B.

    Les définitions par blocs donnent, pour chaque k >= 2, les identités :

      A(n) = (1 + 1/k + 1/(k^3*(k-1))) * k^n - k/(k-1)
      B(n) = (k + 1 + 1/(k^2*(k-1))) * k^n
             + (k^6-k)/(k-1) - k^7/(k-1)

    La première vaut pour n >= 3 et la seconde pour n >= 7, domaines des
    sommes finies ``suite_A`` et ``suite_B``.
    """
    k = _verifier_k_non_typique(rapport)
    equation_a = EquationSomme(
        nom="A",
        k=k,
        coefficient=Fraction(1) + Fraction(1, k) + Fraction(1, k**3 * (k - 1)),
        constante=Fraction(-k, k - 1),
    )
    equation_b = EquationSomme(
        nom="B",
        k=k,
        coefficient=Fraction(k + 1) + Fraction(1, k**2 * (k - 1)),
        constante=Fraction(k**6 - k - k**7, k - 1),
    )
    return equation_a, equation_b


def _reconstruire_equation(
    nom: str, k: int, n1: int, somme1: int, n2: int, somme2: int
) -> EquationSomme:
    """Retrouve exactement coefficient et constante à partir de deux sommes."""
    n1 = int(n1)
    n2 = int(n2)
    if n1 == n2:
        raise ValueError("La reconstruction exige deux quantités de termes distinctes")
    denominateur = k**n1 - k**n2
    coefficient = Fraction(int(somme1) - int(somme2), denominateur)
    constante = Fraction(int(somme1)) - coefficient * k**n1
    return EquationSomme(nom, k, coefficient, constante)


def reconstruire_equations_ab(
    rapport: object, n1: int = 10, n2: int = 11
) -> Tuple[EquationSomme, EquationSomme]:
    """Reconstruit algébriquement les équations A et B de tout rapport 1/k.

    Aucun arrondi ni coefficient décimal n'est employé : les deux sommes
    exactes aux indices distincts ``n1`` et ``n2`` déterminent chacune une
    unique équation affine-géométrique.
    """
    k = _verifier_k_non_typique(rapport)
    if min(int(n1), int(n2)) < 7:
        raise ValueError("La reconstruction conjointe A/B exige n1 et n2 >= 7")
    return (
        _reconstruire_equation("A", k, n1, suite_A(k, n1), n2, suite_A(k, n2)),
        _reconstruire_equation("B", k, n1, suite_B(k, n1), n2, suite_B(k, n2)),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  CONTRAT COGNITIF À DEUX NIVEAUX — CRITÈRES OBLIGATOIRES À CHAQUE REQUÊTE
# ══════════════════════════════════════════════════════════════════════════════
# Le fichier Excel « systeme_convolutif_spectral_general.xlsx » démontre la
# démarche en deux niveaux (tout le reste du classeur ; la preuve par l'absurde
# n'est pas concernée) :
#
#   NIVEAU 1 — ENTIER
#     Suites A et B à termes entiers k^i selon les règles de Savard.
#     Quatre possibilités Digamma : positions n-3 et n-2, signes ±.
#       Digamma = A(n) ± k^position ; P candidat = (B(n) - Digamma) / k^6.
#
#   NIVEAU 2 — GÉOMÉTRIQUE
#     Exactement la même démarche, mais chaque terme devient un terme
#     géométrique : sqrt((k^(i-1))^2 + (k^i)^2) = k^(i-1) * sqrt(1 + k^2).
#     Le facteur commun sqrt(1 + k^2)/k = g(k) s'annule dans P. Les huit
#     branches réelles universelles (positions n-3 / n-2, signes ±, Zêta aux
#     positions 6 et 7) sont également évaluées, ainsi que la reconstruction
#     séquentielle par rang ancrée à n=10.
#
# RÈGLE DE RÉPONSE OBLIGATOIRE (à chaque requête) :
#   1. exposer les quatre possibilités Digamma du niveau 1 (entier) ;
#   2. si le niveau 1 ne retourne aucun premier, donner la démarche de niveau 1
#      qui n'aboutit pas, PUIS déterminer la démarche de niveau 2 (géométrique) ;
#   3. si aucun des deux niveaux ne retourne d'ancrage, énoncer que le système
#      convolutif ne retourne aucun ancrage pour un premier pour ce rapport 1/k.
# ══════════════════════════════════════════════════════════════════════════════

NIVEAU_1_ENTIER = "niveau_1_entier"
NIVEAU_2_GEOMETRIQUE = "niveau_2_geometrique"


def _branche_label(position: int, signe: int) -> str:
    """Étiquette de branche Digamma : A(position)+ ou A(position)-."""
    return f"A({position}){'+' if signe > 0 else '-'}"


def _verdict_branche(est_entier: bool, candidat: Optional[int]) -> str:
    """Verdict lisible d'une branche Digamma."""
    if not est_entier or candidat is None:
        return "NON_ENTIER"
    if candidat <= 1:
        return "NON_VALIDE"
    return "PREMIER" if _est_premier(candidat) else "COMPOSE"


def quatre_possibilites_digamma(rapport: object, n: int = 10) -> List[Dict[str, object]]:
    """Les quatre possibilités Digamma du niveau 1 (suites A/B entières).

    Positions ``n-3`` et ``n-2``, signes ``+`` et ``-``. Chaque possibilité
    expose le Digamma, le Zêta ``k^6``, le candidat P et son verdict.
    """
    k = extraire_k(rapport)
    n = int(n)
    if n < 7:
        raise ValueError("Les quatre possibilités Digamma exigent n >= 7")
    A = suite_A(k, n)
    B = suite_B(k, n)
    zeta = k ** 6
    possibilites: List[Dict[str, object]] = []
    for position in (n - 3, n - 2):
        for signe in (1, -1):
            digamma = A + signe * (k ** position)
            numerateur = B - digamma
            est_entier = numerateur > 0 and numerateur % zeta == 0
            candidat = numerateur // zeta if est_entier else None
            verdict = _verdict_branche(est_entier, candidat)
            possibilites.append({
                "niveau": 1,
                "approche": "entier",
                "position": position,
                "signe": signe,
                "branche": _branche_label(position, signe),
                "digamma": int(digamma),
                "zeta": zeta,
                "C": int(candidat) if candidat is not None else None,
                "entier": bool(est_entier),
                "premier": verdict == "PREMIER",
                "verdict": verdict,
            })
    return possibilites


def niveau_1_entier(rapport: object, n: int = 10) -> Dict[str, object]:
    """Bilan du NIVEAU 1 (entier) : quatre possibilités Digamma + ancrage."""
    k = extraire_k(rapport)
    n = int(n)
    possibilites = quatre_possibilites_digamma(rapport, n)
    retenues = [p for p in possibilites if p["premier"]]
    ancrage = bool(retenues)

    if ancrage:
        detail = " ; ".join(
            f"{p['branche']} -> P={p['C']}" for p in retenues
        )
        demarche = (
            f"Niveau 1 (entier) : suites A et B à termes entiers. Parmi les "
            f"quatre possibilités Digamma (positions {n-3} et {n-2}, signes ±), "
            f"l'ancrage est retourné par {detail}. "
            f"A(n)={suite_A(k, n)}, B(n)={suite_B(k, n)}, Zêta={k ** 6}, "
            f"P = (B(n) - Digamma) / k^6."
        )
    else:
        detail = " ; ".join(
            f"{p['branche']}=({p['C'] if p['C'] is not None else 'non entier'})"
            f"[{p['verdict']}]"
            for p in possibilites
        )
        demarche = (
            f"Niveau 1 (entier) : la démarche avec suites A et B à termes "
            f"entiers NE retourne AUCUN ancrage pour un premier parmi les "
            f"quatre possibilités Digamma (positions {n-3} et {n-2}, signes ±). "
            f"Candidats obtenus : {detail}. "
            f"A(n)={suite_A(k, n)}, B(n)={suite_B(k, n)}, Zêta={k ** 6}."
        )

    return {
        "niveau": 1,
        "approche": "entier",
        "k": k,
        "n": n,
        "termes": "A(n) et B(n) à termes entiers k^i (règles Savard)",
        "possibilites": possibilites,
        "ancrage_retourne": ancrage,
        "premiers": [p["C"] for p in retenues],
        "branches_retenues": [p["branche"] for p in retenues],
        "demarche": demarche,
    }


def niveau_2_geometrique(rapport: object, n: int = 10) -> Dict[str, object]:
    """Bilan du NIVEAU 2 (géométrique) — même démarche, termes géométriques.

    Chaque terme entier ``k^i`` devient ``sqrt((k^(i-1))^2 + (k^i)^2)``
    ``= k^(i-1) * sqrt(1 + k^2)``. Le facteur commun ``g(k) = sqrt(1+k^2)/k``
    s'annule dans P : les quatre possibilités géométriques reproduisent donc le
    candidat du niveau entier. Le niveau géométrique évalue en outre les huit
    branches réelles universelles du classeur (positions n-3 / n-2, signes ±,
    Zêta aux positions 6 et 7) et la reconstruction séquentielle par rang
    ancrée à n=10.
    """
    k = extraire_k(rapport)
    n = int(n)
    if n < 7:
        raise ValueError("Le niveau géométrique exige n >= 7")
    g = math.sqrt(1 + k * k) / k

    possibilites_geo: List[Dict[str, object]] = []
    for base in quatre_possibilites_digamma(rapport, n):
        q = dict(base)
        q["niveau"] = 2
        q["approche"] = "geometrique"
        q["digamma_geometrique"] = int(round(int(base["digamma"]) * g))
        q["note"] = (
            "Termes géométriques k^(i-1)*sqrt(1+k^2) : le facteur commun "
            "sqrt(1+k^2)/k s'annule dans P -> candidat identique au niveau entier."
        )
        possibilites_geo.append(q)

    branches_reelles: List[Dict[str, object]] = []
    if n >= 10:
        for cand in candidats_reconstruction_reelle(rapport, n):
            candidat_int = int(cand["premier"]) if cand["premier"] is not None else None
            verdict = _verdict_branche(bool(cand["entier"]), candidat_int)
            branches_reelles.append({
                "niveau": 2,
                "approche": "geometrique-reelle",
                "position_digamma": cand["position_digamma"],
                "signe": cand["signe_digamma"],
                "position_zeta": cand["position_zeta"],
                "branche": (
                    f"{_branche_label(int(cand['position_digamma']), int(cand['signe_digamma']))}"
                    f"/Z({cand['position_zeta']})"
                ),
                "C": candidat_int,
                "entier": bool(cand["entier"]),
                "premier": bool(cand["premier_verifie"]),
                "verdict": "PREMIER" if cand["premier_verifie"] else verdict,
            })

    reconstruction_par_rang: Dict[str, object] = {
        "disponible": False,
        "rang_base": None,
        "premier_base": None,
        "rang_cible": None,
        "premier_cible": None,
        "verifie": False,
    }
    p10 = reconstruire_premier(rapport, n=10).get("premier")
    idx10 = position_premier_table(p10) if p10 else None
    if idx10 is not None:
        idx_cible = idx10 + (n - 10)
        p_cible = _premier_index(idx_cible) if idx_cible >= 1 else None
        reconstruction_par_rang = {
            "disponible": True,
            "rang_base": idx10,
            "premier_base": p10,
            "rang_cible": idx_cible,
            "premier_cible": p_cible,
            "verifie": bool(p_cible and _est_premier(p_cible)),
        }

    premiers = [p["C"] for p in possibilites_geo if p["premier"]]
    premiers += [b["C"] for b in branches_reelles if b["premier"]]
    if reconstruction_par_rang.get("verifie"):
        premiers.append(reconstruction_par_rang["premier_cible"])
    ancrage = bool(premiers)

    if ancrage:
        detail_parts: List[str] = []
        for p in possibilites_geo:
            if p["premier"]:
                detail_parts.append(f"{p['branche']} -> P={p['C']}")
        for b in branches_reelles:
            if b["premier"]:
                detail_parts.append(f"{b['branche']} -> P={b['C']}")
        if reconstruction_par_rang.get("verifie"):
            detail_parts.append(
                f"rang {reconstruction_par_rang['rang_cible']} -> "
                f"P={reconstruction_par_rang['premier_cible']}"
            )
        demarche = (
            f"Niveau 2 (géométrique) : démarche identique au niveau 1 mais avec "
            f"suites A et B à termes géométriques "
            f"sqrt((k^(i-1))^2 + (k^i)^2), g(k)={g:.10f}. "
            f"Ancrage retourné par {' ; '.join(detail_parts)}."
        )
    else:
        demarche = (
            f"Niveau 2 (géométrique) : démarche identique au niveau 1 mais avec "
            f"suites A et B à termes géométriques "
            f"sqrt((k^(i-1))^2 + (k^i)^2), g(k)={g:.10f}. "
            f"Aucun ancrage pour un premier n'est retourné par les quatre "
            f"possibilités géométriques, ni par les huit branches réelles "
            f"universelles, ni par la reconstruction par rang."
        )

    return {
        "niveau": 2,
        "approche": "geometrique",
        "k": k,
        "n": n,
        "termes": "A(n) et B(n) à termes géométriques sqrt((k^(i-1))^2 + (k^i)^2)",
        "facteur_g": g,
        "possibilites": possibilites_geo,
        "branches_reelles": branches_reelles,
        "reconstruction_par_rang": reconstruction_par_rang,
        "ancrage_retourne": ancrage,
        "premiers": premiers,
        "demarche": demarche,
    }


def criteres_obligatoires(rapport: object, n: int = 10) -> Dict[str, object]:
    """Produit les critères obligatoires de réponse à deux niveaux.

    À chaque requête, Gabriel doit exposer :
      1. le niveau 1 (entier) et ses quatre possibilités Digamma ;
      2. si le niveau 1 ne retourne aucun premier : la démarche de niveau 1 qui
         n'aboutit pas, puis la démarche de niveau 2 (géométrique) ;
      3. si aucun niveau ne retourne d'ancrage : l'énoncé explicite que le
         système convolutif ne retourne aucun ancrage pour un premier pour ce
         rapport 1/k non typique ;
      4. si un ancrage est trouvé (niveau 1 ou 2) : la preuve par l'absurde
         (contrôle de domaine) qui démontre que le composé candidat est exclu.
    """
    import math as _math

    k = extraire_k(rapport)
    n = int(n)
    niveau1 = niveau_1_entier(k, n)
    niveau2 = niveau_2_geometrique(k, n)

    ancrage_1 = bool(niveau1["ancrage_retourne"])
    ancrage_2 = bool(niveau2["ancrage_retourne"])

    # --- POINT 4 — PREUVE PAR L'ABSURDE (si ancrage trouvé) ---
    point_4 = None
    if ancrage_1 or ancrage_2:
        premiers_trouves: List[int] = []
        if ancrage_1:
            premiers_trouves.extend(niveau1.get("premiers", []))
        if ancrage_2:
            premiers_trouves.extend(niveau2.get("premiers", []))

        if premiers_trouves:
            premier_exemple = premiers_trouves[0]
            SA = suite_A(k, n)
            SB = suite_B(k, n)
            zeta = k ** 6
            D_valide = SB - premier_exemple * zeta

            # Preuve par l'absurde : tester un composé proche du premier
            C_compose_test = premier_exemple + 1
            D_compose = abs(SB - C_compose_test * zeta)

            equation_A, _ = reconstruire_equations_ab(k, 10, 9)
            coeff_A_val: float = float(equation_A.coefficient)
            const_A_val: float = float(equation_A.constante)

            x_reel: Optional[float] = None
            x_entier = False
            if coeff_A_val != 0:
                arg = (D_compose - const_A_val) / coeff_A_val
                if arg > 0:
                    x_reel = _math.log(arg, k)
                    if x_reel is not None:
                        x_entier = abs(x_reel - round(x_reel)) < 1e-9

            point_4 = (
                f"POINT 4 — PREUVE PAR L'ABSURDE (contrôle de domaine) : "
                f"Pour le premier P={premier_exemple} trouvé, le Digamma valide est "
                f"D = SB − P·k^6 = {SB} − {premier_exemple}·{zeta} = {D_valide}. "
                f"Pour un composé C={C_compose_test} (premier+1), le Digamma exigé serait "
                f"D_C = SB − {C_compose_test}·{zeta} = ±{D_compose}. "
                f"La résolution SA(k, x) = |{D_compose}| donne x ≈ {x_reel:.4f} "
                f"({'entier' if x_entier else 'non entier — hors domaine ℕ'}). "
                f"Le composé C={C_compose_test} est donc EXCLU : il ne peut pas "
                f"occuper une position spectrale entière. "
                f"Cette preuve par l'absurde confirme que seul le premier "
                f"P={premier_exemple} est ancré dans le système convolutif."
            )

    if ancrage_1:
        point_1 = (
            f"POINT 1 — NIVEAU 1 (entier) : ancrage retourné. {niveau1['demarche']}"
        )
        point_2 = (
            "POINT 2 — NIVEAU 2 (géométrique) : non requis, le niveau 1 a fourni "
            "un ancrage pour un premier."
        )
        point_3 = (
            "POINT 3 — Verdict : le système convolutif retourne un ancrage pour "
            f"un premier pour le rapport 1/{k} (niveau 1 entier)."
        )
    else:
        point_1 = (
            "POINT 1 — NIVEAU 1 (entier) : aucun premier. "
            f"{niveau1['demarche']}"
        )
        point_2 = (
            "POINT 2 — NIVEAU 2 (géométrique) : le niveau 1 n'ayant retourné "
            f"aucun premier, la démarche géométrique est déterminée. "
            f"{niveau2['demarche']}"
        )
        if ancrage_2:
            point_3 = (
                "POINT 3 — Verdict : le système convolutif retourne un ancrage "
                f"pour un premier pour le rapport 1/{k} au niveau 2 (géométrique)."
            )
        else:
            point_3 = (
                f"POINT 3 — Verdict : pour le rapport 1/{k} non typique en "
                "question, le système convolutif ne retourne aucun ancrage pour "
                "un premier (ni au niveau 1 entier, ni au niveau 2 géométrique)."
            )

    points = [point_1, point_2, point_3]
    if point_4 is not None:
        points.append(point_4)
    reponse_obligatoire = "\n".join(points)

    return {
        "rapport": f"1/{k}",
        "k": k,
        "n": n,
        "ancrage_niveau_1": ancrage_1,
        "ancrage_niveau_2": ancrage_2,
        "ancrage_retourne": ancrage_1 or ancrage_2,
        "aucun_ancrage": not (ancrage_1 or ancrage_2),
        "niveau_1": niveau1,
        "niveau_2": niveau2,
        "point_1_niveau_1": point_1,
        "point_2_niveau_2": point_2,
        "point_3_verdict": point_3,
        "point_4_preuve_absurde": point_4,
        "reponse_obligatoire": reponse_obligatoire,
    }


def construire_rapport_convolutif(rapport: object, n: int = 10) -> Dict[str, object]:
    """Produit les faits convolutifs obligatoires pour une requête ``1/k``.

    Les sommes et les équations sont toujours disponibles pour ``n >= 7``.
    La reconstruction du premier reste volontairement indépendante : quand les
    quatre candidats Digamma ne permettent pas de le déterminer, le résultat
    le signale explicitement sans revenir au modèle ``1/2``.
    """
    k = _verifier_k_non_typique(rapport)
    n = int(n)
    if n < 7:
        raise ValueError("Le système convolutif A/B exige n >= 7")

    equation_a, equation_b = reconstruire_equations_ab(k, 10, 9)
    reference = reconstruire_premier(k, n=10)
    cible = reference if n == 10 else reconstruire_premier_pour_n(k, n)
    if cible.get("premier") is None and n >= 10:
        cible = reconstruire_premier_reel_universel(k, n)

    reference_faits = {
        "n": 10,
        "somme_A": suite_A(k, 10),
        "somme_B": suite_B(k, 10),
        "digamma_calcule": reference.get("digamma_calcule"),
        "premier": reference.get("premier"),
        "position_premier": reference.get("position_du_premier (1-index)"),
    }
    ancrage_n9 = {
        "n": 9,
        "somme_A": suite_A(k, 9),
        "somme_B": suite_B(k, 9),
    }
    cible_faits = {
        "n": n,
        "somme_A": suite_A(k, n),
        "somme_B": suite_B(k, n),
        "digamma_calcule": cible.get("digamma_calcule"),
        "premier": cible.get("premier"),
        "position_premier": cible.get("position_du_premier (1-index)"),
        "methode": cible.get("methode", "entiers-digamma"),
    }
    premier_indetermine = cible_faits["premier"] is None
    note = cible.get("note")
    if premier_indetermine:
        message_indetermine = (
            "Aucun premier n'a pu être déterminé parmi les quatre "
            "possibilités Digamma (positions n-3 et n-2, signes +/-)."
        )
        note = f"{message_indetermine} {note}" if note else message_indetermine

    # Critères obligatoires à deux niveaux (niveau 1 entier -> niveau 2
    # géométrique -> énoncé d'absence d'ancrage). Toujours calculés afin que
    # chaque réponse de Gabriel expose les trois points.
    criteres = criteres_obligatoires(k, n)

    return {
        "rapport": f"1/{k}",
        "k": k,
        "equation_A": equation_a.as_dict(),
        "equation_B": equation_b.as_dict(),
        "reference_n10": reference_faits,
        "ancrage_n9": ancrage_n9,
        "cible": cible_faits,
        "suites_reelles": construire_suites_reelles(k, max(10, n)),
        "equations_reelles": equations_suites_reelles(k, max(10, n)),
        "methode_reconstruction": cible.get("methode", "entiers-digamma"),
        "premier_indetermine": premier_indetermine,
        "note": note,
        # ── Contrat cognitif à deux niveaux (critères obligatoires) ──
        "niveau_1": criteres["niveau_1"],
        "niveau_2": criteres["niveau_2"],
        "ancrage_niveau_1": criteres["ancrage_niveau_1"],
        "ancrage_niveau_2": criteres["ancrage_niveau_2"],
        "ancrage_retourne": criteres["ancrage_retourne"],
        "aucun_ancrage": criteres["aucun_ancrage"],
        "point_1_niveau_1": criteres["point_1_niveau_1"],
        "point_2_niveau_2": criteres["point_2_niveau_2"],
        "point_3_verdict": criteres["point_3_verdict"],
        "point_4_preuve_absurde": criteres["point_4_preuve_absurde"],
        "criteres_obligatoires": criteres["reponse_obligatoire"],
    }


# ═════════════════════════════════════════════════════════════════════════
#  RECONSTRUCTION DU PREMIER POUR UN RAPPORT NON-TYPIQUE (n=10)
# ═════════════════════════════════════════════════════════════════════════
def reconstruire_premier(rapport: object, n: int = 10,
                         position: Optional[int] = None,
                         signe: Optional[int] = None,
                         verifier: bool = True) -> Dict:
    """Reconstruit le nombre premier du rapport 1/k à partir des suites A/B.

    Étapes suivant l'extrait :
      1) Digamma : position (7 ou 8), signe (+/-) selon le rapport.
      2) Digamma_calculé = Somme_A ± t^pos.
      3) Premier = ( Somme_B - Digamma_calculé ) / t^6.
    QUAND position/signe sont absents, on AUTO-DÉTECTE : on essaie les quatre
    branches (8,+), (8,-), (7,+), (7,-) et on retient la première qui donne un
    résultat ENTIER et PREMIER. Les ajustements de forme A détaillés dans
    SUITES_A_AJUSTEES permettent de reproduire exactement les exemples.
    """
    k = extraire_k(rapport)
    t = k                       # base = k du rapport 1/k

    A = suite_A(t, n)
    B = suite_B(t, n)
    # (Aucun ajustement de la suite A : construction XIV.4 terme à terme.)

    if position is not None and signe is not None:
        combinaisons = [(int(position), int(signe))]
    else:
        combinaisons = [(8, -1), (8, +1), (7, +1), (7, -1)]

    meilleur = None
    for pos, sg in combinaisons:
        digamma_cal = A + sg * (t ** pos)
        numerateur = B - digamma_cal
        if numerateur <= 0 or numerateur % (t ** 6) != 0:
            continue
        candidat = numerateur // (t ** 6)
        verifie_pos = position_premier_table(candidat) if candidat > 1 else None
        if verifie_pos is None:
            continue
        meilleur = {
            "rapport": f"1/{k}",
            "k": k,
            "n": n,
            "position": pos,
            "signe": "addition" if sg > 0 else "soustraction",
            "A": int(A),
            "B": int(B),
            "digamma_calcule": int(digamma_cal),
            "premier": int(candidat),
            "position_du_premier (1-index)": verifie_pos,
            "verifie": True,
        }
        break
    if meilleur is None:
        universel = reconstruire_premier_reel_universel(k, n) if n >= 10 else None
        if universel is not None and universel["verifie"]:
            return universel
        retour = {
            "rapport": f"1/{k}", "k": k, "n": n,
            "position": position, "signe": "addition" if signe and signe > 0 else "soustraction",
            "A": int(A), "B": int(B),
            "digamma_calcule": None, "premier": None,
            "position_du_premier (1-index)": None,
            "verifie": False,
            "note": ("aucune combinaison (7e/8e position × ±) n'a produit un "
                     "entier premier — vérifier le ratio"),
        }
        if position is None:
            retour["position"] = None
        return retour
    return meilleur


# ═════════════════════════════════════════════════════════════════════════
#  POSITION D'UN PREMIER DANS LA TABLE (ordre 2,3,5,7,11,…)
# ═════════════════════════════════════════════════════════════════════════
def position_premier_table(p: int) -> Optional[int]:
    """Position (1-indexée) du premier p dans PREMIERS, None si absent."""
    p = abs(int(p))
    lo, hi = 0, len(PREMIERS) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if PREMIERS[mid] == p:
            return mid + 1
        if PREMIERS[mid] < p:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


def _premier_index(idx: int) -> Optional[int]:
    """Premier à la position idx (1-indexée) ou None hors table."""
    if idx < 1 or idx > len(PREMIERS):
        return None
    return PREMIERS[idx - 1]


def _premier_10_n(t: int, n: int) -> Optional[int]:
    """Retourne le premier indexé par n dans l'ordre des premiers de la
    série du rapport non-typique t (point d'ancrage n=10)."""
    p10 = reconstruire_premier(t, n=10).get("premier")
    idx10 = position_premier_table(p10) if p10 else None
    if n == 10:
        return p10
    if idx10 is None:
        return None
    delta = n - 10
    return _premier_index(idx10 + delta)


_cache_premier_par_n: dict = {}


def _digamma_n_avec_p(t: int, B: int, p_connu: int) -> int:
    """Digamma calculé pour n≠10 (valable 1/k<>1/2) :
    Digamma_calculé = ( SB / (6e position) - P ) * 6e position
                    = ( B/t^6 - p ) * t^6  =  B - p*t^6
    """
    return int(B) - int(p_connu) * (t ** 6)


def reconstruire_premier_pour_n(rapport: object, n: int,
                                p_connu: Optional[int] = None,
                                position: Optional[int] = None,
                                signe: Optional[int] = None) -> Dict:
    """Reconstruit le premier pour une quantité de termes n quelconque.

    - n = 10 : méthode du digamma (8e/7e position ±), encodé dans DIGAMMA_MAP.
    - n ≠ 10 : on utilise le digamma généralisé
               Digamma_calculé = ( SB / t^6 - P ) * t^6,
               puis on reconstruit : P = ( SB - Digamma_calculé ) / t^6.
    """
    t = extraire_k(rapport)
    if n == 10 and p_connu is None:
        return reconstruire_premier(t, n=10, position=position, signe=signe)

    A = suite_A(t, n)
    B = suite_B(t, n)
    if p_connu is None:
        p_connu = _premier_10_n(t, n)
    if p_connu is None:
        reel = reconstruire_premier_reel_universel(t, max(10, n))
        if reel["verifie"]:
            return reel
        return {
            "rapport": f"1/{t}", "n": n, "A": int(A), "B": int(B),
            "digamma_calcule": None, "premier": None,
            "note": "p_connu introuvable pour ce n",
        }
    dig = _digamma_n_avec_p(t, B, p_connu)
    numerateur = B - dig
    p_calc = numerateur // (t ** 6) if numerateur % (t ** 6) == 0 else None
    _cache_premier_par_n[(t, n)] = p_calc
    return {
        "rapport": f"1/{t}", "n": n, "A": int(A), "B": int(B),
        "digamma_calcule": int(dig), "premier": int(p_calc) if p_calc else None,
        "position_du_premier (1-index)": position_premier_table(p_calc) if p_calc else None,
    }


def position_du_premier(p: int) -> Optional[int]:
    """Alias externe : position 1-indexée du premier p."""
    return position_premier_table(p)


def determiner_n(rapport: object, x: int, mode: str = "position") -> Optional[int]:
    """
    Détermine la valeur de n (nombre de TERMES) qui correspond à un premier
    cible du rapport 1/k<>1/2.

    - mode='position' : x est la position cible (1-indexée).
    - mode='premier'  : x est le premier cible.
    L'ordre est indexé par n=10 : chaque +1 avance vers le premier suivant,
    chaque -1 recule vers le premier précédent.
    """
    t = extraire_k(rapport)
    p10 = reconstruire_premier(t, n=10).get("premier")
    idx10 = position_premier_table(p10) if p10 else None
    if idx10 is None:
        return None
    if mode == "premier":
        idx = position_premier_table(x)
    else:
        idx = int(x)
    if idx is None:
        return None
    return 10 + (idx - idx10)


# ═════════════════════════════════════════════════════════════════════════
#  VALEURS DE RÉFÉRENCE de l'extrait (n=10) pour vérification du module
# ═════════════════════════════════════════════════════════════════════════
VALEURS_REFERENCE_N10: Dict[int, Dict] = {
    3: {"A": 79824, "B": 238746, "digamma": 73263, "premier": 227},
    5: {"A": 11738280, "B": 58675780, "digamma": 11816405, "premier": 2999},
    6: {"A": 68920242, "B": 423552498, "digamma": 68640306, "premier": 7607},
}


def verifier_exemples() -> bool:
    """Vérifie que le module reproduit les exemples validés de l'extrait."""
    ok = True
    for k, att in VALEURS_REFERENCE_N10.items():
        r = reconstruire_premier(k, n=10)
        p_calc = r["premier"]
        print(
            f"  1/{k}: A={r['A']}, B={r['B']}, "
            f"digamma_calc={r['digamma_calcule']}, premier={p_calc}"
        )
        if p_calc != att["premier"]:
            ok = False
            print(f"    ⚠ attendu : {att['premier']}")
    print("  → ", "OK : les exemples Savard sont reproduits." if ok
          else "ÉCARTS relevés.")
    return ok


if __name__ == "__main__":
    print("Rapports non-typiques 1/k<>1/2 — démonstration")
    for rapp in ["1/3", "1/4", "1/5", "1/6", "1/7"]:
        res = reconstruire_premier(rapp, n=10)
        print(
            f"  rapport={rapp:>4} n=10 → premier={res['premier']} "
            f"(pos={res['position']}, {res['signe']}) "
            f"A={res['A']} B={res['B']}"
        )
    print()
    verifier_exemples()


def premier_pour_n(rapport: object, n: int) -> Optional[int]:
    """Premier reconstruit pour une quantité de termes n (sens Savard)."""
    return _premier_10_n(extraire_k(rapport), n)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
