"""Contrat statique complet du workflow Isabelle 2025-2."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".github" / "workflows" / "build.yml"
CONTENT = BUILD.read_text(encoding="utf-8")


def test_workflow_isabelle_2025_2_contract():
    """Vérifie les chemins, la session et l'archive propres à ce dépôt."""
    assert "Isabelle2025-2" in CONTENT
    assert "Isabelle2025-2_linux.tar.gz" in CONTENT
    assert "a20a507bc7c1270d8be96a9f3fbec06345387789d2dc2c4d3df6260d47bfb33c" in CONTENT
    assert "1228480874" in CONTENT
    assert "isabelle.in.tum.de/website-Isabelle2025-2/dist" in CONTENT
    assert "isabelle.in.tum.de/dist/" in CONTENT
    assert "--retry-all-errors" in CONTENT
    assert 'echo "/tmp/isabelle/${ISABELLE_VERSION}/bin" >> "$GITHUB_PATH"' in CONTENT
    assert 'isabelle build -d . -v "${SESSION_NAME}"' in CONTENT
    assert "SESSION_NAME: Geometrie_Spectre_Premier_Philippe_Thomas_Savard" in CONTENT
    assert "working-directory: theories" in CONTENT
    assert "Document-pdf-tex/${DOCUMENT_TEX}" in CONTENT
    assert "reassemble_parts.py" in CONTENT
    assert "sha256sum --check SHA256SUMS_build.txt" in CONTENT
    assert "uses: actions/upload-artifact@v4" in CONTENT
    assert "uses: actions/attest-build-provenance@v2" in CONTENT

    for permission in ("contents: read", "id-token: write", "attestations: write"):
        assert permission in CONTENT
