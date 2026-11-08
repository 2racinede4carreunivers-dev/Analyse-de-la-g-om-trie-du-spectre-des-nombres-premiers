# -*- coding: utf-8 -*-
"""
corpus/extraire_mathlib.py — extraction deterministe de notions depuis Mathlib.

Lit le depot Mathlib local (Lean 4, licence Apache 2.0) et en extrait des
notions de reconnaissance avec leur provenance exacte (fichier:ligne).

Regles computationnalistes (aucune invention) :
- seul le paquet ``Mathlib/`` est lu (coeur de la bibliotheque ; dossiers
  annexes Archive/, MathlibTest/, etc. exclus) ;
- seuls les identifiants REELLEMENT presents dans les .lean sont extraits ;
- l'identifiant est decompose en sous-mots reels (separateur ``_``) : chaque
  sous-mot garde sa provenance ``fichier:ligne (identifiant complet)`` ;
- les mots fonctionnels francais (mots vides) sont rejetes par un ensemble
  ferme ``MOTS_VIDES_FR`` (anti-collision : « est », « que », « sur »...) ;
- le champ est deduit du dossier thematique de premier niveau (table fermee) ;
- sortie triee (ordre total), doublons elimines (premiere occurrence gardee).

Usage :
    python -m pythonLLM.corpus.extraire_mathlib [racine_mathlib] [limite]
"""
from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

# Motif de declaration Lean 4 en debut de ligne (apres espaces).
_DECL_RE = re.compile(
    r"^\s*(?:private\s+|protected\s+)?"
    r"(def|theorem|lemma|example|class|structure|inductive|abbrev)\s+"
    r"([A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*)"
)

# Ensemble ferme : mots fonctionnels francais (>= 3 lettres) rejetes de
# l'enrichissement pour ne jamais faire passer une question hors corpus
# pour une reconnaissance (garantie INV-NO-INVENTION).
MOTS_VIDES_FR = frozenset({
    "les", "des", "une", "dans", "pour", "sur", "que", "qui", "est", "sont",
    "etre", "avec", "comme", "donc", "mais", "cela", "cette", "entre",
    "leur", "leurs", "plus", "moins", "sans", "tout", "tous", "toute",
    "toutes", "meme", "aussi", "depuis", "jusqu", "chez", "selon", "lors",
    "encore", "deja", "ces", "ses", "nos", "vos", "ils", "elles", "nous",
    "vous", "tres", "peut", "doit", "sera", "seront", "etaient", "etait",
    "avait", "avoir", "deux", "trois", "ainsi", "autre", "autres", "chaque",
    "plusieurs", "vers", "apres", "avant", "sous", "parmi", "fait", "faire",
    "par", "son",
})

# Dossier thematique Mathlib de premier niveau -> champ (table fermee).
# Tout dossier non liste est rattache a COMPILATION (analyse formelle).
DOSSIER_VERS_CHAMP = {
    "Logic": "LOGIQUE",
    "Computability": "LOGIQUE",
    "ModelTheory": "LOGIQUE",
    "SetTheory": "LOGIQUE",
    "Algebra": "ALGEBRE",
    "CategoryTheory": "ALGEBRE",
    "LinearAlgebra": "ALGEBRE",
    "RingTheory": "ALGEBRE",
    "GroupTheory": "ALGEBRE",
    "FieldTheory": "ALGEBRE",
    "Order": "ALGEBRE",
    "NumberTheory": "ARITHMETIQUE",
    "Data": "ARITHMETIQUE",
    "Geometry": "GEOMETRIE",
    "Topology": "GEOMETRIE",
    "AlgebraicTopology": "GEOMETRIE",
    "AlgebraicGeometry": "GEOMETRIE",
    "Combinatorics": "GEOMETRIE",
    "MeasureTheory": "STATISTIQUES",
    "Probability": "STATISTIQUES",
    "InformationTheory": "STATISTIQUES",
    "Analysis": "STATISTIQUES",
    "Dynamics": "STATISTIQUES",
    "Tactic": "COMPILATION",
    "Lean": "COMPILATION",
    "Util": "COMPILATION",
    "Testing": "COMPILATION",
}


def _nettoyer(mot: str) -> str:
    """Minuscules, sans accents, caracteres alphanumeriques seulement."""
    decompose = unicodedata.normalize("NFD", mot)
    sans = "".join(c for c in decompose if not unicodedata.combining(c))
    return re.sub(r"[^0-9a-z]", "", sans.lower())


def lemmatiser_multi(nom: str) -> tuple[str, ...]:
    """Decompose un identifiant Lean en sous-mots de reconnaissance.

    - partie apres le dernier point (nom court) ;
    - decoupage sur ``_`` (sous-mots reels, jamais la concatenation) ;
    - minuscules, sans accents ; rejet si < 3 caracteres ou mot vide FR.
    """
    court = nom.rsplit(".", 1)[-1]
    resultats: list[str] = []
    for partie in court.split("_"):
        mot = _nettoyer(partie)
        if len(mot) >= 3 and mot not in MOTS_VIDES_FR and mot not in resultats:
            resultats.append(mot)
    return tuple(resultats)


def lemmatiser(nom: str) -> str:
    """Premier sous-mot valide de l'identifiant (compatibilite API)."""
    sous = lemmatiser_multi(nom)
    return sous[0] if sous else ""


def extraire(racine: Path, limite: int = 0):
    """Extrait (lemme, champ, provenance). Tri deterministe, dedup exact.

    La provenance conserve l'identifiant complet d'origine : chaque notion
    reste exactement verifiable dans le fichier source.
    """
    paquet = racine / "Mathlib"
    base = paquet if paquet.is_dir() else racine
    vus: dict[str, tuple[str, str, str]] = {}
    fichiers = sorted(base.rglob("*.lean"))
    for chemin in fichiers:
        try:
            texte = chemin.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError):
            continue
        relatif = chemin.relative_to(base).as_posix()
        dossier = relatif.split("/", 1)[0] if "/" in relatif else ""
        champ = DOSSIER_VERS_CHAMP.get(dossier, "COMPILATION")
        for num, ligne in enumerate(texte.splitlines(), start=1):
            m = _DECL_RE.match(ligne)
            if not m:
                continue
            identifiant = m.group(2)
            sous_mots = lemmatiser_multi(identifiant)
            if not sous_mots:
                continue
            provenance = f"{relatif}:{num} ({identifiant})"
            for lemme in sous_mots:
                if lemme in vus:
                    continue
                vus[lemme] = (lemme, champ, provenance)
                if limite and len(vus) >= limite:
                    return sorted(vus.values())
    return sorted(vus.values())


def _principal() -> int:
    racine = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if racine is None:
        home = Path.home()
        for cand in (home / "OneDrive" / "Mathlib", home / "mathlib4", Path("C:/mathlib4")):
            if (cand / "Mathlib.lean").exists():
                racine = cand
                break
    if racine is None or not (racine / "Mathlib.lean").exists():
        print("Depot Mathlib introuvable. Passez la racine en argument.")
        return 1
    limite = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 0
    lignes = extraire(racine, limite)
    print(f"Racine : {racine}")
    print(f"Notions extraites : {len(lignes)}")
    for lemme, champ, prov in lignes[:15]:
        print(f"  {lemme} [{champ}] <- {prov}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_principal())
