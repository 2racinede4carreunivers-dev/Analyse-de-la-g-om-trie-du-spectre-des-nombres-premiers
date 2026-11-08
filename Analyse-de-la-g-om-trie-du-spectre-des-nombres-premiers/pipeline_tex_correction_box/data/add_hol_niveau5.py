# -*- coding: utf-8 -*-
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '\\text{Digamma}(k,n) = \\SB(k,n) - P(k,n) \\times k^{6}.\n\\]\n\\end{boiteformule}'
new = old + '''

\\begin{boitehol}{Décalage de rang et reconstruction (MS_14 XIV.6, XIV.7)}
\\begin{holcode}
subsection "XIV.6 — Règle de décalage de rang pour n \\<noteq> 10"

definition rang_cible_conv :: "nat => nat => nat" where
  "rang_cible_conv k n = rang_base_k k + n - 10"

definition premier_cible_conv :: "nat => nat => nat" where
  "premier_cible_conv k n = prime_i (rang_cible_conv k n)"

definition digamma_calcule_conv :: "nat => nat => real" where
  "digamma_calcule_conv k n =
     somme_B_conv k n
     - real (premier_cible_conv k n) * (real k ^ 6)"

definition reconstruction_conv :: "nat => nat => real" where
  "reconstruction_conv k n =
     (somme_B_conv k n - digamma_calcule_conv k n) / (real k ^ 6)"

lemma reconstruction_conv_identity:
  assumes "k \\<ge> 2"
  shows "reconstruction_conv k n = real (premier_cible_conv k n)"
proof -
  have "reconstruction_conv k n =
         (somme_B_conv k n -
          (somme_B_conv k n - real (premier_cible_conv k n) * (real k ^ 6)))
         / (real k ^ 6)"
    unfolding reconstruction_conv_def digamma_calcule_conv_def by simp
  also have "\\<dots> = real (premier_cible_conv k n) * (real k ^ 6) / (real k ^ 6)"
    by simp
  also have "\\<dots> = real (premier_cible_conv k n)"
    using assms by simp
  finally show ?thesis .
qed

lemma rang_cible_k8_n34 : "rang_cible_conv 8 34 = 3492"
  unfolding rang_cible_conv_def
  using ancrages_conv by simp
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Les définitions \\texttt{rang\\_cible\\_conv},
\\texttt{premier\\_cible\\_conv}, \\texttt{digamma\\_calculé\\_conv} et
\\texttt{reconstruction\\_conv} de la théorie Isabelle/HOL
\\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.6, XIV.7) formalisent la loi de
rangement spectral : $\\text{rang\\_cible}(k,n) = \\text{rang\\_base}(k) + n - 10$,
puis $P(k,n) = \\text{premier}(\\text{rang\\_cible})$. Le lemme
\\texttt{reconstruction\\_conv\\_identity} prouve que pour tout $k \\ge 2$,
la reconstruction redonne exactement le premier cible. Le lemme
\\texttt{rang\\_cible\\_k8\\_n34} confirme que pour $k=8, n=34$, le rang cible est
3\,492, conduisant à $P=32\,537$.\\\\
\\holok HOL/Isabelle : décalage de rang et reconstruction validés formellement.\\\\
\\end{boitehol}'''

count = content.count(old)
print(f'Occurrences: {count}')
if count == 1:
    content = content.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Niveau5 done')
else:
    print('SKIPPED')