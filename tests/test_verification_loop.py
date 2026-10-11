"""
Tests pour AutomaticVerificationLoop (Wolfram <-> Gabriel <-> Isabelle).

Comme Isabelle reel et Wolfram ne sont pas presents en environnement de test,
on utilise :
  - Le mode "skipped" de IsabelleAdapter (Isabelle absent -> check syntaxique local)
  - Un WolframClient sans AppID -> etape ignoree resiliente
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.adapters.hol_isabelle.isabelle_adapter import IsabelleAdapter
from src.adapters.wolfram.wolfram_client import WolframClient
from src.audit import AuditStore
from src.multiloop.verification_loop import (
    AutomaticVerificationLoop, VerificationLoopResult, PROOF_TACTICS,
)


@pytest.fixture
def tmp_theories(tmp_path: Path) -> Path:
    d = tmp_path / "theories"
    d.mkdir()
    return d


@pytest.fixture
def loop_with_store(tmp_path: Path, tmp_theories: Path) -> AutomaticVerificationLoop:
    config = {"isabelle": {"theory_dir": str(tmp_theories), "enabled": True}}
    isa = IsabelleAdapter(config)
    # Force WolframClient sans AppID (mode resilient)
    wc = WolframClient(app_id="")
    store = AuditStore(base_dir=tmp_path / "audits")
    return AutomaticVerificationLoop(
        config=config,
        isabelle_adapter=isa,
        wolfram_client=wc,
        audit_store=store,
    )


# ============================================================
# verify() : flux complet
# ============================================================

@pytest.mark.asyncio
async def test_verify_position_26_full_loop(loop_with_store: AutomaticVerificationLoop):
    """
    Position 26 : la boucle complete doit s'executer avec :
    - Wolfram : skipped (pas d'AppID)
    - Gabriel : OK (identite locale)
    - Isabelle : mode mock (Isabelle non installe) -> syntax check OK
    """
    result = await loop_with_store.verify(26, ratio="1/2")
    assert isinstance(result, VerificationLoopResult)
    assert result.position == 26
    assert result.prime == 101
    assert result.ratio == "1/2"
    # Wolfram : skipped mais success=True (resilient)
    assert result.wolfram.success is True
    assert result.wolfram.data.get("skipped") is True
    # Gabriel : OK
    assert result.gabriel.success is True
    assert result.gabriel.data["P_reconstruit"] == pytest.approx(101)
    # Isabelle : mock mais syntax OK
    assert result.isabelle.success is True
    assert result.isabelle.data.get("mock") is True
    # .thy ecrit dans tmp_theories
    assert result.thy_path is not None
    assert Path(result.thy_path).exists()
    # Audit cree
    assert result.audit_id is not None


@pytest.mark.asyncio
async def test_verify_thy_contains_expected_lemmas(loop_with_store: AutomaticVerificationLoop):
    result = await loop_with_store.verify(5, ratio="1/2")
    content = result.thy_content
    # Doit contenir les 4 lemmes generes
    assert "SA_n_5_valeur" in content
    assert "SB_n_5_valeur" in content
    assert "digamma_calc_n_5_p_11" in content
    assert "prime_equation_11_n_5" in content
    # Doit utiliser la 1re tactique (simp) par defaut
    assert "by simp" in content
    # Doit terminer par end
    assert content.rstrip().endswith("end")


@pytest.mark.asyncio
async def test_verify_rejects_unsupported_ratio(loop_with_store: AutomaticVerificationLoop):
    with pytest.raises(ValueError):
        await loop_with_store.verify(26, ratio="1/3")


@pytest.mark.asyncio
async def test_verify_rejects_position_out_of_range(loop_with_store: AutomaticVerificationLoop):
    with pytest.raises(ValueError):
        await loop_with_store.verify(99999, ratio="1/2")


@pytest.mark.asyncio
async def test_verify_creates_audit_in_store(loop_with_store: AutomaticVerificationLoop):
    result = await loop_with_store.verify(26, ratio="1/2")
    audit_id = result.audit_id
    assert audit_id is not None
    rec = loop_with_store.audit_store.get(audit_id)
    assert rec is not None
    assert rec.intervention_type == "verification_loop"
    assert rec.position == 26
    assert rec.prime_value == 101
    # toolkit_reports doit contenir wolfram, gabriel, isabelle
    assert "wolfram" in rec.toolkit_reports
    assert "gabriel_spectral_core" in rec.toolkit_reports
    assert "isabelle" in rec.toolkit_reports
    # Verification de la signature
    assert loop_with_store.audit_store.verify(rec) is True


# ============================================================
# Helpers : generation .thy + analyse erreurs
# ============================================================

def test_generate_thy_structure():
    """Le .thy genere doit avoir une structure valide."""
    thy = AutomaticVerificationLoop._generate_thy(
        theory_name="test_42_p_181", n=42, p=181,
        SA_val=14267403262, SB_val=28534806463,
        digamma_val=28534806463 - 64*181, tactic="auto",
    )
    assert "theory test_42_p_181" in thy
    assert "imports methode_spectral" in thy
    assert "by auto" in thy
    assert thy.rstrip().endswith("end")


def test_local_syntax_check_valid():
    valid = """theory T imports methode_spectral begin
lemma L1: "True" by simp
end
"""
    ok, msg = AutomaticVerificationLoop._local_syntax_check(valid)
    assert ok, f"Devrait passer mais : {msg}"


def test_local_syntax_check_missing_end():
    invalid = """theory T imports methode_spectral begin
lemma L1: "True" by simp
"""
    ok, msg = AutomaticVerificationLoop._local_syntax_check(invalid)
    assert not ok
    assert "end" in msg


def test_local_syntax_check_missing_imports():
    invalid = """theory T begin
lemma L1: "True" by simp
end
"""
    ok, msg = AutomaticVerificationLoop._local_syntax_check(invalid)
    assert not ok
    assert "imports" in msg


def test_analyze_errors_extracts_markers():
    stderr = """
    Loading theory ...
    *** Failed to finish proof
    *** lemma SA_n_26 incomplete
    *** at command "by"
    Done.
    """
    msg = AutomaticVerificationLoop._analyze_errors(stderr)
    assert "Failed to finish proof" in msg


def test_analyze_errors_empty():
    msg = AutomaticVerificationLoop._analyze_errors("")
    assert "vide" in msg.lower()


def test_proof_tactics_ordered():
    """Les tactiques doivent etre ordonnees du moins agressif au plus."""
    assert PROOF_TACTICS[0] == "simp"
    assert "auto" in PROOF_TACTICS
    assert "force" in PROOF_TACTICS
