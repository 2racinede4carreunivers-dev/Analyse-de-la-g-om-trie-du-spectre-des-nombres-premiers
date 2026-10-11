"""archiveur_timeline.py - Archive les timelines du raisonnement recursif.

But : conserver les questions que la Fiancée de Cline n'a PAS pu resoudre, afin
que (a) elles restent disponibles pour les sessions futures et (b) lorsqu'elles
sont resolues INDIRECTEMENT (plus tard), elles deviennent des PREUVES CITABLES
qui contribuent a valider la geometrie du spectre des nombres premiers
(notamment pour la preuve par l'absurde sur l'exclusivite de P premier, section
critique de methode_spectral.thy).

Stockage : SQLite (stdlib) dans data/learning/timelines_recursives.db.
ADDITIF : aucune dependance externe.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

RACINE_DEPOT = Path(__file__).resolve().parents[3]
DOSSIER_DB = RACINE_DEPOT / "data" / "learning"
CHEMIN_DB = DOSSIER_DB / "timelines_recursives.db"


_SCHEMA = """
CREATE TABLE IF NOT EXISTS timelines (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    horodatage      TEXT NOT NULL,
    requete         TEXT NOT NULL,
    divisions       TEXT,
    ancres          TEXT,
    question_modeste TEXT,
    reponse         TEXT,
    blocage         TEXT,
    resolue         INTEGER DEFAULT 0,
    citable         INTEGER DEFAULT 0,
    session_id      TEXT
);
CREATE INDEX IF NOT EXISTS idx_tl_resolue ON timelines(resolue);
"""


class ArchiveurTimeline:
    """Persistance des timelines du 8e moteur (raisonnement recursif)."""

    def __init__(self, chemin: str | Path | None = None):
        self.chemin = Path(chemin) if chemin else CHEMIN_DB
        self.chemin.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.chemin)

    def _init_schema(self) -> None:
        with self._conn() as conn:
            conn.executescript(_SCHEMA)

    def archiver(
        self,
        requete: str,
        question_modeste: str,
        reponse: Optional[str] = None,
        blocage: str = "",
        divisions: Optional[list[str]] = None,
        ancres: Optional[list[str]] = None,
        resolue: bool = False,
        session_id: str = "",
    ) -> int:
        """Archive une timeline ; retourne son identifiant."""
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO timelines (horodatage, requete, divisions, ancres, "
                "question_modeste, reponse, blocage, resolue, citable, session_id) "
                "VALUES (?,?,?,?,?,?,?,?,?,?)",
                (
                    datetime.now(timezone.utc).isoformat(),
                    requete,
                    json.dumps(divisions or [], ensure_ascii=False),
                    json.dumps(ancres or [], ensure_ascii=False),
                    question_modeste,
                    reponse,
                    blocage,
                    1 if resolue else 0,
                    1 if (resolue and reponse) else 0,
                    session_id,
                ),
            )
            return int(cur.lastrowid)

    def marquer_resolue(self, timeline_id: int, reponse: str) -> None:
        """Marque une timeline comme resolue (=> devient citable)."""
        with self._conn() as conn:
            conn.execute(
                "UPDATE timelines SET resolue=1, citable=1, reponse=? WHERE id=?",
                (reponse, timeline_id),
            )

    def _ligne_vers_dict(self, row: tuple) -> dict[str, Any]:
        (i, horo, req, div, anc, qm, rep, blo, resolue, citable, sess) = row
        return {
            "id": i,
            "horodatage": horo,
            "requete": req,
            "divisions": json.loads(div or "[]"),
            "ancres": json.loads(anc or "[]"),
            "question_modeste": qm,
            "reponse": rep,
            "blocage": blo,
            "resolue": bool(resolue),
            "citable": bool(citable),
            "session_id": sess,
        }

    def lister_non_resolues(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id,horodatage,requete,divisions,ancres,question_modeste,"
                "reponse,blocage,resolue,citable,session_id FROM timelines "
                "WHERE resolue=0 ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._ligne_vers_dict(r) for r in rows]

    def rechercher(self, mots: list[str], limit: int = 5) -> list[dict[str, Any]]:
        """Recherche des timelines resolues/similaires (reutilisation inter-session)."""
        if not mots:
            return []
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id,horodatage,requete,divisions,ancres,question_modeste,"
                "reponse,blocage,resolue,citable,session_id FROM timelines "
                "ORDER BY id DESC LIMIT 500",
            ).fetchall()
        resultats: list[tuple[int, dict[str, Any]]] = []
        cible = {m.lower() for m in mots}
        for r in rows:
            d = self._ligne_vers_dict(r)
            texte = (d["requete"] + " " + d["question_modeste"]).lower()
            score = sum(1 for m in cible if m in texte)
            if score > 0:
                resultats.append((score, d))
        resultats.sort(key=lambda x: (x[0], x[1]["citable"]), reverse=True)
        return [d for _, d in resultats[:limit]]

    def statistiques(self) -> dict[str, Any]:
        with self._conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM timelines").fetchone()[0]
            resolues = conn.execute(
                "SELECT COUNT(*) FROM timelines WHERE resolue=1"
            ).fetchone()[0]
            citables = conn.execute(
                "SELECT COUNT(*) FROM timelines WHERE citable=1"
            ).fetchone()[0]
        return {"total": total, "resolues": resolues,
                "non_resolues": total - resolues, "citables": citables}


__all__ = ["ArchiveurTimeline", "CHEMIN_DB"]