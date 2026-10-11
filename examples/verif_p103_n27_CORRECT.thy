theory verif_p103_n27
    imports methode_spectral
begin

(* Script généré automatiquement pour vérifier le premier 103 avec n=27 *)

section "Vérification 103 via modèle 1/2"

(* Formules spectrales *)
(* SA(n) = (3.25/2) × 2^n - 2 *)
(* SB(n) = (6.5/2) × 2^n - 66 *)
(* digamma(n,p) = SB(n) - 64×p *)

lemma SA_n_27_valeur:
  "SA 27 = 218103806.0"
  unfolding SA_def by simp

lemma SB_n_27_valeur:
  "SB 27 = 436207550.0"
  unfolding SB_def by simp

lemma digamma_calc_n_27_p_103:
  "digamma_calc 27 103 = 436200958.0"
  unfolding digamma_calc_def SB_def
  by (simp add: diff_eq_iff_eq_add)

lemma verif_premier_103_n_27:
  "prime_equation 27 103 = real 103"
  unfolding prime_equation_def
  by (simp add: SA_n_27_valeur SB_n_27_valeur digamma_calc_n_27_p_103)

(* Vérification arithmétique détaillée *)
lemma digamma_calculation_detail:
  "SB 27 - 64 * 103 = 436200958.0"
  unfolding SB_def
  by (norm_num; ring)

(* Invariant critique *)
lemma position_invariant:
  "position 103 = 27"
  by simp

end
