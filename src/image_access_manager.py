"""
Image Access Module pour Gabriel Multi-Loop Agent
==================================================

Module universel d'accès aux images depuis n'importe où:
  - Chemins locaux (absolus, relatifs)
  - Partages réseau (UNC paths, SMB)
  - URL HTTP/HTTPS
  - Chemins relatifs à plusieurs racines
  - Cache local pour performance
  - Gestion d'erreurs robuste

Auteur: Gabriel Multi-Loop Agent
Date: 2026
"""

from __future__ import annotations

import logging
import hashlib
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import re

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("requests non disponible - accès URL limité")

try:
    from urllib.parse import urlparse
    URLPARSE_AVAILABLE = True
except ImportError:
    URLPARSE_AVAILABLE = False

logger = logging.getLogger(__name__)


class ImageSourceType(Enum):
    """Types de sources d'images"""
    LOCAL_ABSOLUTE = "local_absolute"  # C:\Users\...\image.png
    LOCAL_RELATIVE = "local_relative"  # ./images/image.png
    NETWORK_UNC = "network_unc"  # \\server\share\image.png
    NETWORK_SMB = "network_smb"  # smb://server/share/image.png
    HTTP_URL = "http_url"  # http://example.com/image.png
    HTTPS_URL = "https_url"  # https://example.com/image.png
    UNKNOWN = "unknown"


@dataclass
class ImageSource:
    """Représente une source d'image"""
    original_path: str  # Chemin fourni par l'utilisateur
    source_type: ImageSourceType
    resolved_path: Optional[Path] = None  # Chemin résolu localement
    url: Optional[str] = None  # URL si applicable
    is_accessible: bool = False
    file_size: int = 0
    last_modified: Optional[datetime] = None
    cached_path: Optional[Path] = None  # Chemin du cache
    cache_created: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ImageAccessManager:
    """Gestionnaire d'accès universel aux images"""
    
    # Racines de recherche possibles (extensible)
    DEFAULT_SEARCH_ROOTS = [
        Path.cwd(),  # Répertoire courant
        Path.cwd() / "images",
        Path.cwd() / "data" / "images",
        Path.home(),  # Répertoire utilisateur
        Path.home() / "Pictures",
        Path.home() / "Desktop",
        Path.home() / "Documents",
        Path("/tmp"),  # Répertoire temporaire
    ]
    
    def __init__(self, 
                 cache_dir: Optional[Path | str] = None,
                 search_roots: Optional[list[Path]] = None,
                 cache_ttl_hours: int = 24):
        """
        Initialise le gestionnaire d'accès aux images
        
        Args:
            cache_dir: Répertoire de cache (défaut: système temp)
            search_roots: Répertoires de recherche personnalisés
            cache_ttl_hours: Durée de vie du cache en heures
        """
        # Configuration du cache
        if cache_dir is None:
            self.cache_dir = Path(tempfile.gettempdir()) / "gabriel_image_cache"
        else:
            self.cache_dir = Path(cache_dir)
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        
        # Racines de recherche
        self.search_roots = search_roots or self.DEFAULT_SEARCH_ROOTS
        
        # Index de sources
        self.sources: Dict[str, ImageSource] = {}
        
        logger.info(f"ImageAccessManager initialisé")
        logger.info(f"Cache: {self.cache_dir}")
        logger.info(f"Racines de recherche: {len(self.search_roots)}")
    
    # ========== DÉTECTION DE TYPE ==========
    
    def detect_source_type(self, path: str) -> Tuple[ImageSourceType, str]:
        """
        Détecte le type de source et normalise le chemin
        
        Args:
            path: Chemin fourni par l'utilisateur
        
        Returns:
            Tuple (type, chemin_normalisé)
        """
        path_lower = path.lower().strip()
        
        # URL HTTP/HTTPS
        if path_lower.startswith(('http://', 'https://')):
            if path_lower.startswith('https://'):
                return ImageSourceType.HTTPS_URL, path
            return ImageSourceType.HTTP_URL, path
        
        # Partage SMB
        if path_lower.startswith(('smb://', '\\\\\\\\', '//')):
            return ImageSourceType.NETWORK_SMB, path
        
        # Chemin UNC Windows (\\server\share)
        if path.startswith('\\\\') and not path.startswith('\\\\\\\\'):
            return ImageSourceType.NETWORK_UNC, path
        
        # Chemin absolu (Windows: C:\..., Linux: /...)
        if Path(path).is_absolute():
            return ImageSourceType.LOCAL_ABSOLUTE, path
        
        # Chemin relatif par défaut
        return ImageSourceType.LOCAL_RELATIVE, path
    
    # ========== RÉSOLUTION DE CHEMINS ==========
    
    def resolve_local_path(self, path: str) -> Optional[Path]:
        """
        Résout un chemin local (absolu ou relatif)
        
        Args:
            path: Chemin à résoudre
        
        Returns:
            Chemin résolu ou None si non trouvé
        """
        p = Path(path)
        
        # Chemin absolu existant
        if p.is_absolute() and p.exists():
            return p.resolve()
        
        # Recherche relative au répertoire courant
        if (Path.cwd() / p).exists():
            return (Path.cwd() / p).resolve()
        
        # Recherche dans les racines de recherche
        for root in self.search_roots:
            candidate = root / p
            if candidate.exists():
                return candidate.resolve()
        
        logger.warning(f"Chemin local non résolu: {path}")
        return None
    
    def resolve_network_path(self, path: str) -> Optional[Path]:
        """
        Résout un chemin réseau (UNC/SMB)
        
        Sur Windows: Les chemins UNC sont accessibles directement via Path
        Sur Linux: Nécessite CIFS/SMB
        
        Args:
            path: Chemin réseau (UNC ou SMB)
        
        Returns:
            Chemin résolu ou None
        """
        try:
            # Normaliser les slashes
            path_normalized = path.replace('/', '\\')
            
            p = Path(path_normalized)
            
            # Vérifier l'accessibilité
            if p.exists():
                return p.resolve()
            
            logger.warning(f"Chemin réseau non accessible: {path}")
            return None
        
        except Exception as e:
            logger.error(f"Erreur résolution chemin réseau: {e}")
            return None
    
    # ========== ACCÈS URL ==========
    
    def download_from_url(self, url: str) -> Optional[Path]:
        """
        Télécharge une image depuis une URL
        
        Args:
            url: URL de l'image (HTTP/HTTPS)
        
        Returns:
            Chemin du fichier téléchargé ou None
        """
        if not REQUESTS_AVAILABLE:
            logger.error("requests non disponible - impossible télécharger depuis URL")
            return None
        
        try:
            logger.info(f"Téléchargement: {url}")
            
            # Vérifier le cache d'abord
            cache_path = self._get_cached_url_path(url)
            if cache_path.exists():
                cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
                if datetime.now() - cache_time < self.cache_ttl:
                    logger.info(f"Utilisé depuis cache: {cache_path}")
                    return cache_path
            
            # Télécharger
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            # Vérifier le content-type
            content_type = response.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                logger.warning(f"Content-Type suspect: {content_type}")
            
            # Sauvegarder
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(cache_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Téléchargé: {cache_path} ({cache_path.stat().st_size} octets)")
            return cache_path
        
        except Exception as e:
            logger.error(f"Erreur téléchargement URL {url}: {e}")
            return None
    
    def _get_cached_url_path(self, url: str) -> Path:
        """Génère le chemin de cache pour une URL"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        
        # Extraire l'extension du nom de fichier
        try:
            filename = Path(urlparse(url).path).name if URLPARSE_AVAILABLE else "image"
        except:
            filename = "image"
        
        if not filename or '.' not in filename:
            # Utiliser l'extension par défaut ou celle trouvée dans Content-Type
            filename = f"{url_hash}.jpg"
        
        return self.cache_dir / f"{url_hash}_{filename}"
    
    # ========== ACCÈS UNIVERSEL ==========
    
    def access_image(self, image_path: str) -> Optional[ImageSource]:
        """
        Accès universel à une image depuis n'importe quelle source
        
        Args:
            image_path: Chemin/URL de l'image
        
        Returns:
            ImageSource avec chemin accessible ou None
        """
        logger.info(f"Accès image: {image_path}")
        
        # Vérifier le cache des sources
        source_key = hashlib.md5(image_path.encode()).hexdigest()
        if source_key in self.sources:
            cached_source = self.sources[source_key]
            if cached_source.is_accessible:
                logger.info(f"Source en cache: {source_key}")
                return cached_source
        
        # Détecter le type
        source_type, normalized_path = self.detect_source_type(image_path)
        
        source = ImageSource(
            original_path=image_path,
            source_type=source_type,
        )
        
        try:
            if source_type == ImageSourceType.HTTP_URL:
                source.url = normalized_path
                local_path = self.download_from_url(normalized_path)
                if local_path:
                    source.resolved_path = local_path
                    source.is_accessible = True
                    source.file_size = local_path.stat().st_size
                    source.cached_path = local_path
            
            elif source_type == ImageSourceType.HTTPS_URL:
                source.url = normalized_path
                local_path = self.download_from_url(normalized_path)
                if local_path:
                    source.resolved_path = local_path
                    source.is_accessible = True
                    source.file_size = local_path.stat().st_size
                    source.cached_path = local_path
            
            elif source_type == ImageSourceType.NETWORK_UNC:
                local_path = self.resolve_network_path(normalized_path)
                if local_path:
                    source.resolved_path = local_path
                    source.is_accessible = True
                    source.file_size = local_path.stat().st_size
            
            elif source_type == ImageSourceType.NETWORK_SMB:
                local_path = self.resolve_network_path(normalized_path)
                if local_path:
                    source.resolved_path = local_path
                    source.is_accessible = True
                    source.file_size = local_path.stat().st_size
            
            elif source_type == ImageSourceType.LOCAL_ABSOLUTE:
                local_path = self.resolve_local_path(normalized_path)
                if local_path:
                    source.resolved_path = local_path
                    source.is_accessible = True
                    source.file_size = local_path.stat().st_size
            
            elif source_type == ImageSourceType.LOCAL_RELATIVE:
                local_path = self.resolve_local_path(normalized_path)
                if local_path:
                    source.resolved_path = local_path
                    source.is_accessible = True
                    source.file_size = local_path.stat().st_size
            
            if source.is_accessible:
                source.last_modified = datetime.fromtimestamp(
                    source.resolved_path.stat().st_mtime
                )
                logger.info(f"✓ Image accessible: {source.resolved_path}")
            else:
                logger.error(f"✗ Image non accessible: {image_path}")
        
        except Exception as e:
            logger.error(f"Erreur accès image: {e}")
        
        # Mettre en cache
        self.sources[source_key] = source
        
        return source if source.is_accessible else None
    
    # ========== GESTION DU CACHE ==========
    
    def clear_cache(self, older_than_hours: Optional[int] = None) -> int:
        """
        Nettoie le cache des images
        
        Args:
            older_than_hours: Supprimer seulement les fichiers plus vieux que N heures
        
        Returns:
            Nombre de fichiers supprimés
        """
        count = 0
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours or 0)
        
        for cache_file in self.cache_dir.glob("*"):
            if older_than_hours is None:
                cache_file.unlink()
                count += 1
            else:
                file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
                if file_time < cutoff_time:
                    cache_file.unlink()
                    count += 1
        
        logger.info(f"Cache nettoyé: {count} fichiers supprimés")
        return count
    
    def add_search_root(self, root: Path | str) -> None:
        """Ajoute une racine de recherche"""
        root_path = Path(root)
        if root_path not in self.search_roots:
            self.search_roots.append(root_path)
            logger.info(f"Racine de recherche ajoutée: {root_path}")
    
    # ========== RAPPORT ET STATISTIQUES ==========
    
    def report_source(self, source: ImageSource) -> str:
        """Génère un rapport sur une source"""
        report = f"""
╭────────────────────────────────────────────────────────────────╮
│            RAPPORT D'ACCÈS À L'IMAGE - GABRIEL                │
╰────────────────────────────────────────────────────────────────╯

📂 SOURCE
   Type: {source.source_type.value}
   Chemin original: {source.original_path}
   Accessible: {'✓ Oui' if source.is_accessible else '✗ Non'}

📍 RÉSOLUTION
   Chemin résolu: {source.resolved_path or 'N/A'}
   Taille: {source.file_size:,} octets
   Modifié: {source.last_modified.strftime('%Y-%m-%d %H:%M:%S') if source.last_modified else 'N/A'}

💾 CACHE
   Chemin cache: {source.cached_path or 'Pas en cache'}
   Créé: {source.cache_created.strftime('%Y-%m-%d %H:%M:%S') if source.cache_created else 'N/A'}

🔗 URL
   {source.url or 'N/A (non URL)'}

📊 MÉTADONNÉES
   {json.dumps(source.metadata, indent=2) if source.metadata else 'Aucune'}
"""
        return report
    
    def list_cached_images(self) -> list[Tuple[Path, int, datetime]]:
        """Liste toutes les images en cache"""
        cached = []
        for cache_file in self.cache_dir.glob("*"):
            if cache_file.is_file():
                size = cache_file.stat().st_size
                mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
                cached.append((cache_file, size, mtime))
        
        return sorted(cached, key=lambda x: x[2], reverse=True)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Statistiques du cache"""
        cached_images = self.list_cached_images()
        total_size = sum(size for _, size, _ in cached_images)
        
        return {
            'total_images': len(cached_images),
            'total_size_mb': total_size / (1024 * 1024),
            'cache_dir': str(self.cache_dir),
            'oldest': cached_images[-1][2] if cached_images else None,
            'newest': cached_images[0][2] if cached_images else None,
        }


# Singleton global
_access_manager: Optional[ImageAccessManager] = None


def get_image_access_manager(cache_dir: Optional[Path | str] = None) -> ImageAccessManager:
    """Obtient ou crée le gestionnaire d'accès universel"""
    global _access_manager
    
    if _access_manager is None:
        _access_manager = ImageAccessManager(cache_dir=cache_dir)
    
    return _access_manager


def access_image(image_path: str, cache_dir: Optional[Path | str] = None) -> Optional[ImageSource]:
    """
    Fonction de haut niveau pour accéder à une image depuis n'importe où
    
    Exemples d'utilisation:
        # Chemin local
        source = access_image("C:/Users/Philippe/Pictures/figure.png")
        source = access_image("./images/graphique.jpg")
        
        # Réseau
        source = access_image("\\\\serveur\\partage\\schema.png")
        source = access_image("smb://serveur/partage/diagram.png")
        
        # URL
        source = access_image("https://example.com/image.png")
    
    Args:
        image_path: Chemin/URL de l'image
        cache_dir: Répertoire de cache personnalisé
    
    Returns:
        ImageSource avec chemin accessible
    """
    manager = get_image_access_manager(cache_dir=cache_dir)
    return manager.access_image(image_path)


if __name__ == '__main__':
    import sys
    
    # Démonstration
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Gabriel Image Access Manager - Démonstration             ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    manager = ImageAccessManager()
    
    # Exemples de chemins
    test_paths = [
        "C:\\Users\\Philippe\\Pictures\\screenshot.png",  # Windows absolu
        "./images/figure.jpg",  # Relatif
        "https://example.com/image.png",  # URL HTTPS
        "\\\\serveur\\partage\\fichier.png",  # UNC
    ]
    
    for test_path in test_paths:
        print(f"\n{'='*60}")
        print(f"Test: {test_path}")
        print('='*60)
        
        source_type, normalized = manager.detect_source_type(test_path)
        print(f"Type détecté: {source_type.value}")
        print(f"Chemin normalisé: {normalized}")
        
        # Essayer d'accéder (peut échouer si le fichier n'existe pas)
        # source = manager.access_image(test_path)
        # if source:
        #     print(manager.report_source(source))
    
    # Afficher les stats de cache
    print(f"\n{'='*60}")
    print("STATISTIQUES DE CACHE")
    print('='*60)
    stats = manager.get_cache_stats()
    print(json.dumps(stats, indent=2, default=str))
    
    print("\n✓ Gestionnaire d'accès universel prêt!")
