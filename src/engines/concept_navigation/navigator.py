"""
Moteur de Navigation Conceptuelle.
Graphe de concepts du corpus Savard, permet de relier des concepts eloignes.
"""
from __future__ import annotations

from typing import Any

import networkx as nx


# Concepts et liens (issus du corpus methode_spectral.thy)
CONCEPT_EDGES: list[tuple[str, str, str]] = [
    # noeud A, noeud B, relation
    ("SA", "SB", "affine: SB = 2*SA - 62"),
    ("SA", "RsP", "numerator"),
    ("SB", "RsP", "denominator"),
    ("RsP", "1/2", "yields constant"),
    ("SB", "digamma_calc", "subtractant"),
    ("digamma_calc", "prime_equation", "input"),
    ("prime_equation", "premier_p", "outputs"),
    ("A_1_3", "B_1_3", "pair_1_3"),
    ("A_1_4", "B_1_4", "pair_1_4"),
    ("RsP_1_3", "1/3", "yields constant"),
    ("RsP_1_4", "1/4", "yields constant"),
    ("gap_equation_1_3", "premier_p", "computes gap"),
    ("gap_equation_1_4", "premier_p", "computes gap"),
    ("asymetrie_ordonnee", "RsP", "configuration"),
    ("asymetrie_chaotique", "RsP", "configuration"),
    ("suites_mixtes", "gap", "covers (-,+)"),
    ("suites_negatives", "gap", "covers (-,-)"),
    ("plan_trifocal", "FZg", "axe_1"),
    ("plan_trifocal", "HyRi", "axe_2"),
    ("plan_trifocal", "MsP", "axe_3"),
    ("HyRi", "Riemann", "hypothese"),
    ("FZg", "zeta", "fonction"),
    ("MsP", "RsP", "methode"),
    ("HypR_demi_solFinal", "Riemann", "geometric_condition"),
    ("Aire_parab", "T_restant_area", "geometric_equality"),
]


class ConceptGraph:
    """Graphe de concepts du corpus."""

    def __init__(self):
        self.graph = nx.DiGraph()
        for a, b, rel in CONCEPT_EDGES:
            self.graph.add_edge(a, b, relation=rel)

    def neighbors(self, concept: str) -> list[str]:
        if concept not in self.graph:
            return []
        return list(self.graph.successors(concept)) + list(self.graph.predecessors(concept))

    def path(self, source: str, target: str) -> list[str]:
        try:
            return nx.shortest_path(self.graph.to_undirected(), source, target)
        except (nx.NodeNotFound, nx.NetworkXNoPath):
            return []

    def all_concepts(self) -> list[str]:
        return list(self.graph.nodes())


class Navigator:
    """Navigation conceptuelle : etend le contexte d'une question."""

    def __init__(self):
        self.graph = ConceptGraph()

    def expand_concepts(self, concept_names: list[str]) -> list[str]:
        """Pour chaque concept fourni, ajoute ses voisins."""
        expanded = set(concept_names)
        for c in concept_names:
            expanded.update(self.graph.neighbors(c))
        return sorted(expanded)

    def find_path_to_riemann(self, from_concept: str) -> list[str]:
        return self.graph.path(from_concept, "Riemann")
