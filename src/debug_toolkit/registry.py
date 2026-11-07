"""Registry — Detecte les outils installes et expose leur disponibilite."""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Optional


@dataclass
class ToolInfo:
    name: str
    package: str        # nom pypi pour pip install
    available: bool
    version: Optional[str] = None
    description: str = ""
    install_hint: str = ""


class ToolkitRegistry:
    """Detecte les outils disponibles au runtime."""

    TOOLS = [
        ("sympy", "sympy", "Validation symbolique des formules SA, SB, digamma"),
        ("mpmath", "mpmath", "Recalcul a precision arbitraire (100 chiffres)"),
        ("z3", "z3-solver", "Preuve formelle SMT de l'INVARIANT 1/2"),
    ]

    def __init__(self) -> None:
        self.tools: dict[str, ToolInfo] = {}
        self._detect_all()

    def _detect_all(self) -> None:
        for module_name, package, description in self.TOOLS:
            info = self._detect_one(module_name, package, description)
            self.tools[module_name] = info

    @staticmethod
    def _detect_one(module_name: str, package: str, description: str) -> ToolInfo:
        try:
            mod = importlib.import_module(module_name)
            version = None
            if hasattr(mod, "__version__"):
                version = mod.__version__
            elif module_name == "z3" and hasattr(mod, "get_version_string"):
                version = mod.get_version_string()
            return ToolInfo(
                name=module_name, package=package, available=True,
                version=version, description=description,
            )
        except ImportError:
            return ToolInfo(
                name=module_name, package=package, available=False,
                description=description,
                install_hint=f"pip install {package}",
            )

    def is_available(self, name: str) -> bool:
        return self.tools.get(name, ToolInfo(name, "", False)).available

    def all_available(self) -> bool:
        return all(t.available for t in self.tools.values())

    def render_table(self) -> str:
        """Rendu texte pour affichage CLI."""
        lines = ["TOOLKIT DEBUGGER DISPONIBLE :"]
        for info in self.tools.values():
            mark = "[OK]" if info.available else "[--]"
            v = f" v{info.version}" if info.version else ""
            hint = "" if info.available else f"  -> {info.install_hint}"
            lines.append(f"  {mark} {info.name:<10}{v:<10} {info.description}{hint}")
        return "\n".join(lines)
