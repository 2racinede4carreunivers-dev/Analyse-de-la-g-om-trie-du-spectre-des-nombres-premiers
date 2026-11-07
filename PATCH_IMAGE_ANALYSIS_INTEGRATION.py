"""
PATCH: Intégration d'analyse d'images dans Gabriel CLI
======================================================

À ajouter dans: src/ui/cli.py

Cherchez la méthode: async def _handle_special(self, cmd: str) -> bool:
(Ligne ~3200)

Ajoutez ces blocs AVANT le 'return False' final
"""

# ============================================================================
# BLOC 1: À ajouter dans la méthode _handle_special
# ============================================================================

# Chercher cette ligne (environ ligne 3250):
#     if cmd.lower().startswith("cognitive"):
#         return await self._handle_cognitive(cmd)

# AJOUTER APRÈS (avant le 'return False' final):

        # Analyse d'images (nouveau v5.5)
        if cmd.lower().startswith(('analyse image', 'valide', 'examine', 'scan')):
            return self._handle_image_analysis(cmd)


# ============================================================================
# BLOC 2: À ajouter comme nouvelle méthode de CLIInterface
# ============================================================================

# Chercher la fin de CLIInterface (avant 'def run_cli():')
# AJOUTER CETTE NOUVELLE MÉTHODE:

    def _handle_image_analysis(self, cmd: str) -> bool:
        """
        Commande d'analyse d'images
        
        Usage:
            analyse image C:\path\to\image.png
            valide C:\path\to\figure.png
            examine C:\path\to\schema.png pour des rayons
            scan C:\path\to\matrice.png et extrait
        """
        try:
            from src.gabriel_image_interface import gabriel_analyze_image
            
            result = gabriel_analyze_image(cmd)
            console.print(result)
            
        except ImportError as e:
            console.print(f"[red]Module vision non disponible: {e}[/red]")
        except Exception as e:
            console.print(f"[red]Erreur analyse image: {e}[/red]")
        
        return True


# ============================================================================
# BLOC 3: Ajouter aussi dans _handle_special pour les commandes d'aide
# ============================================================================

# Chercher: if cmd.lower().startswith(("aide", "help", "commandes"))
# Dans le bloc qui affiche la liste des commandes, AJOUTER:

        # Section VISION (insérer dans la liste)
        vision_commands = """
  [bold cyan]VISION & ANALYSE D'IMAGES[/bold cyan]
    [bold]analyse image[/bold] <chemin>    Analyse complète d'une image
    [bold]valide[/bold] <chemin>            Validation d'une figure (critères auto)
    [bold]examine[/bold] <chemin> pour ...  Examine spécifique (rayons, symétrie)
    [bold]scan[/bold] <chemin> et extrait   Extraction de données (OCR, matrice)
    
    Format: analyse image C:\\path\\to\\image.png
    Critères: rayons, symétrie, équilatéral, rectangle, cercle, régulier, diagonales
"""
        
        # (Ajouter vision_commands à la sortie d'aide)


# ============================================================================
# BLOC 4 (OPTIONNEL): Intégration dans la API HTTP
# ============================================================================

# Si vous voulez aussi l'API HTTP, ajouter à src/api/gabriel_http_api.py:

@app.route('/api/v1/image/analyze', methods=['POST'])
def api_analyze_image():
    """Endpoint HTTP pour analyser une image"""
    try:
        from src.gabriel_image_interface import gabriel_analyze_image
        
        data = request.json or {}
        image_path = data.get('image_path')
        
        if not image_path:
            return {'success': False, 'error': 'image_path required'}, 400
        
        result = gabriel_analyze_image(f"analyse image {image_path}")
        
        # Parser le résultat pour JSON
        return {'success': True, 'result': result}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}, 500


# ============================================================================
# VÉRIFICATION POST-PATCH
# ============================================================================

# Après avoir appliqué le patch, vérifiez:
# 
# 1. Dans Gabriel CLI:
#    gabriel> analyse image C:\path\image.png
#    → Doit afficher l'analyse complète
#
# 2. Tapez 'aide' dans Gabriel pour voir la nouvelle section
#
# 3. Test d'une image réelle:
#    gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png
#    → Doit afficher les détections

print("✓ Patch prêt à appliquer")
print("\nÉtapes:")
print("1. Ouvrir src/ui/cli.py")
print("2. Chercher: async def _handle_special(self, cmd: str) -> bool:")
print("3. Ajouter BLOC 1 avant 'return False'")
print("4. Ajouter BLOC 2 comme nouvelle méthode de CLIInterface")
print("5. Sauvegarder et redémarrer Gabriel")
print("\nTest:")
print("  gabriel> analyse image C:\\path\\image.png")
