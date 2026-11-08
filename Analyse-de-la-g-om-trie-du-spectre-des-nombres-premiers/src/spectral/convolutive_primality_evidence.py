"""Cognitive reference for the reported convolutive-anchor primality run."""
from __future__ import annotations

import re
import unicodedata


CONVOLUTIVE_PRIMALITY_EVIDENCE_CONTEXT = """\
RÉSULTAT RAPPORTÉ — validation de primalité d'ancrages du système convolutif.
Source : Document-pdf-tex/Certification_primalité/parts/
reconstruction_k28M_84M_detail_primalite.txt.part-00011, bilan final daté du
2026-11-01 (lignes 395495-395508).
Le bilan déclare que PARI/GP isprime a vérifié 6 849 579 ancrages candidats :
6 849 579 premiers démontrés, 0 composé/fausse ancre, score rapporté 100.000000 %.
Il distingue 6 045 662 rapports UNIQUE et 396 132 rapports AMBIGU.
Réserve impérative : le même bilan compte une ligne mal formée et inscrit
« Validation intégrale : NON »; la ligne 6 441 797 (1/77 293 103) a un champ de
branches incomplet malgré le statut UNIQUE. Présenter ces chiffres comme le
résultat déclaré du rapport, pas comme une validation intégrale indépendante.
Le criblage convolutif qui produit/reconstruit les candidats n'est pas à lui seul
une preuve de primalité; le rapport attribue la vérification à PARI/GP isprime.
Ne pas extrapoler cette série testée à tous les ancrages possibles.
"""

_CONVOLUTIVE_PRIMALITY_QUERY = re.compile(
    r"\bconvolut\w*\b"
    r"|\bpari\s*/\s*gp\b"
    r"|\b6[\s,.]?849[\s,.]?579\b"
    r"|(?=.*\bprimalite\b)(?=.*\b(?:rapport|resultat|validation|ancrage|certification|verif)\w*\b)",
    re.IGNORECASE,
)


def convolutive_primality_context_for_query(query: str) -> str:
    """Return the reported validation facts for queries about that experiment."""
    normalized = unicodedata.normalize("NFKD", query).encode("ascii", "ignore").decode("ascii")
    if _CONVOLUTIVE_PRIMALITY_QUERY.search(normalized):
        return CONVOLUTIVE_PRIMALITY_EVIDENCE_CONTEXT
    return ""
