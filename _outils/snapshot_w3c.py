# -*- coding: utf-8 -*-
"""
_outils/snapshot_w3c.py — telecharge et verifie les sources ouvertes W3C.

Telecharge le document SKOS Reference (W3C Recommendation, licence W3C
Document License), en calcule le SHA-256, verifie la presence attendue des
termes du vocabulaire dans le texte, puis ecrit le snapshot + une fiche de
provenance (pythonLLM/corpus/snapshots/w3c_skos.sha256).

Determinisme et non-invention : rien n'est encode sans telechargement reussi ;
si le reseau echoue, le script echoue aussi (aucune donnee fabriquee).

Usage :
    python _outils/snapshot_w3c.py
"""
from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

URL = "https://www.w3.org/TR/skos-reference/"
RACINE = Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "pythonLLM" / "corpus" / "snapshots"

# Termes du vocabulaire SKOS attendus dans le document (ensemble ferme).
# Le script VERIFIE leur presence dans le texte telecharge avant d'ecrire.
TERMES_ATTENDUS = (
    "skos:Concept", "skos:ConceptScheme", "skos:inScheme",
    "skos:hasTopConcept", "skos:topConceptOf", "skos:broader",
    "skos:narrower", "skos:related", "skos:semanticRelation",
    "skos:prefLabel", "skos:altLabel", "skos:hiddenLabel",
    "skos:notation", "skos:note", "skos:scopeNote", "skos:definition",
    "skos:example", "skos:historyNote", "skos:editorialNote",
    "skos:changeNote", "skos:member", "skos:memberList",
    "skos:Collection", "skos:OrderedCollection",
    "skos:mappingRelation", "skos:broadMatch", "skos:narrowMatch",
    "skos:relatedMatch", "skos:exactMatch", "skos:closeMatch",
)


def telecharger(url: str, timeout: int = 60) -> bytes:
    requete = urllib.request.Request(
        url, headers={"User-Agent": "pythonLLM-corpus/1.1 (+traçabilité)"}
    )
    with urllib.request.urlopen(requete, timeout=timeout) as r:
        return r.read()


def main() -> int:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    corps = telecharger(URL)
    empreinte = hashlib.sha256(corpus := corps).hexdigest()
    texte = corps.decode("utf-8", errors="replace")
    manquants = [t for t in TERMES_ATTENDUS if t not in texte]
    if manquants:
        print("ERREUR : termes SKOS absents du document :", manquants)
        return 1
    snapshot = DOSSIER / "w3c_skos_reference.html"
    snapshot.write_bytes(corps)
    fiche = DOSSIER / "w3c_skos.sha256"
    fiche.write_text(
        f"url: {URL}\n"
        f"licence: W3C Document License (Copyright W3C, MIT/ERCIM/Keio)\n"
        f"statut: W3C Recommendation 18 August 2009\n"
        f"taille: {len(corps)}\n"
        f"sha256: {empreinte}\n"
        f"termes_verifies: {len(TERMES_ATTENDUS)}\n",
        encoding="utf-8",
    )
    print(f"OK {URL}")
    print(f"  taille   : {len(corps)} o")
    print(f"  sha256   : {empreinte}")
    print(f"  termes   : {len(TERMES_ATTENDUS)} verifies dans le texte")
    print(f"  snapshot : {snapshot}")
    return 0


if __name__ == "__main__":
    sys.exit(main())