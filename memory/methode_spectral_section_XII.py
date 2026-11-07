"""Section XII - Construction generalisee des suites pour rapport 1/k_i.

Ce module integre les regles de la Section XII de methode_spectral.thy
dans le Dictionnaire Spectral RAG de Gabriel, sous forme d'entrees
ontologiques injectables dans les prompts LLM.

Difference avec Section XI : Section XII PARAMETRISE le rapport 1/k_i
pour tout k entier >= 2 (cas valides confirmes : k=2, k=3, k=4), couvre
les suites de 1 a 7 termes ET >= 8 termes, positives ET negatives, avec
24 lemmes numeriques certifies et 1 theoreme central.

Source     : methode_spectral.thy (Section XII, lignes ~2200-2511).
Auteur     : Philippe Thomas Savard.
Validation : 11/11 OK Suite A (n=1..11), 3/3 OK Suite B (n=8..10).
"""
from __future__ import annotations
from fractions import Fraction
from typing import Any


SECTION_XII_TITLE = "XII. Construction generalisee pour rapport spectral 1/k_i"


# Constantes Savard parametriques (extraites du fichier HOL)
CONSTANTES_SAVARD: dict[int, dict[str, Fraction]] = {
    2: {
        "alpha_A": Fraction(13, 4),       # 3.25 = 13/4
        "alpha_B": Fraction(13, 2),       # 6.5 = 13/2
        "offset_A": Fraction(2),
        "offset_B": Fraction(66),
    },
    3: {
        "alpha_A": Fraction(73, 9),
        "alpha_B": Fraction(219, 9),
        "offset_A": Fraction(3, 2),
        "offset_B": Fraction(487) * Fraction(3, 2),
    },
    4: {
        "alpha_A": Fraction(241, 16),
        "alpha_B": Fraction(964, 16),
        "offset_A": Fraction(4, 3),
        "offset_B": Fraction(3073) * Fraction(4, 3),
    },
}


SECTION_XII_REGLES: list[dict[str, Any]] = [
    {
        "code": "XII.1",
        "nom": "constantes_savard_parametriques",
        "regle": (
            "Pour tout k in {2,3,4,...} : 4 constantes alpha_A(k), alpha_B(k), "
            "offset_A(k), offset_B(k). k=2 -> (13/4, 13/2, 2, 66). "
            "k=3 -> (73/9, 219/9, 1.5, 487*1.5). k=4 -> (241/16, 964/16, 4/3, 3073*4/3)."
        ),
        "domaine_validite": "k entier >= 2",
    },
    {
        "code": "XII.2",
        "nom": "somme_A_positive_parametrique",
        "regle": "Somme(A_pos, k, n) = (alpha_A(k) / 2) * k^n - offset_A(k).",
        "domaine_validite": "k >= 2, n >= 1",
    },
    {
        "code": "XII.3",
        "nom": "somme_B_positive_parametrique",
        "regle": "Somme(B_pos, k, n) = (alpha_B(k) / 2) * k^n - offset_B(k).",
        "domaine_validite": "k >= 2, n >= 1",
    },
    {
        "code": "XII.4",
        "nom": "somme_A_negative_parametrique",
        "regle": "Somme(A_neg, k, n) = alpha_A(k) / k^n - offset_A(k). Tend vers -offset_A quand n->inf.",
        "domaine_validite": "k >= 2, n >= 1 (n = nombre de termes du cote negatif)",
    },
    {
        "code": "XII.5",
        "nom": "somme_B_negative_parametrique",
        "regle": "Somme(B_neg, k, n) = alpha_B(k) / k^n - offset_B(k).",
        "domaine_validite": "k >= 2, n >= 1",
    },
    {
        "code": "XII.6",
        "nom": "construction_suite_A_1_a_7_termes",
        "regle": (
            "Pour n in {1..7} avec a_1=2, r=k=2 : "
            "n=1->[2], n=2->[2,3], n=3->[2,3,6], n=4->[2,4,6,12], "
            "n=5->[2,4,8,12,24], n=6->[2,4,8,16,24,48], n=7->[2,4,8,16,32,48,96]. "
            "Regle : i=1 -> a_1 ; n=2,i=2 -> a_1*(r-1/r) ; "
            "n>=3, i<=n-2 -> a_1*r^(i-1) (progression simple) ; "
            "i=n-1 -> a_1*r^(n-3)*(r-1/r) (avant-dernier) ; "
            "i=n -> avant_dernier * r (dernier)."
        ),
        "domaine_validite": "1 <= n <= 7, suite A positive",
    },
    {
        "code": "XII.7",
        "nom": "construction_suite_A_8_termes_et_plus",
        "regle": (
            "Pour n >= 8 : meme regle que XII.6. "
            "Exemples k=2 : n=8->[2,4,8,16,32,64,96,192], "
            "n=10->[2,4,8,16,32,64,128,256,384,768], "
            "n=11->[2,4,8,16,32,64,128,256,512,768,1536]."
        ),
        "domaine_validite": "n >= 8, suite A positive",
    },
    {
        "code": "XII.8",
        "nom": "substitution_position_6_suite_B",
        "regle": (
            "Pour suite B avec n >= 8 UNIQUEMENT : "
            "position 6 -> a_1 * r^6 (substituee, decalee d'un cran). "
            "Positions 7 a n-2 -> a_1 * r^i (decalees). "
            "Avant-dernier et dernier utilisent r^(n-2) au lieu de r^(n-3). "
            "Exemples k=2 : n=8->[2,4,8,16,32,128,192,384], "
            "n=10->[2,4,8,16,32,128,256,512,768,1536]. "
            "Pour n < 8, suite B = suite A."
        ),
        "domaine_validite": "suite B, n >= 8",
    },
    {
        "code": "XII.9",
        "nom": "theoreme_rapport_spectral_universel",
        "regle": (
            "RsP_k(k, n1, n2) = (Somme_A(n1) - Somme_A(n2)) / (Somme_B(n1) - Somme_B(n2)) = 1/k "
            "pour tout k in {2,3,4}, n1, n2 > 0, n1 != n2. "
            "Theoreme certifie : RsP_k_egale_un_sur_k_pos."
        ),
        "domaine_validite": "k in {2,3,4}, regime positif",
    },
    {
        "code": "XII.10",
        "nom": "validation_numerique_negative_savard",
        "regle": (
            "Exemples confirmes par Philippe Savard 2026-02-17 (k=2) : "
            "premier -2 (1 terme) = 3.25/2^1 - 2 = -3/8. "
            "premier -5 (3 termes) = 3.25/2^3 - 2 = -51/32 = -1.59375. "
            "premier -47 (15 termes) = 3.25/2^15 - 2 = -262131/131072 ~ -1.9999. "
            "Note historique : la suite negative converge vers -offset_A = -2 (jamais atteint)."
        ),
        "domaine_validite": "k=2, regime negatif, n = numero d'ordre du premier negatif",
    },
]


def get_section_XII_entries() -> list[dict[str, Any]]:
    """Retourne les regles de la Section XII sous forme d'entrees RAG
    consommables par adaptateur_cognitif_rag.py."""
    return [
        {
            "id": f"section_XII_{r['code']}",
            "titre": f"Section XII / {r['code']} - {r['nom']}",
            "contenu": r["regle"],
            "metadata": {
                "section": "XII",
                "code": r["code"],
                "domaine_validite": r["domaine_validite"],
                "source_thy": "methode_spectral.thy (Section XII)",
            },
        }
        for r in SECTION_XII_REGLES
    ]


def render_section_XII_summary() -> str:
    """Resume textuel pour injection dans un prompt LLM."""
    lines = [f"=== {SECTION_XII_TITLE} ==="]
    for r in SECTION_XII_REGLES:
        lines.append(f"\n[{r['code']}] {r['nom']} ({r['domaine_validite']}):")
        lines.append(f"  {r['regle']}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Helpers de calcul (utilisables par le pipeline cognitif)
# --------------------------------------------------------------------------
def somme_A_pos(k: int, n: int) -> Fraction:
    """Somme fermee de la suite A positive pour rapport 1/k a n termes."""
    c = CONSTANTES_SAVARD[k]
    return c["alpha_A"] / 2 * Fraction(k) ** n - c["offset_A"]


def somme_B_pos(k: int, n: int) -> Fraction:
    """Somme fermee de la suite B positive pour rapport 1/k a n termes."""
    c = CONSTANTES_SAVARD[k]
    return c["alpha_B"] / 2 * Fraction(k) ** n - c["offset_B"]


def somme_A_neg(k: int, n: int) -> Fraction:
    """Somme fermee de la suite A negative pour rapport 1/k a n termes."""
    c = CONSTANTES_SAVARD[k]
    return c["alpha_A"] / Fraction(k) ** n - c["offset_A"]


def somme_B_neg(k: int, n: int) -> Fraction:
    """Somme fermee de la suite B negative pour rapport 1/k a n termes."""
    c = CONSTANTES_SAVARD[k]
    return c["alpha_B"] / Fraction(k) ** n - c["offset_B"]


def terme_A_pos(a1: Fraction, r: Fraction, n: int, i: int) -> Fraction:
    """i-eme terme de la suite A positive (construction Savard, n >= 1)."""
    a1 = Fraction(a1)
    r = Fraction(r)
    if i == 1:
        return a1
    if n == 2 and i == 2:
        return a1 * (r - Fraction(1) / r)
    if n >= 3 and i <= n - 2:
        return a1 * r ** (i - 1)
    if n >= 3 and i == n - 1:
        return a1 * r ** (n - 3) * (r - Fraction(1) / r)
    if n >= 3 and i == n:
        return a1 * r ** (n - 3) * (r - Fraction(1) / r) * r
    return Fraction(0)


def terme_B_pos(a1: Fraction, r: Fraction, n: int, i: int) -> Fraction:
    """i-eme terme de la suite B positive (substitution position 6 si n >= 8)."""
    a1 = Fraction(a1)
    r = Fraction(r)
    if n < 8:
        return terme_A_pos(a1, r, n, i)
    if i == 1:
        return a1
    if i <= 5:
        return a1 * r ** (i - 1)
    if i == 6:
        return a1 * r ** 6
    if i <= n - 2:
        return a1 * r ** i
    if i == n - 1:
        return a1 * r ** (n - 2) * (r - Fraction(1) / r)
    if i == n:
        return a1 * r ** (n - 2) * (r - Fraction(1) / r) * r
    return Fraction(0)


def construire_suite_A(k: int, n: int, a1: int = 2) -> list[Fraction]:
    """Construit la suite A complete pour 1 a n termes, k >= 2, a1 par defaut 2."""
    return [terme_A_pos(Fraction(a1), Fraction(k), n, i) for i in range(1, n + 1)]


def construire_suite_B(k: int, n: int, a1: int = 2) -> list[Fraction]:
    """Construit la suite B complete pour 1 a n termes, avec substitution si n >= 8."""
    return [terme_B_pos(Fraction(a1), Fraction(k), n, i) for i in range(1, n + 1)]


if __name__ == "__main__":
    # Apercu rapide
    print(render_section_XII_summary())
    print(f"\n{len(get_section_XII_entries())} entrees RAG generees.")
    print("\n--- Verification numerique k=2 ---")
    for n in range(1, 11):
        suite_a = construire_suite_A(2, n)
        suite_b = construire_suite_B(2, n)
        print(f"  n={n:2d} : A={[str(x) for x in suite_a]}")
        if n >= 8:
            print(f"        B={[str(x) for x in suite_b]} (avec subst. pos 6)")
