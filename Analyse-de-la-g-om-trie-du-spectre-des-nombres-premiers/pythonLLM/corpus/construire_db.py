# -*- coding: utf-8 -*-
"""
corpus/construire_db.py — construit la base SQLite du corpus normatif.

Cree (ou recree) un fichier ``.db`` contenant le corpus encode. Le schema suit
les conventions du depot (``PRAGMA foreign_keys``, ``journal_mode=WAL``,
horodatage ``datetime('now')``). La base est la source de verite que le moteur
interroge au moment de la reconnaissance.

Usage :
    python -m pythonLLM.corpus.construire_db [chemin_sortie.db]
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Optional

from .corpus_computationnel import (
    CHAMPS,
    INSTITUTIONS,
    INVARIANTS,
    REGLES_INTENTION,
    TOUTES_NOTIONS,
)
from .institutions import PROVENANCE

# Notions issues des sources ouvertes verifiees (module GENERE) : W3C SKOS,
# AI Act, RGPD — chacune avec provenance exacte et SHA-256 en snapshots/.
try:
    from .sources_ouvertes import NOTIONS as NOTIONS_SOURCES_OUVERTES
except ImportError:  # module non genere : enrichissement abstenu, jamais simule
    NOTIONS_SOURCES_OUVERTES = ()

DDL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS champs (
    code         TEXT PRIMARY KEY,
    libelle      TEXT NOT NULL,
    poids        INTEGER NOT NULL UNIQUE,
    description  TEXT
);

CREATE TABLE IF NOT EXISTS institutions (
    identifiant      TEXT PRIMARY KEY,
    nom              TEXT NOT NULL,
    type_institution TEXT NOT NULL,
    autorite         INTEGER NOT NULL,
    perimetre        TEXT,
    licence          TEXT,
    acces            TEXT,
    url              TEXT
);

CREATE TABLE IF NOT EXISTS notions (
    lemme       TEXT PRIMARY KEY,
    champ_code  TEXT NOT NULL REFERENCES champs(code) ON DELETE CASCADE,
    source_id   TEXT REFERENCES institutions(identifiant),
    graphe      INTEGER NOT NULL DEFAULT 0,
    definition  TEXT
);
CREATE INDEX IF NOT EXISTS idx_notions_champ ON notions(champ_code);

CREATE TABLE IF NOT EXISTS invariants (
    code       TEXT PRIMARY KEY,
    champ_code TEXT NOT NULL REFERENCES champs(code) ON DELETE CASCADE,
    enonce     TEXT NOT NULL,
    severite   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS regles_intention (
    priorite        INTEGER PRIMARY KEY,
    intention       TEXT NOT NULL,
    condition       TEXT NOT NULL,
    champ_requis    TEXT REFERENCES champs(code),
    mots_declencheurs TEXT
);

CREATE TABLE IF NOT EXISTS meta (
    cle   TEXT PRIMARY KEY,
    valeur TEXT
);
"""


def racine_mathlib() -> Optional[Path]:
    """Localise le depot Mathlib sans inventer : candidats fixes, testes un a un.

    Ordre deterministe : variable d'environnement PYTHONLLM_MATHLIB, puis
    ~/OneDrive/Mathlib, ~/mathlib4, C:/mathlib4. Retourne None si introuvable
    (l'enrichissement Mathlib est alors simplement abstenu, jamais simule).
    """
    import os
    explicite = os.environ.get("PYTHONLLM_MATHLIB")
    candidats = []
    if explicite:
        candidats.append(Path(explicite))
    home = Path.home()
    candidats.extend([home / "OneDrive" / "Mathlib", home / "mathlib4", Path("C:/mathlib4")])
    for c in candidats:
        if (c / "Mathlib.lean").exists():
            return c
    return None


def _notions_mathlib() -> list[tuple[str, str, str]]:
    """Extraction deterministe depuis le depot Mathlib local (licence Apache 2.0).

    Retourne (lemme, champ, provenance fichier:ligne). Liste vide si le depot
    est absent : aucune notion n'est inventee hors source reelle.
    """
    racine = racine_mathlib()
    if racine is None:
        return []
    from .extraire_mathlib import extraire
    return list(extraire(racine))


def construire(chemin: Path) -> Path:
    """Construit la base au chemin donne et retourne ce chemin."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    # Suppression robuste (le fichier peut etre verrouille ou tronque par un
    # chargement anterieur) : on retire aussi les fichiers WAL/SHM.
    for suffixe in ("", "-wal", "-shm"):
        candidat = Path(str(chemin) + suffixe)
        if candidat.exists():
            candidat.unlink()
    conn = sqlite3.connect(str(chemin))
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.executescript(DDL)

        conn.executemany(
            "INSERT INTO champs(code,libelle,poids,description) VALUES (?,?,?,?)",
            [(c.code, c.libelle, c.poids, c.description) for c in CHAMPS],
        )
        conn.executemany(
            "INSERT INTO institutions(identifiant,nom,type_institution,autorite,"
            "perimetre,licence,acces,url) VALUES (?,?,?,?,?,?,?,?)",
            [(i.identifiant, i.nom, i.type_institution, i.autorite, i.perimetre,
              *(PROVENANCE.get(i.identifiant, ("", "", ""))))
             for i in INSTITUTIONS],
        )
        conn.executemany(
            "INSERT INTO notions(lemme,champ_code,source_id,graphe,definition)"
            " VALUES (?,?,?,?,?)",
            [(n.lemme, n.champ_code, n.source_id, 1 if n.graphe else 0, n.definition)
             for n in TOUTES_NOTIONS],
        )
        # Enrichissement Mathlib : notions extraites REELLEMENT des .lean du
        # depot local (Apache 2.0), avec provenance fichier:ligne. INSERT OR
        # IGNORE : le corpus redige a la main (101 notions) garde la priorite
        # en cas d'egalite de lemme. Depot absent -> rien (jamais simule).
        notions_mathlib = _notions_mathlib()
        conn.executemany(
            "INSERT OR IGNORE INTO notions(lemme,champ_code,source_id,graphe,definition)"
            " VALUES (?,?,?,?,?)",
            [(lemme, champ, "MATHLIB", 0, provenance)
             for lemme, champ, provenance in notions_mathlib],
        )
        # Sources ouvertes verifiees (W3C SKOS, AI Act, RGPD) : memes regles
        # de priorite — le corpus manuel garde la main sur un lemme egal.
        conn.executemany(
            "INSERT OR IGNORE INTO notions(lemme,champ_code,source_id,graphe,definition)"
            " VALUES (?,?,?,?,?)",
            [(lemme, champ, source_id, 0, provenance)
             for lemme, champ, source_id, provenance in NOTIONS_SOURCES_OUVERTES],
        )
        conn.executemany(
            "INSERT INTO invariants(code,champ_code,enonce,severite) VALUES (?,?,?,?)",
            [(v.code, v.champ_code, v.enonce, v.severite) for v in INVARIANTS],
        )
        conn.executemany(
            "INSERT INTO regles_intention(priorite,intention,condition,champ_requis,mots_declencheurs)"
            " VALUES (?,?,?,?,?)",
            [(r.priorite, r.intention, r.condition, r.champ_requis,
              " ".join(r.mots_declencheurs)) for r in REGLES_INTENTION],
        )
        mathlib_inseres = conn.execute(
            "SELECT COUNT(*) FROM notions WHERE source_id = 'MATHLIB'"
        ).fetchone()[0]
        ouvertes_inseres = conn.execute(
            "SELECT COUNT(*) FROM notions WHERE source_id IN"
            " ('W3C','UE-AI-ACT','UE-RGPD','SMC-CMC')"
        ).fetchone()[0]
        # Empreintes SHA-256 des documents sources (fiche snapshots/).
        meta_docs: list[tuple[str, str]] = []
        fiche = Path(__file__).resolve().parent / "snapshots" / "SOURCES.sha256"
        if fiche.exists():
            identifiant = None
            for ligne in fiche.read_text(encoding="utf-8").splitlines():
                if ligne.startswith("# "):
                    identifiant = ligne[2:].split(" — ")[0].strip()
                elif ligne.startswith("sha256:") and identifiant:
                    meta_docs.append((f"doc_sha256:{identifiant}", ligne[8:].strip()))
                    identifiant = None
        conn.executemany(
            "INSERT INTO meta(cle,valeur) VALUES (?,?)",
            [
                ("schema", "pythonllm-corpus-1.2.0"),
                ("nb_notions", str(len(TOUTES_NOTIONS))),
                ("nb_notions_total", str(conn.execute(
                    "SELECT COUNT(*) FROM notions").fetchone()[0])),
                ("nb_notions_mathlib", str(mathlib_inseres)),
                ("nb_notions_sources_ouvertes", str(ouvertes_inseres)),
                ("racine_mathlib", str(racine_mathlib() or "(absente)")),
                ("nb_champs", str(len(CHAMPS))),
                ("nb_institutions", str(len(INSTITUTIONS))),
                ("nb_invariants", str(len(INVARIANTS))),
                *meta_docs,
            ],
        )
        conn.commit()
    finally:
        conn.close()
    return chemin


def _principal() -> int:
    racine = Path(__file__).resolve().parents[2]
    cible = Path(sys.argv[1]) if len(sys.argv) > 1 else racine / "pythonLLM" / "corpus" / "corpus_computationnel.db"
    p = construire(cible)
    print(f"Base SQLite creee : {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_principal())
