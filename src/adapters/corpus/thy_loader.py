"""
Chargeur de fichiers .thy (Isabelle/HOL) - extrait sections, definitions, axiomes.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any


SECTION_RE = re.compile(r'^section\s+"([^"]+)"', re.MULTILINE)
DEFINITION_RE = re.compile(r'^definition\s+(\w+)\s*::', re.MULTILINE)
LEMMA_RE = re.compile(r'^lemma\s+(\w+)\s*:', re.MULTILINE)
THEOREM_RE = re.compile(r'^theorem\s+(\w+)\s*:', re.MULTILINE)
AXIOM_RE = re.compile(r'axiomatization where\s*\n\s*(\w+)\s*:', re.MULTILINE)


class TheoryLoader:
    """Charge et indexe les fichiers .thy du corpus."""

    def __init__(self, theory_dir: str | Path = "/theories"):
        self.theory_dir = Path(theory_dir)
        self.theories: dict[str, dict[str, Any]] = {}

    def load_all(self) -> dict[str, dict[str, Any]]:
        """Charge tous les .thy du dossier."""
        if not self.theory_dir.exists():
            return {}
        for thy in self.theory_dir.glob("*.thy"):
            self.theories[thy.stem] = self.parse_file(thy)
        return self.theories

    def parse_file(self, path: Path) -> dict[str, Any]:
        """Extrait les sections, definitions, lemmes, theoremes et axiomes."""
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return {"name": path.stem, "sections": [], "definitions": [], "lemmas": [], "theorems": [], "axioms": [], "raw_size": 0}

        return {
            "name": path.stem,
            "path": str(path),
            "raw_size": len(content),
            "sections": SECTION_RE.findall(content),
            "definitions": DEFINITION_RE.findall(content),
            "lemmas": LEMMA_RE.findall(content),
            "theorems": THEOREM_RE.findall(content),
            "axioms": AXIOM_RE.findall(content),
        }

    def summary(self) -> str:
        """Resume textuel du corpus charge."""
        if not self.theories:
            return "Corpus HOL : aucun fichier .thy charge."
        lines = [f"Corpus HOL ({len(self.theories)} fichier(s)) :"]
        for name, info in self.theories.items():
            lines.append(
                f"  - {name}.thy : {len(info['sections'])} sections, "
                f"{len(info['definitions'])} defs, {len(info['lemmas'])} lemmes, "
                f"{len(info['theorems'])} theoremes, {len(info['axioms'])} axiomes"
            )
        return "\n".join(lines)

    def detailed_view(self) -> str:
        """Vue detaillee : sections + definitions + lemmes par fichier."""
        if not self.theories:
            return "Corpus HOL vide. Placez vos .thy dans /theories."
        out: list[str] = []
        for name, info in self.theories.items():
            out.append(f"\n=== {name}.thy ({info.get('raw_size', 0)} octets) ===")
            if info.get('sections'):
                out.append("  SECTIONS :")
                for sec in info['sections']:
                    out.append(f"    - {sec}")
            if info.get('definitions'):
                defs = info['definitions']
                out.append(f"  DEFINITIONS ({len(defs)}) : "
                           + ", ".join(defs[:8]) + (" ..." if len(defs) > 8 else ""))
            if info.get('lemmas'):
                lems = info['lemmas']
                out.append(f"  LEMMES ({len(lems)}) : "
                           + ", ".join(lems[:8]) + (" ..." if len(lems) > 8 else ""))
            if info.get('theorems'):
                ths = info['theorems']
                out.append(f"  THEOREMES ({len(ths)}) : "
                           + ", ".join(ths[:5]) + (" ..." if len(ths) > 5 else ""))
            if info.get('axioms'):
                axs = info['axioms']
                out.append(f"  AXIOMES ({len(axs)}) : " + ", ".join(axs[:6]))
        return "\n".join(out)
