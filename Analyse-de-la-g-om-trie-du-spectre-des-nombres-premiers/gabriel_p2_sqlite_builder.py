#!/usr/bin/env python3
# =============================================================================
#  gabriel_p2_sqlite_builder.py
#  PIPELINE COGNITIF GABRIEL — ÉTAPE 2
#  Générateur de base de données SQLite cognitive
#
#  Structure : Ensemble = 1  ↔  1/x + 1/t + 1/ms  (Section XIII Pont Savard)
#  Cercles concentriques dans 3 sphères + disque englobant Ensemble
#
#  Dépôt  : C:\agent-multiloop-Gabriel-local-final
#  Entrée : gabriel_keywords_qr_map.json  (sortie étape 1)
#  Sortie : gabriel_corpus.db
#  Usage  : python gabriel_p2_sqlite_builder.py
# =============================================================================

import sqlite3, json, sys
from pathlib import Path
from datetime import datetime

RACINE  = Path(r"C:\agent-multiloop-Gabriel-local-final")
ENTREE  = RACINE / "gabriel_keywords_qr_map.json"
SORTIE  = RACINE / "gabriel_corpus.db"

# ─────────────────────────────────────────────────────────────────────────────
#  SCHÉMA COMPLET — 10 tables + 3 vues + index
# ─────────────────────────────────────────────────────────────────────────────

DDL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ── Table 1 : Sphères (disques concentriques Ensemble)
CREATE TABLE IF NOT EXISTS spheres (
    id              TEXT PRIMARY KEY,
    nom             TEXT NOT NULL,
    equation        TEXT,
    description     TEXT,
    concordance     TEXT,
    rayon           INTEGER,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ── Table 2 : Cercles concentriques (niveaux 1..4 par sphère)
CREATE TABLE IF NOT EXISTS cercles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sphere_id       TEXT NOT NULL REFERENCES spheres(id) ON DELETE CASCADE,
    niveau          INTEGER NOT NULL,
    nom             TEXT NOT NULL,
    description     TEXT,
    UNIQUE(sphere_id, niveau)
);

-- ── Table 3 : Entités HOL (définitions, lemmes, théorèmes, axiomes...)
CREATE TABLE IF NOT EXISTS entites_hol (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nom             TEXT NOT NULL UNIQUE,
    type_hol        TEXT NOT NULL,
    source_fichier  TEXT,
    ligne           INTEGER,
    contexte        TEXT,
    occurrences     INTEGER DEFAULT 1,
    sphere_id       TEXT REFERENCES spheres(id),
    cercle_niveau   INTEGER,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ── Table 4 : Q&R techniques (corpus principal)
CREATE TABLE IF NOT EXISTS qr_techniques (
    id              TEXT PRIMARY KEY,
    niveau          TEXT NOT NULL,
    source_fichier  TEXT,
    question        TEXT NOT NULL,
    resume          TEXT,
    reponse         TEXT,
    categorie       TEXT,
    mots_cles       TEXT,
    spheres         TEXT,
    sphere_primaire TEXT REFERENCES spheres(id),
    nb_entites      INTEGER DEFAULT 0,
    score_base      REAL    DEFAULT 0.8,
    created_at      TEXT DEFAULT (datetime('now'))
);

-- ── Table 5 : Liens Q&R ↔ entités HOL
CREATE TABLE IF NOT EXISTS liens_qr_entite (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    qr_id       TEXT NOT NULL REFERENCES qr_techniques(id) ON DELETE CASCADE,
    entite_id   INTEGER NOT NULL REFERENCES entites_hol(id) ON DELETE CASCADE,
    score       REAL NOT NULL,
    type_lien   TEXT DEFAULT 'semantique',
    UNIQUE(qr_id, entite_id)
);

-- ── Table 6 : Liens inter-entités HOL (graphe de validation croisée)
CREATE TABLE IF NOT EXISTS liens_hol (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       INTEGER NOT NULL REFERENCES entites_hol(id),
    cible_id        INTEGER NOT NULL REFERENCES entites_hol(id),
    relation        TEXT NOT NULL,
    source_fichier  TEXT,
    sphere_source   TEXT REFERENCES spheres(id),
    sphere_cible    TEXT REFERENCES spheres(id),
    UNIQUE(source_id, cible_id, relation)
);

-- ── Table 7 : Fichiers du dépôt Gabriel (gabriel_repo_map.json)
CREATE TABLE IF NOT EXISTS fichiers_depot (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chemin          TEXT NOT NULL UNIQUE,
    nom             TEXT NOT NULL,
    type_fichier    TEXT,
    taille          INTEGER,
    hash_md5        TEXT,
    modifie         TEXT,
    nb_lignes       INTEGER,
    nb_refs         INTEGER DEFAULT 0,
    est_hub         INTEGER DEFAULT 0,
    sphere_associee TEXT REFERENCES spheres(id)
);

-- ── Table 8 : Liens inter-fichiers (graphe de dépendances réelles)
CREATE TABLE IF NOT EXISTS liens_fichiers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id   INTEGER NOT NULL REFERENCES fichiers_depot(id),
    cible_id    INTEGER NOT NULL REFERENCES fichiers_depot(id),
    type_lien   TEXT,
    ligne       INTEGER,
    UNIQUE(source_id, cible_id, type_lien)
);

-- ── Table 9 : Historique des requêtes (archiviste)
CREATE TABLE IF NOT EXISTS sessions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    question_brute      TEXT NOT NULL,
    question_norm       TEXT,
    mots_cles_detectes  TEXT,
    qr_ids_retournees   TEXT,
    entites_activees    TEXT,
    spheres_activees    TEXT,
    moteur_gabriel      TEXT,
    score_confiance     REAL,
    reponse_generee     TEXT,
    timestamp           TEXT DEFAULT (datetime('now'))
);

-- ── Table 10 : Index de mots-clés (recherche rapide)
CREATE TABLE IF NOT EXISTS index_mots_cles (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    mot_cle     TEXT NOT NULL UNIQUE,
    qr_ids      TEXT,
    entite_noms TEXT,
    spheres     TEXT,
    frequence   INTEGER DEFAULT 1
);

-- ── Vues pratiques
CREATE VIEW IF NOT EXISTS vue_qr_spheres AS
    SELECT q.id, q.niveau, q.question, q.resume, q.categorie,
           q.sphere_primaire, s.nom AS nom_sphere, q.nb_entites
    FROM qr_techniques q
    LEFT JOIN spheres s ON q.sphere_primaire = s.id
    ORDER BY q.sphere_primaire, q.id;

CREATE VIEW IF NOT EXISTS vue_entites_cercles AS
    SELECT e.nom, e.type_hol, e.occurrences, e.source_fichier,
           e.sphere_id, s.nom AS nom_sphere, e.cercle_niveau,
           c.nom AS nom_cercle
    FROM entites_hol e
    LEFT JOIN spheres s ON e.sphere_id = s.id
    LEFT JOIN cercles c ON c.sphere_id = e.sphere_id AND c.niveau = e.cercle_niveau
    ORDER BY e.sphere_id, e.cercle_niveau, e.occurrences DESC;

CREATE VIEW IF NOT EXISTS vue_liens_top AS
    SELECT l.qr_id, q.question, e.nom AS entite, e.type_hol,
           l.score, e.sphere_id, e.cercle_niveau
    FROM liens_qr_entite l
    JOIN qr_techniques q ON l.qr_id = q.id
    JOIN entites_hol e ON l.entite_id = e.id
    WHERE l.score >= 0.5
    ORDER BY l.qr_id, l.score DESC;

-- ── Index
CREATE INDEX IF NOT EXISTS idx_entites_nom     ON entites_hol(nom);
CREATE INDEX IF NOT EXISTS idx_entites_sphere  ON entites_hol(sphere_id);
CREATE INDEX IF NOT EXISTS idx_entites_cercle  ON entites_hol(cercle_niveau);
CREATE INDEX IF NOT EXISTS idx_entites_type    ON entites_hol(type_hol);
CREATE INDEX IF NOT EXISTS idx_liens_qr        ON liens_qr_entite(qr_id);
CREATE INDEX IF NOT EXISTS idx_liens_score     ON liens_qr_entite(score DESC);
CREATE INDEX IF NOT EXISTS idx_hol_src         ON liens_hol(source_id);
CREATE INDEX IF NOT EXISTS idx_hol_rel         ON liens_hol(relation);
CREATE INDEX IF NOT EXISTS idx_mots_cles       ON index_mots_cles(mot_cle);
CREATE INDEX IF NOT EXISTS idx_sessions_ts     ON sessions(timestamp DESC);
"""

# ─────────────────────────────────────────────────────────────────────────────
#  DONNÉES FIXES — Sphères et cercles
# ─────────────────────────────────────────────────────────────────────────────

SPHERES = [
    ("Ensemble", "Ensemble — Disque englobant",
     "Ensemble = 1  ↔  1/x + 1/t + 1/ms",
     "L'ensemble complet Univers-au-carré représenté par la constante 1. "
     "Section XIII : trois vues équivalentes forcent RsP = Re(ρ) = 1/2.",
     None, 100),
    ("1/ms", "1/ms — Méthode Spectrale",
     "1/ms = 1/ms1 + 1/ms2 + 1/ms3",
     "Noyau algorithmique : suites SA/SB, rapports RsP, digamma. "
     "154 définitions, 148 lemmes dans methode_spectral.thy.",
     "(2) 1/y3 = 1/ms1 — Zéros non-triviaux de zeta = valeurs de n", 70),
    ("1/t", "1/t — psi_savard / Théorèmes HOL",
     "1/t  (psi_savard ≡ Tchebychev sur la Suite B)",
     "27 théorèmes formels Isabelle/HOL. Section XIII Pont Savard → "
     "alignement_central, pont_spectral_direct_final, synthese_pont_savard.",
     "(1) 1/y1 = 1/t — Tchebychev = psi_savard (validations XIII.2)", 70),
    ("1/x", "1/x — zeta / Extensions géométriques",
     "1/x = 1/y1 + 1/y2 + 1/y3  (décomposition de zeta)",
     "validation_hol_unifiee.thy : RSA_ratio, riemann_zero_critical, "
     "spectral_hilbert_operator. Correspondance aux zéros de Riemann réfutée pour cet opérateur.",
     "(3) 1/y2 = 1/ms3 — Re(ρ) = 1/2 = RsP = 1/2", 70),
]

CERCLES = [
    # 1/ms
    ("1/ms", 1, "Suites fondamentales SA/SB",
     "SA, SB, A_1_3, B_1_3, A_1_4, B_1_4, digamma_calc, prime_equation"),
    ("1/ms", 2, "Rapports spectraux RsP",
     "RsP, RsP_1_3, RsP_1_4, RsP_nn, RsP_neg, RsP_bloc_1_2"),
    ("1/ms", 3, "Conditions et indices",
     "indice_valide, asymetrique_ordonnee, asymetrique_chaotique, liste_strictement_croissante"),
    ("1/ms", 4, "Postulats axiomatiques",
     "spectral_postulate_pos, spectral_postulate_1_3, spectral_postulate_1_4, "
     "spectral_ratio_neg_un_demi, prime_position_exists"),
    # 1/t
    ("1/t", 1, "Lemmes algébriques fondamentaux",
     "SA_forme_generale, SB_forme_generale, SB_affine_en_SA, ecart_spectral_constant, "
     "digamma_affine_en_SA, difference_SA_succ, difference_SB_succ"),
    ("1/t", 2, "Théorèmes spectraux centraux",
     "RsP_un_demi_general, RsP_un_tiers_constant, RsP_un_quart_constant, "
     "prime_equation_for_primes_pos, reconstruction_premier_pos"),
    ("1/t", 3, "Preuves par l'absurde — exclusivité P",
     "composite_not_prime_i, spectral_method_exclusively_for_primes, "
     "extraction_constante_A, extraction_constante_B, ecart_minimal_universel_A"),
    ("1/t", 4, "Pont Savard — Section XIII",
     "ensemble_savard, ensemble_savard_satisfaisable, alignement_central, "
     "pont_spectral_direct_final, synthese_pont_savard, RsP_universel_entier_naturel"),
    # 1/x
    ("1/x", 1, "Redéfinitions de validation",
     "A_validation, B_validation, digamma_validation, spectral_equation, "
     "prime_nth_reconstruction, Sr2_validation, rsr_validation"),
    ("1/x", 2, "Rapports spectraux asymétriques RSA",
     "alternating_block_sum, RSA_ratio, rsa_converges_to_half, RSA_convergence_implies_distance_decreasing, "
     "RSA_ratio_well_defined"),
    ("1/x", 3, "Zéros de Riemann — opérateur de Hilbert",
     "riemann_zero_critical, spectral_hilbert_operator, riemann_zeros_as_eigenvalues, "
     "riemann_zeros_eigenvalues_correspondence, classify_convergence_state"),
    ("1/x", 4, "Cohérence globale et reconstruction",
     "global_consistency, prime_reconstruction_validity, Sr2_normalization_property, "
     "distance_to_half_metric, consistency_A_B_definitions"),
]

# Liens de validation croisée HOL (graphe des dépendances réelles)
LIENS_HOL = [
    # 1/ms → 1/t : les postulats fondent les lemmes et théorèmes
    ("spectral_postulate_pos",         "prime_equation_for_primes_pos",    "valide",    "methode_spectral.thy"),
    ("spectral_postulate_1_3",         "RsP_un_tiers_constant",            "valide",    "methode_spectral.thy"),
    ("spectral_postulate_1_4",         "RsP_un_quart_constant",            "valide",    "methode_spectral.thy"),
    ("spectral_ratio_neg_un_demi",     "RsP_un_demi_general",              "implique",  "methode_spectral.thy"),
    ("SA",                             "SB_affine_en_SA",                  "utilise",   "methode_spectral.thy"),
    ("SB",                             "SB_affine_en_SA",                  "utilise",   "methode_spectral.thy"),
    ("SA",                             "SA_forme_generale",                "valide",    "methode_spectral.thy"),
    ("SB",                             "SB_forme_generale",                "valide",    "methode_spectral.thy"),
    ("digamma_calc",                   "prime_equation_for_primes_pos",    "depend_de", "methode_spectral.thy"),
    ("digamma_calc",                   "ecart_spectral_constant",          "utilise",   "methode_spectral.thy"),
    ("digamma_calc",                   "digamma_affine_en_SA",             "utilise",   "methode_spectral.thy"),
    ("prime_equation",                 "prime_equation_identity",          "valide",    "methode_spectral.thy"),
    ("A_1_3",                          "RsP_un_tiers_constant",            "utilise",   "methode_spectral.thy"),
    ("B_1_3",                          "RsP_un_tiers_constant",            "utilise",   "methode_spectral.thy"),
    ("A_1_4",                          "RsP_un_quart_constant",            "utilise",   "methode_spectral.thy"),
    ("B_1_4",                          "RsP_un_quart_constant",            "utilise",   "methode_spectral.thy"),
    ("RsP_bloc_1_2",                   "asymetrie_implique_indices_valides","depend_de", "methode_spectral.thy"),
    ("indice_valide",                  "asymetrique_ordonnee",             "utilise",   "methode_spectral.thy"),
    ("indice_valide",                  "asymetrique_chaotique",            "utilise",   "methode_spectral.thy"),
    ("indice_valide_nat",              "asymetrique_ordonnee_nat",         "utilise",   "methode_spectral.thy"),
    ("indice_valide_nat",              "asymetrique_chaotique_nat",        "utilise",   "methode_spectral.thy"),
    # 1/t → 1/t : lemmes → théorèmes
    ("RsP_un_demi_general",            "reconstruction_premier_pos",       "implique",  "methode_spectral.thy"),
    ("prime_equation_for_primes_pos",  "composite_not_prime_i",            "derive_de", "methode_spectral.thy"),
    ("composite_not_prime_i",          "spectral_method_exclusively_for_primes","implique","methode_spectral.thy"),
    ("extraction_constante_A",         "ecart_minimal_universel_A",        "implique",  "methode_spectral.thy"),
    ("extraction_constante_B",         "ecart_minimal_universel_B",        "implique",  "methode_spectral.thy"),
    # 1/t → Pont Savard (Section XIII)
    ("RsP_un_demi_general",            "ensemble_savard_satisfaisable",    "implique",  "methode_spectral.thy"),
    ("ensemble_savard",                "alignement_central",               "contient",  "methode_spectral.thy"),
    ("ensemble_savard",                "conclusion_ensemble",              "contient",  "methode_spectral.thy"),
    ("alignement_central",             "pont_spectral_direct_final",       "implique",  "methode_spectral.thy"),
    ("pont_spectral_direct_final",     "synthese_pont_savard",             "implique",  "methode_spectral.thy"),
    ("reconstruction_premier_pos",     "ensemble_savard_satisfaisable",    "valide",    "methode_spectral.thy"),
    # 1/ms ↔ 1/x : validation croisée
    ("SA",                             "A_validation",                     "correspond_a","validation_hol_unifiee.thy"),
    ("SB",                             "B_validation",                     "correspond_a","validation_hol_unifiee.thy"),
    ("digamma_calc",                   "digamma_validation",               "correspond_a","validation_hol_unifiee.thy"),
    ("prime_equation",                 "prime_nth_reconstruction",         "correspondance_non_etablie","validation_hol_unifiee.thy"),
    ("RsP",                            "RSA_ratio",                        "analogie_non_etablie","validation_hol_unifiee.thy"),
    ("RSA_convergence_implies_distance_decreasing", "rsa_converges_to_half", "requiert", "validation_hol_unifiee.thy"),
    # 1/x → cohérence globale
    ("prime_reconstruction_validity",  "consistency_digamma_reconstruction","identite_algebrique_sans_primalite","validation_hol_unifiee.thy"),
    ("spectral_hilbert_operator_on_critical_line", "riemann_zero_critical", "localise_sur", "validation_hol_unifiee.thy"),
    ("riemann_zeros_eigenvalues_correspondence", "riemann_zeros_as_eigenvalues", "refute", "validation_hol_unifiee.thy"),
    # Pont Savard ↔ 1/x (Re(ρ) = 1/2)
    ("synthese_pont_savard",           "riemann_zero_critical",            "valide",    "methode_spectral.thy"),
    ("alignement_central",             "global_consistency",               "implique",  "validation_hol_unifiee.thy"),
]


# ─────────────────────────────────────────────────────────────────────────────
#  CONSTRUCTEUR SQLite
# ─────────────────────────────────────────────────────────────────────────────

class ConstructeurSQLite:

    def __init__(self):
        self.conn: sqlite3.Connection = None
        self.nom_id: dict[str, int] = {}   # nom entité → id

    def ouvrir(self):
        SORTIE.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(SORTIE))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        print(f"  ✓ DB ouverte : {SORTIE}")

    def creer_schema(self):
        self.conn.executescript(DDL)
        self.conn.commit()
        print("  ✓ Schéma créé — 10 tables + 3 vues + index")

    # ── Sphères et cercles
    def inserer_spheres_cercles(self):
        for row in SPHERES:
            self.conn.execute(
                "INSERT OR REPLACE INTO spheres(id,nom,equation,description,concordance,rayon) VALUES(?,?,?,?,?,?)",
                row)
        for row in CERCLES:
            self.conn.execute(
                "INSERT OR IGNORE INTO cercles(sphere_id,niveau,nom,description) VALUES(?,?,?,?)",
                row)
        self.conn.commit()
        print(f"  ✓ {len(SPHERES)} sphères + {len(CERCLES)} cercles insérés")

    # ── Entités HOL depuis gabriel_keywords_qr_map.json
    def inserer_entites(self, data: dict):
        nb = 0
        for ent in data.get("entites_fondamentales", []):
            cur = self.conn.execute("""
                INSERT OR IGNORE INTO entites_hol
                (nom, type_hol, source_fichier, sphere_id, cercle_niveau)
                VALUES (?,?,?,?,?)
            """, (ent["nom"], ent["type"], ent["source"],
                  ent.get("sphere"), ent.get("cercle")))
            if cur.lastrowid:
                self.nom_id[ent["nom"]] = cur.lastrowid
                nb += 1

        # Entités extraites dynamiquement depuis les fichiers .thy
        for type_hol, liste in data.get("entites_extraites_dynamiques", {}).items():
            for e in liste:
                nom = e.get("nom", "")
                if not nom or nom in self.nom_id:
                    if nom in self.nom_id:
                        self.conn.execute(
                            "UPDATE entites_hol SET occurrences=?, ligne=?, contexte=? WHERE nom=?",
                            (e.get("occurrences",1), e.get("ligne"), e.get("contexte","")[:400], nom))
                    continue
                cur = self.conn.execute("""
                    INSERT OR IGNORE INTO entites_hol
                    (nom, type_hol, source_fichier, ligne, contexte, occurrences)
                    VALUES (?,?,?,?,?,?)
                """, (nom, type_hol, e.get("source",""),
                      e.get("ligne"), e.get("contexte","")[:400],
                      e.get("occurrences",1)))
                if cur.lastrowid:
                    self.nom_id[nom] = cur.lastrowid
                    nb += 1

        # Remplir le dictionnaire pour tout ce qui existait déjà
        for row in self.conn.execute("SELECT id, nom FROM entites_hol"):
            self.nom_id[row["nom"]] = row["id"]

        self.conn.commit()
        print(f"  ✓ {nb} entités HOL insérées ({len(self.nom_id)} au total)")

    # ── Liens inter-entités HOL
    def inserer_liens_hol(self):
        nb = 0
        for src_nom, cib_nom, relation, source in LIENS_HOL:
            src_id = self.nom_id.get(src_nom)
            cib_id = self.nom_id.get(cib_nom)
            if not src_id or not cib_id:
                continue
            r_src = self.conn.execute("SELECT sphere_id FROM entites_hol WHERE id=?", (src_id,)).fetchone()
            r_cib = self.conn.execute("SELECT sphere_id FROM entites_hol WHERE id=?", (cib_id,)).fetchone()
            try:
                self.conn.execute("""
                    INSERT OR IGNORE INTO liens_hol
                    (source_id, cible_id, relation, source_fichier, sphere_source, sphere_cible)
                    VALUES (?,?,?,?,?,?)
                """, (src_id, cib_id, relation, source,
                      r_src["sphere_id"] if r_src else None,
                      r_cib["sphere_id"] if r_cib else None))
                nb += 1
            except sqlite3.IntegrityError:
                pass
        self.conn.commit()
        print(f"  ✓ {nb} liens inter-entités HOL insérés")

    # ── Q&R techniques et leurs liens aux entités
    def inserer_qr(self, data: dict):
        nb_qr = 0
        nb_liens = 0
        for assoc in data.get("associations_qr_entites", []):
            qr_id   = assoc["qr_id"]
            spheres = assoc.get("spheres_ensemble", ["1/ms"])
            sphere_prim = spheres[0] if spheres else "1/ms"
            self.conn.execute("""
                INSERT OR REPLACE INTO qr_techniques
                (id, niveau, source_fichier, question, resume, categorie,
                 mots_cles, spheres, sphere_primaire, nb_entites)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                qr_id,
                assoc.get("niveau","avance"),
                assoc.get("source_thy",""),
                assoc.get("question",""),
                assoc.get("resume",""),
                assoc.get("categorie",""),
                json.dumps(assoc.get("mots_cles",[]), ensure_ascii=False),
                json.dumps(spheres, ensure_ascii=False),
                sphere_prim,
                assoc.get("nb_entites",0),
            ))
            nb_qr += 1
            for ent_assoc in assoc.get("entites_top15", []):
                eid = self.nom_id.get(ent_assoc.get("entite",""))
                if not eid:
                    continue
                try:
                    self.conn.execute("""
                        INSERT OR IGNORE INTO liens_qr_entite(qr_id,entite_id,score,type_lien)
                        VALUES (?,?,?,'semantique')
                    """, (qr_id, eid, ent_assoc.get("score",0.5)))
                    nb_liens += 1
                except sqlite3.IntegrityError:
                    pass
        self.conn.commit()
        print(f"  ✓ {nb_qr} Q&R insérées + {nb_liens} liens Q&R ↔ entités")

    # ── Index des mots-clés
    def construire_index_mots_cles(self, data: dict):
        mc_index: dict[str, dict] = {}
        for assoc in data.get("associations_qr_entites", []):
            qr_id = assoc["qr_id"]
            spheres = assoc.get("spheres_ensemble", [])
            for mc in assoc.get("mots_cles", []):
                mc_low = mc.lower()
                if mc_low not in mc_index:
                    mc_index[mc_low] = {"qr_ids": set(), "entites": set(), "spheres": set()}
                mc_index[mc_low]["qr_ids"].add(qr_id)
                mc_index[mc_low]["spheres"].update(spheres)
                for ea in assoc.get("entites_top15", []):
                    if ea.get("score", 0) >= 0.5:
                        mc_index[mc_low]["entites"].add(ea.get("entite",""))
        nb = 0
        for mc, info in mc_index.items():
            self.conn.execute("""
                INSERT OR REPLACE INTO index_mots_cles(mot_cle, qr_ids, entite_noms, spheres, frequence)
                VALUES (?,?,?,?,?)
            """, (
                mc,
                json.dumps(sorted(info["qr_ids"])),
                json.dumps(sorted(info["entites"])),
                json.dumps(sorted(info["spheres"])),
                len(info["qr_ids"]),
            ))
            nb += 1
        self.conn.commit()
        print(f"  ✓ {nb} mots-clés indexés")

    # ── Fichiers stratégiques du dépôt (depuis gabriel_repo_map.json)
    def inserer_fichiers_depot(self):
        """Insère les fichiers clés du dépôt dans la DB si gabriel_repo_map.json est disponible."""
        repo_path = RACINE / "gabriel_repo_map.json"
        if not repo_path.exists():
            print("  ⚠  gabriel_repo_map.json introuvable — fichiers dépôt non insérés")
            return
        try:
            with open(repo_path, encoding="utf-8") as f:
                repo = json.load(f)
        except Exception as e:
            print(f"  ⚠  Erreur lecture gabriel_repo_map.json : {e}")
            return

        fichiers = repo.get("fichiers", {})
        graphe   = repo.get("graphe_liens", {})
        hubs     = {f for f, n in repo.get("meta",{}).get("fichiers_les_plus_connectes",[]) if n >= 5}

        # Sélectionner les fichiers les plus pertinents pour le corpus
        MOTS_CLES_CORPUS = {
            "spectral","gabriel","cognitive","engine","backend","memory",
            "orchestrat","pipeline","theories","thy","hol","corpus","mathematic",
            "llm","agent","loop","multiloop",
        }
        chemin_id: dict[str, int] = {}
        nb = 0
        for chemin, meta in fichiers.items():
            nom = meta.get("nom","").lower()
            if not any(k in chemin.lower() or k in nom for k in MOTS_CLES_CORPUS):
                if chemin not in hubs:
                    continue
            # Associer une sphère selon le nom
            sphere = None
            if "spectral" in nom or "SA" in nom or "SB" in nom or "digamma" in nom:
                sphere = "1/ms"
            elif "hol" in nom or "thy" in nom or "theories" in chemin.lower():
                sphere = "1/t"
            elif "validat" in nom or "riemann" in nom or "geometri" in nom:
                sphere = "1/x"

            cur = self.conn.execute("""
                INSERT OR IGNORE INTO fichiers_depot
                (chemin, nom, type_fichier, taille, hash_md5, modifie, nb_lignes,
                 nb_refs, est_hub, sphere_associee)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                chemin, meta.get("nom",""), meta.get("type",""),
                meta.get("taille_octets",0), meta.get("hash_md5",""),
                meta.get("modifie",""), meta.get("nb_lignes",0),
                len(meta.get("refs_sortantes",[])),
                1 if chemin in hubs else 0,
                sphere,
            ))
            if cur.lastrowid:
                chemin_id[chemin] = cur.lastrowid
                nb += 1

        # Remplir le dictionnaire pour fichiers déjà existants
        for row in self.conn.execute("SELECT id, chemin FROM fichiers_depot"):
            chemin_id[row["chemin"]] = row["id"]

        # Liens inter-fichiers (graphe dépôt)
        nb_liens = 0
        for src_chemin, liens in graphe.items():
            src_id = chemin_id.get(src_chemin)
            if not src_id:
                continue
            for lien in liens:
                cib_id = chemin_id.get(lien.get("cible",""))
                if not cib_id:
                    continue
                try:
                    self.conn.execute("""
                        INSERT OR IGNORE INTO liens_fichiers(source_id,cible_id,type_lien,ligne)
                        VALUES (?,?,?,?)
                    """, (src_id, cib_id, lien.get("type",""), lien.get("ligne",0)))
                    nb_liens += 1
                except sqlite3.IntegrityError:
                    pass

        self.conn.commit()
        print(f"  ✓ {nb} fichiers dépôt insérés + {nb_liens} liens inter-fichiers")

    # ── Résumé final
    def afficher_stats(self):
        tables = ["spheres","cercles","entites_hol","qr_techniques",
                  "liens_qr_entite","liens_hol","fichiers_depot",
                  "liens_fichiers","index_mots_cles","sessions"]
        print("\n  ┌─────────────────────────────────────────┐")
        print("  │  RÉSUMÉ BASE DE DONNÉES gabriel_corpus.db│")
        print("  ├─────────────────────────────────────────┤")
        for t in tables:
            try:
                n = self.conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                print(f"  │  {t:30s} : {n:5d} │")
            except Exception:
                pass
        print("  └─────────────────────────────────────────┘")

    def fermer(self):
        if self.conn:
            self.conn.close()

    def executer(self):
        print("\n" + "="*70)
        print("  GABRIEL P2 — GÉNÉRATEUR SQLite")
        print("  Ensemble = 1  ↔  1/x + 1/t + 1/ms  (Section XIII Pont Savard)")
        print("="*70)

        # Charger données étape 1
        print(f"\n[1/6] Chargement de gabriel_keywords_qr_map.json...")
        if not ENTREE.exists():
            print(f"  ✗ Fichier introuvable : {ENTREE}")
            print("  → Exécutez d'abord gabriel_p1_keyword_extractor.py")
            sys.exit(1)
        with open(ENTREE, encoding="utf-8") as f:
            data = json.load(f)
        print(f"  ✓ {data['meta']['nb_qr']} Q&R, "
              f"{data['meta']['nb_entites_connues']} entités connues, "
              f"{data['meta']['nb_entites_extraites']} extraites dynamiquement")

        print("\n[2/6] Création de la DB et du schéma...")
        self.ouvrir()
        self.creer_schema()

        print("\n[3/6] Insertion sphères et cercles concentriques...")
        self.inserer_spheres_cercles()

        print("\n[4/6] Insertion entités HOL...")
        self.inserer_entites(data)

        print("\n[4b] Insertion liens inter-entités HOL...")
        self.inserer_liens_hol()

        print("\n[5/6] Insertion Q&R techniques et leurs liens...")
        self.inserer_qr(data)

        print("\n[5b] Construction index mots-clés...")
        self.construire_index_mots_cles(data)

        print("\n[6/6] Insertion fichiers du dépôt Gabriel...")
        self.inserer_fichiers_depot()

        self.afficher_stats()

        taille = SORTIE.stat().st_size / 1024
        print(f"\n  ✅ gabriel_corpus.db → {SORTIE}  ({taille:.1f} Ko)")
        print("\n  ⏭  Prochaine étape : python gabriel_p3_archiviste.py")
        print("="*70 + "\n")

        self.fermer()


if __name__ == "__main__":
    b = ConstructeurSQLite()
    b.executer()
