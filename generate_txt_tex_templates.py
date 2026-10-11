#!/usr/bin/env python3
"""
generate_txt_tex_templates.py

Genere 100 fichiers .txt et 100 fichiers .tex vierges pour Gabriel
Nomenclature: projet_uni_car_savard_01 a projet_uni_car_savard_100
"""

from pathlib import Path

# Dossiers de destination
BASE_DIR = Path(__file__).parent / "theories" / "projects"
TXT_DIR = BASE_DIR / "txt"
TEX_DIR = BASE_DIR / "tex"

TXT_DIR.mkdir(parents=True, exist_ok=True)
TEX_DIR.mkdir(parents=True, exist_ok=True)

# Template pour fichiers .txt
TXT_TEMPLATE = """================================================================================
Projet: {project_name}
Univers au Carre - Methode Spectrale Savard
================================================================================

Description: [A remplir par Gabriel/utilisateur]
Date creation: [A remplir]
Statut: [VIERGE/EN COURS/TERMINE]

================================================================================
CONTENU
================================================================================

[A remplir]

================================================================================
NOTES
================================================================================

[A remplir]

================================================================================
REFERENCES
================================================================================

[A remplir]

================================================================================
Fin du fichier {project_name}
================================================================================
"""

# Template pour fichiers .tex (LaTeX)
TEX_TEMPLATE = r"""% ============================================================
% Projet: {project_name}
% Univers au Carre - Methode Spectrale Savard
% ============================================================

\documentclass[12pt]{{article}}
\usepackage[utf-8]{{inputenc}}
\usepackage[french]{{babel}}
\usepackage{{amsmath}}
\usepackage{{amssymb}}
\usepackage{{geometry}}

\geometry{{margin=1in}}

\title{{{project_name}}}
\author{{Gabriel - Univers au Carre}}
\date{{\today}}

\begin{{document}}

\maketitle

% ============================================================
% SECTION 1 : Introduction
% ============================================================

\section{{Introduction}}

% TODO: Ajouter le contenu d'introduction

% ============================================================
% SECTION 2 : Definition et Notation
% ============================================================

\section{{Definition et Notation}}

% TODO: Ajouter les definitions et notations

% ============================================================
% SECTION 3 : Theoreme Principal
% ============================================================

\section{{Theoreme Principal}}

% TODO: Ajouter le theoreme principal

\begin{{equation}}
% TODO: Ajouter l'equation
\end{{equation}}

% ============================================================
% SECTION 4 : Preuves
% ============================================================

\section{{Preuves}}

% TODO: Ajouter les preuves

% ============================================================
% SECTION 5 : Resultats et Discussion
% ============================================================

\section{{Resultats et Discussion}}

% TODO: Ajouter les resultats et la discussion

% ============================================================
% SECTION 6 : Conclusion
% ============================================================

\section{{Conclusion}}

% TODO: Ajouter la conclusion

% ============================================================
% REFERENCES
% ============================================================

\begin{{thebibliography}}{{99}}

% TODO: Ajouter les references

\end{{thebibliography}}

\end{{document}}
"""

def generate_txt_templates(start=1, end=100):
    """Genere les fichiers .txt vierges"""
    created = 0
    
    for i in range(start, end + 1):
        project_name = f"projet_uni_car_savard_{i:02d}"
        
        content = TXT_TEMPLATE.format(project_name=project_name)
        
        txt_file = TXT_DIR / f"{project_name}.txt"
        txt_file.write_text(content, encoding='utf-8')
        
        created += 1
        
        if i % 10 == 0 or i == 1 or i == end:
            print(f"OK - Cree TXT: {project_name}.txt ({i}/{end})")
    
    return created

def generate_tex_templates(start=1, end=100):
    """Genere les fichiers .tex vierges"""
    created = 0
    
    for i in range(start, end + 1):
        project_name = f"projet_uni_car_savard_{i:02d}"
        
        content = TEX_TEMPLATE.format(project_name=project_name)
        
        tex_file = TEX_DIR / f"{project_name}.tex"
        tex_file.write_text(content, encoding='utf-8')
        
        created += 1
        
        if i % 10 == 0 or i == 1 or i == end:
            print(f"OK - Cree TEX: {project_name}.tex ({i}/{end})")
    
    return created

if __name__ == "__main__":
    print("=" * 70)
    print("Generation des fichiers .txt et .tex vierges pour Gabriel")
    print("=" * 70)
    print()
    
    # Generer les fichiers .txt
    print("Fichiers .txt:")
    txt_count = generate_txt_templates(1, 100)
    print()
    
    # Generer les fichiers .tex
    print("Fichiers .tex:")
    tex_count = generate_tex_templates(1, 100)
    print()
    
    print("=" * 70)
    print(f"SUCCES!")
    print("=" * 70)
    print()
    print(f"Fichiers .txt crees: {txt_count}/100")
    print(f"  Location: theories/projects/txt/")
    print()
    print(f"Fichiers .tex crees: {tex_count}/100")
    print(f"  Location: theories/projects/tex/")
    print()
    print("Structure complete:")
    print("  theories/projects/")
    print("  ├── projet_uni_car_savard_*.thy (100 fichiers Isabelle)")
    print("  ├── txt/")
    print("  │   └── projet_uni_car_savard_*.txt (100 fichiers texte)")
    print("  └── tex/")
    print("      └── projet_uni_car_savard_*.tex (100 fichiers LaTeX)")
    print()
    print("Dans le conteneur Docker:")
    print("  /theories/projects/")
    print("  ├── projet_uni_car_savard_*.thy")
    print("  ├── txt/projet_uni_car_savard_*.txt")
    print("  └── tex/projet_uni_car_savard_*.tex")
    print()
