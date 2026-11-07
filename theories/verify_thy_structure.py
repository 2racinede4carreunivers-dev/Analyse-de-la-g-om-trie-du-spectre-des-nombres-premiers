#!/usr/bin/env python3
r"""
verify_thy_structure.py - Auto-correcteur statique pour fichiers Isabelle/HOL

Objectif : attraper les erreurs Isabelle typiques SANS avoir a lancer un vrai
build (installation d'Isabelle bloquee par le firewall du pod Emergent).

Passes de verification :
  1. STRUCTURE     : balance proof/qed, case/next, theory/end, cartouches \<open>/\<close>
  2. UNICODE       : symboles Unicode hors zones text/comment/string -> conversion ASCII
                     (ex: `\u21d2` -> `\<Rightarrow>`, `\u2264` -> `\<le>`, etc.)
  3. MOJIBAKE      : UTF-8 double-encode (`\u00c3\u00a9` -> `\u00e9`) dans zones texte
  4. TACTIQUES     : detection de patterns risques (`divide_inverse` isole,
                     `field_simps` sans temoin de non-nullite, `sorry` actif, `oops`)
  5. WHITESPACE    : trailing whitespace, tabs, lignes vides finales excessives

Usage :
  python theories/verify_thy_structure.py                  # check-only (defaut)
  python theories/verify_thy_structure.py --fix            # auto-correction en place
  python theories/verify_thy_structure.py --file X.thy     # cible specifique
  python theories/verify_thy_structure.py --strict         # exit 1 sur risky tactics
  python theories/verify_thy_structure.py --json           # sortie JSON pour CI

Integration pre-commit :
  # .git/hooks/pre-commit
  #!/bin/sh
  python theories/verify_thy_structure.py --strict || exit 1

Exit codes :
   0 = pas d'erreur bloquante
   1 = erreurs structurelles ou tactiques risquees (mode --strict)
   2 = fichier introuvable / erreur I/O
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    _HAS_RICH = True
except ImportError:
    _HAS_RICH = False

# =====================================================================
# CONFIGURATION
# =====================================================================

# Table de conversion Unicode -> Isabelle ASCII notation.
# Reference : ~/Isabelle/etc/symbols
UNICODE_TO_ISABELLE: dict[str, str] = {
    # Fleches logiques
    "\u21d2": r"\<Rightarrow>",       # =>
    "\u27f9": r"\<Longrightarrow>",   # =>
    "\u21d0": r"\<Leftarrow>",        # <=
    "\u27f8": r"\<Longleftarrow>",    # <==
    "\u21d4": r"\<Leftrightarrow>",   # <=>
    "\u27fa": r"\<Longleftrightarrow>",
    "\u2192": r"\<rightarrow>",       # ->
    "\u27f6": r"\<longrightarrow>",   # -->
    "\u2190": r"\<leftarrow>",        # <-
    "\u27f5": r"\<longleftarrow>",    # <--
    "\u2194": r"\<leftrightarrow>",   # <->
    "\u21a6": r"\<mapsto>",           # |->
    # Comparaisons
    "\u2264": r"\<le>",               # <=
    "\u2265": r"\<ge>",               # >=
    "\u2260": r"\<noteq>",            # !=
    "\u2261": r"\<equiv>",            # ==
    "\u2248": r"\<approx>",           # ~=
    # Ensembles / logique
    "\u2200": r"\<forall>",           # for all
    "\u2203": r"\<exists>",           # exists
    "\u2204": r"\<nexists>",          # not exists
    "\u2227": r"\<and>",              # AND
    "\u2228": r"\<or>",               # OR
    "\u00ac": r"\<not>",              # NOT
    "\u22a5": r"\<bottom>",           # false
    "\u22a4": r"\<top>",              # true
    "\u2208": r"\<in>",               # in
    "\u2209": r"\<notin>",            # notin
    "\u222a": r"\<union>",            # union
    "\u2229": r"\<inter>",            # intersection
    "\u2286": r"\<subseteq>",         # subset eq
    "\u2282": r"\<subset>",           # subset
    "\u2287": r"\<supseteq>",         # superset eq
    "\u2205": r"\<emptyset>",         # empty
    # Quantificateurs Isar
    "\u22c0": r"\<And>",              # big AND
    "\u22c1": r"\<Or>",               # big OR
    "\u22c3": r"\<Union>",            # big union
    "\u22c2": r"\<Inter>",            # big inter
    "\u2211": r"\<Sum>",              # sum
    "\u220f": r"\<Prod>",             # prod
    # Ensembles numeriques
    "\u2115": r"\<nat>",              # N
    "\u2124": r"\<int>",              # Z
    "\u211a": r"\<rat>",              # Q
    "\u211d": r"\<real>",             # R
    "\u2102": r"\<complex>",          # C
    "\u2119": r"\<P>",                # P (premiers, notation Savard)
    # Autres
    "\u00b7": r"\<cdot>",             # middle dot
    "\u2218": r"\<circ>",             # composition
    "\u2223": r"\<bar>",              # divides / bar
    "\u221e": r"\<infinity>",         # infinity
    "\u03bb": r"\<lambda>",           # lambda
    "\u03b1": r"\<alpha>",
    "\u03b2": r"\<beta>",
    "\u03b3": r"\<gamma>",
    "\u03b4": r"\<delta>",
    "\u03b5": r"\<epsilon>",
    "\u03b6": r"\<zeta>",
    "\u03b8": r"\<theta>",
    "\u03c0": r"\<pi>",
    "\u03c1": r"\<rho>",
    "\u03c3": r"\<sigma>",
    "\u03c6": r"\<phi>",
    "\u03c8": r"\<psi>",
    "\u03c9": r"\<omega>",
    "\u0393": r"\<Gamma>",
    "\u0394": r"\<Delta>",
    "\u03a3": r"\<Sigma>",
    "\u03a6": r"\<Phi>",
    "\u03a9": r"\<Omega>",
}

# Table de restauration mojibake UTF-8 (double encoding latin1 -> utf8)
MOJIBAKE_MAP: dict[str, str] = {
    "\u00c3\u00a9": "\u00e9",  # -> e-acute
    "\u00c3\u00a8": "\u00e8",  # -> e-grave
    "\u00c3\u00aa": "\u00ea",  # -> e-circ
    "\u00c3\u00ab": "\u00eb",  # -> e-diaer
    "\u00c3\u00a0": "\u00e0",  # -> a-grave
    "\u00c3\u00a2": "\u00e2",  # -> a-circ
    "\u00c3\u00a4": "\u00e4",  # -> a-diaer
    "\u00c3\u00ae": "\u00ee",  # -> i-circ
    "\u00c3\u00af": "\u00ef",  # -> i-diaer
    "\u00c3\u00b4": "\u00f4",  # -> o-circ
    "\u00c3\u00b6": "\u00f6",  # -> o-diaer
    "\u00c3\u00b9": "\u00f9",  # -> u-grave
    "\u00c3\u00bb": "\u00fb",  # -> u-circ
    "\u00c3\u00bc": "\u00fc",  # -> u-diaer
    "\u00c3\u00a7": "\u00e7",  # -> c-cedille
    "\u00c3\u0089": "\u00c9",  # -> E-acute
    "\u00c3\u0080": "\u00c0",  # -> A-grave
    "\u00c5\u0093": "\u0153",  # -> oe
    "\u00e2\u0080\u0099": "'",  # right single quote
    "\u00e2\u0080\u0098": "'",  # left single quote
    "\u00e2\u0080\u009c": '"',  # left double quote
    "\u00e2\u0080\u009d": '"',  # right double quote
}

# Tactiques Isabelle a signaler (patterns regex + explication)
RISKY_TACTICS: list[tuple[str, str, str]] = [
    (
        r"by\s*\(\s*simp\s+add:\s*divide_inverse\b",
        "divide_inverse dans simp",
        "Deplie toutes les divisions en `x * inverse y`. Risque de stack overflow. "
        "Prefer `divide_divide_eq_right` ou reformuler la preuve.",
    ),
    (
        r"^\s*sorry\s*$",
        "sorry actif",
        "Preuve incomplete. Doit etre remplacee avant push production.",
    ),
    (
        r"^\s*oops\s*$",
        "oops actif",
        "Abandon de preuve. Doit etre resolu avant push production.",
    ),
    (
        r"\bsledgehammer\b",
        "sledgehammer laisse",
        "Sledgehammer est un aide-recherche, pas une tactique de production. "
        "Remplacer par la tactique concrete suggeree.",
    ),
]

# Zones a IGNORER lors du scan Unicode (contenu autorise a etre en UTF-8)
# Ces regex identifient les zones de texte/commentaire.
# NOTE : les chaines "..." (inner syntax Isabelle) DE FORMULES NE SONT PAS ignorees :
# elles doivent utiliser la notation ASCII (\<Rightarrow>, \<le>, etc.)
# EXCEPTION : les chaines de texte associees a text/subsection/section/chapter/paragraph
# (ancien style Isabelle : `subsection "..."`) SONT ignorees.
IGNORE_ZONES_PATTERNS: list[str] = [
    # Cartouches modernes \<open>...\<close>
    r"text\s*\\<open>.*?\\<close>",
    r"\\<comment>\s*\\<open>.*?\\<close>",
    r"subsection\s*\\<open>.*?\\<close>",
    r"section\s*\\<open>.*?\\<close>",
    r"chapter\s*\\<open>.*?\\<close>",
    r"paragraph\s*\\<open>.*?\\<close>",
    # Style quote ancien (encore valide) : text "...", subsection "...", etc.
    r'text\s*"(?:[^"\\]|\\.)*"',
    r'subsection\s*"(?:[^"\\]|\\.)*"',
    r'section\s*"(?:[^"\\]|\\.)*"',
    r'chapter\s*"(?:[^"\\]|\\.)*"',
    r'paragraph\s*"(?:[^"\\]|\\.)*"',
    # Commentaires ML
    r"\(\*.*?\*\)",
]


# =====================================================================
# STRUCTURES DE DONNEES
# =====================================================================


@dataclass
class Issue:
    """Un probleme detecte dans le fichier .thy"""
    severity: str          # "error" | "warning" | "info"
    passe: str             # "structure" | "unicode" | "mojibake" | "tactique" | "whitespace"
    line: int              # 1-indexed, 0 pour issues globales
    message: str
    fixable: bool = False
    fix_applied: bool = False
    snippet: str = ""


@dataclass
class VerificationReport:
    """Rapport agrege pour un fichier .thy"""
    file_path: str
    total_lines: int
    issues: list[Issue] = field(default_factory=list)
    fixes_applied: int = 0
    passes_run: list[str] = field(default_factory=list)

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    @property
    def infos(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "info"]

    def to_dict(self) -> dict:
        return {
            "file_path": self.file_path,
            "total_lines": self.total_lines,
            "fixes_applied": self.fixes_applied,
            "passes_run": self.passes_run,
            "counts": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "infos": len(self.infos),
            },
            "issues": [
                {
                    "severity": i.severity,
                    "passe": i.passe,
                    "line": i.line,
                    "message": i.message,
                    "fixable": i.fixable,
                    "fix_applied": i.fix_applied,
                    "snippet": i.snippet,
                }
                for i in self.issues
            ],
        }


# =====================================================================
# UTILITAIRES : masquage des zones a ignorer
# =====================================================================


def _mask_ignored_zones(content: str) -> str:
    """
    Remplace les zones text/comment/string par des espaces de meme taille.
    Preserve les numeros de ligne pour le reporting.
    """
    masked = content
    for pattern in IGNORE_ZONES_PATTERNS:
        def _replace(match: re.Match[str]) -> str:
            s = match.group(0)
            # Preserve les newlines pour ne pas casser les numeros de ligne
            return "".join(c if c == "\n" else " " for c in s)
        masked = re.sub(pattern, _replace, masked, flags=re.DOTALL)
    return masked


def _line_of_offset(content: str, offset: int) -> int:
    """Retourne le numero de ligne (1-indexed) d'un offset dans le contenu."""
    return content.count("\n", 0, offset) + 1


# =====================================================================
# PASSE 1 : STRUCTURE
# =====================================================================


def check_structure(content: str, report: VerificationReport) -> None:
    """Verifie la balance des mots-cles structurels."""
    masked = _mask_ignored_zones(content)

    checks = [
        (r"\bproof\b", r"\bqed\b", "proof", "qed"),
        (r"\btheory\b", r"\bend\b", "theory", "end"),
    ]
    for open_pat, close_pat, open_name, close_name in checks:
        n_open = len(re.findall(open_pat, masked))
        n_close = len(re.findall(close_pat, masked))
        if n_open != n_close:
            report.issues.append(Issue(
                severity="error",
                passe="structure",
                line=0,
                message=(
                    f"Desequilibre {open_name}/{close_name} : "
                    f"{n_open} `{open_name}` vs {n_close} `{close_name}` "
                    f"(diff = {n_open - n_close})"
                ),
                fixable=False,
            ))

    # Balance des cartouches \<open>/\<close>
    n_open_cart = len(re.findall(r"\\<open>", content))
    n_close_cart = len(re.findall(r"\\<close>", content))
    if n_open_cart != n_close_cart:
        report.issues.append(Issue(
            severity="error",
            passe="structure",
            line=0,
            message=(
                f"Desequilibre cartouches : {n_open_cart} `\\<open>` vs "
                f"{n_close_cart} `\\<close>` (diff = {n_open_cart - n_close_cart})"
            ),
            fixable=False,
        ))

    # case sans next correspondant : `case True` doit etre suivi par `next` ou `qed`
    # (approximation : chaque `proof (cases ...)` a besoin de (n-1) `next` pour n cas)
    n_case = len(re.findall(r"\bcase\s+(?:True|False|Nil|Cons|\w+)", masked))
    n_next = len(re.findall(r"^\s*next\s*$", masked, re.MULTILINE))
    # Chaque proof (cases) devrait produire n_cases cases et (n_cases - 1) next
    # Donc n_case >= n_next + n_proof_cases (approximatif, on tolere)
    n_proof_cases = len(re.findall(r"proof\s*\(\s*cases\b", masked))
    expected_min_next = max(0, n_case - n_proof_cases)
    if n_next < expected_min_next - 2:  # tolerance de 2 pour patterns exotiques
        report.issues.append(Issue(
            severity="warning",
            passe="structure",
            line=0,
            message=(
                f"Possible desequilibre case/next : {n_case} `case`, {n_next} `next`, "
                f"{n_proof_cases} `proof (cases ...)`. Verifiez manuellement."
            ),
            fixable=False,
        ))

    report.passes_run.append("structure")


# =====================================================================
# PASSE 2 : UNICODE HORS ZONES AUTORISEES
# =====================================================================


def check_unicode(content: str, report: VerificationReport, fix: bool) -> str:
    """
    Scanne les caracteres Unicode HORS zones text/comment/string.
    En mode --fix, convertit vers la notation ASCII Isabelle.
    Retourne le contenu (potentiellement modifie).
    """
    masked = _mask_ignored_zones(content)
    result = list(content)
    fixes_in_pass = 0

    for i, ch in enumerate(masked):
        if ord(ch) <= 127 or ch == "\n":
            continue
        # Character in code zone (not text/comment)
        line_no = _line_of_offset(content, i)
        if ch in UNICODE_TO_ISABELLE:
            replacement = UNICODE_TO_ISABELLE[ch]
            if fix:
                result[i] = replacement
                fixes_in_pass += 1
                report.issues.append(Issue(
                    severity="warning",
                    passe="unicode",
                    line=line_no,
                    message=(
                        f"Unicode `{ch}` (U+{ord(ch):04X}) converti en `{replacement}`"
                    ),
                    fixable=True,
                    fix_applied=True,
                    snippet=content.splitlines()[line_no - 1][:80] if line_no - 1 < len(content.splitlines()) else "",
                ))
            else:
                report.issues.append(Issue(
                    severity="error",
                    passe="unicode",
                    line=line_no,
                    message=(
                        f"Unicode `{ch}` (U+{ord(ch):04X}) hors zone texte. "
                        f"Devrait etre `{replacement}` (utiliser --fix pour corriger)."
                    ),
                    fixable=True,
                    fix_applied=False,
                    snippet=content.splitlines()[line_no - 1][:80] if line_no - 1 < len(content.splitlines()) else "",
                ))
        else:
            # Unicode non repertorie : signal severe
            report.issues.append(Issue(
                severity="error",
                passe="unicode",
                line=line_no,
                message=(
                    f"Unicode `{ch}` (U+{ord(ch):04X}) hors zone texte, "
                    f"AUCUNE conversion Isabelle connue. Correction manuelle requise."
                ),
                fixable=False,
                snippet=content.splitlines()[line_no - 1][:80] if line_no - 1 < len(content.splitlines()) else "",
            ))

    report.passes_run.append("unicode")
    report.fixes_applied += fixes_in_pass
    return "".join(result)


# =====================================================================
# PASSE 3 : MOJIBAKE
# =====================================================================


def check_mojibake(content: str, report: VerificationReport, fix: bool) -> str:
    """Detecte et corrige les sequences UTF-8 double-encodees."""
    fixes_in_pass = 0
    new_content = content
    for bad, good in MOJIBAKE_MAP.items():
        if bad in new_content:
            n_occurrences = new_content.count(bad)
            # Recherche des lignes concernees
            for m in re.finditer(re.escape(bad), new_content):
                line_no = _line_of_offset(new_content, m.start())
                if fix:
                    fixes_in_pass += n_occurrences
                    report.issues.append(Issue(
                        severity="warning",
                        passe="mojibake",
                        line=line_no,
                        message=f"Mojibake `{bad}` -> `{good}` corrige",
                        fixable=True,
                        fix_applied=True,
                    ))
                    break  # Signale une fois par sequence
                else:
                    report.issues.append(Issue(
                        severity="error",
                        passe="mojibake",
                        line=line_no,
                        message=(
                            f"Mojibake detecte : `{bad}` "
                            f"(devrait etre `{good}`, {n_occurrences} occurrences). "
                            f"Utiliser --fix pour corriger."
                        ),
                        fixable=True,
                        fix_applied=False,
                    ))
                    break
            if fix:
                new_content = new_content.replace(bad, good)

    report.passes_run.append("mojibake")
    report.fixes_applied += fixes_in_pass
    return new_content


# =====================================================================
# PASSE 4 : TACTIQUES RISQUEES
# =====================================================================


def check_risky_tactics(content: str, report: VerificationReport) -> None:
    """Detecte les tactiques Isabelle connues pour causer des problemes."""
    lines = content.splitlines()
    for line_no, line in enumerate(lines, start=1):
        # Skip commentaires ML `(* ... *)` sur une ligne
        stripped = line.strip()
        if stripped.startswith("(*") and stripped.endswith("*)"):
            continue
        for pattern, name, hint in RISKY_TACTICS:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                report.issues.append(Issue(
                    severity="warning",
                    passe="tactique",
                    line=line_no,
                    message=f"Tactique risquee : {name}. {hint}",
                    fixable=False,
                    snippet=line.strip()[:100],
                ))
    # Detection specifique : field_simps sans temoin de non-nullite dans les 3 lignes precedentes
    for line_no, line in enumerate(lines, start=1):
        if re.search(r"by\s*\(\s*simp\s+add:\s*field_simps\s*\)", line):
            # Regarde 5 lignes avant pour un `\<noteq> 0` ou `\<noteq> 0` en assumption/have
            start_ctx = max(0, line_no - 6)
            ctx = "\n".join(lines[start_ctx:line_no - 1])
            has_nonzero_witness = bool(re.search(r"\\<noteq>\s*0|!=\s*0|<>\s*0", ctx))
            if not has_nonzero_witness:
                report.issues.append(Issue(
                    severity="warning",
                    passe="tactique",
                    line=line_no,
                    message=(
                        "`field_simps` sans temoin `\\<noteq> 0` dans les 5 lignes "
                        "precedentes. Risque de `Failed to finish proof` sur les fractions."
                    ),
                    fixable=False,
                    snippet=line.strip()[:100],
                ))

    report.passes_run.append("tactique")


# =====================================================================
# PASSE 5 : WHITESPACE
# =====================================================================


def check_whitespace(content: str, report: VerificationReport, fix: bool) -> str:
    """Nettoie whitespace : trailing spaces, tabs, lignes vides finales."""
    fixes_in_pass = 0
    lines = content.splitlines()

    for i, line in enumerate(lines):
        line_no = i + 1
        # Trailing whitespace
        if line.rstrip() != line:
            if fix:
                lines[i] = line.rstrip()
                fixes_in_pass += 1
                report.issues.append(Issue(
                    severity="info",
                    passe="whitespace",
                    line=line_no,
                    message="Trailing whitespace supprime",
                    fixable=True,
                    fix_applied=True,
                ))
            else:
                report.issues.append(Issue(
                    severity="info",
                    passe="whitespace",
                    line=line_no,
                    message="Trailing whitespace (utiliser --fix pour corriger)",
                    fixable=True,
                    fix_applied=False,
                ))
        # Tabs (Isabelle prefere spaces)
        if "\t" in line:
            if fix:
                lines[i] = lines[i].expandtabs(2)
                fixes_in_pass += 1
                report.issues.append(Issue(
                    severity="info",
                    passe="whitespace",
                    line=line_no,
                    message="Tab converti en 2 espaces",
                    fixable=True,
                    fix_applied=True,
                ))
            else:
                report.issues.append(Issue(
                    severity="info",
                    passe="whitespace",
                    line=line_no,
                    message="Tab detecte (utiliser --fix pour convertir en espaces)",
                    fixable=True,
                    fix_applied=False,
                ))

    # Lignes vides finales excessives (garde une seule ligne vide + newline final)
    while len(lines) >= 2 and lines[-1] == "" and lines[-2] == "":
        if fix:
            lines.pop()
            fixes_in_pass += 1
        else:
            report.issues.append(Issue(
                severity="info",
                passe="whitespace",
                line=len(lines),
                message="Ligne vide finale excessive (utiliser --fix)",
                fixable=True,
                fix_applied=False,
            ))
            break

    if fix and fixes_in_pass > 0:
        report.issues.append(Issue(
            severity="info",
            passe="whitespace",
            line=0,
            message=f"Total whitespace fixes appliques : {fixes_in_pass}",
            fixable=True,
            fix_applied=True,
        ))
        report.fixes_applied += fixes_in_pass

    report.passes_run.append("whitespace")
    return "\n".join(lines) + ("\n" if content.endswith("\n") else "")


# =====================================================================
# ORCHESTRATION
# =====================================================================


def verify_file(path: Path, fix: bool = False) -> VerificationReport:
    """Execute toutes les passes de verification sur un fichier .thy."""
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    content = path.read_text(encoding="utf-8")
    report = VerificationReport(
        file_path=str(path),
        total_lines=content.count("\n") + (0 if content.endswith("\n") else 1),
    )

    # Passe 1 : structure (read-only)
    check_structure(content, report)

    # Passe 2 : unicode (auto-fixable)
    content = check_unicode(content, report, fix)

    # Passe 3 : mojibake (auto-fixable)
    content = check_mojibake(content, report, fix)

    # Passe 4 : tactiques risquees (read-only, jamais auto-corrige)
    check_risky_tactics(content, report)

    # Passe 5 : whitespace (auto-fixable)
    content = check_whitespace(content, report, fix)

    # Ecriture des corrections
    if fix and report.fixes_applied > 0:
        path.write_text(content, encoding="utf-8")

    return report


# =====================================================================
# AFFICHAGE
# =====================================================================


def render_report_rich(report: VerificationReport, console: "Console") -> None:
    """Affiche un rapport Rich avec tableau et panneaux."""
    n_err = len(report.errors)
    n_warn = len(report.warnings)
    n_info = len(report.infos)

    if n_err == 0 and n_warn == 0:
        emoji = "OK"
        color = "green"
        title = "AUCUN PROBLEME DETECTE"
    elif n_err > 0:
        emoji = "X"
        color = "red"
        title = f"{n_err} ERREUR(S) BLOQUANTE(S)"
    else:
        emoji = "!"
        color = "yellow"
        title = f"{n_warn} AVERTISSEMENT(S) NON-BLOQUANT(S)"

    header = Text(f"[{emoji}] {title}", style=f"bold {color}")
    stats = Text(
        f"Fichier   : {report.file_path}\n"
        f"Lignes    : {report.total_lines}\n"
        f"Passes    : {', '.join(report.passes_run)}\n"
        f"Fixes     : {report.fixes_applied} correction(s) appliquee(s)\n"
        f"Bilan     : {n_err} erreur(s), {n_warn} warning(s), {n_info} info(s)"
    )

    console.print(Panel(
        Text.assemble(header, "\n\n", stats),
        title="GABRIEL // ISABELLE AUTOCORRECTEUR",
        border_style=color,
    ))

    if not report.issues:
        return

    # Grouper par passe
    by_pass: dict[str, list[Issue]] = {}
    for issue in report.issues:
        by_pass.setdefault(issue.passe, []).append(issue)

    for passe_name, issues in by_pass.items():
        table = Table(
            title=f"Passe : {passe_name.upper()}",
            show_lines=False,
            expand=True,
        )
        table.add_column("Sev", width=6)
        table.add_column("L", width=5, justify="right")
        table.add_column("Fix", width=4, justify="center")
        table.add_column("Message", overflow="fold")

        for issue in issues:
            sev_color = {
                "error": "red",
                "warning": "yellow",
                "info": "cyan",
            }.get(issue.severity, "white")
            fix_indicator = (
                "[green]OK[/]" if issue.fix_applied
                else "[dim]fix[/]" if issue.fixable
                else "-"
            )
            table.add_row(
                f"[{sev_color}]{issue.severity[:5]}[/]",
                str(issue.line) if issue.line > 0 else "-",
                fix_indicator,
                issue.message + (f"\n[dim]  {issue.snippet}[/]" if issue.snippet else ""),
            )
        console.print(table)


def render_report_plain(report: VerificationReport) -> None:
    """Affichage plain-text si Rich n'est pas dispo."""
    print(f"=== VERIFICATION : {report.file_path} ===")
    print(f"Lignes: {report.total_lines} | Passes: {', '.join(report.passes_run)} "
          f"| Fixes: {report.fixes_applied}")
    print(f"Bilan: {len(report.errors)} erreur(s), {len(report.warnings)} warning(s), "
          f"{len(report.infos)} info(s)")
    print()

    for issue in report.issues:
        marker = {"error": "[X]", "warning": "[!]", "info": "[i]"}[issue.severity]
        loc = f"L{issue.line}" if issue.line > 0 else "----"
        fixed = " [FIXED]" if issue.fix_applied else ""
        print(f"{marker} {loc} ({issue.passe}) {issue.message}{fixed}")
        if issue.snippet:
            print(f"       > {issue.snippet}")


# =====================================================================
# ENTRY POINT CLI
# =====================================================================


def _default_thy_files(root: Path) -> list[Path]:
    """Retourne tous les .thy sous `theories/`."""
    theories_dir = root / "theories"
    if not theories_dir.exists():
        return []
    return sorted(theories_dir.glob("*.thy"))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="verify_thy_structure",
        description="Autocorrecteur statique pour fichiers Isabelle/HOL",
    )
    parser.add_argument(
        "--file", "-f", type=Path, default=None,
        help="Chemin d'un .thy specifique (par defaut : tous les theories/*.thy)",
    )
    parser.add_argument(
        "--fix", action="store_true",
        help="Applique les corrections automatiques (Unicode, mojibake, whitespace)",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit 1 si tactiques risquees detectees (mode CI)",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Sortie JSON structuree (pour integration CI/tools)",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Silence l'output detaille (garde uniquement le summary)",
    )
    args = parser.parse_args(argv)

    # Determine files to check
    if args.file:
        files = [args.file]
    else:
        # Le script est dans theories/, donc root = parent
        script_dir = Path(__file__).resolve().parent
        root = script_dir.parent
        files = _default_thy_files(root)
        if not files:
            print(f"[X] Aucun fichier .thy trouve sous {root}/theories/")
            return 2

    exit_code = 0
    all_reports: list[VerificationReport] = []

    for f in files:
        try:
            report = verify_file(f, fix=args.fix)
        except FileNotFoundError as e:
            print(f"[X] {e}")
            exit_code = 2
            continue
        all_reports.append(report)

        # Determine exit code
        if report.errors:
            exit_code = max(exit_code, 1)
        if args.strict and report.warnings:
            exit_code = max(exit_code, 1)

    # Output
    if args.json:
        payload = {
            "success": exit_code == 0,
            "exit_code": exit_code,
            "reports": [r.to_dict() for r in all_reports],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return exit_code

    if _HAS_RICH:
        console = Console(force_terminal=not args.quiet)
        for report in all_reports:
            render_report_rich(report, console)
    else:
        for report in all_reports:
            render_report_plain(report)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
