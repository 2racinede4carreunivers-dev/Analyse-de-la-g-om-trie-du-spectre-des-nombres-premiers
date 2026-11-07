theory test_probe
  imports Complex_Main
begin

definition ancrage_valide :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> string \<Rightarrow> bool" where
  "ancrage_valide k p rang branche = (p > 1 \<and> rang > 0)"

lemma ancrage_k3 : "ancrage_valide 3 227 49 ''A8-''" by (simp add: ancrage_valide_def)
lemma ancrage_k4 : "ancrage_valide 4 947 161 ''A8+''" by (simp add: ancrage_valide_def)

definition inverser_SA_k2 :: "real \<Rightarrow> real" where
  "inverser_SA_k2 v = log 2 ((8/13) * (v + 2))"

lemma cert1: "abs (real (6590 - (64::nat) * 24)) = (5054::real)" by simp
lemma cert2: "inverser_SA_k2 5054 = log 2 (40448 / 13)"
  unfolding inverser_SA_k2_def by simp

lemma log_not_in_nats: "log 2 ((40448/13)::real) \<notin> \<nat>"
proof
  assume "log 2 (40448/13) \<in> \<nat>"
  then obtain n :: nat where eq: "real n = log 2 (40448/13)"
    unfolding Nats_def by blast
  have pos: "(0::real) < 40448/13" by simp
  from eq have "2 powr (real n) = 2 powr (log 2 (40448/13))" by simp
  also have "\<dots> = 40448/13"
    using powr_log_cancel[of 2 "40448/13"] pos by simp
  finally have pow_eq: "(2::real) ^ n = 40448/13"
    by (simp add: powr_realpow)
  have lo: "(2::real) ^ 11 < 40448/13" by simp
  have hi: "(40448/13::real) < (2::real) ^ 12" by simp
  show False
  proof cases
    assume "n \<le> 11"
    then have "(2::real) ^ n \<le> 2 ^ 11" by simp
    with pow_eq lo show False by linarith
  next
    assume "\<not> n \<le> 11"
    then have "12 \<le> n" by simp
    then have "(2::real) ^ 12 \<le> 2 ^ n" by simp
    with pow_eq hi show False by linarith
  qed
qed

lemma P1: assumes "n < m" shows "(2::real)^n < (2::real)^m"
  using assms by simp

lemma P2: assumes "n \<ge> 1" shows "(2::real) \<le> 2^n"
  using assms by (simp add: power_increasing[of 1 n 2])

lemma P3: assumes "n \<ge> 5" shows "(32::real) \<le> 2^n"
  using assms by (simp add: power_increasing[of 5 n 2])

lemma P4: "\<forall> x y. dist (x::real) (1/2) + dist y (1/2) \<ge> dist x y"
  by (metis dist_triangle dist_commute)

lemma P6: "(3::real) \<in> \<real>" by simp

definition Sr2_validation :: "real" where "Sr2_validation = 3 / 2"
definition rsr_validation :: "real" where "rsr_validation = 1 / 2"

lemma Sr2_coherence: "Sr2_validation = 3/2" unfolding Sr2_validation_def by simp
lemma rsr_coherence: "rsr_validation = 1/2" unfolding rsr_validation_def by simp

end
