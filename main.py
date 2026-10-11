#!/usr/bin/env python3
"""Point d'entree principal du Multi-Loop Mathematical Agent."""
from __future__ import annotations

import logging
import os
import sys
import time
from pathlib import Path

# Ajouter le repertoire racine au path
_ROOT = Path(__file__).parent.resolve()
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.core.config import load_config
from src.core.logging_setup import _env_verbose, setup_logging


def _rich_init_banner() -> "tuple[object, object] | tuple[None, None]":
    """Retourne (console, live_context_manager) si Rich est disponible."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        from rich.align import Align
        from rich.box import ROUNDED
    except ImportError:
        return None, None

    console = Console()
    title = Text("La fiancée de Cline Mm. Gabriel multiloop local", style="bold cyan")
    subtitle = Text(
        "Chargement de la Methode Spectrale...",
        style="italic dim",
    )
    body = Align.center(Text.assemble(title, "\n", subtitle))
    panel = Panel(
        body,
        title="[bold]Initialisation[/bold]",
        border_style="cyan",
        box=ROUNDED,
        padding=(1, 2),
    )
    console.print(panel)
    return console, None


def _rich_init_summary(
    console,
    started_at: float,
    log_path: Path,
    verbose: bool,
) -> None:
    """Affiche un mini-résumé propre après l'initialisation (Rich)."""
    if console is None:
        return
    try:
        from rich.panel import Panel
        from rich.text import Text
        from rich.box import ROUNDED
    except ImportError:
        return

    duration = time.monotonic() - started_at
    lines = Text()
    lines.append("  Duree init : ", style="dim")
    lines.append(f"{duration:.2f}s\n", style="bold green")
    lines.append("  Log file   : ", style="dim")
    lines.append(f"{log_path}\n", style="cyan")
    lines.append("  Verbose    : ", style="dim")
    lines.append(
        "ON (logs INFO au terminal)" if verbose else "OFF (logs INFO -> fichier)",
        style="yellow" if verbose else "green",
    )
    if not verbose:
        lines.append("\n  Astuce     : ", style="dim")
        lines.append(
            "GABRIEL_VERBOSE=1 pour voir les logs INFO en direct",
            style="dim italic",
        )

    console.print(
        Panel(
            lines,
            title="[bold]Initialisation terminee[/bold]",
            border_style="green",
            box=ROUNDED,
            padding=(0, 2),
        )
    )


def main() -> None:
    started_at = time.monotonic()

    # 1) Banniere d'init (avant tout log bavard)
    console, _ = _rich_init_banner()

    # 2) Config + logging (INFO -> fichier seulement, sauf si verbose)
    config = load_config()
    log_dir = config.get("logging", {}).get("log_dir", "./logs")
    logger = setup_logging(log_dir)  # verbose=None -> lit GABRIEL_VERBOSE

    # Détermine si on est en mode verbose (recherché aussi par le résumé)
    verbose = _env_verbose()

    logger.info("Starting Multi-Loop Mathematical Agent (Gabriel local)")

    # 3) Charger le CLI (import différé pour que la banniere s'affiche avant)
    from src.ui.cli import run_cli

    # 4) Afficher le badge scientifique (certifications academiques)
    try:
        from src.core.scientific_badge import print_badge_to_console
        if console is not None:
            print_badge_to_console(console)
    except Exception as exc:
        logger.warning("Badge scientifique non disponible: %s", exc)

    # 4b) Pipeline cognitif HOL — initialisation du corpus spectral Savard
    from gabriel_p4_bridge import archiviste as hol_archiviste
    hol_archiviste.initialiser()

    # 5) Résumé d'init (avant que run_cli() prenne le contrôle)
    log_path = Path(log_dir).resolve() / "agent_cli.log"
    _rich_init_summary(console, started_at, log_path, verbose)

    # 6) Lancer le CLI (boucle interactive Rich)
    run_cli()


if __name__ == "__main__":
    main()

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
