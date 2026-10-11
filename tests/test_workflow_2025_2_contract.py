"""Contrat statique complet du workflow Isabelle 2025-2."""
from pathlib import Path
import re


BUILD = Path("/home/agent/app/.github/workflows/build.yml")
CONTENT = BUILD.read_text(encoding="utf-8")


def test_workflow_isabelle_2025_2_contract():
    """Vérifie exactement les propriétés demandées pour le correctif du 404."""
    assert "github.com/isabelle-prover/isabelle/releases/download" not in CONTENT
    assert "Isabelle2025-2" in CONTENT
    assert "Isabelle2025-2_linux.tar.gz" in CONTENT

    cambridge = CONTENT.index("www.cl.cam.ac.uk/research/hvg/Isabelle/dist")
    sourceforge = CONTENT.index("sourceforge.net/projects/isabelle")
    assert cambridge < sourceforge

    assert 'echo "/tmp/isabelle/Isabelle2025-2/bin" >> "$GITHUB_PATH"' in CONTENT
    assert "/tmp/isabelle/Isabelle2025-2/bin/isabelle version" in CONTENT

    forbidden = (
        r"rm\s+-rf\s+.*contrib/z3-",
        r"rm\s+-rf\s+.*contrib/cvc",
        r"rm\s+-rf\s+.*contrib/jedit_build",
        r"rm\s+-rf\s+.*contrib/jortho",
        r"rm\s+-rf\s+.*contrib/isabelle_fonts-",
        r"rm\s+-rf\s+.*src/Tools/jEdit",
    )
    assert not any(re.search(pattern, CONTENT) for pattern in forbidden)

    assert "working-directory: agent-multiloop-Gabriel-local" in CONTENT
    assert "isabelle build -v -D ." in CONTENT
    assert not re.search(r"isabelle\s+process\s+-T", CONTENT)

    assert (
        "uses: actions/attest-build-provenance@v1" in CONTENT
        or "uses: actions/attest@" in CONTENT
    )
    assert "subject-path: agent-multiloop-Gabriel-local/theories/methode_spectral.thy" in CONTENT
    assert "uses: actions/upload-artifact@v4" in CONTENT
    assert "name: methode-spectral-attestation-payload" in CONTENT

    for permission in ("contents: read", "id-token: write", "attestations: write"):
        assert permission in CONTENT
