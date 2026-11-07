import sys
sys.path.insert(0, r'C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers')

from src.spectral.rapports_non_typiques import niveau_1_entier

# Get digamma values for 1/27, n=16
result = niveau_1_entier(27, 16)
print('Digamma values for 1/27, n=16:')
print('=' * 60)
for i, poss in enumerate(result['possibilites']):
    print(f'{i+1}. {poss["branche"]}:')
    print(f'   Digamma: {poss["digamma"]}')
    print(f'   C (candidat): {poss["C"]}')
    print(f'   Premier: {poss["premier"]} ({"OUI" if poss["entier"] and poss["premier"] else "NON"})')
    print(f'   Verdict: {poss["verdict"]}')
    print()
    