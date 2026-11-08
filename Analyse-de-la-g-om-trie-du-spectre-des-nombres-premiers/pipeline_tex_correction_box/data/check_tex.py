# -*- coding: utf-8 -*-
path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

hol_count = content.count('boitehol')
print(f'Nombre de boîtes boitehol: {hol_count}')
holcode_count = content.count('holcode')
print(f'Nombre de environnements holcode: {holcode_count}')
print(f'Ouvertures begin{{document}}: {content.count("begin{document}")}')
print(f'Fermetures end{{document}}: {content.count("end{document}")}')
print(f'Taille du fichier: {len(content)} caractères')