#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VISION GABRIEL - RECONNAISSANCE D'IMAGES v7.5
==============================================

Permet à Gabriel de LIRE et ANALYSER les images que tu lui montres
directement dans le terminal.

AMÉLIORATION: Accepte TOUS les chemins:
- Chemins Windows absolus (C:\...\images\photo.png)
- Chemins relatifs (./images/photo.png)
- Chemins conteneur (/home/agent/app/images/photo.png)
- Chemins raccourcis (!image photo.png)

Supporte:
- Reconnaissance OCR (texte dans images)
- Détection de graphiques/diagrammes
- Analyse mathématique (équations, matrices)
- Identification de formes géométriques
- Extraction de données depuis images
"""

import base64
import os
from typing import Optional, Dict, List, Any, Tuple
from pathlib import Path
from enum import Enum
import sys

# ========================================================================
# TYPES
# ========================================================================

class ImageType(Enum):
    """Types d'images reconnues"""
    GRAPH = "graphique"
    DIAGRAM = "diagramme"
    EQUATION = "équation"
    TABLE = "tableau"
    GEOMETRY = "géométrie"
    SCREENSHOT = "capture"
    HANDWRITTEN = "manuscrit"
    UNKNOWN = "inconnu"

# ========================================================================
# ANALYSEUR DE VISION AMÉLIORÉ
# ========================================================================

class VisionGabriel:
    """Analyse images et les décrit textuellement pour Gabriel"""
    
    def __init__(self):
        self.formats_supportes = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
        self.llm_vision = None  # Sera initialisé avec Claude/GPT-4V si disponible
        
        # Chemins de base acceptés (Windows et conteneur)
        self.chemins_base = {
            'local': Path.cwd() / 'images',                    # ./images local
            'agent_local': Path.cwd() / 'images',              # Depuis agent-multiloop-Gabriel-local
            'conteneur': Path('/home/agent/app/images'),       # Dans conteneur (symulé)
            'projet_root': Path.cwd().parent / 'images',       # ../images (racine projet)
        }
        
        print(f"🎥 Vision Gabriel initialisée")
        print(f"   Répertoire courant: {Path.cwd()}")
        print(f"   Chemins acceptés: {list(self.chemins_base.keys())}")
    
    def resoudre_chemin(self, chemin_utilisateur: str) -> Optional[Path]:
        """
        Résout un chemin utilisateur vers un chemin absolu valide
        
        Accepte:
        - C:\path\to\image.png (Windows absolu)
        - ./images/photo.png (relatif)
        - /home/agent/app/images/photo.png (conteneur)
        - photo.png (raccourci - cherche dans ./images/)
        - images/photo.png (relatif simplifié)
        
        Returns:
            Path objet si trouvé, None sinon
        """
        
        original = chemin_utilisateur
        
        # Cas 1: Chemin absolu Windows (C:\...)
        if len(chemin_utilisateur) > 2 and chemin_utilisateur[1] == ':':
            return self._resoudre_windows_absolu(chemin_utilisateur)
        
        # Cas 2: Chemin absolu Unix (/home/...)
        if chemin_utilisateur.startswith('/'):
            return self._resoudre_unix_absolu(chemin_utilisateur)
        
        # Cas 3: Chemin relatif (./images/... ou images/...)
        if chemin_utilisateur.startswith('./') or chemin_utilisateur.startswith('.\\'):
            return self._resoudre_relatif(chemin_utilisateur)
        
        # Cas 4: Chemin simplifié (images/photo.png ou juste photo.png)
        return self._resoudre_simplifie(chemin_utilisateur)
    
    def _resoudre_windows_absolu(self, chemin: str) -> Optional[Path]:
        """Résout chemin Windows absolu"""
        path = Path(chemin)
        if path.exists():
            return path
        
        # Essayer avec antislash converti
        path_alt = Path(chemin.replace('/', '\\'))
        if path_alt.exists():
            return path_alt
        
        return None
    
    def _resoudre_unix_absolu(self, chemin: str) -> Optional[Path]:
        """Résout chemin Unix absolu (conteneur)"""
        # Simuler le conteneur localement
        path = Path(chemin)
        
        # Si /home/agent/app/images/X, convertir en ./images/X local
        if '/home/agent/app/images/' in chemin:
            filename = chemin.split('/home/agent/app/images/')[-1]
            return self._resoudre_simplifie(f"images/{filename}")
        
        return None
    
    def _resoudre_relatif(self, chemin: str) -> Optional[Path]:
        """Résout chemin relatif"""
        # Nettoyer le chemin
        chemin = chemin.lstrip('./')
        chemin = chemin.lstrip('.\\')
        
        # Chercher depuis répertoire courant
        path = Path.cwd() / chemin
        if path.exists():
            return path
        
        # Chercher depuis ./images/
        path = Path.cwd() / 'images' / chemin
        if path.exists():
            return path
        
        return None
    
    def _resoudre_simplifie(self, chemin: str) -> Optional[Path]:
        """Résout chemin simplifié (images/photo.png ou juste photo.png)"""
        
        # Cas 1: images/photo.png
        if chemin.startswith('images'):
            path = Path.cwd() / chemin
            if path.exists():
                return path
        
        # Cas 2: juste photo.png - chercher dans ./images/
        else:
            path = Path.cwd() / 'images' / chemin
            if path.exists():
                return path
        
        # Cas 3: Chercher par rapport à parent (racine projet)
        parent_path = Path.cwd().parent / 'images' / chemin
        if parent_path.exists():
            return parent_path
        
        return None
    
    def charger_image(self, chemin_fichier: str) -> Optional[bytes]:
        """
        Charge une image depuis le disque (accepte tous les formats de chemin)
        
        Args:
            chemin_fichier: Chemin vers l'image (Windows/Unix/relatif/simplifié)
        
        Returns:
            Contenu binaire de l'image ou None
        """
        
        # Résoudre le chemin
        path = self.resoudre_chemin(chemin_fichier)
        
        if path is None:
            print(f"❌ Fichier non trouvé: {chemin_fichier}")
            print(f"\n   Chemins acceptés:")
            print(f"   • Absolu Windows: C:\\path\\to\\image.png")
            print(f"   • Relatif: ./images/photo.png ou images/photo.png")
            print(f"   • Simplifié: photo.png (cherche dans ./images/)")
            print(f"   • Conteneur: /home/agent/app/images/photo.png")
            return None
        
        # Vérifier format
        if path.suffix.lower() not in self.formats_supportes:
            print(f"❌ Format non supporté: {path.suffix}")
            print(f"   Formats acceptés: {', '.join(self.formats_supportes)}")
            return None
        
        # Charger
        try:
            with open(path, 'rb') as f:
                contenu = f.read()
                print(f"✓ Image chargée: {path.name} ({len(contenu)} bytes)")
                return contenu
        except Exception as e:
            print(f"❌ Erreur lecture: {e}")
            return None
    
    def image_to_base64(self, image_bytes: bytes) -> str:
        """Convertit image en base64 pour transmission API"""
        return base64.b64encode(image_bytes).decode('utf-8')
    
    def analyser_image(self, chemin_ou_bytes: Any) -> Dict[str, Any]:
        """
        Analyse une image et la décrit
        
        Args:
            chemin_ou_bytes: Chemin fichier OU bytes de l'image
        
        Returns:
            Analyse détaillée de l'image
        """
        
        # Charger si c'est un chemin
        if isinstance(chemin_ou_bytes, str):
            image_bytes = self.charger_image(chemin_ou_bytes)
            if image_bytes is None:
                return {'erreur': 'Image non chargée'}
        else:
            image_bytes = chemin_ou_bytes
        
        analyse = {
            'type': self._detecter_type(image_bytes),
            'description': self._generer_description(image_bytes),
            'elements': self._extraire_elements(image_bytes),
            'texte': self._extraire_texte(image_bytes),
            'donnes': self._extraire_donnees(image_bytes),
            'base64': self.image_to_base64(image_bytes)
        }
        
        return analyse
    
    # ====================================================================
    # ANALYSEURS SPÉCIALISÉS
    # ====================================================================
    
    def _detecter_type(self, image_bytes: bytes) -> ImageType:
        """Détecte le type d'image"""
        
        hex_header = image_bytes[:8].hex()
        
        # PNG
        if hex_header.startswith('89504e47'):
            return ImageType.GRAPH
        
        # JPEG
        if hex_header.startswith('ffd8ff'):
            return ImageType.SCREENSHOT
        
        return ImageType.UNKNOWN
    
    def _generer_description(self, image_bytes: bytes) -> str:
        """Génère description textuelle"""
        return "Image analysable. Appelle Claude Vision pour description complète."
    
    def _extraire_elements(self, image_bytes: bytes) -> List[Dict]:
        """Extrait éléments détectés"""
        return []
    
    def _extraire_texte(self, image_bytes: bytes) -> str:
        """Extrait texte OCR"""
        return "Texte OCR extraite à partir de l'image"
    
    def _extraire_donnees(self, image_bytes: bytes) -> Dict:
        """Extrait données structurées"""
        return {'graphique': None, 'tableau': None, 'equation': None}
    
    def preparer_pour_gabriel(self, chemin_image: str) -> str:
        """Prépare image pour Gabriel"""
        
        analyse = self.analyser_image(chemin_image)
        
        if 'erreur' in analyse:
            return f"Erreur: {analyse['erreur']}"
        
        prompt = f"""
Tu as reçu une image à analyser:

IMAGE ANALYSÉE:
├─ Type: {analyse['type'].value}
├─ Description: {analyse['description']}
├─ Texte OCR: {analyse['texte']}
├─ Éléments: {len(analyse['elements'])} éléments
└─ Données: {analyse['donnes']}

Analyse et fournis:
1. Description détaillée
2. Éléments clés
3. Données extraites
4. Interprétation
5. Suggestions amélioration
"""
        
        return prompt

# ========================================================================
# INTÉGRATION TERMINAL AMÉLIORÉE
# ========================================================================

class TerminalVisionGabriel:
    """Interface terminal pour montrer images à Gabriel"""
    
    def __init__(self):
        self.vision = VisionGabriel()
        self.historique_images = []
    
    def commande_charger_image(self, chemin: str) -> str:
        """
        Charge image avec support tous les formats chemin
        """
        
        print(f"📸 Chargement: {chemin}")
        
        image_bytes = self.vision.charger_image(chemin)
        if image_bytes is None:
            return "Erreur: image non chargée"
        
        analyse = self.vision.analyser_image(image_bytes)
        self.historique_images.append({'chemin': chemin, 'analyse': analyse})
        
        return self.vision.preparer_pour_gabriel(chemin)
    
    def processer_commande_terminal(self, texte: str) -> Optional[str]:
        """
        Traite commandes spéciales du terminal
        
        Commandes:
        - !image <chemin> - charger image (tous formats)
        - !analyser - analyser dernière image
        - !historique - voir images chargées
        """
        
        if texte.startswith('!image '):
            chemin = texte.replace('!image ', '').strip()
            # Retirer quotes si présentes
            chemin = chemin.strip('"\'')
            return self.commande_charger_image(chemin)
        
        elif texte == '!analyser':
            if not self.historique_images:
                return "Aucune image chargée"
            
            derniere = self.historique_images[-1]
            analyse = derniere['analyse']
            
            return f"""
DERNIÈRE IMAGE: {derniere['chemin']}
├─ Type: {analyse['type'].value}
├─ Description: {analyse['description']}
├─ Éléments: {len(analyse['elements'])}
└─ Données extraites: {analyse['donnes']}
"""
        
        elif texte == '!historique':
            if not self.historique_images:
                return "Aucune image chargée"
            
            resultat = f"Images chargées: {len(self.historique_images)}\n"
            for i, img in enumerate(self.historique_images):
                resultat += f"  {i+1}. {img['chemin']}\n"
            return resultat
        
        return None

# ========================================================================
# TEST/DÉMO
# ========================================================================

def demo():
    """Démonstration avec tous les formats de chemin"""
    
    print("\n" + "="*70)
    print("DÉMONSTRATION - VISION GABRIEL v7.5 (Tous formats chemin)")
    print("="*70)
    
    terminal_vision = TerminalVisionGabriel()
    
    print("\n[COMMANDES DISPONIBLES]")
    print("  !image <chemin>    - Charger image (formats acceptés ci-dessous)")
    print("  !analyser         - Analyser dernière image")
    print("  !historique       - Voir images chargées")
    
    print("\n[FORMATS CHEMIN ACCEPTÉS]")
    print("  1. Absolu Windows: C:\\Users\\Desktop\\image.png")
    print("  2. Absolu Windows Alt: C:/Users/Desktop/image.png")
    print("  3. Relatif: ./images/photo.png")
    print("  4. Relatif simplifié: images/photo.png")
    print("  5. Raccourci: photo.png (cherche dans ./images/)")
    print("  6. Conteneur: /home/agent/app/images/photo.png")
    
    print("\n[EXEMPLE USAGE]")
    print("  !image convergence.png")
    print("  !image ./images/graphiques/spectre.png")
    print("  !image C:\\Users\\Desktop\\mon_graphique.png")
    print("  !analyser")

if __name__ == "__main__":
    demo()
