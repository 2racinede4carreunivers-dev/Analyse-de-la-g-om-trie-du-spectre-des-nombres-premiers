"""
LLM Router - Routage intelligent Claude (prioritaire) → OpenAI (fallback)
Route chaque requête vers le meilleur modèle selon la tâche
"""

import logging
import os
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import time

import anthropic
import openai

logger = logging.getLogger(__name__)

class TaskType(Enum):
    """Types de tâches avec modèles optimaux"""
    # Claude excelle
    MATHEMATICAL_REASONING = "mathematical_reasoning"      # Claude★★★★★
    CODE_VALIDATION = "code_validation"                    # Claude★★★★★
    HOL_PROOF_GENERATION = "hol_proof_generation"         # Claude★★★★★
    LOGICAL_STRUCTURE = "logical_structure"               # Claude★★★★★
    RIEMANN_ANALYSIS = "riemann_analysis"                 # Claude★★★★★
    FORMAL_VERIFICATION = "formal_verification"           # Claude★★★★★
    
    # OpenAI excelle
    CONTENT_GENERATION = "content_generation"             # OpenAI★★★★★
    WEB_SCRIPTING = "web_scripting"                       # OpenAI★★★★★
    QUICK_OPTIMIZATION = "quick_optimization"            # OpenAI★★★★★
    TEXT_FLUENCY = "text_fluency"                        # OpenAI★★★★★
    
    # Indifférent
    GENERAL = "general"                                   # Indifférent
    FALLBACK = "fallback"                                 # Utiliser disponible

@dataclass
class ModelConfig:
    """Configuration pour un modèle"""
    name: str
    api_key: str
    model_id: str
    max_tokens: int = 1500  # RÉDUIT de 4096 pour économiser tokens
    temperature: float = 0.7
    priority: int = 1  # 1=highest, 999=lowest
    rate_limit_rpm: int = 3500  # Requêtes par minute
    rate_limit_tpm: int = 90000  # Tokens par minute
    monthly_token_budget: int = 500000  # ~$5-7 USD

@dataclass
class RoutingDecision:
    """Décision de routage"""
    selected_model: str
    task_type: TaskType
    reason: str
    fallback_model: Optional[str] = None
    estimated_cost: Optional[float] = None

class LLMRouter:
    """Routeur intelligent entre Claude et OpenAI"""
    
    def __init__(self):
        """Initialise routeur et clients"""
        self.claude_config = self._init_claude()
        self.openai_config = self._init_openai()
        
        self.claude_client = None
        self.openai_client = None
        
        if self.claude_config:
            self.claude_client = anthropic.Anthropic(api_key=self.claude_config.api_key)
        
        if self.openai_config:
            self.openai_client = openai.OpenAI(api_key=self.openai_config.api_key)
        
        self.request_history = []
        self.rate_limit_tracking = {
            'claude': {
                'requests': 0,
                'tokens': 0,
                'reset_time': time.time(),
                'monthly_tokens': 0,
                'month_start': time.time()
            },
            'openai': {
                'requests': 0,
                'tokens': 0,
                'reset_time': time.time(),
                'monthly_tokens': 0,
                'month_start': time.time()
            }
        }
    
    def _init_claude(self) -> Optional[ModelConfig]:
        """Initialise configuration Claude"""
        api_key = os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            logger.warning("CLAUDE_API_KEY non trouvée - Claude désactivé")
            return None
        
        return ModelConfig(
            name="Claude",
            api_key=api_key,
            model_id=os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),  # CLAUDE_MODEL du .env ou defaut 2026
            max_tokens=4096,
            temperature=0.7,
            priority=1,  # Prioritaire
            rate_limit_rpm=3500,
            rate_limit_tpm=90000
        )
    
    def _init_openai(self) -> Optional[ModelConfig]:
        """Initialise configuration OpenAI"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            logger.warning("OPENAI_API_KEY non trouvée - OpenAI désactivé")
            return None
        
        return ModelConfig(
            name="OpenAI",
            api_key=api_key,
            model_id="gpt-4o",
            max_tokens=4096,
            temperature=0.7,
            priority=2,  # Fallback
            rate_limit_rpm=10000,
            rate_limit_tpm=2000000
        )
    
    def classify_task(self, query: str) -> TaskType:
        """Classe automatiquement la tâche"""
        
        query_lower = query.lower()
        
        # Claude-optimised tasks
        claude_keywords = {
            TaskType.MATHEMATICAL_REASONING: ['mathématique', 'calcul', 'équation', 'théorème', 'preuve'],
            TaskType.CODE_VALIDATION: ['code', 'valide', 'syntax', 'erreur', 'debug', 'hol4', 'lean'],
            TaskType.HOL_PROOF_GENERATION: ['hol4', 'isabelle', 'proof', 'preuve', 'théorème'],
            TaskType.LOGICAL_STRUCTURE: ['structure', 'logique', 'axiome', 'principe', 'géométrie'],
            TaskType.RIEMANN_ANALYSIS: ['riemann', 'zéro', 'spectre', 'rsa', 'convergence'],
            TaskType.FORMAL_VERIFICATION: ['formel', 'vérif', 'certification', 'valide'],
        }
        
        # OpenAI-optimised tasks
        openai_keywords = {
            TaskType.CONTENT_GENERATION: ['texte', 'article', 'description', 'contenu', 'script web'],
            TaskType.WEB_SCRIPTING: ['web', 'script', 'javascript', 'html', 'css', 'react'],
            TaskType.QUICK_OPTIMIZATION: ['rapide', 'optimization', 'amélioration', 'perfomance'],
            TaskType.TEXT_FLUENCY: ['fluidité', 'éloquence', 'communication', 'explication simple'],
        }
        
        # Chercher correspondances Claude
        for task_type, keywords in claude_keywords.items():
            if any(kw in query_lower for kw in keywords):
                return task_type
        
        # Chercher correspondances OpenAI
        for task_type, keywords in openai_keywords.items():
            if any(kw in query_lower for kw in keywords):
                return task_type
        
        # Défaut
        return TaskType.GENERAL
    
    def decide_model(self, task_type: TaskType) -> RoutingDecision:
        """Décide quel modèle utiliser"""
        
        # Mappings tâche → modèle optimal
        task_to_model = {
            # Claude prioritaire
            TaskType.MATHEMATICAL_REASONING: ('claude', 'Expert en structures mathématiques'),
            TaskType.CODE_VALIDATION: ('claude', 'Excellent validateur de code formel'),
            TaskType.HOL_PROOF_GENERATION: ('claude', 'Spécialiste preuves HOL4/Lean'),
            TaskType.LOGICAL_STRUCTURE: ('claude', 'Maître en structures logiques'),
            TaskType.RIEMANN_ANALYSIS: ('riemann', 'Analyse géométrie spectrale'),
            TaskType.FORMAL_VERIFICATION: ('claude', 'Vérification formelle rigoureuse'),
            
            # OpenAI pour certaines tâches
            TaskType.CONTENT_GENERATION: ('openai', 'Générateur de contenu fluide'),
            TaskType.WEB_SCRIPTING: ('openai', 'Scripting web rapide'),
            TaskType.QUICK_OPTIMIZATION: ('openai', 'Optimisation rapide'),
            TaskType.TEXT_FLUENCY: ('openai', 'Texte éloquent et clair'),
            
            # Fallback
            TaskType.GENERAL: ('claude', 'Claude en première ligne'),
            TaskType.FALLBACK: ('openai', 'Fallback sur OpenAI'),
        }
        
        selected, reason = task_to_model.get(task_type, ('claude', 'Défaut: Claude prioritaire'))
        
        # Vérifier disponibilité
        if selected == 'claude' and not self.claude_config:
            logger.warning("Claude non disponible, basculement OpenAI")
            selected = 'openai'
            reason = "Claude indisponible, fallback"
        
        elif selected == 'openai' and not self.openai_config:
            logger.warning("OpenAI non disponible, basculement Claude")
            selected = 'claude'
            reason = "OpenAI indisponible, fallback"
        
        # Vérifier rate limits
        if selected == 'claude' and self._is_rate_limited('claude'):
            logger.info("Rate limit Claude - basculement OpenAI")
            selected = 'openai'
            reason = "Rate limit Claude atteint"
        
        elif selected == 'openai' and self._is_rate_limited('openai'):
            logger.info("Rate limit OpenAI - basculement Claude")
            selected = 'claude'
            reason = "Rate limit OpenAI atteint"
        
        fallback = 'openai' if selected == 'claude' else 'claude'
        
        return RoutingDecision(
            selected_model=selected,
            task_type=task_type,
            reason=reason,
            fallback_model=fallback
        )
    
    def _is_rate_limited(self, model: str) -> bool:
        """Vérifie si modèle est rate-limited"""
        
        tracking = self.rate_limit_tracking.get(model)
        if not tracking:
            return False
        
        # Réinitialiser toutes les minutes
        if time.time() - tracking['reset_time'] > 60:
            tracking['requests'] = 0
            tracking['tokens'] = 0
            tracking['reset_time'] = time.time()
            return False
        
        # Vérifier limits
        config = self.claude_config if model == 'claude' else self.openai_config
        
        if tracking['requests'] >= config.rate_limit_rpm * 0.9:  # 90% du limit
            return True
        
        if tracking['tokens'] >= config.rate_limit_tpm * 0.9:
            return True
        
        return False
    
    def query(self, prompt: str, task_type: Optional[TaskType] = None, 
              system_prompt: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Route requête vers meilleur modèle
        
        Returns:
            (response_text, metadata)
        """
        
        # Classifier si nécessaire
        if task_type is None:
            task_type = self.classify_task(prompt)
        
        # Décider modèle
        decision = self.decide_model(task_type)
        
        logger.info(f"[{decision.selected_model.upper()}] {decision.reason}")
        
        try:
            if decision.selected_model == 'claude':
                response, metadata = self._query_claude(prompt, system_prompt)
            else:
                response, metadata = self._query_openai(prompt, system_prompt)
            
            # Enregistrer historique
            self.request_history.append({
                'task_type': task_type.value,
                'model': decision.selected_model,
                'timestamp': time.time(),
                'tokens': metadata.get('tokens_used', 0)
            })
            
            metadata['routing_decision'] = decision.__dict__
            
            return response, metadata
        
        except Exception as e:
            logger.error(f"Erreur {decision.selected_model}: {e}")
            
            # Essayer fallback
            if decision.fallback_model:
                logger.info(f"Basculement vers {decision.fallback_model}")
                return self._query_fallback(prompt, system_prompt, decision.fallback_model)
            
            raise
    
    def _query_claude(self, prompt: str, system_prompt: Optional[str] = None) -> Tuple[str, Dict]:
        """Requête Claude"""
        
        if not self.claude_client:
            raise ValueError("Claude client non initialisé")
        
        messages = [{"role": "user", "content": prompt}]
        
        response = self.claude_client.messages.create(
            model=self.claude_config.model_id,
            max_tokens=self.claude_config.max_tokens,
            system=system_prompt or "Tu es un assistant mathématique expert.",
            messages=messages,
            temperature=self.claude_config.temperature
        )
        
        text = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        
        # Mettre à jour tracking
        self.rate_limit_tracking['claude']['requests'] += 1
        self.rate_limit_tracking['claude']['tokens'] += tokens
        
        return text, {
            'model': 'claude',
            'tokens_used': tokens,
            'input_tokens': response.usage.input_tokens,
            'output_tokens': response.usage.output_tokens
        }
    
    def _query_openai(self, prompt: str, system_prompt: Optional[str] = None) -> Tuple[str, Dict]:
        """Requête OpenAI"""
        
        if not self.openai_client:
            raise ValueError("OpenAI client non initialisé")
        
        messages = [
            {"role": "system", "content": system_prompt or "Tu es un assistant expert."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.openai_client.chat.completions.create(
            model=self.openai_config.model_id,
            messages=messages,
            max_tokens=self.openai_config.max_tokens,
            temperature=self.openai_config.temperature
        )
        
        text = response.choices[0].message.content
        tokens = response.usage.prompt_tokens + response.usage.completion_tokens
        
        # Mettre à jour tracking
        self.rate_limit_tracking['openai']['requests'] += 1
        self.rate_limit_tracking['openai']['tokens'] += tokens
        
        return text, {
            'model': 'openai',
            'tokens_used': tokens,
            'input_tokens': response.usage.prompt_tokens,
            'output_tokens': response.usage.completion_tokens
        }
    
    def _query_fallback(self, prompt: str, system_prompt: Optional[str], 
                       fallback_model: str) -> Tuple[str, Dict]:
        """Essayer fallback"""
        
        if fallback_model == 'claude':
            return self._query_claude(prompt, system_prompt)
        elif fallback_model == 'openai':
            return self._query_openai(prompt, system_prompt)
        else:
            raise ValueError(f"Modèle fallback inconnu: {fallback_model}")
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Retourne statistiques routage"""
        
        claude_count = sum(1 for r in self.request_history if r['model'] == 'claude')
        openai_count = sum(1 for r in self.request_history if r['model'] == 'openai')
        claude_tokens = sum(r['tokens'] for r in self.request_history if r['model'] == 'claude')
        openai_tokens = sum(r['tokens'] for r in self.request_history if r['model'] == 'openai')
        
        return {
            'total_requests': len(self.request_history),
            'claude_requests': claude_count,
            'openai_requests': openai_count,
            'claude_tokens': claude_tokens,
            'openai_tokens': openai_tokens,
            'claude_percentage': (claude_count / len(self.request_history) * 100) if self.request_history else 0,
            'rate_limit_status': self.rate_limit_tracking
        }


if __name__ == '__main__':
    # Test
    logging.basicConfig(level=logging.INFO)
    
    router = LLMRouter()
    
    print("="*70)
    print("LLM ROUTER TEST")
    print("="*70)
    
    # Test 1: Tâche mathématique (Claude)
    print("\n[TEST 1] Requête mathématique → Claude")
    task = router.classify_task("Analyse la géométrie du spectre RSA")
    print(f"Task type: {task.value}")
    decision = router.decide_model(task)
    print(f"Selected: {decision.selected_model}")
    
    # Test 2: Tâche web (OpenAI)
    print("\n[TEST 2] Requête web → OpenAI")
    task = router.classify_task("Crée un script JavaScript optimisé")
    print(f"Task type: {task.value}")
    decision = router.decide_model(task)
    print(f"Selected: {decision.selected_model}")
    
    # Test 3: Stats
    print("\n[TEST 3] Stats routage")
    stats = router.get_routing_stats()
    print(f"Claude: {stats['claude_requests']} requêtes")
    print(f"OpenAI: {stats['openai_requests']} requêtes")
