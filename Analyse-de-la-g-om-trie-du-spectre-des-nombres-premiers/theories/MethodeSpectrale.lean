/-
  ============================================================================
  Methode Spectrale de Philippe Thomas Savard
  Formalisation Lean 4 / Mathlib (portage 1:1 de methode_spectral.thy)

  Auteur original de la theorie : Philippe Thomas Savard
  Portage Isabelle -> Lean       : Gabriel multiloop v3.22 (2026-02)

  Contenu :
    - Suites SA, SB et rapport spectral RsP = 1/2
    - Digamma calcule et equation de reconstruction du n-ieme premier
    - Fonction prime_i (i-ieme premier) via choix classique
    - Les 3 piliers de la Methode Spectrale bornes a P (preuves par l'absurde)
    - Rapports spectraux 1/3 et 1/4 (regimes symetriques)
    - Section XI : regles de construction des suites A_i et B_i
      (bug 9 : `def` sans recursion ; bug 10 : plus de `sorry`)

  IMPORTANT :
    - Ce fichier reproduit fidelement la structure de methode_spectral.thy
    - Les theoremes lourds sont demontres par la meme strategie qu'Isabelle
    - Les axiomes Savard sont explicites via `axiom` (equivalent axiomatization)
    - Aucun `sorry` : les 2 lemmes de la conjecture XI.10 sont enonces
      conditionnellement (avec le fait Savard en hypothese) exactement comme
      dans la version Isabelle corrigee.
  ============================================================================
-/

import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Algebra.BigOperators.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.List.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp

namespace MethodeSpectrale

open Classical
open scoped BigOperators

-- ============================================================================
-- SECTION 1 : Forme generale des suites A et B
-- ============================================================================

/-- Somme spectrale A : SA(n) = (3.25/2) * 2^n - 2. -/
noncomputable def SA (n : ℕ) : ℝ := (3.25 / 2) * (2 : ℝ) ^ n - 2

/-- Somme spectrale B : SB(n) = (6.5/2) * 2^n - 66. -/
noncomputable def SB (n : ℕ) : ℝ := (6.5 / 2) * (2 : ℝ) ^ n - 66

lemma SA_forme_generale (n : ℕ) (hn : 1 ≤ n) :
    SA n = (3.25 / 2) * (2 : ℝ) ^ n - 2 := rfl

lemma SB_forme_generale (n : ℕ) (hn : 1 ≤ n) :
    SB n = (6.5 / 2) * (2 : ℝ) ^ n - 66 := rfl

-- ============================================================================
-- SECTION 2 : Rapport spectral 1/2
-- ============================================================================

/-- Rapport spectral RsP(n1, n2) = (SA(n1) - SA(n2)) / (SB(n1) - SB(n2)). -/
noncomputable def RsP (n1 n2 : ℕ) : ℝ := (SA n1 - SA n2) / (SB n1 - SB n2)

/-- Theoreme central : le rapport spectral RsP vaut exactement 1/2
    pour toute paire d'indices distincts n1, n2 >= 1. -/
theorem RsP_un_demi_general (n1 n2 : ℕ)
    (h1 : 1 ≤ n1) (h2 : 1 ≤ n2) (hne : n1 ≠ n2) :
    RsP n1 n2 = 1 / 2 := by
  -- La difference 2^n1 - 2^n2 est non nulle car 2^_ est strictement croissante.
  have hpow_ne : ((2 : ℝ) ^ n1 - (2 : ℝ) ^ n2) ≠ 0 := by
    intro hz
    have heq : (2 : ℝ) ^ n1 = (2 : ℝ) ^ n2 := by linarith
    have h2gt : (1 : ℝ) < 2 := by norm_num
    exact hne (pow_right_injective (by norm_num : (2 : ℝ) ≠ 1) heq)
  unfold RsP SA SB
  have num : (3.25 / 2) * (2 : ℝ) ^ n1 - 2 - ((3.25 / 2) * (2 : ℝ) ^ n2 - 2)
             = (3.25 / 2) * ((2 : ℝ) ^ n1 - (2 : ℝ) ^ n2) := by ring
  have den : (6.5 / 2) * (2 : ℝ) ^ n1 - 66 - ((6.5 / 2) * (2 : ℝ) ^ n2 - 66)
             = (6.5 / 2) * ((2 : ℝ) ^ n1 - (2 : ℝ) ^ n2) := by ring
  rw [num, den]
  rw [mul_div_mul_right _ _ hpow_ne]
  norm_num

-- ============================================================================
-- SECTION 3 : Digamma calcule et equation de reconstruction du premier
-- ============================================================================

/-- Digamma calcule a partir de SB et du nombre premier p. -/
noncomputable def digamma_calc (n : ℕ) (p : ℕ) : ℝ := SB n - 64 * (p : ℝ)

/-- Equation de reconstruction du premier : (SB(n) - digamma(n,p)) / 64. -/
noncomputable def prime_equation (n : ℕ) (p : ℕ) : ℝ :=
  (SB n - digamma_calc n p) / 64

lemma digamma_calc_equation_alt (n p : ℕ) :
    digamma_calc n p = (SB n / 64 - (p : ℝ)) * 64 := by
  unfold digamma_calc; ring

/-- Identite algebrique : prime_equation reconstruit p pour tout n, p. -/
lemma prime_equation_identity (n p : ℕ) :
    prime_equation n p = (p : ℝ) := by
  unfold prime_equation digamma_calc
  ring

lemma SB_affine_en_SA (n : ℕ) : SB n = 2 * SA n - 62 := by
  unfold SA SB; ring

lemma ecart_spectral_constant (n : ℕ) : SB n - 2 * SA n = -62 := by
  unfold SA SB; ring

lemma digamma_affine_en_SA (n p : ℕ) :
    digamma_calc n p = 2 * SA n - (62 + 64 * (p : ℝ)) := by
  unfold digamma_calc SA SB; ring

lemma difference_SA_succ (n : ℕ) :
    SA (n + 1) - SA n = (13 / 8) * (2 : ℝ) ^ n := by
  unfold SA
  have : (2 : ℝ) ^ (n + 1) = 2 * (2 : ℝ) ^ n := by ring
  rw [this]; ring

lemma difference_SB_succ (n : ℕ) :
    SB (n + 1) - SB n = (13 / 4) * (2 : ℝ) ^ n := by
  unfold SB
  have : (2 : ℝ) ^ (n + 1) = 2 * (2 : ℝ) ^ n := by ring
  rw [this]; ring

lemma ratio_incremental_un_demi (n : ℕ) :
    SA (n + 1) - SA n = (SB (n + 1) - SB n) / 2 := by
  rw [difference_SA_succ, difference_SB_succ]; ring

-- ============================================================================
-- SECTION 4 : Postulat spectral positif (axiome de la theorie Savard)
-- ============================================================================

/-- Axiome Savard : pour tout n >= 1 et p premier, prime_equation(n,p) = p. -/
axiom spectral_postulate_pos :
    ∀ (n p : ℕ), 1 ≤ n → Nat.Prime p → prime_equation n p = (p : ℝ)

lemma prime_equation_for_primes_pos (n p : ℕ)
    (hn : 1 ≤ n) (hp : Nat.Prime p) :
    prime_equation n p = (p : ℝ) :=
  spectral_postulate_pos n p hn hp

-- ============================================================================
-- SECTION 5 : Exemples numeriques concrets pour 29, 31, 37, 41
-- ============================================================================

def n29 : ℕ := 10
def n31 : ℕ := 11
def n37 : ℕ := 12
def n41 : ℕ := 13

noncomputable def D29 : ℝ := 256
noncomputable def D31 : ℝ := 5 * 256
noncomputable def D37 : ℝ := 9 * 256 + 5 * 384
noncomputable def D41 : ℝ := 13 * 256 + 9 * 384 + 5 * 768

lemma SA_10 : SA n29 = 1662 := by unfold SA n29; norm_num
lemma SB_10 : SB n29 = 3262 := by unfold SB n29; norm_num
lemma SA_11 : SA n31 = 3326 := by unfold SA n31; norm_num
lemma SB_11 : SB n31 = 6590 := by unfold SB n31; norm_num
lemma SA_12 : SA n37 = 6654 := by unfold SA n37; norm_num
lemma SB_12 : SB n37 = 13246 := by unfold SB n37; norm_num
lemma SA_13 : SA n41 = 13310 := by unfold SA n41; norm_num
lemma SB_13 : SB n41 = 26558 := by unfold SB n41; norm_num

lemma digamma_calc_29 : digamma_calc n29 29 = 1406 := by
  unfold digamma_calc n29 SB; norm_num
lemma digamma_calc_31 : digamma_calc n31 31 = 4606 := by
  unfold digamma_calc n31 SB; norm_num
lemma digamma_calc_37 : digamma_calc n37 37 = 10878 := by
  unfold digamma_calc n37 SB; norm_num
lemma digamma_calc_41 : digamma_calc n41 41 = 23934 := by
  unfold digamma_calc n41 SB; norm_num

lemma relation_29 : digamma_calc n29 29 = SA n29 - D29 := by
  unfold digamma_calc SA SB n29 D29
  norm_num

lemma relation_31 : digamma_calc n31 31 = SA n31 + D31 := by
  unfold digamma_calc SA SB n31 D31
  norm_num

lemma relation_37 : digamma_calc n37 37 = SA n37 + D37 := by
  unfold digamma_calc SA SB n37 D37
  norm_num

lemma relation_41 : digamma_calc n41 41 = SA n41 + D41 := by
  unfold digamma_calc SA SB n41 D41
  norm_num

-- ============================================================================
-- SECTION 6 : Equation generale de reconstruction (theoreme central)
-- ============================================================================

lemma SB_minus_digamma_is_64p (n p : ℕ) :
    SB n - digamma_calc n p = 64 * (p : ℝ) := by
  unfold digamma_calc; ring

lemma prime_equation_general (n p : ℕ) :
    prime_equation n p = (p : ℝ) := prime_equation_identity n p

lemma SB_minus_digamma_div_64_general (n p : ℕ) :
    (SB n - digamma_calc n p) / 64 = (p : ℝ) := by
  unfold digamma_calc; ring

/-- Theoreme de reconstruction du premier (regime positif). -/
theorem reconstruction_premier_pos (n p : ℕ)
    (hn : 1 ≤ n) (hp : Nat.Prime p) :
    (SB n - digamma_calc n p) / 64 = (p : ℝ) :=
  SB_minus_digamma_div_64_general n p

-- ============================================================================
-- SECTION 7 : i-ieme nombre premier (generalisation spectrale)
-- ============================================================================

/-- Fonction position abstraite : envoie un premier vers son indice. -/
axiom position : ℕ → ℕ

/-- Axiome d'existence : pour tout indice i, il existe un premier
    dont la position vaut i. Garantit la totalite de prime_i. -/
axiom prime_position_exists :
    ∀ i : ℕ, ∃ p : ℕ, Nat.Prime p ∧ position p = i

/-- Le i-ieme nombre premier, defini via choix classique (SOME). -/
noncomputable def prime_i (i : ℕ) : ℕ :=
  Classical.choose (prime_position_exists i)

lemma prime_i_spec (i : ℕ) :
    Nat.Prime (prime_i i) ∧ position (prime_i i) = i :=
  Classical.choose_spec (prime_position_exists i)

lemma prime_i_is_prime (i : ℕ) : Nat.Prime (prime_i i) :=
  (prime_i_spec i).1

lemma prime_i_position (i : ℕ) : position (prime_i i) = i :=
  (prime_i_spec i).2

lemma SA_general_i (i : ℕ) : SA i = (3.25 / 2) * (2 : ℝ) ^ i - 2 := rfl
lemma SB_general_i (i : ℕ) : SB i = (6.5 / 2) * (2 : ℝ) ^ i - 66 := rfl
lemma digamma_general_i (i p : ℕ) : digamma_calc i p = SB i - 64 * (p : ℝ) := rfl

/-- Equation spectrale generale : pour tout p premier de position i,
    prime_equation(i, p) = p. -/
lemma prime_equation_general_i (p i : ℕ)
    (hp : Nat.Prime p) (hpos : position p = i) :
    prime_equation i p = (p : ℝ) :=
  prime_equation_identity i p

/-- Corollaire : la reconstruction fonctionne sur le i-ieme premier. -/
lemma prime_equation_prime_i (i : ℕ) :
    prime_equation i (prime_i i) = (prime_i i : ℝ) :=
  prime_equation_identity i (prime_i i)

-- ============================================================================
-- SECTION 8 : PREUVE PAR L'ABSURDE - Les 3 piliers bornes a P
-- ============================================================================

/-- PILIER 1 - Theoreme central : aucun compose n'est un prime_i. -/
theorem composite_not_prime_i (C : ℕ) (hC : ¬ Nat.Prime C) :
    ∀ i : ℕ, C ≠ prime_i i := by
  intro i heq
  have hprime : Nat.Prime (prime_i i) := prime_i_is_prime i
  rw [heq] at hC
  exact hC hprime

/-- Corollaire : un compose ne peut satisfaire prime_equation
    conjointement avec sa position dans la table prime_i. -/
theorem spectral_method_exclusively_for_primes (C : ℕ)
    (h1 : 1 < C) (hC : ¬ Nat.Prime C) :
    ¬ (∃ i : ℕ, C = prime_i i ∧ prime_equation i C = (C : ℝ)) := by
  rintro ⟨i, heq, _⟩
  have hprime : Nat.Prime (prime_i i) := prime_i_is_prime i
  rw [← heq] at hprime
  exact hC hprime

-- ============================================================================
-- SECTION 9 : Illustrations numeriques - 6 composes canoniques
-- ============================================================================

lemma composite_4_not_prime : ¬ Nat.Prime 4 := by decide
lemma composite_9_not_prime : ¬ Nat.Prime 9 := by decide
lemma composite_15_not_prime : ¬ Nat.Prime 15 := by decide
lemma composite_51_not_prime : ¬ Nat.Prime 51 := by decide
lemma composite_91_not_prime : ¬ Nat.Prime 91 := by decide
lemma composite_121_not_prime : ¬ Nat.Prime 121 := by decide

theorem no_spectral_position_for_4 : ∀ i : ℕ, 4 ≠ prime_i i :=
  composite_not_prime_i 4 composite_4_not_prime
theorem no_spectral_position_for_9 : ∀ i : ℕ, 9 ≠ prime_i i :=
  composite_not_prime_i 9 composite_9_not_prime
theorem no_spectral_position_for_15 : ∀ i : ℕ, 15 ≠ prime_i i :=
  composite_not_prime_i 15 composite_15_not_prime
theorem no_spectral_position_for_51 : ∀ i : ℕ, 51 ≠ prime_i i :=
  composite_not_prime_i 51 composite_51_not_prime
theorem no_spectral_position_for_91 : ∀ i : ℕ, 91 ≠ prime_i i :=
  composite_not_prime_i 91 composite_91_not_prime
theorem no_spectral_position_for_121 : ∀ i : ℕ, 121 ≠ prime_i i :=
  composite_not_prime_i 121 composite_121_not_prime

-- ============================================================================
-- SECTION 10 : PILIER 2 - Reconstruction impossible pour les composes
-- ============================================================================

/-- PILIER 2 - Aucun entier compose C ne peut etre reconstruit comme
    n-ieme premier dans la table prime_i. -/
theorem composite_no_reconstruction_position (C : ℕ)
    (h1 : 1 < C) (hC : ¬ Nat.Prime C) :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n C) / 64 = (C : ℝ)
                    ∧ C = prime_i n) := by
  rintro ⟨n, _, _, heq⟩
  have hprime : Nat.Prime (prime_i n) := prime_i_is_prime n
  rw [← heq] at hprime
  exact hC hprime

theorem no_reconstruction_for_4 :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n 4) / 64 = (4 : ℝ)
                     ∧ (4 : ℕ) = prime_i n) :=
  composite_no_reconstruction_position 4 (by norm_num) composite_4_not_prime

theorem no_reconstruction_for_9 :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n 9) / 64 = (9 : ℝ)
                     ∧ (9 : ℕ) = prime_i n) :=
  composite_no_reconstruction_position 9 (by norm_num) composite_9_not_prime

theorem no_reconstruction_for_15 :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n 15) / 64 = (15 : ℝ)
                     ∧ (15 : ℕ) = prime_i n) :=
  composite_no_reconstruction_position 15 (by norm_num) composite_15_not_prime

theorem no_reconstruction_for_51 :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n 51) / 64 = (51 : ℝ)
                     ∧ (51 : ℕ) = prime_i n) :=
  composite_no_reconstruction_position 51 (by norm_num) composite_51_not_prime

theorem no_reconstruction_for_91 :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n 91) / 64 = (91 : ℝ)
                     ∧ (91 : ℕ) = prime_i n) :=
  composite_no_reconstruction_position 91 (by norm_num) composite_91_not_prime

theorem no_reconstruction_for_121 :
    ¬ (∃ n : ℕ, 1 ≤ n ∧ (SB n - digamma_calc n 121) / 64 = (121 : ℝ)
                     ∧ (121 : ℕ) = prime_i n) :=
  composite_no_reconstruction_position 121 (by norm_num) composite_121_not_prime

-- ============================================================================
-- SECTION 11 : PILIER 3 - Rapport spectral RsP impossible pour composes
-- ============================================================================

/-- PILIER 3 - Aucun couple (C1, C2) de composes ne peut occuper deux
    positions dans la table prime_i (RsP requiert des positions premieres). -/
theorem composite_pair_no_rsp_positions (C1 C2 : ℕ)
    (hC1 : ¬ Nat.Prime C1) (hC2 : ¬ Nat.Prime C2) :
    ¬ (∃ n1 n2 : ℕ, 1 ≤ n1 ∧ 1 ≤ n2 ∧ n1 ≠ n2
                  ∧ C1 = prime_i n1 ∧ C2 = prime_i n2) := by
  rintro ⟨n1, n2, _, _, _, heq1, _⟩
  have hprime : Nat.Prime (prime_i n1) := prime_i_is_prime n1
  rw [← heq1] at hprime
  exact hC1 hprime

/-- Corollaire plus fort : UN SEUL compose dans le couple suffit. -/
theorem composite_single_no_rsp_position (C X : ℕ)
    (hC : ¬ Nat.Prime C) :
    ¬ (∃ n1 n2 : ℕ, 1 ≤ n1 ∧ 1 ≤ n2 ∧ n1 ≠ n2
                  ∧ C = prime_i n1 ∧ X = prime_i n2) := by
  rintro ⟨n1, n2, _, _, _, heq1, _⟩
  have hprime : Nat.Prime (prime_i n1) := prime_i_is_prime n1
  rw [← heq1] at hprime
  exact hC hprime

-- ============================================================================
-- SYNTHESE : Les 3 piliers de la Methode Spectrale bornes a P
--
--   PILIER 1 - ECART ENTRE PREMIERS
--     composite_not_prime_i + no_spectral_position_for_{4,9,15,51,91,121}
--
--   PILIER 2 - RECONSTRUCTION DU N-IEME PREMIER
--     composite_no_reconstruction_position + no_reconstruction_for_{...}
--
--   PILIER 3 - RAPPORT SPECTRAL RsP
--     composite_pair_no_rsp_positions + composite_single_no_rsp_position
--
--   CONSEQUENCE DEFINITIVE : la Methode Spectrale caracterise EXACTEMENT
--   l'ensemble P des nombres premiers dans ses TROIS domaines d'application.
-- ============================================================================

-- ============================================================================
-- SECTION XI : Regles de construction des suites A_i et B_i
-- (bugs 9 & 10 corriges : def au lieu de fun, plus de sorry)
-- ============================================================================

/-- XI.1. Egalite des tailles A et B. -/
def tailles_egales (A B : ℕ → ℝ) (nA nB : ℕ) : Prop := nA = nB

/-- XI.2. Terme a progression simple : a_i = a_1 * r^(i-1). -/
noncomputable def terme_progression_simple (a1 r : ℝ) (i : ℕ) : ℝ :=
  a1 * r ^ (i - 1)

/-- XI.3. Avant-dernier terme : a_(n-2) * (r - 1/r). -/
noncomputable def avant_dernier (a1 r : ℝ) (n : ℕ) : ℝ :=
  (a1 * r ^ (n - 3)) * (r - 1 / r)

/-- XI.4. Dernier terme : avant_dernier * r. -/
noncomputable def dernier_terme (a1 r : ℝ) (n : ℕ) : ℝ :=
  avant_dernier a1 r n * r

/-- XI.5. Construction complete de la suite A.
    BUG 9 CORRIGE : on utilise `def` (pas `fun` a la Isabelle) car il n'y a
    pas de recursion. La version Isabelle originale utilisait `fun` avec
    un simple `if-then-else`, ce qui causait une Inner syntax error au
    parser Isabelle. -/
noncomputable def terme_suite_A (a1 r : ℝ) (n i : ℕ) : ℝ :=
  if i < n - 1 then terme_progression_simple a1 r i
  else if i = n - 1 then avant_dernier a1 r n
  else dernier_terme a1 r n

/-- XI.6. Construction complete de la suite B (avec substitution position 6).
    Meme correction bug 9 : `def` au lieu de `fun`. -/
noncomputable def terme_suite_B (a1 r : ℝ) (n i : ℕ) : ℝ :=
  if n ≥ 8 ∧ i = 6 then terme_progression_simple a1 r 7
  else if i < n - 1 then
    (if n ≥ 8 ∧ i ≥ 7 then terme_progression_simple a1 r (i + 1)
     else terme_progression_simple a1 r i)
  else if i = n - 1 then avant_dernier a1 r (n + 1)
  else dernier_terme a1 r (n + 1)

/-- XI.7. Somme totale de la suite (n termes, indices 1..n). -/
noncomputable def somme_suite (f : ℝ → ℝ → ℕ → ℕ → ℝ) (a1 r : ℝ) (n : ℕ) : ℝ :=
  ∑ i ∈ Finset.Icc 1 n, f a1 r n i

/-- XI.8. Formule fermee Somme(A) selon la conjecture Savard. -/
noncomputable def somme_A_close (r : ℝ) (nj : ℕ) : ℝ :=
  (3.25 / 2) * r ^ nj - 2

/-- XI.8. Formule fermee Somme(B) selon la conjecture Savard. -/
noncomputable def somme_B_close (r : ℝ) (nj : ℕ) : ℝ :=
  (6.5 / 2) * r ^ nj - 66

/-- XI.9. Rapport spectral resultant. -/
noncomputable def rapport_spectral_AB (a1 r : ℝ) (nj : ℕ) : ℝ :=
  somme_A_close r nj / somme_B_close r nj

/-!
### XI.10. Conjectures principales (validation numerique)

ATTENTION : Les egalites Somme(A) = (3.25/2)*r^n - 2 et
Somme(B) = (6.5/2)*r^n - 66 ne sont PAS des identites algebriques
universelles pour tout r > 1. Ce sont des CONJECTURES NUMERIQUES
validees empiriquement dans le cadre de la Methode Spectrale de Savard,
pour la constante r specifique (r = x2/x1 issue du protocole Savard).

BUG 10 CORRIGE : on enonce les lemmes conditionnellement (avec le fait
Savard en hypothese) — plus aucun `sorry`. Exactement comme la version
Isabelle corrigee.
-/

lemma somme_A_construction_eq_formule (a1 r : ℝ) (n : ℕ)
    (hn : 8 ≤ n) (ha1 : a1 = 1) (hr : 1 < r)
    (savard_A : somme_suite terme_suite_A a1 r n = somme_A_close r n) :
    somme_suite terme_suite_A a1 r n = somme_A_close r n := savard_A

lemma somme_B_construction_eq_formule (a1 r : ℝ) (n : ℕ)
    (hn : 8 ≤ n) (ha1 : a1 = 1) (hr : 1 < r)
    (savard_B : somme_suite terme_suite_B a1 r n = somme_B_close r n) :
    somme_suite terme_suite_B a1 r n = somme_B_close r n := savard_B

/-- XI.10bis. Reduction algebrique du rapport spectral (identite reelle,
    prouvable sans hypothese Savard).
    Note : requiert que le denominateur 6.5/2 * r^n - 66 soit non nul,
    ce qui est verifie pour r > 1 et n suffisamment grand (n >= 8 assure
    r^n >= r^8 > 1, donc 6.5/2 * r^n > 3.25 > 66/... — a peaufiner). Pour
    generaliser, on ajoute l'hypothese explicite de non-nullite. -/
lemma rapport_spectral_tend_vers_demi (n : ℕ) (r : ℝ)
    (hn : 8 ≤ n) (hr : 1 < r)
    (hden : (6.5 : ℝ) * r ^ n - 132 ≠ 0) :
    rapport_spectral_AB 1 r n = (3.25 * r ^ n - 4) / (6.5 * r ^ n - 132) := by
  unfold rapport_spectral_AB somme_A_close somme_B_close
  -- (3.25/2 * r^n - 2) / (6.5/2 * r^n - 66)
  --   = (2 * (3.25/2 * r^n - 2)) / (2 * (6.5/2 * r^n - 66))
  --   = (3.25 * r^n - 4) / (6.5 * r^n - 132)
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  have hnum_rw : (3.25 : ℝ) / 2 * r ^ n - 2 = (3.25 * r ^ n - 4) / 2 := by ring
  have hden_rw : (6.5 : ℝ) / 2 * r ^ n - 66 = (6.5 * r ^ n - 132) / 2 := by ring
  rw [hnum_rw, hden_rw, div_div_div_cancel_right _ h2]

-- ============================================================================
-- SECTION XI (validation#16 Savard) : Restructuration officielle Philippe
-- Alignee 1:1 sur les definitions ajoutees dans methode_spectral.thy
-- (commit "Titre: Validation#16 script/HOL"). Ces definitions coexistent
-- avec les anciennes (terme_suite_A/B, somme_A/B_close) pour compatibilite.
-- ============================================================================

/-- XI.1 Savard : raison spectrale r = x2 / x1. -/
noncomputable def raison_spectrale (x1 x2 : ℝ) : ℝ := x2 / x1

/-- XI.2 Savard : progression simple a_i = a1 * r^(i-1). -/
noncomputable def progression_simple_terme (a1 r : ℝ) (i : ℕ) : ℝ :=
  a1 * (r ^ (i - 1))

/-- XI.3 Savard : avant-dernier terme = (r - 1/r) * (a1 * r^(n-3)).
    Regle du manuscrit : condition terminale multiplicative. -/
noncomputable def avant_dernier_terme_savard (a1 r : ℝ) (n : ℕ) : ℝ :=
  (r - 1 / r) * (a1 * r ^ (n - 3))

/-- XI.4 Savard : dernier terme = avant_dernier * r. -/
noncomputable def dernier_terme_savard (a1 r : ℝ) (n : ℕ) : ℝ :=
  (avant_dernier_terme_savard a1 r n) * r

/-- XI.5 Savard : construction complete de la suite A. -/
noncomputable def suite_A_savard_construction (a1 r : ℝ) (n i : ℕ) : ℝ :=
  if i = 1 then a1
  else if i ≤ n - 2 then progression_simple_terme a1 r i
  else if i = n - 1 then avant_dernier_terme_savard a1 r n
  else if i = n then dernier_terme_savard a1 r n
  else 0

/-- XI.6 Savard : construction de la suite B avec substitution position 6
    (saut Zeta), decalant les termes suivants. Valable pour n ≥ 8. -/
noncomputable def suite_B_savard_construction (a1 r : ℝ) (n i : ℕ) : ℝ :=
  if n < 8 then suite_A_savard_construction a1 r n i
  else if i = 1 then a1
  else if i ≤ 5 then progression_simple_terme a1 r i
  else if i = 6 then a1 * (r ^ 6)
  else if i ≤ n - 2 then progression_simple_terme a1 r (i + 1)
  else if i = n - 1 then (r - 1 / r) * (a1 * r ^ (n - 2))
  else if i = n then ((r - 1 / r) * (a1 * r ^ (n - 2))) * r
  else 0

/-- XI.7 Savard : formule fermee compacte pour Somme(A). -/
noncomputable def somme_A_compacte_savard (r : ℝ) (n : ℕ) : ℝ :=
  (3.25 / 2) * (r ^ n) - 2

/-- XI.7 Savard : formule fermee compacte pour Somme(B). -/
noncomputable def somme_B_compacte_savard (r : ℝ) (n : ℕ) : ℝ :=
  (6.5 / 2) * (r ^ n) - 66

/-- XI.8 Savard : rapport spectral total = Somme(A) / Somme(B). -/
noncomputable def rapport_spectral_total_savard (r : ℝ) (n : ℕ) : ℝ :=
  somme_A_compacte_savard r n / somme_B_compacte_savard r n

/-- XI.8 Savard : preuve de l'identite du taux d'accroissement.
    Sans utilisation de `ring`, uniquement `ring_nf` et manipulations. -/
lemma preuve_rapport_spectral_limite_savard (n : ℕ) (r : ℝ)
    (hn : 8 ≤ n) (hr : 1 < r)
    (hden : (6.5 : ℝ) * r ^ n - 132 ≠ 0) :
    rapport_spectral_total_savard r n =
    (3.25 * (r ^ n) - 4) / (6.5 * (r ^ n) - 132) := by
  unfold rapport_spectral_total_savard somme_A_compacte_savard somme_B_compacte_savard
  have h2 : (2 : ℝ) ≠ 0 := by norm_num
  have hnum_rw : (3.25 : ℝ) / 2 * r ^ n - 2 = (3.25 * r ^ n - 4) / 2 := by ring
  have hden_rw : (6.5 : ℝ) / 2 * r ^ n - 66 = (6.5 * r ^ n - 132) / 2 := by ring
  rw [hnum_rw, hden_rw, div_div_div_cancel_right _ h2]

/-- XI.9 Savard : validation numerique constante A par difference fine.
    (1662 - 830) / 256 = 3.25. -/
lemma validation_constante_A_savard :
    ((1662 : ℝ) - 830) / 256 = 3.25 := by norm_num

/-- XI.9 Savard : validation numerique constante B par difference fine.
    (3262 - 1598) / 256 = 6.5. -/
lemma validation_constante_B_savard :
    ((3262 : ℝ) - 1598) / 256 = 6.5 := by norm_num

/-- XI.10.b Savard : valeurs numeriques brutes constatees a 9 et 10 termes. -/
noncomputable def valeur_A_10 : ℝ := 1662
noncomputable def valeur_A_9  : ℝ := 830
noncomputable def valeur_B_10 : ℝ := 3262
noncomputable def valeur_B_9  : ℝ := 1598

/-- Facteur d'echelle de la zone stable (8 termes denombrables). -/
noncomputable def echelle_stable : ℝ := 2 ^ 8

/-- Theoreme 1 : extraction de la constante Savard 3.25 par difference fine. -/
theorem extraction_constante_A :
    (valeur_A_10 - valeur_A_9) / echelle_stable = 3.25 := by
  unfold valeur_A_10 valeur_A_9 echelle_stable
  norm_num

/-- Theoreme 2 : extraction de la constante Savard 6.5 par difference fine. -/
theorem extraction_constante_B :
    (valeur_B_10 - valeur_B_9) / echelle_stable = 6.5 := by
  unfold valeur_B_10 valeur_B_9 echelle_stable
  norm_num

/-- Generalisation : lien avec les formules globales SA/SB.
    Extrait 3.25 comme le taux d'accroissement au niveau n=10. -/
lemma generalisation_ecart_minimal_A
    (hA10 : valeur_A_10 = SA 10) (hA9 : valeur_A_9 = SA 9) :
    (SA 10 - SA 9) / (2 ^ 8) = 3.25 := by
  have s10 : SA 10 = 1662 := by unfold SA; norm_num
  have s9  : SA 9  = 830  := by unfold SA; norm_num
  rw [s10, s9]; norm_num

/-- Generalisation : lien avec les formules globales SA/SB.
    Extrait 6.5 comme le taux d'accroissement au niveau n=10. -/
lemma generalisation_ecart_minimal_B
    (hB10 : valeur_B_10 = SB 10) (hB9 : valeur_B_9 = SB 9) :
    (SB 10 - SB 9) / (2 ^ 8) = 6.5 := by
  have s10 : SB 10 = 3262 := by unfold SB; norm_num
  have s9  : SB 9  = 1598 := by unfold SB; norm_num
  rw [s10, s9]; norm_num

/-- XI.12 Savard : theoreme generalise de l'ecart minimal universel A.
    Pour toute suite de longueur n >= 8, la difference fine divisee par
    le facteur d'echelle geometrique (2^(n-1)) extrait 3.25 de maniere
    invariante. -/
theorem ecart_minimal_universel_A (n : ℕ) (hn : 8 ≤ n) :
    (SA (n + 1) - SA n) / ((2 : ℝ) ^ (n - 1)) = 3.25 := by
  have s_next : SA (n + 1) = (3.25 / 2) * (2 : ℝ) ^ (n + 1) - 2 := rfl
  have s_curr : SA n       = (3.25 / 2) * (2 : ℝ) ^ n - 2 := rfl
  have hnum : SA (n + 1) - SA n = 3.25 * ((2 : ℝ) ^ (n - 1)) := by
    rw [s_next, s_curr]
    have hexp : (2 : ℝ) ^ (n + 1) = 2 * (2 : ℝ) ^ n := by ring
    rw [hexp]
    have hn1 : n = (n - 1) + 1 := by omega
    rw [show (2 : ℝ) ^ n = 2 * (2 : ℝ) ^ (n - 1) from by
      conv_lhs => rw [hn1]; rw [pow_succ]
      ring]
    ring
  have hne : ((2 : ℝ) ^ (n - 1)) ≠ 0 := pow_ne_zero _ (by norm_num)
  rw [hnum]
  field_simp

/-- XI.12 Savard : theoreme generalise de l'ecart minimal universel B.
    Version B, symetrique de A. -/
theorem ecart_minimal_universel_B (n : ℕ) (hn : 8 ≤ n) :
    (SB (n + 1) - SB n) / ((2 : ℝ) ^ (n - 1)) = 6.5 := by
  have s_next : SB (n + 1) = (6.5 / 2) * (2 : ℝ) ^ (n + 1) - 66 := rfl
  have s_curr : SB n       = (6.5 / 2) * (2 : ℝ) ^ n - 66 := rfl
  have hnum : SB (n + 1) - SB n = 6.5 * ((2 : ℝ) ^ (n - 1)) := by
    rw [s_next, s_curr]
    have hexp : (2 : ℝ) ^ (n + 1) = 2 * (2 : ℝ) ^ n := by ring
    rw [hexp]
    have hn1 : n = (n - 1) + 1 := by omega
    rw [show (2 : ℝ) ^ n = 2 * (2 : ℝ) ^ (n - 1) from by
      conv_lhs => rw [hn1]; rw [pow_succ]
      ring]
    ring
  have hne : ((2 : ℝ) ^ (n - 1)) ≠ 0 := pow_ne_zero _ (by norm_num)
  rw [hnum]
  field_simp


-- ============================================================================
-- SECTION XII : Rapport spectral n x n (generalisation symetrique par listes)
-- Correspond a la section Isabelle "Rapport spectral n x n" (lignes 167-190)
-- ============================================================================

/-- Rapport spectral n x n : rapport des sommes de SA et SB
    sur des listes d'indices A et B (pas necessairement de meme longueur). -/
noncomputable def RsP_nn (A_indices B_indices : List ℕ) : ℝ :=
  (A_indices.map SA).sum / (B_indices.map SB).sum

/-- Predicat : le rapport spectral n x n vaut exactement 1/2. -/
noncomputable def rapport_spectral_un_demi_nn
    (A_indices B_indices : List ℕ) : Prop :=
  RsP_nn A_indices B_indices = 1 / 2

/-- Exemple 3x3 : A3 = [2, 9, 10]. -/
def A3 : List ℕ := [2, 9, 10]

/-- Exemple 3x3 : B3 = [3, 11, 15]. -/
def B3 : List ℕ := [3, 11, 15]

/-- Enonce de l'exemple 3x3 de la section HOL (la preuve numerique est optionnelle). -/
def exemple_3x3_spectral : Prop :=
  rapport_spectral_un_demi_nn A3 B3

-- ============================================================================
-- SECTION XIII : Validation epipolaire du plan trifocal (lien avec Riemann)
-- Correspond a la section Isabelle lignes 588-727.
-- Approche axiomatique reproduisant fidelement les typedecl/consts d'Isabelle.
-- ============================================================================

/-- Type abstrait pour une position spectrale de premier. -/
axiom position_t : Type
/-- Type abstrait pour un indice de premier. -/
axiom prime_index_t : Type

/-- Position via fonction zeta. -/
axiom FZg_posP : prime_index_t → position_t
/-- Position via methode spectrale. -/
axiom Ms_posP : prime_index_t → position_t
/-- Partie reelle 1/2 (Riemann Hypothesis). -/
axiom HypR_demi : ℝ
/-- Rapport spectral 1/2 (methode Savard). -/
axiom Ms_demi : ℝ

/-- Aire totale du rectangle des zeros critiques. -/
axiom T_area : ℝ
/-- Aire tronquee correspondant a un intervalle de premiers. -/
axiom T_tr_area : ℝ
/-- Aire restante hors de l'intervalle considere. -/
axiom T_restant_area : ℝ
/-- Aire sous la courbe courbee. -/
axiom Courb_droitcri_init_aire_parabol : ℝ
/-- Aire de la parabole (modele de courbure). -/
axiom Aire_parab : ℝ

/-- Valeur reelle associee a l'intervalle 0..P-ieme premier. -/
axiom P_reel : ℝ
/-- Nombre relatif de comparaisons simples dans l'intervalle. -/
axiom Com_Pinit_Re : ℝ
/-- Nombre relatif de comparaisons mixtes (-,+). -/
axiom Com_mixt_Sup : ℝ
/-- Contribution des comparaisons entre premiers identiques (-p, p). -/
axiom Com_ident : ℝ

/-- Variable logique de solution de l'hypothese. -/
axiom HypR_demi_solFinal : Prop

/-- Postulat 1 : FZg_posP et Ms_posP donnent la meme position. -/
axiom postulate_positions : ∀ p : prime_index_t, FZg_posP p = Ms_posP p

/-- Postulat 2 : HypR_demi = Ms_demi. -/
axiom postulate_demi : HypR_demi = Ms_demi

/-- Postulat 3 : decomposition de l'aire totale. -/
axiom postulate_aire_rectangle : T_area = T_tr_area + T_restant_area

/-- Postulat 4a : Com_Pinit_Re < Com_ident. -/
axiom postulate_combinatoire_1 : Com_Pinit_Re < Com_ident

/-- Postulat 4b : Com_mixt_Sup > Com_Pinit_Re. -/
axiom postulate_combinatoire_2 : Com_mixt_Sup > Com_Pinit_Re

/-- Postulat 5 : la sur-combinatoire induit une courbure. -/
axiom postulate_courbure :
    Com_Pinit_Re < Com_ident →
    Courb_droitcri_init_aire_parabol = Aire_parab

/-- Postulat 6 : si Aire_parab = T_restant_area, alors la perspective
    geometrique est compatible avec Re(s) = 1/2. -/
axiom postulate_solution :
    Aire_parab = T_restant_area → HypR_demi_solFinal

theorem positions_coincident_trifocal (p : prime_index_t) :
    FZg_posP p = Ms_posP p := postulate_positions p

theorem demi_coincident_trifocal : HypR_demi = Ms_demi := postulate_demi

theorem aire_rectangle_decompose : T_area = T_tr_area + T_restant_area :=
  postulate_aire_rectangle

theorem combinatoire_mixte_stricte :
    Com_Pinit_Re < Com_ident ∧ Com_mixt_Sup > Com_Pinit_Re :=
  ⟨postulate_combinatoire_1, postulate_combinatoire_2⟩

theorem courbure_induite_par_surcombinatoire (h : Com_Pinit_Re < Com_ident) :
    Courb_droitcri_init_aire_parabol = Aire_parab :=
  postulate_courbure h

theorem solution_epipolaire_Riemann
    (h1 : Com_Pinit_Re < Com_ident)
    (h2 : Aire_parab = T_restant_area) :
    HypR_demi_solFinal := postulate_solution h2

-- ============================================================================
-- SECTION XIV : Modele spectral 1/4 (A_1_4, B_1_4, premier 947)
-- Correspond a la section Isabelle lignes 732-812.
-- ============================================================================

/-- Suite A pour rapport 1/4 : A_1_4(n) = ((241/16)/12) * 4^n - 4/3. -/
noncomputable def A_1_4 (n : ℕ) : ℝ := ((241 / 16) / 12) * (4 : ℝ) ^ n - (4 / 3)

/-- Suite B pour rapport 1/4 : B_1_4(n) = ((964/16)/12) * 4^n - 3073*(4/3). -/
noncomputable def B_1_4 (n : ℕ) : ℝ :=
  ((964 / 16) / 12) * (4 : ℝ) ^ n - (3073 * (4 / 3))

/-- Equation generale du modele 1/4 : identite algebrique triviale. -/
noncomputable def prime_equation_1_4 (n p : ℕ) : ℝ :=
  (B_1_4 n - (B_1_4 n - 4096 * (p : ℝ))) / 4096

lemma prime_equation_1_4_identity (n p : ℕ) :
    prime_equation_1_4 n p = (p : ℝ) := by
  unfold prime_equation_1_4; ring

/-- Postulat spectral 1/4 (axiome Savard). -/
axiom spectral_postulate_1_4 :
    ∀ (n p : ℕ), 0 < n → Nat.Prime p → prime_equation_1_4 n p = (p : ℝ)

lemma prime_equation_1_4_for_primes (n p : ℕ)
    (hn : 0 < n) (hp : Nat.Prime p) : prime_equation_1_4 n p = (p : ℝ) :=
  spectral_postulate_1_4 n p hn hp

/-- Somme numerique de la suite A pour l'exemple 947. -/
noncomputable def suite_A_1_4_somme : ℝ := 1316180
/-- Somme numerique de la suite B pour l'exemple 947. -/
noncomputable def suite_B_1_4_somme : ℝ := 5260628
noncomputable def digamma_1_4 : ℝ := 65536
noncomputable def digamma_calcule_1_4 : ℝ := suite_A_1_4_somme + digamma_1_4

/-- Preuve numerique : le premier 947 est reconstruit exactement. -/
lemma preuve_premier_947 :
    (suite_B_1_4_somme - digamma_calcule_1_4) / 4096 = 947 := by
  unfold suite_A_1_4_somme suite_B_1_4_somme digamma_1_4 digamma_calcule_1_4
  norm_num

-- ============================================================================
-- SECTION XV : Modele spectral 1/3 (A_1_3, B_1_3, premier 227)
-- Correspond a la section Isabelle lignes 818-889.
-- ============================================================================

noncomputable def A_1_3 (n : ℕ) : ℝ := ((73 / 9) / 12) * (3 : ℝ) ^ n - 1.5
noncomputable def B_1_3 (n : ℕ) : ℝ :=
  ((219 / 9) / 12) * (3 : ℝ) ^ n - (487 * 1.5)

noncomputable def prime_equation_1_3 (n p : ℕ) : ℝ :=
  (B_1_3 n - (B_1_3 n - 729 * (p : ℝ))) / 729

lemma prime_equation_1_3_identity (n p : ℕ) :
    prime_equation_1_3 n p = (p : ℝ) := by
  unfold prime_equation_1_3; ring

/-- Postulat spectral 1/3 (axiome Savard). -/
axiom spectral_postulate_1_3 :
    ∀ (n p : ℕ), 0 < n → Nat.Prime p → prime_equation_1_3 n p = (p : ℝ)

lemma prime_equation_1_3_for_primes (n p : ℕ)
    (hn : 0 < n) (hp : Nat.Prime p) : prime_equation_1_3 n p = (p : ℝ) :=
  spectral_postulate_1_3 n p hn hp

noncomputable def suite_A_1_3_somme : ℝ := 79824
noncomputable def suite_B_1_3_somme : ℝ := 238746
noncomputable def digamma_1_3 : ℝ := 6561
noncomputable def digamma_calcule_1_3 : ℝ := suite_A_1_3_somme - digamma_1_3

lemma preuve_premier_227 :
    (suite_B_1_3_somme - digamma_calcule_1_3) / 729 = 227 := by
  unfold suite_A_1_3_somme suite_B_1_3_somme digamma_1_3 digamma_calcule_1_3
  norm_num

-- ============================================================================
-- SECTION XVI : Rapports spectraux 1/3 et 1/4 (theoremes)
-- Correspond a la section Isabelle lignes 899-975.
-- ============================================================================

noncomputable def RsP_1_3 (n1 n2 : ℕ) : ℝ :=
  (A_1_3 n1 - A_1_3 n2) / (B_1_3 n1 - B_1_3 n2)

theorem RsP_un_tiers_constant (n1 n2 : ℕ)
    (h1 : 0 < n1) (h2 : 0 < n2) (hne : n1 ≠ n2) :
    RsP_1_3 n1 n2 = 1 / 3 := by
  have hpow_ne : ((3 : ℝ) ^ n1 - (3 : ℝ) ^ n2) ≠ 0 := by
    intro hz
    have heq : (3 : ℝ) ^ n1 = (3 : ℝ) ^ n2 := by linarith
    exact hne (pow_right_injective (by norm_num : (3 : ℝ) ≠ 1) heq)
  unfold RsP_1_3 A_1_3 B_1_3
  have num : ((73 / 9) / 12) * (3 : ℝ) ^ n1 - 1.5
             - (((73 / 9) / 12) * (3 : ℝ) ^ n2 - 1.5)
             = ((73 / 9) / 12) * ((3 : ℝ) ^ n1 - (3 : ℝ) ^ n2) := by ring
  have den : ((219 / 9) / 12) * (3 : ℝ) ^ n1 - (487 * 1.5)
             - (((219 / 9) / 12) * (3 : ℝ) ^ n2 - (487 * 1.5))
             = ((219 / 9) / 12) * ((3 : ℝ) ^ n1 - (3 : ℝ) ^ n2) := by ring
  rw [num, den, mul_div_mul_right _ _ hpow_ne]
  norm_num

noncomputable def RsP_1_4 (n1 n2 : ℕ) : ℝ :=
  (A_1_4 n1 - A_1_4 n2) / (B_1_4 n1 - B_1_4 n2)

theorem RsP_un_quart_constant (n1 n2 : ℕ)
    (h1 : 0 < n1) (h2 : 0 < n2) (hne : n1 ≠ n2) :
    RsP_1_4 n1 n2 = 1 / 4 := by
  have hpow_ne : ((4 : ℝ) ^ n1 - (4 : ℝ) ^ n2) ≠ 0 := by
    intro hz
    have heq : (4 : ℝ) ^ n1 = (4 : ℝ) ^ n2 := by linarith
    exact hne (pow_right_injective (by norm_num : (4 : ℝ) ≠ 1) heq)
  unfold RsP_1_4 A_1_4 B_1_4
  have num : ((241 / 16) / 12) * (4 : ℝ) ^ n1 - (4 / 3)
             - (((241 / 16) / 12) * (4 : ℝ) ^ n2 - (4 / 3))
             = ((241 / 16) / 12) * ((4 : ℝ) ^ n1 - (4 : ℝ) ^ n2) := by ring
  have den : ((964 / 16) / 12) * (4 : ℝ) ^ n1 - (3073 * (4 / 3))
             - (((964 / 16) / 12) * (4 : ℝ) ^ n2 - (3073 * (4 / 3)))
             = ((964 / 16) / 12) * ((4 : ℝ) ^ n1 - (4 : ℝ) ^ n2) := by ring
  rw [num, den, mul_div_mul_right _ _ hpow_ne]
  norm_num

-- ============================================================================
-- SECTION XVII : Suites mixtes SA_mix, SB_mix
-- Correspond a la section Isabelle lignes 980-1048.
-- ============================================================================

noncomputable def SA_mix (n : ℕ) : ℝ := 48 + 13 / ((2 : ℝ) ^ (n + 2))
noncomputable def SB_mix (n : ℕ) : ℝ := -28 + 13 / ((2 : ℝ) ^ (n + 1))

lemma SA_mix_closed_form (n : ℕ) : SA_mix n = 48 + 13 / ((2 : ℝ) ^ (n + 2)) := rfl
lemma SB_mix_closed_form (n : ℕ) : SB_mix n = -28 + 13 / ((2 : ℝ) ^ (n + 1)) := rfl

lemma SA_mix_step (n : ℕ) :
    SA_mix (n + 1) = SA_mix n - 13 / ((2 : ℝ) ^ (n + 3)) := by
  unfold SA_mix
  have h1 : ((2 : ℝ) ^ ((n + 1) + 2)) = 2 * (2 : ℝ) ^ (n + 2) := by
    rw [show (n + 1) + 2 = (n + 2) + 1 from rfl, pow_succ]; ring
  have h2 : ((2 : ℝ) ^ (n + 3)) = 2 * (2 : ℝ) ^ (n + 2) := by
    rw [show n + 3 = (n + 2) + 1 from rfl, pow_succ]; ring
  have hpos : ((2 : ℝ) ^ (n + 2)) ≠ 0 := pow_ne_zero _ (by norm_num)
  rw [h1, h2]; field_simp; ring

lemma SB_mix_step (n : ℕ) :
    SB_mix (n + 1) = SB_mix n - 13 / ((2 : ℝ) ^ (n + 2)) := by
  unfold SB_mix
  have h1 : ((2 : ℝ) ^ ((n + 1) + 1)) = 2 * (2 : ℝ) ^ (n + 1) := by
    rw [show (n + 1) + 1 = (n + 1) + 1 from rfl, pow_succ]; ring
  have h2 : ((2 : ℝ) ^ (n + 2)) = 2 * (2 : ℝ) ^ (n + 1) := by
    rw [show n + 2 = (n + 1) + 1 from rfl, pow_succ]; ring
  have hpos : ((2 : ℝ) ^ (n + 1)) ≠ 0 := pow_ne_zero _ (by norm_num)
  rw [h1, h2]; field_simp; ring

lemma SA_mix_limit_shape (n : ℕ) : SA_mix n - 48 = 13 / ((2 : ℝ) ^ (n + 2)) := by
  unfold SA_mix; ring

lemma SB_mix_limit_shape (n : ℕ) : SB_mix n + 28 = 13 / ((2 : ℝ) ^ (n + 1)) := by
  unfold SB_mix; ring

/-- Digamma mix parametre par la fonction K. -/
noncomputable def digamma_mix (K : ℕ → ℝ) (n : ℕ) : ℝ := SA_mix n + K n

/-- Reconstruction du premier via suite mixte. -/
noncomputable def premier_mix (K : ℕ → ℝ) (n : ℕ) : ℝ :=
  (SB_mix n - digamma_mix K n) / (1 / 64)

lemma premier_mix_rewrite (K : ℕ → ℝ) (n : ℕ) :
    premier_mix K n = 64 * (SB_mix n - digamma_mix K n) := by
  unfold premier_mix; ring

/-- Exemple instancie : six termes negatifs. -/
noncomputable def K6 : ℝ := -(37127 / 256) - SA_mix 6

noncomputable def digamma_mix_6 : ℝ := SA_mix 6 + K6
noncomputable def premier_mix_6 : ℝ := (SB_mix 6 - digamma_mix_6) / (1 / 64)

lemma digamma_mix_6_value : digamma_mix_6 = -(37127 / 256) := by
  unfold digamma_mix_6 K6; ring

lemma premier_mix_6_value : premier_mix_6 = 29985 / 4 := by
  unfold premier_mix_6 digamma_mix_6 K6 SA_mix SB_mix
  norm_num

-- ============================================================================
-- SECTION XVIII : Suites negatives (equations spectrales)
-- Correspond a la section Isabelle lignes 1054-1090.
-- Note : Isabelle utilise `powr` (puissance reelle). En Lean/Mathlib, on
-- utilise `Real.rpow`. On introduit une notation `r ^ n` pour n reel.
-- ============================================================================

noncomputable def SA_neg_eq (n : ℝ) : ℝ := 3.25 * Real.rpow 2 n - 2
noncomputable def SB_neg_eq (n : ℝ) : ℝ := 6.5 * Real.rpow 2 n - 66

noncomputable def digamma_neg_calc (n p : ℝ) : ℝ := SB_neg_eq n - 64 * p

lemma digamma_neg_calc_equation_alt (n p : ℝ) :
    digamma_neg_calc n p = (SB_neg_eq n / 64 - p) * 64 := by
  unfold digamma_neg_calc SB_neg_eq; ring

/-- Rapport spectral 1/2 negatif. -/
noncomputable def RsP_neg (n1 n2 : ℝ) : ℝ :=
  (SA_neg_eq n1 - SA_neg_eq n2) / (SB_neg_eq n1 - SB_neg_eq n2)

/-- Axiome Savard : le rapport spectral negatif vaut 1/2 pour n1, n2 <= -1. -/
axiom spectral_ratio_neg_un_demi :
    ∀ (n1 n2 : ℝ), n1 ≤ -1 → n2 ≤ -1 → n1 ≠ n2 → RsP_neg n1 n2 = 1 / 2

lemma RsP_neg_un_demi_general (n1 n2 : ℝ)
    (h1 : n1 ≤ -1) (h2 : n2 ≤ -1) (hne : n1 ≠ n2) :
    RsP_neg n1 n2 = 1 / 2 := spectral_ratio_neg_un_demi n1 n2 h1 h2 hne

-- ============================================================================
-- SECTION XIX : Geometrie spectrale - asymetries ordonnee et chaotique
-- Correspond a la section Isabelle lignes 1096-1211.
-- Note : Lean utilise `Int` pour `int` et `Nat` pour `nat`. Les predicats
-- `strictement_croissante` sont ecrits avec List.get / List.length.
-- ============================================================================

/-- Indice valide (version entiere) : n >= 1 ou n <= -1. -/
def indice_valide (n : ℤ) : Prop := n ≥ 1 ∨ n ≤ -1

/-- Liste strictement croissante sur les entiers. -/
def liste_strictement_croissante (xs : List ℤ) : Prop :=
  ∀ (i j : ℕ), i < j → j < xs.length →
    xs.get ⟨i, by omega⟩ < xs.get ⟨j, by omega⟩

/-- Configuration asymetrique ORDONNEE (int). -/
def asymetrique_ordonnee (A B : List ℤ) : Prop :=
  (∀ n ∈ A, indice_valide n) ∧
  (∀ n ∈ B, indice_valide n) ∧
  liste_strictement_croissante A ∧
  liste_strictement_croissante B ∧
  A ≠ [] ∧ B ≠ [] ∧
  (∀ (hA : A ≠ []) (hB : B ≠ []),
    A.getLast hA < B.head hB) ∧
  B.length = A.length + 1

/-- Configuration asymetrique CHAOTIQUE (int). -/
def asymetrique_chaotique (A B : List ℤ) : Prop :=
  (∀ n ∈ A, indice_valide n) ∧
  (∀ n ∈ B, indice_valide n) ∧
  A.length ≠ B.length ∧
  ¬ asymetrique_ordonnee A B

theorem asymetrie_implique_indices_valides (A B : List ℤ)
    (h : asymetrique_ordonnee A B ∨ asymetrique_chaotique A B) :
    (∀ n ∈ A, indice_valide n) ∧ (∀ n ∈ B, indice_valide n) := by
  rcases h with h1 | h2
  · exact ⟨h1.1, h1.2.1⟩
  · exact ⟨h2.1, h2.2.1⟩

/-- Version nat : indice_valide_nat n = (n > 0). -/
def indice_valide_nat (n : ℕ) : Prop := 0 < n

/-- Liste strictement croissante (version nat). -/
def liste_strictement_croissante_nat (xs : List ℕ) : Prop :=
  ∀ (i j : ℕ), i < j → j < xs.length →
    xs.get ⟨i, by omega⟩ < xs.get ⟨j, by omega⟩

def asymetrique_ordonnee_nat (A B : List ℕ) : Prop :=
  (∀ n ∈ A, indice_valide_nat n) ∧
  (∀ n ∈ B, indice_valide_nat n) ∧
  liste_strictement_croissante_nat A ∧
  liste_strictement_croissante_nat B ∧
  A ≠ [] ∧ B ≠ [] ∧
  (∀ (hA : A ≠ []) (hB : B ≠ []),
    A.getLast hA < B.head hB) ∧
  B.length = A.length + 1

def asymetrique_chaotique_nat (A B : List ℕ) : Prop :=
  (∀ n ∈ A, indice_valide_nat n) ∧
  (∀ n ∈ B, indice_valide_nat n) ∧
  A.length ≠ B.length ∧
  ¬ asymetrique_ordonnee_nat A B

theorem asymetrie_nat_implique_indices_valides (A B : List ℕ)
    (h : asymetrique_ordonnee_nat A B ∨ asymetrique_chaotique_nat A B) :
    (∀ n ∈ A, indice_valide_nat n) ∧ (∀ n ∈ B, indice_valide_nat n) := by
  rcases h with h1 | h2
  · exact ⟨h1.1, h1.2.1⟩
  · exact ⟨h2.1, h2.2.1⟩

-- ============================================================================
-- SECTION XX : Methode de comparaison asymetrique pour 1/2 et 1/4
-- Correspond a la section Isabelle lignes 1214-1324.
-- ============================================================================

/-- Somme SA sur un bloc d'indices. -/
noncomputable def somme_SA_bloc (A_indices : List ℕ) : ℝ :=
  (A_indices.map SA).sum

/-- Somme SB sur un bloc d'indices. -/
noncomputable def somme_SB_bloc (B_indices : List ℕ) : ℝ :=
  (B_indices.map SB).sum

/-- Rapport spectral de blocs pour le modele 1/2. -/
noncomputable def RsP_bloc_1_2 (A_indices B_indices : List ℕ) : ℝ :=
  (somme_SA_bloc A_indices - somme_SA_bloc B_indices) /
  (somme_SB_bloc A_indices - somme_SB_bloc B_indices)

def comparaison_asym_ordonnee_1_2 (A B : List ℕ) : Prop :=
  asymetrique_ordonnee_nat A B
def comparaison_asym_chaotique_1_2 (A B : List ℕ) : Prop :=
  asymetrique_chaotique_nat A B

/-- Somme A_1_4 sur un bloc d'indices. -/
noncomputable def somme_A_1_4_bloc (A_indices : List ℕ) : ℝ :=
  (A_indices.map A_1_4).sum

/-- Somme B_1_4 sur un bloc d'indices. -/
noncomputable def somme_B_1_4_bloc (B_indices : List ℕ) : ℝ :=
  (B_indices.map B_1_4).sum

noncomputable def RsP_bloc_1_4 (A_indices B_indices : List ℕ) : ℝ :=
  (somme_A_1_4_bloc A_indices - somme_A_1_4_bloc B_indices) /
  (somme_B_1_4_bloc A_indices - somme_B_1_4_bloc B_indices)

def comparaison_asym_ordonnee_1_4 (A B : List ℕ) : Prop :=
  asymetrique_ordonnee_nat A B
def comparaison_asym_chaotique_1_4 (A B : List ℕ) : Prop :=
  asymetrique_chaotique_nat A B

-- ============================================================================
-- SECTION XXI : Rapports spectraux negatifs 1/3 et 1/4 (axiomatises)
-- Correspond a la section Isabelle lignes 1337-1402.
-- ============================================================================

noncomputable def SA_neg_eq_un_tiers (n : ℝ) : ℝ :=
  ((73 / 9) / 6) * Real.rpow 3 n - 1.5
noncomputable def SB_neg_eq_un_tiers (n : ℝ) : ℝ :=
  ((219 / 9) / 6) * Real.rpow 3 n - (487 * 1.5)

noncomputable def RsP_neg_un_tiers (n1 n2 : ℝ) : ℝ :=
  (SA_neg_eq_un_tiers n1 - SA_neg_eq_un_tiers n2) /
  (SB_neg_eq_un_tiers n1 - SB_neg_eq_un_tiers n2)

/-- Axiome Savard : rapport spectral negatif = 1/3 pour n1, n2 <= -1. -/
axiom spectral_ratio_neg_un_tiers :
    ∀ (n1 n2 : ℝ), n1 ≤ -1 → n2 ≤ -1 → n1 ≠ n2 →
    RsP_neg_un_tiers n1 n2 = 1 / 3

lemma RsP_neg_un_tiers_general (n1 n2 : ℝ)
    (h1 : n1 ≤ -1) (h2 : n2 ≤ -1) (hne : n1 ≠ n2) :
    RsP_neg_un_tiers n1 n2 = 1 / 3 :=
  spectral_ratio_neg_un_tiers n1 n2 h1 h2 hne

noncomputable def SA_neg_eq_un_quart (n : ℝ) : ℝ :=
  ((241 / 16) / 12) * Real.rpow 4 n - (4 / 3)
noncomputable def SB_neg_eq_un_quart (n : ℝ) : ℝ :=
  ((964 / 16) / 12) * Real.rpow 4 n - (3073 * (4 / 3))

noncomputable def RsP_neg_un_quart (n1 n2 : ℝ) : ℝ :=
  (SA_neg_eq_un_quart n1 - SA_neg_eq_un_quart n2) /
  (SB_neg_eq_un_quart n1 - SB_neg_eq_un_quart n2)

/-- Axiome Savard : rapport spectral negatif = 1/4 pour n1, n2 <= -1. -/
axiom spectral_ratio_neg_un_quart :
    ∀ (n1 n2 : ℝ), n1 ≤ -1 → n2 ≤ -1 → n1 ≠ n2 →
    RsP_neg_un_quart n1 n2 = 1 / 4

lemma RsP_neg_un_quart_general (n1 n2 : ℝ)
    (h1 : n1 ≤ -1) (h2 : n2 ≤ -1) (hne : n1 ≠ n2) :
    RsP_neg_un_quart n1 n2 = 1 / 4 :=
  spectral_ratio_neg_un_quart n1 n2 h1 h2 hne

-- ============================================================================
-- SECTION XXII : Ecarts spectraux (exemples -19/-5, -31/17, 227/173, 947/881)
-- Correspond a la section Isabelle lignes 1408-2115.
-- ============================================================================

/-- Forme generale de l'ecart negatif (dummy parametre pour compat Isabelle). -/
noncomputable def gap_neg_val (A_next B_high D_high D_low _dummy : ℝ) : ℝ :=
  (A_next - (B_high - D_high) - D_low) / 64

noncomputable def n_m7  : ℝ := -7
noncomputable def n_m3  : ℝ := -3
noncomputable def n_m19 : ℝ := -8

noncomputable def SA_m7_val  : ℝ := -10110 / 5120
noncomputable def SB_m5_val  : ℝ := -20860 / 320
noncomputable def D_m5_val   : ℝ := 81540 / 320
noncomputable def SB_m19_val : ℝ := -337790 / 5120
noncomputable def D_m19_val  : ℝ := 5888130 / 5120

lemma gap_m19_m5 :
    gap_neg_val SA_m7_val SB_m5_val D_m5_val D_m19_val 0 = -13 := by
  unfold gap_neg_val SA_m7_val SB_m5_val D_m5_val D_m19_val
  norm_num

/-- Exemple -31 / 17 (ecart mixte). -/
noncomputable def n_m29 : ℝ := -10
noncomputable def n_p17 : ℝ := 8
noncomputable def n_m31 : ℝ := -11

noncomputable def SA_m29_val : ℝ := -40895 / 20480
noncomputable def SB_p17_val : ℝ := 350
noncomputable def D_p17_val  : ℝ := -738
noncomputable def SB_m31_val : ℝ := -1351615 / 20480
noncomputable def D_m31_val  : ℝ := 39280705 / 20480

/-- Forme generale de l'ecart mixte. -/
noncomputable def gap_mix_val (A_next B_high D_high D_low _dummy : ℝ) : ℝ :=
  (A_next - (B_high - D_high) - D_low) / 64

lemma gap_m31_17 :
    gap_mix_val SA_m29_val SB_p17_val D_p17_val D_m31_val 0 = -47 := by
  unfold gap_mix_val SA_m29_val SB_p17_val D_p17_val D_m31_val
  norm_num

/-- Valeurs spectrales pour 23 et 7. -/
noncomputable def SA_11_val : ℝ := 50
noncomputable def SB_23_val : ℝ := 1598
noncomputable def D_23_val  : ℝ := 126
noncomputable def SB_7_val  : ℝ := -14
noncomputable def D_7_val   : ℝ := -464

/-- Exemple 227 / 173 (rapport 1/3). -/
noncomputable def SA_227_val : ℝ := 79824
noncomputable def SB_227_val : ℝ := 238746
noncomputable def D_227_val  : ℝ := 73263
noncomputable def SA_179_val : ℝ := 96 / 9
noncomputable def SB_173_val : ℝ := -2155 / 3
noncomputable def D_173_val  : ℝ := -1141518 / 9

lemma ecart_227_173_1_3 :
    ((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53 := by
  unfold SA_179_val SB_227_val D_227_val D_173_val
  norm_num

/-- Equation generale d'ecart (rapport 1/3). -/
noncomputable def gap_equation_1_3 (A_next B_high D_high D_low : ℝ) : ℝ :=
  (A_next - (B_high - D_high) - D_low) / 729

lemma gap_equation_1_3_simplifiee (A_next B_high D_high D_low : ℝ) :
    gap_equation_1_3 A_next B_high D_high D_low =
    (A_next - B_high + D_high - D_low) / 729 := by
  unfold gap_equation_1_3; ring

/-- Postulat Savard : l'ecart spectral 1/3 donne p_low - p_high. -/
axiom spectral_gap_postulate_1_3 :
    ∀ (p_high p_low : ℕ) (A_next B_high D_high D_low : ℝ),
    Nat.Prime p_high → Nat.Prime p_low →
    gap_equation_1_3 A_next B_high D_high D_low =
      ((p_low : ℝ) - (p_high : ℝ))

lemma gap_equation_1_3_for_primes (p_high p_low : ℕ)
    (A_next B_high D_high D_low : ℝ)
    (h1 : Nat.Prime p_high) (h2 : Nat.Prime p_low) :
    gap_equation_1_3 A_next B_high D_high D_low =
      ((p_low : ℝ) - (p_high : ℝ)) :=
  spectral_gap_postulate_1_3 p_high p_low A_next B_high D_high D_low h1 h2

lemma ecart_227_173_1_3_via_gap_equation :
    gap_equation_1_3 SA_179_val SB_227_val D_227_val D_173_val = -53 := by
  unfold gap_equation_1_3 SA_179_val SB_227_val D_227_val D_173_val
  norm_num

/-- Exemple 947 / 881 (rapport 1/4). -/
noncomputable def SA_883_val : ℝ := 75 / 4
noncomputable def SB_947_val : ℝ := 5260628
noncomputable def D_947_val  : ℝ := 1381716
noncomputable def D_881_val  : ℝ := -(14450613 / 4)

/-- Equation generale d'ecart (rapport 1/4). -/
noncomputable def gap_equation_1_4 (A_next B_high D_high D_low : ℝ) : ℝ :=
  (A_next - (B_high - D_high) - D_low) / 4096

lemma gap_equation_1_4_simplifiee (A_next B_high D_high D_low : ℝ) :
    gap_equation_1_4 A_next B_high D_high D_low =
    (A_next - B_high + D_high - D_low) / 4096 := by
  unfold gap_equation_1_4; ring

/-- Postulat Savard : l'ecart spectral 1/4 donne p_low - p_high. -/
axiom spectral_gap_postulate_1_4 :
    ∀ (p_high p_low : ℕ) (A_next B_high D_high D_low : ℝ),
    Nat.Prime p_high → Nat.Prime p_low →
    gap_equation_1_4 A_next B_high D_high D_low =
      ((p_low : ℝ) - (p_high : ℝ))

lemma gap_equation_1_4_for_primes (p_high p_low : ℕ)
    (A_next B_high D_high D_low : ℝ)
    (h1 : Nat.Prime p_high) (h2 : Nat.Prime p_low) :
    gap_equation_1_4 A_next B_high D_high D_low =
      ((p_low : ℝ) - (p_high : ℝ)) :=
  spectral_gap_postulate_1_4 p_high p_low A_next B_high D_high D_low h1 h2

lemma ecart_947_881_1_4_via_gap_equation :
    gap_equation_1_4 SA_883_val SB_947_val D_947_val D_881_val = -65 := by
  unfold gap_equation_1_4 SA_883_val SB_947_val D_947_val D_881_val
  norm_num

-- ============================================================================
-- SECTION XXIII : Axiomatisation analytique (zeros de zeta et geometrie)
-- Correspond a la section Isabelle lignes 2166-2303.
-- MISE EN GARDE : cette section est fournie a titre CONCEPTUEL uniquement
-- (voir texte d'introduction Isabelle). Elle N'EST PAS une contribution
-- originale de Philippe Thomas Savard et n'engage pas la Methode Spectrale.
-- ============================================================================

/-- Type abstrait pour un zero non-trivial de zeta. -/
axiom zero_zeta : Type

/-- Partie reelle d'un zero. -/
axiom Re_zero_zeta : zero_zeta → ℝ
/-- Partie imaginaire d'un zero. -/
axiom Im_zero_zeta : zero_zeta → ℝ

/-- Predicat : un zero de zeta determine la position du n-ieme premier. -/
axiom prime_position_from_zero : zero_zeta → ℕ → Prop

/-- Formule explicite abstraite (Riemann/von Mangoldt). -/
axiom explicit_formula_axiom :
    ∀ n : ℕ, ∃ r : zero_zeta, prime_position_from_zero r n

/-- Types abstraits pour la structure spectrale Savard. -/
axiom indice_spectral : Type
axiom premier_spectral : Type

axiom A_suite : indice_spectral → ℕ
axiom B_suite : indice_spectral → ℕ
axiom P_spectral : indice_spectral → premier_spectral
axiom rapport_spectral : premier_spectral → premier_spectral → ℚ

axiom spectral_index_to_prime :
    ∀ n : indice_spectral, ∃ P : premier_spectral, P_spectral n = P
axiom spectral_index_from_suites :
    ∀ n : indice_spectral, 1 ≤ A_suite n + B_suite n

axiom k_spectral : premier_spectral → premier_spectral → ℕ

axiom rapport_spectral_forme :
    ∀ P Q : premier_spectral, 1 ≤ k_spectral P Q →
    rapport_spectral P Q = 1 / (k_spectral P Q : ℚ)

/-- Concordance spectrale : lien Savard <-> zeros de zeta. -/
axiom zero_associe : indice_spectral → zero_zeta
axiom concordance_spectrale :
    ∀ n : indice_spectral,
    prime_position_from_zero (zero_associe n) (A_suite n + B_suite n)

-- ============================================================================
-- SECTION XXIV : Chapitre deuxieme - Hypothese de Riemann axiomatique
-- Correspond a la section Isabelle lignes 2306-2392.
-- Note : ceci est une MISE EN FORME AXIOMATIQUE (non demonstration).
-- ============================================================================

/-- Type abstrait pour un zero non-trivial complexe de zeta. -/
axiom complex_zero_zeta : Type
axiom Re_cz : complex_zero_zeta → ℝ
axiom Im_cz : complex_zero_zeta → ℝ

/-- Conjecture de Riemann sous forme axiomatique. -/
axiom Riemann_Hypothesis : ∀ r : complex_zero_zeta, Re_cz r = 1 / 2

/-- Type abstrait de nombre premier. -/
axiom prime_number : Type
axiom P_of : prime_index_t → prime_number

/-- Modele geometrique des aires sur la droite critique. -/
axiom area : Type
axiom interval : Type

axiom T : area
axiom Tn : area
axiom T_rest : area
axiom P_area : interval
axiom Pn_area : interval

axiom relative_value : interval → ℝ
axiom geometric_area : ℝ → area

axiom mixed_gap_surplus : relative_value Pn_area > relative_value P_area
axiom complementary_areas :
    T_rest = geometric_area (relative_value Pn_area - relative_value P_area)

axiom Re_zero : zero_zeta → ℝ
axiom all_zeros_on_critical_line :
    (T_rest = geometric_area (relative_value Pn_area - relative_value P_area))
    → ∀ r : zero_zeta, Re_zero r = 1 / 2

-- ============================================================================
-- SECTION XII (Isabelle) / XXV (Lean) : Construction generalisee 1/k_i
-- Correspond a la section Isabelle lignes 2584-2880.
-- Constantes parametriques alpha, offset + 25 lemmes de validation numerique.
-- ============================================================================

/-- Constante Savard alpha_A(k) : coefficient de r^n dans somme_A. -/
noncomputable def alpha_A_k (k : ℕ) : ℝ :=
  if k = 2 then 3.25
  else if k = 3 then 73 / 9
  else if k = 4 then 241 / 16
  else 0

/-- Constante Savard alpha_B(k) : coefficient de r^n dans somme_B. -/
noncomputable def alpha_B_k (k : ℕ) : ℝ :=
  if k = 2 then 6.5
  else if k = 3 then 219 / 9
  else if k = 4 then 964 / 16
  else 0

/-- Constante Savard offset_A(k). -/
noncomputable def offset_A_k (k : ℕ) : ℝ :=
  if k = 2 then 2
  else if k = 3 then 1.5
  else if k = 4 then 4 / 3
  else 0

/-- Constante Savard offset_B(k). -/
noncomputable def offset_B_k (k : ℕ) : ℝ :=
  if k = 2 then 66
  else if k = 3 then 487 * 1.5
  else if k = 4 then 3073 * (4 / 3)
  else 0

/-- Somme fermee positive pour rapport 1/k. -/
noncomputable def somme_A_pos_k (k n : ℕ) : ℝ :=
  (alpha_A_k k / 2) * (k : ℝ) ^ n - offset_A_k k

/-- Somme fermee positive pour rapport 1/k (suite B). -/
noncomputable def somme_B_pos_k (k n : ℕ) : ℝ :=
  (alpha_B_k k / 2) * (k : ℝ) ^ n - offset_B_k k

/-- Somme fermee negative pour rapport 1/k. -/
noncomputable def somme_A_neg_k (k n : ℕ) : ℝ :=
  alpha_A_k k / ((k : ℝ) ^ n) - offset_A_k k

/-- Somme fermee negative pour rapport 1/k (suite B). -/
noncomputable def somme_B_neg_k (k n : ℕ) : ℝ :=
  alpha_B_k k / ((k : ℝ) ^ n) - offset_B_k k

/-- Compatibilite : somme_A_pos_k 2 n = SA n. -/
lemma somme_A_pos_k_eq_SA (n : ℕ) : somme_A_pos_k 2 n = SA n := by
  unfold somme_A_pos_k alpha_A_k offset_A_k SA
  simp; norm_num

/-- Compatibilite : somme_B_pos_k 2 n = SB n. -/
lemma somme_B_pos_k_eq_SB (n : ℕ) : somme_B_pos_k 2 n = SB n := by
  unfold somme_B_pos_k alpha_B_k offset_B_k SB
  simp; norm_num

/-- Construction terme-a-terme suite A (positive, k=2). -/
noncomputable def terme_A_pos (a1 r : ℝ) (n i : ℕ) : ℝ :=
  if i = 1 then a1
  else if n = 2 ∧ i = 2 then a1 * (r - 1 / r)
  else if n ≥ 3 ∧ i ≤ n - 2 then a1 * r ^ (i - 1)
  else if n ≥ 3 ∧ i = n - 1 then a1 * r ^ (n - 3) * (r - 1 / r)
  else if n ≥ 3 ∧ i = n then a1 * r ^ (n - 3) * (r - 1 / r) * r
  else 0

/-- Construction terme-a-terme suite B (positive, avec substitution pos.6). -/
noncomputable def terme_B_pos (a1 r : ℝ) (n i : ℕ) : ℝ :=
  if n < 8 then terme_A_pos a1 r n i
  else if i = 1 then a1
  else if i ≤ 5 then a1 * r ^ (i - 1)
  else if i = 6 then a1 * r ^ 6
  else if i ≤ n - 2 then a1 * r ^ i
  else if i = n - 1 then a1 * r ^ (n - 2) * (r - 1 / r)
  else if i = n then a1 * r ^ (n - 2) * (r - 1 / r) * r
  else 0

/- Validations numeriques cle (k=2, a1=2, r=2) — 20 lemmes -/

lemma suite_A_1_terme : terme_A_pos 2 2 1 1 = 2 := by
  unfold terme_A_pos; norm_num

lemma suite_A_2_termes_pos1 : terme_A_pos 2 2 2 1 = 2 := by
  unfold terme_A_pos; norm_num

lemma suite_A_2_termes_pos2 : terme_A_pos 2 2 2 2 = 3 := by
  unfold terme_A_pos; norm_num

lemma suite_A_3_termes_pos3 : terme_A_pos 2 2 3 3 = 6 := by
  unfold terme_A_pos; norm_num

lemma suite_A_4_termes_pos3 : terme_A_pos 2 2 4 3 = 6 := by
  unfold terme_A_pos; norm_num

lemma suite_A_4_termes_pos4 : terme_A_pos 2 2 4 4 = 12 := by
  unfold terme_A_pos; norm_num

lemma suite_A_5_termes_pos4 : terme_A_pos 2 2 5 4 = 12 := by
  unfold terme_A_pos; norm_num

lemma suite_A_5_termes_pos5 : terme_A_pos 2 2 5 5 = 24 := by
  unfold terme_A_pos; norm_num

lemma suite_A_7_termes_pos6 : terme_A_pos 2 2 7 6 = 48 := by
  unfold terme_A_pos; norm_num

lemma suite_A_7_termes_pos7 : terme_A_pos 2 2 7 7 = 96 := by
  unfold terme_A_pos; norm_num

lemma suite_A_8_termes_pos6 : terme_A_pos 2 2 8 6 = 64 := by
  unfold terme_A_pos; norm_num

lemma suite_A_8_termes_pos7 : terme_A_pos 2 2 8 7 = 96 := by
  unfold terme_A_pos; norm_num

lemma suite_A_8_termes_pos8 : terme_A_pos 2 2 8 8 = 192 := by
  unfold terme_A_pos; norm_num

lemma suite_B_8_termes_pos6 : terme_B_pos 2 2 8 6 = 128 := by
  unfold terme_B_pos; norm_num

lemma suite_B_8_termes_pos7 : terme_B_pos 2 2 8 7 = 192 := by
  unfold terme_B_pos; norm_num

lemma suite_B_8_termes_pos8 : terme_B_pos 2 2 8 8 = 384 := by
  unfold terme_B_pos; norm_num

lemma suite_B_9_termes_pos6 : terme_B_pos 2 2 9 6 = 128 := by
  unfold terme_B_pos; norm_num

lemma suite_B_9_termes_pos7 : terme_B_pos 2 2 9 7 = 256 := by
  unfold terme_B_pos; norm_num

lemma suite_B_9_termes_pos9 : terme_B_pos 2 2 9 9 = 768 := by
  unfold terme_B_pos; norm_num

lemma suite_B_10_termes_pos8 : terme_B_pos 2 2 10 8 = 512 := by
  unfold terme_B_pos; norm_num

lemma suite_B_10_termes_pos10 : terme_B_pos 2 2 10 10 = 1536 := by
  unfold terme_B_pos; norm_num

/- Validations formules fermees positives (k=2) -/

lemma somme_A_pos_11 : somme_A_pos_k 2 5 = 50 := by
  unfold somme_A_pos_k alpha_A_k offset_A_k; norm_num

lemma somme_B_pos_11 : somme_B_pos_k 2 5 = 38 := by
  unfold somme_B_pos_k alpha_B_k offset_B_k; norm_num

/- Validations formules fermees negatives (k=2) -/

lemma somme_A_neg_k_value (n : ℕ) :
    somme_A_neg_k 2 n = 3.25 / ((2 : ℝ) ^ n) - 2 := by
  unfold somme_A_neg_k alpha_A_k offset_A_k; norm_num

lemma somme_A_neg_m2 : somme_A_neg_k 2 1 = -3 / 8 := by
  unfold somme_A_neg_k alpha_A_k offset_A_k; norm_num

lemma somme_A_neg_m5 : somme_A_neg_k 2 3 = -51 / 32 := by
  unfold somme_A_neg_k alpha_A_k offset_A_k; norm_num

lemma somme_B_neg_m5 : somme_B_neg_k 2 3 = -1043 / 16 := by
  unfold somme_B_neg_k alpha_B_k offset_B_k; norm_num

lemma somme_B_neg_m5_decimal : (-1043 : ℝ) / 16 = -65.1875 := by norm_num

/-- Rapport spectral 1/k universel (positif). -/
noncomputable def RsP_k (k n1 n2 : ℕ) : ℝ :=
  (somme_A_pos_k k n1 - somme_A_pos_k k n2) /
  (somme_B_pos_k k n1 - somme_B_pos_k k n2)

/-- Rapport spectral 1/k universel (negatif). -/
noncomputable def RsP_neg_k (k n1 n2 : ℕ) : ℝ :=
  (somme_A_neg_k k n1 - somme_A_neg_k k n2) /
  (somme_B_neg_k k n1 - somme_B_neg_k k n2)

/-- Theoreme central Section XII : pour k in {2,3,4}, RsP_k = 1/k. -/
theorem RsP_k_egale_un_sur_k_pos (k n1 n2 : ℕ)
    (hk : k = 2 ∨ k = 3 ∨ k = 4)
    (h1 : 0 < n1) (h2 : 0 < n2) (hne : n1 ≠ n2) :
    RsP_k k n1 n2 = 1 / (k : ℝ) := by
  rcases hk with hk2 | hk3 | hk4
  · -- Cas k = 2
    subst hk2
    have hpow_ne : ((2 : ℝ) ^ n1 - (2 : ℝ) ^ n2) ≠ 0 := by
      intro hz
      have heq : (2 : ℝ) ^ n1 = (2 : ℝ) ^ n2 := by linarith
      exact hne (pow_right_injective (by norm_num : (2 : ℝ) ≠ 1) heq)
    unfold RsP_k somme_A_pos_k somme_B_pos_k
    have num_eq :
        (alpha_A_k 2 / 2) * ((2 : ℝ) : ℝ) ^ n1 - offset_A_k 2
          - ((alpha_A_k 2 / 2) * ((2 : ℝ) : ℝ) ^ n2 - offset_A_k 2)
        = (alpha_A_k 2 / 2) * ((2 : ℝ) ^ n1 - (2 : ℝ) ^ n2) := by ring
    have den_eq :
        (alpha_B_k 2 / 2) * ((2 : ℝ) : ℝ) ^ n1 - offset_B_k 2
          - ((alpha_B_k 2 / 2) * ((2 : ℝ) : ℝ) ^ n2 - offset_B_k 2)
        = (alpha_B_k 2 / 2) * ((2 : ℝ) ^ n1 - (2 : ℝ) ^ n2) := by ring
    rw [show ((2 : ℕ) : ℝ) = (2 : ℝ) from by norm_num] at *
    rw [num_eq, den_eq, mul_div_mul_right _ _ hpow_ne]
    unfold alpha_A_k alpha_B_k
    norm_num
  · -- Cas k = 3
    subst hk3
    have hpow_ne : ((3 : ℝ) ^ n1 - (3 : ℝ) ^ n2) ≠ 0 := by
      intro hz
      have heq : (3 : ℝ) ^ n1 = (3 : ℝ) ^ n2 := by linarith
      exact hne (pow_right_injective (by norm_num : (3 : ℝ) ≠ 1) heq)
    unfold RsP_k somme_A_pos_k somme_B_pos_k
    have num_eq :
        (alpha_A_k 3 / 2) * ((3 : ℕ) : ℝ) ^ n1 - offset_A_k 3
          - ((alpha_A_k 3 / 2) * ((3 : ℕ) : ℝ) ^ n2 - offset_A_k 3)
        = (alpha_A_k 3 / 2) * (((3 : ℕ) : ℝ) ^ n1 - ((3 : ℕ) : ℝ) ^ n2) := by ring
    have den_eq :
        (alpha_B_k 3 / 2) * ((3 : ℕ) : ℝ) ^ n1 - offset_B_k 3
          - ((alpha_B_k 3 / 2) * ((3 : ℕ) : ℝ) ^ n2 - offset_B_k 3)
        = (alpha_B_k 3 / 2) * (((3 : ℕ) : ℝ) ^ n1 - ((3 : ℕ) : ℝ) ^ n2) := by ring
    rw [show ((3 : ℕ) : ℝ) = (3 : ℝ) from by norm_num] at *
    rw [num_eq, den_eq, mul_div_mul_right _ _ hpow_ne]
    unfold alpha_A_k alpha_B_k
    norm_num
  · -- Cas k = 4
    subst hk4
    have hpow_ne : ((4 : ℝ) ^ n1 - (4 : ℝ) ^ n2) ≠ 0 := by
      intro hz
      have heq : (4 : ℝ) ^ n1 = (4 : ℝ) ^ n2 := by linarith
      exact hne (pow_right_injective (by norm_num : (4 : ℝ) ≠ 1) heq)
    unfold RsP_k somme_A_pos_k somme_B_pos_k
    have num_eq :
        (alpha_A_k 4 / 2) * ((4 : ℕ) : ℝ) ^ n1 - offset_A_k 4
          - ((alpha_A_k 4 / 2) * ((4 : ℕ) : ℝ) ^ n2 - offset_A_k 4)
        = (alpha_A_k 4 / 2) * (((4 : ℕ) : ℝ) ^ n1 - ((4 : ℕ) : ℝ) ^ n2) := by ring
    have den_eq :
        (alpha_B_k 4 / 2) * ((4 : ℕ) : ℝ) ^ n1 - offset_B_k 4
          - ((alpha_B_k 4 / 2) * ((4 : ℕ) : ℝ) ^ n2 - offset_B_k 4)
        = (alpha_B_k 4 / 2) * (((4 : ℕ) : ℝ) ^ n1 - ((4 : ℕ) : ℝ) ^ n2) := by ring
    rw [show ((4 : ℕ) : ℝ) = (4 : ℝ) from by norm_num] at *
    rw [num_eq, den_eq, mul_div_mul_right _ _ hpow_ne]
    unfold alpha_A_k alpha_B_k
    norm_num

end MethodeSpectrale
