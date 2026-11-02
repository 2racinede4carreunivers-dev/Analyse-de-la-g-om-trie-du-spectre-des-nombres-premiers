from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import valider_primalite_ancres as validator  # noqa: E402


def test_parse_unique_anchor() -> None:
    row = validator.parse_report_line(
        "  1/28000006 | 17 | 17 | UNIQUE | A(8)-=17\n", 4
    )

    assert row is not None
    assert row.report_id == "1/28000006"
    assert row.values == ["17"]
    assert row.errors == []


def test_parse_ambiguous_checks_every_branch() -> None:
    row = validator.parse_report_line(
        "  1/28000001 | - | - | AMBIGU | A(8)-=17, A(7)+=19\n", 4
    )

    assert row is not None
    assert row.values == ["17", "19"]
    assert row.errors == []


def test_truncated_unique_row_keeps_numeric_anchor_and_reports_error() -> None:
    row = validator.parse_report_line(
        "  1/77293103 | 23 | 23 | UNIQUE | A(\n", 4
    )

    assert row is not None
    assert row.values == ["23"]
    assert row.errors


def test_validation_writes_top_and_bottom_scores_and_audit(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    audit = tmp_path / "audit.jsonl"
    report = tmp_path / "annotated.txt"
    source.write_text(
        "% title\n% columns\n% separator\n"
        "1/1 | 17 | 17 | UNIQUE | A(8)-=17\n"
        "1/2 | - | - | AMBIGU | A(8)-=21, A(7)+=19\n",
        encoding="utf-8",
    )

    def fake_gp(_executable: str, values: list[str], _timeout: float) -> list[bool]:
        return [value in {"17", "19"} for value in values]

    with patch.object(validator, "run_gp_batch", side_effect=fake_gp):
        stats = validator.validate_report(
            source, audit, report, "fake-gp", batch_size=2, log_every=10
        )

    assert stats.report_rows == 2
    assert stats.candidates == stats.verified == 3
    assert stats.prime == 2
    assert stats.composite == 1
    assert stats.invalid_rows == 0
    assert stats.complete
    assert stats.prime_percent == pytest.approx(200 / 3)

    annotated = report.read_text(encoding="utf-8")
    assert "VALIDATION DE PRIMALITE — DEBUT" in annotated
    assert "VALIDATION DE PRIMALITE — FIN" in annotated
    assert "Composes / fausses ancres   : 1" in annotated
    records = [json.loads(line) for line in audit.read_text(encoding="utf-8").splitlines()]
    assert [record["anchor"] for record in records] == ["17", "21", "19"]
    assert [record["result"] for record in records] == [
        "PREMIER_DEMONTRE",
        "COMPOSE",
        "PREMIER_DEMONTRE",
    ]


def test_malformed_row_prevents_integral_success(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    audit = tmp_path / "audit.jsonl"
    report = tmp_path / "annotated.txt"
    source.write_text(
        "% title\n% columns\n% separator\n"
        "1/1 | 17 | 17 | UNIQUE | A(\n",
        encoding="utf-8",
    )

    with patch.object(validator, "run_gp_batch", return_value=[True]):
        stats = validator.validate_report(source, audit, report, "fake-gp")

    assert stats.candidates == stats.verified == 1
    assert stats.invalid_rows == 1
    assert not stats.complete
    assert "Validation integrale        : NON" in report.read_text(encoding="utf-8")


def test_resume_skips_only_matching_completed_audit_records(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    audit = tmp_path / "audit.jsonl"
    report = tmp_path / "annotated.txt"
    source.write_text(
        "% title\n% columns\n% separator\n"
        "1/1 | 17 | 17 | UNIQUE | A(8)-=17\n"
        "1/2 | - | - | AMBIGU | A(8)-=21, A(7)+=19\n",
        encoding="utf-8",
    )
    audit.with_name(audit.name + ".partial").write_text(
        json.dumps(
            {
                "line": 4,
                "report": "1/1",
                "status": "UNIQUE",
                "anchor": "17",
                "result": "PREMIER_DEMONTRE",
                "method": "PARI/GP isprime",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    def fake_gp(_executable: str, values: list[str], _timeout: float) -> list[bool]:
        assert values == ["21", "19"]
        return [False, True]

    with patch.object(validator, "run_gp_batch", side_effect=fake_gp):
        stats = validator.validate_report(
            source, audit, report, "fake-gp", batch_size=10, resume=True
        )

    assert stats.complete
    assert stats.candidates == stats.verified == 3
    assert stats.prime == 2
    assert stats.composite == 1
    assert audit.exists()


def test_timed_out_batch_is_split_to_smaller_batches(tmp_path: Path) -> None:
    source = tmp_path / "source.txt"
    audit = tmp_path / "audit.jsonl"
    report = tmp_path / "annotated.txt"
    source.write_text(
        "% title\n% columns\n% separator\n"
        "1/1 | - | - | AMBIGU | A(8)-=17, A(7)+=19\n",
        encoding="utf-8",
    )

    def fake_gp(_executable: str, values: list[str], _timeout: float) -> list[bool]:
        if len(values) > 1:
            raise validator.subprocess.TimeoutExpired("fake-gp", _timeout)
        return [True]

    with patch.object(validator, "run_gp_batch", side_effect=fake_gp):
        stats = validator.validate_report(
            source, audit, report, "fake-gp", batch_size=2
        )

    assert stats.complete
    assert stats.candidates == stats.verified == 2
    assert stats.prime == 2
