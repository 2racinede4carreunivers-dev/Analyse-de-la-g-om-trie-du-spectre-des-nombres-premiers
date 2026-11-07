"""
Gabriel LLM Integration v2 - Utilise Router v2 avec Claude PRIORITAIRE
Intègre effort cognitif, système SPLIT 75/25, Ollama DÉSACTIVÉ
"""

import logging
from typing import Dict, Any, Optional

from src.llm_router_v2 import LLMRouterV2, TaskType, CognitiveEffort
from memory.prompt_injector_enhanced import PromptInjector

logger = logging.getLogger(__name__)

class GabrielLLMIntegrationV2:
    """Gabriel v6.0 - Claude Prioritaire avec Effort Cognitif"""
    
    def __init__(self, monthly_budget_usd: float = 7.0):
        """
        Initialise Gabriel v2 avec routeur nouveau
        
        Architecture:
        - Claude: PRIORITAIRE (tâches logiques/mathématiques)
        - OpenAI: Fallback + tâches simples
        - Ollama: DÉSACTIVÉ
        - SPLIT: 75% Claude + 25% OpenAI si effort mixte
        """
        
        try:
            self.router = LLMRouterV2()
            self.injector = PromptInjector()
            self.monthly_budget_usd = monthly_budget_usd
            self.response_cache = {}
            
            logger.info("✅ Gabriel v6.0 Initialized")
            logger.info("   Architecture: Claude > OpenAI")
            logger.info("   Cognitive Effort: Analyzed")
            logger.info("   Split Mode: 75/25 available")
            logger.info("   Ollama: DISABLED")
            
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            raise
    
    def query_intelligent(self, 
                         question: str,
                         task_type: Optional[TaskType] = None,
                         use_theory_context: bool = True,
                         validate_response: bool = True,
                         force_model: Optional[str] = None,
                         analyze_split: bool = True) -> Dict[str, Any]:
        """
        Requête intelligente avec détection d'effort cognitif
        
        Args:
            question: Requête utilisateur
            task_type: Type de tâche (auto-classifié si None)
            use_theory_context: Injecter axiomes Savard
            validate_response: Valider conformité réponse
            force_model: Force Claude/OpenAI/split
            analyze_split: Analyser si split 75/25 optimal
        
        Returns:
            Réponse avec métadonnées complètes + effort cognitif
        """
        
        logger.info(f"[Gabriel] Requête: {question[:50]}...")
        
        # 1️⃣ Classifier tâche
        if task_type is None:
            task_type = self.router.classify_task(question)
            logger.info(f"  → Tâche classifiée: {task_type.value[0]}")
        
        # 2️⃣ Analyser effort cognitif
        effort = self.router.analyze_cognitive_effort(question)
        logger.info(f"  → Effort cognitif: {effort.value}")
        
        # 3️⃣ Décider si SPLIT optimal
        use_split = False
        if analyze_split and effort == CognitiveEffort.MEDIUM and not force_model:
            # Analyser composition query
            hard_words = sum(1 for w in ['mathématique', 'riemann', 'spectre', 'hol', 'preuve'] if w in question.lower())
            easy_words = sum(1 for w in ['explique', 'simple', 'résumé'] if w in question.lower())
            
            if hard_words > easy_words:
                use_split = True
                logger.info("  → Effort mixte détecté → Mode SPLIT 75% Claude / 25% OpenAI")
        
        # 4️⃣ Injecter contexte théorique si applicable
        if use_theory_context and 'riemann' in question.lower() or 'rsa' in question.lower():
            injected = self.injector.inject_for_claude_hol(question)
            prompt = injected
            logger.info("  → Axiomes Savard injectés")
        else:
            prompt = question
        
        # 5️⃣ Construire system prompt adapté
        system_prompt = self._build_system_prompt(task_type, effort)
        
        try:
            # 6️⃣ Routage avec support SPLIT
            if force_model:
                logger.info(f"  → Forcer modèle: {force_model}")
                response_text, metadata = self.router.query(
                    prompt=prompt,
                    task_type=task_type,
                    system_prompt=system_prompt,
                    force_model=force_model
                )
            else:
                response_text, metadata = self.router.query(
                    prompt=prompt,
                    task_type=task_type,
                    system_prompt=system_prompt
                )
            
            # 7️⃣ Validation si requise
            validation_result = {}
            if validate_response and task_type != TaskType.CONTENT_GENERATION:
                validation_result = self.injector.validate_llm_response(
                    response_text,
                    task_type.value[0]
                )
            
            # 8️⃣ Construire réponse finale
            result = {
                'response': response_text,
                'model': metadata['model'],
                'task_type': task_type.value[0],
                'cognitive_effort': effort.value,
                'routing': metadata.get('routing', {}),
                'tokens': metadata.get('tokens_used', 0),
                'tokens_detail': {
                    'input': metadata.get('input_tokens', 0),
                    'output': metadata.get('output_tokens', 0)
                },
                'validation': validation_result,
                'split_info': None
            }
            
            # Ajouter info split si utilisé
            if metadata['model'] == 'split':
                result['split_info'] = {
                    'ratio': metadata.get('split_ratio', {}),
                    'claude_tokens': metadata.get('claude_tokens', 0),
                    'openai_tokens': metadata.get('openai_tokens', 0)
                }
            
            logger.info(f"  ✓ Réponse obtenue ({result['tokens']} tokens via {metadata['model'].upper()})")
            
            return result
        
        except Exception as e:
            logger.error(f"  ✗ Erreur requête: {e}")
            return {
                'response': None,
                'error': str(e),
                'model': 'error',
                'task_type': task_type.value[0] if task_type else 'unknown',
                'cognitive_effort': effort.value if effort else 'unknown'
            }
    
    def _build_system_prompt(self, task_type: TaskType, effort: CognitiveEffort) -> str:
        """Construit system prompt adapté à tâche + effort"""
        
        base = "Tu es Gabriel, un assistant mathématique multiloop expert."
        
        # Ajouter directives spécifiques effort
        if effort == CognitiveEffort.VERY_HIGH:
            base += "\n\nNIVEAU DE RIGUEUR: MAXIMUM\n- Raisonnement formel requis\n- Preuves complètes\n- Pas d'approximations"
        
        elif effort == CognitiveEffort.HIGH:
            base += "\n\nNIVEAU DE RIGUEUR: ÉLEVÉ\n- Logique rigoureuse\n- Justifications détaillées\n- Structure claire"
        
        elif effort == CognitiveEffort.MEDIUM:
            base += "\n\nNIVEAU DE RIGUEUR: ÉQUILIBRÉ\n- Clair et rigoureux\n- Exemples quand pertinent\n- Accessible"
        
        else:  # LOW
            base += "\n\nNIVEAU DE RIGUEUR: SIMPLE\n- Explications accessibles\n- Exemples concrets\n- Pas de jargon excessif"
        
        # Directives spécifiques tâche
        if task_type == TaskType.MATHEMATICAL_REASONING:
            base += "\n\nTAÂCHE: Raisonnement mathématique rigoureux\n- Structurer clairement les étapes\n- Justifier chaque affirmation"
        
        elif task_type == TaskType.RIEMANN_ANALYSIS:
            base += "\n\nTAÂCHE: Analyse géométrie spectrale\n- Appliquer théorie Savard (Sr2=1.5, RSA)\n- Ordres multiples (k=1,2,3)\n- Jamais théorie classique"
        
        elif task_type == TaskType.HOL_PROOF_GENERATION:
            base += "\n\nTAÂCHE: Génération preuves HOL/Isabelle\n- Code syntaxiquement valide UNIQUEMENT\n- Formules Savard exactes\n- Structures theory...end"
        
        elif task_type == TaskType.CONTENT_GENERATION:
            base += "\n\nTAÂCHE: Génération contenu\n- Éloquence textuelle\n- Communication claire"
        
        return base
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Retourne statistiques routage Gabriel"""
        
        stats = self.router.get_routing_stats()
        
        return {
            'summary': stats['summary'],
            'percentages': stats['percentages'],
            'tokens': stats['tokens'],
            'architecture': {
                'primary': 'Claude-3.5-Sonnet',
                'secondary': 'GPT-4o',
                'tertiary': 'Split 75/25',
                'ollama': 'DISABLED'
            }
        }
    
    def print_routing_stats(self):
        """Affiche statistiques routage formatées"""
        
        stats = self.get_routing_stats()
        
        print("\n" + "="*70)
        print("GABRIEL v6.0 ROUTING STATISTICS")
        print("="*70)
        
        print(f"\n📊 REQUÊTES:")
        print(f"  Total: {stats['summary']['total_requests']}")
        print(f"  Claude: {stats['summary']['claude_requests']} ({stats['percentages']['claude_percent']:.1f}%)")
        print(f"  OpenAI: {stats['summary']['openai_requests']} ({stats['percentages']['openai_percent']:.1f}%)")
        print(f"  Split: {stats['summary']['split_requests']} ({stats['percentages']['split_percent']:.1f}%)")
        
        print(f"\n💾 TOKENS:")
        print(f"  Claude: {stats['tokens']['claude_total']}")
        print(f"  OpenAI: {stats['tokens']['openai_total']}")
        
        print(f"\n🏗️ ARCHITECTURE:")
        for key, val in stats['architecture'].items():
            print(f"  {key}: {val}")
        
        print("\n" + "="*70)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*70)
    print("GABRIEL v6.0 - INTEGRATION TEST")
    print("="*70)
    
    try:
        gabriel = GabrielLLMIntegrationV2()
        
        print("\n✅ Gabriel initialized successfully")
        print("\nArchitecture:")
        print("  - Claude: PRIORITAIRE (TRÈS DIFFICILE, DIFFICILE)")
        print("  - OpenAI: Fallback + tâches SIMPLES")
        print("  - Split: 75% Claude / 25% OpenAI (effort MIXTE)")
        print("  - Ollama: DÉSACTIVÉ")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
