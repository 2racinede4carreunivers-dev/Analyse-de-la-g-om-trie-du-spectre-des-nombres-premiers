path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix duplicated color argument
content = content.replace('{spectralbleu}{spectralbleu}', '{spectralbleu}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed duplicated spectralbleu")