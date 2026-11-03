#!/usr/bin/env python3
"""Validation prouvée des ancrages d'un rapport de reconstruction avec PARI/GP."""

from __future__ import annotations

import argparse
from contextlib import ExitStack
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Sequence


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = PROJECT_ROOT / "reconstruction_k28M_84M_detail.txt"
DEFAULT_AUDIT = PROJECT_ROOT / "reconstruction_k28M_84M_detail_primalite.jsonl"
DEFAULT_REPORT = PROJECT_ROOT / "reconstruction_k28M_84M_detail_primalite.txt"

REPORT_INDEX = re.compile(r"1/\d+\Z")
BRANCH = re.compile(r"A\(\d+\)[+-]=(\d+)")
BRANCH_LIST = re.compile(r"A\(\d+\)[+-]=\d+(?:\s*,\s*A\(\d+\)[+-]=\d+)*\Z")


@dataclass
class ParsedRow:
    report_id: str
    status: str
    values: list[str]
    errors: list[str] = field(default_factory=list)


@dataclass
class ValidationStats:
    report_rows: int = 0
    unique_rows: int = 0
    ambiguous_rows: int = 0
    candidates: int = 0
    verified: int = 0
    prime: int = 0
    composite: int = 0
    invalid_rows: int = 0
    statuses: Counter[str] = field(default_factory=Counter)
    issue_examples: list[str] = field(default_factory=list)
    source_sha256: str = ""
    completed_at: str = ""

    @property
    def complete(self) -> bool:
        return (
            self.candidates > 0
            and self.verified == self.candidates
            and self.invalid_rows == 0
        )

    @property
    def prime_percent(self) -> float:
        return 100 * self.prime / self.verified if self.verified else 0.0

    @property
    def coverage_percent(self) -> float:
        return 100 * self.verified / self.candidates if self.candidates else 0.0


def parse_report_line(line: str, line_number: int) -> ParsedRow | None:
    """Parse une ligne de rapport; les trois premières lignes sont l'en-tête."""
    if line_number <= 3 or not line.strip():
        return None

    fields = [part.strip() for part in line.rstrip("\r\n").split("|")]
    report_id = fields[0] if fields else ""
    if not REPORT_INDEX.fullmatch(report_id):
        return ParsedRow(
            report_id=report_id or f"ligne {line_number}",
            status="ILLISIBLE",
            values=[],
            errors=["ligne non vide inattendue après l'en-tête"],
        )

    errors: list[str] = []
    if len(fields) != 5:
        errors.append(f"{len(fields)} champs au lieu de 5")

    status = fields[3] if len(fields) > 3 else "ILLISIBLE"
    branch_text = fields[4] if len(fields) > 4 else ""
    branch_values = BRANCH.findall(branch_text)
    if not BRANCH_LIST.fullmatch(branch_text):
        errors.append("champ des branches incomplet ou mal formé")

    numeric_columns = [
        value for value in fields[1:3] if value and value.isdecimal()
    ]
    if status == "UNIQUE":
        if len(branch_values) != 1:
            errors.append(f"UNIQUE avec {len(branch_values)} branche(s) lisible(s)")
        if len(numeric_columns) != 2:
            errors.append("colonnes ancre/P(n) invalides pour une ligne UNIQUE")
    elif status == "AMBIGU":
        if len(branch_values) < 2:
            errors.append(f"AMBIGU avec {len(branch_values)} branche(s) lisible(s)")
        if numeric_columns:
            errors.append("une ligne AMBIGU contient une ancre numérique")
    else:
        errors.append(f"statut inconnu: {status or '(vide)'}")

    if branch_values and len(set(branch_values)) != len(branch_values):
        errors.append("valeurs d'ancrage dupliquées dans les branches")

    # Les colonnes numériques de UNIQUE répètent la branche; en cas de ligne
    # tronquée ou incohérente, leurs valeurs sont quand même validées.
    values = list(dict.fromkeys(branch_values + numeric_columns))
    for column_value in numeric_columns:
        if branch_values and column_value not in branch_values:
            errors.append("ancre/P(n) différente de la valeur des branches")

    return ParsedRow(report_id, status, values, errors)


def run_gp_batch(
    executable: str, values: Sequence[str], timeout: float
) -> list[bool]:
    """Exécute PARI/GP isprime pour un lot; les sorties autres que 0/1 échouent."""
    if not values:
        return []

    commands = "".join(f"print(isprime({value}))\n" for value in values)
    completed = subprocess.run(
        [executable, "-q", "-f"],
        input=commands,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip()[-2000:]
        raise RuntimeError(
            f"PARI/GP a quitté avec le code {completed.returncode}: {detail}"
        )

    output = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if len(output) != len(values) or any(item not in {"0", "1"} for item in output):
        detail = completed.stdout[-2000:].strip()
        raise RuntimeError(
            "Réponse PARI/GP incomplète ou inattendue "
            f"({len(output)} résultats pour {len(values)} ancrages): {detail}"
        )
    return [item == "1" for item in output]


def preflight_gp(executable: str, timeout: float) -> None:
    if run_gp_batch(executable, ["17", "21"], timeout) != [True, False]:
        raise RuntimeError("Le contrôle de démarrage PARI/GP a échoué.")


def record_issue(stats: ValidationStats, line_number: int, row: ParsedRow) -> None:
    stats.invalid_rows += 1
    if len(stats.issue_examples) < 20:
        stats.issue_examples.append(
            f"ligne {line_number} ({row.report_id}): {'; '.join(row.errors)}"
        )


def render_summary(stats: ValidationStats, position: str) -> str:
    integrity = "OUI" if stats.complete else "NON"
    rows = [
        f"=== VALIDATION DE PRIMALITE — {position} ===",
        f"Terminee le                 : {stats.completed_at}",
        "Methode                     : PARI/GP isprime (preuve de primalite)",
        f"Rapports UNIQUE             : {stats.unique_rows:,}",
        f"Rapports AMBIGU             : {stats.ambiguous_rows:,}",
        f"Ancrages candidats extraits : {stats.candidates:,}",
        f"Ancrages verifies           : {stats.verified:,}",
        f"Premiers demontres          : {stats.prime:,}",
        f"Composes / fausses ancres   : {stats.composite:,}",
        f"Score premiers              : {stats.prime_percent:.6f} %",
        f"Couverture de verification : {stats.coverage_percent:.6f} %",
        f"Lignes mal formees          : {stats.invalid_rows:,}",
        f"Validation integrale        : {integrity}",
        f"SHA-256 du rapport source   : {stats.source_sha256}",
    ]
    if stats.issue_examples:
        rows.append("Exemples de problemes:")
        rows.extend(f"  - {example}" for example in stats.issue_examples)
    return "\n".join(rows) + "\n"


def write_annotated_report(
    source: Path, destination: Path, stats: ValidationStats
) -> None:
    if source.resolve() == destination.resolve():
        raise ValueError("Le rapport annote doit etre un nouveau fichier.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    digest = hashlib.sha256()
    try:
        with source.open("rb") as src, temporary.open("wb") as out:
            out.write(render_summary(stats, "DEBUT").encode("utf-8"))
            out.write(b"\n=== DEBUT DU RAPPORT ORIGINAL ===\n")
            while True:
                block = src.read(1024 * 1024)
                if not block:
                    break
                digest.update(block)
                out.write(block)
            out.write(b"\n\n=== FIN DU RAPPORT ORIGINAL ===\n")
            out.write(render_summary(stats, "FIN").encode("utf-8"))
            out.flush()
            os.fsync(out.fileno())

        if digest.hexdigest() != stats.source_sha256:
            raise RuntimeError(
                "Le rapport source a change pendant la validation; "
                "le rapport annote n'a pas ete publie."
            )
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def validate_report(
    source: Path,
    audit_path: Path,
    report_path: Path,
    gp_executable: str,
    batch_size: int = 10_000,
    timeout: float = 1800,
    log_every: int = 100_000,
    resume: bool = False,
) -> ValidationStats:
    if batch_size < 1 or timeout <= 0 or log_every < 1:
        raise ValueError("batch-size, timeout et log-every doivent etre positifs.")
    resolved_source = source.resolve()
    if resolved_source in {audit_path.resolve(), report_path.resolve()}:
        raise ValueError("Les fichiers de sortie ne doivent pas ecraser la source.")
    if audit_path.resolve() == report_path.resolve():
        raise ValueError("Les chemins du rapport et de l'audit doivent differer.")

    stats = ValidationStats()
    digest = hashlib.sha256()
    batch: list[tuple[int, ParsedRow, str]] = []
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    partial_audit = audit_path.with_name(audit_path.name + ".partial")
    if resume and not partial_audit.is_file():
        raise FileNotFoundError(
            f"Reprise demandee, mais audit partiel absent: {partial_audit}"
        )
    previous_audit_size = partial_audit.stat().st_size if resume else 0

    audit_mode = "a" if resume else "w"
    with partial_audit.open(
        audit_mode, encoding="utf-8", newline="\n"
    ) as audit, ExitStack() as stack:
        previous_audit = (
            stack.enter_context(partial_audit.open("rb"))
            if resume
            else None
        )
        with source.open("rb") as input_file:
            for line_number, raw_line in enumerate(input_file, 1):
                digest.update(raw_line)
                line = raw_line.decode("utf-8")
                row = parse_report_line(line, line_number)
                if row is None:
                    continue

                stats.report_rows += 1
                stats.statuses[row.status] += 1
                if row.status == "UNIQUE":
                    stats.unique_rows += 1
                elif row.status == "AMBIGU":
                    stats.ambiguous_rows += 1
                if row.errors:
                    record_issue(stats, line_number, row)
                if not row.values:
                    if not row.errors:
                        record_issue(
                            stats,
                            line_number,
                            ParsedRow(row.report_id, row.status, [], ["aucun ancrage extrait"]),
                        )
                    continue

                for value in row.values:
                    stats.candidates += 1
                    if (
                        previous_audit is not None
                        and previous_audit.tell() < previous_audit_size
                    ):
                        previous_line = previous_audit.readline()
                        if previous_line:
                            try:
                                previous = json.loads(previous_line)
                            except json.JSONDecodeError as exc:
                                raise RuntimeError(
                                    f"Audit partiel invalide a la ligne "
                                    f"{stats.candidates}: {exc}"
                                ) from exc
                            expected = {
                                "line": line_number,
                                "report": row.report_id,
                                "status": row.status,
                                "anchor": value,
                            }
                            actual = {key: previous.get(key) for key in expected}
                            if actual != expected or previous.get("result") not in {
                                "PREMIER_DEMONTRE",
                                "COMPOSE",
                            }:
                                raise RuntimeError(
                                    "L'audit partiel ne correspond plus au rapport "
                                    f"a la ligne source {line_number}; reprise arretee."
                                )
                            stats.verified += 1
                            stats.prime += int(
                                previous["result"] == "PREMIER_DEMONTRE"
                            )
                            stats.composite += int(previous["result"] == "COMPOSE")
                            continue
                    batch.append((line_number, row, value))
                    if len(batch) >= batch_size:
                        _validate_batch(
                            batch, audit, gp_executable, timeout, stats, log_every
                        )
                        batch.clear()

            if batch:
                _validate_batch(batch, audit, gp_executable, timeout, stats, log_every)
                batch.clear()
            if (
                previous_audit is not None
                and previous_audit.tell() < previous_audit_size
            ):
                extra_record = previous_audit.readline()
                if extra_record:
                    raise RuntimeError(
                        "L'audit partiel contient plus de verdicts que "
                        "d'ancrages dans le rapport; reprise arretee."
                    )
            if stats.report_rows == 0:
                record_issue(
                    stats,
                    0,
                    ParsedRow("", "ILLISIBLE", [], ["aucune ligne de rapport detectee"]),
                )

    stats.source_sha256 = digest.hexdigest()
    stats.completed_at = datetime.now().astimezone().isoformat(timespec="seconds")
    os.replace(partial_audit, audit_path)
    write_annotated_report(source, report_path, stats)
    return stats


def _validate_batch(
    batch: Sequence[tuple[int, ParsedRow, str]],
    audit,
    executable: str,
    timeout: float,
    stats: ValidationStats,
    log_every: int,
) -> None:
    try:
        results = run_gp_batch(executable, [item[2] for item in batch], timeout)
    except subprocess.TimeoutExpired as exc:
        if len(batch) > 1:
            midpoint = len(batch) // 2
            _validate_batch(
                batch[:midpoint], audit, executable, timeout, stats, log_every
            )
            _validate_batch(
                batch[midpoint:], audit, executable, timeout, stats, log_every
            )
            return
        line_number, row, value = batch[0]
        raise RuntimeError(
            f"PARI/GP depasse {timeout:g}s pour l'ancrage {value} "
            f"(rapport {row.report_id}, ligne {line_number})."
        ) from exc
    for (line_number, row, value), is_prime in zip(batch, results):
        stats.verified += 1
        stats.prime += int(is_prime)
        stats.composite += int(not is_prime)
        audit.write(
            json.dumps(
                {
                    "line": line_number,
                    "report": row.report_id,
                    "status": row.status,
                    "anchor": value,
                    "result": "PREMIER_DEMONTRE" if is_prime else "COMPOSE",
                    "method": "PARI/GP isprime",
                },
                ensure_ascii=True,
                separators=(",", ":"),
            )
            + "\n"
        )
    audit.flush()
    if stats.verified and stats.verified % log_every < len(batch):
        print(
            f"Progression: {stats.verified:,} ancrages verifies "
            f"sur {stats.candidates:,} candidats extraits jusqu'ici",
            file=sys.stderr,
            flush=True,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--gp-executable",
        default="gp",
        help="chemin vers PARI/GP (commande gp); requis pour la preuve",
    )
    parser.add_argument("--batch-size", type=int, default=10_000)
    parser.add_argument("--timeout", type=float, default=1800)
    parser.add_argument("--log-every", type=int, default=100_000)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="reprendre apres les verdicts valides de l'audit .partial",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    executable = shutil.which(args.gp_executable)
    if executable is None and Path(args.gp_executable).is_file():
        executable = str(Path(args.gp_executable).resolve())
    if executable is None:
        print(
            "ERREUR: PARI/GP (commande gp) est requis pour une preuve exacte; "
            "aucune validation probabiliste de remplacement ne sera utilisee.",
            file=sys.stderr,
        )
        return 1

    try:
        preflight_gp(executable, args.timeout)
        stats = validate_report(
            args.input,
            args.audit,
            args.report,
            executable,
            args.batch_size,
            args.timeout,
            args.log_every,
            args.resume,
        )
    except (OSError, UnicodeError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        return 1

    print(render_summary(stats, "RESULTAT"))
    print(f"Audit detaille : {args.audit}")
    print(f"Rapport annote : {args.report}")
    return 0 if stats.complete else 2


if __name__ == "__main__":
    raise SystemExit(main())
