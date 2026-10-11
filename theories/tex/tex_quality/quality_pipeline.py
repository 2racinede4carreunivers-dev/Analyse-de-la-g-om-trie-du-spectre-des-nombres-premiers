#!/usr/bin/env python3
"""TeX quality pipeline with strict semantic guard.

Goals:
- Improve prose quality in .tex files.
- Preserve exact mathematical meaning and never touch HOL validation logic.
- Enforce a quality gate based on semantic preservation score.

This script only edits prose lines and skips math/command-heavy lines by design.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
TEX_OUTPUT_DIR = Path(__file__).resolve().parents[1]

# SÉCURITÉ: Regex corrigée - éviter les portées de caractères ambiguës
# Ancienne regex problématique: r"[A-Za-zA-za-z0-9'\-]+"
# Problème: A-za-z inclut les caractères [\]^_` (ASCII 91-96)
# Nouveau: ordre correct A-Z puis a-z, tiret échappé
WORD_RE = re.compile(r"[A-Za-z0-9'\-]+")
NUMBER_RE = re.compile(r"\d+(?:[\.,]\d+)?")
NEGATION_RE = re.compile(r"\b(ne|n'|pas|jamais|aucun|sans|ni|non)\b", re.IGNORECASE)
TRAILING_LINEBREAK_RE = re.compile(r"^(.*?)(\s*\\\\\s*)$")
TEX_COMMAND_RE = re.compile(r"\\[A-Za-z@]+(?:\[[^\]]*\])?(?:\{[^{}]*\})*")
TEX_ESCAPED_CHAR_RE = re.compile(r"\\[_#%&${}~^\\]")

try:
    from spellchecker import SpellChecker
except Exception:  # pragma: no cover - optional dependency
    SpellChecker = None

SPELLCHECKER_FR = None
if SpellChecker is not None:
    try:
        SPELLCHECKER_FR = SpellChecker(language="fr")
        SPELLCHECKER_FR.distance = 2
    except Exception:
        SPELLCHECKER_FR = None

SPELLCHECK_EXEMPT_TOKENS = {
    "isabelle",
    "hol",
    "llm",
    "pdf",
    "tex",
    "json",
    "yaml",
    "csv",
    "github",
    "ollama",
    "claude",
    "openai",
    "python",
    "languagetool",
    "readme.md",
    "readme",
    "apache",
    "btb",
    "termium",
    "gdt",
    "oqlf",
    "fr-ca",
    "qa_output",
    "termbase_ca_qc",
}

PHRASE_FIXES = {
    "Toute est tiré": "Tout est tiré",
    "Vous êtes invités a consulter": "Vous êtes invités à consulter",
    "mise en place et à la dispositon des contributeur": "mise à disposition des contributeurs",
    "Readme": "README",
    "Bienvenu a tous": "Bienvenue à tous",
    "Apach 2.0": "Apache 2.0",
    "Apach License 2.0": "Apache License 2.0",
    "a la primalité": "à la primalité",
    "a contre sens": "à contre-sens",
    "jusqu'a": "jusqu'à",
    "commençant a": "commençant à",
    "dispositon": "disposition",
    "methode": "méthode",
}


@dataclass
class TermRule:
    preferred: str
    variant: str
    source: str
    source_url: str
    note: str


def load_termbase(path: Path) -> list[TermRule]:
    rules: list[TermRule] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rules.append(
                TermRule(
                    preferred=row.get("preferred_term", "").strip(),
                    variant=row.get("variant", "").strip(),
                    source=row.get("source", "").strip(),
                    source_url=row.get("source_url", "").strip(),
                    note=row.get("note", "").strip(),
                )
            )
    return [r for r in rules if r.preferred and r.variant]


def is_prose_line(line: str, in_math_block: bool) -> tuple[bool, bool]:
    stripped = line.strip()
    if not stripped or stripped.startswith("%"):
        return False, in_math_block

    # Detect and track math blocks.
    if "\\[" in stripped or stripped.startswith("$$") or stripped.startswith("\\begin{equation"):
        in_math_block = True
    if in_math_block:
        if "\\]" in stripped or stripped.endswith("$$") or stripped.startswith("\\end{equation"):
            in_math_block = False
        return False, in_math_block

    # Strict safety filter: skip command-heavy or formula-heavy lines.
    if "\\" in stripped or "$" in stripped or "{" in stripped or "}" in stripped:
        return False, in_math_block

    # Skip technical config-like lines (LaTeX options, placeholders).
    if stripped == "#1":
        return False, in_math_block
    if re.match(r"^[A-Za-z_][A-Za-z0-9_\-]*\s*=\s*[^=]+,?$", stripped):
        return False, in_math_block

    # Keep only substantial prose chunks.
    if len(WORD_RE.findall(stripped)) < 4:
        return False, in_math_block

    return True, in_math_block


def split_trailing_linebreak(line: str) -> tuple[str, str]:
    """Sépare un éventuel `\\` terminal pour corriger le texte sans perdre la mise en page."""
    match = TRAILING_LINEBREAK_RE.match(line)
    if not match:
        return line, ""
    return match.group(1), match.group(2)


def mask_tex_fragments(text: str) -> tuple[str, dict[str, str]]:
    """Masque les commandes TeX simples pour corriger seulement le texte visible."""
    placeholders: dict[str, str] = {}

    def _replace(pattern: re.Pattern[str], source: str, prefix: str) -> str:
        def repl(match: re.Match[str]) -> str:
            key = f"__{prefix}{len(placeholders)}__"
            placeholders[key] = match.group(0)
            return key

        return pattern.sub(repl, source)

    masked = _replace(TEX_COMMAND_RE, text, "TEXCMD")
    masked = _replace(TEX_ESCAPED_CHAR_RE, masked, "TEXESC")
    return masked, placeholders


def unmask_tex_fragments(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for key, value in placeholders.items():
        restored = restored.replace(key, value)
    return restored


def fallback_local_fixes(text: str) -> str:
    # Conservative fixes only. Avoid semantic rewrites.
    out = text
    for old, new in PHRASE_FIXES.items():
        out = out.replace(old, new)

    if SPELLCHECKER_FR is None:
        replacements = {
            " a l ": " a l'",
            " d un ": " d'un ",
            " l Espace ": " l'Espace ",
            " de Theodore": " de Theodore",
            " geometrique": " geometrique",
            " geometriques": " geometriques",
        }
        padded = f" {out} "
        for old, new in replacements.items():
            padded = padded.replace(old, new)
        return padded.strip()

    corrected_parts: list[str] = []
    for part in re.split(r"(\W+)", out):
        if not part or not part.isalpha():
            corrected_parts.append(part)
            continue

        lower = part.lower()
        if (
            len(lower) <= 3
            or lower in SPELLCHECK_EXEMPT_TOKENS
            or re.search(r"[A-Z].*[A-Z]", part)
            or "_" in part
            or "/" in part
            or "-" in part
            or lower.isnumeric()
        ):
            corrected_parts.append(part)
            continue

        if lower in SPELLCHECKER_FR:
            corrected_parts.append(part)
            continue

        candidate = SPELLCHECKER_FR.correction(lower)
        if not candidate or candidate == lower:
            corrected_parts.append(part)
            continue

        if part[0].isupper():
            # Guard against proper-name drifts (e.g. Savard -> Bavard).
            corrected_parts.append(part)
            continue

        corrected_parts.append(candidate)

    return "".join(corrected_parts)


def run_languagetool_if_available(text: str, lang: str) -> str:
    try:
        import language_tool_python  # type: ignore
    except Exception:
        return fallback_local_fixes(text)

    try:
        tool = language_tool_python.LanguageToolPublicAPI(lang)
        matches = tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        return corrected
    except Exception:
        # Fallback to local LanguageTool server when public API is unavailable.
        try:
            tool = language_tool_python.LanguageTool(lang)
            matches = tool.check(text)
            corrected = language_tool_python.utils.correct(text, matches)
            return corrected
        except Exception:
            return fallback_local_fixes(text)


def tokenize(s: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(s)]


def cosine_similarity(a: str, b: str) -> float:
    ca = Counter(tokenize(a))
    cb = Counter(tokenize(b))
    if not ca or not cb:
        return 1.0
    keys = set(ca) | set(cb)
    dot = sum(ca[k] * cb[k] for k in keys)
    na = math.sqrt(sum(v * v for v in ca.values()))
    nb = math.sqrt(sum(v * v for v in cb.values()))
    if na == 0 or nb == 0:
        return 1.0
    return dot / (na * nb)


def numbers_preserved(a: str, b: str) -> float:
    na = NUMBER_RE.findall(a)
    nb = NUMBER_RE.findall(b)
    return 1.0 if na == nb else 0.0


def negation_preserved(a: str, b: str) -> float:
    ca = len(NEGATION_RE.findall(a))
    cb = len(NEGATION_RE.findall(b))
    return 1.0 if ca == cb else 0.0


def semantic_score_out_of_10(original: str, corrected: str) -> float:
    cs = cosine_similarity(original, corrected)
    np = numbers_preserved(original, corrected)
    ng = negation_preserved(original, corrected)

    # Weighted score with heavy emphasis on lexical overlap and invariants.
    score_0_1 = 0.75 * cs + 0.15 * np + 0.10 * ng
    return round(score_0_1 * 10.0, 3)


def apply_termbase_preferred_forms(text: str, rules: Iterable[TermRule]) -> tuple[str, list[dict]]:
    updated = text
    hits: list[dict] = []

    for rule in rules:
        pattern = re.compile(rf"\b{re.escape(rule.variant)}\b", re.IGNORECASE)
        if pattern.search(updated):
            updated = pattern.sub(rule.preferred, updated)
            hits.append(
                {
                    "variant": rule.variant,
                    "preferred": rule.preferred,
                    "source": rule.source,
                    "source_url": rule.source_url,
                    "note": rule.note,
                }
            )
    return updated, hits


def run_single_pass(
    input_text: str,
    term_rules: list[TermRule],
    semantic_threshold: float,
    language: str,
) -> tuple[str, dict]:
    lines = input_text.splitlines()

    in_math_block = False
    updated_lines = list(lines)
    edits = []
    original_editable_chunks: list[str] = []
    accepted_editable_chunks: list[str] = []

    for idx, line in enumerate(lines):
        line_body, trailing = split_trailing_linebreak(line)
        masked_body, placeholders = mask_tex_fragments(line_body)
        editable, in_math_block = is_prose_line(masked_body, in_math_block)
        if not editable:
            continue

        original_editable_chunks.append(masked_body)

        candidate_masked = masked_body
        candidate_masked, term_hits = apply_termbase_preferred_forms(candidate_masked, term_rules)
        candidate_masked = run_languagetool_if_available(candidate_masked, language)
        candidate_visible = unmask_tex_fragments(candidate_masked, placeholders)

        if candidate_visible == line_body:
            accepted_editable_chunks.append(masked_body)
            continue

        score = semantic_score_out_of_10(masked_body, candidate_masked)
        accepted = score >= semantic_threshold

        edit = {
            "line": idx + 1,
            "original": line_body,
            "candidate": candidate_visible,
            "semantic_score": score,
            "threshold": semantic_threshold,
            "accepted": accepted,
            "term_sources": term_hits,
            "trailing_linebreak_preserved": bool(trailing),
        }
        edits.append(edit)

        if accepted:
            updated_lines[idx] = candidate_visible + trailing
            accepted_editable_chunks.append(candidate_masked)
        else:
            accepted_editable_chunks.append(masked_body)

    doc_original = "\n".join(original_editable_chunks)
    doc_after = "\n".join(accepted_editable_chunks)
    global_semantic_score = semantic_score_out_of_10(doc_original, doc_after)
    final_acceptance = global_semantic_score >= semantic_threshold

    report = {
        "total_edits_found": len(edits),
        "total_edits_accepted": sum(1 for e in edits if e["accepted"]),
        "global_semantic_score": global_semantic_score,
        "final_acceptance": final_acceptance,
        "edits": edits,
    }

    return "\n".join(updated_lines) + "\n", report


def run_healthcheck(tex_path: Path, script_path: Path) -> dict:
    result = {
        "enabled": True,
        "script": str(script_path),
        "target": str(tex_path),
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "passed": False,
    }

    if not script_path.exists():
        result["enabled"] = False
        result["stderr"] = f"Healthcheck script introuvable: {script_path}"
        return result

    completed = subprocess.run(
        [sys.executable, str(script_path), str(tex_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    result["returncode"] = completed.returncode
    result["stdout"] = completed.stdout
    result["stderr"] = completed.stderr
    result["passed"] = completed.returncode == 0
    return result


def resolve_tex_output_path(requested_output: Path) -> Path:
    """Force corrected TeX artifacts into theories/tex."""
    return TEX_OUTPUT_DIR / requested_output.name


def compile_pdf(tex_path: Path) -> dict:
    """Compile corrected TeX and place PDF artifacts in theories/tex."""
    engine = "pdflatex"
    if shutil.which(engine) is None:
        engine = "miktex-pdflatex"
    if shutil.which(engine) is None:
        return {
            "enabled": True,
            "engine": None,
            "returncode": 127,
            "stdout": "",
            "stderr": "pdflatex/miktex-pdflatex introuvable dans le PATH",
            "pdf_path": "",
            "passed": False,
        }

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
        capture_output=True,
        text=True,
        check=False,
        cwd=str(REPO_ROOT),
    )
    pdf_path = TEX_OUTPUT_DIR / f"{tex_path.stem}.pdf"
    return {
        "enabled": True,
        "engine": engine,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "pdf_path": str(pdf_path),
        "passed": completed.returncode == 0 and pdf_path.exists(),
    }


def process_file(
    input_path: Path,
    output_path: Path,
    report_path: Path,
    termbase_path: Path,
    semantic_threshold: float,
    language: str,
    dry_run: bool,
    passes: int,
    healthcheck_script: Path | None,
    editorial_context_path: Path | None,
    style_profile_path: Path | None,
    compile_after: bool,
) -> None:
    term_rules = load_termbase(termbase_path)
    current_text = input_path.read_text(encoding="utf-8")
    pass_reports: list[dict] = []
    output_path = resolve_tex_output_path(output_path)

    total_passes = max(1, passes)
    for pass_index in range(1, total_passes + 1):
        current_text, pass_report = run_single_pass(
            current_text,
            term_rules=term_rules,
            semantic_threshold=semantic_threshold,
            language=language,
        )
        pass_report["pass_index"] = pass_index
        pass_report["passes_requested"] = total_passes
        pass_reports.append(pass_report)
        if pass_report["total_edits_accepted"] == 0:
            break

    report = {
        "input": str(input_path),
        "output": str(output_path),
        "semantic_threshold": semantic_threshold,
        "language": language,
        "passes_requested": total_passes,
        "passes_run": len(pass_reports),
        "pass_reports": pass_reports,
        "total_edits_found": sum(p["total_edits_found"] for p in pass_reports),
        "total_edits_accepted": sum(p["total_edits_accepted"] for p in pass_reports),
        "global_semantic_score": pass_reports[-1]["global_semantic_score"] if pass_reports else 10.0,
        "final_acceptance": pass_reports[-1]["final_acceptance"] if pass_reports else True,
        "edits": [edit for p in pass_reports for edit in p["edits"]],
        "compliance_note": (
            "Always verify TERMIUM Plus and GDT/OQLF reuse conditions before bulk import. "
            "This pipeline stores source attribution per terminology replacement."
        ),
    }

    if editorial_context_path and editorial_context_path.exists():
        report["editorial_context_path"] = str(editorial_context_path)
        report["editorial_context_excerpt"] = editorial_context_path.read_text(encoding="utf-8")[:4000]

    if style_profile_path and style_profile_path.exists():
        try:
            report["style_profile"] = json.loads(style_profile_path.read_text(encoding="utf-8"))
        except Exception as exc:
            report["style_profile_error"] = str(exc)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if dry_run:
        print("Dry-run mode: no file written.")
    else:
        output_text = current_text
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
        print(f"Corrected TeX written to {output_path}")

        if healthcheck_script is not None:
            health = run_healthcheck(output_path, healthcheck_script)
            report["healthcheck"] = health
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(health["stdout"], end="")
            if health["stderr"]:
                print(health["stderr"], end="", file=sys.stderr)

        if compile_after:
            compilation = compile_pdf(output_path)
            report["compilation"] = compilation
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            if compilation["stdout"]:
                print(compilation["stdout"], end="")
            if compilation["stderr"]:
                print(compilation["stderr"], end="", file=sys.stderr)

    print(f"Report written to {report_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="TeX quality pipeline with semantic guard")
    parser.add_argument("--input", required=True, help="Input .tex file")
    parser.add_argument("--output", required=True, help="Output corrected .tex file")
    parser.add_argument("--report", required=True, help="Output JSON report file")
    parser.add_argument(
        "--termbase",
        default=str(Path(__file__).with_name("termbase_ca_qc.csv")),
        help="CSV termbase with preferred forms and source attribution",
    )
    parser.add_argument("--threshold", type=float, default=9.6, help="Semantic acceptance score out of 10")
    parser.add_argument("--language", default="fr-CA", help="LanguageTool code, default fr-CA")
    parser.add_argument("--passes", type=int, default=2, help="Number of correction passes to run")
    parser.add_argument(
        "--healthcheck",
        action="store_true",
        help="Run scripts/tex_healthcheck.py on the final output and store the result in the report",
    )
    parser.add_argument(
        "--healthcheck-script",
        default=str(Path(__file__).resolve().parents[3] / "scripts" / "tex_healthcheck.py"),
        help="Path to the LaTeX healthcheck script",
    )
    parser.add_argument(
        "--editorial-context",
        default=None,
        help="Optional text file with editorial or conversation context to store in the report",
    )
    parser.add_argument(
        "--style-profile",
        default=None,
        help="Optional style profile JSON to store in the report",
    )
    parser.add_argument(
        "--compile-pdf",
        action="store_true",
        help="Compile corrected TeX and place resulting PDF in theories/tex",
    )
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, do not write corrected file")
    args = parser.parse_args()

    process_file(
        input_path=Path(args.input),
        output_path=Path(args.output),
        report_path=Path(args.report),
        termbase_path=Path(args.termbase),
        semantic_threshold=args.threshold,
        language=args.language,
        dry_run=args.dry_run,
        passes=args.passes,
        healthcheck_script=Path(args.healthcheck_script) if args.healthcheck else None,
        editorial_context_path=Path(args.editorial_context) if args.editorial_context else None,
        style_profile_path=Path(args.style_profile) if args.style_profile else None,
        compile_after=args.compile_pdf,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
