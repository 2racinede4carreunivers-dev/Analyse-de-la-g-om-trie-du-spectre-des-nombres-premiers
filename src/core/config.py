"""Chargement de la configuration YAML + variables d'environnement."""
from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
_ROOT = Path(__file__).resolve().parent.parent.parent

# Memorise quel .env a ete charge (utile pour la commande 'env-check')
LOADED_ENV_PATH: Path | None = None


def _load_env() -> None:
    """Charge le fichier .env le plus pertinent. Loggue celui retenu.

    NOTE : dans un conteneur Docker avec `docker-compose env_file: - .env`,
    les variables sont DEJA injectees dans os.environ par docker-compose.
    Dans ce cas, l'absence du fichier .env physique n'est pas un probleme.
    """
    global LOADED_ENV_PATH
    candidates = [
        Path.cwd() / ".env",
        _ROOT / ".env",
        Path("/home/agent/app/.env"),
    ]
    # Dedupliquer (les 3 candidats peuvent pointer au meme endroit dans Docker)
    seen: set[Path] = set()
    unique_candidates = []
    for c in candidates:
        rc = c.resolve()
        if rc not in seen:
            seen.add(rc)
            unique_candidates.append(c)

    for candidate in unique_candidates:
        if candidate.exists():
            load_dotenv(candidate)
            LOADED_ENV_PATH = candidate
            logger.info(".env charge depuis : %s", candidate)
            return
    LOADED_ENV_PATH = None

    # Cas Docker : env_file injecte les vars meme sans fichier .env physique
    if os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY"):
        logger.info(
            "Aucun fichier .env physique, mais les variables d'environnement "
            "sont presentes (probablement injectees par docker-compose env_file)."
        )
    else:
        logger.warning(
            ".env INTROUVABLE parmi les candidats : %s "
            "ET aucune variable CLAUDE_API_KEY/OPENAI_API_KEY n'est presente dans l'environnement. "
            "Verifiez que docker-compose.yml contient 'env_file: - .env' et "
            "que le fichier .env existe a cote du docker-compose.yml.",
            [str(c) for c in unique_candidates],
        )


_load_env()


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Charge config.yaml et merge les variables d'environnement critiques."""
    if path is None:
        for candidate in (
            Path.cwd() / "config.yaml",
            _ROOT / "config.yaml",
            Path("/home/agent/app/config.yaml"),
        ):
            if candidate.exists():
                path = candidate
                break
    if path is None or not Path(path).exists():
        return _default_config()

    with open(path, "r", encoding="utf-8") as fh:
        config: dict[str, Any] = yaml.safe_load(fh) or {}

    # Injection des variables d'environnement
    llm_cfg = config.setdefault("llm", {})
    ollama_cfg = llm_cfg.setdefault("ollama", {})
    openai_cfg = llm_cfg.setdefault("openai", {})

    if env_host := os.environ.get("OLLAMA_HOST"):
        ollama_cfg["base_url"] = env_host
    if env_model := os.environ.get("OLLAMA_MODEL"):
        ollama_cfg["model"] = env_model
    if env_oai_model := os.environ.get("OPENAI_MODEL"):
        openai_cfg["model"] = env_oai_model

    # Cles API : on ne les stocke pas dans le YAML, on les lit a la demande
    openai_cfg["api_key_env"] = "OPENAI_API_KEY"

    # Multiloop overrides
    ml_cfg = config.setdefault("multiloop", {})
    if (env_iter := os.environ.get("MULTILOOP_MAX_ITERATIONS")):
        ml_cfg["max_iterations"] = int(env_iter)
    if (env_score := os.environ.get("MULTILOOP_MIN_SCORE")):
        ml_cfg["min_acceptance_score"] = float(env_score)

    return config


def _default_config() -> dict[str, Any]:
    return {
        "agent": {"name": "Multi-Loop Math Agent", "language": "fr", "user_name": "Philippe"},
        "llm": {
            "primary": "ollama",
            "fallback": "openai",
            "ollama": {"model": "llama3.2", "base_url": os.environ.get("OLLAMA_HOST", "http://ollama:11434")},
            "openai": {"model": "gpt-5.4", "api_key_env": "OPENAI_API_KEY"},
        },
        "multiloop": {"max_iterations": 3, "min_acceptance_score": 8.0, "num_candidates_per_round": 2},
        "pipeline": {
            "enable_abstraction": True,
            "enable_meta_reasoning": True,
            "enable_concept_navigation": True,
            "enable_generalization": True,
            "enable_hol_generation": True,
        },
        "data": {"hol_dir": "/theories"},
    }


def get_openai_key() -> str | None:
    return os.environ.get("OPENAI_API_KEY")


def get_ollama_url() -> str:
    return os.environ.get("OLLAMA_HOST", "http://ollama:11434")

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
