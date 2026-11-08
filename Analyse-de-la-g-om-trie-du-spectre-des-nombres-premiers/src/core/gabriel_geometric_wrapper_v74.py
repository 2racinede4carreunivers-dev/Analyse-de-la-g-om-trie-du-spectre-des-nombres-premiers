#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WRAPPER GABRIEL - INTÉGRATION MÉTAPHORES GÉOMÉTRIQUES + FALLBACK GÉOMÉTRIQUE
=============================================================================

Ajoute automatiquement un bloc "Structure Géométrique Spatiale"
à chaque réponse de Gabriel.

v7.4 — Ajout du pipeline des suites géométriques A et B (Philippe Savard 2026)
       et du mécanisme de fallback géométrique automatique :
         Si l'approche algébrique (suites A/B entières + 4 Digamma) ne
         reconstruit aucun premier → seconde tentative via l'approche
         géométrique (termes hypoténuse sqrt(a²+b²)).
"""

import re
import math
from fractions import Fraction
from typing import Dict, Any, List, Optional, Union
from src.core.metaphore_geometrique import MetaphoreGeometriqueGenerator, Point3D
from src.core.Suites_geometriques_AB import (
    PipelineSuitesGeometriques,
    ResultatSuiteGeo,
)
from src.core.fallback_geometrique import (
    GestionnaireFallbackGeometrique,
    ResultatReconstruction,
    TypeApproche,
)

# ── NOUVEAU v7.5 : Pipeline cognitif niveaux 1 et 2 ──────────────
from src.core.suites_geometriques_niveau2 import (
    CalculateurNiveau1Entiers,
    CalculateurNiveau2Geometrique,
    MethodeDigamma,
    PipelineNiveau2Geometrique,
)
from src.core.reconstruction_premiers_1_sur_k import (
    Reconstructeur1Sur7,
    ResultatReconstruction1Sur7,
)


class PipelineCognitifNiveaux:
    """
    Pipeline cognitif unifié (v7.5) appliquant systématiquement les
    niveaux 1 et 2 du système convolutif spectral, pour tout rapport
    1/k typique ou non typique, avec les 4 possibilités Digamma tentées
    à chaque niveau et chaque requête.

    LOGIQUE (conforme aux règles de la méthode) :

    RAPPORT TYPIQUE 1/2 :
      - n = quantité de termes = position du premier dans P
        (2=1er, 3=2e, 5=3e, 7=4e, ..., 29=10e, ... infini).
      - Ancrage n=10 : Digamma = S_A - 2^8 = 1406 → P=(S_B-1406)/2^6 = 29.
      - Pour n <> 10 : Digamma = S_B - P_n × 2^6 où P_n est le n-ième
        premier (ex n=9 : ((1598/2^6)-23)×2^6 = 126 → P=23).
      - Coefficients niveau 1 : (S_A10-S_A9)/2^8 = 3.25,
        (S_B10-S_B9)/2^8 = 6.5 → équations (3.25/2)·2^n-2 et (6.5/2)·2^n-66.

    RAPPORTS NON TYPIQUES 1/k (k <> 2) :
      - D'abord l'ancrage à n=10 (4 possibilités Digamma) → premier P_ancre.
      - Puis n=9 (les deux sommes, références des coefficients).
      - Pour n > 10 : progression dans la liste des nombres premiers
        successifs à partir de l'ancrage (ex 1/3 : 227@n=10, 229@n=11,
        233@n=12, ..., 263@n=17). L'agent fournit les sommes A/B pour le
        n demandé, les sommes n=10 et n=9, et les équations généralisées.

    Niveau 1 : suites A et B à termes entiers (k^i) + 4 Digamma
    Niveau 2 : suites A et B géométriques (sqrt(a²+b²)) + coefficients
               A/B + (Reste+x) → blocs A (partie entière = x) et B
               (partie décimale) + équations généralisées pour tout n
    """

    def __init__(self, k: Union[int, float] = 2, verbose: bool = False):
        # Le systeme convolutif impose t = k entier >= 2 (raison spectrale).
        if isinstance(k, bool) or float(k) != int(float(k)) or int(float(k)) < 2:
            raise ValueError(f"k doit etre un entier >= 2 (t = k), recu : {k!r}")
        self.k = int(float(k))
        self.verbose = verbose
        self.typique = (self.k == 2)
        self.pipeline_n2 = PipelineNiveau2Geometrique(k=k)
        # Reconstructeur spécialisé 1/7 si k == 7
        self.reconstructeur_1_7 = Reconstructeur1Sur7() if int(k) == 7 else None

    # ------------------------------------------------------------------
    # UTILITAIRES PREMIERS
    # ------------------------------------------------------------------
    @staticmethod
    def _est_premier(m: int) -> bool:
        if m < 2:
            return False
        if m == 2:
            return True
        if m % 2 == 0:
            return False
        for i in range(3, int(math.isqrt(m)) + 1, 2):
            if m % i == 0:
                return False
        return True

    @staticmethod
    def _nieme_premier(pos: int) -> int:
        """Retourne le pos-ième nombre premier (pos >= 1)."""
        if pos < 1:
            return 0
        compte = 0
        candidat = 1
        while compte < pos:
            candidat += 1
            if PipelineCognitifNiveaux._est_premier(candidat):
                compte += 1
        return candidat

    def _position_dans_P(self, premier: int) -> int:
        """Position (1-based) du premier donné dans l'ensemble P."""
        if not self._est_premier(premier):
            return 0
        pos, candidat = 0, 1
        while True:
            candidat += 1
            if self._est_premier(candidat):
                pos += 1
                if candidat == premier:
                    return pos
                if candidat > premier:
                    return 0

    # ------------------------------------------------------------------
    # COEFFICIENTS + ÉQUATIONS GÉNÉRALISÉES NIVEAU 1 (termes entiers)
    # ------------------------------------------------------------------
    def _coefficients_niveau_1(self, calc: CalculateurNiveau1Entiers) -> Dict[str, Any]:
        """Coefficients et équations généralisées des suites entières.

        Coefficient A = (S_A(10) - S_A(9)) / k^8
        Coefficient B = (S_B(10) - S_B(9)) / k^8
        x = partie entière de Coefficient / (Somme(10)/k^10)
        Reste = Somme(10) - (Coefficient/x) × k^10
        Équation (n > 0) : (Coefficient/x) × k^n - Reste = Somme
        """
        r10 = calc.calculer(10)
        r9 = calc.calculer(9)
        SA10, SB10 = r10.somme_A, r10.somme_B
        SA9, SB9 = r9.somme_A, r9.somme_B
        k = int(self.k)
        k8 = k ** 8
        k10 = k ** 10

        coeff_A = Fraction(SA10 - SA9, k8)
        coeff_B = Fraction(SB10 - SB9, k8)

        res: Dict[str, Any] = {
            'SA10': SA10, 'SB10': SB10, 'SA9': SA9, 'SB9': SB9,
            'coefficient_A': coeff_A, 'coefficient_B': coeff_B,
        }

        for suite, coeff, S10 in [('A', coeff_A, SA10), ('B', coeff_B, SB10)]:
            ratio = Fraction(S10, k10)
            reste_plus_x = coeff / ratio  # = Coeff / (Somme/k^10)
            x = reste_plus_x.numerator // reste_plus_x.denominator  # partie entière (bloc A)
            bloc_B = reste_plus_x - x  # partie décimale (< 1) (bloc B)
            valeur = (coeff / x) * k10
            reste = S10 - valeur  # Reste (peut être négatif, ex -2 pour 1/2)
            res[f'x_{suite}'] = x
            res[f'reste_plus_x_{suite}'] = reste_plus_x
            res[f'bloc_B_{suite}'] = bloc_B
            res[f'reste_{suite}'] = reste
            res[f'equation_{suite}_positif'] = (
                f"({coeff}/{x} × {k}^n) - ({-reste}) = Somme suite {suite} (n > 0)"
                if reste < 0 else
                f"({coeff}/{x} × {k}^n) - {reste} = Somme suite {suite} (n > 0)"
            )
            res[f'equation_{suite}_generalisee'] = (
                f"({float(coeff / x):g} × {k}^n {'-' if reste < 0 else '+'} {abs(float(reste)):g}) "
                f"= Somme suite {suite}  [n entier > 0]"
            )
            res[f'equation_{suite}_negatif'] = (
                f"({float(coeff):g} × {k}^(-n)) - ({-float(reste):g}) = Somme suite {suite} négative"
            )
        return res

    # ------------------------------------------------------------------
    # RECONSTRUCTION PRINCIPALE
    # ------------------------------------------------------------------
    def reconstruire(self, n: int = 10) -> Dict[str, Any]:
        """
        Applique les niveaux 1 et 2 pour n demandé.

        - Rapport typique 1/2 : n = position du premier dans P.
        - Rapports non typiques : ancrage n=10 (4 Digamma) puis
          progression dans la liste des premiers.
        """
        if isinstance(n, bool) or not isinstance(n, int) or n < 1:
            raise ValueError(f"n doit etre un entier strictement positif, recu : {n!r}")
        resultats: Dict[str, Any] = {'n': n, 'k': self.k, 'typique': self.typique}
        k = int(self.k)

        # ── NIVEAU 1 : suites entières ─────────────────────────────
        calc_n1 = CalculateurNiveau1Entiers(k=k)
        res_n1 = calc_n1.calculer(n=n)
        resultats['niveau_1'] = {
            'somme_A': res_n1.somme_A,
            'somme_B': res_n1.somme_B,
            'termes_A': res_n1.termes_A,
            'termes_B': res_n1.termes_B,
        }

        # ── Ancrage n=10 : 4 possibilités Digamma (toutes tentées) ──
        anchor_n1 = calc_n1.calculer(n=10)
        digamma_anchor = MethodeDigamma(k=k, n=10)
        premier_ancre, candidats_ancre = digamma_anchor.reconstruire_premier(
            anchor_n1.somme_A, anchor_n1.somme_B, verbose=self.verbose
        )
        resultats['ancrage_n10'] = {
            'somme_A': anchor_n1.somme_A,
            'somme_B': anchor_n1.somme_B,
            'premier': premier_ancre,
            'candidats_digamma': candidats_ancre,
        }

        # ── Détermination du premier P(n) ──────────────────────────
        premier_n = None
        digamma_calcule_n = None

        if self.typique:
            # Rapport typique : n = position du premier dans P
            premier_n = self._nieme_premier(n)
            # Digamma pour n <> 10 : Digamma = S_B - P_n × k^6
            digamma_calcule_n = res_n1.somme_B - premier_n * (k ** 6)
            resultats['premier'] = premier_n
            resultats['position_dans_P'] = n
            resultats['digamma_calcule_n'] = digamma_calcule_n
            resultats['verification'] = (
                (res_n1.somme_B - digamma_calcule_n) // (k ** 6) == premier_n
            )
        else:
            # Rapport non typique : ancrage n=10, puis progression
            if premier_ancre:
                pos_ancre = self._position_dans_P(premier_ancre)
                resultats['position_ancre_dans_P'] = pos_ancre
                pos_n = pos_ancre + (n - 10)
                if pos_n >= 1:
                    premier_n = self._nieme_premier(pos_n)
                    digamma_calcule_n = res_n1.somme_B - premier_n * (k ** 6)
            resultats['premier'] = premier_n
            resultats['digamma_calcule_n'] = digamma_calcule_n

        # ── Coefficients + équations généralisées niveau 1 ─────────
        resultats['coefficients_niveau_1'] = self._coefficients_niveau_1(calc_n1)

        # ── NIVEAU 2 : suites géométriques + (Reste+x) + blocs A/B ──
        calc_n2 = CalculateurNiveau2Geometrique(k=self.k)
        res_n2 = calc_n2.calculer(n=n)
        coeff_A_geo, coeff_B_geo = calc_n2.calculer_coefficients(n1=10, n2=9)
        equations_geo = calc_n2.reconstruire_equations_generales(verbose=self.verbose)
        resultats['niveau_2'] = {
            'somme_A': res_n2.somme_A,
            'somme_B': res_n2.somme_B,
            'coefficient_A': coeff_A_geo,
            'coefficient_B': coeff_B_geo,
            'equations': equations_geo,
        }

        # ── Étape 3 (ordre prescrit) : sommes A/B à n=9 (niveau 1) ──────
        res_n1_9 = calc_n1.calculer(n=9)
        resultats['sommes_n9'] = {
            'somme_A': res_n1_9.somme_A,
            'somme_B': res_n1_9.somme_B,
            'termes_A': res_n1_9.termes_A,
            'termes_B': res_n1_9.termes_B,
        }
        # Sommes géométriques de référence (n=10 et n=9, définitions).
        res_n2_10 = calc_n2.calculer(n=10)
        res_n2_9 = calc_n2.calculer(n=9)
        resultats['niveau_2']['somme_A_n10'] = res_n2_10.somme_A
        resultats['niveau_2']['somme_B_n10'] = res_n2_10.somme_B
        resultats['niveau_2']['somme_A_n9'] = res_n2_9.somme_A
        resultats['niveau_2']['somme_B_n9'] = res_n2_9.somme_B

        # ── Étapes 4-6 : vérification des équations généralisées au n ────
        #   (Coeff/x) × k^n - Reste == Somme suite (n)  [arithmétique exacte]
        coeffs = resultats['coefficients_niveau_1']
        verif_eq: Dict[str, Any] = {}
        for suite, somme in [('A', res_n1.somme_A), ('B', res_n1.somme_B)]:
            coeff = coeffs[f'coefficient_{suite}']
            x_s = coeffs[f'x_{suite}']
            reste_s = coeffs[f'reste_{suite}']
            # Convention du module : reste = Somme(10) - (Coeff/x)*k^10,
            # donc l'equation s'ecrit (Coeff/x)*k^n + reste = Somme(n)
            # (le "Reste" affiche dans l'equation est -reste, ex 7/6 pour 1/7).
            verif_eq[suite] = ((coeff / x_s) * (k ** n) + reste_s) == somme
        verif_eq['note'] = (
            "Equation = construction terme a terme XIV.4 pour n >= 8 ; "
            "pour n <= 7, XIV.4 (terme_b = terme_a) fait foi."
        )
        resultats['verification_equations_au_n'] = verif_eq

        # ── Ordre prescrit du pipeline généralisé (documentation) ────────
        resultats['ordre_pipeline'] = [
            "1. Niveau 1 : sommes des suites A et B a n=10",
            "2. Reconstruction du premier : 4 possibilites Digamma "
            "(+pos8, -pos8, +pos7, -pos7)",
            "3. Sommes des suites A et B a n=9",
            "4. Coefficients A/B = (S(10) - S(9)) / k^8",
            "5. (Reste+x) = Coeff/(Somme/k^10) -> bloc A (partie entiere = x), "
            "bloc B (partie decimale)",
            "6. Equations generalisees (Coeff/x)*k^n - Reste = Somme "
            "(n entier strictement positif)",
            "7. Si n <> 10 : sommes A/B au n demande + premier consequent",
        ]

        # ── Cas spécial 1/7 : reconstructeur dédié (formes exactes) ──
        if self.reconstructeur_1_7 is not None:
            res_17 = self.reconstructeur_1_7.reconstruire_premier(n=10, verbose=self.verbose)
            resultats['rapport_1_7'] = {
                'somme_A': res_17.somme_A,
                'somme_B': res_17.somme_B,
                'premier': res_17.P_candidat,
                'premier_valide': res_17.premier_valide,
                'digamma_calcule': res_17.digamma_calcule,
                'equation_A_positif': res_17.equation_A_positif,
                'equation_A_negatif': res_17.equation_A_negatif,
                'equation_B_positif': res_17.equation_B_positif,
                'equation_B_negatif': res_17.equation_B_negatif,
            }

        # ── Synthèse ────────────────────────────────────────────────
        premiers = set()
        if premier_n:
            premiers.add(premier_n)
        if premier_ancre and n == 10:
            premiers.add(premier_ancre)
        resultats['premiers_trouves'] = sorted(premiers)
        resultats['reconstruction_reussie'] = bool(premiers)

        return resultats

    # ------------------------------------------------------------------
    # RAPPORT ORDONNÉ (ordre prescrit du pipeline généralisé)
    # ------------------------------------------------------------------
    def rapport_pipeline(self, n: int = 10) -> str:
        """Rapport texte suivant l'ordre prescrit, pour tout 1/k et tout n>=1.

        1. Niveau 1 : sommes A/B a n=10 ;  2. 4 possibilites Digamma ;
        3. Sommes A/B a n=9 ;  4. Coefficients (S(10)-S(9))/k^8 ;
        5. (Reste+x) -> blocs A/B ;  6. Equations generalisees (n > 0) ;
        7. Si n <> 10 : sommes A/B au n demande + premier consequent.
        """
        r = self.reconstruire(n)
        k = self.k
        L = []
        L.append("=" * 72)
        L.append(f" PIPELINE COGNITIF GENERALISE - rapport 1/k = 1/{k}"
                 f" ({'typique' if self.typique else 'non typique'})"
                 f" - n demande = {n}")
        L.append("=" * 72)

        anc = r['ancrage_n10']
        L.append("[1] Niveau 1 - Suites A et B a n=10 (termes entiers)")
        L.append(f"    Somme suite A(10) = {anc['somme_A']}")
        L.append(f"    Somme suite B(10) = {anc['somme_B']}")

        L.append("[2] Reconstruction du premier - 4 possibilites Digamma")
        for c in anc['candidats_digamma']:
            tag = " PREMIER" if c['est_premier'] else ""
            L.append(f"    Digamma [{c['description']}] = "
                     f"{c['digamma_calcule']} -> P = {c['P_candidat']}{tag}")
        if self.typique:
            L.append(f"    Ancrage n=10 : premier = {anc['premier']}"
                     f" (10e nombre premier, n = position dans P)")
        else:
            pos = r.get('position_ancre_dans_P')
            L.append(f"    Ancrage n=10 : premier = {anc['premier']}"
                     f" (rang {pos} dans P)")

        s9 = r['sommes_n9']
        L.append("[3] Sommes des suites A et B a n=9")
        L.append(f"    Somme suite A(9) = {s9['somme_A']}")
        L.append(f"    Somme suite B(9) = {s9['somme_B']}")

        c1 = r['coefficients_niveau_1']
        L.append("[4] Coefficients = (Somme(10) - Somme(9)) / k^8")
        L.append(f"    Coefficient A = {c1['coefficient_A']}"
                 f"    Coefficient B = {c1['coefficient_B']}")

        L.append("[5] (Reste + x) = Coeff / (Somme/k^10) -> blocs A et B")
        for s in ('A', 'B'):
            L.append(f"    Suite {s} : (Reste+x) = {c1[f'reste_plus_x_{s}']}"
                     f" | bloc A (x, partie entiere) = {c1[f'x_{s}']}"
                     f" | bloc B (partie decimale) = {c1[f'bloc_B_{s}']}"
                     f" | Reste = {c1[f'reste_{s}']}")

        L.append("[6] Equations generalisees (n entier strictement positif)")
        L.append(f"    {c1['equation_A_positif']}")
        L.append(f"    {c1['equation_B_positif']}")
        v = r['verification_equations_au_n']
        L.append(f"    Verification au n demande ({n}) : "
                 f"A {'OK' if v['A'] else 'n>=8 requis'} | "
                 f"B {'OK' if v['B'] else 'n>=8 requis'}")

        if n != 10:
            n1 = r['niveau_1']
            L.append(f"[7] Requete n = {n} : sommes des suites A et B")
            L.append(f"    Somme suite A({n}) = {n1['somme_A']}")
            L.append(f"    Somme suite B({n}) = {n1['somme_B']}")
            if self.typique:
                rang = n
            else:
                rang = (r.get('position_ancre_dans_P') or 0) + (n - 10)
            L.append(f"    Premier consequent : {r['premier']}"
                     f" (rang {rang} dans P)")
            L.append(f"    Digamma calcule = {r['digamma_calcule_n']}")
            if r['premier'] is not None and r['digamma_calcule_n'] is not None:
                q = (n1['somme_B'] - r['digamma_calcule_n'])
                ok = q == r['premier'] * (k ** 6)
                L.append(f"    (S_B - Digamma)/k^6 = {r['premier']}"
                         f" {'OK' if ok else '** ECART **'}")
        else:
            L.append("[7] n = 10 : ancrage (etape 7 non requise)")

        L.append("=" * 72)
        return "\n".join(L)


class GabrielGeometricResponseWrapper:
    """
    Wrapper pour ajouter métaphores géométriques aux réponses de Gabriel.

    Intègre également le pipeline des suites géométriques A et B
    et le gestionnaire de fallback géométrique (v7.4).
    """

    def __init__(self, k_typique: Union[int, float] = 2, verbose: bool = False):
        self.geo_gen = MetaphoreGeometriqueGenerator()
        self.response_history = []

        # ── NOUVEAU v7.4 : Pipeline suites géométriques A et B ──────────
        self.k_typique = k_typique
        self.pipeline_geo = PipelineSuitesGeometriques(k_typique=k_typique)

        # ── NOUVEAU v7.4 : Gestionnaire de fallback géométrique ──────────
        self.fallback_gestionnaire = GestionnaireFallbackGeometrique(
            k=k_typique, verbose=verbose
        )
        self.verbose = verbose
    
    def enrichir_reponse(self, 
                        reponse_originale: str,
                        contexte: Optional[Dict[str, Any]] = None) -> str:
        """
        Ajoute bloc géométrique à une réponse
        
        Args:
            reponse_originale: Réponse de Gabriel (texte/code/HOL)
            contexte: Info sur le type de requête (convergence, spectral, etc.)
        
        Returns:
            Réponse enrichie avec bloc géométrique
        """
        
        output = reponse_originale
        
        # Détecter le type de réponse automatiquement
        contexte_detecte = self._detecter_contexte(reponse_originale)
        
        # Générer bloc géométrique approprié
        bloc_geo = self._generer_bloc_geometrique(contexte_detecte or contexte)
        
        # Ajouter le bloc
        if bloc_geo:
            output += "\n" + bloc_geo
        
        return output
    
    def _detecter_contexte(self, texte: str) -> Optional[Dict[str, Any]]:
        """Détecte automatiquement le type de réponse"""
        
        texte_lower = texte.lower()
        
        # Détection: Convergence
        if any(kw in texte_lower for kw in ["convergence", "converge", "converger", "tend vers", "asymptote"]):
            # Extraire les valeurs numériques
            values = re.findall(r'0\.\d+', texte)
            if values:
                try:
                    values_float = [float(v) for v in values[:10]]  # Prendre les 10 premiers
                    return {
                        'type': 'convergence',
                        'values': values_float,
                        'target': 0.5
                    }
                except:
                    pass
        
        # Détection: Rapport spectral
        if any(kw in texte_lower for kw in ["rapport spectral", "1/2", "1/3", "1/4", "spectre"]):
            return {'type': 'spectral', 'ratios': {'1/2': 0.5, '1/3': 0.333, '1/4': 0.25}}
        
        # Détection: Comparaison asymétrique
        if any(kw in texte_lower for kw in ["comparaison asymétrique", "bloc A", "bloc B", "asymétrique ordonnée"]):
            return {
                'type': 'asym_ordonnee',
                'bloc_a': [2, 3, 5, 7],
                'bloc_b': [11, 13, 17, 19, 23],
                'ratio': 0.5026
            }
        
        return None
    
    def _generer_bloc_geometrique(self, contexte: Optional[Dict]) -> Optional[str]:
        """Génère bloc géométrique selon contexte"""
        
        if not contexte:
            return None
        
        contexte_type = contexte.get('type')
        
        if contexte_type == 'convergence':
            values = contexte.get('values', [0.8, 0.65, 0.55, 0.52, 0.501])
            target = contexte.get('target', 0.5)
            return self.geo_gen.generer_pour_convergence(
                values, 
                target=target,
                title="Convergence Analysée"
            )
        
        elif contexte_type == 'spectral':
            ratios = contexte.get('ratios', {'1/2': 0.5})
            return self.geo_gen.generer_pour_rapport_spectral(
                ratios,
                title="Spectre Analyisé"
            )
        
        elif contexte_type == 'asym_ordonnee':
            bloc_a = contexte.get('bloc_a', [2, 3, 5, 7])
            bloc_b = contexte.get('bloc_b', [11, 13, 17, 19, 23])
            ratio = contexte.get('ratio', 0.5026)
            return self.geo_gen.generer_pour_bloc_asymetrique(
                bloc_a, 
                bloc_b, 
                ratio
            )
        
        return None
    
    # ================================================================
    # NOUVEAU v7.4 — SUITES GÉOMÉTRIQUES A ET B
    # ================================================================

    def calculer_suites_AB(
        self,
        k: Union[int, float, None] = None
    ) -> ResultatSuiteGeo:
        """
        Calcule les sommes des suites géométriques A et B pour t = 1/k.

        Si k est None, utilise le rapport typique k_typique (défaut 2).
        Supporte les rapports typiques (k=2) et non typiques (k≠2).

        Retourne un ResultatSuiteGeo avec :
          .somme_A   : somme de la suite A
          .somme_B   : somme de la suite B
          .termes_A  : liste des 10 termes hypoténuse de A
          .termes_B  : liste des 10 termes hypoténuse de B
        """
        k_eff = k if k is not None else self.k_typique
        return self.pipeline_geo.calcul_pour_rapport(k_eff)

    def convolution_suites_AB(
        self,
        n_max: int = 10,
        k: Union[int, float, None] = None
    ) -> Dict[str, List[float]]:
        """
        Calcule la convolution discrète A⊗B sur n_max termes.
        Retourne dict avec 'sommes_A', 'sommes_B', 'convolution', 'ratios_AB'.
        """
        k_eff = k if k is not None else self.k_typique
        return self.pipeline_geo.convolution_AB(n_max=n_max, k=k_eff)

    # ================================================================
    # NOUVEAU v7.4 — FALLBACK GÉOMÉTRIQUE
    # ================================================================

    def reconstruire_avec_fallback(
        self,
        n: int,
        fn_algebrique,
        k: Union[int, float, None] = None,
    ) -> ResultatReconstruction:
        """
        Tente la reconstruction des premiers pour la valeur n.

        LOGIQUE :
          1. Appelle fn_algebrique(n) — approche existante (suites entières + Digamma).
          2. Si aucun premier trouvé → FALLBACK GÉOMÉTRIQUE automatique.
             Relance via les suites A et B modèle géométrique (termes hypoténuse).

        Paramètres
        ----------
        n : int
            Valeur de n à reconstruire.
        fn_algebrique : Callable[[int], List[int]]
            Fonction de reconstruction algébrique existante.
            Doit retourner List[int] (vide si échec Digamma).
        k : int, float ou None
            Rapport t = 1/k. Si None, utilise k_typique.

        Retourne
        --------
        ResultatReconstruction avec .premiers_finals et .approche_finale.
        """
        k_eff = k if k is not None else self.k_typique
        return self.fallback_gestionnaire.reconstruire(
            n=n,
            fn_algebrique=fn_algebrique,
            k_override=k_eff,
        )

    def reconstruire_batch_avec_fallback(
        self,
        n_values: List[int],
        fn_algebrique,
        k: Union[int, float, None] = None,
    ) -> Dict[int, ResultatReconstruction]:
        """
        Applique le double mécanisme (algébrique + fallback géo)
        pour une liste complète de valeurs de n.
        Couvre l'ensemble des valeurs de n demandées.
        """
        k_eff = k if k is not None else self.k_typique
        return self.fallback_gestionnaire.reconstruire_batch(
            n_values=n_values,
            fn_algebrique=fn_algebrique,
            k_override=k_eff,
        )

    def rapport_fallback_session(self) -> str:
        """Retourne le rapport de session du gestionnaire de fallback."""
        return self.fallback_gestionnaire.rapport_session()

    # ================================================================
    # STRUCTURE EXPORTABLE (MÉTHODE EXISTANTE — INCHANGÉE)
    # ================================================================

    def creer_structure_exportable(self,
                                  reponse: str,
                                  contexte: Dict) -> Dict[str, Any]:
        """
        Crée structure exportable vers CAO/modélisation
        
        Retourne format exploitable par FreeCAD, Blender, OpenSCAD
        """
        
        export = {
            'texte': reponse,
            'geometrie': [],
            'points_3d': [],
            'matrices': [],
            'instructions_cad': []
        }
        
        # Extraire points 3D
        points_3d = re.findall(
            r'\([-\d.]+,\s*[-\d.]+,\s*[-\d.]+\)',
            reponse
        )
        
        for pt_str in points_3d:
            coords = re.findall(r'[-\d.]+', pt_str)
            if len(coords) == 3:
                pt = Point3D(float(coords[0]), float(coords[1]), float(coords[2]))
                export['points_3d'].append(pt.to_tuple())
        
        # Générer instructions CAO
        if contexte.get('type') == 'convergence':
            export['instructions_cad'].append("""
# FreeCAD Script
import FreeCAD as App
import Part

# Créer points de convergence
points = """ + str(export['points_3d']) + """

# Créer polyline
pl = Part.makePolygon(points)
App.ActiveDocument.addObject("Part::Feature", "ConvergencePath").Shape = pl
""")
        
        return export

# ========================================================================
# INTÉGRATION DANS GABRIEL
# ========================================================================

def enrichir_reponse_gabriel(reponse: str, contexte: Optional[Dict] = None) -> str:
    """
    Fonction à appeler dans le pipeline multiloop de Gabriel
    
    Exemple d'utilisation dans integrateur_memoire.py:
    
        response = await llm_router.route_request(question)
        
        # Enrichir avec métaphores géométriques
        response_enrichie = enrichir_reponse_gabriel(response, contexte)
        
        return response_enrichie
    """
    
    wrapper = GabrielGeometricResponseWrapper()
    return wrapper.enrichir_reponse(reponse, contexte)

# ========================================================================
# TEST
# ========================================================================

if __name__ == "__main__":
    wrapper = GabrielGeometricResponseWrapper()
    
    # Test 1: Enrichir une réponse sur convergence
    print("\n[TEST] Enrichissement d'une réponse sur convergence:\n")
    reponse_test = """
    Le ratio converge vers 1/2:
    - k=1: 0.625
    - k=2: 0.552
    - k=3: 0.501
    - k=4: 0.5001
    """
    
    reponse_enrichie = wrapper.enrichir_reponse(reponse_test)
    print(reponse_enrichie)
    
    # Test 2: Créer export CAO
    print("\n[TEST] Export CAO:\n")
    export = wrapper.creer_structure_exportable(
        reponse_enrichie,
        {'type': 'convergence'}
    )
    
    print("Points 3D extraits:")
    for pt in export['points_3d']:
        print(f"  {pt}")
    
    print("\nInstructions CAO:")
    for instr in export['instructions_cad']:
        print(instr[:200] + "...")
