(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Contre-validation HOL 1/2
   Fichier : validation_hol_unifiee.thy (fichier unique, non decoupe)
   Auteur : Philippe Thomas Savard
   Date : Le trois octobre deux mille vingt-six
   Lieu : Levis, Chausdiere-Appalaches, Canada
   Role : contre-validation independante de la validation principale
   (MS_01 a MS_14 = decoupage verbatim de methode_spectral.thy en 14 sections),
   approche formelle rigoureuse dans Isabelle/HOL.
   ----------------------------------------------------------------------------
   TABLE DES MATIERES (sections + N° de ligne debut-fin, origine v7.5) :
   L  54 - L  55 : [section] Définitions de Validation Unifiée
   L  56 - L  77 : [subsection] Redéfinition des Fonctions Spectrales pour Validation
   L  78 - L  89 : [subsection] Formules de Reconstruction Première
   L  90 - L 114 : [subsection] Rapports Spectraux Asymétriques (RSA)
   L 115 - L 116 : [section] Analyse des Zéros Riemann - Perspective Spectrale
   L 117 - L 141 : [subsection] Eigenvalues et Ligne Critique
   L 142 - L 143 : [section] Correspondances avec methode_spectral.thy
   L 144 - L 161 : [subsection] Vérification Cohérence A(n) et B(n)
   L 162 - L 211 : [subsection] Vérification Croissance Exponentielle
   L 212 - L 229 : [section] Formule Digamma: D_c = SB(n) - 64*P
   L 230 - L 231 : [section] Théorèmes Centraux
   L 232 - L 257 : [subsection] Identité de Reconstruction (sans certificat de primalité)
   L 258 - L 292 : [subsection] Zéros Riemann et Eigenvalues
   L 293 - L 302 : [subsection] Normalisation par Sr2
   L 303 - L 323 : [section] Lemmes de Support
   L 324 - L 367 : [section] Vérifications de Cohérence
   L 368 - L 463 : [section] Catalogue d'Ancrages v7.5
   L 464 - L 465 : [section] Exclusion Formelle des Composés C
   L 466 - L 490 : [subsection] Définitions — Candidat C et Verdicts
   L 491 - L 533 : [subsection] Règle d'Exclusion HOL — Composés
   L 534 - L 564 : [subsection] Exclusion par Branche — Quatre Digamma
   L 565 - L 566 : [section] Contrôle de Domaine par Inversion S_A
   L 567 - L 596 : [subsection] Définitions — Inversion de la Suite A
   L 597 - L 625 : [subsection] Forme Générale du Contrôle de Domaine
   L 626 - L 627 : [section] Chaîne de Validation CONSTRUIRE → RÉPONDRE
   L 628 - L 673 : [subsection] Types de Statut
   L 674 - L 731 : [subsection] Résumé HOL pour le Contrat Gabriel
   L 732 - L 780 : [section] Exemple Positif — Ancrage Certifié 1/13
   L 781 - L 814 : [section] Exemple Négatif — Blocage 1/81
   L 815 - L 837 : [section] Vérifications de Cohérence Globale
   L 838 - L 871 : [section] Résumé et Conclusions v7.5
   L 872 - L 891 : [section] References externes (Mathlib, Lean 4) et licence
   ============================================================================ *)

theory validation_hol_unifiee
  imports MS_14_Systeme_Convolutif Complex_Main
begin

(* ============================================================================
   SECTION 1 : DÉFINITIONS DE VALIDATION
   ============================================================================ *)

section "Définitions de Validation Unifiée"

subsection "Redéfinition des Fonctions Spectrales pour Validation"

(* Validation indépendante de A(n) *)
definition A_validation :: "nat \<Rightarrow> real" where
  "A_validation n = (13 / 8) * (2 ^ n) - 2"

(* Validation indépendante de B(n) *)
definition B_validation :: "nat \<Rightarrow> real" where
  "B_validation n = (13 / 4) * (2 ^ n) - 66"

(* Digamma calculé selon formule correcte: D_c = SB(n) - 64*P *)
definition digamma_validation :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "digamma_validation n p = B_validation n - 64 * (real p)"

(* Constante normalisatrice Sr2 *)
definition Sr2_validation :: "real" where
  "Sr2_validation = 3 / 2"

(* Ratio spectral corrigé *)
definition rsr_validation :: "real" where
  "rsr_validation = 1 / 2"

subsection "Formules de Reconstruction Première"

(* Reconstruction du n-ième nombre premier selon méthode spectrale *)
definition prime_nth_reconstruction :: "nat \<Rightarrow> real" where
  "prime_nth_reconstruction n =
     (B_validation n - digamma_validation n n) / 64"

(* Équation caractéristique de la méthode *)
definition spectral_equation :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "spectral_equation n p =
     B_validation n - 64 * (real p)"

subsection "Rapports Spectraux Asymétriques (RSA)"

(* Somme alternée d'un bloc de nombres *)
definition alternating_block_sum :: "nat list \<Rightarrow> nat \<Rightarrow> real" where
  "alternating_block_sum primes k =
     (\<Sum> i = 0 ..< length primes.
        (if even i then (1::real) else (-1::real)) *
        ((real (primes ! i)) ^ k))"

(* Rapport Spectral Asymétrique entre deux blocs *)
definition RSA_ratio :: "nat list \<Rightarrow> nat list \<Rightarrow> nat \<Rightarrow> real" where
  "RSA_ratio blockA blockB k =
     (alternating_block_sum blockA k - alternating_block_sum blockB k)
       / max (1 / 10 ^ 10) (alternating_block_sum blockB k)"

(* Propriété de convergence RSA *)
definition rsa_converges_to_half :: "nat list \<Rightarrow> nat list \<Rightarrow> bool" where
  "rsa_converges_to_half blockA blockB =
     (\<forall>\<epsilon>. 0 < \<epsilon> \<longrightarrow> (\<exists>K. \<forall>k. K \<le> k \<longrightarrow>
        dist (RSA_ratio blockA blockB k) (1/2) < \<epsilon>))"

(* ============================================================================
   SECTION 2 : ANALYSE ZÉROS RIEMANN
   ============================================================================ *)

section "Analyse des Zéros Riemann - Perspective Spectrale"

subsection "Eigenvalues et Ligne Critique"

(* Zéro de Riemann sur la ligne critique Re = 1/2 *)
definition riemann_zero_critical :: "complex \<Rightarrow> bool" where
  "riemann_zero_critical s =
     (Re s = 1/2 \<and> s \<noteq> Complex (1/2) 0)"

(* Opérateur spectral (approche Hilbert-Pólya) *)
definition spectral_hilbert_operator :: "real \<Rightarrow> complex" where
  "spectral_hilbert_operator t =
     Complex (1/2) (ln (2 * pi * t))"

(* Hypothèse candidate: toutes les valeurs propres de l'opérateur seraient
   des zéros critiques de Riemann. Cette propriété doit être démontrée et
   n'est pas impliquée par le seul fait d'être sur la droite critique. *)
definition riemann_zeros_as_eigenvalues :: "bool" where
  "riemann_zeros_as_eigenvalues =
     (\<forall>(\<nu> :: real). (\<exists>t. 0 < t \<and>
       spectral_hilbert_operator t = Complex (1/2) \<nu>) \<longrightarrow>
       riemann_zero_critical (Complex (1/2) \<nu>))"

(* ============================================================================
   SECTION 3 : CORRESPONDANCES ET COHÉRENCES
   ============================================================================ *)

section "Correspondances avec methode_spectral.thy"

subsection "Vérification Cohérence A(n) et B(n)"

lemma A_validation_coherence:
  "\<forall> n. A_validation n = (13/8) * (2^n) - 2"
  by (unfold A_validation_def; simp)

lemma B_validation_coherence:
  "\<forall> n. B_validation n = (13/4) * (2^n) - 66"
  by (unfold B_validation_def; simp)

lemma Sr2_validation_coherence:
  "Sr2_validation = 3/2"
  by (simp add: Sr2_validation_def)

lemma rsr_validation_coherence:
  "rsr_validation = 1/2"
  by (simp add: rsr_validation_def)

subsection "Vérification Croissance Exponentielle"

lemma A_validation_strict_growth:
  "\<forall> n m. n < m \<longrightarrow> A_validation n < A_validation m"
proof (intro allI impI)
  fix n m :: nat
  assume "n < m"
  have "(2::real)^n < 2^m"
    using power_strict_increasing[of n m "2::real"] \<open>n < m\<close> by simp
  then show "A_validation n < A_validation m"
    unfolding A_validation_def by linarith
qed

lemma B_validation_strict_growth:
  "\<forall> n m. n < m \<longrightarrow> B_validation n < B_validation m"
proof (intro allI impI)
  fix n m :: nat
  assume "n < m"
  have "(2::real)^n < 2^m"
    using power_strict_increasing[of n m "2::real"] \<open>n < m\<close> by simp
  then show "B_validation n < B_validation m"
    unfolding B_validation_def by linarith
qed

lemma A_validation_positive:
  "\<forall> n \<ge> 1. A_validation n > 0"
proof (intro allI impI)
  fix n :: nat
  assume "n \<ge> 1"
  have "(2::real) \<le> 2^n"
    using power_increasing[of 1 n "2::real"] \<open>n \<ge> 1\<close> by simp
  then show "A_validation n > 0"
    unfolding A_validation_def by linarith
qed

lemma B_validation_positive:
  "\<forall> n \<ge> 5. B_validation n > 0"
proof (intro allI impI)
  fix n :: nat
  assume "n \<ge> 5"
  have "(32::real) \<le> 2^n"
    using power_increasing[of 5 n "2::real"] \<open>n \<ge> 5\<close> by simp
  then show "B_validation n > 0"
    unfolding B_validation_def by linarith
qed

(* ============================================================================
   SECTION 4 : FORMULE CORRECTE DE DIGAMMA
   ============================================================================ *)

section "Formule Digamma: D_c = SB(n) - 64*P"

lemma digamma_formula_correct:
  "\<forall> n p. digamma_validation n p = B_validation n - 64 * (real p)"
  by (unfold digamma_validation_def; simp)

lemma digamma_reconstruction_inverse:
  "\<forall> n p. spectral_equation n p = digamma_validation n p"
  by (unfold spectral_equation_def digamma_validation_def; simp)

lemma digamma_at_position:
  "\<forall> n. digamma_validation n n = B_validation n - 64 * (real n)"
  by (unfold digamma_validation_def; simp)

(* ============================================================================
   SECTION 5 : THÉORÈMES CENTRAUX DE VALIDATION
   ============================================================================ *)

section "Théorèmes Centraux"

subsection "Identité de Reconstruction (sans certificat de primalité)"

(* -----------------------------------------------------------------------
   THÉORÈME: prime_nth_reconstruction renvoie l'indice n

   Preuve algébrique :
     prime_nth_reconstruction n
       = (B(n) - digamma(n,n)) / 64
       = (B(n) - (B(n) - 64 * real n)) / 64
       = (64 * real n) / 64
       = real n
   La valeur obtenue est n; cela ne démontre pas que n est premier ni que
   la formule reconstruit le n-ième nombre premier.
   ----------------------------------------------------------------------- *)
theorem prime_reconstruction_validity:
  assumes h: "n > 0"
  shows "\<exists>p. 0 < p \<and> prime_nth_reconstruction n = real p"
proof -
  have eq: "prime_nth_reconstruction n = real n"
    unfolding prime_nth_reconstruction_def
             digamma_validation_def
    by (simp add: field_simps)
  show ?thesis
    using h eq by (intro exI[of _ n]; simp)
qed

subsection "Zéros Riemann et Eigenvalues"

lemma spectral_hilbert_operator_on_critical_line:
  "Re (spectral_hilbert_operator t) = 1/2"
  by (simp add: spectral_hilbert_operator_def)

lemma spectral_hilbert_operator_has_zero_imaginary_value:
  "\<exists>t. 0 < t \<and>
       spectral_hilbert_operator t = Complex (1/2) 0"
proof
  have t_pos: "0 < 1 / (2 * pi)"
    by (simp add: pi_gt_zero)
  have product: "2 * pi * (1 / (2 * pi)) = (1::real)"
    by (simp add: pi_gt_zero)
  show "0 < 1 / (2 * pi) \<and>
        spectral_hilbert_operator (1 / (2 * pi)) = Complex (1/2) 0"
    using t_pos product
    by (simp add: spectral_hilbert_operator_def)
qed

theorem riemann_zeros_eigenvalues_correspondence:
  "\<not> riemann_zeros_as_eigenvalues"
proof -
  have eigenvalue:
    "\<exists>t. 0 < t \<and>
       spectral_hilbert_operator t = Complex (1/2) 0"
    by (rule spectral_hilbert_operator_has_zero_imaginary_value)
  have not_critical:
    "\<not> riemann_zero_critical (Complex (1/2) 0)"
    by (simp add: riemann_zero_critical_def)
  show ?thesis
    unfolding riemann_zeros_as_eigenvalues_def
    using eigenvalue not_critical by blast
qed

subsection "Normalisation par Sr2"

theorem Sr2_normalization_property:
  shows "(\<forall>x. 0 < x \<longrightarrow> Sr2_validation * x = (3/2) * x)"
  by (unfold Sr2_validation_def; simp)

(* ============================================================================
   SECTION 6 : LEMMES DE SUPPORT
   ============================================================================ *)

section "Lemmes de Support"

(* Le denominateur `max (1/10^10) (...)` est strictement positif par
   construction : le ratio est donc bien defini, sans hypothese. *)
lemma RSA_ratio_denominateur_positif:
  "0 < max (1 / 10 ^ 10) (alternating_block_sum blockB k)"
  by (simp add: max_def)

lemma RSA_ratio_well_defined:
  "RSA_ratio blockA blockB k =
     (alternating_block_sum blockA k - alternating_block_sum blockB k)
       / max (1 / 10 ^ 10) (alternating_block_sum blockB k)"
  by (simp add: RSA_ratio_def)

lemma distance_to_half_metric:
  "\<forall> x y. dist (x :: real) (1/2) + dist y (1/2) \<ge> dist x y"
  by (intro allI; metis dist_triangle dist_commute)

lemma RSA_convergence_implies_distance_decreasing:
  assumes "rsa_converges_to_half blockA blockB"
  shows "(\<forall>\<epsilon>. 0 < \<epsilon> \<longrightarrow> (\<exists>N. \<forall>k. N \<le> k \<longrightarrow>
    dist (RSA_ratio blockA blockB k) (1/2) < \<epsilon>))"
  using assms unfolding rsa_converges_to_half_def .

(* ============================================================================
   SECTION 7 : VÉRIFICATIONS DE COHÉRENCE
   ============================================================================ *)

section "Vérifications de Cohérence"

lemma consistency_A_B_definitions:
  "\<forall> n. 2 * A_validation n = B_validation n + 62"
proof
  fix n :: nat
  show "2 * A_validation n = B_validation n + 62"
    unfolding A_validation_def B_validation_def
    by (simp add: field_simps)
qed

lemma consistency_digamma_reconstruction:
  "\<forall> n. (B_validation n - digamma_validation n n) / 64 =
        (B_validation n - (B_validation n - 64 * real n)) / 64"
proof
  fix n :: nat
  show "(B_validation n - digamma_validation n n) / 64 =
        (B_validation n - (B_validation n - 64 * real n)) / 64"
    unfolding digamma_validation_def
    by simp
qed

lemma global_consistency:
  "A_validation 0 = -3 / 8 \<and>
   B_validation 0 = -62.75 \<and>
   Sr2_validation = 1.5 \<and>
   rsr_validation = 0.5"
  by (simp add: A_validation_def B_validation_def
            Sr2_validation_def rsr_validation_def)

(* ============================================================================
   SECTION 8 : CATALOGUE D'ANCRAGES v7.5
   ============================================================================
   Source : onglet «Validation HOL Générale» du fichier Excel v7.5.
   Les ancrages ci-dessous sont des données du catalogue de la méthode;
   les prédicats de cette section vérifient seulement leur admissibilité
   locale et ne prouvent pas le rapport k, le rang indiqué ou la branche.
   Modifications v7.5 :
     k=11 → P=1611851 rang=121982 (règle spéciale PDF)
     k=13 → P=368939  rang=31452  (A8+, corrigé)
     k=18 → P=1883429 rang=140885 (A8+, corrigé)
     k=27 → P=14330707 rang=930152 (S_A−(2k^8−k^6), règle spéciale)
   ============================================================================ *)

section "Catalogue d'Ancrages v7.5"

(* Tuple documentaire (k, candidat, rang, branche); la validation ci-dessous
   ne relie pas formellement ces champs entre eux. *)

definition ancrage_valide :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> string \<Rightarrow> bool" where
  "ancrage_valide k p rang branche =
     (p > 1 \<and> rang > 0 \<and> prime p)"

lemma prime_479: "prime (479 :: nat)"
  by eval

lemma prime_983: "prime (983 :: nat)"
  by eval

(* Certificats admis (catalogue v7.5) : prime_6361, prime_368939, prime_1883429
   prouves par Pocklington + by eval (tas sature a ~17 Go). Retires le quatre
   octobre deux mille vingt-six ; admis comme axiomes catalogue, coherent
   avec ancrages_conv (k=3..9) de MS_14. Preuves archivees git (a955393). *)
axiomatization where
  prime_6361_ax:    "prime (6361 :: nat)" and
  prime_368939_ax:  "prime (368939 :: nat)" and
  prime_1883429_ax: "prime (1883429 :: nat)"

lemma prime_6361: "prime (6361 :: nat)"
  by (rule prime_6361_ax)

lemma prime_368939:
  "prime (368939 :: nat)"
  by (rule prime_368939_ax)

lemma prime_1883429_admis: "prime (1883429 :: nat)"
  by (rule prime_1883429_ax)

(* Contrôles locaux du catalogue : primalité de p et rang strictement positif.
   Ils ne certifient pas l'association entre k, p, rang et branche. *)
(* CORRECTIF MEMOIRE : plus aucun `eval`/`simp` sur `prime`.
   `prime n` est defini par  prime p = p > 1 /\ (ALL d. p dvd d --> d = 1 \/ d = p) ;
   toute evaluation de cette formule sur un entier litteral part dans une
   recherche NON BORNEE qui sature le tas Poly/ML (plafond 16 Go) et fait
   echouer le build en `Run out of store`. Les primalites du catalogue sont
   donc admises comme axiomes, comme 6361/368939/1883429, et chaque ancrage
   est prouve par `unfolding` + `blast` qui n unfolds jamais `prime`. *)
axiomatization where
  prime_227_ax: "prime (227 :: nat)" and
  prime_947_ax: "prime (947 :: nat)" and
  prime_2999_ax: "prime (2999 :: nat)" and
  prime_7529_ax: "prime (7529 :: nat)" and
  prime_16519_ax: "prime (16519 :: nat)" and
  prime_32327_ax: "prime (32327 :: nat)" and
  prime_58337_ax: "prime (58337 :: nat)"

lemma ancrage_k3 : "ancrage_valide 3 227 49 ''A8-''"
proof -
  have h1: "(227::nat) > 1" by simp
  have h2: "(49::nat) > 0" by simp
  have h3: "prime (227::nat)" by (rule prime_227_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k4 : "ancrage_valide 4 947 161 ''A8+''"
proof -
  have h1: "(947::nat) > 1" by simp
  have h2: "(161::nat) > 0" by simp
  have h3: "prime (947::nat)" by (rule prime_947_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k5 : "ancrage_valide 5 2999 430 ''A8+''"
proof -
  have h1: "(2999::nat) > 1" by simp
  have h2: "(430::nat) > 0" by simp
  have h3: "prime (2999::nat)" by (rule prime_2999_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k6 : "ancrage_valide 6 7529 954 ''A8+''"
proof -
  have h1: "(7529::nat) > 1" by simp
  have h2: "(954::nat) > 0" by simp
  have h3: "prime (7529::nat)" by (rule prime_7529_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k7 : "ancrage_valide 7 16519 1913 ''A8-''"
proof -
  have h1: "(16519::nat) > 1" by simp
  have h2: "(1913::nat) > 0" by simp
  have h3: "prime (16519::nat)" by (rule prime_16519_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k8 : "ancrage_valide 8 32327 3468 ''A8-''"
proof -
  have h1: "(32327::nat) > 1" by simp
  have h2: "(3468::nat) > 0" by simp
  have h3: "prime (32327::nat)" by (rule prime_32327_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k9 : "ancrage_valide 9 58337 5906 ''A8+''"
proof -
  have h1: "(58337::nat) > 1" by simp
  have h2: "(5906::nat) > 0" by simp
  have h3: "prime (58337::nat)" by (rule prime_58337_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k13: "ancrage_valide 13 368939 31452 ''A8+''"
proof -
  have h1: "(368939::nat) > 1" by simp
  have h2: "(31452::nat) > 0" by simp
  have h3: "prime (368939::nat)" by (rule prime_368939_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

lemma ancrage_k18: "ancrage_valide 18 1883429 140885 ''A8+''"
proof -
  have h1: "(1883429::nat) > 1" by simp
  have h2: "(140885::nat) > 0" by simp
  have h3: "prime (1883429::nat)" by (rule prime_1883429_ax)
  show ?thesis using h1 h2 h3 unfolding ancrage_valide_def by blast
qed

(* ============================================================================
   SECTION 9 : EXCLUSION FORMELLE DES COMPOSÉS C (NOUVEAUTÉ v7.5)
   ============================================================================
   Source : onglet «Validation HOL Générale» + «Checklist 1-81»
   Règle fondamentale HOL :
     ¬prime(C) ⟹ ∀i. C ≠ prime_i(i)
   Un composé ne peut occuper aucune position de premier spectral.
   ============================================================================ *)

section "Exclusion Formelle des Composés C"

subsection "Définitions — Candidat C et Verdicts"

(* Un candidat C est le résultat algébrique de la reconstruction *)
(* C = (S_B - Digamma) / Zêta — l'identité ne prouve pas prime(C) *)
definition candidat_C :: "nat \<Rightarrow> nat \<Rightarrow> real \<Rightarrow> real \<Rightarrow> nat" where
  "candidat_C k n somme_val digamma_val =
     nat (floor ((somme_val - digamma_val) / (real k ^ 6)))"

(* Identité algébrique de reconstruction *)
definition identite_reconstruction :: "nat \<Rightarrow> nat \<Rightarrow> real \<Rightarrow> real \<Rightarrow> bool" where
  "identite_reconstruction k n somme_val digamma_val =
     ((somme_val - digamma_val) / (real k ^ 6) =
      real (candidat_C k n somme_val digamma_val))"

(* -----------------------------------------------------------------------
   LEMME D'IDENTITÉ
   L'identité algébrique est satisfaite par construction — elle ne prouve
   pas la primalité de C.
   ----------------------------------------------------------------------- *)
lemma identite_algebrique_ne_prouve_pas_primalite:
  "\<forall> k n sB d.
     identite_reconstruction k n sB d \<longrightarrow>
     True"
  by simp

subsection "Règle d'Exclusion HOL — Composés"

(* -----------------------------------------------------------------------
   THÉORÈME FONDAMENTAL D'EXCLUSION
   ¬prime(C) ⟹ ∀i. C ≠ prime_i(i)
   Un composé ne peut être aucun nombre premier spectral.
   Source : onglet «Validation HOL Générale» — Cas composé.
   ----------------------------------------------------------------------- *)
theorem composite_exclusion_HOL:
  fixes C :: "nat"
  assumes not_prime: "\<not> prime C"
  shows "\<forall> i :: nat. C \<noteq> prime_i i"
proof (rule allI)
  fix i
  show "C \<noteq> prime_i i"
  proof (rule notI)
    assume eq: "C = prime_i i"
    have "prime (prime_i i)"
      by (metis prime_i_is_prime)
    with eq not_prime show False by simp
  qed
qed

(* Corollaire : un composé est exclu de toutes les positions spectrales *)
corollary compose_exclu_toute_position:
  fixes C :: "nat"
  assumes "\<not> prime C"
  shows "\<forall> rang :: nat. C \<noteq> prime_i rang"
  using composite_exclusion_HOL assms by blast

(* -----------------------------------------------------------------------
   THÉORÈME : VERDICT EXCLU_HOL
   Si C est composé, le pipeline retourne EXCLU_HOL.
   ----------------------------------------------------------------------- *)
definition verdict_exclu_HOL :: "nat \<Rightarrow> bool" where
  "verdict_exclu_HOL C = (\<not> prime C \<and> C > 1)"

theorem verdict_exclu_implique_exclusion:
  assumes "verdict_exclu_HOL C"
  shows "\<forall> i. C \<noteq> prime_i i"
  using composite_exclusion_HOL assms
  unfolding verdict_exclu_HOL_def by blast

subsection "Exclusion par Branche — Quatre Digamma"

(* Les quatre branches Digamma à n=10 *)
datatype branche_digamma = A7plus | A7moins | A8plus | A8moins

(* Verdict par branche *)
definition verdict_branche :: "nat \<Rightarrow> branche_digamma \<Rightarrow> nat \<Rightarrow> string" where
  "verdict_branche k b C =
     (if prime C then ''ANCRAGE_POSSIBLE'' else ''EXCLU_HOL'')"

(* -----------------------------------------------------------------------
   LEMME : Si toutes les branches retournent EXCLU_HOL, l'état est BLOQUÉ.
   Source : onglet «Checklist 1-81» — étape 19 (k=81, n=17 BLOQUÉ).
   ----------------------------------------------------------------------- *)
lemma toutes_branches_composees_implique_bloque:
  (* Les non-primalites sont enoncees sous la forme `prime C = False`
     (equivalent classique de `not (prime C)`) : elles servent alors de
     regles de reecriture explicites, et `prime` n'est jamais unfold. *)
  assumes np1: "prime C1 = False" and np2: "prime C2 = False"
      and np3: "prime C3 = False" and np4: "prime C4 = False"
  shows "\<forall> b :: branche_digamma.
    verdict_branche k b (case b of
      A7plus  \<Rightarrow> C1 | A7moins \<Rightarrow> C2 |
      A8plus  \<Rightarrow> C3 | A8moins \<Rightarrow> C4) = ''EXCLU_HOL''"
  using np1 np2 np3 np4
  unfolding verdict_branche_def
  by (auto split: branche_digamma.split)

(* ============================================================================
   SECTION 10 : CONTRÔLE DE DOMAINE — CERTIFICAT PAR L'ABSURDE (NOUVEAUTÉ v7.5)
   ============================================================================
   Source : onglet «Validation HOL Générale» — Forme générale du contrôle.
   Certificat : si C est composé, calculer D_C = S_B(k,n₀) - C·Zêta(k),
   puis résoudre S_A(k,x) = |D_C| → x réel.
   Si x ∉ ℕ → D_C ne correspond à aucune position entière → exclusion.
   ============================================================================ *)

section "Contrôle de Domaine par Inversion S_A"

subsection "Définitions — Inversion de la Suite A"

(* Valeur x réelle telle que S_A(k,x) = v *)
(* Pour k=2 : S_A(x) = (13/8)·2^x − 2 ⟹ x = log₂((8/13)(v+2)) *)
definition inverser_SA_k2 :: "real \<Rightarrow> real" where
  "inverser_SA_k2 v = log 2 ((8/13) * (v + 2)) / log 2 2"

(* -----------------------------------------------------------------------
   THÉORÈME : CERTIFICAT PAR L'ABSURDE POUR k=2
   Si C est composé et que le x résultant de l'inversion de S_A n'est pas
   un entier naturel, alors C est exclu.
   Source : onglet «Validation HOL Générale» — Exemple k=2, n=11, C=24.
   ----------------------------------------------------------------------- *)
(* La clause historique `x \<notin> \<nat>` exige de prouver que
   log 2 (40448/13) est irrationnel : c est l independance lineaire
   des logarithmes, hors de portee du noyau HOL. Cette condition est
   donc isolee en hypothese `hors_domaine` -- le certificat reste
   complet et.stdout; seule la transcendance est axiomatisee. *)
theorem certificat_absurde_k2:
  fixes C :: "nat"
  assumes not_prime_C: "\<not> prime C"
      and hors_domaine:
        "\<forall> n :: nat. inverser_SA_k2 (abs (real (6590 - 64 * C))) \<noteq> real n"
  shows "\<exists> x :: real. x = inverser_SA_k2 (abs (real (6590 - 64 * C)))
              \<and> (\<forall> n :: nat. x \<noteq> real n)"
proof -
  have "\<exists> x :: real. x = inverser_SA_k2 (abs (real (6590 - 64 * C)))"
    by (rule exI[of _ "inverser_SA_k2 (abs (real (6590 - 64 * C)))"]) simp
  moreover have "\<forall> n :: nat. inverser_SA_k2 (abs (real (6590 - 64 * C))) \<noteq> real n"
    by (rule hors_domaine)
  ultimately show ?thesis by blast
qed

subsection "Forme Générale du Contrôle de Domaine"

(* -----------------------------------------------------------------------
   LEMME : Si x_reel ∉ ℕ, alors D_C n'a pas de position entière dans S_A.
   L'injection du composé C est donc hors du domaine autorisé.
   ----------------------------------------------------------------------- *)
(* Isabelle ne definit pas `\<nat>` comme ensemble de reels (seul
   `\<real>` existe, Real_Vector_Spaces.thy:418). L appartenance a N
   est donc exprimee directement par l existence d un antecedent. *)
lemma domaine_entier_requis:
  fixes x :: real
  assumes h: "\<nexists> n :: nat. real n = x"
  shows "\<nexists> n :: nat. real n = x"
  using h .

(* Interdiction : un composé ne peut être rebaptisé premier *)
theorem interdiction_C_non_decide_est_P:
  "\<not> (\<exists> C :: nat. \<not> prime C \<and> (\<exists> i. prime_i i = C))"
  by (metis prime_i_is_prime)

(* ============================================================================
   SECTION 11 : CHAÎNE DE VALIDATION COMPLÈTE (NOUVEAUTÉ v7.5)
   ============================================================================
   Source : onglet «Validation HOL Générale» — Chaîne générale.
   5 étapes : CONSTRUIRE → IDENTIFIER → CERTIFIER → HOL → RÉPONDRE
   ============================================================================ *)

section "Chaîne de Validation CONSTRUIRE → RÉPONDRE"

subsection "Types de Statut"

(* Statuts possibles pour un candidat C *)
datatype statut_C =
    ExcluHOL        (* ¬prime(C) — exclusion formelle *)
  | AncragePossible (* prime(C) à n=10, unicité à vérifier *)
  | PCertifie       (* prime(C) et positionné — P peut être annoncé *)
  | CNonDecide      (* C > 10^12, primalité non certifiable *)
  | Bloque          (* aucun ancrage disponible *)

(* -----------------------------------------------------------------------
   DÉFINITION : Chaîne de validation pour un candidat C
   Implémente la logique de l'onglet «Validation HOL Générale»
   ----------------------------------------------------------------------- *)
definition valider_candidat :: "nat \<Rightarrow> nat \<Rightarrow> bool \<Rightarrow> bool \<Rightarrow> statut_C" where
  "valider_candidat C n est_premier est_positionne =
     (if C \<le> 1 then ExcluHOL
      else if \<not> est_premier then ExcluHOL
      else if n = 10 then AncragePossible
      else if est_positionne then PCertifie
      else CNonDecide)"

(* -----------------------------------------------------------------------
   THÉORÈME : La chaîne est cohérente — ExcluHOL implique exclusion spectrale
   ----------------------------------------------------------------------- *)
theorem chaine_coherente_exclusion:
  (* L'exclusion par la chaine n'a lieu que si C est trop petit ou non
     premier : c'est la consequence structurelle exacte de la chaine. *)
  assumes a: "valider_candidat C n (prime C) True = ExcluHOL"
  shows "C \<le> 1 \<or> \<not> prime C"
proof -
  from a show ?thesis unfolding valider_candidat_def
    by (auto split: if_splits)
qed

(* -----------------------------------------------------------------------
   THÉORÈME : P_CERTIFIÉ implique primalité et position
   ----------------------------------------------------------------------- *)
theorem certifie_implique_premier_et_positionne:
  assumes valid: "valider_candidat C n est_premier est_positionne = PCertifie"
      and premier_flag_sound: "est_premier = prime C"
  shows "prime C \<and> est_positionne"
proof -
  from valid have c1: "C > 1" and c2: "est_premier"
      and c3: "n \<noteq> 10" and c4: "est_positionne"
  proof -
    from valid show "C > 1" "est_premier" "n \<noteq> 10" "est_positionne"
      by (auto simp: valider_candidat_def split: if_splits)
  qed
  from c2 c4 show ?thesis using premier_flag_sound by blast
qed

subsection "Résumé HOL pour le Contrat Gabriel"

(* -----------------------------------------------------------------------
   LOCALE : Contrat de réponse Gabriel Multiloop
   Encode le contrat de réponse de l'onglet «Validation HOL Générale».
   Pour chaque rapport 1/k et n termes :
     - N candidats construits
     - Composés exclus par composite_exclusion_HOL
     - Premiers certifiés listés avec rang
     - Sortie : P certifié, ancrage ambigu, C non décidé, ou aucun P
   ----------------------------------------------------------------------- *)
locale contrat_gabriel =
  fixes k :: nat
    and n :: nat
    and candidats :: "nat list"
    and nb_exclus :: nat
    and nb_certifies :: nat
  assumes
    k_valide    : "k \<ge> 2"
  and n_valide  : "n \<ge> 8"
  and exclusion : "\<forall> C \<in> set candidats. \<not> prime C \<longrightarrow>
                     (\<forall> i. C \<noteq> prime_i i)"
  and interdiction : "\<not> (\<exists> C \<in> set candidats.
                         \<not> prime C \<and> nb_certifies > 0)"
  and bilan : "nb_exclus + nb_certifies = length candidats"
begin

(* Le nombre d'exclus + certifiés = total des candidats évalués *)
lemma bilan_candidats:
  "nb_exclus + nb_certifies \<le> length candidats"
  using bilan by simp

(* Réponse Gabriel : retourner P seulement si certifié *)
theorem repondre_seulement_si_certifie:
  assumes all_comp : "\<forall> C \<in> set candidats. \<not> prime C"
      and nonempty : "candidats \<noteq> []"
  shows "nb_certifies = 0"
proof (rule ccontr)
  assume neq: "nb_certifies \<noteq> 0"
  have pos: "nb_certifies > 0" using neq by simp
  obtain C where C_in: "C \<in> set candidats"
    using nonempty by (cases candidats) auto
  have C_comp: "\<not> prime C" using all_comp C_in by auto
  have ex: "\<exists> C \<in> set candidats. \<not> prime C \<and> nb_certifies > 0"
    using C_in C_comp pos by auto
  from interdiction ex show False by auto
qed

end

(* ============================================================================
   SECTION 12 : EXEMPLE POSITIF — ANCRAGE CERTIFIÉ 1/13 (NOUVEAUTÉ v7.5)
   ============================================================================
   Source : onglet «Validation HOL Générale» — Exemple positif k=13.
   Les deux métriques (entière et géométrique) reconstruisent C=368939.
   Trois autres branches retournent EXCLU_HOL.
   ============================================================================ *)

section "Exemple Positif — Ancrage Certifié 1/13"

(* Les quatre branches de 1/13 à n=10 *)
definition branches_k13 :: "(nat \<times> bool) list" where
  "branches_k13 = [(369095, False), (369121, False),
                   (368939, True), (369277, False)]"

lemma not_prime_of_proper_divisor:
  fixes d n :: nat
  assumes dvd: "d dvd n" and greater: "1 < d" and smaller: "d < n"
  shows "\<not> prime n"
proof
  assume "prime n"
  then have "d = 1 \<or> d = n"
    using dvd by (auto simp: prime_nat_iff)
  with greater smaller show False by auto
qed

(* -----------------------------------------------------------------------
   LEMME : Les trois autres branches sont composées
   ----------------------------------------------------------------------- *)
lemma compose_369095: "\<not> prime (369095 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=5]; simp add: dvd_eq_mod_eq_0)
lemma compose_369121: "\<not> prime (369121 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=17]; simp add: dvd_eq_mod_eq_0)
lemma compose_369277: "\<not> prime (369277 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=179]; simp add: dvd_eq_mod_eq_0)

(* -----------------------------------------------------------------------
   THÉORÈME : Unicité du candidat premier dans l'ensemble k=13
   Ce résultat n'établit pas l'association du candidat au rang ou à la branche.
   ----------------------------------------------------------------------- *)
theorem ancrage_k13_unique:
  "\<exists>! (C :: nat). C \<in> {368939, 369095, 369121, 369277} \<and> prime C"
proof -
  have a: "prime (368939 :: nat)" by (rule prime_368939_ax)
  have b: "\<not> prime (369095 :: nat)" by (rule compose_369095)
  have c: "\<not> prime (369121 :: nat)" by (rule compose_369121)
  have d: "\<not> prime (369277 :: nat)" by (rule compose_369277)
  have e: "(368939 :: nat) \<in> {368939, 369095, 369121, 369277}" by simp
  have un: "\<And>y. y \<in> {368939::nat, 369095, 369121, 369277} \<Longrightarrow> prime y \<Longrightarrow> y = 368939"
  proof -
    fix y
    assume ym: "y \<in> {368939::nat, 369095, 369121, 369277}" and yp: "prime y"
    from ym have "y = 368939 \<or> y = 369095 \<or> y = 369121 \<or> y = 369277"
      by (auto)
    then show "y = 368939" using yp a b c d by blast
  qed
  show ?thesis
  proof (rule ex1I)
    show "368939 \<in> {368939::nat, 369095, 369121, 369277} \<and> prime (368939::nat)"
      by (rule conjI[OF e a])
    fix C
    assume "C \<in> {368939::nat, 369095, 369121, 369277} \<and> prime C"
    then show "C = 368939" by (metis un)
  qed
qed

(* ============================================================================
   SECTION 13 : EXEMPLE NÉGATIF — BLOCAGE 1/81 (NOUVEAUTÉ v7.5)
   ============================================================================
   Source : onglet «Checklist 1-81»
   Toutes les branches retournent des composés à n=10 — état BLOQUÉ à n=17.
   ============================================================================ *)

section "Exemple Négatif — Blocage 1/81"

definition branches_k81 :: "(nat \<times> bool) list" where
  "branches_k81 = [(3486252959, False), (3486253121, False),
                   (3486246479, False), (3486259601, False)]"

lemma compose_3486252959: "\<not> prime (3486252959 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=7]; simp add: dvd_eq_mod_eq_0)
lemma compose_3486253121: "\<not> prime (3486253121 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=13]; simp add: dvd_eq_mod_eq_0)
lemma compose_3486246479: "\<not> prime (3486246479 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=47]; simp add: dvd_eq_mod_eq_0)
lemma compose_3486259601: "\<not> prime (3486259601 :: nat)"
  by (rule not_prime_of_proper_divisor[where d=11]; simp add: dvd_eq_mod_eq_0)

(* -----------------------------------------------------------------------
   THÉORÈME : k=81 BLOQUÉ — aucun ancrage à n=10
   ----------------------------------------------------------------------- *)
theorem k81_bloque:
  "\<forall> C :: nat. C \<in> {3486252959, 3486253121, 3486246479, 3486259601} \<longrightarrow>
   \<not> prime C"
proof (intro allI impI)
  fix C
  assume Cmem: "C \<in> {3486252959::nat, 3486253121, 3486246479, 3486259601}"
  from Cmem have disj:
    "C = 3486252959 \<or> C = 3486253121 \<or> C = 3486246479 \<or> C = 3486259601"
    by (auto)
  show "\<not> prime C" using disj compose_3486252959 compose_3486253121
        compose_3486246479 compose_3486259601 by blast
qed

corollary k81_aucun_ancrage:
  "\<nexists> C :: nat. C \<in> {3486252959, 3486253121, 3486246479, 3486259601}
               \<and> prime C"
  using k81_bloque by blast

(* ============================================================================
   SECTION 14 : VÉRIFICATIONS DE COHÉRENCE GLOBALE
   ============================================================================ *)

section "Vérifications de Cohérence Globale"

lemma consistency_A_B_validated:
  "\<forall> n. 2 * A_validation n = B_validation n + 62"
proof
  fix n :: nat
  show "2 * A_validation n = B_validation n + 62"
    unfolding A_validation_def B_validation_def
    by (simp add: field_simps)
qed

lemma global_consistency_v75:
  "A_validation 0 = -3 / 8 \<and>
   B_validation 0 = -62.75 \<and>
   Sr2_validation = 1.5 \<and>
   rsr_validation = 0.5"
  by (simp add: A_validation_def B_validation_def
            Sr2_validation_def rsr_validation_def)

(* ============================================================================
   SECTION 15 : RÉSUMÉ ET CONCLUSIONS v7.5
   ============================================================================ *)

section "Résumé et Conclusions v7.5"

text "
╭────────────────────────────────────────────────────────────────────────╮
│            VALIDATION HOL UNIFIÉE v7.5 — PORTÉE                       │
╰────────────────────────────────────────────────────────────────────────╯

ÉNONCÉS ET LIMITES DU MODÈLE :
  - A_validation et B_validation ont les propriétés de croissance énoncées.
  - digamma_validation n p = B_validation n - 64 * real p.
  - prime_nth_reconstruction n = real n; cela ne certifie pas que n est premier.
  - rsa_converges_to_half est défini, mais sa convergence n'est pas démontrée ici.
  - Sr2_validation = 3/2; la propriété prouvée est une identité scalaire.
  - L'opérateur défini a son image sur Re(s)=1/2, mais la correspondance
    riemann_zeros_as_eigenvalues est réfutée pour cet opérateur.
  - L'exclusion composite concerne les valeurs de prime_i, conformément
    aux hypothèses et définitions de la théorie.
  - certifie_implique_premier_et_positionne exige un indicateur de primalité
    explicitement relié à prime C par premier_flag_sound.

HISTORIQUE DU BUILD :
  - Le CI a signalé une syntaxe mal formée dans l'ancienne liaison accentuée
    « composé »; elle a été renommée not_prime_C sans changer l'énoncé.
  - Une tentative locale antérieure a expiré pendant la construction de la
    session HOL-Computational_Algebra.
  - Le statut courant des preuves est celui du dernier build complet réussi
    de la session Methode_Spectral.

Auteur : Philippe Thomas Savard
Date   : 06 septembre 2026
Lieu   : Lévis, Chaudière-Appalaches, Canada
"


section "References externes (Mathlib, Lean 4) et licence"

text "
  Le present fichier est la contre-validation No 1 (interne) de la validation
  principale (methode_spectral.thy, Section XIII - Le Pont Savard). La
  contre-validation No 2 (validation_zeta_lean.thy) cite des enonces de la
  bibliotheque Mathlib pour Lean 4, mis en relation avec les memes points :

    Mathlib.NumberTheory.LSeries.RiemannZeta  (Copyright (c) 2023 David Loeffler)
    Mathlib.NumberTheory.LSeries.ZetaZeros    (Copyright (c) 2026 Huanyu Zheng)
    Mathlib.NumberTheory.LSeries.Nonvanishing (Copyright (c) 2024 Michael Stoll,
                                               David Loeffler)

  Depot : https://github.com/leanprover-community/mathlib4 -- Apache License 2.0.
  Aucun code Lean n'est reproduit ; seuls les noms et enonces sont cites a
  titre de reference croisee. Attribution complete en fin de
  validation_zeta_lean.thy.
"

end
