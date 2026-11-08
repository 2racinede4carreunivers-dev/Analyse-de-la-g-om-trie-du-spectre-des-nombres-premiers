"""
DOMAIN CLASSIFIER FOR GABRIEL
================================================================================
Gabriel est un agent HYPER-SPECIALISE sur le domaine "Univers est au carré".
Ce module rejette strictement toute requête hors domaine.

Domaines autorisés (EXCLUSIFS):
  1. GEOMETRIE_SPECTRE_PREMIERS - Géométrie du spectre des nombres premiers
  2. MECANIQUE_HARMONIQUE_CHAOS - Mécanique harmonique du chaos discret (futur)
  3. POSTULAT_UNIVERS_CARRE - Postulat de l'univers est au carré (futur)
  4. ESPACE_PHILIPPOT - Espace de Philippôt (futur)

Types de requête ACCEPTES (dans le domaine autorisé):
  - TECHNICAL_HOL: Requête technique HOL/Isabelle sur methode_spectral.thy
  - SPECTRAL_CALCULATION: Calcul numérique (RsP, SA, SB, premiers)
  - EPISTEMOLOGICAL: Questions théoriques/philosophiques/ontologiques
  - META_VALIDATION: Certification, archivage, validation référence
  - CONVERSATIONAL: Dialogue contextualisé dans le domaine

Requête REJETEE si hors domaine OU malveillance potentielle.

Author: Philippe Thomas Savard
License: Apache License 2.0
================================================================================
"""

import re
from enum import Enum
from typing import Tuple, Optional


class Domain(Enum):
    """Domaines reconnus par Gabriel."""
    GEOMETRIE_SPECTRE_PREMIERS = "geometrie_spectre_premiers"
    MECANIQUE_HARMONIQUE_CHAOS = "mecanique_harmonique_chaos"  # Futur
    POSTULAT_UNIVERS_CARRE = "postulat_univers_carre"  # Futur
    ESPACE_PHILIPPOT = "espace_philippot"  # Futur
    OUT_OF_DOMAIN = "out_of_domain"


class RequestIntent(Enum):
    """Types de requête acceptés dans le domaine autorisé."""
    TECHNICAL_HOL = "technical_hol"
    SPECTRAL_CALCULATION = "spectral_calculation"
    EPISTEMOLOGICAL = "epistemological"
    META_VALIDATION = "meta_validation"
    CONVERSATIONAL = "conversational"
    OUT_OF_DOMAIN = "out_of_domain"


class DomainClassifier:
    """Classifie et valide les requêtes Gabriel."""

    def __init__(self):
        """Initialise le classifieur avec vocabulaire métier."""
        
        # ========== DOMAINE: Géométrie du spectre des nombres premiers ==========
        self.domain_keywords_spectral = {
            "français": [
                "spectre", "nombre premier", "premier", "RsP", "SA", "SB",
                "géométrie spectral", "méthode spectral", "invariant",
                "ratio", "1/2", "digamma", "reconstruction", "gap", "asymétrie",
                "configuration", "symétrique", "ordonnée", "chaotique",
                "methode_spectral.thy", "hypothèse de riemann", "riemann",
                "harmonique", "oscillation", "densité", "distribution",
                "théorème", "lemme", "preuve", "HOL", "Isabelle",
                "cryptographie", "prime", "composite", "séquence"
            ],
            "symboles": ["RsP", "SA", "SB", "ψ", "Σ", "∑"]
        }

        self.domain_keywords_chaos = {
            "français": [
                "chaos", "discret", "harmonique", "dynamique", "itération",
                "bifurcation", "attracteur", "lyapunov", "entropie",
                "mécanique harmonique du chaos"
            ]
        }

        self.domain_keywords_univers_carre = {
            "français": [
                "univers est au carré", "postulat", "carré", "dimensionnalité",
                "théorie de l'univers est au carré"
            ]
        }

        self.domain_keywords_espace_philippot = {
            "français": [
                "espace de philippôt", "philippot", "espace", "topologie",
                "géométrie philippôtienne"
            ]
        }

        # ========== INTENT KEYWORDS ==========
        self.intent_keywords = {
            RequestIntent.TECHNICAL_HOL: [
                "HOL", "Isabelle", "lemme", "théorème", "preuve", "formel",
                "définition", "axiome", "implémenter", "coder", "syntaxe HOL",
                "validation formelle", "vérification HOL"
            ],
            RequestIntent.SPECTRAL_CALCULATION: [
                "calculer", "RsP", "SA", "SB", "premier", "gap", "ratio",
                "reconstruction", "nombre", "valeur", "résultat", "numérique",
                "exemple", "cas", "configuration", "tuples"
            ],
            RequestIntent.EPISTEMOLOGICAL: [
                "pourquoi", "comment", "lien", "rapport", "compréhension",
                "sens", "nature", "position", "théorie", "ontologie",
                "épistémologie", "fondement", "origine", "signification",
                "explication", "raison", "cause", "principe"
            ],
            RequestIntent.META_VALIDATION: [
                "certification", "archive", "examen", "capacités", "validation",
                "référence", "preuve d'exactitude", "sauvegarde", "certifié",
                "authentique", "approuvé", "vérification", "checkpoint"
            ],
            RequestIntent.CONVERSATIONAL: [
                "accord", "avis", "pense", "propose", "dialogue", "exploration",
                "question", "discuter", "parler", "échange", "avis",
                "d'accord", "selon toi", "crois-tu"
            ]
        }

        # ========== KEYWORDS DE REJET (malveillance / out-of-domain) ==========
        self.rejection_keywords = [
            # Politique générale
            "politique", "élection", "vote", "gouvernement", "parti",
            "ministre", "président", "régime", "idéologie",
            # Divertissement généraliste
            "gâteau", "recette", "cuisine", "film", "musique", "chanson",
            "sport", "football", "tennis", "match", "jeu vidéo",
            # Social généraliste
            "instagram", "facebook", "tiktok", "tweet", "meme",
            "célébrité", "people", "potins",
            # Santé généraliste
            "maladie", "médecine", "diagnostic", "traitement",
            # Code/Tech générale (hors HOL/Isabelle/spectral)
            "javascript", "python général", "web", "html", "css",
            "react", "node.js", "base de données", "sql",
            # Autres domaines scientifiques
            "physique quantique", "mécanique classique", "relativité",
            "biologie", "chimie", "astronomie",
            # Assistance générale
            "qui es-tu", "à quoi tu sers", "que peux-tu faire",
            # Malveillance détectée
            "jailbreak", "prompt injection", "ignore les règles",
            "oublie tes contraintes", "oublie ton domaine"
        ]

        # ========== DOMAINES ACTUELLEMENT IMPLEMENTS ==========
        self.domains_implemented = [
            Domain.GEOMETRIE_SPECTRE_PREMIERS
        ]

    def classify(self, user_input: str) -> Tuple[Domain, RequestIntent, float, str]:
        """
        Classifie la requête utilisateur.
        
        Retourne:
            (domain, intent, confidence, reason_str)
            
        Levant exception si requête hors domaine.
        """
        input_lower = user_input.lower()
        
        # ========== ETAPE 1: DETECTER MALVEILLANCE ==========
        if self._check_malveillance(input_lower):
            return (
                Domain.OUT_OF_DOMAIN,
                RequestIntent.OUT_OF_DOMAIN,
                1.0,
                "REJET: Tentative de jailbreak détectée."
            )
        
        # ========== ETAPE 2: DETECTER LE DOMAINE ==========
        domain = self._detect_domain(input_lower)
        
        if domain == Domain.OUT_OF_DOMAIN:
            return (
                Domain.OUT_OF_DOMAIN,
                RequestIntent.OUT_OF_DOMAIN,
                1.0,
                f"REJET: Requête hors domaine 'Univers est au carré'."
            )
        
        if domain not in self.domains_implemented:
            return (
                domain,
                RequestIntent.OUT_OF_DOMAIN,
                0.8,
                f"REJET: Domaine '{domain.value}' pas encore implémenté. "
                f"Domaines disponibles: {[d.value for d in self.domains_implemented]}"
            )
        
        # ========== ETAPE 3: DETECTER L'INTENT ==========
        intent = self._detect_intent(input_lower)
        confidence = self._calculate_confidence(user_input, domain, intent)
        
        reason = f"ACCEPT: Domain={domain.value}, Intent={intent.value}, Confidence={confidence:.2f}"
        
        return (domain, intent, confidence, reason)
    
    def _check_malveillance(self, input_lower: str) -> bool:
        """Détecte tentatives de jailbreak/injection."""
        for keyword in self.rejection_keywords:
            if keyword.lower() in input_lower:
                return True
        return False
    
    def _detect_domain(self, input_lower: str) -> Domain:
        """Détecte le domaine principal de la requête."""
        
        # Ordre de priorité (du plus spécifique au plus général)
        domains_to_check = [
            (Domain.ESPACE_PHILIPPOT, self.domain_keywords_espace_philippot["français"]),
            (Domain.POSTULAT_UNIVERS_CARRE, self.domain_keywords_univers_carre["français"]),
            (Domain.MECANIQUE_HARMONIQUE_CHAOS, self.domain_keywords_chaos["français"]),
            (Domain.GEOMETRIE_SPECTRE_PREMIERS, self.domain_keywords_spectral["français"]),
        ]
        
        scores = {}
        for domain, keywords in domains_to_check:
            score = sum(1 for kw in keywords if kw.lower() in input_lower)
            scores[domain] = score
        
        # Domaine par défaut: géométrie du spectre (si mentions spectrales)
        max_domain = max(scores, key=scores.get)
        
        if scores[max_domain] > 0:
            return max_domain
        
        # Si aucun keyword trouvé: OUT_OF_DOMAIN
        return Domain.OUT_OF_DOMAIN
    
    def _detect_intent(self, input_lower: str) -> RequestIntent:
        """Détecte le type d'intent dans la requête."""
        
        scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in input_lower)
            scores[intent] = score
        
        # Intent avec le plus de correspondances
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        # Par défaut: CONVERSATIONAL si mention du domaine
        return RequestIntent.CONVERSATIONAL
    
    def _calculate_confidence(self, user_input: str, domain: Domain, intent: RequestIntent) -> float:
        """Calcule confiance de la classification (0.0 à 1.0)."""
        
        confidence = 0.5
        input_lower = user_input.lower()
        
        # Bonus si longueur raisonnable
        if 10 < len(user_input) < 5000:
            confidence += 0.2
        
        # Bonus si bien formé (ponctuation, majuscules)
        if "?" in user_input or "." in user_input:
            confidence += 0.1
        
        # Bonus si mentions multiples du domaine
        domain_keywords = self.domain_keywords_spectral["français"]
        keyword_count = sum(1 for kw in domain_keywords if kw.lower() in input_lower)
        if keyword_count >= 3:
            confidence += 0.2
        
        # Bonus si intent explicite
        intent_keywords = self.intent_keywords[intent]
        intent_count = sum(1 for kw in intent_keywords if kw.lower() in input_lower)
        if intent_count >= 2:
            confidence += 0.1
        
        return min(confidence, 1.0)


class DomainValidationError(Exception):
    """Exception levée quand requête hors domaine."""
    pass


def validate_domain_request(user_input: str, classifier: Optional[DomainClassifier] = None) -> Tuple[Domain, RequestIntent, float]:
    """
    Valide qu'une requête respecte le domaine Gabriel.
    
    Levant DomainValidationError si rejet.
    Retournant (domain, intent, confidence) si acceptée.
    """
    if classifier is None:
        classifier = DomainClassifier()
    
    domain, intent, confidence, reason = classifier.classify(user_input)
    
    if domain == Domain.OUT_OF_DOMAIN or intent == RequestIntent.OUT_OF_DOMAIN:
        raise DomainValidationError(f"{reason}\n\nGabriel n'est disponible que pour: {[d.value for d in Domain if d != Domain.OUT_OF_DOMAIN]}")
    
    return domain, intent, confidence
