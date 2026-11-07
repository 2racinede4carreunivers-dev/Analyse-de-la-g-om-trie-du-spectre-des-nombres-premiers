#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECTION CENTRALE — Zêta Denominator (k^6)
Remplace l'utilisation en dur de 64 (=2^6) par k^6 déduit du rapport 1/k
"""

import re
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def extraire_k_depuis_rapport(rapport: str) -> Optional[int]:
    """
    Extrait k depuis un rapport de la forme '1/k' ou '1/2' ou '1/3', etc.
    
    Args:
        rapport: Chaîne comme '1/2', '1/14', '1/9', etc.
        
    Returns:
        int: La valeur k, ou None si le format est invalide
    """
    # Nettoyage: espaces, parenthèses, etc.
    rapport_clean = str(rapport).strip().replace(" ", "")
    
    # Pattern: 1/k où k est un entier
    match = re.match(r"^1/(\d+)$", rapport_clean)
    if not match:
        logger.warning(f"Rapport invalide: {rapport}")
        return None
    
    k = int(match.group(1))
    if k < 2:
        logger.warning(f"k doit être >= 2 pour un rapport 1/k valide, reçu: {k}")
        return None
    
    return k


def calculer_zeta_denominator(rapport: str) -> Optional[int]:
    """
    Calcule le dénominateur Zêta pour un rapport 1/k.
    
    Pour le rapport 1/k, le dénominateur Zêta est k^6.
    
    Args:
        rapport: Chaîne comme '1/2', '1/14', etc.
        
    Returns:
        int: k^6, ou None si le rapport est invalide
        
    Examples:
        calculer_zeta_denominator('1/2')  -> 64  (2^6)
        calculer_zeta_denominator('1/14') -> 7529536  (14^6)
        calculer_zeta_denominator('1/3')  -> 729  (3^6)
        calculer_zeta_denominator('1/9')  -> 531441  (9^6)
    """
    k = extraire_k_depuis_rapport(rapport)
    if k is None:
        return None
    
    zeta = k ** 6
    logger.info(f"Zêta denominator pour rapport 1/{k}: {k}^6 = {zeta}")
    return zeta


def appliquer_k_au_digamma(somme_b: int, digamma_calcule: int, rapport: str) -> Optional[int]:
    """
    Reconstruit le premier via: P = (SB - Digamma) / k^6
    
    Ceci remplace la formule erronée: P = (SB - Digamma) / 64
    
    Args:
        somme_b: Valeur de la somme B (SB)
        digamma_calcule: Valeur du Digamma calculée
        rapport: Chaîne du rapport '1/k'
        
    Returns:
        int: Le premier reconstruit (P), ou None si erreur
    """
    zeta = calculer_zeta_denominator(rapport)
    if zeta is None:
        return None
    
    numerateur = somme_b - digamma_calcule
    
    # Vérifier que le numérateur est divisible par zeta
    if numerateur % zeta != 0:
        logger.error(
            f"Numérateur ({numerateur}) non divisible par k^6 ({zeta}) "
            f"pour rapport {rapport}"
        )
        return None
    
    premier = numerateur // zeta
    logger.info(
        f"Reconstruction: ({somme_b} - {digamma_calcule}) / {zeta} = {premier}"
    )
    return premier


def valider_zeta_usage(rapport: str, zeta_utilise: int) -> bool:
    """
    Valide que le zeta utilisé correspond au rapport.
    CONTRÔLE DE QUALITÉ: empêche les régressions où 64 serait utilisé
    pour des rapports != 1/2.
    
    Args:
        rapport: Chaîne du rapport '1/k'
        zeta_utilise: Valeur de zeta utilisée dans le calcul
        
    Returns:
        bool: True si valide, False sinon
    """
    zeta_attendu = calculer_zeta_denominator(rapport)
    if zeta_attendu is None:
        return False
    
    if zeta_utilise != zeta_attendu:
        logger.error(
            f"ERREUR ZETA: rapport {rapport} devrait utiliser k^6={zeta_attendu}, "
            f"mais {zeta_utilise} a été utilisé (REGRESSION 64?)"
        )
        return False
    
    logger.info(f"✓ Zêta valide pour {rapport}: {zeta_utilise} = {zeta_attendu}")
    return True


def extraire_k_et_zeta(rapport: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Retourne le couple (k, k^6) déduit du rapport 1/k.
    
    Returns:
        Tuple[int, int]: (k, k^6) ou (None, None) si erreur
    """
    k = extraire_k_depuis_rapport(rapport)
    if k is None:
        return None, None
    
    zeta = k ** 6
    return k, zeta


# Tests unitaires intégrés
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=== Tests d'extraction k ===")
    assert extraire_k_depuis_rapport("1/2") == 2
    assert extraire_k_depuis_rapport("1/14") == 14
    assert extraire_k_depuis_rapport("1/9") == 9
    assert extraire_k_depuis_rapport("1/3") == 3
    print("✓ Tous les tests d'extraction passent")
    
    print("\n=== Tests de calcul Zêta ===")
    assert calculer_zeta_denominator("1/2") == 64
    assert calculer_zeta_denominator("1/3") == 729
    assert calculer_zeta_denominator("1/9") == 531441
    assert calculer_zeta_denominator("1/14") == 7529536
    print("✓ Tous les tests Zêta passent")
    
    print("\n=== Tests de validation ===")
    assert valider_zeta_usage("1/2", 64)
    assert valider_zeta_usage("1/14", 7529536)
    assert not valider_zeta_usage("1/14", 64)  # REGRESSION!
    print("✓ Tous les tests de validation passent")
    
    print("\n=== Tests de reconstruction ===")
    # Exemple fictif: si SB=1000, Digamma=100, 1/2
    # P = (1000-100)/64 = 900/64 = 14.0625 (pas entier, donc None)
    result = appliquer_k_au_digamma(1000, 100, "1/2")
    print(f"Reconstruction test (cas non-entier): {result}")
    
    print("\nTous les tests passent!")

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
