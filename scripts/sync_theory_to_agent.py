"""Script de synchronisation theory <-> RAG cognitif Gabriel.

Verifie que :
  1. methode_spectral.thy est present dans le conteneur (theories/).
  2. La structure HOL passe le static-check (isabelle_static_check.py).
  3. Les modules memory pour Section XI et XII sont chargeables.
  4. Le Dictionnaire Spectral expose bien les nouveaux regimes
     (regime_construction_termes, regime_parametrique_1_k).
  5. L'adaptateur RAG detecte correctement des requetes typiques
     ("construction suite A 7 termes", "rapport spectral 1/3", etc.).

Usage:
    python scripts/sync_theory_to_agent.py
    python scripts/sync_theory_to_agent.py --verbose
"""
from __future__ import annotations
import argparse
import importlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THY = ROOT / "theories" / "methode_spectral.thy"
STATIC_CHECK = ROOT / "scripts" / "isabelle_static_check.py"

# Permet d'importer 'memory.*' meme quand on lance le script depuis /scripts
sys.path.insert(0, str(ROOT))


def check_theory_file() -> tuple[bool, str]:
    """Verifie presence et taille du fichier theory."""
    if not THY.exists():
        return False, f"Fichier introuvable : {THY}"
    size = THY.stat().st_size
    lines = sum(1 for _ in THY.open(encoding="utf-8"))
    return True, f"{THY.name} present ({size:,} octets, {lines} lignes)"


def run_static_check() -> tuple[bool, str]:
    """Lance le static-check Isabelle simule."""
    if not STATIC_CHECK.exists():
        return False, f"Script introuvable : {STATIC_CHECK}"
    result = subprocess.run(
        [sys.executable, str(STATIC_CHECK), str(THY)],
        capture_output=True, text=True, check=False,
    )
    last_line = (result.stdout.strip().splitlines() or ["(no output)"])[-1]
    return result.returncode == 0, last_line


def check_memory_modules() -> tuple[bool, list[str]]:
    """Verifie que les modules memory sont chargeables."""
    msgs = []
    all_ok = True
    for mod_name in [
        "memory.dictionnaire_spectral",
        "memory.adaptateur_cognitif_rag",
        "memory.methode_spectral_section_XI",
        "memory.methode_spectral_section_XII",
        "memory.methode_spectral_section_XIII",
    ]:
        try:
            mod = importlib.import_module(mod_name)
            msgs.append(f"  [OK]  {mod_name} ({mod.__file__})")
        except Exception as exc:
            msgs.append(f"  [FAIL] {mod_name} : {exc}")
            all_ok = False
    return all_ok, msgs


def check_new_regimes_registered() -> tuple[bool, list[str]]:
    """Verifie que les 3 nouveaux regimes (XI/XII/XIII) sont dans le dictionnaire."""
    from memory.dictionnaire_spectral import DICTIONNAIRE_SPECTRAL, list_regimes
    msgs = [f"  Total regimes : {len(DICTIONNAIRE_SPECTRAL)}"]
    expected_new = [
        "regime_construction_termes",
        "regime_parametrique_1_k",
        "regime_pont_savard",
    ]
    all_ok = True
    for r in expected_new:
        if r in DICTIONNAIRE_SPECTRAL:
            reg = DICTIONNAIRE_SPECTRAL[r]
            msgs.append(f"  [OK] {r}: {len(reg.lemmes_certifies)} lemmes, "
                        f"{len(reg.regles_cognitives)} regles")
        else:
            msgs.append(f"  [FAIL] {r} ABSENT du dictionnaire")
            all_ok = False
    msgs.append(f"  Tous les regimes : {list_regimes()}")
    return all_ok, msgs


def check_section_modules() -> tuple[bool, list[str]]:
    """Verifie que les modules Section XI et XII generent leurs entrees RAG."""
    msgs = []
    all_ok = True
    try:
        from memory.methode_spectral_section_XI import get_section_XI_entries
        entries_xi = get_section_XI_entries()
        msgs.append(f"  [OK] Section XI : {len(entries_xi)} entrees RAG")
    except Exception as exc:
        msgs.append(f"  [FAIL] Section XI : {exc}")
        all_ok = False

    try:
        from memory.methode_spectral_section_XII import (
            get_section_XII_entries,
            construire_suite_A,
            construire_suite_B,
        )
        entries_xii = get_section_XII_entries()
        msgs.append(f"  [OK] Section XII : {len(entries_xii)} entrees RAG")

        # Smoke tests sur les helpers de calcul
        from fractions import Fraction
        suite_a_7 = construire_suite_A(2, 7)
        expected_7 = [Fraction(x) for x in [2, 4, 8, 16, 32, 48, 96]]
        if suite_a_7 == expected_7:
            msgs.append(f"  [OK] construire_suite_A(k=2, n=7) = [2,4,8,16,32,48,96]")
        else:
            msgs.append(f"  [FAIL] construire_suite_A(k=2, n=7) = {suite_a_7}")
            all_ok = False

        suite_b_8 = construire_suite_B(2, 8)
        expected_8 = [Fraction(x) for x in [2, 4, 8, 16, 32, 128, 192, 384]]
        if suite_b_8 == expected_8:
            msgs.append(f"  [OK] construire_suite_B(k=2, n=8) = [2,4,8,16,32,128,192,384]")
        else:
            msgs.append(f"  [FAIL] construire_suite_B(k=2, n=8) = {suite_b_8}")
            all_ok = False
    except Exception as exc:
        msgs.append(f"  [FAIL] Section XII : {exc}")
        all_ok = False

    try:
        from memory.methode_spectral_section_XIII import (
            get_section_XIII_entries,
            verifier_validations_canoniques,
        )
        entries_xiii = get_section_XIII_entries()
        msgs.append(f"  [OK] Section XIII : {len(entries_xiii)} entrees RAG")
        verdicts = verifier_validations_canoniques()
        if all(v["ok"] for v in verdicts):
            msgs.append(
                f"  [OK] Section XIII : {len(verdicts)}/{len(verdicts)} validations "
                f"canoniques psi_savard (30, 98, 228, -100)"
            )
        else:
            fails = [v for v in verdicts if not v["ok"]]
            msgs.append(f"  [FAIL] Section XIII : validations echouees : {fails}")
            all_ok = False
    except Exception as exc:
        msgs.append(f"  [FAIL] Section XIII : {exc}")
        all_ok = False

    return all_ok, msgs


def check_rag_detection(verbose: bool = False) -> tuple[bool, list[str]]:
    """Test l'adaptateur RAG sur des requetes typiques de Section XI/XII."""
    from memory.adaptateur_cognitif_rag import AdaptateurCognitifSpectral
    ad = AdaptateurCognitifSpectral()
    cas_tests = [
        ("Construis-moi la suite A pour 7 termes en k=2",
         "regime_construction_termes"),
        ("Quelles sont les constantes alpha_A et alpha_B pour k=3 ?",
         "regime_parametrique_1_k"),
        ("Donne-moi la substitution position 6 pour la suite B avec 8 termes",
         "regime_construction_termes"),
        ("Calcule le rapport spectral 1/4 pour le premier 947",
         "regime_1_4"),
    ]
    msgs = []
    all_ok = True
    for requete, attendu in cas_tests:
        analyse = ad.analyser(requete)
        detected = attendu in analyse.regimes_detectes
        status = "[OK]" if detected else "[FAIL]"
        if not detected:
            all_ok = False
        msgs.append(f"  {status} requete: {requete[:55]}...")
        msgs.append(f"        attendu: {attendu}")
        msgs.append(f"        detecte: {analyse.regimes_detectes}")
        if verbose and analyse.matched_keywords:
            msgs.append(f"        keywords: {analyse.matched_keywords}")
    return all_ok, msgs


def main():
    parser = argparse.ArgumentParser(description="Synchronise theory <-> agent cognitif")
    parser.add_argument("--verbose", action="store_true", help="affichage detaille")
    args = parser.parse_args()

    print("=" * 72)
    print("  Gabriel Multiloop - Synchronisation Theory <-> Agent Cognitif")
    print("=" * 72)

    all_ok = True
    sections = [
        ("1. Fichier theory present",       check_theory_file),
        ("2. Static-check Isabelle",        run_static_check),
        ("3. Modules memory chargeables",   check_memory_modules),
        ("4. Nouveaux regimes XI/XII",      check_new_regimes_registered),
        ("5. Sections XI/XII actives",      check_section_modules),
        ("6. Detection RAG",                lambda: check_rag_detection(args.verbose)),
    ]

    for title, func in sections:
        print(f"\n[ {title} ]")
        ok, payload = func()
        if isinstance(payload, list):
            for line in payload:
                print(line)
        else:
            print(f"  {payload}")
        if not ok:
            all_ok = False

    print("\n" + "=" * 72)
    if all_ok:
        print("  RESULTAT GLOBAL : SYNCHRONISATION OK")
        print("=" * 72)
        return 0
    else:
        print("  RESULTAT GLOBAL : ECHEC - voir les FAIL ci-dessus")
        print("=" * 72)
        return 1


if __name__ == "__main__":
    sys.exit(main())
