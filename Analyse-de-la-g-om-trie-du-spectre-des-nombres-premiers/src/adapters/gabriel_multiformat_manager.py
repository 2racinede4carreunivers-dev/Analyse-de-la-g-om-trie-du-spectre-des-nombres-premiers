#!/usr/bin/env python3
"""
gabriel_multiformat_manager.py

Gère les projets multi-format pour Gabriel:
- .thy (Isabelle/HOL)
- .txt (Documentation texte)
- .tex (Documents LaTeX)
"""

from pathlib import Path
import subprocess
import json
from typing import Optional, Dict, Tuple

class GabrielMultiFormatManager:
    """Gestionnaire de projets multi-format pour Gabriel"""
    
    def __init__(self, projects_dir="/home/agent/app/theories/projects"):
        self.projects_dir = Path(projects_dir)
        self.thy_dir = self.projects_dir
        self.txt_dir = self.projects_dir / "txt"
        self.tex_dir = self.projects_dir / "tex"
        
        # Créer les répertoires s'ils n'existent pas
        self.txt_dir.mkdir(parents=True, exist_ok=True)
        self.tex_dir.mkdir(parents=True, exist_ok=True)
    
    def find_next_available_project(self) -> Optional[Tuple[int, Dict[str, Path]]]:
        """Trouve le prochain projet vierge disponible"""
        for i in range(1, 101):
            thy_file = self.thy_dir / f"projet_uni_car_savard_{i:02d}.thy"
            txt_file = self.txt_dir / f"projet_uni_car_savard_{i:02d}.txt"
            tex_file = self.tex_dir / f"projet_uni_car_savard_{i:02d}.tex"
            
            # Vérifier si tous les fichiers existent
            if thy_file.exists() and txt_file.exists() and tex_file.exists():
                # Vérifier s'ils sont vierges (contiennent TODO)
                thy_content = thy_file.read_text(encoding='utf-8')
                
                if "TODO:" in thy_content:
                    return i, {
                        "thy": thy_file,
                        "txt": txt_file,
                        "tex": tex_file
                    }
        
        return None, None
    
    def get_project_files(self, project_num: int) -> Optional[Dict[str, Path]]:
        """Récupère tous les fichiers d'un projet"""
        thy_file = self.thy_dir / f"projet_uni_car_savard_{project_num:02d}.thy"
        txt_file = self.txt_dir / f"projet_uni_car_savard_{project_num:02d}.txt"
        tex_file = self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.tex"
        
        if all(f.exists() for f in [thy_file, txt_file, tex_file]):
            return {
                "thy": thy_file,
                "txt": txt_file,
                "tex": tex_file
            }
        return None
    
    def fill_project(
        self,
        project_num: int,
        thy_content: str = "",
        txt_content: str = "",
        tex_content: str = ""
    ) -> Dict[str, str]:
        """
        Remplit un projet avec du contenu multi-format
        
        Args:
            project_num: Numéro du projet (1-100)
            thy_content: Contenu Isabelle
            txt_content: Contenu texte
            tex_content: Contenu LaTeX
        
        Returns:
            Dict avec chemin des fichiers générés
        """
        files = self.get_project_files(project_num)
        if not files:
            return {"error": f"Projet {project_num} non trouvé"}
        
        result = {}
        
        # Remplir .thy
        if thy_content:
            thy_template = files["thy"].read_text(encoding='utf-8')
            filled_thy = thy_template.replace(
                "TODO: Ajouter le theoreme principal",
                thy_content
            )
            files["thy"].write_text(filled_thy, encoding='utf-8')
            result["thy"] = str(files["thy"])
        
        # Remplir .txt
        if txt_content:
            txt_template = files["txt"].read_text(encoding='utf-8')
            filled_txt = txt_template.replace(
                "[A remplir]",
                txt_content,
                1  # Remplacer le premier occurrence dans CONTENU
            )
            files["txt"].write_text(filled_txt, encoding='utf-8')
            result["txt"] = str(files["txt"])
        
        # Remplir .tex
        if tex_content:
            tex_template = files["tex"].read_text(encoding='utf-8')
            filled_tex = tex_template.replace(
                "% TODO: Ajouter le theoreme principal",
                tex_content
            )
            files["tex"].write_text(filled_tex, encoding='utf-8')
            result["tex"] = str(files["tex"])
        
        return result
    
    def verify_thy_with_isabelle(self, project_num: int) -> Dict:
        """Vérifie le fichier .thy avec Isabelle CLI"""
        files = self.get_project_files(project_num)
        if not files:
            return {"valid": False, "error": f"Projet {project_num} non trouvé"}
        
        thy_file = files["thy"]
        
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
                "errors": result.stderr if result.returncode != 0 else "",
                "project_num": project_num,
                "file": str(thy_file)
            }
        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "output": "",
                "errors": "Timeout: Isabelle verification took too long",
                "project_num": project_num,
                "file": str(thy_file)
            }
        except Exception as e:
            return {
                "valid": False,
                "output": "",
                "errors": str(e),
                "project_num": project_num,
                "file": str(thy_file)
            }
    
    def compile_latex_to_pdf(self, project_num: int) -> Dict:
        """Compile le fichier .tex en PDF"""
        files = self.get_project_files(project_num)
        if not files:
            return {"success": False, "error": f"Projet {project_num} non trouvé"}
        
        tex_file = files["tex"]
        pdf_file = self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.pdf"
        
        try:
            # Tenter pdflatex
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", 
                 str(self.tex_dir), str(tex_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0 and pdf_file.exists()
            
            return {
                "success": success,
                "pdf_file": str(pdf_file) if success else None,
                "output": result.stdout,
                "errors": result.stderr if result.returncode != 0 else "",
                "project_num": project_num
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "pdf_file": None,
                "output": "",
                "errors": "Timeout: LaTeX compilation took too long",
                "project_num": project_num
            }
        except FileNotFoundError:
            return {
                "success": False,
                "pdf_file": None,
                "output": "",
                "errors": "pdflatex not found - install texlive-latex-base",
                "project_num": project_num
            }
        except Exception as e:
            return {
                "success": False,
                "pdf_file": None,
                "output": "",
                "errors": str(e),
                "project_num": project_num
            }
    
    def process_complete_project(
        self,
        thy_content: str = "",
        txt_content: str = "",
        tex_content: str = ""
    ) -> Dict:
        """
        Workflow complet:
        1. Trouver template vierge
        2. Remplir avec contenu
        3. Vérifier avec Isabelle
        4. Compiler LaTeX en PDF
        
        Returns:
            Dict avec résultats complets
        """
        # 1. Trouver un template vierge
        project_num, files = self.find_next_available_project()
        
        if project_num is None:
            return {
                "success": False,
                "error": "Aucun projet vierge disponible",
                "project_num": None
            }
        
        print(f"[1] Projet trouvé: #{project_num}")
        
        # 2. Remplir le projet
        filled = self.fill_project(project_num, thy_content, txt_content, tex_content)
        print(f"[2] Projet rempli: {project_num}")
        
        # 3. Vérifier Isabelle
        thy_verify = self.verify_thy_with_isabelle(project_num)
        print(f"[3] Vérification Isabelle: {'OK' if thy_verify['valid'] else 'ERREUR'}")
        
        # 4. Compiler LaTeX
        latex_compile = self.compile_latex_to_pdf(project_num)
        print(f"[4] Compilation LaTeX: {'OK' if latex_compile['success'] else 'SKIPPED'}")
        
        return {
            "success": True,
            "project_num": project_num,
            "filled_files": filled,
            "isabelle_verification": thy_verify,
            "latex_compilation": latex_compile,
            "project_files": {
                "thy": str(files["thy"]),
                "txt": str(files["txt"]),
                "tex": str(files["tex"]),
                "pdf": latex_compile.get("pdf_file")
            }
        }
    
    def export_project_manifest(self, project_num: int) -> Dict:
        """Exporte un manifeste JSON d'un projet"""
        files = self.get_project_files(project_num)
        if not files:
            return {"error": f"Projet {project_num} non trouvé"}
        
        manifest = {
            "project_num": project_num,
            "project_name": f"projet_uni_car_savard_{project_num:02d}",
            "files": {
                "thy": str(files["thy"]),
                "txt": str(files["txt"]),
                "tex": str(files["tex"]),
                "pdf": str(self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.pdf")
            },
            "content": {
                "thy": files["thy"].read_text(encoding='utf-8')[:200] + "...",
                "txt": files["txt"].read_text(encoding='utf-8')[:200] + "...",
                "tex": files["tex"].read_text(encoding='utf-8')[:200] + "..."
            }
        }
        
        return manifest


# ============================================================
# Exemple d'utilisation
# ============================================================

def main():
    print("=" * 70)
    print("Gabriel Multi-Format Manager - Demo")
    print("=" * 70)
    print()
    
    manager = GabrielMultiFormatManager()
    
    # Trouver le prochain projet
    project_num, files = manager.find_next_available_project()
    if project_num:
        print(f"[1] Prochain projet disponible: #{project_num}")
        print()
        
        # Exemple de contenu
        thy_content = "theorem p_101_is_prime: \"prime 101\" by trivial"
        txt_content = "101 est le 26ème nombre premier selon la méthode spectrale Savard."
        tex_content = r"\[P_{26} = 101\]"
        
        # Traiter le projet complet
        result = manager.process_complete_project(thy_content, txt_content, tex_content)
        
        print()
        print("Résultat:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Aucun projet vierge trouvé")
    
    print()


if __name__ == "__main__":
    main()
