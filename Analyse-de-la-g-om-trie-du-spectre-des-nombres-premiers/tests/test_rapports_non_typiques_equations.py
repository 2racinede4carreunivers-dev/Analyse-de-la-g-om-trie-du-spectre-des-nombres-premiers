"""Tests des équations exactes A/B pour les rapports non-typiques."""
from __future__ import annotations

from fractions import Fraction

import pytest

from src.spectral.rapports_non_typiques import (
    construire_rapport_convolutif,
    construire_suites_reelles,
    equations_ab,
    equations_suites_reelles,
    candidats_reconstruction_reelle,
    reconstruire_equations_ab,
    reconstruire_premier,
    reconstruire_premier_reel_universel,
    suite_A,
    suite_B,
)
from src.core.spectral_core import SpectralMethodCore
from src.engines.generalization.generalizer import Generalizer
from src.multiloop.refinement_loop import RefinementLoop


@pytest.mark.parametrize("k", [3, 4, 5, 6, 7, 11])
@pytest.mark.parametrize("n", [7, 10, 14])
def test_equations_universelles_reproduisent_les_sommes_par_blocs(k: int, n: int) -> None:
    equation_a, equation_b = equations_ab(f"1/{k}")

    assert equation_a.somme(n) == suite_A(k, n)
    assert equation_b.somme(n) == suite_B(k, n)


@pytest.mark.parametrize("k", [3, 5, 6, 11])
def test_reconstruction_deux_sommes_retrouve_equations_exactes(k: int) -> None:
    attendue_a, attendue_b = equations_ab(k)
    reconstruite_a, reconstruite_b = reconstruire_equations_ab(k, 10, 12)

    assert reconstruite_a == attendue_a
    assert reconstruite_b == attendue_b


def test_convolution_geometrique_propage_la_somme_sans_arrondi() -> None:
    equation_a, equation_b = equations_ab("1/5")

    assert equation_a.convoluer(equation_a.somme(10), 10, 14) == suite_A(5, 14)
    assert equation_b.convoluer(equation_b.somme(10), 10, 14) == suite_B(5, 14)
    assert isinstance(equation_b.somme(10), Fraction)


def test_rapport_typique_1_2_est_accepte_par_les_equations() -> None:
    # Le régime typique 1/2 est l'instance k=2 du même système convolutif :
    # ses équations exactes (13/8 et 13/4) sont produites sans refus.
    equation_a, equation_b = equations_ab("1/2")

    assert equation_a.coefficient == Fraction(13, 8)
    assert equation_a.constante == Fraction(-2)
    assert equation_b.coefficient == Fraction(13, 4)
    assert equation_b.constante == Fraction(-66)
    assert equation_a.somme(10) == suite_A(2, 10)
    assert equation_b.somme(10) == suite_B(2, 10)


def test_rapport_convolutif_transmet_reference_equations_et_premier() -> None:
    rapport = construire_rapport_convolutif("1/23", 27)

    assert rapport["equation_A"]["forme"] == "A(n) = (279313/267674) * 23^n + (-23/22)"
    assert rapport["equation_B"]["forme"] == "B(n) = (279313/11638) * 23^n + (-3256789581/22)"
    assert rapport["reference_n10"]["somme_A"] == suite_A(23, 10)
    assert rapport["reference_n10"]["somme_B"] == suite_B(23, 10)
    assert rapport["ancrage_n9"]["somme_A"] == suite_A(23, 9)
    assert rapport["ancrage_n9"]["somme_B"] == suite_B(23, 9)
    assert rapport["cible"]["somme_A"] == suite_A(23, 27)
    assert rapport["cible"]["somme_B"] == suite_B(23, 27)
    assert rapport["premier_indetermine"] is False
    assert rapport["cible"]["premier"] == 6424919


def test_ancrage_entier_1_23_position_8_moins() -> None:
    resultat = reconstruire_premier("1/23")

    assert resultat["premier"] == 6424727
    assert resultat["position_du_premier (1-index)"] == 439980


def test_suites_reelles_exposent_les_composantes_ai_bi_pour_toute_longueur() -> None:
    suites = construire_suites_reelles("1/23", n=27)

    assert len(suites["suite_Ai"]) == 27
    assert len(suites["suite_Bi"]) == 27
    assert suites["zeta"]["position"] == 6
    assert suites["suite_Ai"][9]["position"] == 10


def test_equations_reelles_universelles_reconstruisent_les_radicandes_sans_catalogue() -> None:
    equations = equations_suites_reelles("1/23", n=27)

    assert equations["radicande_A"] == (1 + 23**2) * equations["coefficient_A"] ** 2
    assert equations["radicande_B"] == (1 + 23**2) * equations["coefficient_B"] ** 2
    assert "sqrt(1 + 23^2)" in equations["forme_A"]


def test_reconstruction_reelle_universelle_essaie_toutes_les_branches() -> None:
    candidats = candidats_reconstruction_reelle("1/23", n=10)
    resultat = reconstruire_premier_reel_universel("1/23", n=10)

    assert len(candidats) == 8
    assert resultat["verifie"] is True
    assert resultat["premier"] == 6424727


def test_rapport_typique_transmet_aussi_les_faits_convolutifs_complets() -> None:
    rapport = SpectralMethodCore().rapport_convolutif_typique(27)

    assert rapport["equation_A"]["forme"] == "A(n) = (13/8) * 2^n + (-2)"
    assert rapport["equation_B"]["forme"] == "B(n) = (13/4) * 2^n + (-66)"
    assert rapport["reference_n10"]["n"] == 10
    assert rapport["reference_n10"]["premier"] == 29
    assert rapport["cible"]["n"] == 27
    assert rapport["cible"]["premier"] == 103


def test_resume_convolutif_force_les_ancrages_n10_et_n9() -> None:
    from src.core.pipeline import Pipeline

    rapport = SpectralMethodCore().rapport_convolutif_non_typique("1/50", 16)
    rapport.update({
        "model": "1/50",
        "equation_holds": False,
    })
    resume = Pipeline._append_convolution_summary("Réponse.", rapport)

    assert "Ancrage n=10 : A=99609390943877550, B=4980469531568877550" in resume
    assert "Ancrage n=9 : A=1992187818877550, B=99609375318877550" in resume
    assert "Cible n=16 : A=1556396733498086734693877550" in resume
    assert "Aucun premier n'a pu être déterminé" in resume


def test_prompt_non_typique_transmet_les_faits_convolutifs_sans_regle_1_2() -> None:
    faits = SpectralMethodCore().rapport_convolutif_non_typique("1/27", 19)
    faits.update({"model": "1/27", "premier_indetermine": True})
    general = Generalizer().generalize(faits, {"intent": "reconstruction", "model": "1/27"})

    class Ctx:
        metadata = {}
        raw_question = "Reconstruire le rapport 1/27 pour n=19"

    from src.core.pipeline import Pipeline

    prompt = Pipeline._build_base_prompt(
        Pipeline.__new__(Pipeline), Ctx(), {"model": "1/27"}, general, [], faits
    )
    rendered = RefinementLoop._build_prompt(
        RefinementLoop.__new__(RefinementLoop), Ctx(), faits, prompt, "", 1
    )

    assert "Ne jamais appliquer le modèle 1/2" in prompt
    assert "A(n) =" in rendered
    assert '"reference_n10"' in rendered
    assert '"cible"' in rendered

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
