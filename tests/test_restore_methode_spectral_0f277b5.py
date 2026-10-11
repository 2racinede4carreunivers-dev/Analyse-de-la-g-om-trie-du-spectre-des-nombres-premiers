"""Régression de la restauration bit-perfect depuis le commit 0f277b5."""
from __future__ import annotations

import hashlib
import subprocess
import unicodedata
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GIT_ROOT = ROOT.parent
THY_PATH = ROOT / "theories" / "methode_spectral.thy"
REPO_PATH = "agent-multiloop-Gabriel-local/theories/methode_spectral.thy"
EXPECTED_SHA256 = "ad1cecfc417e797341c6bc3796bb60103712df6fac0773e5c9808db2e811880d"


@pytest.fixture(scope="module")
def raw() -> bytes:
    return THY_PATH.read_bytes()


@pytest.fixture(scope="module")
def text(raw: bytes) -> str:
    return raw.decode("utf-8", errors="strict")


def _git_blob(commit: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(GIT_ROOT), "show", f"{commit}:{REPO_PATH}"],
        check=True,
        capture_output=True,
    ).stdout


# Identité binaire et métadonnées exactes de la restauration.
def test_exact_binary_identity_with_both_reference_commits(raw: bytes):
    assert raw == _git_blob("0f277b5")
    assert raw == _git_blob("7777f63")


def test_exact_size_hash_and_line_count(raw: bytes, text: str):
    assert len(raw) == 172_896
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
    assert raw.count(b"\n") == 4_276
    assert len(text.splitlines()) == 4_276
    assert raw.endswith(b"\n")


# Encodage Unicode propre, normalisé et sans octets/caractères interdits.
def test_utf8_nfc_without_bom_cr_nul_or_controls(raw: bytes, text: str):
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in raw
    assert b"\x00" not in raw
    assert unicodedata.normalize("NFC", text) == text
    controls = [
        (index, ord(char), unicodedata.name(char, "UNKNOWN"))
        for index, char in enumerate(text)
        if unicodedata.category(char) == "Cc" and char != "\n"
    ]
    assert not controls, controls[:10]


def test_no_known_mojibake_or_replacement_character(text: str):
    bad_sequences = (
        "\ufffd", "Ã©", "Ã¨", "Ãª", "Ãà", "Ã§", "Â ",
        "â€™", "â€˜", "â€œ", "â€�", "â€“", "â€”", "â‰¥", "â‰¤", "â‡’",
    )
    found = [sequence for sequence in bad_sequences if sequence in text]
    assert not found, found


# Enveloppe Isabelle, délimiteurs et contenu fonctionnel clé.
def test_exact_balanced_delimiter_counts(text: str):
    assert text.count(r"\<open>") == 105
    assert text.count(r"\<close>") == 105
    assert text.count("(*") == 380
    assert text.count("*)") == 380


def test_theory_envelope_and_imports(text: str):
    nonempty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    assert nonempty_lines[0] == "theory methode_spectral"
    assert nonempty_lines[-1] == "end"
    assert 'imports Complex_Main "HOL-Computational_Algebra.Primes"' in text


def test_sections_xiii_and_v343_are_preserved(text: str):
    assert "Section XIII" in text
    assert 'section "Blocs A_k / B_k et rapport spectral de blocs (v3.43)"' in text
    for subsection in (
        "XIII.1", "XIII.2", "XIII.2.b", "XIII.3",
        "XIII.4", "XIII.4.b", "XIII.5", "XIII.6",
    ):
        assert f'subsection "{subsection} ' in text


def test_v3451_numeral_fix_is_preserved(text: str):
    assert text.count("numeral_2_eq_2") >= 3
    assert "by (simp add: bloc_B_k_def numeral_2_eq_2)" in text
    assert "by (simp add: somme_bloc_def bloc_B_k_def numeral_2_eq_2)" in text
    assert (
        "by (simp add: RsP_bloc_extreme_def somme_bloc_def "
        "bloc_B_k_def numeral_2_eq_2)"
    ) in text
