theory geometrie_spectre_premier
  imports Complex_Main
begin

text "Formalisation de base de la methode spectrale (rapport 1/2)."

definition Z :: real where
  "Z = 64"

definition SA :: "nat => real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

definition SB :: "nat => real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"

definition D :: "nat => real => real" where
  "D n P = SB n - SA n - Z * P"

definition Dc :: "nat => real => real" where
  "Dc n P = SA n + D n P"

definition P_reconstruit :: "nat => real => real" where
  "P_reconstruit n P = (SB n - Dc n P) / Z"

lemma reconstruction_P:
  fixes n :: nat
  fixes P :: real
  shows "P_reconstruit n P = P"
proof -
  have "P_reconstruit n P =
        (SB n - (SA n + (SB n - SA n - Z * P))) / Z"
    unfolding P_reconstruit_def Dc_def D_def by simp
  also have "... = (SB n - SA n - SB n + SA n + Z * P) / Z"
    by simp
  also have "... = (Z * P) / Z"
    by simp
  also have "... = P"
    unfolding Z_def by simp
  finally show ?thesis .
qed

text \<open>
  Définition générale : un bloc spectral est une liste d’indices
  permettant de former une Somme A ou une Somme B.
\<close>

definition SommeA :: "nat list \<Rightarrow> real" where
  "SommeA ns = (\<Sum>n\<leftarrow>ns. SA n)"

definition SommeB :: "nat list \<Rightarrow> real" where
  "SommeB ns = (\<Sum>n\<leftarrow>ns. SB n)"

text \<open>
  ----------------------------------------------------------------------
  1. Comparaison SPECTRALE SYMÉTRIQUE 1\<times>1
  ----------------------------------------------------------------------
  Deux positions (par exemple deux premiers) sont comparées directement.
  On ne fixe aucune équation : seulement la structure 1\<times>1.
\<close>

record comparaison_1x1 =
  posA :: nat
  posB :: nat

definition est_symetrique_1x1 :: "comparaison_1x1 \<Rightarrow> bool" where
  "est_symetrique_1x1 c \<longleftrightarrow> (posA c \<noteq> posB c)"

text \<open>
  ----------------------------------------------------------------------
  2. Comparaison SPECTRALE SYMÉTRIQUE n\<times>n
  ----------------------------------------------------------------------
  On compare deux blocs de Sommes A et deux blocs de Sommes B :
    - Bloc A  (Sommes A1, A2, ..., An1)
    - Bloc B  (Sommes A3, A4, ..., An2)
    - Bloc C  (Sommes B1, B2, ..., Bn1)
    - Bloc D  (Sommes B3, B4, ..., Bn2)

  Conditions structurelles :
    - Bloc A et Bloc B ont même cardinalité
    - Bloc C et Bloc D ont même cardinalité
    - Les blocs sont distincts
  Aucune équation n’est imposée ici.
\<close>

record comparaison_nxn =
  NA :: "nat list"
  NB :: "nat list"
  NC :: "nat list"
  ND :: "nat list"

definition est_symetrique_nxn :: "comparaison_nxn \<Rightarrow> bool" where
  "est_symetrique_nxn c \<longleftrightarrow>
     length (NA c) = length (NB c) \<and>
     length (NC c) = length (ND c) \<and>
     NA c \<noteq> NB c \<and>
     NC c \<noteq> ND c"

text \<open>
  ----------------------------------------------------------------------
  3. Comparaison ASYMÉTRIQUE ORDONNÉE
  ----------------------------------------------------------------------
  Règles structurelles :
    1. Bloc B est un décalage de Bloc A (indices plus grands)
    2. Bloc D est un décalage de Bloc C
    3. Les blocs sont strictement croissants (ordre chronologique)
    4. Bloc A et Bloc C ont même structure
       Bloc B et Bloc D ont même structure

  Aucune équation n’est donnée : seulement la structure ordonnée.
\<close>

definition est_croissante :: "nat list \<Rightarrow> bool" where
  "est_croissante ns \<longleftrightarrow> (\<forall>i<length ns - 1. ns ! i < ns ! (i+1))"

record comparaison_asym_ordonnee =
  AO :: "nat list"
  BO :: "nat list"
  CO :: "nat list"
  DO :: "nat list"

definition est_asym_ordonnee :: "comparaison_asym_ordonnee \<Rightarrow> bool" where
  "est_asym_ordonnee c \<longleftrightarrow>
     est_croissante (AO c) \<and>
     est_croissante (BO c) \<and>
     est_croissante (CO c) \<and>
     est_croissante (DO c) \<and>
     (\<forall>a\<in>set (AO c). \<forall>b\<in>set (BO c). a < b) \<and>
     (\<forall>a\<in>set (CO c). \<forall>d\<in>set (DO c). a < d)"

text \<open>
  ----------------------------------------------------------------------
  4. Comparaison ASYMÉTRIQUE CHAOTIQUE
  ----------------------------------------------------------------------
  Structure :
    - Bloc A chaotique différent de Bloc B
    - Bloc B chaotique différent de Bloc D
    - Bloc A = Bloc C (même indices)
    - Bloc B = Bloc D (même indices)

  Aucune équation n’est donnée : seulement la structure chaotique.
\<close>

record comparaison_asym_chaotique =
  AC :: "nat list"
  BC :: "nat list"

definition est_asym_chaotique :: "comparaison_asym_chaotique \<Rightarrow> bool" where
  "est_asym_chaotique c \<longleftrightarrow> AC c \<noteq> BC c"

text \<open>
  Extension signée des suites A et B :
  - pour n > 0 : on retrouve les définitions SA et SB existantes
  - pour n < 0 : on utilise les variantes négatives données dans la méthode.
\<close>

definition SA_signed :: "int \<Rightarrow> real" where
  "SA_signed k =
     (if k > 0 then (3.25 / 2) * (2 ^ nat k) - 2
      else (3.25) * ((2::real) powi k) - 2)"

definition SB_signed :: "int \<Rightarrow> real" where
  "SB_signed k =
     (if k > 0 then (6.5 / 2) * (2 ^ nat k) - 66
      else (6.5) * ((2::real) powi k) - 66)"

lemma SA_signed_pos:
  assumes "k > 0"
  shows "SA_signed k = SA (nat k)"
  using assms
  by (simp add: SA_signed_def SA_def)

lemma SB_signed_pos:
  assumes "k > 0"
  shows "SB_signed k = SB (nat k)"
  using assms
  by (simp add: SB_signed_def SB_def)

text \<open>
  Exemple pour le nombre premier négatif -5 (3ᵉ nombre premier négatif).
\<close>

lemma SA_signed_moins_3:
  "SA_signed (-3) = (3.25 * ((2::real) powi (-3))) - 2"
  by (simp add: SA_signed_def)

lemma SA_signed_moins_3_valeur:
  "SA_signed (-3) = -1.59375"
  by (simp add: SA_signed_def)


lemma SB_signed_moins_3:
  "SB_signed (-3) = (6.5 * ((2::real) powi (-3))) - 66"
  by (simp add: SB_signed_def)

lemma SB_signed_moins_3_valeur:
  "SB_signed (-3) = -65.1875"
  by (simp add: SB_signed_def)

text \<open>
  Exemple pour le nombre premier 11 (5ᵉ nombre premier positif).
\<close>

lemma SA_5_11:
  "SA 5 = 50"
  by (simp add: SA_def)

definition suiteA_11 :: "real list" where
  "suiteA_11 = [2, 4, 8, 12, 24]"

lemma somme_suiteA_11:
  "sum_list suiteA_11 = SA 5"
  by (simp add: suiteA_11_def SA_def)

lemma SB_5_11:
  "SB 5 = 38"
  by (simp add: SB_def)

definition suiteB_11 :: "real list" where
  "suiteB_11 = [-59.5, 6.5, 13, 26, 52]"

lemma somme_suiteB_11:
  "sum_list suiteB_11 = SB 5"
  by (simp add: suiteB_11_def SB_def)

text \<open>
  Suites A explicites pour 1 à 11 termes.
\<close>

definition suiteA_1 :: "real list" where
  "suiteA_1 = [2]"

definition suiteA_2 :: "real list" where
  "suiteA_2 = [2, 3]"

definition suiteA_3 :: "real list" where
  "suiteA_3 = [2, 3, 6]"

definition suiteA_4 :: "real list" where
  "suiteA_4 = [2, 4, 6, 12]"

definition suiteA_5' :: "real list" where
  "suiteA_5' = [2, 4, 8, 12, 24]"

definition suiteA_6 :: "real list" where
  "suiteA_6 = [2, 4, 8, 16, 24, 48]"

definition suiteA_7 :: "real list" where
  "suiteA_7 = [2, 4, 8, 16, 32, 48, 96]"

definition suiteA_8 :: "real list" where
  "suiteA_8 = [2, 4, 8, 16, 32, 64, 96, 192]"

definition suiteA_9 :: "real list" where
  "suiteA_9 = [2, 4, 8, 16, 32, 64, 128, 192, 384]"

definition suiteA_10 :: "real list" where
  "suiteA_10 = [2, 4, 8, 16, 32, 64, 128, 256, 384, 768]"

definition suiteA_11' :: "real list" where
  "suiteA_11' = [2, 4, 8, 16, 32, 64, 128, 256, 512, 768, 1536]"

lemma somme_suiteA_5':
  "sum_list suiteA_5' = SA 5"
  by (simp add: suiteA_5'_def SA_def)

lemma somme_suiteA_11':
  "sum_list suiteA_11' = SA 11"
  by (simp add: suiteA_11'_def SA_def)

text \<open>
  Suites B explicites pour 1 à 7 termes (partie négative).
\<close>

definition suiteB_1 :: "real list" where
  "suiteB_1 = [-59.5]"

definition suiteB_2 :: "real list" where
  "suiteB_2 = [-59.5, 6.5]"

definition suiteB_3 :: "real list" where
  "suiteB_3 = [-59.5, 6.5, 13]"

definition suiteB_4 :: "real list" where
  "suiteB_4 = [-59.5, 6.5, 13, 26]"

definition suiteB_5' :: "real list" where
  "suiteB_5' = [-59.5, 6.5, 13, 26, 52]"

definition suiteB_6 :: "real list" where
  "suiteB_6 = [-59.5, 6.5, 13, 26, 52, 104]"

definition suiteB_7 :: "real list" where
  "suiteB_7 = [-59.5, 6.5, 13, 26, 52, 104, 208]"

text \<open>
  Suites B explicites pour 8 termes et plus (partie positive).
\<close>

definition suiteB_8 :: "real list" where
  "suiteB_8 = [2, 4, 8, 16, 32, 128, 192, 384]"

definition suiteB_9 :: "real list" where
  "suiteB_9 = [2, 4, 8, 16, 32, 128, 256, 384, 768]"

definition suiteB_10 :: "real list" where
  "suiteB_10 = [2, 4, 8, 16, 32, 128, 256, 512, 768, 1536]"

lemma somme_suiteB_5':
  "sum_list suiteB_5' = SB 5"
  by (simp add: suiteB_5'_def SB_def)

lemma somme_suiteB_8:
  "sum_list suiteB_8 = SB 8"
  by (simp add: suiteB_8_def SB_def)


end
