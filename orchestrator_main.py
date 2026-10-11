#!/usr/bin/env python3
"""Gabriel repository orchestrator.

Ce module est le point d'entree pour la cartographie locale du depot Gabriel.
Il scanne automatiquement le projet, construit une base SQLite, relie les
fichiers selon leurs imports et leur architecture, puis calcule un score
importances pour les composants de l'agent.

Objectif :
- donner un relevé topographique du depot local
- servir de base pour les futurs patchs, corrections et ajouts
- fournir un point d'entree unique pour orchestrer la mise a jour du code

L'idee est de modeliser le repo comme un reseau fonctionnel :
  - noeuds = fichiers et dossiers
  - aretes = imports, mots-cles, co-structures
  - score = centralite + role + importance fonctionnelle

═══════════════════════════════════════════════════════════════════════════
  VARIATEUR MECANIQUE DE PROGRAMMATION  (phase d'application guidee par la DB)
  Ce module embarque le moteur d'application des modifications :

  - `--apply <contrat.json>` : le variateur consomme un contrat de patch JSON,
    resout chaque fichier cible grace a la base gabriel_repo_map.db
    (role, mots-cles, score, chemin relatif, suffixe de fichier),
    sauvegarde l'etat d'origine, applique, verifie (py_compile / json.loads),
    puis ecrit un rapport + manifeste restaurable.
  - `--apply-dry-run`       : planifie sans rien modifier.
  - `--rollback <dossier>`  : restaure un snapshot complet.
  - `--list-snapshots`      : liste les sauvegardes disponibles.
═══════════════════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional


DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "logs",
    "dist",
    "build",
    "__snapshots__",
    "tmp",
    "temp",
    "site-packages",
    ".gabriel_variateur",
    ".ipynb_checkpoints",
}

DEFAULT_INCLUDE_EXTS = {
    ".py",
    ".md",
    ".txt",
    ".thy",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".sh",
    ".bat",
    ".ps1",
    ".sql",
}

IGNORE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".ico",
    ".pdf",
    ".csv",
    ".aux",
    ".log",
    ".toc",
    ".out",
    ".synctex.gz",
    ".gz",
    ".zip",
    ".tar",
    ".rar",
}

ROLE_KEYWORDS = {
    "core": ["core", "pipeline", "main", "orchestr", "engine", "manager", "config"],
    "spectral": ["spectral", "prime", "digamma", "gap", "ratio", "zeta", "riemann"],
    "multiloop": ["multiloop", "loop", "critic", "refinement", "reason", "coherence", "audit"],
    "hol": ["hol", "isabelle", "thy", "theory", "proof", "validation", "formal"],
    "ui": ["ui", "cli", "frontend", "interface", "terminal", "console"],
    "memory": ["memory", "memoire", "learning", "cognitive", "knowledge", "rag"],
    "vision": ["vision", "image", "ocr", "analysis", "camera", "scan"],
    "test": ["test", "pytest", "validation", "verification", "check"],
    "doc": ["readme", "guide", "doc", "documentation", "summary", "report"],
    "data": ["data", "db", "sqlite", "json", "cache", "corpus"],
}


@dataclass
class FileScanResult:
    path: str
    rel_path: str
    extension: str
    file_type: str
    role: str
    size_bytes: int
    modified_iso: str
    keywords: list[str]
    imports: list[str]
    score: float


class RepoOrchestrator:
    """Scanne le depot et construit la base SQLite de cartographie."""

    def __init__(self, repo_root: Path, db_path: Path):
        self.repo_root = repo_root.resolve()
        self.db_path = db_path.resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def scan_repo(self) -> list[FileScanResult]:
        files: list[FileScanResult] = []
        for path in self._iter_files(self.repo_root):
            rel_path = path.relative_to(self.repo_root).as_posix()
            ext = path.suffix.lower()
            if ext in IGNORE_SUFFIXES:
                continue
            if ext and ext not in DEFAULT_INCLUDE_EXTS:
                # on accepte les fichiers sans extension specifiques comme documents utiles
                if path.name.startswith("."):
                    continue
            if path.name == "orchestrator_main.py":
                # l'orchestrateur ne se considere pas comme un composant fonctionnel de base
                role = "core"
            else:
                role = self._detect_role(rel_path, path)

            keywords = self._extract_keywords(rel_path, path)
            imports = self._extract_python_imports(path)
            score = self._compute_score(rel_path, keywords, imports, path)
            files.append(
                FileScanResult(
                    path=path.as_posix(),
                    rel_path=rel_path,
                    extension=ext,
                    file_type=self._detect_file_type(ext, path),
                    role=role,
                    size_bytes=path.stat().st_size,
                    modified_iso=datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
                    keywords=sorted(set(keywords)),
                    imports=sorted(set(imports)),
                    score=score,
                )
            )
        return files

    def _iter_files(self, root: Path) -> Iterable[Path]:
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in DEFAULT_EXCLUDES for part in path.parts):
                continue
            yield path

    def _detect_file_type(self, ext: str, path: Path) -> str:
        name = path.name.lower()
        if name.endswith(".py"):
            return "python"
        if name.endswith(".thy"):
            return "isabelle_hol"
        if name.endswith(".md"):
            return "markdown"
        if name.endswith(".sql"):
            return "sql"
        if name.endswith(".json"):
            return "json"
        if name.endswith(".yaml") or name.endswith(".yml"):
            return "yaml"
        if name.endswith(".sh") or name.endswith(".bat") or name.endswith(".ps1"):
            return "script"
        if ext:
            return ext.lstrip(".")
        return "other"

    def _detect_role(self, rel_path: str, path: Path) -> str:
        lower = rel_path.lower()
        for role, keywords in ROLE_KEYWORDS.items():
            if any(keyword in lower for keyword in keywords):
                return role
        parts = set(str(path.parent).lower().split("/"))
        if "src" in parts:
            return "core"
        if "theories" in parts:
            return "hol"
        if "tests" in parts:
            return "test"
        if "docs" in parts or lower.startswith("readme"):
            return "doc"
        return "core"

    def _extract_keywords(self, rel_path: str, path: Path) -> list[str]:
        lower = rel_path.lower()
        keywords: list[str] = []
        for role, terms in ROLE_KEYWORDS.items():
            if any(term in lower for term in terms):
                keywords.append(role)
        if path.name.startswith("test_"):
            keywords.append("test")
        if path.name.endswith(".thy"):
            keywords.append("hol")
        if path.name.endswith(".py"):
            keywords.append("python")
        if path.name.endswith(".md"):
            keywords.append("doc")
        if "spectral" in lower or "prime" in lower or "zeta" in lower:
            keywords.append("spectral")
        if "multiloop" in lower or "critic" in lower or "refinement" in lower:
            keywords.append("multiloop")
        if "rag" in lower or "memoire" in lower or "memory" in lower:
            keywords.append("memory")
        if "vision" in lower or "image" in lower:
            keywords.append("vision")
        return keywords

    def _extract_python_imports(self, path: Path) -> list[str]:
        if path.suffix.lower() != ".py":
            return []
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return []
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return []

        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports

    def _compute_score(self, rel_path: str, keywords: list[str], imports: list[str], path: Path) -> float:
        score = 1.0
        lower = rel_path.lower()
        if "src" in lower or "core" in lower:
            score += 4.0
        if "multiloop" in lower or "spectral" in lower or "hol" in lower:
            score += 5.5
        if "main.py" in lower or "pipeline" in lower or "orchestr" in lower:
            score += 7.0
        if path.name.startswith("test_"):
            score += 1.5
        if lower.endswith(".md"):
            score += 0.7
        score += 0.6 * len(keywords)
        score += 0.25 * len(imports)
        return round(score, 3)

    def build_database(self, files: list[FileScanResult]) -> dict[str, int]:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")

        conn.execute("DROP TABLE IF EXISTS file_edges")
        conn.execute("DROP TABLE IF EXISTS files")
        conn.execute("DROP TABLE IF EXISTS snapshots")

        conn.execute(
            """
            CREATE TABLE files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE,
                rel_path TEXT NOT NULL,
                extension TEXT,
                file_type TEXT,
                role TEXT,
                size_bytes INTEGER,
                modified_iso TEXT,
                keywords TEXT,
                imports TEXT,
                score REAL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE file_edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                src_path TEXT NOT NULL,
                dst_path TEXT NOT NULL,
                relation TEXT NOT NULL,
                weight REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                generated_at TEXT NOT NULL,
                repo_root TEXT NOT NULL,
                total_files INTEGER NOT NULL,
                total_edges INTEGER NOT NULL,
                summary_json TEXT NOT NULL
            )
            """
        )

        for item in files:
            conn.execute(
                """
                INSERT INTO files (
                    path, rel_path, extension, file_type, role, size_bytes,
                    modified_iso, keywords, imports, score, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.path,
                    item.rel_path,
                    item.extension,
                    item.file_type,
                    item.role,
                    item.size_bytes,
                    item.modified_iso,
                    json.dumps(item.keywords, ensure_ascii=False),
                    json.dumps(item.imports, ensure_ascii=False),
                    item.score,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )

        # Creation des liens structuraux: imports locaux, co-rôles, chemins proches.
        module_map = {f.rel_path.replace("\\", "/"): f for f in files}
        module_names = {
            f.rel_path.replace("\\", "/").replace("/", ".").rsplit(".", 1)[0] if "." in f.rel_path else f.rel_path.replace("\\", "/").replace("/", ".")
            : f.rel_path.replace("\\", "/")
            for f in files if f.file_type == "python"
        }

        for item in files:
            for sql_import in item.imports:
                resolved = self._resolve_import(sql_import, item.rel_path, module_names)
                if not resolved:
                    continue
                conn.execute(
                    """
                    INSERT INTO file_edges (src_path, dst_path, relation, weight, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (item.rel_path.replace("\\", "/"), resolved, "import", 2.0, datetime.now(timezone.utc).isoformat()),
                )

            # liaisons par chevrons structurels et role commun
            for other in files:
                if other.rel_path == item.rel_path:
                    continue
                if item.role == other.role and item.role in {"core", "multiloop", "spectral", "hol", "ui"}:
                    conn.execute(
                        """
                        INSERT INTO file_edges (src_path, dst_path, relation, weight, created_at)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (item.rel_path.replace("\\", "/"), other.rel_path.replace("\\", "/"), "role_cluster", 0.7, datetime.now(timezone.utc).isoformat()),
                    )

        conn.commit()
        total_files = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
        total_edges = conn.execute("SELECT COUNT(*) FROM file_edges").fetchone()[0]

        summary = {
            "repo_root": self.repo_root.as_posix(),
            "total_files": total_files,
            "total_edges": total_edges,
            "top_roles": self._top_roles(conn),
            "top_files": self._top_files(conn),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        conn.execute(
            "INSERT INTO snapshots (generated_at, repo_root, total_files, total_edges, summary_json) VALUES (?, ?, ?, ?, ?)",
            (summary["generated_at"], summary["repo_root"], total_files, total_edges, json.dumps(summary, ensure_ascii=False)),
        )
        conn.commit()
        conn.close()
        return summary

    def _resolve_import(self, import_name: str, current_rel_path: str, module_names: dict[str, str]) -> str | None:
        current_dir = str(Path(current_rel_path).parent).replace("\\", "/")
        # 1. import direct du module complet
        candidates = [
            import_name,
            import_name.replace(".", "/"),
            (current_dir + "/" + import_name).replace("\\", "/"),
            (current_dir + "/" + import_name.replace(".", "/")).replace("\\", "/"),
        ]
        for candidate in candidates:
            normalized = candidate.replace("\\", "/")
            if normalized.endswith(".py"):
                normalized = normalized[:-3]
            if normalized in module_names:
                return module_names[normalized]
            if normalized.startswith("src/") and normalized[:-3].split("/")[-1] in module_names:
                pass

        # 2. tentative de resolution simple depuis le module python local
        if import_name.startswith("src."):
            module = import_name[4:]
            normalized = module.replace(".", "/")
            for suffix in ["", ".py"]:
                candidate = f"src/{normalized}{suffix}"
                if candidate in module_names.values():
                    return candidate
        if import_name.startswith("."):
            return None
        return None

    def _top_roles(self, conn: sqlite3.Connection) -> list[dict[str, object]]:
        rows = conn.execute(
            "SELECT role, COUNT(*) AS c FROM files GROUP BY role ORDER BY c DESC, role ASC LIMIT 10"
        ).fetchall()
        return [{"role": r[0], "count": r[1]} for r in rows]

    def _top_files(self, conn: sqlite3.Connection) -> list[dict[str, object]]:
        rows = conn.execute(
            "SELECT rel_path, role, score FROM files ORDER BY score DESC, rel_path ASC LIMIT 20"
        ).fetchall()
        return [{"path": r[0], "role": r[1], "score": r[2]} for r in rows]

    def print_summary(self, summary: dict[str, object]) -> None:
        print("\n=== Gabriel repository orchestrator ===")
        print(f"repo root : {summary['repo_root']}")
        print(f"total files : {summary['total_files']}")
        print(f"total edges : {summary['total_edges']}")
        print("\nTop roles:")
        for item in summary["top_roles"]:
            print(f"  - {item['role']}: {item['count']}")
        print("\nTop files:")
        for item in summary["top_files"]:
            print(f"  - {item['path']} [{item['role']}] score={item['score']}")


# ═══════════════════════════════════════════════════════════════════════════
#  VARIATEUR MECANIQUE DE PROGRAMMATION
#  Moteur d'application de « contrats de patch » (JSON) guide par la base de
#  cartographie gabriel_repo_map.db. Chaque cible est resolue a partir du
#  reseau fonctionnel (role, mots-cles, score, chemins), chaque fichier touche
#  est sauvegarde avant modification, et un `--rollback` restaure tout.
# ═══════════════════════════════════════════════════════════════════════════

VARIATEUR_VERSION = "1.0"
VARIATEUR_DIR = ".gabriel_variateur"
OPERATIONS_SUPPORTEES = {
    "remplacer_texte", "inserer_lignes", "supprimer_lignes",
    "ajouter_a_la_fin", "creer_fichier", "deployer_fichier", "executer_python",
    "propager_texte",
}
OPERATIONS_ALIASES = {
    "replace_text": "remplacer_texte", "remplacement": "remplacer_texte",
    "replace": "remplacer_texte",
    "insert_lines": "inserer_lignes", "inserer": "inserer_lignes",
    "insert": "inserer_lignes",
    "delete_lines": "supprimer_lignes", "supprimer": "supprimer_lignes",
    "delete": "supprimer_lignes",
    "append": "ajouter_a_la_fin", "ajouter": "ajouter_a_la_fin",
    "append_lines": "ajouter_a_la_fin",
    "create_file": "creer_fichier", "creer": "creer_fichier",
    "deploy_file": "deployer_fichier", "copier": "deployer_fichier",
    "run_python": "executer_python", "python": "executer_python",
    "propager": "propager_texte", "propager_reseau": "propager_texte",
    "propagation": "propager_texte", "transmission": "propager_texte",
}


class VariateurError(Exception):
    """Erreur metier du variateur (cible introuvable, contrat invalide...)."""


def _lire_patch_texte(chemin: Path) -> tuple[str, bool]:
    """Lit un fichier texte en normalisant les fins de ligne (CRLF -> LF)."""
    brut = chemin.read_bytes()
    try:
        txt = brut.decode("utf-8-sig")
    except UnicodeDecodeError:
        txt = brut.decode("latin-1", errors="replace")
    crlf = "\r\n" in txt
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    return txt, crlf


def _ecrire_patch_texte(chemin: Path, txt: str, crlf: bool) -> None:
    """Ecrit un fichier texte en restaurant le style de fins de ligne d'origine."""
    if crlf:
        txt = txt.replace("\n", "\r\n")
    chemin.write_bytes(txt.encode("utf-8"))


class VariateurMecanique:
    """Moteur d'application de patches guide par la base de cartographie.

    Contrat de patch (JSON) :
        {
          "meta": { "nom": ..., "description": ..., "version": "1.0" },
          "operations": [
            {
              "op": "remplacer_texte"              # ou inserer_lignes,
              "cible": "src/core/spectral_core.py", # resolution DB possible
              "mots_cles": ["spectral", "reconstructor"],  # si cible absente
              "role": "core",
              "ancien_texte": ..., "nouveau_texte": ...,   # remplacer
              "ligne_insertion": N,                        # inserer_lignes
              "ligne_debut": N, "ligne_fin": M,            # supprimer_lignes
              "contenu": ...,                              # ecritures divers
              "source": "pipeline_correction/corrections/src/core/...py", # deploy
              "message": "..."
            }
          ]
        }
    """

    def __init__(self, repo_root: Path, db_path: Path):
        self.repo_root = repo_root.resolve()
        self.db_path = db_path.resolve()
        self.dossier_var = self.repo_root / VARIATEUR_DIR
        self.dossier_var.mkdir(parents=True, exist_ok=True)
        self._index: Optional[list[dict]] = None
        self._manifeste: dict[str, dict] = {}
        self._fichiers_crees: list[str] = []
        self._snapshot_dir: Optional[Path] = None
        self._dry_run = False
        self._strict = False
        # Transmission : l'archiviste de correction (module archiviste.py) relie
        # l'orchestrateur au reseau neuronal de la base (mots-cles → adresses).
        self._archiviste: Optional[object] = None
        try:
            from archiviste import ArchivisteCorrection as _ArchivisteCorrection
            self._archiviste = _ArchivisteCorrection(self.db_path, self.repo_root)
        except Exception:
            self._archiviste = None

    def charger_contrat(self, chemin: Path) -> dict:
        if not chemin.exists():
            raise VariateurError(f"Contrat introuvable : {chemin}")
        try:
            contrat = json.loads(chemin.read_text(encoding="utf-8-sig"))
        except Exception as exc:
            raise VariateurError(f"Contrat JSON invalide : {exc}") from exc
        if not isinstance(contrat, dict) or "operations" not in contrat:
            raise VariateurError("Contrat invalide : cle 'operations' (liste) obligatoire.")
        if not isinstance(contrat.get("operations"), list) or not contrat["operations"]:
            raise VariateurError("Contrat invalide : 'operations' doit etre une liste non vide.")
        meta = contrat.get("meta", {})
        version = str(meta.get("version", VARIATEUR_VERSION))
        if version != VARIATEUR_VERSION:
            raise VariateurError(
                f"Version de contrat incompatible : {version} (attendu {VARIATEUR_VERSION})"
            )
        return contrat

    # ─────────────────────────────────────────────────────────────────────────
    #  Index DB (gabriel_repo_map.db)
    # ─────────────────────────────────────────────────────────────────────────

    def _charger_index(self) -> None:
        if self._index is not None:
            return
        lignes: list[dict] = []
        if self.db_path.exists():
            try:
                conn = sqlite3.connect(str(self.db_path))
                conn.row_factory = sqlite3.Row
                lignes = conn.execute(
                    "SELECT rel_path, path, role, score, keywords, file_type FROM files"
                ).fetchall()
                conn.close()
            except sqlite3.Error:
                lignes = []
        index: list[dict] = []
        for r in lignes:
            try:
                mots = json.loads(r["keywords"]) if r["keywords"] else []
            except Exception:
                mots = []
            index.append({
                "rel_path": r["rel_path"],
                "path": r["path"],
                "role": r["role"] or "core",
                "score": float(r["score"] or 1.0),
                "keywords": mots,
                "file_name": r["rel_path"].split("/")[-1],
            })
        self._index = index

    # ─────────────────────────────────────────────────────────────────────────
    #  Resolution des cibles (guidee par la DB)
    # ─────────────────────────────────────────────────────────────────────────

    def _assurer_relatif_sous_repo(self, norm: str) -> str:
        rel = norm if norm else "nouveau_fichier"
        if not rel or rel.startswith("../") or ".." in rel.split("/"):
            rel = "src/" + rel.replace("..", "_").replace(":", "_").lstrip("/")
        return rel

    def _chemin_depuis_relatif(self, cible: str, doit_exister: bool) -> Path:
        norm = cible.replace("\\", "/").lstrip("/")
        cands: list[Path] = []
        abs_p = Path(cible)
        if abs_p.is_absolute():
            cands.append(abs_p)
        cands.append(self.repo_root / norm)
        for c in cands:
            try:
                if c.exists():
                    return c
            except OSError:
                continue
        hit = self._trouver_index_suffixe(norm)
        if hit:
            return Path(hit["path"])
        if not doit_exister:
            rel = self._assurer_relatif_sous_repo(norm)
            return self.repo_root / rel
        raise VariateurError(f"Cible inexistante et introuvable dans la DB : {cible}")

    def _trouver_index_suffixe(self, rel: str) -> Optional[dict]:
        rel = rel.replace("\\", "/").lstrip("/").lower()
        for f in self._index or []:
            if f["rel_path"].lower() == rel:
                return f
        suff = [f for f in self._index or [] if f["rel_path"].lower().endswith("/" + rel)]
        if suff:
            return max(suff, key=lambda f: f["score"])
        base = rel.split("/")[-1]
        bas = [f for f in self._index or [] if f["file_name"] == base]
        if bas:
            return max(bas, key=lambda f: f["score"])
        return None

    def _cible_par_mots_cles(self, op: dict) -> dict:
        mots = [str(m).lower() for m in op.get("mots_cles", [])]
        role = op.get("role")
        candidats = []
        for f in self._index or []:
            if role and f["role"] != role:
                continue
            corpus = " ".join([
                f["rel_path"].lower(), f["role"] or "",
                " ".join(f["keywords"]),
            ])
            if all(m in corpus for m in mots):
                candidats.append(f)
        if not candidats:
            raise VariateurError(
                f"Aucun fichier resolu pour mots_cles={mots} role={role}"
            )
        candidats.sort(key=lambda f: f["score"], reverse=True)
        if len(candidats) > 1 and self._strict:
            raise VariateurError(
                f"Cible ambigue ({len(candidats)}) : "
                + ", ".join(c["rel_path"] for c in candidats[:5])
            )
        return candidats[0]

    def _resoudre_source(self, source: str, patch_dir: Path) -> Path:
        if not source:
            raise VariateurError("deployer_fichier : cle 'source' requise.")
        p = Path(source)
        cands: list[Path] = []
        if p.is_absolute():
            cands.append(p)
        cands += [patch_dir / p, self.repo_root.parent / p, self.repo_root / p]
        for c in cands:
            if c.exists():
                return c
        raise VariateurError(f"Source introuvable pour deploy : {source}")

    def _resoudre_dossier_cible(self, op: dict) -> Path:
        """Resout le dossier d'accueil d'un fichier a creer via la DB."""
        mots = [str(m).lower() for m in op.get("mots_cles", [])]
        if mots:
            for f in self._index or []:
                corpus = " ".join([
                    f["rel_path"].lower(), f["role"] or "",
                    " ".join(f["keywords"]),
                ])
                if all(m in corpus for m in mots):
                    return Path(f["path"]).parent
        if op.get("role") and self._index:
            role_matches = [f for f in self._index if f["role"] == op["role"]]
            if role_matches:
                role_matches.sort(key=lambda f: f["score"], reverse=True)
                return Path(role_matches[0]["path"]).parent
        return self.repo_root

    def _est_sous_repo(self, chemin: Path) -> bool:
        try:
            chemin.resolve().relative_to(self.repo_root)
            return True
        except (ValueError, OSError):
            return False

    def _resoudre_cible(self, op: dict, patch_dir: Path) -> Path:
        op_type = op["op"]
        cible = (op.get("cible") or "").strip()
        if op_type == "deployer_fichier":
            source = self._resoudre_source(op.get("source"), patch_dir)
            if cible:
                # creat_si_absent autorise le deploiement vers une cible inexistante
                return self._chemin_depuis_relatif(cible, doit_exister=not op.get("creer_si_absent", False))
            hit = self._trouver_index_suffixe(source.name)
            if hit:
                return Path(hit["path"])
            if cible or op.get("creer_si_absent"):
                rel = self._assurer_relatif_sous_repo(source.name)
                return self.repo_root / rel
            raise VariateurError(f"Deploy : cible non resolue pour {source}")
        if op_type == "creer_fichier":
            if cible:
                return self._chemin_depuis_relatif(cible, doit_exister=False)
            dossier = self._resoudre_dossier_cible(op)
            nom = op.get("nom_fichier") or "nouveau_fichier.txt"
            return dossier / nom
        if cible:
            return self._chemin_depuis_relatif(cible, doit_exister=True)
        if op.get("mots_cles") or op.get("role"):
            hit = self._cible_par_mots_cles(op)
            return Path(hit["path"])
        raise VariateurError(
            f"Operation {op_type} : cible ou mots_cles/role requis."
        )

    # ─────────────────────────────────────────────────────────────────────────
    #  Sauvegarde / écriture / vérification
    # ─────────────────────────────────────────────────────────────────────────

    def _sauvegarder_fichier(self, cible: Path) -> None:
        """Copie l'etat d'origine d'un fichier avant modification (une seule fois)."""
        rel = self._rel_depot(cible)
        if rel in self._manifeste:
            return
        backup_rel: Optional[str] = None
        existed = cible.exists()
        if existed:
            data = cible.read_bytes()
            sha = hashlib.sha256(data).hexdigest()[:10]
            nom = f"{sha}_{cible.name}.bak"
            dest = self._snapshot_dir / "fichiers" / nom
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            backup_rel = dest.relative_to(self._snapshot_dir).as_posix()
        self._manifeste[rel] = {
            "rel": rel,
            "existed_before": existed,
            "backup_relatif": backup_rel,
        }
        if not existed:
            self._fichiers_crees.append(rel)

    def _rel_depot(self, chemin: Path) -> str:
        try:
            return chemin.resolve().relative_to(self.repo_root).as_posix()
        except ValueError:
            return chemin.as_posix()

    def _verifier_syntaxe(self, cible: Path, contenu: str) -> str:
        """Retourne une chaine vide si OK, sinon le message d'erreur."""
        ext = cible.suffix.lower()
        try:
            if ext == ".py":
                compile(contenu, str(cible), "exec")
            elif ext == ".json":
                json.loads(contenu)
            elif ext in (".yaml", ".yml"):
                try:
                    import yaml  # type: ignore
                    yaml.safe_load(contenu)
                except ImportError:
                    pass
            return ""
        except Exception as exc:
            return f"{type(exc).__name__}: {exc}"

    # ─────────────────────────────────────────────────────────────────────
    #  TRANSMISSION : l'orchestrateur interroge l'archiviste (réseau) puis
    #  applique la correction à TOUS les fichiers impliqués du dépôt.
    # ─────────────────────────────────────────────────────────────────────
    def _editer_fichier(self, op: dict, cible: Path) -> None:
        """Applique une opération d'édition texte à UN fichier (avec copie
        de sauvegarde avant modification + vérification de syntaxe)."""
        if op.get("op") == "creer_fichier":
            contenu = op.get("contenu", "")
            crlf = False
            op_type = "creer_fichier"
        else:
            contenu, crlf = _lire_patch_texte(cible)
            op_type = op["op"]
        if op_type == "remplacer_texte":
            ancien = op.get("ancien_texte", "")
            nouveau = op.get("nouveau_texte", "")
            if not ancien:
                raise VariateurError("remplacer_texte : 'ancien_texte' requis.")
            n = contenu.count(ancien)
            if n == 0:
                raise VariateurError(f"remplacer_texte : ancien texte introuvable (cible {cible})")
            if n > 1 and not op.get("toutes"):
                if self._strict:
                    raise VariateurError(
                        f"remplacer_texte : texte present {n} fois, ajouter 'toutes': true"
                    )
                contenu = contenu.replace(ancien, nouveau, 1)
            else:
                contenu = contenu.replace(ancien, nouveau)
        elif op_type == "inserer_lignes":
            ligne = int(op.get("ligne_insertion", 1))
            lignes = contenu.split("\n")
            bloc = op.get("contenu", "").split("\n")
            pos = max(0, min(ligne - 1, len(lignes)))
            lignes = lignes[:pos] + bloc + lignes[pos:]
            contenu = "\n".join(lignes)
        elif op_type == "supprimer_lignes":
            debut = int(op.get("ligne_debut", 1))
            fin = int(op.get("ligne_fin", debut))
            lignes = contenu.split("\n")
            if debut < 1 or fin > len(lignes):
                raise VariateurError(
                    f"supprimer_lignes : bornes {debut}..{fin} hors fichier ({len(lignes)} lignes)"
                )
            lignes = lignes[: debut - 1] + lignes[fin:]
            contenu = "\n".join(lignes)
        elif op_type == "ajouter_a_la_fin":
            ajout = op.get("contenu", "")
            contenu = (contenu.rstrip("\n") + "\n" if contenu else "") + ajout
        elif op_type == "creer_fichier":
            contenu = op.get("contenu", "")
            crlf = False

        erreur = self._verifier_syntaxe(cible, contenu)
        if erreur:
            raise VariateurError(f"verification syntaxe {cible.name} : {erreur}")
        if not self._dry_run:
            self._sauvegarder_fichier(cible)
            if not cible.parent.exists():
                cible.parent.mkdir(parents=True, exist_ok=True)
            _ecrire_patch_texte(cible, contenu, crlf)

    def _adresses_archiviste(self, op: dict) -> list:
        """Demande à l'archiviste (transmission) les adresses à corriger."""
        if self._archiviste is None:
            raise VariateurError(
                "propager_texte : l'archiviste (archiviste.py, module absent) est "
                "indisponible pour résoudre le réseau."
            )
        mots = [str(m) for m in (op.get("mots_cles") or [])]
        role = op.get("role")
        cible_exp = (op.get("cible") or "").strip() or None
        profondeur = max(1, int(op.get("profondeur", 1)))
        if not mots and not cible_exp:
            raise VariateurError(
                "propager_texte : fournir 'mots_cles' et/ou 'cible' pour le réseau."
            )
        adresses = self._archiviste.reseau_de_correction(
            mots, role=role, profondeur=profondeur, cible_explicite=cible_exp
        )
        if not adresses:
            raise VariateurError("propager_texte : aucune adresse résolue pour le réseau.")
        chemins: list = []
        for ad in adresses:
            rel = ad["rel_path"]
            p = Path(ad["path"]) if ad.get("path") else self.repo_root / rel
            if p.is_file():
                chemins.append(p)
            else:
                chemins.append(self.repo_root / rel)
        return chemins

    def _executer_propagation(self, i: int, op: dict, patch_dir: Path) -> dict:
        """Applique l'opération d'édition à TOUS les fichiers du réseau."""
        rep = {"index": i, "type": op["op"], "message": op.get("message", ""), "statut": "ok"}
        sous = dict(op.get("operation") or op)
        sous.pop("mots_cles", None)
        sous.pop("role", None)
        sous.pop("profondeur", None)
        sous.pop("operation", None)
        sous["message"] = op.get("message", "")
        cibles = self._adresses_archiviste(op)
        touches: list = []
        echecs: list = []
        for cible in cibles:
            try:
                self._editer_fichier(sous, cible)
                touches.append(self._rel_depot(cible))
            except VariateurError as exc:
                echecs.append(f"{self._rel_depot(cible)} : {exc}")
                if self._strict:
                    raise
        rep["cible"] = touches[0] if touches else ""
        rep["cibles_appliquees"] = touches
        rep["echecs"] = echecs
        if self._dry_run:
            rep["statut"] = "simule"
        if not touches:
            raise VariateurError(" - ".join(echecs) if echecs else "aucune application réseau")
        return rep

    def _executer_op(self, i: int, op: dict, patch_dir: Path) -> dict:
        op_type = op["op"]
        rep = {"index": i, "type": op_type, "message": op.get("message", ""), "statut": "ok"}

        if op_type == "executer_python":
            contenu = op.get("contenu", "")
            if not contenu:
                raise VariateurError("executer_python : 'contenu' requis.")
            script = self._snapshot_dir / "exec" / f"op_{i}.py"
            rep["detail"] = f"script de {len(contenu)} caracteres"
            if self._dry_run:
                rep["statut"] = "simule"
                return rep
            script.parent.mkdir(parents=True, exist_ok=True)
            script.write_text(contenu, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=900,
            )
            if proc.returncode != 0:
                raise VariateurError(
                    f"executer_python a echoue (rc={proc.returncode}) : {proc.stderr[-800:]}"
                )
            rep["detail"] = f"rc=0, sortie {len(proc.stdout)} octets"
            return rep

        if op_type == "propager_texte":
            return self._executer_propagation(i, op, patch_dir)

        cible = self._resoudre_cible(op, patch_dir)
        rep["cible"] = self._rel_depot(cible)
        rep["resolu_via"] = "DB" if cible.resolve() != (self.repo_root / cible.name) else "chemin"

        if op_type == "deployer_fichier":
            source = self._resoudre_source(op.get("source"), patch_dir)
            rep["source"] = source.as_posix()
            contenu = source.read_bytes()
            if self._dry_run:
                rep["statut"] = "simule"
            else:
                self._sauvegarder_fichier(cible)
                if not cible.parent.exists():
                    cible.parent.mkdir(parents=True, exist_ok=True)
                cible.write_bytes(contenu)
            return rep

        if op_type == "creer_fichier":
            contenu = op.get("contenu", "")
            crlf = False
        else:
            contenu, crlf = _lire_patch_texte(cible)
            if op_type == "remplacer_texte":
                ancien = op.get("ancien_texte", "")
                nouveau = op.get("nouveau_texte", "")
                if not ancien:
                    raise VariateurError("remplacer_texte : 'ancien_texte' requis.")
                n = contenu.count(ancien)
                if n == 0:
                    raise VariateurError(f"remplacer_texte : ancien texte introuvable (cible {cible})")
                if n > 1 and not op.get("toutes"):
                    if self._strict:
                        raise VariateurError(f"remplacer_texte : texte present {n} fois, ajouter 'toutes': true")
                    contenu = contenu.replace(ancien, nouveau, 1)
                else:
                    contenu = contenu.replace(ancien, nouveau)
            elif op_type == "inserer_lignes":
                ligne = int(op.get("ligne_insertion", 1))
                lignes = contenu.split("\n")
                bloc = op.get("contenu", "").split("\n")
                pos = max(0, min(ligne - 1, len(lignes)))
                lignes = lignes[:pos] + bloc + lignes[pos:]
                contenu = "\n".join(lignes)
            elif op_type == "supprimer_lignes":
                debut = int(op.get("ligne_debut", 1))
                fin = int(op.get("ligne_fin", debut))
                lignes = contenu.split("\n")
                if debut < 1 or fin > len(lignes):
                    raise VariateurError(
                        f"supprimer_lignes : bornes {debut}..{fin} hors fichier ({len(lignes)} lignes)"
                    )
                lignes = lignes[: debut - 1] + lignes[fin:]
                contenu = "\n".join(lignes)
            elif op_type == "ajouter_a_la_fin":
                ajout = op.get("contenu", "")
                contenu = (contenu.rstrip("\n") + "\n" if contenu else "") + ajout

        erreur = self._verifier_syntaxe(cible, contenu)
        if erreur:
            raise VariateurError(f"verification syntaxe {cible.name} : {erreur}")
        if self._dry_run:
            rep["statut"] = "simule"
        else:
            self._sauvegarder_fichier(cible)
            if not cible.parent.exists():
                cible.parent.mkdir(parents=True, exist_ok=True)
            _ecrire_patch_texte(cible, contenu, crlf)
        return rep

    def _ecrire_manifeste(self, contrat_path: Path) -> Optional[str]:
        """Ecrit manifeste.json si modifications reelles effectuees."""
        if self._dry_run or self._snapshot_dir is None:
            return None
        if not self._manifeste:
            return None
        self._snapshot_dir.mkdir(parents=True, exist_ok=True)
        manifeste = {
            "version": VARIATEUR_VERSION,
            "horodatage": datetime.now(timezone.utc).isoformat(),
            "contrat": contrat_path.as_posix(),
            "repo_root": self.repo_root.as_posix(),
            "dossier_sauvegarde": self._snapshot_dir.as_posix(),
            "fichiers": sorted(self._manifeste.values(), key=lambda e: e["rel"]),
        }
        chemin = self._snapshot_dir / "manifeste.json"
        chemin.write_text(json.dumps(manifeste, ensure_ascii=False, indent=2), encoding="utf-8")
        return chemin.as_posix()

    def executer_contrat(
        self, contrat_path: Path, dry_run: bool = False, strict: bool = False
    ) -> dict:
        contrat = self.charger_contrat(contrat_path)
        patch_dir = contrat_path.resolve().parent
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self._snapshot_dir = self.dossier_var / "snapshots" / f"{stamp}_{contrat_path.stem}"
        self._dry_run = dry_run
        self._strict = strict
        self._charger_index()

        rapport = {
            "contrat": contrat_path.as_posix(),
            "horodatage": stamp,
            "dry_run": dry_run,
            "meta": contrat.get("meta", {}),
            "operations": [],
            "defaillances": [],
            "ok": 0,
            "simules": 0,
            "echouees": 0,
            "manifeste": None,
        }
        for i, op_brut in enumerate(contrat["operations"], start=1):
            try:
                op = self._normaliser_op(op_brut)
                res = self._executer_op(i, op, patch_dir)
            except VariateurError as exc:
                res = {
                    "index": i,
                    "type": str(op_brut.get("op")) if isinstance(op_brut, dict) else "?",
                    "statut": "echouee",
                    "raison": str(exc),
                }
                rapport["defaillances"].append(res)
                if strict:
                    raise
            except Exception as exc:  # filet de securite
                res = {
                    "index": i,
                    "type": str(op_brut.get("op")) if isinstance(op_brut, dict) else "?",
                    "statut": "echouee",
                    "raison": f"{type(exc).__name__}: {exc}",
                }
                rapport["defaillances"].append(res)
                if strict:
                    raise

            rapport["operations"].append(res)
            if res["statut"] == "ok":
                rapport["ok"] += 1
            elif res["statut"] == "simule":
                rapport["simules"] += 1
            else:
                rapport["echouees"] += 1

        rapport["manifeste"] = self._ecrire_manifeste(contrat_path)
        return rapport

    @staticmethod
    def _normaliser_op(op: dict) -> dict:
        """Normalise une operation (alias anglais/francais) et valide sa forme."""
        if not isinstance(op, dict):
            raise VariateurError("Operation invalide : objet attendu.")
        brut = op.get("op")
        if not brut:
            raise VariateurError("Operation invalide : cle 'op' manquante.")
        brut = str(brut).strip()
        type_op = OPERATIONS_ALIASES.get(brut, brut)
        if type_op not in OPERATIONS_SUPPORTEES:
            raise VariateurError(f"Operation non supportee : {brut}")
        op = dict(op)
        op["op"] = type_op
        return op

    def restaurer_snapshot(self, dossier: Path, dry_run: bool = False) -> dict:
        """Restaure l'etat exact enregistre dans un snapshot du variateur."""
        dossier = dossier.resolve() if dossier.is_absolute() else (self.repo_root / dossier).resolve()
        if not dossier.exists():
            raise VariateurError(f"Snapshot introuvable : {dossier}")
        manifeste = dossier / "manifeste.json"
        if not manifeste.exists():
            raise VariateurError(f"manifeste.json introuvable : {manifeste}")
        data = json.loads(manifeste.read_text(encoding="utf-8-sig"))
        dossier_fichiers = dossier / "fichiers"
        rapport = {
            "snapshot": dossier.as_posix(),
            "restaures": [],
            "supprimes": [],
            "manquants": [],
            "dry_run": dry_run,
        }
        for entree in sorted(data.get("fichiers", []), key=lambda e: e["rel"], reverse=True):
            dest = self.repo_root / entree["rel"]
            if entree.get("existed_before"):
                srcb_rel = entree.get("backup_relatif")
                # backup_relatif est relatif au DOSSIER du snapshot
                # (ex : "fichiers/abc123_fichier.py.bak")
                srcb = (dossier / srcb_rel) if srcb_rel else None
                if srcb is None or not srcb.exists():
                    rapport["manquants"].append(entree["rel"])
                    continue
                if dry_run:
                    rapport["restaures"].append(entree["rel"])
                    continue
                try:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(str(srcb), str(dest))
                    rapport["restaures"].append(entree["rel"])
                except OSError as exc:
                    rapport["manquants"].append(f"{entree['rel']} ({exc})")
            else:
                # le fichier avait ete cree par le contrat -> on le supprime
                if dry_run:
                    rapport["supprimes"].append(entree["rel"])
                    continue
                if dest.exists():
                    dest.unlink()
                    rapport["supprimes"].append(entree["rel"])
        return rapport

    @staticmethod
    def lister_snapshots(repo_root: Path) -> list[Path]:
        dossier = repo_root / VARIATEUR_DIR / "snapshots"
        if not dossier.exists():
            return []
        return sorted(
            [p for p in dossier.iterdir() if p.is_dir() and (p / "manifeste.json").exists()],
            key=lambda p: p.name,
            reverse=True,
        )

    # --- FIN CLASSE VARIATEUR ---


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gabriel repository orchestrator + variateur")
    parser.add_argument("--root", default=Path(__file__).resolve().parent.as_posix(), help="Chemin du depot local")
    parser.add_argument("--db", default="data/gabriel_repo_map.db", help="Chemin cible vers la base SQLite")
    parser.add_argument("--summary-json", default="data/gabriel_repo_summary.json", help="Sortie JSON du resume")
    parser.add_argument("--rebuild", action="store_true", help="Reconstruit la base et les summaries")
    parser.add_argument(
        "--apply", metavar="CONTRAT.json", default=None,
        help="[VARIATEUR] Applique un contrat de patch (JSON) guide par la DB",
    )
    parser.add_argument(
        "--apply-dry-run", action="store_true",
        help="[VARIATEUR] Simule le contrat sans rien modifier",
    )
    parser.add_argument(
        "--apply-strict", action="store_true",
        help="[VARIATEUR] Echec immediat des la premiere cible non resolue",
    )
    parser.add_argument(
        "--rollback", metavar="DOSSIER_SNAPSHOT", default=None,
        help="[VARIATEUR] Restaure un snapshot (.gabriel_variateur/snapshots/<id>)",
    )
    parser.add_argument(
        "--list-snapshots", action="store_true",
        help="[VARIATEUR] Liste les sauvegardes disponibles",
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    db_path = (repo_root / args.db).resolve() if not Path(args.db).is_absolute() else Path(args.db).resolve()
    summary_path = (repo_root / args.summary_json).resolve() if not Path(args.summary_json).is_absolute() else Path(args.summary_json).resolve()

    # ── Mode VARIATEUR ────────────────────────────────────────────────────
    if args.list_snapshots:
        snaps = VariateurMecanique.lister_snapshots(repo_root)
        print("\n=== Snapshots du variateur ===")
        for s in snaps:
            print(f"  - {s.name}  ({s})")
        if not snaps:
            print("  (aucun snapshot pour le moment)")
        return

    if args.rollback:
        v = VariateurMecanique(repo_root, db_path)
        rapport = v.restaurer_snapshot(Path(args.rollback), dry_run=args.apply_dry_run)
        print(f"\n=== Rollback {rapport['snapshot']} ===")
        print(f"  restaures : {len(rapport['restaures'])}")
        print(f"  supprimes : {len(rapport['supprimes'])}")
        print(f"  manquants : {len(rapport['manquants'])}")
        if rapport["manquants"]:
            print("  ATTENTION fichiers manquants :")
            for m in rapport["manquants"]:
                print(f"    - {m}")
        print(f"  dry_run : {rapport['dry_run']}")
        return

    if args.apply:
        v = VariateurMecanique(repo_root, db_path)
        rapport = v.executer_contrat(
            Path(args.apply).resolve(),
            dry_run=args.apply_dry_run,
            strict=args.apply_strict,
        )
        print("\n=== Variateur : rapport d'application ===")
        print(f"  contrat   : {rapport['contrat']}")
        print(f"  mode      : {'SIMULATION (dry-run)' if rapport['dry_run'] else 'APPLICATION RELLE'}")
        print(f"  ok        : {rapport['ok']}")
        print(f"  simulees  : {rapport['simules']}")
        print(f"  echouees  : {rapport['echouees']}")
        print(f"  manifeste : {rapport['manifeste']}")
        for op in rapport["operations"]:
            etat = op["statut"]
            cible = op.get("cible") or op.get("detail") or ""
            raison = f" — {op['raison']}" if etat == "echouee" and op.get("raison") else ""
            print(f"    [{etat}] #{op['index']} {op['type']} -> {cible}{raison}")
            cibles_reseau = op.get("cibles_appliquees")
            if cibles_reseau and len(cibles_reseau) > 1:
                print(f"           fichiers du reseau concernes : {len(cibles_reseau)}")
                for cr in cibles_reseau:
                    print(f"             • {cr}")
            if op.get("echecs"):
                print(f"           echoues : {len(op['echecs'])}")
        return

    # ── Cartographie standard ─────────────────────────────────────────────
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    orchestrator = RepoOrchestrator(repo_root=repo_root, db_path=db_path)
    files = orchestrator.scan_repo()
    summary = orchestrator.build_database(files)
    orchestrator.print_summary(summary)

    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDB SQLite created: {db_path}")
    print(f"Summary JSON created: {summary_path}")
    print("\nNext step: python orchestrator_main.py --apply <contrat.json> [--apply-dry-run]")
    print("Rappel    : python orchestrator_main.py --list-snapshots / --rollback <snapshot>")


if __name__ == "__main__":
    main()
