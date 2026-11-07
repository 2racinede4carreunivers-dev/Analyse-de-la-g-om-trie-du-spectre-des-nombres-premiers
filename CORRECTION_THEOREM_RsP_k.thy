theorem RsP_k_egale_un_sur_k_pos:
  assumes "k \<in> {2, 3, 4}" "n1 > 0" "n2 > 0" "n1 \<noteq> n2"
  shows "RsP_k k n1 n2 = 1 / real k"
proof -
  from assms(1) consider "k = 2" | "k = 3" | "k = 4" by auto
  thus ?thesis
  proof cases
    case 1
    (* k = 2 *)
    have hne_pow_2: "(2::real)^n1 - 2^n2 \<noteq> 0"
    proof (cases "n1 < n2")
      case True
      hence "(2::real)^n1 < 2^n2"
        using power_strict_increasing[of n1 n2 "2::real"] by simp
      thus ?thesis by simp
    next
      case False
      with assms(4) have "n2 < n1" by simp
      hence "(2::real)^n2 < 2^n1"
        using power_strict_increasing[of n2 n1 "2::real"] by simp
      thus ?thesis by simp
    qed
    
    have A_diff: "somme_A_pos_k 2 n1 - somme_A_pos_k 2 n2 =
                   (alpha_A_k 2 / 2) * (2 ^ n1 - 2 ^ n2)"
      unfolding somme_A_pos_k_def by (simp add: algebra_simps)
    
    have B_diff: "somme_B_pos_k 2 n1 - somme_B_pos_k 2 n2 =
                   (alpha_B_k 2 / 2) * (2 ^ n1 - 2 ^ n2)"
      unfolding somme_B_pos_k_def by (simp add: algebra_simps)
    
    have "RsP_k 2 n1 n2 = 
          ((alpha_A_k 2 / 2) * (2 ^ n1 - 2 ^ n2)) /
          ((alpha_B_k 2 / 2) * (2 ^ n1 - 2 ^ n2))"
      unfolding RsP_k_def by (simp add: A_diff B_diff)
    
    also have "... = (alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)"
      using hne_pow_2 by (field_simp; ring)
    
    also have "... = 1 / real 2"
      unfolding alpha_A_k_def alpha_B_k_def by norm_num
    
    finally show ?thesis using 1 by simp
  
  next
    case 2
    (* k = 3 *)
    have hne_pow_3: "(3::real)^n1 - 3^n2 \<noteq> 0"
    proof (cases "n1 < n2")
      case True
      hence "(3::real)^n1 < 3^n2"
        using power_strict_increasing[of n1 n2 "3::real"] by simp
      thus ?thesis by simp
    next
      case False
      with assms(4) have "n2 < n1" by simp
      hence "(3::real)^n2 < 3^n1"
        using power_strict_increasing[of n2 n1 "3::real"] by simp
      thus ?thesis by simp
    qed
    
    have A_diff: "somme_A_pos_k 3 n1 - somme_A_pos_k 3 n2 =
                   (alpha_A_k 3 / 2) * (3 ^ n1 - 3 ^ n2)"
      unfolding somme_A_pos_k_def by (simp add: algebra_simps)
    
    have B_diff: "somme_B_pos_k 3 n1 - somme_B_pos_k 3 n2 =
                   (alpha_B_k 3 / 2) * (3 ^ n1 - 3 ^ n2)"
      unfolding somme_B_pos_k_def by (simp add: algebra_simps)
    
    have "RsP_k 3 n1 n2 = 
          ((alpha_A_k 3 / 2) * (3 ^ n1 - 3 ^ n2)) /
          ((alpha_B_k 3 / 2) * (3 ^ n1 - 3 ^ n2))"
      unfolding RsP_k_def by (simp add: A_diff B_diff)
    
    also have "... = (alpha_A_k 3 / 2) / (alpha_B_k 3 / 2)"
      using hne_pow_3 by (field_simp; ring)
    
    also have "... = 1 / real 3"
      unfolding alpha_A_k_def alpha_B_k_def by norm_num
    
    finally show ?thesis using 2 by simp
  
  next
    case 3
    (* k = 4 *)
    have hne_pow_4: "(4::real)^n1 - 4^n2 \<noteq> 0"
    proof (cases "n1 < n2")
      case True
      hence "(4::real)^n1 < 4^n2"
        using power_strict_increasing[of n1 n2 "4::real"] by simp
      thus ?thesis by simp
    next
      case False
      with assms(4) have "n2 < n1" by simp
      hence "(4::real)^n2 < 4^n1"
        using power_strict_increasing[of n2 n1 "4::real"] by simp
      thus ?thesis by simp
    qed
    
    have A_diff: "somme_A_pos_k 4 n1 - somme_A_pos_k 4 n2 =
                   (alpha_A_k 4 / 2) * (4 ^ n1 - 4 ^ n2)"
      unfolding somme_A_pos_k_def by (simp add: algebra_simps)
    
    have B_diff: "somme_B_pos_k 4 n1 - somme_B_pos_k 4 n2 =
                   (alpha_B_k 4 / 2) * (4 ^ n1 - 4 ^ n2)"
      unfolding somme_B_pos_k_def by (simp add: algebra_simps)
    
    have "RsP_k 4 n1 n2 = 
          ((alpha_A_k 4 / 2) * (4 ^ n1 - 4 ^ n2)) /
          ((alpha_B_k 4 / 2) * (4 ^ n1 - 4 ^ n2))"
      unfolding RsP_k_def by (simp add: A_diff B_diff)
    
    also have "... = (alpha_A_k 4 / 2) / (alpha_B_k 4 / 2)"
      using hne_pow_4 by (field_simp; ring)
    
    also have "... = 1 / real 4"
      unfolding alpha_A_k_def alpha_B_k_def by norm_num
    
    finally show ?thesis using 3 by simp
  qed
qed
