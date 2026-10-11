#!/usr/bin/env python3
"""
DEPLOYMENT PATCH - Image Analysis Integration for Gabriel CLI
Applique les 3 modifications nécessaires à src/ui/cli.py
"""

import re
import sys
from pathlib import Path

def apply_cli_patch(cli_path: str) -> bool:
    """Applique les 3 modifications à cli.py"""
    
    with open(cli_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"[1/3] Vérification du fichier: {cli_path}")
    if not content:
        print("❌ Fichier vide!")
        return False
    
    # ========================================================================
    # MODIFICATION 1: Ajouter les imports (après les imports existants)
    # ========================================================================
    
    print("[2/3] Ajout des imports vision...")
    
    imports_to_add = """
# ============================================================================
# IMAGE ANALYSIS INTEGRATION (NEW)
# ============================================================================

import re
from pathlib import Path

try:
    from .gabriel_vision_integration import GabrielVisionIntegration, ImageAnalysisType
    VISION_AVAILABLE = True
    logger.info("[Gabriel Vision] Module loaded successfully")
except ImportError as e:
    VISION_AVAILABLE = False
    logger.warning(f"[Gabriel Vision] Not available: {e}")
"""
    
    # Chercher le premier `async def` ou `class` pour savoir où ajouter les imports
    if "IMAGE ANALYSIS INTEGRATION" not in content:
        # Trouver une bonne position (après les imports existants)
        match = re.search(r'(^from rich\..*?\n)(\nclass CLIInterface)', content, re.MULTILINE)
        if match:
            insert_point = match.end(1)
            content = content[:insert_point] + imports_to_add + content[insert_point:]
            print("  ✅ Imports ajoutés")
        else:
            print("  ⚠️ Point d'insertion d'imports non trouvé")
    else:
        print("  ✅ Imports déjà présents")
    
    # ========================================================================
    # MODIFICATION 2: Ajouter la méthode _handle_image_query() dans CLIInterface
    # ========================================================================
    
    print("[3/3] Ajout de la méthode _handle_image_query()...")
    
    new_method = '''
    async def _handle_image_query(self, query: str) -> bool:
        """
        Handle image analysis requests.
        Detects: "analyse image C:\\\\path\\\\to\\\\image.png"
        """
        
        if not VISION_AVAILABLE:
            console.print(
                "\\n  [yellow]❌ Vision module not available.[/yellow]\\n"
                "  [dim]Install: pip install Pillow numpy[/dim]\\n"
            )
            return False
        
        vision = GabrielVisionIntegration()
        
        if not vision.is_image_query(query):
            return False
        
        image_path = vision.extract_image_path(query)
        if not image_path:
            console.print("\\n  [yellow]⚠️ No image path detected.[/yellow]\\n")
            return False
        
        image_file = Path(image_path)
        if not image_file.exists():
            console.print(f"\\n  [red]❌ Not found: {image_path}[/red]\\n")
            return False
        
        try:
            console.print("\\n  [dim]🔍 Analyzing image...[/dim]\\n")
            
            result = await vision.analyze_image(image_path, query)
            
            if result.get('success'):
                console.print(Panel(
                    result.get('report', 'Analysis complete'),
                    title="[cyan]📸 Image Analysis[/cyan]",
                    border_style="cyan",
                    padding=(1, 2),
                ))
                
                confidence = result.get('confidence', 0.0)
                console.print(
                    f"\\n  [green]✅ Confidence: {confidence:.1f}/10\\n"
                    f"  [green]Source: Vision Module\\n"
                )
            else:
                error = result.get('error', 'Unknown error')
                console.print(f"\\n  [red]❌ Failed: {error}[/red]\\n")
            
            return True
        
        except Exception as e:
            logger.error(f"Image analysis error: {e}", exc_info=True)
            console.print(f"\\n  [red]❌ Error: {e}[/red]\\n")
            return False

'''
    
    if "def _handle_image_query" not in content:
        # Trouver un bon endroit pour ajouter la méthode (avant _handle_special)
        match = re.search(r'(    async def _handle_special\(self)', content)
        if match:
            insert_point = match.start(1)
            content = content[:insert_point] + new_method + "\n    " + content[insert_point:]
            print("  ✅ Méthode ajoutée")
        else:
            print("  ⚠️ Point d'insertion de la méthode non trouvé")
    else:
        print("  ✅ Méthode déjà présente")
    
    # ========================================================================
    # MODIFICATION 3: Ajouter le hijack dans _handle_special()
    # ========================================================================
    
    print("[4/4] Ajout du hijack dans _handle_special()...")
    
    hijack_code = '''        # ====================================================================
        # IMAGE ANALYSIS REQUESTS (NEW - PRIORITY)
        # ====================================================================
        
        if await self._handle_image_query(user_input):
            return True
        
        # ====================================================================
        # Continue with existing special commands
        # ====================================================================
        '''
    
    if "IMAGE ANALYSIS REQUESTS (NEW" not in content:
        # Trouver le debut de _handle_special et ajouter après la docstring
        match = re.search(r'(    async def _handle_special\(self, user_input: str\) -> bool:\s*"""[^"]*""")\s*\n', content)
        if match:
            insert_point = match.end()
            content = content[:insert_point] + hijack_code + "\n" + content[insert_point:]
            print("  ✅ Hijack ajouté")
        else:
            print("  ⚠️ Point d'insertion du hijack non trouvé")
    else:
        print("  ✅ Hijack déjà présent")
    
    # ========================================================================
    # Écrire le fichier modifié
    # ========================================================================
    
    with open(cli_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ MODIFICATIONS APPLIQUÉES AVEC SUCCÈS!")
    return True


if __name__ == "__main__":
    cli_file = Path("src/ui/cli.py")
    
    if not cli_file.exists():
        print(f"❌ Fichier non trouvé: {cli_file}")
        sys.exit(1)
    
    success = apply_cli_patch(str(cli_file))
    
    if success:
        print("\n🎉 DÉPLOIEMENT RÉUSSI!")
        print("\nProchaines étapes:")
        print("  1. pip install Pillow numpy")
        print("  2. python src/ui/cli.py")
        print("  3. gabriel> analyse image C:\\chemin\\image.png")
    else:
        print("\n❌ Erreur lors de l'application des modifications")
        sys.exit(1)
