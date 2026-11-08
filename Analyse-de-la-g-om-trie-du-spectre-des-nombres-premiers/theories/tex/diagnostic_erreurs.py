#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostic rapide des environnements LaTeX du .tex de Gabriel."""

import re
import sys
from pathlib import Path

TEX_PATH = Path(__file__).resolve().parent / "Le-systeme-convolutif-Gabriel.tex"


def main() -> int:
    content = TEX_PATH.read_text(encoding="utf-8")
    lines = content.split("\n")

    # --- Comptage des boitenote ---
    begin_pat = re.compile(r"\\begin\{boitenote\}")
    end_pat = re.compile(r"\\end\{boitenote\}")
    begins = [m.start() for m in begin_pat.finditer(content)]
    ends = [m.start() for m in end_pat.finditer(content)]
    print(f"[boitenote] begins={len(begins)} ends={len(ends)} diff={len(begins)-len(ends)}")

    # --- Analyse pile simple (stack-based) ---
    begin_re = re.compile(r"\\begin\{([^}]+)\}")
    end_re = re.compile(r"\\end\{([^}]+)\}")
    events = []
    for m in begin_re.finditer(content):
        events.append((m.start(), "begin", m.group(1)))
    for m in end_re.finditer(content):
        events.append((m.start(), "end", m.group(1)))
    events.sort(key=lambda x: x[0])

    stack: list[tuple[str, int]] = []
    unclosed = []
    for pos, kind, name in events:
        if kind == "begin":
            stack.append((name, pos))
        else:
            # pop until matching
            found = False
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]
                    found = True
                    break
            if not found:
                print(f"  WARNING: \\end{{{name}}} at pos {pos} has no matching begin")

    if stack:
        print(f"[PILE] {len(stack)} environnements toujours ouverts :")
        for name, pos in stack:
            line_no = content[:pos].count("\n") + 1
            print(f"  {name} opened at line {line_no}")

    # --- Bare \\ (ligne 2258 style) ---
    bare_breaks = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped == "\\\\":
            bare_breaks.append(i)
    print(f"\n[\\\\] Lignes avec seulement \\\\\\\\ : {bare_breaks}")

    # --- Verif braces balance ---
    depth = 0
    for i, ch in enumerate(content):
        if ch == "\\":
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                line_no = content[:i].count("\n") + 1
                print(f"  Brace fermante excendante a la ligne {line_no}")
                break
    print(f"[BRACES] Profondeur finale = {depth} (0 = equilibree)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())