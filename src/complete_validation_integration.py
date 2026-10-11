"""
Gabriel Complete Validation Integration
========================================

Intègre la validation paramétrique avec l'analyse d'image complète
Permet de valider les figures détectées contre des critères et données théoriques
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import json

try:
    from complete_vision_system import (
        get_complete_vision_system,
        CompleteAnalysisResult,
    )
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False

try:
    from parametric_validation_module import (
        get_parametric_validator,
        ParametricValidator,
    )
    VALIDATION_AVAILABLE = True
except ImportError:
    VALIDATION_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class CompleteValidationResult:
    """Résultat complet d'une validation avec analyse"""
    success: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    image_path: Optional[str] = None
    
    # Analyse d'image
    image_analysis: Optional[CompleteAnalysisResult] = None
    
    # Validation paramétrique
    validation_results: Dict[str, Any] = field(default_factory=dict)
    validation_criteria: List[str] = field(default_factory=list)
    theoretical_data: Dict[str, Any] = field(default_factory=dict)
    
    # Figure détectée
    figure_type: str = ""
    figure_points: List[Tuple[float, float]] = field(default_factory=list)
    
    # Résultats
    is_valid: bool = False
    confidence: float = 0.0
    
    # Rapports
    analysis_report: str = ""
    validation_report: str = ""
    combined_report: str = ""
    
    # Erreurs
    error_message: Optional[str] = None


class CompleteValidationSystem:
    """Système complet de validation paramétrique"""
    
    def __init__(self):
        """Initialise le système de validation complet"""
        if VISION_AVAILABLE:
            self.vision_system = get_complete_vision_system()
        else:
            self.vision_system = None
        
        if VALIDATION_AVAILABLE:
            self.validator = get_parametric_validator()
        else:
            self.validator = None
        
        logger.info("CompleteValidationSystem initialisé")
        logger.info(f"  - Vision: {'✓' if VISION_AVAILABLE else '✗'}")
        logger.info(f"  - Validation: {'✓' if VALIDATION_AVAILABLE else '✗'}")
    
    def validate_image_complete(self,
                               image_path: str,
                               criteria: str | List[str],
                               theoretical_data: Optional[Dict] = None,
                               extract_points: bool = True) -> CompleteValidationResult:
        """
        Valide une image complètement: analyse + validation paramétrique
        
        Args:
            image_path: Chemin/URL de l'image
            criteria: Critères en langage naturel ou liste
            theoretical_data: Données théoriques pour comparaison
            extract_points: Extraire automatiquement les points de l'image
        
        Returns:
            CompleteValidationResult
        """
        import time
        start_time = time.time()
        
        result = CompleteValidationResult(
            success=False,
            image_path=image_path,
        )
        
        try:
            logger.info(f"Validation complète: {image_path}")
            logger.info(f"Critères: {criteria}")
            
            # ÉTAPE 1: Analyser l'image
            if self.vision_system and extract_points:
                logger.debug("Étape 1: Analyse d'image...")
                result.image_analysis = self.vision_system.analyze_image_complete(
                    image_path,
                    generate_code=False
                )
                
                if not result.image_analysis.success:
                    result.error_message = "Analyse d'image échouée"
                    return result
                
                result.analysis_report = result.image_analysis.full_report
                
                # Extraire les points
                coords = result.image_analysis.coordinate
                if coords and 'shapes' in coords:
                    for shape in coords['shapes']:
                        if 'points' in shape:
                            result.figure_points = [
                                (p['x'], p['y']) for p in shape['points']
                            ]
                            result.figure_type = shape.get('type', 'Unknown')
                            break
            
            # ÉTAPE 2: Si pas de points extraits, utiliser les données fournies
            if not result.figure_points and theoretical_data and 'points' in theoretical_data:
                result.figure_points = theoretical_data['points']
                logger.debug(f"Utilisé points théoriques: {len(result.figure_points)}")
            
            if not result.figure_points:
                result.error_message = "Aucun point détecté ou fourni"
                return result
            
            # ÉTAPE 3: Validation paramétrique
            if self.validator:
                logger.debug("Étape 2: Validation paramétrique...")
                
                validation_data = self.validator.validate_image_with_criteria(
                    image_path,
                    result.figure_points,
                    criteria,
                    theoretical_data
                )
                
                result.validation_results = validation_data
                result.validation_criteria = validation_data.get('criteria_checked', [])
                result.is_valid = validation_data.get('overall_valid', False)
                
                # Calculer la confiance
                validations = validation_data.get('validations', [])
                if validations:
                    valid_count = sum(1 for v in validations if v.valid)
                    result.confidence = valid_count / len(validations)
                
                result.validation_report = self.validator.generate_validation_report(validation_data)
            
            # ÉTAPE 4: Générer le rapport combiné
            result.combined_report = self._generate_combined_report(result)
            
            result.success = True
            logger.info(f"Validation complète réussie - Valide: {result.is_valid}")
        
        except Exception as e:
            logger.error(f"Erreur validation: {e}")
            result.error_message = str(e)
        
        return result
    
    def _generate_combined_report(self, result: CompleteValidationResult) -> str:
        """Génère un rapport combiné"""
        report = f"""
╭════════════════════════════════════════════════════════════════╮
│    RAPPORT DE VALIDATION COMPLET - GABRIEL SYSTEM             │
╰════════════════════════════════════════════════════════════════╯

📁 IMAGE ANALYSÉE
   Chemin: {result.image_path}

📊 ANALYSE D'IMAGE
   Succès: {'✓' if result.image_analysis and result.image_analysis.success else '✗'}
   Figure détectée: {result.figure_type}
   Points détectés: {len(result.figure_points)}

🔍 VALIDATION PARAMÉTRIQUE
   Critères vérifiés: {', '.join(result.validation_criteria)}
   Figure valide: {'✓ OUI' if result.is_valid else '✗ NON'}
   Confiance: {result.confidence:.1%}

"""
        
        if result.image_analysis:
            report += f"""📈 PROPRIÉTÉS GÉOMÉTRIQUES
   Détails:
"""
            for key, value in result.image_analysis.coordinate.get('shapes', [{}])[0].items():
                if isinstance(value, (int, float)):
                    report += f"      {key}: {value:.2f}\n"
        
        report += f"""
✅ RÉSULTAT FINAL
   Validation: {'✓ PASSÉE' if result.is_valid else '✗ ÉCHOUÉE'}
   Confiance: {result.confidence:.1%}
"""
        
        if result.error_message:
            report += f"\n⚠️  ERREUR: {result.error_message}\n"
        
        return report
    
    def validate_with_natural_language(self,
                                       image_path: str,
                                       natural_language_request: str,
                                       theoretical_data: Optional[Dict] = None) -> CompleteValidationResult:
        """
        Valide une image avec une demande en langage naturel
        
        Exemples:
        - "C:/schema.png a-t-elle des rayons?"
        - "Ce triangle est-il équilatéral?"
        - "La figure a des rayons uniformes?"
        
        Args:
            image_path: Chemin de l'image
            natural_language_request: Demande en langage naturel
            theoretical_data: Données théoriques optionnelles
        
        Returns:
            CompleteValidationResult
        """
        logger.info(f"Validation langage naturel: {natural_language_request}")
        
        # Parser la requête en langage naturel
        request_lower = natural_language_request.lower()
        
        # Extraire les critères
        criteria = []
        
        if 'rayon' in request_lower:
            criteria.append('rayons')
        if 'équilatéral' in request_lower or 'équilatérale' in request_lower:
            criteria.append('équilatéral')
        if 'rectangle' in request_lower or 'carré' in request_lower:
            criteria.append('rectangle')
        if 'cercle' in request_lower:
            criteria.append('cercle')
        if 'symétri' in request_lower:
            criteria.append('symétrie')
        if 'régulier' in request_lower or 'régulière' in request_lower:
            criteria.append('régulier')
        if 'diagonal' in request_lower:
            criteria.append('diagonales')
        if 'distance' in request_lower or 'éloignement' in request_lower:
            criteria.append('distance')
        if 'angle' in request_lower:
            criteria.append('angle')
        
        # Si aucun critère détecté, utiliser la validation générique
        if not criteria:
            criteria = ['rayons', 'régulier']  # Par défaut
        
        logger.info(f"Critères détectés: {criteria}")
        
        # Valider
        return self.validate_image_complete(
            image_path,
            criteria,
            theoretical_data
        )
    
    def create_theoretical_dataset(self, **kwargs) -> Dict[str, Any]:
        """
        Crée un dataset théorique pour comparaison
        
        Examples:
        - Cercle: create_theoretical_dataset(
            figure='circle', radius=100, center=(200, 200)
          )
        - Triangle équilatéral: create_theoretical_dataset(
            figure='triangle', side_length=100
          )
        - Rectangle: create_theoretical_dataset(
            figure='rectangle', width=100, height=150
          )
        """
        figure_type = kwargs.get('figure', 'unknown')
        
        theoretical_data = {
            'figure_type': figure_type,
        }
        
        if figure_type == 'circle':
            radius = kwargs.get('radius', 100)
            center = kwargs.get('center', (0, 0))
            
            # Générer des points sur le cercle
            import math
            n_points = 8
            points = []
            for i in range(n_points):
                angle = 2 * math.pi * i / n_points
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append((x, y))
            
            theoretical_data['points'] = points
            theoretical_data['radius'] = radius
            theoretical_data['expected_distances'] = {
                f'P0_P{i}': radius * 2 * math.sin(i * math.pi / n_points)
                for i in range(1, n_points)
            }
        
        elif figure_type == 'triangle':
            side_length = kwargs.get('side_length', 100)
            height = side_length * (3**0.5) / 2
            
            theoretical_data['points'] = [
                (0, 0),
                (side_length, 0),
                (side_length / 2, height)
            ]
            
            theoretical_data['expected_distances'] = {
                'P0_P1': side_length,
                'P0_P2': side_length,
                'P1_P2': side_length,
            }
            
            theoretical_data['expected_angles'] = {
                'angle_0': 60,
                'angle_1': 60,
                'angle_2': 60,
            }
        
        elif figure_type == 'rectangle':
            width = kwargs.get('width', 100)
            height = kwargs.get('height', 50)
            
            theoretical_data['points'] = [
                (0, 0),
                (width, 0),
                (width, height),
                (0, height)
            ]
            
            theoretical_data['expected_angles'] = {
                'angle_0': 90,
                'angle_1': 90,
                'angle_2': 90,
                'angle_3': 90,
            }
        
        return theoretical_data


# Singleton global
_complete_validation_system: Optional[CompleteValidationSystem] = None


def get_complete_validation_system() -> CompleteValidationSystem:
    """Obtient ou crée le système complet de validation"""
    global _complete_validation_system
    
    if _complete_validation_system is None:
        _complete_validation_system = CompleteValidationSystem()
    
    return _complete_validation_system


def validate_image_parametric(image_path: str,
                             criteria: str | List[str],
                             theoretical_data: Optional[Dict] = None) -> CompleteValidationResult:
    """Validation rapide d'une image"""
    system = get_complete_validation_system()
    return system.validate_image_complete(image_path, criteria, theoretical_data)


def validate_image_natural_language(image_path: str,
                                   request: str,
                                   theoretical_data: Optional[Dict] = None) -> CompleteValidationResult:
    """Validation en langage naturel"""
    system = get_complete_validation_system()
    return system.validate_with_natural_language(image_path, request, theoretical_data)


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Gabriel Complete Validation Integration - Prêt           ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    system = get_complete_validation_system()
    
    print("Système de validation complet initialisé!")
    print("\nUtilisation:")
    print("  validate_image_parametric(path, ['rayons', 'équilatéral'])")
    print("  validate_image_natural_language(path, 'a-t-elle des rayons?')")
