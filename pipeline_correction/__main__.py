"""
═════════════════════════════════════════════════════════════════════════════
  ENTRYPOINT PRINCIPAL — Pipeline de Correction Gabriel
═════════════════════════════════════════════════════════════════════════════

Usage :
    python -m pipeline_correction --help
    python -m pipeline_correction --scan
    python -m pipeline_correction --apply patch.json
    python -m pipeline_correction --list-snapshots
═════════════════════════════════════════════════════════════════════════════
"""

import sys
import argparse
from pathlib import Path

# Import du module orchestrator_main depuis le même package
try:
    from .orchestrator_main import main as orchestrator_main
    from .config import ensure_dirs
except ImportError as e:
    print(f"ERREUR : Impossible d'importer le pipeline : {e}")
    sys.exit(1)


def main():
    """Point d'entrée du package pipeline_correction."""
    ensure_dirs()
    
    parser = argparse.ArgumentParser(
        description="Pipeline de Correction Gabriel — Orchestrateur et Archiviste",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
    python -m pipeline_correction --scan              # Scanne le dépôt et génère la DB
    python -m pipeline_correction --apply patch.json  # Applique un patch
    python -m pipeline_correction --dry-run patch.json # Simule l'application
    python -m pipeline_correction --rollback snap-20260902-150000  # Restaure
    python -m pipeline_correction --list-snapshots    # Liste les snapshots
        """,
    )
    
    # Grouper les commandes principales
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--scan", action="store_true", help="Scanne le dépôt et génère la DB")
    group.add_argument("--apply", metavar="PATCH", help="Applique un patch JSON")
    group.add_argument("--dry-run", metavar="PATCH", help="Simule l'application du patch")
    group.add_argument("--rollback", metavar="SNAPSHOT", help="Restaure un snapshot")
    group.add_argument("--list-snapshots", action="store_true", help="Liste les snapshots")
    group.add_argument("--archiviste-search", metavar="MOTS", nargs="+", help="Recherche par mots-clés")
    
    # Options supplémentaires
    parser.add_argument("--role", help="Filtre par rôle (core, spectral, ui...)")
    parser.add_argument("--profondeur", type=int, default=2, help="Profondeur de propagation réseau")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")
    
    args = parser.parse_args()
    
    # Rediriger vers orchestrator_main avec les arguments appropriés
    try:
        orchestrator_main(args)
    except Exception as e:
        print(f"ERREUR : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
