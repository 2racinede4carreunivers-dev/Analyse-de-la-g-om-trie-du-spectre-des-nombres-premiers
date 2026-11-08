"""generateur_question_modeste.py - Construit une question plus modeste.

A partir des associations lexicales (decomposeur_lexical), ce module produit une
ou plusieurs questions SIMPLIFIEES, repondables par la Fiancée de Cline (ou par
un oracle numerique comme Wolfram), afin de faire progresser la reponse a la
requete initiale, trop complexe.

Principe : on conserve les ANCRES du sujet spectral + les NOMBRES, et on
reformule selon des gabarits modestes (reconstruction, ratio, gap, psi_savard,
question generale du spectre).

ADDITIF : stdlib uniquement ; aucun effet de bord.
"""
from __future__ import annotations

from .decomposeur_lexical import AnalyseLexicale, normaliser


def _a(analyse: AnalyseLexicale, *mots: str) -> bool:
    """Vrai si l'un des mots apparait parmi les tokens/ancres analyses."""
    cible = set(analyse.ancres) | set(analyse.associations.keys())
    return any(m in cible for m in mots)


def construire_questions_modestes(analyse: AnalyseLexicale) -> list[str]:
    """Retourne une liste de questions modestes, de la plus pertinente a la moins."""
    questions: list[str] = []
    nombres = analyse.nombres
    n = nombres[0] if nombres else None

    # 1. Reconstruction d'un nombre premier
    if _a(analyse, "reconstruire", "reconstruction", "premier", "premiers", "position", "rang"):
        if n:
            questions.append(f"Quel est le {n}e nombre premier (rapport 1/2) ?")
        else:
            questions.append("Quelle est la definition de la reconstruction du n-ieme nombre premier ?")

    # 2. Rapport spectral / ratio
    if _a(analyse, "ratio", "rapport", "rsp", "1/2", "1/k"):
        if n:
            questions.append(f"Quelle est la valeur du rapport spectral RsP pour n = {n} ?")
        else:
            questions.append("Pourquoi le rapport spectral 1/2 est-il un invariant ?")

    # 3. Gap / ecart / asymetrie
    if _a(analyse, "gap", "ecart", "asymetrie"):
        questions.append("Comment se calcule le gap (ecart) spectral entre deux positions ?")

    # 4. Psi Savard / Tchebychev
    if _a(analyse, "psi", "tchebychev", "chebyshev", "savard"):
        questions.append("Comment se definit Psi_Savard(x, n) et quel est son lien avec Tchebychev ?")

    # 5. Suites A/B / digamma
    if _a(analyse, "suite", "suites", "digamma", "somme"):
        questions.append("Quelles sont les formules des sommes des suites A et B (rapport 1/2) ?")

    # 6. Question generale du sujet (toujours disponible)
    questions.append("Quels sont les elements essentiels de la geometrie du spectre des nombres premiers ?")

    # dedup en gardant l'ordre
    vus: set[str] = set()
    out: list[str] = []
    for q in questions:
        if q not in vus:
            vus.add(q)
            out.append(q)
    return out


def meilleure_question_modeste(analyse: AnalyseLexicale) -> str:
    """Retourne la question modeste la plus pertinente."""
    questions = construire_questions_modestes(analyse)
    return questions[0] if questions else "Qu'est-ce que la geometrie du spectre des nombres premiers ?"


def choix_scores(analyse: AnalyseLexicale) -> list[tuple[str, float]]:
    """Score chaque question modeste selon le recouvrement avec les associations."""
    anime = set(analyse.associations.keys())
    scored: list[tuple[str, float]] = []
    for q in construire_questions_modestes(analyse):
        mots_q = set(normaliser(q).split())
        score = len(mots_q & anime) / max(1, len(mots_q))
        scored.append((q, round(score, 3)))
    return sorted(scored, key=lambda x: x[1], reverse=True)


__all__ = [
    "construire_questions_modestes", "meilleure_question_modeste", "choix_scores",
]