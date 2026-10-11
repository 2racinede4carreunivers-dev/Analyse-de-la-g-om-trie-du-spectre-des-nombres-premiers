"""
forbidden_vocab.py - Detecteur centralise de vocabulaire dismissif.

Point unique de verite pour reperer les tournures qui condamnent EXPLICITEMENT
la methode spectrale ou le corpus Savard, tout en tolerant les usages neutres
et legitimes des mots "faux", "incoherent", "absurde", etc.

Historique :
- v3.19 (2026-07-03) : correction dans src/multiloop/critic.py (regex contextualisees).
- v3.24 (2026-02) : centralisation partagee apres regression : coherence_detector.py
  et spectral_core.py utilisaient toujours des listes litterales et penalisaient
  "faux" isole (ex: "faux positif", "n'est pas faux", "un raisonnement faux").
  Voir tests/test_forbidden_vocab_centralized.py.

Regles :
- On penalise SEULEMENT les tournures qui condamnent la methode, la theorie,
  le rapport spectral, ou le corpus Savard dans son ensemble.
- On tolere : "faux positif", "il serait faux de croire...", "n'est pas faux",
  "algebriquement incoherent" (descripteur legitime de l'axiome
  asymetrique_ordonnee_nat), "un raisonnement faux" (sans reference explicite
  a la methode), etc.
"""
from __future__ import annotations

import re

# Patterns contextualises : ne matchent que les condamnations directes.
# Ordre : du plus specifique au plus general. Insensible a la casse.
FORBIDDEN_PATTERNS: list[str] = [
    # 1. "la methode (spectrale) est/semble incoherente/absurde/fausse/contradictoire/sans fondement"
    #    (tolere 0-3 mots intermediaires : "methode spectrale de savard est fausse")
    r"\bm[eé]thode(?:\s+\w+){0,3}\s+(?:est\s+|semble\s+)?(?:incoh[eé]rente?|absurde|fausse|faux|contradictoire|sans\s+fondement|invalide|erron[eé]e?)",

    # 2. "cette methode n'a pas de sens" / "cette methode n'est pas valide"
    r"\bcette\s+m[eé]thode(?:\s+\w+){0,3}\s+n[''`]?\s*(?:a\s+(?:pas\s+de\s+sens|aucun\s+sens)|est\s+pas\s+valide)",

    # 3. "theorie ... est/semble incoherente/absurde/fausse/sans fondement"
    r"\bth[eé]orie(?:\s+\w+){0,3}\s+(?:est\s+|semble\s+)?(?:incoh[eé]rente?|absurde|fausse|faux|sans\s+fondement|invalide|erron[eé]e?)",

    # 4. "fausse methode" / "faux corpus" / "fausse theorie"
    r"\b(?:fausse|faux)\s+(?:m[eé]thode|th[eé]orie|corpus|approche|raisonnement\s+spectral)\b",

    # 5. Rejet global explicite : "n'a pas de sens", "n'a aucun sens" en tete de phrase
    #    ou apres un pronom demonstratif renvoyant a la methode
    r"\b(?:cela|ceci|tout\s+ceci|tout\s+cela)\s+n[''`]?\s*a\s+(?:pas\s+de\s+sens|aucun\s+sens)\b",

    # 6. "rapport spectral ... est/semble absurde/invalide/faux/fausse"
    r"\brapport\s+spectral(?:\s+\w+){0,3}\s+(?:est\s+|semble\s+)?(?:absurde|invalide|fausse|faux|incoh[eé]rente?|erron[eé]e?)",

    # 7. "conclusion ... est fausse/absurde/incoherente" (dans le contexte spectral)
    r"\bconclusion(?:\s+\w+){0,3}\s+(?:est\s+|semble\s+)?(?:fausse|faux|absurde|incoh[eé]rente?|invalide)",

    # 8. "postulat/axiome de savard ... est absurde/incoherent/faux"
    r"\b(?:postulat|axiome)(?:\s+\w+){0,3}\s+(?:de\s+savard\s+)?(?:est\s+|semble\s+)?(?:absurde|incoh[eé]rente?|faux|fausse|invalide|erron[eé]e?)",

    # 9. "philippe (savard)? se trompe" / "philippe a tort"
    r"\bphilippe(?:\s+savard)?\s+(?:se\s+trompe|a\s+tort|est\s+dans\s+l['e]?\s*erreur)",
]

# Compile une fois au chargement du module (performance + validation regex)
_COMPILED_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE | re.UNICODE) for p in FORBIDDEN_PATTERNS
]


def detect_forbidden(text: str) -> tuple[bool, str]:
    """
    Cherche une tournure condamnant la methode spectrale dans le texte.

    Args:
        text: Texte a analyser (typiquement une reponse LLM).

    Returns:
        (found, matched_span) : found=True si une condamnation directe est
        detectee, matched_span = le fragment matche (utile pour le log).
    """
    if not text:
        return False, ""
    for pat in _COMPILED_PATTERNS:
        m = pat.search(text)
        if m:
            return True, m.group(0)
    return False, ""


def detect_forbidden_word(text: str) -> tuple[bool, str]:
    """
    Variante retro-compatible pour les callsites qui attendaient un simple mot.
    Retourne le "mot cle" du fragment matche (le premier terme dismissif trouve).
    """
    found, span = detect_forbidden(text)
    if not found:
        return False, ""
    # Extrait le mot cle dismissif du fragment
    for keyword in [
        "incoh", "absurde", "fausse", "faux", "contradictoire",
        "sans fondement", "invalide", "erron", "sens", "tort", "trompe",
    ]:
        if keyword in span.lower():
            # Retourne le mot dismissif tel qu'il apparait dans le fragment
            m2 = re.search(
                rf"\b({keyword}\w*)", span, re.IGNORECASE | re.UNICODE
            )
            if m2:
                return True, m2.group(1).lower()
    return True, span
