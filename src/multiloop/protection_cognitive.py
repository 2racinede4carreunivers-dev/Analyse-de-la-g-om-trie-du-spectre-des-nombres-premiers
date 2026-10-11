"""protection_cognitive.py - Protege les capacites cognitives de l'agent fusionne.

Objectif : lorsqu'une modification touche le COEUR COGNITIF / EXPERT de
<< La fiancée de Cline Mm. Gabriel multiloop local >> (pipeline cognitif
convolutif, moteurs, systeme spectral, pipeline HOL, corpus), un SNAPSHOT est
cree avant toute ecriture, et le retour a la version precedente se fait en UNE
COMMANDE :

    python -m src.multiloop.protection_cognitive --rollback <snapshot>
    (ou)  ./RESTAURER_COGNITIF.ps1 -Rollback <snapshot>

Commandes :
    --snapshot [label]     cree un snapshot de reference du coeur cognitif
    --list                 liste les snapshots disponibles
    --rollback <snapshot>  restaure l'ancienne version (une commande)
    --verifier <snapshot>  compare l'etat courant au snapshot (integrite)

ADDITIF : aucun effet sur le fonctionnement de l'agent ; ne fait que des copies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

RACINE_DEPOT = Path(__file__).resolve().parents[2]
DOSSIER_PROTECTION = RACINE_DEPOT / ".gabriel_cognitif"
DOSSIER_SNAPSHOTS = DOSSIER_PROTECTION / "snapshots"

# ── Motifs du COEUR COGNITIF (relatifs a la racine du depot) ──────────────
MOTIFS_PROTEGES: tuple[str, ...] = (
    "src/core/*.py",
    "src/multiloop/*.py",
    "src/multiloop/raisonnement_recursif/*.py",
    "src/spectral/*.py",
    "src/engines/**/*.py",
    "src/adapters/hol_isabelle/*.py",
    "src/adapters/wolfram/*.py",
    "pipeline_cognitif/*.py",
    "theories/methode_spectral.thy",
    "theories/validation_hol_unifiee.thy",
    "theories/geometrie_spectre_premier.thy",
    "corpus/*",
)

EXCLUSIONS = ("__pycache__",)


@dataclass
class Manifeste:
    label: str
    horodatage: str
    racine: str
    fichiers: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "horodatage": self.horodatage,
            "racine": self.racine,
            "total": len(self.fichiers),
            "fichiers": self.fichiers,
        }


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _fichiers_proteges() -> list[Path]:
    """Retourne la liste triee des fichiers du coeur cognitif existants."""
    trouves: set[Path] = set()
    for motif in MOTIFS_PROTEGES:
        for p in RACINE_DEPOT.glob(motif):
            if p.is_file() and not any(x in p.parts for x in EXCLUSIONS):
                trouves.add(p.resolve())
    return sorted(trouves)


def creer_snapshot(label: str = "reference") -> dict:
    """Cree un snapshot horodate du coeur cognitif. Retourne son manifeste."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    cible = DOSSIER_SNAPSHOTS / f"{stamp}_{label}"
    fichiers_dir = cible / "fichiers"
    fichiers_dir.mkdir(parents=True, exist_ok=True)

    manifeste = Manifeste(label=label, horodatage=stamp, racine=RACINE_DEPOT.as_posix())
    for src in _fichiers_proteges():
        rel = src.relative_to(RACINE_DEPOT)
        dest = fichiers_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        manifeste.fichiers.append({
            "rel": rel.as_posix(),
            "sha256": _sha256(src),
            "octets": src.stat().st_size,
        })

    (cible / "manifeste.json").write_text(
        json.dumps(manifeste.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {**manifeste.to_dict(), "dossier": cible.as_posix()}


def lister_snapshots() -> list[Path]:
    if not DOSSIER_SNAPSHOTS.exists():
        return []
    return sorted([p for p in DOSSIER_SNAPSHOTS.iterdir() if p.is_dir()])


def restaurer_snapshot(snapshot: str | Path, dry_run: bool = False) -> dict:
    """Restaure l'ancienne version a partir d'un snapshot (rollback une commande)."""
    snap = Path(snapshot)
    if not snap.is_absolute():
        snap = DOSSIER_SNAPSHOTS / snapshot
    man_path = snap / "manifeste.json"
    if not man_path.exists():
        raise FileNotFoundError(f"Snapshot introuvable ou incomplet : {snap}")

    manifeste = json.loads(man_path.read_text(encoding="utf-8"))
    fichiers_dir = snap / "fichiers"
    restaures: list[str] = []
    manquants: list[str] = []

    for entree in manifeste.get("fichiers", []):
        src = fichiers_dir / entree["rel"]
        dest = RACINE_DEPOT / entree["rel"]
        if not src.exists():
            manquants.append(entree["rel"])
            continue
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        restaures.append(entree["rel"])

    return {
        "snapshot": snap.as_posix(),
        "label": manifeste.get("label"),
        "dry_run": dry_run,
        "restaures": restaures,
        "manquants": manquants,
    }


def verifier_integrite(snapshot: str | Path) -> dict:
    """Compare l'etat courant au snapshot : fichiers modifies / absents."""
    snap = Path(snapshot)
    if not snap.is_absolute():
        snap = DOSSIER_SNAPSHOTS / snapshot
    man_path = snap / "manifeste.json"
    if not man_path.exists():
        raise FileNotFoundError(f"Snapshot introuvable : {snap}")

    manifeste = json.loads(man_path.read_text(encoding="utf-8"))
    modifies: list[str] = []
    absents: list[str] = []
    for entree in manifeste.get("fichiers", []):
        courant = RACINE_DEPOT / entree["rel"]
        if not courant.exists():
            absents.append(entree["rel"])
        elif _sha256(courant) != entree["sha256"]:
            modifies.append(entree["rel"])
    return {"snapshot": snap.as_posix(), "modifies": modifies, "absents": absents}


def proteger_avant_modification(label: str = "auto-avant-modif") -> dict:
    """Raccourci : snapshot automatique avant une modification du coeur cognitif."""
    return creer_snapshot(label=label)


def _main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Protection des capacites cognitives - snapshot / rollback."
    )
    parser.add_argument("--snapshot", nargs="?", const="reference",
                        help="Cree un snapshot (label optionnel).")
    parser.add_argument("--list", action="store_true", help="Liste les snapshots.")
    parser.add_argument("--rollback", help="Restaure un snapshot (nom ou chemin).")
    parser.add_argument("--verifier", help="Verifie l'integrite d'un snapshot.")
    parser.add_argument("--dry-run", action="store_true", help="Simule le rollback.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.list:
        snaps = lister_snapshots()
        print("\n=== Snapshots du coeur cognitif ===")
        for s in snaps:
            print(f"  - {s.name}")
        if not snaps:
            print("  (aucun snapshot pour le moment)")
        return 0

    if args.snapshot is not None:
        man = creer_snapshot(label=args.snapshot)
        print("\n=== Snapshot cree ===")
        print(f"  label     : {man['label']}")
        print(f"  dossier   : {man['dossier']}")
        print(f"  fichiers  : {man['total']}")
        return 0

    if args.rollback:
        res = restaurer_snapshot(args.rollback, dry_run=args.dry_run)
        print("\n=== Rollback du coeur cognitif ===")
        print(f"  snapshot  : {res['snapshot']}")
        print(f"  mode      : {'SIMULATION' if res['dry_run'] else 'RESTAURATION REELLE'}")
        print(f"  restaures : {len(res['restaures'])}")
        if res["manquants"]:
            print(f"  ATTENTION manquants : {len(res['manquants'])}")
        return 0

    if args.verifier:
        res = verifier_integrite(args.verifier)
        print("\n=== Integrite vs snapshot ===")
        print(f"  modifies : {len(res['modifies'])}")
        for m in res["modifies"]:
            print(f"    ~ {m}")
        print(f"  absents  : {len(res['absents'])}")
        for a in res["absents"]:
            print(f"    - {a}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())