from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    from .suites_geometriques_niveau2 import (
        CalculateurNiveau1Entiers, est_premier, valider_n
    )
except ImportError:
    from suites_geometriques_niveau2 import (
        CalculateurNiveau1Entiers, est_premier, valider_n
    )

ANCHORS_N10 = {
    2: 29, 3: 227, 4: 947, 5: 2999, 6: 7529, 7: 16519, 8: 32327, 9: 58337,
    10: 99109, 12: 247259, 13: 368939, 15: 755789, 16: 1044751, 17: 1414943,
    18: 1883429, 19: 2469277, 20: 3192419, 21: 4074419, 23: 6424727,
    24: 7949399, 25: 9750649, 26: 11863799, 30: 24273929, 32: 33522719,
    36: 60420851, 37: 69293303, 40: 102337639, 42: 130617143, 43: 146929021,
    46: 205867801, 49: 282357599, 52: 380066179, 54: 459010529,
    57: 601506977, 58: 656165077, 62: 915894503, 63: 992182589,
    64: 1073483839, 65: 1160020289, 66: 1252049501, 69: 1563702839,
    70: 1680356999, 71: 1803876551, 75: 2372624999, 77: 2706333629,
    78: 2886705977, 80: 3276294479, 85: 4436438999, 87: 4983550877,
    96: 8152842431, 97: 8586418271, 102: 11039747027, 103: 11591637509,
    105: 12761657999, 106: 13381076101, 107: 14024303819, 108: 14692021271,
    109: 15384932747, 111: 16849226351
}

def _regle_speciale(k: int) -> Optional[str]:
    regles = {
        11: "REGLE_SPECIALE_PDF",
        27: "REGLE_SPECIALE_HOL",
        22: "AUCUN_P", 28: "AUCUN_P", 29: "AUCUN_P", 31: "AUCUN_P",
        33: "AUCUN_P", 34: "AUCUN_P", 35: "AUCUN_P", 38: "AUCUN_P",
        39: "AUCUN_P", 41: "AUCUN_P", 44: "AUCUN_P", 45: "AUCUN_P",
        47: "AUCUN_P", 48: "AUCUN_P", 50: "AUCUN_P", 51: "AUCUN_P",
        53: "AUCUN_P", 55: "AUCUN_P", 56: "AUCUN_P", 59: "AUCUN_P",
        60: "AUCUN_P", 61: "AUCUN_P", 67: "AUCUN_P", 68: "AUCUN_P",
        72: "AUCUN_P", 73: "AUCUN_P", 74: "AUCUN_P", 76: "AUCUN_P",
        79: "AUCUN_P", 81: "AUCUN_P", 82: "AUCUN_P", 83: "AUCUN_P",
        84: "AUCUN_P", 86: "AUCUN_P", 89: "AUCUN_P", 90: "AUCUN_P",
        91: "AUCUN_P", 92: "AUCUN_P", 93: "AUCUN_P", 94: "AUCUN_P",
        95: "AUCUN_P", 98: "AUCUN_P", 99: "AUCUN_P", 100: "AUCUN_P",
        101: "AUCUN_P", 104: "AUCUN_P", 110: "AUCUN_P"
    }
    return regles.get(k, None)

def _nieme_premier(pos: int) -> int:
    if pos < 1:
        return 0
    compte, candidat = 0, 1
    while compte < pos:
        candidat += 1
        if est_premier(candidat):
            compte += 1
    return candidat

@dataclass
class ResultatRatioUnique:
    k: int
    n: int
    typique: bool
    somme_A: int
    somme_B: int
    premier_ancre_n10: Optional[int]
    premier_n: Optional[int]
    digamma_calcule: Optional[int]
    position_dans_P: Optional[int]
    reconstruction_reussie: bool
    message: str = ""

@dataclass
class ResultatMultiRatio:
    n: int
    liste_k: List[int]
    resultats: Dict[int, ResultatRatioUnique] = field(default_factory=dict)

    def rapport_texte(self):
        sep = "=" * 72
        L = [sep]
        L.append(f"REQUETE MULTI-RATIO | n={self.n}")
        L.append(sep)
        for k, r in self.resultats.items():
            L.append(f"1/{k} | P={r.premier_n} | {r.message}")
        L.append(sep)
        return "\n".join(L)

class MultiRatioDispatcher:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def requete(self, n: int, liste_k=None) -> ResultatMultiRatio:
        valider_n(n)
        if liste_k is None:
            raise ValueError("Vous devez fournir une liste de k.")
        res = ResultatMultiRatio(n=n, liste_k=list(liste_k))
        for k in liste_k:
            res.resultats[k] = self._traiter_ratio(k, n)
        return res

    def _traiter_ratio(self, k: int, n: int) -> ResultatRatioUnique:
        special = _regle_speciale(k)
        if special:
            return ResultatRatioUnique(k, n, False, 0, 0, None, None, None, None, False, special)

        calc = CalculateurNiveau1Entiers(k)
        res_n = calc.calculer(n)
        res_10 = calc.calculer(10)

        if k in ANCHORS_N10:
            ancre = ANCHORS_N10[k]
            pos_ancre = 1
            pos_n = pos_ancre + (n - 10)
            premier_n = _nieme_premier(pos_n)
            return ResultatRatioUnique(k, n, False, res_n.somme_A, res_n.somme_B, ancre, premier_n, None, pos_n, True, "")

        return ResultatRatioUnique(k, n, False, res_n.somme_A, res_n.somme_B, None, None, None, None, False, "Reconstruction generale (k > 111).")

def requete_multi_k(n: int, liste_k=None, verbose=False):
    return MultiRatioDispatcher(verbose).requete(n, liste_k)
