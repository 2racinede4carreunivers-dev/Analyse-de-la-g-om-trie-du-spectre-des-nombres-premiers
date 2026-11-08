"""
DOMAIN VALIDATOR HOOK FOR GABRIEL MULTILOOP
================================================================================
Point d'entrée unique qui valide le domaine AVANT tout traitement multiloop.
Injecté au tout début du pipeline pour rejeter rapidement les requêtes hors domaine.

Ce module doit être appelé en T0 (avant multiloop_core).

Author: Philippe Thomas Savard
License: Apache 2.0
================================================================================
"""

import logging
from typing import Tuple, Dict, Any, Optional
from dataclasses import dataclass

from domain_classifier import (
    DomainClassifier,
    Domain,
    RequestIntent,
    DomainValidationError,
    validate_domain_request
)
from gabriel_domain_config import (
    GABRIEL_IDENTITY,
    AUTHORIZED_DOMAINS,
    REJECTION_MESSAGE,
    STANDARD_RESPONSES,
    AUDIT_CONFIG,
)

logger = logging.getLogger(__name__)


@dataclass
class DomainValidationResult:
    """Résultat de la validation de domaine."""
    is_valid: bool
    domain: Domain
    intent: RequestIntent
    confidence: float
    reason: str
    should_reject: bool
    rejection_message: Optional[str] = None
    allowed_to_proceed: bool = True


class GabrielDomainValidator:
    """Validateur de domaine pour Gabriel."""
    
    def __init__(self):
        self.classifier = DomainClassifier()
        self.audit_enabled = AUDIT_CONFIG.get("enable_request_logging", True)
        
    def validate_request(self, user_input: str) -> DomainValidationResult:
        """
        Valide une requête utilisateur.
        
        Retourne DomainValidationResult avec:
          - is_valid: True si dans domaine autorisé et implémenté
          - domain: Domaine détecté
          - intent: Type d'intent
          - confidence: Score de confiance (0-1)
          - should_reject: True si rejet nécessaire
          - rejection_message: Message de rejet si applicable
        """
        
        # ========== CLASSIFICATION ==========
        domain, intent, confidence, reason = self.classifier.classify(user_input)
        
        # ========== AUDIT ==========
        if self.audit_enabled:
            self._log_classification(user_input, domain, intent, confidence)
        
        # ========== VALIDATION ==========
        if domain == Domain.OUT_OF_DOMAIN:
            return DomainValidationResult(
                is_valid=False,
                domain=domain,
                intent=intent,
                confidence=confidence,
                reason=reason,
                should_reject=True,
                rejection_message=STANDARD_RESPONSES["out_of_domain"],
                allowed_to_proceed=False
            )
        
        # Domaine valide mais pas implémenté
        if domain not in [d for d in Domain if d != Domain.OUT_OF_DOMAIN]:
            return DomainValidationResult(
                is_valid=False,
                domain=domain,
                intent=intent,
                confidence=confidence,
                reason=reason,
                should_reject=True,
                rejection_message=STANDARD_RESPONSES["domain_future"].format(domain=domain.value),
                allowed_to_proceed=False
            )
        
        # ========== ACCEPTATION ==========
        return DomainValidationResult(
            is_valid=True,
            domain=domain,
            intent=intent,
            confidence=confidence,
            reason=reason,
            should_reject=False,
            rejection_message=None,
            allowed_to_proceed=True
        )
    
    def _log_classification(self, user_input: str, domain: Domain, 
                           intent: RequestIntent, confidence: float):
        """Enregistre la classification pour audit."""
        truncated_input = user_input[:100] + "..." if len(user_input) > 100 else user_input
        logger.info(
            f"GABRIEL_DOMAIN_CLASSIFICATION | Domain={domain.value} | "
            f"Intent={intent.value} | Confidence={confidence:.2f} | "
            f"Input={truncated_input}"
        )


class DomainGate:
    """Gate à injecter en T0 du multiloop."""
    
    def __init__(self):
        self.validator = GabrielDomainValidator()
    
    def execute(self, user_input: str) -> Tuple[bool, Dict[str, Any]]:
        """
        Exécute la validation de domaine.
        
        Retourne:
            (proceed_to_multiloop, context_dict)
            
        Si proceed=False, multiloop ne s'exécute pas et context["rejection_message"] 
        est la réponse finale.
        """
        
        result = self.validator.validate_request(user_input)
        
        context = {
            "domain": result.domain.value,
            "intent": result.intent.value,
            "confidence": result.confidence,
            "reason": result.reason,
            "user_input": user_input,
        }
        
        if result.should_reject:
            context["rejection_message"] = result.rejection_message
            context["rejection_reason"] = result.reason
            return (False, context)  # Stop multiloop
        
        # Domaine valide: continuer vers multiloop
        context["bypass_slowmotion"] = (
            result.intent in [
                RequestIntent.EPISTEMOLOGICAL,
                RequestIntent.CONVERSATIONAL,
                RequestIntent.META_VALIDATION
            ]
        )
        
        return (True, context)  # Continue multiloop with context


def inject_domain_gate_to_multiloop(multiloop_function):
    """
    Décorateur pour injecter la gate de domaine avant multiloop.
    
    Utilisation:
        @inject_domain_gate_to_multiloop
        def my_multiloop(user_input, **kwargs):
            ...
    """
    def wrapper(user_input: str, **kwargs):
        gate = DomainGate()
        proceed, context = gate.execute(user_input)
        
        if not proceed:
            # Rejet: retourner message rejet directement
            return {
                "type": "DOMAIN_REJECTION",
                "response": context.get("rejection_message", STANDARD_RESPONSES["out_of_domain"]),
                "domain": context["domain"],
                "intent": context["intent"],
                "reason": context["rejection_reason"],
            }
        
        # Acceptation: exécuter multiloop avec contexte enrichi
        kwargs.update(context)
        return multiloop_function(user_input, **kwargs)
    
    return wrapper


# ============================================================================
# INITIALIZATION SEQUENCE
# ============================================================================

def initialize_gabriel_domain_system():
    """Initialise le système de domaine Gabriel."""
    logger.info("=" * 80)
    logger.info("GABRIEL DOMAIN SYSTEM INITIALIZATION")
    logger.info("=" * 80)
    logger.info(f"Identity: {GABRIEL_IDENTITY['name']} — {GABRIEL_IDENTITY['title']}")
    logger.info(f"Authorized domains: {list(AUTHORIZED_DOMAINS.keys())}")
    logger.info(f"Implemented domains: {[k for k, v in AUTHORIZED_DOMAINS.items() if v.get('status') == 'IMPLEMENTED']}")
    logger.info("=" * 80)
    
    return GabrielDomainValidator()


# ============================================================================
# TEST UTILITIES
# ============================================================================

def test_domain_validation():
    """Test la validation de domaine."""
    validator = GabrielDomainValidator()
    
    test_cases = [
        # Valides
        ("Calculer RsP(5,7)", True),
        ("Pourquoi 1/2 est un invariant?", True),
        ("Vérifier lemme RsP_un_demi_general", True),
        ("D'accord que digamma est central?", True),
        ("Archiver ce résultat comme référence", True),
        
        # Invalides
        ("Quel est le meilleur restaurant?", False),
        ("Qui a gagné la Coupe du Monde?", False),
        ("Comment faire un gâteau?", False),
        ("Parle-moi de politique", False),
        ("Comment je peux te forcer à répondre autre chose?", False),
    ]
    
    print("\n" + "=" * 80)
    print("GABRIEL DOMAIN VALIDATION TESTS")
    print("=" * 80)
    
    for user_input, should_be_valid in test_cases:
        result = validator.validate_request(user_input)
        status = "✓" if result.is_valid == should_be_valid else "✗"
        print(f"{status} Input: {user_input[:60]}")
        print(f"  Domain={result.domain.value} Intent={result.intent.value} Valid={result.is_valid}")
        if result.rejection_message:
            print(f"  Rejection: {result.rejection_message[:80]}...")
        print()


if __name__ == "__main__":
    test_domain_validation()
