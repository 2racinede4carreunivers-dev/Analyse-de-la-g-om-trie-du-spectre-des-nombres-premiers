#!/usr/bin/env python3
"""Script pour ajouter les patterns théoriques au request_decomposer"""

import re

# Lire le fichier
with open(r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Chercher INTENT_PATTERNS et reconstruction
pattern_to_find = '''    INTENT_PATTERNS = {
        "reconstruction": ['''

pattern_replacement = '''    INTENT_PATTERNS = {
        "theoretical_advanced": [
            # Section 13 et pont logique Psi-Savard / Chebyshev
            r"section\\s+13", r"pont\\s+(?:logique|direct)",
            r"psi\\s*[-_]?savard", r"psi\\s*\\(\\s*savard",
            r"chebyshev|tchebychev", r"équation\\s+psi",
            # Premiers négatifs (cas théorique avancé)
            r"premiers\\s+négatifs", r"nombres\\s+premiers\\s+négatifs",
            r"psi\\s*\\(\\s*-",
            # Analyse de structure mathématique
            r"écart\\s+minimal", r"écart\\s+comme\\s+pour",
            r"équation\\s+\\s*=\\s*0\\.5\\s*\\*\\s*it",
            r"résoudre\\s+l'équation",
            # Lien aux zéros de zeta, droite critique
            r"zéros?\\s+(?:de\\s+)?zêta", r"droite\\s+critique",
            r"hypothèse\\s+de\\s+riemann", r"\\briemann\\b",
        ],
        "reconstruction": ['''

if pattern_to_find in content:
    content = content.replace(pattern_to_find, pattern_replacement)
    print("✅ Patterns théoriques ajoutés!")
else:
    print("❌ Pattern de remplacement non trouvé")
    print("Contenu recherché:")
    print(repr(pattern_to_find[:100]))

# Maintenant il faut aussi marquer les requêtes théoriques comme conversationnelles
# Trouver la section de détection d'intention dans decompose()
detection_section = '''        # 1. Detecter l'intention
        for intent, patterns in self.INTENT_PATTERNS.items():'''

detection_replacement = '''        # 0.ter Detecter les requetes THEORIQUES AVANCEES 
        # (Section 13, Psi-Savard, Chebyshev, etc.)
        # Ces requetes doivent être traitées comme conversationnelles.
        for pat in self.INTENT_PATTERNS.get("theoretical_advanced", []):
            if re.search(pat, q_low):
                result.detected_intent = "theoretical_advanced"
                result.is_conversational = True
                break

        # 1. Detecter l'intention (autres types)
        if result.detected_intent == "unknown":
            for intent, patterns in self.INTENT_PATTERNS.items():'''

if detection_section in content:
    content = content.replace(detection_section, detection_replacement)
    print("✅ Détection théorique avancée ajoutée!")
else:
    print("❌ Section de détection non trouvée")

# Écrire le fichier modifié
with open(r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ request_decomposer.py modifié avec succès!")
