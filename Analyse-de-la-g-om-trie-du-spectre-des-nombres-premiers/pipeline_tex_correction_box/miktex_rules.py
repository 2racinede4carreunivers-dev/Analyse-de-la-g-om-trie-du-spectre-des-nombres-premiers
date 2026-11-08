"""
miktex_rules.py — Base de règles de compilation LaTeX (style MiKTeX).

Ce module définit les règles structurales qu'un document LaTeX doit respecter
pour compiler sans erreur. Ces règles sont appliquées statiquement (sans
compilateur) sur la séquence tokenisée produite par ``analyste_tex.py``.

Règles couvertes
----------------
  1. R_BALANCED_ENVS : tout \\begin{env} doit avoir un \\end{env} correspondant,
     avec imbrication correcte (pas de chevauchement).
  2. R_NO_BARE_BACKSLASH : un \\ isolé (saut de ligne "nu") n'est autorisé
     qu'en dehors de tout environnement et uniquement entre paragraphes.
  3. R_BRACE_BALANCE : la profondeur d'accolades doit revenir à 0 en fin de
     document.
  4. R_DOCUMENT_STRUCTURE : le document doit commencer par \\begin{document}
     et se terminer par \\end{document}.
  5. R_TCOLORBOX_CLOSE : tout environnement tcolorbox (\\begin{tcolorbox} ou
     \\begin{boitenote}, etc.) doit être fermé avant le \\end{document}.

Chaque règle a un identifiant, un nom, une sévérité, et une description.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

# ── Règles de compilation ───────────────────────────────────────────────────

@dataclass
class CompilationRule:
    """Une règle de compilation LaTeX."""
    rule_id: str
    name: str
    severity: str  # "ERROR", "WARNING", "INFO"
    description: str
    check_sql: str | None = None  # Requête SQL pour détecter les violations


# Règles standards MiKTeX/LaTeX
COMPILATION_RULES: list[CompilationRule] = [
    CompilationRule(
        rule_id="R_BALANCED_ENVS",
        name="Environnements équilibrés",
        severity="ERROR",
        description=(
            "Chaque \\begin{env} doit être fermé par un \\end{env} correspondant, "
            "avec une imbrication correcte (pas de chevauchement d'environnements)."
        ),
    ),
    CompilationRule(
        rule_id="R_NO_BARE_BACKSLASH",
        name="Pas de backslash isolé",
        severity="ERROR",
        description=(
            "Un \\\\ isolé (saut de ligne nu) provoque l'erreur 'There's no line "
            "here to end'. Il doit être remplacé par une ligne vide (paragraphe) "
            "ou retiré."
        ),
    ),
    CompilationRule(
        rule_id="R_BRACE_BALANCE",
        name="Accolades équilibrées",
        severity="ERROR",
        description=(
            "La profondeur d'accolades { } doit revenir à 0 à la fin du document. "
            "Une profondeur non nulle indique une accolade manquante ou excédentaire."
        ),
    ),
    CompilationRule(
        rule_id="R_DOCUMENT_STRUCTURE",
        name="Structure document",
        severity="ERROR",
        description=(
            "Le document doit commencer par \\begin{document} et se terminer par "
            "\\end{document}."
        ),
    ),
    CompilationRule(
        rule_id="R_TCOLORBOX_CLOSE",
        name="Fermeture des boîtes tcolorbox",
        severity="ERROR",
        description=(
            "Chaque environnement de type tcolorbox (boitenote, boitealerte, "
            "boitecalc, etc.) doit être fermé par \\end{...} avant la fin du "
            "document, sinon l'erreur \\begin{tcb@savebox} ... ended by "
            "\\end{document} se produit."
        ),
    ),
]


# ── Persistance ──────────────────────────────────────────────────────────────

def create_miktex_rules_db(db_path: Path) -> None:
    """
    Crée la base de données ``miktex_compilation_rules.db`` contenant toutes
    les règles de compilation.

    Parameters
    ----------
    db_path : Path
        Chemin vers le fichier de base de données à créer.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE compilation_rules (
            rule_id TEXT PRIMARY KEY,
            name TEXT,
            severity TEXT,
            description TEXT,
            check_sql TEXT
        )
    """)

    for rule in COMPILATION_RULES:
        cursor.execute(
            "INSERT INTO compilation_rules VALUES (?, ?, ?, ?, ?)",
            (rule.rule_id, rule.name, rule.severity,
             rule.description, rule.check_sql),
        )

    conn.commit()
    conn.close()


def load_rules(db_path: Path) -> list[CompilationRule]:
    """
    Charge toutes les règles depuis la base de données.

    Parameters
    ----------
    db_path : Path
        Chemin vers la base de données.

    Returns
    -------
    list[CompilationRule]
        Liste des règles chargées.
    """
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute(
        "SELECT rule_id, name, severity, description, check_sql "
        "FROM compilation_rules ORDER BY rule_id"
    )
    rules = [
        CompilationRule(
            rule_id=row[0],
            name=row[1],
            severity=row[2],
            description=row[3],
            check_sql=row[4],
        )
        for row in cursor.fetchall()
    ]
    conn.close()
    return rules


if __name__ == "__main__":
    db_path = Path(__file__).resolve().parent / "data" / "miktex_compilation_rules.db"
    create_miktex_rules_db(db_path)
    print(f"Base de règles créée : {db_path}")
    for rule in load_rules(db_path):
        print(f"  {rule.rule_id} [{rule.severity}]: {rule.name}")
