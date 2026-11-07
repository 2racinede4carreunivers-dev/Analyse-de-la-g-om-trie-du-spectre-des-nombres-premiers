#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Healthcheck_HOL_correction.py - sante + correction sessions Isabelle/HOL.

Reproduit en Python, SANS lancer Isabelle, les controles de
`cygwin-terminal.bat` + `isabelle build -D DIR`, puis genere et applique
un patch de correction. Reutilisable pour tout projet de validation HOL.

Usage:
  python Healthcheck_HOL_correction.py --theories-dir <DIR> [--session NOM]
      [--fix] [--patch-out rapport.json] [--json] [--strict]

Phases: P0 terminal / P1 ROOT / P2 entetes / P3 structure / P4 encodage /
        P5 unicode / P6 memoire / P7 rapport+patch.

Sources (05-10-2026): `isabelle build -h` (Isabelle2025-2 via Cygwin),
Cygwin-Terminal.bat, doc System officielle (Sessions/Presentation),
verify_thy_structure.py du projet.

Auteur: Philippe Thomas Savard - Licence Apache 2.0. v1.0.0.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

VERSION = "1.0.0"
CYGWIN_TERMINAL_EXPECTED = {
    "home": r"set HOME=%HOMEDRIVE%%HOMEPATH%",
    "path": r"set PATH=%CD%\bin;%PATH%",
    "lang": "set LANG=en_US.UTF-8",
    "chere": "set CHERE_INVOKING=true",
    "bash": r"contrib\cygwin\bin\bash",
}
ML_ENV_VARS = ("ML_PLATFORM", "ML_HOME", "ML_SYSTEM", "ML_OPTIONS",
               "ISABELLE_TOOL_JAVA_OPTIONS", "ISABELLE_BUILD_OPTIONS")
ML_PLATFORM_MAXHEAP_MB = {"x86_64_32-windows": 16384, "x86_64_32-linux": 16384,
                          "x86_64-linux": 1 << 30, "x86_64-darwin": 1 << 30}

@dataclass
class EnvReport:
    cygwin_bat_ok: bool = False
    cygwin_bat_missing: list = field(default_factory=list)
    isabelle_found: bool = False
    isabelle_version: str = ""
    ml_env: dict = field(default_factory=dict)
    build_help_ok: bool = False
    notes: list = field(default_factory=list)


@dataclass
class Issue:
    severity: str
    passe: str
    file: str
    line: int
    message: str
    fixable: bool = False
    fix_applied: bool = False
    snippet: str = ""


@dataclass
class PatchOp:
    file: str
    line: int
    kind: str
    old: str = ""
    new: str = ""
    reason: str = ""


@dataclass
class HealthReport:
    session: str
    theories_dir: str
    issues: list = field(default_factory=list)
    patches: list = field(default_factory=list)
    fixes_applied: int = 0
    env: object = None

    @property
    def errors(self): return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self): return [i for i in self.issues if i.severity == "warning"]

    def to_dict(self) -> dict:
        return {"tool": "Healthcheck_HOL_correction v" + VERSION,
                "session": self.session, "theories_dir": self.theories_dir,
                "counts": {"errors": len(self.errors),
                           "warnings": len(self.warnings),
                           "patches": len(self.patches),
                           "fixes_applied": self.fixes_applied},
                "issues": [i.__dict__ for i in self.issues],
                "patches": [p.__dict__ for p in self.patches]}

def emulate_terminal(isabelle_home=None, cygwin_bat=None, probe=True):
    """Emule cygwin-terminal.bat + `isabelle build -h` + `isabelle getenv`.

    1. Controle le contenu du .bat (HOME/PATH/LANG/CHERE/bash).
    2. Localise `isabelle` (PATH ou <ISABELLE_HOME>/bin).
    3. Via bash Cygwin si present : version, aide build, ML_OPTIONS/PLATFORM.

    `probe=False` saute les appels subprocess (mode --offline) : l'analyse
    des .thy reste identique, seule l'rospection de l'outil est omise.
    Ne leve jamais : consigne tout dans EnvReport.
    """
    import os
    rep = EnvReport()
    if cygwin_bat and cygwin_bat.is_file():
        text = cygwin_bat.read_text(encoding="utf-8", errors="replace")
        for key, needle in CYGWIN_TERMINAL_EXPECTED.items():
            if needle not in text:
                rep.cygwin_bat_missing.append(key)
        rep.cygwin_bat_ok = not rep.cygwin_bat_missing
    else:
        rep.notes.append("Cygwin-Terminal.bat introuvable : lanceur non verifie.")
    isabelle = shutil.which("isabelle")
    if not isabelle and isabelle_home:
        cand = isabelle_home / "bin" / "isabelle"
        if cand.is_file():
            isabelle = str(cand)
    rep.isabelle_found = bool(isabelle)
    if not isabelle:
        rep.notes.append("isabelle absent du PATH : analyse statique seule.")
        return rep
    if not probe:
        rep.notes.append("Mode --offline : version/ML_PLATFORM non interroges.")
        return rep
    bash = None
    if isabelle_home:
        cand = isabelle_home / "contrib" / "cygwin" / "bin" / "bash.exe"
        if cand.is_file():
            bash = str(cand)
    bash = bash or shutil.which("bash")
    if not bash:
        for key, cmd in (("version", [isabelle, "version"]),
                         ("help", [isabelle, "build", "-h"])):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                out = (r.stdout or "") + (r.stderr or "")
                if key == "version" and r.returncode == 0 and out.strip():
                    rep.isabelle_version = out.strip().splitlines()[0]
                if key == "help" and "Usage: isabelle build" in out:
                    rep.build_help_ok = True
            except Exception as exc:
                rep.notes.append(f"{key} : {type(exc).__name__}: {exc}")
        return rep
    env = dict(os.environ)
    if isabelle_home:
        env["PATH"] = str(isabelle_home / "bin") + ";" + env.get("PATH", "")
    env.setdefault("LANG", "en_US.UTF-8")
    env["CHERE_INVOKING"] = "true"
    for key, script in (
            ("version", "isabelle version"),
            ("help", "isabelle build -h"),
            ("getenv", "isabelle getenv ML_OPTIONS ML_PLATFORM ML_SYSTEM ISABELLE_HEAPS")):
        try:
            r = subprocess.run([bash, "--login", "-c", script],
                               capture_output=True, text=True, timeout=180, env=env)
            out = (r.stdout or "") + (r.stderr or "")
            if key == "version" and r.returncode == 0:
                for line in out.splitlines():
                    if re.match(r"Isabelle\d", line.strip()):
                        rep.isabelle_version = line.strip()
                        break
            elif key == "help" and "Usage: isabelle build" in out:
                rep.build_help_ok = True
            elif key == "getenv":
                for line in out.splitlines():
                    m = re.match(r"(\w+)=(.*)", line.strip())
                    if m and (m.group(1) in ML_ENV_VARS or m.group(1) == "ISABELLE_HEAPS"):
                        rep.ml_env[m.group(1)] = m.group(2)
        except Exception as exc:
            rep.notes.append(f"{key} : {type(exc).__name__}: {exc}")
    return rep

SESSION_RE = re.compile(r"^\s*session\s+(\S+)\s*=\s*(.*?)\s*\+\s*$")
THEORY_ENTRY_RE = re.compile(r"^\s*([\w\-.]+)\s*(?:\(.*\))?\s*$")
THEORY_HEAD_RE = re.compile(r"^\s*theory\s+(\S+)\s*$")
IMPORTS_RE = re.compile(r"^\s*imports\b(.*)$")
BEGIN_RE = re.compile(r"^\s*begin\s*$")
END_RE = re.compile(r"^\s*end\s*$")
# Modele de blocs Isar, conforme a la grammaire reelle :
#   - `theory X` N'ouvre PAS de bloc : c'est le `begin` suivant qui l'ouvre,
#     et le `end` final qui le ferme. (theory + begin + ... + end = 1 bloc)
#   - `locale/context/notepad ... begin ... end` : 1 bloc via son `begin`.
#     Variante one-liner `context foo begin` : le `begin` est sur la meme ligne.
#   - `proof ... qed` : 1 bloc ouvert par `proof`, ferme par `qed`.
# Compter `theory` contre `end` a plat donne un faux positif systematique.
BLOCK_OPEN_RE = re.compile(r"^\s*(locale|context|notepad)\b")
PROOF_OPEN_RE = re.compile(r"^\s*proof\b")


def parse_root(root_path, report):
    """Parse ROOT (outer syntax Isar). Retourne (session, parents, theories)."""
    text = root_path.read_text(encoding="utf-8")
    session, parents, theories = "", [], []
    in_theories, in_sessions = False, False
    for no, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("(*"):
            continue
        m = SESSION_RE.match(line)
        if m:
            session = m.group(1).strip('"')
            parent = m.group(2).strip().strip('"')
            if parent and parent.upper() != "HOL":
                report.issues.append(Issue("warning", "p1-session", str(root_path), no,
                    "Parent inattendu : '%s' (attendu HOL)." % parent))
            in_theories = in_sessions = False
            continue
        if s.startswith("sessions"):
            in_sessions, in_theories = True, False
            continue
        if s.startswith("theories"):
            in_theories, in_sessions = True, False
            continue
        if s.startswith(("options", "document", "directories", "chapter")):
            in_theories = in_sessions = False
            continue
        if in_sessions:
            m2 = re.match(r'^\s*"([^"]+)"\s*$', line)
            if m2:
                parents.append(m2.group(1))
            continue
        if in_theories:
            m3 = THEORY_ENTRY_RE.match(line)
            if m3 and m3.group(1) != "options":
                theories.append(m3.group(1))
    if not session:
        report.issues.append(Issue("error", "p1-session", str(root_path), 0,
            "Pas de 'session NOM = HOL +' dans ROOT.", False))
    if not theories:
        report.issues.append(Issue("error", "p1-session", str(root_path), 0,
            "Bloc 'theories' vide/absent.", False))
    seen, dupes = set(), set()
    for t in theories:
        if t in seen:
            dupes.add(t)
        seen.add(t)
    for d in sorted(dupes):
        report.issues.append(Issue("error", "p1-session", str(root_path), 0,
            "Theorie 2x dans ROOT : %s (Duplicate theory)." % d, False))
    report.session = session
    return session, parents, theories


def check_theory_files(theories_dir, theories, report):
    """Chaque entree ROOT -> fichier homonyme (decouverte -D)."""
    mapping = {}
    for t in theories:
        cand = theories_dir / (t + ".thy")
        if not cand.is_file():
            report.issues.append(Issue("error", "p1-session", str(theories_dir / "ROOT"), 0,
                "Missing theory file : %s.thy declare mais absent." % t, False))
        else:
            mapping[t] = cand
    declared = set(theories)
    for f in sorted(theories_dir.glob("*.thy")):
        if f.stem not in declared:
            report.issues.append(Issue("warning", "p1-session", str(f), 0,
                "Fichier %s non declare dans ROOT : ignore par build -D." % f.name, False))
    return mapping

def _read_text(path):
    """Lecture tolérante : retire le BOM UTF-8 avant analyse.

    Le BOM est signale par ailleurs (P4) mais il rendrait illisibles
    `theory NOM`, `imports`, `begin`... et masquerait les vraies erreurs.
    """
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return raw.decode("utf-8", errors="strict")


def check_theory_header(path, theories, report):
    """theory X / imports / begin / end. Emule le chargeur de theories.

    NOTE: les blocs `locale NOM = ... begin ... end` ont leur propre
    paire begin/end imbriquee : on ne compte pour la theorie que le
    `begin` suivant les imports et le `end` final du fichier.
    """
    lines = _read_text(path).splitlines()
    heads = [(i + 1, m.group(1)) for i, l in enumerate(lines)
             if (m := THEORY_HEAD_RE.match(l))]
    if not heads:
        report.issues.append(Issue("error", "p2-header", str(path), 0,
            "Pas de 'theory NOM' : Outer syntax error au build.", False))
        return []
    if len(heads) > 1:
        report.issues.append(Issue("error", "p2-header", str(path), heads[1][0],
            "2x 'theory' : 1 fichier = 1 theorie.", False))
    name = heads[0][1]
    if name != path.stem:
        report.issues.append(Issue("error", "p2-header", str(path), heads[0][0],
            "Bad theory name : %s declare 'theory %s' (fixable)."
            % (path.name, name), True, snippet="theory " + name))
        report.patches.append(PatchOp(str(path), heads[0][0], "replace",
                                      "theory " + name, "theory " + path.stem,
                                      "Nom aligne sur le fichier."))
    imports = []
    for i, l in enumerate(lines):
        m = IMPORTS_RE.match(l)
        if m:
            j, buf = i, m.group(1)
            while j + 1 < len(lines) and buf.count('"') % 2 == 1:
                j += 1
                buf += " " + lines[j]
            for a, b in re.findall(r'"([^"]+)"|(\S+)', buf):
                if a or b:
                    imports.append(a or b)
            break
    declared = set(theories)
    for imp in imports:
        base = imp.split(".")[-1]
        if imp in ("HOL", "Complex_Main", "Pure", "Main") or imp.startswith("HOL-") \
                or base in declared or imp in declared:
            continue
        report.issues.append(Issue("warning", "p2-header", str(path), heads[0][0],
            "Import non resolu localement : '%s'." % imp, False, snippet=imp))
    # `begin` ouvre la theorie PUIS chaque locale/context imbrique :
    # on ne peut donc pas exiger exactement 1 occurrence. On verifie
    # seulement qu'un `begin` existe et que la pile de blocs est fermee.
    if not any(BEGIN_RE.match(l) for l in lines):
        report.issues.append(Issue("error", "p2-header", str(path), 0,
            "'begin' absent apres les imports.", False))
    if not any(END_RE.match(l) for l in lines):
        report.issues.append(Issue("error", "p2-header", str(path), len(lines),
            "'end' final absent.", False))
    return imports


def check_import_graph(mapping, all_imports, theories, report):
    """Cycles + imports vers theories posterieures (ordre fragile)."""
    order = {t: i for i, t in enumerate(theories)}
    graph = {t: [imp.split(".")[-1] for imp in imps if imp.split(".")[-1] in order]
             for t, imps in all_imports.items()}
    color = {}

    def visit(u, stack):
        color[u] = 1
        for v in graph.get(u, []):
            if color.get(v) == 1:
                report.issues.append(Issue("error", "p2-header", str(mapping[u]), 0,
                    "Cycle : %s." % " -> ".join(stack + [u, v]), False))
            elif not color.get(v):
                visit(v, stack + [u])
        color[u] = 2

    for t in graph:
        if not color.get(t):
            visit(t, [])
    for t, imps in graph.items():
        for v in imps:
            if order.get(v, -1) > order.get(t, 0):
                report.issues.append(Issue("info", "p2-header", str(mapping[t]), 0,
                    "%s importe %s declare APRES lui : ordre fragile." % (t, v), False))

def _mask_code(text):
    masked = text
    for pat in (r"text\s*\\<open>.*?\\<close>", r"section\s*\\<open>.*?\\<close>",
                r"subsection\s*\\<open>.*?\\<close>",
                r'text\s*"(?:[^"\\]|\\.)*"', r'section\s*"(?:[^"\\]|\\.)*"',
                r'subsection\s*"(?:[^"\\]|\\.)*"', r"\(\*.*?\*\)"):
        masked = re.sub(pat, lambda m: "".join(c if c == "\n" else " " for c in m.group(0)),
                        masked, flags=re.DOTALL)
    return masked


def check_block_nesting(path):
    """Analyse a PILE des blocs Isar imbriques (le vrai juge de syntaxe).

    Retourne la liste des anomalies. Un `locale X = ... begin ... end`
    consomme 2 `end` au total : celui du bloc et celui de la theorie.
    Compter `theory` contre `end` a plat produit un faux positif.
    """
    text = _read_text(path)
    lines = _mask_code(text).splitlines()
    stack = []            # (ligne, type_de_bloc)
    errors = []
    for no, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        if BEGIN_RE.match(line):
            stack.append((no, "begin"))
            continue
        if END_RE.match(line):
            if not stack:
                errors.append((no, "`end' orphelin : aucun bloc ouvert."))
            else:
                stack.pop()
            continue
        if s.startswith("qed"):
            if stack and stack[-1][1] == "proof":
                stack.pop()
            elif not stack:
                errors.append((no, "`qed' orphelin : aucun `proof' ouvert."))
            continue
        # `proof` ouvre une portee closee par `qed`.
        if PROOF_OPEN_RE.match(line):
            stack.append((no, "proof"))
            continue
        # `locale`/`context`/`notepad` : n'ouvrent un bloc QUE si `begin`
        # est sur la meme ligne (variante one-liner). Sinon c'est le `begin`
        # pose plus bas qui ouvrira, et BEGIN_RE le comptera.
        # NOTE : un `locale ... assumes ...` SANS `begin ... end` est legal
        # en Isar (corps vide) -- ex. MS_01_Fondements.thy:263.
        mo = BLOCK_OPEN_RE.match(line)
        if mo and s.endswith("begin"):
            stack.append((no, mo.group(1)))
    for no, kind in stack:
        errors.append((no, "Bloc `%s' ouvert a la ligne %d jamais ferme "
                           "(`end'/`qed' manquant) -> Erreur de syntaxe au build."
                           % (kind, no)))
    return errors


def check_balance(path, report):
    """proof/qed, blocs imbriques, cartouches, accolades : desequilibre = echec build."""
    text = _read_text(path)
    masked = _mask_code(text)
    for no, msg in check_block_nesting(path):
        report.issues.append(Issue("error", "p3-structure", str(path), no, msg, False))
    o, c = len(re.findall(r"^\s*proof\b", masked, re.M)), \
           len(re.findall(r"^\s*qed\b", masked, re.M))
    if o != c:
        report.issues.append(Issue("error", "p3-structure", str(path), 0,
            "Desequilibre proof/qed : %d vs %d." % (o, c), False))
    oo, cc = text.count("\\<open>"), text.count("\\<close>")
    if oo != cc:
        report.issues.append(Issue("error", "p3-structure", str(path), 0,
            "Cartouches : %d \\<open> vs %d \\<close>." % (oo, cc), False))
    if masked.count("{") != masked.count("}"):
        report.issues.append(Issue("warning", "p3-structure", str(path), 0,
            "Accolades desequilibrees.", False))


def check_encoding(path, report, fix):
    """UTF-8 strict, BOM, EOL : emule le chargeur de fichiers."""
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        report.issues.append(Issue("error", "p4-encoding", str(path), 1,
            "BOM UTF-8 : refuse par le chargeur (fixable).", True))
        report.patches.append(PatchOp(str(path), 1, "note", "BOM", "", "Supprimer EF BB BF."))
        if fix:
            path.write_bytes(raw[3:])
            report.fixes_applied += 1
            raw = raw[3:]
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        report.issues.append(Issue("error", "p4-encoding", str(path), 0,
            "Non UTF-8 : %s." % exc, False))
        return
    tmp = raw.replace(b"\r\n", b"")
    n_cr, n_lf, n_crlf = tmp.count(b"\r"), tmp.count(b"\n"), raw.count(b"\r\n")
    if n_cr:
        report.issues.append(Issue("error", "p4-encoding", str(path), 0,
            "%d CR isoles (fixable)." % n_cr, True))
        if fix:
            path.write_bytes(raw.replace(b"\r", b""))
            report.fixes_applied += 1
    elif n_crlf and n_lf:
        report.issues.append(Issue("warning", "p4-encoding", str(path), 0,
            "EOL melanges : %d CRLF + %d LF." % (n_crlf, n_lf), False))

UNICODE_TO_ISABELLE = {
    "\u21d2": r"\<Rightarrow>", "\u27f9": r"\<Longrightarrow>",
    "\u2264": r"\<le>", "\u2265": r"\<ge>", "\u2260": r"\<noteq>",
    "\u2200": r"\<forall>", "\u2203": r"\<exists>",
    "\u2227": r"\<and>", "\u2228": r"\<or>", "\u00ac": r"\<not>",
    "\u2208": r"\<in>", "\u03c0": r"\<pi>", "\u03c1": r"\<rho>",
    "\u03c8": r"\<psi>", "\u03b1": r"\<alpha>", "\u03b2": r"\<beta>",
    "\u221e": r"\<infinity>", "\u03bb": r"\<lambda>",
}
HEAVY_PATTERNS = [
    (r"\bby\s+eval\b", "by eval (certificat vivant jusqu'a fin de session)", 1.0),
    (r"pocklington_primefact", "Pocklington (Go de tas)", 8.0),
    (r"mod_exp\s+\d+\s+\d+\s+\d+", "mod_exp grands entiers", 3.0),
    (r"prime\s*\(\s*\d{7,}", "primalite >= 10^7", 4.0),
    (r"^\s*sorry\s*$", "sorry actif", 0.0),
    (r"^\s*oops\s*$", "oops actif", 0.0),
]
UNIT_GO = 0.5


def check_unicode_mem(path, report, fix, cap_mb):
    """P5 unicode (+delegue a verify_thy_structure si present) et P6 memoire."""
    try:
        sys.path.insert(0, str(path.parent))
        import verify_thy_structure as verifier
        rep = verifier.verify_file(path, fix=fix)
        for e in rep.errors:
            # verify_thy_structure compare `theory` a `end` a plat : faux
            # positif systematique quand la theorie contient un locale
            # imbrique (2 `end` pour 1 `theory`). check_block_nesting
            # (analyse a pile) fait foi a la place.
            if "theory/end" in e.message:
                continue
            report.issues.append(Issue("error", "p5-unicode", str(path), e.line,
                                       e.message, e.fixable, e.fix_applied, e.snippet))
        for w in rep.warnings:
            if "theory/end" in w.message:
                continue
            report.issues.append(Issue("warning", "p5-unicode", str(path), w.line,
                                       w.message, w.fixable, w.fix_applied, w.snippet))
        report.fixes_applied += rep.fixes_applied
    except Exception:
        text = _read_text(path)
        if fix:
            out = text
            for bad, good in UNICODE_TO_ISABELLE.items():
                out = out.replace(bad, good)
            if out != text:
                path.write_text(out, encoding="utf-8")
        else:
            for no, line in enumerate(text.splitlines(), 1):
                for ch in set(line) & set(UNICODE_TO_ISABELLE):
                    report.issues.append(Issue("warning", "p5-unicode", str(path), no,
                        "Unicode '%s' (fixable : %s)." % (ch, UNICODE_TO_ISABELLE[ch]),
                        True, snippet=line.strip()[:100]))
    text = _read_text(path)
    cost = 0.0
    for pat, label, weight in HEAVY_PATTERNS:
        hits = re.findall(pat, text, re.MULTILINE)
        if hits:
            cost += weight * len(hits)
            sev = "warning" if weight < 4 else "error"
            extra = " Extraire en session annexe ou axiomatiser." if weight >= 4 else ""
            report.issues.append(Issue(sev, "p6-memoire", str(path), 0,
                "%dx %s.%s" % (len(hits), label, extra), False))
    if re.search(r"\d{10,}", text):
        report.issues.append(Issue("info", "p6-memoire", str(path), 0,
            "Litteraux >= 10 chiffres : arithmetique ML lourde.", False))
    return cost

def analyse(theories_dir, session_filter, isabelle_home, cygwin_bat, fix,
            probe=True):
    """Pipeline P0..P6 : environnement -> ROOT -> entetes -> structure -> patch."""
    report = HealthReport(session_filter or "", str(theories_dir))
    report.env = emulate_terminal(isabelle_home, cygwin_bat, probe)
    env = report.env
    if not env.isabelle_found:
        report.issues.append(Issue("warning", "p0-env", "", 0,
            "isabelle introuvable : analyse statique seule.", False))
    else:
        report.issues.append(Issue("info", "p0-env", "", 0,
            "Terminal emule : %s, ML_OPTIONS=%s."
            % (env.isabelle_version or "isabelle trouve",
               env.ml_env.get("ML_OPTIONS", "?")), False))
    if env.cygwin_bat_ok:
        report.issues.append(Issue("info", "p0-env", "", 0,
            "Cygwin-Terminal.bat conforme.", False))
    for missing in env.cygwin_bat_missing:
        report.issues.append(Issue("warning", "p0-env", "", 0,
            "Lanceur : champ manquant '%s'." % missing, False))
    root_path = theories_dir / "ROOT"
    if not root_path.is_file():
        report.issues.append(Issue("error", "p1-session", str(root_path), 0,
            "ROOT absent : build -D ne voit aucune session.", False))
        return report
    session, parents, theories = parse_root(root_path, report)
    if session_filter and session != session_filter:
        report.issues.append(Issue("warning", "p1-session", str(root_path), 0,
            "ROOT='%s', filtre='%s'." % (session, session_filter), False))
    mapping = check_theory_files(theories_dir, theories, report)
    maxheap_mb = 16384
    m = re.search(r"--maxheap\s+(\d+)", env.ml_env.get("ML_OPTIONS", "") or "")
    if m:
        maxheap_mb = int(m.group(1))
        if maxheap_mb <= 4000:
            report.issues.append(Issue("error", "p6-memoire", "", 0,
                "--maxheap %d Mo = plafond %.1f Go < besoin ~16 Go."
                % (maxheap_mb, maxheap_mb / 1024), False))
    plat = (env.ml_env.get("ML_PLATFORM", "") or "").strip() or "x86_64_32-windows"
    cap_mb = min(maxheap_mb, ML_PLATFORM_MAXHEAP_MB.get(plat, 16384))
    all_imports, total_cost = {}, 0.0
    for t in theories:
        p = mapping.get(t)
        if not p:
            continue
        try:
            all_imports[t] = check_theory_header(p, theories, report)
            check_balance(p, report)
            check_encoding(p, report, fix)
            total_cost += check_unicode_mem(p, report, fix, cap_mb)
        except UnicodeDecodeError as exc:
            report.issues.append(Issue("error", "p4-encoding", str(p), 0,
                "Decode UTF-8 : %s." % exc, False))
    check_import_graph(mapping, all_imports, theories, report)
    est_go = total_cost * UNIT_GO
    if est_go > cap_mb / 1024 * 0.8:
        report.issues.append(Issue("error", "p6-memoire", "", 0,
            "Cout ~%.1f Go vs plafond %d Go (%s). Extraire certificats, -j1."
            % (est_go, cap_mb / 1024, plat), False))
    else:
        report.issues.append(Issue("info", "p6-memoire", "", 0,
            "Cout ~%.1f Go sous plafond %d Go (%s)." % (est_go, cap_mb / 1024, plat),
            False))
    return report

def apply_patches(report):
    n = 0
    for p in report.patches:
        fp = Path(p.file)
        if p.kind != "replace" or not fp.is_file():
            continue
        lines = fp.read_text(encoding="utf-8").splitlines()
        if 1 <= p.line <= len(lines) and p.old in lines[p.line - 1]:
            lines[p.line - 1] = lines[p.line - 1].replace(p.old, p.new)
            fp.write_text("\n".join(lines) + "\n", encoding="utf-8")
            n += 1
            for i in report.issues:
                if i.file == p.file and i.line == p.line and i.fixable and not i.fix_applied:
                    i.fix_applied = True
                    break
    report.fixes_applied += n
    return n


def render(report, verbose=True):
    tag = {"error": "[X]", "warning": "[!]", "info": "[i]"}
    for i in report.issues:
        if not verbose and i.severity == "info":
            continue
        loc = ("%s:L%d" % (Path(i.file).name, i.line)) if i.file else "ENV"
        fixed = " [FIXED]" if i.fix_applied else ""
        print("%s [%s] %s : %s%s" % (tag[i.severity], i.passe, loc, i.message, fixed))
        if verbose and i.snippet:
            print("       > %s" % i.snippet[:120])
    print("\nBilan '%s' : %d erreur(s), %d warning(s), %d patch(s), %d correction(s)."
          % (report.session or "?", len(report.errors), len(report.warnings),
             len(report.patches), report.fixes_applied))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="Healthcheck_HOL_correction")
    ap.add_argument("--theories-dir", type=Path, required=True)
    ap.add_argument("--session", default=None)
    ap.add_argument("--isabelle-home", type=Path, default=None)
    ap.add_argument("--cygwin-bat", type=Path, default=None)
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--patch-out", type=Path, default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", "-q", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--offline", action="store_true",
                    help="ne pas interroger Isabelle/Cygwin (analyse .thy seule, rapide)")
    args = ap.parse_args(argv)
    isabelle_home = args.isabelle_home
    if not isabelle_home:
        for cand in (Path(r"C:\Users\isabelle\Isabelle2025-2"), Path(r"C:\Isabelle2025-2")):
            if (cand / "bin" / "isabelle").is_file():
                isabelle_home = cand
                break
    cygwin_bat = args.cygwin_bat
    if not cygwin_bat and isabelle_home:
        cand = isabelle_home / "Cygwin-Terminal.bat"
        if cand.is_file():
            cygwin_bat = cand
    if not args.theories_dir.is_dir():
        print("[X] theories-dir introuvable : %s" % args.theories_dir)
        return 2
    report = analyse(args.theories_dir, args.session, isabelle_home, cygwin_bat,
                       args.fix, probe=not args.offline)
    if args.fix:
        apply_patches(report)
    if args.patch_out:
        args.patch_out.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False),
                                  encoding="utf-8")
        print("Rapport+patch : %s" % args.patch_out)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    elif not args.quiet:
        render(report)
    else:
        print("erreurs=%d warnings=%d patch=%d fixes=%d"
              % (len(report.errors), len(report.warnings),
                 len(report.patches), report.fixes_applied))
    return 1 if (report.errors or (args.strict and report.warnings)) else 0


if __name__ == "__main__":
    raise SystemExit(main())

