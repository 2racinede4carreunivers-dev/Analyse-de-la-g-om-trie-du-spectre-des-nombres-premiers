#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WRAPPER GABRIEL - INTÉGRATION MÉTAPHORES GÉOMÉTRIQUES
=====================================================

Ajoute automatiquement un bloc "Structure Géométrique Spatiale" 
à chaque réponse de Gabriel.
"""

import re
from typing import Dict, Any, Optional
from src.core.metaphore_geometrique import MetaphoreGeometriqueGenerator, Point3D

class GabrielGeometricResponseWrapper:
    """Wrapper pour ajouter métaphores géométriques aux réponses"""
    
    def __init__(self):
        self.geo_gen = MetaphoreGeometriqueGenerator()
        self.response_history = []
    
    def enrichir_reponse(self, 
                        reponse_originale: str,
                        contexte: Optional[Dict[str, Any]] = None) -> str:
        """
        Ajoute bloc géométrique à une réponse
        
        Args:
            reponse_originale: Réponse de Gabriel (texte/code/HOL)
            contexte: Info sur le type de requête (convergence, spectral, etc.)
        
        Returns:
            Réponse enrichie avec bloc géométrique
        """
        
        output = reponse_originale
        
        # Détecter le type de réponse automatiquement
        contexte_detecte = self._detecter_contexte(reponse_originale)
        
        # Générer bloc géométrique approprié
        bloc_geo = self._generer_bloc_geometrique(contexte_detecte or contexte)
        
        # Ajouter le bloc
        if bloc_geo:
            output += "\n" + bloc_geo
        
        return output
    
    def _detecter_contexte(self, texte: str) -> Optional[Dict[str, Any]]:
        """Détecte automatiquement le type de réponse"""
        
        texte_lower = texte.lower()
        
        # Détection: Convergence
        if any(kw in texte_lower for kw in ["convergence", "converge", "converger", "tend vers", "asymptote"]):
            # Extraire les valeurs numériques
            values = re.findall(r'0\.\d+', texte)
            if values:
                try:
                    values_float = [float(v) for v in values[:10]]  # Prendre les 10 premiers
                    return {
                        'type': 'convergence',
                        'values': values_float,
                        'target': 0.5
                    }
                except:
                    pass
        
        # Détection: Rapport spectral
        if any(kw in texte_lower for kw in ["rapport spectral", "1/2", "1/3", "1/4", "spectre"]):
            return {'type': 'spectral', 'ratios': {'1/2': 0.5, '1/3': 0.333, '1/4': 0.25}}
        
        # Détection: Comparaison asymétrique
        if any(kw in texte_lower for kw in ["comparaison asymétrique", "bloc A", "bloc B", "asymétrique ordonnée"]):
            return {
                'type': 'asym_ordonnee',
                'bloc_a': [2, 3, 5, 7],
                'bloc_b': [11, 13, 17, 19, 23],
                'ratio': 0.5026
            }
        
        return None
    
    def _generer_bloc_geometrique(self, contexte: Optional[Dict]) -> Optional[str]:
        """Génère bloc géométrique selon contexte"""
        
        if not contexte:
            return None
        
        contexte_type = contexte.get('type')
        
        if contexte_type == 'convergence':
            values = contexte.get('values', [0.8, 0.65, 0.55, 0.52, 0.501])
            target = contexte.get('target', 0.5)
            return self.geo_gen.generer_pour_convergence(
                values, 
                target=target,
                title="Convergence Analysée"
            )
        
        elif contexte_type == 'spectral':
            ratios = contexte.get('ratios', {'1/2': 0.5})
            return self.geo_gen.generer_pour_rapport_spectral(
                ratios,
                title="Spectre Analyisé"
            )
        
        elif contexte_type == 'asym_ordonnee':
            bloc_a = contexte.get('bloc_a', [2, 3, 5, 7])
            bloc_b = contexte.get('bloc_b', [11, 13, 17, 19, 23])
            ratio = contexte.get('ratio', 0.5026)
            return self.geo_gen.generer_pour_bloc_asymetrique(
                bloc_a, 
                bloc_b, 
                ratio
            )
        
        return None
    
    def creer_structure_exportable(self,
                                  reponse: str,
                                  contexte: Dict) -> Dict[str, Any]:
        """
        Crée structure exportable vers CAO/modélisation
        
        Retourne format exploitable par FreeCAD, Blender, OpenSCAD
        """
        
        export = {
            'texte': reponse,
            'geometrie': [],
            'points_3d': [],
            'matrices': [],
            'instructions_cad': []
        }
        
        # Extraire points 3D
        points_3d = re.findall(
            r'\([-\d.]+,\s*[-\d.]+,\s*[-\d.]+\)',
            reponse
        )
        
        for pt_str in points_3d:
            coords = re.findall(r'[-\d.]+', pt_str)
            if len(coords) == 3:
                pt = Point3D(float(coords[0]), float(coords[1]), float(coords[2]))
                export['points_3d'].append(pt.to_tuple())
        
        # Générer instructions CAO
        if contexte.get('type') == 'convergence':
            export['instructions_cad'].append("""
# FreeCAD Script
import FreeCAD as App
import Part

# Créer points de convergence
points = """ + str(export['points_3d']) + """

# Créer polyline
pl = Part.makePolygon(points)
App.ActiveDocument.addObject("Part::Feature", "ConvergencePath").Shape = pl
""")
        
        return export

# ========================================================================
# INTÉGRATION DANS GABRIEL
# ========================================================================

def enrichir_reponse_gabriel(reponse: str, contexte: Optional[Dict] = None) -> str:
    """
    Fonction à appeler dans le pipeline multiloop de Gabriel
    
    Exemple d'utilisation dans integrateur_memoire.py:
    
        response = await llm_router.route_request(question)
        
        # Enrichir avec métaphores géométriques
        response_enrichie = enrichir_reponse_gabriel(response, contexte)
        
        return response_enrichie
    """
    
    wrapper = GabrielGeometricResponseWrapper()
    return wrapper.enrichir_reponse(reponse, contexte)

# ========================================================================
# TEST
# ========================================================================

if __name__ == "__main__":
    wrapper = GabrielGeometricResponseWrapper()
    
    # Test 1: Enrichir une réponse sur convergence
    print("\n[TEST] Enrichissement d'une réponse sur convergence:\n")
    reponse_test = """
    Le ratio converge vers 1/2:
    - k=1: 0.625
    - k=2: 0.552
    - k=3: 0.501
    - k=4: 0.5001
    """
    
    reponse_enrichie = wrapper.enrichir_reponse(reponse_test)
    print(reponse_enrichie)
    
    # Test 2: Créer export CAO
    print("\n[TEST] Export CAO:\n")
    export = wrapper.creer_structure_exportable(
        reponse_enrichie,
        {'type': 'convergence'}
    )
    
    print("Points 3D extraits:")
    for pt in export['points_3d']:
        print(f"  {pt}")
    
    print("\nInstructions CAO:")
    for instr in export['instructions_cad']:
        print(instr[:200] + "...")
