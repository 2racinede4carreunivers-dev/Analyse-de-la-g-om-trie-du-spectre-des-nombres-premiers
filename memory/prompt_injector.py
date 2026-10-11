"""
Prompt Injector - Injecte axiomes théorie dans requêtes LLM
Intercepte appels Ollama/WolframAlpha/OpenAI avant envoi
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import sys
from pathlib import Path

# Importer manager axiomes
sys.path.insert(0, str(Path(__file__).parent.parent))
from memory.theory_axioms_manager import TheoryAxiomsManager

logger = logging.getLogger(__name__)

@dataclass
class PromptContext:
    """Contexte pour injection axiomes"""
    original_query: str
    query_type: str  # 'rsa_calculation', 'riemann_analysis', etc.
    include_axioms: bool = True
    include_directives: bool = True
    include_parameters: bool = True
    target_llm: str = "ollama"  # ollama, openai, wolfram

class PromptInjector:
    """Injecte axiomes théorie avant envoi requête LLM"""
    
    def __init__(self, memory_path: str = "memory"):
        self.manager = TheoryAxiomsManager(memory_path)
        self.injection_count = 0
        self.cache = {}
    
    def inject_axioms(self, query: str, query_type: str = "riemann_analysis") -> str:
        """
        Injecte axiomes avant requête
        
        Args:
            query: Requête originale utilisateur
            query_type: Type de requête
        
        Returns:
            Requête augmentée avec axiomes
        """
        
        # Vérifier cache
        cache_key = f"{query}_{query_type}"
        if cache_key in self.cache:
            logger.debug(f"Injection en cache: {query_type}")
            return self.cache[cache_key]
        
        # Créer contexte
        ctx = PromptContext(
            original_query=query,
            query_type=query_type
        )
        
        # Générer pre-prompt
        pre_prompt = self.manager.get_pre_prompt(query_type)
        
        # Augmenter requête
        augmented_query = f"""{pre_prompt}

REQUÊTE UTILISATEUR:
{'-'*60}
{query}

RÉPONDEZ EN RESPECTANT LES AXIOMES CI-DESSUS.
"""
        
        # Cacher
        self.cache[cache_key] = augmented_query
        self.injection_count += 1
        
        logger.info(f"✓ Axiomes injectés ({self.injection_count})")
        
        return augmented_query
    
    def detect_query_type(self, query: str) -> str:
        """
        Détecte automatiquement type requête
        
        Returns:
            'rsa_calculation', 'riemann_analysis', 'prime_spectrum', etc.
        """
        
        query_lower = query.lower()
        
        # Détection patterns
        if any(word in query_lower for word in ['rapport spectral', 'rsa', 'asymétrique']):
            return 'rsa_calculation'
        
        elif any(word in query_lower for word in ['riemann', 'zéro', 'zero', 'hypothèse']):
            return 'riemann_analysis'
        
        elif any(word in query_lower for word in ['premier', 'prime', 'spectre', 'spectrum']):
            return 'prime_spectrum'
        
        elif any(word in query_lower for word in ['sr2', '1.5', 'ratio corrigé']):
            return 'sr2_calculation'
        
        else:
            return 'default'
    
    def inject_for_ollama(self, query: str, query_type: Optional[str] = None) -> str:
        """Injecte axiomes pour Ollama"""
        
        if query_type is None:
            query_type = self.detect_query_type(query)
        
        augmented = self.inject_axioms(query, query_type)
        
        logger.info(f"[Ollama] Injection pour: {query_type}")
        return augmented
    
    def inject_for_wolfram(self, query: str, query_type: Optional[str] = None) -> str:
        """Injecte axiomes pour WolframAlpha"""
        
        if query_type is None:
            query_type = self.detect_query_type(query)
        
        # Format adapté Wolfram
        pre_prompt = self.manager.get_pre_prompt(query_type)
        
        # Wolfram préfère format compact
        compact_prompt = f"""
CONTEXTE: Théorie Savard "L'univers est au carré"
- Sr2 = 1.5 (constante)
- RSA (Rapport Spectral Asymétrique) utilisé
- Ordres multiples analysés
- Géométrie spectrale asymétrique

REQUÊTE: {query}

APPLIQUER AXIOMES SAVARD UNIQUEMENT, PAS THÉORIE CLASSIQUE.
"""
        
        logger.info(f"[Wolfram] Injection pour: {query_type}")
        return compact_prompt
    
    def inject_for_openai(self, query: str, query_type: Optional[str] = None) -> Dict[str, Any]:
        """Injecte axiomes pour OpenAI (format messages)"""
        
        if query_type is None:
            query_type = self.detect_query_type(query)
        
        pre_prompt = self.manager.get_pre_prompt(query_type)
        
        # Format OpenAI
        messages = [
            {
                "role": "system",
                "content": pre_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        logger.info(f"[OpenAI] Injection pour: {query_type}")
        return messages
    
    def validate_llm_response(self, response: str, query_type: str = "default") -> Dict[str, Any]:
        """
        Valide si réponse LLM respecte axiomes
        
        Returns:
            Résultat validation + suggestions
        """
        
        result = self.manager.validate_response(response, query_type)
        
        if not result['is_compliant']:
            logger.warning(f"Réponse non-conforme (score: {result['score']:.2f})")
            logger.warning(f"Violations: {result['violations']}")
        
        return result
    
    def rewrite_response(self, response: str, query_type: str = "default") -> str:
        """
        Ré-écrit réponse non-conforme pour respecter axiomes
        
        (Utilise patterns de réécriture)
        """
        
        validation = self.validate_llm_response(response, query_type)
        
        if validation['is_compliant']:
            return response  # Déjà conforme
        
        # Appliquer corrections
        corrected = response
        
        # Ajouter axiomes manquants
        for suggestion in validation['suggestions']:
            if "Sr2" in suggestion:
                corrected = f"(Avec Sr2 = 1.5 correction spectrale appliquée:) {corrected}"
            
            if "RSA" in suggestion:
                corrected = f"RSA = (Sum_A - Sum_B) / Sum_B → {corrected}"
        
        # Remplacer théorie classique
        replacements = {
            'prime number theorem': 'théorème Savard (spectral)',
            'distribution de Cramér': 'distribution spectrale asymétrique',
            'nombre d\'or': 'Sr2 = 1.5',
            'normal distribution': 'géométrie spectrale'
        }
        
        for old, new in replacements.items():
            corrected = corrected.replace(old, new)
        
        return corrected
    
    def export_injection_stats(self) -> Dict[str, Any]:
        """Exporte statistiques injections"""
        
        return {
            'total_injections': self.injection_count,
            'cache_size': len(self.cache),
            'axioms_loaded': len(self.manager.axioms),
            'directives_loaded': len(self.manager.directives),
            'parameters': self.manager.parameters
        }


def create_injector(memory_path: str = "memory") -> PromptInjector:
    """Factory pour créer injector"""
    return PromptInjector(memory_path)


if __name__ == '__main__':
    # Test
    injector = PromptInjector()
    
    print("="*70)
    print("PROMPT INJECTOR TEST")
    print("="*70)
    
    # Test 1: Détection query type
    print("\n[TEST 1] Détection query type")
    
    test_queries = [
        "Calcule le RSA pour blocs [2] et [3,5]",
        "Explique les zéros de Riemann",
        "Quel est le spectre premier jusqu'à 100?"
    ]
    
    for q in test_queries:
        query_type = injector.detect_query_type(q)
        print(f"  '{q[:40]}...' → {query_type}")
    
    # Test 2: Injection Ollama
    print("\n[TEST 2] Injection pour Ollama")
    
    query = "Calcule RSA([2], [3,5]) ordre 1"
    injected = injector.inject_for_ollama(query)
    print(f"  Query originale: {len(query)} chars")
    print(f"  Query injectée: {len(injected)} chars")
    print(f"  Début: {injected[:150]}...")
    
    # Test 3: Validation réponse
    print("\n[TEST 3] Validation réponse LLM")
    
    # Bonne réponse
    good = """
RSA = (Sum_A - Sum_B) / Sum_B
Ordre 1: RSA = -2.0 (divergent)
Sr2 = 1.5 correction appliquée
Convergence géométrique attendue
"""
    
    result = injector.validate_llm_response(good, "rsa_calculation")
    print(f"  Bonne réponse conforme: {result['is_compliant']} (score {result['score']:.2f})")
    
    # Mauvaise réponse
    bad = """
Selon Cramér, la distribution suit une loi normale
avec le nombre d'or φ = 1.618
"""
    
    result = injector.validate_llm_response(bad, "rsa_calculation")
    print(f"  Mauvaise réponse conforme: {result['is_compliant']} (score {result['score']:.2f})")
    if result['violations']:
        print(f"  Violations: {result['violations'][:1]}")
    
    # Test 4: Stats
    print("\n[TEST 4] Statistiques")
    stats = injector.export_injection_stats()
    for key, val in stats.items():
        print(f"  {key}: {val}")
