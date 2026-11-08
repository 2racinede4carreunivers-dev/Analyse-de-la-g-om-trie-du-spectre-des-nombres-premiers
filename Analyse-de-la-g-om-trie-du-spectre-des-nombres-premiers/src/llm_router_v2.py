"""
LLM Router v2 - Claude Prioritaire avec Système d'Effort Cognitif
- Ollama DÉSACTIVÉ (trop lent, fallback permanent)
- Claude PRIORITAIRE automatiquement
- OpenAI pour tâches simples + fallback
- Partage intelligent: 75% Claude / 25% OpenAI si effort mixte
"""

import logging
import os
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass
from enum import Enum
import time

import anthropic
import openai

logger = logging.getLogger(__name__)

class CognitiveEffort(Enum):
    """Niveaux d'effort cognitif requis"""
    LOW = "low"              # Facile (OpenAI)
    MEDIUM = "medium"        # Moyen (peut être soit)
    HIGH = "high"           # Difficile (Claude)
    VERY_HIGH = "very_high" # Très difficile (Claude ONLY)

class TaskType(Enum):
    """Types de tâches avec effort requis"""
    # Claude ONLY (Very High / High Effort)
    MATHEMATICAL_REASONING = ("mathematical_reasoning", CognitiveEffort.VERY_HIGH)
    CODE_VALIDATION = ("code_validation", CognitiveEffort.VERY_HIGH)
    HOL_PROOF_GENERATION = ("hol_proof_generation", CognitiveEffort.VERY_HIGH)
    LOGICAL_STRUCTURE = ("logical_structure", CognitiveEffort.VERY_HIGH)
    RIEMANN_ANALYSIS = ("riemann_analysis", CognitiveEffort.VERY_HIGH)
    FORMAL_VERIFICATION = ("formal_verification", CognitiveEffort.VERY_HIGH)
    SPECTRAL_ANALYSIS = ("spectral_analysis", CognitiveEffort.VERY_HIGH)
    
    # OpenAI (Low / Medium Effort)
    CONTENT_GENERATION = ("content_generation", CognitiveEffort.LOW)
    WEB_SCRIPTING = ("web_scripting", CognitiveEffort.LOW)
    QUICK_OPTIMIZATION = ("quick_optimization", CognitiveEffort.MEDIUM)
    TEXT_FLUENCY = ("text_fluency", CognitiveEffort.LOW)
    SIMPLE_EXPLANATION = ("simple_explanation", CognitiveEffort.LOW)
    
    # Mixte (peut être combiné)
    GENERAL = ("general", CognitiveEffort.MEDIUM)
    RESEARCH = ("research", CognitiveEffort.MEDIUM)
    
    @property
    def effort(self) -> CognitiveEffort:
        """Retourne effort cognitif requis"""
        return self.value[1]

@dataclass
class ModelConfig:
    """Configuration pour un modèle"""
    name: str
    api_key: str
    model_id: str
    max_tokens: int = 1500
    temperature: float = 0.7
    priority: int = 1
    rate_limit_rpm: int = 3500
    rate_limit_tpm: int = 90000
    monthly_token_budget: int = 500000

@dataclass
class RoutingDecision:
    """Décision de routage"""
    selected_model: str
    task_type: TaskType
    cognitive_effort: CognitiveEffort
    reason: str
    fallback_model: Optional[str] = None
    split_ratio: Optional[Dict[str, float]] = None  # Pour partage 75/25
    estimated_cost: Optional[float] = None

class LLMRouterV2:
    """Routeur v2: Claude prioritaire, effort cognitif, Ollama OFF"""
    
    def __init__(self):
        """Initialise routeur (Ollama DÉSACTIVÉ)"""
        self.claude_config = self._init_claude()
        self.openai_config = self._init_openai()
        
        # Vérifier que Claude existe
        if not self.claude_config:
            raise ValueError("❌ CLAUDE_API_KEY non trouvée dans .env - Gabriel ne peut pas fonctionner")
        
        self.claude_client = anthropic.Anthropic(api_key=self.claude_config.api_key)
        self.openai_client = None
        
        if self.openai_config:
            self.openai_client = openai.OpenAI(api_key=self.openai_config.api_key)
        
        # Historique requêtes
        self.request_history = []
        
        # Tracking rate limits
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
        
        logger.info("✅ LLM Router v2 Initialized")
        logger.info("   Claude: PRIORITAIRE")
        logger.info("   OpenAI: Fallback + tâches simples")
        logger.info("   Ollama: DÉSACTIVÉ")
    
    def _init_claude(self) -> Optional[ModelConfig]:
        """Initialise configuration Claude"""
        api_key = os.getenv('CLAUDE_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key:
            logger.error("❌ CLAUDE_API_KEY non trouvée")
            return None
        
        return ModelConfig(
            name="Claude-3.5-Sonnet",
            api_key=api_key,
            model_id=os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
            max_tokens=2000,  # Augmenté pour qualité
            temperature=0.7,
            priority=1,  # PRIORITAIRE
            rate_limit_rpm=3500,
            rate_limit_tpm=90000
        )
    
    def _init_openai(self) -> Optional[ModelConfig]:
        """Initialise configuration OpenAI"""
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            logger.warning("⚠️ OPENAI_API_KEY non trouvée - OpenAI désactivé")
            return None
        
        return ModelConfig(
            name="GPT-4o",
            api_key=api_key,
            model_id="gpt-4o",
            max_tokens=1500,
            temperature=0.7,
            priority=2,  # FALLBACK
            rate_limit_rpm=10000,
            rate_limit_tpm=2000000
        )
    
    def analyze_cognitive_effort(self, query: str) -> CognitiveEffort:
        """
        Analyse l'effort cognitif requis
        
        HEURISTIQUES:
        - Longue query + mots complexes = HIGH/VERY_HIGH
        - Query courte + mots simples = LOW
        """
        
        query_lower = query.lower()
        query_len = len(query)
        
        # Mots indicateurs effort HIGH
        high_effort_words = [
            'mathématique', 'riemann', 'zéro', 'spectre', 'rsa',
            'hol4', 'isabelle', 'proof', 'théorème', 'preuve',
            'convergence', 'géométrie', 'spectral', 'analyse',
            'formel', 'axiome', 'lemme', 'vérif', 'logique'
        ]
        
        # Mots indicateurs effort LOW
        low_effort_words = [
            'explication simple', 'résumé', 'traduit', 'génère texte',
            'description', 'exemple', 'article web', 'blague',
            'poème', 'chanson', 'histoire courte'
        ]
        
        high_count = sum(1 for w in high_effort_words if w in query_lower)
        low_count = sum(1 for w in low_effort_words if w in query_lower)
        
        # Scorer
        effort_score = high_count * 10 - low_count * 5 + (query_len / 100)
        
        if effort_score > 30:
            return CognitiveEffort.VERY_HIGH
        elif effort_score > 15:
            return CognitiveEffort.HIGH
        elif effort_score > 5:
            return CognitiveEffort.MEDIUM
        else:
            return CognitiveEffort.LOW
    
    def classify_task(self, query: str) -> TaskType:
        """Classe automatiquement la tâche"""
        
        query_lower = query.lower()
        
        # Détection patterns
        patterns = {
            TaskType.MATHEMATICAL_REASONING: ['mathématique', 'calcul', 'équation', 'théorème'],
            TaskType.RIEMANN_ANALYSIS: ['riemann', 'zéro', 'spectre', 'rsa', 'convergence'],
            TaskType.HOL_PROOF_GENERATION: ['hol4', 'isabelle', 'lean', 'proof', 'preuve'],
            TaskType.CODE_VALIDATION: ['code', 'syntax', 'erreur', 'debug', 'valide'],
            TaskType.LOGICAL_STRUCTURE: ['structure', 'logique', 'axiome', 'géométrie'],
            TaskType.FORMAL_VERIFICATION: ['formel', 'vérif', 'certification', 'rigoureux'],
            TaskType.SPECTRAL_ANALYSIS: ['spectral', 'eigenvalue', 'hermitien', 'opérateur'],
            TaskType.CONTENT_GENERATION: ['génère', 'écris', 'contenu', 'article'],
            TaskType.WEB_SCRIPTING: ['web', 'javascript', 'html', 'script'],
            TaskType.TEXT_FLUENCY: ['explication', 'explique', 'résumé', 'simple'],
        }
        
        for task_type, keywords in patterns.items():
            if any(kw in query_lower for kw in keywords):
                return task_type
        
        return TaskType.GENERAL
    
    def decide_model(self, task_type: TaskType) -> RoutingDecision:
        """
        Décide quel modèle utiliser basé sur effort cognitif
        
        LOGIQUE:
        - VERY_HIGH effort → Claude ONLY
        - HIGH effort → Claude ONLY
        - MEDIUM effort → Claude prioritaire, OpenAI fallback
        - LOW effort → OpenAI FIRST, Claude fallback
        """
        
        effort = task_type.effort
        
        # Mapper effort → modèle
        if effort == CognitiveEffort.VERY_HIGH or effort == CognitiveEffort.HIGH:
            # Claude ONLY
            selected = 'claude'
            reason = f"Effort cognitif {effort.value} = Claude requis"
            fallback = 'openai'
        
        elif effort == CognitiveEffort.MEDIUM:
            # Claude prioritaire
            selected = 'claude'
            reason = f"Effort {effort.value} = Claude prioritaire"
            fallback = 'openai'
        
        else:  # LOW
            # OpenAI prioritaire pour économiser Claude
            selected = 'openai'
            reason = f"Effort {effort.value} = OpenAI suffisant"
            fallback = 'claude'
        
        # Vérifier disponibilité
        if selected == 'claude' and not self.claude_client:
            selected = 'openai'
            reason = "Claude indisponible → OpenAI"
        
        elif selected == 'openai' and not self.openai_client:
            selected = 'claude'
            reason = "OpenAI indisponible → Claude"
        
        # Vérifier rate limits
        if self._is_rate_limited(selected):
            old_selected = selected
            selected = fallback
            reason = f"Rate limit {old_selected} → {fallback}"
        
        return RoutingDecision(
            selected_model=selected,
            task_type=task_type,
            cognitive_effort=effort,
            reason=reason,
            fallback_model=fallback
        )
    
    def decide_model_split(self, task_type: TaskType, query_length: int) -> RoutingDecision:
        """
        Décide si split 75% Claude / 25% OpenAI
        
        Utilisé quand effort est mixte (75% dur + 25% facile)
        """
        
        effort = task_type.effort
        
        if effort == CognitiveEffort.MEDIUM:
            # Analyser composition query
            # Si query contient 75% mots "durs" → split
            
            logger.info(f"[SPLIT] 75% Claude + 25% OpenAI pour {task_type.value}")
            
            return RoutingDecision(
                selected_model='split',
                task_type=task_type,
                cognitive_effort=effort,
                reason="Effort mixte = Partage 75% Claude / 25% OpenAI",
                fallback_model=None,
                split_ratio={'claude': 0.75, 'openai': 0.25}
            )
        
        # Sinon, décision standard
        return self.decide_model(task_type)
    
    def _is_rate_limited(self, model: str) -> bool:
        """Vérifie si modèle rate-limited"""
        
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
        
        if config and tracking['requests'] >= config.rate_limit_rpm * 0.9:
            return True
        
        if config and tracking['tokens'] >= config.rate_limit_tpm * 0.9:
            return True
        
        return False
    
    def query(self, prompt: str, task_type: Optional[TaskType] = None,
              system_prompt: Optional[str] = None,
              force_model: Optional[str] = None) -> Tuple[str, Dict[str, Any]]:
        """
        Route requête vers Claude ou OpenAI
        
        Args:
            prompt: Requête utilisateur
            task_type: Type de tâche (auto-classifié si None)
            system_prompt: System prompt personnalisé
            force_model: Force modèle ('claude' ou 'openai')
        
        Returns:
            (response_text, metadata)
        """
        
        # Classifier si nécessaire
        if task_type is None:
            task_type = self.classify_task(prompt)
        
        # Forcer modèle si demandé
        if force_model:
            decision = RoutingDecision(
                selected_model=force_model,
                task_type=task_type,
                cognitive_effort=task_type.effort,
                reason="Force model demandé",
                fallback_model='claude' if force_model == 'openai' else 'openai'
            )
        else:
            # Décider modèle
            decision = self.decide_model(task_type)
        
        logger.info(f"[{decision.selected_model.upper()}] {decision.reason}")
        
        try:
            if decision.selected_model == 'claude':
                response, metadata = self._query_claude(prompt, system_prompt)
            elif decision.selected_model == 'openai':
                response, metadata = self._query_openai(prompt, system_prompt)
            elif decision.selected_model == 'split':
                # Partage 75/25
                response, metadata = self._query_split(prompt, system_prompt, decision)
            else:
                raise ValueError(f"Modèle inconnu: {decision.selected_model}")
            
            # Enregistrer historique
            self.request_history.append({
                'task_type': task_type.value[0],
                'model': decision.selected_model,
                'effort': decision.cognitive_effort.value,
                'timestamp': time.time(),
                'tokens': metadata.get('tokens_used', 0)
            })
            
            metadata['routing'] = {
                'model': decision.selected_model,
                'effort': decision.cognitive_effort.value,
                'reason': decision.reason
            }
            
            return response, metadata
        
        except Exception as e:
            logger.error(f"Erreur {decision.selected_model}: {e}")
            
            # Essayer fallback
            if decision.fallback_model:
                logger.info(f"Basculement vers {decision.fallback_model}")
                return self.query(prompt, task_type, system_prompt, force_model=decision.fallback_model)
            
            raise
    
    def _query_claude(self, prompt: str, system_prompt: Optional[str] = None) -> Tuple[str, Dict]:
        """Requête Claude"""
        
        messages = [{"role": "user", "content": prompt}]
        
        response = self.claude_client.messages.create(
            model=self.claude_config.model_id,
            max_tokens=self.claude_config.max_tokens,
            system=system_prompt or "Tu es Claude, expert en mathématiques et programmation formelle.",
            messages=messages,
            temperature=self.claude_config.temperature
        )
        
        text = response.content[0].text
        tokens = response.usage.input_tokens + response.usage.output_tokens
        
        # Tracking
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
            raise ValueError("OpenAI non disponible")
        
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
        
        # Tracking
        self.rate_limit_tracking['openai']['requests'] += 1
        self.rate_limit_tracking['openai']['tokens'] += tokens
        
        return text, {
            'model': 'openai',
            'tokens_used': tokens,
            'input_tokens': response.usage.prompt_tokens,
            'output_tokens': response.usage.completion_tokens
        }
    
    def _query_split(self, prompt: str, system_prompt: Optional[str], 
                    decision: RoutingDecision) -> Tuple[str, Dict]:
        """
        Requête SPLIT: 75% Claude + 25% OpenAI
        
        Divise le travail intelligemment:
        - Claude: Raisonnement logique, mathématique (75%)
        - OpenAI: Simplifications, fluidité textuelle (25%)
        """
        
        logger.info("🔀 SPLIT MODE: 75% Claude + 25% OpenAI")
        
        # Étape 1: Claude traite 75% (le cœur)
        claude_response, claude_meta = self._query_claude(
            prompt,
            system_prompt or "Traite le cœur logique de cette requête (75%)"
        )
        
        # Étape 2: OpenAI affine/complète 25% (intégration)
        refinement_prompt = f"""
Tu as reçu cette réponse d'un expert (Claude):

{claude_response[:500]}...

Réalisez les tâches suivantes (25% d'effort):
1. Vérifier la fluidité du texte
2. Ajouter des explications simples si nécessaire
3. Formater pour meilleure lisibilité

Garder 75% de la réponse Claude intacte, affiner les 25% de présentation.
"""
        
        openai_response, openai_meta = self._query_openai(
            refinement_prompt,
            system_prompt or "Affine et complète la réponse d'un expert."
        )
        
        # Combiner réponses
        combined = f"""
{claude_response}

[Intégration OpenAI:]
{openai_response}
"""
        
        return combined, {
            'model': 'split',
            'tokens_used': claude_meta['tokens_used'] + openai_meta['tokens_used'],
            'claude_tokens': claude_meta['tokens_used'],
            'openai_tokens': openai_meta['tokens_used'],
            'split_ratio': decision.split_ratio
        }
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Retourne statistiques routage"""
        
        claude_count = sum(1 for r in self.request_history if r['model'] == 'claude')
        openai_count = sum(1 for r in self.request_history if r['model'] == 'openai')
        split_count = sum(1 for r in self.request_history if r['model'] == 'split')
        
        claude_tokens = sum(r['tokens'] for r in self.request_history if r['model'] == 'claude')
        openai_tokens = sum(r['tokens'] for r in self.request_history if r['model'] == 'openai')
        
        total = len(self.request_history)
        
        return {
            'summary': {
                'total_requests': total,
                'claude_requests': claude_count,
                'openai_requests': openai_count,
                'split_requests': split_count,
            },
            'percentages': {
                'claude_percent': (claude_count / total * 100) if total else 0,
                'openai_percent': (openai_count / total * 100) if total else 0,
                'split_percent': (split_count / total * 100) if total else 0,
            },
            'tokens': {
                'claude_total': claude_tokens,
                'openai_total': openai_tokens,
            },
            'rate_limits': self.rate_limit_tracking
        }


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "="*70)
    print("LLM ROUTER v2 - CLAUDE PRIORITAIRE + EFFORT COGNITIF")
    print("="*70)
    
    try:
        router = LLMRouterV2()
        
        # Test 1: Tâche TRÈS difficile → Claude
        print("\n[TEST 1] Tâche très difficile")
        task = router.classify_task("Génère une théorie Isabelle pour reconstruction des nombres premiers via RSA")
        effort = router.analyze_cognitive_effort("Génère une théorie Isabelle pour reconstruction des nombres premiers via RSA avec formules Savard")
        print(f"  Task: {task.value[0]}")
        print(f"  Effort: {effort.value}")
        decision = router.decide_model(task)
        print(f"  Selected: {decision.selected_model}")
        
        # Test 2: Tâche facile → OpenAI
        print("\n[TEST 2] Tâche simple")
        task = router.classify_task("Écris un poème court sur les nombres")
        effort = router.analyze_cognitive_effort("Écris un poème")
        print(f"  Task: {task.value[0]}")
        print(f"  Effort: {effort.value}")
        decision = router.decide_model(task)
        print(f"  Selected: {decision.selected_model}")
        
        # Test 3: Tâche mixte → Split
        print("\n[TEST 3] Tâche mixte (75/25)")
        task = router.classify_task("Analyse RSA et explique simplement")
        effort = router.analyze_cognitive_effort("Analyse la convergence RSA mathématiquement et explique simplement pour un enfant")
        print(f"  Task: {task.value[0]}")
        print(f"  Effort: {effort.value}")
        decision = router.decide_model_split(task, 50)
        print(f"  Selected: {decision.selected_model}")
        if decision.split_ratio:
            print(f"  Ratio: {decision.split_ratio}")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("\nVérifier .env:")
        print("  CLAUDE_API_KEY=sk-ant-...")
        print("  OPENAI_API_KEY=sk-... (optionnel)")
