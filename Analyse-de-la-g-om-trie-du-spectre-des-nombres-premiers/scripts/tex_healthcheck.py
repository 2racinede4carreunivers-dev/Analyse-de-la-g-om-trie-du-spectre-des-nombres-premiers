#!/usr/bin/env python3
"""Healthcheck statique pour documents LaTeX (.tex).

Usage:
  python scripts/tex_healthcheck.py theories/tex/mon_fichier.tex
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEX_OUTPUT_DIR = REPO_ROOT / "theories" / "tex"


def check(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"[OK] {message}")
    else:
        print(f"[FAIL] {message}")
        failures.append(message)


def balanced_braces(text: str) -> bool:
    depth = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0


def balanced_envs(text: str) -> bool:
    events = []
    for m in re.finditer(r"\\begin\{([^{}]+)\}", text):
        events.append((m.start(), "begin", m.group(1)))
    for m in re.finditer(r"\\end\{([^{}]+)\}", text):
        events.append((m.start(), "end", m.group(1)))
    events.sort(key=lambda x: x[0])

    stack: list[str] = []
    for _, kind, env in events:
        if kind == "begin":
            stack.append(env)
        else:
            if not stack:
                return False
            top = stack.pop()
            if top != env:
                return False
    return not stack


def unicode_mappings_cover_symbols(text: str) -> tuple[bool, list[str]]:
    used = {ord(ch) for ch in text if ord(ch) > 255}
    declared = {
        int(code, 16)
        for code in re.findall(r"\\DeclareUnicodeCharacter\{([0-9A-Fa-f]+)\}", text)
    }
    missing = sorted(code for code in used if code not in declared)
    missing_hex = [f"U+{code:04X}" for code in missing]
    return (len(missing) == 0, missing_hex)


def run(tex_path: Path) -> int:
    failures: list[str] = []

    check(tex_path.exists(), f"Fichier existe: {tex_path}", failures)
    if failures:
        return 1

    raw = tex_path.read_bytes()
    check(not raw.startswith(b"\xef\xbb\xbf"), "Pas de BOM UTF-8", failures)
    check(b"\x00" not in raw, "Pas d'octet NUL", failures)
    # On accepte LF ou CRLF, mais jamais un CR isole.
    normalized = raw.replace(b"\r\n", b"")
    check(b"\r" not in normalized, "Fins de ligne valides (LF ou CRLF)", failures)

    try:
        text = raw.decode("utf-8", errors="strict")
        check(True, "Decodage UTF-8 strict", failures)
    except UnicodeDecodeError:
        check(False, "Decodage UTF-8 strict", failures)
        return 1

    required = (
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[T1]{fontenc}",
        "\\usepackage[french]{babel}",
        "\\begin{document}",
        "\\tableofcontents",
        "\\end{document}",
    )
    for marker in required:
        check(marker in text, f"Marqueur present: {marker}", failures)

    check(balanced_braces(text), "Accolades equilibrees", failures)
    check(balanced_envs(text), "Environnements LaTeX equilibres", failures)

    ok_unicode, missing_hex = unicode_mappings_cover_symbols(text)
    check(ok_unicode, "Mappings Unicode declares pour symboles > U+00FF", failures)
    if not ok_unicode:
        print("  Symboles non couverts:", ", ".join(missing_hex))

    section_like = len(re.findall(r"^\\(?:sub)*section\{", text, flags=re.MULTILINE))
    tables = text.count("\\begin{longtable}")
    items = len(re.findall(r"^\\item ", text, flags=re.MULTILINE))

    print(f"[INFO] Sections detectees: {section_like}")
    print(f"[INFO] Tableaux longtable detectes: {tables}")
    print(f"[INFO] Items de liste detectes: {items}")

    check(section_like >= 50, "Densite sections >= 50", failures)
    check(tables >= 37, "Densite tableaux >= 37", failures)
    check(items >= 33, "Densite listes >= 33", failures)

    if failures:
        print(f"\nHealthcheck termine avec {len(failures)} echec(s).")
        return 1

    print("\nHealthcheck termine: OK (0 echec).")
    return 0


def compile_pdf(tex_path: Path) -> int:
    """Compile a TeX file and always write PDF artifacts under theories/tex."""
    engine = "pdflatex"
    if shutil.which(engine) is None:
        engine = "miktex-pdflatex"
    if shutil.which(engine) is None:
        print("Erreur: pdflatex/miktex-pdflatex introuvable dans le PATH.")
        return 127

    completed = subprocess.run(
        [
            engine,
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-output-directory",
            str(TEX_OUTPUT_DIR),
            str(tex_path),
        ],
        check=False,
        cwd=str(REPO_ROOT),
    )
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Healthcheck statique pour documents TeX")
    parser.add_argument("tex_file", help="Chemin du fichier .tex a verifier")
    parser.add_argument(
        "--compile-pdf",
        action="store_true",
        help="Compiler le .tex apres healthcheck et ecrire le PDF dans theories/tex",
    )
    args = parser.parse_args()

    tex_path = Path(args.tex_file)
    if not tex_path.is_absolute():
        tex_path = Path.cwd() / tex_path

    code = run(tex_path)
    if args.compile_pdf:
        compile_code = compile_pdf(tex_path)
        if compile_code != 0:
            return compile_code
    return code


if __name__ == "__main__":
    raise SystemExit(main())
