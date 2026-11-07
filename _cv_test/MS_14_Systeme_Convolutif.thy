(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Validation principale methode_spectral.thy — section 14/14
   Fichier : MS_14_Systeme_Convolutif.thy  (section : Systeme convolutif 1-k (XIV) + References + Licence (COEUR))
   Origine : methode_spectral.thy lignes 4233-5014 (verbatim phase 1, sans perte)
   Auteur : Philippe Thomas Savard
   Date : Le trois octobre deux mille vingt-six
   Lieu : Levis Chausdiere-Appalaches Canada
   Titre ouvrage : L'univers est au carre !
   Chapitre : La geometrie du spectre des nombres premiers
   ----------------------------------------------------------------------------
   TABLE DES MATIERES GLOBALE (14 fichiers de validation principale) :
    1/14 : MS_01_Fondements  — Fondements / Meta-theory  (lignes origine 118-351)
    2/14 : MS_02_Suites_AB_RsP_1_2  — Suites A et B + Rapport 1-2 + n x n  (lignes origine 352-491)
    3/14 : MS_03_Digamma_Equation_Generale  — Digamma + Axiomatisation positive + Exemples 29 31 37 41 + Equation generale  (lignes origine 492-676)
    4/14 : MS_04_Generalisation_Prime_i  — Generalisation i-eme nombre premier (prime_i)  (lignes origine 677-761)
    5/14 : MS_05_Modeles_1_3_1_4  — Modeles 1-4 et 1-3 + Validations generalisees  (lignes origine 762-1039)
    6/14 : MS_06_Mixtes_Negatives_Asymetries  — Suites mixtes + Reconstruction + Negatives + Asymetries  (lignes origine 1040-1204)
    7/14 : MS_07_Comparaison_Blocs  — Comparaison asymetrique + Blocs A_k B_k  (lignes origine 1205-1658)
    8/14 : MS_08_Ecarts_Negatifs  — Rapports negatifs 1-3 1-4 + Ecarts negatifs (-19 / -5)  (lignes origine 1659-1978)
    9/14 : MS_09_Preuve_Absurde  — Preuve par l'absurde — exclusion des composes (INTEGRAL)  (lignes origine 1979-2307)
   10/14 : MS_10_Ecarts_Mixtes_Positifs  — Ecarts mixtes (-31 / 17) + Ecarts 1-3 (227 / 173) + Ecarts 1-4 (947 / 881)  (lignes origine 2308-2630)
   11/14 : MS_11_Construction_SpectralFamily  — Regles construction A_i B_i (XI) + spectral_family (XI.bis) (INTEGRAL)  (lignes origine 2631-3224)
   12/14 : MS_12_Construction_Generalisee_1k  — Construction generalisee 1-k_i (XII)  (lignes origine 3225-3492)
   13/14 : MS_13_Pont_Savard  — Pont Savard : psi Tchebychev, zeta, Re = 1-2 + Synthese-index (INTEGRAL)  (lignes origine 3493-4232)
   14/14 : MS_14_Systeme_Convolutif  — Systeme convolutif 1-k (XIV) + References + Licence (COEUR)  (lignes origine 4233-5014)
   ----------------------------------------------------------------------------
   STATUT : F09 preuve par l'absurde / F11 reconstruction + spectral_family /
   F13 Pont Savard / F14 convolutif = A CONSERVER INTEGRAUX.
   F05 rapports 1-2/1-3/1-4 + F08/F10 ecarts numeriques = CANDIDATS
   suppression / generalisation phase 2 (voir DEVIS_NETTOYAGE_HOL.md).
   Memoire : le decoupage ne reduit pas le pic (1 session = 1 tas partage).
   ============================================================================ *)
theory MS_14_Systeme_Convolutif
  imports MS_13_Pont_Savard
begin

(* TOC locale (origine) :
   L4233 : XIV. Système convolutif complet — rapport général 1/k
   L4304 : XIV.1 — Constantes Savard universelles
   L4374 : XIV.2 — Formules fermées générales
   L4403 : XIV.3 — Rapport spectral 1/k universel (preuve algébrique)
   L4524 : XIV.4 — Construction terme à terme (convolutive)
   L4603 : XIV.5 — Mécanisme d'ancrage à n=10 (quatre essais Digamma)
   L4660 : XIV.6 — Règle de décalage de rang pour n \<noteq> 10
   L4730 : XIV.7 — Validation exacte : k=8, n=34 (P = 32 537)
   L4786 : XIV.8 — Rapport spectral de convolution : instance k=8
   L4807 : XIV.9 — Postulat convolutif général
   L4841 : XIV.10 — Synthèse : le système convolutif dans l'architecture Savard
   L4905 : XIV.11 — Portée des ancrages et cas ambigus (PDF, classeur et journaux)
   L4951 : References externes - Mathlib (Lean 4)
   L4970 : License - Apache 2.0 (adaptation pour methode_spectral.thy)
*)

section "XIV. Système convolutif complet — rapport général 1/k"

text \<open>
  ===========================================================================
  SYSTÈME CONVOLUTIF — VUE D'ENSEMBLE
  ===========================================================================
  Le système convolutif généralise les modèles 1/2, 1/3 et 1/4 à tout
  rapport non-typique 1/k (k entier >= 3). Les formules fermées exactes
  des sommes des suites A et B sont :

      Somme_A(k, n) = (alphaA(k) / 2) * k^n  -  offsetA(k)
      Somme_B(k, n) = (alphaB(k) / 2) * k^n  -  offsetB(k)

  où les quatre constantes Savard universelles valent :

      alphaA(k) = 2 * (k^4 - k^2 + 1) / ((k-1) * k^3)
      alphaB(k) = k * alphaA(k)
      offsetA(k) = k / (k-1)
      offsetB(k) = (k^7 - k^6 + k) / (k-1)

  Ces formules sont dérivées algébriquement de la construction convolutive
  terme à terme validée dans les feuilles Convolution, Modèle Formel,
  Démonstration Formelle et Système Général du tableur.

  RÈGLE DE RECONSTRUCTION (ancrage n=10 + décalage de rang) :
     1. À n=10 : tester les quatre Digamma ΣA ± A(7) et ΣA ± A(8) ;
       un candidat unique peut être retenu automatiquement. Une branche
       explicitement inscrite au catalogue peut aussi être utilisée, mais
       toutes les autres branches premières doivent rester visibles.
       Sans catalogue, zéro ou plusieurs candidats ne donnent aucun ancrage.
    2. Pour n \<noteq> 10 : rang cible = rang base + n - 10 ;
       P cible = tblPremiers[rang cible] ;
       Digamma calculé = ΣB(k,n) - P_cible × k^6.

  VALIDATION EXACTE : k=8, n=34 donne P = 32 537 (rang 3492), avec
      Somme A exacte = 5 705 842 489 643 358 455 620 763 423 304
      Somme B exacte = 45 646 739 917 146 867 644 966 107 124 296
      Digamma exact  = 45 646 739 917 146 867 644 957 577 744 968
      Contrôle       : (ΣB - Digamma) / k^6 = 32 537 ✓
\<close>

text \<open>
  RÉCONCILIATION TYPIQUE (1/2) ET NON-TYPIQUE (1/k) — CONCORDANCE PIPELINE

  Le pipeline cognitif (PipelineCognitifNiveaux, v7.5) distingue deux régimes
  qui PARTAGENT exactement les mêmes constantes Savard et les mêmes formes
  fermées (les lemmes somme_A_conv_k2_eq_SA et somme_B_conv_k2_eq_SB le
  prouvent pour k = 2) :

    RAPPORT TYPIQUE 1/2 (k = 2) :
      - n = quantité de termes = position du premier dans P
        (2 = 1er, 3 = 2e, 5 = 3e, ..., 29 = 10e, ... infini).
      - Ancrage n = 10 : Digamma = S_A(10) - 2^8 = 1406
        → P = (S_B(10) - 1406) / 2^6 = 29.
      - Pour n \<noteq> 10 : Digamma = S_B(n) - P_n * 2^6, où P_n est le n-ième
        premier (ex. n = 9 : (1598 - 23 * 64) = 126 → P = 23).

    RAPPORTS NON-TYPIQUES 1/k (k >= 3) :
      - Ancrage à n = 10 par les quatre essais Digamma ; le candidat premier
        unique constitue l'ancrage (rang base, premier base).
      - Pour n \<noteq> 10 : rang_cible = rang_base + n - 10 ;
        Digamma = S_B(k,n) - P_cible * k^6 (règle XIV.6).

    ORDRE D'ANCRAGE DÉTERMINISTE (implémentation) :
      Les quatre essais sont tentés dans l'ordre (position 8, signe −),
      (position 8, signe +), (position 7, signe +), (position 7, signe −) ;
      le PREMIER candidat entier premier dans cet ordre est retenu. Cet ordre
      reproduit exactement le catalogue d'ancrages de XIV.6 (k = 3..9) ainsi
      que l'ancre typique 29 pour k = 2, validé numériquement par le pipeline.
\<close>

subsection "XIV.1 — Constantes Savard universelles"

text \<open>
  Les quatre constantes alphaA, alphaB, offsetA, offsetB sont définies
  algébriquement pour tout entier k >= 2. Elles constituent le cœur du
  système convolutif général et s'instancient exactement sur les valeurs
  numériques vérifiées pour k = 3, 4, 5, 6, 7, 8, 9 dans le tableur.
\<close>

definition alphaA_conv :: "nat \<Rightarrow> real" where
  "alphaA_conv k = 2 * (real k ^ 4 - real k ^ 2 + 1)
                   / ((real k - 1) * real k ^ 3)"

definition alphaB_conv :: "nat \<Rightarrow> real" where
  "alphaB_conv k = real k * alphaA_conv k"

definition offsetA_conv :: "nat \<Rightarrow> real" where
  "offsetA_conv k = real k / (real k - 1)"

definition offsetB_conv :: "nat \<Rightarrow> real" where
  "offsetB_conv k = (real k ^ 7 - real k ^ 6 + real k) / (real k - 1)"

text \<open>
  Vérification numérique : pour k = 3, alphaA = 2*(81-9+1)/(2*27) = 2*73/54 = 73/27
  et alphaB = 3 * 73/27 = 73/9. Ces valeurs correspondent exactement aux
  coefficients utilisés dans les définitions A_1_3 et B_1_3 de la Section III.
\<close>

lemma alphaA_conv_k3 : "alphaA_conv 3 = 73 / 27"
  unfolding alphaA_conv_def by simp

lemma alphaB_conv_k3 : "alphaB_conv 3 = 73 / 9"
  unfolding alphaB_conv_def alphaA_conv_def by simp

lemma offsetA_conv_k3 : "offsetA_conv 3 = 3 / 2"
  unfolding offsetA_conv_def by simp

lemma offsetB_conv_k3 : "offsetB_conv 3 = (2187 - 729 + 3) / 2"
  unfolding offsetB_conv_def by simp

text \<open>
  Pour k = 2 : alphaA = 2*(16-4+1)/(1*8) = 2*13/8 = 13/4 = 3.25 et
  alphaB = 2 * 3.25 = 6.5. Ces valeurs recoupent exactement les coefficients
  de SA et SB (Sections I et XI.bis). Le système convolutif est donc une
  généralisation stricte du régime central 1/2.
\<close>

lemma alphaA_conv_k2 : "alphaA_conv 2 = 13 / 4"
  unfolding alphaA_conv_def by simp

lemma alphaB_conv_k2 : "alphaB_conv 2 = 13 / 2"
  unfolding alphaB_conv_def alphaA_conv_def by simp

lemma offsetA_conv_k2 : "offsetA_conv 2 = 2"
  unfolding offsetA_conv_def by simp

lemma offsetB_conv_k2 : "offsetB_conv 2 = 132 / 2"
  unfolding offsetB_conv_def by simp

text \<open>
  Pour k = 4 : alphaA = 2*(256-16+1)/(3*64) = 2*241/192 = 241/96 et
  alphaB = 4 * alphaA = 241/24. Ces valeurs correspondent aux coefficients
  de A_1_4 et B_1_4 de la Section II.
\<close>

lemma alphaA_conv_k4 : "alphaA_conv 4 = 241 / 96"
  unfolding alphaA_conv_def by simp

lemma alphaB_conv_k4 : "alphaB_conv 4 = 241 / 24"
  unfolding alphaB_conv_def alphaA_conv_def by simp
subsection "XIV.2 — Formules fermées générales"

text \<open>
  Les deux formules fermées universelles pour les sommes des suites A et B,
  valables pour tout k >= 2 et tout n >= 1. La relation alphaB = k * alphaA
  garantit algébriquement que le rapport spectral (ΣA(n1)-ΣA(n2))/(ΣB(n1)-ΣB(n2))
  vaut exactement 1/k pour toute paire (n1, n2) avec n1 \<noteq> n2.
\<close>

definition somme_A_conv :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_A_conv k n = (alphaA_conv k / 2) * (real k) ^ n - offsetA_conv k"

definition somme_B_conv :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_B_conv k n = (alphaB_conv k / 2) * (real k) ^ n - offsetB_conv k"

text \<open>
  Compatibilité avec les définitions historiques SA (k=2), A_1_3 (k=3), A_1_4 (k=4).
\<close>

lemma somme_A_conv_k2_eq_SA :
  "somme_A_conv 2 n = SA n"
  unfolding somme_A_conv_def alphaA_conv_def offsetA_conv_def SA_def
  by (simp add: field_simps)

lemma somme_B_conv_k2_eq_SB :
  "somme_B_conv 2 n = SB n"
  unfolding somme_B_conv_def alphaB_conv_def alphaA_conv_def offsetB_conv_def SB_def
  by (simp add: field_simps)

subsection "XIV.3 — Rapport spectral 1/k universel (preuve algébrique)"

text \<open>
  Théorème central du système convolutif : le rapport spectral
  (ΣA(n1) - ΣA(n2)) / (ΣB(n1) - ΣB(n2)) vaut exactement 1/k
  pour tout k >= 2 et toute paire d'entiers positifs distincts n1, n2.

  La preuve n'utilise que la relation alphaB = k * alphaA et la
  non-nullité de k^n1 - k^n2 (pour n1 \<noteq> n2, k >= 2).
\<close>

definition RsP_conv :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_conv k n1 n2 =
     (somme_A_conv k n1 - somme_A_conv k n2) /
     (somme_B_conv k n1 - somme_B_conv k n2)"

theorem RsP_conv_constant :
  assumes hk   : "k \<ge> 2"
      and hn1  : "n1 \<ge> 1"
      and hn2  : "n2 \<ge> 1"
      and hneq : "n1 \<noteq> n2"
  shows "RsP_conv k n1 n2 = 1 / real k"
proof -
  have hk_gt1 : "(real k) > 1"  using hk by simp
  have hk_ne0 : "(real k) \<noteq> 0"  using hk by simp

  (* Non-nullité de k^n1 - k^n2 *)
  have hpow_ne : "(real k) ^ n1 - (real k) ^ n2 \<noteq> 0"
  proof (cases "n1 < n2")
    case True
    hence "(real k) ^ n1 < (real k) ^ n2"
      using power_strict_increasing[of n1 n2 "real k"] hk_gt1 by simp
    thus ?thesis by simp
  next
    case False
    with hneq have "n2 < n1" by simp
    hence "(real k) ^ n2 < (real k) ^ n1"
      using power_strict_increasing[of n2 n1 "real k"] hk_gt1 by simp
    thus ?thesis by simp
  qed

  (* Développement de la différence ΣA *)
  have hA :
    "somme_A_conv k n1 - somme_A_conv k n2 =
       (alphaA_conv k / 2) * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding somme_A_conv_def by (simp add: field_simps)

  (* Développement de la différence ΣB *)
  have hB :
    "somme_B_conv k n1 - somme_B_conv k n2 =
       (alphaB_conv k / 2) * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding somme_B_conv_def by (simp add: field_simps)

  (* alphaB = k * alphaA, donc le rapport vaut alphaA / alphaB = 1/k *)
  have halphaB : "alphaB_conv k = real k * alphaA_conv k"
    unfolding alphaB_conv_def by simp

  have halphaA_ne0 : "alphaA_conv k \<noteq> 0"
  proof -
    have hk_pos: "real k > 0" using hk_gt1 by simp
    have hk2: "real k ^ 2 > 1" using hk_gt1 by (simp add: power_gt1)
    have hk2_pos: "real k ^ 2 > 0" using hk_pos by simp

    (* Étape 1 : k^4 = k^2 * k^2 *)
    have "4 = (2::nat) + 2" by simp
    hence "real k ^ 4 = real k ^ (2 + 2)" by simp
    also have "\<dots> = real k ^ 2 * real k ^ 2" by (simp add: power_add)
    finally have k4_eq: "real k ^ 4 = real k ^ 2 * real k ^ 2" .

    (* Étape 2 : Construction de l'inégalité stricte *)
    have p1: "0 < real k ^ 2 - 1" using hk2 by simp
    have p2: "0 < real k ^ 2 * (real k ^ 2 - 1)"
      using hk2_pos p1 by (rule mult_pos_pos)
    have p3: "0 < real k ^ 2 * (real k ^ 2 - 1) + 1"
      using p2 by simp

    (* Étape 3 : Substitution algébrique *)
    have p4: "real k ^ 2 * (real k ^ 2 - 1) + 1 = real k ^ 2 * real k ^ 2 - real k ^ 2 + 1"
      by (simp add: algebra_simps)
    have p5: "real k ^ 2 * real k ^ 2 - real k ^ 2 + 1 = real k ^ 4 - real k ^ 2 + 1"
      using k4_eq by simp

    (* Conclusion *)
    have "0 < real k ^ 4 - real k ^ 2 + 1"
      using p3 p4 p5 by simp
    hence "alphaA_conv k > 0"
      unfolding alphaA_conv_def using hk_gt1 by (auto simp: field_simps)
    thus ?thesis by simp
  qed

  have halphaB_ne0 : "alphaB_conv k \<noteq> 0"
    using halphaB halphaA_ne0 hk_ne0 by simp

  (* Calcul final du rapport *)
  have "RsP_conv k n1 n2 =
        ((alphaA_conv k / 2) * ((real k) ^ n1 - (real k) ^ n2)) /
        ((alphaB_conv k / 2) * ((real k) ^ n1 - (real k) ^ n2))"
    unfolding RsP_conv_def hA hB by simp
  also have "\<dots> = alphaA_conv k / alphaB_conv k"
    using hpow_ne halphaB_ne0 by (simp add: field_simps)
  also have "\<dots> = alphaA_conv k / (real k * alphaA_conv k)"
    using halphaB by simp
  also have "\<dots> = 1 / real k"
    using halphaA_ne0 hk_ne0 by (simp add: field_simps)
  finally show ?thesis .
qed
corollary RsP_conv_k3 :
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "RsP_conv 3 n1 n2 = 1 / 3"
  using RsP_conv_constant[of 3 n1 n2] assms by simp

corollary RsP_conv_k4 :
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "RsP_conv 4 n1 n2 = 1 / 4"
  using RsP_conv_constant[of 4 n1 n2] assms by simp

corollary RsP_conv_k8 :
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "RsP_conv 8 n1 n2 = 1 / 8"
  using RsP_conv_constant[of 8 n1 n2] assms by simp

subsection "XIV.4 — Construction terme à terme (convolutive)"

text \<open>
  Les suites A et B sont construites terme à terme selon les règles
  de la Section XI et du code Python du tableur :

  Suite A (pour n >= 8) :
    - Position i = 1..n-2  : terme_a(k,n,i) = k^i
    - Position i = n-1     : terme_a(k,n,n-1) = k^(n-1) - k^(n-3)
    - Position i = n       : terme_a(k,n,n)   = k^n - k^(n-2)

  Suite B (pour n >= 8) — saut Zêta à la position 6 :
    - Position i = 1..5    : terme_b(k,n,i) = k^i
    - Position i = 6       : terme_b(k,n,6) = k^7             [Saut Zêta]
    - Position i = 7..n-2  : terme_b(k,n,i) = k^(i+1)        [décalée]
    - Position i = n-1     : terme_b(k,n,n-1) = k^n - k^(n-2)
    - Position i = n       : terme_b(k,n,n)   = k^(n+1) - k^(n-1)

  Pour n <= 7 : terme_b = terme_a (pas de substitution Zêta).
\<close>

definition terme_a_conv :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "terme_a_conv k n i =
     (if k < 2 \<or> n < 1 \<or> i < 1 \<or> i > n then 0
      else if n \<le> 7 then (real k) ^ i
      else if i \<le> n - 2 then (real k) ^ i
      else if i = n - 1 then (real k) ^ (n - 1) - (real k) ^ (n - 3)
      else (real k) ^ n - (real k) ^ (n - 2))"

definition terme_b_conv :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "terme_b_conv k n i =
     (if k < 2 \<or> n < 1 \<or> i < 1 \<or> i > n then 0
      else if n \<le> 7 then terme_a_conv k n i
      else if i \<le> 5 then (real k) ^ i
      else if i = 6 then (real k) ^ 7
      else if i \<le> n - 2 then (real k) ^ (i + 1)
      else if i = n - 1 then (real k) ^ n - (real k) ^ (n - 2)
      else (real k) ^ (n + 1) - (real k) ^ (n - 1))"

text \<open>
  Lemmes de validation numérique pour k=8, n=10
  (extraits de la feuille Moteur Universel du tableur).
\<close>

lemma terme_a_conv_k8_n10_pos6 :
  "terme_a_conv 8 10 6 = 262144"
  unfolding terme_a_conv_def by simp

lemma terme_a_conv_k8_n10_pos9 :
  "terme_a_conv 8 10 9 = 132120576"
  unfolding terme_a_conv_def by simp

lemma terme_a_conv_k8_n10_pos10 :
  "terme_a_conv 8 10 10 = 1056964608"
  unfolding terme_a_conv_def by simp

lemma terme_b_conv_k8_n10_pos6 :
  "terme_b_conv 8 10 6 = 2097152"
  unfolding terme_b_conv_def by simp

lemma terme_b_conv_k8_n10_pos9 :
  "terme_b_conv 8 10 9 = 1056964608"
  unfolding terme_b_conv_def by simp

lemma terme_b_conv_k8_n10_pos10 :
  "terme_b_conv 8 10 10 = 8455716864"
  unfolding terme_b_conv_def by simp

text \<open>
  Le saut Zêta à la position 6 de la suite B (k^7 au lieu de k^6) constitue
  la signature structurelle qui distingue le système convolutif des suites
  symétriques simples. Pour k=8, ce saut donne k^7 = 2^21 = 2 097 152
  au lieu de k^6 = 2^18 = 262 144.
\<close>

lemma saut_zeta_k8 :
  "terme_b_conv 8 10 6 = 8 * terme_a_conv 8 10 6"
  unfolding terme_b_conv_def terme_a_conv_def by simp

subsection "XIV.5 — Mécanisme d'ancrage à n=10 (quatre essais Digamma)"

text \<open>
  Le mécanisme d'ancrage à n=10 détermine le premier de référence pour
  chaque rapport 1/k. Les quatre candidats Digamma sont construits en
  ajustant la somme A par le terme de position 7 ou 8, avec signe + ou - :

      Digamma_j = ΣA(k,10) ± terme_a_conv(k,10,7 ou 8)
      P_j       = (ΣB(k,10) - Digamma_j) / k^6

  Le candidat retenu est le seul P_j qui soit un entier premier.
  (Si plusieurs candidats sont premiers, un critère supplémentaire est requis.)
\<close>

definition digamma_option_conv :: "real \<Rightarrow> real \<Rightarrow> int \<Rightarrow> real" where
  "digamma_option_conv sa_val terme (signe::int) =
     sa_val + real_of_int signe * terme"

definition candidat_P_conv :: "nat \<Rightarrow> real \<Rightarrow> real \<Rightarrow> real" where
  "candidat_P_conv k sb_val digamma_val =
     (sb_val - digamma_val) / (real k ^ 6)"

text \<open>
  Validation numérique pour k=3, n=10.
  Ancrage validé : position 8, signe −1, premier = 227 (rang 49).
  Les trois autres candidats (221, 215, 209) sont composés.
\<close>

definition SA_k3_n10 :: real where "SA_k3_n10 = 79824"
definition SB_k3_n10 :: real where "SB_k3_n10 = 238746"
definition zeta_k3    :: real where "zeta_k3    = 729"   (* k^6 = 3^6 *)

definition digamma_k3_pos8_neg :: real where
  "digamma_k3_pos8_neg = SA_k3_n10 - 6561"  (* 6561 = 3^8 *)

lemma candidat_k3_pos8_neg_est_227 :
  "(SB_k3_n10 - digamma_k3_pos8_neg) / zeta_k3 = 227"
  unfolding SB_k3_n10_def digamma_k3_pos8_neg_def SA_k3_n10_def zeta_k3_def
  by simp

text \<open>
  Validation numérique pour k=8, n=10.
  Ancrage validé : position 8, signe −1, premier = 32327 (rang 3468).
\<close>

definition SA_k8_n10 :: real where "SA_k8_n10 = 1208259144"
definition SB_k8_n10 :: real where "SB_k8_n10 = 9665811016"
definition zeta_k8    :: real where "zeta_k8    = 262144"  (* k^6 = 8^6 *)

definition digamma_k8_pos8_neg :: real where
  "digamma_k8_pos8_neg = SA_k8_n10 - 16777216"  (* 16777216 = 8^8 *)

lemma candidat_k8_pos8_neg_est_32327 :
  "(SB_k8_n10 - digamma_k8_pos8_neg) / zeta_k8 = 32327"
  unfolding SB_k8_n10_def digamma_k8_pos8_neg_def SA_k8_n10_def zeta_k8_def
  by simp

subsection "XIV.6 — Règle de décalage de rang pour n \<noteq> 10"

text \<open>
  Une fois l'ancrage obtenu à n=10, la reconstruction pour n \<noteq> 10
  utilise la règle de décalage de rang :

      rang_cible(n) = rang_base + n - 10
      P_cible(n)    = nth_prime(rang_cible(n))
      Digamma(k,n)  = ΣB(k,n) - P_cible(n) × k^6

  Cette règle est valide pour tout n >= 1 dès lors que rang_cible >= 1.
  Elle remplace les quatre essais Digamma qui ne s'appliquent qu'à n=10.

  Formellement, le rang base et le premier base sont modélisés par
  deux constantes axiomatisées par rapport (ils sont donnés par le
  catalogue des ancrages du tableur). Cette axiomatisation fournit des
  données d'entrée pour les cas listés; elle ne prouve ni leur génération
  par les quatre essais, ni une règle d'ancrage pour tout k.
\<close>

consts
  rang_base_k   :: "nat \<Rightarrow> nat"      (* rang du premier d'ancrage à n=10 *)
  premier_base_k :: "nat \<Rightarrow> nat"     (* premier d'ancrage à n=10 *)

axiomatization where
  ancrages_conv :
    "rang_base_k 3 = 49  \<and> premier_base_k 3 = 227   \<and>
     rang_base_k 4 = 161 \<and> premier_base_k 4 = 947   \<and>
     rang_base_k 5 = 430 \<and> premier_base_k 5 = 2999  \<and>
     rang_base_k 6 = 954 \<and> premier_base_k 6 = 7529  \<and>
     rang_base_k 7 = 1913 \<and> premier_base_k 7 = 16519 \<and>
     rang_base_k 8 = 3468 \<and> premier_base_k 8 = 32327 \<and>
     rang_base_k 9 = 5906 \<and> premier_base_k 9 = 58337"

definition rang_cible_conv :: "nat \<Rightarrow> nat \<Rightarrow> nat" where
  "rang_cible_conv k n = rang_base_k k + n - 10"

text \<open>
  Le premier cible est lu dans la table des premiers au rang calculé.
  La fonction prime_i existante (définie en Section I) joue ce rôle.
\<close>

definition premier_cible_conv :: "nat \<Rightarrow> nat \<Rightarrow> nat" where
  "premier_cible_conv k n = prime_i (rang_cible_conv k n)"

definition digamma_calcule_conv :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "digamma_calcule_conv k n =
     somme_B_conv k n
     - real (premier_cible_conv k n) * (real k ^ 6)"

definition reconstruction_conv :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "reconstruction_conv k n =
     (somme_B_conv k n - digamma_calcule_conv k n) / (real k ^ 6)"

lemma reconstruction_conv_identity :
  assumes hk : "k \<ge> 2"
  shows "reconstruction_conv k n = real (premier_cible_conv k n)"
proof -
  have "reconstruction_conv k n =
        (somme_B_conv k n -
         (somme_B_conv k n - real (premier_cible_conv k n) * (real k ^ 6)))
        / (real k ^ 6)"
    unfolding reconstruction_conv_def digamma_calcule_conv_def by simp
  also have "\<dots> = real (premier_cible_conv k n) * (real k ^ 6) / (real k ^ 6)"
    by simp
  also have "\<dots> = real (premier_cible_conv k n)"
    using hk by simp
  finally show ?thesis .
qed

subsection "XIV.7 — Validation exacte : k=8, n=34 (P = 32 537)"

text \<open>
  Le cas k=8, n=34 est la validation de référence du système convolutif.
  Les grandes sommes sont représentées par leurs valeurs entières exactes
  (extraites du tableur — les calculs Excel étant indicatifs, les valeurs
  exactes proviennent du code Python à arithmétique entière).

  Données vérifiées :
    - Premier base à n=10  : P₁₀ = 32 327, rang base = 3 468
    - Décalage             : n - 10 = 24
    - Rang cible           : 3 468 + 24 = 3 492
    - Premier cible        : P₃₄ = 32 537
    - k^6                  : 8^6 = 262 144
    - Somme A(8, 34) exacte: 5 705 842 489 643 358 455 620 763 423 304
    - Somme B(8, 34) exacte: 45 646 739 917 146 867 644 966 107 124 296
    - Digamma calculé      : 45 646 739 917 146 867 644 957 577 744 968
    - Contrôle             : (ΣB - Digamma) / 262144 = 32 537  ✓
\<close>

definition SA_k8_n34_exact :: real where
  "SA_k8_n34_exact = 5705842489643358455620763423304"

definition SB_k8_n34_exact :: real where
  "SB_k8_n34_exact = 45646739917146867644966107124296"

definition digamma_k8_n34_exact :: real where
  "digamma_k8_n34_exact = 45646739917146867644957577744968"

definition zeta6_k8 :: real where
  "zeta6_k8 = 262144"   (* 8^6 *)

lemma reconstruction_k8_n34 :
  "(SB_k8_n34_exact - digamma_k8_n34_exact) / zeta6_k8 = 32537"
  unfolding SB_k8_n34_exact_def digamma_k8_n34_exact_def zeta6_k8_def
  by simp

text \<open>
  Cohérence interne : le Digamma calculé est bien la différence
  ΣB(8,34) − P×k^6.
\<close>

lemma digamma_k8_n34_coherence :
  "SB_k8_n34_exact - 32537 * zeta6_k8 = digamma_k8_n34_exact"
  unfolding SB_k8_n34_exact_def digamma_k8_n34_exact_def zeta6_k8_def
  by simp

text \<open>
  Le décalage de rang est exact : rang_base(k=8) + (34-10) = 3468 + 24 = 3492.
\<close>

lemma rang_cible_k8_n34 :
  "rang_cible_conv 8 34 = 3492"
  unfolding rang_cible_conv_def
  using ancrages_conv by simp

subsection "XIV.8 — Rapport spectral de convolution : instance k=8"

text \<open>
  Instance du théorème RsP_conv_constant pour k=8.
  Pour toute paire (n₁, n₂) avec n₁,n₂ >= 1 et n₁ \<noteq> n₂,
  le rapport spectral de convolution vaut exactement 1/8.
\<close>

theorem RsP_conv_k8_general :
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "RsP_conv 8 n1 n2 = 1 / 8"
  using RsP_conv_constant[of 8 n1 n2] assms by simp

text \<open>
  Ce théorème, combiné à la validation exacte du cas k=8, n=34,
  constitue la démonstration complète que le système convolutif :
    (a) construit des suites A et B à partir de règles explicites,
    (b) reconstruit exactement le nombre premier cible,
    (c) maintient le rapport spectral 1/k = 1/8 entre toutes les paires.
\<close>

subsection "XIV.9 — Postulat convolutif général"

text \<open>
  Le postulat convolutif général affirme que, pour tout rapport non-typique
  1/k (k >= 3) admettant un ancrage unique à n=10, la règle de décalage
  de rang reconstruit exactement le i-ième nombre premier pour tout n >= 1.

  Ce postulat généralise le spectral_postulate_pos (k=2) aux rapports
  non-typiques validés numériquement dans le tableur (k=3..9).

  Portée logique : reconstruction_conv_identity démontre une identité issue
  de la définition de digamma_calcule_conv. Le corollaire ci-dessous est
  donc redondant; il ne prouve pas que premier_cible_conv est premier, que
  les rangs catalogués sont corrects, ni une conjecture sur les zéros de zêta.
\<close>

axiomatization where
  postulat_convolutif :
    "\<And>k n. k \<ge> 3 \<Longrightarrow> n \<ge> 1 \<Longrightarrow>
       prime (premier_cible_conv k n) \<Longrightarrow>
       reconstruction_conv k n = real (premier_cible_conv k n)"

text \<open>
  Corollaire : ce postulat est compatible avec le théorème
  reconstruction_conv_identity (démontré algébriquement sans hypothèse),
  qui le prouve pour tout k >= 2 sans restriction sur n.
\<close>

corollary postulat_convolutif_redondant :
  assumes "k \<ge> 3" "n \<ge> 1" "prime (premier_cible_conv k n)"
  shows "reconstruction_conv k n = real (premier_cible_conv k n)"
  using reconstruction_conv_identity[of k n] assms
  by linarith

subsection "XIV.10 — Synthèse : le système convolutif dans l'architecture Savard"

text \<open>
  ==========================================================================
  SYNTHÈSE DU SYSTÈME CONVOLUTIF (Section XIV)
  ==========================================================================
  Le système convolutif complet réunit les éléments suivants :

  NIVEAU 1 — CONSTANTES UNIVERSELLES
    alphaA(k), alphaB(k), offsetA(k), offsetB(k) : quatre formules
    algébriques exactes définies pour tout k >= 2 et instanciées
    numériquement pour k = 3, 4, 5, 6, 7, 8, 9 (tableur + lemmes).

  NIVEAU 2 — FORMULES FERMÉES GÉNÉRALES
    somme_A_conv(k, n) et somme_B_conv(k, n) : deux équations paramétrées
    en k et n, compatibles avec SA (k=2), A_1_3 (k=3), A_1_4 (k=4).

  NIVEAU 3 — RAPPORT SPECTRAL CONSTANT
    RsP_conv(k, n1, n2) = 1/k pour tout k >= 2, n1 >= 1, n2 >= 1, n1 \<noteq> n2.
    Théorème prouvé algébriquement (RsP_conv_constant), sans axiome.

  NIVEAU 4 — CONSTRUCTION CONVOLUTIVE (TERME À TERME)
    terme_a_conv et terme_b_conv : règles explicites de la Section XI
    (progression simple + deux termes terminaux Savard + saut Zêta à i=6
    dans la suite B). Validées numériquement pour k=8, n=10.

  NIVEAU 5 — MÉCANISME D'ANCRAGE ET DÉCALAGE
    À n=10 : calculer les quatre candidats dans l'ordre
             A(8)-, A(8)+, A(7)+, A(7)- et conserver chaque branche première.
             Hors catalogue, ne retenir automatiquement qu'un candidat unique.
             Toute sélection de catalogue doit être explicite et garder visibles
             les branches alternatives.
    À n\<noteq>10 : pour une ancre choisie, rang_cible = rang_base + n - 10 ;
             P = prime_i(rang_cible) ; Digamma = ΣB - P×k^6.
             Le cas k=8, n=34 vérifie l'identité arithmétique exacte.

  NIVEAU 6 — VALIDATION EXACTE
    k=8, n=34 : (ΣB - Digamma) / 262144 = 32537 ✓
    (Arithmétique entière exacte, sans limite de 15 chiffres d'Excel.)

  NIVEAU 7 — REQUÊTES MULTI-RAPPORTS
    Pour un n commun, chaque k est évalué séparément. Le rapport doit conserver
    la liste des branches premières et leur statut : ancre unique, choix explicite
    du catalogue, ambiguïté sans décision, ou aucun candidat standard.
    Les journaux 1/k pour k=2..1001 et k=1002..10001 sont des sorties du
    dispatcher v7.9 ; ils ne forment pas une preuve HOL et n'établissent pas
    l'unicité des ancres qu'ils affichent.

  POSITION DANS L'ARCHITECTURE SAVARD :
    RsP_conv_constant prouve l'invariant 1/k des formules fermées.
    reconstruction_conv_identity prouve que la définition de Digamma restitue
    premier_cible_conv par simplification. Les rangs des ancrages sont fournis
    par l'axiomatisation ancrages_conv pour k=3..9 ; ils ne sont pas dérivés
    des quatre essais Digamma. Le tableau k=10..111 et les listes multi-k
    ne sont pas formalisés ni vérifiés par ces résultats HOL.

  PORTÉE DES RÉSULTATS : la preuve RsP_conv_constant est algébrique et porte
  sur les fonctions définies ici. L'identité reconstruction_conv_identity
  porte sur premier_cible_conv fourni en entrée ; à elle seule, elle ne prouve
  ni sa primalité, ni l'exactitude des rangs catalogués, ni l'hypothèse de
  Riemann. Les affirmations de portée plus large dans le corpus restent des
  positions de l'auteur ou des hypothèses explicitement déclarées.
\<close>

subsection "XIV.11 — Portée des ancrages et cas ambigus (PDF, classeur et journaux)"

text \<open>
  La source Word/PDF fournie comporte 36 pages physiques. Le système généralisé
  apparaît aux pages imprimées 22..28 ; les exemples k=13, 42 et 54 occupent
  les pages 29..36. Le PDF compilé depuis le .tex local est un autre artefact
  (27 pages PDF, pagination imprimée jusqu'à 26). Il n'existe pas de pages
  37..49 dans la source fournie.

  Le tableau PDF k=10..111 distingue trois états, qui ne doivent pas être
  ramenés à un seul résultat automatique :

    - un candidat standard premier unique : ancrage admissible ;
    - plusieurs candidats premiers (C_MULTIPLE) : hors branche explicitement
      cataloguée, conserver chaque branche et demander une confirmation sans
      en retenir une par ordre ; une sélection de catalogue doit être tracée
      et afficher les branches alternatives ;
    - aucun candidat premier (AUCUN P) : déclarer l'absence d'ancrage standard.

  Le document compte 38 cas uniques, 20 multiples et 44 sans candidat pour
  k=10..111. Il donne aussi des règles spéciales, notamment pour k=11 et k=27.
  Elles ne doivent pas être extrapolées aux autres rapports. La table PDF
  Les constantes rang_base_k et premier_base_k ci-dessus ne couvrent que
  k=3..9; cette section ne formalise pas le catalogue étendu. Les pages
  k=10..111 et les deux journaux multi-k ne sont donc pas des théorèmes de
  la présente session Isabelle.

  La feuille « Validation Convolutive » inscrit 16 421 comme premier PDF
  pour 1/7. Le calcul exact confirme qu'il s'agit de la branche A(8)+ ;
  16 519 est la branche A(8)- explicitement retenue par le catalogue XIV.6.
  Ces valeurs sont deux candidats distincts, et non une erreur d'arrondi.
  Le rapport cognitif doit afficher leur branche et distinguer la sélection
  explicite du catalogue d'une sélection dynamique unique.

  Enfin, les deux journaux multi-k couvrent respectivement k=2..1001
  (1 000 requêtes, 423 succès rapportés) et k=1002..10001
  (9 000 requêtes, 2 604 succès rapportés). Ils ont été produits par le
  dispatcher v7.9, qui retenait le premier candidat premier rencontré et
  n'enregistrait pas toutes les branches premières. Ce sont des résultats
  d'exécution à reprendre avec le dispatcher qui conserve les candidats ;
  ils ne certifient ni l'unicité de leurs ancres, ni une proposition HOL,
  ni un résultat sur l'hypothèse de Riemann.
\<close>



section "References externes - Mathlib (Lean 4)"

text \<open>
  La contre-validation inter-assistants validation_zeta_lean.thy met en
  relation les points de la presente validation principale (Section XIII,
  Le Pont Savard) avec des enonces de la bibliotheque Mathlib pour Lean 4 :

    Mathlib.NumberTheory.LSeries.RiemannZeta  (Copyright (c) 2023 David Loeffler)
    Mathlib.NumberTheory.LSeries.ZetaZeros    (Copyright (c) 2026 Huanyu Zheng)
    Mathlib.NumberTheory.LSeries.Nonvanishing (Copyright (c) 2024 Michael Stoll,
                                               David Loeffler)

  Depot : https://github.com/leanprover-community/mathlib4
  Licence : Apache License, Version 2.0. Les enonces sont cites par nom
  uniquement ; aucun code Lean n'est reproduit. Detail complet et
  conformite de licence : section References externes de
  validation_zeta_lean.thy.
\<close>

section "License - Apache 2.0 (adaptation pour methode_spectral.thy)"

text \<open>
  Copyright (c) 2026 Philippe Thomas Savard

  This project, including the file methode_spectral.thy, its mathematical
  constructions, spectral models, axioms, proofs, and all associated
  documentation, is released under the terms of the Apache License,
  Version 2.0.
  You may use, reproduce, distribute, modify, and create derivative works
  from this project under the following conditions:

    1. Attribution
       You must include a notice stating that the original work was
       created by Philippe Thomas Savard, and you must retain all
       copyright notices.

    2. License Notice
       Any redistribution of the project, in source or binary form,
       must include this license and a clear reference to the Apache
       License, Version 2.0.

    3. Modifications
       If you modify the project, you must clearly indicate that
       changes were made.

    4. Patent Grant
       This license grants you a non-exclusive, worldwide, royalty-free
       patent license for any patent claims necessarily infringed by
       the project as originally provided.

    5. No Trademark Rights
       This license does not grant permission to use the name
       "Philippe Thomas Savard" or any project-specific branding
       for endorsement.

    6. Disclaimer
       The project is provided on an "AS IS" basis, without warranties
       or conditions of any kind, express or implied. The author is
       not liable for any damages arising from the use of this project.

  For the full legal text of the Apache License, Version 2.0, please refer to:
    https://www.apache.org/licenses/LICENSE-2.0
\<close>


end
