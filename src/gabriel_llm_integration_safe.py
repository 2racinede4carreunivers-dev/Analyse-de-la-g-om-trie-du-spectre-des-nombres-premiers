"""
Gabriel LLM Integration - Version SAFE BUDGET
Intègre Cost Manager pour protéger budget Claude
"""

import logging
from typing import Dict, Any, Optional

from src.llm_router import LLMRouter, TaskType
from src.prompt_injector import PromptInjector
from src.cost_manager import ClaudeBudgetManager

logger = logging.getLogger(__name__)

class GabrielLLMIntegrationSafeBudget:
    """Gabriel avec gestion budget Claude - version sûre"""
    
    def __init__(self, monthly_budget_usd: float = 7.0):
        """
        Initialise Gabriel avec budget protection
        
        Args:
            monthly_budget_usd: Budget mensuel en USD (défaut 7$)
        """
        self.router = LLMRouter()
        self.injector = PromptInjector()
        self.budget_manager = ClaudeBudgetManager(monthly_budget_usd=monthly_budget_usd)
        self.response_cache = {}
    
    def query_intelligent(self, 
                         question: str,
                         task_type: Optional[TaskType] = None,
                         use_theory_context: bool = True,
                         force_openai_if_budget_low: bool = True) -> Dict[str, Any]:
        """
        Requête intelligente avec protection budget
        
        Args:
            question: Question utilisateur
            task_type: Type de tâche (auto-détecté si None)
            use_theory_context: Injecter axiomes Savard
            force_openai_if_budget_low: Basculer OpenAI si budget proche limite
        
        Returns:
            Réponse complète avec métadonnées
        """
        
        logger.info(f"[Gabriel] Requête: {question[:50]}...")
        
        # 🛡️ VÉRIFIER BUDGET AVANT REQUÊTE
        budget_ok = self.budget_manager.check_budget()
        
        if not budget_ok:
            logger.warning("⚠️ Budget Claude atteint - Utiliser OpenAI seul")
            # Forcer OpenAI
            use_claude = False
        else:
            use_claude = True
        
        # Classifier si nécessaire
        if task_type is None:
            task_type = self.router.classify_task(question)
            logger.info(f"  → Tâche classifiée: {task_type.value}")
        
        # Injecter contexte théorique si applicable
        if use_theory_context:
            injected = self.injector.inject_for_ollama(question, str(task_type.value))
            prompt = injected
        else:
            prompt = question
        
        # Décider modèle
        decision = self.router.decide_model(task_type)
        
        # BUDGET CHECK: Si budget bas et tâche non-critique, utiliser OpenAI
        report = self.budget_manager.get_monthly_report()
        token_usage_percent = report['tokens']['percent_used']
        
        if token_usage_percent > 80 and force_openai_if_budget_low:
            logger.info(f"  ⚠️ Budget à {token_usage_percent:.0f}% - Utiliser OpenAI au lieu de Claude")
            decision.selected_model = 'openai'
        
        logger.info(f"  → Modèle sélectionné: {decision.selected_model.upper()}")
        logger.info(f"  → Budget utilisé: {token_usage_percent:.1f}%")
        
        # System prompt adapté
        system_prompt = self._build_system_prompt(task_type)
        
        try:
            # Requête via routeur
            response_text, metadata = self.router.query(
                prompt=prompt,
                task_type=task_type,
                system_prompt=system_prompt
            )
            
            # 📊 ENREGISTRER USAGE
            input_tokens = metadata.get('input_tokens', 0)
            output_tokens = metadata.get('output_tokens', 0)
            
            self.budget_manager.record_usage(input_tokens, output_tokens)
            
            logger.info(f"  ✓ Requête complète")
            logger.info(f"    Tokens: {input_tokens + output_tokens} (input={input_tokens}, output={output_tokens})")
            
            # Retourner avec métadonnées budget
            result = {
                'response': response_text,
                'model': metadata['model'],
                'task_type': task_type.value,
                'tokens': {
                    'total': input_tokens + output_tokens,
                    'input': input_tokens,
                    'output': output_tokens
                },
                'budget': {
                    'tokens_used_this_month': self.budget_manager.tokens_used_this_month,
                    'tokens_budget': self.budget_manager.monthly_token_budget,
                    'tokens_remaining': max(0, self.budget_manager.monthly_token_budget - self.budget_manager.tokens_used_this_month),
                    'cost_this_month': f"${self.budget_manager.cost_this_month:.2f}",
                    'cost_budget': f"${self.budget_manager.monthly_budget_usd:.2f}",
                    'percent_used': (self.budget_manager.tokens_used_this_month / self.budget_manager.monthly_token_budget) * 100
                }
            }
            
            return result
        
        except Exception as e:
            logger.error(f"  ✗ Erreur requête: {e}")
            return {
                'response': None,
                'error': str(e),
                'model': decision.selected_model
            }
    
    def _build_system_prompt(self, task_type: TaskType) -> str:
        """Construit system prompt adapté à la tâche"""
        
        base_prompt = """Tu es Gabriel, un assistant mathématique multiloop de haut niveau.

Ton expertise couvre:
- Théorie personnelle "L'univers est au carré" (Philippe Thomas Savard)
- Géométrie spectrale asymétrique des nombres premiers
- Analyse RSA (Rapport Spectral Asymétrique Ordonné)
- Preuves formelles en HOL4/Lean4
- Validation de structures mathématiques rigoureuses

IMPORTANT: Réponses COURTES et DIRECTES (≤ 150 mots si possible)
pour optimiser utilisation tokens."""
        
        if task_type == TaskType.MATHEMATICAL_REASONING:
            return base_prompt + "\nFOCUS: Raisonnement clair, structuré, économe."
        elif task_type == TaskType.CODE_VALIDATION:
            return base_prompt + "\nFOCUS: Validation code HOL4/Lean4 concise."
        elif task_type == TaskType.HOL_PROOF_GENERATION:
            return base_prompt + "\nFOCUS: Preuves complètes mais sans verbosité."
        elif task_type == TaskType.RIEMANN_ANALYSIS:
            return base_prompt + "\nFOCUS: Analyse géométrie spectrale directe."
        else:
            return base_prompt
    
    def print_budget_report(self):
        """Affiche rapport budget courant"""
        self.budget_manager.print_budget_report()
    
    def get_budget_status(self) -> Dict[str, Any]:
        """Retourne statut budget sans rapport complet"""
        
        report = self.budget_manager.get_monthly_report()
        
        return {
            'tokens_percent': report['tokens']['percent_used'],
            'cost_percent': report['cost']['percent_used'],
            'tokens_remaining': report['tokens']['remaining'],
            'cost_remaining': report['cost']['remaining'],
            'requests_count': report['requests']
        }


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("="*70)
    print("GABRIEL LLM INTEGRATION - SAFE BUDGET MODE")
    print("="*70)
    
    # Initialiser avec budget safe
    gabriel = GabrielLLMIntegrationSafeBudget(monthly_budget_usd=7.0)
    
    # Test 1: Requête standard
    print("\n[TEST 1] Requête mathématique")
    result = gabriel.query_intelligent(
        "Explique brièvement RSA et sa convergence vers 0.5"
    )
    
    if result.get('response'):
        print(f"✓ Réponse obtenue ({result['tokens']['total']} tokens)")
        print(f"  Modèle: {result['model'].upper()}")
        print(f"  Budget: {result['budget']['percent_used']:.1f}% utilisé")
    
    # Afficher rapport
    print("\n[BUDGET REPORT]")
    gabriel.print_budget_report()
