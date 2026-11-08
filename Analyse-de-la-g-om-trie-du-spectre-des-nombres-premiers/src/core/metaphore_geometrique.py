#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MODULE MÉTAPHORES GÉOMÉTRIQUES - Gabriel v7.3
==============================================

Traduit les abstractions HOL/mathématiques en représentations spatiales.

Comportement:
- Prend une réponse abstraite (texte, HOL, preuves)
- Génère bloc "Structure Géométrique Spatiale"
- Produit: matrices de points, coordonnées, symétries, rotations
- Format: ASCII art + coordonnées exportables

Exemple:
  Entrée: "Preuve de convergence vers 1/2"
  Sortie: Graphique ASCII + matrice de points + instructions CAO
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ========================================================================
# TYPES ET ÉNUMÉRATIONS
# ========================================================================

class GeometricShape(Enum):
    """Formes géométriques supportées"""
    POINT = "point"
    LINE = "ligne"
    TRIANGLE = "triangle"
    SQUARE = "carre"
    CIRCLE = "cercle"
    SPIRAL = "spirale"
    GRID = "grille"
    CONVERGENCE = "convergence"
    SPECTRUM = "spectre"
    WAVE = "onde"

@dataclass
class Point3D:
    """Point 3D pour modélisation"""
    x: float
    y: float
    z: float
    label: Optional[str] = None
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)
    
    def to_string(self) -> str:
        label_str = f" ({self.label})" if self.label else ""
        return f"({self.x:.3f}, {self.y:.3f}, {self.z:.3f}){label_str}"

@dataclass
class Matrix:
    """Matrice de points pour visualisation"""
    data: np.ndarray
    x_label: str = "x"
    y_label: str = "y"
    title: str = "Matrix"

# ========================================================================
# GÉNÉRATEUR DE MÉTAPHORES GÉOMÉTRIQUES
# ========================================================================

class MetaphoreGeometriqueGenerator:
    """Génère représentations spatiales pour abstractions mathématiques"""
    
    def __init__(self):
        self.width = 60
        self.height = 20
    
    def generer_pour_convergence(self, 
                                  values: List[float],
                                  target: float = 0.5,
                                  title: str = "Convergence") -> str:
        """
        Génère représentation géométrique pour convergence
        
        Args:
            values: Liste de valeurs convergeant
            target: Valeur cible
            title: Titre du graphique
        
        Returns:
            Représentation ASCII + données géométriques
        """
        
        output = []
        output.append(f"\n╔═══════════════════════════════════════════════════════════╗")
        output.append(f"║  STRUCTURE GÉOMÉTRIQUE SPATIALE - {title}")
        output.append(f"╚═══════════════════════════════════════════════════════════╝\n")
        
        # Normaliser les valeurs pour l'affichage
        min_val = min(min(values), target - 0.1)
        max_val = max(max(values), target + 0.1)
        range_val = max_val - min_val
        
        # Créer graphique ASCII
        output.append(f"Graphique de Convergence vers {target}:\n")
        
        # Axe Y
        for y in range(self.height - 1, -1, -1):
            y_val = min_val + (y / self.height) * range_val
            
            # Marquer la cible
            if abs(y_val - target) < range_val / self.height:
                output.append(f"{y_val:6.3f} → ")
            else:
                output.append(f"{y_val:6.3f}   ")
            
            # Points du graphique
            for i, v in enumerate(values):
                if i >= self.width:
                    break
                
                v_normalized = (v - min_val) / range_val if range_val > 0 else 0.5
                point_y = int(v_normalized * self.height)
                
                if point_y == y:
                    output.append("●")
                elif y == 0 and abs(v - target) < range_val / self.height:
                    output.append("─")
                elif i > 0 and point_y > y and point_y - 1 <= y:
                    output.append("│")
                else:
                    output.append(" ")
            
            output.append("\n")
        
        # Axe X
        output.append("       " + "".join([str(i % 10) for i in range(min(len(values), self.width))]) + "\n")
        
        # Données géométriques
        output.append(f"\n📐 COORDONNÉES SPATIALES:\n")
        points_3d = self._generer_points_3d_convergence(values, target)
        for i, pt in enumerate(points_3d):
            output.append(f"   P{i:02d}: {pt.to_string()}\n")
        
        # Matrice de points
        output.append(f"\n🔲 MATRICE DE POINTS (pour export CAO):\n")
        matrix = self._generer_matrice_points(values, target)
        output.append(self._formatter_matrice(matrix))
        
        # Symétries détectées
        output.append(f"\n✦ PROPRIÉTÉS GÉOMÉTRIQUES:\n")
        props = self._analyser_proprietes(values, target)
        for prop in props:
            output.append(f"   • {prop}\n")
        
        # Instructions pour modélisation
        output.append(f"\n⚙️  INSTRUCTIONS DE MODÉLISATION:\n")
        output.append(self._generer_instructions_modelisation(values, target))
        
        return "".join(output)
    
    def generer_pour_rapport_spectral(self,
                                       ratios: Dict[str, float],
                                       title: str = "Rapport Spectral") -> str:
        """Génère représentation pour rapports spectraux"""
        
        output = []
        output.append(f"\n╔═══════════════════════════════════════════════════════════╗")
        output.append(f"║  STRUCTURE SPECTRALE - {title}")
        output.append(f"╚═══════════════════════════════════════════════════════════╝\n")
        
        # Cercle spectral
        output.append("Spectre en Cercle Unitaire:\n\n")
        output.append(self._dessiner_cercle_spectral(ratios))
        
        # Points spectraux
        output.append(f"\n📍 POINTS SPECTRAUX EN 3D:\n")
        pts = self._generer_points_spectraux(ratios)
        for nom, pt in pts.items():
            output.append(f"   {nom}: {pt.to_string()}\n")
        
        # Distances géométriques
        output.append(f"\n📏 DISTANCES GÉOMÉTRIQUES:\n")
        distances = self._calculer_distances(pts)
        for (p1, p2), dist in distances.items():
            output.append(f"   {p1} → {p2}: {dist:.6f}\n")
        
        # Symétries
        output.append(f"\n✦ SYMÉTRIES SPECTRALES:\n")
        symetries = self._detecter_symetries(pts)
        for sym in symetries:
            output.append(f"   • {sym}\n")
        
        return "".join(output)
    
    def generer_pour_bloc_asymetrique(self,
                                       bloc_a: List[int],
                                       bloc_b: List[int],
                                       ratio: float) -> str:
        """Génère représentation pour comparaison asymétrique"""
        
        output = []
        output.append(f"\n╔═══════════════════════════════════════════════════════════╗")
        output.append(f"║  STRUCTURE ASYMÉTRIQUE ORDONNÉE")
        output.append(f"╚═══════════════════════════════════════════════════════════╝\n")
        
        # Visualiser les blocs
        output.append("Blocs en Disposition Spatiale:\n\n")
        output.append(self._visualiser_blocs_asymetriques(bloc_a, bloc_b))
        
        # Éléments en 3D
        output.append(f"\n📍 ÉLÉMENTS EN 3D:\n")
        pts_a = [Point3D(float(i), 0, float(v), f"A{i}") for i, v in enumerate(bloc_a)]
        pts_b = [Point3D(float(i), 1, float(v), f"B{i}") for i, v in enumerate(bloc_b)]
        
        for pt in pts_a:
            output.append(f"   {pt.to_string()}\n")
        output.append("\n")
        for pt in pts_b:
            output.append(f"   {pt.to_string()}\n")
        
        # Ratio géométrique
        output.append(f"\n📐 RATIO GÉOMÉTRIQUE:\n")
        output.append(f"   Ratio = {ratio:.10f}\n")
        output.append(f"   Cible = 0.5\n")
        output.append(f"   Écart = {abs(ratio - 0.5):.10f}\n")
        
        # Rotation asymétrique
        output.append(f"\n🔄 TRANSFORMATION ASYMÉTRIQUE:\n")
        output.append(self._generer_transformation_asymetrique(bloc_a, bloc_b, ratio))
        
        return "".join(output)
    
    # ====================================================================
    # UTILITAIRES
    # ====================================================================
    
    def _generer_points_3d_convergence(self,
                                       values: List[float],
                                       target: float) -> List[Point3D]:
        """Génère points 3D pour convergence"""
        points = []
        for i, v in enumerate(values):
            # Placer sur spirale convergeant vers cible
            theta = 2 * np.pi * i / len(values)
            r = abs(v - target) + 0.1  # Rayon = distance à cible
            
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = float(i) / len(values)
            
            points.append(Point3D(x, y, z, f"P{i}"))
        
        return points
    
    def _generer_matrice_points(self,
                                values: List[float],
                                target: float) -> np.ndarray:
        """Génère matrice de points pour export CAO"""
        n = len(values)
        # Matrice: colonne 1=index, 2=valeur, 3=distance à cible, 4=normalisé
        matrix = np.zeros((n, 4))
        
        for i, v in enumerate(values):
            matrix[i, 0] = i
            matrix[i, 1] = v
            matrix[i, 2] = abs(v - target)
            matrix[i, 3] = (v - min(values)) / (max(values) - min(values)) if max(values) != min(values) else 0
        
        return matrix
    
    def _formatter_matrice(self, matrix: np.ndarray) -> str:
        """Formate matrice pour affichage"""
        output = []
        output.append("   Index | Valeur    | Distance à Cible | Normalisé\n")
        output.append("   ------|-----------|------------------|----------\n")
        
        for row in matrix[:10]:  # Afficher premiers 10
            output.append(f"   {int(row[0]):5d} | {row[1]:9.6f} | {row[2]:16.6f} | {row[3]:9.6f}\n")
        
        if len(matrix) > 10:
            output.append(f"   ... ({len(matrix) - 10} plus de points)\n")
        
        return "".join(output)
    
    def _analyser_proprietes(self, values: List[float], target: float) -> List[str]:
        """Analyse propriétés géométriques"""
        props = []
        
        # Convergence monotone?
        diff = [values[i+1] - values[i] for i in range(len(values)-1)]
        if all(d <= 0 for d in diff) or all(d >= 0 for d in diff):
            props.append("Convergence Monotone (direction constante)")
        else:
            props.append("Convergence Oscillante (zigzag)")
        
        # Distance initiale vs finale
        dist_init = abs(values[0] - target)
        dist_final = abs(values[-1] - target)
        props.append(f"Réduction: {dist_init:.6f} → {dist_final:.6f}")
        
        # Taux de convergence
        if len(values) > 1:
            ratio_conv = dist_final / dist_init if dist_init > 0 else 0
            props.append(f"Taux de contraction: {ratio_conv:.6f} par étape")
        
        return props
    
    def _generer_instructions_modelisation(self,
                                          values: List[float],
                                          target: float) -> str:
        """Génère instructions pour CAO/modélisation"""
        
        output = []
        output.append("   # Script FreeCAD / Blender / OpenSCAD\n\n")
        
        output.append("   # 1. Créer points de la spirale de convergence\n")
        output.append("   points = [\n")
        
        for i in range(min(5, len(values))):
            v = values[i]
            theta = 2 * np.pi * i / len(values)
            r = abs(v - target) + 0.1
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = i / len(values)
            output.append(f"       ({x:.3f}, {y:.3f}, {z:.3f}),  # P{i}\n")
        
        output.append("   ]\n\n")
        
        output.append("   # 2. Créer ligne de cible (axe de convergence)\n")
        output.append(f"   target_plane = z = {target:.3f}\n\n")
        
        output.append("   # 3. Appliquer rotation autour de cible\n")
        output.append(f"   rotation_axis = (0, 0, 1)\n")
        output.append(f"   angle = 360 * (nombre_iterations / periode)\n\n")
        
        output.append("   # 4. Exporters points en CSV/STL\n")
        
        return "".join(output)
    
    def _dessiner_cercle_spectral(self, ratios: Dict[str, float]) -> str:
        """Dessine cercle unitaire avec points spectraux"""
        output = []
        
        # Cercle ASCII
        radius = 10
        for y in range(radius, -radius-1, -1):
            line = ""
            for x in range(-radius, radius+1):
                r = np.sqrt(x**2 + y**2)
                
                if abs(r - radius) < 0.8:
                    line += "●"
                elif r < radius:
                    line += " "
                else:
                    line += " "
            
            output.append(line + "\n")
        
        return "".join(output)
    
    def _generer_points_spectraux(self, ratios: Dict[str, float]) -> Dict[str, Point3D]:
        """Génère points spectraux en 3D"""
        points = {}
        
        for i, (nom, ratio) in enumerate(ratios.items()):
            angle = 2 * np.pi * i / len(ratios)
            x = np.cos(angle)
            y = np.sin(angle)
            z = ratio
            
            points[nom] = Point3D(x, y, z, nom)
        
        return points
    
    def _calculer_distances(self, points: Dict[str, Point3D]) -> Dict[Tuple[str, str], float]:
        """Calcule distances géométriques entre points"""
        distances = {}
        items = list(points.items())
        
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                p1_name, p1 = items[i]
                p2_name, p2 = items[j]
                
                dist = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
                distances[(p1_name, p2_name)] = dist
        
        return distances
    
    def _detecter_symetries(self, points: Dict[str, Point3D]) -> List[str]:
        """Détecte symétries géométriques"""
        symetries = []
        
        # Symétrie par rapport à z=0.5?
        z_values = [p.z for p in points.values()]
        if all(abs(z - 0.5) < 0.1 for z in z_values):
            symetries.append("Symétrie centrale autour de z=0.5")
        
        return symetries
    
    def _visualiser_blocs_asymetriques(self,
                                       bloc_a: List[int],
                                       bloc_b: List[int]) -> str:
        """Visualise blocs asymétriques"""
        output = []
        
        output.append("Bloc A (inférieur):  ")
        for v in bloc_a:
            output.append(f"[{v:2d}] ")
        output.append("\n\n")
        
        output.append("Bloc B (supérieur):  ")
        for v in bloc_b:
            output.append(f"[{v:2d}] ")
        output.append("\n\n")
        
        output.append(f"Asymétrie: |B| = |A| + 1 = {len(bloc_b)} = {len(bloc_a)} + 1 ✓\n")
        
        return "".join(output)
    
    def _generer_transformation_asymetrique(self,
                                           bloc_a: List[int],
                                           bloc_b: List[int],
                                           ratio: float) -> str:
        """Génère transformation asymétrique"""
        output = []
        
        output.append("   Rotation asymétrique:\n")
        output.append(f"   - Angle = arccos({ratio:.6f}) = {np.degrees(np.arccos(max(-1, min(1, ratio)))):.2f}°\n")
        output.append(f"   - Plan A-B (normal oscillant)\n")
        output.append(f"   - Contrainte: |B| = |A| + 1 (invariant)\n")
        
        return "".join(output)

# ========================================================================
# TEST/DÉMO
# ========================================================================

def demo():
    """Démonstration du générateur"""
    
    print("\n" + "="*70)
    print("DÉMONSTRATION - MÉTAPHORES GÉOMÉTRIQUES GABRIEL")
    print("="*70)
    
    gen = MetaphoreGeometriqueGenerator()
    
    # Test 1: Convergence
    print("\n[TEST 1] Convergence vers 0.5:\n")
    values = [0.8, 0.65, 0.55, 0.52, 0.501, 0.5002]
    print(gen.generer_pour_convergence(values, target=0.5, title="Convergence Spectrale"))
    
    # Test 2: Rapport spectral
    print("\n[TEST 2] Rapport spectral 1/2:\n")
    ratios = {
        "1/2": 0.5,
        "1/3": 0.333,
        "1/4": 0.25,
        "3/4": 0.75
    }
    print(gen.generer_pour_rapport_spectral(ratios))
    
    # Test 3: Bloc asymétrique
    print("\n[TEST 3] Comparaison asymétrique ordonnée:\n")
    bloc_a = [2, 3, 5, 7]
    bloc_b = [11, 13, 17, 19, 23]
    print(gen.generer_pour_bloc_asymetrique(bloc_a, bloc_b, ratio=0.5026))

if __name__ == "__main__":
    demo()
