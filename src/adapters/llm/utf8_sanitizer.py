"""
UTF-8 Sanitizer - Corrige les caractères parasites et mal encodés.

Problème: Les accents et caractères spéciaux mal encodés causent:
  UTF-8 encoding can fail when an isolated Unicode surrogate is present.
  
Solution: Nettoyer le texte avant envoi aux LLM.
"""
from __future__ import annotations

import logging
import unicodedata
from typing import Optional


logger = logging.getLogger(__name__)


class UTF8Sanitizer:
    """Nettoie les textes pour éviter les erreurs d'encodage UTF-8."""
    
    @staticmethod
    def sanitize(text: str) -> str:
        """
        Nettoie un texte en supprimant les caractères malformés.
        
        Processus:
        1. Remplacer les surrogates isolés
        2. Normaliser Unicode (NFC)
        3. Remplacer les caractères non-imprimables
        4. Nettoyer les espaces
        """
        if not text:
            return ""
        
        try:
            # Étape 1: Remplacer les surrogates mal formés
            # Remplacer les surrogates isolés par un caractère sûr.
            cleaned = text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            
            # Étape 2: Normaliser Unicode (NFC = Canonical Decomposition + Canonical Composition)
            cleaned = unicodedata.normalize('NFC', cleaned)
            
            # Étape 3: Remplacer les caractères problématiques
            # Mais garder les accents français courants (é, è, ê, à, ù, etc.)
            result = []
            for char in cleaned:
                # Rejeter les caractères de contrôle sauf \n, \t, \r
                if ord(char) < 32 and char not in '\n\t\r':
                    result.append(' ')
                # Garder les caractères imprimables et accents
                elif ord(char) >= 32 or char in '\n\t\r':
                    result.append(char)
            
            cleaned = ''.join(result)
            
            # Étape 4: Nettoyer les espaces multiples
            # Remplacer plusieurs espaces par un seul
            cleaned = ' '.join(cleaned.split())
            
            logger.debug(f"UTF-8 Sanitized: {len(text)} chars → {len(cleaned)} chars")
            return cleaned
            
        except Exception as e:
            logger.error(f"Sanitization error: {e}")
            # En dernier recours, garder seulement ASCII
            return text.encode('ascii', errors='replace').decode('ascii')
    
    @staticmethod
    def sanitize_dict(data: dict) -> dict:
        """Nettoie tous les strings d'un dictionnaire."""
        return {
            k: UTF8Sanitizer.sanitize(v) if isinstance(v, str) else v
            for k, v in data.items()
        }
    
    @staticmethod
    def sanitize_list(items: list) -> list:
        """Nettoie tous les strings d'une liste."""
        return [
            UTF8Sanitizer.sanitize(item) if isinstance(item, str) else item
            for item in items
        ]


def ensure_utf8_safe(text: str) -> str:
    """Alias court pour sanitize()."""
    return UTF8Sanitizer.sanitize(text)
