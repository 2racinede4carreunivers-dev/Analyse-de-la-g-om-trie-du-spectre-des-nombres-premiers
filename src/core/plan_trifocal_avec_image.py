#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plan Trifocal - Integration schema image (Quadrature Parabole Zero Critique).

Cross-platform :
  - Utilise la variable d'environnement TRIFOCAL_IMAGE_PATH si definie.
  - Sinon cherche dans les emplacements standards du projet :
      docs/quadrature_parabole_zero_critique.png
      data/images/quadrature_parabole_zero_critique.png
  - Utilise voir_image() (apercu ASCII + metadonnees) au lieu de la classe
    rich.image inexistante.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from .filesystem_access import voir_image, format_image

# Racine du projet (agent-multiloop-Gabriel-local/)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Emplacements candidats (recherche dans l'ordre)
_DEFAULT_CANDIDATES = [
    _PROJECT_ROOT / "docs" / "quadrature_parabole_zero_critique.png",
    _PROJECT_ROOT / "data" / "images" / "quadrature_parabole_zero_critique.png",
    _PROJECT_ROOT / "docs" / "images" / "quadrature_parabole_zero_critique.png",
]


def _find_image() -> Optional[Path]:
    """Retourne le chemin de l'image si trouvee, sinon None."""
    env_path = os.environ.get("TRIFOCAL_IMAGE_PATH")
    if env_path:
        p = Path(env_path).expanduser()
        if p.exists():
            return p
    for candidate in _DEFAULT_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


class PlanTrifocalAvecImage:
    """Plan Trifocal avec schema d'image integre (cross-platform)."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.image_path: Optional[Path] = _find_image()
        self.image_disponible = self.image_path is not None

    def afficher_image(self) -> None:
        """Affiche l'image (apercu ASCII + metadonnees)."""
        if not self.image_disponible or self.image_path is None:
            self.console.print(Panel(
                "[yellow]Image non trouvee.[/yellow]\n\n"
                "Emplacements testes :\n"
                + "\n".join(f"  - {p}" for p in _DEFAULT_CANDIDATES)
                + "\n\nDefinissez [cyan]TRIFOCAL_IMAGE_PATH[/cyan] dans .env "
                "pour pointer vers votre image.",
                title="[yellow]Schema Quadrature - image absente[/yellow]",
                border_style="yellow",
            ))
            return

        try:
            preview = voir_image(str(self.image_path), cols=70)
            self.console.print(Panel(
                format_image(preview),
                title="[cyan]Schema: Quadrature Parabole Zero Critique[/cyan]",
                border_style="cyan",
            ))
        except (RuntimeError, OSError) as exc:
            self.console.print(f"[yellow]Image non chargeable : {exc}[/yellow]")

    def description_image(self) -> str:
        """Description textuelle de ce que le schema montre."""
        return (
            "[bold cyan]Schema: Quadrature Parabole Zero Critique[/bold cyan]\n\n"
            "Ce schema illustre :\n\n"
            "1. [bold]Rectangle des zeros critiques[/bold]\n"
            "   - Zone consideree (tronquee) : T_tr\n"
            "   - Zone restante : T_rest\n\n"
            "2. [bold]Parabole formee par ecarts mixtes[/bold]\n"
            "   - Courbe creee par surdensite combinatoire\n"
            "   - Suit la quadrature d'Archimede\n\n"
            "3. [bold]Equilibre geometrique[/bold]\n"
            "   - Aire parabole = (4/3) x aire triangle\n"
            "   - Si Aire_parabole = T_rest -> HR vraie\n\n"
            "4. [bold]Geometrie epipolaire[/bold]\n"
            "   - Lien entre 3 piliers (Zeta, Spectral, Equivalence)\n"
            "   - Observe position des zeros critiques"
        )


def handle_plan_trifocal_with_image(cmd: str, console: Optional[Console] = None) -> bool:
    """Gestionnaire pour `trifocal image` et `trifocal schema`.

    Retourne True quand la commande a ete geree.
    """
    plan = PlanTrifocalAvecImage(console=console)
    tokens = cmd.strip().split()
    sub_cmd = tokens[1].lower() if len(tokens) >= 2 else "complete"

    if sub_cmd == "image":
        plan.afficher_image()
        return True
    if sub_cmd == "schema":
        plan.console.print(plan.description_image())
        plan.console.print()
        plan.afficher_image()
        return True
    return False


if __name__ == "__main__":
    plan = PlanTrifocalAvecImage()
    plan.console.print("\n[bold]STATUS ACCES IMAGE:[/bold]")
    if plan.image_disponible:
        plan.console.print(f"[green]Image trouvee : {plan.image_path}[/green]")
        plan.afficher_image()
    else:
        plan.console.print(
            "[red]Image NON trouvee. Utilisez TRIFOCAL_IMAGE_PATH dans .env.[/red]"
        )
