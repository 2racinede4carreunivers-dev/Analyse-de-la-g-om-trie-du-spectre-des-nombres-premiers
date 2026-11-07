"""
Tests du script `theories/verify_thy_structure.py`.

Verifie que l'autocorrecteur :
  1. Detecte correctement les problemes (unicode hors zone, mojibake, tactiques risquees,
     structure desequilibree, whitespace).
  2. Corrige effectivement les problemes safe en mode --fix.
  3. Preserve les zones text/comment/string (l'UTF-8 y est autorise).
  4. Renvoie les bons exit codes (0/1/2) et un JSON structure exploitable en CI.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

# On importe le module directement pour tester les fonctions unitaires
ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "theories" / "verify_thy_structure.py"
sys.path.insert(0, str(ROOT / "theories"))
import verify_thy_structure as vts  # noqa: E402


# =====================================================================
# FIXTURES
# =====================================================================


@pytest.fixture
def tmp_thy(tmp_path: Path):
    """Retourne une fabrique de fichiers .thy temporaires."""
    def _make(content: str, name: str = "test.thy") -> Path:
        p = tmp_path / name
        p.write_text(content, encoding="utf-8")
        return p
    return _make


# =====================================================================
# PASSE 1 : STRUCTURE
# =====================================================================


class TestStructure:

    def test_balanced_proof_qed_passes(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True" proof - show ?thesis by simp qed\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        assert not report.errors, [i.message for i in report.errors]

    def test_unbalanced_proof_qed_detected(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True" proof - show ?thesis by simp\n'   # missing qed
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        errs = [i.message for i in report.errors if "proof/qed" in i.message]
        assert errs, "Un desequilibre proof/qed doit etre signale comme erreur"

    def test_unbalanced_cartouches_detected(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'text \\<open>Un texte sans close\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        errs = [i.message for i in report.errors if "cartouches" in i.message]
        assert errs, "Un desequilibre \\<open>/\\<close> doit etre signale"


# =====================================================================
# PASSE 2 : UNICODE
# =====================================================================


class TestUnicode:

    def test_unicode_in_text_block_is_allowed(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'text \\<open>Ceci contient des accents : é è à ç ω\\<close>\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        unicode_issues = [i for i in report.issues if i.passe == "unicode"]
        assert not unicode_issues, (
            f"L'UTF-8 dans text \\<open>...\\<close> doit etre autorise. "
            f"Detecte a tort : {[i.message for i in unicode_issues]}"
        )

    def test_rightarrow_symbol_flagged_outside_text(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "P \u21d2 Q"\n'   # U+21D2 hors zone texte
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        errs = [i for i in report.errors if i.passe == "unicode"]
        assert errs, "\u21d2 hors text_block doit etre signale comme erreur"
        assert any("\\<Rightarrow>" in i.message for i in errs)

    def test_rightarrow_auto_fixed(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "P \u21d2 Q"\n'
            'end\n'
        )
        p = tmp_thy(content)
        report = vts.verify_file(p, fix=True)
        assert report.fixes_applied >= 1
        new_content = p.read_text(encoding="utf-8")
        assert "\u21d2" not in new_content
        assert "\\<Rightarrow>" in new_content

    def test_all_common_symbols_convertible(self, tmp_thy):
        """Verifie que les symboles Isabelle courants ont tous leur mapping."""
        required = ["\u21d2", "\u2264", "\u2265", "\u2260", "\u2200", "\u2203",
                    "\u2227", "\u2228", "\u2192", "\u2115", "\u211d", "\u2119"]
        for ch in required:
            assert ch in vts.UNICODE_TO_ISABELLE, (
                f"Symbole {ch} (U+{ord(ch):04X}) devrait avoir une conversion Isabelle"
            )

    def test_unknown_unicode_flagged_not_fixable(self, tmp_thy):
        """Un caractere Unicode inconnu doit generer une erreur non-fixable."""
        # Utilise un emoji peu probable d'etre dans la table de conversion
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "P \U0001f600 Q"\n'  # emoji
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=True)
        unknown = [i for i in report.errors if "AUCUNE conversion" in i.message]
        assert unknown, "Unicode inconnu doit etre signale comme non-fixable"


# =====================================================================
# PASSE 3 : MOJIBAKE
# =====================================================================


class TestMojibake:

    def test_mojibake_detected(self, tmp_thy):
        # `é` mal encode devient `Ã©`
        content = (
            'theory Foo imports Main begin\n'
            'text \\<open>Preuve alg\u00c3\u00a9brique valide\\<close>\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        errs = [i for i in report.errors if i.passe == "mojibake"]
        assert errs, "Mojibake \u00c3\u00a9 doit etre detecte comme erreur"

    def test_mojibake_auto_fixed(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'text \\<open>Preuve alg\u00c3\u00a9brique valide\\<close>\n'
            'end\n'
        )
        p = tmp_thy(content)
        vts.verify_file(p, fix=True)
        new_content = p.read_text(encoding="utf-8")
        assert "\u00c3\u00a9" not in new_content, "Mojibake doit avoir ete corrige"
        assert "alg\u00e9brique" in new_content, "Devrait contenir le vrai `algebrique`"


# =====================================================================
# PASSE 4 : TACTIQUES RISQUEES
# =====================================================================


class TestRiskyTactics:

    def test_divide_inverse_flagged(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True" by (simp add: divide_inverse)\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        risky = [i for i in report.warnings if "divide_inverse" in i.message]
        assert risky, "divide_inverse doit etre signale comme risque"

    def test_sorry_flagged(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True"\n'
            '  sorry\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        risky = [i for i in report.warnings if "sorry" in i.message]
        assert risky, "sorry actif doit etre signale"

    def test_sledgehammer_flagged(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True"\n'
            '  sledgehammer\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        risky = [i for i in report.warnings if "sledgehammer" in i.message]
        assert risky

    def test_field_simps_without_witness_flagged(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "1 = 1"\n'
            '  by (simp add: field_simps)\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        warns = [i for i in report.warnings
                 if "field_simps" in i.message and "temoin" in i.message]
        assert warns, "field_simps sans temoin doit etre signale"

    def test_field_simps_with_witness_not_flagged(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True"\n'
            '  assumes h: "x \\<noteq> 0"\n'
            '  shows "y = y"\n'
            '  using h\n'
            '  by (simp add: field_simps)\n'
            'end\n'
        )
        report = vts.verify_file(tmp_thy(content), fix=False)
        warns = [i for i in report.warnings
                 if "field_simps" in i.message and "temoin" in i.message]
        assert not warns, (
            "field_simps avec temoin \\<noteq> 0 ne doit pas etre signale. "
            f"Detecte a tort : {[w.message for w in warns]}"
        )


# =====================================================================
# PASSE 5 : WHITESPACE
# =====================================================================


class TestWhitespace:

    def test_trailing_whitespace_detected(self, tmp_thy):
        content = "theory Foo imports Main begin   \nend\n"
        report = vts.verify_file(tmp_thy(content), fix=False)
        ws = [i for i in report.infos if "Trailing" in i.message]
        assert ws

    def test_trailing_whitespace_auto_fixed(self, tmp_thy):
        content = "theory Foo imports Main begin   \nend   \n"
        p = tmp_thy(content)
        vts.verify_file(p, fix=True)
        new = p.read_text(encoding="utf-8")
        for line in new.splitlines():
            assert line.rstrip() == line, f"Trailing whitespace non nettoye : {line!r}"

    def test_tabs_detected_and_fixed(self, tmp_thy):
        content = "theory Foo imports Main begin\n\tlemma bar: \"True\" by simp\nend\n"
        p = tmp_thy(content)
        report = vts.verify_file(p, fix=True)
        tabs = [i for i in report.issues if "Tab" in i.message]
        assert tabs
        new = p.read_text(encoding="utf-8")
        assert "\t" not in new


# =====================================================================
# CLI + JSON
# =====================================================================


class TestCLI:

    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_help_works(self):
        r = self._run("--help")
        assert r.returncode == 0
        assert "verify_thy_structure" in r.stdout

    def test_json_output_valid(self, tmp_thy):
        content = "theory Foo imports Main begin\nend\n"
        p = tmp_thy(content)
        r = self._run("--file", str(p), "--json")
        assert r.returncode == 0
        payload = json.loads(r.stdout)
        assert "success" in payload
        assert "reports" in payload
        assert len(payload["reports"]) == 1
        assert payload["reports"][0]["total_lines"] > 0

    def test_json_reports_unicode_error_as_dict(self, tmp_thy):
        content = 'theory Foo imports Main begin\nlemma bar: "P \u21d2 Q"\nend\n'
        p = tmp_thy(content)
        r = self._run("--file", str(p), "--json")
        # Sans --fix, le probleme est une erreur -> exit code 1
        assert r.returncode == 1
        payload = json.loads(r.stdout)
        assert payload["reports"][0]["counts"]["errors"] > 0

    def test_strict_mode_returns_1_on_warnings(self, tmp_thy):
        content = (
            'theory Foo imports Main begin\n'
            'lemma bar: "True"\n'
            '  by (simp add: divide_inverse)\n'  # tactique risquee -> warning
            'end\n'
        )
        p = tmp_thy(content)
        r_normal = self._run("--file", str(p))
        r_strict = self._run("--file", str(p), "--strict")
        assert r_normal.returncode == 0, "Sans --strict, warnings non-bloquants"
        assert r_strict.returncode == 1, "Avec --strict, warnings bloquants"


# =====================================================================
# REGRESSION SUR LE FICHIER REEL methode_spectral.thy
# =====================================================================


class TestRealFile:
    """Verifie que methode_spectral.thy passe sans erreur (0 error bloquante)."""

    def test_methode_spectral_no_blocking_errors(self):
        target = ROOT / "theories" / "methode_spectral.thy"
        if not target.exists():
            pytest.skip("methode_spectral.thy absent")
        report = vts.verify_file(target, fix=False)
        assert not report.errors, (
            f"methode_spectral.thy ne doit avoir AUCUNE erreur bloquante. "
            f"Trouve : {[i.message for i in report.errors]}"
        )
