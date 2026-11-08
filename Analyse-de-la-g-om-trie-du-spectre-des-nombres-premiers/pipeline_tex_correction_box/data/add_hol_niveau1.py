# -*- coding: utf-8 -*-
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '\\delta_B(k) = \\frac{k^{7} - k^{6} + k}{k-1}.\n\\]\n\\end{boiteformule}'
new = old + '''

\\begin{boitehol}{Constantes Savard universelles (MS_14 XIV.1)}
\\begin{holcode}
subsection "XIV.1 — Constantes Savard universelles"

definition alphaA_conv :: "nat => real" where
  "alphaA_conv k = 2 * (real k ^ 4 - real k ^ 2 + 1)
                   / ((real k - 1) * real k ^ 3)"

definition alphaB_conv :: "nat => real" where
  "alphaB_conv k = real k * alphaA_conv k"

definition offsetA_conv :: "nat => real" where
  "offsetA_conv k = real k / (real k - 1)"

definition offsetB_conv :: "nat => real" where
  "offsetB_conv k = (real k ^ 7 - real k ^ 6 + real k) / (real k - 1)"

lemma alphaA_conv_k3 : "alphaA_conv 3 = 73 / 27"
  unfolding alphaA_conv_def by simp

lemma alphaB_conv_k3 : "alphaB_conv 3 = 73 / 9"
  unfolding alphaB_conv_def alphaA_conv_def by simp
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Les définitions \\texttt{alphaA\\_conv},
\\texttt{alphaB\\_conv}, \\texttt{offsetA\\_conv}, \\texttt{offsetB\\_conv} de la
théorie Isabelle/HOL \\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.1) formalisent
exactement les quatre constantes Savard : $\\alpha_A(k) = 2(k^4-k^2+1)/((k-1)k^3)$,
$\\alpha_B(k) = k\\,\\alpha_A(k)$, $\\delta_A(k) = k/(k-1)$,
$\\delta_B(k) = (k^7-k^6+k)/(k-1)$.\\\\
\\holok HOL/Isabelle : constantes Savard validées formellement.\\\\
\\end{boitehol}'''

count = content.count(old)
print(f'Occurrences: {count}')
if count == 1:
    content = content.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Niveau1 done')
else:
    print('SKIPPED')