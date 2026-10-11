#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de validation Gabriel - Rapports 1/14 et 1/9"""

import sys
sys.path.insert(0, '/home/agent/app')

from src.core.spectral_core import SpectralMethodCore
from src.core.zeta_denominator_core import calculer_zeta_denominator

def test_rapport(rapport: str, n: int):
    """Test une reconstruction pour un rapport et n donnés"""
    core = SpectralMethodCore()
    
    print(f"\n{'='*70}")
    print(f"TEST: Reconstruction {rapport} n={n}")
    print(f"{'='*70}")
    
    result = core.rapport_convolutif_non_typique(rapport, n=n)
    
    print(f"Rapport: {result.get('rapport')}")
    print(f"Premier indéterminé: {result.get('premier_indetermine')}")
    
    if 'cible' in result:
        cible = result['cible']
        print(f"\nCible (n={n}):")
        print(f"  Somme A: {cible.get('somme_A')}")
        print(f"  Somme B: {cible.get('somme_B')}")
        print(f"  Digamma calculé: {cible.get('digamma_calcule')}")
        print(f"  Premier: {cible.get('premier')}")
        
        # Vérifier que k^6 a été utilisé (pas 64)
        zeta = calculer_zeta_denominator(rapport)
        if cible.get('somme_B') and cible.get('digamma_calcule') and cible.get('premier'):
            try:
                p_test = (cible['somme_B'] - cible['digamma_calcule']) // zeta
                print(f"\n  Formule P = (SB - Digamma) / k^6:")
                print(f"  ({cible['somme_B']} - {cible['digamma_calcule']}) / {zeta} = {p_test}")
                if p_test == cible.get('premier'):
                    print(f"  ✓ CORRECT: P = {p_test}")
                    return True
                else:
                    print(f"  ✗ ERREUR: P calculé={p_test}, premier={cible.get('premier')}")
                    return False
            except Exception as e:
                print(f"  Calcul: {e}")
    return result.get('premier') is not None


if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTS DE VALIDATION GABRIEL — Correction Zêta k^6")
    print("="*70)
    
    results = {}
    results["1/14 n=15"] = test_rapport("1/14", n=15)
    results["1/9 n=34"] = test_rapport("1/9", n=34)
    results["1/3 n=9"] = test_rapport("1/3", n=9)
    
    print(f"\n{'='*70}")
    print("RÉSUMÉ")
    print(f"{'='*70}")
    for test_name, passed in results.items():
        status = "✓ RÉUSSI" if passed else "✗ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    if all(results.values()):
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        sys.exit(0)
    else:
        print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
        sys.exit(1)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
