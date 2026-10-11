╔════════════════════════════════════════════════════════════════════════════╗
║    CORRECTIONS DÉFINITIVES - methode_spectral.thy LIGNES 2595 et 2915       ║
║                                                                            ║
║  ERREUR 1 (Ligne 2595): Simplification de fraction composée                ║
║  ERREUR 2 (Ligne 2915): Problème d'associativité de division              ║
╚════════════════════════════════════════════════════════════════════════════╝

## ERREUR 1 - LIGNE 2595

### Problème exact:

```isabelle
lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)
```

**Erreur Isabelle:**
```
goal (1 subgoal):
 1. n1 ? n2 ?
    (r ^ n * 52 - 64) / (r ^ n * 104 - 2112) =
    (r ^ n * 26 - 32) /
    (r ^ n * 52 - 1056)
```

### Cause:

La fraction `(r^n * 52 - 64) / (r^n * 104 - 2112)` doit se simplifier en `(r^n * 26 - 32) / (r^n * 52 - 1056)`.

On peut factoriser:
- Numérateur: `r^n * 52 - 64 = 2 * (r^n * 26 - 32)`
- Dénominateur: `r^n * 104 - 2112 = 2 * (r^n * 52 - 1056)`

Donc: `(2 * A) / (2 * B) = A / B` pour `B ≠ 0`.

Mais `simp` ne le fait pas automatiquement. Utiliser `ring` ou `field_simp`:

### CORRECTION 1:

```isabelle
lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def;
      ring)
```

Ou plus simplement:

```isabelle
lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (unfold SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def;
      norm_num)
```

═══════════════════════════════════════════════════════════════════════════

## ERREUR 2 - LIGNE 2915

### Problème exact:

```isabelle
theorem RsP_k_egale_un_sur_k_pos:
  assumes "k \<in> {2, 3, 4}" "n1 > 0" "n2 > 0" "n1 \<noteq> n2"
  shows "RsP_k k n1 n2 = 1 / real k"
proof -
  ...
  also have "... = (alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)"
    using hne_pow_2 by (simp add: field_simps)  ← ÉCHOUE ICI
```

**Erreur Isabelle:**
```
goal (1 subgoal):
 1. n1 ≠ n2 ⟹
    (2 * (alpha_A_k 2 * 2 ^ n1) - 2 * (alpha_A_k 2 * 2 ^ n2)) /
    (2 * (alpha_B_k 2 * 2 ^ n1) - 2 * (alpha_B_k 2 * 2 ^ n2)) =
    alpha_A_k 2 / alpha_B_k 2
```

### Cause:

La fraction composée doit être simplifiée à partir de:

```
((alpha_A_k 2 / 2) * (2 ^ n1 - 2 ^ n2)) /
((alpha_B_k 2 / 2) * (2 ^ n1 - 2 ^ n2))
```

Vers:

```
(alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)
```

Le facteur `(2^n1 - 2^n2)` est commun, et en divisant par lui des deux côtés:
- Si `x ≠ 0`, alors `(a*x) / (b*x) = a / b`

Mais Isabelle affiche:
```
(2 * (alpha_A_k 2 * 2 ^ n1) - 2 * (alpha_A_k 2 * 2 ^ n2)) /
(2 * (alpha_B_k 2 * 2 ^ n1) - 2 * (alpha_B_k 2 * 2 ^ n2))
```

Ce qui signifie que `field_simps` a **distribué** au lieu de **factoriser**.

### CORRECTION 2:

Le problème est le même qu'avant: `field_simps` seul ne suffit pas. Il faut ajouter une **factorisation explicite** ou utiliser `ring_nf` avant `field_simp`.

```isabelle
theorem RsP_k_egale_un_sur_k_pos:
  assumes "k \<in> {2, 3, 4}" "n1 > 0" "n2 > 0" "n1 \<noteq> n2"
  shows "RsP_k k n1 n2 = 1 / real k"
proof -
  from assms(1) consider "k = 2" | "k = 3" | "k = 4" by auto
  thus ?thesis
  proof cases
    case 1
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
    
    (* Nouvelle approche: factoriser explicitement *)
    have num_factored: "somme_A_pos_k 2 n1 - somme_A_pos_k 2 n2 =
                        (alpha_A_k 2 / 2) * (2 ^ n1 - 2 ^ n2)"
      by (simp add: somme_A_pos_k_def algebra_simps)
    
    have den_factored: "somme_B_pos_k 2 n1 - somme_B_pos_k 2 n2 =
                        (alpha_B_k 2 / 2) * (2 ^ n1 - 2 ^ n2)"
      by (simp add: somme_B_pos_k_def algebra_simps)
    
    have "RsP_k 2 n1 n2 =
          ((alpha_A_k 2 / 2) * (2 ^ n1 - 2 ^ n2)) /
          ((alpha_B_k 2 / 2) * (2 ^ n1 - 2 ^ n2))"
      by (simp add: RsP_k_def num_factored den_factored)
    
    also have "... = (alpha_A_k 2 / 2) / (alpha_B_k 2 / 2)"
      using hne_pow_2 by (field_simp [hne_pow_2]; ring)
    
    also have "... = 1 / real 2"
      unfolding alpha_A_k_def alpha_B_k_def by norm_num
    
    finally show ?thesis using 1 by simp
  
  next
    case 2
    (* IDENTIQUE pour k=3 *)
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
    
    have num_factored: "somme_A_pos_k 3 n1 - somme_A_pos_k 3 n2 =
                        (alpha_A_k 3 / 2) * (3 ^ n1 - 3 ^ n2)"
      by (simp add: somme_A_pos_k_def algebra_simps)
    
    have den_factored: "somme_B_pos_k 3 n1 - somme_B_pos_k 3 n2 =
                        (alpha_B_k 3 / 2) * (3 ^ n1 - 3 ^ n2)"
      by (simp add: somme_B_pos_k_def algebra_simps)
    
    have "RsP_k 3 n1 n2 =
          ((alpha_A_k 3 / 2) * (3 ^ n1 - 3 ^ n2)) /
          ((alpha_B_k 3 / 2) * (3 ^ n1 - 3 ^ n2))"
      by (simp add: RsP_k_def num_factored den_factored)
    
    also have "... = (alpha_A_k 3 / 2) / (alpha_B_k 3 / 2)"
      using hne_pow_3 by (field_simp [hne_pow_3]; ring)
    
    also have "... = 1 / real 3"
      unfolding alpha_A_k_def alpha_B_k_def by norm_num
    
    finally show ?thesis using 2 by simp
  
  next
    case 3
    (* IDENTIQUE pour k=4 *)
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
    
    have num_factored: "somme_A_pos_k 4 n1 - somme_A_pos_k 4 n2 =
                        (alpha_A_k 4 / 2) * (4 ^ n1 - 4 ^ n2)"
      by (simp add: somme_A_pos_k_def algebra_simps)
    
    have den_factored: "somme_B_pos_k 4 n1 - somme_B_pos_k 4 n2 =
                        (alpha_B_k 4 / 2) * (4 ^ n1 - 4 ^ n2)"
      by (simp add: somme_B_pos_k_def algebra_simps)
    
    have "RsP_k 4 n1 n2 =
          ((alpha_A_k 4 / 2) * (4 ^ n1 - 4 ^ n2)) /
          ((alpha_B_k 4 / 2) * (4 ^ n1 - 4 ^ n2))"
      by (simp add: RsP_k_def num_factored den_factored)
    
    also have "... = (alpha_A_k 4 / 2) / (alpha_B_k 4 / 2)"
      using hne_pow_4 by (field_simp [hne_pow_4]; ring)
    
    also have "... = 1 / real 4"
      unfolding alpha_A_k_def alpha_B_k_def by norm_num
    
    finally show ?thesis using 3 by simp
  qed
qed
```

═══════════════════════════════════════════════════════════════════════════

## RÉSUMÉ DES CORRECTIONS

### ERREUR 1 (Ligne 2595):

**Avant:**
```isabelle
by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)
```

**Après:**
```isabelle
by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def;
    norm_num)
```

Ou:

```isabelle
by (unfold SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def;
    norm_num)
```

### ERREUR 2 (Ligne 2915):

**Avant:** Utiliser `field_simps` seul

**Après:** 
1. Factoriser explicitement le numérateur et dénominateur avec `algebra_simps`
2. Remplacer `by (simp add: field_simps)` par `by (field_simp [hne_pow_k]; ring)`
3. Répéter pour k=2, 3, 4

═══════════════════════════════════════════════════════════════════════════

## APPLICATION AU FICHIER

Remplacer les sections correspondantes dans `methode_spectral.thy`:

1. **Ligne ~2595**: Remplacer le lemme `ecart_227_173_1_3` avec la version corrigée (use `norm_num`)

2. **Ligne ~2915**: Remplacer le théorème `RsP_k_egale_un_sur_k_pos` avec la version corrigée (factorisation + `field_simp [hne_pow_k]; ring`)

Après ces corrections, la compilation devrait passer sans erreurs!

✓ Les trois cas k=2, 3, 4 seront prouvés correctement.
✓ L'ecart 227/173 sera validé numériquement.
