#!/usr/bin/env python3
"""
APPLY_VISION_PATCH_NOW.py - Applique les 3 modifications CLI pour image analysis
Exécution directe : python APPLY_VISION_PATCH_NOW.py
"""

import os
import re
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

CLI_FILE = Path("src/ui/cli.py")
VISION_MODULE = Path("src/gabriel_vision_integration.py")

# Modifications à appliquer
MODIFICATIONS = [
    {
        "name": "MOD 1 - Ajouter imports (ligne ~20)",
        "search_pattern": r"(import asyncio\s+import logging\s+import os\s+import sys\s+import time)",
        "replacement": r"\1\nimport re\nfrom pathlib import Path as PathlibPath",
    },
    {
        "name": "MOD 2 - Ajouter import GabrielVisionIntegration (après imports existants)",
        "search_pattern": r"(from rich\.panel import Panel)",
        "replacement": r"\1\n\n# === IMAGE ANALYSIS INTEGRATION ===\nVISION_AVAILABLE = False\ntry:\n    from src.gabriel_vision_integration import GabrielVisionIntegration\n    VISION_AVAILABLE = True\nexcept ImportError as _e:\n    GabrielVisionIntegration = None",
    },
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def apply_modifications(cli_path: Path) -> bool:
    """Applique les modifications au fichier cli.py."""
    if not cli_path.exists():
        print(f"❌ ERREUR : {cli_path} introuvable")
        return False
    
    with open(cli_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Vérifier si déjà patché
    if "IMAGE ANALYSIS INTEGRATION" in content and "GabrielVisionIntegration" in content:
        print("✅ CLI déjà patché (GabrielVisionIntegration trouvé)")
        return True
    
    # MOD 1 : Ajouter imports
    print("\n[MOD 1] Ajout des imports...")
    if "import re" not in content:
        # Chercher la ligne 'import asyncio'
        if "import asyncio" in content:
            content = content.replace(
                "import asyncio",
                "import re\nimport asyncio"
            )
            print("  ✓ Import 're' ajouté")
        
        if "from pathlib import Path as PathlibPath" not in content and "PathlibPath" not in content:
            # Ajouter après les autres imports Path
            if "from pathlib import Path" in content:
                content = content.replace(
                    "from pathlib import Path",
                    "from pathlib import Path, Path as PathlibPath"
                )
                print("  ✓ Path alias ajouté")
            else:
                # Ajouter après 'import os'
                if "import os" in content:
                    content = content.replace(
                        "import os",
                        "import os\nfrom pathlib import Path as PathlibPath"
                    )
                    print("  ✓ Path import ajouté")
    
    # MOD 2 : Ajouter GabrielVisionIntegration import
    print("\n[MOD 2] Ajout de GabrielVisionIntegration...")
    if "GabrielVisionIntegration" not in content:
        # Chercher 'from rich.panel import Panel'
        vision_import_block = """
# === IMAGE ANALYSIS INTEGRATION ===
VISION_AVAILABLE = False
try:
    from src.gabriel_vision_integration import GabrielVisionIntegration
    VISION_AVAILABLE = True
except ImportError as _e:
    GabrielVisionIntegration = None
"""
        
        if "from rich.panel import Panel" in content:
            content = content.replace(
                "from rich.panel import Panel",
                "from rich.panel import Panel" + vision_import_block
            )
            print("  ✓ Import GabrielVisionIntegration ajouté")
        else:
            # Ajouter après 'from rich'
            match = re.search(r"(from rich\.[^\n]+\n)", content)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + vision_import_block + content[insert_pos:]
                print("  ✓ Import GabrielVisionIntegration ajouté (position auto)")
    
    # MOD 3 : Ajouter _handle_image_query() et hijack dans _handle_special()
    print("\n[MOD 3] Ajout de _handle_image_query() et hijack...")
    
    # 3a) Ajouter la méthode _handle_image_query AVANT _handle_special
    if "_handle_image_query" not in content:
        image_query_method = '''
    async def _handle_image_query(self, cmd: str) -> bool:
        """Traite les requêtes d'analyse d'image.
        
        Format : "analyse image C:\\\\chemin\\\\image.png"
        """
        if not VISION_AVAILABLE or GabrielVisionIntegration is None:
            console.print("\\n  [red]Module vision non disponible. Installez Pillow et numpy.[/red]\\n")
            return True
        
        # Extraire le chemin du fichier
        match = re.search(r"analyse\\s+image\\s+(.+?)(?:\\s*\\||\\s*$)", cmd, re.IGNORECASE)
        if not match:
            console.print("\\n  [yellow]Usage: analyse image <chemin_fichier>[/yellow]\\n")
            return True
        
        file_path_str = match.group(1).strip()
        try:
            file_path = PathlibPath(file_path_str)
            if not file_path.exists():
                console.print(f"\\n  [red]Fichier introuvable: {file_path}[/red]\\n")
                return True
            
            # Analyser l'image
            console.print(f"\\n  [cyan]🔍 Analyse de l'image...\\n")
            vision = GabrielVisionIntegration()
            report = vision.analyze_image(str(file_path))
            
            # Afficher le rapport
            console.print(Panel(
                report,
                title="[bold cyan]📊 Rapport d'Analyse d'Image[/bold cyan]",
                border_style="cyan",
            ))
            return True
        except Exception as e:
            console.print(f"\\n  [red]Erreur lors de l'analyse: {e}[/red]\\n")
            return True

'''
        # Trouver le début de _handle_special et insérer avant
        if "async def _handle_special" in content:
            special_match = re.search(r"(\s+async def _handle_special\()", content)
            if special_match:
                insert_pos = special_match.start()
                content = content[:insert_pos] + image_query_method + "\n" + content[insert_pos:]
                print("  ✓ Méthode _handle_image_query() ajoutée")
    
    # 3b) Ajouter le hijack dans _handle_special
    if "async def _handle_special" in content:
        # Chercher le corps de _handle_special
        match = re.search(r'(async def _handle_special\(self, cmd: str\) -> bool:)\s+"""', content)
        if match:
            # Ajouter après la docstring
            docstring_end = re.search(
                r'(async def _handle_special\(self, cmd: str\) -> bool:\s+""".*?""")',
                content,
                re.DOTALL
            )
            if docstring_end:
                insert_pos = docstring_end.end()
                hijack_code = '''

        # === IMAGE ANALYSIS HIJACK ===
        if re.search(r"analyse\\s+image", cmd, re.IGNORECASE):
            return await self._handle_image_query(cmd)
'''
                # Vérifier que le hijack n'existe pas déjà
                if "IMAGE ANALYSIS HIJACK" not in content:
                    content = content[:insert_pos] + hijack_code + content[insert_pos:]
                    print("  ✓ Hijack IMAGE ANALYSIS ajouté dans _handle_special()")
    
    # Sauvegarder
    if content != original_content:
        with open(cli_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("\n✅ Fichier cli.py modifié avec succès!")
        return True
    else:
        print("\n⚠️ Aucune modification n'a été appliquée")
        return False

def verify_vision_module() -> bool:
    """Vérifie que le module vision existe."""
    if VISION_MODULE.exists():
        size_kb = VISION_MODULE.stat().st_size / 1024
        print(f"✅ Module vision trouvé : {VISION_MODULE} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"❌ Module vision introuvable : {VISION_MODULE}")
        return False

def main():
    print("=" * 80)
    print("APPLY_VISION_PATCH_NOW - Patch direct pour Gabriel Vision Integration")
    print("=" * 80)
    
    # Changer de répertoire
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"\nRépertoire: {script_dir}")
    
    # Vérifications
    print("\n[VÉRIFICATIONS]")
    if not CLI_FILE.exists():
        print(f"❌ {CLI_FILE} introuvable")
        return False
    print(f"✅ CLI trouvé : {CLI_FILE}")
    
    if not verify_vision_module():
        return False
    
    # Appliquer les modifications
    print("\n[MODIFICATIONS]")
    if not apply_modifications(CLI_FILE):
        return False
    
    # Succès
    print("\n" + "=" * 80)
    print("✅ PATCH APPLIQUÉ AVEC SUCCÈS!")
    print("=" * 80)
    print("\nProchaines étapes:")
    print("  1. Installez les dépendances : pip install Pillow numpy")
    print("  2. Testez : python src/ui/cli.py")
    print("  3. Commande : gabriel> analyse image C:\\\\chemin\\\\image.png")
    print("\n")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
