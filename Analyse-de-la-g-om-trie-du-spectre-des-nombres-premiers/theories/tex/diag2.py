#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagnostic détaillé pour les lignes problématiques."""

import re
from pathlib import Path

TEX = Path(__file__).resolve().parent / "Le-systeme-convolutif-Gabriel.tex"

content = TEX.read_text(encoding="utf-8")
lines = content.split("\n")

# Hex dump of specific lines
for ln in [2257, 2258, 2262, 2263]:
    line = lines[ln - 1]
    print(f"Line {ln}: {line.encode('utf-8')!r}")

print()

# Count all \begin{boitenote} and \end{boitenote}
begin_re = re.compile(r"\\begin\{boitenote\}")
end_re = re.compile(r"\\end\{boitenote\}")
begins = [i + 1 for i, l in enumerate(lines) if begin_re.search(l)]
ends = [i + 1 for i, l in enumerate(lines) if end_re.search(l)]
print(f"BEGIN boitenote: {len(begins)} at {begins}")
print(f"END boitenote: {len(ends)} at {ends}")
print(f"Unclosed: {len(begins) - len(ends)}")

print()

# Brace depth with proper Verbatim/verbatim handling
in_verbatim = False
in_verb = False
depth = 0
for i, line in enumerate(lines, 1):
    # Check for verbatim blocks
    if not in_verbatim:
        if re.search(r"\\begin\{verbatim\}", line) or re.search(r"\\begin\{Verbatim\}", line):
            in_verbatim = True
            # Process the part before \begin{verbatim}
            before = re.split(r"\\begin\{(verbatim|Verbatim)\}", line)[0]
            j = 0
            while j < len(before):
                ch = before[j]
                if ch == "\\":
                    j += 2
                    continue
                if ch == "%":
                    break
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                j += 1
            continue
    else:
        if re.search(r"\\end\{verbatim\}", line) or re.search(r"\\end\{Verbatim\}", line):
            in_verbatim = False
            continue
        else:
            continue

    # Normal line processing
    j = 0
    while j < len(line):
        ch = line[j]
        if ch == "\\":
            j += 2
            continue
        if ch == "%":
            break
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        j += 1

print(f"Final brace depth (with verbatim awareness): {depth}")

# If depth != 0, find where it diverges
if depth != 0:
    in_verbatim = False
    depth = 0
    for i, line in enumerate(lines, 1):
        if not in_verbatim:
            if re.search(r"\\begin\{verbatim\}", line) or re.search(r"\\begin\{Verbatim\}", line):
                in_verbatim = True
                continue
        else:
            if re.search(r"\\end\{verbatim\}", line) or re.search(r"\\end\{Verbatim\}", line):
                in_verbatim = False
                continue
            continue
        j = 0
        line_depth_before = depth
        while j < len(line):
            ch = line[j]
            if ch == "\\":
                j += 2
                continue
            if ch == "%":
                break
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1
        if line_depth_before != depth:
            print(f"  Line {i}: depth {line_depth_before}->{depth} | {line[:80]}")
