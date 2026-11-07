#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FALLBACK GÉOMÉTRIQUE — Gabriel Multiloop v7.4
==============================================

Gestionnaire du mécanisme de seconde tentative géométrique.

LOGIQUE DE FALLBACK :
  1. L'agent tente d'abord la reconstruction via l'approche ALGÉBRIQUE
     (suites A et B à termes entiers + 4 possibilités Digamma).
  2. Si AUCUN premier n'est reconstruit via les 4 Digamma → FALLBACK.
  3. L'agent RELANCE automatiquement la reconstruction via l'approche
     GÉOMÉTRIQUE (suites A et B modèle géométrique, termes hypoténuse).
  4. Le résultat est journalisé dans DiagnosticFallback.

Ce module s'intercale dans le pipeline cognitif de Gabriel entre
l'étape de reconstruction algébrique et la réponse finale.

Auteur : Gabriel Multiloop — Extension géométrique Philippe Savard 2026
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple, Union

try:
    from .Suites_geometriques_AB import (
    CalculateurSuitesGeometriques,
    DiagnosticFallback,
    ExtracteurPremiersGeometriques,
    PipelineSuitesGeometriques,
    ResultatSuiteGeo,
    declencher_fallback_geometrique,
)
except ImportError:  # execution directe du script
    from Suites_geometriques_AB import (
    CalculateurSuitesGeometriques,
    DiagnosticFallback,
    ExtracteurPremiersGeometriques,
    PipelineSuitesGeometriques,
    ResultatSuiteGeo,
    declencher_fallback_geometrique,
)


# ============================================================
# TYPES D'APPROCHE
# ============================================================

class TypeApproche:
    ALGEBRIQUE = "algebrique"      # Suites A/B à termes entiers + Digamma
    GEOMETRIQUE = "geometrique"    # Suites A/B modèle géométrique (hypoténuse)


# ============================================================
# RÉSULTAT UNIFIÉ
# ============================================================

@dataclass
class ResultatReconstruction:
    """
    Résultat unifié après application de l'approche algébrique
    et éventuellement du fallback géométrique.
    """
    n: int
    k: Union[int, float]

    # Résultats algébriques (fournis par le pipeline existant)
    premiers_algebriques: List[int] = field(default_factory=list)
    digamma_reussi: bool = False

    # Résultats géométriques (fallback)
    fallback_declenche: bool = False
    diagnostic_geo: Optional[DiagnosticFallback] = None
    premiers_geometriques: List[int] = field(default_factory=list)

    # Résultat final (union des deux approches)
    premiers_finals: List[int] = field(default_factory=list)
    approche_finale: str = TypeApproche.ALGEBRIQUE
    reconstruction_reussie: bool = False

    # Métriques
    temps_algebrique_ms: float = 0.0
    temps_geometrique_ms: float = 0.0
    timestamp: str = ""

    def __repr__(self) -> str:
        approche = self.approche_finale
        statut = "✓" if self.reconstruction_reussie else "✗"
        fallback = " [+fallback géo]" if self.fallback_declenche else ""
        return (
            f"ResultatReconstruction(n={self.n}, k={self.k}, "
            f"{statut} approche={approche}{fallback}, "
            f"premiers={self.premiers_finals})"
        )


# ============================================================
# GESTIONNAIRE DE FALLBACK
# ============================================================

class GestionnaireFallbackGeometrique:
    """
    Orchestre le double mécanisme de reconstruction :
      1. Approche algébrique (méthode existante, inchangée)
      2. Fallback géométrique (déclenchement automatique si échec)

    Intégration dans le pipeline cognitif de Gabriel :

        gestionnaire = GestionnaireFallbackGeometrique(k=2)
        resultat = gestionnaire.reconstruire(
            n=n,
            fn_algebrique=ma_fonction_digamma_existante
        )
        if resultat.reconstruction_reussie:
            premiers = resultat.premiers_finals

    La fonction fn_algebrique est votre pipeline existant (Digamma).
    Elle doit retourner List[int] (liste de premiers, vide si échec).
    """

    def __init__(self, k: Union[int, float] = 2, verbose: bool = False):
        self.k = k
        self.verbose = verbose
        self.pipeline_geo = PipelineSuitesGeometriques(k_typique=k)
        self._historique: List[ResultatReconstruction] = []

    # ----------------------------------------------------------
    # POINT D'ENTRÉE PRINCIPAL
    # ----------------------------------------------------------

    def reconstruire(
        self,
        n: int,
        fn_algebrique: Callable[[int], List[int]],
        k_override: Optional[Union[int, float]] = None,
    ) -> ResultatReconstruction:
        """
        Tente la reconstruction des premiers pour la valeur n.

        Étape 1 : appel de fn_algebrique(n) — approche existante.
        Étape 2 : si aucun premier trouvé → fallback géométrique.

        Paramètres
        ----------
        n : int
            Valeur de n à traiter.
        fn_algebrique : Callable[[int], List[int]]
            Votre fonction existante de reconstruction algébrique
            (suites A/B entières + 4 Digamma). Doit retourner
            une liste d'entiers premiers (vide si échec).
        k_override : int ou float, optionnel
            Surcharge le rapport k pour ce calcul spécifique.

        Retourne
        --------
        ResultatReconstruction complet.
        """
        k = k_override if k_override is not None else self.k
        res = ResultatReconstruction(
            n=n,
            k=k,
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
        )

        # ── ÉTAPE 1 : Approche algébrique ──────────────────────
        t0 = time.perf_counter()
        try:
            premiers_alg = fn_algebrique(n)
        except Exception as exc:
            premiers_alg = []
            if self.verbose:
                print(f"  [FallbackGeo] Erreur algébrique pour n={n}: {exc}")
        res.temps_algebrique_ms = (time.perf_counter() - t0) * 1000
        res.premiers_algebriques = premiers_alg
        res.digamma_reussi = len(premiers_alg) > 0

        if res.digamma_reussi:
            # Succès algébrique → pas de fallback nécessaire
            res.premiers_finals = premiers_alg
            res.approche_finale = TypeApproche.ALGEBRIQUE
            res.reconstruction_reussie = True
            if self.verbose:
                print(f"  [FallbackGeo] n={n} ✓ Algébrique: {premiers_alg}")
            self._historique.append(res)
            return res

        # ── ÉTAPE 2 : Fallback géométrique ─────────────────────
        if self.verbose:
            print(f"  [FallbackGeo] n={n} ✗ Algébrique échoué → Déclenchement fallback géométrique")

        res.fallback_declenche = True
        t1 = time.perf_counter()

        diag = declencher_fallback_geometrique(n=n, k=k, verbose=self.verbose)

        res.temps_geometrique_ms = (time.perf_counter() - t1) * 1000
        res.diagnostic_geo = diag
        res.premiers_geometriques = diag.premiers_trouves

        if diag.premiers_trouves:
            res.premiers_finals = diag.premiers_trouves
            res.approche_finale = TypeApproche.GEOMETRIQUE
            res.reconstruction_reussie = True
            if self.verbose:
                print(f"  [FallbackGeo] n={n} ✓ Géométrique: {diag.premiers_trouves}")
        else:
            res.premiers_finals = []
            res.approche_finale = TypeApproche.GEOMETRIQUE
            res.reconstruction_reussie = False
            if self.verbose:
                print(f"  [FallbackGeo] n={n} ✗ Les deux approches ont échoué")

        self._historique.append(res)
        return res

    # ----------------------------------------------------------
    # TRAITEMENT EN LOT (POUR ENSEMBLE DE n)
    # ----------------------------------------------------------

    def reconstruire_batch(
        self,
        n_values: List[int],
        fn_algebrique: Callable[[int], List[int]],
        k_override: Optional[Union[int, float]] = None,
    ) -> Dict[int, ResultatReconstruction]:
        """
        Applique le double mécanisme pour une liste de valeurs de n.

        Retourne un dict {n: ResultatReconstruction}.
        """
        return {
            n: self.reconstruire(n, fn_algebrique, k_override)
            for n in n_values
        }

    # ----------------------------------------------------------
    # RAPPORT DE SESSION
    # ----------------------------------------------------------

    def rapport_session(self) -> str:
        """
        Génère un rapport de la session courante :
        combien de fois l'algébrique a réussi / échoué,
        combien de fois le fallback géométrique a sauvé la mise.
        """
        total = len(self._historique)
        if total == 0:
            return "Aucune reconstruction effectuée dans cette session."

        alg_ok = sum(1 for r in self._historique if r.digamma_reussi)
        fallback_ok = sum(1 for r in self._historique
                          if r.fallback_declenche and r.reconstruction_reussie)
        fallback_echec = sum(1 for r in self._historique
                             if r.fallback_declenche and not r.reconstruction_reussie)
        total_ok = sum(1 for r in self._historique if r.reconstruction_reussie)

        lignes = [
            "=" * 60,
            "  RAPPORT SESSION — Fallback Géométrique Gabriel v7.4",
            "=" * 60,
            f"  Total reconstructions tentées : {total}",
            f"  Succès algébriques (Digamma)   : {alg_ok}/{total}",
            f"  Fallbacks géométriques déclenchés : {total - alg_ok}",
            f"    → Succès via géométrique      : {fallback_ok}",
            f"    → Échecs les deux approches   : {fallback_echec}",
            f"  TOTAL succès globaux            : {total_ok}/{total}",
            "=" * 60,
            "",
            "  Détail par n :",
        ]

        for r in self._historique:
            fb = " ↳ fallback géo ✓" if (r.fallback_declenche and r.reconstruction_reussie) else \
                 " ↳ fallback géo ✗" if r.fallback_declenche else ""
            statut = "✓" if r.reconstruction_reussie else "✗"
            lignes.append(
                f"    {statut} n={r.n:3d} | k={r.k} | "
                f"premiers={r.premiers_finals[:5]} "
                f"| t_alg={r.temps_algebrique_ms:.1f}ms "
                f"| t_geo={r.temps_geometrique_ms:.1f}ms{fb}"
            )

        return "\n".join(lignes)


# ============================================================
# INTÉGRATION DANS gabriel_geometric_wrapper.py
# ============================================================

# Exemple d'utilisation dans gabriel_geometric_wrapper.py :
#
#   from src.core.fallback_geometrique import GestionnaireFallbackGeometrique
#
#   gestionnaire = GestionnaireFallbackGeometrique(k=2, verbose=True)
#
#   # fn_digamma = votre fonction existante de reconstruction algébrique
#   def fn_digamma(n: int) -> list:
#       return pipeline_digamma_existant.reconstruire(n)  # retourne [] si échec
#
#   for n in range(2, 100):
#       resultat = gestionnaire.reconstruire(n, fn_digamma)
#       premiers = resultat.premiers_finals
#       approche = resultat.approche_finale
#
#   print(gestionnaire.rapport_session())


# ============================================================
# DÉMO / TEST AUTONOME
# ============================================================

def demo():
    """Démontre le mécanisme de fallback avec une fonction simulée."""

    print("\n" + "=" * 60)
    print("  DÉMO — Fallback Géométrique Gabriel v7.4")
    print("=" * 60)

    # Simuler une fonction algébrique qui réussit pour certains n
    # et échoue pour d'autres (simulation réaliste)
    PREMIERS_CONNUS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}

    def fn_algebrique_simulee(n: int) -> List[int]:
        """Simule l'approche Digamma : réussit sur n pairs, échoue sur n impairs."""
        if n % 2 == 0:  # simulation : réussit pour n pair
            candidats = [p for p in PREMIERS_CONNUS if p <= n + 5]
            return candidats[:2] if candidats else []
        return []  # simulation : échec pour n impair → fallback déclenché

    gestionnaire = GestionnaireFallbackGeometrique(k=2, verbose=True)

    print("\n  Test sur n = 2 à 12 :")
    print("  (n pair → algébrique réussit | n impair → fallback géométrique)")
    print()

    for n in range(2, 13):
        res = gestionnaire.reconstruire(n=n, fn_algebrique=fn_algebrique_simulee)
        print(f"  → {res}")

    print()
    print(gestionnaire.rapport_session())


if __name__ == "__main__":
    demo()
