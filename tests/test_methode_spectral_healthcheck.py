"""Healthcheck exhaustif de theories/methode_spectral.thy (v3.42).

Ces tests restent purement statiques : Isabelle/HOL n'est pas installe dans
le conteneur. La grammaire de surface est donc validee par
verify_thy_structure en plus des controles binaires et structurels directs.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
THY_PATH = ROOT / "theories" / "methode_spectral.thy"
sys.path.insert(0, str(ROOT / "theories"))
import verify_thy_structure as vts  # noqa: E402


@pytest.fixture(scope="module")
def raw() -> bytes:
    return THY_PATH.read_bytes()


@pytest.fixture(scope="module")
def text(raw: bytes) -> str:
    return raw.decode("utf-8", errors="strict")


def _assert_balanced_tokens(content: str, opening: str, closing: str) -> None:
    """Verifie le compte, l'ordre et l'imbrication de deux delimiteurs."""
    depth = 0
    cursor = 0
    while cursor < len(content):
        if content.startswith(opening, cursor):
            depth += 1
            cursor += len(opening)
        elif content.startswith(closing, cursor):
            depth -= 1
            assert depth >= 0, f"Delimiteur {closing!r} ferme avant toute ouverture"
            cursor += len(closing)
        else:
            cursor += 1
    assert depth == 0, f"Delimiteurs desequilibres : profondeur finale {depth}"
    assert content.count(opening) == content.count(closing)


class TestMethodeSpectralHealthcheck:
    """Quinze controles de sante independants sur le fichier Isabelle."""

    def test_01_no_utf8_bom(self, raw: bytes):
        assert not raw.startswith(b"\xef\xbb\xbf"), "BOM UTF-8 detecte en tete"

    def test_02_strict_utf8_decode(self, raw: bytes):
        decoded = raw.decode("utf-8", errors="strict")
        assert decoded.encode("utf-8") == raw

    def test_03_no_mojibake(self, text: str):
        bad_sequences = set(vts.MOJIBAKE_MAP) | {
            "Ã©", "Ã¨", "Ãª", "Ã ", "Ã§", "Â ",
            "â€™", "â€˜", "â€œ", "â€�", "â€“", "â€”",
            "â€¹", "â€º", "â‰¥", "â‰¤", "â‡’", "â„™",
        }
        found = sorted(sequence for sequence in bad_sequences if sequence in text)
        assert not found, f"Sequences mojibake detectees : {found}"

    def test_04_consistent_line_endings(self, raw: bytes):
        without_crlf = raw.replace(b"\r\n", b"")
        assert b"\r" not in without_crlf, "Retour chariot isole detecte"
        assert not (b"\r\n" in raw and b"\n" in without_crlf), (
            "Fins de ligne LF et CRLF melangees"
        )

    def test_05_no_illegal_control_characters(self, text: str):
        illegal = [
            (index, ord(char))
            for index, char in enumerate(text)
            if (ord(char) < 32 or ord(char) == 127) and char not in "\n\r\t"
        ]
        assert not illegal, f"Caracteres de controle illegaux : {illegal[:10]}"

    def test_06_no_nul_byte(self, raw: bytes):
        assert b"\x00" not in raw, "Octet NUL detecte"

    def test_07_balanced_isabelle_cartouches(self, text: str):
        _assert_balanced_tokens(text, r"\<open>", r"\<close>")
        assert text.count(r"\<open>") >= 60

    def test_08_balanced_ml_comments(self, text: str):
        _assert_balanced_tokens(text, "(*", "*)")

    def test_09_native_theory_declaration_and_begin(self, text: str):
        lines = text.lstrip().splitlines()
        assert lines[0] == "theory methode_spectral"
        header = "\n".join(lines[:4])
        assert re.search(
            r'^theory methode_spectral\n\s+imports Complex_Main '
            r'"HOL-Computational_Algebra\.Primes"\nbegin$',
            header,
            flags=re.MULTILINE,
        )

    def test_10_theory_ends_with_end(self, text: str):
        assert text.rstrip().splitlines()[-1].strip() == "end"

    def test_11_all_section_xiii_subsections_present(self, text: str):
        expected = (
            'subsection "XIII.1 ',
            'subsection "XIII.2 ',
            'subsection "XIII.2.b ',
            'subsection "XIII.3 ',
            'subsection "XIII.4 ',
            'subsection "XIII.4.b ',
            'subsection "XIII.5 ',
            'subsection "XIII.6 ',
        )
        missing = [marker for marker in expected if marker not in text]
        assert not missing, f"Sous-sections XIII manquantes : {missing}"

    def test_12_key_section_xiii_lemmas_and_theorems_intact(self, text: str):
        expected = (
            "psi_savard_at_49_228_expanded",
            "rapport_zeta_savard_at_10",
            "rapport_zeta_savard_at_25",
            "rapport_zeta_savard_at_49",
            "methode_spectrale_exclusivite_P",
            "RsP_universel_entier_naturel",
            "synthese_pont_savard",
            "ensemble_savard_satisfaisable",
        )
        for name in expected:
            declarations = re.findall(rf"^(?:lemma|theorem)\s+{re.escape(name)}\s*:", text, re.MULTILINE)
            assert len(declarations) == 1, f"Declaration {name!r}: attendu 1, trouve {len(declarations)}"

    def test_13_v342_markers_present(self, text: str):
        expected = (
            "-0.7981841",
            "-100.7981582",
            "ref v3.34",
            "Ensemble = 1",
            "version enrichie v3.42",
            'subsection "XIII.2.b ',
            'subsection "XIII.4.b ',
        )
        missing = [marker for marker in expected if marker not in text]
        assert not missing, f"Marqueurs v3.42 manquants : {missing}"

    def test_14_v342_table_has_eight_plus_one_validations(self, text: str):
        start = text.index("TABLE COMPLETE DES VALIDATIONS NUMERIQUES")
        end = text.index("Les 4 lignes negatives", start)
        table = text[start:end]
        rows = re.findall(r"^\s*\|\s*[+-]\s*\|", table, re.MULTILINE)
        assert len(rows) == 9, f"Table v3.42 : 9 validations attendues, {len(rows)} trouvees"
        assert len(re.findall(r"^\s*\|\s*\+\s*\|", table, re.MULTILINE)) == 4
        assert len(re.findall(r"^\s*\|\s*-\s*\|", table, re.MULTILINE)) == 5
        assert table.count("(*ref v3.34*)") == 1

    def test_15_static_structure_parser_has_no_blocking_error(self):
        report = vts.verify_file(THY_PATH, fix=False)
        assert report.passes_run == [
            "structure", "unicode", "mojibake", "tactique", "whitespace"
        ]
        assert not report.errors, [issue.message for issue in report.errors]
