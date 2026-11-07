import sys
sys.path.insert(0, r'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers')

from src.core.pipeline import Pipeline

# Test the _append_convolution_summary function with n_demandee=16

# Construct facts as they would be for 1/27, n=16
facts = {
    "model": "1/27",
    "equation_A": {"forme": "A(n) = ...", "coefficient": 1, "constante": 0},
    "equation_B": {"forme": "B(n) = ...", "coefficient": 1, "constante": 0},
    "reference_n10": {
        "somme_A": 213517131900912,
        "somme_B": 5764962173904162,
        "digamma_calcule": None,
        "premier": None,
    },
    "ancrage_n9": {
        "somme_A": 7908041922255,
        "somme_B": 213516744480423,
    },
    "cible": {
        "n": 16,  # This should now be properly reported
        "somme_A": 82720911650929228907244,  # From our earlier calculation
        "somme_B": 2233464614575088793075126,
        "digamma_calcule": None,  # No prime found
        "premier": None,
    },
    "premier_indetermine": True,
    # ADD n_demandee explicitly
    "n_demandee": 16,
}

print("=== Testing summary with n_demandee=16 ===")
resume = Pipeline._append_convolution_summary("Réponse.", facts)
print(resume)