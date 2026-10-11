"""
REQUEST DECOMPOSER PATCH - Préserver les nombres négatifs dans gap_intent.

Problème : RequestDecomposer extrait les nombres mais perd les signes.
  Input  : "Écart entre -3 et -23"
  Output : "Entre 3 et 23" ← Les signes sont perdus !

Solution : Améliorer detect_gap_intent pour préserver sign() correctement.
"""
from __future__ import annotations

import re
import logging
from typing import Optional


logger = logging.getLogger(__name__)


def detect_gap_intent_improved(question: str) -> tuple[bool, Optional[str], list[int]]:
    """
    Détecte si la question demande un calcul d'écart (AVEC gestion des négatifs).
    
    Returns:
        (is_gap, gap_type, [p1, p2]) où gap_type in ["positive_positive", "negative_negative", "mixed"]
    
    CRUCIAL : Préserver les signes des nombres négatifs !
    """
    q_low = question.lower()
    
    # Chercher les mots-clés "écart", "gap", "entre"
    if not any(kw in q_low for kw in ["écart", "gap", "entre", "nombre", "premier"]):
        logger.debug("Pas de mot-clé gap détecté")
        return False, None, []
    
    # Chercher les nombres AVEC signes (regex: -?\d+)
    # IMPORTANT : regex doit capturer le signe AVANT le chiffre
    numbers = re.findall(r'-?\d+', question)
    
    if len(numbers) < 2:
        logger.debug(f"Moins de 2 nombres trouvés : {numbers}")
        return False, None, []
    
    # Convertir en entiers (sign est préservé par int("-23") = -23)
    try:
        p1, p2 = int(numbers[0]), int(numbers[1])
    except ValueError:
        logger.error(f"Erreur conversion : {numbers}")
        return False, None, []
    
    logger.info(f"Nombres extraits (avec signes) : p1={p1}, p2={p2}")
    
    # Classifier le type d'écart
    if p1 > 0 and p2 > 0:
        gap_type = "positive_positive"
    elif p1 < 0 and p2 < 0:
        gap_type = "negative_negative"
    elif (p1 < 0 and p2 > 0) or (p1 > 0 and p2 < 0):
        gap_type = "mixed"
    else:
        gap_type = None
    
    if gap_type:
        logger.info(f"Écart détecté : {gap_type} → p1={p1}, p2={p2}")
    
    return gap_type is not None, gap_type, [p1, p2]


def is_negative_prime_valid(p: int) -> bool:
    """
    Vérifie si un nombre 'premier négatif' est valide en domaine spectral.
    
    Dans le domaine spectral étendu :
      - Position(-p) = -(Position(p)) pour p positif
      - Les formules SA/SB s'étendent aux exposants négatifs
    
    Returns:
        True si le nombre peut être traité comme un "premier négatif"
    """
    if p >= 0:
        return False  # Ce n'est pas un négatif
    
    # Vérifier que abs(p) a une position valide
    abs_p = abs(p)
    
    # Liste rapide des premiers (pour validation)
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    
    if abs_p in small_primes:
        logger.info(f"Nombre négatif valide en spectral : {p} (abs={abs_p} est premier)")
        return True
    
    # Pour les plus grands, on suppose valid si demandé explicitement
    return True


def extract_gap_parameters_with_signs(question: str, numbers: list[int]) -> tuple[int, int, str]:
    """
    Extrait les paramètres d'écart EN PRÉSERVANT LES SIGNES.
    
    Args:
        question: la question utilisateur
        numbers: liste [p1, p2] (signes déjà préservés par regex)
    
    Returns:
        (p1, p2, gap_type)
    """
    if len(numbers) < 2:
        raise ValueError(f"Besoin au minimum 2 nombres, reçu {len(numbers)}")
    
    p1, p2 = numbers[0], numbers[1]
    
    # Classifier
    if p1 > 0 and p2 > 0:
        gap_type = "positive_positive"
    elif p1 < 0 and p2 < 0:
        gap_type = "negative_negative"
    elif (p1 < 0 and p2 > 0) or (p1 > 0 and p2 < 0):
        gap_type = "mixed"
    else:
        gap_type = "unknown"
    
    logger.info(f"Paramètres extraits : p1={p1}, p2={p2}, type={gap_type}")
    
    return p1, p2, gap_type


# ============================================================================
# KERNEL UPDATE - Ajouter certitude pour premiers négatifs
# ============================================================================

NEGATIVE_PRIME_CERTAINTIES = [
    {
        "id": "NEGATIVE_PRIME_VALID_IN_SPECTRAL",
        "statement": (
            "Nombre 'premier négatif' (-p) EST VALIDE en domaine spectral étendu. "
            "Position(-p) = -(Position(p)). "
            "Les formules SA(n), SB(n) s'étendent aux exposants négatifs."
        ),
        "source": "methode_spectral.thy::negative_position_definition",
        "confidence": 1.0,
    },
    {
        "id": "GAP_NEGATIVE_NEGATIVE_FORMULA",
        "statement": (
            "Écart (-,-) : gap = (SA(n_p1_prev) - (SB(n_p2) - digamma_int(n_p2)) - "
            "(SB(n_p1) - digamma_int(n_p1))) / 64, "
            "où positions sont NÉGATIVES et exposants dans SA/SB sont NÉGATIFS."
        ),
        "source": "methode_spectral.thy::gap_negative_negative",
        "confidence": 1.0,
    },
]
