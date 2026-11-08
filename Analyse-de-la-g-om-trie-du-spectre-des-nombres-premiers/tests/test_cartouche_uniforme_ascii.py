"""
Tests v3.26 : verifie l'uniformisation des cartouches Isabelle en style ASCII.

Bug reporte par Philippe le 2026-07-09 (log GitHub Actions) :
  *** Malformed command syntax
  *** At command '<malformed>' (line 2455 of 'methode_spectral.thy')

Cause : la Section XI (validation#16, ajoutee par Philippe le 2026-06-29)
utilisait des cartouches Unicode directs ('‹...›') alors que le reste du
fichier utilisait le style ASCII ('\\<open>...\\<close>'). En mode
'isabelle build' batch (headless CI), les cartouches Unicode multilignes
peuvent poser probleme au parser.

Correction : uniformisation de TOUS les cartouches en style ASCII
(\\<open>/\\<close>) pour maximiser la compatibilite avec les 3
frontends Isabelle : jEdit, batch build, VSCode extension.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="module")
def thy_content() -> str:
    return (ROOT / "theories" / "methode_spectral.thy").read_text(encoding="utf-8")


class TestUniformCartoucheStyle:
    """Regression : les cartouches doivent etre uniformement en style ASCII."""

    def test_no_unicode_open_cartouche(self, thy_content):
        assert '\u2039' not in thy_content, (
            "Cartouche Unicode ouvrant '‹' (U+2039) detecte. "
            "Utiliser '\\<open>' pour compatibilite build headless."
        )

    def test_no_unicode_close_cartouche(self, thy_content):
        assert '\u203a' not in thy_content, (
            "Cartouche Unicode fermant '›' (U+203A) detecte. "
            "Utiliser '\\<close>' pour compatibilite build headless."
        )

    def test_cartouche_ascii_balance(self, thy_content):
        n_open = thy_content.count(r"\<open>")
        n_close = thy_content.count(r"\<close>")
        assert n_open == n_close, (
            f"Desequilibre cartouches ASCII : {n_open} '\\<open>' "
            f"vs {n_close} '\\<close>'"
        )

    def test_at_least_60_cartouches(self, thy_content):
        """Le fichier doit contenir >= 60 pairs de cartouches (validation#16
        + code precedent)."""
        n_open = thy_content.count(r"\<open>")
        assert n_open >= 60, (
            f"Nombre de cartouches trop faible ({n_open}). "
            f"Attendu >= 60 apres validation#16."
        )


class TestIsabelleParserCompatibility:
    """Simulation d'une passe parser Isabelle basique."""

    def test_starts_with_theory(self, thy_content):
        # Isabelle autorise des commentaires (* ... *) avant `theory` (bloc
        # d'en-tete metadata). On retire le premier bloc de commentaire s'il
        # precede immediatement le mot-cle theory.
        import re
        stripped = thy_content.lstrip()
        stripped = re.sub(r"^\(\*.*?\*\)\s*", "", stripped, count=1, flags=re.DOTALL)
        assert stripped.startswith("theory "), (
            "Le fichier doit commencer par 'theory <nom>' (apres un eventuel "
            "commentaire d'en-tete)"
        )

    def test_ends_with_end(self, thy_content):
        assert thy_content.rstrip().endswith("end"), (
            "Le fichier doit se terminer par 'end'"
        )

    def test_has_begin_after_imports(self, thy_content):
        import re
        m = re.search(
            r"^theory\s+\w+\s*\n\s*imports\s+.+?\n\s*begin\b",
            thy_content, re.MULTILINE | re.DOTALL,
        )
        assert m is not None, (
            "Bloc 'theory X imports Y begin' malforme"
        )

    def test_proof_qed_balance(self, thy_content):
        import re
        n_proof = len(re.findall(r"^\s*proof\b", thy_content, re.MULTILINE))
        n_qed = len(re.findall(r"^\s*qed\b", thy_content, re.MULTILINE))
        assert n_proof == n_qed, (
            f"Desequilibre proof/qed : {n_proof} vs {n_qed}"
        )

    def test_comment_balance(self, thy_content):
        n_open = thy_content.count("(*")
        n_close = thy_content.count("*)")
        assert n_open == n_close, (
            f"Desequilibre commentaires : {n_open} '(*' vs {n_close} '*)'"
        )


class TestFileEncodingClean:
    """Regression : fichier UTF-8 propre sans BOM ni caracteres invisibles."""

    def test_no_bom(self, thy_content):
        assert not thy_content.startswith("\ufeff")

    @pytest.mark.parametrize("invisible,name", [
        ("\u200b", "ZERO-WIDTH SPACE"),
        ("\u200c", "ZERO-WIDTH NON-JOINER"),
        ("\u200d", "ZERO-WIDTH JOINER"),
        ("\u2028", "LINE SEPARATOR"),
        ("\u2029", "PARAGRAPH SEPARATOR"),
    ])
    def test_no_invisible_chars(self, thy_content, invisible, name):
        assert invisible not in thy_content, (
            f"Caractere invisible {name} detecte"
        )

    def test_no_mojibake(self, thy_content):
        mojibake_seqs = ["â€¹", "â€º", "â‰¥", "â‡'", "â„™", "Ã©", "Ã¨"]
        for m in mojibake_seqs:
            assert m not in thy_content, (
                f"Mojibake residuel '{m}'"
            )


class TestSectionXIValidation16Preserved:
    """Verifie que les 9 definitions Savard validation#16 sont bien preservees
    apres la conversion cartouches."""

    @pytest.mark.parametrize("name", [
        "raison_spectrale", "progression_simple_terme",
        "avant_dernier_terme_savard", "dernier_terme_savard",
        "suite_A_savard_construction", "suite_B_savard_construction",
        "somme_A_compacte_savard", "somme_B_compacte_savard",
        "rapport_spectral_total_savard",
    ])
    def test_definition_still_present(self, thy_content, name):
        assert f"definition {name}" in thy_content

    def test_section_XI_still_present(self, thy_content):
        assert "Section XI" in thy_content

    def test_text_blocks_use_ascii(self, thy_content):
        """Les blocs 'text' de la Section XI utilisent maintenant
        \\<open>...\\<close> (ASCII), pas ‹...› (Unicode)."""
        import re
        # Il doit y avoir des 'text \<open>' apres la ligne 2400
        # (Section XI commence vers 2440-2455)
        after_2400 = "\n".join(thy_content.splitlines()[2400:])
        assert r"text \<open>" in after_2400, (
            "La Section XI doit avoir des 'text \\<open>' ASCII"
        )
        assert "text ‹" not in after_2400, (
            "Aucun 'text ‹' Unicode ne doit subsister"
        )


class TestNoUnicodeIsabelleSymbols:
    """v3.27b : regression du bug 'Inner lexical error' sur ligne 2465
    (build GitHub Actions 2026-07-10). Isabelle 2024 en mode batch refuse
    les symboles Unicode dans les declarations de types et d'expressions
    (=>, >=, <=, forall, exists, etc.). Il faut utiliser les tokens ASCII
    \\<Rightarrow>, \\<ge>, \\<le>, \\<forall>, etc."""

    @pytest.fixture(scope="class")
    def thy(self):
        return (Path("/app/agent-multiloop-Gabriel-local") / "theories" /
                "methode_spectral.thy").read_text(encoding="utf-8")

    @pytest.mark.parametrize("unicode_sym,ascii_token", [
        ("\u21d2", r"\<Rightarrow>"),   # =>
        ("\u2265", r"\<ge>"),           # >=
        ("\u2264", r"\<le>"),           # <=
        ("\u2260", r"\<noteq>"),        # !=
        ("\u2119", r"\<P>"),            # P majuscule ajoure
        ("\u2200", r"\<forall>"),
        ("\u2203", r"\<exists>"),
        ("\u2227", r"\<and>"),
        ("\u2228", r"\<or>"),
        ("\u00ac", r"\<not>"),
        ("\u2208", r"\<in>"),
        ("\u27f9", r"\<Longrightarrow>"),
    ])
    def test_no_unicode_symbol(self, thy, unicode_sym, ascii_token):
        assert unicode_sym not in thy, (
            f"Symbole Unicode Isabelle '{unicode_sym}' (U+{ord(unicode_sym):04X}) "
            f"detecte. Utiliser '{ascii_token}' (ASCII) pour compatibilite "
            f"batch build."
        )
