"""
hybrid_dispatcher.py  —  Dispatcher unifié Gabriel + Cline
═══════════════════════════════════════════════════════════════════════════════
Fusionne le dispatch Gabriel (ratio, analyse, validation) avec les outils Cline
(file editing, command execution).

Détecte automatiquement si la requête est :
  1. Une commande Cline (file edit, run, search, etc.)
  2. Une requête Gabriel native (ratio 1/k, analyse vision, etc.)
  3. Un appel LLM routé automatiquement
═══════════════════════════════════════════════════════════════════════════════
"""

import re
import logging
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, Callable

from .cline_tools_bridge import ClineToolDispatcher, ToolResult
from ..dispatch.ratio_dispatcher import dispatch_from_prompt as gabriel_dispatch

logger = logging.getLogger("gabriel.hybrid_dispatcher")


class CommandCategory(Enum):
    """Catégories de commandes."""
    CLINE_FILE = "cline_file"        # read, create, update, delete
    CLINE_EXEC = "cline_exec"        # run, execute
    CLINE_SEARCH = "cline_search"    # search
    GABRIEL_MATH = "gabriel_math"    # ratio 1/k, spectral, etc.
    GABRIEL_VISION = "gabriel_vision"  # analyse image
    GABRIEL_VALIDATION = "gabriel_validation"  # validation HOL/Isabelle
    GABRIEL_COGNITION = "gabriel_cognition"  # cognitive pipeline
    LLM_ROUTING = "llm_routing"      # autres requêtes → LLM


@dataclass
class DispatchResult:
    """Résultat du dispatching."""
    category: CommandCategory
    is_cline: bool  # True si c'est une commande Cline
    is_gabriel: bool  # True si c'est une requête Gabriel native
    command_text: str
    cline_result: Optional[ToolResult] = None
    gabriel_handler: Optional[Callable] = None
    metadata: dict = None


class HybridDispatcher:
    """Dispatcher unifié Gabriel + Cline."""
    
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root
        self.cline_dispatcher = ClineToolDispatcher(workspace_root)
        self.gabriel_dispatch = gabriel_dispatch
        
        # Patterns Cline (évalués d'abord)
        self.cline_patterns = {
            r"^(read|cat)\s+": CommandCategory.CLINE_FILE,
            r"^(create|write|touch)\s+": CommandCategory.CLINE_FILE,
            r"^(update|edit|modify)\s+": CommandCategory.CLINE_FILE,
            r"^(delete|remove|rm)\s+": CommandCategory.CLINE_FILE,
            r"^(search|grep|find)\s+": CommandCategory.CLINE_SEARCH,
            r"^(run|execute|exec|do)\s+": CommandCategory.CLINE_EXEC,
        }
        
        # Patterns Gabriel (après Cline)
        self.gabriel_patterns = {
            r"(?:ratio|spectral|1/\d)": CommandCategory.GABRIEL_MATH,
            r"(?:analyse|analyse image|vision|image|examine|scan|valide)": CommandCategory.GABRIEL_VISION,
            r"(?:hol|isabelle|formal|proof|validation)": CommandCategory.GABRIEL_VALIDATION,
            r"(?:cognitive|multiloop|cognition|think|reflect)": CommandCategory.GABRIEL_COGNITION,
        }
    
    def detect_category(self, command: str) -> CommandCategory:
        """Détecte la catégorie d'une commande."""
        command_lower = command.lower().strip()
        
        # 1. Patterns Cline d'abord (priorité haute)
        for pattern, category in self.cline_patterns.items():
            if re.search(pattern, command_lower):
                logger.debug(f"Detected CLINE command: {category.value}")
                return category
        
        # 2. Patterns Gabriel
        for pattern, category in self.gabriel_patterns.items():
            if re.search(pattern, command_lower):
                logger.debug(f"Detected GABRIEL command: {category.value}")
                return category
        
        # 3. Default : LLM routing
        logger.debug("No specific pattern matched → LLM routing")
        return CommandCategory.LLM_ROUTING
    
    def dispatch(self, command: str) -> DispatchResult:
        """Dispatch une commande vers le bon subsystème."""
        command = command.strip()
        logger.info(f"HybridDispatcher: {command[:60]}...")
        
        category = self.detect_category(command)
        
        # Commandes Cline
        if category in [
            CommandCategory.CLINE_FILE,
            CommandCategory.CLINE_EXEC,
            CommandCategory.CLINE_SEARCH
        ]:
            cline_result = self.cline_dispatcher.dispatch(command)
            return DispatchResult(
                category=category,
                is_cline=True,
                is_gabriel=False,
                command_text=command,
                cline_result=cline_result,
                metadata={
                    "tool_type": cline_result.tool_type.value,
                    "success": cline_result.success
                }
            )
        
        # Commandes Gabriel natives
        elif category == CommandCategory.GABRIEL_MATH:
            try:
                ratio, formulas = self.gabriel_dispatch(command)
                return DispatchResult(
                    category=category,
                    is_cline=False,
                    is_gabriel=True,
                    command_text=command,
                    gabriel_handler=lambda: (ratio, formulas),
                    metadata={"ratio": ratio, "k": formulas.k}
                )
            except Exception as e:
                logger.warning(f"Gabriel math dispatch failed: {e}")
                # Fallback to LLM
                return DispatchResult(
                    category=CommandCategory.LLM_ROUTING,
                    is_cline=False,
                    is_gabriel=False,
                    command_text=command,
                    metadata={"fallback_reason": str(e)}
                )
        
        elif category == CommandCategory.GABRIEL_VISION:
            return DispatchResult(
                category=category,
                is_cline=False,
                is_gabriel=True,
                command_text=command,
                gabriel_handler=lambda: f"Vision analysis for: {command}",
                metadata={"type": "vision_analysis"}
            )
        
        elif category == CommandCategory.GABRIEL_VALIDATION:
            return DispatchResult(
                category=category,
                is_cline=False,
                is_gabriel=True,
                command_text=command,
                gabriel_handler=lambda: f"Formal validation for: {command}",
                metadata={"type": "formal_validation"}
            )
        
        elif category == CommandCategory.GABRIEL_COGNITION:
            return DispatchResult(
                category=category,
                is_cline=False,
                is_gabriel=True,
                command_text=command,
                gabriel_handler=lambda: f"Cognitive processing for: {command}",
                metadata={"type": "cognitive_pipeline"}
            )
        
        # LLM routing (default)
        else:
            return DispatchResult(
                category=CommandCategory.LLM_ROUTING,
                is_cline=False,
                is_gabriel=False,
                command_text=command,
                metadata={"type": "llm_routing"}
            )
    
    def get_help(self) -> str:
        """Affiche l'aide sur les commandes disponibles."""
        return """
╭─ GABRIEL + CLINE HYBRID COMMANDS ─────────────────────────╮
│                                                             │
│  CLINE TOOLS (File & Execution)                            │
│  ├─ read <path>              Read file content             │
│  ├─ create <path> <content>  Create new file               │
│  ├─ update <path> <content>  Update/modify file            │
│  ├─ delete <path>            Delete file                   │
│  ├─ search <pattern> [in dir] Search files by pattern      │
│  └─ run <command>            Execute shell command         │
│                                                             │
│  GABRIEL CAPABILITIES (Native)                             │
│  ├─ ratio 1/k, spectral      Spectral math analysis        │
│  ├─ analyse image <path>     Vision/image analysis         │
│  ├─ validation, proof, HOL   Formal verification          │
│  ├─ cognitive, multiloop     Multi-loop cognition         │
│  └─ (other)                  Route to LLM                  │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
"""


# ─────────────────────────────────────────────────────────
#  Tests Unitaires
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Hybrid Dispatcher Tests ===")
    
    dispatcher = HybridDispatcher()
    
    # Test 1: Detect Cline file command
    category = dispatcher.detect_category("read /path/to/file.txt")
    assert category == CommandCategory.CLINE_FILE, f"Failed: {category}"
    print("✓ Cline file detection OK")
    
    # Test 2: Detect Cline execution
    category = dispatcher.detect_category("run python script.py")
    assert category == CommandCategory.CLINE_EXEC, f"Failed: {category}"
    print("✓ Cline exec detection OK")
    
    # Test 3: Detect Gabriel math
    category = dispatcher.detect_category("Calculate spectral ratio 1/2")
    assert category == CommandCategory.GABRIEL_MATH, f"Failed: {category}"
    print("✓ Gabriel math detection OK")
    
    # Test 4: Detect Gabriel vision
    category = dispatcher.detect_category("analyse image /path/image.png")
    assert category == CommandCategory.GABRIEL_VISION, f"Failed: {category}"
    print("✓ Gabriel vision detection OK")
    
    # Test 5: LLM routing
    category = dispatcher.detect_category("What is the weather today?")
    assert category == CommandCategory.LLM_ROUTING, f"Failed: {category}"
    print("✓ LLM routing detection OK")
    
    # Test 6: Help
    help_text = dispatcher.get_help()
    assert "GABRIEL" in help_text and "CLINE" in help_text
    print("✓ Help text OK")
    
    print("\nAll hybrid dispatcher tests passed!")
