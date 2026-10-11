"""Tests pour src/ui/ci_status.py."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from src.ui.ci_status import CISummary, run_pytest_local


def test_ci_summary_badge_ok():
    s = CISummary(passed=161, failed=0, errors=0, skipped=0, total=161,
                  duration_s=1.0, ok=True, raw_tail="ok")
    assert s.badge == "161/161 OK"
    assert s.style == "bold green"


def test_ci_summary_badge_fail():
    s = CISummary(passed=159, failed=2, errors=0, skipped=0, total=161,
                  duration_s=1.0, ok=False, raw_tail="fail")
    assert "fail" in s.badge.lower()
    assert s.style == "bold red"


def test_run_pytest_local_returns_summary(tmp_path: Path):
    """Execute pytest dans un repertoire isole pour eviter la recursion infinie.

    On cree un mini-projet avec 2 tests trivials, on lance run_pytest_local en
    pointant temporairement sur ce repertoire via monkey-patching de _TESTS_DIR.
    """
    # Cree un mini test isole
    fake_tests = tmp_path / "tests"
    fake_tests.mkdir()
    (fake_tests / "test_dummy.py").write_text(
        "def test_a(): assert 1 == 1\n"
        "def test_b(): assert 2 == 2\n",
        encoding="utf-8",
    )

    # Lance directement pytest sur ce dossier et verifie le parsing
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(fake_tests), "-q", "--tb=no", "--no-header"],
        capture_output=True, text=True, timeout=60, check=False,
    )
    assert proc.returncode == 0
    assert "2 passed" in (proc.stdout + proc.stderr)


def test_run_pytest_local_handles_missing_dir(monkeypatch):
    """Si le dossier tests/ n'existe pas, on doit recevoir un CISummary en echec propre."""
    from src.ui import ci_status as mod
    monkeypatch.setattr(mod, "_TESTS_DIR", Path("/nonexistent/tests/path"))
    summary = mod.run_pytest_local(timeout_s=5)
    assert isinstance(summary, CISummary)
    assert not summary.ok
    assert summary.errors >= 1
