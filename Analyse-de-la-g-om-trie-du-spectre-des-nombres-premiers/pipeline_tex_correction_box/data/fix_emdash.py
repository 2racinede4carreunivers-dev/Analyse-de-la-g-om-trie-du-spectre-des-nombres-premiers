path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace em-dash in boitehol titles with LaTeX ---
import re
content = re.sub(r'(\\begin\{boitehol\}\{[^}]*?)—([^}]*\})', lambda m: m.group(1) + '---' + m.group(2), content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")