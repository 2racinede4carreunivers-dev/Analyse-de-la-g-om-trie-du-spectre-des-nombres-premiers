"""
GUIDE D'INTÉGRATION: Mode Cinématique Intelligent + Analyseur de Complexité

Ce document explique comment intégrer les nouveaux modules d'analyse de
complexité et d'affichage cinématique dans Gabriel.

====================================================================
MODULES CRÉÉS
====================================================================

1. src/ui/complexity_analyzer.py
   - ComplexityAnalyzer: Analyse la requête et détecte le nombre de loops
   - ResponseMode: Enum (RAPIDE, STANDARD, APPROFONDI, TRÈS_COMPLEXE)
   - ComplexityProfile: Résultat de l'analyse

2. src/ui/cinematic_display.py
   - CinematicDisplay: Gère l'affichage cinématique avec chronomètre
   - CinematicState: État courant (temps, progression, étapes)
   - CinematicProgressCallback: Adaptateur pour pipeline.process()

3. src/ui/cinematic_orchestrator.py
   - CinematicOrchestrator: Orchestre l'analyse + affichage
   - FastModeBypass: Détecte les questions triviales pour réponse instantanée

====================================================================
UTILISATION: INTÉGRATION DANS main_cli.py
====================================================================

Exemple d'intégration simple dans la boucle de l'agent:

    # Dans run_cli() ou ask_gabriel()
    from src.ui.cinematic_orchestrator import CinematicOrchestrator, FastModeBypass
    
    orch = CinematicOrchestrator(pipeline, verbose=True)
    bypass = FastModeBypass()
    
    while True:
        question = input("Gabriel> ")
        
        # 1. Tenter une réponse rapide triviale
        if fast_answer := bypass.try_fast_response(question):
            print(f"[Réponse immédiate] {fast_answer}\\n")
            continue
        
        # 2. Sinon, utiliser l'orchestrator avec cinématique
        try:
            final_answer = await orch.process(
                question,
                print_cinematic=True,  # Affiche chronomètre + loops
            )
            print(final_answer.answer_text)
            
            # 3. Afficher le rapport de complexité (optionnel)
            report = orch.get_complexity_report()
            print(f"\\n[Complexité] Mode: {report['mode']}, "
                  f"Loops: {report['num_loops']}, "
                  f"Temps: {report['elapsed_sec']:.1f}s")
        
        except Exception as e:
            print(f"[Erreur] {e}")

====================================================================
AFFICHAGE CINÉMATIQUE: EXEMPLE DE SORTIE
====================================================================

╔════════════════════════════════════════════════════════════════╗
║  GABRIEL - Mode Réponse Intelligente (Cinématique)            ║
╠════════════════════════════════════════════════════════════════╣
║  Loops prévues: 1/3                                            ║
║  ⏱️ 00:12 / ~00:18                                              ║
║  [██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 45% ⠹          ║
║  🔄 Boucle multi-itération                                      ║
║  📍 Loops complétées:                                           ║
║     ✓ Loop 1/5 terminée                                        ║
║                                                                ║
║  🔄 Loop 2/3 en cours...                                       ║
║     Itération 3/5                                              ║
║                                                                ║
║  📝 Derniers événements:                                       ║
║     • abstraction_done @ 00:02                                 ║
║     • meta_reasoning_done @ 00:04                              ║
║     • multiloop_iteration @ 00:10                              ║
╚════════════════════════════════════════════════════════════════╝

====================================================================
MODES DE RÉPONSE AUTODETECTÉS
====================================================================

Mode RAPIDE (1 loop)
  Durée: 5-10 secondes
  Cas d'usage:
    - Questions définitionnelles simples
    - "C'est quoi un nombre premier?"
    - "Explique le rapport 1/2"
    - Singleton numérique connu
  
  Activation auto si:
    - Score de complexité < 20
    - ≤ 2 facteurs de complexité
    - Pas d'objectifs multiples

Mode STANDARD (2 loops)
  Durée: 15-20 secondes
  Cas d'usage:
    - Reconstruction simple d'un nombre premier
    - "Reconstruis le 26e premier"
    - "Calcule le rapport spectral 1/2"
    - Questions avec 1-2 valeurs numériques
  
  Activation auto si:
    - Score de complexité 20-40
    - Intention clear (reconstruction, gap)

Mode APPROFONDI (3 loops)
  Durée: 25-35 secondes
  Cas d'usage:
    - Rapport spectral n×m explicite
    - "Configuration symétrique 3×3"
    - Comparaison entre deux domaines
    - Vérification + justification demandée
  
  Activation auto si:
    - Score de complexité 40-65
    - Facteurs multiples (ratio + comparaison)

Mode TRÈS COMPLEXE (4 loops)
  Durée: 40-60 secondes
  Cas d'usage:
    - Questions théoriques avancées (Section 13)
    - "Pont logique Savard <-> Zêta"
    - Requêtes multi-objectifs (2+ objectifs techniques)
    - Négatives + domaines étendus
  
  Activation auto si:
    - Score de complexité > 65
    - Patterns théoriques avancés détectés
    - Multi-objectifs explicites

====================================================================
FACTEURS DE COMPLEXITÉ DÉTECTÉS
====================================================================

Chaque analyse identifie les facteurs qui augmentent la complexité:

✓ reconstruction de nombre premier
✓ calcul de rapport spectral
✓ calcul d'écart entre nombres premiers
✓ question théorique avancée (Section 13)
✓ requête multi-objectifs
✓ configuration n×m explicite
✓ tuples nommés (Bloc A, Bloc B)
✓ nombres négatifs (domaine étendu)
✓ vérification/validation demandée
✓ comparaison ou analyse différentielle
✓ théorie analytique des nombres (Zêta, Chebyshev)
✓ démonstration/preuve formelle

====================================================================
CONFIGURATION ET PERSONNALISATION
====================================================================

Pour ajuster les seuils de complexité:

    # Dans complexity_analyzer.py, modifier _calculate_complexity_score()
    score += min(numbers / 20, 10)    # ← augmenter si trop sensible
    score += min(math_symbols * 2, 15)  # ← ajuster ici

Pour modifier les durées estimées:

    # Dans _estimate_duration()
    base_times = {
        1: 8,    # ← rapidité de mode RAPIDE
        2: 18,   # ← temps mode STANDARD
        3: 30,   # ← temps mode APPROFONDI
        4: 50,   # ← temps mode TRÈS COMPLEXE
    }

Pour ajouter des patterns de réponse rapide:

    # Dans FastModeBypass.FAST_PATTERNS
    r"mon pattern": "Ma réponse prédéfinie",

====================================================================
INTÉGRATION AVEC PROGRESS CALLBACKS
====================================================================

Le CinematicDisplay se met à jour automatiquement via le progress_cb
existant du pipeline. Les événements supportés:

progression de l'étape pipeline:
  - abstraction_done
  - intent_hypotheses
  - meta_reasoning_done
  - multiloop_iteration
  - spectral_compute_done
  - silent_audit_done
  - pipeline_done

Chaque événement met à jour:
  - L'étage courant (stage_label)
  - Les loop/iteration en cours
  - Le log des événements affichés

====================================================================
DÉPLOIEMENT
====================================================================

1. Copier les 3 nouveaux fichiers:
   - src/ui/complexity_analyzer.py
   - src/ui/cinematic_display.py
   - src/ui/cinematic_orchestrator.py

2. Mettre à jour src/ui/__init__.py pour exposer:
   
   from .complexity_analyzer import ComplexityAnalyzer, ResponseMode
   from .cinematic_display import CinematicDisplay
   from .cinematic_orchestrator import CinematicOrchestrator, FastModeBypass

3. Modifier src/ui/cli.py (ou ask_gabriel.py) pour:
   
   # Remplacer l'appel pipeline.process() par:
   orch = CinematicOrchestrator(pipeline)
   final_answer = await orch.process(question, print_cinematic=True)

4. (Optionnel) Reconstruire l'image Docker:
   
   docker build -f Dockerfile.cli -t llm-agent-multiloop:latest .

====================================================================
PERFORMANCE ET OPTIMISATIONS
====================================================================

✓ Caching: Les profils de complexité sont cachés (même question = même profil)
✓ Async: Compatible avec async/await du pipeline
✓ Rich optional: Fonctionne avec ou sans la bibliothèque Rich
✓ Legger: < 50 KB de code supplémentaire
✓ Zero-impact: Aucun changement au pipeline existant

====================================================================
TESTS ET VALIDATION
====================================================================

Tester l'analyseur de complexité:

    from src.ui.complexity_analyzer import ComplexityAnalyzer
    
    analyzer = ComplexityAnalyzer()
    
    # Test RAPIDE
    profile = analyzer.analyze("C'est quoi un nombre premier?")
    assert profile.mode.value == "rapide"
    assert profile.num_loops == 1
    
    # Test TRÈS_COMPLEXE
    profile = analyzer.analyze(
        "Rapport spectral symétrique 5×5: "
        "Bloc A = {2,3,5,7,11} Bloc B = {13,17,19,23,29} "
        "avec validation Zêta et Section 13"
    )
    assert profile.num_loops >= 3

Tester le cinématique:

    display = CinematicDisplay(num_loops=3, estimated_duration_sec=30)
    
    # Simuler des événements
    display.update_from_progress_event({\"event\": \"abstraction_done\"})
    display.update_from_progress_event({
        \"event\": \"multiloop_iteration\",
        \"loop\": 1,
        \"iteration\": 2,
    })
    
    print(display.render_cinematic_header())

====================================================================
TROUBLESHOOTING
====================================================================

Q: Le mode Rapide ne s'active pas
A: Vérifier que le score de complexité < 20 et len(factors) <= 2
   Modifier les seuils dans _calculate_complexity_score()

Q: Les étapes n'apparaissent pas dans le cinématique
A: Vérifier que le pipeline appelle progress_cb avec "event" key
   Ajouter des logs: logger.debug(event)

Q: Affichage cinématique lagge
A: Désactiver l'affichage à chaque événement (ne mettre à jour qu'à la fin)
   ou réduire la fréquence des mises à jour

Q: Temps estimé incorrect
A: Ajuster base_times dans _estimate_duration()
   ou réduire estimated_duration_sec en entrée

====================================================================
"""

# Code d'exemple complet d'intégration

INTEGRATION_EXAMPLE = """
# Dans src/ui/ask_gabriel.py ou src/ui/cli.py

async def ask_gabriel_with_cinematic(pipeline, question: str) -> FinalAnswer:
    '''
    Traite une question Gabriel avec cinématique intelligente.
    
    Args:
        pipeline: Instance Pipeline configurée
        question: Question de l'utilisateur
    
    Returns:
        FinalAnswer avec métadonnées de complexité
    '''
    from .cinematic_orchestrator import CinematicOrchestrator, FastModeBypass
    
    # Tentative de réponse rapide triviale
    bypass = FastModeBypass()
    if fast_answer := bypass.try_fast_response(question):
        print(f"\\n✨ Réponse immédiate:\\n{fast_answer}\\n")
        # Retourner un FinalAnswer stub
        return FinalAnswer(
            question_id="fast-bypass",
            answer_text=fast_answer,
            confidence=1.0,
            iterations_used=0,
            best_score=10.0,
        )
    
    # Orchestration complète avec cinématique
    orch = CinematicOrchestrator(pipeline, verbose=True)
    
    try:
        final_answer = await orch.process(
            question,
            print_cinematic=True,  # Afficher chronomètre + loops
        )
        
        # Optionnel: Afficher le rapport détaillé
        report = orch.get_complexity_report()
        print(f"\\n📊 Analyse de complexité:")
        print(f"   Mode: {report['mode']}")
        print(f"   Loops exécutées: {report['num_loops']}")
        print(f"   Temps réel: {report['elapsed_sec']:.1f}s")
        print(f"   Facteurs: {', '.join(report['factors'][:3])}")
        
        return final_answer
    
    except Exception as e:
        print(f"\\n❌ Erreur pipeline: {e}")
        raise
"""
