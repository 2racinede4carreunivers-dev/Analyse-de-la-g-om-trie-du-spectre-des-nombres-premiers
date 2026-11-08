#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMMANDES LaTeX pour Gabriel CLI
================================

Integration des commandes LaTeX dans le CLI de Gabriel.

Commandes disponibles:
  latex generer --type=article --question=rsp1x1
  latex valider "<code LaTeX>"
  latex compiler mon_article.tex
  latex template methode-spectrale
  latex miktex-check
"""

from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .latex_generator import (
    LaTeXValidator,
    LaTeXCodeGenerator,
    LaTeXArticleGenerator,
    MikTeXCompiler,
    LaTeXQuestionType,
)


console = Console()


def cmd_latex_validate(latex_code: str) -> None:
    """Valide le code LaTeX."""
    validator = LaTeXValidator()
    result = validator.validate(latex_code)
    
    # Affichage
    if result.is_valid:
        color = "green"
        verdict = "✓ VALIDE"
    else:
        color = "red"
        verdict = "✗ ERREURS"
    
    body = Text()
    body.append(f"{verdict}\n\n", style=f"bold {color}")
    
    if result.errors:
        body.append("ERREURS :\n", style="bold red")
        for i, err in enumerate(result.errors, 1):
            body.append(f"  [{i}] {err}\n", style="red")
        body.append("\n")
    
    if result.warnings:
        body.append("AVERTISSEMENTS :\n", style="bold yellow")
        for i, warn in enumerate(result.warnings, 1):
            body.append(f"  [{i}] {warn}\n", style="yellow")
    
    console.print(Panel(
        body,
        title="[bold]Validation LaTeX[/bold]",
        border_style=color,
        padding=(1, 2),
    ))


def cmd_latex_compile(tex_file_path: str) -> None:
    """Compile un fichier .tex en PDF."""
    
    tex_file = Path(tex_file_path)
    if not tex_file.exists():
        console.print(f"[red]Fichier non trouve: {tex_file}[/red]")
        return
    
    compiler = MikTeXCompiler()
    
    if not compiler.is_available():
        console.print(Panel(
            "  [red]MikTeX non trouve sur le systeme[/red]\n\n"
            "  Solutions:\n"
            "  1. [cyan]Windows[/cyan] : Installer MikTeX de "
            "[bold]https://miktex.org/download[/bold]\n"
            "  2. [cyan]Linux/Mac[/cyan] : [bold]brew install mactex[/bold] "
            "ou [bold]apt install texlive-full[/bold]\n"
            "  3. [cyan]Docker[/cyan] : Image contient texlive-full\n\n"
            "  Apres installation, redemarrer Gabriel pour redetection.",
            title="[red]MikTeX non disponible[/red]",
            border_style="red",
        ))
        return
    
    console.print(f"\n  [dim]Compilation {tex_file.name} -> PDF...[/dim]")
    
    success, message = compiler.compile_to_pdf(tex_file)
    
    if success:
        console.print(Panel(
            f"[green]✓ Compilation reussie[/green]\n\n  {message}",
            title="[bold green]PDF genere[/bold green]",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[red]✗ Compilation echouee[/red]\n\n  {message}",
            title="[bold red]Erreur compilation[/bold red]",
            border_style="red",
        ))


def cmd_latex_template(template_name: str) -> None:
    """Affiche un template scientifique LaTeX."""
    
    templates = {
        'methode-spectrale': (
            "Template: Methode Spectrale Savard (article complet)",
            LaTeXArticleGenerator.TEMPLATE_ARTICLE_FULL
        ),
        'court': (
            "Template: Article court (5-7 pages)",
            "% Template court - a implementer"
        ),
        'theoreme': (
            "Template: Theoreme + Preuve",
            "% Template theoreme - a implementer"
        ),
    }
    
    if template_name not in templates:
        console.print(
            f"[yellow]Template '{template_name}' inconnu[/yellow]\n\n"
            "Templates disponibles:\n"
            + "\n".join(f"  • {k}" for k in templates.keys())
        )
        return
    
    title, content = templates[template_name]
    console.print(Panel(content, title=f"[cyan]{title}[/cyan]", border_style="cyan"))


def cmd_latex_generate(question_type: str, params: dict) -> None:
    """Genere du code LaTeX pour une question."""
    
    gen = LaTeXCodeGenerator()
    
    if question_type == "rsp1x1":
        n1 = params.get("n1", 2)
        n2 = params.get("n2", 3)
        latex_code = gen.generate_rsp_section(
            A=[n1],
            B=[n2],
            rsp_value="1/2",
            rsp_decimal=0.5,
            config_type="1x1"
        )
    elif question_type == "reconstruction":
        n = params.get("n", 26)
        prime = params.get("prime", 101)
        latex_code = gen.generate_reconstruction_section(n, prime)
    elif question_type == "gap":
        p1 = params.get("p1", -19)
        p2 = params.get("p2", -5)
        delta_p = abs(p2 - p1)
        latex_code = gen.generate_gap_section(p1, p2, delta_p, "1/2")
    else:
        console.print(f"[yellow]Type inconnu: {question_type}[/yellow]")
        return
    
    console.print(Panel(
        latex_code,
        title=f"[cyan]Code LaTeX genere: {question_type}[/cyan]",
        border_style="cyan",
    ))


def cmd_miktex_check() -> None:
    """Verifie l'installation de MikTeX."""
    
    compiler = MikTeXCompiler()
    
    info = Text()
    info.append("STATUS MikTeX\n\n", style="bold cyan")
    
    if compiler.is_available():
        info.append("[green]✓ MikTeX DISPONIBLE[/green]\n\n", style="bold green")
        info.append(f"  Chemin     : {compiler.miktex_path}\n")
        info.append("  Pret pour  : compilation .tex -> PDF\n")
        info.append("  Commande   : latex compiler mon_article.tex\n")
    else:
        info.append("[red]✗ MikTeX NON TROUVE[/red]\n\n", style="bold red")
        info.append("  Installation requise pour compiler PDF\n\n")
        info.append("  [bold yellow]Installation:[/bold yellow]\n")
        info.append("    Windows : https://miktex.org/download\n")
        info.append("    macOS   : brew install mactex\n")
        info.append("    Linux   : apt install texlive-full\n\n")
        info.append("  [bold yellow]Alternative Docker:[/bold yellow]\n")
        info.append("    Compiler dans le container (texlive-full inclus)\n")
    
    console.print(Panel(
        info,
        title="[bold]MikTeX Status[/bold]",
        border_style="green" if compiler.is_available() else "red",
        padding=(1, 2),
    ))


def print_latex_help() -> None:
    """Affiche l'aide des commandes LaTeX."""
    
    help_text = """
  Commandes LaTeX pour articles mathematiques
  ============================================

  latex validate "<code>"          Valide la syntaxe LaTeX (aucune erreur)
  latex compile mon_article.tex    Compile en PDF via MikTeX
  latex template methode-spectrale Affiche template article complet
  latex generate rsp1x1 [n1] [n2] Genere section LaTeX pour Q1.a
  latex generate reconstruction    Genere section LaTeX pour Q2
  latex generate gap [p1] [p2]     Genere section LaTeX pour Q3
  latex miktex-check              Verifie installation MikTeX

  Exemples:
    latex validate "\\documentclass{article}\\begin{document}Test\\end{document}"
    latex template methode-spectrale
    latex generate rsp1x1 3 5
    latex miktex-check
"""
    
    console.print(Panel(help_text, title="[cyan]Aide LaTeX[/cyan]", border_style="cyan"))


# Export pour CLI
async def handle_latex_command(cmd: str) -> bool:
    """Gestionnaire pour commandes latex."""
    
    tokens = cmd.strip().split(maxsplit=1)
    
    if len(tokens) < 2:
        print_latex_help()
        return True
    
    sub_cmd = tokens[1].lower()
    args = cmd.strip()[len(tokens[0]) + 1 + len(tokens[1]):].strip()
    
    if sub_cmd == "validate":
        if not args:
            console.print("[yellow]Usage: latex validate \"<code>\"[/yellow]")
            return True
        cmd_latex_validate(args)
    
    elif sub_cmd == "compile":
        if not args:
            console.print("[yellow]Usage: latex compile mon_article.tex[/yellow]")
            return True
        cmd_latex_compile(args)
    
    elif sub_cmd == "template":
        template = args if args else "methode-spectrale"
        cmd_latex_template(template)
    
    elif sub_cmd == "generate":
        # Parsing: generate <type> [param1] [param2]
        gen_tokens = args.split()
        if not gen_tokens:
            console.print("[yellow]Usage: latex generate <type> [params]\\nTypes: rsp1x1, reconstruction, gap[/yellow]")
            return True
        
        gen_type = gen_tokens[0]
        params = {}
        
        if gen_type == "rsp1x1" and len(gen_tokens) >= 3:
            try:
                params['n1'] = int(gen_tokens[1])
                params['n2'] = int(gen_tokens[2])
            except ValueError:
                pass
        elif gen_type == "gap" and len(gen_tokens) >= 3:
            try:
                params['p1'] = int(gen_tokens[1])
                params['p2'] = int(gen_tokens[2])
            except ValueError:
                pass
        
        cmd_latex_generate(gen_type, params)
    
    elif sub_cmd == "miktex-check":
        cmd_miktex_check()
    
    else:
        console.print(f"[yellow]Sous-commande inconnue: {sub_cmd}[/yellow]")
        print_latex_help()
    
    return True


__all__ = [
    'handle_latex_command',
    'print_latex_help',
    'cmd_latex_validate',
    'cmd_latex_compile',
    'cmd_latex_template',
    'cmd_latex_generate',
    'cmd_miktex_check',
]
