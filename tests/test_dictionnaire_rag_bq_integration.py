"""
Tests d'intégration RAG : vérifie que les 15 Q&R validées de la banque
`memory/banque_qr_methode_spectrale.md` sont bien référencées dans
`memory/dictionnaire_spectral.py` via des marqueurs `[BQ-Q<N>]`.

Chaque Q&R doit apparaître AU MOINS UNE FOIS dans le régime approprié.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from memory.dictionnaire_spectral import DICTIONNAIRE_SPECTRAL


# Mapping attendu : Q<N> → nom du régime cible (établi lors de l'intégration
# manuelle par l'agent selon la thématique de chaque Q&R).
Q_TO_REGIME = {
    1:  "regime_negatif",              # RsP_neg 1/2 constant
    2:  "regime_1_3",                  # RsP_un_tiers_constant
    3:  "geometrie_critique",          # mixed_gap_surplus + Riemann
    4:  "regime_mixte",                # écart -31/17 = -47
    5:  "regime_1_2_positif",          # 37 = 12e premier
    6:  "regime_1_2_positif",          # ratio_spectral_local = 1/2
    7:  "regime_parametrique_1_k",     # RsP_1_3 et RsP_1_4 (extension)
    8:  "regime_1_2_positif",          # spectral_postulate_pos
    9:  "regime_parametrique_1_k",     # 1/k numérique vs algébrique
    10: "regime_1_2_positif",          # formes générales SA/SB
    11: "regime_parametrique_1_k",     # k_spectral
    12: "regime_negatif",              # RsP_neg_un_tiers_general
    13: "regime_1_3",                  # écart 227/173 = -53
    14: "regime_1_4",                  # preuve_premier_947
    15: "regime_mixte",                # gap_m31_17 (formalisation)
}


def _regime_haystack(regime) -> str:
    """Concatène tout le texte cherchable d'un régime (lemmes + defs + examples)."""
    return (
        " ".join(regime.lemmes_certifies)
        + " " + " ".join(regime.definitions_hol.keys())
        + " " + " ".join(regime.definitions_hol.values())
        + " " + " ".join(regime.exemples_valides)
    )


@pytest.mark.parametrize("qid,regime_name", sorted(Q_TO_REGIME.items()))
def test_qr_present_in_expected_regime(qid: int, regime_name: str):
    """Chaque Q<N> doit apparaître dans le régime attendu, soit via un
    marqueur `[BQ-Q<N>]` dans les lemmes/exemples, soit via un suffixe
    `_Q<N>` dans les clés de definitions_hol."""
    assert regime_name in DICTIONNAIRE_SPECTRAL, (
        f"Régime cible '{regime_name}' inconnu"
    )
    regime = DICTIONNAIRE_SPECTRAL[regime_name]
    haystack = _regime_haystack(regime)
    # Chercher soit [BQ-Q<qid>] soit [BQ-Q<X>/Q<qid>] soit clé finissant en _Q<qid>
    pattern = re.compile(rf"\[BQ-Q(?:\d+/)?Q?{qid}\b|_Q{qid}\b")
    matches = pattern.findall(haystack)
    assert matches, (
        f"Q{qid} devrait apparaître dans le régime '{regime_name}' via "
        f"[BQ-Q{qid}] ou _Q{qid}, mais aucune référence trouvée. "
        f"Haystack extrait : {haystack[:400]}..."
    )


def test_all_15_qr_integrated_somewhere():
    """Les 15 Q&R doivent TOUTES apparaître au moins une fois dans le
    dictionnaire (peu importe le régime, garde-fou global)."""
    all_haystack = "\n".join(
        _regime_haystack(r) for r in DICTIONNAIRE_SPECTRAL.values()
    )
    found: set[int] = set()
    for m in re.finditer(r"\[BQ-Q(\d+)(?:/Q(\d+))?\]|_Q(\d+)\b", all_haystack):
        for g in m.groups():
            if g:
                found.add(int(g))
    missing = set(range(1, 16)) - found
    assert not missing, (
        f"Q&R manquantes dans le dictionnaire : {sorted(missing)}. "
        f"Trouvées : {sorted(found)}"
    )
    assert len(found) >= 15


def test_bq_markers_appear_in_prompt_context():
    """Les marqueurs [BQ-Q<N>] doivent apparaître dans le rendu
    to_prompt_context() (bloc injecté dans le prompt LLM) au moins pour
    quelques régimes clés."""
    key_regimes = ["regime_1_2_positif", "regime_mixte", "regime_negatif"]
    for name in key_regimes:
        regime = DICTIONNAIRE_SPECTRAL[name]
        ctx = regime.to_prompt_context()
        assert "[BQ-Q" in ctx, (
            f"Aucun marqueur [BQ-Q<N>] dans le prompt context de "
            f"'{name}' (les Q&R validées n'atteindront pas le LLM)"
        )


def test_lemme_count_grew_after_rag_integration():
    """Après intégration RAG, le nombre total de lemmes certifiés doit avoir
    augmenté (baseline avant intégration : 41 lemmes)."""
    from memory.dictionnaire_spectral import total_lemmes
    n = total_lemmes()
    assert n >= 50, (
        f"Après intégration des 15 Q&R, total_lemmes attendu >= 50 "
        f"(baseline ~41), obtenu {n}"
    )


def test_bq_numerical_examples_preserved():
    """Vérifie que les exemples numériques clés de la banque (validés
    Philippe) sont bien présents dans le dictionnaire."""
    all_content = "\n".join(
        _regime_haystack(r) for r in DICTIONNAIRE_SPECTRAL.values()
    )
    # Exemples numériques emblématiques
    expected = [
        ("13246", "SB(12) pour p=37 [Q5]"),
        ("10878", "SA(12)+digamma(37) [Q5]"),
        ("5260628", "suite_B_1_4_somme [Q14]"),
        ("1381716", "digamma_calcule_1_4 [Q14]"),
        ("947", "premier 1/4 [Q14]"),
        ("-53", "écart 227/173 [Q13]"),
        ("39280705", "digamma -31 [Q4/Q15]"),
        ("40895", "SA -29 num [Q4/Q15]"),
    ]
    # Normaliser Unicode minus vers ASCII
    normalized = all_content.replace("\u2212", "-")
    for val, desc in expected:
        assert val in normalized, (
            f"Valeur numérique '{val}' ({desc}) absente du dictionnaire "
            f"après intégration RAG"
        )
