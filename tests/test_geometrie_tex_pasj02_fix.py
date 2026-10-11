"""Régressions statiques du correctif pasj02/MiKTeX de l'Avant-Propos."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEX_PATH = ROOT / "theories" / "tex" / "geometrie_gabriel_savard_13.tex"
EXPECTED_BIB_KEYS = (
    "Riemann1859",
    "Tchebychev1852",
    "HardyWright1979",
    "Davenport2000",
    "Titchmarsh1986",
    "Nipkow2002",
    "Isabelle2024",
    "Savard2026a",
    "Savard2026b",
    "Savard2026c",
)
GITHUB_URL = "https://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel"


@pytest.fixture(scope="module")
def tex_bytes() -> bytes:
    return TEX_PATH.read_bytes()


@pytest.fixture(scope="module")
def tex(tex_bytes: bytes) -> str:
    return tex_bytes.decode("utf-8", errors="strict")


def _without_comments(source: str) -> str:
    r"""Retire les commentaires TeX tout en conservant les \% échappés."""
    clean_lines = []
    for line in source.splitlines():
        for index, char in enumerate(line):
            if char != "%":
                continue
            preceding_backslashes = 0
            cursor = index - 1
            while cursor >= 0 and line[cursor] == "\\":
                preceding_backslashes += 1
                cursor -= 1
            if preceding_backslashes % 2 == 0:
                line = line[:index]
                break
        clean_lines.append(line)
    return "\n".join(clean_lines)


def _count_unescaped(source: str, token: str) -> int:
    count = 0
    for index, char in enumerate(source):
        if char != token:
            continue
        preceding_backslashes = 0
        cursor = index - 1
        while cursor >= 0 and source[cursor] == "\\":
            preceding_backslashes += 1
            cursor -= 1
        if preceding_backslashes % 2 == 0:
            count += 1
    return count


def test_utf8_strict_clean_nfc(tex_bytes: bytes, tex: str) -> None:
    """Le source reste portable entre MiKTeX et Overleaf."""
    assert not tex_bytes.startswith(b"\xef\xbb\xbf"), "BOM UTF-8 détecté"
    assert b"\r" not in tex_bytes, "CR/CRLF détecté"
    assert b"\x00" not in tex_bytes, "Octet NUL détecté"
    controls = [
        (index, char)
        for index, char in enumerate(tex)
        if unicodedata.category(char) == "Cc" and char not in {"\n", "\t"}
    ]
    assert not controls, f"Caractères de contrôle détectés : {controls[:5]}"
    assert unicodedata.normalize("NFC", tex) == tex, "Le fichier n'est pas en NFC"
    for marker in ("\ufffd", "Ã", "Â", "â€", "ðŸ"):
        assert marker not in tex, f"Mojibake probable détecté : {marker!r}"


def test_document_boundaries_and_delimiters(tex: str) -> None:
    clean = _without_comments(tex)
    commands = [line.strip() for line in clean.splitlines() if line.strip()]
    assert commands[0] == r"\documentclass[]{pasj02}"
    assert tex.rstrip().endswith(r"\end{document}")

    depth = 0
    for index, char in enumerate(clean):
        if char not in "{}":
            continue
        if _count_unescaped(clean[: index + 1], char) == _count_unescaped(
            clean[:index], char
        ):
            continue
        depth += 1 if char == "{" else -1
        assert depth >= 0, f"Accolade fermante sans ouverture à l'index {index}"
    assert depth == 0, f"Accolades déséquilibrées : profondeur finale {depth}"
    assert _count_unescaped(clean, "$") % 2 == 0, "Nombre impair de délimiteurs $"



def test_file_length_and_size_after_duplicate_removal(tex_bytes: bytes, tex: str) -> None:
    """v3.45 : la suppression du bloc orphelin + extension des macros unnumbered
    (subsection/subsubsection) et le remplacement des starred sections en
    appendice conservent une taille raisonnable proche de 1099 lignes."""
    assert 1080 <= len(tex.splitlines()) <= 1120
    assert 44_000 <= len(tex_bytes) <= 46_000


def test_single_active_document_and_bibliography_boundaries(tex: str) -> None:
    """Le document et sa bibliographie n'ont chacun qu'une paire de bornes."""
    clean = _without_comments(tex)
    commands = [line.strip() for line in clean.splitlines() if line.strip()]
    assert clean.count(r"\begin{document}") == 1
    assert clean.count(r"\end{document}") == 1
    assert clean.count(r"\begin{thebibliography}") == 1
    assert clean.count(r"\end{thebibliography}") == 1
    assert commands[-1] == r"\end{document}"
    assert tex.splitlines()[-1] == r"\end{document}"


def test_bibliography_has_ten_unique_expected_keys_and_full_urls(tex: str) -> None:
    """Les dix références attendues sont uniques et les URL GitHub non tronquées."""
    clean = _without_comments(tex)
    bibliography = clean.split(r"\begin{thebibliography}{}", maxsplit=1)[1].split(
        r"\end{thebibliography}", maxsplit=1
    )[0]
    keys = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}", bibliography)
    assert keys == list(EXPECTED_BIB_KEYS)
    assert len(keys) == len(set(keys)) == 10
    assert bibliography.count(GITHUB_URL) == 2
    assert all(
        r"\url{" + GITHUB_URL + "}" in bibliography.split(
            rf"\bibitem[Savard(2026{suffix})]{{Savard2026{suffix}}}", maxsplit=1
        )[1]
        for suffix in ("a", "b")
    )


def test_all_labels_are_unique(tex: str) -> None:
    """Les 82 labels actifs sont uniques, notamment celui des perspectives."""
    clean = _without_comments(tex)
    labels = re.findall(r"\\label\{([^{}]+)\}", clean)
    assert len(labels) == 82
    assert len(labels) == len(set(labels))
    assert labels.count("ssec:perspectives") == 1


def test_perspectives_and_acknowledgements_are_intact(tex: str) -> None:
    clean = _without_comments(tex)
    perspective_start = clean.index(r"\subsection{Perspectives}")
    perspective_end = clean.index(r"\end{itemize}", perspective_start)
    perspectives = clean[perspective_start:perspective_end]
    for fragment in (
        "suites de 1 à 7 termes",
        "suites négatives et mixtes",
        "convergence asymptotique",
        "Publication et soumission",
    ):
        assert fragment in perspectives

    ack_match = re.search(r"\\begin\{ack\}(.*?)\\end\{ack\}", clean, re.DOTALL)
    assert ack_match is not None
    acknowledgements = ack_match.group(1)
    for fragment in ("Copilot", "E1", "Gordon", "Gabriel"):
        assert fragment in acknowledgements


def test_unnumberedsection_macro_is_complete_and_in_preamble(tex: str) -> None:
    macro_start = tex.index(r"\newcommand{\unnumberedsection}")
    document_start = tex.index(r"\begin{document}")
    makeatletter = tex.rfind(r"\makeatletter", 0, macro_start)
    makeatother = tex.find(r"\makeatother", macro_start)
    assert 0 <= makeatletter < macro_start < makeatother < document_start

    macro_block = tex[macro_start:makeatother]
    for required in (
        r"\phantomsection",
        r"\addcontentsline{toc}{section}{#1}",
        r"\Large\bfseries",
        r"\@afterheading",
    ):
        assert required in macro_block, f"Élément absent de la macro : {required}"


def test_first_two_starred_sections_are_replaced(tex: str) -> None:
    """v3.45 : Avant-Propos utilise \\unnumberedsection ; les \\section*
    residuels d'appendice sont AUSSI convertis pour eviter les crashes
    pasj02 potentiels (5 invocations totales : 2 Avant-Propos + 3 appendice)."""
    clean = _without_comments(tex)
    invocations = re.findall(r"\\unnumberedsection\{[^\n]+\}", clean)
    assert len(invocations) >= 2, f"attendu >=2 unnumberedsection, obtenu {len(invocations)}"
    assert r"\section*{Note liminaire}" not in clean
    assert r"\section*{Avant-Propos" not in clean
    assert clean.count(r"\unnumberedsection{Note liminaire}") == 1
    assert clean.count(
        r"\unnumberedsection{Avant-Propos --- La Chair Première Géométrique}"
    ) == 1

    lines = clean.splitlines()
    note_line = next(
        index for index, line in enumerate(lines, start=1)
        if r"\unnumberedsection{Note liminaire}" in line
    )
    foreword_line = next(
        index for index, line in enumerate(lines, start=1)
        if r"\unnumberedsection{Avant-Propos" in line
    )
    assert 150 <= note_line <= 200
    assert note_line < foreword_line <= 210
    assert not any(r"\section*" in line for line in lines[144:210])


def test_no_problematic_section_pattern_after_abstract(tex: str) -> None:
    clean = _without_comments(tex)
    after_abstract = clean.split(r"\end{abstract}", maxsplit=1)[1]
    first_30_lines = "\n".join(after_abstract.splitlines()[:30])
    assert r"\section*" not in first_30_lines
    assert not re.search(
        r"\\section\*\{[^}]+\}\s*\\addcontentsline",
        first_30_lines,
        flags=re.DOTALL,
    )
    assert r"\unnumberedsection{Note liminaire}" in first_30_lines
    assert r"\unnumberedsection{Avant-Propos" in first_30_lines


def test_integral_foreword_content_is_preserved(tex: str) -> None:
    start = tex.index(r"\unnumberedsection{Note liminaire}")
    end = tex.index(r"\section{Fondements et Architecture", start)
    foreword = tex[start:end].replace("~", " ")
    required_fragments = (
        "Perelman",
        "MK 39",
        "Apocalypse Now",
        "Royal Victoria",
        "aqueduc",
        "Université Laval",
        "élite universitaire",
        "biais algorithmique",
        "haine",
        "L'Univers est au Carré",
        "Mme Gabriel",
        "v0.9.1 (HOL-corrigé)",
        "20 juillet 2026",
        "Lévis, Chaudière-Appalaches",
    )
    flattened = re.sub(r"[{}]", "", foreword)
    for fragment in required_fragments:
        assert fragment in flattened, f"Contenu de l'Avant-Propos absent : {fragment}"
