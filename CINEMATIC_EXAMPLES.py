#!/usr/bin/env python3
"""
EXEMPLE D'INTÉGRATION : Mode Cinématique Intelligent

Ce script montre comment intégrer le mode cinématique dans Gabriel.
À copier dans src/ui/ask_gabriel.py (fonction ask_gabriel_with_cinematic)
ou à exécuter directement pour tester.
"""

import asyncio
import logging
from typing import Optional

# Import hypothétique du pipeline
# from src.core.pipeline import Pipeline, FinalAnswer

# Imports des nouveaux modules de cinématique
from complexity_analyzer import ComplexityAnalyzer, ResponseMode
from cinematic_display import CinematicDisplay, CinematicProgressCallback
from cinematic_orchestrator import CinematicOrchestrator, FastModeBypass

logger = logging.getLogger(__name__)


# ============================================================================
# EXEMPLE 1: Utilisation Simple (Recommandée)
# ============================================================================

async def ask_gabriel_simple(pipeline, question: str):
    """
    Approche simple : une ligne pour intégrer le cinématique.
    
    Avant:
        final = await pipeline.process(question)
    
    Après:
        final = await ask_gabriel_simple(pipeline, question)
    """
    
    orch = CinematicOrchestrator(pipeline, verbose=True)
    final = await orch.process(question, print_cinematic=True)
    
    return final


# ============================================================================
# EXEMPLE 2: Utilisation Avancée (Contrôle Complet)
# ============================================================================

async def ask_gabriel_advanced(
    pipeline,
    question: str,
    show_complexity_report: bool = True,
) -> dict:
    """
    Approche avancée : accès complet aux analyses et métadonnées.
    
    Retourne un dictionnaire contenant:
    - answer_text: La réponse de Gabriel
    - complexity_profile: Analyse de complexité complète
    - cinematic_metadata: Chronomètre, événements, etc.
    """
    
    # 1. Tentative de réponse rapide (bypass)
    bypass = FastModeBypass()
    if fast_answer := bypass.try_fast_response(question):
        print(f"\n✨ Réponse immédiate (bypass):\n{fast_answer}\n")
        return {
            "answer_text": fast_answer,
            "mode": "fast_bypass",
            "elapsed_sec": 0.01,
            "complexity_profile": None,
        }
    
    # 2. Analyse de complexité
    analyzer = ComplexityAnalyzer()
    profile = analyzer.analyze(question)
    
    print(f"\n📊 Analyse de complexité:")
    print(f"   Mode détecté: {profile.mode.value}")
    print(f"   Loops prévues: {profile.num_loops}")
    print(f"   Score: {profile.complexity_score:.1f}/100")
    print(f"   Confiance: {profile.confidence:.0%}")
    if profile.factors:
        print(f"   Facteurs: {', '.join(profile.factors[:3])}")
    print()
    
    # 3. Orchestration avec cinématique
    orch = CinematicOrchestrator(pipeline, verbose=False)
    final_answer = await orch.process(
        question,
        print_cinematic=True,
    )
    
    # 4. Récupérer les rapports détaillés
    complexity_report = orch.get_complexity_report()
    
    # 5. Afficher le résumé optionnel
    if show_complexity_report:
        print(f"\n📈 Résumé d'exécution:")
        print(f"   Temps réel: {complexity_report['elapsed_sec']:.1f}s")
        print(f"   Progression: {complexity_report['progress_percent']}%")
        print(f"   Événements: {len(complexity_report['events_log'])}")
    
    return {
        "answer_text": final_answer.answer_text,
        "mode": profile.mode.value,
        "elapsed_sec": complexity_report.get("elapsed_sec", 0),
        "complexity_profile": profile,
        "cinematic_metadata": complexity_report,
    }


# ============================================================================
# EXEMPLE 3: Boucle Interactive Complète
# ============================================================================

async def interactive_gabriel_session(pipeline):
    """
    Boucle interactive avec support cinématique complet.
    
    Usage:
        await interactive_gabriel_session(pipeline)
    """
    
    print("\n" + "="*60)
    print("  GABRIEL - Mode Réponse Intelligente (Cinématique)")
    print("  Entrez 'quit' pour quitter, 'help' pour l'aide")
    print("="*60 + "\n")
    
    orch = CinematicOrchestrator(pipeline, verbose=False)
    bypass = FastModeBypass()
    
    session_stats = {
        "total_questions": 0,
        "fast_bypass_count": 0,
        "total_time_sec": 0.0,
        "modes_used": {},
    }
    
    while True:
        try:
            question = input("Gabriel> ").strip()
            
            if not question:
                continue
            
            if question.lower() == "quit":
                print("\nAu revoir! 👋")
                break
            
            if question.lower() == "help":
                print("""
Commandes spéciales:
  quit         → Quitter
  help         → Afficher cette aide
  stats        → Afficher les statistiques de session
  clear        → Effacer l'écran (Ctrl+L)

Exemples de questions:
  "C'est quoi un nombre premier?"        → Mode RAPIDE (< 1s)
  "Reconstruis le 26e premier"          → Mode STANDARD (15-20s)
  "Rapport spectral 3x3: ..."           → Mode APPROFONDI (25-35s)
  "Section 13: pont logique Zêta"       → Mode TRÈS_COMPLEXE (40-60s)
                """)
                continue
            
            if question.lower() == "stats":
                print(f"\n📊 Statistiques de session:")
                print(f"   Questions traitées: {session_stats['total_questions']}")
                print(f"   Réponses rapides (bypass): {session_stats['fast_bypass_count']}")
                print(f"   Temps total: {session_stats['total_time_sec']:.1f}s")
                if session_stats['modes_used']:
                    print(f"   Modes utilisés:")
                    for mode, count in session_stats['modes_used'].items():
                        print(f"      {mode}: {count}x")
                print()
                continue
            
            # Traiter la question
            session_stats['total_questions'] += 1
            
            # Tentative de bypass
            if fast_answer := bypass.try_fast_response(question):
                session_stats['fast_bypass_count'] += 1
                print(f"\n✨ Réponse immédiate: {fast_answer}\n")
                continue
            
            # Orchestration complète
            try:
                final = await orch.process(question, print_cinematic=True)
                print(f"\n{final.answer_text}\n")
                
                # Mettre à jour les stats
                report = orch.get_complexity_report()
                mode = report.get("mode", "unknown")
                session_stats["modes_used"][mode] = session_stats["modes_used"].get(mode, 0) + 1
                session_stats["total_time_sec"] += report.get("elapsed_sec", 0)
            
            except Exception as e:
                print(f"\n❌ Erreur: {e}\n")
        
        except KeyboardInterrupt:
            print("\n\nAu revoir! 👋")
            break


# ============================================================================
# EXEMPLE 4: Batch Processing (Traiter plusieurs questions)
# ============================================================================

async def batch_process_questions(
    pipeline,
    questions: list[str],
    show_timing: bool = True,
) -> list[dict]:
    """
    Traite une liste de questions en batch.
    
    Utile pour:
    - Tests de performance
    - Analyse comparative des modes
    - Génération de statistiques
    """
    
    results = []
    orch = CinematicOrchestrator(pipeline, verbose=False)
    
    print(f"\n📋 Traitement en batch: {len(questions)} questions\n")
    
    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] Traitement...")
        
        try:
            final = await orch.process(question, print_cinematic=False)
            report = orch.get_complexity_report()
            
            result = {
                "question": question,
                "mode": report.get("mode"),
                "loops": report.get("num_loops"),
                "elapsed_sec": report.get("elapsed_sec"),
                "confidence": report.get("confidence"),
                "answer_length": len(final.answer_text),
            }
            results.append(result)
            
            if show_timing:
                print(f"   ✓ {result['mode']} - {result['elapsed_sec']:.1f}s\n")
        
        except Exception as e:
            print(f"   ✗ Erreur: {e}\n")
            results.append({
                "question": question,
                "error": str(e),
            })
    
    # Résumé
    if show_timing and results:
        print(f"\n📊 Résumé du batch:")
        print(f"   Questions traitées: {len([r for r in results if 'error' not in r])}")
        print(f"   Temps total: {sum(r.get('elapsed_sec', 0) for r in results):.1f}s")
        print(f"   Temps moyen: {sum(r.get('elapsed_sec', 0) for r in results) / max(1, len(results)):.1f}s")
    
    return results


# ============================================================================
# TESTS ET VALIDATION
# ============================================================================

def test_complexity_analyzer():
    """Test l'analyseur de complexité sur des exemples."""
    
    analyzer = ComplexityAnalyzer()
    
    test_cases = [
        ("C'est quoi un nombre premier?", "rapide"),
        ("Reconstruis le 26e premier", "standard"),
        ("Rapport spectral 5x5: A={...} B={...}", "approfondi"),
        ("Section 13: pont logique Zêta + nombres négatifs", "très_complexe"),
    ]
    
    print("🧪 Test de l'analyseur de complexité:\n")
    
    for question, expected_mode in test_cases:
        profile = analyzer.analyze(question)
        status = "✓" if profile.mode.value == expected_mode else "✗"
        print(f"{status} {question[:50]:50} → {profile.mode.value:15} "
              f"(score={profile.complexity_score:5.1f}, loops={profile.num_loops})")


def test_cinematic_display():
    """Test l'affichage cinématique."""
    
    print("\n🧪 Test de l'affichage cinématique:\n")
    
    display = CinematicDisplay(num_loops=3, estimated_duration_sec=30)
    
    # Simuler progression
    for i in range(5):
        display.state.loop_current = i // 2
        display.state.iteration_current = i % 5 + 1
        print(display.render_cinematic_header())
        print()
        
        import time
        time.sleep(0.5)  # Simuler le travail


def test_fast_bypass():
    """Test le mode réponse rapide."""
    
    print("🧪 Test du bypass rapide:\n")
    
    test_questions = [
        "C'est quoi un nombre premier?",
        "Reconstruis le 26e premier",
        "Le 2e nombre premier?",
        "Définition du rapport 1/2",
    ]
    
    bypass = FastModeBypass()
    
    for q in test_questions:
        if answer := bypass.try_fast_response(q):
            print(f"✓ BYPASS: {q:40} → {answer[:60]}...")
        else:
            print(f"  NORMAL: {q:40} → (utiliser orchestrator)")


# ============================================================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    print("🧪 Mode Test - Exemples de cinématique\n")
    print("1. Test analyseur de complexité")
    test_complexity_analyzer()
    
    print("\n2. Test affichage cinématique")
    test_cinematic_display()
    
    print("\n3. Test bypass rapide")
    test_fast_bypass()
    
    print("\n✅ Tous les tests d'exemple sont terminés!")
    print("   Pour une intégration réelle, voir ask_gabriel_simple() ou ask_gabriel_advanced()")
