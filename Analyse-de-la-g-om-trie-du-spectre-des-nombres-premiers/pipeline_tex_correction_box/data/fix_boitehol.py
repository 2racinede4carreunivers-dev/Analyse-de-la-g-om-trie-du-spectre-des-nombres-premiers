import re

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all \begin{boitehol}{...} and add color argument
pattern = r'\\begin\{boitehol\}\{([^}]*)\}'
matches = re.findall(pattern, content)
print(f"Found {len(matches)} boitehol calls")
for m in matches:
    print(f"  - {m}")

# Replace: add {spectralbleu} after the title argument
new_content = re.sub(pattern, lambda m: '\\begin{boitehol}{' + m.group(1) + '}{spectralbleu}', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done! All boitehol calls now have a color argument.")