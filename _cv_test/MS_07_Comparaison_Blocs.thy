(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Validation principale methode_spectral.thy — section 7/14
   Fichier : MS_07_Comparaison_Blocs.thy  (section : Comparaison asymetrique + Blocs A_k B_k)
   Origine : methode_spectral.thy lignes 1205-1658 (verbatim phase 1, sans perte)
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
theory MS_07_Comparaison_Blocs
  imports MS_06_Mixtes_Negatives_Asymetries
begin

(* TOC locale (origine) :
   L1205 : Methode de comparaison asymetrique pour 1/2 et 1/4
   L1391 : Blocs A_k / B_k et rapport spectral de blocs (v3.43)
*)

section "Methode de comparaison asymetrique pour 1/2 et 1/4"

text \<open>
  La methode de comparaison asymetrique relie :

  - des suites de nombres premiers A et B (via leurs indices n),
  - les equations generales des suites A et B (SA, SB pour 1/2 ; A_1_4, B_1_4 pour 1/4),
  - et un rapport spectral construit a partir des sommes de blocs.

  Les puissances utilisees dans les equations generales sont egales
  aux positions (indices) des termes dans les suites, ou a la longueur
  des blocs consideres. La methode est applicable a tout ensemble
  de nombres premiers dont la position correspond aux puissances
  des equations generales A et B.
\<close>
(**************************************************************)
(* 1. Version nat des asymetries (indices naturels)           *)
(**************************************************************)

text \<open>
  Les definitions asymetrique_ordonnee et asymetrique_chaotique
  existent deja pour des listes d'entiers (int). Pour travailler
  directement avec les indices naturels des suites SA, SB, A_1_4
  et B_1_4, on introduit une version analogue sur nat.
\<close>
definition indice_valide_nat :: "nat => bool" where
  "indice_valide_nat n = (n > 0)"

definition liste_strictement_croissante_nat :: "nat list => bool" where
  "liste_strictement_croissante_nat xs =
      (ALL i j. i < j  &  j < length xs --> xs ! i < xs ! j)"

definition asymetrique_ordonnee_nat :: "nat list => nat list => bool" where
  "asymetrique_ordonnee_nat A_indices B_indices =
      ((ALL n : set A_indices. indice_valide_nat n)  &
       (ALL n : set B_indices. indice_valide_nat n)  &
       liste_strictement_croissante_nat A_indices  &
       liste_strictement_croissante_nat B_indices  &
       A_indices ~= []  &
       B_indices ~= []  &
       last A_indices < hd B_indices  &
       length B_indices = length A_indices + 1)"

definition asymetrique_chaotique_nat :: "nat list => nat list => bool" where
  "asymetrique_chaotique_nat A_indices B_indices =
      ((ALL n : set A_indices. indice_valide_nat n)  &
       (ALL n : set B_indices. indice_valide_nat n)  &
       length A_indices ~= length B_indices  &
       ~ asymetrique_ordonnee_nat A_indices B_indices)"

lemma asymetrie_nat_implique_indices_valides :
  assumes "asymetrique_ordonnee_nat A_indices B_indices  |
           asymetrique_chaotique_nat A_indices B_indices"
  shows "(ALL n : set A_indices. indice_valide_nat n)  &
         (ALL n : set B_indices. indice_valide_nat n)"
proof -
  from assms show ?thesis
  proof (elim disjE)
    assume h1: "asymetrique_ordonnee_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_nat_def by auto
  next
    assume h2: "asymetrique_chaotique_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_nat_def by auto
  qed
qed


(**************************************************************)
(* 2. Methode de comparaison asymetrique pour le modele 1/2   *)
(**************************************************************)

text \<open>
  Pour le modele 1/2, on utilise les suites SA et SB deja definies :

    SA n = (3.25 / 2) * 2^n - 2
    SB n = (6.5 / 2) * 2^n - 66

  La methode de comparaison asymetrique travaille sur des blocs
  d'indices A_indices et B_indices, qui correspondent a des positions
  dans les suites de nombres premiers. On construit un rapport
  spectral de blocs a partir des sommes des valeurs SA et SB.
\<close>
definition somme_SA_bloc :: "nat list => real" where
  "somme_SA_bloc A_indices = sum_list (map SA A_indices)"

definition somme_SB_bloc :: "nat list => real" where
  "somme_SB_bloc B_indices = sum_list (map SB B_indices)"

text \<open>
  Rapport spectral de blocs pour le modele 1/2 :
  on compare la difference des sommes de deux blocs A et B
  pour SA et SB, comme dans l'exemple (11 - 50) / (-40 - 38).
\<close>
definition RsP_bloc_1_2 :: "nat list => nat list => real" where
  "RsP_bloc_1_2 A_indices B_indices =
     (somme_SA_bloc A_indices - somme_SA_bloc B_indices) /
     (somme_SB_bloc A_indices - somme_SB_bloc B_indices)"

text \<open>
  Comparaison asymetrique ordonnee (modele 1/2) :
  - A_indices et B_indices sont strictement croissants,
  - les indices sont valides (n > 0),
  - B contient exactement un element de plus que A,
  - les puissances associees aux equations generales sont donc
    dans l'ordre naturel et decalees d'une unite.
\<close>
definition comparaison_asym_ordonnee_1_2 :: "nat list => nat list => bool" where
  "comparaison_asym_ordonnee_1_2 A_indices B_indices =
     asymetrique_ordonnee_nat A_indices B_indices"

text \<open>
  Comparaison asymetrique chaotique (modele 1/2) :
  - A_indices et B_indices ont des longueurs differentes,
  - l'ordre croissant naturel n'est pas impose,
  - les puissances associees aux equations generales ne sont pas
    necessairement consecutives.
\<close>
definition comparaison_asym_chaotique_1_2 :: "nat list => nat list => bool" where
  "comparaison_asym_chaotique_1_2 A_indices B_indices =
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  La methode de comparaison asymetrique pour le modele 1/2
  consiste donc a :
  - choisir deux blocs A_indices et B_indices,
  - verifier s'ils sont en configuration asymetrique ordonnee
    ou chaotique,
  - calculer le rapport RsP_bloc_1_2 A_indices B_indices.

  Ce rapport est numeriquement tres proche de 1/2 dans le regime
  chaotique, et evolue vers 1 dans certaines configurations
  asymetriques ordonnees lorsque la taille des blocs augmente.
  Ces comportements sont observes numeriquement et interpretes
  comme signatures spectrales, sans etre derives algebriquement.
\<close>
(**************************************************************)
(* 3. Methode de comparaison asymetrique pour le modele 1/4   *)
(**************************************************************)

text \<open>
  Pour le modele 1/4, on utilise les suites A_1_4 et B_1_4 :

    A_1_4 n = ((241/16)/12) * 4^n - 4/3
    B_1_4 n = ((964/16)/12) * 4^n - (3073 * (4/3))

  On applique la meme methode de comparaison asymetrique,
  cette fois avec ces equations generales.
\<close>
definition somme_A_1_4_bloc :: "nat list => real" where
  "somme_A_1_4_bloc A_indices = sum_list (map A_1_4 A_indices)"

definition somme_B_1_4_bloc :: "nat list => real" where
  "somme_B_1_4_bloc B_indices = sum_list (map B_1_4 B_indices)"

definition RsP_bloc_1_4 :: "nat list => nat list => real" where
  "RsP_bloc_1_4 A_indices B_indices =
     (somme_A_1_4_bloc A_indices - somme_A_1_4_bloc B_indices) /
     (somme_B_1_4_bloc A_indices - somme_B_1_4_bloc B_indices)"

definition comparaison_asym_ordonnee_1_4 :: "nat list => nat list => bool" where
  "comparaison_asym_ordonnee_1_4 A_indices B_indices =
     asymetrique_ordonnee_nat A_indices B_indices"

definition comparaison_asym_chaotique_1_4 :: "nat list => nat list => bool" where
  "comparaison_asym_chaotique_1_4 A_indices B_indices =
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  Comme pour le modele 1/2, la methode de comparaison asymetrique
  pour le modele 1/4 s'applique a tout ensemble de nombres premiers
  dont les positions (indices) correspondent aux puissances utilisees
  dans les equations generales A_1_4 et B_1_4.

  Les configurations asymetriques ordonnees et chaotiques permettent
  d'observer numeriquement des rapports proches de 1/4 ou evoluant
  vers 1, sans que ces valeurs puissent etre obtenues par une
  simplification algebrique directe des equations generales.
\<close>

(**************************************************************)
(* SECTION : Blocs A_k / B_k - Comparaison asym. ordonnee     *)
(*          + chaotique + extension complexe (v3.43)          *)
(**************************************************************)

section "Blocs A_k / B_k et rapport spectral de blocs (v3.43)"

text \<open>
  ==========================================================================
  BLOCS A_k, B_k ET COMPARAISONS ASYMETRIQUES ORDONNEES / CHAOTIQUES
  ==========================================================================

  Cette section formalise les equations manuscrites de Philippe Thomas
  Savard portant sur les blocs A_k et B_k (comparaison asymetrique
  ordonnee) et sur les blocs chaotiques (comparaison ponderee avec
  reels ou complexes).

  1. DEFINITION DES BLOCS.

     Soit (a_i)_{i>=1} et (b_j)_{j>=1} deux familles de reels (dans le
     regime reel) ou de complexes (dans le regime etendu XIII.4.b).
     Pour un indice de bloc k>=1 :

        Bloc A_k = { a_1, a_2, ..., a_k }              (k termes)
        Bloc B_k = { b_1, b_2, ..., b_k, b_{k+1} }     (k+1 termes)

     Le bloc B_k porte volontairement UN terme de plus que A_k : c'est
     l'asymetrie structurelle qui caracterise la Methode Spectrale.

  2. COMPARAISON ASYMETRIQUE ORDONNEE.

     Les indices sont ranges dans l'ordre naturel des positions
     premieres. Le rapport spectral de blocs est defini par la
     difference des sommes rapportee au denominateur B :

        RsP_bloc(k) = (sum_{i=1..k} a_i - sum_{j=1..k+1} b_j)
                    / (sum_{j=1..k+1} b_j)

     Une variante utile pour l'analyse de l'asymetrie porte
     uniquement sur les extremites (a_k et b_{k+1}) :

        RsP_bloc_extreme(k) = (a_k - b_{k+1}) / (SB_bloc(k))

     ou SB_bloc(k) = sum_{j=1..k+1} b_j est la somme totale du bloc B.

     NOTE IMPORTANTE : ces deux formes NE SONT PAS numeriquement
     egales au rapport historique RsP(n1, n2) = (SA(n1) - SA(n2))
     / (SB(n1) - SB(n2)) demontre a 1/2 par RsP_un_demi_general.
     Elles decrivent une observable spectrale DIFFERENTE (la
     comparaison de blocs entiers, pas de deux positions). Leur
     valeur numerique depend des suites (a, b) choisies et n'est
     PAS forcee a 1/2 par la construction. Le lien avec le regime
     central 1/2 se fait EXCLUSIVEMENT via le theoreme
     RsP_un_demi_general pour la forme de difference historique.

  3. COMPARAISON ASYMETRIQUE CHAOTIQUE.

     Les indices ne suivent plus l'ordre naturel : on prend deux
     permutations sigma : {1..k} -> Nat et tau : {1..k+1} -> Nat des
     positions premieres. Le fonctionnel spectral pondere est

        S(A_k, B_k) = (sum_i alpha_i * p_{sigma(i)})
                    / (sum_j beta_j * p_{tau(j)})

     ou (alpha_i), (beta_j) sont des ponderations reelles (ou
     complexes dans le regime XIII.4.b). La comparaison asymetrique
     chaotique s'ecrit alors S(A_k, B_k) = c ou c est une constante
     reelle ou complexe (typiquement proche de 1/2).

  4. EXTENSION COMPLEXE.

     Voir subsection XIII.4.b pour la construction detaillee. En
     substituant p_i^s = |p_i|^sigma * exp(i*t*ln|p_i|) (Dirichlet),
     le fonctionnel S devient complexe et son invariance se transporte
     sur la partie reelle : Re(RsP_bloc_complexe) = 1/2.

  Les definitions HOL ci-dessous formalisent (1) et (2) au niveau
  reel ; (3) est capture par la definition ponderee ; (4) est
  documente en text-bloc et reliee au theoreme
  pont_spectral_direct_final de la Section XIII.
  --------------------------------------------------------------------------
\<close>

(* Bloc A_k : liste des k premiers termes de la suite a *)
definition bloc_A_k :: "(nat \<Rightarrow> real) \<Rightarrow> nat \<Rightarrow> real list" where
  "bloc_A_k a k = map a [1..<k+1]"

(* Bloc B_k : liste des k+1 premiers termes de la suite b *)
definition bloc_B_k :: "(nat \<Rightarrow> real) \<Rightarrow> nat \<Rightarrow> real list" where
  "bloc_B_k b k = map b [1..<k+2]"

(* Somme d'un bloc *)
definition somme_bloc :: "real list \<Rightarrow> real" where
  "somme_bloc xs = sum_list xs"

(* Rapport spectral de blocs (forme generale) *)
definition RsP_bloc :: "(nat \<Rightarrow> real) \<Rightarrow> (nat \<Rightarrow> real) \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_bloc a b k =
     (somme_bloc (bloc_A_k a k) - somme_bloc (bloc_B_k b k))
     / somme_bloc (bloc_B_k b k)"

(* Version "extremites" : (a_k - b_{k+1}) / SB_bloc(k) *)
definition RsP_bloc_extreme :: "(nat \<Rightarrow> real) \<Rightarrow> (nat \<Rightarrow> real) \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_bloc_extreme a b k =
     (a k - b (k+1)) / somme_bloc (bloc_B_k b k)"

(* Cardinalites : |A_k| = k, |B_k| = k+1 (asymetrie structurelle) *)
lemma card_bloc_A_k: "length (bloc_A_k a k) = k"
  unfolding bloc_A_k_def by simp

lemma card_bloc_B_k: "length (bloc_B_k b k) = k + 1"
  unfolding bloc_B_k_def by simp

lemma asymetrie_structurelle_blocs:
  "length (bloc_B_k b k) = length (bloc_A_k a k) + 1"
  unfolding bloc_A_k_def bloc_B_k_def by simp

(* Cas de base : bloc de taille 1 *)
lemma bloc_A_1_singleton: "bloc_A_k a 1 = [a 1]"
  unfolding bloc_A_k_def by simp

lemma bloc_B_1_paire: "bloc_B_k b 1 = [b 1, b 2]"
  by (simp add: bloc_B_k_def numeral_2_eq_2)

(* Somme du bloc B a l'ordre 1 : somme_bloc [b 1, b 2] = b 1 + b 2.
   Preuve directe (unfolding complet) pour eviter la dependance
   transitive a bloc_B_1_paire qui pouvait etre fragile en simp. *)
lemma somme_bloc_B_1: "somme_bloc (bloc_B_k b 1) = b 1 + b 2"
  by (simp add: somme_bloc_def bloc_B_k_def numeral_2_eq_2)

(* Identite du rapport extreme pour k=1 *)
lemma RsP_bloc_extreme_at_1:
  assumes "b 1 + b 2 \<noteq> 0"
  shows "RsP_bloc_extreme a b 1 = (a 1 - b 2) / (b 1 + b 2)"
  using assms
  by (simp add: RsP_bloc_extreme_def somme_bloc_def bloc_B_k_def numeral_2_eq_2)

(* -----------------------------------------------------------------------
   FONCTIONNEL SPECTRAL PONDERE (comparaison chaotique)
   ----------------------------------------------------------------------- *)

text \<open>
  Le fonctionnel spectral pondere prend deux listes de reels : les
  ponderations `alphas` (pour le bloc A) et `betas` (pour le bloc B),
  ainsi que les listes des valeurs a_i et b_j eventuellement
  permutees. Il retourne le rapport (sum alpha_i * a_i) / (sum beta_j * b_j).
\<close>

definition ponderation_bloc :: "real list \<Rightarrow> real list \<Rightarrow> real" where
  "ponderation_bloc coeffs valeurs =
     sum_list (map2 (\<lambda>c v. c * v) coeffs valeurs)"

definition S_pondere :: "real list \<Rightarrow> real list \<Rightarrow>
                         real list \<Rightarrow> real list \<Rightarrow> real" where
  "S_pondere alphas a_vals betas b_vals =
     ponderation_bloc alphas a_vals / ponderation_bloc betas b_vals"

(* Poids unitaires : la ponderation degenere en somme simple *)
lemma ponderation_bloc_uniforme:
  "length coeffs = length valeurs \<Longrightarrow>
   (\<forall>c \<in> set coeffs. c = 1) \<Longrightarrow>
   ponderation_bloc coeffs valeurs = sum_list valeurs"
  unfolding ponderation_bloc_def
  by (induction coeffs valeurs rule: list_induct2) auto

(* Cas trivial de la comparaison chaotique avec poids unitaires :
   le fonctionnel se ramene au rapport des sommes brutes. *)
lemma S_pondere_uniforme:
  assumes "length alphas = length a_vals"
      and "length betas  = length b_vals"
      and "\<forall>c \<in> set alphas. c = 1"
      and "\<forall>c \<in> set betas.  c = 1"
      and "sum_list b_vals \<noteq> 0"
  shows "S_pondere alphas a_vals betas b_vals = sum_list a_vals / sum_list b_vals"
  unfolding S_pondere_def
  using ponderation_bloc_uniforme[OF assms(1) assms(3)]
        ponderation_bloc_uniforme[OF assms(2) assms(4)]
  by simp

text \<open>
  EXTENSION COMPLEXE (parallele a XIII.4.b) - formalisation HOL.

  Dans le regime complexe, les ponderations sont des elements du
  type `complex` (fourni par Complex_Main, deja importe en tete du
  fichier). Le fonctionnel S_pondere_complexe se transporte
  identiquement dans Complex_Main et son invariance sur la partie
  reelle se lit :

    Re(S_complexe(A_k, B_k)) = 1/2  pour s sur la droite critique.
\<close>

(* Ponderation complexe : identique a la version reelle mais sur le
   corps des complexes. Complex_Main est deja importe en tete. *)
definition ponderation_bloc_complexe :: "complex list \<Rightarrow> complex list \<Rightarrow> complex" where
  "ponderation_bloc_complexe coeffs valeurs =
     sum_list (map2 (\<lambda>c v. c * v) coeffs valeurs)"

definition S_pondere_complexe :: "complex list \<Rightarrow> complex list \<Rightarrow>
                                   complex list \<Rightarrow> complex list \<Rightarrow> complex" where
  "S_pondere_complexe alphas a_vals betas b_vals =
     ponderation_bloc_complexe alphas a_vals /
     ponderation_bloc_complexe betas b_vals"

(* Poids unitaires complexes : le fonctionnel degenere en somme simple *)
lemma ponderation_bloc_complexe_uniforme:
  "length coeffs = length valeurs \<Longrightarrow>
   (\<forall>c \<in> set coeffs. c = 1) \<Longrightarrow>
   ponderation_bloc_complexe coeffs valeurs = sum_list valeurs"
  unfolding ponderation_bloc_complexe_def
  by (induction coeffs valeurs rule: list_induct2) auto

(* Injection reel -> complexe : la version complexe restreinte aux
   reels retrouve la version reelle. *)
lemma ponderation_bloc_complexe_of_real:
  "ponderation_bloc_complexe (map complex_of_real cs) (map complex_of_real vs)
   = complex_of_real (ponderation_bloc cs vs)"
proof (induction cs vs rule: list_induct2')
  case 1 show ?case
    by (simp add: ponderation_bloc_complexe_def ponderation_bloc_def)
next
  case (2 c cs) show ?case
    by (simp add: ponderation_bloc_complexe_def ponderation_bloc_def)
next
  case (3 v vs) show ?case
    by (simp add: ponderation_bloc_complexe_def ponderation_bloc_def)
next
  case (4 c cs v vs) thus ?case
    by (simp add: ponderation_bloc_complexe_def ponderation_bloc_def)
qed

text \<open>
  Cette section documente et formalise TROIS niveaux :
  1. Reel (definitions ponderation_bloc / S_pondere + lemmes).
  2. Complexe (definitions ponderation_bloc_complexe / S_pondere_complexe
     + lemme d'injection reel -> complexe).
  3. Le passage explicite s = sigma + i*t (series de Dirichlet) et le
     transport Re(RsP_complexe) = 1/2 est adresse en Section XIII.4.b
     (extension chaotique, asymetrique et complexe) via le theoreme
     pont_spectral_direct_final. La construction complete des series
     de Dirichlet requiert HOL-Analysis / HOL-Complex_Analysis et
     depasse le cadre de ce fichier.

  --------------------------------------------------------------------------
  RELATION AVEC LE THEOREME RsP_un_demi_general :

  Le regime central 1/2 est etabli EXCLUSIVEMENT pour le rapport
  de difference historique RsP(n1, n2) = (SA(n1)-SA(n2))/(SB(n1)-SB(n2))
  (theoreme RsP_un_demi_general). Le rapport de blocs RsP_bloc(k) et
  ses variantes definis ci-dessus decrivent une observable
  spectrale DIFFERENTE (comparaison de blocs entiers). Leur valeur
  numerique depend des suites (a, b) choisies et n'est PAS forcee a 1/2
  par la construction. Aucun lemme HOL ne pretend le contraire.
\<close>

(* Ancrage syntaxique : quand a = SA et b = SB, les blocs se
   deplient en listes explicites de SA et SB (pure identite de map).
   ATTENTION : ceci ne signifie PAS que RsP_bloc(k) sur SA/SB vaut
   1/2 (contre-exemple exact a k=1 : RsP_bloc(1) = -91/90). Le
   regime central 1/2 est etabli EXCLUSIVEMENT par RsP_un_demi_general
   pour la forme de difference historique (SA(n1)-SA(n2))/(SB(n1)-SB(n2)). *)
lemma bloc_A_k_pour_SA:
  "bloc_A_k SA k = map SA [1..<k+1]"
  by (simp add: bloc_A_k_def)

lemma bloc_B_k_pour_SB:
  "bloc_B_k SB k = map SB [1..<k+2]"
  by (simp add: bloc_B_k_def)


(**************************************************************)
(* SECTION : Rapport spectral 1/3 negatif (axiomatisation)     *)
(**************************************************************)


end
