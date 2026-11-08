#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction DÉFINITIVE de la ligne 2605 - methode_spectral.thy
"""

filepath = r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\theories\methode_spectral.thy"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("[START] Lecture du fichier...")

# CORRECTION UNIQUE: Remplacer la tactique échouée
# Avant (ligne 2608):
old_tactic = "by (simp add: hnum hden)"

# Après (tactique correcte):
new_tactic = "by (simp only: hnum hden; ring)"

if old_tactic in content:
    # Vérifier le contexte (doit être après "show ?thesis")
    if "show ?thesis\n      " + old_tactic in content:
        content = content.replace(
            "show ?thesis\n      " + old_tactic,
            "show ?thesis\n      " + new_tactic
        )
        print("[OK] Correction appliquée: by (simp only: hnum hden; ring)")
    else:
        print("[ERREUR] Contexte 'show ?thesis' non trouvé")
else:
    print(f"[ATTENTION] Ancien texte non trouvé: {old_tactic}")
    print("Vérification du contexte actuel...")
    
    # Chercher la ligne problématique
    if "show ?thesis" in content:
        pos = content.find("show ?thesis")
        print(f"Contexte trouvé à position {pos}")
        print(content[pos:pos+200])

# Sauvegarder
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("[DONE] Fichier modifié")
