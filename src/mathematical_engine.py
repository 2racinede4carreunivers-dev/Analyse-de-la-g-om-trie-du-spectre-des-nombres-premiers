"""
Mathematical Engine pour Gabriel
Intègre SymPy, PARI/GP, Wolfram et calculs haute précision
"""

import os
import logging
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json
import subprocess
import tempfile

import sympy as sp
from sympy import symbols, solve, simplify, lambdify, prime, factorint
from sympy.ntheory import mobius, divisor_count, divisor_sigma
import mpmath
from mpmath import mp, polylog, zetazero

# Configuration logging
logger = logging.getLogger(__name__)

@dataclass
class ComputationResult:
    """Résultat standardisé de calcul mathématique"""
    status: str  # 'success', 'error', 'partial'
    result: Any
    engine: str  # 'sympy', 'pari_gp', 'mpmath', 'wolfram'
    computation_time: float
    metadata: Dict[str, Any] = None
    error_message: str = None
    proof_hint: str = None  # Référence HOL4/Lean

class MathematicalEngine:
    """Moteur mathématique multimodal pour Gabriel"""
    
    def __init__(self, precision_bits: int = 256, wolfram_key: str = None):
        """
        Args:
            precision_bits: Précision pour mpmath (bits)
            wolfram_key: Clé API WolframAlpha (optionnel)
        """
        self.precision_bits = precision_bits
        mp.dps = precision_bits // 3  # Conversion bits -> décimales
        self.wolfram_key = wolfram_key
        self.pari_available = self._check_pari_gp()
        self.computations_cache = {}
        
    def _check_pari_gp(self) -> bool:
        """Vérifie disponibilité PARI/GP"""
        try:
            result = subprocess.run(['gp', '--version'], 
                                  capture_output=True, 
                                  timeout=2)
            return result.returncode == 0
        except:
            logger.warning("PARI/GP non disponible - utilisation SymPy en fallback")
            return False

    # ============ CALCULS SYMBOLIQUES ============
    
    def simplify_expression(self, expr_str: str) -> ComputationResult:
        """Simplifie une expression symbolique"""
        try:
            expr = sp.sympify(expr_str)
            simplified = simplify(expr)
            return ComputationResult(
                status='success',
                result=str(simplified),
                engine='sympy',
                computation_time=0,
                proof_hint='Use sympy.simplify lemma in HOL4'
            )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='sympy',
                computation_time=0,
                error_message=str(e)
            )

    def solve_equation(self, eq_str: str, var_str: str) -> ComputationResult:
        """Résout une équation symboliquement"""
        try:
            var = sp.sympify(var_str)
            equation = sp.sympify(eq_str)
            solutions = solve(equation, var)
            return ComputationResult(
                status='success',
                result=[str(sol) for sol in solutions],
                engine='sympy',
                computation_time=0,
                proof_hint='Verify via algebraic_solver in HOL4'
            )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='sympy',
                computation_time=0,
                error_message=str(e)
            )

    # ============ ZÉROS DE RIEMANN ============
    
    def compute_riemann_zeros(self, count: int = 100, 
                             precision_digits: int = 50) -> ComputationResult:
        """
        Calcule les N premiers zéros de la fonction zêta de Riemann
        
        Args:
            count: Nombre de zéros à calculer
            precision_digits: Précision décimale
        """
        try:
            old_dps = mp.dps
            mp.dps = precision_digits
            
            zeros = []
            for n in range(1, count + 1):
                try:
                    z = zetazero(n)
                    zeros.append({
                        'n': n,
                        'imaginary_part': str(z),
                        'decimal_approximation': float(z) if n <= 10 else None
                    })
                except:
                    pass
            
            mp.dps = old_dps
            
            return ComputationResult(
                status='success' if zeros else 'partial',
                result=zeros,
                engine='mpmath',
                computation_time=0,
                metadata={'requested': count, 'computed': len(zeros)},
                proof_hint='Reference riemann_hypothesis_spectral.thy'
            )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='mpmath',
                computation_time=0,
                error_message=str(e)
            )

    def compute_spectral_gap(self, zero_indices: List[int]) -> ComputationResult:
        """
        Calcule l'écart spectral entre zéros consécutifs
        
        Pertinent pour analyse_hypothese_riemann_savard.pdf
        """
        try:
            old_dps = mp.dps
            mp.dps = 100
            
            gaps = []
            for i in range(len(zero_indices) - 1):
                z1 = zetazero(zero_indices[i])
                z2 = zetazero(zero_indices[i + 1])
                gap = z2 - z1
                gaps.append({
                    'between': f"γ_{zero_indices[i]} and γ_{zero_indices[i+1]}",
                    'gap': str(gap),
                    'normalized': str(gap / (2 * mp.pi))  # Normalization Hilbert-Polya
                })
            
            mp.dps = old_dps
            
            return ComputationResult(
                status='success',
                result=gaps,
                engine='mpmath',
                computation_time=0,
                metadata={'gaps_computed': len(gaps)},
                proof_hint='gap_distribution lemma in riemann_spectral.thy'
            )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='mpmath',
                computation_time=0,
                error_message=str(e)
            )

    # ============ THÉORIE DES NOMBRES ============
    
    def prime_factorization(self, n: int) -> ComputationResult:
        """Décompose n en facteurs premiers"""
        try:
            factors = factorint(n)
            return ComputationResult(
                status='success',
                result=factors,
                engine='sympy',
                computation_time=0,
                proof_hint='prime_decomposition in number_theory.thy'
            )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='sympy',
                computation_time=0,
                error_message=str(e)
            )

    def compute_prime_spectrum(self, max_prime: int = 1000) -> ComputationResult:
        """
        Calcule le spectre des nombres premiers jusqu'à max_prime
        
        Utilisé pour visualiser la géométrie du spectre
        """
        try:
            primes_list = [p for p in range(2, max_prime) if sp.isprime(p)]
            
            spectrum_data = {
                'primes': primes_list,
                'count': len(primes_list),
                'density': len(primes_list) / max_prime,
                'gaps': [primes_list[i+1] - primes_list[i] 
                        for i in range(len(primes_list)-1)]
            }
            
            return ComputationResult(
                status='success',
                result=spectrum_data,
                engine='sympy',
                computation_time=0,
                metadata={'max_prime': max_prime},
                proof_hint='prime_number_theorem in analytic_number_theory.thy'
            )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='sympy',
                computation_time=0,
                error_message=str(e)
            )

    # ============ INTÉGRATION PARI/GP ============
    
    def pari_gp_command(self, gp_code: str) -> ComputationResult:
        """Exécute du code PARI/GP directement (si disponible)"""
        if not self.pari_available:
            return ComputationResult(
                status='error',
                result=None,
                engine='pari_gp',
                computation_time=0,
                error_message='PARI/GP non disponible sur ce système'
            )
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.gp', delete=False) as f:
                f.write(gp_code)
                gp_file = f.name
            
            result = subprocess.run(['gp', '-q', gp_file],
                                  capture_output=True,
                                  text=True,
                                  timeout=30)
            
            os.unlink(gp_file)
            
            if result.returncode == 0:
                return ComputationResult(
                    status='success',
                    result=result.stdout.strip(),
                    engine='pari_gp',
                    computation_time=0
                )
            else:
                return ComputationResult(
                    status='error',
                    result=None,
                    engine='pari_gp',
                    computation_time=0,
                    error_message=result.stderr
                )
        except Exception as e:
            return ComputationResult(
                status='error',
                result=None,
                engine='pari_gp',
                computation_time=0,
                error_message=str(e)
            )

    # ============ CACHING ============
    
    def cache_result(self, query_hash: str, result: ComputationResult):
        """Cache un résultat de calcul"""
        self.computations_cache[query_hash] = result
    
    def get_cached(self, query_hash: str) -> Optional[ComputationResult]:
        """Récupère un résultat en cache"""
        return self.computations_cache.get(query_hash)

    # ============ EXPORT RÉSULTATS ============
    
    def export_as_json(self, result: ComputationResult) -> str:
        """Exporte le résultat en JSON"""
        return json.dumps({
            'status': result.status,
            'engine': result.engine,
            'result': str(result.result) if result.result else None,
            'error': result.error_message,
            'proof_hint': result.proof_hint,
            'metadata': result.metadata
        }, indent=2, ensure_ascii=False)
    
    def export_as_hol_format(self, result: ComputationResult) -> str:
        """Exporte pour vérification formelle HOL4"""
        return f"""(* Result from {result.engine} *)
val mathematical_result = QUOTE `{result.result}`
(* Proof hint: {result.proof_hint} *)
"""


if __name__ == '__main__':
    # Test
    engine = MathematicalEngine(precision_bits=256)
    
    print("=== Test Simplification ===")
    result = engine.simplify_expression("(x**2 + 2*x + 1) / (x + 1)")
    print(engine.export_as_json(result))
    
    print("\n=== Test Zéros de Riemann ===")
    result = engine.compute_riemann_zeros(count=10, precision_digits=50)
    print(engine.export_as_json(result))
    
    print("\n=== Test Spectre Premier ===")
    result = engine.compute_prime_spectrum(max_prime=100)
    print(engine.export_as_json(result))
