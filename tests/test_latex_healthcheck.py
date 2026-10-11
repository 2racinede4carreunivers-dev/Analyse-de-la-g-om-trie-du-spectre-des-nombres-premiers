"""Healthcheck statique du document LaTeX principal genere depuis le DOCX."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TEX_PATH = ROOT / "theories" / "tex" / "Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.tex"


@pytest.fixture(scope="module")
def raw() -> bytes:
    return TEX_PATH.read_bytes()


@pytest.fixture(scope="module")
def text(raw: bytes) -> str:
    return raw.decode("utf-8", errors="strict")


class TestLatexHealthcheck:
    def test_01_file_exists(self):
        assert TEX_PATH.exists(), f"Fichier introuvable: {TEX_PATH}"

    def test_02_no_utf8_bom(self, raw: bytes):
        assert not raw.startswith(b"\xef\xbb\xbf"), "BOM UTF-8 detecte"

    def test_03_strict_utf8_decode_roundtrip(self, raw: bytes, text: str):
        assert text.encode("utf-8") == raw

    def test_04_no_nul_byte(self, raw: bytes):
        assert b"\x00" not in raw, "Octet NUL detecte"

    def test_05_lf_only(self, raw: bytes):
        assert b"\r\n" not in raw, "Fins de ligne CRLF detectees"
        assert b"\r" not in raw, "Caractere CR detecte"

    def test_06_required_packages_present(self, text: str):
        required = (
            r"\\usepackage[utf8]{inputenc}",
            r"\\usepackage[T1]{fontenc}",
            r"\\usepackage[french]{babel}",
            r"\\usepackage{hyperref}",
            r"\\usepackage{longtable}",
            r"\\usepackage{newunicodechar}",
        )
        for marker in required:
            assert marker in text, f"Package manquant: {marker}"

    def test_07_balanced_braces_ignoring_escapes(self, text: str):
        depth = 0
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == "\\":
                i += 2
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                assert depth >= 0, "Accolade fermante sans ouverture"
            i += 1
        assert depth == 0, f"Accolades desequilibrees: profondeur finale={depth}"

    def test_08_balanced_environments(self, text: str):
        begin_iter = re.finditer(r"\\begin\{([^{}]+)\}", text)
        end_iter = re.finditer(r"\\end\{([^{}]+)\}", text)
        events = []
        for m in begin_iter:
            events.append((m.start(), "begin", m.group(1)))
        for m in end_iter:
            events.append((m.start(), "end", m.group(1)))
        events.sort(key=lambda item: item[0])

        stack: list[str] = []
        for _, kind, name in events:
            if kind == "begin":
                stack.append(name)
            else:
                assert stack, f"\\end{{{name}}} sans \\begin"
                top = stack.pop()
                assert top == name, f"Environnement ferme={name} attendu={top}"
        assert not stack, f"Environnements non fermes: {stack[:10]}"

    def test_09_unicode_symbols_are_declared(self, text: str):
        used = {ord(ch) for ch in text if ord(ch) > 255}
        declared = {
            int(code, 16)
            for code in re.findall(r"\\\\DeclareUnicodeCharacter\{([0-9A-Fa-f]+)\}", text)
        }
        missing = sorted(code for code in used if code not in declared)
        assert not missing, f"Unicode sans mapping DeclareUnicodeCharacter: {missing}"

    def test_10_document_structure_markers(self, text: str):
        assert "\\begin{document}" in text
        assert "\\tableofcontents" in text
        assert "\\end{document}" in text

    def test_11_expected_density(self, text: str):
        section_like = len(re.findall(r"^\\\\(?:sub)*section\{", text, flags=re.MULTILINE))
        tables = text.count("\\begin{longtable}")
        items = len(re.findall(r"^\\\\item ", text, flags=re.MULTILINE))

        assert section_like >= 50, f"Sections insuffisantes: {section_like}"
        assert tables >= 37, f"Tableaux insuffisants: {tables}"
        assert items >= 33, f"Items de liste insuffisants: {items}"
