"""
Garde-fou REPONSE DIRECTE (obligatoire, sans exception).

Probleme corrige : le LLM local (Qwen) repondait a une requete claire par un
preambule redondant au lieu du contenu demande, par exemple :

    "Bonjour! Je suis Gabriel, agent specialise dans ... Je suis ici pour vous
     aider ... Pourriez-vous me preciser ... ? Je peux vous donner un resume
     exhaustif des caracteristiques de ..."

Ce module supprime de facon deterministe, en tete et en fin de reponse :
  - les salutations isolees ("Bonjour !", "Bonjour Philippe,") ;
  - l'auto-presentation ("Je suis Gabriel, agent specialise ...") ;
  - les formules de service ("Je suis ici pour vous aider", "Avec plaisir") ;
  - l'enumeration de ses propres capacites / l'echo de la requete
    ("Je peux vous donner un resume ...", "Si vous le souhaitez, je peux ...") ;
  - les demandes de precision inutiles ("Pourriez-vous me preciser ... ?") ;
  - les offres de suite ("N'hesitez pas a ...", "Souhaitez-vous que je ... ?").

Si, une fois ces phrases retirees, il ne reste aucun contenu, la reponse est
une NON-REPONSE : l'appelant doit regenerer avec
``DIRECT_ANSWER_RETRY_INSTRUCTION``.
"""
from __future__ import annotations

import re

__all__ = [
    "DIRECT_ANSWER_RULES",
    "DIRECT_ANSWER_RETRY_INSTRUCTION",
    "strip_meta_discourse",
    "is_non_answer",
]


# ---------------------------------------------------------------------------
# Regles injectees dans les prompts (systeme + utilisateur)
# ---------------------------------------------------------------------------
DIRECT_ANSWER_RULES = """
=== REPONSE DIRECTE OBLIGATOIRE (AUCUNE EXCEPTION) ===
- Commence IMMEDIATEMENT par le contenu demande. La premiere phrase de ta
  reponse doit deja contenir de l'information sur le sujet de la question.
- INTERDIT : saluer ("Bonjour !"), te presenter ("Je suis Gabriel..."),
  dire que tu es la pour aider, enumerer tes capacites, reformuler ou repeter
  la question, annoncer ce que tu "peux" faire ("Je peux vous donner...",
  "Si vous le souhaitez, je peux...").
- INTERDIT : demander une precision quand la question est comprehensible.
  Une demande "Peux-tu ... ?" ou "Pourrais-tu ... ?" est un ORDRE d'executer :
  execute-la directement, ne reponds jamais "oui, je peux".
  Si la question couvre plusieurs elements, traite-les TOUS, dans l'ordre.
- INTERDIT : terminer par une offre ("N'hesitez pas...", "Souhaitez-vous que
  je detaille...?", "Voulez-vous que...?").
- Seule exception toleree : une DONNEE NUMERIQUE indispensable a un calcul
  est absente ; dans ce cas, reponds d'abord a tout ce qui peut l'etre, puis
  nomme la donnee manquante en une phrase.
=== FIN REPONSE DIRECTE ===
"""

DIRECT_ANSWER_RETRY_INSTRUCTION = (
    "ATTENTION : ta reponse precedente ne contenait qu'un preambule "
    "(salutation, presentation, enumeration de capacites ou demande de "
    "precision) et AUCUN contenu. C'est interdit. Reponds MAINTENANT "
    "directement a la question, en commencant par le contenu lui-meme, "
    "sans saluer, sans te presenter, sans reformuler la question et sans "
    "poser de question."
)

# ---------------------------------------------------------------------------
# Detection des phrases meta (non-contenu)
# ---------------------------------------------------------------------------
_A = r"[aàâ]"
_E = r"[eéèê]"
_VOUS = r"(?:vous|tu|te|t['’])"

_META_SENTENCE_PATTERNS = [
    # Salutation isolee (phrase courte qui ne fait que saluer / interpeller)
    r"^(?:bonjour|bonsoir|salut|coucou|allo|allô|hello|hey|hi)\b[\s,]*"
    r"(?:(?:cher|ch[eè]re|mon|ma)\s+)?(?:[A-ZÀ-Ý][\w\-]*(?:\s+[A-ZÀ-Ý][\w\-]*){0,3})?\s*[!.,?:;]*$",
    # Auto-presentation
    r"^(?:(?:bonjour|bonsoir|salut)\b[\s!,.]*)?(?:moi\s*,?\s*)?je\s+suis\s+"
    r"(?:mme\.?\s+|mm\.?\s+|madame\s+)?gabriel\b",
    r"^(?:(?:bonjour|bonsoir|salut)\b[\s!,.]*)?je\s+suis\s+(?:un|une|votre|ton|ta|l['’])\s*"
    r"(?:agent|agente|assistant|assistante|ia|intelligence)\b",
    r"^en\s+tant\s+qu['’e]\s*(?:agent|agente|assistant|assistante|ia|gabriel)\b",
    # Formules de service
    r"^je\s+suis\s+(?:l" + _A + r"|ici|pr" + _E + r"sente?|disponible)\s+pour\s+" + _VOUS + r"\s*aider",
    r"^(?:avec\s+(?:grand\s+)?plaisir|bien\s+s[uû]r|certainement|absolument|volontiers|"
    r"excellente\s+question|tr" + _E + r"s\s+bonne\s+question|bonne\s+question)\s*[!.,]*$",
    r"^(?:oui|d['’]accord)\s*[,!.]?\s*(?:bien\s+s[uû]r|certainement|absolument|volontiers|"
    r"je\s+peux|avec\s+plaisir)?\s*[!.,]*$",
    r"^(?:oui\s*[,!.]?\s*)?je\s+serai(?:s)?\s+(?:ravie?|heureuse?|enchant" + _E + r"e?)\s+de\b",
    r"^(?:oui\s*[,!.]?\s*)?(?:ces\s+)?(?:souvenirs?|sujets?|th" + _E + r"mes?|questions?)\s+"
    r"(?:me\s+)?(?:passionne|fascine|int" + _E + r"resse|sont\s+bien)",
    # Enumeration de capacites / echo de la requete
    r"^(?:oui\s*[,!.]?\s*)?(?:et\s+)?(?:si\s+(?:vous\s+le|tu\s+le)\s+(?:d" + _E + r"sire[sz]?|souhaite[sz]?|"
    r"veu[xt]|voulez)\s*,?\s*)?je\s+(?:peux|pourrai[st]?|suis\s+en\s+mesure\s+de|suis\s+capable\s+de|"
    r"saurai[st]?)\s+(?:vous\s+|te\s+|t['’]\s*)?(?:donner|fournir|g" + _E + r"n" + _E + r"rer|"
    r"d" + _E + r"crire|pr" + _E + r"senter|proposer|faire|expliquer|aider|r" + _E + r"pondre|"
    r"r" + _E + r"sumer|d" + _E + r"tailler|pr" + _E + r"ciser|" + _E + r"num" + _E + r"rer|apporter|"
    r"offrir|accompagner|guider|parler)\b",
    r"^je\s+(?:vais|peux)\s+(?:tenter|essayer)\s+de\s+(?:vous|te)\s+",
    # Demandes de precision / offres de suite
    r"^(?:mais\s+)?(?:pourriez|pouvez|pourrais|peux|voudriez|voulez)[\s-]*(?:vous|tu)\s+(?:me\s+|m['’])?"
    r"(?:pr" + _E + r"ciser|indiquer|dire|sp" + _E + r"cifier|clarifier)",
    r"^merci\s+de\s+(?:bien\s+vouloir\s+)?(?:me\s+)?(?:pr" + _E + r"ciser|indiquer|sp" + _E + r"cifier)",
    r"^(?:souhaitez|voulez|d" + _E + r"sirez|souhaites|veux|d" + _E + r"sires)[\s-]*(?:vous|tu)\s+que\s+je\b",
    r"^(?:sur\s+)?quel(?:le)?s?\s+(?:rapport|aspect|point|partie|sujet|" + _E + r"l" + _E + r"ment)s?\s+"
    r"(?:\w+\s+)?(?:souhaitez|voulez|d" + _E + r"sirez|souhaites|veux)[\s-]*(?:vous|tu)\b",
    r"^dites[\s-]*moi\s+(?:sur\s+)?(?:quel|ce\s+que|si)\b",
    r"^n['’]?\s*h" + _E + r"sitez\s+pas\b",
    r"^n['’]?\s*h" + _E + r"site\s+pas\b",
    r"^je\s+(?:reste|demeure)\s+(?:" + _A + r"\s+(?:votre|ta)\s+disposition|disponible)\b",
]
_META_RE = [re.compile(p, re.IGNORECASE) for p in _META_SENTENCE_PATTERNS]

# Decoupage en phrases : ponctuation finale suivie d'espace, ou saut de ligne.
# Les decimaux (0.5) et fractions (1/2) ne sont pas coupes (pas d'espace).
_SPLIT_RE = re.compile(r"(?<=[.!?…])[ \t]+|\r?\n+")
_MD_PREFIX_RE = re.compile(r"^[\s>*_#\-•]+")
_GREETING_PREFIX_RE = re.compile(
    r"^[\s>*_]*(?:bonjour|bonsoir|salut|coucou|allo|allô|hello|hey|hi)\b"
    r"(?:\s+(?:cher|ch[eè]re|mon|ma))?"
    r"(?:\s+[A-ZÀ-Ý][\w\-]*(?:\s+[A-ZÀ-Ý][\w\-]*){0,3})?"
    r"\s*[,!:;]+\s*",
    re.IGNORECASE,
)


def _segments(text: str) -> list[str]:
    return [s for s in _SPLIT_RE.split(text) if s and s.strip()]


def _is_meta(sentence: str) -> bool:
    s = _MD_PREFIX_RE.sub("", sentence).strip().strip("*_` ")
    if not s:
        return False
    return any(r.search(s) for r in _META_RE)


def strip_meta_discourse(text: str | None) -> str:
    """Retire les phrases meta (preambule et offres finales) d'une reponse.

    Seules les phrases situees EN TETE (avant le premier contenu) et EN FIN
    (apres le dernier contenu) sont retirees : le corps de la reponse n'est
    jamais modifie. Retourne une chaine vide si la reponse ne contenait que
    du meta-discours. Les messages d'erreur ``[ERREUR LLM]`` sont conserves.
    """
    if not text:
        return ""
    if text.lstrip().startswith("[ERREUR LLM]"):
        return text

    out = text.strip()
    while out:
        # Salutation en prefixe sur la meme ligne ("Bonjour Philippe, La ...")
        m = _GREETING_PREFIX_RE.match(out)
        if m and m.end() < len(out):
            out = out[m.end():].lstrip(" \t\r\n,;:")
            continue
        segs = _segments(out)
        if not segs:
            break
        if _is_meta(segs[0]):
            idx = out.find(segs[0])
            out = out[idx + len(segs[0]):].lstrip(" \t\r\n,;:")
            continue
        if _is_meta(segs[-1]):
            idx = out.rfind(segs[-1])
            out = out[:idx].rstrip()
            continue
        break
    return out.strip()


def is_non_answer(text: str | None) -> bool:
    """Vrai si la reponse ne contient que du meta-discours (aucun contenu)."""
    if not text or not text.strip():
        return True
    if text.lstrip().startswith("[ERREUR LLM]"):
        return False
    return strip_meta_discourse(text) == ""
