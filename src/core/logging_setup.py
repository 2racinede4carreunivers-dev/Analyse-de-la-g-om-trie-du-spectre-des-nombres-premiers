"""Setup logging UTF-8 robuste (Windows + Docker) — mode terminal esthétique.

Par défaut, seuls WARNING/ERROR/CRITICAL apparaissent dans le terminal.
Les logs INFO/DEBUG (verbeux, techniques) sont écrits dans le fichier
`logs/agent_cli.log` seulement — pour ne pas polluer l'affichage Rich.

Pour restaurer l'ancien comportement (INFO au terminal) :
  * `verbose=True` en argument
  * OU variable d'environnement `GABRIEL_VERBOSE=1`
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path


def _env_verbose() -> bool:
    """Détecte le mode verbose via variable d'environnement."""
    val = os.environ.get("GABRIEL_VERBOSE", "").strip().lower()
    return val in ("1", "true", "yes", "on")


def setup_logging(
    log_dir: str | Path = "./logs",
    verbose: bool | None = None,
    log_file: str = "agent_cli.log",
) -> logging.Logger:
    """Configure les handlers de logging pour Gabriel.

    Args:
        log_dir: Dossier des fichiers .log
        verbose: Si True, les INFO passent aussi au terminal.
                 Si None (défaut), lit `GABRIEL_VERBOSE` env var.
        log_file: Nom du fichier log.

    Returns:
        Logger nommé `multiloop-agent`.
    """
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(parents=True, exist_ok=True)

    if verbose is None:
        verbose = _env_verbose()

    # Fichier : TOUJOURS INFO (log complet pour debug)
    file_level = logging.INFO
    # Terminal : INFO si verbose, sinon WARNING+ (silencieux esthétique)
    console_level = logging.INFO if verbose else logging.WARNING

    fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(fmt)

    file_handler = logging.FileHandler(
        log_dir_path / log_file, encoding="utf-8", errors="replace"
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    if hasattr(sys.stderr, "reconfigure"):
        try:
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except Exception:
            pass

    root = logging.getLogger()
    # Root doit accepter tous les niveaux, ce sont les handlers qui filtrent
    root.setLevel(logging.DEBUG)
    # Eviter les doublons si re-appele
    root.handlers = [file_handler, console_handler]

    # Bruit reseau bas (silencieux même en mode verbose)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("anthropic").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    # Matplotlib est particulièrement bavard sur les fonts
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    return logging.getLogger("multiloop-agent")
