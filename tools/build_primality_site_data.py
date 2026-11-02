#!/usr/bin/env python3
"""Build reproducible, SHA-256-checkable shards for the prime validation site."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import BinaryIO


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIT = ROOT / "reconstruction_k28M_84M_detail_primalite.jsonl"
DEFAULT_SOURCE = ROOT / "reconstruction_k28M_84M_detail.txt"
DEFAULT_OUTPUT = ROOT / "site"
EXPECTED_COUNT = 6_849_579
PART_COUNT = 29


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def merkle_root(part_hashes: list[str]) -> str:
    if not part_hashes:
        raise ValueError("Aucun fragment de donnees.")
    level = [hashlib.sha256(b"\x00" + bytes.fromhex(value)).digest() for value in part_hashes]
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [
            hashlib.sha256(b"\x01" + level[index] + level[index + 1]).digest()
            for index in range(0, len(level), 2)
        ]
    return level[0].hex()


def open_gzip_shard(path: Path) -> tuple[BinaryIO, gzip.GzipFile]:
    raw = path.open("wb")
    compressed = gzip.GzipFile(
        filename="",
        mode="wb",
        compresslevel=9,
        fileobj=raw,
        mtime=0,
    )
    return raw, compressed


def build(audit: Path, source: Path, output: Path, expected_count: int) -> dict:
    data_dir = output / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    audit_sha = sha256_file(audit)
    source_sha = sha256_file(source)
    with audit.open("rb") as stream:
        actual_count = sum(block.count(b"\n") for block in iter(
            lambda: stream.read(8 * 1024 * 1024), b""
        ))
    if actual_count != expected_count:
        raise ValueError(
            f"Nombre de verdicts inattendu: {actual_count:,} "
            f"(attendu {expected_count:,})."
        )

    counts = {"UNIQUE": 0, "AMBIGU": 0}
    verdicts = {"PREMIER_DEMONTRE": 0, "COMPOSE": 0}
    dataset_digest = hashlib.sha256()
    parts = []
    with audit.open("r", encoding="utf-8") as records:
        for part_number in range(PART_COUNT):
            start = part_number * actual_count // PART_COUNT
            stop = (part_number + 1) * actual_count // PART_COUNT
            path = data_dir / f"ancrages-{part_number + 1:02d}.tsv.gz"
            raw, compressed = open_gzip_shard(path)
            first_report = last_report = None
            try:
                for ordinal in range(start, stop):
                    line = records.readline()
                    if not line:
                        raise ValueError(
                            f"Audit interrompu au verdict {ordinal + 1:,}."
                        )
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(
                            f"JSON invalide au verdict {ordinal + 1:,}: {exc}"
                        ) from exc
                    report_id = record.get("report")
                    status = record.get("status")
                    anchor = record.get("anchor")
                    result = record.get("result")
                    if (
                        not isinstance(report_id, str)
                        or status not in counts
                        or not isinstance(anchor, str)
                        or not anchor.isdecimal()
                        or result not in verdicts
                    ):
                        raise ValueError(
                            f"Enregistrement invalide au verdict {ordinal + 1:,}."
                        )
                    if record.get("method") != "PARI/GP isprime":
                        raise ValueError(
                            f"Methode inattendue au verdict {ordinal + 1:,}."
                        )
                    row = (
                        f"{report_id}\t{status}\t{anchor}\t{result}\n"
                    ).encode("ascii")
                    compressed.write(row)
                    dataset_digest.update(row)
                    counts[status] += 1
                    verdicts[result] += 1
                    first_report = first_report or report_id
                    last_report = report_id
            finally:
                compressed.close()
                raw.close()

            parts.append(
                {
                    "number": part_number + 1,
                    "file": path.name,
                    "first_record": start + 1,
                    "last_record": stop,
                    "count": stop - start,
                    "first_report": first_report,
                    "last_report": last_report,
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )

        if records.readline():
            raise ValueError("L'audit contient plus de verdicts que prevu.")

    if sum(counts.values()) != actual_count or sum(verdicts.values()) != actual_count:
        raise ValueError("Les totaux des fragments ne correspondent pas a l'audit.")

    manifest = {
        "format": "TSV UTF-8, report/status/anchor/result, gzip mtime=0",
        "validation_method": "PARI/GP 2.19 isprime",
        "source_report": {
            "file": "reconstruction_k28M_84M_detail.txt",
            "sha256": source_sha,
            "report_rows": 6_441_794,
            "unique_rows": 6_045_662,
            "ambiguous_rows": 396_132,
            "malformed_rows": 1,
        },
        "audit": {
            "file": "reconstruction_k28M_84M_detail_primalite.jsonl",
            "sha256": audit_sha,
        },
        "records": actual_count,
        "primes_proven": verdicts["PREMIER_DEMONTRE"],
        "composites": verdicts["COMPOSE"],
        "unique_anchor_records": counts["UNIQUE"],
        "ambiguous_branch_records": counts["AMBIGU"],
        "canonical_tsv_sha256": dataset_digest.hexdigest(),
        "merkle_scheme": (
            "SHA256 leaves: SHA256(0x00 || raw-shard-SHA256); "
            "parents: SHA256(0x01 || left || right); duplicate odd final node"
        ),
        "merkle_root": merkle_root([part["sha256"] for part in parts]),
        "part_count": len(parts),
        "parts": parts,
    }
    manifest_path = data_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Created {len(parts)} shards for {actual_count:,} records; "
        f"Merkle root {manifest['merkle_root']}"
    )
    print(f"Manifest: {manifest_path}")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--source-report", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--expected-count", type=int, default=EXPECTED_COUNT)
    args = parser.parse_args()
    build(args.audit, args.source_report, args.output, args.expected_count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
