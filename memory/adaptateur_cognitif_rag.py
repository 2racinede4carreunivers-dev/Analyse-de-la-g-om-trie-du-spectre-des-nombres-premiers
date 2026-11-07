"""Adaptateur Cognitif RAG Spectral - injection dynamique du contexte.

Analyse une requete utilisateur, detecte les regimes mathematiques impliques
via regex, extrait les lemmes/regles/avertissements du dictionnaire, et
construit un prompt systeme augmente a injecter dans Claude.

Pipeline :
  requete -> patterns regex -> regimes detectes -> contexte HOL -> prompt augmente

100% deterministe, zero appel LLM.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Optional

from .dictionnaire_spectral import (
    DICTIONNAIRE_SPECTRAL,
    Regime,
    list_regimes,
)

logger = logging.getLogger(__name__)


@dataclass
class AnalyseRequete:
    """Resultat de l'analyse RAG d'une requete."""
    requete_originale: str
    regimes_detectes: list[str]
    matched_keywords: dict[str, list[str]]  # regime -> mots-cles trouves
    contexte_brut: str
    prompt_augmente: str
    nombre_regimes: int


class AdaptateurCognitifSpectral:
    """Adaptateur RAG semantique pour Gabriel.

    Detecte automatiquement les regimes mathematiques d'une requete et injecte
    le contexte spectral (lemmes, regles, avertissements) dans le prompt LLM.
    """

    # Regles d'injection obligatoires (toujours presentes en preambule)
    REGLES_GLOBALES = """REGLES D'INJECTION OBLIGATOIRES POUR TOUTE REPONSE :

REGLE 1 - SUBSTITUTION AUTOMATIQUE:
   SB n - 2 * SA n -> -62 (immediat)

REGLE 2 - PUISSANCE OBLIGATOIRE:
   Indices POSITIFS -> ^ (entiere)
   Indices NEGATIFS -> powr (continue)

REGLE 3 - FACTEUR DE RECONSTRUCTION (generique k^6, jamais 64 hors 1/2) :
   Regime 1/2 -> 64            (EXCLUSIF : 2^6 = 64, JAMAIS pour 1/k avec k != 2)
   Regime 1/3 -> 729           (3^6)
   Regime 1/4 -> 4096          (4^6)
   Regime 1/k, k != 2 -> k^6   (GENERATEUR : 1/14 -> 7529536, 1/23 -> 148035889, 1/50 -> 282429536481)
   digamma_calc(n,p) = SB(n) - k^6 * p   (formule GENERIQUE ; 64 est le cas particulier k=2)
   Facteur geometrique niveau 2 = sqrt(1 + k^2)   (1/14 -> sqrt(197) = 14.0356688476)

REGLE 4 - CONSTANTES RIGIDES:
   D29=256, D31=1280, K6=-(37127/256) - SA_mix(6)
   JAMAIS d'interpolation

REGLE 5 - ZERO ET ECARTS:
   Ecart NEGATIF (-,-) -> Zero EXCLU
   Ecart MIXTE (-,+) -> Zero INCLUS

REGLE 6 - VALIDATION HOL:
   TOUJOURS fournir lemmes HOL certifies
   Utiliser lemmes pre-certifies du dictionnaire"""

    def __init__(self, dictionnaire: Optional[dict[str, Regime]] = None):
        """Initialise l'adaptateur avec le dictionnaire fourni (ou officiel)."""
        self.dictionnaire = dictionnaire or DICTIONNAIRE_SPECTRAL
        # Compile les patterns une seule fois pour performance
        self._compiled_patterns: dict[str, list[re.Pattern]] = {}
        for nom, regime in self.dictionnaire.items():
            self._compiled_patterns[nom] = [
                re.compile(p, re.IGNORECASE) for p in regime.patterns_detection
            ]
        logger.info(
            f"AdaptateurCognitifSpectral initialise : {len(self.dictionnaire)} regimes, "
            f"{sum(len(p) for p in self._compiled_patterns.values())} patterns"
        )

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------
    def detecter_regimes(
        self, requete: str
    ) -> tuple[list[str], dict[str, list[str]]]:
        """Detecte les regimes correspondants a une requete.

        Returns:
            (liste_noms_regimes, dict[regime -> mots_cles_trouves])
        """
        regimes_trouves: list[str] = []
        matched: dict[str, list[str]] = {}
        for nom, patterns in self._compiled_patterns.items():
            keywords: list[str] = []
            for p in patterns:
                m = p.search(requete)
                if m:
                    keywords.append(m.group(0))
            if keywords:
                regimes_trouves.append(nom)
                matched[nom] = keywords
        return regimes_trouves, matched

    # ------------------------------------------------------------------
    # Construction du contexte
    # ------------------------------------------------------------------
    def construire_contexte(self, regimes: list[str]) -> str:
        """Construit le bloc texte du contexte injectable."""
        if not regimes:
            return ""
        blocs = []
        for nom in regimes:
            regime = self.dictionnaire[nom]
            blocs.append(regime.to_prompt_context())
        return "\n\n".join(blocs)

    def construire_prompt_augmente(
        self, requete: str, contexte: str
    ) -> str:
        """Assemble le prompt final : regles globales + contexte + requete."""
        if not contexte:
            return requete  # Aucun regime detecte -> requete brute
        return (
            f"{self.REGLES_GLOBALES}\n\n"
            f"=== CONTEXTE SPECTRAL INJECTE ===\n\n"
            f"{contexte}\n\n"
            f"=== FIN CONTEXTE ===\n\n"
            f"REQUETE UTILISATEUR :\n{requete}"
        )

    # ------------------------------------------------------------------
    # API publique principale
    # ------------------------------------------------------------------
    def analyser(self, requete: str) -> AnalyseRequete:
        """Analyse complete d'une requete : detection + contexte + prompt."""
        regimes, matched = self.detecter_regimes(requete)
        contexte = self.construire_contexte(regimes)
        prompt = self.construire_prompt_augmente(requete, contexte)
        return AnalyseRequete(
            requete_originale=requete,
            regimes_detectes=regimes,
            matched_keywords=matched,
            contexte_brut=contexte,
            prompt_augmente=prompt,
            nombre_regimes=len(regimes),
        )

    def afficher_analyse(self, requete: str) -> None:
        """Affiche l'analyse RAG dans la console (mode verbose)."""
        analyse = self.analyser(requete)
        print("\n" + "=" * 70)
        print(f"ANALYSE RAG - Requete : {requete[:60]}...")
        print("=" * 70)
        print(f"\n[X] Regimes detectes : {analyse.nombre_regimes}")
        if not analyse.regimes_detectes:
            print("  Aucun regime detecte - requete generique")
            print("=" * 70 + "\n")
            return
        for i, nom in enumerate(analyse.regimes_detectes, 1):
            r = self.dictionnaire[nom]
            kws = analyse.matched_keywords.get(nom, [])
            print(f"\n  {i}. {r.titre}")
            print(f"     Mots-cles : {', '.join(kws[:5])}")
            print(f"     Lemmes    : {len(r.lemmes_certifies)}")
            if r.ratio_attendu:
                print(f"     Ratio     : {r.ratio_attendu}")
        print("\n" + "=" * 70 + "\n")


# ==========================================================================
# Fonction utilitaire de haut niveau
# ==========================================================================
def preparer_requete_avec_rag(requete: str) -> dict[str, Any]:
    """API attendue par `src/gabriel_v6_2_rag.py`.

    Returns:
        Dict contenant : prompt_augmente, regimes_detectes, contexte_brut.
    """
    adaptateur = AdaptateurCognitifSpectral()
    analyse = adaptateur.analyser(requete)
    return {
        "prompt_augmente": analyse.prompt_augmente,
        "regimes_detectes": analyse.regimes_detectes,
        "contexte_brut": analyse.contexte_brut,
        "matched_keywords": analyse.matched_keywords,
        "nombre_regimes": analyse.nombre_regimes,
    }

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
