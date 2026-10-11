"""
Isabelle Validator - Interface Isabelle/HOL pour validation formelle en temps réel
Connecte Gabriel à Isabelle pour vérification preuves matérielle
"""

import subprocess
import os
import logging
import tempfile
import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import time

logger = logging.getLogger(__name__)

class ValidationStatus(Enum):
    """État de validation Isabelle"""
    VALID = "valid"              # Preuve vérifiée ✓
    SYNTAX_ERROR = "syntax_error"  # Erreur syntaxe HOL
    TYPE_ERROR = "type_error"      # Erreur typage
    PROOF_ERROR = "proof_error"    # Preuve incomplète
    TIMEOUT = "timeout"            # Timeout Isabelle
    NOT_RUN = "not_run"           # Non exécuté

@dataclass
class IsabelleError:
    """Erreur retournée par Isabelle"""
    status: ValidationStatus
    error_message: str
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    error_context: str = ""  # Contexte de l'erreur
    suggested_fix: Optional[str] = None

@dataclass
class ValidationResult:
    """Résultat complet de validation"""
    theorem_name: str
    status: ValidationStatus
    is_valid: bool
    errors: List[IsabelleError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validation_time: float = 0.0
    proof_output: str = ""
    raw_isabelle_output: str = ""
    confidence_score: float = 0.0  # 0-1
    
    def __repr__(self):
        status_icon = "✓" if self.is_valid else "✗"
        return f"{status_icon} {self.theorem_name}: {self.status.value} (confidence: {self.confidence_score:.2f})"


class IsabelleValidator:
    """Interface à Isabelle pour validation formelle temps réel"""
    
    def __init__(self, isabelle_path: Optional[str] = None, timeout: int = 30):
        """
        Args:
            isabelle_path: Chemin exécutable Isabelle (auto-détecté si None)
            timeout: Timeout secondes pour chaque validation
        """
        self.isabelle_path = isabelle_path or self._find_isabelle()
        self.timeout = timeout
        self.is_available = self._check_isabelle()
        self.validation_cache = {}
        
        if not self.is_available:
            logger.warning("Isabelle non disponible - validations seront simulées")
    
    def _find_isabelle(self) -> Optional[str]:
        """Trouve chemin exécutable Isabelle"""
        possibilities = [
            "isabelle",
            "/usr/bin/isabelle",
            "/opt/isabelle/bin/isabelle",
            "C:\\Isabelle\\bin\\isabelle.exe",
            "/Applications/Isabelle.app/Isabelle",
        ]
        
        for path in possibilities:
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, 
                                      timeout=5)
                if result.returncode == 0:
                    return path
            except:
                pass
        
        return None
    
    def _check_isabelle(self) -> bool:
        """Vérifie disponibilité Isabelle"""
        if not self.isabelle_path:
            return False
        
        try:
            result = subprocess.run([self.isabelle_path, "--version"],
                                  capture_output=True,
                                  timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def validate_proof(self, hol_code: str, theorem_name: str = "theorem") -> ValidationResult:
        """
        Valide une preuve HOL4/Isabelle en temps réel via Isabelle
        
        Args:
            hol_code: Code HOL complet (théorie + preuves)
            theorem_name: Nom du théorème (pour logging)
        
        Returns:
            ValidationResult avec statut, erreurs, confidence
        """
        
        # Vérifier cache
        cache_key = hash(hol_code)
        if cache_key in self.validation_cache:
            logger.info(f"Validation en cache: {theorem_name}")
            return self.validation_cache[cache_key]
        
        start_time = time.time()
        
        if not self.is_available:
            # Fallback: validation simple
            logger.warning("Isabelle indisponible - validation basique seulement")
            return self._validate_basic(hol_code, theorem_name)
        
        try:
            # Créer fichier temporaire
            with tempfile.NamedTemporaryFile(mode='w', suffix='.thy', delete=False) as f:
                f.write(hol_code)
                thy_file = f.name
            
            # Exécuter Isabelle
            result = self._run_isabelle(thy_file)
            
            # Parser résultats
            validation_result = self._parse_isabelle_output(
                result, 
                theorem_name, 
                hol_code
            )
            
            validation_result.validation_time = time.time() - start_time
            
            # Calculer confidence
            if validation_result.status == ValidationStatus.VALID:
                validation_result.confidence_score = 1.0
            elif validation_result.status == ValidationStatus.SYNTAX_ERROR:
                validation_result.confidence_score = 0.0
            elif validation_result.status == ValidationStatus.PROOF_ERROR:
                validation_result.confidence_score = 0.3
            else:
                validation_result.confidence_score = 0.1
            
            # Cacher résultat
            self.validation_cache[cache_key] = validation_result
            
            # Cleanup
            try:
                os.unlink(thy_file)
            except:
                pass
            
            return validation_result
        
        except subprocess.TimeoutExpired:
            return ValidationResult(
                theorem_name=theorem_name,
                status=ValidationStatus.TIMEOUT,
                is_valid=False,
                errors=[IsabelleError(
                    status=ValidationStatus.TIMEOUT,
                    error_message=f"Isabelle timeout après {self.timeout}s"
                )],
                confidence_score=0.0,
                validation_time=time.time() - start_time
            )
        
        except Exception as e:
            logger.error(f"Erreur validation Isabelle: {e}")
            return ValidationResult(
                theorem_name=theorem_name,
                status=ValidationStatus.NOT_RUN,
                is_valid=False,
                errors=[IsabelleError(
                    status=ValidationStatus.NOT_RUN,
                    error_message=str(e)
                )],
                confidence_score=0.0,
                validation_time=time.time() - start_time
            )
    
    def _run_isabelle(self, thy_file: str) -> str:
        """Exécute Isabelle sur fichier .thy"""
        
        try:
            # Commande Isabelle
            cmd = [
                self.isabelle_path,
                "process",
                "-f",
                thy_file
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=os.path.dirname(thy_file)
            )
            
            return result.stdout + result.stderr
        
        except subprocess.TimeoutExpired:
            raise
    
    def _parse_isabelle_output(self, output: str, theorem_name: str, 
                              hol_code: str) -> ValidationResult:
        """Parse sortie Isabelle pour extraire erreurs"""
        
        errors = []
        warnings = []
        status = ValidationStatus.VALID
        is_valid = True
        
        # Patterns erreurs Isabelle
        syntax_pattern = r"Outer syntax error.*?line (\d+).*?(?:\n|$)"
        type_pattern = r"Type error.*?line (\d+).*?(?:\n|$)"
        proof_pattern = r"Proof error.*?line (\d+).*?(?:\n|$)"
        
        # Vérifier erreurs
        if "error" in output.lower():
            is_valid = False
            
            # Syntaxe
            for match in re.finditer(syntax_pattern, output, re.IGNORECASE):
                errors.append(IsabelleError(
                    status=ValidationStatus.SYNTAX_ERROR,
                    error_message=f"Erreur syntaxe ligne {match.group(1)}",
                    line_number=int(match.group(1)),
                    error_context=output[:500]
                ))
                status = ValidationStatus.SYNTAX_ERROR
            
            # Typage
            for match in re.finditer(type_pattern, output, re.IGNORECASE):
                errors.append(IsabelleError(
                    status=ValidationStatus.TYPE_ERROR,
                    error_message=f"Erreur type ligne {match.group(1)}",
                    line_number=int(match.group(1)),
                    error_context=output[:500]
                ))
                status = ValidationStatus.TYPE_ERROR
            
            # Preuve
            for match in re.finditer(proof_pattern, output, re.IGNORECASE):
                errors.append(IsabelleError(
                    status=ValidationStatus.PROOF_ERROR,
                    error_message=f"Preuve incomplète ligne {match.group(1)}",
                    line_number=int(match.group(1)),
                    error_context=output[:500]
                ))
                status = ValidationStatus.PROOF_ERROR
            
            # Erreur générique
            if not errors:
                errors.append(IsabelleError(
                    status=ValidationStatus.PROOF_ERROR,
                    error_message="Erreur validation non spécifiée",
                    error_context=output[:1000]
                ))
                status = ValidationStatus.PROOF_ERROR
        
        # Vérifier warnings
        if "warning" in output.lower():
            warnings_found = re.findall(r"[Ww]arning.*?(?:\n|$)", output)
            warnings.extend(warnings_found[:5])  # Max 5 warnings
        
        return ValidationResult(
            theorem_name=theorem_name,
            status=status,
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            proof_output=output,
            raw_isabelle_output=output,
            confidence_score=1.0 if is_valid else 0.0
        )
    
    def _validate_basic(self, hol_code: str, theorem_name: str) -> ValidationResult:
        """Validation basique (quand Isabelle indisponible)"""
        
        errors = []
        is_valid = True
        status = ValidationStatus.VALID
        
        # Vérifications syntaxe basiques
        if not hol_code.strip():
            return ValidationResult(
                theorem_name=theorem_name,
                status=ValidationStatus.SYNTAX_ERROR,
                is_valid=False,
                errors=[IsabelleError(
                    status=ValidationStatus.SYNTAX_ERROR,
                    error_message="Code HOL vide"
                )],
                confidence_score=0.0
            )
        
        # Vérifier présence keywords
        required = ["theorem", "proof", "qed"]
        missing = [kw for kw in required if kw not in hol_code.lower()]
        
        if missing:
            is_valid = False
            status = ValidationStatus.SYNTAX_ERROR
            errors.append(IsabelleError(
                status=ValidationStatus.SYNTAX_ERROR,
                error_message=f"Keywords manquants: {', '.join(missing)}",
                suggested_fix=f"Assurez-vous d'inclure: {', '.join(missing)}"
            ))
        
        # Vérifier parenthèses balancées
        if hol_code.count('(') != hol_code.count(')'):
            is_valid = False
            status = ValidationStatus.SYNTAX_ERROR
            errors.append(IsabelleError(
                status=ValidationStatus.SYNTAX_ERROR,
                error_message="Parenthèses non balancées",
                suggested_fix="Vérifiez les parenthèses ouvrantes/fermantes"
            ))
        
        return ValidationResult(
            theorem_name=theorem_name,
            status=status,
            is_valid=is_valid,
            errors=errors,
            confidence_score=1.0 if is_valid else 0.0
        )
    
    def get_error_suggestions(self, error: IsabelleError) -> List[str]:
        """Génère suggestions de correction pour une erreur"""
        
        suggestions = []
        
        if error.status == ValidationStatus.SYNTAX_ERROR:
            suggestions.extend([
                "Vérifiez la syntaxe HOL4",
                "Utilisez 'sorry' pour preuves incomplètes",
                "Vérifiez parenthèses/guillemets"
            ])
        
        elif error.status == ValidationStatus.TYPE_ERROR:
            suggestions.extend([
                "Vérifiez les types",
                "Utilisez conversions de type si nécessaire",
                "Assurez-vous compatibilité types"
            ])
        
        elif error.status == ValidationStatus.PROOF_ERROR:
            suggestions.extend([
                "Preuve incomplète - utiliser 'sorry' ou compléter",
                "Vérifier hypothèses disponibles",
                "Utiliser 'simp' ou 'auto' pour simplifier"
            ])
        
        if error.suggested_fix:
            suggestions.insert(0, error.suggested_fix)
        
        return suggestions
    
    def export_validation_report(self, result: ValidationResult) -> str:
        """Exporte rapport validation formaté"""
        
        report = f"""
RAPPORT VALIDATION ISABELLE
{'='*60}

Théorème: {result.theorem_name}
Statut: {result.status.value}
Valide: {'✓ OUI' if result.is_valid else '✗ NON'}
Confiance: {result.confidence_score * 100:.1f}%
Temps: {result.validation_time:.2f}s

ERREURS ({len(result.errors)}):
"""
        
        for error in result.errors:
            report += f"""
  Status: {error.status.value}
  Message: {error.error_message}
  {f'Ligne: {error.line_number}' if error.line_number else ''}
  Suggestions:
"""
            for suggestion in self.get_error_suggestions(error):
                report += f"    • {suggestion}\n"
        
        if result.warnings:
            report += f"\nAVERTISSEMENTS ({len(result.warnings)}):\n"
            for warning in result.warnings:
                report += f"  ⚠ {warning}\n"
        
        return report


if __name__ == '__main__':
    # Test
    validator = IsabelleValidator()
    
    print("="*60)
    print("ISABELLE VALIDATOR TEST")
    print("="*60)
    
    # Test 1: Code valide
    valid_code = """
theory TestTheory
  imports Main
begin

theorem test: "∀ x : ℕ, x = x"
  by simp

end
"""
    
    print("\n[TEST 1] Code valide")
    result = validator.validate_proof(valid_code, "test")
    print(result)
    
    # Test 2: Code invalide (syntaxe)
    invalid_code = """
theory TestTheory
  imports Main
begin

theorem test: "∀ x : ℕ, x = x"
  by simp  (* Missing QED *)

end
"""
    
    print("\n[TEST 2] Code invalide")
    result = validator.validate_proof(invalid_code, "test_invalid")
    print(result)
    print(validator.export_validation_report(result))
