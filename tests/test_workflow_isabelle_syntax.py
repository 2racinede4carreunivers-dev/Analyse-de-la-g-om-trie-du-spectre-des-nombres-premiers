"""
Tests v3.25 : verifie que les workflows GitHub Actions Isabelle utilisent
la syntaxe CORRECTE.

Bug reporte par Philippe : la commande `isabelle process -T ./theories/xxx.thy`
etait INVALIDE (l'option -T attend un nom de theorie sans extension, ou on
utilise `isabelle build -D .` avec un fichier ROOT). Ceci causait l'erreur
`Malformed theory import`.

Ce test scanne TOUS les workflows .yml et refuse les patterns buggues.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# v3.26 : Detection dynamique de la racine du repo au lieu de Path("/app")
# en dur, qui ne marchait qu'en pod Emergent. Priorite :
#   1. Le parent du dossier tests/ (cas standard, marche partout)
#   2. Un sous-dossier `agent-multiloop-Gabriel-local/` si le repo est nested
#   3. /app pour retro-compatibilite pod Emergent
_TESTS_DIR = Path(__file__).resolve().parent
LOCAL_ROOT = _TESTS_DIR.parent
REPO_ROOT = LOCAL_ROOT.parent if (LOCAL_ROOT.parent / ".git").is_dir() else LOCAL_ROOT


def _workflow_files():
    """Retourne tous les fichiers .yml dans .github/workflows/ des 2 racines."""
    files = []
    for base in (REPO_ROOT, LOCAL_ROOT):
        wf_dir = base / ".github" / "workflows"
        if wf_dir.exists():
            files.extend(sorted(wf_dir.glob("*.yml")))
    return files


class TestNoInvalidIsabelleCommand:
    """Regression : le pattern `isabelle process -T ./PATH.thy` est INVALIDE
    et cause 'Malformed theory import'. Il ne doit apparaitre dans AUCUN
    workflow YAML."""

    @pytest.mark.parametrize("wf", _workflow_files(), ids=str)
    def test_no_process_dash_T_with_dotthy_path(self, wf):
        content = wf.read_text(encoding="utf-8")
        # Pattern buggue : "process -T " suivi d'un chemin se terminant par ".thy"
        import re
        bad = re.findall(r"isabelle\s+process\s+-T\s+\S+\.thy", content)
        assert not bad, (
            f"Workflow {wf} contient la commande INVALIDE : {bad}. "
            f"Utiliser `isabelle build -D .` avec un fichier ROOT a la place."
        )

    @pytest.mark.parametrize("wf", _workflow_files(), ids=str)
    def test_no_relative_path_prefix_theory_arg(self, wf):
        """Pattern `-T ./xxx` ou `-T ./theories/xxx.thy` est aussi mauvais."""
        content = wf.read_text(encoding="utf-8")
        import re
        # Chercher `-T ./` suivi d'un chemin (n'importe quelle option Isabelle)
        bad = re.findall(r"isabelle\s+\S+\s+-T\s+\./\S+", content)
        assert not bad, (
            f"Workflow {wf} passe un chemin relatif `./...` a `-T`. "
            f"L'option `-T` attend un nom de theorie (sans extension)."
        )


class TestRootFileExists:
    """Le fichier ROOT Isabelle doit exister pour permettre `isabelle build -D .`."""

    def test_theories_ROOT_exists(self):
        root = LOCAL_ROOT / "theories" / "ROOT"
        assert root.exists(), (
            "Le fichier `theories/ROOT` doit exister pour declarer la session "
            "Isabelle 'Methode_Spectral'."
        )

    def test_ROOT_declares_methode_spectral_session(self):
        root = LOCAL_ROOT / "theories" / "ROOT"
        content = root.read_text(encoding="utf-8")
        # v3.32 : la session peut etre declaree avec ou sans guillemets
        # (syntaxe Isabelle valide dans les deux cas).
        assert (
            "session \"Methode_Spectral\"" in content
            or "session Methode_Spectral" in content
        )
        assert "methode_spectral" in content
        assert "HOL-Computational_Algebra" in content


class TestBuildWorkflowUsesIsabelleBuild:
    """Le workflow doit utiliser `isabelle build -D .` (pas `process -T`)."""

    def test_root_build_yml_uses_isabelle_build(self):
        build = REPO_ROOT / ".github" / "workflows" / "build.yml"
        if not build.exists():
            pytest.skip(f"{build} n'existe pas")
        content = build.read_text(encoding="utf-8")
        assert "isabelle build" in content, (
            "Le workflow doit utiliser `isabelle build -D .` "
            "(commande standard pour compiler une session Isabelle)."
        )

    def test_paths_point_to_correct_theories(self):
        """Verifie que les chemins pointent bien vers
        agent-multiloop-Gabriel-local/theories/methode_spectral.thy
        (et non l'ancien src/hol/ inexistant)."""
        build = REPO_ROOT / ".github" / "workflows" / "build.yml"
        if not build.exists():
            pytest.skip(f"{build} n'existe pas")
        content = build.read_text(encoding="utf-8")
        # L'ancien chemin src/hol/ ne doit plus apparaitre
        assert "src/hol/methode_spectral.thy" not in content, (
            "Le workflow reference encore l'ancien chemin `src/hol/...` "
            "qui n'existe pas. Corriger vers "
            "`agent-multiloop-Gabriel-local/theories/methode_spectral.thy`."
        )


class TestGithubReleaseInstallation:
    """v3.35 (fix Philippe 2026-02) : le workflow telecharge Isabelle 2025-2
    via une strategie multi-miroirs robuste (Cambridge en tete + fallback
    SourceForge). L'ancienne strategie via `github.com/isabelle-prover/...`
    n'existait pas (URL fictive) et provoquait les 15 echecs consecutifs
    sur le depot public."""

    @pytest.fixture(scope="class")
    def build_content(self):
        build = REPO_ROOT / ".github" / "workflows" / "build.yml"
        if not build.exists():
            pytest.skip(f"{build} n'existe pas")
        return build.read_text(encoding="utf-8")

    def test_multi_mirror_strategy(self, build_content):
        """Le workflow doit lister plusieurs miroirs Isabelle."""
        # Cambridge (le nouveau miroir en tete de liste)
        assert "www.cl.cam.ac.uk/research/hvg/Isabelle/dist" in build_content, (
            "Le workflow doit lister le miroir Cambridge (le plus stable "
            "pour les IP GitHub Actions)."
        )
        # SourceForge en fallback ultime
        assert "sourceforge.net/projects/isabelle" in build_content, (
            "Le workflow doit avoir SourceForge en fallback."
        )

    def test_isabelle_2025_2_version(self, build_content):
        """v3.35 : Isabelle 2025-2 est la version confirmee par la
        compilation locale de Philippe (Cygwin, 2026-02, 1:35 elapsed)."""
        assert "Isabelle2025-2" in build_content
        assert "Isabelle2025-2_linux.tar.gz" in build_content

    def test_isabelle_version_verified_after_install(self, build_content):
        """L'installation se termine par `isabelle version` (sanity check)."""
        assert "isabelle version" in build_content

    def test_path_registered(self, build_content):
        """Le binaire Isabelle doit etre ajoute au GITHUB_PATH."""
        assert "GITHUB_PATH" in build_content

    def test_no_removal_of_referenced_components(self, build_content):
        """CRITIQUE : ne PAS supprimer les composants references dans
        etc/build.props ou etc/settings d'Isabelle.
        Bugs reportes :
        - 2026-07-10 (a) : contrib/z3-* + src/Tools/jEdit/ -> 'Missing component'
        - 2026-07-10 (b) : contrib/isabelle_fonts-* -> 'Undefined ISABELLE_FONTS'
        """
        forbidden_removals = [
            r"rm\s+-rf\s+.*contrib/z3-",
            r"rm\s+-rf\s+.*contrib/cvc",
            r"rm\s+-rf\s+.*contrib/jedit_build",
            r"rm\s+-rf\s+.*contrib/jortho",
            r"rm\s+-rf\s+.*contrib/isabelle_fonts-",  # AJOUTE (bug 2026-07-10b)
            r"rm\s+-rf\s+.*src/Tools/jEdit",
        ]
        import re
        for pat in forbidden_removals:
            assert not re.search(pat, build_content), (
                f"Suppression interdite detectee : pattern `{pat}` "
                f"est reference dans Isabelle (build.props/settings/env)."
            )


class TestProvenanceAttestation:
    """v3.32 : le workflow certifie la provenance de methode_spectral.thy
    via actions/attest (attestation signee GitHub)."""

    @pytest.fixture(scope="class")
    def build_content(self):
        build = REPO_ROOT / ".github" / "workflows" / "build.yml"
        if not build.exists():
            pytest.skip(f"{build} n'existe pas")
        return build.read_text(encoding="utf-8")

    def test_attest_action_present(self, build_content):
        # v3.35 : `actions/attest@v2` a ete remplace par
        # `actions/attest-build-provenance@v1`, l'action officielle
        # GitHub pour la provenance SLSA (recommandation actuelle).
        assert (
            "actions/attest-build-provenance@" in build_content
            or "actions/attest@" in build_content
        ), (
            "Le workflow doit generer une attestation de provenance signee "
            "(actions/attest-build-provenance ou actions/attest)."
        )

    def test_attestation_permissions(self, build_content):
        """Les permissions id-token + attestations sont requises par attest."""
        assert "id-token: write" in build_content
        assert "attestations: write" in build_content

    def test_attestation_subject_is_thy_file(self, build_content):
        assert "theories/methode_spectral.thy" in build_content

    def test_author_credited(self, build_content):
        assert "Philippe Thomas Savard" in build_content

    def test_artifact_uploaded(self, build_content):
        assert "actions/upload-artifact@" in build_content


class TestBuildStep:
    """v3.32 : la compilation utilise `isabelle build -v -D .` depuis le
    dossier agent-multiloop-Gabriel-local (ou se trouve le ROOT)."""

    @pytest.fixture(scope="class")
    def build_content(self):
        build = REPO_ROOT / ".github" / "workflows" / "build.yml"
        if not build.exists():
            pytest.skip(f"{build} n'existe pas")
        return build.read_text(encoding="utf-8")

    def test_build_command(self, build_content):
        assert "isabelle build" in build_content

    def test_working_directory_correct(self, build_content):
        assert "agent-multiloop-Gabriel-local" in build_content

    def test_polyml_and_jdk_preserved(self, build_content):
        """CRITIQUE : polyml (moteur ML) et jdk (JVM) NE doivent PAS
        etre supprimes — Isabelle en depend imperativement."""
        import re
        assert not re.search(r"rm\s+-rf\s+.*polyml-", build_content), (
            "polyml est requis par Isabelle. Ne JAMAIS le supprimer."
        )
        assert not re.search(r"rm\s+-rf\s+.*jdk-", build_content), (
            "jdk est requis par Isabelle (JVM). Ne JAMAIS le supprimer."
        )
