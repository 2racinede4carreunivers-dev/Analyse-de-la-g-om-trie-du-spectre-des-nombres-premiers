#!/usr/bin/env python3
"""
patch_cli_hol_v2.py
Injecte les 8 lignes HOL dans cli.py via remplacement texte exact.

Usage : python patch_cli_hol_v2.py
Lancer depuis : C:\\agent-multiloop-Gabriel-local-final\\
"""
import shutil
import sys
from pathlib import Path

CLI_CANDIDATES = [
    Path("src/ui/cli.py"),
    Path("agent-multiloop-Gabriel-local/src/ui/cli.py"),
    Path("backend/src/ui/cli.py"),
]

# ── Texte EXACT à trouver (copié mot pour mot du cli.py)
ANCIEN = (
    '                verbose_trace = self._env_enabled("GABRIEL_TRACE_VERBOSE", default=True)\n'
    '\n'
    '                if not live_trace:'
)

# ── Texte de remplacement (même texte + bloc HOL inséré entre les deux)
NOUVEAU = (
    '                verbose_trace = self._env_enabled("GABRIEL_TRACE_VERBOSE", default=True)\n'
    '\n'
    '                # 4c) Pipeline cognitif HOL — enrichissement corpus spectral Savard\n'
    '                try:\n'
    '                    from gabriel_p4_bridge import enrichir_prompt_hol as _hol\n'
    '                    _ctx = await _hol(user_input)\n'
    '                    if _ctx:\n'
    '                        user_input = _ctx + "\\n\\n---\\nQuestion : " + user_input\n'
    '                except Exception:\n'
    '                    pass\n'
    '\n'
    '                if not live_trace:'
)


def trouver_cli() -> Path:
    for p in CLI_CANDIDATES:
        if p.exists():
            return p
    for p in Path(".").rglob("cli.py"):
        if "ui" in p.parts:
            return p
    print("ERREUR : cli.py introuvable.")
    sys.exit(1)


def patcher(cli: Path) -> None:
    print(f"  cli.py          : {cli.resolve()}")

    content = cli.read_text(encoding="utf-8")
    lignes_avant = content.count("\n")
    print(f"  Lignes avant    : {lignes_avant}")

    if "Pipeline cognitif HOL" in content:
        print("  DEJA PATCHE — rien a faire.")
        return

    if ANCIEN not in content:
        # Essai avec fins de ligne Windows \r\n
        ancien_crlf = ANCIEN.replace("\n", "\r\n")
        if ancien_crlf in content:
            nouveau_crlf = NOUVEAU.replace("\n", "\r\n")
            content = content.replace(ancien_crlf, nouveau_crlf, 1)
        else:
            print("  ERREUR : texte cible introuvable.")
            print("  Verifiez que GABRIEL_TRACE_VERBOSE existe dans cli.py :")
            print()
            print('  Select-String -Path src\\ui\\cli.py -Pattern "GABRIEL_TRACE_VERBOSE"')
            sys.exit(1)
    else:
        content = content.replace(ANCIEN, NOUVEAU, 1)

    backup = cli.with_suffix(".py.backup_hol")
    shutil.copy(cli, backup)
    print(f"  Backup          : {backup.name}")

    cli.write_text(content, encoding="utf-8")

    lignes_apres = content.count("\n")
    ajout = lignes_apres - lignes_avant
    print(f"  Lignes apres    : {lignes_apres}")
    print(f"  Lignes ajoutees : {ajout}")

    if ajout >= 8:
        print("\n  OK — Patch applique avec succes.")
    else:
        print(f"\n  ATTENTION : seulement {ajout} lignes ajoutees.")


if __name__ == "__main__":
    print("\n  PATCH CLI HOL v2 — Pipeline Cognitif Gabriel")
    print("  =============================================")
    cli = trouver_cli()
    patcher(cli)
    print()
