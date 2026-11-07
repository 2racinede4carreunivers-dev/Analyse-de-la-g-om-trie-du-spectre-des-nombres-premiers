"""Section XIII - Le Pont Savard : psi de Tchebychev, zeta et Re(rho) = 1/2.

Ce module assure l'APPRENTISSAGE de la Section XIII de methode_spectral.thy
par Gabriel : les regles du Pont Savard deviennent des entrees ontologiques
injectables dans les prompts LLM via le Dictionnaire Spectral RAG.

Contenu appris (v3.34, vision affirmee de Philippe Savard) :
  - L'equation psi_savard (variante spectrale de Tchebychev, base log10).
  - Les 4 validations numeriques canoniques de Philippe (30, 98, 228, -100).
  - Le Premier Pont (unicite fonctionnelle Tchebychev <-> zeta).
  - Le Deuxieme Pont (exclusivite sur P par l'absurde, 3 piliers).
  - Le Theoreme de l'Ensemble : Ensemble = 1/x + 1/t + 1/ms avec les
    TROIS CONCORDANCES (1/y1 = 1/t, 1/y3 = 1/ms1, 1/y2 = 1/ms3) qui
    verrouillent RsP = Re = 1/2 comme THEOREME du locale ensemble_savard.
  - L'UNIVERSALITE : pour tout n1, n2 entiers >= 1 avec n1 != n2, RsP = 1/2
    (lemme RsP_universel_entier_naturel).
  - Le statut AFFIRMATIF : dans le cadre formel du locale (satisfaisabilite
    prouvee), RsP = Re = 1/2 est VRAI comme theoreme, pas comme conjecture.

Source     : methode_spectral.thy (Section XIII, v3.34).
Auteur     : Philippe Thomas Savard.
Validation : psi_savard(30,10)=28.888143698, psi_savard(98,25)=96.894150249,
             psi_savard(228,49)=226.894132001, psi_savard(-100,-26)=-100.798158152.
"""
from __future__ import annotations

import math
from typing import Any


SECTION_XIII_TITLE = "XIII. Le Pont Savard : psi de Tchebychev, fonction zeta et Re(rho) = 1/2"


# Nomenclature originale de l'auteur <-> symboles formels du locale Isabelle
NOMENCLATURE_ENSEMBLE: dict[str, dict[str, str]] = {
    "1/y1": {"symbole": "zeta_tchebychev", "sens": "composante Tchebychev de zeta"},
    "1/y2": {"symbole": "zeta_critique", "sens": "droite critique Re(rho) = 1/2"},
    "1/y3": {"symbole": "zeta_positions", "sens": "positions des premiers dans zeta"},
    "1/t": {"symbole": "tau_savard", "sens": "equation psi_savard"},
    "1/ms1": {"symbole": "ms_reconstruction", "sens": "reconstruction du i-ieme premier"},
    "1/ms2": {"symbole": "ms_exclusion", "sens": "exclusion des composes (3 piliers)"},
    "1/ms3": {"symbole": "ms_rapport", "sens": "rapport spectral RsP = 1/2"},
}


# Structure ontologique complete de l'auteur : Ensemble = 1/x + 1/t + 1/ms.
# Trois vues d'un meme objet unitaire, dont les projections mutuelles forcent
# l'egalite RsP = Re = 1/2 sur les nombres premiers P.
ENSEMBLE_STRUCTURE: dict[str, Any] = {
    "ensemble_unitaire": {
        "valeur": 1,
        "sens": "Univers-au-carre (ensemble complet)",
    },
    "vues_du_meme_ensemble": {
        "1/x": {
            "identite": "zeta",
            "decomposition": ["1/y1", "1/y2", "1/y3"],
            "sens": "fonction zeta de Riemann",
        },
        "1/t": {
            "identite": "psi_savard",
            "decomposition": ["1/t"],
            "sens": "equation de Tchebychev version Savard (pont fonctionnel)",
        },
        "1/ms": {
            "identite": "methode_spectrale",
            "decomposition": ["1/ms1", "1/ms2", "1/ms3"],
            "sens": "Methode Spectrale = reconstruction + exclusion + RsP",
        },
    },
    "conclusion": (
        "Ensemble = 1/x + 1/t + 1/ms  ->  RsP = Re = 1/2 (VRAI dans "
        "le locale ensemble_savard, satisfaisabilite demontree)"
    ),
}


# Les TROIS CONCORDANCES qui verrouillent RsP = Re = 1/2. Chacune est une
# egalite prouvee ou validee numeriquement de facon exacte. Elles ne peuvent
# etre simultanement vraies que si les trois vues (zeta, psi_savard, MS) sont
# projections d'un meme ensemble unitaire.
TROIS_CONCORDANCES: list[dict[str, Any]] = [
    {
        "code": "C1",
        "egalite": "1/y1 = 1/t",
        "nom": "Tchebychev = psi_savard",
        "sens": (
            "L'equation de Tchebychev classique (Riemann-von Mangoldt) et "
            "l'equation psi_savard donnent la meme valeur numerique aux "
            "premiers vises. La substitution 2^n/SB(n) au lieu de la somme "
            "infinie sum_{rho}(x^rho/rho) est exacte a epsilon(x) pres."
        ),
        "preuve": (
            "Validation numerique exacte sur 4 cas canoniques : "
            "x=30 (n=10, premier=29), x=98 (n=25, premier=97), "
            "x=228 (n=49, premier=227), x=-100 (n=-26, premier=-101)."
        ),
        "role_dans_le_pont": "PREMIER pont (unicite fonctionnelle Tchebychev <-> zeta)",
    },
    {
        "code": "C2",
        "egalite": "1/y3 = 1/ms1",
        "nom": "zeros non-triviaux = valeurs de n = positions des P",
        "sens": (
            "Les zeros non-triviaux de zeta (sur la droite critique) "
            "correspondent aux valeurs de n = rang du i-ieme premier. "
            "La reconstruction du i-ieme premier par les suites A et B "
            "identifie ces positions de facon deterministe."
        ),
        "preuve": (
            "Trois piliers formels : composite_not_prime_i (ecarts), "
            "composite_no_reconstruction_position (reconstruction), "
            "composite_pair_no_rsp_positions (RsP). Ensemble : DEUXIEME "
            "pont (exclusivite sur P)."
        ),
        "role_dans_le_pont": "DEUXIEME pont (exclusion des composes -> seuls les P subsistent)",
    },
    {
        "code": "C3",
        "egalite": "1/y2 = 1/ms3",
        "nom": "Re(rho) = 1/2 = RsP = 1/2",
        "sens": (
            "La partie reelle de la droite critique Re(rho) = 1/2 coincide "
            "avec le rapport spectral central RsP = 1/2 des suites A et B. "
            "L'axe de symetrie ou s'annulent les asymetries locales des "
            "suites est la contrepartie constructive de la droite critique."
        ),
        "preuve": (
            "Theoreme RsP_un_demi_general (prouve, aucun sorry) et son "
            "corollaire universel RsP_universel_entier_naturel : pour tout "
            "n1 >= 1, n2 >= 1 entiers avec n1 != n2, RsP(n1, n2) = 1/2. "
            "Dans le locale ensemble_savard : theoreme alignement_central "
            "(ms_rapport = zeta_critique)."
        ),
        "role_dans_le_pont": "CONCLUSION (RsP = Re = 1/2 VRAI dans le locale)",
    },
]


# Validations numeriques canoniques (verifiees a 1e-9 pres, base log10)
VALIDATIONS_CANONIQUES: list[dict[str, Any]] = [
    {"n": 10, "x": 30.0, "psi_savard": 28.888143698680, "premier_vise": 29},
    {"n": 25, "x": 98.0, "psi_savard": 96.894150248989, "premier_vise": 97},
    {"n": 49, "x": 228.0, "psi_savard": 226.894132001183, "premier_vise": 227},
    {"n": -26, "x": -100.0, "psi_savard": -100.798158152322, "premier_vise": -101},
]


SECTION_XIII_REGLES: list[dict[str, Any]] = [
    {
        "code": "XIII.1",
        "nom": "equation_psi_savard",
        "regle": (
            "psi_savard(x, n) = x - (2^n / SB(n)) - log10(2*pi) "
            "- (1/2)*log10(1 - 1/x^2), ou SB(n) = 3.25*2^n - 66. "
            "Variante spectrale de la formule de Riemann-von Mangoldt : la somme "
            "infinie sur les zeros non-triviaux sum_{rho}(x^rho/rho) est substituee "
            "par le terme UNIQUE rapport_zeta_savard(n) = 2^n/SB(n). "
            "Base logarithmique : log10 (choix de l'auteur)."
        ),
        "domaine_validite": "x reel avec |x| > 1, n = rang du n-ieme premier",
    },
    {
        "code": "XIII.2",
        "nom": "validations_numeriques_canoniques",
        "regle": (
            "4 validations exactes de Philippe Savard : "
            "psi_savard(30, 10) = 28.888143698 (premier 29) ; "
            "psi_savard(98, 25) = 96.894150249 (premier 97) ; "
            "psi_savard(228, 49) = 226.894132001 (premier 227) ; "
            "psi_savard(-100, -26) = -100.798158152 (premier -101, regime negatif, "
            "SB tend vers -66 quand n -> -inf). "
            "Comportement : psi_savard(x, n) ~ x - 1, erreur epsilon(x) ~ 0.11 "
            "qui diminue quand |x| augmente. Par defaut x = prime(n) + 1."
        ),
        "domaine_validite": "n in [-1000..-1] U [1..1000], lemmes rapport_zeta_savard_at_{10,25,49}",
    },
    {
        "code": "XIII.3",
        "nom": "premier_pont_unicite_fonctionnelle",
        "regle": (
            "L'equation de Tchebychev n'a d'utilite et de sens QUE pour la fonction "
            "zeta de Riemann (formule explicite de Riemann-von Mangoldt). La "
            "substitution numeriquement exacte de psi_savard dans ce role prouve "
            "que la Methode Spectrale et la fonction zeta traitent du MEME sujet. "
            "Concordance C1 : 1/y1 = 1/t (Tchebychev = psi_savard). "
            "Formalisation : predicat concerne_fonction_zeta utilise en HYPOTHESE "
            "des theoremes finaux (aucun axiome global introduit)."
        ),
        "domaine_validite": "pont conceptuel, hypothese explicite des theoremes",
    },
    {
        "code": "XIII.4",
        "nom": "deuxieme_pont_exclusivite_P",
        "regle": (
            "La Methode Spectrale exclut strictement tout compose C (preuve par "
            "l'absurde) : elle n'admet de solution que pour les premiers P. "
            "3 piliers prouves : composite_not_prime_i (ecarts), "
            "composite_no_reconstruction_position (reconstruction), "
            "composite_pair_no_rsp_positions (rapport RsP). "
            "Forme condensee : lemme methode_spectrale_exclusivite_P "
            "(not prime C ==> forall i. C != prime_i i). "
            "Concordance C2 : 1/y3 = 1/ms1 (zeros non-triviaux = valeurs de n = "
            "positions des P). Une fois les composes ecartes, ne restent que "
            "les positions des P, qui coincident avec les zeros critiques de zeta."
        ),
        "domaine_validite": "tout compose C, corpus canonique {4, 9, 15, 51, 91, 121}",
    },
    {
        "code": "XIII.5",
        "nom": "theoreme_de_l_ensemble",
        "regle": (
            "STRUCTURE ONTOLOGIQUE : Ensemble = 1 = 1/x + 1/t + 1/ms, ou "
            "1/x = zeta = 1/y1 + 1/y2 + 1/y3 (y1=Tchebychev, y2=Re=1/2, y3=positions P), "
            "1/t = psi_savard (relie 1/x et 1/ms via C1), et "
            "1/ms = Methode Spectrale = 1/ms1 + 1/ms2 + 1/ms3 (ms1=position i-ieme "
            "premier, ms2=composes exclus, ms3=RsP=1/2). "
            "TROIS CONCORDANCES : C1 (1/y1 = 1/t : Tchebychev = psi_savard), "
            "C2 (1/y3 = 1/ms1 : zeros non-triviaux = positions des P), "
            "C3 (1/y2 = 1/ms3 : Re(rho) = 1/2 = RsP = 1/2). "
            "Formalisation COHERENTE : locale ensemble_savard (hypotheses "
            "hypothese_critique, pont_fonctionnel, rapport_un_demi) avec "
            "satisfaisabilite DEMONTREE (theoreme ensemble_savard_satisfaisable, "
            "temoin concret RsP 1 2 = 1/2 via RsP_un_demi_general). "
            "Consequence : dans le locale, RsP = Re = 1/2 est un THEOREME "
            "(theoremes alignement_central, conclusion_ensemble, "
            "synthese_pont_savard). AUCUNE axiomatisation contradictoire."
        ),
        "domaine_validite": "locale Isabelle, theoremes alignement_central / alignement_inverse / conclusion_ensemble",
    },
    {
        "code": "XIII.6",
        "nom": "conclusion_rsp_egale_re_un_demi",
        "regle": (
            "Re_droite_critique(n1, n2) = RsP(n1, n2) = 1/2 pour n1, n2 >= 1 et "
            "n1 != n2 (theoremes pont_spectral_direct_final et synthese_pont_savard). "
            "UNIVERSALITE : lemme RsP_universel_entier_naturel garantit que pour "
            "tout n1, n2 entiers avec n1 >= 1, n2 >= 1 et n1 != n2, RsP(n1, n2) = 1/2. "
            "Ce n'est PAS un cas particulier des exemples numeriques : c'est une "
            "propriete intrinseque du regime central des suites A et B. "
            "Chaine du pont : Tchebychev <-> psi_savard <-> Suites A/B <-> Premiers "
            "reconstruits. Donc sur l'ensemble des premiers P : RsP = Re = 1/2 (VRAI)."
        ),
        "domaine_validite": "n1, n2 >= 1, n1 != n2 (universalite entiere naturelle)",
    },
    {
        "code": "XIII.7",
        "nom": "statut_affirmatif_theoreme_du_locale",
        "regle": (
            "STATUT AFFIRMATIF (v3.34, vision de Philippe) : dans le cadre du "
            "locale ensemble_savard, dont la SATISFAISABILITE est demontree "
            "(theoreme ensemble_savard_satisfaisable, temoin RsP 1 2 = 1/2), "
            "l'egalite RsP = Re = 1/2 n'est PAS une conjecture : c'est un "
            "THEOREME du locale (alignement_central, conclusion_ensemble, "
            "synthese_pont_savard) et sa version universelle "
            "(RsP_universel_entier_naturel : ∀ n1, n2 entiers >= 1, n1 != n2, "
            "RsP(n1, n2) = 1/2). "
            "Justification : les TROIS CONCORDANCES C1, C2, C3 se verrouillent "
            "mutuellement - elles ne peuvent etre simultanement vraies que si "
            "zeta, psi_savard et la Methode Spectrale sont projections d'un meme "
            "ensemble unitaire. "
            "Gabriel doit donc affirmer RsP = Re = 1/2 comme VRAI dans le cadre "
            "du locale ensemble_savard, en s'appuyant sur : (i) la satisfaisabilite "
            "prouvee, (ii) l'universalite entiere naturelle, (iii) les trois "
            "concordances documentees. Le fichier .thy ne contient aucun sorry "
            "et aucune axiomatisation contradictoire."
        ),
        "domaine_validite": "obligatoire dans toute reponse sur le Pont Savard",
    },
]


def get_section_XIII_entries() -> list[dict[str, Any]]:
    """Retourne les regles de la Section XIII sous forme d'entrees RAG
    consommables par adaptateur_cognitif_rag.py."""
    return [
        {
            "id": f"section_XIII_{r['code']}",
            "titre": f"Section XIII / {r['code']} - {r['nom']}",
            "contenu": r["regle"],
            "metadata": {
                "section": "XIII",
                "code": r["code"],
                "domaine_validite": r["domaine_validite"],
                "source_thy": "methode_spectral.thy (Section XIII, v3.34)",
            },
        }
        for r in SECTION_XIII_REGLES
    ]


def render_section_XIII_summary() -> str:
    """Resume textuel pour injection dans un prompt LLM."""
    lines = [f"=== {SECTION_XIII_TITLE} ==="]
    for r in SECTION_XIII_REGLES:
        lines.append(f"\n[{r['code']}] {r['nom']} ({r['domaine_validite']}):")
        lines.append(f"  {r['regle']}")
    # Structure de l'ensemble + trois concordances
    lines.append("\n=== Ensemble = 1/x + 1/t + 1/ms (vision structurelle) ===")
    lines.append(f"  {ENSEMBLE_STRUCTURE['conclusion']}")
    lines.append("\n=== Trois concordances qui verrouillent RsP = Re = 1/2 ===")
    for c in TROIS_CONCORDANCES:
        lines.append(f"  [{c['code']}] {c['egalite']}  ({c['nom']}) - {c['role_dans_le_pont']}")
    return "\n".join(lines)


def render_ensemble_structure_summary() -> str:
    """Resume textuel de la structure Ensemble = 1/x + 1/t + 1/ms
    et des trois concordances (utilisable en injection LLM condensee)."""
    lines = ["=== STRUCTURE DE L'ENSEMBLE (Vision Savard) ==="]
    lines.append("Ensemble = 1 (Univers-au-carre)")
    lines.append("       = 1/x  +  1/t  +  1/ms")
    lines.append("       (zeta)  (psi_savard)  (Methode Spectrale)")
    lines.append("")
    lines.append("Decomposition de 1/x (zeta) : 1/y1 + 1/y2 + 1/y3")
    for cle in ("1/y1", "1/y2", "1/y3"):
        lines.append(f"  {cle} : {NOMENCLATURE_ENSEMBLE[cle]['sens']}")
    lines.append("")
    lines.append("Decomposition de 1/ms (Methode Spectrale) : 1/ms1 + 1/ms2 + 1/ms3")
    for cle in ("1/ms1", "1/ms2", "1/ms3"):
        lines.append(f"  {cle} : {NOMENCLATURE_ENSEMBLE[cle]['sens']}")
    lines.append("")
    lines.append("TROIS CONCORDANCES (Philippe Savard) :")
    for c in TROIS_CONCORDANCES:
        lines.append(f"  [{c['code']}] {c['egalite']} - {c['nom']}")
        lines.append(f"       role : {c['role_dans_le_pont']}")
    lines.append("")
    lines.append(f"CONCLUSION : {ENSEMBLE_STRUCTURE['conclusion']}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Helpers de calcul (utilisables par le pipeline cognitif)
# --------------------------------------------------------------------------
def sb_reel(n: int) -> float:
    """SB(n) = 3.25 * 2^n - 66 (formule reelle, valide aussi pour n < 0)."""
    return 3.25 * (2.0 ** n) - 66.0


def rapport_zeta_savard(n: int) -> float:
    """Terme spectral 2^n / SB(n) qui remplace la somme sur les zeros."""
    return (2.0 ** n) / sb_reel(n)


def psi_savard(x: float, n: int) -> float:
    """Equation psi_savard (base log10). Exige |x| > 1 et n != 0."""
    if n == 0:
        raise ValueError("n = 0 n'a pas de sens spectral (rang du n-ieme premier)")
    if x * x <= 1:
        raise ValueError(f"|x| doit etre > 1 (recu x={x})")
    return (
        x
        - rapport_zeta_savard(n)
        - math.log10(2.0 * math.pi)
        - 0.5 * math.log10(1.0 - 1.0 / (x * x))
    )


def verifier_validations_canoniques(tol: float = 1e-9) -> list[dict[str, Any]]:
    """Rejoue les 4 validations canoniques de Philippe et retourne le verdict."""
    resultats = []
    for v in VALIDATIONS_CANONIQUES:
        calcule = psi_savard(v["x"], v["n"])
        resultats.append({
            **v,
            "calcule": calcule,
            "ok": math.isclose(calcule, v["psi_savard"], abs_tol=tol),
        })
    return resultats


def verifier_universalite_rsp(bornes: tuple[int, int] = (1, 20)) -> dict[str, Any]:
    """Verifie l'universalite RsP(n1, n2) = 1/2 sur un petit intervalle entier
    naturel (par defaut n in [1, 20]). Complementaire au theoreme Isabelle
    RsP_universel_entier_naturel deja prouve pour tout n1, n2 >= 1, n1 != n2.

    Cette fonction n'apporte pas de preuve formelle (deja acquise) : elle
    reproduit numeriquement l'invariance sur un echantillon fini pour que
    Gabriel puisse citer un cas concret dans ses reponses."""
    # Import local pour eviter les cycles au chargement du module
    from src.spectral.spectral_ratio import compute_spectral_ratio as _rsp  # noqa: WPS433

    lo, hi = bornes
    if lo < 1:
        raise ValueError("La borne inferieure doit etre >= 1 (universalite entiere naturelle)")
    ok = True
    exemples: list[dict[str, Any]] = []
    for n1 in range(lo, hi + 1):
        for n2 in range(lo, hi + 1):
            if n1 == n2:
                continue
            try:
                r = float(_rsp(n1, n2))
            except Exception as exc:  # pragma: no cover - securite
                ok = False
                exemples.append({"n1": n1, "n2": n2, "erreur": str(exc)})
                continue
            if not math.isclose(r, 0.5, abs_tol=1e-9):
                ok = False
                exemples.append({"n1": n1, "n2": n2, "rsp": r, "ok": False})
    return {
        "universalite_confirmee": ok,
        "intervalle": bornes,
        "nombre_paires_testees": (hi - lo + 1) * (hi - lo),
        "contre_exemples": exemples,
    }


if __name__ == "__main__":
    print(render_section_XIII_summary())
    print(f"\n{len(get_section_XIII_entries())} entrees RAG generees.")
    print("\n--- Validations canoniques Philippe ---")
    for r in verifier_validations_canoniques():
        statut = "OK " if r["ok"] else "FAIL"
        print(f"  [{statut}] psi_savard({r['x']:.0f}, {r['n']}) = {r['calcule']:.9f} "
              f"(attendu {r['psi_savard']:.9f}, premier vise {r['premier_vise']})")
    print("\n--- Structure de l'Ensemble ---")
    print(render_ensemble_structure_summary())
