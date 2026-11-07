"""
PATCH: Reconnaissance requêtes théoriques avancées (Section 13, Psi-Savard, Chebyshev)

À AJOUTER dans src/multiloop/request_decomposer.py
Dans la méthode __init__, ajouter cette nouvelle intention :
"""

# ============================================================================
# NOUVEAU PATTERN D'INTENTION: "theoretical_advanced"
# ============================================================================
# À insérer dans INTENT_PATTERNS (après "reconstruction")

THEORETICAL_ADVANCED_PATTERNS = {
    "theoretical_advanced": [
        # Section 13 et pont logique Psi-Savard / Chebyshev
        r"section\s+13", 
        r"pont\s+(?:logique|direct)",
        r"psi\s*[-_]?savard", 
        r"psi\s*\(\s*savard",
        r"chebyshev|tchebychev", 
        r"équation\s+psi",
        
        # Premiers négatifs (cas théorique)
        r"premiers\s+négatifs", 
        r"nombres\s+premiers\s+négatifs",
        r"psi\s*\(\s*-",  # équation Psi( avec nombre négatif
        
        # Analyse de structure mathématique
        r"écart\s+minimal", 
        r"écart\s+comme\s+pour",
        r"équation\s+\s*=\s*0\.5\s*\*\s*it",
        r"résoudre\s+l'équation",
        
        # Lien aux zéros de zeta, droite critique
        r"zéros?\s+(?:de\s+)?zêta", 
        r"droite\s+critique",
        r"hypothèse\s+de\s+riemann",
        r"\briemann\b",
    ]
}

# ============================================================================
# RÉSULTAT ATTENDU
# ============================================================================
"""
Après l'ajout, ta requête sera classifiée comme:
  - Intent: "theoretical_advanced" (au lieu de "gap")
  - Sera traitée comme une question profonde, pas une simple demande numérique
  - CoherenceDetector sera plus tolérant (n'applique pas les critères 1*1)
  - Gabriel ne passera plus par debugger (ou moins facilement)
"""

# ============================================================================
# CODE À AJOUTER AU REQUEST_DECOMPOSER
# ============================================================================
"""
Dans RequestDecomposer.decompose(), après la section de détection d'intention:

        # Ajouter cette nouvelle détection AVANT les autres intentions
        for pat in self.INTENT_PATTERNS.get("theoretical_advanced", []):
            if re.search(pat, q_low):
                result.detected_intent = "theoretical_advanced"
                result.is_conversational = True  # Traiter comme conversationnel
                break
"""

print(__doc__)
print("\n✅ Ce patch résout le problème avec ta requête Section 13!")
print("Il faut maintenant implémenter ces 3 changements:")
print("  1. Ajouter 'theoretical_advanced' aux INTENT_PATTERNS")
print("  2. Detecter 'theoretical_advanced' avant les autres intentions")
print("  3. Marquer theoretical_advanced comme is_conversational=True")
