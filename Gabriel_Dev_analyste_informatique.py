#!/usr/bin/env python3
"""Gabriel_Dev_analyste_informatique.py - Banque de connaissance d'analyste
informatique + auto-analyse du depot + propositions d'amelioration de code.

Pipeline autonome, stdlib uniquement, EXECUTION DIRECTE (pas de -m : l'environnement
local n'a ni httpx ni sympy) :

    python Gabriel_Dev_analyste_informatique.py --initialiser
    python Gabriel_Dev_analyste_informatique.py --telecharger
    python Gabriel_Dev_analyste_informatique.py --consulter "preuve par l'absurde"
    python Gabriel_Dev_analyste_informatique.py --analyser "nombres premiers"
    python Gabriel_Dev_analyste_informatique.py --stats

Trois etapes :
  1. BANQUE NEURONALE (SQLite) : noeuds (connaissances liees) + liens (schema
     neuronal : repose_sur / utilise / est_exemple_de / contraint / applique_a /
     coocurrence) + index des termes. Alimentee par (a) un corpus d'amorcage
     hors-ligne toujours disponible, et (b) un telechargement BEST-EFFORT depuis
     une whitelist de sources universitaires / ouvertes (echecs logges, jamais
     fatals : la banque reste utilisable hors-ligne).
  2. AUTO-ANALYSE DU DEPOT : reutilise la cartographie existante
     data/gabriel_repo_map.db (tables files / file_edges) puis complete par une
     passe statique locale (ast) : marqueurs TODO/FIXME, docstrings absentes,
     imports morts, tests manquants.
  3. PROPOSITIONS : chaque point ameliorable devient une PropositionAnalyste
     portant un contrat de patch au format du variateur (meta + operations ;
     ops creer_fichier / remplacer_texte / inserer_lignes / supprimer_lignes /
     ajouter_a_la_fin), partageable avec le 8e moteur.

SECURITE (invariants absolus) :
  * ce script N'ECRIT JAMAIS dans le depot vivant : seuls data/analyste/** et la
    sandbox sont ecrits ;
  * les patches ne sont que SIMULES (dry-run), sauf --appliquer-sandbox ;
  * GABRIEL_DEV_ANALYSTE=0 coupe tout (kill-switch) ;
  * telechargement borne (timeout, taille max, nombre de sources).
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import io
import json
import os
import re
import sqlite3
import sys
import tempfile
import tokenize
import unicodedata
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Optional

RACINE = Path(__file__).resolve().parent
DOSSIER_BANQUE = RACINE / "data" / "analyste"
CHEMIN_DB = DOSSIER_BANQUE / "banque_analyste.db"
DOSSIER_RAPPORTS = DOSSIER_BANQUE / "rapports"
DOSSIER_SANDBOX = DOSSIER_BANQUE / "sandbox"
CHEMIN_CARTE_DEPOT = RACINE / "data" / "gabriel_repo_map.db"

KILL_SWITCH = "GABRIEL_DEV_ANALYSTE"
APPLY_SANDBOX = "GABRIEL_RECURSIVE_APPLY"

MAX_OCTETS_PAGE = 1_500_000
MAX_SOURCES = 6
TIMEOUT_RESEAU = 10.0

DOSSIERS_EXCLUS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache",
    "node_modules", "reference_old_agent", "theories", "tmp_geometrie_docx",
    "build", "dist", ".gabriel_cognitif", ".vscode", ".idea",
    # Artefacts produits par le pipeline lui-meme : on n'ameliore pas la copie.
    "data", "logs", ".gabriel_variateur",
}

RELATIONS_VALIDES = {
    "repose_sur", "utilise", "est_exemple_de", "contraint", "applique_a",
    "coocurrence",
}

_SCHEMA = """
CREATE TABLE IF NOT EXISTS noeuds (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cle         TEXT UNIQUE NOT NULL,
    type        TEXT NOT NULL DEFAULT 'notion',
    domaine     TEXT NOT NULL,
    titre       TEXT NOT NULL,
    contenu     TEXT NOT NULL,
    origine     TEXT NOT NULL DEFAULT 'amorcage',
    url         TEXT,
    poids       REAL NOT NULL DEFAULT 1.0,
    horodatage  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_noeuds_domaine ON noeuds(domaine);

CREATE TABLE IF NOT EXISTS liens (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    src         INTEGER NOT NULL,
    dst         INTEGER NOT NULL,
    relation    TEXT NOT NULL,
    poids       REAL NOT NULL DEFAULT 1.0,
    horodatage  TEXT NOT NULL,
    UNIQUE(src, dst, relation)
);

CREATE TABLE IF NOT EXISTS index_termes (
    terme       TEXT NOT NULL,
    noeud_id    INTEGER NOT NULL,
    tf          INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (terme, noeud_id)
);

CREATE TABLE IF NOT EXISTS propositions (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    requete       TEXT NOT NULL,
    fichier       TEXT,
    categorie     TEXT NOT NULL,
    justification TEXT NOT NULL,
    contrat       TEXT,
    statut        TEXT NOT NULL DEFAULT 'propose',
    horodatage    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS telechargements (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    source      TEXT NOT NULL,
    url         TEXT NOT NULL,
    statut      TEXT NOT NULL,
    octets      INTEGER DEFAULT 0,
    message     TEXT,
    horodatage  TEXT NOT NULL
);
"""


def _maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def actif() -> bool:
    """Kill-switch : GABRIEL_DEV_ANALYSTE=0 coupe tout le pipeline."""
    return os.environ.get(KILL_SWITCH, "1").strip().lower() not in (
        "0", "false", "non", "off", "no",
    )


def _charger_variateur() -> Any:
    """Charge le variateur sandboxe par chemin de fichier.

    Evite l'import de src/multiloop/__init__.py qui tire httpx (absent ici).
    Retourne le module, ou None si indisponible (le script reste autonome).
    """
    chemin = RACINE / "src" / "multiloop" / "raisonnement_recursif" / "pipeline_auto_programmation.py"
    nom = "_gabriel_variateur_charge"
    deja = sys.modules.get(nom)
    if deja is not None:
        return deja
    try:
        spec = importlib.util.spec_from_file_location(nom, chemin)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        # Python >= 3.12 : @dataclass resout cls.__module__ via sys.modules.
        # L'enregistrer AVANT exec_module est donc obligatoire.
        sys.modules[nom] = module
        spec.loader.exec_module(module)
        return module
    except Exception:
        sys.modules.pop(nom, None)
        return None


# ═════════════════════════════════════════════════════════════════════════
# 1. CORPUS D'AMORCAGE (hors-ligne, toujours disponible)
# ═════════════════════════════════════════════════════════════════════════
# Chaque entree : (cle, domaine, titre, contenu, liens[(cle_cible, relation)])
# Les liens forment le "schema neuronal" : on ne stocke pas des fichiers
# isoles, on stocke des CONNAISSANCES RELIEES.

CORPUS: tuple[tuple[str, str, str, str, tuple[tuple[str, str], ...]], ...] = (
    # ── Analyse informatique ────────────────────────────────────────────
    (
        "analyse-des-besoins", "analyse_informatique", "Analyse des besoins",
        "Recueil et qualification des besoins d'un systeme d'information : "
        "acteurs, cas d'utilisation, regles metier, contraintes non "
        "fonctionnelles (performance, securite, ergonomie). Activite de base "
        "de l'analyste informatique, a la frontiere entre metier et technique.",
        (("specification-fonctionnelle", "repose_sur"),
         ("cahier-des-charges", "est_exemple_de")),
    ),
    (
        "specification-fonctionnelle", "analyse_informatique",
        "Specification fonctionnelle",
        "Description PRECISE de ce que le systeme doit faire, sans prescrire "
        "comment : entrees, sorties, etats, cas particuliers, criteres "
        "d'acceptation. Sert de reference unique aux developpeurs et aux "
        "testeurs ; toute exigence non specifiee ne peut etre validee.",
        (("analyse-des-besoins", "repose_sur"),
         ("uml", "utilise"), ("tests-logiciels", "contraint")),
    ),
    (
        "cahier-des-charges", "analyse_informatique", "Cahier des charges",
        "Document contractuel qui fige les besoins, le perimetre, les "
        "livrables, le planning et les criteres de recette. Enonce aussi les "
        "exigences de qualite : couverture de tests, documentations livrees, "
        "engages de maintenabilite.",
        (("specification-fonctionnelle", "est_exemple_de"),),
    ),
    (
        "uml", "analyse_informatique", "Modeles UML",
        "Langage de modelisation graphique standardise : diagrammes de cas "
        "d'utilisation, de classes, de sequence, d'activites, d'etats. Permet "
        "de raisonner sur la structure et le comportement du systeme avant "
        "toute ecriture de code, et de faire relire le modele par le metier.",
        (("specification-fonctionnelle", "repose_sur"),
         ("programmation-orientee-objet", "applique_a")),
    ),
    (
        "modele-de-donnees", "analyse_informatique",
        "Modele de donnees (MCD / MLD)",
        "Conception des donnees : entites, attributs, cardinalites (MCD), "
        "normalisation jusqu'en forme normale de Boyce-Codd (MLD). Conditionne "
        "l'integrite, la requetabilite et l'evolution d'une base.",
        (("specification-fonctionnelle", "repose_sur"),
         ("sql", "applique_a"), ("bases-de-donnees", "repose_sur")),
    ),

    # ── Informatique (technique) ────────────────────────────────────────
    (
        "sql", "informatique", "Langage SQL",
        "Langage declaratif de manipulation des donnees relationnelles : "
        "SELECT, jointures, agregations, sous-requetes, transactions ACID. "
        "L'analyste l'ecrit pour interroger la donnee et en verifier la "
        "coherence avant tout developpement applicatif.",
        (("schema-relationnel", "applique_a"), ("bases-de-donnees", "utilise")),
    ),
    (
        "bases-de-donnees", "informatique", "Bases de donnees",
        "Persistance organisee : relationnel, documentaire, cle-valeur, "
        "graphe. Choix conditionne par le modele de donnees, le volume et les "
        "acces. Index, vues, contraintes et migrations en constituent la "
        "maintenance courante.",
        (("schema-relationnel", "repose_sur"), ("modele-de-donnees", "utilise")),
    ),
    (
        "programmation-orientee-objet", "informatique",
        "Programmation orientee objet",
        "Encapsulation, heritance, polymorphisme, composition. Organise le "
        "code en entites a responsabilites nettes ; la composition est "
        "generalement preferable a l'heritage pour raisonner sur les "
        "dependances.",
        (("uml", "utilise"), ("design-patterns", "repose_sur")),
    ),
    (
        "algorithmique", "informatique", "Algorithmique",
        "Conception de suites finies d'operations resolvant un probleme : "
        "tri, recherche, programmation dynamique, graphes, diviser pour "
        "regner. Discipline fondatrice dont depend toute analyse de "
        "performance ou de faisabilite.",
        (("complexite-algorithmique", "repose_sur"),
         ("theorie-de-la-calculabilite", "repose_sur")),
    ),
    (
        "theorie-de-la-calculabilite", "logique",
        "Theorie de la calculabilite",
        "Machines de Turing, fonctions recursives, problemes indécidables "
        "(halt, correspondance de Post), reducibilite. Etablit ce qui est "
        "PRINCIPIELLEMENT calculable, avant toute question d'efficacite.",
        (("algorithmique", "repose_sur"), ("logique-fol", "utilise")),
    ),
    (
        "verification-par-modele", "informatique", "Verification par modele",
        "Construction explicite de l'arbre des etats atteignables pour "
        "prouver des proprietes de securite (absence d'etat bloquant, de "
        "deadlock). Complementaire des tests : couvre toutes les traces "
        "plutot qu'un echantillon.",
        (("logique-fol", "repose_sur"), ("tests-logiciels", "est_exemple_de")),
    ),

    # ── Mathematiques / theorie des nombres ────────────────────────────
    (
        "theorie-des-nombres", "mathematiques", "Theorie des nombres",
        "Etude des proprietes des entiers : divisibilite, congruences, "
        "arithmetic modulaire, distributions. Branche la plus ancienne des "
        "mathematiques et socle de la cryptographie moderne ; son energie "
        "vient de problemes simples a enoncer, durs a prouver.",
        (("nombres-premiers", "repose_sur"), ("codes-correcteurs", "utilise")),
    ),
    (
        "nombres-premiers", "mathematiques", "Nombres premiers",
        "Entiers n > 1 n'ayant aucun diviseur autre que 1 et n. Theoreme "
        "fondamental de l'arithmetique : toute decomposition en facteurs "
        "premiers est unique a l'ordre pres. Leur repartition (theoreme des "
        "nombres premiers, fonction zeta de Riemann) reste centrale.",
        (("theorie-des-nombres", "repose_sur"),
         ("spectre-geometrique", "repose_sur")),
    ),
    (
        "spectre-geometrique", "geometrie", "Geometrie spectrale",
        "Etude des spectres de operateurs differentiels (Laplace-Beltrami) "
        "sur une variete : les eigenfrequences codent la geometrie, et "
        "l'asymptotique de Weyl compte le nombre de modes sous une frequence "
        "donnee. Pont explicit entre forme geometrique et repartition "
        "arithmetique.",
        (("geometrie-des-varietes", "repose_sur"),
         ("nombres-premiers", "repose_sur"),
         ("analyse-harmonique", "utilise")),
    ),
    (
        "codes-correcteurs", "mathematiques", "Codes correcteurs d'erreurs",
        "Codes de Hamming, Reed-Solomon, CRC : ajouter de la redondance pour "
        "detecter et corriger des fautes de transmission. L'espace de Hamming "
        "et les corps finis en fournissent l'outillage ; l'application "
        "courante est le controle d'integrite des donnees.",
        (("theorie-des-nombres", "applique_a"),
         ("analyse-numerique", "utilise")),
    ),
    (
        "analyse-harmonique", "mathematiques", "Analyse harmonique",
        "Decomposition d'un signal ou d'une fonction en ondes de base "
        "(series de Fourier, transformee, ondelettes). Outil de resolution "
        "des PDE et de traitement du signal ; le spectre d'un operateur en "
        "est l'objet d'etude direct.",
        (("spectre-geometrique", "utilise"),
         ("algebre-lineaire", "repose_sur")),
    ),
    (
        "algebre-lineaire", "mathematiques", "Algebre lineaire",
        "Espaces vectoriels, matrices, valeurs propres, diagonalisation, "
        "decomposition SVD. Langage commun de tout calcul scientifique et de "
        "tout modele lineaire ; la stabilite numerique en depend.",
        (("analyse-harmonique", "repose_sur"),
         ("analyse-numerique", "utilise")),
    ),
    (
        "geometrie-des-varietes", "geometrie", "Geometrie des varietes",
        "Espaces localement euclidiens, courbure, connexions, tenseurs. "
        "Generalise la geometrie euclidienne ; la courbure dictate la "
        "propagation (chaleur, ondes) dont depend le spectre.",
        (("spectre-geometrique", "repose_sur"), ("algebre-lineaire", "utilise")),
    ),

    # ── Logique computationnelle ────────────────────────────────────────
    (
        "logique-fol", "logique", "Logique du premier ordre",
        "Predicats, quantificateurs universel et existentiel, formules "
        "formelles, deduction naturelle et semantic des modeles. Cadre dans "
        "lequel un enonce devient un THEOREME prouvable mecaniquement, par "
        "exemple sous Isabelle/HOL.",
        (("logique-propositionnelle", "repose_sur"),
         ("preuves-assistees", "applique_a")),
    ),
    (
        "logique-propositionnelle", "logique", "Logique propositionnelle",
        "Connecteurs booleens, tables de verite, satisfiabilite, normalisation "
        "CNF/DNF. Base du raisonnement automatise et des solveurs SAT ; "
        "l'evaluation d'une formule est en temps lineaire en sa taille.",
        (("logique-fol", "repose_sur"), ("algorithmique", "utilise")),
    ),
    (
        "preuves-assistees", "logique", "Preuves assistees par ordinateur",
        "Systemes type Isabelle/HOL, Coq, Lean : le programme verifie la "
        "preuve d'un theoreme ecrit dans un langage formel. Force du "
        "dispositif : l'impossibilite d'un raisonnement non verifie ; cout : "
        "toute propriete doit etre formalisee.",
        (("logique-fol", "repose_sur"), ("preuve-par-absurde", "utilise")),
    ),
    (
        "preuve-par-absurde", "logique", "Preuve par l'absurde",
        "On suppose la negation de la these, on en deduit une contradiction, "
        "donc la these est vraie (intuitionnement : la double negation). "
        "Methode de reference pour l'exclusivite et l'existence, notamment en "
        "arithmetique et en geometrie spectrale.",
        (("logique-fol", "repose_sur"), ("preuves-assistees", "utilise")),
    ),
    (
        "analyse-numerique", "numerique", "Analyse numerique",
        "Calcul sur machines a nombres reels approximes : arithmetique "
        "flottante, erreurs de troncature et d'arrondi, stabilite des "
        "algorithmes, extrapolation. Toute simulation numerique doit "
        "quantifier son erreur pour etre interpretee.",
        (("algebre-lineaire", "utilise"), ("codes-correcteurs", "utilise")),
    ),

    # ── Qualite logicielle (completes le lot d'analyse) ─────────────────
    (
        "tests-logiciels", "analyse_informatique", "Tests logiciels",
        "Verification par exercice du code : tests unitaires, d'integration, "
        "de non-regression, de bout en bout, tests de charge. Strategie : "
        "equivalence de classes, valeurs limites, couverture de branches. Un "
        "code sans test ne peut etre ameliore en confiance.",
        (("specification-fonctionnelle", "contraint"),
         ("complexite-algorithmique", "applique_a")),
    ),
    (
        "revue-de-code", "analyse_informatique", "Revue de code",
        "Inspection structuree du code par un pairs : lisibilite, respect des "
        "conventions, cas limites, complexite, tests associes. Detecte les "
        "defauts en amont de l'integration ; son efficacite depend d'une "
        "grille de criteres explicite et partagee.",
        (("documentation-technique", "utilise"), ("tests-logiciels", "utilise")),
    ),
    (
        "architecture-logicielle", "analyse_informatique",
        "Architecture logicielle",
        "Organisation des composants, de leurs dependances et de leurs "
        "responsabilites : couche, hexagonale, evenementielle. Arbitre "
        "livraison rapide contre cout d'evolution. Une architecture "
        "explicite permet de localiser ou agir pour une modification.",
        (("design-patterns", "utilise"), ("tests-logiciels", "contraint")),
    ),
    (
        "documentation-technique", "analyse_informatique",
        "Documentation technique",
        "README, docstrings, notes d'API, ADR (Architecture Decision Records). "
        "Doit decrivre le POURQUOI autant que le QUEL ; une documentation non "
        "tenue est pire qu'une absence car elle induit en erreur. Critere de "
        "qualite d'un depot analysable.",
        (("revue-de-code", "utilise"), ("architecture-logicielle", "utilise")),
    ),
    (
        "design-patterns", "analyse_informatique", "Patterns de conception",
        "Solutions reutilisables a des problemes recurents : strategie, "
        "observateur, fabrique, decorateur, gabarit. A employer avec "
        "parcimonie — un pattern introduit de l'indirection dont il faut "
        "justifier le cout.",
        (("programmation-orientee-objet", "repose_sur"),
         ("architecture-logicielle", "applique_a")),
    ),
    (
        "complexite-algorithmique", "analyse_informatique",
        "Complexite algorithmique",
        "Notation O(.) : temps et espace en fonction de la taille d'entree. "
        "Analyse asymptotique, cas moyen versus pire cas, amortisation. Outil "
        "de decision pour choisir un algorithme selon le volume reel de "
        "donnees attendu.",
        (("algorithmique", "repose_sur"), ("tests-logiciels", "applique_a")),
    ),
    (
        "indexation-inversion", "analyse_informatique", "Indexation inverse",
        "Structure associant a chaque terme la liste des documents ou il "
        "apparait, ponderee par la frequence (TF) et la rarete (IDF). Base de "
        "tout moteur de recherche et de toute banque de connaissances "
        "interrogeable par mots-cles.",
        (("schema-relationnel", "repose_sur"),
         ("theorie-des-nombres", "applique_a")),
    ),
    (
        "schema-relationnel", "analyse_informatique", "Schema relationnel",
        "Formalisme de Codd : relations (tables), cles primaires et "
        "etrangeres, dependances fonctionnelles, normalisation. Le contrat "
        "formel qui rend une base coherente et interrogeable ; tout schema "
        "relie est un graphe des dependances entre entites.",
        (("modele-de-donnees", "repose_sur"), ("sql", "utilise"),
         ("logique-fol", "applique_a")),
    ),
)

# ═════════════════════════════════════════════════════════════════════════
# 2. SOURCES DE TELECHARGEMENT (whitelist, best-effort)
# ═════════════════════════════════════════════════════════════════════════
# Uniquement des sources universitaires / ouvertes. Chaque echec (DNS, TLS,
# 404, timeout, parsing) est LOGGE dans la table `telechargements` et n'est
# JAMAIS fatal : la banque reste pleinement utilisable hors-ligne via CORPUS.

SOURCES: tuple[tuple[str, str], ...] = (
    ("MIT OpenCourseWare - Linear Algebra (Strang)",
     "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/"),
    ("MIT OpenCourseWare - Introduction to Computer Science",
     "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-"
     "programming-in-python-fall-2016/"),
    ("Universite de Bordeaux - Theorie des nombres (master MathInfo)",
     "https://www.math.u-bordeaux.fr/~jzapirin/tn1.html"),
    ("Isabelle/HOL - Reference (documentation formelle)",
     "https://isabelle.in.tum.de/dist/Isabelle2024/doc/tutorial.pdf"),
    ("Stanford Encyclopedia of Philosophy - Computability and Complexity",
     "https://plato.stanford.edu/entries/computability/"),
    ("Wikipedia (ouvert) - Spectral geometry",
     "https://en.wikipedia.org/wiki/Spectral_geometry"),
)

MAX_MOTS = 400
STOPWORDS = frozenset(
    "le la les un une des du de d l et ou o car mais donc or ni si que qui "
    "ce cet cette ces est sont etre avoir dans pour par sur sous avec sans "
    "the of and to in is are for on a an".split()
)

_MOT_RE = re.compile(r"[a-z0-9]+")


def normaliser(texte: str) -> str:
    """Minuscules + suppression des accents (comparaison robuste FR/EN)."""
    decompose = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in decompose if not unicodedata.combining(c))


def jetonner(texte: str) -> list[str]:
    """Decoupe en jetons pertinents : sans mots vides, >= 3 signes."""
    if not texte:
        return []
    mots = _MOT_RE.findall(normaliser(texte))
    return [m for m in mots if len(m) >= 3 and m not in STOPWORDS][:MAX_MOTS]


# ═════════════════════════════════════════════════════════════════════════
# 3. BANQUE NEURONALE (SQLite)
# ═════════════════════════════════════════════════════════════════════════

@dataclass
class Noeud:
    id: int
    cle: str
    domaine: str
    titre: str
    contenu: str
    origine: str
    poids: float
    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id, "cle": self.cle, "domaine": self.domaine,
            "titre": self.titre, "origine": self.origine,
            "poids": self.poids, "url": self.url,
        }


@dataclass
class PropositionAnalyste:
    """Point ameliorable du depot + operation de patch (variateur) associee."""
    categorie: str
    fichier: str
    titre: str
    justification: str
    ligne: int = 0
    operation: Optional[dict[str, Any]] = None
    noeuds_connaissance: list[str] = field(default_factory=list)

    @property
    def patchable(self) -> bool:
        return self.operation is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "categorie": self.categorie, "fichier": self.fichier,
            "ligne": self.ligne, "titre": self.titre,
            "justification": self.justification,
            "patchable": self.patchable, "operation": self.operation,
            "noeuds_connaissance": list(self.noeuds_connaissance),
        }


class BanqueAnalyste:
    """Base SQLite du savoir d'analyste : noeuds + liens + index de termes."""

    def __init__(self, chemin: str | Path | None = None):
        # Base en memoire : connexion unique partagee (sinon chaque `_conn()`
        # recreerait une base vide et le schema serait perdu).
        self.en_memoire = chemin is not None and str(chemin) == ":memory:"
        if self.en_memoire:
            self.chemin = Path(":memory:")
        else:
            self.chemin = Path(chemin) if chemin else CHEMIN_DB
            self.chemin.parent.mkdir(parents=True, exist_ok=True)
        self._partage: Optional[sqlite3.Connection] = None
        if self.en_memoire:
            self._partage = sqlite3.connect(":memory:")
            self._partage.row_factory = sqlite3.Row
        with self._conn() as conn:
            conn.executescript(_SCHEMA)

    def _conn(self) -> sqlite3.Connection:
        if self._partage is not None:
            return self._partage
        conn = sqlite3.connect(self.chemin)
        conn.row_factory = sqlite3.Row
        return conn

    def fermer(self) -> None:
        if self._partage is not None:
            self._partage.close()
            self._partage = None

    def _indexer(self, conn: sqlite3.Connection, noeud_id: int, texte: str) -> None:
        compteur = Counter(jetonner(texte))
        if not compteur:
            return
        conn.executemany(
            "INSERT OR REPLACE INTO index_termes(terme, noeud_id, tf) "
            "VALUES (?, ?, ?)",
            [(t, noeud_id, n) for t, n in compteur.items()],
        )

    # ── ecriture ────────────────────────────────────────────────────────
    def inserer_noeud(
        self, cle: str, domaine: str, titre: str, contenu: str,
        origine: str = "amorcage", url: str = "", poids: float = 1.0,
        type_: str = "notion", conn: Optional[sqlite3.Connection] = None,
    ) -> int:
        """Insere (ou met a jour) un noeud et l'indexe. Idempotent sur `cle`."""
        externe = conn is not None
        conn = conn or self._conn()
        try:
            conn.execute(
                "INSERT INTO noeuds(cle,type,domaine,titre,contenu,origine,url,"
                "poids,horodatage) VALUES (?,?,?,?,?,?,?,?,?) "
                "ON CONFLICT(cle) DO UPDATE SET titre=excluded.titre, "
                "contenu=excluded.contenu, url=excluded.url, "
                "poids=excluded.poids, origine=excluded.origine",
                (cle, type_, domaine, titre, contenu, origine, url or None,
                 poids, _maintenant()),
            )
            nid = int(conn.execute(
                "SELECT id FROM noeuds WHERE cle = ?", (cle,)
            ).fetchone()[0])
            self._indexer(conn, nid, f"{titre} {contenu} {cle} {domaine}")
            if not externe:
                conn.commit()
            return nid
        finally:
            if not externe and not self.en_memoire:
                conn.close()

    def lier(self, src: int, dst: int, relation: str, poids: float = 1.0) -> bool:
        """Cree un lien neuronal. Refuse relations inconnues et auto-boucles."""
        if relation not in RELATIONS_VALIDES or src == dst:
            return False
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO liens(src,dst,relation,poids,horodatage) "
                "VALUES (?,?,?,?,?)", (src, dst, relation, poids, _maintenant()),
            )
            return cur.rowcount > 0

    # ── lecture ─────────────────────────────────────────────────────────
    def stats(self) -> dict[str, int]:
        with self._conn() as conn:
            compte = lambda sql: int(conn.execute(sql).fetchone()[0])  # noqa: E731
            return {
                "noeuds": compte("SELECT COUNT(*) FROM noeuds"),
                "liens": compte("SELECT COUNT(*) FROM liens"),
                "termes": compte("SELECT COUNT(DISTINCT terme) FROM index_termes"),
                "propositions": compte("SELECT COUNT(*) FROM propositions"),
                "telechargements": compte(
                    "SELECT COUNT(*) FROM telechargements WHERE statut='ok'"
                ),
            }

    def noeud(self, cle: str) -> Optional[Noeud]:
        with self._conn() as conn:
            row = conn.execute("SELECT * FROM noeuds WHERE cle=?", (cle,)).fetchone()
        return self._vers_noeud(row) if row else None

    @staticmethod
    def _vers_noeud(row: sqlite3.Row) -> Noeud:
        return Noeud(
            id=row["id"], cle=row["cle"], domaine=row["domaine"],
            titre=row["titre"], contenu=row["contenu"],
            origine=row["origine"], poids=row["poids"], url=row["url"] or "",
        )

    def voisins(self, cle: str) -> list[dict[str, Any]]:
        """Cone de connaissances autour d'un noeud (1 saut, tous relations)."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT n.cle, n.titre, n.domaine, l.relation, l.poids "
                "FROM liens l "
                "JOIN noeuds n ON n.id = l.dst "
                "WHERE l.src = (SELECT id FROM noeuds WHERE cle = ?) "
                "ORDER BY l.poids DESC",
                (cle,),
            ).fetchall()
        return [dict(r) for r in rows]

    def rechercher(self, requete: str, limite: int = 6) -> list[dict[str, Any]]:
        """Recherche plein-texte ponderee (TF * rarete) dans l'index."""
        jetons = jetonner(requete)
        if not jetons:
            return []
        placeholders = ",".join("?" * len(jetons))
        with self._conn() as conn:
            nb_total = max(1, int(
                conn.execute("SELECT COUNT(*) FROM noeuds").fetchone()[0]
            ))
            rows = conn.execute(
                f"""
                SELECT n.id, n.cle, n.domaine, n.titre, n.contenu, n.origine,
                       n.poids, n.url,
                       SUM(i.tf) AS score,
                       COUNT(DISTINCT i.terme) AS couverture
                FROM index_termes i
                JOIN noeuds n ON n.id = i.noeud_id
                WHERE i.terme IN ({placeholders})
                GROUP BY n.id
                ORDER BY score * n.poids * (1.0 + couverture * 0.25) DESC
                LIMIT ?
                """,
                (*jetons, limite),
            ).fetchall()
        total = len(jetons)
        out: list[dict[str, Any]] = []
        for r in rows:
            d = dict(r)
            d["couverture"] = round(d["couverture"] / total, 3)
            out.append(d)
        return out

    def tracer_voisinage(self, cles: str, profondeur: int = 2) -> list[dict[str, Any]]:
        """Explore le graphe de liens autour des cles donnees (BFS pondere)."""
        vus: set[str] = set()
        frontiere = [c.strip() for c in cles.split(",") if c.strip()]
        trace: dict[str, dict[str, Any]] = {}
        for _ in range(max(1, profondeur)):
            suivante: list[str] = []
            for cle in frontiere:
                if cle in vus:
                    continue
                vus.add(cle)
                n = self.noeud(cle)
                if n is None:
                    continue
                entree = n.to_dict()
                entree["voisins"] = []
                trace[cle] = entree
                for v in self.voisins(cle):
                    entree["voisins"].append(v)
                    if v["cle"] not in vus and v["cle"] not in trace:
                        suivante.append(v["cle"])
            frontiere = suivante
        return list(trace.values())

    def enregistrer_proposition(
        self, requete: str, proposition: PropositionAnalyste,
        contrat: Optional[dict[str, Any]], statut: str = "propose",
    ) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                "INSERT INTO propositions(requete,fichier,categorie,"
                "justification,contrat,statut,horodatage) VALUES (?,?,?,?,?,?,?)",
                (requete, proposition.fichier, proposition.categorie,
                 proposition.justification,
                 json.dumps(contrat, ensure_ascii=False) if contrat else None,
                 statut, _maintenant()),
            )
            return int(cur.lastrowid or 0)

    # ── alimentation ────────────────────────────────────────────────────
    def amorcer(self) -> int:
        """Insere le corpus d'amorcage + ses liens explicites. Idempotent."""
        with self._conn() as conn:
            ids: dict[str, int] = {}
            for cle, domaine, titre, contenu, liens in CORPUS:
                ids[cle] = self.inserer_noeud(
                    cle, domaine, titre, contenu, origine="amorcage", conn=conn,
                )
            for cle, domaine, titre, contenu, liens in CORPUS:
                for cible, relation in liens:
                    dst = ids.get(cible) or conn.execute(
                        "SELECT id FROM noeuds WHERE cle=?", (cible,)
                    ).fetchone()
                    if dst is None:
                        continue
                    if not isinstance(dst, int):
                        dst = int(dst[0])
                    conn.execute(
                        "INSERT OR IGNORE INTO liens(src,dst,relation,poids,"
                        "horodatage) VALUES (?,?,?,?,?)",
                        (ids[cle], dst, relation, 1.0, _maintenant()),
                    )
            conn.commit()
        self.relier_coocurrence()
        return len(CORPUS)

    def relier_coocurrence(self, seuil: int = 3, plafond: int = 400) -> int:
        """Relie deux noeuds partageant assez de termes (schema neuronal
        emergent). Cout en O(n^2) : plafonne a `plafond` noeuds."""
        with self._conn() as conn:
            noeuds = conn.execute(
                "SELECT id, cle FROM noeuds ORDER BY id LIMIT ?", (plafond,)
            ).fetchall()
            termes: dict[int, set[str]] = {}
            for n in noeuds:
                termes[n["id"]] = {
                    r[0] for r in conn.execute(
                        "SELECT terme FROM index_termes WHERE noeud_id=?",
                        (n["id"],),
                    )
                }
            ids = {n["id"]: n["cle"] for n in noeuds}
            ajouts = 0
            cles = list(termes)
            for i, a in enumerate(cles):
                for b in cles[i + 1:]:
                    partages = termes[a] & termes[b]
                    if len(partages) < seuil:
                        continue
                    poids = round(len(partages) / max(
                        1, len(termes[a] | termes[b])
                    ), 4)
                    conn.execute(
                        "INSERT OR IGNORE INTO liens(src,dst,relation,poids,"
                        "horodatage) VALUES (?,?,?,?,?)",
                        (a, b, "coocurrence", poids, _maintenant()),
                    )
                    ajouts += 1
            conn.commit()
        return ajouts


# ═════════════════════════════════════════════════════════════════════════
# 4. TELECHARGEMENT BEST-EFFORT (jamais fatal)
# ═════════════════════════════════════════════════════════════════════════

class _ExtraitHTML(HTMLParser):
    """Extraction de texte brut : ignore script/style, garde les paragraphes."""

    IGNORES = frozenset({"script", "style", "noscript", "svg", "head"})

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._ignorer = 0
        self._morceaux: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag.lower() in self.IGNORES:
            self._ignorer += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in self.IGNORES and self._ignorer:
            self._ignorer -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignorer and data.strip():
            self._morceaux.append(data.strip())

    @property
    def texte(self) -> str:
        return " ".join(self._morceaux)


def html_vers_texte(brut: str) -> str:
    parseur = _ExtraitHTML()
    try:
        parseur.feed(brut)
    except Exception:
        # HTML malforme : on retombe sur un nettoyage balise-naif.
        return re.sub(r"<[^>]+>", " ", brut)
    return parseur.texte


def _journal_telechargement(
    base: sqlite3.Connection, source: str, url: str, statut: str,
    octets: int = 0, message: str = "",
) -> None:
    base.execute(
        "INSERT INTO telechargements(source,url,statut,octets,message,"
        "horodatage) VALUES (?,?,?,?,?,?)",
        (source, url, statut, octets, message[:500], _maintenant()),
    )
    base.commit()


def telecharger(banque: BanqueAnalyste, limites: int = MAX_SOURCES) -> dict[str, Any]:
    """Recupere les sources whitelist puis en extrait des noeuds relies.

    Best-effort integral : chaque echec est enregistre dans la table
    `telechargements` et l'iteration continue. Retourne un bilan JSON-friendly.
    """
    bilan: dict[str, Any] = {"tentes": 0, "ok": 0, "echecs": 0, "noeuds": 0,
                             "details": []}
    if not actif():
        return {**bilan, "annule": "GABRIEL_DEV_ANALYSTE=0"}

    entete = {"User-Agent": "Gabriel-Dev-Analyste/1.0 (recherche universitaire)"}
    for source, url in SOURCES[:limites]:
        bilan["tentes"] += 1
        try:
            requete = urllib.request.Request(url, headers=entete)
            with urllib.request.urlopen(requete, timeout=TIMEOUT_RESEAU) as rep:
                if rep.length and int(rep.length) > MAX_OCTETS_PAGE:
                    raise ValueError(f"page trop lourde ({rep.length} octets)")
                corps = rep.read(MAX_OCTETS_PAGE)
            texte = html_vers_texte(corps.decode("utf-8", errors="replace"))
            if len(jetonner(texte)) < 40:
                raise ValueError("contenu trop pauvre pour etre indexe")
        except Exception as exc:                       # fail-closed, jamais fatal
            bilan["echecs"] += 1
            bilan["details"].append({"source": source, "statut": "echec",
                                     "message": str(exc)[:200]})
            with banque._conn() as conn:
                _journal_telechargement(conn, source, url, "echec", 0, str(exc))
            continue

        cle = "web:" + normaliser(source)[:60].replace(" ", "-").strip("-")
        nid = banque.inserer_noeud(
            cle, domaine=_domaine_devine(texte), titre=source,
            contenu=texte[:20000], origine="web", url=url, poids=0.6,
            type_="source",
        )
        # Relie la source web aux notions d'amorcage qu'elle recouvre.
        recouvertes = banque.rechercher(texte[:4000], limite=4)
        for n in recouvertes:
            if n["cle"] != cle and n["origine"] == "amorcage":
                banque.lier(nid, n["id"], "utilise",
                            poids=round(0.3 + n["couverture"], 3))
        bilan["ok"] += 1
        bilan["noeuds"] += 1
        bilan["details"].append({"source": source, "statut": "ok",
                                 "octets": len(corps)})
        with banque._conn() as conn:
            _journal_telechargement(conn, source, url, "ok", len(corps), cle)

    banque.relier_coocurrence()
    return bilan


def _domaine_devine(texte: str) -> str:
    """Classe grossierement un document recupere selon ses termes dominants."""
    scores: Counter = Counter()
    for mot, domaine in _AFFECTATIONS_DOMAINES:
        scores[domaine] += normaliser(texte).count(mot)
    return scores.most_common(1)[0][0] if any(scores.values()) else "informatique"


_AFFECTATIONS_DOMAINES: tuple[tuple[str, str], ...] = (
    ("nombre premier", "mathematiques"), ("theorie des nombres", "mathematiques"),
    ("matrix", "mathematiques"), ("eigenvalue", "mathematiques"),
    ("spectral", "geometrie"), ("manifold", "geometrie"),
    ("algorithm", "informatique"), ("complexity", "informatique"),
    ("database", "informatique"), ("software", "analyse_informatique"),
    ("requirement", "analyse_informatique"), ("test", "analyse_informatique"),
    ("logic", "logique"), ("proof", "logique"), ("computab", "logique"),
    ("numerical", "numerique"), ("floating point", "numerique"),
)


# ═════════════════════════════════════════════════════════════════════════
# 5. AUTO-ANALYSE DU DEPOT (conscience du code propre)
# ═════════════════════════════════════════════════════════════════════════

LIAISON_CONNAISSANCE = {
    "documentation_absente": ("documentation-technique", "revue-de-code"),
    "fonction_sans_docstring": ("documentation-technique", "revue-de-code"),
    "import_mort": ("revue-de-code", "architecture-logicielle"),
    "test_manquant": ("tests-logiciels", "specification-fonctionnelle"),
    "marqueur_todo": ("specification-fonctionnelle", "revue-de-code"),
}

_MARQUEURS = re.compile(r"\b(TODO|FIXME|XXX|HACK)\b")


def _trouver_marqueurs(texte: str) -> list[dict[str, Any]]:
    """Marqueurs de detude, COMMENTAIRES uniquement.

    Un TODO ecrit dans un docstring ou une chaine (pour decrire la regle) n'est
    pas un chantier ouvert : on tokenise pour ne retenir que les tokens COMMENT.
    """
    trouve: list[dict[str, Any]] = []
    try:
        for jeton in tokenize.generate_tokens(io.StringIO(texte).readline):
            if jeton.type == tokenize.COMMENT and _MARQUEURS.search(jeton.string):
                trouve.append({
                    "ligne": jeton.start[0],
                    "texte": jeton.string.strip()[:160],
                })
    except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
        # Fichier non tokenisable : repli ligne a ligne (bruyant mais complet).
        for i, ligne in enumerate(texte.splitlines(), start=1):
            if ligne.lstrip().startswith("#") and _MARQUEURS.search(ligne):
                trouve.append({"ligne": i, "texte": ligne.strip()[:160]})
    return trouve


def _ignorer(chemin: Path) -> bool:
    """True si le chemin tombe dans un dossier exclu (venv, data, build, ...).

    Seuls les DOSSIERS sont examines pour les variantes de prefixe (`.venv-1`,
    `venv-3.12`) : le nom de fichier est epargne pour ne pas exclure a tort
    un module comme `venv_utils.py`.
    """
    parties = chemin.parts
    for i, part in enumerate(parties):
        if part in DOSSIERS_EXCLUS:
            return True
        if i < len(parties) - 1 and (
            part.startswith(".venv") or part.startswith("venv")
        ):
            return True
    return False


def parcourir_py(racine: Path) -> list[Path]:
    """Tous les .py du depot hors exclus (venv, theories, build, ...)."""
    out: list[Path] = []
    for p in sorted(racine.rglob("*.py")):
        if _ignorer(p.relative_to(racine)):
            continue
        out.append(p)
    return out


def lire_carte(racine: Path = RACINE) -> list[dict[str, Any]]:
    """Reutilise la cartographie existante (gabriel_repo_mapper) si presente."""
    chemin = racine / "data" / "gabriel_repo_map.db"
    if not chemin.exists():
        return []
    try:
        conn = sqlite3.connect(chemin)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT rel_path, role, score, keywords FROM files "
            "ORDER BY score DESC LIMIT 300"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def analyser_fichier(chemin: Path) -> dict[str, Any]:
    """Passe statique locale : docstrings, imports morts, marqueurs, syntaxe."""
    result: dict[str, Any] = {
        "chemin": chemin, "todos": [], "imports_morts": [], "doc_module": False,
        "premiere_def": 1, "fonctions_sans_doc": [], "parseable": True,
        "taille": 0, "texte": "",
    }
    try:
        texte = chemin.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        result["parseable"] = False
        return result
    result["taille"] = len(texte)
    result["texte"] = texte
    result["todos"] = _trouver_marqueurs(texte)
    try:
        arbre = ast.parse(texte, filename=str(chemin))
    except SyntaxError:
        result["parseable"] = False
        return result

    result["doc_module"] = bool(ast.get_docstring(arbre))
    if not result["doc_module"]:
        for node in arbre.body:
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                                 ast.AsyncFunctionDef, ast.ClassDef)):
                result["premiere_def"] = node.lineno
                break
        else:
            result["premiere_def"] = 1

    importes: dict[str, int] = {}
    for node in ast.walk(arbre):
        if isinstance(node, ast.Import):
            # Import etalant sur plusieurs lignes : sa suppression isolee
            # casserait la syntaxe — on ne le propose pas.
            if (node.end_lineno or node.lineno) != node.lineno:
                continue
            for a in node.names:
                nom = (a.asname or a.name).split(".")[0]
                importes[nom] = node.lineno
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            if (node.end_lineno or node.lineno) != node.lineno:
                continue
            for a in node.names:
                if a.name == "*":
                    continue
                importes[a.asname or a.name] = node.lineno
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                result["fonctions_sans_doc"].append(
                    {"nom": node.name, "ligne": node.lineno}
                )
    # Un import est "mort" s'il n'apparait plus nulle part ailleurs dans le corps.
    corps = [n for n in ast.walk(arbre) if not isinstance(n, (ast.Import, ast.ImportFrom))]
    utilises: set[str] = set()
    for n in corps:
        if isinstance(n, ast.Name):
            utilises.add(n.id)
        elif isinstance(n, ast.Attribute):
            utilises.add(n.value.id if isinstance(n.value, ast.Name) else "")
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            utilises.update(jetonner(n.value))
    for nom, ligne in importes.items():
        if nom not in utilises and _suppression_valide(texte, ligne):
            result["imports_morts"].append({"nom": nom, "ligne": ligne})
    return result


def _suppression_valide(texte: str, ligne: int) -> bool:
    """Verifie a priori que retirer la ligne conserve un module parseable."""
    lignes = texte.splitlines()
    if not 1 <= ligne <= len(lignes):
        return False
    cible = lignes[ligne - 1].strip()
    if not (cible.startswith("import ") or cible.startswith("from ")):
        return False
    candidat = "\n".join(lignes[:ligne - 1] + lignes[ligne:])
    if not candidat.strip():
        return False
    try:
        ast.parse(candidat)
    except SyntaxError:
        return False
    # L'import doit rester inutilise une fois retire (cas des aliases partiels).
    return True


def modules_sans_test(racine: Path = RACINE) -> set[str]:
    """Modules src/** pour lesquels aucun tests/test_<nom>.py n'existe."""
    tests = {p.stem[5:] for p in (racine / "tests").glob("test_*.py")}
    manquants: set[str] = set()
    src = racine / "src"
    if not src.exists():
        return manquants
    for p in src.rglob("*.py"):
        if p.name == "__init__.py" or _ignorer(p.relative_to(racine)):
            continue
        if p.stem not in tests and not p.stem.startswith("_"):
            manquants.add(p.stem)
    return manquants


# ═════════════════════════════════════════════════════════════════════════
# 6. PROPOSITIONS D'AMELIORATION (contrat au format du variateur)
# ═════════════════════════════════════════════════════════════════════════

def _relatif(chemin: Path, racine: Path) -> str:
    try:
        return chemin.relative_to(racine).as_posix()
    except ValueError:
        return chemin.as_posix()


def _doc_module_proposee(rel: str, titres: list[str]) -> str:
    matiere = ", ".join(titres[:3]) or "analyse informatique"
    return (
        '"""' + rel.replace('"', "'") + " — module analyse par "
        "Gabriel_Dev_analyste_informatique.\n\n"
        "Competences mobilisees : " + matiere + ".\n"
        '"""\n\n'
    )


def construire_propositions(
    banque: BanqueAnalyste, requete: str, racine: Path = RACINE,
    par_fichier: int = 2, plafond: int = 40,
) -> list[PropositionAnalyste]:
    """Transforme l'auto-analyse du depot en propositions concretes.

    Chaque proposition emporte (quand c'est possible) une operation de patch
    valide pour le variateur sandboxe ; sinon elle reste informative.
    """
    if not actif():
        return []
    contexte = banque.rechercher(requete, limite=5)
    titres = [c["titre"] for c in contexte]
    prop: list[PropositionAnalyste] = []

    for chemin in parcourir_py(racine):
        if len(prop) >= plafond:
            break
        rel = _relatif(chemin, racine)
        analyse = analyser_fichier(chemin)
        if not analyse["parseable"]:
            continue
        emis = 0

        if not analyse["doc_module"] and emis < par_fichier:
            prop.append(PropositionAnalyste(
                categorie="documentation_absente", fichier=rel,
                titre="Module sans docstring",
                justification=(
                    "Aucune docstring de module : le POURQUOI de ce fichier "
                    "n'est pas documente, ce qui rend l'auto-analyse du depot "
                    "incomplete. Competences : "
                    + ", ".join(LIAISON_CONNAISSANCE["documentation_absente"])
                ),
                ligne=analyse["premiere_def"],
                operation={
                    "op": "inserer_lignes",
                    "cible": rel,
                    "ligne_insertion": max(1, analyse["premiere_def"]),
                    "contenu": _doc_module_proposee(rel, titres),
                },
                noeuds_connaissance=list(
                    LIAISON_CONNAISSANCE["documentation_absente"]),
            ))
            emis += 1

        if analyse["imports_morts"] and emis < par_fichier:
            imp = analyse["imports_morts"][0]
            prop.append(PropositionAnalyste(
                categorie="import_mort", fichier=rel, ligne=imp["ligne"],
                titre=f"Import inutilise : {imp['nom']}",
                justification=(
                    f"L'import `{imp['nom']}` (ligne {imp['ligne']}) n'est plus "
                    "recharge nulle part : cout de chargement et bruit pour la "
                    "revue de code. Competences : "
                    + ", ".join(LIAISON_CONNAISSANCE["import_mort"])
                ),
                operation={
                    "op": "supprimer_lignes", "cible": rel,
                    "ligne_debut": imp["ligne"], "ligne_fin": imp["ligne"],
                },
                noeuds_connaissance=list(LIAISON_CONNAISSANCE["import_mort"]),
            ))
            emis += 1

        if analyse["todos"] and emis < par_fichier:
            todo = analyse["todos"][0]
            prop.append(PropositionAnalyste(
                categorie="marqueur_todo", fichier=rel, ligne=todo["ligne"],
                titre="Detude non resolue",
                justification=(
                    f"Marqueur de detude ligne {todo['ligne']} : {todo['texte']}. "
                    "Aucun patch automatique n'est propose : remplacer un TODO "
                    "par une implementation supposee serait une affirmation non "
                    "verifiee. La pointe est signalee pour arbitrage humain."
                ),
                operation=None,
                noeuds_connaissance=list(LIAISON_CONNAISSANCE["marqueur_todo"]),
            ))
            emis += 1

    # Tests manquants : une proposition = un fichier de test auto-genere.
    for nom in sorted(modules_sans_test(racine))[: max(0, plafond - len(prop))]:
        prop.append(PropositionAnalyste(
            categorie="test_manquant", fichier=f"src/**/{nom}.py",
            titre=f"Module `{nom}` sans test",
            justification=(
                "Aucun tests/test_" + nom + ".py : le module ne peut etre "
                "ameliore en confiance sans filet de non-regression. "
                "Competences : " + ", ".join(LIAISON_CONNAISSANCE["test_manquant"])
            ),
            operation={
                "op": "creer_fichier",
                "cible": f"tests/test_{nom}_propose.py",
                "contenu": _test_propose(nom),
            },
            noeuds_connaissance=list(LIAISON_CONNAISSANCE["test_manquant"]),
        ))

    return prop[:plafond]


def _test_propose(nom: str) -> str:
    """Test de non-regression sans dependance externe (parse + compile)."""
    return (
        '"""Test propose par Gabriel_Dev_analyste_informatique (amorcage).\n\n'
        "Aucune dependance externe : il verifie que la source reste parsee et\n"
        'compilable, filet minimal avant enrichissement humain.\n"""\n'
        "from __future__ import annotations\n\n"
        "import ast\n"
        "from pathlib import Path\n\n\n"
        f"def test_{nom}_parseable():\n"
        '    racine = Path(__file__).resolve().parents[1]\n'
        f"    cibles = [p for p in racine.rglob('{nom}.py')\n"
        '              if ".venv" not in p.parts and "__pycache__" not in p.parts]\n'
        "    assert cibles, f\"module introuvable : {nom}\"\n"
        "    for source in cibles:\n"
        "        texte = source.read_text(encoding=\"utf-8\")\n"
        "        ast.parse(texte, filename=str(source))\n"
        "        compile(texte, str(source), \"exec\")\n"
    )


def contrat_pour(
    proposition: PropositionAnalyste, requete: str,
) -> Optional[dict[str, Any]]:
    """Contrat `meta` + `operations` attendu par PipelineAutoProgrammation."""
    if proposition.operation is None:
        return None
    variateur = _charger_variateur()
    if variateur is not None:
        return variateur.construire_contrat_squelette(
            role="dev-analyste",
            mots_cles=jetonner(requete)[:12],
            operation=proposition.operation,
            description=f"{proposition.categorie} — {proposition.fichier}",
        )
    # Repli autonome : meme forme que le variateur si le module est absent.
    return {
        "meta": {
            "nom": "gabriel-dev-analyste",
            "description": f"{proposition.categorie} — {proposition.fichier}",
            "role": "dev-analyste",
            "mots_cles": jetonner(requete)[:12],
            "version": "1.0",
        },
        "operations": [dict(proposition.operation)],
    }


# ═════════════════════════════════════════════════════════════════════════
# 7. SIMULATION EN SANDBOX (dry-run par defaut)
# ═════════════════════════════════════════════════════════════════════════

def _amorcer_cibles(
    pipe: Any, contrats: list[dict[str, Any]], racine: Path,
) -> int:
    """Copie dans la sandbox les fichiers cibles qui doivent exister.

    Sans cela, une operation `inserer_lignes` / `supprimer_lignes` /
    `remplacer_texte` echouerait faute de cible : la simulation doit pouvoir
    valider la syntaxe du resultat. Seule la SANDBOX est ecrite.
    """
    recopie = 0
    for contrat in contrats:
        for op in contrat.get("operations", []):
            if op.get("op") == "creer_fichier":
                continue
            cible = op.get("cible", "")
            source = (racine / cible).resolve()
            try:
                dest = pipe._resoudre(cible)
            except Exception:
                continue
            if dest.exists() or not source.is_file():
                continue
            if racine.resolve() not in source.parents:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(source.read_bytes())
            recopie += 1
    return recopie


def simuler(
    contrats: list[dict[str, Any]],
    ecrire: bool = False,
    racine: Path = RACINE,
    dossier: Optional[Path] = None,
) -> list[dict[str, Any]]:
    """Applique les contrats dans une SANDBOX isolee. Jamais le depot vivant.

    ecrire=False (defaut) : pure simulation. ecrire=True (GABRIEL_RECURSIVE_APPLY)
    : ecrit dans data/analyste/sandbox/ uniquement.
    """
    variateur = _charger_variateur()
    if variateur is None:
        return [{"statut": "indisponible", "raison": "variateur introuvable"}]
    if not contrats:
        return []
    if dossier is not None:
        racine_sandbox = dossier
    elif racine == RACINE:
        racine_sandbox = DOSSIER_SANDBOX
    else:
        # Depot de test : sandbox temporaire pour ne pas polluer la vraie.
        racine_sandbox = Path(tempfile.mkdtemp(prefix="gabriel_analyste_"))
    racine_sandbox.mkdir(parents=True, exist_ok=True)
    pipe = variateur.PipelineAutoProgrammation(
        sandbox_root=racine_sandbox, dry_run=not ecrire,
    )
    _amorcer_cibles(pipe, contrats, racine)
    return [pipe.appliquer_contrat(c) for c in contrats]

# ═════════════════════════════════════════════════════════════════════════
# 8. ORCHESTRATION + CLI
# ═════════════════════════════════════════════════════════════════════════

def analyser(
    requete: str,
    banque: Optional[BanqueAnalyste] = None,
    racine: Path = RACINE,
    alimenter_web: bool = False,
    ecrire_sandbox: bool = False,
    plafond: int = 12,
    journal: bool = True,
) -> dict[str, Any]:
    """Boucle complete : banque -> contexte -> analyse depot -> patches simules.

    Retourne un rapport JSON-friendly. Ne quitte jamais en exception pour un
    defaut reseau ou une lecture de fichier : les echecs sont des donnees.
    """
    resultat: dict[str, Any] = {
        "requete": requete, "horodatage": _maintenant(), "actif": actif(),
        "contexte": [], "propositions": [], "contrats": 0,
        "simulations": [], "carte": 0, "erreurs": [],
    }
    if not actif():
        resultat["annule"] = f"{KILL_SWITCH}=0"
        return resultat

    try:
        base = banque or BanqueAnalyste()
        if base.stats()["noeuds"] == 0:
            base.amorcer()
        resultat["carte"] = len(lire_carte(racine))
        if alimenter_web:
            resultat["telechargement"] = telecharger(base)
        resultat["contexte"] = base.rechercher(requete, limite=6)
        propositions = construire_propositions(
            base, requete, racine=racine, plafond=plafond,
        )
    except Exception as exc:
        resultat["erreurs"].append(f"analyse : {exc}")
        return resultat

    contrats: list[dict[str, Any]] = []
    for p in propositions:
        contrat = contrat_pour(p, requete)
        lignes = p.to_dict()
        lignes["contrat"] = contrat
        resultat["propositions"].append(lignes)
        if contrat is not None:
            contrats.append(contrat)
            try:
                base.enregistrer_proposition(requete, p, contrat)
            except Exception as exc:
                resultat["erreurs"].append(f"journal : {exc}")
    resultat["contrats"] = len(contrats)

    try:
        resultat["simulations"] = simuler(
            contrats, ecrire=ecrire_sandbox, racine=racine,
        )
    except Exception as exc:
        resultat["erreurs"].append(f"simulation : {exc}")

    if journal:
        ecrire_rapport(resultat, racine)
    return resultat


def ecrire_rapport(rapport: dict[str, Any], racine: Path = RACINE) -> Optional[Path]:
    """Persiste le rapport JSON sous data/analyste/rapports/ (jamais ailleurs)."""
    try:
        DOSSIER_RAPPORTS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        chemin = DOSSIER_RAPPORTS / f"rapport_{stamp}.json"
        chemin.write_text(
            json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8",
        )
        return chemin
    except Exception:
        return None

def resume_texte(rapport: dict[str, Any]) -> str:
    """Affichage console concis (stdlib seule : pas de Rich ici)."""
    if not rapport.get("actif", True):
        return f"[analyste] desactive ({rapport.get('annule')})"
    patchables = [p for p in rapport["propositions"] if p["patchable"]]
    sim_ok = sum(
        1 for s in rapport["simulations"]
        if (s.get("simules", 0) or s.get("ok", 0)) and not s.get("echouees")
    )
    lignes = [
        "[analyste] banque : "
        f"{len(rapport['contexte'])} notions de contexte, "
        f"{rapport['carte']} fichiers cartographies",
        f"[analyste] {len(rapport['propositions'])} proposition(s), "
        f"{len(patchables)} patchable(s), {rapport['contrats']} contrat(s), "
        f"{sim_ok} simulation(s) propre(s)",
    ]
    for p in rapport["propositions"][:8]:
        marque = "PATCH" if p["patchable"] else "NOTE"
        lignes.append(
            f"  [{marque}] {p['categorie']:<24} {p['fichier']}"
            + (f":{p['ligne']}" if p["ligne"] else "")
        )
    for err in rapport.get("erreurs", []):
        lignes.append(f"  ! {err}")
    return "\n".join(lignes)


def _construire_cli() -> argparse.ArgumentParser:
    parseur = argparse.ArgumentParser(
        prog="Gabriel_Dev_analyste_informatique",
        description="Banque d'analyste + auto-analyse du depot + patches simules.",
    )
    parseur.add_argument("--initialiser", action="store_true",
                         help="Amorce le corpus hors-ligne dans SQLite")
    parseur.add_argument("--telecharger", action="store_true",
                         help="Tente le telechargement web (best-effort)")
    parseur.add_argument("--consulter", metavar="REQUETE", default=None,
                         help="Interroge la banque de connaissances")
    parseur.add_argument("--voisinage", metavar="CLES", default=None,
                         help="Trace le graphe de liens (cles separees par ,)")
    parseur.add_argument("--analyser", metavar="REQUETE", default=None,
                         help="Auto-analyse du depot + propositions de patch")
    parseur.add_argument("--appliquer-sandbox", action="store_true",
                         help="Ecrit les patches dans data/analyste/sandbox "
                              "(sinon dry-run)")
    parseur.add_argument("--stats", action="store_true", help="Etat de la banque")
    parseur.add_argument("--json", action="store_true",
                         help="Sortie JSON sur la sortie standard")
    return parseur


def main(argv: Optional[list[str]] = None) -> int:
    args = _construire_cli().parse_args(argv)
    if not actif():
        print(f"[analyste] desactive : {KILL_SWITCH}=0")
        return 0

    banque = BanqueAnalyste()
    if not any((args.initialiser, args.telecharger, args.consulter,
                args.analyser, args.stats, args.voisinage)):
        args.stats = True

    if args.initialiser:
        print(f"[analyste] corpus d'amorcage : {banque.amorcer()} notions")
    if args.telecharger:
        bilan = telecharger(banque)
        print(f"[analyste] telechargement : {bilan['ok']}/{bilan['tentes']} ok, "
              f"{bilan['echecs']} echec(s) (non bloquants)")
    if args.consulter:
        ctx = banque.rechercher(args.consulter, limite=8)
        if args.json:
            print(json.dumps(ctx, ensure_ascii=False, indent=2))
        else:
            for n in ctx:
                print(f"  {n['couverture']:.2f}  {n['cle']:<34} {n['titre']}")
            if not ctx:
                print("  (aucune notion correspondante)")
    if args.voisinage:
        print(json.dumps(
            banque.tracer_voisinage(args.voisinage, profondeur=2),
            ensure_ascii=False, indent=2,
        ))
    if args.analyser:
        rapport = analyser(
            args.analyser, banque=banque, ecrire_sandbox=args.appliquer_sandbox,
        )
        print(json.dumps(rapport, ensure_ascii=False, indent=2)
              if args.json else resume_texte(rapport))
    if args.stats:
        s = banque.stats()
        print("[analyste] " + ", ".join(f"{k}={v}" for k, v in s.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
