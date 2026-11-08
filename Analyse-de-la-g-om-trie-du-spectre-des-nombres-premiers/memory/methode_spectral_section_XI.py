"""Section XI - Suites A_i et B_i (8+ termes) - rapport spectral 1/k_i.

Ce module integre les regles de la Section XI de methode_spectral.thy
dans le Dictionnaire Spectral RAG de Gabriel, sous forme d'entrees
ontologiques injectables dans les prompts LLM.

Source : methode_spectral_section_XI.thy (formalisation Isabelle/HOL).
Auteur regles : Philippe Savard.
"""
from __future__ import annotations
from typing import Any


SECTION_XI_TITLE = "XI. Suites A_i et B_i (8+ termes) - construction et formules"

SECTION_XI_REGLES: list[dict[str, Any]] = [
    {
        "code": "XI.1",
        "nom": "tailles_egales",
        "regle": "Les suites A_i et B_i doivent avoir la meme quantite de termes : TSA_i = TSB_i.",
        "domaine_validite": "toutes tailles n >= 1",
    },
    {
        "code": "XI.2",
        "nom": "progression_simple",
        "regle": "Pour positions 1 a n-2 : chaque terme a_(i+1) = a_i * (x2/x1). Soit r=x2/x1, alors a_i = a_1 * r^(i-1).",
        "domaine_validite": "toutes tailles, positions 1..n-2",
    },
    {
        "code": "XI.3",
        "nom": "avant_dernier_terme",
        "regle": "Position n-1 (avant-dernier) = a_(n-2) * (r - 1/r), ou a_(n-2) est le terme precedant l'avant-dernier.",
        "domaine_validite": "n >= 3",
    },
    {
        "code": "XI.4",
        "nom": "dernier_terme",
        "regle": "Position n (dernier) = avant_dernier * (x2/x1) = avant_dernier * r.",
        "domaine_validite": "n >= 3",
    },
    {
        "code": "XI.5",
        "nom": "substitution_position_6_suite_B",
        "regle": "UNIQUEMENT pour suites B de 8+ termes : la position 6 de B prend la valeur de la position 7 de A. Effet : B saute l'exposant 6.",
        "domaine_validite": "suites B, n >= 8",
    },
    {
        "code": "XI.6",
        "nom": "formule_fermee_somme_A",
        "regle": "Pour A_i positif : Somme(A) = (3.25/2) * (x2/x1)^n_j - 2, ou n_j est le nombre total de termes.",
        "constante_savard_a": 3.25 / 2,
        "constante_savard_b": -2,
        "domaine_validite": "A_i positif",
    },
    {
        "code": "XI.7",
        "nom": "formule_fermee_somme_B",
        "regle": "Pour B_i positif : Somme(B) = (6.5/2) * (x2/x1)^n_j - 66.",
        "constante_savard_a": 6.5 / 2,
        "constante_savard_b": -66,
        "domaine_validite": "B_i positif",
    },
    {
        "code": "XI.8",
        "nom": "rapport_spectral_resultant",
        "regle": "RsP(A,B) = Somme(A) / Somme(B) = (3.25*r^n - 4) / (6.5*r^n - 132). Tend vers 1/2 quand n grand.",
        "domaine_validite": "n >= 8, A et B positifs",
    },
]


def get_section_XI_entries() -> list[dict[str, Any]]:
    """Retourne les regles de la Section XI sous forme d'entrees pour le
    Dictionnaire Spectral RAG (consommable par adaptateur_cognitif_rag.py)."""
    return [
        {
            "id": f"section_XI_{r['code']}",
            "titre": f"Section XI / {r['code']} - {r['nom']}",
            "contenu": r["regle"],
            "metadata": {
                "section": "XI",
                "code": r["code"],
                "domaine_validite": r["domaine_validite"],
                "source_thy": "methode_spectral_section_XI.thy",
            },
        }
        for r in SECTION_XI_REGLES
    ]


def render_section_XI_summary() -> str:
    """Resume textuel pour injection dans un prompt LLM."""
    lines = [f"=== {SECTION_XI_TITLE} ==="]
    for r in SECTION_XI_REGLES:
        lines.append(f"\n[{r['code']}] {r['nom']} ({r['domaine_validite']}):")
        lines.append(f"  {r['regle']}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Apercu rapide
    print(render_section_XI_summary())
    print(f"\n{len(get_section_XI_entries())} entrees RAG generees.")
