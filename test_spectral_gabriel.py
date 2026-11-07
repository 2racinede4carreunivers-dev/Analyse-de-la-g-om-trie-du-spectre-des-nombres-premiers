#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST_SPECTRAL_GABRIEL.py - Tests unitaires pour Gabriel spectral

Teste:
1. Reconstruction du 56ième premier (position=56, n=56, 56 termes)
2. Validation du mapping n=position=termes
3. Anti-hallucination validator
4. Integration avec pipeline
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Import le module spectral_core
sys.path.insert(0, str(Path(__file__).parent / "src" / "core"))
from spectral_core import SpectralMethodCore, AntiHallucinationValidator, SpectralRatio


def test_56th_prime():
    """Test: Reconstruire le 56ième nombre premier"""
    print("\n" + "="*80)
    print("TEST 1: Reconstruction du 56ieme nombre premier")
    print("="*80)
    
    core = SpectralMethodCore()
    
    # Le 56ième nombre premier devrait être 263
    data = core.reconstruct_prime_1_2(56)
    
    assert data is not None, "Failed to reconstruct prime at position 56"
    assert data.position == 56, f"Position should be 56, got {data.position}"
    assert data.num_terms == 56, f"Num terms should be 56, got {data.num_terms}"
    assert data.prime_value == 263, f"Prime should be 263, got {data.prime_value}"
    assert data.validated == True, f"Reconstruction should be validated"
    
    print(f"[OK] Position: {data.position}")
    print(f"[OK] Number of terms in A and B: {data.num_terms}")
    print(f"[OK] Prime value: {data.prime_value}")
    print(f"[OK] SA({data.position}) = {data.SA_sum:.1f}")
    print(f"[OK] SB({data.position}) = {data.SB_sum:.1f}")
    print(f"[OK] Validated: {data.validated}")
    print("\n[PASS] TEST 1 PASSED")


def test_invariant():
    """Test: Vérifier que position = n = num_termes"""
    print("\n" + "="*80)
    print("TEST 2: INVARIANT - position = n = num_termes")
    print("="*80)
    
    core = SpectralMethodCore()
    
    # Tester plusieurs positions
    positions = [5, 10, 20, 30, 50, 56]
    
    for pos in positions:
        data = core.reconstruct_prime_1_2(pos)
        assert data is not None, f"Failed for position {pos}"
        assert data.position == pos, f"Position mismatch for {pos}"
        assert data.num_terms == pos, f"Num terms != position for {pos}"
        print(f"[OK] Position {pos:2d}: n={data.position:2d}, terms={data.num_terms:2d}, prime={data.prime_value:3d}")
    
    print("\n[PASS] TEST 2 PASSED: INVARIANT VERIFIED")


def test_anti_hallucination():
    """Test: Anti-hallucination validator"""
    print("\n" + "="*80)
    print("TEST 3: Anti-hallucination Validator")
    print("="*80)
    
    validator = AntiHallucinationValidator()
    
    # Test 1: Hallucinated answer (says n=6 instead of n=56)
    question = "Reconstruct the 56th prime with suites A and B"
    hallucinated = "To solve this, we need 6 terms in suites A and B"
    
    is_valid, msg = validator.validate_answer(question, hallucinated)
    print(f"\nHallucinated answer: '{hallucinated}'")
    print(f"Validation: {is_valid}")
    print(f"Message: {msg}")
    assert not is_valid, "Should detect hallucination"
    
    # Test 2: Correct answer (mentions position 56)
    correct = "The 56th prime is 263 with 56 terms in suites A and B"
    is_valid, msg = validator.validate_answer(question, correct)
    print(f"\nCorrect answer: '{correct}'")
    print(f"Validation: {is_valid}")
    print(f"Message: {msg}")
    
    print("\n[PASS] TEST 3 PASSED")


def test_spectral_ratio():
    """Test: Validate spectral ratio = 1/2"""
    print("\n" + "="*80)
    print("TEST 4: Spectral Ratio Validation (1/2)")
    print("="*80)
    
    core = SpectralMethodCore()
    
    # Test ratio between positions 10 and 11
    is_valid, ratio = core.validate_ratio(10, 11, SpectralRatio.RATIO_1_2)
    print(f"\nRatio between position 10 and 11:")
    print(f"  Computed: {ratio:.6f}")
    print(f"  Expected: {SpectralRatio.RATIO_1_2.value:.6f}")
    print(f"  Valid: {is_valid}")
    assert is_valid, "Ratio should be 1/2"
    
    print("\n[PASS] TEST 4 PASSED")


def test_explanation():
    """Test: Generate explanation for position 56"""
    print("\n" + "="*80)
    print("TEST 5: Full Explanation for Position 56")
    print("="*80)
    
    core = SpectralMethodCore()
    explanation = core.explain_reconstruction(56)
    print(explanation)
    
    # Verify key elements are present
    assert "56" in explanation, "Should mention position 56"
    assert "263" in explanation, "Should mention prime 263"
    assert "INVARIANT" in explanation, "Should mention invariant"
    
    print("\n[PASS] TEST 5 PASSED")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("TESTING GABRIEL SPECTRAL CORE")
    print("="*80)
    
    try:
        test_56th_prime()
        test_invariant()
        test_anti_hallucination()
        test_spectral_ratio()
        test_explanation()
        
        print("\n" + "="*80)
        print("[SUCCESS] ALL TESTS PASSED")
        print("="*80)
        print("\nGabriel is ready with strict spectral understanding!")
        print("Invariant: position = n = num_termes (NO EXCEPTIONS)")
        return 0
        
    except AssertionError as e:
        print(f"\n[FAILED] TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
