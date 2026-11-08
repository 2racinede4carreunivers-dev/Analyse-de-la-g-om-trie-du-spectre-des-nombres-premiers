# -*- coding: utf-8 -*-
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = 'box(r"section 3.6 : table de vérification $k=3$ à $9$")\n\\end{pycode}'
new = old + '''

\\begin{boitehol}{Ancrages k=3 à 9 (MS_14 XIV.6)}
\\begin{holcode}
lemma ancrages_conv:
  "rang_base_k 3 = 49 \\<and> premier_base_k 3 = 227 \\<and>
   rang_base_k 4 = 80 \\<and> premier_base_k 4 = 947 \\<and>
   rang_base_k 5 = 439 \\<and> premier_base_k 5 = 2999 \\<and>
   rang_base_k 6 = 954 \\<and> premier_base_k 6 = 7529 \\<and>
   rang_base_k 7 = 1913 \\<and> premier_base_k 7 = 16519 \\<and>
   rang_base_k 8 = 3468 \\<and> premier_base_k 8 = 32327 \\<and>
   rang_base_k 9 = 5906 \\<and> premier_base_k 9 = 58337"
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Le lemme \\texttt{ancrages\\_conv} de la théorie
Isabelle/HOL \\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.6) catalogue les ancrages
officiels pour $k=3$ à $9$ : $(k, \\text{rang}, P) = (3,49,227), (4,80,947),
(5,439,2999), (6,954,7529), (7,1913,16519), (8,3468,32327), (9,5906,58337)$.
Ces valeurs correspondent exactement au tableau de vérification $k=3$ à $9$ du
document.\\\\
\\holok HOL/Isabelle : ancrages $k=3$ à $9$ validés formellement.\\\\
\\end{boitehol}'''

count = content.count(old)
print(f'Occurrences: {count}')
if count == 1:
    content = content.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Ancrages done')
else:
    print('SKIPPED')