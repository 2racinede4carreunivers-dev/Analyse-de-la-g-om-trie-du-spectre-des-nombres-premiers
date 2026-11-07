#!/usr/bin/env python3
"""Split, verify, or reconstruct certification files using a SHA-256 manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import BinaryIO

CHUNK_SIZE = 90 * 1024 * 1024
READ_SIZE = 1024 * 1024
MANIFEST_VERSION = 1


def sha256_stream(stream: BinaryIO, output: BinaryIO | None = None) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    while True:
        block = stream.read(READ_SIZE)
        if not block:
            break
        if output is not None:
            output.write(block)
        digest.update(block)
        size += len(block)
    return size, digest.hexdigest()


def ensure_relative_path(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Chemin de manifeste non sûr : {relative}")
    resolved_root = root.resolve()
    resolved_path = (root / path).resolve()
    if resolved_path != resolved_root and resolved_root not in resolved_path.parents:
        raise ValueError(f"Chemin hors du dossier du manifeste : {relative}")
    return resolved_path


def split_sources(source_dir: Path, parts_dir: Path, manifest_path: Path, chunk_size: int) -> None:
    source_dir = source_dir.resolve()
    parts_dir = parts_dir.resolve()
    manifest_path = manifest_path.resolve()
    if not source_dir.is_dir():
        raise FileNotFoundError(f"Dossier des originaux introuvable : {source_dir}")
    if chunk_size < 1:
        raise ValueError("La taille de fragment doit être positive.")
    if manifest_path.exists():
        raise FileExistsError(f"Le manifeste existe déjà : {manifest_path}")

    source_files = sorted(path for path in source_dir.rglob("*") if path.is_file())
    if not source_files:
        raise ValueError(f"Aucun fichier source dans {source_dir}")

    entries = []
    for source in source_files:
        relative_source = source.relative_to(source_dir)
        parts = []
        original_digest = hashlib.sha256()
        original_size = 0
        part_number = 0
        with source.open("rb") as input_file:
            while True:
                block = input_file.read(chunk_size)
                if not block:
                    break
                part_number += 1
                original_digest.update(block)
                original_size += len(block)
                relative_part = relative_source.parent / f"{relative_source.name}.part-{part_number:05d}"
                target = parts_dir / relative_part
                if target.exists():
                    raise FileExistsError(f"Le fragment existe déjà : {target}")
                target.parent.mkdir(parents=True, exist_ok=True)
                part_digest = hashlib.sha256(block).hexdigest()
                target.write_bytes(block)
                parts.append(
                    {
                        "path": (Path("parts") / relative_part).as_posix(),
                        "size_bytes": len(block),
                        "sha256": part_digest,
                    }
                )

        entries.append(
            {
                "source_path": relative_source.as_posix(),
                "size_bytes": original_size,
                "sha256": original_digest.hexdigest(),
                "parts": parts,
            }
        )
        print(f"Fragmenté : {relative_source} ({original_size} octets, {len(parts)} fragment(s))")

    manifest = {
        "schema_version": MANIFEST_VERSION,
        "chunk_size_bytes": chunk_size,
        "files": entries,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Manifeste écrit : {manifest_path}")


def load_manifest(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != MANIFEST_VERSION:
        raise ValueError(f"Version de manifeste non prise en charge : {manifest.get('schema_version')}")
    if not isinstance(manifest.get("files"), list) or not manifest["files"]:
        raise ValueError("Le manifeste ne contient aucun fichier.")
    return manifest


def verify_or_reassemble(manifest_path: Path, output_dir: Path | None) -> None:
    manifest_path = manifest_path.resolve()
    root = manifest_path.parent
    manifest = load_manifest(manifest_path)

    for entry in manifest["files"]:
        source_relative = Path(entry["source_path"])
        if source_relative.is_absolute() or ".." in source_relative.parts:
            raise ValueError(f"Chemin source non sûr : {entry['source_path']}")
        source_size = 0
        source_digest = hashlib.sha256()
        temporary_path: Path | None = None
        output_stream: BinaryIO | None = None
        target: Path | None = None

        if output_dir is not None:
            if source_relative.is_absolute() or ".." in source_relative.parts:
                raise ValueError(f"Chemin de sortie non sûr : {entry['source_path']}")
            target = output_dir.resolve() / source_relative
            if target.exists():
                raise FileExistsError(f"La sortie existe déjà, elle n’est pas écrasée : {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            handle = tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=f".{target.name}.",
                suffix=".tmp",
                dir=target.parent,
                delete=False,
            )
            temporary_path = Path(handle.name)
            output_stream = handle

        try:
            for part in entry["parts"]:
                part_path = ensure_relative_path(root, part["path"])
                if not part_path.is_file():
                    raise FileNotFoundError(f"Fragment manquant : {part['path']}")
                part_digest = hashlib.sha256()
                part_size = 0
                with part_path.open("rb") as input_part:
                    while True:
                        block = input_part.read(READ_SIZE)
                        if not block:
                            break
                        if output_stream is not None:
                            output_stream.write(block)
                        source_digest.update(block)
                        part_digest.update(block)
                        source_size += len(block)
                        part_size += len(block)
                if part_size != part["size_bytes"] or part_digest.hexdigest() != part["sha256"]:
                    raise ValueError(f"Taille ou SHA-256 incorrect pour le fragment : {part['path']}")

            if output_stream is not None:
                output_stream.flush()
                os.fsync(output_stream.fileno())
                output_stream.close()
                output_stream = None

            if source_size != entry["size_bytes"] or source_digest.hexdigest() != entry["sha256"]:
                raise ValueError(f"Taille ou SHA-256 incorrect pour l’original : {entry['source_path']}")

            if temporary_path is not None and target is not None:
                temporary_path.replace(target)
                temporary_path = None
            print(f"Vérifié : {entry['source_path']} ({source_size} octets)")
        finally:
            if output_stream is not None:
                output_stream.close()
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path(__file__).with_name("manifest.json"),
        help="Manifeste des fichiers fragmentés",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Créer les fragments et le manifeste")
    split_parser.add_argument("--source-dir", type=Path, required=True)
    split_parser.add_argument("--parts-dir", type=Path, default=Path(__file__).with_name("parts"))
    split_parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)

    subparsers.add_parser("verify", help="Vérifier fragments et empreintes sans reconstituer")

    reassemble_parser = subparsers.add_parser("reassemble", help="Reconstituer les originaux")
    reassemble_parser.add_argument("--output-dir", type=Path, required=True)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "split":
            split_sources(args.source_dir, args.parts_dir, args.manifest, args.chunk_size)
        elif args.command == "verify":
            verify_or_reassemble(args.manifest, None)
        else:
            verify_or_reassemble(args.manifest, args.output_dir)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Erreur de certification : {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
