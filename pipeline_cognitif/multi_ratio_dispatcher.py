#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MULTI-RATIO DISPATCHER ETENDU v7.9 - Pipeline Cognitif Gabriel
==============================================================
Correction critique v7.9 : raccourci O(1) pour n=10.

BUG v7.8 : pour n=10, pos_n = pos_ancre + (10-10) = pos_ancre.
  Donc prime(pos_ancre) = ancre directement.
  primepi(ancre) etait calcule inutilement -> bloquage 2h pour k~1000.

CORRECTIF v7.9 :
  if n == 10:
      premier_n = premier_ancre   # O(1) - direct, sans primepi ni prime
  else:
      pos_ancre = primepi(premier_ancre)   # seulement si n != 10
      pos_n     = pos_ancre + (n - 10)
      premier_n = prime(pos_n)

Performance apres correction :
  k=985..1001 a n=10 : < 5 secondes (au lieu de 2+ heures)
  k=2..1000   a n=10 : < 30 secondes
  k quelconque a n!=10 : primepi utilise normalement

Support k arbitraire : de k=2 jusqu a K_MAX_RECORD=10^13.
Retro-compatible v7.6, v7.7, v7.8 (API identique).

RECORD DE REFERENCE - Zeros non triviaux de la fonction zeta de Riemann :
  Platt & Trudgian (2021) : 3 x 10^12 premiers zeros verifies.
  LMFDB : ~10^13 zeros calcules.
  K_MAX_RECORD = 10_000_000_000_000  (10^13)

Auteur : Philippe Savard 2026
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from sympy import isprime, prime, primepi

try:
    from .suites_geometriques_niveau2 import (
        CalculateurNiveau1Entiers, est_premier, valider_n, ORDRE_DIGAMMA
    )
except ImportError:
    from suites_geometriques_niveau2 import (
        CalculateurNiveau1Entiers, est_premier, valider_n, ORDRE_DIGAMMA
    )

# =============================================================================
# CONSTANTES
# =============================================================================

ANCHORS_N10: Dict[int, int] = {
    2: 29, 3: 227, 4: 947, 5: 2999,
    6: 7529, 7: 16519, 8: 32327, 9: 58337,
}

K_TYPIQUE      = 2
K_MIN          = 2
K_MAX_RECORD   = 10_000_000_000_000   # 10^13
K_NON_TYPIQUES = list(range(3, 10))
K_TOUS         = list(range(2, 10))

# =============================================================================
# UTILITAIRES PREMIERS (sympy)
# =============================================================================

def _est_premier(m: int) -> bool:
    if m < 2:
        return False
    return isprime(m)


def _nieme_premier(pos: int) -> int:
    """Retourne le pos-ieme premier via sympy.prime(). Utilise seulement si n != 10."""
    if pos < 1:
        return 0
    return prime(pos)


def _position_dans_P(p: int) -> int:
    """Position 1-based de p dans P via sympy.primepi(). Utilise seulement si n != 10."""
    if not _est_premier(p):
        return 0
    return int(primepi(p))


def _valider_k(k: int, k_max: int = K_MAX_RECORD) -> None:
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError(f"k doit etre un entier, recu : {type(k).__name__}")
    if k < K_MIN:
        raise ValueError(f"k doit etre >= {K_MIN}, recu : {k}")
    if k > k_max:
        raise ValueError(
            f"k={k} depasse K_MAX_RECORD={k_max:,}. "
            "Utilisez k_max_override pour depasser cette limite."
        )


def plage_k(k_debut: int, k_fin: int) -> List[int]:
    """Genere la liste des k entiers de k_debut a k_fin inclus."""
    if k_debut < K_MIN:
        raise ValueError(f"k_debut doit etre >= {K_MIN}")
    if k_fin < k_debut:
        raise ValueError(f"k_fin ({k_fin}) < k_debut ({k_debut})")
    return list(range(k_debut, k_fin + 1))


# =============================================================================
# STRUCTURES DE DONNEES
# =============================================================================

@dataclass
class ResultatRatioUnique:
    k: int
    n: int
    typique: bool
    somme_A: int
    somme_B: int
    premier_ancre_n10: Optional[int]
    premier_n: Optional[int]
    digamma_calcule: Optional[int]
    position_dans_P: Optional[int]
    reconstruction_reussie: bool
    ancrage_dynamique: bool = False
    message: str = ""
    candidats_ancre_n10: List[Tuple[int, int, int]] = field(default_factory=list)

    def __repr__(self):
        s   = "OK" if self.reconstruction_reussie else "ECHEC"
        dyn = " [DYN]" if self.ancrage_dynamique else ""
        return f"Ratio1/k(k={self.k}, n={self.n}, P={self.premier_n}, {s}{dyn})"


@dataclass
class ResultatMultiRatio:
    n: int
    liste_k: List[int]
    resultats: Dict[int, ResultatRatioUnique] = field(default_factory=dict)

    @property
    def premiers_trouves(self) -> Dict[int, Optional[int]]:
        return {k: r.premier_n for k, r in self.resultats.items()}

    @property
    def succes_total(self) -> bool:
        return all(r.reconstruction_reussie for r in self.resultats.values())

    @property
    def nb_succes(self) -> int:
        return sum(1 for r in self.resultats.values() if r.reconstruction_reussie)

    def rapport_texte(self) -> str:
        sep = "=" * 80
        L = [sep]
        L.append(
            f" REQUETE MULTI-RATIO v7.9 | n={self.n} "
            f"| {len(self.liste_k)} rapport(s) 1/k"
            f" | k_min={min(self.liste_k)} k_max={max(self.liste_k)}"
        )
        L.append(sep)
        for k, r in self.resultats.items():
            tag = "typique" if r.typique else "non typique"
            st  = "PREMIER TROUVE" if r.reconstruction_reussie else "ECHEC"
            dyn = " [DYN]" if r.ancrage_dynamique else ""
            L.append(
                f"  1/{k:<14} ({tag:<11}){dyn} | "
                f"ancre={r.premier_ancre_n10} | "
                f"P(n={r.n})={r.premier_n} | [{st}]"
            )
            if r.message:
                L.append(f"    Note: {r.message}")
        L.append(sep)
        L.append(
            f" Succes : {self.nb_succes}/{len(self.liste_k)} | "
            f"Global : {'OUI' if self.succes_total else 'PARTIEL/ECHEC'}"
        )
        L.append(sep)
        return "\n".join(L)

    def tableau_texte(self) -> str:
        sep = "-" * 128
        L = [f"Tableau comparatif v7.9 - n={self.n}", sep,
             f"{'Rapport':>16} | {'Type':>11} | {'Ancre n=10':>16} | "
             f"{'P(n)':>16} | {'Digamma':>18} | {'Statut':>10} | "
             f"{'Branches premières':<54} | Src",
             sep]
        for k, r in self.resultats.items():
            t   = "typique" if r.typique else "non typique"
            a   = str(r.premier_ancre_n10) if r.premier_ancre_n10 is not None else "ECHEC"
            p   = str(r.premier_n)         if r.premier_n          is not None else "ECHEC"
            d   = str(r.digamma_calcule)   if r.digamma_calcule     is not None else "?"
            src = "DYN" if r.ancrage_dynamique else "REF"
            statut = (
                "AMBIGU" if len(r.candidats_ancre_n10) > 1 and r.ancrage_dynamique
                else "CATALOGUE" if len(r.candidats_ancre_n10) > 1
                else "UNIQUE" if r.candidats_ancre_n10
                else "ABSENT"
            )
            branches = ", ".join(
                f"A({pos}){'+' if signe > 0 else '-'}={premier}"
                for pos, signe, premier in r.candidats_ancre_n10
            ) or "-"
            L.append(
                f"{'1/'+str(k):>16} | {t:>11} | {a:>16} | "
                f"{p:>16} | {d:>18} | {statut:>10} | "
                f"{branches:<54} | {src}"
            )
        L.append(sep)
        return "\n".join(L)


# =============================================================================
# DISPATCHER PRINCIPAL
# =============================================================================

class MultiRatioDispatcher:
    """
    Dispatcher multi-rapports 1/k pour une valeur de n commune.

    v7.9 : raccourci O(1) pour n=10 (primepi/prime JAMAIS appeles pour n=10).

    Usage:
        # k=2..9 classiques - instantane
        res = MultiRatioDispatcher().requete(n=10)

        # k=985..1001 - quelques secondes grace au raccourci n=10
        res = MultiRatioDispatcher(verbose=True).requete(n=10, liste_k=plage_k(985, 1001))

        # n != 10 - primepi utilise normalement
        res = MultiRatioDispatcher().requete(n=12, liste_k=[2, 10, 100])
    """

    def __init__(self, verbose: bool = False, k_max_override: Optional[int] = None):
        self.verbose = verbose
        self.k_max   = k_max_override if k_max_override is not None else K_MAX_RECORD
        self._cache_ancres: Dict[int, List[Tuple[int, int, int]]] = {}

    def requete(self, n: int, liste_k: Optional[List[int]] = None) -> ResultatMultiRatio:
        valider_n(n)
        if liste_k is None:
            liste_k = K_TOUS
        else:
            for k in liste_k:
                _valider_k(k, self.k_max)
        res = ResultatMultiRatio(n=n, liste_k=list(liste_k))
        for k in liste_k:
            r = self._traiter_ratio(k=k, n=n)
            res.resultats[k] = r
            if self.verbose:
                print(r)
        return res

    def requete_plage(self, n: int, k_debut: int = 2, k_fin: int = 9) -> ResultatMultiRatio:
        return self.requete(n=n, liste_k=plage_k(k_debut, k_fin))

    def _traiter_ratio(self, k: int, n: int) -> ResultatRatioUnique:
        typique           = (k == K_TYPIQUE)
        ancrage_dynamique = k not in ANCHORS_N10

        try:
            calc   = CalculateurNiveau1Entiers(k=k)
            res_n  = calc.calculer(n)
            res_10 = calc.calculer(10)
        except Exception as exc:
            return ResultatRatioUnique(
                k=k, n=n, typique=typique,
                somme_A=0, somme_B=0,
                premier_ancre_n10=None, premier_n=None,
                digamma_calcule=None, position_dans_P=None,
                reconstruction_reussie=False,
                ancrage_dynamique=ancrage_dynamique,
                message=f"Erreur calculateur : {exc}",
            )

        candidats_ancre = self._ancre_n10_cached(k=k, res_10=res_10)
        premier_ancre = None
        premier_n = digamma_n = position = None
        message = ""

        if k in ANCHORS_N10:
            ancre_catalogue = ANCHORS_N10[k]
            if any(premier == ancre_catalogue for _, _, premier in candidats_ancre):
                premier_ancre = ancre_catalogue
                if len(candidats_ancre) > 1:
                    branches = ", ".join(
                        f"A({pos}){'+' if signe > 0 else '-'}={premier}"
                        for pos, signe, premier in candidats_ancre
                    )
                    message = (
                        f"Ancrage du catalogue sélectionné explicitement : "
                        f"{ancre_catalogue}; {len(candidats_ancre)} candidats "
                        f"premiers sont conservés ({branches})."
                    )
            else:
                message = (
                    f"Ancre de catalogue {ancre_catalogue} absente des "
                    f"candidats premiers calculés pour k={k}."
                )
        elif len(candidats_ancre) == 1:
            premier_ancre = candidats_ancre[0][2]
        elif len(candidats_ancre) > 1:
            branches = ", ".join(
                f"A({pos}){'+' if signe > 0 else '-'}={premier}"
                for pos, signe, premier in candidats_ancre
            )
            message = (
                f"Ancrage ambigu : {len(candidats_ancre)} candidats premiers "
                f"({branches}); confirmation requise."
            )
        elif not candidats_ancre and not typique:
            message = "Aucun candidat premier parmi les quatre essais Digamma."

        if typique:
            # Rapport 1/2 : n = position dans P
            if n == 10:
                # RACCOURCI O(1) : prime(10) = 29 = ancre
                premier_n = premier_ancre
                position  = n
            else:
                premier_n = _nieme_premier(n)
                position  = n
            if premier_n is not None:
                digamma_n = res_n.somme_B - premier_n * (k ** 6)
        else:
            if premier_ancre is not None:
                if n == 10:
                    # ============================================================
                    # RACCOURCI CRITIQUE v7.9 - O(1) pour n=10
                    # pos_n = pos_ancre + (10-10) = pos_ancre
                    # prime(pos_ancre) = premier_ancre  <- direct, sans primepi !
                    # ============================================================
                    premier_n = premier_ancre
                    position  = None   # pos_ancre non calcule (non necessaire)
                    digamma_n = res_n.somme_B - premier_n * (k ** 6)
                else:
                    # n != 10 : calcul complet via primepi + prime
                    pos_ancre = _position_dans_P(premier_ancre)
                    if pos_ancre == 0:
                        message = f"Ancre {premier_ancre} introuvable dans P."
                    else:
                        pos_n = pos_ancre + (n - 10)
                        if pos_n >= 1:
                            premier_n = _nieme_premier(pos_n)
                            digamma_n = res_n.somme_B - premier_n * (k ** 6)
                            position  = pos_n
                        else:
                            message = (
                                f"n={n} trop petit "
                                f"(rang ancre={pos_ancre} a n=10)."
                            )
            else:
                if not candidats_ancre and not message:
                    message = f"Ancrage n=10 echoue pour k={k} (4 Digamma testes)."

        ok = premier_n is not None and _est_premier(premier_n)
        return ResultatRatioUnique(
            k=k, n=n, typique=typique,
            somme_A=res_n.somme_A, somme_B=res_n.somme_B,
            premier_ancre_n10=premier_ancre, premier_n=premier_n,
            digamma_calcule=digamma_n, position_dans_P=position,
            reconstruction_reussie=ok,
            ancrage_dynamique=ancrage_dynamique,
            message=message,
            candidats_ancre_n10=candidats_ancre,
        )

    def _ancre_n10_cached(self, k: int, res_10) -> List[Tuple[int, int, int]]:
        if k in self._cache_ancres:
            return self._cache_ancres[k]
        candidats = self._candidats_ancre_n10(k=k, res_10=res_10)
        self._cache_ancres[k] = candidats
        return candidats

    def _candidats_ancre_n10(self, k: int, res_10) -> List[Tuple[int, int, int]]:
        k6 = k ** 6
        candidats = []
        for (pos_exp, signe) in ORDRE_DIGAMMA:
            try:
                digamma = res_10.somme_A + signe * (k ** pos_exp)
                num     = res_10.somme_B - digamma
                if k6 != 0 and num % k6 == 0:
                    P = num // k6
                    if P > 1 and _est_premier(P):
                        candidats.append((pos_exp, signe, P))
            except (OverflowError, ZeroDivisionError):
                continue
        return candidats

    def tableau_comparatif(self, n: int, liste_k: Optional[List[int]] = None) -> str:
        return self.requete(n=n, liste_k=liste_k).tableau_texte()


# =============================================================================
# FONCTIONS PUBLIQUES
# =============================================================================

def requete_multi_k(
    n: int,
    liste_k: Optional[List[int]] = None,
    k_max_override: Optional[int] = None,
) -> ResultatMultiRatio:
    return MultiRatioDispatcher(k_max_override=k_max_override).requete(
        n=n, liste_k=liste_k
    )


def requete_plage_k(n: int, k_debut: int = 2, k_fin: int = 9) -> ResultatMultiRatio:
    return MultiRatioDispatcher().requete_plage(n=n, k_debut=k_debut, k_fin=k_fin)


def tableau_multi_k(n: int, liste_k: Optional[List[int]] = None) -> str:
    return MultiRatioDispatcher().tableau_comparatif(n=n, liste_k=liste_k)


if __name__ == "__main__":
    import sys, io, time
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

    print("\n" + "=" * 80)
    print("  MULTI-RATIO DISPATCHER v7.9 - Raccourci O(1) pour n=10")
    print(f"  K_MAX_RECORD = {K_MAX_RECORD:,}")
    print("=" * 80)

    t0 = time.time()
    print("\n--- k=985..1001, n=10 (doit etre < 5 secondes) ---")
    res = MultiRatioDispatcher(verbose=True).requete(n=10, liste_k=plage_k(985, 1001))
    print(res.rapport_texte())
    print(f"Temps : {time.time()-t0:.2f} sec")
