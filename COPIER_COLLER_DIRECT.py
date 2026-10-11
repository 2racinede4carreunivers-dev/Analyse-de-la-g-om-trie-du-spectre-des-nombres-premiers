"""
COPIER-COLLER DIRECT: Intégration Image Analysis dans Gabriel CLI

Ce fichier contient le code EXACT à ajouter. Pas de modification, juste copier-coller.
"""

# ========================================================================
# FICHIER: src/ui/cli.py
# ========================================================================

# LOCALISATION:
# Ligne ~3215, dans la méthode: async def _handle_special(self, cmd: str) -> bool:

# CODE EXISTANT À TROUVER:
"""
    async def _handle_special(self, cmd: str) -> bool:
        ...
        if cmd.lower().startswith("cognitive"):
            return await self._handle_cognitive(cmd)
        
        return False  # ← Cette ligne
"""

# ========================================================================
# MODIFICATION 1: Avant 'return False', ajouter:
# ========================================================================

# AJOUTER APRÈS le bloc "cognitive" ET AVANT "return False":
        
        # Analyse d'images (v5.5)
        if cmd.lower().startswith(('analyse image', 'valide', 'examine', 'scan')):
            return self._handle_image_analysis(cmd)

# ========================================================================
# MODIFICATION 2: Ajouter cette nouvelle méthode
# ========================================================================

# TROUVER: La fin de la classe CLIInterface (avant "def run_cli():")
# AJOUTER CETTE MÉTHODE:

    def _handle_image_analysis(self, cmd: str) -> bool:
        """
        Commande d'analyse d'images
        
        Exemples:
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

# ========================================================================
# VÉRIFICATION: Après intégration
# ========================================================================

# Dans Gabriel, vérifier que ces commandes fonctionnent:

# Test 1: Aide
"""
gabriel> aide
... (doit montrer la nouvelle section "VISION & ANALYSE D'IMAGES")
"""

# Test 2: Image réelle
"""
gabriel> analyse image C:\theorie-mathematique\src\tex\tex-2\quadrature_parabole_zero_critique.png

Résultat attendu:
╭────────────────────────────────────────────────────────────────╮
│         ANALYSE VISION COMPLÈTE - GABRIEL SYSTEM              │
╰────────────────────────────────────────────────────────────────╯

📁 IMAGE
   Chemin: C:\theorie-mathematique\src\tex\tex-2\...
   Succès: ✓ Oui
   Durée: XXXms

🎯 CAPACITÉS UTILISÉES (X)
   ✓ ...
   ✓ ...

📊 DÉTECTIONS
   ...
"""

# ========================================================================
# C'EST TOUT!
# ========================================================================

print("""
RÉSUMÉ D'INTÉGRATION
====================

Fichier à modifier: src/ui/cli.py

Modifications:
1. Une ligne de condition (ajouter avant "return False", ligne ~3220)
2. Une nouvelle méthode (ajouter avant "def run_cli():", ligne ~3500)

Code total: ~20 lignes (très court!)

Après intégration:
  gabriel> analyse image C:\path\image.png

Fonctionne immédiatement!
""")
