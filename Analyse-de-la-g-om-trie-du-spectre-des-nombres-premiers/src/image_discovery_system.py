"""
Gabriel Image Discovery System - Découverte Universelle d'Images
=================================================================

Permet à Gabriel de TROUVER les images n'importe où sur le système
- Par nom (fuzzy search)
- Par chemin partiel
- Par contenu (géométrie détectée)
- Par localisation (dossier spécifique)
- Par date de modification

Utilisateur peut taper:
  gabriel> analyse quadrature_parabole
  gabriel> analyse image:parabole
  gabriel> trouve image dans C:\theories
  gabriel> analyse la dernière figure
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from threading import Lock
import json

try:
    from difflib import SequenceMatcher
    DIFFLIB_AVAILABLE = True
except ImportError:
    DIFFLIB_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class FoundImage:
    """Représente une image trouvée"""
    full_path: Path
    name: str
    extension: str
    size_bytes: int
    modified_time: datetime
    search_score: float = 0.0  # 0-1, pertinence de la recherche
    category: str = "unknown"  # geometry, graph, table, diagram, mixed


class ImageIndexer:
    """Indexe les images du système pour recherche rapide"""
    
    def __init__(self, cache_path: Optional[Path | str] = None):
        """Initialise l'indexeur"""
        self.cache_path = Path(cache_path) if cache_path else Path("./data/image_index")
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        self.index: Dict[str, FoundImage] = {}
        self.index_file = self.cache_path / "image_index.json"
        self.lock = Lock()
        
        # Index par dossier (pour recherche rapide)
        self.folder_index: Dict[str, List[FoundImage]] = {}
        
        # Extensions supportées
        self.supported_extensions = {
            '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp',
            '.PNG', '.JPG', '.JPEG', '.BMP', '.GIF', '.TIFF', '.WEBP'
        }
        
        self._load_index()
        logger.info("ImageIndexer initialisé")
    
    def _load_index(self):
        """Charge l'index depuis le cache"""
        if self.index_file.exists():
            try:
                with open(self.index_file) as f:
                    data = json.load(f)
                    # Reconstruire les objets FoundImage
                    for path_str, img_data in data.items():
                        try:
                            found = FoundImage(
                                full_path=Path(path_str),
                                name=img_data['name'],
                                extension=img_data['extension'],
                                size_bytes=img_data['size_bytes'],
                                modified_time=datetime.fromisoformat(img_data['modified_time']),
                                search_score=img_data.get('search_score', 0.0),
                                category=img_data.get('category', 'unknown'),
                            )
                            self.index[path_str] = found
                        except Exception as e:
                            logger.debug(f"Erreur chargement image {path_str}: {e}")
                logger.info(f"Index chargé: {len(self.index)} images")
            except Exception as e:
                logger.warning(f"Erreur chargement index: {e}")
    
    def _save_index(self):
        """Sauvegarde l'index"""
        try:
            with self.lock:
                data = {}
                for path_str, img in self.index.items():
                    data[path_str] = {
                        'name': img.name,
                        'extension': img.extension,
                        'size_bytes': img.size_bytes,
                        'modified_time': img.modified_time.isoformat(),
                        'search_score': img.search_score,
                        'category': img.category,
                    }
                
                with open(self.index_file, 'w') as f:
                    json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Erreur sauvegarde index: {e}")
    
    def index_directory(self, directory: Path | str, recursive: bool = True) -> int:
        """
        Index toutes les images d'un dossier
        
        Args:
            directory: Dossier à indexer
            recursive: Chercher aussi dans les sous-dossiers
        
        Returns:
            Nombre d'images indexées
        """
        directory = Path(directory)
        if not directory.exists():
            logger.warning(f"Dossier non trouvé: {directory}")
            return 0
        
        count = 0
        try:
            pattern = "**/*" if recursive else "*"
            
            for file_path in directory.glob(pattern):
                if not file_path.is_file():
                    continue
                
                if file_path.suffix.lower() not in self.supported_extensions:
                    continue
                
                try:
                    stat = file_path.stat()
                    found = FoundImage(
                        full_path=file_path,
                        name=file_path.stem,
                        extension=file_path.suffix.lower(),
                        size_bytes=stat.st_size,
                        modified_time=datetime.fromtimestamp(stat.st_mtime),
                    )
                    
                    self.index[str(file_path)] = found
                    
                    # Index par dossier
                    folder = str(file_path.parent)
                    if folder not in self.folder_index:
                        self.folder_index[folder] = []
                    self.folder_index[folder].append(found)
                    
                    count += 1
                
                except Exception as e:
                    logger.debug(f"Erreur indexage {file_path}: {e}")
        
        except Exception as e:
            logger.error(f"Erreur indexage dossier: {e}")
        
        self._save_index()
        logger.info(f"Indexé {count} images dans {directory}")
        return count
    
    def index_common_paths(self) -> int:
        """Index les chemins courants pour les théories/figures"""
        paths_to_index = [
            Path.home() / "Documents",
            Path.home() / "Desktop",
            Path("C:/Users"),  # Windows
            Path("/home"),  # Linux
            Path("./"),  # Répertoire courant
            Path("../"),  # Parent
        ]
        
        # Chemins spécifiques au projet
        project_paths = [
            Path("C:/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/data"),
            Path("C:/theorie-mathematique"),
            Path("C:/theories"),
            Path("./figures"),
            Path("./images"),
            Path("./data"),
        ]
        
        paths_to_index.extend(project_paths)
        
        total = 0
        for path in paths_to_index:
            if path.exists():
                count = self.index_directory(path, recursive=True)
                total += count
                logger.debug(f"Indexé {count} images dans {path}")
        
        return total
    
    def search_by_name(self, query: str, max_results: int = 10) -> List[FoundImage]:
        """
        Recherche les images par nom (fuzzy search)
        
        Args:
            query: Nom ou partie du nom
            max_results: Nombre max de résultats
        
        Returns:
            Liste d'images trouvées, triées par pertinence
        """
        query_lower = query.lower()
        results = []
        
        for img in self.index.values():
            # Exact match
            if query_lower == img.name.lower():
                img.search_score = 1.0
                results.append(img)
            
            # Substring match
            elif query_lower in img.name.lower():
                # Score basé sur la position
                pos = img.name.lower().find(query_lower)
                img.search_score = 0.9 - (pos / len(img.name) * 0.1)
                results.append(img)
            
            # Fuzzy match (si difflib disponible)
            elif DIFFLIB_AVAILABLE:
                ratio = SequenceMatcher(None, query_lower, img.name.lower()).ratio()
                if ratio > 0.6:
                    img.search_score = ratio
                    results.append(img)
        
        # Trier par score
        results.sort(key=lambda x: x.search_score, reverse=True)
        return results[:max_results]
    
    def search_by_path(self, path_pattern: str, max_results: int = 10) -> List[FoundImage]:
        """
        Recherche par chemin partiel ou dossier
        
        Args:
            path_pattern: Partie du chemin (ex: "C:\theories\figures")
            max_results: Nombre max de résultats
        
        Returns:
            Images correspondant au chemin
        """
        pattern_lower = path_pattern.lower()
        results = []
        
        for img in self.index.values():
            path_lower = str(img.full_path).lower()
            if pattern_lower in path_lower:
                # Score basé sur la spécificité
                score = len(pattern_lower) / len(path_lower)
                img.search_score = score
                results.append(img)
        
        results.sort(key=lambda x: x.search_score, reverse=True)
        return results[:max_results]
    
    def get_recent_images(self, count: int = 10) -> List[FoundImage]:
        """Retourne les images modifiées récemment"""
        results = sorted(
            self.index.values(),
            key=lambda x: x.modified_time,
            reverse=True
        )
        return results[:count]
    
    def get_images_in_folder(self, folder: Path | str) -> List[FoundImage]:
        """Retourne toutes les images dans un dossier"""
        folder_str = str(Path(folder).absolute())
        return self.folder_index.get(folder_str, [])
    
    def clear_index(self):
        """Efface l'index"""
        with self.lock:
            self.index.clear()
            self.folder_index.clear()
        self._save_index()
        logger.info("Index effacé")


class ImageDiscoverySystem:
    """
    Système de découverte d'images
    Permet aux utilisateurs de trouver et analyser des images
    """
    
    def __init__(self):
        """Initialise le système"""
        self.indexer = ImageIndexer()
        
        # Index les chemins courants au démarrage
        logger.info("Indexation des chemins courants...")
        count = self.indexer.index_common_paths()
        logger.info(f"✓ {count} images indexées au démarrage")
    
    def process_query(self, user_query: str) -> Optional[FoundImage]:
        """
        Traite une requête utilisateur et retourne une image
        
        Formats supportés:
        - "analyse quadrature" → Cherche "quadrature"
        - "analyse image:parabole" → Cherche spécifiquement
        - "trouve image dans C:\theories" → Cherche dans dossier
        - "analyse la dernière figure" → Dernière image modifiée
        - "analyse image théorie" → Recherche floue
        
        Args:
            user_query: Requête utilisateur
        
        Returns:
            FoundImage trouvée, ou None
        """
        query = user_query.strip().lower()
        
        # Pattern: "la dernière figure/image"
        if "dernière" in query or "recent" in query:
            recents = self.indexer.get_recent_images(1)
            if recents:
                logger.info(f"Trouvé récent: {recents[0].name}")
                return recents[0]
        
        # Pattern: "image:nom" ou "figure:nom"
        if "image:" in query or "figure:" in query:
            name_part = query.split(":", 1)[1].strip()
            results = self.indexer.search_by_name(name_part, max_results=1)
            if results:
                logger.info(f"Trouvé par pattern: {results[0].name}")
                return results[0]
        
        # Pattern: "dans C:\chemin"
        if "dans " in query:
            path_part = query.split("dans ", 1)[1].strip()
            results = self.indexer.search_by_path(path_part, max_results=1)
            if results:
                logger.info(f"Trouvé dans dossier: {results[0].name}")
                return results[0]
        
        # Pattern: Simple name search
        # Extraire le nom depuis la requête
        # Enlever les mots courants
        common_words = {'analyse', 'examine', 'valide', 'scan', 'image', 'figure', 'pour', 'et', 'avec', 'dans'}
        tokens = [w for w in query.split() if w not in common_words and len(w) > 2]
        
        if tokens:
            search_term = tokens[0]
            results = self.indexer.search_by_name(search_term, max_results=1)
            if results:
                logger.info(f"Trouvé par recherche: {results[0].name}")
                return results[0]
        
        logger.debug(f"Aucune image trouvée pour: {query}")
        return None
    
    def get_search_suggestions(self, partial_name: str, count: int = 5) -> List[FoundImage]:
        """
        Retourne des suggestions d'images pour autocomplétion
        
        Args:
            partial_name: Début du nom
            count: Nombre de suggestions
        
        Returns:
            Liste d'images suggérées
        """
        return self.indexer.search_by_name(partial_name, max_results=count)


# Singleton global
_discovery_system: Optional[ImageDiscoverySystem] = None


def get_image_discovery_system() -> ImageDiscoverySystem:
    """Obtient ou crée le système de découverte"""
    global _discovery_system
    
    if _discovery_system is None:
        _discovery_system = ImageDiscoverySystem()
    
    return _discovery_system


def find_image(query: str) -> Optional[FoundImage]:
    """
    Trouve une image basée sur la requête utilisateur
    
    Exemples:
        find_image("quadrature_parabole")
        find_image("analyse la dernière figure")
        find_image("dans C:\\theories")
    """
    system = get_image_discovery_system()
    return system.process_query(query)


def find_images(query: str, count: int = 5) -> List[FoundImage]:
    """Trouve plusieurs images"""
    system = get_image_discovery_system()
    indexer = system.indexer
    
    # Essayer d'abord par nom
    results = indexer.search_by_name(query, max_results=count)
    if results:
        return results
    
    # Puis par chemin
    results = indexer.search_by_path(query, max_results=count)
    return results


def index_folder(folder_path: str) -> int:
    """Index un dossier spécifique"""
    system = get_image_discovery_system()
    return system.indexer.index_directory(folder_path, recursive=True)


if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Gabriel Image Discovery System - Test                    ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    system = get_image_discovery_system()
    
    print(f"✓ {len(system.indexer.index)} images indexées\n")
    
    # Test: Chercher "quadrature"
    print("Test 1: Chercher 'quadrature'")
    results = system.indexer.search_by_name("quadrature", max_results=3)
    for img in results:
        print(f"  • {img.name}{img.extension} (score: {img.search_score:.2f})")
    
    # Test: Dernières images
    print("\nTest 2: Dernières images modifiées")
    recents = system.indexer.get_recent_images(3)
    for img in recents:
        print(f"  • {img.name}{img.extension} ({img.modified_time.strftime('%Y-%m-%d')})")
    
    print("\n✓ Système prêt!")
