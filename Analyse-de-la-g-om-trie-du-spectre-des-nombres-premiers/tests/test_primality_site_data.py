from __future__ import annotations

import gzip
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATOR_PATH = ROOT / "tools" / "build_primality_site_data.py"
SPEC = importlib.util.spec_from_file_location("build_primality_site_data", GENERATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
GENERATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR)


def test_build_emits_checkable_shards_and_merkle_root(tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    source = tmp_path / "source.txt"
    output = tmp_path / "site"
    records = [
        {
            "report": "1/1",
            "status": "UNIQUE",
            "anchor": "17",
            "result": "PREMIER_DEMONTRE",
            "method": "PARI/GP isprime",
        },
        {
            "report": "1/2",
            "status": "AMBIGU",
            "anchor": "21",
            "result": "COMPOSE",
            "method": "PARI/GP isprime",
        },
    ]
    audit.write_text(
        "".join(json.dumps(record) + "\n" for record in records),
        encoding="utf-8",
    )
    source.write_text("source report\n", encoding="utf-8")

    manifest = GENERATOR.build(audit, source, output, expected_count=2)

    assert manifest["records"] == 2
    assert manifest["primes_proven"] == 1
    assert manifest["composites"] == 1
    assert manifest["part_count"] == 29
    assert manifest["merkle_root"] == GENERATOR.merkle_root(
        [part["sha256"] for part in manifest["parts"]]
    )
    recovered = b"".join(
        gzip.decompress((output / "data" / part["file"]).read_bytes())
        for part in manifest["parts"]
    )
    assert recovered == (
        b"1/1\tUNIQUE\t17\tPREMIER_DEMONTRE\n"
        b"1/2\tAMBIGU\t21\tCOMPOSE\n"
    )
