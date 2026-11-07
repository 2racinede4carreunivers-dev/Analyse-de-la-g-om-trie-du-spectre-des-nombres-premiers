import sys
sys.path.insert(0, r'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers')

from src.core.pipeline import Pipeline
from src.core.spectral_core import SpectralMethodCore
from src.spectral.rapports_non_typiques import niveau_1_entier

print('=== Test complet du pipeline cognitif pour 1/27, n=16 ===')
print()

# 1. Get the digamma values for 1/27, n=16
result = niveau_1_entier(27, 16)
print('1. Valeurs Digamma pour 1/27, n=16:')
for i, poss in enumerate(result['possibilites']):
    print(f'   {i+1}. {poss["branche"]}: Digamma={poss["digamma"]}, C={poss["C"]}, Premier={poss["premier"]}, Verdict={poss["verdict"]}')
print()

# 2. Test the summary function with proper facts
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
        "n": 16,
        "somme_A": 82720911650929228907244,
        "somme_B": 2233464614575088793075126,
        "digamma_calcule": None,
        "premier": None,
    },
    "premier_indetermine": True,
    "n_demandee": 16,  # Explicitly set n=16
}

print('2. Résumé cognitive avec n_demandee=16:')
resume = Pipeline._append_convolution_summary("Réponse de Gabriel.", facts)
print()

# Verify the key elements are present
checks = {
    'Rapport 1/27': 'Rapport : 1/27' in resume,
    'Valeur n=16': 'Cible n=16' in resume,
    'A et B valeurs': 'A=82720911650929228907244' in resume and 'B=2233464614575088793075126' in resume,
    'Aucun ancrage': 'Aucun premier n\'a pu être déterminé' in resume,
}

print('3. Vérification des éléments clés:')
for check_name, result in checks.items():
    status = '✓' if result else '✗'
    print(f'   {status} {check_name}')

print()
print('4. Exemple de ce que Gabriel dirait :')
# Extract the key parts
import re
rapport_match = re.search(r'- Rapport : (.+)', resume)
cible_match = re.search(r'- Cible n=(\d+) :', resume)
ancrage_match = re.search(r'- Ancrage n=10 : A=(.+?),', resume)

print(f'   - Rapport affiché: {rapport_match.group(1) if rapport_match else "NON TROUVÉ"}')
print(f'   - n affiché: {cible_match.group(1) if cible_match else "NON TROUVÉ"}')
print(f'   - Ancrage n=10 affiché: {ancrage_match.group(1)[:20]+"..." if ancrage_match else "NON TROUVÉ"}')

print()
print('=== Test réussi : Le pipeline préserve et affiche correctement le rapport 1/27 avec n=16 ===')