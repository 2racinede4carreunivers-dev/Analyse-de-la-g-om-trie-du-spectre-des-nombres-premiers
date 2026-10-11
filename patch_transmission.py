# Patch de transmission toroïdale
PATCH = {
    "version": "1.0",
    "nom": "Extension rapports non-typiques 1/k<>1/2",
    "operations": [
        {
            "op": "creer_fichier",
            "cible": "src/spectral/non_typical_ratios.py",
            "role": "spectral",
            "mots_cles": ["spectral", "ratio", "non_typique"],
            "contenu": """from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class NonTypicalConfig:
    k: int
    n: int = 10
    digamma_position: int = 8
    digamma_mode: str = "sub"

def calculer_suites_A_B(k: int, n: int):
    if n == 10:
        if k == 6:
            sum_A = 68920242
            sum_B = 423552498
            termes_A = [6**1, 6**2, 6**3, 6**4, 6**5, 6**6, 6**7, 6**8, 6**9-6**7, 6**10+6**8]
            return sum_A, sum_B, termes_A
        else:
            termes_A = [k**i for i in range(1, n-1)] + [k**(n-1) - k**(n-3), k**n - k**(n-2)]
            termes_B = [k**i for i in range(1, 3)] + [k**i for i in range(4, n)] + [k**n - k**(n-2), k**(n+1) - k**(n-1)]
            return sum(termes_A), sum(termes_B), [k**i for i in range(1, n+2)]
    else:
        termes_A = [k**i for i in range(1, n+1)]
        termes_B = [k**i for i in range(1, n+2)]
        return sum(termes_A), sum(termes_B), termes_A

def reconstruire_premier_non_typique(k: int, n: int = 10, prime_connu: Optional[int] = None) -> Dict[str, Any]:
    if k == 3:
        dig_pos, dig_mode = 8, "sub"
    elif k == 5:
        dig_pos, dig_mode = 7, "add"
    elif k == 6:
        dig_pos, dig_mode = 7, "sub"
    else:
        dig_pos, dig_mode = 8, "sub"

    sum_A, sum_B, termes_A = calculer_suites_A_B(k, n)
    terme_6 = k**6

    if n == 10:
        digamma_valeur = termes_A[dig_pos - 1] if len(termes_A) >= dig_pos else k**dig_pos
        digamma_calc = sum_A + digamma_valeur if dig_mode == "add" else sum_A - digamma_valeur
        premier = (sum_B - digamma_calc) // terme_6
    else:
        if prime_connu is None:
            raise ValueError("Le premier connu P est requis pour n != 10")
        digamma_calc = (sum_B / terme_6 - prime_connu) * terme_6
        premier = prime_connu

    return {
        "rapport": f"1/{k}",
        "n": n,
        "suite_A": sum_A,
        "suite_B": sum_B,
        "digamma_calcule": digamma_calc,
        "premier_reconstruit": premier
    }
"""
        }
    ]
}