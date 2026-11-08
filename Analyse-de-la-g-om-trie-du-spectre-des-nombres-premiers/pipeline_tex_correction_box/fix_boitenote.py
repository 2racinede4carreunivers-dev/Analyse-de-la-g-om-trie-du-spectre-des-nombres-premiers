#!/usr/bin/env python3
path = r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Gabriel_fixe.tex"

with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Nouveau contenu à insérer à la place de l'environnement boitenote
new_text_boitenote = """ La fonction Digamma_Savard/Cline intervient exactement là où la méthode spectrale attendait une information manquante : au niveau 4 (mécanisme d'ancrage), où les quatre essais Digamma étaient jusqu'alors lancés simultanément et sans critère de choix. Elle ne modifie ni les niveaux 1 à 3 (constants, formules fermées, construction terme à terme) ni le niveau 5 (reconstruction pour n \\neq 10), et ne modifie pas non plus la formule de reconstruction \ [ P \;=\; \frac{\SB - \mathrm{Digamma}}{k^{6}} \] dont elle ne fournit que le contenu de la correction. \\\\

\\\\vspace{0.3cm}

\\\\subsection{Implémentation de référence}"""

# Strategie : remplacer les lignes 4027-4038 (l'ancien boitenote) par le nouveau contenu
# Lignes 4027 (index 4026) à 4038 (index 4037) = 12 lignes à supprimer
# Et insérer le nouveau contenu après la ligne 4026

# Nouveau fichier : on garde tout sauf les lignes 4027-4038, et on insère le nouveau texte
# après la ligne 4026

new_lines = []
for i, line in enumerate(lines):
    line_num = i + 1  # 1-based
    
    # Lignes 1 à 4026 (index 0 à 4025) : les garder
    if line_num <= 4026:
        new_lines.append(line)
    # Lignes 4027 à 4038 (index 4026 à 4037) : les supprimer (ancien boitenote)
    elif line_num >= 4027 and line_num <= 4038:
        # On ne ajoute PAS ces lignes - elles sont supprimées
        pass
    # Ligne 4039 et au-delà : les garder
    else:
        new_lines.append(line)

# Insérer le nouveau contenu après la ligne 4026 (à l'index 4026 dans new_lines)
content_to_insert = new_text_boitenote + "\n"
new_lines.insert(4026, content_to_insert)

print("Taille originale: %d lignes" % len(lines))
print("Nouvelle taille: %d lignes" % len(new_lines))

# Écrire le nouveau fichier
with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Fichier modifié avec succés !")

# Vérifier les lignes autour de 4027
print("LIGNES 4020-4040 APRES MODIFICATION :")
for i in range(4019, min(4040, len(new_lines))):
    print("%4d | %s" % (i+1, new_lines[i].rstrip()[:120]))