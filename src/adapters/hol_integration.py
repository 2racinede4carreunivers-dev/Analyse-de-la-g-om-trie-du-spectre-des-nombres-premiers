"""
Intégration du HOL Script Generator dans le Pipeline.

Cette classe améliore la génération HOL avec les formules correctes.
"""
from __future__ import annotations

import logging
from typing import Optional

from ..spectral.hol_script_generator import HOLScriptGenerator


logger = logging.getLogger(__name__)


class HOLIntegration:
    """Intègre la génération HOL dans le pipeline Gabriel."""
    
    def __init__(self):
        self.generator = HOLScriptGenerator()
        logger.info("✓ HOLIntegration initialized")
    
    def generate_for_reconstruction(self, n: int, prime_value: int) -> dict:
        """
        Génère un script HOL complet pour une reconstruction de premier.
        
        Args:
            n: Position/nombre de termes
            prime_value: La valeur du N-ième premier
        
        Returns:
            dict avec:
              - hol_script: script HOL complet
              - values: dict des valeurs calculées
              - validation: checks de validité
        """
        logger.info(f"Generating HOL for n={n}, prime={prime_value}")
        
        try:
            # Générer le script de base
            script = self.generator.generate_prime_verification(n, prime_value)
            
            # Générer avec fractions (plus rigoureux)
            script_rational, values = self.generator.generate_prime_verification_with_rationals(
                n, prime_value
            )
            
            # Validation interne
            sa = values["sa_float"]
            sb = values["sb_float"]
            digamma = values["digamma_float"]
            
            # Vérifier que digamma = SB - 64*p
            expected_digamma = sb - 64 * prime_value
            digamma_valid = abs(digamma - expected_digamma) < 1e-6
            
            logger.info(f"  SA({n}) = {sa}")
            logger.info(f"  SB({n}) = {sb}")
            logger.info(f"  digamma({n}, {prime_value}) = {digamma}")
            logger.info(f"  Digamma validation: {digamma_valid}")
            
            return {
                "hol_script": script,
                "hol_script_rational": script_rational,
                "values": values,
                "validation": {
                    "digamma_correct": digamma_valid,
                    "sa_float": sa,
                    "sb_float": sb,
                    "digamma_float": digamma,
                    "digamma_formula_check": f"{sb} - 64*{prime_value} = {digamma}",
                },
                "success": True,
            }
        except Exception as e:
            logger.error(f"Error generating HOL: {e}")
            return {
                "success": False,
                "error": str(e),
                "hol_script": None,
            }
    
    def format_hol_output(self, hol_data: dict) -> str:
        """
        Formate la sortie HOL pour présentation à l'utilisateur.
        """
        if not hol_data.get("success"):
            return f"❌ Erreur HOL: {hol_data.get('error', 'Unknown error')}"
        
        script = hol_data.get("hol_script", "")
        values = hol_data.get("values", {})
        validation = hol_data.get("validation", {})
        
        output = f"""
### HOL/Isabelle Script de Vérification

**Formules Spectrales Calculées:**
- SA({values.get('n')}) = {values.get('sa_float', 'N/A')}
- SB({values.get('n')}) = {values.get('sb_float', 'N/A')}
- digamma({values.get('n')}, {values.get('prime')}) = {values.get('digamma_float', 'N/A')}

**Vérification:**
- Formule digamma: SB(n) - 64×p = {validation.get('digamma_formula_check', 'N/A')}
- Validité: {'✅' if validation.get('digamma_correct') else '❌'}

**Script HOL Généré:**
```isabelle
{script}
```

**Alternative avec Fractions (Plus Rigoureux):**
```isabelle
{hol_data.get('hol_script_rational', '')}
```
"""
        return output
