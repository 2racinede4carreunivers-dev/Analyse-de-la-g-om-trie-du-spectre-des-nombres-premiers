"""
cline_tools_bridge.py  —  Intégration des capacités Cline dans Gabriel
═══════════════════════════════════════════════════════════════════════════════
Adapte les fonctionnalités clés de Cline pour Gabriel :
  • File Editing (create, read, update, delete)
  • Command Execution (shell commands, avec timeout et capture)
  • Tool Abstraction (dispatcher unifié)
═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import os
import re
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Any
from enum import Enum

logger = logging.getLogger("gabriel.cline_bridge")


class ToolType(Enum):
    """Types d'outils disponibles dans le bridge Cline."""
    FILE_EDIT = "file_edit"
    FILE_READ = "file_read"
    FILE_CREATE = "file_create"
    FILE_DELETE = "file_delete"
    COMMAND_EXEC = "command_exec"
    SEARCH_FILES = "search_files"


@dataclass
class ToolResult:
    """Résultat unifié de l'exécution d'un outil."""
    success: bool
    tool_type: ToolType
    output: str
    error: Optional[str] = None
    metadata: dict = None

    def __str__(self) -> str:
        result = f"[{self.tool_type.value}] {'✓' if self.success else '✗'}\n"
        if self.output:
            result += f"Output:\n{self.output}\n"
        if self.error:
            result += f"Error:\n{self.error}\n"
        return result


class ClineFileToolAdapter:
    """Adapter pour les opérations fichiers style Cline."""
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = Path(workspace_root or os.getcwd())
    
    def _resolve_path(self, file_path: str) -> Path:
        """Résout le chemin en absolu si nécessaire."""
        p = Path(file_path)
        if not p.is_absolute():
            p = self.workspace_root / p
        return p.resolve()
    
    def read_file(self, file_path: str) -> ToolResult:
        """Lit un fichier."""
        try:
            path = self._resolve_path(file_path)
            if not path.exists():
                return ToolResult(
                    success=False,
                    tool_type=ToolType.FILE_READ,
                    output="",
                    error=f"File not found: {path}"
                )
            content = path.read_text(encoding='utf-8')
            logger.info(f"Read file: {path} ({len(content)} bytes)")
            return ToolResult(
                success=True,
                tool_type=ToolType.FILE_READ,
                output=content,
                metadata={"path": str(path), "size": len(content)}
            )
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ToolResult(
                success=False,
                tool_type=ToolType.FILE_READ,
                output="",
                error=str(e)
            )
    
    def create_file(self, file_path: str, content: str) -> ToolResult:
        """Crée un nouveau fichier."""
        try:
            path = self._resolve_path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                return ToolResult(
                    success=False,
                    tool_type=ToolType.FILE_CREATE,
                    output="",
                    error=f"File already exists: {path}"
                )
            path.write_text(content, encoding='utf-8')
            logger.info(f"Created file: {path} ({len(content)} bytes)")
            return ToolResult(
                success=True,
                tool_type=ToolType.FILE_CREATE,
                output=f"Created: {path}",
                metadata={"path": str(path), "size": len(content)}
            )
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
            return ToolResult(
                success=False,
                tool_type=ToolType.FILE_CREATE,
                output="",
                error=str(e)
            )
    
    def update_file(self, file_path: str, content: str) -> ToolResult:
        """Modifie ou crée un fichier."""
        try:
            path = self._resolve_path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            logger.info(f"Updated file: {path} ({len(content)} bytes)")
            return ToolResult(
                success=True,
                tool_type=ToolType.FILE_EDIT,
                output=f"Updated: {path}",
                metadata={"path": str(path), "size": len(content)}
            )
        except Exception as e:
            logger.error(f"Error updating file {file_path}: {e}")
            return ToolResult(
                success=False,
                tool_type=ToolType.FILE_EDIT,
                output="",
                error=str(e)
            )
    
    def delete_file(self, file_path: str) -> ToolResult:
        """Supprime un fichier."""
        try:
            path = self._resolve_path(file_path)
            if not path.exists():
                return ToolResult(
                    success=False,
                    tool_type=ToolType.FILE_DELETE,
                    output="",
                    error=f"File not found: {path}"
                )
            path.unlink()
            logger.info(f"Deleted file: {path}")
            return ToolResult(
                success=True,
                tool_type=ToolType.FILE_DELETE,
                output=f"Deleted: {path}",
                metadata={"path": str(path)}
            )
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            return ToolResult(
                success=False,
                tool_type=ToolType.FILE_DELETE,
                output="",
                error=str(e)
            )
    
    def search_files(self, pattern: str, directory: Optional[str] = None) -> ToolResult:
        """Cherche des fichiers par pattern (regex)."""
        try:
            search_dir = self._resolve_path(directory or ".")
            if not search_dir.is_dir():
                return ToolResult(
                    success=False,
                    tool_type=ToolType.SEARCH_FILES,
                    output="",
                    error=f"Not a directory: {search_dir}"
                )
            
            regex = re.compile(pattern)
            matches = []
            for root, dirs, files in os.walk(search_dir):
                for f in files:
                    if regex.search(f):
                        full_path = Path(root) / f
                        matches.append(str(full_path.relative_to(self.workspace_root)))
            
            output = "\n".join(matches) if matches else "No matches found."
            logger.info(f"Search found {len(matches)} matches for pattern: {pattern}")
            return ToolResult(
                success=True,
                tool_type=ToolType.SEARCH_FILES,
                output=output,
                metadata={"pattern": pattern, "matches": len(matches)}
            )
        except Exception as e:
            logger.error(f"Error searching files with pattern {pattern}: {e}")
            return ToolResult(
                success=False,
                tool_type=ToolType.SEARCH_FILES,
                output="",
                error=str(e)
            )


class ClineCommandToolAdapter:
    """Adapter pour l'exécution de commandes style Cline."""
    
    def __init__(self, workspace_root: Optional[str] = None, timeout: int = 30):
        self.workspace_root = workspace_root or os.getcwd()
        self.timeout = timeout
    
    def execute_command(self, command: str, shell: str = "powershell") -> ToolResult:
        """Exécute une commande shell."""
        try:
            logger.info(f"Executing command: {command}")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.workspace_root
            )
            
            output = result.stdout + result.stderr
            success = result.returncode == 0
            
            logger.info(f"Command completed with exit code: {result.returncode}")
            return ToolResult(
                success=success,
                tool_type=ToolType.COMMAND_EXEC,
                output=output,
                error=None if success else f"Exit code: {result.returncode}",
                metadata={"exit_code": result.returncode, "timeout": self.timeout}
            )
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {self.timeout}s: {command}")
            return ToolResult(
                success=False,
                tool_type=ToolType.COMMAND_EXEC,
                output="",
                error=f"Command timed out after {self.timeout} seconds"
            )
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return ToolResult(
                success=False,
                tool_type=ToolType.COMMAND_EXEC,
                output="",
                error=str(e)
            )


class ClineToolDispatcher:
    """Dispatcher unifié pour tous les outils Cline."""
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.getcwd()
        self.file_adapter = ClineFileToolAdapter(workspace_root)
        self.cmd_adapter = ClineCommandToolAdapter(workspace_root)
        
        # Registre des commandes reconnues
        self.command_patterns = {
            r"^read\s+(.+)$": self._handle_read,
            r"^create\s+(.+?)\s+(.+)$": self._handle_create,
            r"^update\s+(.+?)\s+(.+)$": self._handle_update,
            r"^delete\s+(.+)$": self._handle_delete,
            r"^search\s+(.+?)(?:\s+in\s+(.+))?$": self._handle_search,
            r"^run\s+(.+)$": self._handle_run,
            r"^execute\s+(.+)$": self._handle_run,
        }
    
    def dispatch(self, command: str) -> ToolResult:
        """Dispatch une commande vers le bon outil."""
        command = command.strip()
        logger.info(f"Dispatching command: {command[:50]}...")
        
        for pattern, handler in self.command_patterns.items():
            match = re.match(pattern, command, re.IGNORECASE)
            if match:
                return handler(*match.groups())
        
        # Pas de pattern reconnu → traiter comme commande shell
        return self.cmd_adapter.execute_command(command)
    
    def _handle_read(self, file_path: str) -> ToolResult:
        return self.file_adapter.read_file(file_path.strip())
    
    def _handle_create(self, file_path: str, content: str) -> ToolResult:
        return self.file_adapter.create_file(file_path.strip(), content.strip())
    
    def _handle_update(self, file_path: str, content: str) -> ToolResult:
        return self.file_adapter.update_file(file_path.strip(), content.strip())
    
    def _handle_delete(self, file_path: str) -> ToolResult:
        return self.file_adapter.delete_file(file_path.strip())
    
    def _handle_search(self, pattern: str, directory: Optional[str] = None) -> ToolResult:
        return self.file_adapter.search_files(pattern.strip(), directory.strip() if directory else None)
    
    def _handle_run(self, command: str) -> ToolResult:
        return self.cmd_adapter.execute_command(command.strip())


# ─────────────────────────────────────────────────────────
#  Tests Unitaires
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Cline Tools Bridge Tests ===")
    
    dispatcher = ClineToolDispatcher()
    
    # Test 1: Create file
    result = dispatcher.dispatch("create test_file.txt Hello World")
    assert result.success, f"Create failed: {result.error}"
    print("[OK] Create file OK")
    
    # Test 2: Read file
    result = dispatcher.dispatch("read test_file.txt")
    assert result.success and "Hello World" in result.output, f"Read failed: {result.error}"
    print("[OK] Read file OK")
    
    # Test 3: Delete file
    result = dispatcher.dispatch("delete test_file.txt")
    assert result.success, f"Delete failed: {result.error}"
    print("[OK] Delete file OK")
    
    # Test 4: Execute command
    result = dispatcher.dispatch("run powershell -Command \"Write-Host 'test'\"")
    assert result.success, f"Command execution failed: {result.error}"
    print("[OK] Command execution OK")
    
    print("\n[SUCCESS] All bridge tests passed!")
