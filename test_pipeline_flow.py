import sys
sys.path.insert(0, r'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers')

# Check the pipeline flow for non-typical ratios
from src.core.pipeline import Pipeline
from src.core.spectral_core import SpectralMethodCore
from src.spectral.rapports_non_typiques import reconstruire_premier

# Let's trace through what happens when Gabriel processes a request
print('=== Analyse du pipeline cognitif pour 1/27, n=16 ===')
print()

# 1. Check how the pipeline receives the request
core = SpectralMethodCore()

# The rapport_convolutif_non_typique method is patched, let's check what it returns
# for different n values
for n_val in [10, 16, 19]:
    try:
        rapport = core.rapport_convolutif_non_typique('1/27', n=n_val)
        print(f'Rapport for n={n_val}:')
        print(f'  - modèle: {rapport.get("model")}')
        print(f'  - n in rapport: {"n" in rapport}')
        print(f'  - cible n: {rapport.get("cible", {}).get("n", "N/A")}')
        print(f'  - premier_indetermine: {rapport.get("premier_indetermine", False)}')
        print(f'  - digamma_calcule: {rapport.get("digamma_calcule", "N/A")}')
        print()
    except Exception as e:
        print(f'Error for n={n_val}: {e}')
        print()