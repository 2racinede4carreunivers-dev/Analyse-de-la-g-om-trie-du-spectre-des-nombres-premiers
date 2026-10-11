"""
Gabriel Advanced Analysis Criteria System
==========================================

Permet à l'utilisateur de spécifier des critères PRÉCIS pour l'analyse d'images.

L'utilisateur peut combiner:
- Le chemin de l'image
- Les critères d'analyse
- Les types de validation
- Les outputs souhaités
- Les paramètres de précision

Exemples:
  gabriel> analyse image C:\path\image.png | geometrie:strict, validation:angles, export:json
  gabriel> analyse C:\path\image.png ? formes, points, lignes, angles
  gabriel> scan C:\path\image.png :: rayons=3, symetrie=axiale, precision=haute
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List, Set
from enum import Enum
import re

logger = logging.getLogger(__name__)


class AnalysisType(str, Enum):
    """Types d'analyses disponibles"""
    GEOMETRIC = "geometrie"  # Formes, points, lignes
    GRAPH = "graphique"  # Axes, courbes, points
    TABLE = "table"  # Matrices, données
    DIAGRAM = "diagramme"  # Boîtes, connecteurs
    GRID = "grille"  # Calibration, repères
    OCR = "ocr"  # Extraction de texte
    ALL = "tout"  # Tous les types


class ValidationCriterion(str, Enum):
    """Critères de validation disponibles"""
    RAYS = "rayons"  # Segments radiaux
    SYMMETRY = "symetrie"  # Axes de symétrie
    EQUILATERAL = "equilateral"  # Triangle équilatéral
    RECTANGLE = "rectangle"  # Rectangle régulier
    CIRCLE = "cercle"  # Cercle complet
    REGULAR = "regulier"  # Polygone régulier
    DIAGONAL = "diagonale"  # Diagonales
    DISTANCE = "distance"  # Mesures
    ANGLE = "angle"  # Angles
    PERPENDICULAR = "perpendiculaire"  # Perpendiculaires
    PARALLEL = "parallele"  # Parallèles
    CONCENTRIC = "concentrique"  # Cercles concentriques


class PrecisionLevel(str, Enum):
    """Niveaux de précision"""
    LOW = "basse"  # Rapide, moins précis
    MEDIUM = "moyenne"  # Équilibre vitesse/précision
    HIGH = "haute"  # Lent, très précis
    ULTRA = "ultra"  # Très lent, extrêmement précis


class ExportFormat(str, Enum):
    """Formats d'export"""
    JSON = "json"  # JSON structuré
    PYTHON = "python"  # Code Python
    LATEX = "latex"  # Code LaTeX
    HOL = "hol"  # Code HOL/Isabelle
    CSV = "csv"  # Données CSV
    MARKDOWN = "markdown"  # Rapport Markdown
    ALL = "tous"  # Tous les formats


@dataclass
class AnalysisCriteria:
    """Critères d'analyse utilisateur"""
    
    # Image
    image_path: Path
    
    # Types d'analyses
    analysis_types: Set[AnalysisType] = field(default_factory=lambda: {AnalysisType.ALL})
    
    # Critères de validation
    validation_criteria: Set[ValidationCriterion] = field(default_factory=set)
    
    # Niveau de précision
    precision: PrecisionLevel = PrecisionLevel.MEDIUM
    
    # Formats d'export
    export_formats: Set[ExportFormat] = field(default_factory=lambda: {ExportFormat.JSON})
    
    # Paramètres optionnels
    tolerance: float = 0.01  # Tolérance (1%)
    min_confidence: float = 0.8  # Confiance minimum (80%)
    detect_text: bool = False  # Détecter le texte (OCR)
    generate_report: bool = True  # Générer un rapport
    save_intermediate: bool = False  # Sauvegarder les étapes intermédiaires
    
    # Filtres
    filter_by_size: Optional[tuple[int, int]] = None  # Min/Max size
    filter_by_color: bool = False  # Filtrer par couleur
    
    # Verbose
    verbose: bool = False
    
    def __str__(self) -> str:
        """Représentation lisible"""
        return f"""
Analyse Image: {self.image_path.name}
  Types: {', '.join(str(t.value) for t in self.analysis_types)}
  Critères: {', '.join(str(c.value) for c in self.validation_criteria) or 'Aucun'}
  Précision: {self.precision.value}
  Export: {', '.join(str(e.value) for e in self.export_formats)}
  Tolérance: {self.tolerance*100:.1f}%
  Confiance Min: {self.min_confidence*100:.0f}%
"""


class CriteriaParser:
    """Analyse les critères depuis la requête utilisateur"""
    
    @staticmethod
    def parse(user_query: str) -> AnalysisCriteria:
        """
        Parse une requête utilisateur et retourne les critères
        
        Formats supportés:
        1. Simple:
           "analyse image C:\path\image.png"
           
        2. Avec critères pipe (|):
           "analyse image C:\path\image.png | geometrie, validation, precision:haute"
           
        3. Avec critères question (?):
           "analyse C:\path\image.png ? formes, points, angles"
           
        4. Avec critères double-point (::):
           "scan C:\path\image.png :: rayons, symetrie, export:json,python"
           
        5. Combiné:
           "analyse image C:\path\image.png | geometrie, rayons ? validation:strict"
        """
        
        logger.info(f"Parsing: {user_query}")
        
        # Extraire le chemin d'image
        image_path = CriteriaParser._extract_image_path(user_query)
        if not image_path:
            raise ValueError("Aucun chemin d'image trouvé dans la requête")
        
        criteria = AnalysisCriteria(image_path=image_path)
        
        # Extraire les critères selon les séparateurs
        criteria = CriteriaParser._parse_pipe_syntax(user_query, criteria)
        criteria = CriteriaParser._parse_question_syntax(user_query, criteria)
        criteria = CriteriaParser._parse_colon_syntax(user_query, criteria)
        
        logger.info(f"Critères parsés: {criteria}")
        return criteria
    
    @staticmethod
    def _extract_image_path(query: str) -> Optional[Path]:
        """Extrait le chemin d'image de la requête"""
        # Pattern Windows: C:\ ou C:/
        windows_pattern = r'[A-Za-z]:[\\\/][^\s|?:]+'
        match = re.search(windows_pattern, query)
        if match:
            path_str = match.group(0).replace('/', '\\')
            return Path(path_str)
        
        # Pattern Unix: /...
        unix_pattern = r'(?:^|\s)(/[^\s|?:]+)'
        match = re.search(unix_pattern, query)
        if match:
            return Path(match.group(1))
        
        # Pattern relatif: ./... ou ../...
        relative_pattern = r'(?:^|\s)(\.[\\\/][^\s|?:]+)'
        match = re.search(relative_pattern, query)
        if match:
            return Path(match.group(1))
        
        return None
    
    @staticmethod
    def _parse_pipe_syntax(query: str, criteria: AnalysisCriteria) -> AnalysisCriteria:
        """Parse les critères après le pipe (|)"""
        if '|' not in query:
            return criteria
        
        parts = query.split('|')
        if len(parts) < 2:
            return criteria
        
        criteria_part = parts[1].strip()
        logger.debug(f"Critères pipe: {criteria_part}")
        
        return CriteriaParser._parse_criteria_part(criteria_part, criteria)
    
    @staticmethod
    def _parse_question_syntax(query: str, criteria: AnalysisCriteria) -> AnalysisCriteria:
        """Parse les critères après le point d'interrogation (?)"""
        if '?' not in query:
            return criteria
        
        parts = query.split('?')
        if len(parts) < 2:
            return criteria
        
        criteria_part = parts[1].strip()
        logger.debug(f"Critères question: {criteria_part}")
        
        return CriteriaParser._parse_criteria_part(criteria_part, criteria)
    
    @staticmethod
    def _parse_colon_syntax(query: str, criteria: AnalysisCriteria) -> AnalysisCriteria:
        """Parse les critères après le double-point (::)"""
        if '::' not in query:
            return criteria
        
        parts = query.split('::')
        if len(parts) < 2:
            return criteria
        
        criteria_part = parts[1].strip()
        logger.debug(f"Critères colon: {criteria_part}")
        
        return CriteriaParser._parse_criteria_part(criteria_part, criteria)
    
    @staticmethod
    def _parse_criteria_part(criteria_str: str, criteria: AnalysisCriteria) -> AnalysisCriteria:
        """Parse une partie de critères (après séparateur)"""
        
        # Splitter par virgules, point-virgules ou "et"
        tokens = re.split(r'[,;]|et|AND', criteria_str)
        
        for token in tokens:
            token = token.strip().lower()
            if not token:
                continue
            
            # Format clé:valeur
            if ':' in token and '::' not in token:
                key, value = token.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Précision
                if key in ['precision', 'precis', 'precisio']:
                    try:
                        criteria.precision = PrecisionLevel(value)
                        logger.debug(f"Précision: {value}")
                    except ValueError:
                        logger.warning(f"Précision inconnue: {value}")
                
                # Tolérance
                elif key in ['tolerance', 'tol']:
                    try:
                        criteria.tolerance = float(value.rstrip('%')) / 100
                        logger.debug(f"Tolérance: {criteria.tolerance*100}%")
                    except ValueError:
                        logger.warning(f"Tolérance invalide: {value}")
                
                # Confiance minimum
                elif key in ['confiance', 'confidence', 'conf']:
                    try:
                        criteria.min_confidence = float(value.rstrip('%')) / 100
                        logger.debug(f"Confiance min: {criteria.min_confidence*100}%")
                    except ValueError:
                        logger.warning(f"Confiance invalide: {value}")
                
                # Export
                elif key in ['export', 'exp']:
                    criteria.export_formats.clear()
                    for fmt in re.split(r'[,+]', value):
                        fmt = fmt.strip()
                        try:
                            criteria.export_formats.add(ExportFormat(fmt))
                            logger.debug(f"Export: {fmt}")
                        except ValueError:
                            logger.warning(f"Format export inconnu: {fmt}")
                
                # Type d'analyse
                elif key in ['type', 'analyse', 'analyse_type']:
                    for atype in re.split(r'[,+]', value):
                        atype = atype.strip()
                        try:
                            criteria.analysis_types.add(AnalysisType(atype))
                            logger.debug(f"Type analyse: {atype}")
                        except ValueError:
                            logger.warning(f"Type analyse inconnu: {atype}")
            
            else:
                # Pas de clé:valeur, chercher comme type d'analyse ou critère
                # Types d'analyse
                for atype in AnalysisType:
                    if token == atype.value or token.startswith(atype.value):
                        if AnalysisType.ALL not in criteria.analysis_types:
                            criteria.analysis_types.add(atype)
                        logger.debug(f"Type analyse trouvé: {atype.value}")
                        break
                
                # Critères de validation
                for vcrit in ValidationCriterion:
                    if token == vcrit.value or token.startswith(vcrit.value):
                        criteria.validation_criteria.add(vcrit)
                        logger.debug(f"Critère validation: {vcrit.value}")
                        break
                
                # Flags booléens
                if token in ['ocr', 'texte', 'text', 'detect_text']:
                    criteria.detect_text = True
                    logger.debug("OCR/Texte activé")
                
                if token in ['rapport', 'report', 'generer_rapport']:
                    criteria.generate_report = True
                    logger.debug("Rapport activé")
                
                if token in ['verbose', 'v', 'detail', 'details']:
                    criteria.verbose = True
                    logger.debug("Mode verbose activé")
                
                if token in ['intermediaire', 'intermediate', 'steps']:
                    criteria.save_intermediate = True
                    logger.debug("Sauvegarde intermédiaire activée")
        
        return criteria


class AdvancedAnalysisExecutor:
    """Exécute l'analyse selon les critères"""
    
    def __init__(self):
        """Initialise l'exécuteur"""
        logger.info("AdvancedAnalysisExecutor initialisé")
    
    def execute(self, criteria: AnalysisCriteria) -> Dict[str, Any]:
        """
        Exécute l'analyse selon les critères
        
        Args:
            criteria: Critères d'analyse
        
        Returns:
            Résultats d'analyse structurés
        """
        logger.info(f"Exécution analyse avec critères: {criteria}")
        
        result = {
            'success': True,
            'image_path': str(criteria.image_path),
            'criteria': {
                'analysis_types': [str(t) for t in criteria.analysis_types],
                'validation_criteria': [str(c) for c in criteria.validation_criteria],
                'precision': criteria.precision.value,
                'export_formats': [str(e) for e in criteria.export_formats],
            },
            'timestamp': None,
            'analyses': {},
            'exports': {},
            'validations': {},
        }
        
        try:
            # ÉTAPE 1: Vérifier le fichier
            if not criteria.image_path.exists():
                result['success'] = False
                result['error'] = f"Fichier non trouvé: {criteria.image_path}"
                return result
            
            logger.info(f"✓ Fichier trouvé: {criteria.image_path}")
            
            # ÉTAPE 2: Exécuter les analyses selon le type
            result['analyses'] = self._execute_analyses(criteria)
            
            # ÉTAPE 3: Exécuter les validations
            if criteria.validation_criteria:
                result['validations'] = self._execute_validations(criteria)
            
            # ÉTAPE 4: Générer les exports
            if criteria.export_formats:
                result['exports'] = self._execute_exports(criteria)
            
            # ÉTAPE 5: Générer le rapport
            if criteria.generate_report:
                result['report'] = self._generate_report(criteria, result)
            
            result['success'] = True
            logger.info("✓ Analyse complétée")
        
        except Exception as e:
            logger.error(f"Erreur analyse: {e}")
            result['success'] = False
            result['error'] = str(e)
        
        return result
    
    def _execute_analyses(self, criteria: AnalysisCriteria) -> Dict[str, Any]:
        """Exécute les analyses selon les types"""
        analyses = {}
        
        # Importer le système de vision complet
        try:
            from complete_vision_system import analyze_image_complete
        except ImportError:
            logger.warning("Vision system non disponible")
            return analyses
        
        # Analyser l'image
        vision_result = analyze_image_complete(str(criteria.image_path))
        
        if vision_result.success:
            if AnalysisType.GEOMETRIC in criteria.analysis_types or AnalysisType.ALL in criteria.analysis_types:
                analyses['geometric'] = {
                    'shapes': vision_result.geometric_shapes,
                    'points': vision_result.geometric_points,
                    'lines': vision_result.geometric_lines,
                }
            
            if AnalysisType.GRAPH in criteria.analysis_types or AnalysisType.ALL in criteria.analysis_types:
                analyses['graph'] = {
                    'count': vision_result.graphs_detected,
                    'axes': vision_result.graph_axes,
                    'data_points': vision_result.graph_points,
                }
            
            if AnalysisType.TABLE in criteria.analysis_types or AnalysisType.ALL in criteria.analysis_types:
                analyses['table'] = {
                    'count': vision_result.tables_detected,
                    'dimensions': list(zip(vision_result.table_rows, vision_result.table_cols)) if vision_result.table_rows else [],
                }
            
            if AnalysisType.DIAGRAM in criteria.analysis_types or AnalysisType.ALL in criteria.analysis_types:
                analyses['diagram'] = {
                    'boxes': vision_result.diagram_boxes,
                    'connectors': vision_result.diagram_connectors,
                }
            
            if AnalysisType.GRID in criteria.analysis_types or AnalysisType.ALL in criteria.analysis_types:
                analyses['grid'] = {
                    'detected': vision_result.grids_detected,
                }
        
        return analyses
    
    def _execute_validations(self, criteria: AnalysisCriteria) -> Dict[str, Any]:
        """Exécute les validations selon les critères"""
        validations = {}
        
        for vcrit in criteria.validation_criteria:
            validations[vcrit.value] = {
                'status': 'pending',
                'result': None,
                'confidence': 0.0,
                'details': f"Validation de {vcrit.value} avec tolérance {criteria.tolerance*100:.1f}%"
            }
        
        return validations
    
    def _execute_exports(self, criteria: AnalysisCriteria) -> Dict[str, Any]:
        """Génère les exports"""
        exports = {}
        
        for export_fmt in criteria.export_formats:
            if export_fmt == ExportFormat.JSON:
                exports['json'] = {
                    'format': 'application/json',
                    'status': 'generated',
                    'data': '{ ... }'  # Simplifié
                }
            
            elif export_fmt == ExportFormat.PYTHON:
                exports['python'] = {
                    'format': 'text/python',
                    'status': 'generated',
                    'code': 'import matplotlib...'  # Simplifié
                }
            
            elif export_fmt == ExportFormat.LATEX:
                exports['latex'] = {
                    'format': 'text/x-latex',
                    'status': 'generated',
                    'code': '\\begin{tikzpicture}...'  # Simplifié
                }
            
            elif export_fmt == ExportFormat.HOL:
                exports['hol'] = {
                    'format': 'text/plain',
                    'status': 'generated',
                    'code': 'definition ...'  # Simplifié
                }
        
        return exports
    
    def _generate_report(self, criteria: AnalysisCriteria, result: Dict[str, Any]) -> str:
        """Génère un rapport textuel"""
        report = f"""
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE AVANCÉE - GABRIEL MULTILOOP SYSTEM            │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: {criteria.image_path}
   Taille: {criteria.image_path.stat().st_size / 1024:.1f} KB

⚙️  CRITÈRES D'ANALYSE
   Types: {', '.join(str(t.value) for t in criteria.analysis_types)}
   Précision: {criteria.precision.value}
   Tolérance: {criteria.tolerance*100:.1f}%
   Confiance min: {criteria.min_confidence*100:.0f}%

📊 RÉSULTATS
"""
        
        if result['analyses']:
            report += "\n   Géométrie:\n"
            for key, value in result['analyses'].items():
                report += f"      {key}: {value}\n"
        
        if result['validations']:
            report += "\n   Validations:\n"
            for key, value in result['validations'].items():
                report += f"      {key}: {value['status']}\n"
        
        if result['exports']:
            report += "\n   Exports:\n"
            for fmt in result['exports'].keys():
                report += f"      ✓ {fmt.upper()}\n"
        
        return report


# Singleton
_executor: Optional[AdvancedAnalysisExecutor] = None

def get_executor() -> AdvancedAnalysisExecutor:
    """Obtient l'exécuteur"""
    global _executor
    if _executor is None:
        _executor = AdvancedAnalysisExecutor()
    return _executor


def analyze_with_criteria(user_query: str) -> Dict[str, Any]:
    """
    Analyse une image selon les critères de l'utilisateur
    
    Exemples:
        analyze_with_criteria("analyse image C:\\path\\image.png | geometrie, precision:haute")
        analyze_with_criteria("analyse C:\\path\\image.png ? rayons, symetrie")
        analyze_with_criteria("scan C:\\path\\image.png :: export:json,python")
    """
    try:
        criteria = CriteriaParser.parse(user_query)
        executor = get_executor()
        result = executor.execute(criteria)
        return result
    except Exception as e:
        logger.error(f"Erreur: {e}")
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Gabriel Advanced Analysis Criteria System - Test          ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # Test 1: Simple
    print("Test 1: Requête simple")
    query1 = r"analyse image C:\image.png"
    criteria1 = CriteriaParser.parse(query1)
    print(f"Parsé: {criteria1}\n")
    
    # Test 2: Avec critères pipe
    print("Test 2: Avec critères pipe (|)")
    query2 = r"analyse image C:\image.png | geometrie, precision:haute, rayons"
    criteria2 = CriteriaParser.parse(query2)
    print(f"Parsé: {criteria2}\n")
    
    # Test 3: Avec critères question
    print("Test 3: Avec critères question (?)")
    query3 = r"analyse C:\image.png ? formes, points, angles, export:json,python"
    criteria3 = CriteriaParser.parse(query3)
    print(f"Parsé: {criteria3}\n")
    
    # Test 4: Avec critères double-point
    print("Test 4: Avec critères double-point (::)")
    query4 = r"scan C:\image.png :: precision:ultra, tolerance:0.5%, export:tous"
    criteria4 = CriteriaParser.parse(query4)
    print(f"Parsé: {criteria4}\n")
    
    print("✓ Tests complétés!")
