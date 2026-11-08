# -*- coding: utf-8 -*-
"""Script pour ajouter des boîtes de validation HOL/Isabelle dans le .tex"""
import io

path = r'c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\pipeline_tex_correction_box\data\Le-systeme-convolutif-Philippe-Thomas-Savard-2026-10-30.tex'

with io.open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Boîte HOL après "Détermination du nombre premier" (Digamma)
old1 = '\\end{boiteformule}\n\n\\subsubsection{Équations des sommes des suites A et B}'

new1 = '''\\end{boiteformule}

\\begin{boitehol}{Digamma et reconstruction (MS_14 XIV.5)}
\\begin{holcode}
subsection "XIV.5 — Mécanisme d'ancrage à n=10 (quatre essais Digamma)"

definition digamma_option_conv :: "real => real => int => real" where
  "digamma_option_conv sa_val terme (signe::int) =
     sa_val + real_of_int signe * terme"

definition candidat_P_conv :: "nat => real => real => real" where
  "candidat_P_conv k sb_val digamma_val =
     (sb_val - digamma_val) / (real k ^ 6)"

lemma candidat_k3_pos8_neg_est_227:
  "(SB_k3_n10 - digamma_k3_pos8_neg) / zeta_k3 = 227"
  unfolding SB_k3_n10_def digamma_k3_pos8_neg_def SA_k3_n10_def zeta_k3_def
  by simp

lemma candidat_k8_pos8_neg_est_32327:
  "(SB_k8_n10 - digamma_k8_pos8_neg) / zeta_k8 = 32327"
  unfolding SB_k8_n10_def digamma_k8_pos8_neg_def SA_k8_n10_def zeta_k8_def
  by simp
\\end{holcode}
\\smallskip
\\textbf{Correspondance HOL.} Les définitions de la théorie Isabelle/HOL
\\texttt{MS\\_14\\_Systeme\\_Convolutif} (XIV.5) formalisent le mécanisme d'ancrage
à $n=10$ : les quatre candidats Digamma sont construits par ajustement de la
somme A par le terme de position 7 ou 8, avec signe $+$ ou $-$. Les lemmes
\\texttt{candidat\\_k3\\_pos8\\_neg\\_est\\_227} et
\\texttt{candidat\\_k8\\_pos8\\_neg\\_est\\_32327} confirment respectivement les ancrages
$P=227$ pour $k=3$ et $P=32\\,327$ pour $k=8$.\\\\
\\holok HOL/Isabelle : mécanisme d'ancrage Digamma validé formellement.\\\\
\\end{boitehol}

\\subsubsection{Équations des sommes des suites A et B}'''

count = content.count(old1)
print(f'Old1 occurrences: {count}')
if count == 1:
    content = content.replace(old1, new1, 1)
    print('Replacement 1 done')
else:
    print('Skipping replacement 1 (count != 1)')

with io.open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')