"""
================================================================================
GABRIEL IMAGE ANALYSIS INTEGRATION PATCH
================================================================================

Ce patch intègre COMPLÈTEMENT la pipeline d'analyse d'images dans Gabriel.

À appliquer à: src/ui/cli.py
Modifie: async def _handle_special() et async def ask()

================================================================================
"""

# STEP 1: Ajouter cet import au début du fichier cli.py (après les imports existants)

"""
# ============================================================================
# IMAGE ANALYSIS INTEGRATION (NEW)
# ============================================================================

import re
from pathlib import Path

# Tenez les imports image analysis
try:
    from ..gabriel_vision_integration import GabrielVisionIntegration
    from ..advanced_vision_module import AdvancedVisionSystem
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    logger.warning("Vision module not available - image analysis disabled")
"""


# STEP 2: Ajouter cette fonction NOUVELLE dans la classe CLIInterface

"""
async def _handle_image_query(self, query: str) -> bool:
    \"\"\"
    Traite les requêtes d'analyse d'image.
    
    Format supporté:
      - "analyse image C:\\path\\image.png"
      - "analyse image /path/image.png"
      - "valide C:\\path\\image.png"
    
    Retourne: True si requête traitée, False sinon
    \"\"\"
    
    if not VISION_AVAILABLE:
        console.print(
            "\\n  [yellow]Vision module not available.[/yellow]\\n"
            "  [dim]Install vision dependencies: pip install Pillow numpy[/dim]\\n"
        )
        return False
    
    # Détecter si c'est une requête image
    query_lower = query.lower()
    image_commands = ['analyse image', 'valide', 'examine', 'scan', 'analyse']
    
    is_image_query = any(query_lower.startswith(cmd) for cmd in image_commands)
    is_image_file = any(ext in query_lower for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'])
    
    if not (is_image_query and is_image_file):
        return False
    
    # Extraire le chemin d'image
    image_path = self._extract_image_path(query)
    if not image_path:
        console.print("\\n  [yellow]No image path detected in query.[/yellow]\\n")
        return False
    
    # Vérifier que le fichier existe
    image_file = Path(image_path)
    if not image_file.exists():
        console.print(f"\\n  [red]Image not found: {image_path}[/red]\\n")
        return False
    
    try:
        console.print("\\n  [dim]Analyzing image...[/dim]")
        
        # Initialiser le système de vision
        vision = AdvancedVisionSystem()
        
        # Analyser l'image
        result = await vision.analyze_image(str(image_file), query)
        
        # Afficher les résultats
        if result.get('success'):
            console.print(Panel(
                result.get('report', 'Analysis complete'),
                title="[cyan]Image Analysis Report[/cyan]",
                border_style="cyan",
                padding=(1, 2),
            ))
            
            # Afficher la confiance
            confidence = result.get('confidence', 0.0)
            console.print(
                f"\\n  [green]Confidence:[/green] {confidence:.1f}/10\\n"
                f"  [green]Source:[/green] Vision Analysis Module\\n"
            )
        else:
            error = result.get('error', 'Unknown error')
            console.print(f"\\n  [red]Analysis failed: {error}[/red]\\n")
        
        return True
    
    except Exception as e:
        logger.error(f"Image analysis error: {e}", exc_info=True)
        console.print(f"\\n  [red]Error analyzing image: {e}[/red]\\n")
        return False

@staticmethod
def _extract_image_path(query: str) -> str | None:
    \"\"\"Extrait le chemin d'image d'une requête.\"\"\"
    
    # Chercher Windows paths (C:\\path\\to\\file.ext)
    windows_pattern = r'[A-Za-z]:\\\\[^\\s"]+\\.(?:png|jpg|jpeg|gif|bmp|tiff|webp)'
    match = re.search(windows_pattern, query, re.IGNORECASE)
    if match:
        return match.group(0)
    
    # Chercher Unix paths (/path/to/file.ext)
    unix_pattern = r'/[^\\s"]+\\.(?:png|jpg|jpeg|gif|bmp|tiff|webp)'
    match = re.search(unix_pattern, query, re.IGNORECASE)
    if match:
        return match.group(0)
    
    # Chercher des chemins relatifs (./path ou ../path)
    relative_pattern = r'(?:\\.|\\.\\.)/[^\\s"]+\\.(?:png|jpg|jpeg|gif|bmp|tiff|webp)'
    match = re.search(relative_pattern, query, re.IGNORECASE)
    if match:
        return match.group(0)
    
    return None
"""


# STEP 3: Modifier la fonction async def _handle_special() 

"""
AVANT (rechercher cette ligne dans _handle_special):
    async def _handle_special(self, user_input: str) -> bool:

APRÈS (ajouter ce code au début de la fonction, après les commentaires de log):

        # ====================================================================
        # IMAGE ANALYSIS REQUESTS (NEW) - PRIORITY
        # ====================================================================
        
        if await self._handle_image_query(user_input):
            return True
        
        # ====================================================================
        # Continue with existing special commands
        # ====================================================================
"""


# STEP 4: Créer le fichier gabriel_vision_integration.py

"""
Créer: src/gabriel_vision_integration.py

Le fichier doit contenir:

class GabrielVisionIntegration:
    def __init__(self):
        self.vision_system = AdvancedVisionSystem()
    
    async def analyze_image(self, image_path: str, query: str) -> dict:
        '''Analyze image and return structured results'''
        # Impl...

Voir le fichier d'exemple plus loin.
"""


# ============================================================================
# SUMMARY OF CHANGES
# ============================================================================

"""
FICHIERS À MODIFIER:
  ✅ src/ui/cli.py
     1. Ajouter imports (ligne ~20)
     2. Ajouter méthode _handle_image_query() (ligne ~500)
     3. Ajouter méthode _extract_image_path() (ligne ~600)
     4. Modifier _handle_special() pour router vers image analysis (ligne ~300)

FICHIERS À CRÉER:
  ✅ src/gabriel_vision_integration.py (wrapper)
  ✅ src/image_analysis_manager.py (orchestrateur)

DÉPENDANCES À INSTALLER:
  pip install Pillow numpy

RÉSULTAT FINAL:
  - Gabriel détecte les requêtes image automatiquement
  - Route vers le module de vision
  - Retourne analyse complète avec confiance
  - Support des formats: PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP

TEST:
  gabriel> analyse image C:\\theorie-mathematique\\src\\tex\\quadrature_parabole_zero_critique.png
  
  Résultat attendu:
  [cyan]Image Analysis Report[/cyan]
  [green]Confidence: 9.5/10[/green]
  [green]Source: Vision Analysis Module[/green]

"""
