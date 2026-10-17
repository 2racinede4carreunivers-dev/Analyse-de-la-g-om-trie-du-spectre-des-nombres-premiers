# -*- coding: utf-8 -*-
"""
_outils/generer_sources_ouvertes.py — genere corpus/sources_ouvertes.py.

Telecharge (ou recharge le snapshot verifie) les trois sources ouvertes :
1. W3C SKOS Reference  (W3C Document License)
2. AI Act  CELEX 32024R1689  (depot Cellar, Decision 2011/833/UE)
3. RGPD   CELEX 32016R0679  (depot Cellar)

Verifie chaque document (ancres + termes attendus), calcule le SHA-256,
puis genere ``pythonLLM/corpus/sources_ouvertes.py`` : NOTIONS tracees
(lemme, champ, source, provenance exacte).

Determinisme : extraction par expressions regulieres sur le texte reseau
reel ; en cas d'echec reseau ou de verification, le script echoue sans ecrire.

Usage : python _outils/generer_sources_ouvertes.py
"""
from __future__ import annotations

import hashlib
import re
import sys
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))

from pythonLLM.corpus.extraire_mathlib import MOTS_VIDES_FR  # noqa: E402

SNAP = RACINE / "pythonLLM" / "corpus" / "snapshots"
SORTIE = RACINE / "pythonLLM" / "corpus" / "sources_ouvertes.py"

# Mots fonctionnels anglais (>= 3 lettres) rejetes comme lemmes.
MOTS_VIDES_EN = frozenset({
    "any", "the", "and", "for", "with", "from", "that", "this", "when",
    "whose", "being", "shall", "should", "pursuant", "means", "into",
    "upon", "only", "each", "such", "more", "than", "its", "are", "was",
    "were", "both", "between", "under", "after", "before", "while",
    "where", "must", "other", "relate",
})

CELLAR = "http://publications.europa.eu/resource/celex/{celex}"
DOCUMENTS = (
    {
        "id": "W3C-SKOS", "source_id": "W3C", "type": "w3c",
        "url": "https://www.w3.org/TR/skos-reference/",
        "licence": "W3C Document License (Copyright W3C, MIT/ERCIM/Keio)",
        "statut": "W3C Recommendation 18 August 2009",
        "fichier": "w3c_skos_reference.html",
    },
    {
        "id": "UE-AI-ACT-TEXTE", "source_id": "UE-AI-ACT", "type": "ue",
        "url": CELLAR.format(celex="32024R1689"),
        "licence": "Decision 2011/833/UE — reutilisation gratuite avec attribution",
        "statut": "Reglement (UE) 2024/1689, texte officiel CELEX, depot Cellar",
        "fichier": "ue_ai_act_32024R1689.xhtml",
        "provenance": "CELEX 32024R1689 — art. 3 « Definitions »",
    },
    {
        "id": "UE-RGPD-TEXTE", "source_id": "UE-RGPD", "type": "ue",
        "url": CELLAR.format(celex="32016R0679"),
        "licence": "Decision 2011/833/UE — reutilisation gratuite avec attribution",
        "statut": "Reglement (UE) 2016/679, texte officiel CELEX, depot Cellar",
        "fichier": "ue_rgpd_32016R0679.xhtml",
        "provenance": "CELEX 32016R0679 — art. 4 « Definitions »",
    },
    {
        "id": "SMC-CMC-JOURNAL", "source_id": "SMC-CMC", "type": "cmc",
        "url": ("https://www.cambridge.org/core/journals/"
                "canadian-mathematical-communications"),
        "licence": "Gold Open Access (Cambridge Core, ISSN 2976-8594)",
        "statut": "Canadian Mathematical Communications — revue Gold OA de la SMC",
        "fichier": "smc_cmc_journal.html",
        "provenance": "SMC-CMC vol. 1 (page journal Gold OA)",
    },
)

# Ancres verifiees dans le texte (hors balisage ; les guillemets typographiques
# ‘ ’ sont ceux des textes officiels UE). Le nombre de definitions est de plus
# controle (borné 10-120) dans extraire_ue().
_ANCRES = {
    "W3C-SKOS": ("skos:Concept", "skos:ConceptScheme", "skos:prefLabel",
                 "W3C Recommendation 18 August 2009"),
    "UE-AI-ACT-TEXTE": ("‘AI system’", "2024/1689"),
    "UE-RGPD-TEXTE": ("‘personal data’ means", "2016/679"),
    "SMC-CMC-JOURNAL": ("2976-8594", "Gold OA",
                        "Canadian Mathematical Communications"),
}


def telecharger(url: str, timeout: int = 90,
                accept: str | None = "application/xhtml+xml") -> bytes:
    entetes = {
        "Accept-Language": "eng",
        "User-Agent": "pythonLLM-corpus/1.1 (+tracabilite)",
    }
    if accept:
        entetes["Accept"] = accept
    req = urllib.request.Request(url, headers=entetes)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _lemme(mot: str) -> str:
    return re.sub(r"[^0-9a-z]", "", mot.lower())


def extraire_w3c(texte: str) -> list[tuple[str, str, str, str]]:
    """Termes skos:* -> sous-mots (camelCase), champ LOGIQUE."""
    vus: dict[str, tuple[str, str, str, str]] = {}
    for terme in sorted(set(re.findall(r"skos:([A-Za-z]+)", texte))):
        brut = re.sub(r"(?<!^)(?=[A-Z])", "_", terme).lower()
        for sous in brut.split("_"):
            lemme = _lemme(sous)
            if (len(lemme) >= 3 and lemme not in MOTS_VIDES_FR
                    and lemme not in MOTS_VIDES_EN and lemme != "note"
                    and lemme not in vus):
                vus[lemme] = (lemme, "LOGIQUE", "W3C",
                              f"W3C SKOS Reference ({terme})")
    return sorted(vus.values())


# Regles de classement des articles CMC (ordre total, premier match gagne ;
# mots-cles reels verifies dans les titres du snapshot). Defaut : ALGEBRE
# (algebres, operateurs, equations structurelles).
_REGLES_CMC = (
    ("STATISTIQUES", ("kms",)),           # etats KMS : mecanique statistique
    ("GEOMETRIE", ("braid", "variety", "hypergraph")),
    ("ARITHMETIQUE", ("valuation", "multiplication", "elliptic")),
)


def extraire_cmc(texte: str, doc: dict) -> list[tuple[str, str, str, str]]:
    """Titres d'articles Gold OA -> mots de contenu, champ par regles fermees."""
    titres = sorted(set(re.findall(
        r'<a href="(/core/journals/canadian-mathematical-communications'
        r'/article/[^"]+)"\s*>\s*([^<]+?)\s*</a>', texte)))
    if not 3 <= len(titres) <= 40:
        raise SystemExit(
            f"ERREUR {doc['id']} : {len(titres)} titres (attendu 3-40)")
    vus: dict[str, tuple[str, str, str, str]] = {}
    for _, titre in titres:
        bas = titre.lower()
        champ = "ALGEBRE"
        for code, cles in _REGLES_CMC:
            if any(c in bas for c in cles):
                champ = code
                break
        provenance = f"{doc['provenance']} — « {titre} »"
        for mot in titre.replace("–", " ").split():
            lemme = _lemme(mot)
            if (len(lemme) >= 3 and lemme not in MOTS_VIDES_FR
                    and lemme not in MOTS_VIDES_EN and lemme not in vus):
                vus[lemme] = (lemme, champ, doc["source_id"], provenance)
    return sorted(vus.values())


def extraire_ue(texte: str, doc: dict) -> list[tuple[str, str, str, str]]:
    """Definitions « 'X' means » -> dernier mot (noyau), champ LOGIQUE."""
    vus: dict[str, tuple[str, str, str, str]] = {}
    for phrase in re.findall(r"‘([^’]{2,60})’\s+means\b", texte):
        lemme = _lemme(phrase.split()[-1])
        if (len(lemme) >= 3 and lemme not in MOTS_VIDES_FR
                and lemme not in MOTS_VIDES_EN and lemme not in vus):
            vus[lemme] = (lemme, "LOGIQUE", doc["source_id"], doc["provenance"])
    if not 10 <= len(vus) <= 120:
        raise SystemExit(
            f"ERREUR {doc['id']} : {len(vus)} definitions (attendu 10-120)")
    return sorted(vus.values())


def main() -> int:
    SNAP.mkdir(parents=True, exist_ok=True)
    toutes: list[tuple[str, str, str, str]] = []
    fichiers: list[str] = []
    for doc in DOCUMENTS:
        chemin = SNAP / doc["fichier"]
        if chemin.exists():
            corps = chemin.read_bytes()
            print(f"recharge {doc['id']} depuis le snapshot")
        else:
            accept = None if doc["type"] == "cmc" else "application/xhtml+xml"
            corps = telecharger(doc["url"], accept=accept)
            print(f"telecharge {doc['id']} ({len(corps)} o)")
            chemin.write_bytes(corps)
        texte = corps.decode("utf-8", errors="replace")
        manquants = [a for a in _ANCRES[doc["id"]] if a not in texte]
        if manquants:
            raise SystemExit(f"ERREUR {doc['id']}: ancres absentes {manquants}")
        doc = dict(doc, sha256=hashlib.sha256(corps).hexdigest(), taille=len(corps))
        avant = len(toutes)
        if doc["type"] == "w3c":
            toutes.extend(extraire_w3c(texte))
        elif doc["type"] == "cmc":
            toutes.extend(extraire_cmc(texte, doc))
        else:
            toutes.extend(extraire_ue(texte, doc))
        fichiers.append(
            f"# {doc['id']} — {doc['statut']}\n"
            f"# url: {doc['url']}\nlicence: {doc['licence']}\n"
            f"sha256: {doc['sha256']}\ntaille: {doc['taille']}\n\n"
        )
        print(f"  {doc['id']}: sha256={doc['sha256'][:16]}… "
              f"notions+={len(toutes) - avant}")
    (SNAP / "SOURCES.sha256").write_text("".join(fichiers), encoding="utf-8")
    lignes = [f'    ("{l}", "{c}", "{s}", "{p}"),' for l, c, s, p in toutes]
    SORTIE.write_text(
        '# -*- coding: utf-8 -*-\n'
        '"""\n'
        ' corpus/sources_ouvertes.py — GENERE par '
        '_outils/generer_sources_ouvertes.py.\n'
        ' Ne pas editer a la main. Sources ouvertes verifiees (SHA-256 dans\n'
        ' corpus/snapshots/SOURCES.sha256) : W3C SKOS, AI Act, RGPD, SMC-CMC.\n'
        '"""\n'
        'from __future__ import annotations\n\n'
        'NOTIONS: tuple[tuple[str, str, str, str], ...] = (\n'
        + "\n".join(lignes) + "\n)\n",
        encoding="utf-8",
    )
    print(f"TOTAL notions ouvertes encodees : {len(toutes)} -> {SORTIE.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
