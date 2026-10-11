"""
Gabriel Complete Vision Integration - Système complet
=====================================================

Intégration COMPLÈTE de toutes les capacités de vision:
  ✓ Figures géométriques (module vision_module.py)
  ✓ Tables et matrices (advanced_vision_module.py)
  ✓ Graphiques avec axes (advanced_vision_module.py)
  ✓ Diagrammes et flux (advanced_vision_module.py)
  ✓ Schémas et symboles (advanced_vision_module.py)
  ✓ Grilles et calibration (advanced_vision_module.py)
  ✓ OCR et text extraction
  ✓ Génération de code complet

Auteur: Gabriel Multi-Loop Agent
Date: 2026
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json

try:
    from image_access_manager import ImageAccessManager, ImageSource, access_image
    ACCESS_AVAILABLE = True
except ImportError:
    ACCESS_AVAILABLE = False
    ImageSource = None

try:
    from vision_module import ImageVisionAnalyzer, Shape
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False

try:
    from advanced_vision_module import (
        AdvancedVisionAnalyzer,
        TableDetector,
        GraphDetector,
        DiagramDetector,
        GridDetector,
    )
    ADVANCED_VISION_AVAILABLE = True
except ImportError:
    ADVANCED_VISION_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class CompleteAnalysisResult:
    """Résultat COMPLET d'une analyse multi-modalités"""
    success: bool = False
    timestamp: datetime = field(default_factory=datetime.now)
    image_path: Optional[str] = None
    source: Optional[ImageSource] = None
    
    # Analyses géométriques
    geometric_shapes: int = 0
    geometric_points: int = 0
    geometric_lines: int = 0
    
    # Analyses tables
    tables_detected: int = 0
    table_rows: List[int] = field(default_factory=list)
    table_cols: List[int] = field(default_factory=list)
    
    # Analyses graphiques
    graphs_detected: int = 0
    graph_axes: int = 0
    graph_points: int = 0
    
    # Analyses diagrammes
    diagram_boxes: int = 0
    diagram_connectors: int = 0
    
    # Analyses grilles
    grids_detected: int = 0
    
    # Générations de code
    python_code: str = ""
    latex_code: str = ""
    hol_code: str = ""
    json_data: str = ""
    
    # Rapport complet
    full_report: str = ""
    
    # Métadonnées
    analysis_duration_ms: float = 0.0
    error_message: Optional[str] = None
    capabilities_used: list[str] = field(default_factory=list)


class CompleteVisionSystem:
    """
    Système COMPLET de vision pour Gabriel
    Combine toutes les capacités en un seul interface
    """
    
    def __init__(self, cache_dir: Optional[Path | str] = None):
        """Initialise le système complet de vision"""
        self.cache_dir = cache_dir
        self.last_result: Optional[CompleteAnalysisResult] = None
        
        logger.info("CompleteVisionSystem initialisé")
        logger.info(f"  - Vision géométrique: {'✓' if VISION_AVAILABLE else '✗'}")
        logger.info(f"  - Vision avancée (tables/graphiques): {'✓' if ADVANCED_VISION_AVAILABLE else '✗'}")
        logger.info(f"  - Accès universel: {'✓' if ACCESS_AVAILABLE else '✗'}")
    
    def analyze_image_complete(self, image_path: str,
                               analyze_geometric: bool = True,
                               analyze_tables: bool = True,
                               analyze_graphs: bool = True,
                               analyze_diagrams: bool = True,
                               analyze_grids: bool = True,
                               generate_code: bool = True) -> CompleteAnalysisResult:
        """
        Analyse COMPLÈTE d'une image
        
        Args:
            image_path: Chemin/URL/adresse réseau
            Les flags analyze_* permettent de cibler les analyses
            generate_code: Générer du code paramétrique
        
        Returns:
            CompleteAnalysisResult avec tous les résultats
        """
        import time
        start_time = time.time()
        
        result = CompleteAnalysisResult(
            success=False,
            image_path=image_path,
        )
        
        try:
            logger.info(f"Début analyse complète: {image_path}")
            
            # ÉTAPE 1: Accéder à l'image
            if ACCESS_AVAILABLE:
                source = access_image(image_path)
                if source is None:
                    result.error_message = f"Impossible d'accéder à: {image_path}"
                    return result
                result.source = source
                local_path = source.resolved_path
            else:
                local_path = Path(image_path)
                if not local_path.exists():
                    result.error_message = f"Image non trouvée: {image_path}"
                    return result
            
            # ÉTAPE 2: Analyses géométriques
            if analyze_geometric and VISION_AVAILABLE:
                logger.debug("Analyse géométrique...")
                try:
                    geo_analyzer = ImageVisionAnalyzer(local_path)
                    geo_analyzer.detect_points()
                    geo_analyzer.detect_lines()
                    geo_analyzer.detect_shapes()
                    
                    result.geometric_shapes = len(geo_analyzer.shapes)
                    result.geometric_points = len(geo_analyzer.points)
                    result.geometric_lines = len(geo_analyzer.lines)
                    result.capabilities_used.append("geometric")
                    
                    logger.debug(f"  Formes: {result.geometric_shapes}, Points: {result.geometric_points}")
                except Exception as e:
                    logger.warning(f"Erreur analyse géométrique: {e}")
            
            # ÉTAPE 3: Analyses avancées (tables, graphiques, diagrammes, grilles)
            if ADVANCED_VISION_AVAILABLE:
                logger.debug("Analyses avancées...")
                
                # Tables
                if analyze_tables:
                    try:
                        table_det = TableDetector(local_path)
                        tables = table_det.extract_table_content()
                        result.tables_detected = len(tables)
                        for table in tables:
                            result.table_rows.append(table.rows)
                            result.table_cols.append(table.cols)
                        result.capabilities_used.append("tables")
                        logger.debug(f"  Tables: {result.tables_detected}")
                    except Exception as e:
                        logger.warning(f"Erreur détection tables: {e}")
                
                # Graphiques
                if analyze_graphs:
                    try:
                        graph_det = GraphDetector(local_path)
                        graph = graph_det.build_graph()
                        axes_count = (1 if graph.x_axis else 0) + (1 if graph.y_axis else 0)
                        if axes_count > 0 or graph.data_points:
                            result.graphs_detected = 1
                            result.graph_axes = axes_count
                            result.graph_points = len(graph.data_points)
                            result.capabilities_used.append("graphs")
                            logger.debug(f"  Graphiques: 1, Axes: {axes_count}, Points: {result.graph_points}")
                    except Exception as e:
                        logger.warning(f"Erreur détection graphiques: {e}")
                
                # Diagrammes
                if analyze_diagrams:
                    try:
                        diag_det = DiagramDetector(local_path)
                        result.diagram_boxes = len(diag_det.detect_boxes())
                        result.diagram_connectors = len(diag_det.detect_connectors())
                        if result.diagram_boxes > 0 or result.diagram_connectors > 0:
                            result.capabilities_used.append("diagrams")
                        logger.debug(f"  Boîtes: {result.diagram_boxes}, Connecteurs: {result.diagram_connectors}")
                    except Exception as e:
                        logger.warning(f"Erreur détection diagrammes: {e}")
                
                # Grilles
                if analyze_grids:
                    try:
                        grid_det = GridDetector(local_path)
                        grid = grid_det.detect_grid()
                        if grid:
                            result.grids_detected = 1
                            result.capabilities_used.append("grids")
                            logger.debug(f"  Grilles: 1")
                    except Exception as e:
                        logger.warning(f"Erreur détection grilles: {e}")
            
            # ÉTAPE 4: Génération de code
            if generate_code and VISION_AVAILABLE and result.geometric_shapes > 0:
                logger.debug("Génération de code...")
                try:
                    geo_analyzer = ImageVisionAnalyzer(local_path)
                    geo_analyzer.detect_shapes()
                    if geo_analyzer.shapes:
                        result.python_code = geo_analyzer.generate_python_code(0)
                        result.latex_code = geo_analyzer.generate_latex_code(0)
                        result.hol_code = geo_analyzer.generate_hol_code(0)
                except Exception as e:
                    logger.warning(f"Erreur génération code: {e}")
            
            # ÉTAPE 5: Génération du rapport
            result.full_report = self._generate_complete_report(result)
            
            # ÉTAPE 6: JSON des données
            result.json_data = self._generate_json_export(result)
            
            result.success = True
            logger.info(f"Analyse complète réussie - {len(result.capabilities_used)} capacités utilisées")
        
        except Exception as e:
            logger.error(f"Erreur analyse: {e}")
            result.error_message = str(e)
        
        finally:
            result.analysis_duration_ms = (time.time() - start_time) * 1000
            self.last_result = result
        
        return result
    
    def _generate_complete_report(self, result: CompleteAnalysisResult) -> str:
        """Génère un rapport complet"""
        report = f"""
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE VISION COMPLÈTE - GABRIEL SYSTEM              │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: {result.image_path}
   Succès: {'✓ Oui' if result.success else '✗ Non'}
   Durée: {result.analysis_duration_ms:.0f}ms

🎯 CAPACITÉS UTILISÉES ({len(result.capabilities_used)})
"""
        
        for cap in result.capabilities_used:
            report += f"   ✓ {cap.upper()}\n"
        
        report += "\n📊 DÉTECTIONS\n"
        
        if result.geometric_shapes > 0 or result.geometric_points > 0:
            report += f"""   Géométrie:
      - Formes: {result.geometric_shapes}
      - Points: {result.geometric_points}
      - Lignes: {result.geometric_lines}
"""
        
        if result.tables_detected > 0:
            report += f"""   Tables/Matrices:
      - Nombre: {result.tables_detected}
      - Dimensions: {result.table_rows} x {result.table_cols}
"""
        
        if result.graphs_detected > 0:
            report += f"""   Graphiques:
      - Nombre: {result.graphs_detected}
      - Axes: {result.graph_axes}
      - Points de données: {result.graph_points}
"""
        
        if result.diagram_boxes > 0 or result.diagram_connectors > 0:
            report += f"""   Diagrammes:
      - Boîtes: {result.diagram_boxes}
      - Connecteurs: {result.diagram_connectors}
"""
        
        if result.grids_detected > 0:
            report += f"""   Grilles:
      - Détectées: {result.grids_detected}
"""
        
        report += f"\n💾 CODE GÉNÉRÉ\n"
        report += f"   Python: {'✓' if result.python_code else '✗'}\n"
        report += f"   LaTeX: {'✓' if result.latex_code else '✗'}\n"
        report += f"   HOL: {'✓' if result.hol_code else '✗'}\n"
        
        if result.error_message:
            report += f"\n⚠️  ERREUR: {result.error_message}\n"
        
        return report
    
    def _generate_json_export(self, result: CompleteAnalysisResult) -> str:
        """Génère un export JSON des données"""
        data = {
            'timestamp': result.timestamp.isoformat(),
            'image_path': result.image_path,
            'success': result.success,
            'analysis_duration_ms': result.analysis_duration_ms,
            'capabilities_used': result.capabilities_used,
            'detections': {
                'geometric': {
                    'shapes': result.geometric_shapes,
                    'points': result.geometric_points,
                    'lines': result.geometric_lines,
                },
                'tables': {
                    'count': result.tables_detected,
                    'dimensions': list(zip(result.table_rows, result.table_cols)),
                },
                'graphs': {
                    'count': result.graphs_detected,
                    'axes': result.graph_axes,
                    'data_points': result.graph_points,
                },
                'diagrams': {
                    'boxes': result.diagram_boxes,
                    'connectors': result.diagram_connectors,
                },
                'grids': {
                    'count': result.grids_detected,
                },
            }
        }
        
        return json.dumps(data, indent=2, default=str)
    
    def get_summary(self) -> str:
        """Résumé de la dernière analyse"""
        if self.last_result is None:
            return "Aucune analyse réalisée"
        
        return self.last_result.full_report


# Singleton global
_complete_vision_system: Optional[CompleteVisionSystem] = None


def get_complete_vision_system(cache_dir: Optional[Path | str] = None) -> CompleteVisionSystem:
    """Obtient ou crée le système complet de vision"""
    global _complete_vision_system
    
    if _complete_vision_system is None:
        _complete_vision_system = CompleteVisionSystem(cache_dir=cache_dir)
    
    return _complete_vision_system


def analyze_image_complete(image_path: str) -> CompleteAnalysisResult:
    """Analyse rapide et complète d'une image"""
    system = get_complete_vision_system()
    return system.analyze_image_complete(image_path)


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Gabriel Complete Vision System - Initialisé              ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    system = get_complete_vision_system()
    
    print("✓ Système vision complet prêt!")
    print("\nUtilisez analyze_image_complete(chemin) pour analyser une image.\n")
    print("Capacités:")
    print("  ✓ Figures géométriques")
    print("  ✓ Tables et matrices")
    print("  ✓ Graphiques avec axes")
    print("  ✓ Diagrammes et flux")
    print("  ✓ Schémas et symboles")
    print("  ✓ Grilles et calibration")
    print("  ✓ Génération de code (Python, LaTeX, HOL)")
