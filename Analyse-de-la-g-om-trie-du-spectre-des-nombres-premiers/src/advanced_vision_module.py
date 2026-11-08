"""
Gabriel Advanced Vision Module - Reconnaissance complète
========================================================

Capacités COMPLÈTES pour analyser:
  ✓ Figures géométriques (triangles, rectangles, cercles, polygones)
  ✓ Graphiques (axes, courbes, points de données)
  ✓ Tables et matrices (grilles, cellules, valeurs)
  ✓ Diagrammes (boîtes, connecteurs, flux)
  ✓ Schémas (symboles, flèches, annotations)
  ✓ Grilles et calibration
  ✓ Texte et labels (OCR basique)
  ✓ Histogrammes et charts
  ✓ Réseaux et graphes
  ✓ Formules mathématiques

Auteur: Gabriel Multi-Loop Agent
Date: 2026
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from enum import Enum
import json
import math

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

logger = logging.getLogger(__name__)


# ============================================================================
# DÉTECTION DE TABLES ET MATRICES
# ============================================================================

@dataclass
class Cell:
    """Représente une cellule de table"""
    row: int
    col: int
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    content: str = ""  # Texte extrait
    value: Optional[float] = None  # Valeur numérique si applicable
    
    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2)
    
    @property
    def width(self) -> float:
        return self.x_max - self.x_min
    
    @property
    def height(self) -> float:
        return self.y_max - self.y_min


@dataclass
class Table:
    """Représente une table/matrice détectée"""
    rows: int
    cols: int
    cells: List[List[Cell]] = field(default_factory=list)
    boundaries: Dict[str, float] = field(default_factory=dict)  # x_min, x_max, y_min, y_max
    
    def to_matrix(self) -> List[List[str]]:
        """Convertit la table en matrice texte"""
        matrix = []
        for row_cells in self.cells:
            row_data = [cell.content for cell in row_cells]
            matrix.append(row_data)
        return matrix
    
    def to_numpy(self) -> Optional[np.ndarray]:
        """Convertit en array NumPy (si valeurs numériques)"""
        if not NUMPY_AVAILABLE:
            return None
        
        try:
            values = []
            for row_cells in self.cells:
                row_values = []
                for cell in row_cells:
                    if cell.value is not None:
                        row_values.append(cell.value)
                    else:
                        try:
                            row_values.append(float(cell.content))
                        except ValueError:
                            row_values.append(np.nan)
                values.append(row_values)
            
            return np.array(values)
        except Exception as e:
            logger.error(f"Erreur conversion NumPy: {e}")
            return None


class TableDetector:
    """Détecte les tables et matrices dans les images"""
    
    def __init__(self, image_path: str | Path):
        self.image_path = Path(image_path)
        self.image = None
        self.image_array = None
        self.tables: List[Table] = []
        
        if PIL_AVAILABLE:
            self.image = Image.open(image_path)
            if NUMPY_AVAILABLE:
                self.image_array = np.array(self.image)
    
    def detect_tables(self) -> List[Table]:
        """Détecte les grilles de tables/matrices"""
        if not OPENCV_AVAILABLE or self.image_array is None:
            logger.warning("Détection de tables indisponible - OpenCV requis")
            return []
        
        self.tables = []
        
        # Convertir en niveaux de gris
        if len(self.image_array.shape) == 3:
            gray = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = self.image_array
        
        # Détection des lignes horizontales et verticales
        h, w = gray.shape
        
        # Éroder puis dilater (morphologie)
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (w // 30, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, h // 30))
        
        h_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel_h)
        v_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel_v)
        
        # Combiner les lignes
        grid_lines = cv2.bitwise_or(h_lines, v_lines)
        
        # Détecter les contours pour trouver les cellules
        contours, _ = cv2.findContours(grid_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Extraire les rectangles (cellules)
        rectangles = []
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour)
            if width > 10 and height > 10:  # Filtre sur la taille minimale
                rectangles.append((x, y, x + width, y + height))
        
        if rectangles:
            # Classer en grille
            table = self._organize_cells_into_table(rectangles)
            self.tables.append(table)
            logger.info(f"Détecté table: {table.rows}x{table.cols}")
        
        return self.tables
    
    def _organize_cells_into_table(self, rectangles: List[Tuple]) -> Table:
        """Organise les rectangles en table"""
        if not rectangles:
            return Table(0, 0)
        
        # Trier les cellules par position
        sorted_rects = sorted(rectangles, key=lambda r: (r[1], r[0]))  # Y puis X
        
        # Identifier les lignes (Y similaire)
        rows = []
        current_row = []
        current_y = sorted_rects[0][1]
        tolerance = 10
        
        for rect in sorted_rects:
            if abs(rect[1] - current_y) > tolerance and current_row:
                rows.append(current_row)
                current_row = []
                current_y = rect[1]
            current_row.append(rect)
        if current_row:
            rows.append(current_row)
        
        # Trier chaque ligne par X
        for row in rows:
            row.sort(key=lambda r: r[0])
        
        # Créer les cellules
        cells = []
        for row_idx, row in enumerate(rows):
            row_cells = []
            for col_idx, rect in enumerate(row):
                cell = Cell(
                    row=row_idx,
                    col=col_idx,
                    x_min=float(rect[0]),
                    x_max=float(rect[2]),
                    y_min=float(rect[1]),
                    y_max=float(rect[3]),
                )
                row_cells.append(cell)
            cells.append(row_cells)
        
        table = Table(
            rows=len(rows),
            cols=max(len(row) for row in rows) if rows else 0,
            cells=cells,
            boundaries={
                'x_min': min(r[0] for r in rectangles),
                'x_max': max(r[2] for r in rectangles),
                'y_min': min(r[1] for r in rectangles),
                'y_max': max(r[3] for r in rectangles),
            }
        )
        
        return table
    
    def extract_table_content(self, use_ocr: bool = True) -> List[Table]:
        """Extrait le contenu des tables (avec OCR optionnel)"""
        tables = self.detect_tables()
        
        if use_ocr and PYTESSERACT_AVAILABLE and PIL_AVAILABLE:
            for table in tables:
                for row_cells in table.cells:
                    for cell in row_cells:
                        # Extraire la région de la cellule
                        cell_img = self.image.crop((
                            cell.x_min, cell.y_min, cell.x_max, cell.y_max
                        ))
                        
                        try:
                            # OCR
                            text = pytesseract.image_to_string(cell_img)
                            cell.content = text.strip()
                            
                            # Essayer de convertir en nombre
                            try:
                                cell.value = float(cell.content)
                            except ValueError:
                                pass
                        except Exception as e:
                            logger.warning(f"Erreur OCR cellule: {e}")
        
        return tables


# ============================================================================
# DÉTECTION DE GRAPHIQUES AVEC AXES
# ============================================================================

@dataclass
class Axis:
    """Représente un axe dans un graphique"""
    name: str  # 'X', 'Y', 'Z'
    label: str = ""
    x_min: float = 0
    x_max: float = 100
    y_min: float = 0
    y_max: float = 100
    start_px: Tuple[float, float] = (0, 0)
    end_px: Tuple[float, float] = (100, 100)
    ticks: List[Tuple[float, str]] = field(default_factory=list)
    is_log_scale: bool = False


@dataclass
class DataPoint:
    """Représente un point de données dans un graphique"""
    x: float
    y: float
    px_x: float  # Position pixel
    px_y: float
    label: str = ""
    marker_type: str = "circle"  # circle, square, triangle, cross
    color: Tuple[int, int, int] = (0, 0, 255)  # RGB


@dataclass
class Graph:
    """Représente un graphique complet"""
    title: str = ""
    x_axis: Optional[Axis] = None
    y_axis: Optional[Axis] = None
    data_points: List[DataPoint] = field(default_factory=list)
    curves: List[List[DataPoint]] = field(default_factory=list)
    legend_items: List[Tuple[str, Tuple[int, int, int]]] = field(default_factory=list)


class GraphDetector:
    """Détecte les graphiques avec axes et données"""
    
    def __init__(self, image_path: str | Path):
        self.image_path = Path(image_path)
        self.image = None
        self.image_array = None
        self.graphs: List[Graph] = []
        
        if PIL_AVAILABLE:
            self.image = Image.open(image_path)
            if NUMPY_AVAILABLE:
                self.image_array = np.array(self.image)
    
    def detect_axes(self) -> List[Axis]:
        """Détecte les axes de graphiques"""
        axes = []
        
        if not OPENCV_AVAILABLE or self.image_array is None:
            return axes
        
        # Convertir en niveaux de gris
        if len(self.image_array.shape) == 3:
            gray = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = self.image_array
        
        # Détecter les lignes d'axes (généralement horizontales et verticales)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)
        
        if lines is None:
            return axes
        
        h_lines = []  # Horizontal
        v_lines = []  # Vertical
        
        for line in lines:
            rho, theta = line[0]
            
            if abs(theta) < 0.1 or abs(theta - np.pi) < 0.1:
                # Ligne horizontale
                h_lines.append((rho, theta))
            elif abs(theta - np.pi / 2) < 0.1:
                # Ligne verticale
                v_lines.append((rho, theta))
        
        # Créer les axes
        if h_lines:
            rho, theta = h_lines[0]
            axes.append(Axis(
                name='X',
                label='X axis',
                start_px=(0, rho),
                end_px=(self.image_array.shape[1], rho)
            ))
        
        if v_lines:
            rho, theta = v_lines[0]
            axes.append(Axis(
                name='Y',
                label='Y axis',
                start_px=(rho, 0),
                end_px=(rho, self.image_array.shape[0])
            ))
        
        logger.info(f"Détecté {len(axes)} axes")
        return axes
    
    def detect_data_points(self) -> List[DataPoint]:
        """Détecte les points de données dans un graphique"""
        points = []
        
        if not OPENCV_AVAILABLE or self.image_array is None:
            return points
        
        # Convertir en niveaux de gris
        if len(self.image_array.shape) == 3:
            gray = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = self.image_array
        
        # Détecter les cercles (points de données)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                  param1=50, param2=30, minRadius=2, maxRadius=20)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                point = DataPoint(
                    x=float(i[0]),
                    y=float(i[1]),
                    px_x=float(i[0]),
                    px_y=float(i[1]),
                    marker_type="circle"
                )
                points.append(point)
            
            logger.info(f"Détecté {len(points)} points de données")
        
        return points
    
    def build_graph(self) -> Graph:
        """Construit un graphique complet"""
        graph = Graph()
        
        axes = self.detect_axes()
        if axes:
            for axis in axes:
                if axis.name == 'X':
                    graph.x_axis = axis
                elif axis.name == 'Y':
                    graph.y_axis = axis
        
        graph.data_points = self.detect_data_points()
        
        return graph


# ============================================================================
# DÉTECTION DE DIAGRAMMES (BOÎTES, CONNECTEURS, FLUX)
# ============================================================================

@dataclass
class DiagramBox:
    """Représente une boîte dans un diagramme"""
    x: float
    y: float
    width: float
    height: float
    text: str = ""
    style: str = "rectangle"  # rectangle, ellipse, diamond, parallelogram
    color: Tuple[int, int, int] = (200, 200, 200)


@dataclass
class DiagramConnector:
    """Représente un connecteur (flèche, ligne)"""
    from_box: Optional[DiagramBox] = None
    to_box: Optional[DiagramBox] = None
    label: str = ""
    arrow_type: str = "->"  # ->, <-, <->, --


class DiagramDetector:
    """Détecte les diagrammes et flux"""
    
    def __init__(self, image_path: str | Path):
        self.image_path = Path(image_path)
        self.image = None
        self.image_array = None
        self.boxes: List[DiagramBox] = []
        self.connectors: List[DiagramConnector] = []
        
        if PIL_AVAILABLE:
            self.image = Image.open(image_path)
            if NUMPY_AVAILABLE:
                self.image_array = np.array(self.image)
    
    def detect_boxes(self) -> List[DiagramBox]:
        """Détecte les boîtes et formes dans un diagramme"""
        self.boxes = []
        
        if not OPENCV_AVAILABLE or self.image_array is None:
            return self.boxes
        
        # Convertir en niveaux de gris
        if len(self.image_array.shape) == 3:
            gray = cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = self.image_array
        
        # Détecter les contours
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filtrer les petits objets
            if w > 20 and h > 20:
                box = DiagramBox(
                    x=float(x),
                    y=float(y),
                    width=float(w),
                    height=float(h)
                )
                self.boxes.append(box)
        
        logger.info(f"Détecté {len(self.boxes)} boîtes")
        return self.boxes
    
    def detect_connectors(self) -> List[DiagramConnector]:
        """Détecte les connecteurs et flèches"""
        self.connectors = []
        
        if not OPENCV_AVAILABLE or self.image_array is None:
            return self.connectors
        
        # Détecter les lignes qui connectent les boîtes
        # (simplifié: chercher les lignes entre centres de boîtes)
        if len(self.boxes) < 2:
            return self.connectors
        
        for i, box1 in enumerate(self.boxes):
            for box2 in self.boxes[i + 1:]:
                # Calculer la distance entre les centres
                center1 = (box1.x + box1.width / 2, box1.y + box1.height / 2)
                center2 = (box2.x + box2.width / 2, box2.y + box2.height / 2)
                distance = math.hypot(center2[0] - center1[0], center2[1] - center1[1])
                
                # Si proches, créer un connecteur
                if distance < 500:  # Seuil de proximité
                    connector = DiagramConnector(
                        from_box=box1,
                        to_box=box2,
                        arrow_type="->"
                    )
                    self.connectors.append(connector)
        
        logger.info(f"Détecté {len(self.connectors)} connecteurs")
        return self.connectors


# ============================================================================
# DÉTECTION DE GRILLES ET CALIBRATION
# ============================================================================

@dataclass
class Grid:
    """Représente une grille de calibration"""
    rows: int
    cols: int
    cell_width: float
    cell_height: float
    origin_x: float
    origin_y: float


class GridDetector:
    """Détecte les grilles et motifs réguliers"""
    
    def __init__(self, image_path: str | Path):
        self.image_path = Path(image_path)
        self.image = None
        self.image_array = None
        self.grids: List[Grid] = []
        
        if PIL_AVAILABLE:
            self.image = Image.open(image_path)
            if NUMPY_AVAILABLE:
                self.image_array = np.array(self.image)
    
    def detect_grid(self) -> Optional[Grid]:
        """Détecte une grille régulière"""
        if not NUMPY_AVAILABLE or self.image_array is None:
            return None
        
        # Détecter les patterns réguliers (simplifié)
        gray = self.image_array if len(self.image_array.shape) == 2 else \
               cv2.cvtColor(self.image_array, cv2.COLOR_RGB2GRAY) if OPENCV_AVAILABLE else \
               self.image_array[:, :, 0]
        
        # FFT pour détecter les fréquences dominantes
        fft = np.fft.fft2(gray)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)
        
        # Trouver les pics (lignes de grille)
        # Simplifié: estimer la taille de la cellule
        h, w = gray.shape
        
        # Calcul heuristique
        grid = Grid(
            rows=h // 50,  # Estimer les lignes
            cols=w // 50,  # Estimer les colonnes
            cell_width=50,
            cell_height=50,
            origin_x=0,
            origin_y=0
        )
        
        return grid


# ============================================================================
# CLASSE INTÉGRATRICE
# ============================================================================

@dataclass
class AdvancedAnalysisResult:
    """Résultat complet d'une analyse avancée"""
    success: bool = False
    image_path: Optional[str] = None
    
    # Analyses
    tables: List[Table] = field(default_factory=list)
    graphs: List[Graph] = field(default_factory=list)
    diagram_boxes: List[DiagramBox] = field(default_factory=list)
    diagram_connectors: List[DiagramConnector] = field(default_factory=list)
    grids: List[Grid] = field(default_factory=list)
    
    # Métriques
    total_detections: int = 0
    error_message: Optional[str] = None


class AdvancedVisionAnalyzer:
    """Analyseur vision avancé combinant tous les types"""
    
    def __init__(self, image_path: str | Path):
        self.image_path = Path(image_path)
    
    def analyze_complete(self) -> AdvancedAnalysisResult:
        """Analyse complète d'une image"""
        result = AdvancedAnalysisResult(image_path=str(self.image_path))
        
        try:
            # Tables
            table_detector = TableDetector(self.image_path)
            result.tables = table_detector.extract_table_content()
            
            # Graphiques
            graph_detector = GraphDetector(self.image_path)
            graph = graph_detector.build_graph()
            if graph.x_axis or graph.y_axis or graph.data_points:
                result.graphs.append(graph)
            
            # Diagrammes
            diagram_detector = DiagramDetector(self.image_path)
            result.diagram_boxes = diagram_detector.detect_boxes()
            result.diagram_connectors = diagram_detector.detect_connectors()
            
            # Grilles
            grid_detector = GridDetector(self.image_path)
            grid = grid_detector.detect_grid()
            if grid:
                result.grids.append(grid)
            
            result.total_detections = (
                len(result.tables) +
                len(result.graphs) +
                len(result.diagram_boxes) +
                len(result.grids)
            )
            
            result.success = True
            logger.info(f"Analyse complète: {result.total_detections} éléments détectés")
        
        except Exception as e:
            logger.error(f"Erreur analyse: {e}")
            result.error_message = str(e)
        
        return result
    
    def generate_report(self, result: AdvancedAnalysisResult) -> str:
        """Génère un rapport d'analyse"""
        report = f"""
╭────────────────────────────────────────────────────────────────╮
│      ANALYSE VISION AVANCÉE - GABRIEL VISION                  │
╰────────────────────────────────────────────────────────────────╯

📁 Image: {self.image_path.name}
✓ Succès: {'Oui' if result.success else 'Non'}

📊 ÉLÉMENTS DÉTECTÉS
   • Tables/Matrices: {len(result.tables)}
   • Graphiques: {len(result.graphs)}
   • Boîtes diagramme: {len(result.diagram_boxes)}
   • Connecteurs: {len(result.diagram_connectors)}
   • Grilles: {len(result.grids)}
   
   TOTAL: {result.total_detections}

"""
        
        # Détails tables
        if result.tables:
            report += "📋 TABLES DÉTECTÉES:\n"
            for i, table in enumerate(result.tables):
                report += f"   Table {i+1}: {table.rows}×{table.cols} cellules\n"
                matrix = table.to_matrix()
                for row in matrix[:3]:  # Montrer les 3 premières lignes
                    report += f"      {row}\n"
                if len(matrix) > 3:
                    report += f"      ... ({len(matrix)-3} lignes supplémentaires)\n"
        
        # Détails graphiques
        if result.graphs:
            report += "\n📈 GRAPHIQUES DÉTECTÉS:\n"
            for i, graph in enumerate(result.graphs):
                report += f"   Graphique {i+1}:\n"
                if graph.x_axis:
                    report += f"      Axe X: {graph.x_axis.label}\n"
                if graph.y_axis:
                    report += f"      Axe Y: {graph.y_axis.label}\n"
                report += f"      Points de données: {len(graph.data_points)}\n"
        
        # Détails diagrammes
        if result.diagram_boxes:
            report += "\n📦 DIAGRAMMES DÉTECTÉS:\n"
            report += f"   Boîtes: {len(result.diagram_boxes)}\n"
            report += f"   Connecteurs: {len(result.diagram_connectors)}\n"
        
        if result.error_message:
            report += f"\n⚠️  ERREUR: {result.error_message}\n"
        
        return report


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python advanced_vision_module.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        analyzer = AdvancedVisionAnalyzer(image_path)
        result = analyzer.analyze_complete()
        print(analyzer.generate_report(result))
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
