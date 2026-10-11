(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Validation principale methode_spectral.thy — section 5/14
   Fichier : MS_05_Modeles_1_3_1_4.thy  (section : Modeles 1-4 et 1-3 + Validations generalisees)
   Origine : methode_spectral.thy lignes 762-1039 (verbatim phase 1, sans perte)
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
theory MS_05_Modeles_1_3_1_4
  imports MS_04_Generalisation_Prime_i
begin

(* TOC locale (origine) :
   L762 : Modele spectral 1/4 : Forme generale des suites A et B.
   L795 : Axiomatisation spectral 1/4
   L816 : Modele spectral 1/4: Sommes de suite A et B, Digamma, Digamma calcule et determination du premier 947.
   L848 : Rapport 1/3 forme generaliser pour les suites A et B.
   L879 : Axiomatisation rapport 1/3.
   L900 : Rapport spectal 1/3 : validation numerique pour les suites A et B, Digamma, Digamma calcule et la determination du premier 227.
   L908 : Rapport 1/3
   L924 : Rapport spectral constant 1/3 et 1/4.
   L929 : Rapport spectral 1/3 - validation generalisee.
   L984 : Rapport spectral constant 1/4.
   L991 : Rapport spectral 1/4 - validation generalisee.
*)

section "Modele spectral 1/4 : Forme generale des suites A et B."

text \<open>
  Formes generalisees pour le rapport 1/4.
  On suit les equations :
    ((241/16)/12 * 4^n) - 4/3
    ((964/16)/12 * 4^n) - (3073 * (4/3))
\<close>
(* --- Definition des suites A_1_4 et B_1_4 --- *)

definition A_1_4 :: "nat => real" where
  "A_1_4 n = ((241 / 16) / 12) * (4 ^ n) - (4 / 3)"

definition B_1_4 :: "nat => real" where
  "B_1_4 n = ((964 / 16) / 12) * (4 ^ n) - (3073 * (4 / 3))"


(**************************************************************)
(* SECTION : Equation generale pour le modele spectral 1/4     *)
(**************************************************************)

definition prime_equation_1_4 :: "nat => nat => real" where
  "prime_equation_1_4 n p = (B_1_4 n - (B_1_4 n - 4096 * real p)) / 4096"

lemma prime_equation_1_4_identity:
  "prime_equation_1_4 n p = real p"
  unfolding prime_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral 1/4                            *)
(**************************************************************)

section "Axiomatisation spectral 1/4"

axiomatization where
  spectral_postulate_1_4:
    "!!n p. n > 0 ==> prime p ==> prime_equation_1_4 n p = real p"


(**************************************************************)
(* SECTION : Lemme final pour les nombres premiers (1/4)      *)
(**************************************************************)

lemma prime_equation_1_4_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_4 n p = real p"
  using spectral_postulate_1_4 assms by blast


(**************************************************************)
(* SECTION : Exemple concret pour 947                         *)
(**************************************************************)

section "Modele spectral 1/4: Sommes de suite A et B, Digamma, Digamma calcule et determination du premier 947."

text \<open>
  Donnees numeriques globales pour le modele 1/4 :
  - Somme de la suite A : 1316180
  - Somme de la suite B : 5260628
  - Digamma : 65536
  - Digamma calcule : 1316180 + 65536 = 1381716
  - (5260628 - 1381716) / 4096 = 947 (premier)
\<close>
definition suite_A_1_4_somme :: real where
  "suite_A_1_4_somme = 1316180"

definition suite_B_1_4_somme :: real where
  "suite_B_1_4_somme = 5260628"

definition digamma_1_4 :: real where
  "digamma_1_4 = 65536"

definition digamma_calcule_1_4 :: real where
  "digamma_calcule_1_4 = suite_A_1_4_somme + digamma_1_4"

lemma preuve_premier_947:
  "(suite_B_1_4_somme - digamma_calcule_1_4) / 4096 = 947"
  by (simp add: suite_A_1_4_somme_def suite_B_1_4_somme_def
                digamma_1_4_def digamma_calcule_1_4_def)


(**************************************************************)
(* SECTION : Modele Spectral 1/3 - Definitions completes      *)
(**************************************************************)

section "Rapport 1/3 forme generaliser pour les suites A et B."

text \<open>
  Formes generalisees pour le rapport 1/3.
  On suit les equations :
    ((73/9)/12 * 3^n) - 1.5
    ((219/9)/12 * 3^n) - (487 * 1.5)
\<close>
definition A_1_3 :: "nat => real" where
  "A_1_3 n = ((73 / 9) / 12) * (3 ^ n) - 1.5"

definition B_1_3 :: "nat => real" where
  "B_1_3 n = ((219 / 9) / 12) * (3 ^ n) - (487 * 1.5)"


(**************************************************************)
(* SECTION : Equation generale pour le modele spectral 1/3     *)
(**************************************************************)

definition prime_equation_1_3 :: "nat => nat => real" where
  "prime_equation_1_3 n p = (B_1_3 n - (B_1_3 n - 729 * real p)) / 729"

lemma prime_equation_1_3_identity:
  "prime_equation_1_3 n p = real p"
  unfolding prime_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral 1/3                            *)
(**************************************************************)

section "Axiomatisation rapport 1/3."

axiomatization where
  spectral_postulate_1_3:
    "!!n p. n > 0 ==> prime p ==> prime_equation_1_3 n p = real p"


(**************************************************************)
(* SECTION : Lemme final pour les nombres premiers (1/3)      *)
(**************************************************************)

lemma prime_equation_1_3_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_3 n p = real p"
  using spectral_postulate_1_3 assms by blast


(**************************************************************)
(* SECTION : Exemple concret pour 227                         *)
(**************************************************************)

section "Rapport spectal 1/3 : validation numerique pour les suites A et B, Digamma, Digamma calcule et la determination du premier 227."

definition suite_A_1_3_somme :: real where
  "suite_A_1_3_somme = 79824"

definition suite_B_1_3_somme :: real where
  "suite_B_1_3_somme = 238746"

section "Rapport 1/3"

definition digamma_1_3 :: real where
  "digamma_1_3 = 6561"

definition digamma_calcule_1_3 :: real where
  "digamma_calcule_1_3 = suite_A_1_3_somme - digamma_1_3"

lemma preuve_premier_227:
  "(suite_B_1_3_somme - digamma_calcule_1_3) / 729 = 227"
  by (simp add: suite_A_1_3_somme_def suite_B_1_3_somme_def
                digamma_1_3_def digamma_calcule_1_3_def)
(**************************************************************)
(* SECTION 6 : Rapport Spectral 1/3 et 1/4                    *)
(**************************************************************)

section "Rapport spectral constant 1/3 et 1/4."

text \<open>
  Definition du Rapport Spectral pour les modeles 1/3 et 1/4.
\<close>
section "Rapport spectral 1/3 - validation generalisee."

(* Rapport spectral 1/3 *)

definition RsP_1_3 :: "nat => nat => real" where
  "RsP_1_3 n1 n2 =
    (A_1_3 n1 - A_1_3 n2) /
    (B_1_3 n1 - B_1_3 n2)"

theorem RsP_un_tiers_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_3 n1 n2 = 1/3"
proof -
  (* Correction 2026-02 : temoin de non-nullite pour 3^n1 - 3^n2. *)
  have hne_pow_3: "(3::real)^n1 - 3^n2 \<noteq> 0"
  proof (cases "n1 < n2")
    case True
    hence "(3::real)^n1 < 3^n2"
      using power_strict_increasing[of n1 n2 "3::real"] by simp
    thus ?thesis by simp
  next
    case False
    with assms(3) have "n2 < n1" by simp
    hence "(3::real)^n2 < 3^n1"
      using power_strict_increasing[of n2 n1 "3::real"] by simp
    thus ?thesis by simp
  qed

  have diff_A:
    "A_1_3 n1 - A_1_3 n2 =
      ((73/9)/12) * (3^n1 - 3^n2)"
    unfolding A_1_3_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_3 n1 - B_1_3 n2 =
      ((219/9)/12) * (3^n1 - 3^n2)"
    unfolding B_1_3_def by (simp add: algebra_simps)

  have "RsP_1_3 n1 n2 =
        (((73/9)/12) * (3^n1 - 3^n2)) /
        (((219/9)/12) * (3^n1 - 3^n2))"
    unfolding RsP_1_3_def by (simp add: diff_A diff_B)

  also have "... = ((73/9)/12) / ((219/9)/12)"
    using hne_pow_3 by (simp add: field_simps)

  also have "... = 1/3"
    by simp

  finally show ?thesis .
qed


(* Rapport spectral 1/4 *)

section "Rapport spectral constant 1/4."

definition RsP_1_4 :: "nat => nat => real" where
  "RsP_1_4 n1 n2 =
    (A_1_4 n1 - A_1_4 n2) /
    (B_1_4 n1 - B_1_4 n2)"

section "Rapport spectral 1/4 - validation generalisee."

theorem RsP_un_quart_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_4 n1 n2 = 1/4"
proof -
  (* Correction 2026-02 : temoin de non-nullite pour 4^n1 - 4^n2. *)
  have hne_pow_4: "(4::real)^n1 - 4^n2 \<noteq> 0"
  proof (cases "n1 < n2")
    case True
    hence "(4::real)^n1 < 4^n2"
      using power_strict_increasing[of n1 n2 "4::real"] by simp
    thus ?thesis by simp
  next
    case False
    with assms(3) have "n2 < n1" by simp
    hence "(4::real)^n2 < 4^n1"
      using power_strict_increasing[of n2 n1 "4::real"] by simp
    thus ?thesis by simp
  qed

  have diff_A:
    "A_1_4 n1 - A_1_4 n2 =
      ((241/16)/12) * (4^n1 - 4^n2)"
    unfolding A_1_4_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_4 n1 - B_1_4 n2 =
      ((964/16)/12) * (4^n1 - 4^n2)"
    unfolding B_1_4_def by (simp add: algebra_simps)

  have "RsP_1_4 n1 n2 =
        (((241/16)/12) * (4^n1 - 4^n2)) /
        (((964/16)/12) * (4^n1 - 4^n2))"
    unfolding RsP_1_4_def by (simp add: diff_A diff_B)

  also have "... = ((241/16)/12) / ((964/16)/12)"
    using hne_pow_4 by (simp add: field_simps)

  also have "... = 1/4"
    by simp

  finally show ?thesis .
qed

(**************************************************************)
(* SECTION : Suites-mixtes A et B (-,+)                       *)
(**************************************************************)


end
