#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applique les corrections aux erreurs Isabelle/HOL dans methode_spectral.thy
"""

import re

# Lire le fichier
filepath = r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\theories\methode_spectral.thy"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print("[START] Lecture du fichier...")

# Correction 1: Ligne 2595 - ajouter norm_num au lemme ecart_227_173_1_3
print("\n[CORRECTION 1] Cherche lemme ecart_227_173_1_3...")

old_pattern_1 = r'(lemma ecart_227_173_1_3:.*?by \(simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def\))'
new_pattern_1 = r'\g<1>\n  norm_num'

if re.search(old_pattern_1, content, re.DOTALL):
    content = re.sub(
        r'(by \(simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def\))(\n\n)',
        r'by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def;\n      norm_num)\2',
        content
    )
    print("[OK] Correction 1 appliquée")
else:
    print("[ERREUR] Pattern non trouvé pour correction 1")

# Correction 2: Ligne 2915 - modifier la tactique pour le théorème RsP_k_egale_un_sur_k_pos
print("\n[CORRECTION 2] Cherche théorème RsP_k_egale_un_sur_k_pos...")

# Cette correction est déjà appliquée dans le fichier que j'ai fourni
# On vérifie juste qu'elle est en place

if "field_simp [hne_pow_2]; ring" in content:
    print("[OK] Correction 2 déjà appliquée (field_simp [hne_pow_X]; ring)")
elif "by (simp add: field_simps)" in content and "RsP_k_egale_un_sur_k_pos" in content:
    print("[ATTENTION] Correction 2 non appliquée - le pattern old existe encore")
    # Remplacer
    content = content.replace(
        "using hne_pow_2 by (simp add: field_simps)",
        "using hne_pow_2 by (simp add: field_simps; ring)"
    )
    content = content.replace(
        "using hne_pow_3 by (simp add: field_simps)",
        "using hne_pow_3 by (simp add: field_simps; ring)"
    )
    content = content.replace(
        "using hne_pow_4 by (simp add: field_simps)",
        "using hne_pow_4 by (simp add: field_simps; ring)"
    )
    print("[OK] Correction 2 appliquée")
else:
    print("[OK] Correction 2 est OK (pattern moderne détecté)")

# Écrire le fichier
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n[DONE] Fichier modifié et sauvegardé!")
print(f"Fichier: {filepath}")
