#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRANSMISSION UN CLIC (variateur mécanique de correction autonome)

Ce script est l'intermédiaire « un clic » entre l'utilisateur et le pipeline
de correction du dépôt Gabriel. Il reçoit un PATCH décrit en Python, le
transmet à `archiviste.py` (la transmission qui retrouve les adresses dans le
réseau SQLite gabriel_repo_map.db), puis instruit `orchestrator_main.py`
(variateur) pour appliquer la correction à TOUS les fichiers impliqués.

Usage :
  python transmission_un_clic.py --patch fichier_patch.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent
DB = REPO / "data" / "gabriel_repo_map.db"
ORCHESTRATEUR = REPO / "orchestrator_main.py"

OPERATIONS_VALIDES = {
    "remplacer_texte", "inserer_lignes", "supprimer_lignes",
    "ajouter_a_la_fin", "creer_fichier", "deployer_fichier",
    "executer_python", "propager_texte",
}


def _charger_patch(chemin: Path) -> dict:
    """Exécute le fichier patch Python et récupère son objet PATCH."""
    namespace: dict = {"__file__": str(chemin.resolve()), "__name__": "__patch__"}
    code = chemin.read_text(encoding="utf-8")
    exec(compile(code, str(chemin), "exec"), namespace)
    patch = namespace.get("PATCH") or namespace.get("patch")
    if not isinstance(patch, dict):
        raise SystemExit("Le patch doit définir une variable PATCH = { ... } (dict).")
    return patch


def _normaliser_patch(patch: dict, args) -> dict:
    """Rassemble les exigences du patch en un contrat exécutable.

    Deux formats sont acceptés :

    1) PATCH réseau (une seule opération propagée via l'archiviste) :
         PATCH = {
            "mots_cles": [...], "role": ..., "profondeur": N,
            "operation": {"op": "remplacer_texte", ...},
         }

    2) PATCH multi-opérations (contrat direct, mode « variateur complet ») :
         PATCH = {
            "operations": [
                {"op": "creer_fichier", "cible": "...", "contenu": "..."},
                {"op": "remplacer_texte", "cible": "...",
                 "ancien_texte": "...", "nouveau_texte": "...", "toutes": True},
                # ou opérations réseau :
                {"op": "propager_texte", "mots_cles": [...], "operation": {...}},
            ]
         }
    """
    meta = patch.get("meta") or {}
    if "operations" in patch and isinstance(patch["operations"], list):
        # ── Format 2 : liste directe d'opérations ─────────────────────
        operations = []
        for i, op_brut in enumerate(patch["operations"], start=1):
            if not isinstance(op_brut, dict):
                raise SystemExit(f"operations[{i}] : un objet dict est attendu.")
            if op_brut.get("op") == "propager_texte":
                sous = op_brut.get("operation")
                if sous:
                    op_type = sous.get("op")
                    if op_type not in OPERATIONS_VALIDES:
                        raise SystemExit(
                            f"Opération réseau '{op_type}' non supportée. "
                            f"Valides : {sorted(OPERATIONS_VALIDES)}"
                        )
                operations.append(op_brut)
            elif op_brut.get("op") in OPERATIONS_VALIDES:
                operations.append(op_brut)
            else:
                raise SystemExit(
                    f"operations[{i}] : op '{op_brut.get('op')}' inconnue "
                    f"(ou opération réseau mal formée)."
                )
        return {
            "meta": {
                "nom": meta.get("nom") or "transmission_un_clic",
                "description": meta.get("description") or "",
                "version": "1.0",
            },
            "operations": operations,
        }

    # ── Format 1 : réseau + une opération d'édition propagée ──────────
    mots_cles = [str(m) for m in (patch.get("mots_cles") or args.mots or [])]
    role = patch.get("role") or args.role
    profondeur = int(patch.get("profondeur") or args.profondeur or 1)

    operation = patch.get("operation")
    if not operation:
        raise SystemExit("Le patch doit fournir une clé 'operation' (édit).")
    op = dict(operation)
    op_type = op.get("op")
    if op_type not in OPERATIONS_VALIDES:
        raise SystemExit(f"Opération '{op_type}' non supportée. "
                         f"Valides : {sorted(OPERATIONS_VALIDES)}")

    return {
        "meta": {
            "nom": meta.get("nom") or "transmission_un_clic",
            "description": meta.get("description") or "",
            "version": "1.0",
        },
        "operations": [
            {
                "op": "propager_texte",
                "mots_cles": mots_cles,
                "role": role or None,
                "profondeur": profondeur,
                "operation": op,
                "message": meta.get("description") or "",
            }
        ],
    }


def _consulter_archiviste(critere: dict) -> list:
    """Interroge l'archiviste (transmission) pour lister les adresses."""
    from archiviste import ArchivisteCorrection
    a = ArchivisteCorrection(DB, REPO)
    return a.reseau_de_correction(
        critere["mots_cles"],
        role=critere["role"],
        profondeur=critere["profondeur"],
    )


def _appliquer_contrat(contrat: dict, dry_run: bool) -> dict:
    """Rédige le contrat JSON puis lance orchestrator_main.py --apply."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as f:
        json.dump(contrat, f, ensure_ascii=False, indent=2)
        tmp = f.name
    cmd = [sys.executable, str(ORCHESTRATEUR), "--apply", tmp]
    if dry_run:
        cmd.append("--apply-dry-run")
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True)
    print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    Path(tmp).unlink(missing_ok=True)
    return {"returncode": proc.returncode}


def main() -> None:
    parser = argparse.ArgumentParser(description="Transmission un clic — variateur de correction.")
    parser.add_argument("--patch", help="Fichier Python décrivant le PATCH (PATCH = {...}).")
    parser.add_argument("--mots", nargs="*", default=[], help="Mots-clés (si patch inline).")
    parser.add_argument("--role", default=None, help="Rôle cible du réseau.")
    parser.add_argument("--profondeur", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Simule sans modifier.")
    args = parser.parse_args()

    if not args.patch:
        raise SystemExit("Fournir --patch fichier.py (le patch PATCH={...}).")
    patch = _charger_patch(Path(args.patch).resolve())
    contrat = _normaliser_patch(patch, args)
    op = contrat["operations"][0]

    print("\n═══ TRANSMISSION — VARIATEUR DE CORRECTION AUTONOME ═══")
    print(f"  dépôt        : {REPO}")
    print(f"  base réseau  : {DB}")
    if "mots_cles" in op:
        print(f"  mots-clés    : {op['mots_cles']}")
        print(f"  rôle         : {op['role']}")
        print(f"  profondeur   : {op['profondeur']}")
        adresses = _consulter_archiviste(op)
        print(f"\n  → Archiviste a trouvé {len(adresses)} fichiers impliqués :")
        for ad in adresses[:15]:
            print(f"      • {ad['rel_path']}")
        if len(adresses) > 15:
            print(f"      … et {len(adresses) - 15} autres.")
        if not adresses:
            print("      (aucun — le patch ne cible rien)")
    else:
        print(f"  → {len(contrat['operations'])} opération(s) d'édition ciblées :")
        for i, o in enumerate(contrat["operations"], start=1):
            print(f"      [{i}] {o.get('op')} -> {o.get('cible') or (o.get('mots_cles') or 'réseau')}")
    print("\n  → Transmission de l'ordre d'application à orchestrator_main.py\n")

    rapport = _appliquer_contrat(contrat, dry_run=args.dry_run)
    if rapport["returncode"] != 0:
        raise SystemExit(f"Échec de l'application (rc={rapport['returncode']})")
    print("\n✅ Correction appliquée conformément au réseau neuronal détecté.")


if __name__ == "__main__":
    main()