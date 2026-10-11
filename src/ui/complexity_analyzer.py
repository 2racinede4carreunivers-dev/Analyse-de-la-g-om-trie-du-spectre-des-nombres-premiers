"""
Analyseur de Complexité pour Gabriel Multiloop.

Détermine automatiquement:
  - Le nombre de loops nécessaires (1 à 4)
  - Le mode de réponse (Rapide vs Complet)
  - Les domaines concernés

Basé sur:
  1. Nombre de concepts détectés
  2. Profondeur de la question
  3. Nombres de valeurs numériques
  4. Intention détectée
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ResponseMode(Enum):
    """Mode de réponse automatiquement détecté."""
    RAPIDE = "rapide"          # 1 loop → ~5-10 secondes
    STANDARD = "standard"       # 2 loops → ~15-20 secondes
    APPROFONDI = "approfondi"   # 3 loops → ~25-35 secondes
    TRES_COMPLEXE = "très_complexe"  # 4 loops → ~40-60 secondes


@dataclass
class ComplexityProfile:
    """Profil de complexité détecté pour une requête."""
    mode: ResponseMode
    num_loops: int  # 1, 2, 3 ou 4
    confidence: float  # 0.0 à 1.0
    
    # Détails
    complexity_score: float  # 0-100
    factors: list[str]  # raisons de la complexité détectée
    estimated_duration_sec: int  # estimation en secondes
    can_use_fast_mode: bool  # peut répondre immédiatement
    
    # Recommandations
    recommendation: str


class ComplexityAnalyzer:
    """Analyseur de complexité des requêtes Gabriel."""

    # Mots-clés indicateurs de complexité
    LOW_COMPLEXITY = [
        r"\b(?:qui|quoi|où|quand|quel)\b",
        r"\b(?:definition|explique|c'est quoi)\b",
        r"\b(?:premier|nombre premier)\b",
        r"\b(?:simple|basique|facile)\b",
    ]

    MEDIUM_COMPLEXITY = [
        r"\b(?:reconstruis|retrouve|calcul)\b",
        r"\b(?:position|rang|index)\b",
        r"\b(?:verif|check|valide)\b",
        r"\b(?:compare|comparer)\b",
    ]

    HIGH_COMPLEXITY = [
        r"\b(?:rapport|ratio|RsP)\b",
        r"\b(?:ecart|gap)\b",
        r"\b(?:equation|formula|equation)\b",
        r"\b(?:symetrique|asymetrique|configuration)\b",
    ]

    VERY_HIGH_COMPLEXITY = [
        r"\b(?:methode spectrale|spectral method)\b",
        r"\b(?:zeta|riemann|chebyshev|tchebychev)\b",
        r"\b(?:psi_savard|psi-savard)\b",
        r"\b(?:section\s+13|pont\s+logique)\b",
        r"\b(?:plusieurs|multi|multiple)\b.*\b(?:objectif|objective)\b",
    ]

    def __init__(self):
        self.complexity_cache = {}

    def analyze(self, question: str, intent: Optional[str] = None) -> ComplexityProfile:
        """Analyse la complexité d'une requête et recommande le nombre de loops."""
        
        # Cache pour éviter les recalculs
        cache_key = hash(question)
        if cache_key in self.complexity_cache:
            return self.complexity_cache[cache_key]

        q_low = question.lower()
        
        # 1. Calculer le score de complexité (0-100)
        score = self._calculate_complexity_score(q_low)
        
        # 2. Détecter les facteurs de complexité
        factors = self._detect_factors(q_low, intent)
        
        # 3. Dériver le mode et nombre de loops
        mode, num_loops, confidence = self._derive_mode(score, factors, intent)
        
        # 4. Estimer la durée
        estimated_duration = self._estimate_duration(num_loops)
        
        # 5. Déterminer si mode rapide est possible
        can_fast = (
            score < 25 
            and len(factors) <= 2
            and intent in (None, "unknown", "general")
        )
        
        # 6. Générer recommandation
        recommendation = self._generate_recommendation(mode, factors, can_fast)
        
        profile = ComplexityProfile(
            mode=mode,
            num_loops=num_loops,
            confidence=confidence,
            complexity_score=score,
            factors=factors,
            estimated_duration_sec=estimated_duration,
            can_use_fast_mode=can_fast,
            recommendation=recommendation,
        )
        
        self.complexity_cache[cache_key] = profile
        return profile

    def _calculate_complexity_score(self, question_low: str) -> float:
        """Calcule un score de complexité (0-100)."""
        score = 0.0
        
        # Longueur de la question (bonus si longue)
        words = len(question_low.split())
        score += min(words / 20, 10)  # max 10 points
        
        # Nombre de valeurs numériques
        numbers = len(re.findall(r'-?\d+', question_low))
        score += min(numbers * 3, 20)  # max 20 points
        
        # Nombre de signes mathématiques
        math_symbols = len(re.findall(r'[+\-*/=()]', question_low))
        score += min(math_symbols * 2, 15)  # max 15 points
        
        # Connecteurs logiques (et, ou, mais, si...)
        connectors = len(re.findall(
            r'\b(?:et|ou|mais|si|alors|donc|car|parce que|bien que)\b',
            question_low
        ))
        score += min(connectors * 4, 15)  # max 15 points
        
        # Mots complexes
        complex_words = len([
            w for w in question_low.split()
            if len(w) > 12  # mots longs = concepts complexes
        ])
        score += min(complex_words * 2, 10)  # max 10 points
        
        # Points bonus pour patterns très complexes
        if re.search(r'(?:symetrique|asymetrique).*\d+\s*[x*]\s*\d+', question_low):
            score += 15
        
        if re.search(r'bloc\s*[ab]\s*=.*bloc\s*[ab]\s*=', question_low):
            score += 10
        
        if len(re.findall(r'[{}()\[\]]', question_low)) > 4:
            score += 8  # beaucoup de parenthèses = structure complexe
        
        return min(score, 100.0)

    def _detect_factors(self, question_low: str, intent: Optional[str]) -> list[str]:
        """Détecte les facteurs spécifiques de complexité."""
        factors = []
        
        # Intention
        if intent == "reconstruction":
            factors.append("reconstruction de nombre premier")
        elif intent == "ratio_spectral":
            factors.append("calcul de rapport spectral")
        elif intent == "gap":
            factors.append("calcul d'écart entre nombres premiers")
        elif intent == "theoretical_advanced":
            factors.append("question théorique avancée (Section 13)")
        
        # Patterns
        if re.search(r'plusieurs|multi', question_low):
            factors.append("requête multi-objectifs")
        
        if re.search(r'(?:symetrique|asymetrique).*\d+\s*[x*]\s*\d+', question_low):
            factors.append("configuration n×m explicite")
        
        if re.search(r'bloc\s*[ab]\s*=', question_low):
            factors.append("tuples nommés (Bloc A, Bloc B)")
        
        if re.search(r'nombres?\s+negatif', question_low):
            factors.append("nombres négatifs (domaine étendu)")
        
        if re.search(r'verif|valid|check|confirm', question_low):
            factors.append("vérification/validation demandée")
        
        if re.search(r'compare|compara|difference|ecart', question_low):
            factors.append("comparaison ou analyse différentielle")
        
        # Complexité théorique
        if re.search(r'zeta|riemann|chebyshev|psi_savard', question_low):
            factors.append("théorie analytique des nombres (Zêta, Chebyshev)")
        
        if re.search(r'equation|formula|preuve|demonstration', question_low):
            factors.append("démonstration/preuve formelle")
        
        return factors

    def _derive_mode(
        self,
        score: float,
        factors: list[str],
        intent: Optional[str],
    ) -> tuple[ResponseMode, int, float]:
        """Dérive le mode de réponse et le nombre de loops."""
        
        # Matrice score -> mode
        if score < 20:
            mode = ResponseMode.RAPIDE
            num_loops = 1
            confidence = 0.95
        elif score < 40:
            mode = ResponseMode.STANDARD
            num_loops = 2
            confidence = 0.90
        elif score < 65:
            mode = ResponseMode.APPROFONDI
            num_loops = 3
            confidence = 0.85
        else:
            mode = ResponseMode.TRES_COMPLEXE
            num_loops = 4
            confidence = 0.80
        
        # Ajustements selon les facteurs
        if "multi-objectifs" in factors:
            num_loops = min(4, num_loops + 1)
            confidence = max(0.75, confidence - 0.05)
        
        if "théorie analytique" in factors:
            num_loops = min(4, num_loops + 1)
            confidence = max(0.70, confidence - 0.10)
        
        # Downgrade si nombre insuffisant de facteurs
        if len(factors) <= 1 and score < 30:
            num_loops = 1
            mode = ResponseMode.RAPIDE
        
        return mode, num_loops, confidence

    def _estimate_duration(self, num_loops: int) -> int:
        """Estime la durée en secondes."""
        # Temps par loop (approximatif)
        base_times = {
            1: 8,    # Rapide: ~8-10 sec
            2: 18,   # Standard: ~15-20 sec
            3: 30,   # Approfondi: ~25-35 sec
            4: 50,   # Très complexe: ~40-60 sec
        }
        return base_times.get(num_loops, 30)

    def _generate_recommendation(
        self,
        mode: ResponseMode,
        factors: list[str],
        can_fast: bool,
    ) -> str:
        """Génère une recommandation textuelle."""
        
        if can_fast:
            return "Mode RAPIDE recommandé. Réponse directe sans itérations."
        
        mode_names = {
            ResponseMode.RAPIDE: "Mode RAPIDE",
            ResponseMode.STANDARD: "Mode STANDARD",
            ResponseMode.APPROFONDI: "Mode APPROFONDI",
            ResponseMode.TRES_COMPLEXE: "Mode TRÈS COMPLEXE",
        }
        
        mode_name = mode_names[mode]
        factors_str = " + ".join(factors[:3]) if factors else "complexité générale"
        
        return f"{mode_name} recommandé ({factors_str}). Gabriel exécutera {len(factors)} étapes de raffinement."

    def suggest_fast_response(self, question: str) -> Optional[str]:
        """Suggère une réponse rapide si possible."""
        profile = self.analyze(question)
        
        if not profile.can_use_fast_mode:
            return None
        
        # Patterns pour réponses rapides
        if "qui est" in question.lower() or "c'est quoi" in question.lower():
            return "réponse définitionnelle directe"
        
        if "explique" in question.lower():
            return "explication rapide sans calcul"
        
        if "premier premier" in question.lower() or "2" in question:
            return "réponse sur le 1er nombre premier (2)"
        
        return "réponse simple sans multiloop"
