"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║  PIPELINE DE CORRECTION — Package Python pour Gabriel Multiloop           ║
║                                                                            ║
║  Ce package contient la « transmission/variateur mécanique » du pipeline   ║
║  de correction autonome pour l'agent Gabriel. Il permet de :               ║
║                                                                            ║
║    1. Scander et cartographier le dépôt complet dans SQLite              ║
║    2. Retrouver automatiquement les fichiers à corriger par mots-clés    ║
║    3. Appliquer des patchs ciblés avec vérification                      ║
║    4. Générer des rapports et snapshots                                  ║
║                                                                            ║
║  MODULES PRINCIPAUX :                                                      ║
║    • orchestrator_main.py  — Directeur d'orchestre (scan, apply, rollback)║
║    • archiviste.py         — Moteur de recherche dans le réseau (DB)     ║
║    • config.py             — Configuration centralisée                     ║
║                                                                            ║
║  USAGE RAPIDE :                                                            ║
║    python -m pipeline_correction --help                                    ║
║    python -m pipeline_correction --scan (génère la DB)                     ║
║    python -m pipeline_correction --apply patch.json (applique le patch)   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

__version__ = "1.0.0"
__author__ = "Gabriel Pipeline Team"

from .archiviste import ArchivisteCorrection, ArchivisteError
from .config import PIPELINE_CONFIG, load_config

__all__ = [
    "ArchivisteCorrection",
    "ArchivisteError",
    "PIPELINE_CONFIG",
    "load_config",
]
