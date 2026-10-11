"""
Gabriel Parametric Validation Module - Validation théorique avancée
====================================================================

Module de validation paramétrique permettant de:
  ✓ Valider figures selon critères précis en langage naturel
  ✓ Validation théorique (suites, formules mathématiques)
  ✓ Validation géométrique (distances, angles, ratios)
  ✓ Validation de propriétés (régularité, symétrie, etc.)
  ✓ Génération de rapports de validation
  ✓ Validation comparative (figure vs données théoriques)
  ✓ Detection d'éléments spécifiques (rayons, diagonales, etc.)

Auteur: Gabriel Multi-Loop Agent
Date: 2026
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any, Callable
from enum import Enum
import json
import re

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

logger = logging.getLogger(__name__)


# ============================================================================
# CRITÈRES ET RÈGLES DE VALIDATION
# ============================================================================

@dataclass
class ValidationCriterion:
    """Représente un critère de validation"""
    name: str  # 'rayons', 'distance_points', 'angle', etc.
    description: str
    type: str  # 'geometric', 'property', 'theoretical', 'comparative'
    expected_value: Optional[float] = None
    tolerance: float = 5.0  # Tolérance en % ou unités
    required: bool = True
    validation_func: Optional[Callable] = None
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationRule:
    """Ensemble de critères de validation"""
    name: str
    description: str
    criteria: List[ValidationCriterion] = field(default_factory=list)
    theoretical_data: Dict[str, Any] = field(default_factory=dict)
    natural_language: str = ""


@dataclass
class ValidationResult:
    """Résultat d'une validation"""
    valid: bool
    criterion_name: str
    actual_value: Optional[float] = None
    expected_value: Optional[float] = None
    tolerance: float = 5.0
    error_message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0  # 0-1
    
    def passes(self) -> bool:
        if self.actual_value is None:
            return False
        
        if self.expected_value is None:
            return True
        
        # Calcul d'erreur relative
        error = abs(self.actual_value - self.expected_value)
        if self.expected_value != 0:
            error_percent = (error / abs(self.expected_value)) * 100
        else:
            error_percent = error
        
        return error_percent <= self.tolerance


# ============================================================================
# ANALYSEUR GÉOMÉTRIQUE AVANCÉ
# ============================================================================

class AdvancedGeometricAnalyzer:
    """Analyseur géométrique avec calculs avancés"""
    
    def __init__(self, points: List[Tuple[float, float]]):
        """
        Initialise l'analyseur
        
        Args:
            points: Liste de tuples (x, y) représentant les points
        """
        self.points = [np.array(p) for p in points]
        self.n_points = len(self.points)
    
    def calculate_distances(self) -> Dict[str, float]:
        """Calcule les distances entre tous les points"""
        distances = {}
        for i in range(self.n_points):
            for j in range(i + 1, self.n_points):
                key = f"P{i}_P{j}"
                dist = np.linalg.norm(self.points[i] - self.points[j])
                distances[key] = dist
        return distances
    
    def calculate_angles(self) -> Dict[str, float]:
        """Calcule les angles entre les points"""
        angles = {}
        
        if self.n_points < 3:
            return angles
        
        for i in range(self.n_points):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % self.n_points]
            p3 = self.points[(i + 2) % self.n_points]
            
            # Vecteurs
            v1 = p2 - p1
            v2 = p3 - p2
            
            # Angle
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10)
            angle = math.degrees(math.acos(np.clip(cos_angle, -1, 1)))
            
            angles[f"angle_{i}"] = angle
        
        return angles
    
    def calculate_center(self) -> np.ndarray:
        """Calcule le centre de masse"""
        return np.mean(self.points, axis=0)
    
    def calculate_area(self) -> float:
        """Calcule l'aire (shoelace formula)"""
        if self.n_points < 3:
            return 0.0
        
        area = 0.0
        for i in range(self.n_points):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % self.n_points]
            area += x1 * y2 - x2 * y1
        
        return abs(area) / 2.0
    
    def calculate_perimeter(self) -> float:
        """Calcule le périmètre"""
        perimeter = 0.0
        for i in range(self.n_points):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % self.n_points]
            perimeter += np.linalg.norm(p2 - p1)
        return perimeter
    
    def is_regular_polygon(self, tolerance: float = 5.0) -> bool:
        """Vérifie si c'est un polygone régulier"""
        distances = self.calculate_distances()
        if not distances:
            return False
        
        avg_dist = np.mean(list(distances.values()))
        return all(abs(d - avg_dist) / avg_dist * 100 < tolerance 
                  for d in distances.values())
    
    def has_symmetry(self, axis: str = 'horizontal') -> bool:
        """Vérifie la symétrie"""
        if axis == 'horizontal':
            # Symétrie horizontale autour du centre Y
            center_y = self.calculate_center()[1]
            symmetric_pairs = []
            for p1 in self.points:
                # Chercher un point symétrique
                for p2 in self.points:
                    if abs((p1[1] + p2[1]) / 2 - center_y) < 1:
                        symmetric_pairs.append((p1, p2))
            return len(symmetric_pairs) >= self.n_points / 2
        
        elif axis == 'vertical':
            # Symétrie verticale autour du centre X
            center_x = self.calculate_center()[0]
            symmetric_pairs = []
            for p1 in self.points:
                for p2 in self.points:
                    if abs((p1[0] + p2[0]) / 2 - center_x) < 1:
                        symmetric_pairs.append((p1, p2))
            return len(symmetric_pairs) >= self.n_points / 2
        
        return False
    
    def detect_radii(self) -> List[Dict[str, Any]]:
        """Détecte les rayons (lignes du centre vers les points)"""
        center = self.calculate_center()
        radii = []
        
        for i, point in enumerate(self.points):
            radius = np.linalg.norm(point - center)
            radii.append({
                'point_index': i,
                'radius': radius,
                'from_center': tuple(center),
                'to_point': tuple(point),
            })
        
        return radii
    
    def detect_diagonals(self) -> List[Dict[str, Any]]:
        """Détecte les diagonales"""
        diagonals = []
        
        for i in range(self.n_points):
            for j in range(i + 2, self.n_points):
                # Éviter d'inclure les côtés adjacents
                if j - i == 1 or (i == 0 and j == self.n_points - 1):
                    continue
                
                p1 = self.points[i]
                p2 = self.points[j]
                length = np.linalg.norm(p2 - p1)
                
                diagonals.append({
                    'from': i,
                    'to': j,
                    'length': length,
                    'points': (tuple(p1), tuple(p2)),
                })
        
        return diagonals
    
    def check_collinearity(self, indices: List[int], tolerance: float = 1.0) -> bool:
        """Vérifie si des points sont collinéaires"""
        if len(indices) < 3:
            return True
        
        p1 = self.points[indices[0]]
        p2 = self.points[indices[1]]
        
        # Vecteur direction
        direction = p2 - p1
        direction = direction / (np.linalg.norm(direction) + 1e-10)
        
        # Vérifier les autres points
        for i in indices[2:]:
            p = self.points[i]
            v = p - p1
            # Distance perpendiculaire à la ligne
            perp_dist = abs(np.cross(direction, v / np.linalg.norm(v)))
            if perp_dist > tolerance:
                return False
        
        return True
    
    def calculate_ratio(self, length1_key: str, length2_key: str) -> float:
        """Calcule le ratio entre deux longueurs"""
        distances = self.calculate_distances()
        
        if length1_key not in distances or length2_key not in distances:
            return 0.0
        
        return distances[length1_key] / (distances[length2_key] + 1e-10)


# ============================================================================
# VALIDATEUR PARAMÉTRIQUE
# ============================================================================

class ParametricValidator:
    """Validateur paramétrique avec support langage naturel et théories"""
    
    def __init__(self):
        self.rules: Dict[str, ValidationRule] = {}
        self.theoretical_data: Dict[str, Dict] = {}
        self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialise les règles de validation prédéfinies"""
        
        # Règle: Triangle équilatéral
        self.rules['equilateral_triangle'] = ValidationRule(
            name='Équilatéral',
            description='Vérifie si tous les côtés sont égaux',
            criteria=[
                ValidationCriterion(
                    name='equal_sides',
                    description='Tous les côtés égaux',
                    type='geometric',
                    tolerance=5.0,
                ),
            ],
            natural_language='tous les côtés sont égaux, triangle régulier',
        )
        
        # Règle: Carré/Rectangle
        self.rules['rectangle'] = ValidationRule(
            name='Rectangle',
            description='Vérifie les propriétés d\'un rectangle',
            criteria=[
                ValidationCriterion(
                    name='right_angles',
                    description='4 angles droits',
                    type='geometric',
                    expected_value=90.0,
                    tolerance=5.0,
                ),
                ValidationCriterion(
                    name='equal_diagonals',
                    description='Diagonales égales',
                    type='geometric',
                    tolerance=5.0,
                ),
            ],
            natural_language='4 angles droits, côtés opposés égaux',
        )
        
        # Règle: Cercle
        self.rules['circle'] = ValidationRule(
            name='Cercle',
            description='Vérifie les propriétés d\'un cercle',
            criteria=[
                ValidationCriterion(
                    name='equal_radii',
                    description='Tous les rayons égaux',
                    type='geometric',
                    tolerance=5.0,
                ),
                ValidationCriterion(
                    name='center_exists',
                    description='Un centre identifiable',
                    type='property',
                ),
            ],
            natural_language='tous les points équidistants du centre',
        )
        
        # Règle: Rayons détectables
        self.rules['has_radii'] = ValidationRule(
            name='Présence de rayons',
            description='Détecte la présence de rayons depuis le centre',
            criteria=[
                ValidationCriterion(
                    name='radii_count',
                    description='Au moins N rayons détectés',
                    type='property',
                ),
                ValidationCriterion(
                    name='radii_uniform',
                    description='Rayons de longueur uniforme',
                    type='geometric',
                    tolerance=10.0,
                ),
            ],
            natural_language='a des rayons, lignes du centre vers la périphérie',
        )
        
        # Règle: Symétrie
        self.rules['symmetry'] = ValidationRule(
            name='Symétrie',
            description='Vérifie la symétrie de la figure',
            criteria=[
                ValidationCriterion(
                    name='symmetric',
                    description='Figure symétrique',
                    type='property',
                ),
            ],
            natural_language='figure symétrique, reflet autour d\'un axe',
        )
        
        # Règle: Régularité
        self.rules['regular_polygon'] = ValidationRule(
            name='Polygone régulier',
            description='Tous les côtés et angles égaux',
            criteria=[
                ValidationCriterion(
                    name='equal_sides',
                    description='Côtés égaux',
                    type='geometric',
                    tolerance=5.0,
                ),
                ValidationCriterion(
                    name='equal_angles',
                    description='Angles égaux',
                    type='geometric',
                    tolerance=5.0,
                ),
            ],
            natural_language='polygone régulier, tous les côtés et angles égaux',
        )
    
    def parse_natural_language_criteria(self, description: str) -> List[str]:
        """
        Parse une description en langage naturel pour extraire les critères
        
        Args:
            description: Description en langage naturel
        
        Returns:
            Liste des critères détectés
        """
        description_lower = description.lower()
        detected_criteria = []
        
        # Patterns pour détecter les critères
        patterns = {
            'rayons': ['rayon', 'rayons', 'du centre', 'lignes du centre'],
            'équilatéral': ['équilatéral', 'tous les côtés égaux', 'côtés égaux'],
            'rectangle': ['rectangle', '4 angles droits', 'angles droits'],
            'cercle': ['cercle', 'équidistants du centre', 'tous les points'],
            'symétrie': ['symétrique', 'symétrie', 'reflet'],
            'régulier': ['régulier', 'régulière', 'polygone régulier'],
            'diagonales': ['diagonales', 'diagonale'],
            'distance': ['distance', 'éloignement', 'écart'],
            'angle': ['angle', 'angles'],
        }
        
        for criterion, keywords in patterns.items():
            for keyword in keywords:
                if keyword in description_lower:
                    detected_criteria.append(criterion)
                    break
        
        return detected_criteria
    
    def validate_figure(self, 
                       points: List[Tuple[float, float]],
                       criteria: str | List[str],
                       theoretical_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Valide une figure selon les critères spécifiés
        
        Args:
            points: Points de la figure
            criteria: Critères en langage naturel ou liste de critères
            theoretical_data: Données théoriques pour comparaison
        
        Returns:
            Résultats de validation
        """
        analyzer = AdvancedGeometricAnalyzer(points)
        
        # Parser les critères
        if isinstance(criteria, str):
            criteria_list = self.parse_natural_language_criteria(criteria)
        else:
            criteria_list = criteria
        
        results = {
            'figure_name': self._identify_figure(points),
            'points_count': len(points),
            'criteria_checked': criteria_list,
            'validations': [],
            'overall_valid': True,
            'details': {},
        }
        
        # Calculer les propriétés
        distances = analyzer.calculate_distances()
        angles = analyzer.calculate_angles()
        center = analyzer.calculate_center()
        area = analyzer.calculate_area()
        perimeter = analyzer.calculate_perimeter()
        radii = analyzer.detect_radii()
        diagonals = analyzer.detect_diagonals()
        
        # Stocker les détails
        results['details'] = {
            'center': tuple(center),
            'area': area,
            'perimeter': perimeter,
            'radii_count': len(radii),
            'diagonals_count': len(diagonals),
            'average_radius': np.mean([r['radius'] for r in radii]) if radii else 0,
        }
        
        # Valider chaque critère
        for criterion in criteria_list:
            if criterion == 'rayons':
                validation = self._validate_radii(analyzer, radii, theoretical_data)
                results['validations'].append(validation)
            
            elif criterion == 'équilatéral':
                validation = self._validate_equilateral(analyzer, distances)
                results['validations'].append(validation)
            
            elif criterion == 'rectangle':
                validation = self._validate_rectangle(analyzer, angles, diagonals)
                results['validations'].append(validation)
            
            elif criterion == 'cercle':
                validation = self._validate_circle(analyzer, radii)
                results['validations'].append(validation)
            
            elif criterion == 'symétrie':
                validation = self._validate_symmetry(analyzer)
                results['validations'].append(validation)
            
            elif criterion == 'régulier':
                validation = self._validate_regular_polygon(analyzer, distances, angles)
                results['validations'].append(validation)
            
            elif criterion == 'diagonales':
                validation = self._validate_diagonals(diagonals)
                results['validations'].append(validation)
            
            elif criterion == 'distance':
                validation = self._validate_distances(distances, theoretical_data)
                results['validations'].append(validation)
            
            elif criterion == 'angle':
                validation = self._validate_angles(angles, theoretical_data)
                results['validations'].append(validation)
        
        # Déterminer la validité globale
        results['overall_valid'] = all(v.valid for v in results['validations'])
        
        return results
    
    def _identify_figure(self, points: List[Tuple[float, float]]) -> str:
        """Identifie le type de figure"""
        n = len(points)
        if n == 3:
            return "Triangle"
        elif n == 4:
            return "Quadrilatère"
        elif n == 5:
            return "Pentagone"
        elif n == 6:
            return "Hexagone"
        else:
            return f"Polygone à {n} côtés"
    
    def _validate_radii(self, analyzer: AdvancedGeometricAnalyzer, 
                       radii: List[Dict], theoretical_data: Optional[Dict]) -> ValidationResult:
        """Valide la présence et uniformité des rayons"""
        if not radii:
            return ValidationResult(
                valid=False,
                criterion_name='rayons',
                error_message='Aucun rayon détecté'
            )
        
        radius_values = [r['radius'] for r in radii]
        avg_radius = np.mean(radius_values)
        std_radius = np.std(radius_values)
        
        # Vérifier l'uniformité
        variation = (std_radius / (avg_radius + 1e-10)) * 100
        tolerance = 10.0  # 10% de tolérance
        
        valid = variation < tolerance
        
        return ValidationResult(
            valid=valid,
            criterion_name='rayons',
            actual_value=variation,
            expected_value=0.0,
            tolerance=tolerance,
            details={
                'count': len(radii),
                'average_radius': avg_radius,
                'std_deviation': std_radius,
                'variation_percent': variation,
            },
            confidence=1.0 if valid else 0.5,
        )
    
    def _validate_equilateral(self, analyzer: AdvancedGeometricAnalyzer,
                            distances: Dict[str, float]) -> ValidationResult:
        """Valide un triangle équilatéral"""
        if not distances:
            return ValidationResult(
                valid=False,
                criterion_name='équilatéral',
                error_message='Aucune distance calculée'
            )
        
        dist_values = list(distances.values())
        avg_dist = np.mean(dist_values)
        max_dist = max(dist_values)
        min_dist = min(dist_values)
        
        variation = ((max_dist - min_dist) / (avg_dist + 1e-10)) * 100
        tolerance = 5.0
        
        valid = variation < tolerance
        
        return ValidationResult(
            valid=valid,
            criterion_name='équilatéral',
            actual_value=variation,
            expected_value=0.0,
            tolerance=tolerance,
            details={
                'distances': distances,
                'average': avg_dist,
                'variation_percent': variation,
            }
        )
    
    def _validate_rectangle(self, analyzer: AdvancedGeometricAnalyzer,
                          angles: Dict[str, float],
                          diagonals: List[Dict]) -> ValidationResult:
        """Valide un rectangle"""
        # Vérifier les angles
        angle_values = list(angles.values())
        all_90 = all(abs(angle - 90) < 5 for angle in angle_values)
        
        # Vérifier les diagonales égales
        if len(diagonals) >= 2:
            diag_lengths = [d['length'] for d in diagonals]
            diagonals_equal = abs(diag_lengths[0] - diag_lengths[1]) / diag_lengths[0] < 0.05
        else:
            diagonals_equal = False
        
        valid = all_90 and diagonals_equal
        
        return ValidationResult(
            valid=valid,
            criterion_name='rectangle',
            details={
                'angles_90': all_90,
                'diagonals_equal': diagonals_equal,
                'angles': angles,
            }
        )
    
    def _validate_circle(self, analyzer: AdvancedGeometricAnalyzer,
                        radii: List[Dict]) -> ValidationResult:
        """Valide un cercle"""
        if not radii:
            return ValidationResult(
                valid=False,
                criterion_name='cercle',
                error_message='Aucun rayon détecté'
            )
        
        radius_values = [r['radius'] for r in radii]
        avg_radius = np.mean(radius_values)
        std_radius = np.std(radius_values)
        
        variation = (std_radius / (avg_radius + 1e-10)) * 100
        tolerance = 5.0
        
        valid = variation < tolerance
        
        return ValidationResult(
            valid=valid,
            criterion_name='cercle',
            actual_value=variation,
            expected_value=0.0,
            tolerance=tolerance,
            details={
                'average_radius': avg_radius,
                'std_deviation': std_radius,
                'variation_percent': variation,
            }
        )
    
    def _validate_symmetry(self, analyzer: AdvancedGeometricAnalyzer) -> ValidationResult:
        """Valide la symétrie"""
        h_sym = analyzer.has_symmetry('horizontal')
        v_sym = analyzer.has_symmetry('vertical')
        
        valid = h_sym or v_sym
        
        return ValidationResult(
            valid=valid,
            criterion_name='symétrie',
            details={
                'horizontal_symmetry': h_sym,
                'vertical_symmetry': v_sym,
            }
        )
    
    def _validate_regular_polygon(self, analyzer: AdvancedGeometricAnalyzer,
                                distances: Dict[str, float],
                                angles: Dict[str, float]) -> ValidationResult:
        """Valide un polygone régulier"""
        # Vérifier les côtés égaux
        if distances:
            dist_values = list(distances.values())
            avg_dist = np.mean(dist_values)
            sides_equal = all(abs(d - avg_dist) / avg_dist < 0.05 for d in dist_values)
        else:
            sides_equal = False
        
        # Vérifier les angles égaux
        if angles:
            angle_values = list(angles.values())
            avg_angle = np.mean(angle_values)
            angles_equal = all(abs(a - avg_angle) / avg_angle < 0.05 for a in angle_values)
        else:
            angles_equal = False
        
        valid = sides_equal and angles_equal
        
        return ValidationResult(
            valid=valid,
            criterion_name='régulier',
            details={
                'sides_equal': sides_equal,
                'angles_equal': angles_equal,
            }
        )
    
    def _validate_diagonals(self, diagonals: List[Dict]) -> ValidationResult:
        """Valide la présence de diagonales"""
        valid = len(diagonals) > 0
        
        return ValidationResult(
            valid=valid,
            criterion_name='diagonales',
            actual_value=len(diagonals),
            details={
                'count': len(diagonals),
                'diagonals': diagonals,
            }
        )
    
    def _validate_distances(self, distances: Dict[str, float],
                          theoretical_data: Optional[Dict]) -> ValidationResult:
        """Valide les distances selon données théoriques"""
        if not theoretical_data or 'expected_distances' not in theoretical_data:
            return ValidationResult(
                valid=True,
                criterion_name='distance',
                details={'distances': distances}
            )
        
        # Comparer avec les données théoriques
        expected = theoretical_data['expected_distances']
        errors = []
        
        for key, expected_val in expected.items():
            if key in distances:
                actual_val = distances[key]
                error = abs(actual_val - expected_val) / expected_val
                if error > 0.1:
                    errors.append(f"{key}: {error*100:.1f}% d'erreur")
        
        valid = len(errors) == 0
        
        return ValidationResult(
            valid=valid,
            criterion_name='distance',
            details={
                'actual_distances': distances,
                'expected_distances': expected,
                'errors': errors,
            }
        )
    
    def _validate_angles(self, angles: Dict[str, float],
                        theoretical_data: Optional[Dict]) -> ValidationResult:
        """Valide les angles selon données théoriques"""
        if not theoretical_data or 'expected_angles' not in theoretical_data:
            return ValidationResult(
                valid=True,
                criterion_name='angle',
                details={'angles': angles}
            )
        
        # Comparer avec les données théoriques
        expected = theoretical_data['expected_angles']
        errors = []
        
        for key, expected_val in expected.items():
            if key in angles:
                actual_val = angles[key]
                error = abs(actual_val - expected_val)
                if error > 5:  # 5 degrés de tolérance
                    errors.append(f"{key}: {error:.1f}° d'erreur")
        
        valid = len(errors) == 0
        
        return ValidationResult(
            valid=valid,
            criterion_name='angle',
            details={
                'actual_angles': angles,
                'expected_angles': expected,
                'errors': errors,
            }
        )


# ============================================================================
# VALIDATEUR D'IMAGE
# ============================================================================

class ImageParametricValidator:
    """Valide les images de figures selon critères paramétriques"""
    
    def __init__(self):
        self.validator = ParametricValidator()
    
    def validate_image_with_criteria(self,
                                     image_path: str | Path,
                                     points: List[Tuple[float, float]],
                                     criteria: str | List[str],
                                     theoretical_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Valide une image avec critères spécifiques
        
        Args:
            image_path: Chemin de l'image
            points: Points de la figure détectés
            criteria: Critères en langage naturel ou liste
            theoretical_data: Données théoriques pour comparaison
        
        Returns:
            Résultats complets de validation
        """
        
        validation_result = self.validator.validate_figure(
            points,
            criteria,
            theoretical_data
        )
        
        validation_result['image_path'] = str(image_path)
        
        return validation_result
    
    def generate_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Génère un rapport de validation"""
        report = f"""
╭────────────────────────────────────────────────────────────────╮
│         RAPPORT DE VALIDATION PARAMÉTRIQUE - GABRIEL          │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: {validation_result.get('image_path', 'N/A')}

🔍 FIGURE
   Type: {validation_result.get('figure_name', 'N/A')}
   Points: {validation_result.get('points_count', 0)}

📋 CRITÈRES VÉRIFIÉS
"""
        
        for criterion in validation_result.get('criteria_checked', []):
            report += f"   • {criterion}\n"
        
        report += "\n✅ RÉSULTATS DES VALIDATIONS\n"
        
        for validation in validation_result.get('validations', []):
            status = "✓ VALIDE" if validation.valid else "✗ INVALIDE"
            report += f"""   {status} - {validation.criterion_name}
      Message: {validation.error_message or 'OK'}
"""
            if validation.details:
                for key, value in validation.details.items():
                    if isinstance(value, (int, float)):
                        report += f"      {key}: {value:.2f}\n"
                    else:
                        report += f"      {key}: {value}\n"
        
        report += f"\n📊 DÉTAILS GÉOMÉTRIQUES\n"
        
        for key, value in validation_result.get('details', {}).items():
            if isinstance(value, (int, float)):
                report += f"   {key}: {value:.2f}\n"
            else:
                report += f"   {key}: {value}\n"
        
        report += f"\n🎯 RÉSULTAT GLOBAL\n"
        overall = "✓ FIGURE VALIDE" if validation_result.get('overall_valid') else "✗ FIGURE INVALIDE"
        report += f"   {overall}\n"
        
        return report


# Singleton global
_parametric_validator: Optional[ImageParametricValidator] = None


def get_parametric_validator() -> ImageParametricValidator:
    """Obtient ou crée le validateur paramétrique"""
    global _parametric_validator
    
    if _parametric_validator is None:
        _parametric_validator = ImageParametricValidator()
    
    return _parametric_validator


def validate_figure_parametric(points: List[Tuple[float, float]],
                               criteria: str | List[str],
                               theoretical_data: Optional[Dict] = None) -> Dict[str, Any]:
    """Valide une figure avec critères paramétriques"""
    validator = get_parametric_validator()
    return validator.validate_image_with_criteria(
        "unknown",
        points,
        criteria,
        theoretical_data
    )


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Gabriel Parametric Validation - Module initialisé        ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # Exemple: Triangle
    triangle_points = [(0, 0), (100, 0), (50, 86.6)]
    
    validator = get_parametric_validator()
    result = validator.validate_image_with_criteria(
        "C:/test_triangle.png",
        triangle_points,
        "triangle équilatéral avec rayons"
    )
    
    print(validator.generate_validation_report(result))
