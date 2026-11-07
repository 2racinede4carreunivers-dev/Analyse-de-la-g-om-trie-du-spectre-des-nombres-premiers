"""Static traceability audit for the TeX/PDF document and Isabelle sources.

This script checks source/file references and selected exact anchor values.
It does not prove semantic equivalence, validate axioms, or replace an
Isabelle session build.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


THEORY_ROWS = (
    ("MS_01_Fondements.thy", ("foundations_marker_satisfaisable",)),
    ("MS_02_Suites_AB_RsP_1_2.thy", ("RsP_un_demi_general",)),
    ("MS_03_Digamma_Equation_Generale.thy", ()),
    ("MS_04_Generalisation_Prime_i.thy", ("prime_position_exists",)),
    (
        "MS_05_Modeles_1_3_1_4.thy",
        ("RsP_un_tiers_constant", "RsP_un_quart_constant"),
    ),
    ("MS_06_Mixtes_Negatives_Asymetries.thy", ("RsP_neg_un_demi_general",)),
    ("MS_07_Comparaison_Blocs.thy", ("ponderation_bloc_uniforme",)),
    ("MS_08_Ecarts_Negatifs.thy", ("non_typique_absurde",)),
    (
        "MS_09_Preuve_Absurde.thy",
        ("composite_not_prime_i", "composite_no_reconstruction_position"),
    ),
    ("MS_10_Ecarts_Mixtes_Positifs.thy", ("gap_equation_1_3_for_primes",)),
    ("MS_11_Construction_SpectralFamily.thy", ("RsP_generic_constant",)),
    ("MS_12_Construction_Generalisee_1k.thy", ("somme_A_pos_k_eq_SA",)),
    (
        "MS_13_Pont_Savard.thy",
        (
            "alignement_central",
            "pont_spectral_direct_final",
            "synthese_pont_savard",
        ),
    ),
    (
        "MS_14_Systeme_Convolutif.thy",
        (
            "RsP_conv_constant",
            "reconstruction_conv_identity",
            "ancrages_conv",
        ),
    ),
    (
        "validation_hol_unifiee.thy",
        ("prime_227_ax", "ancrage_k4"),
    ),
    (
        "validation_zeta_lean.thy",
        ("equation_fonctionnelle_lean", "premier_pont_tchebychev_zeta"),
    ),
)


def normalize(text: str) -> str:
    text = text.replace(r"\_", "_")
    return re.sub(r"\s+", " ", text).strip()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", normalize(text))


def read_root_theories(root_file: Path) -> list[str]:
    theories: list[str] = []
    in_theories = False
    for line in root_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "theories":
            in_theories = True
            continue
        if not in_theories:
            continue
        if not stripped or stripped.startswith("(*"):
            continue
        if re.match(r"^[A-Za-z][A-Za-z0-9_-]*\s", stripped):
            break
        theories.append(stripped.split()[0])
    return theories


def extract_anchor_values(text: str) -> dict[int, tuple[int, int]]:
    ranks = {
        int(k): int(value)
        for k, value in re.findall(r"rang_base_k\s+(\d+)\s*=\s*(\d+)", text)
    }
    primes = {
        int(k): int(value)
        for k, value in re.findall(r"premier_base_k\s+(\d+)\s*=\s*(\d+)", text)
    }
    return {
        k: (rank, primes[k])
        for k, rank in ranks.items()
        if k in primes
    }


def get_pdf_text(pdf_path: Path) -> tuple[str | None, str]:
    extractor = shutil.which("pdftotext")
    if not extractor:
        return None, "pdftotext is unavailable"
    if not pdf_path.is_file():
        return None, f"PDF not found: {pdf_path}"
    result = subprocess.run(
        [extractor, "-layout", str(pdf_path), "-"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        detail = result.stderr.strip() or f"exit code {result.returncode}"
        return None, f"PDF extraction failed: {detail}"
    return result.stdout, ""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        help="Repository root (defaults to the parent of this script's folder).",
    )
    parser.add_argument("--tex", type=Path, help="TeX source file to audit.")
    parser.add_argument("--pdf", type=Path, help="Compiled PDF to audit.")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Attempt an Isabelle build of the session declared in theories/ROOT.",
    )
    args = parser.parse_args()

    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    theories_dir = root / "theories"
    root_file = theories_dir / "ROOT"
    tex_path = (
        args.tex
        or root
        / "Document-pdf-tex"
        / "Philippe_Thomas_Savard_@_tous_droits_réservé-2026.tex"
    ).resolve()
    pdf_path = (args.pdf or tex_path.with_suffix(".pdf")).resolve()
    incomplete = False
    inconsistent = False

    if not root_file.is_file():
        print(f"ERREUR: session ROOT introuvable: {root_file}")
        return 2
    if not tex_path.is_file():
        print(f"ERREUR: source TeX introuvable: {tex_path}")
        return 2

    root_text = root_file.read_text(encoding="utf-8")
    tex_text = tex_path.read_text(encoding="utf-8")
    tex_normalized = normalize(tex_text)
    pdf_text, pdf_status = get_pdf_text(pdf_path)
    pdf_compact = compact(pdf_text) if pdf_text is not None else ""

    print("Audit statique TeX/PDF <-> Isabelle/HOL")
    print(f"Session: {root_file}")
    session_match = re.search(r"(?m)^\s*session\s+([^\s=]+)", root_text)
    if session_match:
        print(f"Session déclarée: {session_match.group(1)}")
    print(f"TeX: {tex_path}")
    print(f"PDF: {pdf_path}")

    root_theories = read_root_theories(root_file)
    missing_session_files = [
        name for name in root_theories if not (theories_dir / f"{name}.thy").is_file()
    ]
    if missing_session_files:
        incomplete = True
        print(
            "BLOQUÉ: théorie(s) référencée(s) mais absente(s): "
            + ", ".join(missing_session_files)
        )
    else:
        print(f"OK: {len(root_theories)} théories référencées présentes.")

    print("\nCorrespondances source / TeX / PDF:")
    for filename, symbols in THEORY_ROWS:
        source_path = theories_dir / filename
        tex_has_file = compact(filename) in compact(tex_normalized)
        source_text = (
            source_path.read_text(encoding="utf-8") if source_path.is_file() else ""
        )
        missing_symbols = [
            symbol for symbol in symbols if symbol not in source_text
        ]
        missing_tex_symbols = [
            symbol for symbol in symbols if symbol not in compact(tex_normalized)
        ]
        missing_pdf_symbols = [
            symbol for symbol in symbols if pdf_text is not None and symbol not in pdf_compact
        ]
        status = "OK"
        if not source_path.is_file():
            status = "ABSENT"
            incomplete = True
        elif missing_symbols or not tex_has_file or missing_tex_symbols or missing_pdf_symbols:
            status = "À CORRIGER"
            inconsistent = True
        details = []
        if symbols:
            details.append("symboles " + ", ".join(symbols))
        if not tex_has_file:
            details.append("référence TeX absente")
        if missing_symbols:
            details.append("source sans " + ", ".join(missing_symbols))
        if missing_tex_symbols:
            details.append("TeX sans " + ", ".join(missing_tex_symbols))
        if missing_pdf_symbols:
            details.append("PDF sans " + ", ".join(missing_pdf_symbols))
        print(f"[{status}] {filename}" + (": " + "; ".join(details) if details else ""))

    ms14_path = theories_dir / "MS_14_Systeme_Convolutif.thy"
    ms14_text = ms14_path.read_text(encoding="utf-8") if ms14_path.is_file() else ""
    anchor_axiom = re.search(
        r"axiomatization\s+where\s+ancrages_conv\s*:\s*\"(.*?)\"",
        ms14_text,
        flags=re.DOTALL,
    )
    anchor_box = re.search(
        r"\\begin\{boitehol\}\{Données d'ancrage k=3 à 9.*?"
        r"\\begin\{holcode\}(.*?)\\end\{holcode\}",
        tex_text,
        flags=re.DOTALL,
    )
    if not anchor_axiom or not anchor_box:
        inconsistent = True
        print("\nERREUR: impossible d'extraire l'axiome ou l'extrait d'ancrages.")
    else:
        source_values = extract_anchor_values(anchor_axiom.group(1))
        tex_values = extract_anchor_values(anchor_box.group(1))
        if source_values == tex_values:
            print(f"\nOK: rangs et premiers d'ancrage identiques: {source_values}")
        else:
            inconsistent = True
            print(f"\nÉCART d'ancrages: source={source_values}; TeX={tex_values}")

    if pdf_text is None:
        incomplete = True
        print(f"\nAVERTISSEMENT PDF: {pdf_status}")
    else:
        print("\nOK: texte PDF extrait pour contrôle des symboles.")

    prime_axioms = re.findall(
        r"(?m)^\s*prime_\d+_ax\s*:",
        (theories_dir / "validation_hol_unifiee.thy").read_text(encoding="utf-8"),
    )
    print(
        "Note de statut: "
        f"{len(prime_axioms)} déclarations d'axiomes prime_<n>_ax recensées "
        "dans validation_hol_unifiee.thy."
    )

    if args.build:
        isabelle = shutil.which("isabelle")
        if not isabelle:
            print("\nBUILD BLOQUÉ: commande Isabelle introuvable.")
            return 2
        if not session_match:
            print("\nBUILD BLOQUÉ: nom de session introuvable dans ROOT.")
            return 2
        result = subprocess.run(
            [
                isabelle,
                "build",
                "-D",
                str(theories_dir),
                session_match.group(1),
            ],
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode:
            print(f"\nÉCHEC du build Isabelle (code {result.returncode}).")
            return result.returncode
        print("\nOK: build Isabelle réussi.")

    if inconsistent:
        print(
            "\nRésultat: incohérence de références ou de données. "
            "Le contrôle statique ne certifie pas les preuves HOL."
        )
        return 1
    if incomplete:
        print(
            "\nRésultat: références et données comparées cohérentes, "
            "mais session/source incomplète. "
            "Le contrôle statique ne certifie pas les preuves HOL."
        )
        return 1
    print(
        "\nRésultat: références et données numériques cohérentes. "
        "Le contrôle statique ne certifie pas les preuves HOL."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
