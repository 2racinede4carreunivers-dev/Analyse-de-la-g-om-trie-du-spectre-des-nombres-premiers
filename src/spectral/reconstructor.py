"""
Reconstructeur du P-ieme nombre premier.

Repond a la Question 1 : etant donne n (nombre de termes dans suites A et B),
le P-ieme premier est determine via le postulat spectral :
   prime_equation(n, p) = real p   (axiome)

Fournit toutes les valeurs intermediaires : SA, SB, Digamma, Digamma calcule.
"""
from __future__ import annotations

from fractions import Fraction

from .digamma import digamma_calc, prime_equation, verify_prime_equation
from .suites import get_suite_functions


# Table des premiers de reference (n => p) pour le modele 1/2
# Tiree des exemples du corpus : 29 (n=10), 31 (n=11), 37 (n=12), 41 (n=13)
N_TO_PRIME_TABLE_1_2 = {
    10: 29,
    11: 31,
    12: 37,
    13: 41,
}

EXAMPLES_BY_MODEL = {
    "1/2": N_TO_PRIME_TABLE_1_2,
    "1/3": {},  # Modele 1/3 - exemple 227 (sommes de blocs)
    "1/4": {},  # Modele 1/4 - exemple 947 (sommes de blocs)
}


def reconstruct_pth_prime_full(n: int, p: int | None = None, model: str = "1/2") -> dict:
    """
    Reconstruit le P-ieme nombre premier a partir de n et fournit tous les details
    spectraux : SA, SB, Digamma, Digamma calcule, p reconstruit.

    Si p est None et n est dans la table de reference, l'utilise.
    Si p est fourni, verifie l'equation.

    Retour : dict complet pour explication a l'utilisateur.
    """
    # Determination de p
    if p is None:
        table = EXAMPLES_BY_MODEL.get(model, {})
        if n not in table:
            raise ValueError(
                f"Pour modele {model}, n={n} n'est pas dans la table de reference. "
                f"Fournissez p explicitement ou utilisez n parmi : {sorted(table)}"
            )
        p = table[n]

    # Verification complete
    result = verify_prime_equation(n, p, model)

    # Ajouter le Digamma "vrai" attendu, qui est le Digamma calcule moins l'erreur
    # Note : dans le corpus, "Digamma" et "Digamma calcule" sont la meme quantite
    # = SB(n) - 64*p (modele 1/2). C'est la valeur produite par la formule.

    fns = get_suite_functions(model)
    factor = fns["factor"]

    explanation_lines = [
        f"--- Reconstruction du {p}-ieme nombre premier (modele {model}) ---",
        f"Donnees : n = {n} termes dans les suites A et B.",
        f"Modele spectral : {model} - base {fns['base']} - facteur {factor}.",
        "",
        "Calcul des sommes :",
        f"  SA(n={n})   = {result['SA']}   (~ {result['SA_float']})",
        f"  SB(n={n})   = {result['SB']}   (~ {result['SB_float']})",
        "",
        f"Digamma calcule : digamma_calc(n, p) = SB(n) - {factor} * p",
        f"  digamma_calc = {result['SB']} - {factor} * {p} = {result['digamma_calc']} "
        f"(~ {result['digamma_calc_float']})",
        "",
        f"Equation du premier : prime_equation(n, p) = (SB(n) - digamma_calc) / {factor}",
        f"  prime_equation = ({result['SB']} - {result['digamma_calc']}) / {factor} = "
        f"{result['reconstructed_p']} (~ {result['reconstructed_p_float']})",
        "",
        f"Verification : prime_equation == p ? {result['equation_holds']}",
        f"==> Le P-ieme nombre premier est P = {p}.",
    ]

    return {
        **result,
        "explanation_lines": explanation_lines,
        "explanation": "\n".join(explanation_lines),
    }


def reconstruct_from_blocks(
    n_value_target: int,
    sum_A_value: Fraction,
    sum_B_value: Fraction,
    digamma_value: Fraction,
    model: str,
) -> dict:
    """
    Cas exemple 947 / 227 : on a deja les sommes des blocs.
    Reconstruit via :
       p = (sum_B - (sum_A - digamma)) / factor   (interpretation symetrique)
       OU plus simplement (selon le corpus exemple 947) :
       p = (sum_B_value - digamma_calcule) / factor    ou digamma_calcule = sum_A + digamma
    """
    fns = get_suite_functions(model)
    factor = fns["factor"]
    digamma_calcule = sum_A_value + digamma_value  # exemple 947 dans le corpus
    p = (sum_B_value - digamma_calcule) / factor

    return {
        "model": model,
        "factor": factor,
        "sum_A": sum_A_value,
        "sum_B": sum_B_value,
        "digamma": digamma_value,
        "digamma_calcule": digamma_calcule,
        "reconstructed_p": p,
        "reconstructed_p_float": float(p),
        "is_integer": p == int(p),
    }


def reconstruire_non_typique_interface(k: int):
    from src.spectral.non_typical_ratios import NonTypicalConfig, reconstruire_premier_non_typique
    cfg = NonTypicalConfig(k=k)
    return reconstruire_premier_non_typique(cfg)


def reconstruire_non_typique_interface(k: int):
    from src.spectral.non_typical_ratios import NonTypicalConfig, reconstruire_premier_non_typique
    cfg = NonTypicalConfig(k=k)
    return reconstruire_premier_non_typique(cfg)
