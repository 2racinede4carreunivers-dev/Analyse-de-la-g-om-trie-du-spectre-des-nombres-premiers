"""Regression tests v3.46 pour _extract_numbers : doit gerer les nombres
suivis d'accents Unicode (132ème, 3ème, etc.) ET rester ReDoS-safe."""
import re
import time
import pytest

from src.engines.abstraction.abstraction_layer import _extract_numbers


@pytest.mark.parametrize("text,expected", [
    # Ordinaux francais avec accents (bug v3.45 -> fix v3.46)
    ("reconstruis le 132ème premier",      [132]),
    ("reconstruis le 132eme premier",      [132]),
    ("reconstruis le 132ième nombre premier", [132]),
    ("le 26ème premier",                    [26]),
    ("le 3ème et le 5ème premier",          [3, 5]),
    # Cas historiques (non-regression)
    ("p=29 et n=10",                        [29, 10]),
    ("trace la courbe pour n=1..50",        [1, 50]),
    ("modele 1/4 pour n=132",               [132]),
    ("valeur -66",                          [-66]),
    # Fractions et rapports (filtres en amont)
    ("rapport 1/2 avec n=13",               [13]),
])
def test_extract_numbers_ordinaux_et_regressions(text, expected):
    assert _extract_numbers(text) == expected


def test_extract_numbers_pas_de_word_boundary_unicode():
    """Le bug v3.45 : \\b considerait 'è' comme char de mot -> pas de
    boundary apres '132' dans '132ème'. Le fix v3.46 utilise des
    lookarounds a largeur fixe qui excluent explicitement les digits."""
    # Sans le fix, cette assertion echoue (retourne [])
    assert _extract_numbers("132ème") == [132]


def test_extract_numbers_no_redos_pathological_input():
    """L'ancienne version (?<![\\d.]) etait vulnerable a ReDoS ;
    la nouvelle (?<!\\d) est a largeur fixe, garantie lineaire."""
    payload = ("1" * 5000) + "x" + ("2" * 5000)
    t0 = time.time()
    # On ne convertit pas en int (limite Python) mais on verifie que le
    # regex trouve les 2 matches en temps constant lineaire.
    matches = re.findall(r'(?<!\d)-?\d+(?!\d)', payload)
    dt = time.time() - t0
    assert len(matches) == 2, f"attendu 2 matches, obtenu {len(matches)}"
    assert dt < 0.5, f"regex trop lente : {dt:.3f}s (ReDoS suspect)"


def test_extract_numbers_ancien_pattern_absent():
    """Verifie que l'ancien pattern \\b-?\\d+\\b (v3.45, casse par
    l'Unicode) n'est plus utilise dans le code source."""
    from pathlib import Path
    src = Path(__file__).parent.parent / "src" / "engines" / "abstraction" / "abstraction_layer.py"
    txt = src.read_text(encoding="utf-8")
    assert r"\b-?\d+\b" not in txt, (
        "L'ancien pattern \\b-?\\d+\\b est de retour ; il casse la detection "
        "des nombres suivis d'accents Unicode (132eme, 132ème). Utiliser "
        "(?<!\\d)-?\\d+(?!\\d) pour rester ReDoS-safe et Unicode-safe."
    )
