#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GÉNÉRATEUR DE SCHÉMAS ET FIGURES - Gabriel v7.4
================================================

Crée des schémas/figures rudimentaires en ASCII art avancé
avec la même qualité de présentation que les graphiques.

Supporte:
- Diagrammes de flux
- Arbres (HOL proofs, structures)
- Matrices et grilles
- Graphes et réseaux
- Circuits logiques
- Organigrammes
"""

from typing import List, Dict, Tuple, Optional
from enum import Enum
import math

# ========================================================================
# TYPES DE SCHÉMAS
# ========================================================================

class SchemaType(Enum):
    """Types de schémas supportés"""
    FLOWCHART = "organigramme"
    TREE = "arbre"
    MATRIX = "matrice"
    GRAPH = "graphe"
    CIRCUIT = "circuit"
    PYRAMID = "pyramide"
    NETWORK = "réseau"
    LOGIC_GATE = "porte_logique"
    STATE_DIAGRAM = "automate"

# ========================================================================
# GÉNÉRATEUR DE SCHÉMAS
# ========================================================================

class GenerateurSchemasAvances:
    """Génère schémas rudimentaires de qualité professionnelle"""
    
    def __init__(self):
        self.width = 80
        self.height = 30
    
    # ====================================================================
    # ORGANIGRAMMES (FLOWCHARTS)
    # ====================================================================
    
    def generer_flowchart(self, 
                         etapes: List[str],
                         decisions: Optional[List[Tuple[str, str, str]]] = None) -> str:
        """
        Génère un organigramme
        
        Args:
            etapes: Liste des étapes
            decisions: Liste de (condition, branche_oui, branche_non)
        
        Returns:
            Schéma ASCII du flowchart
        """
        
        output = []
        output.append("\n╔════════════════════════════════════════════════════════════════╗")
        output.append("║  ORGANIGRAMME - PROCESSUS")
        output.append("╚════════════════════════════════════════════════════════════════╝\n")
        
        # Début
        output.append("              ┌─────────────┐\n")
        output.append("              │   DÉBUT     │\n")
        output.append("              └──────┬──────┘\n")
        output.append("                     │\n")
        
        # Étapes
        for i, etape in enumerate(etapes):
            output.append("              ┌─────────────────┐\n")
            output.append(f"              │ {etape[:13]:13s} │\n")
            output.append("              └────────┬────────┘\n")
            
            if i < len(etapes) - 1:
                output.append("                       │\n")
        
        # Fin
        output.append("              ┌─────────────┐\n")
        output.append("              │    FIN      │\n")
        output.append("              └─────────────┘\n")
        
        # Décisions
        if decisions:
            output.append("\n┌─ DÉCISIONS ─────────────────────────┐\n")
            for condition, oui, non in decisions:
                output.append(f"\n  Si {condition}:\n")
                output.append(f"    ✓ OUI  → {oui}\n")
                output.append(f"    ✗ NON  → {non}\n")
            output.append("\n└──────────────────────────────────────┘\n")
        
        return "".join(output)
    
    # ====================================================================
    # ARBRES (TREES - HOL PROOFS, STRUCTURES)
    # ====================================================================
    
    def generer_arbre_binaire(self, 
                             valeurs: List[int],
                             titre: str = "Arbre Binaire") -> str:
        """Génère arbre binaire"""
        
        output = []
        output.append(f"\n╔════════════════════════════════════════════════════════════════╗")
        output.append(f"║  {titre}")
        output.append(f"╚════════════════════════════════════════════════════════════════╝\n")
        
        if not valeurs:
            return "".join(output) + "Arbre vide\n"
        
        # Construire arbre
        arbre = self._construire_arbre_binaire(valeurs)
        output.append(self._afficher_arbre_binaire(arbre))
        
        return "".join(output)
    
    def _construire_arbre_binaire(self, valeurs: List[int]) -> Dict:
        """Construit structure arbre binaire"""
        if not valeurs:
            return None
        
        root = {'val': valeurs[0], 'gauche': None, 'droit': None}
        
        for val in valeurs[1:]:
            self._inserer_arbre(root, val)
        
        return root
    
    def _inserer_arbre(self, node: Dict, val: int):
        """Insère valeur dans arbre binaire"""
        if val < node['val']:
            if node['gauche'] is None:
                node['gauche'] = {'val': val, 'gauche': None, 'droit': None}
            else:
                self._inserer_arbre(node['gauche'], val)
        else:
            if node['droit'] is None:
                node['droit'] = {'val': val, 'gauche': None, 'droit': None}
            else:
                self._inserer_arbre(node['droit'], val)
    
    def _afficher_arbre_binaire(self, node: Dict, prefix: str = "", est_gauche: Optional[bool] = None) -> str:
        """Affiche arbre en ASCII"""
        
        if node is None:
            return ""
        
        output = []
        
        # Nœud courant
        if est_gauche is None:
            output.append(f"        {node['val']}\n")
        elif est_gauche:
            output.append(f"{prefix}├─── {node['val']}\n")
        else:
            output.append(f"{prefix}└─── {node['val']}\n")
        
        # Enfants
        enfants = [node['gauche'], node['droit']]
        prefixes = ["│   ", "    "]
        
        for i, enfant in enumerate(enfants):
            if enfant:
                new_prefix = prefix + prefixes[i]
                output.append(self._afficher_arbre_binaire(enfant, new_prefix, i == 0))
        
        return "".join(output)
    
    # ====================================================================
    # MATRICES ET GRILLES
    # ====================================================================
    
    def generer_matrice_visuelle(self,
                                matrice: List[List[float]],
                                titre: str = "Matrice") -> str:
        """Génère matrice avec bordures"""
        
        output = []
        output.append(f"\n╔════════════════════════════════════════════════════════════════╗")
        output.append(f"║  {titre}")
        output.append(f"╚════════════════════════════════════════════════════════════════╝\n")
        
        rows = len(matrice)
        cols = len(matrice[0]) if rows > 0 else 0
        
        # En-tête
        output.append("    ")
        for j in range(cols):
            output.append(f"  C{j:2d}  ")
        output.append("\n")
        
        # Séparateur
        output.append("  ┌" + "─" * (cols * 7) + "┐\n")
        
        # Rows
        for i, row in enumerate(matrice):
            output.append(f"R{i:2d}│ ")
            for val in row:
                output.append(f"{val:6.2f} ")
            output.append("│\n")
        
        # Séparateur bas
        output.append("  └" + "─" * (cols * 7) + "┘\n")
        
        return "".join(output)
    
    # ====================================================================
    # GRAPHES ET RÉSEAUX
    # ====================================================================
    
    def generer_graphe_connexions(self,
                                 nœuds: List[str],
                                 connexions: List[Tuple[str, str]],
                                 titre: str = "Graphe de Connexions") -> str:
        """Génère graphe de connexions"""
        
        output = []
        output.append(f"\n╔════════════════════════════════════════════════════════════════╗")
        output.append(f"║  {titre}")
        output.append(f"╚════════════════════════════════════════════════════════════════╝\n")
        
        # Afficher nœuds
        output.append("NŒUDS:\n")
        for i, nœud in enumerate(nœuds):
            output.append(f"  {i}. [{nœud}]\n")
        
        # Afficher connexions
        output.append("\nCONNEXIONS:\n")
        for src, dst in connexions:
            output.append(f"  {src} ──→ {dst}\n")
        
        # Visualisation matricielle
        output.append("\nMATRICE D'ADJACENCE:\n")
        
        nœud_idx = {nœud: i for i, nœud in enumerate(nœuds)}
        n = len(nœuds)
        
        # En-tête
        output.append("    ")
        for nœud in nœuds:
            output.append(f"{nœud[:4]:4s} ")
        output.append("\n")
        
        # Matrice
        adj = [[0] * n for _ in range(n)]
        for src, dst in connexions:
            if src in nœud_idx and dst in nœud_idx:
                adj[nœud_idx[src]][nœud_idx[dst]] = 1
        
        for i, nœud in enumerate(nœuds):
            output.append(f"{nœud[:4]:4s} ")
            for j in range(n):
                output.append(f"  {adj[i][j]}   ")
            output.append("\n")
        
        return "".join(output)
    
    # ====================================================================
    # CIRCUITS LOGIQUES
    # ====================================================================
    
    def generer_circuit_logique(self,
                               portes: List[Dict],
                               titre: str = "Circuit Logique") -> str:
        """Génère schéma circuit logique"""
        
        output = []
        output.append(f"\n╔════════════════════════════════════════════════════════════════╗")
        output.append(f"║  {titre}")
        output.append(f"╚════════════════════════════════════════════════════════════════╝\n")
        
        output.append("PORTES:\n")
        for i, porte in enumerate(portes):
            type_porte = porte.get('type', 'AND')
            entrees = porte.get('entrees', [])
            sortie = porte.get('sortie', '')
            
            output.append(f"\n  Porte {i}: {type_porte}\n")
            output.append(f"    Entrées: {entrees}\n")
            output.append(f"    Sortie: {sortie}\n")
        
        # Schéma ASCII
        output.append("\nSCHÉMA:\n\n")
        output.append("  A ──┐\n")
        output.append("      ├─ AND ──┐\n")
        output.append("  B ──┘       │\n")
        output.append("              ├─ OR ── OUT\n")
        output.append("  C ──┐       │\n")
        output.append("      ├─ NOT ─┘\n")
        output.append("  D ──┘\n")
        
        return "".join(output)
    
    # ====================================================================
    # AUTOMATES D'ÉTATS
    # ====================================================================
    
    def generer_automate_etats(self,
                               etats: List[str],
                               transitions: List[Tuple[str, str, str]],
                               etat_initial: str,
                               etats_finaux: List[str],
                               titre: str = "Automate") -> str:
        """Génère automate d'états"""
        
        output = []
        output.append(f"\n╔════════════════════════════════════════════════════════════════╗")
        output.append(f"║  {titre}")
        output.append(f"╚════════════════════════════════════════════════════════════════╝\n")
        
        output.append("ÉTATS:\n")
        for etat in etats:
            if etat == etat_initial:
                output.append(f"  → {etat} (INITIAL)\n")
            elif etat in etats_finaux:
                output.append(f"  ◉ {etat} (FINAL)\n")
            else:
                output.append(f"  ○ {etat}\n")
        
        output.append("\nTRANSITIONS:\n")
        for src, condition, dst in transitions:
            output.append(f"  {src} --[{condition}]--> {dst}\n")
        
        # Visualisation
        output.append("\nDIAGRAMME:\n\n")
        output.append("       ┌─ INITIAL\n")
        output.append("       ↓\n")
        
        for i, etat in enumerate(etats):
            if etat == etat_initial:
                output.append(f"      ┌─────┐\n")
                output.append(f"  ┌──→│{etat:5s}│\n")
                output.append(f"  │   └─────┘\n")
        
        return "".join(output)
    
    # ====================================================================
    # PYRAMIDES ET HIÉRARCHIES
    # ====================================================================
    
    def generer_pyramide(self,
                        niveaux: List[List[str]],
                        titre: str = "Hiérarchie Pyramidale") -> str:
        """Génère pyramide hiérarchique"""
        
        output = []
        output.append(f"\n╔════════════════════════════════════════════════════════════════╗")
        output.append(f"║  {titre}")
        output.append(f"╚════════════════════════════════════════════════════════════════╝\n")
        
        max_width = max(len(niveau) for niveau in niveaux)
        
        for i, niveau in enumerate(niveaux):
            # Centrer
            spacing = " " * ((max_width - len(niveau)) * 4)
            output.append(spacing)
            
            # Afficher éléments du niveau
            for j, elem in enumerate(niveau):
                output.append(f"┌─ {elem[:8]:8s} ─┐")
                if j < len(niveau) - 1:
                    output.append("  ")
            
            output.append("\n")
            
            # Connexions vers niveau suivant
            if i < len(niveaux) - 1:
                output.append(spacing)
                for j in range(len(niveau)):
                    output.append("└───────┘  ")
                output.append("\n")
        
        return "".join(output)

# ========================================================================
# TEST/DÉMO
# ========================================================================

def demo():
    """Démonstration"""
    
    print("\n" + "="*70)
    print("DÉMONSTRATION - SCHÉMAS ET FIGURES AVANCÉS")
    print("="*70)
    
    gen = GenerateurSchemasAvances()
    
    # Test 1: Flowchart
    print(gen.generer_flowchart(
        ["Initialiser", "Calculer", "Valider"],
        [("Résultat > 0.5?", "Accepter", "Rejeter")]
    ))
    
    # Test 2: Arbre
    print(gen.generer_arbre_binaire([4, 2, 6, 1, 3, 5, 7], "Arbre BST"))
    
    # Test 3: Matrice
    print(gen.generer_matrice_visuelle(
        [[1.5, 2.3, 3.1], [4.2, 5.6, 6.9], [7.1, 8.4, 9.8]],
        "Matrice 3x3"
    ))
    
    # Test 4: Graphe
    print(gen.generer_graphe_connexions(
        ["A", "B", "C", "D"],
        [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")],
        "Réseau de Calcul"
    ))
    
    # Test 5: Circuit
    print(gen.generer_circuit_logique(
        [
            {"type": "AND", "entrees": ["A", "B"], "sortie": "X"},
            {"type": "OR", "entrees": ["X", "C"], "sortie": "OUT"}
        ],
        "Circuit Combinatoire"
    ))
    
    # Test 6: Automate
    print(gen.generer_automate_etats(
        ["Q0", "Q1", "Q2"],
        [("Q0", "0", "Q1"), ("Q1", "1", "Q2"), ("Q2", "0", "Q0")],
        "Q0",
        ["Q2"],
        "Automate Fini"
    ))

if __name__ == "__main__":
    demo()
