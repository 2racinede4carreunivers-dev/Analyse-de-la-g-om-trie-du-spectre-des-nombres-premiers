#!/usr/bin/env python3
"""
gabriel_project_manager.py

Permet à Gabriel de gérer les 100 projets Isabelle
Démontre comment remplir un template et le vérifier
"""

from pathlib import Path
import subprocess
import time
from typing import Optional, Tuple

class GabrielProjectManager:
    """Gestionnaire de projets Isabelle pour Gabriel"""
    
    def __init__(self, projects_dir="/home/agent/app/theories/projects"):
        self.projects_dir = Path(projects_dir)
        self.generated_dir = self.projects_dir.parent / "generated"
        self.generated_dir.mkdir(parents=True, exist_ok=True)
    
    def list_all_projects(self) -> list:
        """Liste tous les 100 projets disponibles"""
        projects = sorted(self.projects_dir.glob("projet_uni_car_savard_*.thy"))
        return projects
    
    def find_next_available_project(self) -> Optional[Tuple[int, Path]]:
        """Trouve le prochain projet vierge disponible"""
        projects = self.list_all_projects()
        
        for project_file in projects:
            content = project_file.read_text(encoding='utf-8')
            # Vérifier si le projet contient toujours des TODO (vierge)
            if "TODO:" in content:
                # Extraire le numéro
                name = project_file.stem
                num = int(name.split("_")[-1])
                return num, project_file
        
        return None, None
    
    def get_project_by_number(self, project_num: int) -> Optional[Path]:
        """Récupère un projet par son numéro"""
        project_file = self.projects_dir / f"projet_uni_car_savard_{project_num:02d}.thy"
        if project_file.exists():
            return project_file
        return None
    
    def fill_project_from_template(
        self,
        template_num: int,
        definitions: str = "",
        lemmas: str = "",
        main_theorem: str = "",
        proof: str = ""
    ) -> Optional[Path]:
        """
        Remplit un template avec du contenu Isabelle
        
        Args:
            template_num: Numéro du template (1-100)
            definitions: Code pour la section Définitions
            lemmas: Code pour la section Lemmes
            main_theorem: Code pour le théorème principal
            proof: Code pour la preuve
        
        Returns:
            Chemin du fichier rempli
        """
        template_file = self.get_project_by_number(template_num)
        if not template_file:
            return None
        
        # Lire le template
        template_content = template_file.read_text(encoding='utf-8')
        
        # Remplacer les sections TODO
        filled_content = template_content
        
        if definitions:
            filled_content = filled_content.replace(
                "(* TODO: Ajouter les definitions *)",
                definitions
            )
        
        if lemmas:
            filled_content = filled_content.replace(
                "(* TODO: Ajouter les lemmes *)",
                lemmas
            )
        
        if main_theorem:
            filled_content = filled_content.replace(
                "(* TODO: Ajouter le theoreme principal *)",
                main_theorem
            )
        
        if proof:
            filled_content = filled_content.replace(
                "(* TODO: Ajouter les preuves *)",
                proof
            )
        
        # Sauvegarder dans le dossier /generated/
        output_file = self.generated_dir / f"execution_projet_{template_num:02d}.thy"
        output_file.write_text(filled_content, encoding='utf-8')
        
        return output_file
    
    def verify_with_isabelle(self, thy_file: Path) -> dict:
        """Vérifie un fichier .thy avec Isabelle CLI"""
        try:
            result = subprocess.run(
                ["isabelle", "process", "-o", "quick", "-T", str(thy_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "valid": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "file": str(thy_file),
                "timestamp": time.time()
            }
        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "output": "",
                "errors": "Timeout: Isabelle verification took too long",
                "file": str(thy_file),
                "timestamp": time.time()
            }
    
    def process_new_project(
        self,
        definitions: str = "",
        lemmas: str = "",
        main_theorem: str = "",
        proof: str = ""
    ) -> dict:
        """
        Workflow complet: Trouver template → Remplir → Vérifier
        
        Returns:
            Dict avec résultats
        """
        # 1. Trouver un template vierge
        project_num, template_file = self.find_next_available_project()
        
        if project_num is None:
            return {
                "success": False,
                "error": "Aucun projet vierge disponible (tous les 100 sont utilisés)",
                "project_num": None
            }
        
        print(f"[1] Template trouvé: {template_file.name} (projet #{project_num})")
        
        # 2. Remplir le template
        filled_file = self.fill_project_from_template(
            project_num,
            definitions=definitions,
            lemmas=lemmas,
            main_theorem=main_theorem,
            proof=proof
        )
        
        print(f"[2] Projet rempli: {filled_file.name}")
        
        # 3. Vérifier avec Isabelle
        verification = self.verify_with_isabelle(filled_file)
        
        print(f"[3] Vérification Isabelle: {'OK' if verification['valid'] else 'ERREUR'}")
        
        return {
            "success": True,
            "project_num": project_num,
            "template_file": str(template_file),
            "filled_file": str(filled_file),
            "verification": verification
        }


# ============================================================
# Exemple d'utilisation
# ============================================================

def main():
    print("=" * 70)
    print("Gabriel Project Manager - Demo")
    print("=" * 70)
    print()
    
    manager = GabrielProjectManager()
    
    # 1. Lister les projets
    all_projects = manager.list_all_projects()
    print(f"[1] Total de projets disponibles: {len(all_projects)}")
    print(f"    Premier: {all_projects[0].name}")
    print(f"    Dernier: {all_projects[-1].name}")
    print()
    
    # 2. Trouver le prochain projet vierge
    next_num, next_file = manager.find_next_available_project()
    if next_num:
        print(f"[2] Prochain projet disponible: #{next_num}")
        print(f"    Fichier: {next_file.name}")
    print()
    
    # 3. Exemple: Remplir un projet avec du contenu
    print("[3] Exemple: Remplir un projet...")
    
    # Contenu exemple: Vérifier que 97 est premier
    example_theorem = """
    theorem p_97_is_prime: "prime 97" by
      (norm_num using prime_list)
    """
    
    result = manager.process_new_project(
        definitions="definition is_odd (n : nat) := n mod 2 = 1",
        main_theorem=example_theorem,
        proof="simp"
    )
    
    if result["success"]:
        print()
        print("Résultat:")
        print(f"  Project #: {result['project_num']}")
        print(f"  Fichier rempli: {result['filled_file']}")
        print(f"  Vérification: {'VALIDE' if result['verification']['valid'] else 'ERREUR'}")
        if not result['verification']['valid']:
            print(f"  Erreurs: {result['verification']['errors'][:100]}")
    else:
        print(f"  Erreur: {result['error']}")
    
    print()
    print("=" * 70)
    print("Gabriel peut maintenant utiliser ces templates automatiquement!")
    print("=" * 70)


if __name__ == "__main__":
    # Note: Pour tester en dehors du conteneur, assure-toi que:
    # 1. Isabelle est installé sur le système
    # 2. Les fichiers .thy sont accessibles à /theories/projects/
    # 
    # Pour tester dans le conteneur:
    # docker exec llm-agent-multiloop-run python3 src/adapters/gabriel_project_manager.py
    
    main()
