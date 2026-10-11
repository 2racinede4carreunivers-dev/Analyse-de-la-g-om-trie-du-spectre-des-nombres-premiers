"""
Gabriel Image Analysis Interface - Module d'interface utilisateur
==================================================================

Permet aux utilisateurs de demander à Gabriel d'analyser des images
sauvegardées sur leur système local.

Usage dans Gabriel:
  "analyse image C:\path\to\image.png"
  "valide image C:\path\to\figure.png"
  "examine C:\path\to\schema.png pour des rayons"
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional, Dict, Any
import re

try:
    from complete_validation_integration import get_complete_vision_system
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False

try:
    from production_validation_system import get_production_validation_system
    PRODUCTION_AVAILABLE = True
except ImportError:
    PRODUCTION_AVAILABLE = False

logger = logging.getLogger(__name__)


class GabrielImageInterface:
    """
    Interface pour les demandes d'analyse d'images à Gabriel
    Comprend et traite les requêtes en langage naturel
    """
    
    def __init__(self):
        """Initialise l'interface"""
        if VISION_AVAILABLE:
            self.vision_system = get_complete_vision_system()
        else:
            self.vision_system = None
        
        if PRODUCTION_AVAILABLE:
            self.production_system = get_production_validation_system()
        else:
            self.production_system = None
    
    def process_image_request(self, user_input: str) -> Dict[str, Any]:
        """
        Traite une requête d'analyse d'image en langage naturel
        
        Exemples de requêtes:
        - "analyse image C:\path\image.png"
        - "valide C:\path\figure.png"
        - "examine C:\path\schema.png pour des rayons"
        - "C:\path\quadrature.png contient-elle des propriétés géométriques?"
        - "scan C:\path\matrice.png et extrait les données"
        
        Args:
            user_input: Requête en langage naturel
        
        Returns:
            Dict avec résultats et métadonnées
        """
        
        logger.info(f"Processing image request: {user_input}")
        
        # ÉTAPE 1: Extraire le chemin d'image
        image_path = self._extract_image_path(user_input)
        
        if not image_path:
            return {
                'success': False,
                'error': 'Aucun chemin d\'image détecté. Format: "analyse image C:\\chemin\\image.png"',
                'suggestion': 'Utilisez: analyse image C:\\theories\\figures\\image.png'
            }
        
        # ÉTAPE 2: Vérifier l'accès au fichier
        if not Path(image_path).exists():
            return {
                'success': False,
                'error': f'Fichier non trouvé: {image_path}',
                'suggestion': f'Vérifiez le chemin: {image_path}'
            }
        
        # ÉTAPE 3: Déterminer le type d'analyse demandé
        analysis_type = self._detect_analysis_type(user_input)
        
        # ÉTAPE 4: Extraire les critères/paramètres
        criteria = self._extract_criteria(user_input)
        
        # ÉTAPE 5: Effectuer l'analyse
        result = self._perform_analysis(image_path, analysis_type, criteria)
        
        return result
    
    def _extract_image_path(self, user_input: str) -> Optional[str]:
        """Extrait le chemin d'image de la requête"""
        
        # Patterns possibles:
        # C:\path\image.png
        # C:/path/image.png
        # /path/image.png
        # ./relative/path.png
        
        # Pattern Windows: C:\ ou C:/
        windows_pattern = r'[A-Za-z]:[\\\/][^\s]+'
        match = re.search(windows_pattern, user_input)
        if match:
            path = match.group(0).strip('"\'')
            # Normaliser les slashes
            path = path.replace('/', '\\')
            return path
        
        # Pattern Unix: /...
        unix_pattern = r'(?:^|\s)(/[^\s]+)'
        match = re.search(unix_pattern, user_input)
        if match:
            return match.group(1).strip()
        
        # Pattern relatif: ./...
        relative_pattern = r'(?:^|\s)(\.[\\\/][^\s]+)'
        match = re.search(relative_pattern, user_input)
        if match:
            return match.group(1).strip()
        
        return None
    
    def _detect_analysis_type(self, user_input: str) -> str:
        """Détecte le type d'analyse demandé"""
        
        user_lower = user_input.lower()
        
        # Vision complète (tous types)
        if any(word in user_lower for word in ['complet', 'complet', 'tous les', 'tout', 'analyse complet', 'scan complet']):
            return 'complete_vision'
        
        # Géométrie formelle
        if any(word in user_lower for word in ['géométr', 'geometr', 'formel', 'figure', 'polyg', 'triangle', 'quadrilat', 'propriét', 'property']):
            return 'formal_geometry'
        
        # Table/Matrice
        if any(word in user_lower for word in ['table', 'matric', 'données', 'data', 'ocr', 'extrait']):
            return 'table_analysis'
        
        # Graphique
        if any(word in user_lower for word in ['graphique', 'graph', 'courbe', 'axes', 'axis', 'plot']):
            return 'graph_analysis'
        
        # Validation paramétrique
        if any(word in user_lower for word in ['valid', 'vérifie', 'verif', 'contrôl', 'rayon', 'ray']):
            return 'parametric_validation'
        
        # Par défaut: vision complète
        return 'complete_vision'
    
    def _extract_criteria(self, user_input: str) -> list[str]:
        """Extrait les critères de validation si présents"""
        
        criteria = []
        user_lower = user_input.lower()
        
        # Critères géométriques
        criterion_map = {
            'rayon': 'rayons',
            'symétri': 'symétrie',
            'symmet': 'symétrie',
            'équilateral': 'équilatéral',
            'equilateral': 'équilatéral',
            'rectangle': 'rectangle',
            'cercle': 'cercle',
            'circle': 'cercle',
            'régulier': 'régulier',
            'regular': 'régulier',
            'diagonal': 'diagonales',
            'distance': 'distance',
            'angle': 'angle',
        }
        
        for keyword, criterion in criterion_map.items():
            if keyword in user_lower:
                criteria.append(criterion)
        
        return criteria if criteria else ['rayons', 'régulier']  # Par défaut
    
    def _perform_analysis(self, image_path: str, analysis_type: str, criteria: list[str]) -> Dict[str, Any]:
        """Effectue l'analyse selon le type demandé"""
        
        try:
            if analysis_type == 'complete_vision':
                return self._analyze_complete_vision(image_path, criteria)
            
            elif analysis_type == 'formal_geometry':
                return self._analyze_formal_geometry(image_path, criteria)
            
            elif analysis_type == 'table_analysis':
                return self._analyze_table(image_path)
            
            elif analysis_type == 'graph_analysis':
                return self._analyze_graph(image_path)
            
            elif analysis_type == 'parametric_validation':
                return self._analyze_parametric_validation(image_path, criteria)
            
            else:
                return self._analyze_complete_vision(image_path, criteria)
        
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return {
                'success': False,
                'error': str(e),
                'image_path': image_path,
                'analysis_type': analysis_type
            }
    
    def _analyze_complete_vision(self, image_path: str, criteria: list[str]) -> Dict[str, Any]:
        """Analyse vision complète"""
        
        if not self.vision_system:
            return {'success': False, 'error': 'Vision system unavailable'}
        
        result = self.vision_system.analyze_image_complete(image_path)
        
        return {
            'success': result.success,
            'image_path': image_path,
            'analysis_type': 'complete_vision',
            'timestamp': result.timestamp.isoformat(),
            'detections': {
                'geometric_shapes': result.geometric_shapes,
                'geometric_points': result.geometric_points,
                'geometric_lines': result.geometric_lines,
                'tables': result.tables_detected,
                'graphs': result.graphs_detected,
                'diagrams': result.diagram_boxes,
                'grids': result.grids_detected,
            },
            'capabilities_used': result.capabilities_used,
            'full_report': result.full_report,
            'json_data': result.json_data,
            'error': result.error_message
        }
    
    def _analyze_formal_geometry(self, image_path: str, criteria: list[str]) -> Dict[str, Any]:
        """Analyse géométrie formelle"""
        
        if not self.production_system:
            return {'success': False, 'error': 'Production validation system unavailable'}
        
        # Extraire les points de l'image (simplifié pour cette démo)
        # En production, utiliser complete_vision_system pour extraire les points
        
        return {
            'success': False,
            'error': 'Formal geometry analysis requires point extraction from vision system first',
            'image_path': image_path,
            'note': 'Utilisez "analyse image" pour vision complète d\'abord'
        }
    
    def _analyze_table(self, image_path: str) -> Dict[str, Any]:
        """Analyse table/matrice"""
        
        if not self.vision_system:
            return {'success': False, 'error': 'Vision system unavailable'}
        
        result = self.vision_system.analyze_image_complete(
            image_path,
            analyze_geometric=False,
            analyze_graphs=False,
            analyze_diagrams=False,
            analyze_grids=False,
        )
        
        return {
            'success': result.success,
            'image_path': image_path,
            'analysis_type': 'table',
            'tables_detected': result.tables_detected,
            'report': result.full_report,
            'error': result.error_message
        }
    
    def _analyze_graph(self, image_path: str) -> Dict[str, Any]:
        """Analyse graphique"""
        
        if not self.vision_system:
            return {'success': False, 'error': 'Vision system unavailable'}
        
        result = self.vision_system.analyze_image_complete(
            image_path,
            analyze_geometric=False,
            analyze_tables=False,
            analyze_diagrams=False,
            analyze_grids=False,
        )
        
        return {
            'success': result.success,
            'image_path': image_path,
            'analysis_type': 'graph',
            'graphs_detected': result.graphs_detected,
            'graph_axes': result.graph_axes,
            'graph_points': result.graph_points,
            'report': result.full_report,
            'error': result.error_message
        }
    
    def _analyze_parametric_validation(self, image_path: str, criteria: list[str]) -> Dict[str, Any]:
        """Analyse validation paramétrique"""
        
        if not self.vision_system:
            return {'success': False, 'error': 'Vision system unavailable'}
        
        result = self.vision_system.analyze_image_complete(image_path)
        
        return {
            'success': result.success,
            'image_path': image_path,
            'analysis_type': 'parametric_validation',
            'criteria': criteria,
            'detections': {
                'shapes': result.geometric_shapes,
                'points': result.geometric_points,
            },
            'report': result.full_report,
            'error': result.error_message
        }
    
    def format_result_for_gabriel(self, result: Dict[str, Any]) -> str:
        """Formate le résultat pour affichage Gabriel"""
        
        if not result.get('success'):
            return f"❌ Erreur: {result.get('error', 'Unknown error')}\n{result.get('suggestion', '')}"
        
        output = f"""
╭────────────────────────────────────────────────────────────────╮
│           ANALYSE D'IMAGE GABRIEL - RÉSULTATS                 │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: {result.get('image_path')}
   Type:   {result.get('analysis_type')}

📊 DÉTECTIONS
"""
        
        if 'detections' in result:
            dets = result['detections']
            output += f"""   Formes géométriques: {dets.get('geometric_shapes', 0)}
   Points: {dets.get('geometric_points', 0)}
   Lignes: {dets.get('geometric_lines', 0)}
   Tables: {dets.get('tables', 0)}
   Graphiques: {dets.get('graphs', 0)}
   Diagrammes: {dets.get('diagrams', 0)}
   Grilles: {dets.get('grids', 0)}
"""
        
        if 'capabilities_used' in result:
            output += f"\n✓ CAPACITÉS UTILISÉES\n"
            for cap in result['capabilities_used']:
                output += f"   • {cap.upper()}\n"
        
        if 'report' in result:
            output += f"\n{result['report']}\n"
        
        return output


# Singleton global
_interface: Optional[GabrielImageInterface] = None


def get_gabriel_image_interface() -> GabrielImageInterface:
    """Obtient l'interface d'analyse d'images"""
    global _interface
    
    if _interface is None:
        _interface = GabrielImageInterface()
    
    return _interface


def gabriel_analyze_image(user_input: str) -> str:
    """
    Fonction principale pour Gabriel d'analyser une image
    
    Examples:
        gabriel_analyze_image("analyse image C:\\theorie-mathematique\\src\\tex\\tex-2\\quadrature_parabole_zero_critique.png")
        gabriel_analyze_image("valide C:\\path\\figure.png pour des rayons et symétrie")
        gabriel_analyze_image("examine C:\\path\\schema.png")
    """
    
    interface = get_gabriel_image_interface()
    result = interface.process_image_request(user_input)
    formatted = interface.format_result_for_gabriel(result)
    
    return formatted


if __name__ == '__main__':
    print("Gabriel Image Analysis Interface - Ready")
    print("\nExemples:")
    print("  gabriel_analyze_image('analyse image C:\\\\path\\\\image.png')")
    print("  gabriel_analyze_image('valide C:\\\\path\\\\figure.png')")
    print("  gabriel_analyze_image('examine C:\\\\path\\\\schema.png')")
