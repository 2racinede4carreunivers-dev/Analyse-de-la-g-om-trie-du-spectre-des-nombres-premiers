#!/usr/bin/env python3
"""
generate_thy_templates.py

Genere 100 fichiers .thy vierges pour Gabriel
Nomenclature: projet_uni_car_savard_01 a projet_uni_car_savard_100
"""

from pathlib import Path

# Dossier de destination
THEORIES_DIR = Path(__file__).parent / "theories" / "projects"
THEORIES_DIR.mkdir(parents=True, exist_ok=True)

# Template vierge pour chaque fichier
TEMPLATE = """(* ============================================================
 * Projet: {project_name}
 * Univers au Carre - Methode Spectrale Savard
 * 
 * Description: [A remplir par Gabriel/utilisateur]
 * Date creation: [A remplir]
 * Statut: [VIERGE/EN COURS/TERMINE]
 * ============================================================ *)

theory {theory_name}
  imports Main
begin

(* ============================================================
 * SECTION 1 : Definitions
 * ============================================================ *)

(* TODO: Ajouter les definitions *)

(* ============================================================
 * SECTION 2 : Lemmes preliminaires
 * ============================================================ *)

(* TODO: Ajouter les lemmes *)

(* ============================================================
 * SECTION 3 : Theoreme principal
 * ============================================================ *)

(* TODO: Ajouter le theoreme principal *)

(* ============================================================
 * SECTION 4 : Preuves
 * ============================================================ *)

(* TODO: Ajouter les preuves *)

end
(* ============================================================
 * Fin du fichier {project_name}
 * ============================================================ *)
"""

def generate_templates(start=1, end=100):
    """Genere les fichiers .thy vierges"""
    created = 0
    
    for i in range(start, end + 1):
        # Nomenclature: projet_uni_car_savard_01 a projet_uni_car_savard_100
        project_name = f"projet_uni_car_savard_{i:02d}"
        theory_name = f"Savard_Project_{i:03d}"
        
        # Creer le contenu
        content = TEMPLATE.format(
            project_name=project_name,
            theory_name=theory_name
        )
        
        # Ecrire le fichier
        thy_file = THEORIES_DIR / f"{project_name}.thy"
        thy_file.write_text(content, encoding='utf-8')
        
        created += 1
        
        # Afficher la progression
        if i % 10 == 0 or i == 1 or i == end:
            print(f"OK - Cree: {project_name}.thy ({i}/{end})")
    
    return created

if __name__ == "__main__":
    print("=" * 70)
    print("Generation des fichiers .thy vierges pour Gabriel")
    print("=" * 70)
    print(f"Destination: {THEORIES_DIR}")
    print()
    
    created = generate_templates(1, 100)
    
    print()
    print("=" * 70)
    print(f"SUCCES - {created} fichiers crees!")
    print("=" * 70)
    print()
    print("Fichiers crees:")
    print(f"  - projet_uni_car_savard_001.thy")
    print(f"  - projet_uni_car_savard_002.thy")
    print(f"  - ...")
    print(f"  - projet_uni_car_savard_100.thy")
    print()
    print("Location: C:\\agent-multiloop-Gabriel-local-final\\agent-multiloop-Gabriel-local\\theories\\projects\\")
    print()
    print("Dans le conteneur:")
    print("  - /theories/projects/projet_uni_car_savard_001.thy")
    print("  - /theories/projects/projet_uni_car_savard_002.thy")
    print("  - ...")
    print()
    print("Gabriel peut utiliser ces fichiers pour les nouveaux projets!")
    print()
