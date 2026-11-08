# -*- coding: utf-8 -*-
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '\\SB(k,n) = \\frac{\\alpha_B(k)}{2}\\cdot k^{n} - \\delta_B(k).\n\\]\n\\end{boiteformule}'
new = old + '''

\\begin{boitehol}{Formules fermées des sommes (MS_14 XIV.2)}
\\begin{holcode}
subsection "XIV.2 — Formules fermées générales"

definition somme_A_conv :: "nat => nat => real" where
  "somme_A_conv k n = (alphaA_conv k / 2) * (real k) ^ n - offsetA_conv k"

definition somme_B_conv :: "nat => nat => real" where
  "somme_B_conv k n = (alphaB_conv k / 2) * (real k) ^ n - offsetB_conv k"

lemma somme_A_conv_k2_eq_SA :
  "somme_A_conv 2 n = SA n"
  unfolding somme_A_conv_def alphaA_conv_def offsetA_conv_def SA_def
  by (simp add: field_simps)

lemma somme_B_conv_k2_eq_SB :
  "somme_B_conv 2 n = SB n"
  unfolding somme_B_conv_def alphaB_conv_def alphaA_conv_def offsetB_conv_def SB_def
  by (simp add: field_simps)
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Les définitions \\texttt{somme\\_A\\_conv} et
\\texttt{somme\\_B\\_conv} de la théorie Isabelle/HOL
\\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.2) généralisent les suites historiques
$SA$ ($k=2$) et $SB$ ($k=2$) à tout rapport $1/k$. Les lemmes de compatibilité
prouvent que pour $k=2$, on retrouve exactement $SA$ et $SB$.\\\\
\\holok HOL/Isabelle : formules fermées validées formellement.\\\\
\\end{boitehol}'''

count = content.count(old)
print(f'Occurrences: {count}')
if count == 1:
    content = content.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Niveau2 done')
else:
    print('SKIPPED')