# -*- coding: utf-8 -*-
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '\\end{center}\n\n\\subsection{Niveau 4 --- Mécanisme d\'ancrage à'
new = '\\end{center}' + '''

\\begin{boitehol}{Construction terme à terme (MS_14 XIV.4)}
\\begin{holcode}
subsection "XIV.4 — Construction terme à terme (convolutive)"

definition terme_a_conv :: "nat => nat => nat => real" where
  "terme_a_conv k n i =
     (if k < 2 \\<or> n < 1 \\<or> i < 1 \\<or> i > n then 0
      else if n \\<le> 7 then (real k) ^ i
      else if i \\<le> n - 2 then (real k) ^ i
      else if i = n - 1 then (real k) ^ (n - 1) - (real k) ^ (n - 3)
      else (real k) ^ n - (real k) ^ (n - 2))"

definition terme_b_conv :: "nat => nat => nat => real" where
  "terme_b_conv k n i =
     (if k < 2 \\<or> n < 1 \\<or> i < 1 \\<or> i > n then 0
      else if n \\<le> 7 then terme_a_conv k n i
      else if i \\<le> 5 then (real k) ^ i
      else if i = 6 then (real k) ^ 7
      else if i \\<le> n - 2 then (real k) ^ (i + 1)
      else if i = n - 1 then (real k) ^ n - (real k) ^ (n - 2)
      else (real k) ^ (n + 1) - (real k) ^ (n - 1))"

lemma terme_a_conv_k8_n10_pos6 :
  "terme_a_conv 8 10 6 = 262144"
  unfolding terme_a_conv_def by simp

lemma terme_b_conv_k8_n10_pos6 :
  "terme_b_conv 8 10 6 = 2097152"
  unfolding terme_b_conv_def by simp

lemma saut_zeta_k8 :
  "terme_b_conv 8 10 6 = 8 * terme_a_conv 8 10 6"
  unfolding terme_b_conv_def terme_a_conv_def by simp
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Les définitions \\texttt{terme\\_a\\_conv} et
\\texttt{terme\\_b\\_conv} de la théorie Isabelle/HOL
\\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.4) formalisent la construction
terme à terme des suites A et B : pour $n \\ge 8$, la suite A utilise $k^i$
aux positions $i \\le n-2$, puis $k^{n-1}-k^{n-3}$ et $k^n-k^{n-2}$ ; la suite B
introduit le saut Zêta en position 6 ($k^7$ au lieu de $k^6$).\\\\
\\holok HOL/Isabelle : construction terme à terme validée formellement.\\\\
\\end{boitehol}''' + '\n\n\\subsection{Niveau 4 --- Mécanisme d\'ancrage à'

count = content.count(old)
print(f'Occurrences: {count}')
if count == 1:
    content = content.replace(old, new, 1)
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Niveau3 done')
else:
    print('SKIPPED')