#!/usr/bin/env python3
"""Pipeline automatique de production du rapport / document présentenciel (.tex).

Étapes (exécutées comme une mécanique, sans intervention manuelle) :

  1. Téléchargement des sources officielles (Barreau du Québec, doctrine,
     législation, jurisprudence) et journalisation dans SQLite.
  2. Construction d'une base SQLite dont le graphe (``noeud`` / ``lien``)
     forme un réseau pondéré : la figure logique du schéma code les
     conditions de recevabilité et les exigences de forme du dépôt.
  3. Propagation d'activation sur le graphe + application des règles de
     recevabilité (art. 721 (1) C.cr.) selon le plaidoyer.
  4. Génération mécanique du .tex du document à déposer, compilé en .pdf
     si un LaTeX est disponible sur la machine.

Usage :
    python pipeline_rapport_presentenciel.py --plaidoyer non_coupable \\
        --extrait theories/tex/extrait_faits_rapport_presentenciel.tex

Avertissement : la production automatisée ne remplace pas la révision par
un membre du Barreau du Québec avant tout dépôt au palais de justice.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR = REPO_ROOT / "data" / "rapport_presentenciel"
DEFAULT_DB = DATA_DIR / "rapport_presentenciel.db"
DEFAULT_EXTRAIT = REPO_ROOT / "theories" / "tex" / "extrait_faits_rapport_presentenciel.tex"
DEFAULT_OUT = REPO_ROOT / "docs" / "rapport_presentenciel_2026-10-23.tex"

USER_AGENT = "Mozilla/5.0 (compatible; pipeline-rapport-presentenciel/1.0)"

# Sources vérifiées (accessibilité HTTP testée à la conception du pipeline).
SOURCES: tuple[dict[str, str], ...] = (
    {
        "code": "barreau_procedure_penale",
        "titre": "Barreau du Québec — Procédure pénale",
        "url": "https://www.barreau.qc.ca/media/osyeiodv/procedure-penale.pdf",
        "categorie": "barreau",
    },
    {
        "code": "barreau_determination_peine",
        "titre": "Barreau du Québec — Détermination de la peine",
        "url": "https://www.barreau.qc.ca/media/00idra3c/penal-peine.pdf",
        "categorie": "barreau",
    },
    {
        "code": "barreau_accueil",
        "titre": "Barreau du Québec — Site officiel",
        "url": "https://www.barreau.qc.ca/",
        "categorie": "barreau",
    },
    {
        "code": "fondation_barreau_preparation_cour",
        "titre": "Fondation du Barreau du Québec — Se préparer pour la cour en matière pénale (guide 2025)",
        "url": (
            "https://fondationdubarreau.qc.ca/assets/documents/"
            "Guide_Comment-se-pr%C3%A9parer-pour-la-cour-en-mati%C3%A8re-p%C3%A9nale-VF-2025.pdf"
        ),
        "categorie": "barreau",
    },
    {
        "code": "loi_ccr_721",
        "titre": "Code criminel (Canada), art. 721 — Rapport de l'agent de probation",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/c-46/section-721.html",
        "categorie": "loi",
    },
    {
        "code": "loi_ccr_723",
        "titre": "Code criminel (Canada), art. 723 — Production d'éléments de preuve",
        "url": "https://laws-lois.justice.gc.ca/eng/acts/c-46/section-723.html",
        "categorie": "loi",
    },
    {
        "code": "doct_rapports_prealables",
        "titre": "Le carnet de droit pénal — Rapports préalables à la condamnation",
        "url": (
            "https://carnetdroitpenal.ca/fr/index.php?"
            "title=Rapports_pr%C3%A9alables_%C3%A0_la_condamnation"
        ),
        "categorie": "doctrine",
    },
    {
        "code": "doct_nguyen_qcca_2010_1053",
        "titre": "Revue de droit criminel — Nguyen c. R., 2010 QCCA 1053",
        "url": (
            "http://revuededroitcriminel.blogspot.com/2026/02/"
            "un-rapport-presentenciel-peut-etre.html"
        ),
        "categorie": "jurisprudence",
    },
    {
        "code": "regle_cour_quebec_chambre_criminelle",
        "titre": "Règles de pratique de la cour du Québec (chambre criminelle et pénale)",
        "url": (
            "https://www.canlii.org/fr/qc/legis/regl/rlrq-1981-c-t-16-r-6/"
            "derniere/rlrq-1981-c-t-16-r-6.html"
        ),
        "categorie": "regle",
    },
    {
        "code": "loi_ccr_legisquebec",
        "titre": "Code criminel (Légis Québec, version française)",
        "url": "https://www.legisquebec.gouv.qc.ca/fr/document/lc/C-46",
        "categorie": "loi",
    },
)


@dataclass
class Source:
    code: str
    titre: str
    url: str
    categorie: str
    statut: str = "hors_ligne"
    octets: int = 0
    sha256: str = ""
    type_contenu: str = ""
    texte: str = ""


@dataclass
class Decision:
    conclusion: str
    recu: bool
    titre_document: str
    motifs: list[str] = field(default_factory=list)
    demandes: list[str] = field(default_factory=list)
    regle_code: str = ""
    chemin: list[str] = field(default_factory=list)


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def configurer_console() -> None:
    """Affiche les accents et les flèches sans erreur sous Windows."""
    for flux in (sys.stdout, sys.stderr):
        reconf = getattr(flux, "reconfigure", None)
        if reconf is not None:
            try:
                reconf(encoding="utf-8", errors="replace")
            except (OSError, ValueError):  # pragma: no cover
                pass


def journaliser(conn: sqlite3.Connection, etape: str, message: str) -> None:
    conn.execute(
        "INSERT INTO journal(date_utc, etape, message) VALUES (?, ?, ?)",
        (utcnow(), etape, message),
    )
    conn.commit()
    print(f"[{etape}] {message}")


def echapper_latex(texte: str) -> str:
    """Échappe les caractères réservés de LaTeX dans une chaîne utilisateur."""
    table = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "#": r"\#",
        "$": r"\$",
        "%": r"\%",
        "&": r"\&",
        "_": r"\_",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(table.get(ch, ch) for ch in texte)


class _ExtracteurTexte(HTMLParser):
    """Extrait le texte visible d'une page HTML (stdlib uniquement)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._bout: list[str] = []
        self._ignorer = 0

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in {"script", "style", "noscript"}:
            self._ignorer += 1

    def handle_endtag(self, tag: str) -> None:  # noqa: ANN001
        if tag in {"script", "style", "noscript"} and self._ignorer:
            self._ignorer -= 1

    def handle_data(self, data: str) -> None:
        if not self._ignorer and data.strip():
            self._bout.append(data.strip())

    def texte(self) -> str:
        return " ".join(self._bout)


# ============================================================================
# Base SQLite : schéma du réseau (noeuds, liens pondérés, règles, sections)
# ============================================================================

DDL = """
CREATE TABLE IF NOT EXISTS source (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT UNIQUE NOT NULL,
    titre       TEXT NOT NULL,
    url         TEXT NOT NULL,
    categorie   TEXT NOT NULL,
    statut      TEXT NOT NULL DEFAULT 'hors_ligne',
    octets      INTEGER NOT NULL DEFAULT 0,
    sha256      TEXT NOT NULL DEFAULT '',
    type_contenu TEXT NOT NULL DEFAULT '',
    date_utc    TEXT NOT NULL,
    texte       TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS noeud (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    code      TEXT UNIQUE NOT NULL,
    type      TEXT NOT NULL,
    libelle   TEXT NOT NULL,
    contenu   TEXT NOT NULL DEFAULT '',
    source_code TEXT,
    poids     REAL NOT NULL DEFAULT 1.0,
    FOREIGN KEY (source_code) REFERENCES source(code)
);
CREATE TABLE IF NOT EXISTS lien (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    src    TEXT NOT NULL,
    dst    TEXT NOT NULL,
    type   TEXT NOT NULL,
    poids  REAL NOT NULL DEFAULT 1.0,
    UNIQUE (src, dst, type),
    FOREIGN KEY (src) REFERENCES noeud(code),
    FOREIGN KEY (dst) REFERENCES noeud(code)
);
CREATE TABLE IF NOT EXISTS regle (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    code       TEXT UNIQUE NOT NULL,
    plaidoyer  TEXT NOT NULL,
    conclusion TEXT NOT NULL,
    titre      TEXT NOT NULL,
    motif      TEXT NOT NULL,
    ref        TEXT NOT NULL,
    priorite   INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS section (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    code   TEXT UNIQUE NOT NULL,
    ordre  INTEGER NOT NULL,
    titre  TEXT NOT NULL,
    mode   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS section_decision (
    section_code  TEXT NOT NULL,
    conclusion    TEXT NOT NULL,
    PRIMARY KEY (section_code, conclusion),
    FOREIGN KEY (section_code) REFERENCES section(code)
);
CREATE TABLE IF NOT EXISTS affinite (
    source_code TEXT NOT NULL,
    noeud_code  TEXT NOT NULL,
    score       REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY (source_code, noeud_code)
);
CREATE TABLE IF NOT EXISTS journal (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    date_utc TEXT NOT NULL,
    etape    TEXT NOT NULL,
    message  TEXT NOT NULL
);
"""


TEXTE_721_1 = (
    "721 (1) Sous réserve des règlements d'application du paragraphe (2), "
    "lorsque l'accusé, autre qu'une organisation, plaide coupable ou est "
    "reconnu coupable d'une infraction, l'agent de probation est tenu, s'il "
    "est requis de le faire par le tribunal, de préparer et de déposer "
    "devant celui-ci un rapport écrit concernant l'accusé afin d'aider le "
    "tribunal à infliger une peine ou à décider si l'accusé devrait être "
    "absous en application de l'article 730."
)

TEXTE_NGUYEN = (
    "Nguyen c. R., 2010 QCCA 1053. Demande de rapport présentenciel "
    "présentée immédiatement après le verdict : refus de première instance "
    "au motif que « le rapport présentenciel devient pas très très utile » "
    "lorsque l'accusé nie l'infraction. La Cour d'appel confirme : « rien "
    "dans la loi n'oblige le juge de première instance à demander et à "
    "obtenir un rapport présentenciel ». La demande demeure recevable "
    "après une déclaration de culpabilité, mais son accueil relève de la "
    "discrétion du tribunal."
)

# ---------------------------------------------------------------------------
# Graphe initial (figure logique du schéma)
# ---------------------------------------------------------------------------
NOEUDS: tuple[tuple[str, str, str, str, str | None, float], ...] = (
    ("fait_plaidoyer", "fait", "Plaidoyer enregistré par la cour", "",
     None, 1.0),
    ("d_721_1", "disposition",
     "Art. 721 (1) C.cr. — Rapport de l'agent de probation",
     TEXTE_721_1, "loi_ccr_721", 1.0),
    ("d_721_3", "disposition", "Art. 721 (3) et (4) C.cr. — Contenu du rapport",
     "Le rapport contient, si possible : l'âge, le degré de maturité, le "
     "caractère et le comportement du délinquant ainsi que son désir de "
     "réparer le tort; ses antécédents; l'effet des mesures de rechange; "
     "tout autre renseignement exigé par le tribunal.",
     "loi_ccr_721", 0.9),
    ("d_723_3", "disposition",
     "Art. 723 (3) C.cr. — Production d'éléments de preuve",
     "Le tribunal peut exiger d'office, après avoir entendu le poursuivant "
     "et le délinquant, la présentation des éléments de preuve qui pourront "
     "l'aider à déterminer la peine.", "loi_ccr_723", 0.8),
    ("juris_nguyen", "jurisprudence", "Nguyen c. R., 2010 QCCA 1053",
     TEXTE_NGUYEN, "doct_nguyen_qcca_2010_1053", 1.0),
    ("cond_culpabilite", "condition",
     "Condition de recevabilité : l'accusé plaide coupable ou est reconnu "
     "coupable (art. 721 (1) C.cr.)", "", "loi_ccr_721", 1.0),
    ("cond_requisition", "condition",
     "Condition procédurale : le rapport n'est dû que s'il est requis par "
     "le tribunal (art. 721 (1) C.cr.)", "", "loi_ccr_721", 0.8),
    ("cond_utilite", "condition",
     "Condition d'utilité : le rapport doit pouvoir éclairer la Cour "
     "(Nguyen c. R.)", "", "doct_nguyen_qcca_2010_1053", 0.7),
    ("criterium_forme", "critere",
     "Exigences de forme du dépôt : juridiction et district, numéro de "
     "dossier, intitulé des parties, acte daté et signé, transmission au "
     "greffe", "", "barreau_procedure_penale", 0.6),
    ("dec_imm", "decision",
     "Recevabilité immédiate (plaidoyer de culpabilité)", "", None, 1.0),
    ("dec_sous_reserve", "decision",
     "Recevabilité sous réserve de la déclaration de culpabilité", "",
     None, 1.0),
    ("dec_impossible", "decision",
     "Non-recevabilité avant la réunion de la condition de l'art. 721 (1)",
     "", None, 1.0),
    ("sec_objet", "section", "Objet du document", "", None, 1.0),
    ("sec_faits", "section", "Faits allégués", "", None, 1.0),
    ("sec_cadre", "section", "Cadre juridique applicable", "", None, 1.0),
    ("sec_analyse", "section", "Analyse de recevabilité", "", None, 1.0),
    ("sec_demandes", "section", "Demandes", "", None, 1.0),
    ("sec_sources", "section", "Sources et pièces consultées", "", None, 1.0),
    ("sec_signature", "section", "Signature et dépôt", "", None, 1.0),
)

LIENS: tuple[tuple[str, str, str, float], ...] = (
    ("fait_plaidoyer", "cond_culpabilite", "pose_condition", 1.0),
    ("d_721_1", "cond_culpabilite", "pose_condition", 1.0),
    ("d_721_1", "cond_requisition", "pose_condition", 0.8),
    ("cond_utilite", "juris_nguyen", "fonde_sur", 0.9),
    ("d_721_1", "dec_imm", "produit", 0.95),
    ("juris_nguyen", "dec_sous_reserve", "produit", 0.9),
    ("juris_nguyen", "dec_imm", "contredit", 0.6),
    ("d_721_1", "sec_cadre", "ordonne", 1.0),
    ("d_721_3", "sec_cadre", "ordonne", 0.9),
    ("d_723_3", "sec_cadre", "ordonne", 0.8),
    ("juris_nguyen", "sec_analyse", "ordonne", 1.0),
    ("fait_plaidoyer", "sec_faits", "ordonne", 1.0),
    ("criterium_forme", "sec_objet", "ordonne", 0.5),
    ("criterium_forme", "sec_sources", "ordonne", 0.5),
    ("dec_imm", "sec_objet", "ordonne", 1.0),
    ("dec_imm", "sec_analyse", "ordonne", 1.0),
    ("dec_imm", "sec_demandes", "ordonne", 1.0),
    ("dec_imm", "sec_signature", "ordonne", 1.0),
    ("dec_sous_reserve", "sec_objet", "ordonne", 1.0),
    ("dec_sous_reserve", "sec_analyse", "ordonne", 1.0),
    ("dec_sous_reserve", "sec_demandes", "ordonne", 1.0),
    ("dec_sous_reserve", "sec_signature", "ordonne", 1.0),
    ("dec_impossible", "sec_objet", "ordonne", 1.0),
    ("dec_impossible", "sec_analyse", "ordonne", 1.0),
    ("dec_impossible", "sec_signature", "ordonne", 1.0),
)

REGLES: tuple[tuple[str, str, str, str, str, str, int], ...] = (
    ("R_COUPABLE", "coupable", "IMMEDIATE",
     "Recevabilité immédiate de la demande",
     "L'accusé plaide coupable : la condition posée à l'article 721 (1) du "
     "Code criminel est réunie (« plaide coupable ou est reconnu coupable ») "
     "et le tribunal peut être requis de faire confectionner un rapport "
     "présentenciel.", "d_721_1", 10),
    ("R_NON_COUPABLE", "non_coupable", "SOUS_RESERVE_VERDICT",
     "Recevabilité sous réserve de la déclaration de culpabilité",
     "Le plaidoyer est de non-culpabilité : la condition de l'article 721 "
     "(1) du Code criminel n'est pas réunie, aucun rapport présentenciel ne "
     "pouvant être ordonné tant que l'accusé n'est pas déclaré coupable. La "
     "demande devient recevable après le verdict de culpabilité, sous la "
     "discrétion du tribunal (Nguyen c. R., 2010 QCCA 1053). Entre-temps, "
     "la défense dépose ses observations et la preuve dont elle entend "
     "soutenir sa position.", "juris_nguyen", 10),
    ("R_VERDICT_NEGATIF", "acquittement", "IMPOSSIBLE",
     "Non-recevabilité après acquittement",
     "Un acquittement met fin à la procédure de sentence : l'article 721 "
     "(1) du Code criminel ne vise que l'accusé plaide coupable ou reconnu "
     "coupable, de sorte qu'aucun rapport présentenciel ne peut être ordonné.",
     "d_721_1", 10),
)

SECTIONS: tuple[tuple[str, int, str, str], ...] = (
    ("sec_objet", 1, "Objet du document", "objet"),
    ("sec_faits", 2, "Faits allégués", "faits"),
    ("sec_cadre", 3, "Cadre juridique applicable", "cadre"),
    ("sec_analyse", 4, "Analyse de recevabilité", "analyse"),
    ("sec_demandes", 5, "Demandes", "demandes"),
    ("sec_sources", 6, "Sources et pièces consultées", "sources"),
    ("sec_signature", 7, "Signature et dépôt", "signature"),
)

# Sections produites selon la conclusion de la règle de recevabilité.
SECTION_DECISION: tuple[tuple[str, str], ...] = tuple(
    (sec_code, conclusion)
    for conclusion in ("IMMEDIATE", "SOUS_RESERVE_VERDICT", "IMPOSSIBLE")
    for sec_code, *_ in SECTIONS
    if not (conclusion == "IMPOSSIBLE" and sec_code == "sec_demandes")
)


def ouvrir_base(chemin: Path) -> sqlite3.Connection:
    """Crée (si nécessaire) et configure la base SQLite du pipeline."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(chemin))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(DDL)
    return conn


def semer(conn: sqlite3.Connection) -> None:
    """Insère (idempotent) le réseau de base dans la base SQLite."""
    for spec in SOURCES:
        conn.execute(
            "INSERT OR IGNORE INTO source(code, titre, url, categorie, "
            "date_utc) VALUES (?, ?, ?, ?, ?)",
            (spec["code"], spec["titre"], spec["url"], spec["categorie"],
             utcnow()),
        )
    conn.executemany(
        "INSERT OR IGNORE INTO noeud(code, type, libelle, contenu, "
        "source_code, poids) VALUES (?, ?, ?, ?, ?, ?)",
        NOEUDS,
    )
    conn.executemany(
        "INSERT OR IGNORE INTO lien(src, dst, type, poids) VALUES (?, ?, ?, ?)",
        LIENS,
    )
    conn.executemany(
        "INSERT OR IGNORE INTO regle(code, plaidoyer, conclusion, titre, "
        "motif, ref, priorite) VALUES (?, ?, ?, ?, ?, ?, ?)",
        REGLES,
    )
    conn.executemany(
        "INSERT OR IGNORE INTO section(code, ordre, titre, mode) "
        "VALUES (?, ?, ?, ?)",
        SECTIONS,
    )
    conn.executemany(
        "INSERT OR IGNORE INTO section_decision(section_code, conclusion) "
        "VALUES (?, ?)",
        SECTION_DECISION,
    )
    conn.commit()


# ============================================================================
# Étape 1 — Téléchargement des sources (Barreau du Québec et autres)
# ============================================================================

def _extraire_texte(data: bytes, type_contenu: str) -> str:
    if "html" in type_contenu:
        parseur = _ExtracteurTexte()
        try:
            parseur.feed(data.decode("utf-8", "replace"))
        except Exception:  # pragma: no cover - parseur tolérant
            return ""
        return parseur.texte()[:200000]
    if "pdf" in type_contenu:
        # Aucune dépendance externe : on conserve uniquement l'empreinte.
        return ""
    return data.decode("utf-8", "replace")[:200000]


def telecharger_sources(conn: sqlite3.Connection, hors_ligne: bool = False,
                        delai: int = 20) -> None:
    """Télécharge chaque source et enregistre le résultat dans la base."""
    for spec in SOURCES:
        code = spec["code"]
        if hors_ligne:
            conn.execute(
                "UPDATE source SET statut = 'hors_ligne' WHERE code = ?",
                (code,),
            )
            journaliser(conn, "telechargement",
                        f"{code} : ignoré (mode hors ligne)")
            continue
        try:
            requete = Request(spec["url"], headers={"User-Agent": USER_AGENT})
            with urlopen(requete, timeout=delai) as rep:
                data = rep.read()
                type_contenu = rep.headers.get("Content-Type", "")
                statut = "telecharge"
        except HTTPError as exc:
            data, type_contenu, statut = b"", "", f"echec_http_{exc.code}"
        except (URLError, TimeoutError, OSError) as exc:
            data, type_contenu, statut = b"", "", f"echec_{type(exc).__name__}"
        texte = _extraire_texte(data, type_contenu)
        conn.execute(
            "UPDATE source SET statut = ?, octets = ?, sha256 = ?, "
            "type_contenu = ?, date_utc = ?, texte = ? WHERE code = ?",
            (statut, len(data), hashlib.sha256(data).hexdigest(),
             type_contenu, utcnow(), texte, code),
        )
        journaliser(conn, "telechargement",
                    f"{code} : {statut} ({len(data)} octets)")
    conn.commit()


# ============================================================================
# Étape 2 — Mise en relation interne (affinités) et propagation d'activation
# ============================================================================

_MOTS_VIDES = {
    "le", "la", "les", "un", "une", "des", "du", "de", "et", "ou", "que",
    "qui", "pour", "dans", "sur", "au", "aux", "en", "est", "sont", "par",
    "avec", "plus", "tout", "tous", "toute", "cette", "ces", "son", "sa",
    "ses", "il", "elle", "ils", "ne", "pas", "se", "auquel", "auxquels",
}


def _jetonner(texte: str) -> set[str]:
    mots = re.findall(r"[a-zA-Zàâçéèêëîïôûùüÿœ]+", texte.lower())
    return {m for m in mots if len(m) > 3 and m not in _MOTS_VIDES}


def calculer_affinites(conn: sqlite3.Connection) -> int:
    """Relie chaque source téléchargée aux nœuds par similarité lexical."""
    conn.execute("DELETE FROM affinite")
    noeuds = conn.execute(
        "SELECT code, libelle || ' ' || contenu AS corpus FROM noeud"
    ).fetchall()
    sources = conn.execute(
        "SELECT code, titre || ' ' || texte AS corpus FROM source "
        "WHERE statut = 'telecharge'"
    ).fetchall()
    total = 0
    for src in sources:
        jetons_src = _jetonner(src["corpus"])
        if not jetons_src:
            continue
        for noeud in noeuds:
            jetons_noeud = _jetonner(noeud["corpus"])
            if not jetons_noeud:
                continue
            score = len(jetons_src & jetons_noeud) / len(jetons_noeud)
            if score > 0.05:
                conn.execute(
                    "INSERT OR REPLACE INTO affinite(source_code, "
                    "noeud_code, score) VALUES (?, ?, ?)",
                    (src["code"], noeud["code"], round(score, 4)),
                )
                total += 1
    conn.commit()
    return total


def propager(conn: sqlite3.Connection, depart: str,
             profondeur: int = 3) -> dict[str, float]:
    """Propage l'activation sur le graphe pondéré (figure logique du schéma)."""
    activation: dict[str, float] = {depart: 1.0}
    frontier = [depart]
    for _ in range(profondeur):
        suivant: list[str] = []
        for noeud in frontier:
            base = activation.get(noeud, 0.0)
            for ligne in conn.execute(
                "SELECT dst, poids FROM lien WHERE src = ?", (noeud,)
            ):
                nouveau = base * float(ligne["poids"])
                if nouveau > activation.get(ligne["dst"], 0.0):
                    activation[ligne["dst"]] = nouveau
                    suivant.append(ligne["dst"])
        frontier = suivant
    return activation


# ============================================================================
# Étape 3 — Recevabilité (art. 721 (1) C.cr.) et circuit de sections
# ============================================================================

TITRES_DECISION = {
    "IMMEDIATE": (
        "Demande de confection d'un rapport présentenciel "
        "(article 721 (1) du Code criminel)"
    ),
    "SOUS_RESERVE_VERDICT": (
        "Demande de confection d'un rapport présentenciel sous réserve de la "
        "déclaration de culpabilité et observations de la défense "
        "(article 721 (1) du Code criminel)"
    ),
    "IMPOSSIBLE": (
        "Avis de non-recevabilité d'un rapport présentenciel "
        "(article 721 (1) du Code criminel)"
    ),
}

DEMANDES_PAR_CONCLUSION = {
    "IMMEDIATE": [
        "Ordonner à l'agent de probation du district de préparer, en "
        "application de l'article 721 (1) du Code criminel, un rapport écrit "
        "concernant l'accusé.",
        "Fixer le délai dans lequel le rapport devra être déposé avant la "
        "détermination de la peine.",
        "Autoriser la défense à déposer ses observations écrites dans les "
        "dix jours suivant la réception du rapport.",
    ],
    "SOUS_RESERVE_VERDICT": [
        "Prendre acte du plaidoyer de non-culpabilité enregistré.",
        "Dans l'éventualité d'un verdict de culpabilité, ordonner dès lors la "
        "confection d'un rapport présentenciel conformément à l'article 721 "
        "(1) du Code criminel, le tribunal n'y étant pas tenu mais pouvant "
        "y procéder sur demande.",
        "À défaut, accorder à la défense le délai de coutume pour déposer "
        "ses observations écrites en vue de la détermination de la peine.",
        "Déclarer recevable le présent document, qui vaut observations "
        "écrites de la défense aux termes de l'article 723 (3) du Code "
        "criminel.",
    ],
    "IMPOSSIBLE": [],
}


def evaluer_recevabilite(conn: sqlite3.Connection,
                         plaidoyer: str) -> Decision:
    """Traverse le réseau de la base et conclut à la recevabilité."""
    regle = conn.execute(
        "SELECT * FROM regle WHERE plaidoyer = ? ORDER BY priorite DESC "
        "LIMIT 1",
        (plaidoyer,),
    ).fetchone()
    if regle is None:
        raise ValueError(f"Plaidoyer inconnu : {plaidoyer!r}")

    conclusion = regle["conclusion"]
    noeud_decision = {
        "IMMEDIATE": "dec_imm",
        "SOUS_RESERVE_VERDICT": "dec_sous_reserve",
        "IMPOSSIBLE": "dec_impossible",
    }[conclusion]

    activation = activation_globale(conn, noeud_decision)
    cheminement = [
        code for code, valeur in sorted(
            activation.items(), key=lambda kv: -kv[1]
        )
        if not code.startswith("sec_") and valeur >= 0.2
    ]

    motifs = [regle["motif"]]
    for code in ("cond_culpabilite", "cond_requisition", "cond_utilite"):
        noeud = conn.execute(
            "SELECT libelle FROM noeud WHERE code = ?", (code,)
        ).fetchone()
        if noeud is not None:
            motifs.append(noeud["libelle"] + ".")

    return Decision(
        conclusion=conclusion,
        recu=conclusion != "IMPOSSIBLE",
        titre_document=TITRES_DECISION[conclusion],
        motifs=motifs,
        demandes=list(DEMANDES_PAR_CONCLUSION[conclusion]),
        regle_code=regle["code"],
        chemin=cheminement,
    )


def activation_globale(conn: sqlite3.Connection,
                       noeud_decision: str) -> dict[str, float]:
    """Activation maximale issue des nœuds sources et de la décision."""
    fusion: dict[str, float] = {}
    for depart in ("d_721_1", "juris_nguyen", noeud_decision):
        for code, valeur in propager(conn, depart).items():
            fusion[code] = max(fusion.get(code, 0.0), valeur)
    return fusion


# ============================================================================
# Étape 4 — Lecture de l'extrait factuel (.tex) et génération du .tex
# ============================================================================

_RE_TITRE_TEX = re.compile(r"\\(?:sub)*section\*?\{([^}]*)\}")


def equilibre_accolades(texte: str) -> int:
    """Retourne l'écart d'accolades (0 = équilibré), hors commentaires."""
    nettoye = "\n".join(
        re.sub(r"(?<!\\)%.*", "", ligne) for ligne in texte.splitlines()
    )
    return nettoye.count("{") - nettoye.count("}")


def lire_extrait(chemin: Path) -> list[tuple[str, str]]:
    """Découpe l'extrait .tex en blocs (titre de section, corps LaTeX).

    Les lignes de commentaire (« % » en début de ligne) sont ignorées afin
    que les consignes de rédaction du fragment ne polluent pas le document.
    """
    texte = chemin.read_text(encoding="utf-8")
    texte = "\n".join(
        ligne for ligne in texte.splitlines()
        if not ligne.lstrip().startswith("%")
    )
    titres = list(_RE_TITRE_TEX.finditer(texte))
    if not titres:
        return [("Faits", texte.strip())] if texte.strip() else []
    blocs: list[tuple[str, str]] = []
    for i, m in enumerate(titres):
        debut = m.end()
        fin = titres[i + 1].start() if i + 1 < len(titres) else len(texte)
        corps = texte[debut:fin].strip()
        if corps:
            blocs.append((m.group(1).strip(), corps))
    return blocs


@dataclass
class Contexte:
    dossier: str = "[N° DE DOSSIER]"
    accuse: str = "[NOM DE L'ACCUSÉ]"
    couronne: str = "Sa Majesté la Procureure du Québec"
    avocat: str = "[NOM DE L'AVOCAT·E], membre du Barreau du Québec"
    juridiction: str = "Cour du Québec — chambre criminelle"
    district: str = "District de Québec"
    palais: str = "Palais de justice de Québec"
    salle: str = "2.15"
    date_audience: str = "23 octobre 2026"
    heure_audience: str = "9 h 30"
    infraction: str = "[INFRACTION REPROCHÉE]"
    plaidoyer: str = "non_coupable"


LIBELLE_PLAIDOYER = {
    "coupable": "coupable",
    "non_coupable": "non-culpabilité",
    "acquittement": "acquittement prononcé",
}


def _en_tete(ctx: Contexte, decision: Decision) -> list[str]:
    return [
        r"\begin{minipage}[t]{0.60\textwidth}",
        r"\textbf{" + echapper_latex(ctx.juridiction) + r"}\\",
        echapper_latex(ctx.district) + r"\\",
        echapper_latex(ctx.palais) + r"\\",
        "Salle " + echapper_latex(ctx.salle),
        r"\end{minipage}\hfill",
        r"\begin{minipage}[t]{0.37\textwidth}",
        r"\raggedleft",
        "Dossier : \textbf{" + echapper_latex(ctx.dossier) + r"}\\",
        "Accusé·e : " + echapper_latex(ctx.accuse) + r"\\",
        "Intimée : " + echapper_latex(ctx.couronne) + r"\\",
        "Plaidoyer : " + echapper_latex(
            LIBELLE_PLAIDOYER.get(ctx.plaidoyer, ctx.plaidoyer)
        ),
        r"\end{minipage}",
        r"\vspace{0.8cm}",
        r"\begin{center}",
        r"\rule{\textwidth}{0.4pt}\\[0.4em]",
        r"\textbf{\large " + echapper_latex(decision.titre_document) + r"}\\[0.3em]",
        "Infraction reprochée : " + echapper_latex(ctx.infraction) + r"\\",
        "Audience : " + echapper_latex(ctx.date_audience) + " à "
        + echapper_latex(ctx.heure_audience) + ", salle "
        + echapper_latex(ctx.salle) + r", " + echapper_latex(ctx.palais),
        r"\rule{\textwidth}{0.4pt}",
        r"\end{center}",
        "",
    ]


def _corps_section(mode: str, ctx: Contexte, decision: Decision,
                   conn: sqlite3.Connection,
                   blocs: list[tuple[str, str]]) -> list[str]:
    """Construit le corps LaTeX d'une section à partir de la base."""
    if mode == "objet":
        return [
            "Le document qui suit est produit en vue de l'audience du "
            + echapper_latex(ctx.date_audience) + " à "
            + echapper_latex(ctx.heure_audience) + ", salle "
            + echapper_latex(ctx.salle) + ", au "
            + echapper_latex(ctx.palais) + ".",
            "",
            "Son objet est double : exposer la recevabilité de la demande de "
            "confection d'un rapport présentenciel au regard de l'article "
            "721 (1) du Code criminel et, subsidiairement, valoir observations "
            "écrites de la défense.",
            "",
            "\\textbf{Conclusion du réseau de recevabilité :} "
            + echapper_latex(decision.titre_document) + " "
            "(règle appliquée : " + echapper_latex(decision.regle_code) + ").",
        ]

    if mode == "faits":
        lignes: list[str] = []
        if not blocs:
            return [
                "\\textbf{[À COMPLÉTER :]} joindre l'extrait factuel "
                "(fichier \\texttt{extrait\\_faits\\_rapport\\_presentenciel.tex})."
            ]
        pour_sous = len(blocs) > 1
        for titre, corps in blocs:
            if pour_sous:
                lignes.append("\\subsection*{" + titre + "}")
            lignes.append(corps)
            lignes.append("")
        return lignes

    if mode == "cadre":
        noeuds_decision = {
            "IMMEDIATE": "dec_imm",
            "SOUS_RESERVE_VERDICT": "dec_sous_reserve",
            "IMPOSSIBLE": "dec_impossible",
        }[decision.conclusion]
        activation = activation_globale(conn, noeuds_decision)
        lignes: list[str] = []
        selection = conn.execute(
            "SELECT code, libelle, contenu, poids, source_code FROM noeud "
            "WHERE type IN ('disposition', 'jurisprudence') "
            "ORDER BY poids DESC"
        ).fetchall()
        for noeud in selection:
            score = activation.get(noeud["code"], 0.0)
            lignes.append("\\subsection*{"
                          + echapper_latex(noeud["libelle"]) + "}")
            lignes.append(echapper_latex(noeud["contenu"]))
            ref = None
            if noeud["source_code"]:
                ref = conn.execute(
                    "SELECT titre, url, statut FROM source WHERE code = ?",
                    (noeud["source_code"],),
                ).fetchone()
            if ref is not None:
                lignes.append(
                    "\\emph{Source : " + echapper_latex(ref["titre"])
                    + " — " + echapper_latex(ref["url"])
                    + " (statut : " + echapper_latex(ref["statut"])
                    + "; activation du réseau : "
                    + format(score, ".2f") + ").}"
                )
            lignes.append("")
        return lignes

    if mode == "analyse":
        lignes = [
            "\\textbf{Règle appliquée :} "
            + echapper_latex(decision.regle_code) + ".",
            "",
            "\\textbf{Motif :}",
            "",
            "\\begin{enumerate}[leftmargin=*]",
            "\\item " + echapper_latex(decision.motifs[0]),
        ]
        for condition in decision.motifs[1:]:
            lignes.append("\\item " + echapper_latex(condition))
        lignes.append("\\end{enumerate}")
        lignes.append("")
        lignes.append(
            "\\textbf{Chemin de propagation dans le réseau ("
            + str(len(decision.chemin)) + " nœuds actifs) :}"
        )
        lignes.append("")
        lignes.append("\\texttt{" + echapper_latex(
            " -> ".join(decision.chemin)) + "}")
        lignes.append("")
        if not decision.recu:
            lignes.append(
                "En conséquence, aucun rapport présentenciel ne peut être "
                "ordonné sur le présent plaidoyer; le document est déposé "
                "comme prise de acte et comme base d'une demande subséquente."
            )
        return lignes

    if mode == "demandes":
        if not decision.demandes:
            return ["Aucune demande n'est formulée en l'état."]
        lignes = ["La défense demande au tribunal :"]
        lignes.append("")
        lignes.append("\\begin{enumerate}[leftmargin=*]")
        for demande in decision.demandes:
            lignes.append("\\item " + echapper_latex(demande))
        lignes.append("\\end{enumerate}")
        return lignes

    if mode == "sources":
        lignes = [
            "Sources téléchargées et mises en relation dans la base SQLite "
            "du pipeline :",
            "",
            "\\begin{itemize}[leftmargin=*]",
        ]
        requete = (
            "SELECT s.code, s.titre, s.url, s.statut, s.sha256, "
            "COALESCE(MAX(a.score), 0.0) AS score "
            "FROM source s LEFT JOIN affinite a ON a.source_code = s.code "
            "GROUP BY s.code ORDER BY score DESC, s.code"
        )
        for src in conn.execute(requete):
            lignes.append(
                "\\item " + echapper_latex(src["titre"])
                + " — \\texttt{" + echapper_latex(src["url"]) + "}"
                + " (statut : " + echapper_latex(src["statut"])
                + "; affinité max : " + format(float(src["score"]), ".3f")
                + "; SHA-256 : "
                + echapper_latex((src["sha256"] or "n/a")[:16]) + "…)"
            )
        lignes.append("\\end{itemize}")
        lignes.append("")
        lignes.append(
            "Le dépôt effectif au greffe (nombre de copies, format "
            "numérique, délai) doit être confirmé auprès du greffe de la "
            "juridiction saisie."
        )
        return lignes

    if mode == "signature":
        return [
            "\\vspace{1cm}",
            "\\begin{flushright}",
            "Fait à Québec, le " + echapper_latex(ctx.date_audience) + ".",
            "",
            "\\vspace{1.2cm}",
            "\\rule{6cm}{0.4pt}",
            echapper_latex(ctx.avocat),
            "Pour la défense",
            "\\end{flushright}",
        ]

    raise ValueError(f"Mode de section inconnu : {mode}")


def generer_tex(conn: sqlite3.Connection, ctx: Contexte, decision: Decision,
                blocs: list[tuple[str, str]], sortie: Path) -> Path:
    """Assemble le document .tex complet à partir des sections de la base."""
    lignes: list[str] = [
        r"\documentclass[12pt,a4paper]{article}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[french]{babel}",
        r"\usepackage{lmodern}",
        r"\usepackage{geometry}",
        r"\geometry{margin=2.5cm, top=2cm}",
        r"\usepackage{setspace}",
        r"\onehalfspacing",
        r"\usepackage{parskip}",
        r"\usepackage{enumitem}",
        r"\usepackage[hidelinks]{hyperref}",
        r"\begin{document}",
        r"\thispagestyle{empty}",
    ]
    lignes += _en_tete(ctx, decision)

    sections = conn.execute(
        "SELECT s.code, s.ordre, s.titre, s.mode FROM section s "
        "JOIN section_decision sd ON sd.section_code = s.code "
        "AND sd.conclusion = ? ORDER BY s.ordre",
        (decision.conclusion,),
    ).fetchall()
    for sec in sections:
        lignes.append("\\section{" + sec["titre"] + "}")
        lignes += _corps_section(sec["mode"], ctx, decision, conn, blocs)
        lignes.append("")

    lignes += [
        r"\vspace{0.8cm}",
        r"\hrule",
        r"\vspace{0.4em}",
        r"\small\emph{Document assemblé automatiquement par le pipeline "
        r"\texttt{pipeline\_rapport\_presentenciel.py} à partir de la base "
        r"SQLite \texttt{rapport\_presentenciel.db} (réseau de recevabilité, "
        r"art. 721 (1) C.cr.) et de l'extrait factuel fourni. Il doit être "
        r"revu par un membre du Barreau du Québec avant tout dépôt au greffe.}",
        "",
        r"\end{document}",
    ]

    sortie.parent.mkdir(parents=True, exist_ok=True)
    sortie.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return sortie


_RE_ENV = re.compile(r"\\(begin|end)\{([A-Za-z*]+)\}")
_RESERVES_HORS_ECHAPPEMENT = re.compile(r"(?<!\\)[&_$#]")


def valider_tex(chemin: Path, ctx: Contexte,
                decision: Decision) -> dict[str, object]:
    """Contrôles de forme du document généré (retourne un rapport)."""
    erreurs: list[str] = []
    avertissements: list[str] = []

    brut = chemin.read_bytes()
    if brut.startswith(b"\xef\xbb\xbf"):
        erreurs.append("BOM UTF-8 détecté.")
    try:
        texte = brut.decode("utf-8")
    except UnicodeDecodeError as exc:
        return {"ok": False, "erreurs": [f"UTF-8 invalide : {exc}"],
                "avertissements": []}

    ecart = equilibre_accolades(texte)
    if ecart:
        erreurs.append(f"Accolades déséquilibrées (écart = {ecart:+d}).")

    piles: list[str] = []
    for sens, env in _RE_ENV.findall(texte):
        if sens == "begin":
            piles.append(env)
        elif piles and piles[-1] == env:
            piles.pop()
        else:
            erreurs.append(f"Environnement « {env} » fermé sans ouverture.")
    if piles:
        erreurs.append("Environnements non fermés : " + ", ".join(piles))

    marqueurs = {
        "titre du document": decision.titre_document,
        "article 721 (1)": "721 (1)",
        "date d'audience": ctx.date_audience,
        "heure d'audience": ctx.heure_audience,
        "salle d'audience": "salle " + ctx.salle,
        "ouverture du document": r"\begin{document}",
        "fermeture du document": r"\end{document}",
    }
    for libelle, marqueur in marqueurs.items():
        if marqueur not in texte:
            erreurs.append(f"Marqueur manquant ({libelle}) : {marqueur!r}.")

    for i, ligne in enumerate(texte.splitlines(), start=1):
        if ligne.lstrip().startswith("%"):
            continue
        if _RESERVES_HORS_ECHAPPEMENT.search(ligne):
            avertissements.append(
                f"Ligne {i} : caractère réservé non échappé possible."
            )
    return {
        "ok": not erreurs,
        "erreurs": erreurs,
        "avertissements": avertissements[:40],
        "accolades_ecart": ecart,
        "octets": len(brut),
    }


def compiler_pdf(chemin_tex: Path) -> dict[str, object]:
    """Compile le .tex en .pdf si un LaTeX est installé sur la machine."""
    exe = shutil.which("pdflatex") or shutil.which("latexmk")
    if exe is None:
        return {"statut": "latex_indisponible",
                "message": "pdflatex/latexmk introuvable dans le PATH."}
    commande = [exe]
    if Path(exe).name.lower().startswith("latexmk"):
        commande += ["-pdf", "-interaction=nonstopmode"]
    else:
        commande += ["-interaction=nonstopmode", "-halt-on-error"]
    commande += [chemin_tex.name]
    try:
        proc = subprocess.run(
            commande, cwd=str(chemin_tex.parent), capture_output=True,
            text=True, timeout=300, check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"statut": "echec", "message": str(exc)}
    sortie = (proc.stdout or "")[-4000:]
    pdf = chemin_tex.with_suffix(".pdf")
    if proc.returncode == 0 and pdf.exists():
        return {"statut": "compile", "pdf": str(pdf), "sortie": sortie}
    return {"statut": "echec", "code": proc.returncode, "sortie": sortie}


# ============================================================================
# Orchestration
# ============================================================================

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pipeline de production du rapport présentenciel (.tex)"
    )
    parser.add_argument(
        "--plaidoyer",
        choices=("coupable", "non_coupable", "acquittement"),
        default="non_coupable",
        help="Plaidoyer enregistré (défaut : non_coupable)",
    )
    parser.add_argument("--extrait", type=Path, default=DEFAULT_EXTRAIT,
                        help="Extrait factuel au format .tex")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB,
                        help="Base SQLite du réseau de recevabilité")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="Fichier .tex à produire")
    parser.add_argument("--report", type=Path, default=None,
                        help="Rapport JSON (défaut : <out>.report.json)")
    parser.add_argument("--offline", action="store_true",
                        help="Ne rien télécharger (utilise la base existante)")
    parser.add_argument("--no-compile", action="store_true",
                        help="Ne pas tenter la compilation PDF")
    parser.add_argument("--dossier", default="[N° DE DOSSIER]")
    parser.add_argument("--accuse", default="[NOM DE L'ACCUSÉ]")
    parser.add_argument("--couronne", default="Sa Majesté la Procureure du Québec")
    parser.add_argument("--avocat", default="[NOM DE L'AVOCAT·E], membre du Barreau du Québec")
    parser.add_argument("--juridiction", default="Cour du Québec — chambre criminelle")
    parser.add_argument("--district", default="District de Québec")
    parser.add_argument("--palais", default="Palais de justice de Québec")
    parser.add_argument("--salle", default="2.15")
    parser.add_argument("--date-audience", default="23 octobre 2026")
    parser.add_argument("--heure-audience", default="9 h 30")
    parser.add_argument("--infraction", default="[INFRACTION REPROCHÉE]")
    args = parser.parse_args(argv)
    configurer_console()

    conn = ouvrir_base(args.db)
    try:
        semer(conn)
        journaliser(conn, "base", f"base prête : {args.db}")

        telecharger_sources(conn, hors_ligne=args.offline)
        nb_affinites = calculer_affinites(conn)
        journaliser(conn, "reseau",
                    f"{nb_affinites} affinités source↔nœud enregistrées")

        decision = evaluer_recevabilite(conn, args.plaidoyer)
        journaliser(
            conn, "recevabilite",
            f"plaidoyer={args.plaidoyer} -> {decision.conclusion} "
            f"(règle {decision.regle_code}, "
            f"{len(decision.chemin)} nœuds activés)",
        )

        blocs: list[tuple[str, str]] = []
        if args.extrait.exists():
            texte_extrait = args.extrait.read_text(encoding="utf-8")
            ecart = equilibre_accolades(texte_extrait)
            if ecart:
                journaliser(conn, "extrait",
                            f"accolades déséquilibrées dans l'extrait "
                            f"({ecart:+d})")
            blocs = lire_extrait(args.extrait)
            journaliser(conn, "extrait",
                        f"{len(blocs)} bloc(s) lu(s) dans {args.extrait.name}")
        else:
            journaliser(conn, "extrait",
                        f"extrait introuvable : {args.extrait}")

        ctx = Contexte(
            dossier=args.dossier,
            accuse=args.accuse,
            couronne=args.couronne,
            avocat=args.avocat,
            juridiction=args.juridiction,
            district=args.district,
            palais=args.palais,
            salle=args.salle,
            date_audience=args.date_audience,
            heure_audience=args.heure_audience,
            infraction=args.infraction,
            plaidoyer=args.plaidoyer,
        )

        tex = generer_tex(conn, ctx, decision, blocs, args.out)
        validation = valider_tex(tex, ctx, decision)
        journaliser(
            conn, "validation",
            f"{tex.name} : {'OK' if validation['ok'] else 'ERREURS'} "
            f"({len(validation['erreurs'])} erreur(s), "
            f"{len(validation['avertissements'])} avertissement(s))",
        )

        compilation = ({"statut": "ignore"}
                       if args.no_compile else compiler_pdf(tex))
        journaliser(conn, "pdf", str(compilation.get("statut")))

        rapport = {
            "genere_le": utcnow(),
            "plaidoyer": args.plaidoyer,
            "conclusion": decision.conclusion,
            "regle": decision.regle_code,
            "titre_document": decision.titre_document,
            "recu": decision.recu,
            "chemin": decision.chemin,
            "blocs_extrait": [titre for titre, _ in blocs],
            "base": str(args.db),
            "extrait": str(args.extrait),
            "tex": str(tex),
            "validation": validation,
            "compilation": compilation,
        }
        chemin_rapport = args.report or args.out.with_suffix(".report.json")
        chemin_rapport.parent.mkdir(parents=True, exist_ok=True)
        chemin_rapport.write_text(
            json.dumps(rapport, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        journaliser(conn, "rapport", f"rapport JSON : {chemin_rapport}")

        print()
        print("Conclusion :", decision.titre_document)
        print("Document .tex :", tex)
        if validation["erreurs"]:
            for err in validation["erreurs"]:
                print("ERREUR :", err, file=sys.stderr)
        return 0 if validation["ok"] else 2
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())













