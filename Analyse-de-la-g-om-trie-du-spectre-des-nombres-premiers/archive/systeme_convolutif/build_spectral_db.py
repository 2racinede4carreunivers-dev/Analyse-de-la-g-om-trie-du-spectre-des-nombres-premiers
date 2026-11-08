# -*- coding: utf-8 -*-
"""
Construit la base de données SQLite formelle du système convolutif spectral,
généralisée à l'ensemble des rapports non typiques 1/k (k entier >= 3).

Tables produites :
  rapports            : catalogue des rapports 1/k pris en charge
  termes_convolution  : table de convolution formelle (c1*k^e1 + c2*k^e2) par
                        rapport, suite (A/B), ordre et n de référence
  sommes              : sommes A(k,n) et B(k,n) évaluées pour chaque (k,n)
                        demandé, avec vérification croisée forme close /
                        somme terme à terme
  digamma_essais      : les 4 essais Digamma par (k,n) avec statut premier
  catalogue_digamma   : la règle Digamma retenue (position, signe) par (k,n)
                        quand plusieurs candidats premiers existent
  reconstructions     : résultat final retenu (premier reconstruit, rang)

Usage: python build_spectral_db.py
"""

import sqlite3
from pathlib import Path

from spectral_engine import (
    termes_suite, sumA, sumB, candidats_digamma, CATALOGUE_DIGAMMA,
    reconstruire_premier, _prime_rank,
)

DB_PATH = Path(__file__).parent / "systeme_convolutif_spectral.sqlite"

SCHEMA = """
CREATE TABLE IF NOT EXISTS rapports (
    k INTEGER PRIMARY KEY,
    rapport TEXT NOT NULL,
    statut TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS termes_convolution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    k INTEGER NOT NULL,
    n_reference INTEGER NOT NULL,
    suite TEXT NOT NULL CHECK (suite IN ('A','B')),
    ordre INTEGER NOT NULL,
    coeff1 INTEGER NOT NULL,
    exposant1 INTEGER NOT NULL,
    coeff2 INTEGER NOT NULL,
    exposant2 INTEGER NOT NULL,
    valeur INTEGER NOT NULL,
    expression TEXT NOT NULL,
    FOREIGN KEY (k) REFERENCES rapports(k)
);

CREATE TABLE IF NOT EXISTS sommes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    k INTEGER NOT NULL,
    n INTEGER NOT NULL,
    somme_a_terme_a_terme INTEGER,
    somme_a_forme_close TEXT NOT NULL,
    somme_b_terme_a_terme INTEGER,
    somme_b_forme_close TEXT NOT NULL,
    coherent INTEGER NOT NULL,
    UNIQUE(k, n),
    FOREIGN KEY (k) REFERENCES rapports(k)
);

CREATE TABLE IF NOT EXISTS digamma_essais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    k INTEGER NOT NULL,
    n INTEGER NOT NULL,
    position INTEGER NOT NULL,
    signe INTEGER NOT NULL,
    digamma_calcule TEXT NOT NULL,
    p_candidat TEXT NOT NULL,
    est_entier INTEGER NOT NULL,
    est_premier INTEGER NOT NULL,
    rang_premier INTEGER,
    FOREIGN KEY (k) REFERENCES rapports(k)
);

CREATE TABLE IF NOT EXISTS catalogue_digamma (
    k INTEGER NOT NULL,
    n INTEGER NOT NULL,
    position_relative INTEGER NOT NULL,
    signe INTEGER NOT NULL,
    PRIMARY KEY (k, n)
);

CREATE TABLE IF NOT EXISTS reconstructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    k INTEGER NOT NULL,
    n INTEGER NOT NULL,
    position INTEGER NOT NULL,
    signe INTEGER NOT NULL,
    premier_reconstruit INTEGER NOT NULL,
    rang_premier INTEGER,
    UNIQUE(k, n),
    FOREIGN KEY (k) REFERENCES rapports(k)
);
"""


def build(k_values=range(3, 8), n_values=(9, 10)):
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)

    for k in k_values:
        con.execute(
            "INSERT OR REPLACE INTO rapports (k, rapport, statut) VALUES (?,?,?)",
            (k, f"1/{k}", "Généralisé (formes closes validées)"),
        )

    for k in k_values:
        for n in n_values:
            for suite in ("A", "B"):
                for t in termes_suite(suite, n):
                    con.execute(
                        """INSERT INTO termes_convolution
                           (k, n_reference, suite, ordre, coeff1, exposant1,
                            coeff2, exposant2, valeur, expression)
                           VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (k, n, suite, t.ordre, t.coeff1, t.exposant1,
                         t.coeff2, t.exposant2, t.valeur(k), t.expression()),
                    )

            a_terme = sum(t.valeur(k) for t in termes_suite("A", n))
            b_terme = sum(t.valeur(k) for t in termes_suite("B", n))
            a_close = sumA(k, n)
            b_close = sumB(k, n)
            coherent = int(a_terme == a_close and b_terme == b_close)
            con.execute(
                """INSERT OR REPLACE INTO sommes
                   (k, n, somme_a_terme_a_terme, somme_a_forme_close,
                    somme_b_terme_a_terme, somme_b_forme_close, coherent)
                   VALUES (?,?,?,?,?,?,?)""",
                (k, n, a_terme, str(a_close), b_terme, str(b_close), coherent),
            )

            if n >= 8:
                for c in candidats_digamma(k, n):
                    con.execute(
                        """INSERT INTO digamma_essais
                           (k, n, position, signe, digamma_calcule, p_candidat,
                            est_entier, est_premier, rang_premier)
                           VALUES (?,?,?,?,?,?,?,?,?)""",
                        (k, n, c.position, c.signe, str(c.digamma_calcule),
                         str(c.p_candidat), int(c.est_entier),
                         int(c.est_premier), c.rang_premier),
                    )

    for (k, n), (pos_rel, signe) in CATALOGUE_DIGAMMA.items():
        con.execute(
            """INSERT OR REPLACE INTO catalogue_digamma
               (k, n, position_relative, signe) VALUES (?,?,?,?)""",
            (k, n, pos_rel, signe),
        )

    for k in k_values:
        for n in n_values:
            if n < 8:
                continue
            try:
                c = reconstruire_premier(k, n)
            except ValueError:
                continue
            con.execute(
                """INSERT OR REPLACE INTO reconstructions
                   (k, n, position, signe, premier_reconstruit, rang_premier)
                   VALUES (?,?,?,?,?,?)""",
                (k, n, c.position, c.signe, int(c.p_candidat), c.rang_premier),
            )

    con.commit()
    return con


def rapport_verification(con: sqlite3.Connection):
    print("=== Cohérence sommes (terme à terme vs forme close) ===")
    for row in con.execute("SELECT k,n,coherent FROM sommes ORDER BY k,n"):
        print(f"k={row[0]} n={row[1]}: {'OK' if row[2] else 'INCOHERENT'}")

    print("\n=== Reconstructions des nombres premiers ===")
    for row in con.execute(
        "SELECT k,n,premier_reconstruit,rang_premier FROM reconstructions ORDER BY k,n"
    ):
        print(f"1/{row[0]}, n={row[1]}: premier={row[2]} (rang {row[3]})")


if __name__ == "__main__":
    con = build()
    rapport_verification(con)
    con.close()
    print(f"\nBase créée : {DB_PATH}")
