(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Validation principale methode_spectral.thy — section 12/14
   Fichier : MS_12_Construction_Generalisee_1k.thy  (section : Construction generalisee 1-k_i (XII))
   Origine : methode_spectral.thy lignes 3225-3492 (verbatim phase 1, sans perte)
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
theory MS_12_Construction_Generalisee_1k
  imports MS_11_Construction_SpectralFamily
begin

(* TOC locale (origine) :
   L3225 : Section XII : Construction generalisee pour rapport spectral 1/k_i
*)

section "Section XII : Construction generalisee pour rapport spectral 1/k_i"

text \<open>
  Generalisation pour tout rapport spectral 1/k_i (k = 2, 3, 4, ...) :

    somme_A_pos(k, n) = (alpha_A(k) / 2) * k^n - offset_A(k)
    somme_B_pos(k, n) = (alpha_B(k) / 2) * k^n - offset_B(k)
    somme_A_neg(k, n) = alpha_A(k) * k^(-n) - offset_A(k)
    somme_B_neg(k, n) = alpha_B(k) * k^(-n) - offset_B(k)

  ou les constantes Savard sont :
    k=2 : alpha_A=3.25,    alpha_B=6.5,    offset_A=2,   offset_B=66
    k=3 : alpha_A=73/9,    alpha_B=219/9,  offset_A=1.5, offset_B=487*1.5
    k=4 : alpha_A=241/16,  alpha_B=964/16, offset_A=4/3, offset_B=3073*(4/3)
\<close>

(* === XII.1. Constantes Savard parametriques === *)

definition alpha_A_k :: "nat \<Rightarrow> real" where
  "alpha_A_k k =
     (if k = 2 then 3.25
      else if k = 3 then 73/9
      else if k = 4 then 241/16
      else 0)"

definition alpha_B_k :: "nat \<Rightarrow> real" where
  "alpha_B_k k =
     (if k = 2 then 6.5
      else if k = 3 then 219/9
      else if k = 4 then 964/16
      else 0)"

definition offset_A_k :: "nat \<Rightarrow> real" where
  "offset_A_k k =
     (if k = 2 then 2
      else if k = 3 then 1.5
      else if k = 4 then 4/3
      else 0)"

definition offset_B_k :: "nat \<Rightarrow> real" where
  "offset_B_k k =
     (if k = 2 then 66
      else if k = 3 then 487 * 1.5
      else if k = 4 then 3073 * (4/3)
      else 0)"

(* === XII.2. Formules fermees positives et negatives === *)

definition somme_A_pos_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_A_pos_k k n = (alpha_A_k k / 2) * (real k) ^ n - offset_A_k k"

definition somme_B_pos_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_B_pos_k k n = (alpha_B_k k / 2) * (real k) ^ n - offset_B_k k"

definition somme_A_neg_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_A_neg_k k n = alpha_A_k k / ((real k) ^ n) - offset_A_k k"

definition somme_B_neg_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_B_neg_k k n = alpha_B_k k / ((real k) ^ n) - offset_B_k k"

(* === XII.3. Lemmes : compatibilite avec SA, SB existantes (k=2 positif) === *)

lemma somme_A_pos_k_eq_SA:
  "somme_A_pos_k 2 n = SA n"
  unfolding somme_A_pos_k_def alpha_A_k_def offset_A_k_def SA_def
  by simp

lemma somme_B_pos_k_eq_SB:
  "somme_B_pos_k 2 n = SB n"
  unfolding somme_B_pos_k_def alpha_B_k_def offset_B_k_def SB_def
  by simp

(* === XII.4. Construction terme-a-terme suite A (positive, k=2)              === *)
(*   Pour i de 1 a n-2 : a_i = a_1 * r^(i-1) (progression simple, r = k)      *)
(*   Position n-1 (penultieme) : a_(n-2) * (r - 1/r)                          *)
(*   Position n (dernier)      : penultieme * r                               *)
(*   Pour n = 1 : juste a_1                                                   *)

definition terme_A_pos :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "terme_A_pos a1 r n i =
     (if i = 1 then a1
      else if (n = 2 \<and> i = 2) then a1 * (r - 1/r)
      else if (n \<ge> 3 \<and> i \<le> n - 2) then a1 * r ^ (i - 1)
      else if (n \<ge> 3 \<and> i = n - 1) then a1 * r ^ (n - 3) * (r - 1/r)
      else if (n \<ge> 3 \<and> i = n) then a1 * r ^ (n - 3) * (r - 1/r) * r
      else 0)"

(* === XII.5. Suite B : meme construction + substitution position 6 (n >= 8) === *)

definition terme_B_pos :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "terme_B_pos a1 r n i =
     (if (n < 8) then terme_A_pos a1 r n i
      else if (i = 1) then a1
      else if i \<le> 5 then a1 * r ^ (i - 1)
      else if (i = 6) then a1 * r ^ 6
      else if i \<le> n - 2 then a1 * r ^ i
      else if (i = n - 1) then a1 * r ^ (n - 2) * (r - 1/r)
      else if (i = n) then a1 * r ^ (n - 2) * (r - 1/r) * r
      else 0)"

(* === XII.6. Validations numeriques cle (k=2, a1=2, r=2)                     === *)

(*  Suite A 1 terme   : [2]                                                   *)
lemma suite_A_1_terme:
  "terme_A_pos 2 2 1 1 = 2"
  unfolding terme_A_pos_def by simp

(*  Suite A 2 termes  : [2, 3]                                                *)
lemma suite_A_2_termes_pos1:
  "terme_A_pos 2 2 2 1 = 2"
  unfolding terme_A_pos_def by simp

lemma suite_A_2_termes_pos2:
  "terme_A_pos 2 2 2 2 = 3"
  unfolding terme_A_pos_def by simp

(*  Suite A 3 termes  : [2, 3, 6]                                             *)
lemma suite_A_3_termes_pos3:
  "terme_A_pos 2 2 3 3 = 6"
  unfolding terme_A_pos_def by simp

(*  Suite A 4 termes  : [2, 4, 6, 12] - position 3 = 6 (penultieme)           *)
lemma suite_A_4_termes_pos3:
  "terme_A_pos 2 2 4 3 = 6"
  unfolding terme_A_pos_def by simp

lemma suite_A_4_termes_pos4:
  "terme_A_pos 2 2 4 4 = 12"
  unfolding terme_A_pos_def by simp

(*  Suite A 5 termes  : [2, 4, 8, 12, 24]                                     *)
lemma suite_A_5_termes_pos4:
  "terme_A_pos 2 2 5 4 = 12"
  unfolding terme_A_pos_def by simp

lemma suite_A_5_termes_pos5:
  "terme_A_pos 2 2 5 5 = 24"
  unfolding terme_A_pos_def by simp

(*  Suite A 7 termes  : [2, 4, 8, 16, 32, 48, 96]                             *)
lemma suite_A_7_termes_pos6:
  "terme_A_pos 2 2 7 6 = 48"
  unfolding terme_A_pos_def by simp

lemma suite_A_7_termes_pos7:
  "terme_A_pos 2 2 7 7 = 96"
  unfolding terme_A_pos_def by simp

(*  Suite A 8 termes  : [2, 4, 8, 16, 32, 64, 96, 192]                        *)
lemma suite_A_8_termes_pos6:
  "terme_A_pos 2 2 8 6 = 64"
  unfolding terme_A_pos_def by simp

lemma suite_A_8_termes_pos7:
  "terme_A_pos 2 2 8 7 = 96"
  unfolding terme_A_pos_def by simp

lemma suite_A_8_termes_pos8:
  "terme_A_pos 2 2 8 8 = 192"
  unfolding terme_A_pos_def by simp

(*  Suite B 8 termes  : [2, 4, 8, 16, 32, 128, 192, 384]                      *)
(*  Substitution position 6 : 128 = 2 * 64 = position 7 de la suite A         *)
(*  Positions 7 et 8 suivent la regle penultieme / dernier avec base decalee  *)
lemma suite_B_8_termes_pos6:
  "terme_B_pos 2 2 8 6 = 128"
  unfolding terme_B_pos_def by simp

lemma suite_B_8_termes_pos7:
  "terme_B_pos 2 2 8 7 = 192"
  unfolding terme_B_pos_def by simp

lemma suite_B_8_termes_pos8:
  "terme_B_pos 2 2 8 8 = 384"
  unfolding terme_B_pos_def by simp

(*  Suite B 9 termes  : [2, 4, 8, 16, 32, 128, 256, 384, 768]                 *)
lemma suite_B_9_termes_pos6:
  "terme_B_pos 2 2 9 6 = 128"
  unfolding terme_B_pos_def by simp

lemma suite_B_9_termes_pos7:
  "terme_B_pos 2 2 9 7 = 256"
  unfolding terme_B_pos_def by simp

lemma suite_B_9_termes_pos9:
  "terme_B_pos 2 2 9 9 = 768"
  unfolding terme_B_pos_def by simp

(*  Suite B 10 termes : [2, 4, 8, 16, 32, 128, 256, 512, 768, 1536]           *)
lemma suite_B_10_termes_pos8:
  "terme_B_pos 2 2 10 8 = 512"
  unfolding terme_B_pos_def by simp

lemma suite_B_10_termes_pos10:
  "terme_B_pos 2 2 10 10 = 1536"
  unfolding terme_B_pos_def by simp

(* === XII.7. Validations numeriques formules fermees positives (k=2)         === *)
(*   Premier 11 = 5ieme positif : Somme A = 50, Somme B = 38                  *)

lemma somme_A_pos_11:
  "somme_A_pos_k 2 5 = 50"
  unfolding somme_A_pos_k_def alpha_A_k_def offset_A_k_def by simp

lemma somme_B_pos_11:
  "somme_B_pos_k 2 5 = 38"
  unfolding somme_B_pos_k_def alpha_B_k_def offset_B_k_def by simp

(* === XII.8. Validations numeriques formules fermees negatives (k=2)         === *)
(*   Premier -2 (1 terme) : 13/4 / 2^1 - 2 = 13/8 - 2 = -3/8                  *)
(*   Premier -5 (3 termes): 13/4 / 2^3 - 2 = 13/32 - 2 = -51/32 = -1.59375    *)
(*                                                                            *)
(*   Note Savard 2026-02-17 : la formule fermee pour les suites negatives    *)
(*   est telle que somme_A_neg(k, n) converge vers -offset_A(k) quand n -> +inf.*)
(*   Pour k=2 : somme_A_neg(2, n) = 3.25 / 2^n - 2, qui tend vers -2.         *)

lemma somme_A_neg_k_value:
  "somme_A_neg_k 2 n = 3.25 / (2 ^ n) - 2"
  unfolding somme_A_neg_k_def alpha_A_k_def offset_A_k_def by simp

lemma somme_A_neg_m2:
  "somme_A_neg_k 2 1 = -3/8"
  unfolding somme_A_neg_k_def alpha_A_k_def offset_A_k_def by simp

lemma somme_A_neg_m5:
  "somme_A_neg_k 2 3 = -51/32"
  unfolding somme_A_neg_k_def alpha_A_k_def offset_A_k_def by simp

(*   Premier -5 (3 termes) : Somme B negative = 6.5 / 2^3 - 66 = 13/16 - 66 = -1043/16 *)
lemma somme_B_neg_m5:
  "somme_B_neg_k 2 3 = -1043/16"
  unfolding somme_B_neg_k_def alpha_B_k_def offset_B_k_def by simp

(* Verification numerique : somme B negative pour -5 vaut -65.1875 = -1043/16 *)
lemma somme_B_neg_m5_decimal:
  "(-1043::real) / 16 = -65.1875"
  by simp

(* === XII.9. Rapport spectral 1/k_i universel (positif et negatif)            === *)

definition RsP_k :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_k k n1 n2 =
     (somme_A_pos_k k n1 - somme_A_pos_k k n2) /
     (somme_B_pos_k k n1 - somme_B_pos_k k n2)"

definition RsP_neg_k :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_neg_k k n1 n2 =
     (somme_A_neg_k k n1 - somme_A_neg_k k n2) /
     (somme_B_neg_k k n1 - somme_B_neg_k k n2)"


(****************************************************************************
 * SECTION XIII. LE PONT LOGIQUE SAVARD : CHEBYSHEV <-> SPECTRAL <-> RH
 *
 * Auteur      : Philippe Thomas Savard
 * Date        : Juillet 2026
 * Lieu        : Lévis, Chaudière-Appalaches, Canada
 * Licence     : Apache 2.0
 *
 * Cette section établit formellement le double pont logique de manière
 * DIRECTE et CONSTRUCTIVE, sans aucun postulat abstrait ni "sorry".
 ****************************************************************************)

(****************************************************************************
 * SECTION XIII. LE PONT LOGIQUE SAVARD : CHEBYSHEV <-> SPECTRAL <-> RH
 ****************************************************************************)


end
