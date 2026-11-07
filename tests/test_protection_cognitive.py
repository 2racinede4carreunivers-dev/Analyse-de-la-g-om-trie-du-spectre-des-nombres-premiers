"""Tests de la protection des capacites cognitives (snapshot / rollback)."""
from __future__ import annotations

from pathlib import Path

import src.multiloop.protection_cognitive as pc


def test_perimetre_protege_non_vide():
    fichiers = pc._fichiers_proteges()
    assert fichiers, "aucun fichier protege detecte"
    # le coeur doit inclure au moins le pipeline et un module multiloop
    rels = {f.relative_to(pc.RACINE_DEPOT).as_posix() for f in fichiers}
    assert any(r.startswith("src/core/") for r in rels)
    assert any(r.startswith("src/multiloop/") for r in rels)


def test_snapshot_integrite_rollback_dryrun(tmp_path, monkeypatch):
    monkeypatch.setattr(pc, "DOSSIER_PROTECTION", tmp_path)
    monkeypatch.setattr(pc, "DOSSIER_SNAPSHOTS", tmp_path / "snapshots")

    man = pc.creer_snapshot("pytest")
    assert man["total"] > 0
    snap = Path(man["dossier"])
    assert (snap / "manifeste.json").exists()

    # integrite : rien n'a change juste apres le snapshot
    integ = pc.verifier_integrite(snap)
    assert integ["modifies"] == []
    assert integ["absents"] == []

    # rollback dry-run : ne modifie rien, liste tout
    rb = pc.restaurer_snapshot(snap, dry_run=True)
    assert rb["dry_run"] is True
    assert len(rb["restaures"]) == man["total"]

    # listing
    snaps = pc.lister_snapshots()
    assert any(s.name == snap.name for s in snaps)


def test_verifier_integrite_detecte_modification(tmp_path, monkeypatch):
    monkeypatch.setattr(pc, "DOSSIER_PROTECTION", tmp_path)
    monkeypatch.setattr(pc, "DOSSIER_SNAPSHOTS", tmp_path / "snapshots")

    man = pc.creer_snapshot("pytest2")
    snap = Path(man["dossier"])
    # Simule une modification en alterant une copie du manifeste (cible fictive)
    import json
    man_path = snap / "manifeste.json"
    data = json.loads(man_path.read_text(encoding="utf-8"))
    data["fichiers"][0]["sha256"] = "0" * 64  # empreinte falsifiee
    man_path.write_text(json.dumps(data), encoding="utf-8")

    integ = pc.verifier_integrite(snap)
    assert len(integ["modifies"]) >= 1


def test_rollback_snapshot_inexistant(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        pc.restaurer_snapshot(tmp_path / "introuvable")