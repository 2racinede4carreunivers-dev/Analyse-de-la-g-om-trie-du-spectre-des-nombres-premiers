"""
Tests v3.23 : verifie que les 9 nouvelles definitions Section XI de la
validation#16 (Philippe Savard 2026-06-29) sont bien portees en Lean 4
dans theories/MethodeSpectrale.lean.

Correspondance 1:1 avec les nouveaux blocs de methode_spectral.thy :
  raison_spectrale                       -> raison_spectrale
  progression_simple_terme               -> progression_simple_terme
  avant_dernier_terme_savard             -> avant_dernier_terme_savard
  dernier_terme_savard                   -> dernier_terme_savard
  suite_A_savard_construction            -> suite_A_savard_construction
  suite_B_savard_construction            -> suite_B_savard_construction
  somme_A_compacte_savard                -> somme_A_compacte_savard
  somme_B_compacte_savard                -> somme_B_compacte_savard
  rapport_spectral_total_savard          -> rapport_spectral_total_savard
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="module")
def lean() -> str:
    path = ROOT / "theories" / "MethodeSpectrale.lean"
    if not path.is_file():
        pytest.skip(
            f"Fichier {path} introuvable (probablement Docker sans mount "
            "'./theories'). Ce test est optionnel dans ce contexte."
        )
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def thy() -> str:
    path = ROOT / "theories" / "methode_spectral.thy"
    if not path.is_file():
        pytest.skip(
            f"Fichier {path} introuvable (probablement Docker sans mount "
            "'./theories'). Ce test est optionnel dans ce contexte."
        )
    return path.read_text(encoding="utf-8")


# ============================================================================
# 9 nouvelles definitions Section XI Savard (validation#16)
# ============================================================================


class TestNewDefinitionsSavard:
    """Chaque nouvelle definition XI Savard doit exister DANS LES DEUX
    fichiers .thy (Isabelle) ET .lean (Lean 4)."""

    @pytest.mark.parametrize("name", [
        "raison_spectrale",
        "progression_simple_terme",
        "avant_dernier_terme_savard",
        "dernier_terme_savard",
        "suite_A_savard_construction",
        "suite_B_savard_construction",
        "somme_A_compacte_savard",
        "somme_B_compacte_savard",
        "rapport_spectral_total_savard",
    ])
    def test_in_thy(self, thy, name):
        assert f"definition {name}" in thy, (
            f"La definition Savard `{name}` doit exister dans methode_spectral.thy"
        )

    @pytest.mark.parametrize("name", [
        "raison_spectrale",
        "progression_simple_terme",
        "avant_dernier_terme_savard",
        "dernier_terme_savard",
        "suite_A_savard_construction",
        "suite_B_savard_construction",
        "somme_A_compacte_savard",
        "somme_B_compacte_savard",
        "rapport_spectral_total_savard",
    ])
    def test_in_lean(self, lean, name):
        assert f"def {name}" in lean, (
            f"La definition Savard `{name}` doit exister dans MethodeSpectrale.lean"
        )


# ============================================================================
# Theoremes et lemmes cle de validation#16
# ============================================================================


class TestKeyLemmasValidation16:
    """Les theoremes cle de la validation#16 doivent exister dans les 2 fichiers."""

    @pytest.mark.parametrize("name", [
        "preuve_rapport_spectral_limite_savard",
        "validation_constante_A_savard",
        "validation_constante_B_savard",
        "extraction_constante_A",
        "extraction_constante_B",
        "generalisation_ecart_minimal_A",
        "generalisation_ecart_minimal_B",
        "ecart_minimal_universel_A",
        "ecart_minimal_universel_B",
    ])
    def test_in_thy(self, thy, name):
        # Peut etre `theorem` ou `lemma`
        assert (f"theorem {name}" in thy) or (f"lemma {name}" in thy), (
            f"Le lemme/theoreme `{name}` doit exister dans methode_spectral.thy"
        )

    @pytest.mark.parametrize("name", [
        "preuve_rapport_spectral_limite_savard",
        "validation_constante_A_savard",
        "validation_constante_B_savard",
        "extraction_constante_A",
        "extraction_constante_B",
        "generalisation_ecart_minimal_A",
        "generalisation_ecart_minimal_B",
        "ecart_minimal_universel_A",
        "ecart_minimal_universel_B",
    ])
    def test_in_lean(self, lean, name):
        assert (f"theorem {name}" in lean) or (f"lemma {name}" in lean), (
            f"Le lemme/theoreme `{name}` doit exister dans MethodeSpectrale.lean"
        )


# ============================================================================
# Valeurs numeriques brutes (XI.10.b)
# ============================================================================


class TestValeursNumeriques:
    """Les valeurs numeriques brutes valeur_A_10/9, valeur_B_10/9 et
    echelle_stable doivent etre presentes dans les 2 fichiers."""

    @pytest.mark.parametrize("name,value", [
        ("valeur_A_10", "1662"),
        ("valeur_A_9",  "830"),
        ("valeur_B_10", "3262"),
        ("valeur_B_9",  "1598"),
    ])
    def test_valeur_in_thy(self, thy, name, value):
        assert f"definition {name}" in thy
        assert value in thy

    @pytest.mark.parametrize("name,value", [
        ("valeur_A_10", "1662"),
        ("valeur_A_9",  "830"),
        ("valeur_B_10", "3262"),
        ("valeur_B_9",  "1598"),
    ])
    def test_valeur_in_lean(self, lean, name, value):
        assert f"def {name}" in lean
        assert value in lean

    def test_echelle_stable(self, thy, lean):
        assert "echelle_stable" in thy
        assert "echelle_stable" in lean
        # 2^8 = 256, formule geometrique
        assert "2 ^ 8" in thy or "256" in thy
        assert "2 ^ 8" in lean or "256" in lean


# ============================================================================
# Absence de tactiques Lean 4 dans le .thy Isabelle (regression mojibake)
# ============================================================================


class TestNoLeanTacticsInThy:
    """Regression : le fichier .thy ne doit contenir aucune tactique Lean 4."""

    @pytest.mark.parametrize("forbidden", [
        "ring_nf", "norm_num", "by decide",
        "Classical.choose", "Real.rpow", "Nat.Prime",
    ])
    def test_no_lean_tactic(self, thy, forbidden):
        assert forbidden not in thy, (
            f"Tactique Lean 4 interdite `{forbidden}` detectee dans .thy"
        )


# ============================================================================
# Absence de mojibake dans le .thy (regression du fix precedent)
# ============================================================================


class TestNoMojibakeInThy:
    """Regression : le fichier .thy doit etre en UTF-8 propre, sans mojibake."""

    @pytest.mark.parametrize("bad", [
        "â€¹",  # cartouche ouvrant corrompu
        "â€º",  # cartouche fermant corrompu
        "â‰¥",  # >= corrompu
        "â‰¤",  # <= corrompu
        "â‡'",  # => corrompu
        "â„™",  # P majuscule ajouree corrompue
    ])
    def test_no_mojibake_sequence(self, thy, bad):
        assert bad not in thy, (
            f"Sequence mojibake `{bad}` detectee — double-encodage UTF-8"
        )

    def test_no_bom(self, thy):
        assert not thy.startswith("\ufeff"), (
            "Le fichier .thy ne doit pas commencer par un BOM UTF-8"
        )


# ============================================================================
# GitHub Actions build.yml : compilation Lean + attestation SHA256
# ============================================================================


@pytest.fixture(scope="module")
def workflow_yml() -> str:
    path = ROOT / ".github" / "workflows" / "build.yml"
    if not path.is_file():
        pytest.skip(
            f"Fichier {path} introuvable (probablement Docker sans mount "
            "'./.github'). Ajouter au docker-compose.yml :\n"
            "    - ./.github:/home/agent/app/.github:ro"
        )
    return path.read_text(encoding="utf-8")


class TestBuildWorkflow:
    """Le workflow build.yml doit compiler ET Isabelle ET Lean, et generer
    une attestation SHA256 de provenance."""

    def test_has_isabelle_job(self, workflow_yml):
        assert "validation-isabelle:" in workflow_yml
        assert "isabelle build" in workflow_yml

    def test_has_lean_job(self, workflow_yml):
        assert "validation-lean:" in workflow_yml
        assert "lake build MethodeSpectrale" in workflow_yml

    def test_installs_elan(self, workflow_yml):
        assert "elan-init.sh" in workflow_yml or "elan" in workflow_yml.lower()

    def test_computes_sha256_both_files(self, workflow_yml):
        assert "sha256sum theories/methode_spectral.thy" in workflow_yml
        assert "sha256sum theories/MethodeSpectrale.lean" in workflow_yml

    def test_generates_attestation(self, workflow_yml):
        # GitHub attestations
        assert "actions/attest" in workflow_yml
        # Doit couvrir les DEUX fichiers
        assert "theories/methode_spectral.thy" in workflow_yml
        assert "theories/MethodeSpectrale.lean" in workflow_yml

    def test_sha256sums_bundle(self, workflow_yml):
        """Un fichier SHA256SUMS.txt doit etre genere et uploade."""
        assert "SHA256SUMS.txt" in workflow_yml

    def test_upload_artifact(self, workflow_yml):
        assert "actions/upload-artifact" in workflow_yml

    def test_apache_licence_mentioned(self, workflow_yml):
        assert "Apache" in workflow_yml
