theory verif_p1097_n23_ratio4
  imports methode_spectral
begin

(* Fragment HOL corrigé — ratio 1/4, n=23, p=1097 *)
(* CORRECTION DEF-05 : formules SA_k4_def/SB_k4_def, invariant asymétrique *)
(*
   FORMULES SPECTRALES k=4 :
   SA(n) = (241/192) * 4^n - 4/3
   SB(n) = (964/192) * 4^n - 12292/3
   digamma(n,p) = SB(n) - p * 4^6
   Reconstruction : (SB(n) - digamma(n,p)) / 4^6 = p
*)

section "Verification p=1097 via modele 1/4"

(* CORRECTION : SA_k4_def encode le modèle k=4, pas le modèle 1/2 *)
lemma SA_n_23_ratio_4:
  "SA_k4 23 = 88327434098004"
  unfolding SA_k4_def by norm_num

lemma SB_n_23_ratio_4:
  "SB_k4 23 = 353309736387924"
  unfolding SB_k4_def by norm_num

lemma digamma_n23_p1097:
  "digamma_k4 23 1097 = SB_k4 23 - 1097 * 4^6"
  unfolding digamma_k4_def by simp

lemma digamma_valeur:
  "SB_k4 23 - 1097 * 4^6 = 353309731894612"
  by (simp add: SB_n_23_ratio_4)

lemma verif_premier_1097_n_23:
  "(SB_k4 23 - digamma_k4 23 1097) / 4^6 = 1097"
  by (simp add: SB_n_23_ratio_4 digamma_n23_p1097)

(* Invariant ASYMÉTRIQUE — CORRECTION DEF-05 *)
(* n = 23 = nombre_de_termes  !=  position du premier 1097 *)
(* 1097 est le 184ème nombre premier ; n=23 est la quantité de termes *)
lemma invariant_ratio_asymetrique:
  "n_termes = 23 \<and> position_1097 = 184 \<and> position_1097 \<noteq> 23"
  by (simp add: position_1097_eq_184)

end
