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

import json
import re
import unicodedata
from typing import Dict, List, Optional, Tuple

from memory.memoire_conceptuelle import (
    rechercher_concept_par_theme,
    obtenir_contexte_regime,
    generer_prompt_conceptuel,
    AXIOMES_FONDAMENTAUX,
    DEFINITIONS_GEOMETRIQUES,
    PROPRIETES_ETABLIES,
    CONCEPTS_CLES,
)

from memory.memoire_technique import (
    PATTERNS_PREUVE_REUSSIS,
    LEMMES_VALIDES,
    ANTIPATTERNS_PREUVE,
    trouver_pattern,
    trouver_lemme_pertinent,
    eviter_antipattern,
    PatternPreuve
)

from memory.gestionnaire_erreurs import (
    CacheErreursPersistent,
    ErreurPreuve,
    TypeErreur,
    StrategieEvitementErreurs,
    AnalyseurPatternErreurs,
    ERREURS_PERSISTEES
)

from memory.dictionnaire_spectral import DICTIONNAIRE_SPECTRAL
from ..spectral.digamma_savard_cognitive import digamma_savard_context_for_query
from ..spectral.convolutive_primality_evidence import convolutive_primality_context_for_query

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

    _STOP_WORDS = {
        "avec", "dans", "pour", "quoi", "dont", "elle", "elles", "est", "etre",
        "faire", "fait", "sur", "une", "des", "les", "aux", "qui", "que", "par",
        "plus", "moins", "comme", "cette", "cela", "comment", "quel", "quelle",
        "quels", "quelles", "donner", "donne", "deux", "tout", "tous", "the",
        "and", "for", "from", "with", "what", "when", "where", "that", "this",
    }

    def __init__(self):
        self.cache_erreurs = CacheErreursPersistent()
        self.strategie_evitement = StrategieEvitementErreurs()
        self.analyseur = AnalyseurPatternErreurs()

    @classmethod
    def _tokens(cls, text: str) -> set[str]:
        normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
        return {
            token
            for token in re.findall(r"[a-z0-9]+", normalized.casefold())
            if len(token) > 2 and token not in cls._STOP_WORDS
        }

    @staticmethod
    def _flatten_record(value: object) -> str:
        if isinstance(value, dict):
            return " ".join(
                f"{key} {IntegrateurMemoireGabriel._flatten_record(item)}"
                for key, item in value.items()
            )
        if isinstance(value, (list, tuple)):
            return " ".join(IntegrateurMemoireGabriel._flatten_record(item) for item in value)
        return str(value)

    @staticmethod
    def _extract_question(prompt: str) -> str:
        match = re.search(
            r"QUESTION DE L['’]UTILISATEUR\s*:\s*(.*?)(?:\n\s*CHIFFRES CALCULES\b|\Z)",
            prompt,
            re.IGNORECASE | re.DOTALL,
        )
        return match.group(1).strip() if match else prompt
    
    # ====================================================================
    # RAG SÉMANTIQUE: Injection de contexte conceptuel
    # ====================================================================
    
    def _augmenter_prompt_conceptuel(self, question: str) -> str:
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

    def augmenter_prompt(self, prompt: str, domaine: str = "general") -> str:
        """Injecte une sélection courte de mémoire liée à la question."""
        question = self._extract_question(prompt)
        question_tokens = self._tokens(question)
        digamma_context = digamma_savard_context_for_query(question)
        primality_validation_context = convolutive_primality_context_for_query(question)
        retrieved: list[tuple[int, str, str, object]] = []
        corpora = (
            ("axiome", AXIOMES_FONDAMENTAUX),
            ("définition", DEFINITIONS_GEOMETRIQUES),
            ("propriété du corpus", PROPRIETES_ETABLIES),
            ("concept", CONCEPTS_CLES),
        )
        if not digamma_context:
            for category, records in corpora:
                for key, record in records.items():
                    record_text = self._flatten_record(record)
                    overlap = question_tokens & self._tokens(f"{key} {record_text}")
                    if overlap:
                        retrieved.append((len(overlap), category, key, record))
        retrieved.sort(key=lambda item: (-item[0], item[1], item[2]))

        blocks: list[str] = []
        remaining = 2200
        for _, category, key, record in retrieved[:3]:
            entry = (
                f"- {category} « {key} » : "
                f"{json.dumps(record, ensure_ascii=False, default=str)}"
            )
            if len(entry) > remaining:
                entry = entry[: max(0, remaining - 3)].rstrip() + "..."
            if entry:
                blocks.append(entry)
                remaining -= len(entry)
            if remaining <= 0:
                break

        if digamma_context:
            blocks.append(digamma_context)
        if primality_validation_context:
            blocks.append(primality_validation_context)
        if not blocks:
            return prompt

        memory_context = (
            "CONTEXTE DE MÉMOIRE SÉMANTIQUE — corpus interne de l'auteur; "
            "ne pas présenter ses assertions comme des preuves indépendantes. "
            "Pour une demande théorique, donner une réponse développée et structurée, "
            "définir les termes, expliciter les équations et étapes, fournir un exemple "
            "seulement s'il est étayé, et signaler les limites et le statut épistémique.\n"
            f"Domaine détecté : {domaine}\n"
            + "\n".join(blocks)
        )
        return f"{prompt}\n\n=== MÉMOIRE SÉMANTIQUE PERTINENTE ===\n{memory_context}\n=== FIN MÉMOIRE ==="

    def detecter_regimes(self, requete: str) -> tuple[list[str], dict[str, list[str]]]:
        from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral

        return AdaptateurCognitifSpectral().detecter_regimes(requete)

    def info(self) -> dict[str, int]:
        return {
            "regimes": len(DICTIONNAIRE_SPECTRAL),
            "lemmes_certifies": sum(
                len(regime.lemmes_certifies)
                for regime in DICTIONNAIRE_SPECTRAL.values()
            ),
        }
    
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
    
    def _trouver_pattern_optimal(self, type_probleme: str, domaine: str) -> Optional[PatternPreuve]:
        """Trouve le pattern de preuve optimal"""
        pattern = trouver_pattern(type_probleme, domaine)
        
        if pattern:
            print(f"✓ Pattern trouvé: {pattern.nom}")
            print(f"  Tactique: {pattern.tactique_primaire.value}")
            print(f"  Taux réussite: {pattern.taux_reussite:.1%}")
            print(f"  Validations: {pattern.validations}x")
        
        return pattern
    
    def _trouver_lemmes_pertinents(self, concept: str, top_n: int = 3) -> List[Tuple[str, Dict]]:
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
    prompt_aug = integrateur.augmenter_prompt(question, domaine="spectral")
    print("RAG SÉMANTIQUE - Contexte injecté:")
    print(prompt_aug[:500] + "...")
    
    print("\n" + "-"*60)
    print("DÉMONSTRATION: Preuve de classification de régime")
    print("-"*60)
    
    # RAG Syntaxique
    pattern = integrateur._trouver_pattern_optimal("classification", "regime")
    if pattern:
        print(f"\nPattern optimal trouvé: {pattern.nom}")
        print(f"Lemmes pertinents:")
        integrateur._trouver_lemmes_pertinents("prime mod")
    
    print("\n" + "-"*60)
    print("DIAGNOSTIC PAR DOMAINE")
    print("-"*60)
    
    for domaine in ["regime", "gap", "harmonie"]:
        print("\n" + integrateur.diagnostiquer_domaine(domaine))

if __name__ == "__main__":
    demo()
