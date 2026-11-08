"""
Test sentinelle pour la banque Q&R Méthode Spectrale.

Ne fait PAS de validation sémantique — juste des garde-fous structurels
pour éviter que le fichier ne soit supprimé, tronqué ou corrompu par erreur.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BANQUE_PATH = ROOT / "memory" / "banque_qr_methode_spectrale.md"


@pytest.fixture(scope="module")
def banque_content() -> str:
    if not BANQUE_PATH.exists():
        pytest.fail(
            f"Fichier banque Q&R absent : {BANQUE_PATH}. "
            "Ne PAS supprimer memory/banque_qr_methode_spectrale.md — "
            "curation manuelle Philippe."
        )
    return BANQUE_PATH.read_text(encoding="utf-8")


def test_banque_file_exists():
    assert BANQUE_PATH.exists(), (
        f"Fichier banque Q&R absent : {BANQUE_PATH}"
    )


def test_banque_has_exactly_15_questions(banque_content: str):
    """Curation Philippe : exactement 15 Q&R pertinentes (sur 184 initiales
    → 27 pré-filtrées → 15 cohérentes)."""
    n = banque_content.count("\n## Q")
    assert n == 15, (
        f"La banque doit contenir exactement 15 Q&R (curation Philippe), "
        f"trouvé : {n}"
    )


def test_banque_covers_key_regimes(banque_content: str):
    """Vérifie que les 5 régimes canoniques sont mentionnés dans la table
    récapitulative."""
    expected_regimes = [
        "1/2 positif",
        "1/2 négatif",
        "1/3",  # couvre 1/3 positif ET négatif
        "1/4",
        "mixte",
    ]
    for r in expected_regimes:
        assert r in banque_content, (
            f"Régime '{r}' absent de la banque Q&R"
        )


def test_banque_has_validation_status_markers(banque_content: str):
    """Chaque Q doit avoir une ligne de statut, peu importe le contenu entre
    crochets ([ ], [OK], [Ok], [ok], [KO], [Ko], [ko], [X], etc.).

    Ce test est volontairement TOLERANT : il vérifie juste qu'il y a 15
    lignes de statut, sans imposer une casse ou une syntaxe précise. La
    validation sémantique fine est faite par test_banque_validation_progress.
    """
    import re
    # Matche n'importe quel contenu (non-vide OU vide) entre crochets après "**Statut** : "
    pattern = re.compile(
        r"^\*\*Statut\*\*\s*:\s*\[[^\]]*\]",
        re.MULTILINE,
    )
    matches = pattern.findall(banque_content)
    assert len(matches) == 15, (
        f"La banque doit avoir 15 lignes de statut (une par Q&R), "
        f"trouvé {len(matches)}. Vérifier que le fichier "
        f"memory/banque_qr_methode_spectrale.md contient exactement 15 "
        f"lignes commençant par '**Statut** : [...]' (peu importe le "
        f"contenu entre crochets)."
    )


def test_banque_validation_progress(banque_content: str) -> None:
    """Snapshot de l'état de validation Philippe (informatif, pas bloquant).
    Compte les Q&R validées [OK]/[Ok]/[ok], rejetées [KO]/[Ko]/[ko] et
    encore en attente [ ]."""
    import re
    ok_pattern = re.compile(
        r"^\*\*Statut\*\* : \[(?:OK|Ok|ok)\]", re.MULTILINE
    )
    ko_pattern = re.compile(
        r"^\*\*Statut\*\* : \[(?:KO|Ko|ko)\]", re.MULTILINE
    )
    pending_pattern = re.compile(r"^\*\*Statut\*\* : \[ \]", re.MULTILINE)

    n_ok = len(ok_pattern.findall(banque_content))
    n_ko = len(ko_pattern.findall(banque_content))
    n_pending = len(pending_pattern.findall(banque_content))
    total = n_ok + n_ko + n_pending

    # Invariant : total = 15 (le fichier a 15 Q)
    assert total == 15, (
        f"Somme des statuts (OK+KO+pending) doit valoir 15, "
        f"obtenu {n_ok} OK + {n_ko} KO + {n_pending} pending = {total}"
    )
    # État attendu au 2026-07-01 : les 15 Q&R sont validées [OK] par Philippe
    # (commit github/main 0639761 "Titre: Réponse pour E1 Q et R .")
    assert n_ok == 15, (
        f"Les 15 Q&R doivent être marquées [OK]/[Ok]/[ok] par Philippe. "
        f"État actuel : {n_ok} OK, {n_ko} KO, {n_pending} pending"
    )


def test_banque_references_key_lemmas(banque_content: str):
    """Les lemmes Isabelle/HOL clés doivent apparaître dans la banque."""
    key_lemmas = [
        "spectral_postulate_pos",
        "spectral_ratio_neg_un_demi",
        "RsP_neg_un_demi_general",
        "RsP_neg_un_tiers_general",
        "ratio_spectral_local",
        "mixed_gap_surplus",
        "ecart_227_173_1_3",
        "preuve_premier_947",
        "gap_m31_17",
        "gap_mix_val",
        "k_spectral",
    ]
    for lemma in key_lemmas:
        assert lemma in banque_content, (
            f"Lemme/axiome '{lemma}' manquant de la banque Q&R"
        )


def test_banque_references_key_numerical_examples(banque_content: str):
    """Exemples numériques clés doivent être présents.
    Normalise le tiret Unicode « minus sign » (U+2212) en tiret ASCII pour
    la recherche (le fichier .md utilise le tiret typographique)."""
    normalized = banque_content.replace("\u2212", "-")
    examples = [
        "13246",   # SB(12) pour reconstruction de 37
        "10878",   # SA(12) + Digamma(37)
        "40895",   # SA(-10) numérateur
        "20480",   # dénominateur commun
        "39280705",  # Digamma(-31)
        "5260628",  # suite_B_1_4_somme
        "1381716",  # digamma_calcule_1_4
        "947",     # premier reconstruit (modèle 1/4)
        "37",      # 12e premier (modèle 1/2)
        "-47",     # écart -31/17
        "-53",     # écart 227/173
        "-738",    # Digamma(17)
    ]
    for ex in examples:
        assert ex in normalized, (
            f"Exemple numérique '{ex}' manquant de la banque Q&R"
        )


def test_banque_excludes_philosophical_content(banque_content: str):
    """Vérifie qu'aucun terme philosophique/ontologique n'a été introduit
    dans la banque (critère strict Philippe)."""
    forbidden = [
        "téléosémantique",
        "teleosemantique",
        "ontologique",
        "onthologique",
        "isossophie",
        "métaphysique",
    ]
    lower = banque_content.lower()
    for term in forbidden:
        # On tolère le mot dans les critères de REJET (au début du doc)
        # mais pas ailleurs. Vérification simple : mention max 1 fois
        # (dans la section critères).
        count = lower.count(term.lower())
        assert count <= 1, (
            f"Terme rejeté '{term}' apparaît {count} fois dans la banque "
            f"(devrait apparaître au max 1 fois dans la section critères de rejet)"
        )


def test_banque_sources_are_spectral_files(banque_content: str):
    """Les sources doivent être des fichiers de la Méthode Spectrale, pas
    d'autres théories (Espace de Philippôt, etc.)."""
    assert "geometry_prime_spectrum.tex" in banque_content
    assert "methode_spectral.thy" in banque_content
    # Fichiers d'AUTRES théories interdits comme source principale
    forbidden_sources = [
        "espace_de_philippot.tex",
        "espace_philippot.thy",
        "mecanique_discret.thy",
        "postulat_carre.thy",
    ]
    # On les tolère uniquement dans la section de critères, pas comme
    # source des Q retenues. On compte les occurrences comme "**Source** : `<fichier>`"
    for fs in forbidden_sources:
        source_line = f"**Source** : `{fs}`"
        assert source_line not in banque_content, (
            f"Fichier interdit '{fs}' utilisé comme source d'une Q&R "
            "(seuls geometry_prime_spectrum.tex et methode_spectral.thy autorisés)"
        )
