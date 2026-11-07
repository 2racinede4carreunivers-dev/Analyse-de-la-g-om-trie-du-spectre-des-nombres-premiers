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
    
    (* Déplier les définitions *)
    have "RsP_k 2 n1 n2 = (somme_A_pos_k 2 n1 - somme_A_pos_k 2 n2) / 
                           (somme_B_pos_k 2 n1 - somme_B_pos_k 2 n2)"
      unfolding RsP_k_def by simp
    
    (* Déplier somme_A_pos_k et somme_B_pos_k *)
    also have "... = (((alpha_A_k 2 / 2) * (2 ^ n1) - offset_A_k 2) - 
                      ((alpha_A_k 2 / 2) * (2 ^ n2) - offset_A_k 2)) /
                     (((alpha_B_k 2 / 2) * (2 ^ n1) - offset_B_k 2) - 
                      ((alpha_B_k 2 / 2) * (2 ^ n2) - offset_B_k 2))"
      unfolding somme_A_pos_k_def somme_B_pos_k_def by simp
    
    (* Simplifier les différences (les offset s'annulent) *)
    also have "... = ((alpha_A_k 2 / 2) * (2 ^ n1 - 2 ^ n2)) /
                     ((alpha_B_k 2 / 2) * (2 ^ n1 - 2 ^ n2))"
      by (ring_nf; simp add: hne_pow_2)
    
    (* Utiliser field_simp correctement avec parenthèses explicites *)
    also have "... = ((alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)) * 
                     ((2 ^ n1 - 2 ^ n2) / (2 ^ n1 - 2 ^ n2))"
      by (field_simp [hne_pow_2]; ring)
    
    also have "... = ((alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)) * 1"
      using hne_pow_2 by (field_simp; ring)
    
    also have "... = (alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)"
      by simp
    
    (* Évaluer les constantes Savard *)
    also have "... = 3.25 / 2 / (6.5 / 2)"
      unfolding alpha_A_k_def alpha_B_k_def by simp
    
    also have "... = 3.25 / 6.5"
      by (field_simp; ring)
    
    also have "... = 1 / 2"
      by norm_num
    
    also have "... = 1 / real 2"
      by simp
    
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
    
    have "RsP_k 3 n1 n2 = (somme_A_pos_k 3 n1 - somme_A_pos_k 3 n2) / 
                           (somme_B_pos_k 3 n1 - somme_B_pos_k 3 n2)"
      unfolding RsP_k_def by simp
    
    also have "... = (((alpha_A_k 3 / 2) * (3 ^ n1) - offset_A_k 3) - 
                      ((alpha_A_k 3 / 2) * (3 ^ n2) - offset_A_k 3)) /
                     (((alpha_B_k 3 / 2) * (3 ^ n1) - offset_B_k 3) - 
                      ((alpha_B_k 3 / 2) * (3 ^ n2) - offset_B_k 3))"
      unfolding somme_A_pos_k_def somme_B_pos_k_def by simp
    
    also have "... = ((alpha_A_k 3 / 2) * (3 ^ n1 - 3 ^ n2)) /
                     ((alpha_B_k 3 / 2) * (3 ^ n1 - 3 ^ n2))"
      by (ring_nf; simp add: hne_pow_3)
    
    also have "... = ((alpha_A_k 3 / 2) / (alpha_B_k 3 / 2)) * 
                     ((3 ^ n1 - 3 ^ n2) / (3 ^ n1 - 3 ^ n2))"
      by (field_simp [hne_pow_3]; ring)
    
    also have "... = ((alpha_A_k 3 / 2) / (alpha_B_k 3 / 2)) * 1"
      using hne_pow_3 by (field_simp; ring)
    
    also have "... = (alpha_A_k 3 / 2) / (alpha_B_k 3 / 2)"
      by simp
    
    also have "... = (73/9) / 2 / ((219/9) / 2)"
      unfolding alpha_A_k_def alpha_B_k_def by simp
    
    also have "... = (73/9) / (219/9)"
      by (field_simp; ring)
    
    also have "... = 1 / 3"
      by norm_num
    
    also have "... = 1 / real 3"
      by simp
    
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
    
    have "RsP_k 4 n1 n2 = (somme_A_pos_k 4 n1 - somme_A_pos_k 4 n2) / 
                           (somme_B_pos_k 4 n1 - somme_B_pos_k 4 n2)"
      unfolding RsP_k_def by simp
    
    also have "... = (((alpha_A_k 4 / 2) * (4 ^ n1) - offset_A_k 4) - 
                      ((alpha_A_k 4 / 2) * (4 ^ n2) - offset_A_k 4)) /
                     (((alpha_B_k 4 / 2) * (4 ^ n1) - offset_B_k 4) - 
                      ((alpha_B_k 4 / 2) * (4 ^ n2) - offset_B_k 4))"
      unfolding somme_A_pos_k_def somme_B_pos_k_def by simp
    
    also have "... = ((alpha_A_k 4 / 2) * (4 ^ n1 - 4 ^ n2)) /
                     ((alpha_B_k 4 / 2) * (4 ^ n1 - 4 ^ n2))"
      by (ring_nf; simp add: hne_pow_4)
    
    also have "... = ((alpha_A_k 4 / 2) / (alpha_B_k 4 / 2)) * 
                     ((4 ^ n1 - 4 ^ n2) / (4 ^ n1 - 4 ^ n2))"
      by (field_simp [hne_pow_4]; ring)
    
    also have "... = ((alpha_A_k 4 / 2) / (alpha_B_k 4 / 2)) * 1"
      using hne_pow_4 by (field_simp; ring)
    
    also have "... = (alpha_A_k 4 / 2) / (alpha_B_k 4 / 2)"
      by simp
    
    also have "... = (241/16) / 2 / ((964/16) / 2)"
      unfolding alpha_A_k_def alpha_B_k_def by simp
    
    also have "... = (241/16) / (964/16)"
      by (field_simp; ring)
    
    also have "... = 1 / 4"
      by norm_num
    
    also have "... = 1 / real 4"
      by simp
    
    finally show ?thesis using 3 by simp
  qed
qed
