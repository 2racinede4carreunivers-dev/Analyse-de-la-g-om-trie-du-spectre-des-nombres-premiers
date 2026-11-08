"""decomposeur_lexical.py - Decomposition d'une requete en divisions et associations.

8e moteur (arriere-plan) de << La fiancée de Cline >> : lorsque l'agent ne sait
pas repondre, il decoupe le message de la requete en DIVISIONS (phrases/clauses),
puis en MOTS et GROUPES DE MOTS, et les associe au vocabulaire :
  * du corpus spectrale (methode_spectral, suites A/B, digamma...),
  * du pipeline cognitif convolutif,
  * du pipeline HOL/Isabelle/LEAN.

Ces associations servent a construire une question plus modeste (voir
generateur_question_modeste.py).

ADDITIF : stdlib uniquement ; aucun effet de bord.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ── Lexiques integres (fallback + base du matching) ───────────────────────
LEXIQUE_SPECTRAL = {
    "spectre", "spectral", "spectrale", "premier", "premiers", "premiere",
    "nombre", "nombres", "prime", "primalite", "rsp", "ratio", "rapport",
    "digamma", "reconstruction", "reconstruire", "gap", "ecart", "asymetrie",
    "invariant", "convolutif", "convolutive", "suite", "suites", "position",
    "rang", "ancrage", "riemann", "zeta", "critique", "savard", "tchebychev",
    "chebyshev", "psi", "somme", "terme", "termes", "typique", "negatif",
    "possession", "exclusivite", "parite", "logarithme", "densite",
}
LEXIQUE_HOL = {
    "hol", "isabelle", "lean", "lean4", "thy", "theorie", "preuve", "prouver",
    "lemme", "theoreme", "axiome", "formal", "formaliser", "formalisation",
    "qed", "tactique", "hypothese", "absurde", "contradiction", "locale",
    "definition", "corollaire", "demonstration", "verification", "valider",
    "certifier", "verifier", "exclusivite",
}
LEXIQUE_COGNITIF = {
    "cognitif", "moteur", "multiloop", "boucle", "loops", "raisonner",
    "raisonnement", "coherence", "audit", "critique", "raffinement",
    "induction", "deduction", "analogie", "abstraction", "generalisation",
    "navigation", "concept", "hypothese", "meta",
}
LEXIQUE_CORPUS = {
    "corpus", "methode", "methode_spectral", "section", "chapitre", "regime",
    "configuration", "symetrique", "ordonnee", "chaotique", "bloc",
    "formule", "formules", "equation", "coefficient", "facteur", "table",
    "reference", "validation", "unifiee", "geometrie", "univers", "carre",
}


@dataclass
class AnalyseLexicale:
    """Resultat de la decomposition lexicale d'un message."""
    message: str
    divisions: list[str] = field(default_factory=list)
    tokens: list[str] = field(default_factory=list)
    associations: dict[str, list[str]] = field(default_factory=dict)
    ancres: list[str] = field(default_factory=list)
    nombres: list[str] = field(default_factory=list)
    couverture: float = 0.0

    @property
    def vocabulaires_touches(self) -> list[str]:
        vus: set[str] = set()
        for tags in self.associations.values():
            vus.update(tags)
        return sorted(vus)


def normaliser(texte: str) -> str:
    """Minuscule + suppression des accents (matching robuste)."""
    texte = texte.lower()
    return texte.translate(str.maketrans(
        "àâäáãåéèêëíìîïóòôöõúùûüçñ",
        "aaaaaaeeeeiiiiooooouuuucn",
    ))


def diviser(message: str) -> list[str]:
    """Decoupe le message en divisions (phrases, clauses, segments)."""
    if not message:
        return []
    brut = re.split(r"[.!?;:\n]+", message)
    divisions: list[str] = []
    for d in brut:
        # sous-decoupe sur les connecteurs de coordination
        for sub in re.split(r"\s+(?:et|puis|mais|or|donc|car|ainsi)\s+", d):
            sub = sub.strip()
            if sub:
                divisions.append(sub)
    # si rien, garder le message entier
    return divisions or [message.strip()]


def tokeniser(divisions: list[str]) -> list[str]:
    """Retourne les mots + groupes de mots (bigrammes) pertinents."""
    tokens: list[str] = []
    for div in divisions:
        mots = re.findall(r"[0-9A-Za-zÀ-ÿ_/\-']+", normaliser(div))
        mots = [m for m in mots if len(m) >= 2 or m.isdigit()]
        tokens.extend(mots)
        for i in range(len(mots) - 1):
            tokens.append(f"{mots[i]} {mots[i + 1]}")
    # deduplicate en gardant l'ordre
    vus: set[str] = set()
    out: list[str] = []
    for t in tokens:
        if t not in vus:
            vus.add(t)
            out.append(t)
    return out


def charger_vocabulaire() -> dict[str, set[str]]:
    """Charge les 4 vocabulaires ; enrichit depuis le corpus si possible."""
    vocab = {
        "spectral": set(LEXIQUE_SPECTRAL),
        "hol": set(LEXIQUE_HOL),
        "cognitif": set(LEXIQUE_COGNITIF),
        "corpus": set(LEXIQUE_CORPUS),
    }
    # Enrichissement optionnel depuis la base de connaissance spectrale.
    try:
        from ...spectral.spectral_knowledge import SPECTRAL_KNOWLEDGE_FR
        for mot in re.findall(r"[0-9A-Za-zÀ-ÿ_]{3,}", normaliser(SPECTRAL_KNOWLEDGE_FR)):
            if mot.isdigit():
                continue
            vocab["spectral"].add(mot)
    except Exception:
        pass
    return vocab


def _associer_token(token: str, vocab: dict[str, set[str]]) -> list[str]:
    tags: list[str] = []
    for nom, lexique in vocab.items():
        if token in lexique:
            tags.append(nom)
            continue
        # bigrammes : au moins un mot du lexique
        for mot in token.split():
            if mot in lexique:
                tags.append(nom)
                break
    # dedup
    vus: set[str] = set()
    out: list[str] = []
    for t in tags:
        if t not in vus:
            vus.add(t)
            out.append(t)
    return out


def analyser(message: str, vocab: dict[str, set[str]] | None = None) -> AnalyseLexicale:
    """Analyse lexicale complete : divisions, tokens, associations, ancres."""
    vocab = vocab or charger_vocabulaire()
    divisions = diviser(message)
    tokens = tokeniser(divisions)
    associations: dict[str, list[str]] = {}
    ancres: list[str] = []
    for tok in tokens:
        tags = _associer_token(tok, vocab)
        if tags:
            associations[tok] = tags
            if "spectral" in tags or "corpus" in tags:
                ancres.append(tok)
    nombres = re.findall(r"-?\d+", normaliser(message))
    trouves = sum(1 for t in tokens if t in associations)
    couverture = trouves / len(tokens) if tokens else 0.0
    return AnalyseLexicale(
        message=message,
        divisions=divisions,
        tokens=tokens,
        associations=associations,
        ancres=ancres,
        nombres=nombres,
        couverture=couverture,
    )


__all__ = [
    "AnalyseLexicale", "LEXIQUE_SPECTRAL", "LEXIQUE_HOL",
    "LEXIQUE_COGNITIF", "LEXIQUE_CORPUS",
    "normaliser", "diviser", "tokeniser", "charger_vocabulaire", "analyser",
]