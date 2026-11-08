"""Exact n=10 Digamma_Savard/Cline rule from the author's 2026 document."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from fractions import Fraction


SIEVE_PRIMES = (3, 5, 7, 11, 13, 17, 19, 23)

_BRANCHES = (
    ("A(8)-", -1, 8, 1),
    ("A(8)+", 1, 8, -1),
    ("A(7)+", 1, 7, -1),
    ("A(7)-", -1, 7, 1),
)

DIGAMMA_SAVARD_COGNITIVE_CONTEXT = """\
RÉFÉRENCE DU CORPUS — Digamma_Savard/Cline, document de Philippe Thomas Savard,
section « Fonction Digamma_Savard/Cline » (2026), niveaux d'ancrage n=10.
Formules fermées :
  alpha_A(k)=2(k^4-k^2+1)/((k-1)k^3), alpha_B(k)=k alpha_A(k)
  delta_A(k)=k/(k-1), delta_B(k)=(k^7-k^6+k)/(k-1)
  SA(k,n)=alpha_A(k)k^n/2-delta_A(k)
  SB(k,n)=alpha_B(k)k^n/2-delta_B(k)
Pour n=10, B0(k)=(SB-SA)/k^6=k^5-k^3+k-1. Les quatre candidats
P et corrections correspondantes sont :
  A(8)- : P=B0+k^2 ; Digamma=SA-k^8
  A(8)+ : P=B0-k^2 ; Digamma=SA+k^8
  A(7)+ : P=B0-k   ; Digamma=SA+k^7
  A(7)- : P=B0+k   ; Digamma=SA-k^7
Éliminer un candidat s'il est divisible par l'un de {3,5,7,11,13,17,19,23}.
Si un seul candidat survit, sa branche détermine Digamma et P=(SB-Digamma)/k^6.
Avec plusieurs survivants, le résultat est indéterminé : ne pas choisir au hasard.
Le criblage ne prouve pas que le candidat survivant est premier.
La correspondance branche/polarité est expérimentale selon le document, non une
preuve formelle. Les polynômes de sélection sont dérivés à n=10; pour n différent
de 10, le document prévoit séparément un décalage de rang, pas ce criblage.
"""

_DIGAMMA_QUERY = re.compile(
    r"\bdigamma\b|\bb_?0\b|\bcriblage\b|\bquatre\s+branches\b"
    r"|\bfonction\s+calculable\b",
    re.IGNORECASE,
)
_DIGAMMA_CALCULATION_QUERY = re.compile(
    r"\bdigamma\b|\bb_?0\b|\bcriblage\b|\bquatre\s+branches\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class DigammaSavardResult:
    k: int
    n: int
    sum_a: int
    sum_b: int
    b0: int
    candidates: tuple[tuple[str, int], ...]
    survivors: tuple[tuple[str, int], ...]
    status: str
    digamma: int | None = None
    candidate_p: int | None = None
    primality_proven: bool = False


def spectral_sums(k: int, n: int) -> tuple[Fraction, Fraction]:
    """Return the document's exact closed-form sums using rational arithmetic."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k doit être un entier >= 2.")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n doit être un entier >= 1.")

    alpha_a = Fraction(2 * (k**4 - k**2 + 1), (k - 1) * k**3)
    alpha_b = k * alpha_a
    delta_a = Fraction(k, k - 1)
    delta_b = Fraction(k**7 - k**6 + k, k - 1)
    sum_a = alpha_a * Fraction(k**n, 2) - delta_a
    sum_b = alpha_b * Fraction(k**n, 2) - delta_b
    return sum_a, sum_b


def digamma_savard_n10(k: int) -> DigammaSavardResult:
    """Apply the document's modular branch selection at its n=10 anchor only.

    A unique surviving branch yields a Digamma value and reconstructed
    candidate. Survivorship is not a primality proof; ambiguity stays explicit.
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 2:
        raise ValueError("k doit être un entier >= 2.")

    sum_a_fraction, sum_b_fraction = spectral_sums(k, 10)
    if sum_a_fraction.denominator != 1 or sum_b_fraction.denominator != 1:
        raise ArithmeticError("Les sommes spectrales à n=10 ne sont pas entières.")
    sum_a = sum_a_fraction.numerator
    sum_b = sum_b_fraction.numerator
    b0 = k**5 - k**3 + k - 1
    candidates = (
        ("A(8)-", b0 + k**2),
        ("A(8)+", b0 - k**2),
        ("A(7)+", b0 - k),
        ("A(7)-", b0 + k),
    )
    survivors = tuple(
        (branch, candidate)
        for branch, candidate in candidates
        if all(candidate % prime for prime in SIEVE_PRIMES)
    )

    if len(survivors) != 1:
        return DigammaSavardResult(
            k=k,
            n=10,
            sum_a=sum_a,
            sum_b=sum_b,
            b0=b0,
            candidates=candidates,
            survivors=survivors,
            status="indetermine",
        )

    branch = survivors[0][0]
    _, correction_sign, exponent, _ = next(
        item for item in _BRANCHES if item[0] == branch
    )
    digamma = sum_a + correction_sign * k**exponent
    reconstructed_p = Fraction(sum_b - digamma, k**6)
    if reconstructed_p.denominator != 1 or reconstructed_p.numerator != survivors[0][1]:
        return DigammaSavardResult(
            k=k,
            n=10,
            sum_a=sum_a,
            sum_b=sum_b,
            b0=b0,
            candidates=candidates,
            survivors=survivors,
            status="incoherent",
            digamma=digamma,
        )

    return DigammaSavardResult(
        k=k,
        n=10,
        sum_a=sum_a,
        sum_b=sum_b,
        b0=b0,
        candidates=candidates,
        survivors=survivors,
        status="branche_unique",
        digamma=digamma,
        candidate_p=reconstructed_p.numerator,
    )


def digamma_savard_context_for_query(query: str) -> str:
    """Return the bounded cognitive reference only for relevant questions."""
    normalized = unicodedata.normalize("NFKD", query).encode("ascii", "ignore").decode("ascii")
    if _DIGAMMA_QUERY.search(normalized):
        return DIGAMMA_SAVARD_COGNITIVE_CONTEXT
    return ""


def digamma_savard_facts_for_query(query: str) -> dict[str, object] | None:
    """Compute explicit n=10 anchor facts when a related query supplies k."""
    if not digamma_savard_context_for_query(query):
        return None

    normalized = unicodedata.normalize("NFKD", query).encode("ascii", "ignore").decode("ascii")
    match = re.search(r"\bk\s*=\s*(\d+)\b", normalized, re.IGNORECASE)
    if match is None:
        match = re.search(r"\b1\s*/\s*(\d+)\b", normalized)
    if match is None:
        return None

    k = int(match.group(1))
    if k < 2:
        return {
            "source": "Document-pdf-tex, section Fonction Digamma_Savard/Cline",
            "status": "k_invalide",
            "k": k,
            "message": "Le domaine documenté est k >= 2.",
        }

    result = digamma_savard_n10(k)
    facts: dict[str, object] = {
        "source": "Document-pdf-tex, section Fonction Digamma_Savard/Cline, ancrage n=10",
        "status": result.status,
        "k": result.k,
        "n": result.n,
        "somme_suite_A": result.sum_a,
        "somme_suite_B": result.sum_b,
        "B0": result.b0,
        "candidats_P": dict(result.candidates),
        "branches_survivantes": dict(result.survivors),
        "Digamma_calcule": result.digamma,
        "candidat_P": result.candidate_p,
        "preuve_de_primalite": result.primality_proven,
        "consigne": (
            "Reprendre ces valeurs exactement. Si le statut est indetermine, "
            "ne choisir aucune branche. Le criblage n'est pas une preuve de primalite."
        ),
    }
    if _DIGAMMA_CALCULATION_QUERY.search(normalized):
        facts["réponse_déterministe"] = format_digamma_savard_report(result)
    return facts


def format_digamma_savard_report(result: DigammaSavardResult) -> str:
    """Render a detailed deterministic report without LLM inference."""
    lines = [
        "## Fonction Digamma_Savard/Cline — ancrage n=10",
        "",
        "Portée : les quatre polynômes de sélection sont dérivés pour n=10.",
        "Le document traite n≠10 séparément par décalage de rang; ce criblage",
        "ne doit pas être extrapolé à ces autres valeurs.",
        "",
        "### Équations utilisées",
        f"- SA(k,10) = {result.sum_a}",
        f"- SB(k,10) = {result.sum_b}",
        f"- B0(k) = k^5 − k^3 + k − 1 = {result.b0}",
        "- P candidates : A(8)- = B0+k²; A(8)+ = B0−k²; "
        "A(7)+ = B0−k; A(7)- = B0+k.",
        "- Crible : éliminer un candidat divisible par 3, 5, 7, 11, 13, 17, 19 ou 23.",
        "",
        "### Évaluation des quatre branches",
    ]
    for branch, candidate in result.candidates:
        _, sign, exponent, _ = next(item for item in _BRANCHES if item[0] == branch)
        digamma = result.sum_a + sign * result.k**exponent
        divisors = [prime for prime in SIEVE_PRIMES if candidate % prime == 0]
        sieve_result = (
            "survit au crible"
            if not divisors
            else "éliminée (divisible par " + ", ".join(map(str, divisors)) + ")"
        )
        lines.append(
            f"- {branch} : P candidat={candidate}; Digamma candidat={digamma}; {sieve_result}."
        )

    lines.extend(["", "### Résultat"])
    if result.status == "branche_unique":
        lines.extend(
            [
                f"Branche unique survivante : {result.survivors[0][0]}.",
                f"Digamma calculé = {result.digamma}.",
                f"(SB − Digamma)/k^6 = ({result.sum_b} − {result.digamma})/"
                f"{result.k**6} = {result.candidate_p}.",
                f"{result.candidate_p} est le candidat P reconstruit; le criblage "
                "seul n'en prouve pas la primalité.",
            ]
        )
    else:
        survivors = ", ".join(
            f"{branch} (P={candidate})" for branch, candidate in result.survivors
        ) or "aucune branche"
        lines.extend(
            [
                f"Statut : indéterminé ({len(result.survivors)} branche(s) survivante(s)).",
                f"Survivants : {survivors}.",
                "Aucun Digamma ni candidat P n'est sélectionné.",
            ]
        )

    lines.extend(
        [
            "",
            "### Limites et provenance",
            "- Le criblage écarte des branches; il ne constitue pas un test complet de primalité.",
            "- Le document décrit la correspondance branche/polarité comme empiriquement "
            "validée, non comme formellement démontrée.",
            "- Source : document de Philippe Thomas Savard (2026), section "
            "« Fonction Digamma_Savard/Cline ».",
        ]
    )
    return "\n".join(lines)
