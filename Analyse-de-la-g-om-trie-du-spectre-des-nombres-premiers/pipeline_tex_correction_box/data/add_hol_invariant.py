# -*- coding: utf-8 -*-
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '\\frac{\\SA(k,n_1) - \\SA(k,n_2)}{\\SB(k,n_1) - \\SB(k,n_2)} = \\frac{1}{k}\n\\qquad \\forall\\, n_1 \\neq n_2,\\ k \\ge 2.\n\\]\n\\end{boitenote}'
new = old + '''

\\begin{boitehol}{Invariant spectral 1/k (MS_14 XIV.3)}
\\begin{holcode}
subsection "XIV.3 — Rapport spectral 1/k universel (preuve algébrique)"

definition RsP_conv :: "nat => nat => nat => real" where
  "RsP_conv k n1 n2 =
     (somme_A_conv k n1 - somme_A_conv k n2) /
     (somme_B_conv k n1 - somme_B_conv k n2)"

theorem RsP_conv_constant:
  assumes "k \\<ge> 2" "n1 \\<ge> 1" "n2 \\<ge> 1" "n1 \\<noteq> n2"
  shows "RsP_conv k n1 n2 = 1 / real k"
proof -
  have "somme_A_conv k n1 - somme_A_conv k n2 =
         (alphaA_conv k / 2) * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding somme_A_conv_def by (simp add: field_simps)
  moreover have "somme_B_conv k n1 - somme_B_conv k n2 =
         (alphaB_conv k / 2) * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding somme_B_conv_def by (simp add: field_simps)
  moreover have "alphaB_conv k = real k * alphaA_conv k"
    unfolding alphaB_conv_def by simp
  ultimately show ?thesis
    unfolding RsP_conv_def by (simp add: field_simps)
qed

corollary RsP_conv_k3 :
  assumes "n1 \\<ge> 1" "n2 \\<ge> 1" "n1 \\<noteq> n2"
  shows "RsP_conv 3 n1 n2 = 1 / 3"
  using RsP_conv_constant[of 3 n1 n2] assms by simp
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Le théorème \\texttt{RsP\\_conv\\_constant} de la
théorie Isabelle/HOL \\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.3) prouve
algébriquement que pour tout $k \\ge 2$ et tout $n_1 \\neq n_2$,
$(S_A(k,n_1)-S_A(k,n_2))/(S_B(k,n_1)-S_B(k,n_2)) = 1/k$. Le corollaire
\\texttt{RsP\\_conv\\_k3} instancie ce résultat pour le rapport $1/3$.\\\\
\\holok HOL/Isabelle : invariant spectral $1/k$ démontré formellement.\\\\
\\end{boitehol}'''

count = content.count(old)
print(f'Occurrences: {count}')
if count == 1:
    content = content.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Invariant done')
else:
    print('SKIPPED')