"""
Image Vision Module pour Gabriel Multi-Loop Agent
===================================================

Module complet pour l'analyse, validation et génération de code paramétrique
à partir d'images (graphiques, figures géométriques, diagrammes, schémas).

Capacités:
  1. Charger et analyser les images (PNG, JPG, etc.)
  2. Détecter les points, lignes, formes géométriques
  3. Extraire les coordonnées des points
  4. Valider la cohérence entre les points et la figure
  5. Générer du code paramétrique (Python, Isabelle/HOL, LaTeX)
  6. Créer des représentations textuelles (ASCII, SVG)

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
import re

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    logging.warning("NumPy non disponible - certaines analyses limitées")

try:
    from PIL import Image, ImageDraw, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL non disponible - analyse d'images limitée")

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV non disponible - détection de contours limitée")

logger = logging.getLogger(__name__)


class PointType(Enum):
    """Types de points détectables"""
    VERTEX = "vertex"  # Sommet (coin)
    INTERSECTION = "intersection"  # Intersection de lignes
    EXTREMUM = "extremum"  # Point extrême (max/min)
    MARKED = "marked"  # Point marqué explicitement
    ENDPOINT = "endpoint"  # Extrémité de ligne/segment
    GRID = "grid"  # Point de grille


class LineType(Enum):
    """Types de lignes détectables"""
    STRAIGHT = "straight"
    CURVED = "curved"
    DOTTED = "dotted"
    DASHED = "dashed"
    AXIS = "axis"


@dataclass
class Point:
    """Représente un point dans une image"""
    x: float
    y: float
    type: PointType
    label: Optional[str] = None
    confidence: float = 1.0  # 0.0 à 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def distance_to(self, other: Point) -> float:
        """Distance euclidienne à un autre point"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def to_dict(self) -> dict:
        return {
            'x': self.x,
            'y': self.y,
            'type': self.type.value,
            'label': self.label,
            'confidence': self.confidence,
            'metadata': self.metadata,
        }


@dataclass
class Line:
    """Représente une ligne dans une image"""
    start: Point
    end: Point
    type: LineType
    label: Optional[str] = None
    confidence: float = 1.0
    is_horizontal: bool = False
    is_vertical: bool = False
    slope: Optional[float] = None
    
    def length(self) -> float:
        """Longueur de la ligne"""
        return self.start.distance_to(self.end)
    
    def is_parallel_to(self, other: Line, tolerance: float = 0.1) -> bool:
        """Vérifie si la ligne est parallèle à une autre"""
        if self.slope is None or other.slope is None:
            return False
        return abs(self.slope - other.slope) < tolerance
    
    def is_perpendicular_to(self, other: Line, tolerance: float = 0.1) -> bool:
        """Vérifie si la ligne est perpendiculaire à une autre"""
        if self.slope is None or other.slope is None:
            return False
        product = self.slope * other.slope
        return abs(product + 1) < tolerance
    
    def to_dict(self) -> dict:
        return {
            'start': self.start.to_dict(),
            'end': self.end.to_dict(),
            'type': self.type.value,
            'label': self.label,
            'length': self.length(),
            'slope': self.slope,
            'is_horizontal': self.is_horizontal,
            'is_vertical': self.is_vertical,
        }


@dataclass
class Shape:
    """Représente une forme géométrique"""
    type: str  # 'triangle', 'rectangle', 'circle', 'polygon', etc.
    points: List[Point]
    lines: List[Line] = field(default_factory=list)
    label: Optional[str] = None
    area: Optional[float] = None
    perimeter: Optional[float] = None
    center: Optional[Point] = None
    
    def calculate_area(self) -> float:
        """Calcule l'aire de la forme (shoelace formula pour polygones)"""
        if len(self.points) < 3:
            return 0.0
        
        area = 0.0
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            area += p1.x * p2.y - p2.x * p1.y
        
        return abs(area) / 2.0
    
    def calculate_perimeter(self) -> float:
        """Calcule le périmètre"""
        perimeter = 0.0
        for line in self.lines:
            perimeter += line.length()
        return perimeter
    
    def calculate_center(self) -> Point:
        """Calcule le centre de masse"""
        if not self.points:
            return Point(0, 0, PointType.MARKED)
        
        cx = sum(p.x for p in self.points) / len(self.points)
        cy = sum(p.y for p in self.points) / len(self.points)
        
        return Point(cx, cy, PointType.MARKED, label="center")
    
    def to_dict(self) -> dict:
        return {
            'type': self.type,
            'label': self.label,
            'points': [p.to_dict() for p in self.points],
            'lines': [l.to_dict() for l in self.lines],
            'area': self.calculate_area(),
            'perimeter': self.calculate_perimeter(),
            'center': self.calculate_center().to_dict(),
        }


class ImageVisionAnalyzer:
    """Analyseur d'images pour Gabriel"""
    
    def __init__(self, image_path: str | Path):
        """
        Initialise l'analyseur avec un chemin d'image
        
        Args:
            image_path: Chemin vers le fichier image
        """
        self.image_path = Path(image_path)
        self.image = None
        self.image_array = None
        self.points: List[Point] = []
        self.lines: List[Line] = []
        self.shapes: List[Shape] = []
        self.width: int = 0
        self.height: int = 0
        self.metadata: Dict[str, Any] = {}
        
        if not self.image_path.exists():
            raise FileNotFoundError(f"Image non trouvée: {image_path}")
        
        self._load_image()
    
    def _load_image(self) -> None:
        """Charge l'image"""
        if not PIL_AVAILABLE:
            logger.error("PIL non disponible - impossible de charger l'image")
            return
        
        try:
            self.image = Image.open(self.image_path)
            self.width, self.height = self.image.size
            
            # Convertir en array NumPy si disponible
            if NUMPY_AVAILABLE:
                self.image_array = np.array(self.image)
            
            logger.info(f"Image chargée: {self.width}x{self.height} ({self.image.mode})")
            
        except Exception as e:
            logger.error(f"Erreur chargement image: {e}")
            raise
    
    def detect_points(self, threshold: float = 0.5) -> List[Point]:
        """
        Détecte les points importants dans l'image
        
        Args:
            threshold: Seuil de confiance (0-1)
        
        Returns:
            Liste des points détectés
        """
        if not PIL_AVAILABLE or self.image_array is None:
            logger.warning("Impossible de détecter les points - PIL/NumPy non disponibles")
            return []
        
        self.points = []
        
        # Convertir en niveaux de gris
        img_gray = Image.open(self.image_path).convert('L')
        img_array = np.array(img_gray)
        
        # Détecter les bords (Canny edge detection si OpenCV disponible)
        if OPENCV_AVAILABLE:
            edges = cv2.Canny(img_array, 50, 150)
        else:
            # Fallback: Sobel simple
            edges = img_array > 200
        
        # Détecter les points de coin (Harris corners si OpenCV)
        if OPENCV_AVAILABLE:
            corners = cv2.cornerHarris(img_array, 2, 3, 0.04)
            # Normaliser et threshold
            corners = cv2.normalize(corners, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            threshold_val = 200
            corner_points = np.where(corners > threshold_val)
        else:
            # Fallback: détecter les pixels isolés
            corner_points = np.where(edges)
        
        # Créer des points
        for y, x in zip(corner_points[0], corner_points[1]):
            point = Point(
                x=float(x),
                y=float(y),
                type=PointType.VERTEX,
                confidence=threshold,
            )
            self.points.append(point)
        
        logger.info(f"Détecté {len(self.points)} points")
        return self.points
    
    def detect_lines(self) -> List[Line]:
        """Détecte les lignes dans l'image"""
        if not self.image_array is None and OPENCV_AVAILABLE:
            # Utiliser Hough Line Transform
            img_gray = np.array(Image.open(self.image_path).convert('L'))
            edges = cv2.Canny(img_gray, 50, 150)
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
            
            self.lines = []
            if lines is not None:
                for line in lines:
                    rho, theta = line[0]
                    # Convertir en points d'extrémité
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                    pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                    
                    p1 = Point(pt1[0], pt1[1], PointType.ENDPOINT)
                    p2 = Point(pt2[0], pt2[1], PointType.ENDPOINT)
                    
                    detected_line = Line(
                        start=p1,
                        end=p2,
                        type=LineType.STRAIGHT,
                        is_horizontal=abs(a) < 0.1,
                        is_vertical=abs(b) < 0.1,
                        slope=b / a if a != 0 else None,
                    )
                    self.lines.append(detected_line)
                
                logger.info(f"Détecté {len(self.lines)} lignes")
        
        return self.lines
    
    def detect_shapes(self) -> List[Shape]:
        """Détecte les formes géométriques"""
        if not OPENCV_AVAILABLE or self.image_array is None:
            logger.warning("Détection de formes indisponible - OpenCV requis")
            return []
        
        self.shapes = []
        
        # Charge l'image en niveaux de gris
        img_gray = np.array(Image.open(self.image_path).convert('L'))
        edges = cv2.Canny(img_gray, 50, 150)
        
        # Détecte les contours
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            # Approxime le contour
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) >= 3:  # Au moins 3 points
                points = [Point(float(pt[0][0]), float(pt[0][1]), PointType.VERTEX) 
                         for pt in approx]
                
                # Déterminer le type de forme
                if len(approx) == 3:
                    shape_type = "triangle"
                elif len(approx) == 4:
                    shape_type = "rectangle"
                elif len(approx) > 4:
                    # Vérifier si c'est un cercle
                    if cv2.isContourConvex(approx):
                        shape_type = "circle"
                    else:
                        shape_type = "polygon"
                else:
                    continue
                
                # Créer les lignes
                lines = []
                for i in range(len(points)):
                    p1 = points[i]
                    p2 = points[(i + 1) % len(points)]
                    line = Line(
                        start=p1,
                        end=p2,
                        type=LineType.STRAIGHT,
                    )
                    lines.append(line)
                
                shape = Shape(
                    type=shape_type,
                    points=points,
                    lines=lines,
                )
                
                self.shapes.append(shape)
        
        logger.info(f"Détecté {len(self.shapes)} formes")
        return self.shapes
    
    def validate_figure(self) -> Dict[str, Any]:
        """
        Valide la cohérence entre les points et la figure
        
        Returns:
            Dict avec résultats de validation
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'consistency_score': 1.0,
        }
        
        if not self.shapes:
            result['warnings'].append("Aucune forme détectée")
            return result
        
        # Valider chaque forme
        for i, shape in enumerate(self.shapes):
            # Vérifier que tous les points sont cohérents
            for j, point in enumerate(shape.points):
                if point.x < 0 or point.x > self.width or point.y < 0 or point.y > self.height:
                    result['errors'].append(
                        f"Forme {i}, point {j}: coordonnée hors limites"
                    )
                    result['valid'] = False
            
            # Vérifier que les lignes sont cohérentes
            total_length = 0
            for line in shape.lines:
                length = line.length()
                if length < 1:
                    result['warnings'].append(
                        f"Forme {i}: ligne très courte ({length:.2f}px)"
                    )
                total_length += length
            
            # Vérifier l'aire
            area = shape.calculate_area()
            if area < 10:
                result['warnings'].append(
                    f"Forme {i}: aire très petite ({area:.2f}px²)"
                )
        
        if result['warnings']:
            result['consistency_score'] = 0.8
        
        return result
    
    def extract_coordinates(self) -> Dict[str, Any]:
        """Extrait les coordonnées de tous les points et lignes"""
        return {
            'points': [p.to_dict() for p in self.points],
            'lines': [l.to_dict() for l in self.lines],
            'shapes': [s.to_dict() for s in self.shapes],
        }
    
    def generate_python_code(self, shape_index: int = 0) -> str:
        """
        Génère du code Python paramétrique pour une forme
        
        Args:
            shape_index: Index de la forme à générer
        
        Returns:
            Code Python
        """
        if shape_index >= len(self.shapes):
            return "# Aucune forme à générer"
        
        shape = self.shapes[shape_index]
        
        code = f'''"""
Génération paramétrique: {shape.type} (Gabriel Vision)
Auto-généré depuis l'analyse d'image
"""

import matplotlib.pyplot as plt
import numpy as np

# Points détectés
points = {{
'''
        
        for i, point in enumerate(shape.points):
            code += f"    'P{i}': ({point.x:.2f}, {point.y:.2f}),\n"
        
        code += '''}}

# Paramètres géométriques
geometry = {
    'type': '%s',
    'area': %.2f,
    'perimeter': %.2f,
    'center': (%.2f, %.2f),
}

# Visualisation
fig, ax = plt.subplots(figsize=(8, 6))

# Tracer les points
for label, (x, y) in points.items():
    ax.plot(x, y, 'ro', markersize=8)
    ax.text(x, y, f'  {label}', fontsize=10)

# Tracer les lignes
''' % (
            shape.type,
            shape.calculate_area(),
            shape.calculate_perimeter(),
            shape.calculate_center().x,
            shape.calculate_center().y,
        )
        
        for i, line in enumerate(shape.lines):
            code += f"ax.plot([{line.start.x:.2f}, {line.end.x:.2f}], [{line.start.y:.2f}, {line.end.y:.2f}], 'b-')\n"
        
        code += '''
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title(f"{geometry['type']} - Area: {geometry['area']:.2f}, Perimeter: {geometry['perimeter']:.2f}")
plt.show()
'''
        
        return code
    
    def generate_latex_code(self, shape_index: int = 0) -> str:
        """Génère du code LaTeX TikZ pour une forme"""
        if shape_index >= len(self.shapes):
            return "% Aucune forme à générer"
        
        shape = self.shapes[shape_index]
        
        code = r'''
\documentclass{standalone}
\usepackage{tikz}

\begin{document}

\begin{tikzpicture}[scale=0.01]
  % Points
'''
        
        for i, point in enumerate(shape.points):
            code += f"  \\node (P{i}) at ({point.x:.2f}, {point.y:.2f}) {{P{i}}};\n"
        
        code += "  % Lignes\n"
        
        for i, line in enumerate(shape.lines):
            start_idx = shape.points.index(line.start)
            end_idx = shape.points.index(line.end)
            code += f"  \\draw (P{start_idx}) -- (P{end_idx});\n"
        
        code += r'''
\end{tikzpicture}

\end{document}
'''
        
        return code
    
    def generate_hol_code(self, shape_index: int = 0) -> str:
        """Génère du code Isabelle/HOL pour formaliser la forme"""
        if shape_index >= len(self.shapes):
            return "(* Aucune forme à générer *)"
        
        shape = self.shapes[shape_index]
        
        code = f'''(* Formalisation {shape.type} - Gabriel Vision Analysis *)
(* Auto-généré depuis l'analyse d'image *)

theory {shape.type.capitalize()}_Vision
  imports Main
begin

(* Points détectés *)
'''
        
        for i, point in enumerate(shape.points):
            code += f"definition P{i} :: \"real × real\" where \"P{i} = ({point.x:.2f}, {point.y:.2f})\"\n"
        
        code += f'''
(* Géométrie *)
definition {shape.type}_points :: \"(real × real) list\" where
  \"{shape.type}_points = ['''
        
        for i in range(len(shape.points)):
            code += f"P{i}"
            if i < len(shape.points) - 1:
                code += ", "
        
        code += f''']\"

lemma {shape.type}_area:
  \"area_of_{shape.type} = {shape.calculate_area():.2f}\"
  by simp

lemma {shape.type}_perimeter:
  \"perimeter_of_{shape.type} = {shape.calculate_perimeter():.2f}\"
  by simp

end
'''
        
        return code
    
    def analyze_and_report(self) -> str:
        """Génère un rapport complet d'analyse"""
        report = f"""
╭────────────────────────────────────────────────────────────────╮
│          ANALYSE D'IMAGE - GABRIEL VISION MODULE              │
╰────────────────────────────────────────────────────────────────╯

📁 Image: {self.image_path.name}
   Dimensions: {self.width}×{self.height}px
   Format: {self.image.format if self.image else "N/A"}

📊 DÉTECTIONS
   • Points détectés: {len(self.points)}
   • Lignes détectées: {len(self.lines)}
   • Formes détectées: {len(self.shapes)}

🔍 FORMES ANALYSÉES:
"""
        
        for i, shape in enumerate(self.shapes):
            report += f"""
   Forme {i + 1}: {shape.type.upper()}
     - Points: {len(shape.points)}
     - Aire: {shape.calculate_area():.2f}px²
     - Périmètre: {shape.calculate_perimeter():.2f}px
     - Centre: ({shape.calculate_center().x:.2f}, {shape.calculate_center().y:.2f})
"""
        
        validation = self.validate_figure()
        report += f"""
✅ VALIDATION
   Résultat: {'✓ VALIDE' if validation['valid'] else '✗ ERREURS'}
   Score de cohérence: {validation['consistency_score']:.1%}
"""
        
        if validation['errors']:
            report += "   Erreurs:\n"
            for error in validation['errors']:
                report += f"     • {error}\n"
        
        if validation['warnings']:
            report += "   Avertissements:\n"
            for warning in validation['warnings']:
                report += f"     • {warning}\n"
        
        return report


# Singleton global
_vision_analyzer: Optional[ImageVisionAnalyzer] = None


def get_vision_analyzer(image_path: str | Path) -> ImageVisionAnalyzer:
    """Obtient ou crée l'analyseur de vision"""
    global _vision_analyzer
    
    current_path = Path(image_path)
    
    if _vision_analyzer is None or _vision_analyzer.image_path != current_path:
        _vision_analyzer = ImageVisionAnalyzer(image_path)
    
    return _vision_analyzer


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python vision_module.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    try:
        analyzer = ImageVisionAnalyzer(image_path)
        
        # Analyser
        analyzer.detect_points()
        analyzer.detect_lines()
        analyzer.detect_shapes()
        
        # Rapport
        print(analyzer.analyze_and_report())
        
        # Générer du code
        if analyzer.shapes:
            print("\n🐍 CODE PYTHON GÉNÉRÉ:")
            print(analyzer.generate_python_code())
            
            print("\n📐 CODE LATEX GÉNÉRÉ:")
            print(analyzer.generate_latex_code())
            
            print("\n✓ CODE HOL GÉNÉRÉ:")
            print(analyzer.generate_hol_code())
        
        # Exporter les coordonnées
        coords = analyzer.extract_coordinates()
        print(f"\n📍 COORDONNÉES EXTRAITES: {json.dumps(coords, indent=2)}")
        
    except Exception as e:
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
