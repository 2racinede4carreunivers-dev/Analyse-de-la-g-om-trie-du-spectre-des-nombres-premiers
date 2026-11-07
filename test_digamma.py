import sys
sys.path.insert(0, r"C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from src.spectral.rapports_non_typiques import reconstruire_premier

# Test for ratio 1/27, n=16
result = reconstruire_premier("1/27", n=16)
print("Result for 1/27, n=16:")
for k, v in result.items():
    print(f"  {k}: {v}")

# Also test for n=10 to compare
result10 = reconstruire_premier("1/27", n=10)
print("\nResult for 1/27, n=10:")
for k, v in result10.items():
    print(f"  {k}: {v}")