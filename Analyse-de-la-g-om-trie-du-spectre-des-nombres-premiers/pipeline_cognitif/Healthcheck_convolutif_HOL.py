#!/usr/bin/env python3
"""Healthcheck for the cognitive convolution pipeline and its Isabelle session."""
from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
THEORY_DIR = ROOT / "agent-multiloop-Gabriel-local" / "theories"
THY_PATH = THEORY_DIR / "methode_spectral.thy"
WORKBOOK_PATH = ROOT / "systeme_convolutif_spectral_general.xlsx"
PDF_PATH = ROOT / "Le-systeme-convolutif-Gabriel.pdf"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(THEORY_DIR))

REPORT: list[tuple[str, str, str]] = []


def record(status: str, name: str, detail: str) -> None:
    REPORT.append((status, name, detail))
    print(f"[{status}] {name}: {detail}")


def verify(name: str, action: Callable[[], str]) -> None:
    try:
        record("OK", name, action())
    except Exception as exc:
        record("FAIL", name, f"{type(exc).__name__}: {exc}")


def check_dependencies_and_sources() -> str:
    missing = [
        name for name in ("sympy", "openpyxl", "pypdf")
        if importlib.util.find_spec(name) is None
    ]
    if missing:
        raise RuntimeError(f"dépendances requises absentes: {', '.join(missing)}")
    if not THY_PATH.is_file() or not WORKBOOK_PATH.is_file() or not PDF_PATH.is_file():
        raise FileNotFoundError("théorie HOL, classeur Excel ou PDF de référence absent")

    import openpyxl
    from pypdf import PdfReader

    workbook = openpyxl.load_workbook(WORKBOOK_PATH, read_only=True, data_only=True)
    required_sheets = {"Validation Convolutive", "Tests Digamma", "Code Python"}
    missing_sheets = sorted(required_sheets.difference(workbook.sheetnames))
    if missing_sheets:
        raise RuntimeError(f"feuilles Excel absentes: {missing_sheets}")
    pdf_pages = len(PdfReader(PDF_PATH).pages)
    if pdf_pages < 49:
        record(
            "WARN",
            "couverture PDF",
            f"le PDF disponible a {pdf_pages} pages; les pages 37–49 demandées ne sont pas présentes",
        )
    def normalized_values(sheet_name: str) -> set[str]:
        values = set()
        for row in workbook[sheet_name].iter_rows():
            for cell in row:
                value = cell.value
                if value is None:
                    continue
                if isinstance(value, float) and value.is_integer():
                    value = int(value)
                values.add(str(value).replace(" ", ""))
        return values

    validation_values = normalized_values("Validation Convolutive")
    system_values = normalized_values("Systeme General")
    if "16421" in validation_values and "16519" in system_values:
        record(
            "INFO",
            "branches 1/7 du classeur",
            "16421 apparaît dans Validation Convolutive; 16519 dans Systeme General; les deux sont des branches premières distinctes, catalogue A(8)- retenu",
        )
    numpy_status = "numpy présent" if importlib.util.find_spec("numpy") else "numpy absent (métaphore géométrique indisponible)"
    return (
        f"sympy/openpyxl/pypdf présents; théorie, PDF et classeur présents; "
        f"{len(workbook.sheetnames)} feuilles Excel; {pdf_pages} pages PDF; {numpy_status}"
    )


def check_theory_structure() -> str:
    raw = THY_PATH.read_bytes()
    text = raw.decode("utf-8", errors="strict")
    without_crlf = raw.replace(b"\r\n", b"")
    if b"\r" in without_crlf or (b"\r\n" in raw and b"\n" in without_crlf):
        raise ValueError("fins de ligne isolées ou mélangées dans methode_spectral.thy")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("BOM UTF-8 en tête du fichier HOL")

    required = [
        'subsection "XIV.1 ', 'subsection "XIV.2 ',
        'subsection "XIV.3 ', 'subsection "XIV.4 ',
        'subsection "XIV.5 ', 'subsection "XIV.6 ',
        'subsection "XIV.7 ', 'subsection "XIV.8 ',
        'subsection "XIV.9 ', 'subsection "XIV.10 ',
        'subsection "XIV.11 ', "RsP_conv_constant",
        "ancrages_conv", "reconstruction_conv_identity",
    ]
    missing = [marker for marker in required if marker not in text]
    if missing:
        raise ValueError(f"contenu HOL manquant: {missing}")

    import verify_thy_structure as verifier

    report = verifier.verify_file(THY_PATH, fix=False)
    if report.errors:
        raise ValueError("structure Isabelle: " + "; ".join(e.message for e in report.errors))

    root = (THEORY_DIR / "ROOT").read_text(encoding="utf-8")
    if 'session Methode_Spectral = HOL +' not in root:
        raise ValueError("session Methode_Spectral absente de theories/ROOT")
    if '"HOL-Computational_Algebra"' not in root:
        raise ValueError("dépendance HOL-Computational_Algebra absente de theories/ROOT")
    if "methode_spectral" not in root:
        raise ValueError("methode_spectral absent de la session Isabelle")
    return "UTF-8, EOL homogènes, structure vérifiée, sections XIV.1–XIV.11 et dépendances ROOT présentes"


def check_cognitive_pipeline() -> str:
    from pipeline_cognitif.multi_ratio_dispatcher import MultiRatioDispatcher
    from pipeline_cognitif.suites_geometriques_niveau2 import (
        ANCRAGES_XIV,
        CalculateurNiveau1Entiers,
        CalculateurNiveau2Geometrique,
        MethodeDigamma,
    )

    dispatcher = MultiRatioDispatcher()
    for k, reference in ANCRAGES_XIV.items():
        integer_result = CalculateurNiveau1Entiers(k).calculer(10)
        integer_prime, integer_candidates = MethodeDigamma(k, 10).reconstruire_premier(
            integer_result.somme_A, integer_result.somme_B, verbose=False
        )
        geometric_prime, geometric_candidates = CalculateurNiveau2Geometrique(k).reconstruire_premier(
            n=10, verbose=False
        )
        integer_branches = {
            (c["position"], c["signe"], c["P_candidat"])
            for c in integer_candidates if c["est_premier"]
        }
        geometric_branches = {
            (c["position"], c["signe"], c["P_candidat"])
            for c in geometric_candidates if c["est_premier"]
        }
        if integer_branches != geometric_branches:
            raise AssertionError(f"branches entières/géométriques différentes pour k={k}")
        result = dispatcher.requete(n=10, liste_k=[k]).resultats[k]
        if integer_prime != reference["premier"] or geometric_prime != reference["premier"]:
            raise AssertionError(f"ancre catalogue incohérente pour k={k}")
        if result.premier_ancre_n10 != reference["premier"]:
            raise AssertionError(f"dispatcher incohérent pour k={k}")
        if {(p, s, n) for p, s, n in result.candidats_ancre_n10} != integer_branches:
            raise AssertionError(f"branches du dispatcher incomplètes pour k={k}")

    for k, expected_count in ((10, 3), (20, 2)):
        result = dispatcher.requete(n=10, liste_k=[k]).resultats[k]
        if result.premier_ancre_n10 is not None:
            raise AssertionError(f"ancrage ambigu choisi automatiquement pour k={k}")
        if len(result.candidats_ancre_n10) != expected_count or "ambigu" not in result.message.lower():
            raise AssertionError(f"branches ambiguës non exposées pour k={k}")

    compact_report = dispatcher.requete(n=10, liste_k=[7, 10, 20]).tableau_texte()
    for marker in ("A(8)+=16421", "A(8)-=16519", "AMBIGU", "3192419"):
        if marker not in compact_report:
            raise AssertionError(f"branche absente du tableau multi-rapports: {marker}")

    large = dispatcher.requete(n=10, liste_k=[9999]).resultats[9999]
    cited_anchor = 99950008999300019999
    if cited_anchor not in {candidate[2] for candidate in large.candidats_ancre_n10}:
        raise AssertionError("l'ancre citée pour k=9999 n'est pas issue des quatre essais")
    if cited_anchor > 2 ** 64:
        record(
            "WARN",
            "certification du candidat k=9999",
            "candidat supérieur à 2^64: le résultat SymPy n'est pas une preuve HOL de primalité",
        )
    return (
        "ancres catalogue k=2..9; candidats entiers=géométriques; "
        "ambiguïtés k=10/20 signalées; ancre citée k=9999 retrouvée"
    )


def run_hol_build() -> None:
    isabelle = shutil.which("isabelle")
    if not isabelle:
        record("FAIL", "build Isabelle", "exécutable isabelle absent du PATH")
        return
    try:
        result = subprocess.run(
            [isabelle, "build", "-d", ".", "-v", "Methode_Spectral"],
            cwd=THEORY_DIR,
            capture_output=True,
            text=True,
            timeout=1800,
            check=False,
        )
    except subprocess.TimeoutExpired:
        record("FAIL", "build Isabelle", "délai dépassé après 30 minutes")
        return
    if result.returncode:
        tail = (result.stdout + "\n" + result.stderr).splitlines()[-20:]
        record("FAIL", "build Isabelle", "\n".join(tail))
    else:
        record("OK", "build Isabelle", "session Methode_Spectral compilée")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--build-hol", action="store_true",
        help="compile la session Isabelle Methode_Spectral si Isabelle est accessible",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="retourner un code non nul si Isabelle n'est pas disponible",
    )
    args = parser.parse_args()

    verify("sources et dépendances", check_dependencies_and_sources)
    verify("structure HOL et session", check_theory_structure)
    verify("pipeline cognitif à deux niveaux", check_cognitive_pipeline)

    if args.build_hol:
        run_hol_build()
    elif shutil.which("isabelle"):
        record("INFO", "build Isabelle", "disponible; relancer avec --build-hol pour compiler")
    else:
        record("WARN", "build Isabelle", "non disponible dans ce terminal; utiliser Cygwin ou GitHub Actions")

    failures = sum(status == "FAIL" for status, _, _ in REPORT)
    warnings = sum(status == "WARN" for status, _, _ in REPORT)
    print(f"\nBilan: {len(REPORT) - failures - warnings} OK, {warnings} avertissement(s), {failures} échec(s)")
    return 1 if failures or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
