(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Validation principale methode_spectral.thy — section 10/14
   Fichier : MS_10_Ecarts_Mixtes_Positifs.thy  (section : Ecarts mixtes (-31 / 17) + Ecarts 1-3 (227 / 173) + Ecarts 1-4 (947 / 881))
   Origine : methode_spectral.thy lignes 2308-2630 (verbatim phase 1, sans perte)
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
theory MS_10_Ecarts_Mixtes_Positifs
  imports MS_09_Preuve_Absurde
begin

(* TOC locale (origine) :
   L2308 : Exemple complet : ecart entre -31 et 17
   L2319 : Valeurs spectrales exactes pour -31 et 17
   L2341 : Forme generale de l'ecart mixte
   L2353 : Demonstration finale : ecart -31 / 17
   L2365 : Valeurs spectrales exactes pour 23 et 7
   L2378 : Note sur l'inclusion du zero dans les ecarts spectraux
   L2389 : Exemple complet : ecart entre les premiers 227 et 173 (rapport 1/3)
   L2425 : Valeurs spectrales exactes pour 227 et 173 (1/3)
   L2450 : Validation numerique de l'ecart entre 227 et 173 (1/3)
   L2461 : Equation generale d'ecart pour le rapport spectral 1/3
   L2528 : Validation de l'exemple 227 / 173 via l'equation generale 1/3
   L2541 : Valeurs spectrales exactes pour 947 et 881 (1/4)
   L2560 : Equation generale d'ecart pour le rapport spectral 1/4
   L2609 : Validation de l'exemple 947 / 881 via l'equation generale 1/4
*)

section "Exemple complet : ecart entre -31 et 17"

definition n_m29 :: real where "n_m29 = -10"
definition n_p17 :: real where "n_p17 = 8"
definition n_m31 :: real where "n_m31 = -11"


(**************************************************************)
(* SECTION : Valeurs spectrales exactes (-31 et 17)           *)
(**************************************************************)

section "Valeurs spectrales exactes pour -31 et 17"

definition SA_m29_val :: real where
  "SA_m29_val = -40895 / 20480"

definition SB_p17_val :: real where
  "SB_p17_val = 350"

definition D_p17_val :: real where
  "D_p17_val = -738"

definition SB_m31_val :: real where
  "SB_m31_val = -1351615 / 20480"

definition D_m31_val :: real where
  "D_m31_val = 39280705 / 20480"


(**************************************************************)
(* SECTION : Forme generale de l'ecart mixte                  *)
(**************************************************************)

section "Forme generale de l'ecart mixte"

definition gap_mix_val ::
  "real => real => real => real => real => real" where
  "gap_mix_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* SECTION : Lemme final - ecart -31 / 17                     *)
(**************************************************************)

section "Demonstration finale : ecart -31 / 17"

lemma gap_m31_17:
  "gap_mix_val SA_m29_val SB_p17_val D_p17_val D_m31_val 0 = -47"
  unfolding gap_mix_val_def
            SA_m29_val_def SB_p17_val_def
            D_p17_val_def D_m31_val_def
  by simp
(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 23 et 7          *)
(**************************************************************)

section "Valeurs spectrales exactes pour 23 et 7"

definition SA_11_val :: real where "SA_11_val = 50"
definition SB_23_val :: real where "SB_23_val = 1598"
definition D_23_val  :: real where "D_23_val = 126"
definition SB_7_val  :: real where "SB_7_val = -14"
definition D_7_val   :: real where "D_7_val = -464"


(**************************************************************)
(* SECTION : Note explicite sur l'inclusion du zero           *)
(**************************************************************)

section "Note sur l'inclusion du zero dans les ecarts spectraux"

text \<open>
  Le zero n'est inclus que dans les ecarts mixtes (exemple -31 / 17).
  Dans les ecarts du meme signe (-19 / -5 et 23 / 7), la progression
  spectrale ne traverse pas 0, donc il n'est pas compte.
\<close>
(**************************************************************)
(* SECTION : Exemple complet - ecart entre 227 et 173 (1/3)   *)
(**************************************************************)

section "Exemple complet : ecart entre les premiers 227 et 173 (rapport 1/3)"

text \<open>
  Exemple positif : quantite de nombres entre les deux premiers 227 et 173.

  Donnees spectrales :

    - Le premier suivant 173 est 179
    - Rang spectral de 227 : 10
    - Rang spectral de 173 : 1

  Valeurs numeriques :

    SA(227) = 79824
    SB(227) = 238746
    D(227)  = 73263

    SA(179) = 96/9

    SB(173) = -2155/3
    D(173)  = -1141518/9

  Formule generale (rapport 1/3) :

      (A_next - (B_high - D_high) - D_low) / 729

  Resultat :

      ((96/9) - (238746 - 73263) - (-1141518/9)) / 729 = -53

  Ce qui correspond aux 53 nombres entre 227 et 173.
\<close>
(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 227 et 173       *)
(**************************************************************)

section "Valeurs spectrales exactes pour 227 et 173 (1/3)"

definition SA_227_val :: real where
  "SA_227_val = 79824"

definition SB_227_val :: real where
  "SB_227_val = 238746"

definition D_227_val :: real where
  "D_227_val = 73263"

definition SA_179_val :: real where
  "SA_179_val = 96/9"

definition SB_173_val :: real where
  "SB_173_val = -2155/3"

definition D_173_val :: real where
  "D_173_val = -1141518/9"


(**************************************************************)
(* SECTION : Validation de l'ecart entre 227 et 173           *)
(**************************************************************)

section "Validation numerique de l'ecart entre 227 et 173 (1/3)"

lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)


(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/3    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/3"

text \<open>
  Formule generale pour l'ecart entre deux nombres premiers
  dans le modele spectral 1/3, a partir de deux suites A et B
  de n termes et de leurs Digamma associes.

  Forme generale (rapport 1/3) :

      (A_next - (B_high - D_high) - D_low) / 729

  ou :

    - A_next  : somme de la suite A pour le premier suivant du plus petit
    - B_high  : somme de la suite B pour le plus grand premier
    - D_high  : Digamma du plus grand premier
    - D_low   : Digamma du plus petit premier

  Le resultat correspond a la quantite de nombres entiers entre les deux premiers.
\<close>
definition gap_equation_1_3 :: "real => real => real => real => real" where
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 729"

lemma gap_equation_1_3_simplifiee:
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 729"
  unfolding gap_equation_1_3_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/3                    *)
(**************************************************************)

text \<open>
  Postulat spectral d'ecart pour le rapport 1/3 :

  Pour toute paire de nombres premiers (p_high, p_low),
  et pour leurs valeurs spectrales associees (A_next, B_high, D_high, D_low)
  construites selon le modele 1/3, l'equation d'ecart donne exactement
  la quantite de nombres entiers entre ces deux premiers :

      gap_equation_1_3 ... = p_low - p_high
\<close>
axiomatization where
  spectral_gap_postulate_1_3:
    "!!p_high p_low A_next B_high D_high D_low.
       prime p_high ==> prime p_low ==>
       gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* SECTION : Lemme general pour l'ecart entre deux premiers   *)
(**************************************************************)

lemma gap_equation_1_3_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_3 assms by blast


(**************************************************************)
(* SECTION : Lien avec l'exemple 227 / 173                    *)
(**************************************************************)

section "Validation de l'exemple 227 / 173 via l'equation generale 1/3"

lemma ecart_227_173_1_3_via_gap_equation:
  "gap_equation_1_3 SA_179_val SB_227_val D_227_val D_173_val = -53"
  by (simp add: gap_equation_1_3_def
                SA_179_val_def SB_227_val_def
                D_227_val_def D_173_val_def)


(**************************************************************)
(* SECTION : Valeurs spectrales exactes pour 947 et 881 (1/4) *)
(**************************************************************)

section "Valeurs spectrales exactes pour 947 et 881 (1/4)"

definition SA_883_val :: real where
  "SA_883_val = 75/4"

definition SB_947_val :: real where
  "SB_947_val = 5260628"

definition D_947_val :: real where
  "D_947_val = 1381716"

definition D_881_val :: real where
  "D_881_val = -(14450613/4)"


(**************************************************************)
(* SECTION : Equation generale d'ecart pour le rapport 1/4    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/4"

definition gap_equation_1_4 :: "real => real => real => real => real" where
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 4096"

lemma gap_equation_1_4_simplifiee:
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 4096"
  unfolding gap_equation_1_4_def by simp


(**************************************************************)
(* SECTION : Postulat spectral d'ecart 1/4                    *)
(**************************************************************)

text \<open>
  Postulat spectral d'ecart pour le rapport 1/4 :

  Pour toute paire de nombres premiers (p_high, p_low),
  et pour leurs valeurs spectrales associees (A_next, B_high, D_high, D_low)
  construites selon le modele 1/4, l'equation d'ecart donne exactement
  la quantite de nombres entiers entre ces deux premiers :

      gap_equation_1_4 ... = p_low - p_high
\<close>
axiomatization where
  spectral_gap_postulate_1_4:
    "!!p_high p_low A_next B_high D_high D_low.
       prime p_high ==> prime p_low ==>
       gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* SECTION : Lemme general pour l'ecart entre deux premiers   *)
(**************************************************************)

lemma gap_equation_1_4_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_4 assms by blast


(**************************************************************)
(* SECTION : Lien avec l'exemple 947 / 881                    *)
(**************************************************************)

section "Validation de l'exemple 947 / 881 via l'equation generale 1/4"

lemma ecart_947_881_1_4_via_gap_equation:
  "gap_equation_1_4 SA_883_val SB_947_val D_947_val D_881_val = -65"
  by (simp add: gap_equation_1_4_def
                SA_883_val_def SB_947_val_def
                D_947_val_def D_881_val_def)


(****************************************************************************
 * SECTION XI. REGLES DE CONSTRUCTION DES SUITES A_i / B_i (8+ TERMES)
 * POUR RAPPORT SPECTRAL RsP = 1/k_i
 *
 * Auteur      : Philippe Thomas Savard
 * Date        : 29 juin 2026
 * Lieu        : Lévis, Chaudière-Appalaches, Canada
 * Licence     : Apache 2.0 (Attribution et conservation des mentions requises)
 *
 * REGLES FORMALISEES SANS UTILISATION DE LA TACTIQUE 'RING'
 * Utilisation exclusive de: algebra_simps, field_simps et simplifications directes.
 ****************************************************************************)


end
