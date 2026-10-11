#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTÉGRATEUR DE MÉMOIRE POUR GABRIEL
===================================

Module central qui:
1. Injecte la mémoire conceptuelle avant les requêtes
2. Recherche les lemmes techniques lors de preuves
3. Évite les erreurs persistées
4. Apprend des new erreurs
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Imports des modules de mémoire
sys.path.insert(0, str(Path(__file__).parent))

from memoire_conceptuelle import (
    rechercher_concept_par_theme,
    obtenir_contexte_regime,
    generer_prompt_conceptuel,
    AXIOMES_FONDAMENTAUX,
    DEFINITIONS_GEOMETRIQUES
)

from memoire_technique import (
    PATTERNS_PREUVE_REUSSIS,
    LEMMES_VALIDES,
    ANTIPATTERNS_PREUVE,
    trouver_pattern,
    trouver_lemme_pertinent,
    eviter_antipattern,
    PatternPreuve
)

from gestionnaire_erreurs import (
    CacheErreursPersistent,
    ErreurPreuve,
    TypeErreur,
    StrategieEvitementErreurs,
    AnalyseurPatternErreurs,
    ERREURS_PERSISTEES
)

try:
    from detecteur_asymetrique_ordonnee import router_requete
    from gabriel_comparaison_asymetrique import GabrielComparaisonAsymetrique
except ImportError:
    router_requete = None
    GabrielComparaisonAsymetrique = None

# ========================================================================
# CORE: INTÉGRATEUR DE MÉMOIRE
# ========================================================================

class IntegrateurMemoireGabriel:
    """Intégrateur central de la mémoire pour Gabriel"""
    
    def __init__(self):
        self.cache_erreurs = CacheErreursPersistent()
        self.strategie_evitement = StrategieEvitementErreurs()
        self.analyseur = AnalyseurPatternErreurs()
    
    # ====================================================================
    # RAG SÉMANTIQUE: Injection de contexte conceptuel
    # ====================================================================
    
    def augmenter_prompt_conceptuel(self, question: str) -> str:
        """RAG Sémantique: Augmente le prompt avec contexte conceptuel"""
        
        prompt_rag = generer_prompt_conceptuel(question)
        
        # Ajouter contexte spécifique pour régimes
        if "régime" in question.lower() or "regime" in question.lower():
            for regime in ["1/2-positif", "1/4", "1/3", "négatif", "mixte"]:
                if regime.lower() in question.lower():
                    contexte = obtenir_contexte_regime(regime)
                    prompt_rag += f"\n\nContexte spécifique pour {regime}:\n"
                    prompt_rag += self._formatter_contexte(contexte)
        
        return prompt_rag
    
    def _formatter_contexte(self, contexte: Dict) -> str:
        """Formate le contexte pour affichage"""
        result = ""
        for category, items in contexte.items():
            if items:
                result += f"\n{category.upper()}:\n"
                for key, data in items:
                    result += f"  - {key}: {str(data)[:100]}...\n"
        return result
    
    # ====================================================================
    # RAG SYNTAXIQUE: Injection de patterns techniques
    # ====================================================================
    
    def trouver_pattern_optimal(self, type_probleme: str, domaine: str) -> Optional[PatternPreuve]:
        """Trouve le pattern de preuve optimal"""
        pattern = trouver_pattern(type_probleme, domaine)
        
        if pattern:
            print(f"✓ Pattern trouvé: {pattern.nom}")
            print(f"  Tactique: {pattern.tactique_primaire.value}")
            print(f"  Taux réussite: {pattern.taux_reussite:.1%}")
            print(f"  Validations: {pattern.validations}x")
        
        return pattern
    
    def trouver_lemmes_pertinents(self, concept: str, top_n: int = 3) -> List[Tuple[str, Dict]]:
        """Trouve les lemmes les plus pertinents"""
        lemmes = trouver_lemme_pertinent(concept)
        
        result = []
        for lemme_key, lemme_data in lemmes[:top_n]:
            result.append((lemme_key, lemme_data))
            print(f"  - {lemme_key}: {lemme_data['taux_reussite']:.1%}")
        
        return result
    
    def generer_suggestion_tactique(self, domaine: str) -> str:
        """Génère la tactique recommandée pour un domaine"""
        
        # Analyser les erreurs passées
        erreurs = self.cache_erreurs.trouver_erreurs_similaires(TypeErreur.TIMEOUT, domaine)
        
        if erreurs:
            # Il y a eu des timeouts
            tactique = self.analyseur.tactique_plus_fiable(domaine, self.cache_erreurs)
            print(f"⚠️ Domaine {domaine}: utiliser {tactique} (basé sur {len(erreurs)} erreurs passées)")
            return tactique
        
        # Sinon, utiliser le pattern par défaut
        return "metis"
    
    # ====================================================================
    # PRÉVENTION D'ERREURS: Stratégie d'évitement
    # ====================================================================
    
    def verification_antipattern(self, strategie: str) -> Optional[Dict]:
        """Vérifie si une stratégie est un antipattern connu"""
        antipattern = eviter_antipattern(strategie)
        
        if antipattern:
            print(f"❌ ANTIPATTERN DÉTECTÉ: {antipattern['description']}")
            print(f"   Raison: {antipattern['pourquoi_ca_ne_marche_pas']}")
            print(f"   Rencontré {antipattern['rencontres']} fois")
            print(f"   Solution: {antipattern['solution_correcte'][:100]}...")
        
        return antipattern
    
    def peut_tenter_strategie(self, lemme_id: str, tactique: str) -> Tuple[bool, Optional[str]]:
        """Vérifie si on peut tenter une stratégie"""
        peut_tenter, suggestion = self.strategie_evitement.peut_tenter(lemme_id, tactique)
        
        if not peut_tenter:
            print(f"⚠️ Stratégie {tactique} déjà tentée 2x sur {lemme_id}")
            print(f"   Suggestion: {suggestion}")
        
        return peut_tenter, suggestion
    
    # ====================================================================
    # APPRENTISSAGE: Enregistrement des erreurs
    # ====================================================================
    
    def enregistrer_erreur(self, 
                          lemme_name: str,
                          domaine: str,
                          tactique_tentee: str,
                          type_erreur: TypeErreur,
                          message_erreur: str,
                          code_hol: str,
                          hypotheses: List[str],
                          suggestions: List[str]) -> str:
        """Enregistre une erreur pour apprentissage futur"""
        
        err_id = f"ERR_{len(self.cache_erreurs.erreurs) + 1:03d}"
        
        from datetime import datetime
        erreur = ErreurPreuve(
            id=err_id,
            timestamp=datetime.now().isoformat(),
            type_erreur=type_erreur,
            lemme_name=lemme_name,
            domaine=domaine,
            tactique_tentee=tactique_tentee,
            code_hol=code_hol,
            message_erreur=message_erreur,
            contexte_hypotheses=hypotheses,
            suggestions=suggestions,
            resolu=False
        )
        
        self.cache_erreurs.enregistrer_erreur(erreur)
        print(f"✓ Erreur enregistrée: {err_id}")
        print(f"  Lemme: {lemme_name}")
        print(f"  Type: {type_erreur.value}")
        print(f"  Domaine: {domaine}")
        
        return err_id
    
    def marquer_erreur_resolue(self, err_id: str, resolution: str):
        """Marque une erreur comme résolue"""
        if err_id in self.cache_erreurs.erreurs:
            err = self.cache_erreurs.erreurs[err_id]
            err['resolu'] = True
            err['resolution'] = resolution
            self.cache_erreurs.sauvegarder_cache()
            print(f"✓ Erreur {err_id} marquée résolue")
            print(f"  Solution: {resolution}")
    
    # ====================================================================
    # RAPPORTS ET DIAGNOSTICS
    # ====================================================================
    
    def generer_rapport_memoire(self) -> str:
        """Génère un rapport complet sur l'état de la mémoire"""
        rapport = """
╔════════════════════════════════════════════════════════════════╗
║           RAPPORT MÉMOIRE GABRIEL - ÉTAT ACTUEL              ║
╚════════════════════════════════════════════════════════════════╝

MÉMOIRE CONCEPTUELLE
─────────────────────
"""
        rapport += f"  Axiomes fondamentaux: {len(AXIOMES_FONDAMENTAUX)}\n"
        rapport += f"  Définitions géométriques: {len(DEFINITIONS_GEOMETRIQUES)}\n"
        
        rapport += """
MÉMOIRE TECHNIQUE
─────────────────
"""
        rapport += f"  Patterns de preuve: {len(PATTERNS_PREUVE_REUSSIS)}\n"
        rapport += f"  Lemmes HOL validés: {len(LEMMES_VALIDES)}\n"
        rapport += f"  Antipatterns: {len(ANTIPATTERNS_PREUVE)}\n"
        
        taux_moyen = sum(p.taux_reussite for p in PATTERNS_PREUVE_REUSSIS.values()) / len(PATTERNS_PREUVE_REUSSIS)
        rapport += f"  Taux moyen réussite: {taux_moyen:.1%}\n"
        
        rapport += """
CONTEXTE D'ERREUR PERSISTENT
────────────────────────────
"""
        rapport += f"  Erreurs enregistrées: {len(self.cache_erreurs.erreurs)}\n"
        rapport += f"  Erreurs persistées: {len(ERREURS_PERSISTEES)}\n"
        
        nb_resolues = sum(1 for e in self.cache_erreurs.erreurs.values() if e['resolu'])
        rapport += f"  Taux résolution: {nb_resolues}/{len(self.cache_erreurs.erreurs)}\n"
        
        return rapport
    
    def diagnostiquer_domaine(self, domaine: str) -> str:
        """Diagnostique l'état d'un domaine"""
        
        diag = f"DIAGNOSTIC DOMAINE: {domaine}\n"
        diag += "─" * 40 + "\n"
        
        # Erreurs les plus fréquentes
        err_freq = self.analyseur.type_erreur_le_plus_frequent(domaine, self.cache_erreurs)
        if err_freq:
            diag += f"Erreur la plus fréquente: {err_freq[0]} ({err_freq[1]}x)\n"
        
        # Tactique la plus fiable
        tac_fiable = self.analyseur.tactique_plus_fiable(domaine, self.cache_erreurs)
        diag += f"Tactique recommandée: {tac_fiable}\n"
        
        # Hypothèses problématiques
        hyp_prob = self.analyseur.hypotheses_problematiques(domaine, self.cache_erreurs)
        if hyp_prob:
            diag += f"\nHypothèses problématiques:\n"
            for hyp, count in hyp_prob[:3]:
                diag += f"  - {hyp} ({count}x)\n"
        
        return diag

# ========================================================================
# EXEMPLE D'UTILISATION
# ========================================================================

def demo():
    """Démo du système intégré"""
    
    integrateur = IntegrateurMemoireGabriel()
    
    print(integrateur.generer_rapport_memoire())
    
    print("\n" + "="*60)
    print("DÉMONSTRATION: Requête sur régime spectral")
    print("="*60)
    
    question = "Quel est le comportement spectral des nombres 1/2-positifs?"
    print(f"\nQuestion: {question}\n")
    
    # RAG Sémantique
    prompt_aug = integrateur.augmenter_prompt_conceptuel(question)
    print("RAG SÉMANTIQUE - Contexte injecté:")
    print(prompt_aug[:500] + "...")
    
    print("\n" + "-"*60)
    print("DÉMONSTRATION: Preuve de classification de régime")
    print("-"*60)
    
    # RAG Syntaxique
    pattern = integrateur.trouver_pattern_optimal("classification", "regime")
    if pattern:
        print(f"\nPattern optimal trouvé: {pattern.nom}")
        print(f"Lemmes pertinents:")
        integrateur.trouver_lemmes_pertinents("prime mod")
    
    print("\n" + "-"*60)
    print("DIAGNOSTIC PAR DOMAINE")
    print("-"*60)
    
    for domaine in ["regime", "gap", "harmonie"]:
        print("\n" + integrateur.diagnostiquer_domaine(domaine))

if __name__ == "__main__":
    demo()
