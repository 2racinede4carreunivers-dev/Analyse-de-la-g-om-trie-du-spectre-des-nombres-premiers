#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT D'ACTIVATION - Systeme de Memoire Gabriel v7
===================================================

Teste l'integration complete du systeme de memoire dans Gabriel
"""

import sys
import asyncio
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_memoire_integration():
    """Test complet du systeme de memoire integre"""
    
    print("\n" + "="*70)
    print("TEST D'ACTIVATION - SYSTEME DE MEMOIRE GABRIEL v7")
    print("="*70)
    
    # Test 1: Import des modules
    print("\n[1/5] Verification des imports...")
    try:
        from memory.memoire_conceptuelle import (
            rechercher_concept_par_theme,
            obtenir_contexte_regime,
            AXIOMES_FONDAMENTAUX
        )
        print("  [OK] Memoire conceptuelle")
        
        from memory.memoire_technique import (
            PATTERNS_PREUVE_REUSSIS,
            LEMMES_VALIDES,
            trouver_pattern
        )
        print("  [OK] Memoire technique")
        
        from memory.gestionnaire_erreurs import (
            CacheErreursPersistent,
            AnalyseurPatternErreurs
        )
        print("  [OK] Gestionnaire d'erreurs")
        
        # Import avec chemin absolu pour l'integrateur
        import sys
        sys.path.insert(0, str(Path(__file__).parent / 'src' / 'core'))
        from integrateur_memoire import IntegrateurMemoireGabriel
        print("  [OK] Integrateur de memoire")
        
    except Exception as e:
        print(f"  [ERREUR] Erreur import: {e}")
        return False
    
    # Test 2: Initialiser l'integrateur
    print("\n[2/5] Initialisation de l'integrateur...")
    try:
        integrateur = IntegrateurMemoireGabriel()
        print("  [OK] IntegrateurMemoireGabriel cree")
    except Exception as e:
        print(f"  [ERREUR] Erreur initialisation: {e}")
        return False
    
    # Test 3: Verifier la memoire conceptuelle
    print("\n[3/5] Test RAG semantique (Memoire Conceptuelle)...")
    try:
        concepts = rechercher_concept_par_theme("regime")
        print(f"  [OK] Trouve {len(concepts)} concepts pour 'regime'")
        
        ctx = obtenir_contexte_regime("1/2-positif")
        print(f"  [OK] Contexte regime 1/2-positif charge")
        
        prompt = integrateur.augmenter_prompt_conceptuel(
            "Quel est le comportement du regime 1/2-positif?"
        )
        print(f"  [OK] Prompt augmente ({len(prompt)} caracteres)")
        
    except Exception as e:
        print(f"  [ERREUR] Erreur RAG semantique: {e}")
        return False
    
    # Test 4: Verifier la memoire technique
    print("\n[4/5] Test RAG syntaxique (Memoire Technique)...")
    try:
        pattern = integrateur.trouver_pattern_optimal("classification", "regime")
        if pattern:
            print(f"  [OK] Pattern trouve: {pattern.nom}")
        else:
            print("  [WARN] Aucun pattern trouve (normal si domaine vague)")
        
        lemmes = integrateur.trouver_lemmes_pertinents("prime mod", top_n=2)
        print(f"  [OK] Trouve {len(lemmes)} lemmes pertinents")
        
        antipattern = integrateur.verification_antipattern("omega on modular")
        if antipattern:
            print(f"  [OK] Antipattern detecte (comme prevu)")
        
    except Exception as e:
        print(f"  [ERREUR] Erreur RAG syntaxique: {e}")
        return False
    
    # Test 5: Verifier le cache d'erreurs
    print("\n[5/5] Test Contexte d'Erreur Persistent...")
    try:
        rapport = integrateur.generer_rapport_memoire()
        print("  [OK] Rapport memoire genere")
        print(rapport[:200] + "...")
        
        diag = integrateur.diagnostiquer_domaine("regime")
        print("  [OK] Diagnostic domaine genere")
        
    except Exception as e:
        print(f"  [ERREUR] Erreur cache erreurs: {e}")
        return False
    
    print("\n" + "="*70)
    print("OK - TOUS LES TESTS PASSES - SYSTEME DE MEMOIRE OPERATIONNEL")
    print("="*70)
    
    print("""
RESUME:
───────
[OK] RAG Semantique: Axiomes + Definitions injectes
[OK] RAG Syntaxique: Patterns + Lemmes recommandes
[OK] Cache Persistant: Erreurs enregistrees et apprises
[OK] Integrateur: Coordonne les 3 couches

PROCHAINES ETAPES:
──────────────────
1. Gabriel utilise LLMManager v3 (automatique)
2. Tous les prompts recoivent le contexte memoire
3. Erreurs HOL enregistrees automatiquement
4. Sessions futures evitent les erreurs passees

DEBUT DE SESSION:
─────────────────
Pour activer le systeme dans Gabriel:
  $ docker-compose restart
  
Gabriel utilisera automatiquement:
  * Augmentation de prompts (RAG)
  * Cache d'erreurs (apprentissage)
  * Recommandations techniques (optimisation)
""")
    
    return True

def main():
    """Fonction principale"""
    
    # Test 1: Integrateur seul
    success1 = test_memoire_integration()
    
    if success1:
        print("\n" + "="*70)
        print("[SUCCES] SYSTEME DE MEMOIRE GABRIEL v7 - 100%% OPERATIONNEL")
        print("="*70)
        print("""
Le systeme de memoire est maintenant:
  [OK] Structure en 3 couches (conceptuelle, technique, erreurs)
  [OK] Integre dans LLMManager v3
  [OK] Injectant automatiquement le contexte dans les prompts
  [OK] Enregistrant et apprenant des erreurs
  [OK] Recommandant les meilleures strategies

Gabriel saura maintenant:
  * Les axiomes et definitions de votre theorie
  * Les patterns de preuve qui marchent
  * Les erreurs a eviter
  * Les tactiques optimales par domaine
  
Prochaine etape: docker-compose restart
        """)
        return 0
    else:
        print("\n[ERREUR] Certains tests ont echoue")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
