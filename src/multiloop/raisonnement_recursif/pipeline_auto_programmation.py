"""pipeline_auto_programmation.py - Copie SANDBOXEE du variateur de correction.

Copie (adaptée au raisonnement recursif) du pipeline de correction historique
<< variateur mecanique / transformateur toroidal >> de Mm. Gabriel
(orchestrator_main.py + transmission_un_clic.py).

Difference cle : ce moteur n'ecrit JAMAIS dans le depot vivant. Il opere dans une
sandbox isolee (par defaut un dossier temporaire), en dry-run par defaut, avec
snapshot + manifeste + rollback verifiables.

Operations supportees (mêmes noms que le variateur d'origine) :
  creer_fichier, remplacer_texte, inserer_lignes, supprimer_lignes,
  ajouter_a_la_fin

SECURITE :
  * dry_run=True par defaut (aucune ecriture sauf demande explicite) ;
  * racine d'ecriture confinee a la sandbox ;
  * verification syntaxe (.py via compile, .json via json.loads) ;
  * snapshot des fichiers modifies + rollback possible.
"""
from __future__ import annotations

import json
import shutil
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

OPERATIONS_VALIDES = {
    "creer_fichier",
    "remplacer_texte",
    "inserer_lignes",
    "supprimer_lignes",
    "ajouter_a_la_fin",
}


class VariateurSandboxError(Exception):
    """Erreur d'application d'une operation dans la sandbox."""


@dataclass
class RapportApplication:
    """Rapport d'application d'un contrat dans la sandbox."""

    contrat: str
    horodatage: str
    dry_run: bool
    sandbox: str
    snapshot: Optional[str] = None
    ok: int = 0
    simules: int = 0
    echouees: int = 0
    operations: list[dict[str, Any]] = field(default_factory=list)
    defaillances: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contrat": self.contrat,
            "horodatage": self.horodatage,
            "dry_run": self.dry_run,
            "sandbox": self.sandbox,
            "snapshot": self.snapshot,
            "ok": self.ok,
            "simules": self.simules,
            "echouees": self.echouees,
            "operations": self.operations,
            "defaillances": self.defaillances,
        }


def construire_contrat_squelette(
    role: Optional[str],
    mots_cles: list[str],
    operation: dict[str, Any],
    description: str = "",
) -> dict[str, Any]:
    """Construit un contrat JSON (même forme que le variateur d'origine).

    Le contrat produit sert de base a un patch de correction .json que le
    raisonnement recursif remplit puis applique en sandbox.
    """
    return {
        "meta": {
            "nom": "auto-programmation-fiancee-de-cline",
            "description": description,
            "role": role,
            "mots_cles": list(mots_cles or []),
            "version": "1.0",
        },
        "operations": [dict(operation)],
    }


class PipelineAutoProgrammation:
    """Moteur d'application sandboxe (copie reduite du variateur)."""

    def __init__(
        self,
        sandbox_root: Optional[str | Path] = None,
        dry_run: bool = True,
    ) -> None:
        if sandbox_root is None:
            sandbox_root = Path(tempfile.mkdtemp(prefix="fiancee_sandbox_"))
        self.sandbox_root = Path(sandbox_root).resolve()
        self.sandbox_root.mkdir(parents=True, exist_ok=True)
        self.dry_run = dry_run
        self._snapshot_dir: Optional[Path] = None

    # ── resolution / confinement ───────────────────────────────────────────
    def _resoudre(self, cible: str) -> Path:
        """Resout une cible en la confinant a la sandbox (jamais le depot vivant)."""
        p = Path(cible)
        if p.is_absolute():
            # On refuse d'ecrire hors sandbox : on re-racine sur le nom de fichier.
            p = self.sandbox_root / p.name
        else:
            p = (self.sandbox_root / p).resolve()
        root = self.sandbox_root
        if p != root and root not in p.parents:
            raise VariateurSandboxError(f"Cible hors sandbox refusee : {cible}")
        return p

    # ── snapshot / rollback ────────────────────────────────────────────────
    def _sauvegarder(self, cible: Path) -> Optional[Path]:
        if self._snapshot_dir is None or not cible.exists():
            return None
        self._snapshot_dir.mkdir(parents=True, exist_ok=True)
        dest = self._snapshot_dir / cible.name
        shutil.copy2(cible, dest)
        return dest

    def rollback(self, snapshot_dir: str | Path) -> dict[str, Any]:
        """Restaure les fichiers a partir d'un dossier de snapshot."""
        snap = Path(snapshot_dir)
        restaures: list[str] = []
        if snap.exists():
            for bak in snap.glob("*"):
                if bak.is_file():
                    dest = self.sandbox_root / bak.name
                    shutil.copy2(bak, dest)
                    restaures.append(dest.as_posix())
        return {"snapshot": snap.as_posix(), "restaures": restaures}

    # ── verification syntaxe ───────────────────────────────────────────────
    @staticmethod
    def _verifier_syntaxe(cible: Path, contenu: str) -> Optional[str]:
        suffix = cible.suffix.lower()
        if suffix == ".py":
            try:
                compile(contenu, str(cible), "exec")
            except SyntaxError as exc:
                return f"SyntaxError: {exc}"
            return None
        if suffix == ".json":
            try:
                json.loads(contenu)
            except json.JSONDecodeError as exc:
                return f"JSONDecodeError: {exc}"
            return None
        return None

    # ── application d'une operation ────────────────────────────────────────
    def _appliquer_op(self, index: int, op: dict[str, Any]) -> dict[str, Any]:
        op_type = op.get("op")
        if op_type not in OPERATIONS_VALIDES:
            raise VariateurSandboxError(
                f"operation '{op_type}' non supportee. Valides : {sorted(OPERATIONS_VALIDES)}"
            )
        cible = self._resoudre(op.get("cible", ""))
        rep: dict[str, Any] = {"index": index, "type": op_type, "cible": cible.as_posix()}

        if op_type == "creer_fichier":
            contenu = op.get("contenu", "")
            crlf = False
        else:
            if not cible.exists():
                raise VariateurSandboxError(f"cible introuvable : {cible}")
            contenu = cible.read_text(encoding="utf-8")
            crlf = "\r\n" in contenu

            if op_type == "remplacer_texte":
                ancien = op.get("ancien_texte", "")
                nouveau = op.get("nouveau_texte", "")
                if not ancien:
                    raise VariateurSandboxError("remplacer_texte : 'ancien_texte' requis.")
                n = contenu.count(ancien)
                if n == 0:
                    raise VariateurSandboxError("remplacer_texte : ancien texte introuvable.")
                if op.get("toutes") or n == 1:
                    contenu = contenu.replace(ancien, nouveau)
                else:
                    contenu = contenu.replace(ancien, nouveau, 1)
            elif op_type == "inserer_lignes":
                ligne = int(op.get("ligne_insertion", 1))
                lignes = contenu.split("\n")
                bloc = op.get("contenu", "").split("\n")
                pos = max(0, min(ligne - 1, len(lignes)))
                contenu = "\n".join(lignes[:pos] + bloc + lignes[pos:])
            elif op_type == "supprimer_lignes":
                debut = int(op.get("ligne_debut", 1))
                fin = int(op.get("ligne_fin", debut))
                lignes = contenu.split("\n")
                if debut < 1 or fin > len(lignes):
                    raise VariateurSandboxError(
                        f"supprimer_lignes : bornes {debut}..{fin} hors fichier."
                    )
                contenu = "\n".join(lignes[: debut - 1] + lignes[fin:])
            elif op_type == "ajouter_a_la_fin":
                ajout = op.get("contenu", "")
                contenu = (contenu.rstrip("\n") + "\n" if contenu else "") + ajout

        erreur = self._verifier_syntaxe(cible, contenu)
        if erreur:
            raise VariateurSandboxError(f"verification syntaxe {cible.name} : {erreur}")

        if self.dry_run:
            rep["statut"] = "simule"
            return rep

        self._sauvegarder(cible)
        cible.parent.mkdir(parents=True, exist_ok=True)
        data = contenu.replace("\n", "\r\n") if crlf else contenu
        cible.write_text(data, encoding="utf-8")
        rep["statut"] = "ok"
        return rep

    # ── application d'un contrat ───────────────────────────────────────────
    def appliquer_contrat(self, contrat: dict[str, Any]) -> dict[str, Any]:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        nom = contrat.get("meta", {}).get("nom", "patch")
        self._snapshot_dir = self.sandbox_root / ".snapshots" / f"{stamp}_{nom}"
        rapport = RapportApplication(
            contrat=nom,
            horodatage=stamp,
            dry_run=self.dry_run,
            sandbox=self.sandbox_root.as_posix(),
        )
        for i, op in enumerate(contrat.get("operations", []), start=1):
            try:
                res = self._appliquer_op(i, op)
                rapport.operations.append(res)
                if res["statut"] == "simule":
                    rapport.simules += 1
                else:
                    rapport.ok += 1
            except VariateurSandboxError as exc:
                fail = {"index": i, "type": op.get("op"), "raison": str(exc)}
                rapport.defaillances.append(fail)
                rapport.operations.append({**fail, "statut": "echouee"})
                rapport.echouees += 1
        if not self.dry_run and rapport.ok and self._snapshot_dir is not None:
            rapport.snapshot = self._snapshot_dir.as_posix()
        return rapport.to_dict()


__all__ = [
    "OPERATIONS_VALIDES",
    "VariateurSandboxError",
    "RapportApplication",
    "construire_contrat_squelette",
    "PipelineAutoProgrammation",
]