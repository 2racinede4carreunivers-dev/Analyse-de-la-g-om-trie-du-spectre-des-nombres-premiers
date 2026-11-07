#!/usr/bin/env python3
"""
Backend Multiloop Service - Orchestration complète Gabriel + Isabelle
Exécute en arrière-plan: génération → validation → correction
"""

import logging
import sys
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import json
import time

# Ajuster path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.multiloop_validation_engine import MultiloopValidationEngine, MultiloopResult
from src.isabelle_validator import IsabelleValidator
from src.hol_proof_corrector import HOLProofCorrector

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/multiloop_backend.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MultiloopBackendService:
    """Service backend pour exécution multiloop"""
    
    def __init__(self, max_iterations: int = 3, target_confidence: float = 0.8):
        self.engine = MultiloopValidationEngine(
            max_iterations=max_iterations,
            target_confidence=target_confidence
        )
        self.results_cache = {}
        self.is_running = False
    
    def start(self):
        """Démarre le service"""
        self.is_running = True
        logger.info("✓ Service multiloop backend démarré")
    
    def stop(self):
        """Arrête le service"""
        self.is_running = False
        logger.info("✓ Service multiloop backend arrêté")
    
    def process_proof_request(self, theorem_name: str, proof_code: str,
                            metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Traite requête preuve complète via multiloop
        
        Args:
            theorem_name: Nom du théorème
            proof_code: Code HOL initial
            metadata: Données additionnelles
        
        Returns:
            Résultat complet avec trajectoire validation
        """
        
        logger.info(f"[REQUEST] Nouveau théorème: {theorem_name}")
        
        # Exécuter multiloop
        result = self.engine.process_theorem(theorem_name, proof_code)
        
        # Enregistrer
        self.results_cache[theorem_name] = result
        
        # Formatter réponse
        response = {
            'theorem_name': theorem_name,
            'request_id': f"{theorem_name}_{int(time.time())}",
            'status': 'valid' if result.is_valid else 'invalid',
            'confidence': result.final_confidence,
            'iterations': result.total_iterations,
            'total_time': result.total_time,
            'proof': result.final_proof,
            'is_valid': result.is_valid,
            'report': self.engine.export_multiloop_report(result),
            'metadata': metadata or {}
        }
        
        # Logging
        if result.is_valid:
            logger.info(f"✓ {theorem_name} VALIDÉ (confiance: {result.final_confidence:.2f})")
        else:
            logger.warning(
                f"~ {theorem_name} non validé (confiance: {result.final_confidence:.2f})"
            )
        
        return response
    
    def batch_process(self, theorems: Dict[str, str]) -> Dict[str, Dict]:
        """
        Traite batch de théorèmes
        
        Args:
            theorems: Dict {theorem_name: proof_code}
        
        Returns:
            Dict {theorem_name: résultat}
        """
        
        logger.info(f"[BATCH] Traitement {len(theorems)} théorèmes")
        
        results = {}
        for theorem_name, proof_code in theorems.items():
            try:
                result = self.process_proof_request(theorem_name, proof_code)
                results[theorem_name] = result
            except Exception as e:
                logger.error(f"Erreur {theorem_name}: {e}")
                results[theorem_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results
    
    def export_results(self, output_file: str):
        """Exporte tous les résultats en JSON"""
        
        export_data = {}
        for theorem_name, result in self.results_cache.items():
            export_data[theorem_name] = {
                'is_valid': result.is_valid,
                'confidence': result.final_confidence,
                'iterations': result.total_iterations,
                'time': result.total_time
            }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"✓ Résultats exportés: {output_file}")


def main():
    """Point d'entrée principal"""
    
    print("="*70)
    print("GABRIEL MULTILOOP BACKEND SERVICE")
    print("="*70)
    
    # Initialiser service
    service = MultiloopBackendService(max_iterations=3, target_confidence=0.8)
    service.start()
    
    try:
        # Test 1: Théorème simple
        print("\n[TEST 1] Théorème simple avec preuve incomplète")
        print("-"*70)
        
        test_proof_1 = """
Theorem simple_arithmetic: "∀ x y : ℕ, x + y = y + x"
Proof
  intro x y
  sorry
"""
        
        result_1 = service.process_proof_request("simple_arithmetic", test_proof_1)
        print(f"Status: {result_1['status']}")
        print(f"Confiance: {result_1['confidence']:.2f}")
        print(f"Itérations: {result_1['iterations']}")
        
        # Test 2: Théorème Riemann
        print("\n[TEST 2] Théorème Riemann (complexe)")
        print("-"*70)
        
        test_proof_2 = """
Theorem riemann_zeros: "∃ ζ : ℕ → ℂ, ∀ n, 0 < Im(ζ n) ∧ Re(ζ n) = 1/2"
Proof
  sorry
"""
        
        result_2 = service.process_proof_request("riemann_zeros", test_proof_2)
        print(f"Status: {result_2['status']}")
        print(f"Confiance: {result_2['confidence']:.2f}")
        
        # Test 3: Batch processing
        print("\n[TEST 3] Batch processing")
        print("-"*70)
        
        batch_theorems = {
            "theorem_1": "Theorem t1: \"True\"\nProof\nsorry\nQED",
            "theorem_2": "Theorem t2: \"∀ x, x = x\"\nProof\nsorry\nQED"
        }
        
        batch_results = service.batch_process(batch_theorems)
        print(f"Théorèmes traités: {len(batch_results)}")
        for name, res in batch_results.items():
            print(f"  • {name}: {res.get('status', 'unknown')}")
        
        # Export
        print("\n[EXPORT] Résultats")
        print("-"*70)
        
        os.makedirs('data/multiloop_results', exist_ok=True)
        service.export_results('data/multiloop_results/latest.json')
        
    finally:
        service.stop()
    
    print("\n" + "="*70)
    print("✓ Service terminé")
    print("="*70)


if __name__ == '__main__':
    main()
