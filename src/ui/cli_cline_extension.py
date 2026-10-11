"""
cli_cline_extension.py  —  Extension Cline pour Gabriel CLI
═══════════════════════════════════════════════════════════════════════════════
Ajoute les capacités Cline au CLI Gabriel :
  • File operations (read, create, update, delete)
  • Command execution (run, execute)
  • File search (search, grep)

S'intègre dans la boucle REPL existante de Gabriel sans modifier son core.
═══════════════════════════════════════════════════════════════════════════════
"""

import logging
from pathlib import Path
from typing import Optional, Callable

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from ..adapters.hybrid_dispatcher import HybridDispatcher, CommandCategory
from ..adapters.cline_tools_bridge import ToolResult

logger = logging.getLogger("gabriel.cli_cline_ext")
console = Console()


class CLIClikeExtension:
    """Extension Cline pour le CLI Gabriel."""
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.dispatcher = HybridDispatcher(workspace_root)
        self.workspace_root = workspace_root or Path.cwd()
    
    def handle_cline_command(self, command: str) -> bool:
        """
        Traite une commande Cline et affiche le résultat.
        Retourne True si la commande a été traitée, False sinon.
        """
        command = command.strip()
        if not command:
            return False
        
        # Dispatch la commande
        result = self.dispatcher.dispatch(command)
        
        # Si c'est une commande Cline, traiter le résultat
        if result.is_cline and result.cline_result:
            self._display_cline_result(result.cline_result)
            return True
        
        # Si c'est une commande Gabriel native
        if result.is_gabriel and result.gabriel_handler:
            try:
                output = result.gabriel_handler()
                console.print(f"[bold cyan]Gabriel:[/bold cyan] {output}")
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")
            return True
        
        # Sinon, pas géré par l'extension
        return False
    
    def _display_cline_result(self, result: ToolResult) -> None:
        """Affiche le résultat d'une commande Cline de manière formatée."""
        
        # Couleur selon succès/erreur
        status_color = "green" if result.success else "red"
        status_icon = "OK" if result.success else "ERROR"
        
        # Créer le panel
        output_text = result.output if result.output else "(no output)"
        
        # Si c'est un fichier, faire une syntaxe highlight
        if result.tool_type.value == "file_read" and result.metadata:
            path = result.metadata.get("path", "")
            if path.endswith((".py", ".ts", ".js", ".go")):
                try:
                    lexer = self._get_lexer_for_path(path)
                    output_text = Syntax(result.output, lexer, theme="monokai", line_numbers=True)
                except Exception:
                    pass  # Fallback to plain text
        
        # Panel principal
        title_text = f"[bold {status_color}]{status_icon}  {result.tool_type.value}[/bold {status_color}]"
        panel = Panel(
            output_text,
            title=title_text,
            border_style=status_color,
            padding=(1, 2),
        )
        console.print(panel)
        
        # Afficher les erreurs en rouge
        if result.error:
            console.print(f"\n[red]Error: {result.error}[/red]")
        
        # Afficher les métadonnées si pertinentes
        if result.metadata:
            self._display_metadata(result.metadata)
    
    def _get_lexer_for_path(self, path: str) -> str:
        """Retourne un lexer Pygments selon l'extension du fichier."""
        ext_map = {
            ".py": "python",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".js": "javascript",
            ".jsx": "javascript",
            ".go": "go",
            ".rs": "rust",
            ".c": "c",
            ".cpp": "cpp",
            ".sh": "bash",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
            ".tex": "latex",
        }
        ext = Path(path).suffix.lower()
        return ext_map.get(ext, "text")
    
    def _display_metadata(self, metadata: dict) -> None:
        """Affiche les métadonnées dans un tableau."""
        if not metadata:
            return
        
        table = Table(title="Metadata", show_header=False, box=None)
        table.add_column(style="dim")
        table.add_column(style="white")
        
        for key, value in metadata.items():
            table.add_row(f"  {key}:", str(value))
        
        console.print(table)
    
    def get_cline_help(self) -> str:
        """Retourne le texte d'aide pour les commandes Cline."""
        return self.dispatcher.get_help()
    
    def is_cline_command(self, command: str) -> bool:
        """Vérifie si la commande est une commande Cline."""
        category = self.dispatcher.detect_category(command)
        return category in [
            CommandCategory.CLINE_FILE,
            CommandCategory.CLINE_EXEC,
            CommandCategory.CLINE_SEARCH
        ]


def integrate_cline_in_cli(cli_interface_class) -> None:
    """
    Intègre l'extension Cline dans la classe CLI existante de Gabriel.
    
    Ajoute la méthode `_handle_cline_command` et enrichit `handle_command`.
    
    Usage:
        integrate_cline_in_cli(CLIInterface)
        # Maintenant, CLIInterface a les méthodes Cline
    """
    
    def __init_with_cline__(self, *args, **kwargs):
        """Initialiser avec support Cline."""
        self.__original_init__(*args, **kwargs)
        self._cline_ext = CLIClikeExtension(
            workspace_root=self.workspace_root if hasattr(self, 'workspace_root') else None
        )
    
    def handle_command_with_cline(self, cmd: str) -> bool:
        """Enrichi avec support Cline."""
        # Essayer d'abord Cline
        if self._cline_ext.handle_cline_command(cmd):
            return True
        # Sinon, utiliser le handler original
        return self.__original_handle_command__(cmd)
    
    def get_help_with_cline(self) -> str:
        """Help enrichi avec commandes Cline."""
        original_help = self.__original_get_help__() if hasattr(self, '__original_get_help__') else ""
        cline_help = self._cline_ext.get_cline_help()
        return f"{original_help}\n{cline_help}"
    
    # Patcher la classe
    cli_interface_class.__original_init__ = cli_interface_class.__init__
    cli_interface_class.__original_handle_command__ = cli_interface_class.handle_command if hasattr(cli_interface_class, 'handle_command') else lambda self, cmd: False
    cli_interface_class.__original_get_help__ = cli_interface_class.get_help if hasattr(cli_interface_class, 'get_help') else lambda self: ""
    
    cli_interface_class.__init__ = __init_with_cline__
    if hasattr(cli_interface_class, 'handle_command'):
        cli_interface_class.handle_command = handle_command_with_cline
    if hasattr(cli_interface_class, 'get_help'):
        cli_interface_class.get_help = get_help_with_cline
    
    logger.info("✓ Cline extension integrated into CLI")


# ─────────────────────────────────────────────────────────
#  Tests Unitaires
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Cline CLI Extension Tests ===")
    
    ext = CLIClikeExtension()
    
    # Test 1: Créer un fichier
    result = ext.handle_cline_command("create test.txt Hello from Cline")
    assert result, "Create command should be handled"
    print("✓ Create file OK")
    
    # Test 2: Lire le fichier
    result = ext.handle_cline_command("read test.txt")
    assert result, "Read command should be handled"
    print("✓ Read file OK")
    
    # Test 3: Détecter une commande Cline
    is_cline = ext.is_cline_command("run python script.py")
    assert is_cline, "Should detect as Cline command"
    print("✓ Cline detection OK")
    
    # Test 4: Supprimer le fichier
    result = ext.handle_cline_command("delete test.txt")
    assert result, "Delete command should be handled"
    print("✓ Delete file OK")
    
    print("\nAll CLI extension tests passed!")
