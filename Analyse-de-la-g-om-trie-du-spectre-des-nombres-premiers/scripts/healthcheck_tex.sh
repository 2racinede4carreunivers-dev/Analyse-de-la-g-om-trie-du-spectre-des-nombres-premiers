#!/usr/bin/env bash
# =============================================================================
#  healthcheck_tex.sh - Garde-fou pre-commit pour les fichiers .tex de Gabriel
# =============================================================================
#  v3.45 - Verifie statiquement 15+ proprietes du .tex avant chaque commit :
#    - Encodage : UTF-8 strict, sans BOM, LF-only, NFC, sans NUL/ctrl/mojibake
#    - Structure LaTeX : documentclass + begin/end{document} uniques
#    - Bibliographie : begin/end{thebibliography} equilibres, bibitems uniques
#    - Duplicatas : aucun \label{...} duplique, aucun \bibitem[...]{cle} duplique
#    - pasj02 : aucun \section*/\subsection*/\subsubsection* residuel (utiliser
#      \unnumberedsection/\unnumberedsubsection/\unnumberedsubsubsection)
#    - Delimiteurs : accolades { } equilibrees, math $ de parite paire
#
#  Usage :
#    ./scripts/healthcheck_tex.sh                  # verifie UNIQUEMENT le
#                                                  # fichier canonique v13
#                                                  # (geometrie_gabriel_savard_13.tex)
#    ./scripts/healthcheck_tex.sh path/to/file.tex # verifie un fichier specifique
#
#  Installation en pre-commit git :
#    ln -s ../../scripts/healthcheck_tex.sh .git/hooks/pre-commit
#    chmod +x .git/hooks/pre-commit
#
#  Sortie : code 0 si OK, code 1 si un controle echoue.
# =============================================================================
set -euo pipefail

# Determiner le repertoire racine (script est dans scripts/, .tex dans theories/tex/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"

# Cibler soit le(s) fichier(s) passe(s) en argument, soit UNIQUEMENT le .tex
# courant destine a la compilation (geometrie_gabriel_savard_13.tex).
# v3.45-fix : eviter de bloquer sur les .tex historiques (v10/v11/v12) qui
# contiennent volontairement les anciennes formes non-corrigees.
if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  # Fichier canonique (le seul destine a la compilation actuelle)
  DEFAULT_TEX="${REPO_ROOT}/theories/tex/geometrie_gabriel_savard_13.tex"
  if [[ -f "${DEFAULT_TEX}" ]]; then
    FILES=("${DEFAULT_TEX}")
  else
    echo "ERREUR : fichier canonique introuvable : ${DEFAULT_TEX}" >&2
    echo "  Passez explicitement les .tex a verifier en argument," >&2
    echo "  ou restaurez le fichier canonique." >&2
    exit 2
  fi
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "Aucun fichier .tex trouve."
  exit 0
fi

FAIL=0
for f in "${FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "  SKIP $f (introuvable)"
    continue
  fi

  echo "=============================================================================="
  echo "  Healthcheck : $f"
  echo "=============================================================================="

  # Delegue tous les controles a Python (portable, robuste)
  python3 - "$f" <<'PYEOF' || FAIL=$((FAIL+1))
import re
import sys
import unicodedata

p = sys.argv[1]
raw = open(p, 'rb').read()
try:
    txt = raw.decode('utf-8', errors='strict')
except UnicodeDecodeError as exc:
    print(f"  FAIL : UTF-8 strict -> {exc}")
    sys.exit(1)

# ligne active = supprime les commentaires (y compris inline `... % ...`).
# Une contre-barre echappee `\%` n'est PAS un commentaire.
def _strip_inline_comments(line: str) -> str:
    out = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == '\\' and i + 1 < len(line):
            out.append(line[i:i+2])
            i += 2
            continue
        if c == '%':
            break
        out.append(c)
        i += 1
    return ''.join(out)

active = "\n".join(_strip_inline_comments(l) for l in txt.splitlines())

BOM = b'\xef\xbb\xbf'
bibitems = re.findall(r'\\bibitem\[[^\]]*\]\{([^}]+)\}', active)
labels   = re.findall(r'\\label\{([^}]+)\}', active)
# v3.45-fix : detecter les starred sections AILLEURS que colonne 1 (indentation
# ou apres blanc) pour eviter le contournement `  \section*{...}`.
starred_secs = re.findall(r'(?:^|\s)\\(?:sub){0,2}section\*|(?:^|\s)\\paragraph\*', active)

checks = [
    ("BOM absent (UTF-8 sans BOM)",         not raw.startswith(BOM)),
    ("UTF-8 strict",                        True),
    # v3.45-fix : rejeter TOUT byte \r (CRLF ET CR seuls, ancien Mac)
    ("Aucun caractere CR (\\r)",            raw.count(b'\r') == 0),
    ("Aucun octet NUL",                     raw.count(b'\x00') == 0),
    ("Aucun caractere de controle illegal", not [i for i,c in enumerate(txt) if ord(c)<32 and c not in '\n\r\t']),
    ("NFC normalized",                      txt == unicodedata.normalize('NFC', txt)),
    ("Aucun mojibake (Ã©/â€™/etc.)",        not any(m in txt for m in ['\u00c3\u00a9','\u00c3\u00a8','\u00e2\u0080\u0099','\u00c3\u00a0','\u00c3\u00b4'])),
    ("Contient \\documentclass",            r'\documentclass' in active),
    ("1 seul \\begin{document} actif",      active.count(r'\begin{document}') == 1),
    ("1 seul \\end{document} actif",        active.count(r'\end{document}') == 1),
    ("Termine par \\end{document}",         txt.rstrip().endswith(r'\end{document}')),
    ("\\begin/\\end{thebibliography} equilibres",
                                            active.count(r'\begin{thebibliography}') == active.count(r'\end{thebibliography}')),
    ("Accolades { } equilibrees",           txt.count('{') == txt.count('}')),
    ("Math $ de parite paire",              txt.count('$') % 2 == 0),
    ("Aucun \\bibitem duplique",            len(bibitems) == len(set(bibitems))),
    ("Aucun \\label duplique",              len(labels) == len(set(labels))),
    ("Aucun \\section*/\\subsection*/\\subsubsection* residuel (pasj02)",
                                            len(starred_secs) == 0),
]

ok = 0
for lbl, r in checks:
    print(f"  {'OK  ' if r else 'FAIL'} : {lbl}")
    if r: ok += 1

# Details sur les duplicatas eventuels
if len(bibitems) != len(set(bibitems)):
    from collections import Counter
    dups = [k for k,c in Counter(bibitems).items() if c > 1]
    print(f"        Bibitems dupliques : {dups}")
if len(labels) != len(set(labels)):
    from collections import Counter
    dups = [k for k,c in Counter(labels).items() if c > 1]
    print(f"        Labels dupliques : {dups}")
if starred_secs:
    print(f"        Starred sections residuels : {len(starred_secs)}")

print()
print(f"  Bilan : {ok}/{len(checks)}  |  lignes={len(txt.splitlines())}  bytes={len(raw)}")
sys.exit(0 if ok == len(checks) else 1)
PYEOF

done

echo "=============================================================================="
if [[ $FAIL -eq 0 ]]; then
  echo "  TOUS LES CONTROLES ONT PASSE. Compilation LaTeX prete."
  exit 0
else
  echo "  ECHEC : $FAIL fichier(s) avec au moins un controle en erreur."
  echo "  Corrigez les problemes ci-dessus avant de commiter."
  exit 1
fi
