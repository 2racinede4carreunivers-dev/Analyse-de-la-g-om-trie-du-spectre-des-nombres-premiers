#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SUITES GÉOMÉTRIQUES A ET B - Gabriel Multiloop v7.4
=====================================================

Module de calcul des sommes des suites géométriques A et B
pour la reconstruction des nombres premiers via l'approche géométrique.

SUITE A (Modèle géométrique):
  S_A = sqrt(1² + t¹²) + sqrt(t¹² + t²²) + sqrt(t²² + t³²)
      + sqrt(t³² + t⁴²) + sqrt(t⁴² + t⁵²) + sqrt(t⁵² + t⁶²)
      + sqrt(t⁶² + t⁷²) + sqrt(t⁷² + t⁸²)
      + sqrt((t⁸-t⁶)² + (t⁹-t⁷)²)
      + sqrt((t⁹-t⁷)² + (t¹⁰-t⁸)²)

SUITE B (Modèle géométrique):
  S_B = sqrt(1² + t¹²) + sqrt(t¹² + t²²) + sqrt(t²² + t³²)
      + sqrt(t³² + t⁴²) + sqrt(t⁴² + t⁵²) + sqrt(t⁶² + t⁷²)
      + sqrt(t⁷² + t⁸²) + sqrt(t⁸² + t⁹²)
      + sqrt((t¹⁰-t⁸)² + (t¹¹-t⁹)²)
      + sqrt((t¹¹-t⁹)² + (t¹²-t¹⁰)²)

ADAPTABILITÉ:
  - Rapport typique  : t = 1/k avec k=2  →  t = 1/2
  - Rapport non typique : t = 1/k pour tout k entier ≥ 2 (ou rationnel)

La méthode Digamma pour reconstruire les premiers reste inchangée.
Ce module fournit l'APPROCHE GÉOMÉTRIQUE comme fallback lorsque
l'approche algébrique (suites A et B à termes entiers + 4 Digamma)
échoue à reconstruire un premier.

Auteur : Gabriel Multiloop — Extension géométrique Philippe Savard 2026
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Dict, List, Optional, Tuple, Union


# ============================================================
# STRUCTURES DE DONNÉES
# ============================================================

@dataclass
class ResultatSuiteGeo:
    """Résultat complet du calcul d'une suite géométrique."""
    t: float
    k: Union[int, float]
    rapport_typique: bool          # True si k est entier et t = 1/k
    somme_A: float
    somme_B: float
    termes_A: List[float] = field(default_factory=list)
    termes_B: List[float] = field(default_factory=list)
    puissances_t: List[float] = field(default_factory=list)
    candidats_premiers: List[int] = field(default_factory=list)
    reconstruction_reussie: bool = False
    methode: str = "geometrique"

    def __repr__(self) -> str:
        statut = "✓ Reconstruction réussie" if self.reconstruction_reussie else "✗ Échec reconstruction"
        return (
            f"ResultatSuiteGeo(t=1/{self.k:.4g}, "
            f"S_A={self.somme_A:.8f}, S_B={self.somme_B:.8f}, "
            f"candidats={self.candidats_premiers}, {statut})"
        )


@dataclass
class DiagnosticFallback:
    """Trace complète du mécanisme de fallback géométrique."""
    n: int                              # valeur de n considérée
    echec_algebrique: bool = False      # l'approche algébrique a échoué
    tentative_geometrique: bool = False # le fallback a été déclenché
    resultat_geo: Optional[ResultatSuiteGeo] = None
    premiers_trouves: List[int] = field(default_factory=list)
    message: str = ""


# ============================================================
# CALCUL DES SUITES GÉOMÉTRIQUES A ET B
# ============================================================

class CalculateurSuitesGeometriques:
    """
    Calcule les sommes des suites géométriques A et B
    pour un rapport t = 1/k donné (typique ou non typique).

    Paramètres
    ----------
    k : int ou float
        Le dénominateur du rapport t = 1/k.
        k = 2 → rapport typique (t = 1/2).
        k quelconque → rapport non typique.
    """

    def __init__(self, k: Union[int, float] = 2):
        self.k = k
        self.t = 1.0 / float(k)
        self.rapport_typique = isinstance(k, int) and k == 2

        # Pré-calcul des puissances de t jusqu'à t^12
        # t^0 = 1 par convention (utilisé dans le premier terme)
        self._puissances: List[float] = [self.t ** n for n in range(13)]
        # Index 0 = t^0 = 1 (la constante initiale "1^1")
        # mais on pose _puissances[0] = 1 explicitement
        self._puissances[0] = 1.0

    # ----------------------------------------------------------
    # TERMES INDIVIDUELS
    # ----------------------------------------------------------

    def _terme(self, a: float, b: float) -> float:
        """sqrt(a² + b²) — terme géométrique hypoténuse."""
        return math.sqrt(a * a + b * b)

    def _p(self, n: int) -> float:
        """Retourne t^n avec t^0 = 1 (constante initiale)."""
        if n == 0:
            return 1.0
        return self.t ** n

    # ----------------------------------------------------------
    # SUITE A
    # ----------------------------------------------------------

    def calculer_somme_A(self) -> Tuple[float, List[float]]:
        """
        Calcule S_A et retourne (somme, liste_des_termes).

        Termes de la suite A :
          T1  = sqrt(1²      + (t¹)²)
          T2  = sqrt((t¹)²   + (t²)²)
          T3  = sqrt((t²)²   + (t³)²)
          T4  = sqrt((t³)²   + (t⁴)²)
          T5  = sqrt((t⁴)²   + (t⁵)²)
          T6  = sqrt((t⁵)²   + (t⁶)²)
          T7  = sqrt((t⁶)²   + (t⁷)²)
          T8  = sqrt((t⁷)²   + (t⁸)²)
          T9  = sqrt((t⁸-t⁶)² + (t⁹-t⁷)²)   ← terme différentiel
          T10 = sqrt((t⁹-t⁷)² + (t¹⁰-t⁸)²)  ← terme différentiel
        """
        p = self._p

        termes = [
            self._terme(p(0), p(1)),           # T1 : sqrt(1² + t¹²)
            self._terme(p(1), p(2)),            # T2
            self._terme(p(2), p(3)),            # T3
            self._terme(p(3), p(4)),            # T4
            self._terme(p(4), p(5)),            # T5
            self._terme(p(5), p(6)),            # T6
            self._terme(p(6), p(7)),            # T7
            self._terme(p(7), p(8)),            # T8
            self._terme(p(8) - p(6), p(9) - p(7)),   # T9  différentiel
            self._terme(p(9) - p(7), p(10) - p(8)),  # T10 différentiel
        ]

        return sum(termes), termes

    # ----------------------------------------------------------
    # SUITE B
    # ----------------------------------------------------------

    def calculer_somme_B(self) -> Tuple[float, List[float]]:
        """
        Calcule S_B et retourne (somme, liste_des_termes).

        Termes de la suite B :
          T1  = sqrt(1²      + (t¹)²)
          T2  = sqrt((t¹)²   + (t²)²)
          T3  = sqrt((t²)²   + (t³)²)
          T4  = sqrt((t³)²   + (t⁴)²)
          T5  = sqrt((t⁴)²   + (t⁵)²)
          [NOTE: le terme (t⁵, t⁶) est absent — décalage structurel A→B]
          T6  = sqrt((t⁶)²   + (t⁷)²)
          T7  = sqrt((t⁷)²   + (t⁸)²)
          T8  = sqrt((t⁸)²   + (t⁹)²)
          T9  = sqrt((t¹⁰-t⁸)²  + (t¹¹-t⁹)²)   ← terme différentiel décalé
          T10 = sqrt((t¹¹-t⁹)²  + (t¹²-t¹⁰)²)  ← terme différentiel décalé
        """
        p = self._p

        termes = [
            self._terme(p(0), p(1)),            # T1 : sqrt(1² + t¹²)
            self._terme(p(1), p(2)),             # T2
            self._terme(p(2), p(3)),             # T3
            self._terme(p(3), p(4)),             # T4
            self._terme(p(4), p(5)),             # T5
            # SAUT : pas de terme (t⁵, t⁶) dans B
            self._terme(p(6), p(7)),             # T6 (exposants 6,7)
            self._terme(p(7), p(8)),             # T7
            self._terme(p(8), p(9)),             # T8
            self._terme(p(10) - p(8), p(11) - p(9)),   # T9  différentiel décalé
            self._terme(p(11) - p(9), p(12) - p(10)),  # T10 différentiel décalé
        ]

        return sum(termes), termes

    # ----------------------------------------------------------
    # CALCUL COMPLET
    # ----------------------------------------------------------

    def calculer(self) -> ResultatSuiteGeo:
        """Lance le calcul complet des deux suites et retourne le résultat."""
        somme_A, termes_A = self.calculer_somme_A()
        somme_B, termes_B = self.calculer_somme_B()

        puissances = [self._p(n) for n in range(13)]

        return ResultatSuiteGeo(
            t=self.t,
            k=self.k,
            rapport_typique=self.rapport_typique,
            somme_A=somme_A,
            somme_B=somme_B,
            termes_A=termes_A,
            termes_B=termes_B,
            puissances_t=puissances,
            methode="geometrique",
        )


# ============================================================
# EXTRACTION DE CANDIDATS PREMIERS DEPUIS LES SOMMES
# ============================================================

class ExtracteurPremiersGeometriques:
    """
    Extrait des candidats nombres premiers à partir des sommes
    géométriques S_A et S_B, pour toutes les valeurs de n.

    Stratégies d'extraction :
      1. Arrondi entier de S_A et S_B
      2. Parties entières floor/ceil
      3. Combinaisons linéaires entières de S_A et S_B
      4. Ratios et différences entre S_A et S_B normalisés
    """

    def __init__(self, calc: CalculateurSuitesGeometriques):
        self.calc = calc

    @staticmethod
    def est_premier(n: int) -> bool:
        """Test de primalité (Miller-Rabin simplifié pour petits entiers)."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        if n < 9:
            return True
        if n % 3 == 0:
            return False
        r = int(math.isqrt(n))
        f = 5
        while f <= r:
            if n % f == 0 or n % (f + 2) == 0:
                return False
            f += 6
        return True

    def extraire_candidats(self, res: ResultatSuiteGeo) -> List[int]:
        """
        Génère tous les candidats entiers depuis S_A et S_B
        et filtre les nombres premiers.
        """
        candidats_bruts: List[int] = []
        S_A, S_B = res.somme_A, res.somme_B

        # Stratégie 1 : arrondis directs
        for val in [S_A, S_B, S_A + S_B, abs(S_A - S_B)]:
            for c in [math.floor(val), math.ceil(val), round(val)]:
                if c > 1:
                    candidats_bruts.append(c)

        # Stratégie 2 : multiples entiers (n * S_A, n * S_B)
        for n in range(1, 15):
            for val in [n * S_A, n * S_B]:
                for c in [math.floor(val), math.ceil(val), round(val)]:
                    if 2 <= c <= 10000:
                        candidats_bruts.append(c)

        # Stratégie 3 : inverses normalisés (1/t = k correspond à un premier?)
        k_int = round(self.calc.k)
        candidats_bruts.append(k_int)

        # Stratégie 4 : différences entre termes individuels normalisées
        for i, ta in enumerate(res.termes_A):
            for j, tb in enumerate(res.termes_B):
                diff = abs(ta - tb)
                if diff > 0:
                    c_floor = math.floor(1.0 / diff) if diff < 1 else math.floor(diff)
                    if 2 <= c_floor <= 10000:
                        candidats_bruts.append(c_floor)

        # Filtrage : garder uniquement les premiers, sans doublons
        premiers = sorted(set(c for c in candidats_bruts if self.est_premier(c)))
        return premiers

    def extraire_pour_n(self,
                        n_values: List[int],
                        k_base: Union[int, float] = 2
                        ) -> Dict[int, List[int]]:
        """
        Pour chaque valeur de n, adapte k et extrait les premiers.
        Permet de couvrir l'ensemble des valeurs de n.

        Stratégie d'adaptation de k selon n :
          - k = k_base (rapport typique ou fourni)
          - ou k = n (rapport non typique dépendant de n)
        """
        resultats: Dict[int, List[int]] = {}

        for n in n_values:
            # Cas typique : t = 1/k_base fixe
            calc_fixe = CalculateurSuitesGeometriques(k=k_base)
            res_fixe = calc_fixe.calculer()
            candidats_fixe = self.extraire_candidats(res_fixe)

            # Cas non typique : t = 1/n (rapport dépendant de n)
            if n >= 2:
                calc_n = CalculateurSuitesGeometriques(k=n)
                res_n = calc_n.calculer()
                ext_n = ExtracteurPremiersGeometriques(calc_n)
                candidats_n = ext_n.extraire_candidats(res_n)
            else:
                candidats_n = []

            # Union des candidats des deux approches
            tous = sorted(set(candidats_fixe) | set(candidats_n))
            resultats[n] = tous

        return resultats


# ============================================================
# PIPELINE COGNITIF — INTÉGRATION GÉOMÉTRIQUE
# ============================================================

class PipelineSuitesGeometriques:
    """
    Module d'intégration des suites géométriques dans le pipeline
    cognitif et le système convolutif de Gabriel Multiloop.

    Fournit :
      - calcul_pour_rapport(k)  : calcul complet pour un rapport donné
      - convolution_AB(n_max)   : convolution des sommes A et B sur 1..n_max
      - reconstruire_premiers(n_values) : reconstruction de premiers via géométrie
    """

    def __init__(self, k_typique: Union[int, float] = 2):
        self.k_typique = k_typique
        self._cache: Dict[float, ResultatSuiteGeo] = {}

    # ----------------------------------------------------------
    # CALCUL POUR UN RAPPORT DONNÉ
    # ----------------------------------------------------------

    def calcul_pour_rapport(self,
                             k: Union[int, float]
                             ) -> ResultatSuiteGeo:
        """
        Calcule S_A et S_B pour t = 1/k.
        Résultats mis en cache pour éviter les recalculs.
        """
        k_float = float(k)
        if k_float not in self._cache:
            calc = CalculateurSuitesGeometriques(k=k)
            self._cache[k_float] = calc.calculer()
        return self._cache[k_float]

    # ----------------------------------------------------------
    # CONVOLUTION DES SUITES A ET B
    # ----------------------------------------------------------

    def convolution_AB(self,
                       n_max: int = 50,
                       k: Union[int, float] = 2
                       ) -> Dict[str, List[float]]:
        """
        Calcule la convolution discrète des suites A et B
        pour n = 1 à n_max avec t = 1/k.

        La convolution est définie ici comme :
          C[n] = sum_{j=1}^{n} A_j * B_{n-j+1}

        où A_j et B_j sont les j-ièmes termes des suites A et B.

        Retourne un dict avec :
          'sommes_A'    : [S_A(n) pour n=1..n_max]  (k fixe)
          'sommes_B'    : [S_B(n) pour n=1..n_max]
          'convolution' : [C(n) pour n=1..n_max]
          'ratios_AB'   : [S_A(n)/S_B(n)]
        """
        res = self.calcul_pour_rapport(k)
        termes_A = res.termes_A
        termes_B = res.termes_B
        n_termes = min(len(termes_A), len(termes_B), n_max)

        sommes_A_cumul = []
        sommes_B_cumul = []
        convolution = []
        ratios_AB = []

        s_a, s_b = 0.0, 0.0
        for j in range(n_termes):
            s_a += termes_A[j]
            s_b += termes_B[j]
            sommes_A_cumul.append(s_a)
            sommes_B_cumul.append(s_b)
            ratios_AB.append(s_a / s_b if s_b != 0 else float('inf'))

            # Convolution discrète
            c_n = sum(
                termes_A[l] * termes_B[j - l]
                for l in range(j + 1)
                if j - l < len(termes_B)
            )
            convolution.append(c_n)

        return {
            'sommes_A': sommes_A_cumul,
            'sommes_B': sommes_B_cumul,
            'convolution': convolution,
            'ratios_AB': ratios_AB,
        }

    # ----------------------------------------------------------
    # RECONSTRUCTION DES PREMIERS VIA GÉOMÉTRIE
    # ----------------------------------------------------------

    def reconstruire_premiers(self,
                               n_values: List[int],
                               k: Union[int, float] = 2
                               ) -> Dict[int, ResultatSuiteGeo]:
        """
        Tente de reconstruire des nombres premiers pour chaque n
        via l'approche géométrique des suites A et B.

        Retourne un dict {n: ResultatSuiteGeo} avec le champ
        'reconstruction_reussie' et 'candidats_premiers' renseignés.
        """
        resultats: Dict[int, ResultatSuiteGeo] = {}

        for n in n_values:
            # Essai 1 : rapport typique k fixe
            calc_fixe = CalculateurSuitesGeometriques(k=k)
            res = calc_fixe.calculer()
            ext = ExtracteurPremiersGeometriques(calc_fixe)
            candidats = ext.extraire_candidats(res)

            # Essai 2 : rapport non typique k = n si différent
            if n >= 2 and float(n) != float(k):
                calc_n = CalculateurSuitesGeometriques(k=n)
                res_n = calc_n.calculer()
                ext_n = ExtracteurPremiersGeometriques(calc_n)
                candidats_n = ext_n.extraire_candidats(res_n)
                candidats = sorted(set(candidats) | set(candidats_n))

            res.candidats_premiers = candidats
            res.reconstruction_reussie = len(candidats) > 0
            resultats[n] = res

        return resultats

    # ----------------------------------------------------------
    # AFFICHAGE DIAGNOSTIQUE
    # ----------------------------------------------------------

    def rapport_complet(self, k: Union[int, float] = 2) -> str:
        """Génère un rapport lisible des suites A et B pour t = 1/k."""
        res = self.calcul_pour_rapport(k)
        t = res.t
        rapport = res.rapport_typique

        lignes = [
            "=" * 65,
            f"  SUITES GÉOMÉTRIQUES A ET B — Gabriel Multiloop v7.4",
            "=" * 65,
            f"  t = 1/{k} = {t:.10f}",
            f"  Rapport : {'TYPIQUE (k=2)' if rapport else f'NON TYPIQUE (k={k})'}",
            "",
            "  TERMES DE LA SUITE A :",
        ]
        labels_A = [
            "√(1²+t¹²)", "√(t¹²+t²²)", "√(t²²+t³²)", "√(t³²+t⁴²)",
            "√(t⁴²+t⁵²)", "√(t⁵²+t⁶²)", "√(t⁶²+t⁷²)", "√(t⁷²+t⁸²)",
            "√((t⁸-t⁶)²+(t⁹-t⁷)²)", "√((t⁹-t⁷)²+(t¹⁰-t⁸)²)",
        ]
        for i, (label, val) in enumerate(zip(labels_A, res.termes_A)):
            lignes.append(f"    T{i+1:2d}: {label:35s} = {val:.10f}")
        lignes.append(f"  → SOMME A = {res.somme_A:.10f}")
        lignes.append("")
        lignes.append("  TERMES DE LA SUITE B :")
        labels_B = [
            "√(1²+t¹²)", "√(t¹²+t²²)", "√(t²²+t³²)", "√(t³²+t⁴²)",
            "√(t⁴²+t⁵²)", "√(t⁶²+t⁷²)", "√(t⁷²+t⁸²)", "√(t⁸²+t⁹²)",
            "√((t¹⁰-t⁸)²+(t¹¹-t⁹)²)", "√((t¹¹-t⁹)²+(t¹²-t¹⁰)²)",
        ]
        for i, (label, val) in enumerate(zip(labels_B, res.termes_B)):
            lignes.append(f"    T{i+1:2d}: {label:35s} = {val:.10f}")
        lignes.append(f"  → SOMME B = {res.somme_B:.10f}")
        lignes.append("")
        lignes.append(f"  S_A + S_B = {res.somme_A + res.somme_B:.10f}")
        lignes.append(f"  S_A - S_B = {res.somme_A - res.somme_B:.10f}")
        lignes.append(f"  S_A / S_B = {res.somme_A / res.somme_B:.10f}")
        lignes.append("=" * 65)

        return "\n".join(lignes)


# ============================================================
# FALLBACK — MÉCANISME DE DÉCLENCHEMENT DANS GABRIEL
# ============================================================

def declencher_fallback_geometrique(
    n: int,
    k: Union[int, float] = 2,
    verbose: bool = True
) -> DiagnosticFallback:
    """
    Point d'entrée du mécanisme de fallback géométrique.

    À appeler depuis gabriel_geometric_wrapper.py lorsque
    l'approche algébrique (suites A et B à termes entiers +
    4 possibilités Digamma) n'a pas reconstruit de premier.

    Paramètres
    ----------
    n : int
        La valeur de n pour laquelle la reconstruction a échoué.
    k : int ou float
        Le rapport t = 1/k à utiliser (typique ou non typique).
    verbose : bool
        Affiche le rapport si True.

    Retourne
    --------
    DiagnosticFallback avec les résultats de la tentative géométrique.
    """
    diag = DiagnosticFallback(
        n=n,
        echec_algebrique=True,
        tentative_geometrique=True,
        message=f"Fallback géométrique déclenché pour n={n}, k={k}",
    )

    pipeline = PipelineSuitesGeometriques(k_typique=k)
    resultats = pipeline.reconstruire_premiers(n_values=[n], k=k)
    res = resultats.get(n)

    if res is not None:
        diag.resultat_geo = res
        diag.premiers_trouves = res.candidats_premiers
        if verbose:
            print(pipeline.rapport_complet(k=k))
            if res.candidats_premiers:
                print(f"  ✓ Fallback géométrique : premiers trouvés = {res.candidats_premiers}")
            else:
                print(f"  ✗ Fallback géométrique : aucun premier reconstruit pour n={n}")

    return diag


# ============================================================
# DÉMO / TEST AUTONOME
# ============================================================

def demo():
    print("\n" + "=" * 65)
    print("  DÉMO — SUITES GÉOMÉTRIQUES A ET B (Gabriel Multiloop v7.4)")
    print("=" * 65)

    pipeline = PipelineSuitesGeometriques()

    # Rapport typique t = 1/2
    print("\n[1] Rapport typique t = 1/2 (k=2) :")
    print(pipeline.rapport_complet(k=2))

    # Rapport non typique t = 1/3
    print("\n[2] Rapport non typique t = 1/3 (k=3) :")
    print(pipeline.rapport_complet(k=3))

    # Rapport non typique t = 1/5
    print("\n[3] Rapport non typique t = 1/5 (k=5) :")
    print(pipeline.rapport_complet(k=5))

    # Convolution sur 10 termes
    print("\n[4] Convolution A⊗B sur 10 termes (k=2) :")
    conv = pipeline.convolution_AB(n_max=10, k=2)
    for i, (sa, sb, c, r) in enumerate(zip(
        conv['sommes_A'], conv['sommes_B'], conv['convolution'], conv['ratios_AB']
    )):
        print(f"    n={i+1:2d} | S_A={sa:.6f} | S_B={sb:.6f} | Conv={c:.8f} | S_A/S_B={r:.6f}")

    # Reconstruction de premiers pour n = 2..10
    print("\n[5] Reconstruction premiers pour n = 2..10 (k=2) :")
    recs = pipeline.reconstruire_premiers(n_values=list(range(2, 11)), k=2)
    for n, res in recs.items():
        statut = "✓" if res.reconstruction_reussie else "✗"
        print(f"    {statut} n={n:2d} : premiers = {res.candidats_premiers[:8]}")

    # Test du fallback
    print("\n[6] Test du mécanisme de fallback (n=7, k=2) :")
    diag = declencher_fallback_geometrique(n=7, k=2, verbose=True)
    print(f"    Premiers trouvés via fallback : {diag.premiers_trouves}")


if __name__ == "__main__":
    demo()
