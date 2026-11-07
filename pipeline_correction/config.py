"""
═════════════════════════════════════════════════════════════════════════════
  CONFIGURATION CENTRALISÉE — Pipeline de Correction Gabriel
═════════════════════════════════════════════════════════════════════════════
"""

from pathlib import Path
import json
from typing import Optional, Dict, Any


# ──────────────────────────────────────────────────────────────────────────
# CHEMINS DE BASE
# ──────────────────────────────────────────────────────────────────────────

PIPELINE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PIPELINE_ROOT.parent
DATA_DIR = PIPELINE_ROOT / "data"
DB_PATH = DATA_DIR / "gabriel_repo_map.db"
SNAPSHOTS_DIR = DATA_DIR / "snapshots"
LOGS_DIR = DATA_DIR / "logs"


# ──────────────────────────────────────────────────────────────────────────
# CONFIGURATION DU SCANNER (orchestrator_main.py)
# ──────────────────────────────────────────────────────────────────────────

SCANNER_CONFIG = {
    "repo_root": str(REPO_ROOT),
    "db_path": str(DB_PATH),
    "exclude_dirs": {
        ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
        ".idea", ".vscode", "node_modules", "logs", "dist", "build",
        "__snapshots__", "tmp", "temp", ".gabriel_variateur",
    },
    "include_extensions": {
        ".py", ".md", ".txt", ".thy", ".yaml", ".yml", ".json", ".toml",
        ".ini", ".cfg", ".sh", ".bat", ".ps1", ".sql",
    },
    "max_file_size_mb": 10,
    "timeout_seconds": 300,
}


# ──────────────────────────────────────────────────────────────────────────
# CONFIGURATION DE L'ARCHIVISTE (archiviste.py)
# ──────────────────────────────────────────────────────────────────────────

ARCHIVISTE_CONFIG = {
    "db_path": str(DB_PATH),
    "repo_root": str(REPO_ROOT),
    "profondeur_defaut": 2,
    "top_k_resultats": 20,
    "relations_suivis": {"import", "role_cluster"},
}


# ──────────────────────────────────────────────────────────────────────────
# CONFIGURATION DE L'APPLICATEUR (apply patches)
# ──────────────────────────────────────────────────────────────────────────

APPLICATEUR_CONFIG = {
    "snapshots_dir": str(SNAPSHOTS_DIR),
    "dry_run_par_defaut": False,
    "verifier_syntax": True,
    "verifier_imports": True,
    "backup_original": True,
}


# ──────────────────────────────────────────────────────────────────────────
# CONFIGURATION GLOBALE (union de tous les modes)
# ──────────────────────────────────────────────────────────────────────────

PIPELINE_CONFIG = {
    "pipeline_root": str(PIPELINE_ROOT),
    "repo_root": str(REPO_ROOT),
    "data_dir": str(DATA_DIR),
    "db_path": str(DB_PATH),
    "snapshots_dir": str(SNAPSHOTS_DIR),
    "logs_dir": str(LOGS_DIR),
    #
    "scanner": SCANNER_CONFIG,
    "archiviste": ARCHIVISTE_CONFIG,
    "applicateur": APPLICATEUR_CONFIG,
    #
    "version": "1.0.0",
    "author": "Gabriel Pipeline Team",
}


# ──────────────────────────────────────────────────────────────────────────
# UTILITAIRES DE CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────

def load_config(config_file: Optional[Path] = None) -> Dict[str, Any]:
    """Charge la configuration depuis un fichier YAML/JSON (optionnel).
    
    Si config_file n'existe pas, retourne la configuration par défaut.
    """
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, "r") as f:
                if str(config_file).endswith(".json"):
                    return json.load(f)
                # Sinon, on supposerait du YAML, mais json suffira ici
        except Exception as e:
            print(f"⚠️  Impossible de charger {config_file} : {e}")
    return PIPELINE_CONFIG


def ensure_dirs() -> None:
    """Crée les répertoires nécessaires s'ils n'existent pas."""
    for d in [DATA_DIR, SNAPSHOTS_DIR, LOGS_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def get_pipeline_summary() -> Dict[str, Any]:
    """Retourne un résumé de l'état du pipeline."""
    ensure_dirs()
    return {
        "pipeline_root": str(PIPELINE_ROOT),
        "repo_root": str(REPO_ROOT),
        "db_exists": DB_PATH.exists(),
        "db_size_mb": DB_PATH.stat().st_size / (1024 * 1024) if DB_PATH.exists() else 0,
        "snapshots_count": len(list(SNAPSHOTS_DIR.glob("*/"))),
        "logs_count": len(list(LOGS_DIR.glob("*"))),
    }


if __name__ == "__main__":
    import pprint
    ensure_dirs()
    print("\n╔════ CONFIGURATION PIPELINE ════╗\n")
    pprint.pprint(get_pipeline_summary())
    print("\n")
