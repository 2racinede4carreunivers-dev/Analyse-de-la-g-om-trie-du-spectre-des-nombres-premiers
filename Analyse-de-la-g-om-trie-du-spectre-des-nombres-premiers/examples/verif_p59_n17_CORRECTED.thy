theory verif_p59_n17_CORRECTED
  imports methode_spectral
begin

(* Script corrigé - le 17ième nombre premier est 59 *)
(* 
   FORMULES SPECTRALES:
   SA(17) = (3.25/2) × 2^17 - 2 = 212990.0
   SB(17) = (6.5/2) × 2^17 - 66 = 425918.0
   digamma(17, 59) = SB(17) - 64×59 = 425918.0 - 3776 = 425854.0
*)

section "Verification 59 via modele 1/2"

lemma SA_n_17_valeur:
  "SA 17 = 212990.0"
  unfolding SA_def by simp

lemma SB_n_17_valeur:
  "SB 17 = 425918.0"
  unfolding SB_def by simp

(* LA FORMULE CORRECTE - PAS JUSTE 59.0 ! *)
lemma digamma_calc_n_17_p_59:
  "digamma_calc 17 59 = 425854.0"
  unfolding digamma_calc_def SB_def
  by (simp add: diff_eq_iff_eq_add)

lemma verif_premier_59_n_17:
  "prime_equation 17 59 = real 59"
  unfolding prime_equation_def
  by (simp add: SA_n_17_valeur SB_n_17_valeur digamma_calc_n_17_p_59)

(* Verification arithmetique detaillee *)
lemma digamma_calculation_detail:
  "SB 17 - 64 * 59 = 425854.0"
  unfolding SB_def
  by (norm_num; ring)

(* Invariant critique *)
lemma position_invariant:
  "position 59 = 17"
  by simp

end
