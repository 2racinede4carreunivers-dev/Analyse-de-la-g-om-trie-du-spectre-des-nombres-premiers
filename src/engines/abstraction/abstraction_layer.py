"""
Moteur d'Abstraction (PROFOND).
Extrait les concepts spectraux d'une question en langage naturel.
"""
from __future__ import annotations

import logging
import re
from typing import Any

from ...core.spectral_types import CognitiveConcept, QuestionContext, SpectralModel


logger = logging.getLogger(__name__)

# CONSTANTES DE SÉCURITÉ
MAX_INPUT_LENGTH = 10000  # Limite pour éviter les attaques par régrex complexes


# Patterns lexicaux pour le corpus de Philippe Thomas Savard
SPECTRAL_PATTERNS: dict[str, list[str]] = {
    "rapport_spectral": [
        r"rapport\s+spectr",
        r"\bRsP\b",
        r"1\s*/\s*[234]",
    ],
    "digamma_calc": [
        r"digamma",
        r"\bdgm\b",
    ],
    "prime_equation": [
        r"prime[\s_]?equation",
        r"reconstr.*premier",
        r"P-?[èe]me\s+premier",
        r"p[-\s]?ieme\s+premier",
    ],
    "gap_equation": [
        r"\becart\b", r"\bgap\b", r"quantit[eé]\s+(?:de\s+)?(?:terme|nombre|entier)",
        r"distance\s+entre\s+(?:deux\s+)?premier",
    ],
    "suites_AB": [
        r"\bsuite[s]?\s+A\b", r"\bsuite[s]?\s+B\b",
        r"\bSA\b", r"\bSB\b",
    ],
    "asymetrie": [
        r"asym[ée]trique", r"chaotique", r"ordonn[ée]e",
    ],
    "plan_trifocal": [
        r"plan\s+trifocal", r"[ée]pipolaire", r"trifocal",
    ],
    "riemann": [
        r"riemann", r"hypoth[èe]se", r"z[êe]ta", r"\bRH\b",
    ],
    "suites_mixtes": [
        r"\(-\s*,\s*\+\)", r"mixt", r"n[ée]gatif",
    ],
}


# Detection du modele spectral
def _detect_model(text: str) -> SpectralModel | None:
    text_low = text.lower()
    if "1/2" in text or "un demi" in text_low or "1 sur 2" in text_low:
        return SpectralModel.RATIO_1_2
    if "1/3" in text or "un tiers" in text_low or "1 sur 3" in text_low:
        return SpectralModel.RATIO_1_3
    if "1/4" in text or "un quart" in text_low or "1 sur 4" in text_low:
        return SpectralModel.RATIO_1_4
    return None


def _is_explicit_request(text: str) -> bool:
    """Retourne True si la phrase contient une demande actionnable explicite."""
    t = text.lower()

    # Question explicite ou numerotation de sous-questions (2.1, 3.2, ...)
    if "?" in text or re.search(r"\b\d+\.\d+\b", t):
        return True

    request_patterns = [
        r"\b(?:determine|détermine|calcul|calcule|calcules|trouve|trouver|reconstrui|reconstruis|reconstitue|montre|donne|fournis|genere|génère|trace|dessine|visualise)\b",
        r"\b(?:peux[-\s]?tu|pourrais[-\s]?tu|pouvez[-\s]?vous|merci\s+de|j[' ]aimerais\s+que\s+tu)\b",
        r"\b(?:quel|quelle|quels|quelles|combien)\b",
    ]
    return any(re.search(pat, t) for pat in request_patterns)


def _is_contextual_statement(text: str) -> bool:
    """Retourne True si la phrase est surtout descriptive/conceptuelle."""
    t = text.lower()
    contextual_patterns = [
        r"\best\s+une\b",
        r"\bpermet\s+de\b",
        r"\bconsiste\s+en\b",
        r"\bd[ée]finition\b",
        r"\bcontexte\b",
        r"\bsens\s+de\s+la\s+question\b",
        r"\bparle\s+de\b",
    ]
    return any(re.search(pat, t) for pat in contextual_patterns)


def _extract_numbers(text: str) -> list[int]:
    """Extrait les entiers pertinents d'un segment (hors fractions usuelles).
    
    SÉCURITÉ: Limite la taille d'entrée pour éviter ReDoS (Regular Expression Denial of Service).
    Utilise une approche sans lookaround complexe qui pourrait causer des exponentielles.
    """
    # SÉCURITÉ: Limiter la taille d'entrée pour éviter les attaques ReDoS
    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]
        logger.warning(f"_extract_numbers: input tronqué de {MAX_INPUT_LENGTH} chars")
    
    cleaned = re.sub(r'\b1\s*/\s*[0-9]+\b', ' ', text)
    cleaned = re.sub(r'\brapport\s+[0-9]+\s*/\s*[0-9]+\b', ' ', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'modele?\s+\d+\s*/\s*\d+', ' ', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b13\s*/\s*\d+\b', ' ', cleaned)
    cleaned = re.sub(r'\b3\.25\s*/\s*\d+\b', ' ', cleaned)
    cleaned = re.sub(r'\b6\.5\s*/\s*\d+\b', ' ', cleaned)
    
    # SÉCURITÉ: Regex simplifiée et sécurisée (pas de lookaround complexe)
    # Approche itérative pour extraire les nombres sans lookaround qui cause ReDoS
    numbers: list[int] = []
    for match in re.finditer(r'-?\d+', cleaned):
        try:
            # Vérifier que c'est un nombre isolé (pas partie d'un plus grand nombre)
            start = match.start()
            end = match.end()
            # Vérifier les bornes pour éviter de capturer des parties de nombres
            if (start == 0 or not cleaned[start-1].isdigit()) and (end == len(cleaned) or not cleaned[end].isdigit()):
                numbers.append(int(match.group()))
        except (ValueError, IndexError):
            continue
    
    return numbers


def _split_objective_chunks(text: str) -> list[str]:
    """Decoupe une requete en chunks d'objectifs potentiels, dans l'ordre.
    
    SÉCURITÉ: Limite la taille d'entrée et utilise des regex sécurisées sans ReDoS.
    """
    # SÉCURITÉ: Limiter la taille d'entrée
    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]
        logger.warning(f"_split_objective_chunks: input tronqué à {MAX_INPUT_LENGTH} chars")
    
    q = text.strip()
    if not q:
        return []

    # Cas prioritaire: sous-questions numerotees (2.1, 2.2, ...)
    numbered = list(re.finditer(r'\b\d+\.\d+\b', q))
    if numbered:
        chunks: list[str] = []
        starts = [m.start() for m in numbered] + [len(q)]
        for i in range(len(starts) - 1):
            chunk = q[starts[i]:starts[i + 1]].strip(" .;:\n\t")
            if chunk:
                chunks.append(chunk)
        return chunks

    # SÉCURITÉ: Regex simplifiée et sécurisée (pas d'ambigüité sur \s+)
    # Ancienne regex problématique: r'\s+(?:puis|ensuite|et\s+apres|et\s+puis)\s+|[;\n]+'
    # Problème: \s+ avant le groupe peut matcher de façons multiples (régrex polynomial)
    # Solution: Utiliser une approche plus directe avec séparateurs simples
    # Remplacer par: exactement 1+ espaces suivi du mot clé (sans ambigüité)
    separators = r'\s(?:puis|ensuite|et\s+apres|et\s+puis)\s|[;\n]+'
    rough = [c.strip(" .;:\n\t") for c in re.split(separators, q) if c.strip(" .;:\n\t")]
    
    if len(rough) <= 1:
        # SÉCURITÉ: Regex corrigée - pas de lookbehind complexe
        # Ancienne regex problématique: r'(?<=[\?\.])\s+' (lookbehind variable)
        # Problème: lookbehind peut matcher de plusieurs façons (ReDoS polynomial)
        # Solution: Utiliser simple split sur caractères littéraux
        rough = [c.strip(" .;:\n\t") for c in re.split(r'\?\s+|\.\s+', q) if c.strip(" .;:\n\t")]
    
    return rough


def _extract_objectives(raw_question: str) -> tuple[str, list[dict[str, Any]]]:
    """Extrait un preambule contextuel et des objectifs explicites ordonnes.
    
    SÉCURITÉ: Limite la taille d'entrée pour éviter les attaques.
    """
    # SÉCURITÉ: Limiter la taille d'entrée globale
    if len(raw_question) > MAX_INPUT_LENGTH:
        raw_question = raw_question[:MAX_INPUT_LENGTH]
        logger.warning(f"_extract_objectives: input tronqué à {MAX_INPUT_LENGTH} chars")
    
    chunks = _split_objective_chunks(raw_question)
    objectives: list[dict[str, Any]] = []
    contextual_prefix_parts: list[str] = []

    for i, chunk in enumerate(chunks, start=1):
        explicit = _is_explicit_request(chunk)
        intent = _detect_intent(chunk)
        numbers = _extract_numbers(chunk)
        entry: dict[str, Any] = {
            "index": i,
            "text": chunk,
            "explicit": explicit,
            "intent": intent,
            "numbers": numbers,
        }
        if explicit:
            objectives.append(entry)
        else:
            contextual_prefix_parts.append(chunk)

    contextual_prefix = " ".join(contextual_prefix_parts).strip()
    return contextual_prefix, objectives


def _detect_intent(text: str) -> str:
    """Categorise l'intention : reconstruction / ratio / gap / autre.
    
    SÉCURITÉ: Utilise des regex sécurisées sans ReDoS.
    """
    # SÉCURITÉ: Limiter la taille d'entrée
    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]
    
    t = text.lower()

    # Garde-fou majeur : ne pas traiter une description de contexte comme une
    # demande de calcul. Si ce n'est pas une demande explicite, on route vers
    # conversation/general meme si des mots techniques sont presents.
    explicit_request = _is_explicit_request(text)
    contextual_statement = _is_contextual_statement(text)
    if contextual_statement and not explicit_request:
        return "conversation"

    # SÉCURITÉ: Regex avec lookahead/behind limités (pas de quantificateurs imbriqués)
    if re.search(r"reconstr|p-?i[èe]me|p\s+i[èe]me", t):
        return "reconstruction"
    # Chercher digamma séparément avec une limite de 200 caractères
    if re.search(r"digamma", t) and re.search(r"déterminer", t[:200]):
        return "reconstruction"
    if re.search(r"rapport|ratio|asym[ée]trique|sym[ée]trique|chaotique", t):
        return "ratio"
    # Chercher les patterns gap plus simplement
    if re.search(r"\becart\b|\bgap\b", t) and re.search(r"quantit[eé]|terme|entier|nombre", t):
        return "gap"
    if re.search(r"riemann|hypoth[èe]se|z[êe]ta", t):
        return "riemann_link"
    return "general"


class ConceptExtractor:
    """Extrait concepts mathematiques avec regex et signatures."""

    def extract(self, text: str) -> list[CognitiveConcept]:
        concepts: list[CognitiveConcept] = []
        for concept_name, patterns in SPECTRAL_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text, re.IGNORECASE):
                    concepts.append(
                        CognitiveConcept(
                            name=concept_name,
                            category="spectral",
                            keywords=[pat],
                            confidence=0.9,
                        )
                    )
                    break
        return concepts


class AbstractionLayer:
    """Couche d'abstraction : transforme question -> contexte structure."""

    def __init__(self):
        self.extractor = ConceptExtractor()

    def abstract(self, question_id: str, raw_question: str) -> QuestionContext:
        concepts = self.extractor.extract(raw_question)
        model = _detect_model(raw_question)
        intent = _detect_intent(raw_question)
        explicit_request = _is_explicit_request(raw_question)
        contextual_statement = _is_contextual_statement(raw_question)
        contextual_prefix, objectives = _extract_objectives(raw_question)

        # Intent primaire = premier objectif explicite technique, sinon intent global.
        primary_obj = next(
            (o for o in objectives if o.get("intent") in {"reconstruction", "ratio", "gap"}),
            None,
        )
        if primary_obj is not None:
            intent = str(primary_obj.get("intent", intent))
        domain = "methode_spectrale_savard" if concepts else "general"

        # Extraction des nombres mentionnes (p, n, indices)
        # On retire d'abord les motifs de rapport 1/2, 1/3, 1/4, 1/k pour ne pas les capter
        primary_text = str(primary_obj.get("text")) if primary_obj else raw_question
        numbers = _extract_numbers(primary_text)

        ctx = QuestionContext(
            question_id=question_id,
            raw_question=raw_question,
            detected_domain=domain,
            detected_model=model,
            concepts=concepts,
            metadata={
                "intent": intent,
                "explicit_request": explicit_request,
                "contextual_statement": contextual_statement,
                "contextual_prefix": contextual_prefix,
                "objectives": objectives,
                "primary_objective": primary_obj,
                "has_multiple_objectives": len(objectives) > 1,
                "numbers_mentioned": numbers,
                "language": "fr",
            },
        )
        logger.debug("Abstraction : domain=%s model=%s intent=%s concepts=%d",
                     domain, model, intent, len(concepts))
        return ctx
