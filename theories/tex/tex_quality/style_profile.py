#!/usr/bin/env python3
"""Build a lightweight author style profile from TeX prose.

The profile is used as a soft guide to keep the author's voice while improving
orthography and grammar with external tools.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from statistics import mean

# SÉCURITÉ: Regex corrigée - éviter les portées de caractères ambiguës
# Ancienne regex problématique: r"[A-Za-zA-za-z0-9'\-]+"
# Problème: A-za-z inclut les caractères [\]^_` (ASCII 91-96)
# Nouveau: ordre correct A-Z puis a-z, tiret échappé
WORD_RE = re.compile(r"[A-Za-z0-9'\-]+")
SENTENCE_RE = re.compile(r"[^.!?]+[.!?]")


def extract_plain_lines(tex_text: str) -> list[str]:
    lines = []
    in_math_block = False
    for raw in tex_text.splitlines():
        line = raw.strip()

        if "\\[" in line or line.startswith("$$") or line.startswith("\\begin{equation"):
            in_math_block = True
        if in_math_block:
            if "\\]" in line or line.endswith("$$") or line.startswith("\\end{equation"):
                in_math_block = False
            continue

        if not line or line.startswith("%"):
            continue

        # Keep prose-only lines. We intentionally skip command-heavy lines.
        if "\\" in line or "$" in line or "{" in line or "}" in line:
            continue

        lines.append(line)
    return lines


def build_profile(lines: list[str]) -> dict:
    words = []
    sentence_lengths = []
    line_lengths = []

    for line in lines:
        line_lengths.append(len(line))
        line_words = [w.lower() for w in WORD_RE.findall(line)]
        words.extend(line_words)
        for sentence in SENTENCE_RE.findall(line):
            sent_words = WORD_RE.findall(sentence)
            if sent_words:
                sentence_lengths.append(len(sent_words))

    unigrams = Counter(words)
    profile = {
        "line_count": len(lines),
        "token_count": len(words),
        "avg_line_chars": round(mean(line_lengths), 3) if line_lengths else 0.0,
        "avg_sentence_words": round(mean(sentence_lengths), 3) if sentence_lengths else 0.0,
        "top_unigrams": unigrams.most_common(200),
    }
    return profile


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a style profile from TeX prose")
    parser.add_argument("--input", required=True, help="Input .tex file")
    parser.add_argument("--output", required=True, help="Output .json profile")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    text = input_path.read_text(encoding="utf-8")
    lines = extract_plain_lines(text)
    profile = build_profile(lines)

    output_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Style profile written to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
