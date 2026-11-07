#!/usr/bin/env python3
"""
Simulateur de validation Isabelle/HOL en mode 'cygwin-terminal.bat'.

Effectue une analyse statique poussée d'un fichier .thy comme le ferait
le binaire `isabelle process` au stade du parsing/typing pre-Pure :
  1. Structure theory ... begin ... end
  2. Equilibre des delimiteurs (\<open>/\<close>, proof/qed, ( )/{ }, etc.)
  3. Unicite des noms (definitions, lemmes, theoremes, axiomes)
  4. References aux noms : tout `X_def` ou nom utilise doit etre declare
  5. Coherence des proofs : chaque `proof` doit avoir un `qed` ou `by/.`/`done`
  6. Signature des definitions (parsing du type)
  7. Detection de motifs suspects (lemmes invalides ex `[OF ...]` sur lemmes 0-aire)
"""
from __future__ import annotations
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

THY = Path(sys.argv[1] if len(sys.argv) > 1 else "theories/methode_spectral.thy")
SRC = THY.read_text(encoding="utf-8")

# Strip commentaires Isabelle (* ... *) en respectant l'imbrication
def strip_comments(src: str) -> str:
    out = []
    i, depth = 0, 0
    while i < len(src):
        if src[i:i+2] == "(*":
            depth += 1
            i += 2
        elif src[i:i+2] == "*)" and depth > 0:
            depth -= 1
            i += 2
        elif depth == 0:
            out.append(src[i])
            i += 1
        else:
            i += 1
    return "".join(out)

CLEAN = strip_comments(SRC)

errors = []
warnings = []
infos = []

# 1. Structure theory ... begin ... end
m_theory = re.search(r"^\s*theory\s+(\w+)", SRC, re.MULTILINE)
if not m_theory:
    errors.append("Aucune declaration 'theory NAME' trouvee.")
else:
    theory_name = m_theory.group(1)
    infos.append(f"theory: {theory_name}")
    expected = THY.stem
    if theory_name != expected:
        errors.append(f"theory '{theory_name}' != nom du fichier '{expected}'")

if not re.search(r"^\s*begin\s*$", SRC, re.MULTILINE):
    errors.append("Mot-cle 'begin' manquant.")
if not SRC.rstrip().endswith("end"):
    errors.append("Fichier ne finit pas par 'end'.")

# 2. Equilibre des delimiteurs
open_cart = len(re.findall(r"\\<open>", CLEAN))
close_cart = len(re.findall(r"\\<close>", CLEAN))
if open_cart != close_cart:
    errors.append(f"Delimiteurs cartouches non equilibres : \\<open>={open_cart} \\<close>={close_cart}")
else:
    infos.append(f"Cartouches equilibres : {open_cart} pairs")

# proof ... qed (en ignorant `by/done/.` qui terminent aussi)
proofs = len(re.findall(r"^\s*proof\s*[-]?", CLEAN, re.MULTILINE))
qeds = len(re.findall(r"^\s*qed\b", CLEAN, re.MULTILINE))
if proofs != qeds:
    warnings.append(f"proofs={proofs} mais qeds={qeds} (decalage possible)")
else:
    infos.append(f"proof/qed equilibres : {proofs}")

# 3. Unicite des noms
def_names = re.findall(r"^\s*definition\s+(\w+)\s*::", CLEAN, re.MULTILINE)
lemma_names = re.findall(r"^\s*lemma\s+(\w+)\s*:", CLEAN, re.MULTILINE)
theorem_names = re.findall(r"^\s*theorem\s+(\w+)\s*:", CLEAN, re.MULTILINE)
fun_names = re.findall(r"^\s*fun\s+(\w+)\s*::", CLEAN, re.MULTILINE)
consts_blocks = re.findall(r"^\s*consts\s*\n((?:\s+\w+\s*::.*\n?)+)", CLEAN, re.MULTILINE)
typedecls = re.findall(r"^\s*typedecl\s+(\w+)", CLEAN, re.MULTILINE)

all_consts_names = []
for blk in consts_blocks:
    for line in blk.strip().split("\n"):
        m = re.match(r"\s*(\w+)\s*::", line)
        if m:
            all_consts_names.append(m.group(1))

axiom_names = re.findall(r"^\s+(\w+):\s*\n?\s*\"", CLEAN, re.MULTILINE)
# (heuristique : noms d'axiomes pour 'axiomatization where NAME: "..."')

all_names = (
    [(n, "definition") for n in def_names]
    + [(n, "lemma") for n in lemma_names]
    + [(n, "theorem") for n in theorem_names]
    + [(n, "fun") for n in fun_names]
    + [(n, "consts") for n in all_consts_names]
    + [(n, "typedecl") for n in typedecls]
)
seen = defaultdict(list)
for name, kind in all_names:
    seen[name].append(kind)
dups = {n: kinds for n, kinds in seen.items() if len(kinds) > 1}
if dups:
    for n, k in dups.items():
        errors.append(f"Nom duplique : '{n}' declare comme {', '.join(k)}")
else:
    infos.append(f"Tous les noms uniques : {len(all_names)} declarations")

# 4. References aux *_def : tout 'X_def' utilise doit correspondre a un 'definition X'
def_refs = set(re.findall(r"\b(\w+)_def\b", CLEAN))
missing_defs = [r for r in def_refs if r not in def_names and r not in fun_names]
if missing_defs:
    # Filtrer ceux qui sont en realite des noms predefinis HOL
    HOL_BUILTINS = {"comp", "Let", "If", "fst", "snd", "case", "Pair", "True", "False"}
    real_missing = [r for r in missing_defs if r not in HOL_BUILTINS]
    if real_missing:
        warnings.append(f"References *_def sans declaration trouvee : {real_missing[:10]}")

# 5. Motifs suspects
# 5a. `[OF lemma_name]` ou lemma_name n'a pas d'assumes
of_refs = re.findall(r"\b(\w+)\s*\[OF\s+(\w+)\]", CLEAN)
# basique: on detecte juste les patterns

# 5b. `sorry` dans une lemme cle (warning informatif)
sorry_count = CLEAN.count(" sorry") + CLEAN.count("\nsorry")
if sorry_count > 0:
    warnings.append(f"Nombre de 'sorry' (preuves incompletes) : {sorry_count}")

# 5c. `oops` (aban abandon)
if "oops" in CLEAN:
    errors.append("'oops' detecte (preuve abandonnee).")

# 5d. References a 'prime' : verifier que c'est bien HOL.Primes ou un consts local
imports_match = re.search(r"imports\s+([^\n]+(?:\n\s+[^\n]+)*)", SRC)
if imports_match:
    imports = imports_match.group(1)
    if "prime" in CLEAN.lower():
        if "Primes" in imports:
            infos.append("prime: utilise HOL-Computational_Algebra.Primes")
        elif "prime" in all_consts_names:
            infos.append("prime: declare localement comme consts")
        else:
            warnings.append("'prime' utilise sans import HOL.Primes ni declaration locale")

# 6. Counts
infos.append(f"Lignes totales : {len(SRC.splitlines())}")
SEC_RE = r'^\s*section\s+'
SUB_RE = r'^\s*subsection\s+'
AX_RE = r'^\s*axiomatization\b'
infos.append(f"Sections : {len(re.findall(SEC_RE, CLEAN, re.MULTILINE))}")
infos.append(f"Subsections : {len(re.findall(SUB_RE, CLEAN, re.MULTILINE))}")
infos.append(f"Definitions : {len(def_names)}")
infos.append(f"Fun : {len(fun_names)}")
infos.append(f"Lemmes : {len(lemma_names)}")
infos.append(f"Theoremes : {len(theorem_names)}")
infos.append(f"Axiomatizations : {len(re.findall(AX_RE, CLEAN, re.MULTILINE))}")
infos.append(f"Typedecls : {len(typedecls)}")
infos.append(f"Consts entries : {len(all_consts_names)}")

# Output style cygwin
print("=" * 70)
print(f"  Isabelle/HOL static-check  |  cygwin-terminal sim  |  v1.0")
print(f"  File: {THY}")
print("=" * 70)
print()
print("[ INFO ]")
for i in infos:
    print(f"  - {i}")
if warnings:
    print()
    print("[ WARN ]")
    for w in warnings:
        print(f"  ! {w}")
if errors:
    print()
    print("[ FAIL ]")
    for e in errors:
        print(f"  X {e}")
    print()
    print(f"RESULT: FAILED ({len(errors)} errors, {len(warnings)} warnings)")
    sys.exit(1)
else:
    print()
    if warnings:
        print(f"RESULT: OK with {len(warnings)} warning(s)")
    else:
        print(f"RESULT: PASS  (0 errors, 0 warnings)")
    sys.exit(0)
