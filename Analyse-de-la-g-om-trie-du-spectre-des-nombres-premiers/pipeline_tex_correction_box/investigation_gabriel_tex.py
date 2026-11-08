"""
investigation_gabriel_tex.py — Application des règles de compilation LaTeX.

Ce module lit les résultats de l'analyse (``relever_CMD_tex.db``) et les règles
de compilation (``miktex_compilation_rules.db``), puis produit une liste de
drapeaux d'erreur (``investigation_flags.db``).
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path

# ── Données ──────────────────────────────────────────────────────────────────

@dataclass
class InvestigationFlag:
    """Un drapeau d'erreur détecté lors de l'investigation."""
    rule_id: str
    severity: str
    line_num: int
    col_num: int
    description: str
    token_seq: int | None = None
    env_name: str | None = None


# ── Détection d'erreurs ──────────────────────────────────────────────────────

def detect_unclosed_environments(db_path: Path) -> list[InvestigationFlag]:
    """
    Détecte les environnements non fermés depuis la base d'analyse.

    Parameters
    ----------
    db_path : Path
        Chemin vers ``relever_CMD_tex.db``.

    Returns
    -------
    list[InvestigationFlag]
        Drapeaux pour chaque environnement non fermé.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute(
        "SELECT env_name, begin_line, begin_col, begin_seq "
        "FROM environments WHERE closed = 0 AND end_seq IS NULL "
        "ORDER BY begin_line"
    )
    flags: list[InvestigationFlag] = []
    TBOX_ENVS = {
        "boitenote", "boitealerte", "boitecalc", "boiteexo",
        "boitedef", "boitereference", "boiteex", "boite",
        "tcolorbox",
    }
    for env_name, line, col, seq in cursor.fetchall():
        rule_id = "R_TCOLORBOX_CLOSE" if env_name.lower() in TBOX_ENVS else "R_BALANCED_ENVS"
        flags.append(InvestigationFlag(
            rule_id=rule_id,
            severity="ERROR",
            line_num=line,
            col_num=col,
            description=(
                f"Environnement '{env_name}' non fermé — "
                f"ajouter \\end{{{env_name}}} avant \\end{{document}}"
            ),
            token_seq=seq,
            env_name=env_name,
        ))

    conn.close()
    return flags


def detect_bare_backslashes(db_path: Path) -> list[InvestigationFlag]:
    """
    Détecte les backslashes isolés (\\\\ seul sur une ligne) depuis la base
    d'analyse.

    Parameters
    ----------
    db_path : Path
        Chemin vers ``relever_CMD_tex.db``.

    Returns
    -------
    list[InvestigationFlag]
        Drapeaux pour chaque backslash isolé.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute(
        "SELECT token_seq, line_num, col_num, extra_json "
        "FROM commands WHERE command_name = '' "
        "ORDER BY line_num"
    )
    flags: list[InvestigationFlag] = []
    for seq, line, col, extra_json in cursor.fetchall():
        extra = json.loads(extra_json) if extra_json else {}
        if extra.get("is_bare_backslash"):
            flags.append(InvestigationFlag(
                rule_id="R_NO_BARE_BACKSLASH",
                severity="ERROR",
                line_num=line,
                col_num=col,
                description=(
                    "Backslash isolé (\\\\ seul sur une ligne) — "
                    "provoque 'There's no line here to end'. "
                    "Remplacer par une ligne vide ou retirer."
                ),
                token_seq=seq,
            ))

    conn.close()
    return flags



def detect_brace_imbalance(db_path: Path) -> list[InvestigationFlag]:
    """
    Détecte un déséquilibre d'accolades en fin de document.

    Parameters
    ----------
    db_path : Path
        Chemin vers ``relever_CMD_tex.db``.

    Returns
    -------
    list[InvestigationFlag]
        Drapeau si la profondeur d'accolades finale != 0.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM meta WHERE key = 'brace_depth_final'")
    row = cursor.fetchone()
    conn.close()

    if row and int(row[0]) != 0:
        return [InvestigationFlag(
            rule_id="R_BRACE_BALANCE",
            severity="ERROR",
            line_num=0,
            col_num=0,
            description=(
                f"Profondeur d'accolades finale = {row[0]} (attendu: 0). "
                "Il manque ou il y a trop d'accolades fermantes."
            ),
        )]
    return []


def detect_document_structure(db_path: Path) -> list[InvestigationFlag]:
    """
    Vérifie que le document a \\begin{document} et \\end{document}.

    La recherche s'effectue dans la table ``environments`` car les commandes
    ``begin``/``end`` ne sont pas insérées dans la table ``commands``.

    Parameters
    ----------
    db_path : Path
        Chemin vers ``relever_CMD_tex.db``.

    Returns
    -------
    list[InvestigationFlag]
        Drapeaux si la structure document est incomplète.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    flags: list[InvestigationFlag] = []

    cursor.execute(
        "SELECT begin_line, begin_col FROM environments "
        "WHERE env_name = 'document' "
        "ORDER BY begin_line LIMIT 1"
    )
    if not cursor.fetchone():
        flags.append(InvestigationFlag(
            rule_id="R_DOCUMENT_STRUCTURE",
            severity="ERROR",
            line_num=0,
            col_num=0,
            description="\\begin{document} manquant",
        ))

    cursor.execute(
        "SELECT end_line FROM environments "
        "WHERE env_name = 'document' AND closed = 1 "
        "ORDER BY end_line DESC LIMIT 1"
    )
    if not cursor.fetchone():
        flags.append(InvestigationFlag(
            rule_id="R_DOCUMENT_STRUCTURE",
            severity="ERROR",
            line_num=0,
            col_num=0,
            description="\\end{document} manquant",
        ))

    conn.close()
    return flags


def investigate(db_path: Path) -> list[InvestigationFlag]:
    """
    Exécute toutes les détections d'erreurs et retourne la liste agrégée.

    Parameters
    ----------
    db_path : Path
        Chemin vers ``relever_CMD_tex.db``.

    Returns
    -------
    list[InvestigationFlag]
        Tous les drapeaux d'erreur détectés.
    """
    flags: list[InvestigationFlag] = []
    flags.extend(detect_unclosed_environments(db_path))
    flags.extend(detect_bare_backslashes(db_path))
    flags.extend(detect_brace_imbalance(db_path))
    flags.extend(detect_document_structure(db_path))
    return flags




# ── Persistance ──────────────────────────────────────────────────────────────

def save_investigation_flags(flags: list[InvestigationFlag], db_path: Path) -> None:
    """
    Sauvegarde les drapeaux d'erreur dans une base SQLite.

    Parameters
    ----------
    flags : list[InvestigationFlag]
        Drapeaux à sauvegarder.
    db_path : Path
        Chemin vers le fichier de base de données à créer.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE investigation_flags (
            flag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id TEXT,
            severity TEXT,
            line_num INTEGER,
            col_num INTEGER,
            description TEXT,
            token_seq INTEGER,
            env_name TEXT
        )
    """)

    for flag in flags:
        cursor.execute(
            "INSERT INTO investigation_flags VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
            (flag.rule_id, flag.severity, flag.line_num, flag.col_num,
             flag.description, flag.token_seq, flag.env_name),
        )

    conn.commit()
    conn.close()


def load_investigation_flags(db_path: Path) -> list[InvestigationFlag]:
    """
    Charge les drapeaux d'erreur depuis la base SQLite.

    Parameters
    ----------
    db_path : Path
        Chemin vers la base de données.

    Returns
    -------
    list[InvestigationFlag]
        Drapeaux chargés.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT rule_id, severity, line_num, col_num, description, "
        "token_seq, env_name FROM investigation_flags ORDER BY line_num, col_num"
    )
    flags = [
        InvestigationFlag(
            rule_id=row[0],
            severity=row[1],
            line_num=row[2],
            col_num=row[3],
            description=row[4],
            token_seq=row[5],
            env_name=row[6],
        )
        for row in cursor.fetchall()
    ]
    conn.close()
    return flags


# ── Entrée principale ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    analysis_db = repo_root / "pipeline_tex_correction_box" / "data" / "relever_CMD_tex_v2.db"
    output_db = repo_root / "pipeline_tex_correction_box" / "data" / "investigation_flags.db"

    flags = investigate(analysis_db)
    save_investigation_flags(flags, output_db)

    print(f"Investigation terminée : {len(flags)} drapeau(x) détecté(s)")
    for flag in flags:
        print(f"  L{flag.line_num}:{flag.col_num} [{flag.severity}] "
              f"{flag.rule_id}: {flag.description}")
