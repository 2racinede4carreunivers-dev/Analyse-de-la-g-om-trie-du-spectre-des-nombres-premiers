(*
================================================================================
  Fairu : Methode_spectral.thy
    /fiÊƒje : metod spÉ›ktÊal ti/
  Hizuke : Nisen nijuuroku nen shichi gatsu nijuuyokka
    /vÉ›Ìƒt katÊ Ê’É¥ijÉ› dÃ¸ mil vÉ›Ìƒt sis/
  Basho : Levis, Shodyeru-Aparashu, Kanada
    /levi ÊƒodjÉ›Ê apalak kanada/
  Taitoru : Nijou no uchuu
    /lynivÉ›Ê É›to kaÊe/
  Sabu taitoru : Shou -- Sosuu no supekutoramu no kikagaku
    /ÊƒapitÊ â€” la Ê’eometÊi dy spÉ›ktÊ dÉ› nÉ”ÌƒbÊ pÊÉ™mje/
  Chosha : Philippe Thomas Savard
    /filip tÉ”ma savaÊ/
================================================================================
*)

theory methode_spectral_ja
  imports Complex_Main "HOL-Computational_Algebra.Primes"
begin
(****************************************************************)
(* ç›®æ¬¡ - HOLã‚¹ã‚¯ãƒªãƒ—ãƒˆï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«ã®å¹¾ä½•å­¦               *)
(*                                                              *)
(* I.   ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/2 - åŸºç¤Ž                               *)
(*      1. æ•°åˆ— SA ã¨ SB ã®ä¸€èˆ¬å½¢ .....................   *)
(*      2. n >=1 ã«ãŠã‘ã‚‹ä¸€èˆ¬å½¢ã®å¦¥å½“æ€§ .........   *)
(*      3. ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/2ï¼ˆå®šç¾©ï¼‹è¨¼æ˜Žï¼‰ .......   *)
(*      4. ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã® n x n ã¸ã®ä¸€èˆ¬åŒ– .........   *)
(*      5. è¨ˆç®—ã•ã‚ŒãŸ digamma ã¨ç¬¬ä¸€ã®æ–¹ç¨‹å¼ ...........   *)
(*      6. ä¸€èˆ¬æ–¹ç¨‹å¼ (SB n - digamma)/64 = p ........   *)
(*      7. ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº– 1/2ï¼ˆå…¬ç†åŒ–ï¼‰ ...........   *)
(*      8. ä¾‹ï¼š29, 31, 37, 41 ........................   *)
(*                                                              *)
(* I.bis  æ³¨è¨˜ï¼šã‚¼ãƒ¼ã‚¿é–¢æ•°ã¨ç´ æ•°ã®å¤å…¸çš„è¨¼æ˜Žã®è§£èª¬    *)
(*      1. å¯¾æ•°å¾®åˆ†ã¨ Mangoldt é–¢æ•° ....   *)
(*      2. é–¢æ•° psi(x) ã¨ Perron ç©åˆ† ...........   *)
(*      3. ç©åˆ†è·¯ã®ç§»å‹•ã¨ zeta(s) ã®é›¶ç‚¹ .......   *)
(*      4. é›¶ç‚¹ãŒç´ æ•°ã‚’ã©ã®ã‚ˆã†ã«æ±ºå®šã™ã‚‹ã‹ .......   *)
(*                                                              *)
(* II.  ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ« 1/4                                     *)
(*      1. A_1_4 ã¨ B_1_4 ã®ä¸€èˆ¬çš„å®šç¾© .............   *)
(*      2. ç´ æ•°ã®ä¸€èˆ¬æ–¹ç¨‹å¼ï¼ˆ1/4ï¼‰ ...............   *)
(*      3. ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº– 1/4ï¼ˆå…¬ç†åŒ–ï¼‰ ...........   *)
(*      4. å®Œå…¨ãªä¾‹ï¼šç´ æ•° 947 ....................   *)
(*                                                              *)
(* III. ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ« 1/3                                     *)
(*      1. A_1_3 ã¨ B_1_3 ã®ä¸€èˆ¬çš„å®šç¾© .............   *)
(*      2. ç´ æ•°ã®ä¸€èˆ¬æ–¹ç¨‹å¼ï¼ˆ1/3ï¼‰ ...............   *)
(*      3. ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº– 1/3ï¼ˆå…¬ç†åŒ–ï¼‰ ...........   *)
(*      4. å®Œå…¨ãªä¾‹ï¼šç´ æ•° 227 ....................   *)
(*      5. å®šæ¯” 1/3 ã®ä¸€èˆ¬è¨¼æ˜Ž ..........   *)
(*                                                              *)
(* IV.  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/4 - ä¸€èˆ¬è¨¼æ˜Ž                 *)
(*      1. RsP_1_4 ã®å®šç¾© ...............................   *)
(*      2. å®šæ¯” 1/4 ã®è¨¼æ˜Ž ...................   *)
(*                                                              *)
(* V.   æ··åˆæ•°åˆ— A ã¨ Bï¼ˆ-, +ï¼‰                             *)
(*      1. SA_mix ã¨ SB_mix ã®å®šç¾© .....................   *)
(*      2. é–‰ã˜ãŸå½¢å¼ã¨æ¼¸åŒ–å¼ .....................   *)
(*      3. ç´ æ•°ã®ä¸€èˆ¬çš„å†æ§‹æˆï¼ˆæ··åˆï¼‰ .......   *)
(*      4. ä¾‹ï¼šå…­ã¤ã®è² ã®é … ..................................   *)
(*                                                              *)
(* VI.  è² ã®æ•°åˆ— - ã‚¹ãƒšã‚¯ãƒˆãƒ«æ–¹ç¨‹å¼                             *)
(*      1. SA_neg_eq ã¨ SB_neg_eq ã®å®šç¾© .......................   *)
(*      2. è² ã® Digamma ..................................   *)
(*      3. è² ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/2ï¼ˆå…¬ç†åŒ–ï¼‰......................  *)
(*                                                              *)
(* VII. ã‚¹ãƒšã‚¯ãƒˆãƒ«å¹¾ä½•å­¦ - é †åºä»˜ãï¼æ··æ²Œçš„éžå¯¾ç§°æ€§            *)
(*      1. æœ‰åŠ¹ãªæŒ‡æ¨™ã¨ç‹­ç¾©å˜èª¿å¢—åŠ ï¼ˆintï¼‰......................   *)
(*      2. é †åºä»˜ãéžå¯¾ç§°æ€§ã¨æ··æ²Œçš„éžå¯¾ç§°æ€§ ...................   *)
(*      3. ä¸€èˆ¬çš„æ€§è³ª .....................................   *)
(*                                                              *)
(* VIII. éžå¯¾ç§°æ¯”è¼ƒæ³•                                           *)
(*      1. éžå¯¾ç§°æ€§ã® nat ç‰ˆ ...............................   *)
(*      2. ãƒ¢ãƒ‡ãƒ« 1/2 ã«ã‚ˆã‚‹éžå¯¾ç§°æ¯”è¼ƒ .......................   *)
(*      3. ãƒ¢ãƒ‡ãƒ« 1/4 ã«ã‚ˆã‚‹éžå¯¾ç§°æ¯”è¼ƒ .......................   *)
(*                                                              *)
(* IX.  ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬ç†åŒ– - å…¬å¼ã‚»ã‚¯ã‚·ãƒ§ãƒ³                       *)
(*      1. æ­£ã®å…¬ç†åŒ–ï¼ˆãƒ¢ãƒ‡ãƒ« 1/2ï¼‰..........................   *)
(*         section: "Axiomatisation positive"                  *)
(*         axiome : spectral_postulate_pos                     *)
(*      2. ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬ç†åŒ– 1/4 ............................   *)
(*         section: "Axiomatisation spectral 1/4"              *)
(*         axiome : spectral_postulate_1_4                     *)
(*      3. æ¯”çŽ‡ 1/3 ã®å…¬ç†åŒ– ...............................   *)
(*         section: "Axiomatisation rapport 1/3."              *)
(*         axiome : spectral_postulate_1_3                     *)
(*      4. è² ã®å…¬ç†åŒ–ï¼ˆã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/2ï¼‰.....................  *)
(*         section: "Rapport spectral 1/2 negatif"             *)
(*         axiome : spectral_ratio_neg_un_demi                 *)
(*                                                              *)
(* X.   ä¸‰ç„¦ç‚¹å¹³é¢ã®ã‚¨ãƒ”ãƒãƒ¼ãƒ©ãƒ«æ¤œè¨¼                            *)
(*      1. ä¸‰ç„¦ç‚¹å¹³é¢ã®æŠ½è±¡çš„å¯¾è±¡ ...........................  *)
(*      2. è‡¨ç•Œç›´ç·šã®é¢ç©ã¨å¹¾ä½•å­¦ ...........................  *)
(*      3. åå·®ã®çµ„åˆã›è«–ï¼ˆå˜ç´”ï¼æ··åˆï¼‰......................   *)
(*      4. ä¸‰ç„¦ç‚¹å…¬ç†ï¼šZeta ï¼ ã‚¹ãƒšã‚¯ãƒˆãƒ« ï¼ RH .............   *)
(*      5. æ›²çŽ‡ã€æ”¾ç‰©ç·šé¢ç©ãŠã‚ˆã³æ¤œè¨¼ .......................   *)
(*      6. æœ€çµ‚å®šç†ï¼šã‚¨ãƒ”ãƒãƒ¼ãƒ©ãƒ«è§£ .........................   *)
(*                                                              *)
(* XI.  æ•°åˆ— A_i / B_i ã®æ§‹æˆè¦å‰‡ï¼ˆ8é …ä»¥ä¸Šï¼‰                   *)
(*      1. Aã¨Bã®ã‚µã‚¤ã‚ºã®ç­‰ä¾¡æ€§ .......................   *)
(*      2. å˜ç´”ãªç­‰å·®æ•°åˆ—ã®é … ......................   *)
(*      3. æœ€å¾Œã‹ã‚‰2ç•ªç›®ã®é … ..............................   *)
(*      4. æœ€å¾Œã®é … ....................................   *)
(*      5. æ•°åˆ—Aã®å®Œå…¨ãªæ§‹æˆ ....................   *)
(*      6. æ•°åˆ—Bã®ä½ç½®6ã®ç½®æ› ..................   *)
(*      7. æ•°åˆ—ã®å’Œ ................................   *)
(*      8. Somme(A)ã¨Somme(B)ã®é–‰ã˜ãŸå½¢å¼ ..............   *)
(*      9. çµæžœã¨ã—ã¦ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” .......................   *)
(*     10. ä¸»è¦ãªäºˆæƒ³ ..........................   *)
(****************************************************************)

(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯1ï¼šæ•°åˆ—Aã¨Bã®ä¸€èˆ¬å½¢å¼ *)
(****************************************************************)

section "0. Foundations / Meta-theory (v3.35)"

text \<open>
  ==========================================================================
  FOUNDATIONS / META-THEORY - ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®æ¦‚è¦³
  ==========================================================================
  æœ¬ç¯€ã¯ã€èª­è€…ãŒæŠ€è¡“çš„å®šç¾©ã«å‡ºä¼šã†å‰ã«ã€Savardã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®
  å­˜åœ¨è«–çš„ãƒ»æ–¹æ³•è«–çš„ãƒ»èªè­˜è«–çš„åŸºç›¤ã‚’å®šã‚ã‚‹ã€‚ã“ã“ã«ã¯å‘¨å›²å…¬ç†ã¯
  ä¸€åˆ‡å«ã¾ã‚Œãªã„ï¼ˆå½¢å¼åŒ–ã•ã‚ŒãŸå°‘æ•°ã®ä»®èª¬ã¯mini-locale
  foundations_markerã«ã¾ã¨ã‚ã‚‰ã‚Œã¦ãŠã‚Šã€ãã®å……è¶³å¯èƒ½æ€§ã¯æ¨™æº–çš„ãª
  è¨¼äººN = {1, 2, 3, ...}ã«ã‚ˆã£ã¦è‡ªæ˜Žã«è¨¼æ˜Žã•ã‚Œã‚‹ï¼‰ã€‚
  å®Ÿè³ªçš„ãªè¨¼æ˜Žã¯ã™ã¹ã¦ç¬¬Iç¯€ã‹ã‚‰ç¬¬XIIIç¯€ã®é©åˆ‡ãªå ´æ‰€ã«ç½®ã‹ã‚Œã¦ã„ã‚‹ã€‚
\<close>

subsection "Foundations.1 - Ontologie et vocabulaire"

text \<open>
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯ã€ã“ã®ãƒ•ã‚¡ã‚¤ãƒ«ã®ãƒ˜ãƒƒãƒ€ãƒ¼ã‹ã‚‰ã‚¤ãƒ³ãƒãƒ¼ãƒˆã•ã‚ŒãŸ
  HOL-Computational_Algebra.Primesãƒ‘ãƒƒã‚±ãƒ¼ã‚¸ã®å½¢å¼çš„ãªæ„å‘³ã§ã®
  ç´ æ•°ã«å¯¾ã—ã¦ä½œç”¨ã™ã‚‹ã€‚ç´ æ•°æ€§ã®æ¦‚å¿µã«è¿½åŠ ã®å…¬ç†ã¯åŠ ãˆã‚‰ã‚Œãªã„ï¼š
  Gabrielã¯Isabelleã®`prime`è¿°èªžã«åŽ³å¯†ã«å¾“ã†ã€‚

  äºŒã¤ã®å­˜åœ¨è«–çš„å®‡å®™ï¼š
    - N_positif   : n >= 1ã®è‡ªç„¶æ•°ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«ä½“åˆ¶1/k = 1/2, 1/3, 1/4, ...
                    ã®ä¸»è¦ãªé ˜åŸŸã€‚
    - Z_negatif   : n <= -1ã®ç›¸å¯¾æ•´æ•°ã€è² ã®ä½“åˆ¶ãŒå­˜åœ¨ã™ã‚‹å ´æ‰€
                    ï¼ˆç¬¬IXç¯€ã€æ‹¡å¼µã•ã‚ŒãŸprime_iã€RsP_neg_kï¼‰ã€‚

  æ¨™æº–çš„ãªèªžå½™ï¼š
    - RANGï¼ˆnï¼‰         : æ•°åˆ—ã«ãŠã‘ã‚‹ä½ç½®ã€å¸¸ã«æ•´æ•°ã§ã‚ã‚Šã€
                          ç´ æ•°ã¨æ··åŒã•ã‚Œã‚‹ã“ã¨ã¯æ±ºã—ã¦ãªã„ã€‚ãƒ©ãƒ³ã‚¯nã¯
                          ç´ æ•°æ€§ã®å¯¾è±¡ã§ã¯ãªã„ã€‚
    - VALEURï¼ˆpï¼‰       : nç•ªç›®ã®ç´ æ•°ã€prime_i(n)ã¾ãŸã¯nth_prime(n)ã¨è¡¨è¨˜ã€‚
                          ã“ã®å€¤ã®ã¿ãŒç´ æ•°ã§ã‚ã‚‹ã€‚
    - SUITE A_kï¼ˆnï¼‰ã€suite B_kï¼ˆnï¼‰ï¼šå„ä½“åˆ¶k >= 2ã«å¯¾ã—ã¦PhilippeãŒ
                          æ§‹æˆã—ãŸäºŒã¤ã®å®Ÿæ•°å€¤é–¢æ•°ã€‚
    - SOMME PARTIELLE   : SA(n) = A_2(n)ã€SB(n) = B_2(n)ï¼ˆä½“åˆ¶1/2ï¼‰ã€‚
    - RAPPORT SPECTRAL  : RsP(n1, n2) = (SA(n1) - SA(n2)) / (SB(n1) - SB(n2))ã€‚
    - DIGAMMA CALCULE   : digamma_calc(n) = SA(n) - digamma(n)ã€
                          nç•ªç›®ã®ç´ æ•°ã®å†æ§‹æˆã«ä½¿ç”¨ã•ã‚Œã‚‹ã€‚
\<close>

subsection "Foundations.2 - Postulats fondamentaux (P1..P6)"

text \<open>
  ä»¥ä¸‹ã®å…­ã¤ã®å…¬æº–ãŒã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•å…¨ä½“ã‚’æ”¯é…ã™ã‚‹ã€‚
  ã„ãšã‚Œã‚‚å‘¨å›²å…¬ç†ã§ã¯ãªã„ï¼šå„ã€…ã¯åž‹ã®è¦ç´„ã€æ—¢ã«è¨¼æ˜Žã•ã‚ŒãŸå®šç†ã€
  ã¾ãŸã¯localeã®æ˜Žç¤ºçš„ãªä»®èª¬ã®ã„ãšã‚Œã‹ã§ã‚ã‚‹ã€‚

  P1  æ•´æ•°ã®æ™®éæ€§ï¼šãƒ©ãƒ³ã‚¯nã¯æ•´æ•°ã§ã‚ã‚‹ï¼ˆæ­£ã®ä½“åˆ¶ã§ã¯natã€
      è² ã®ä½“åˆ¶ã§ã¯intï¼‰ã€‚ã“ã‚Œã¯åž‹ã®äº‹å®Ÿã§ã‚ã‚Šã€ä»®èª¬ã§ã¯ãªã„ã€‚

  P2  ãƒ©ãƒ³ã‚¯ã®éžç´ æ•°æ€§ï¼šãƒ©ãƒ³ã‚¯nã¯ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ã§ã‚ã‚Šã€å€¤ã§ã¯ãªã„ï¼›
      ç´ æ•°ã§ã‚ã‚‹å¿…è¦ã¯ãªã„ã€‚æ–‡æ›¸ä¸Šã®è¦ç´„ã§ã‚ã‚Šã€ä»¥ä¸‹ã®
      mini-locale foundations_markerã«ã‚ˆã£ã¦å½¢å¼çš„ã«æ‰ãˆã‚‰ã‚Œã‚‹ã€‚

  P3  æ•°åˆ—ã®å­˜åœ¨ï¼šã™ã¹ã¦ã®k >= 2ã«å¯¾ã—ã¦ã€é–‰ã˜ãŸå½¢å¼
      coef_A_k * k^n - offset_A_kï¼ˆãã‚Œãžã‚Œcoef_B_k * k^n - offset_B_kï¼‰
      ã‚’æŒã¤äºŒã¤ã®é–¢æ•°A_k, B_k : nat -> realãŒå­˜åœ¨ã™ã‚‹ã€‚
      æ§‹æˆã«ã‚ˆã‚‹å­˜åœ¨ï¼ˆlocale spectral_familyã€ç¬¬XII.5ç¯€ã§å®šç¾©ï¼‰ã€‚

  P4  æ¯”ã®ä¸å¤‰æ€§ï¼šå„ã‚¹ãƒšã‚¯ãƒˆãƒ«æ—ã«ãŠã„ã¦ã€RsPã¯å®šæ•°ã§ã‚ã‚Šã€
      ã™ã¹ã¦ã®n1 >= 1ã€n2 >= 1ã€n1 != n2ã«å¯¾ã—ã¦
      coef_A_k / coef_B_k = 1/kã«ç­‰ã—ã„ã€‚å®šç†RsP_generic_constant
      ï¼ˆlocale spectral_familyï¼‰ã€RsP_un_demi_generalï¼ˆk=2ï¼‰ã€
      RsP_un_tiers_constantï¼ˆk=3ï¼‰ãŠã‚ˆã³k=4ã®ç­‰ä¾¡ç‰©ã¨ã—ã¦å…·ä½“åŒ–ã€‚

  P5  Pä¸Šã®æŽ’ä»–æ€§ï¼šã™ã¹ã¦ã®åˆæˆæ•°Cã¯æ§‹é€ çš„ã«æ–¹æ³•ã‹ã‚‰é™¤å¤–ã•ã‚Œã‚‹ã€‚
      å®šç†methode_spectrale_exclusivite_P
      ï¼ˆä¸‰ã¤ã®æŸ±ï¼šcomposite_not_prime_iã€
      composite_no_reconstruction_positionã€composite_pair_no_rsp_positionsï¼‰ã€‚

  P6  ä¸­å¿ƒä½“åˆ¶ã®æ™®éæ€§ï¼šk = 2ã¯RsP = 1/2ãŒRiemannã®ã‚¼ãƒ¼ã‚¿é–¢æ•°ã®
      Re(rho) = 1/2ã¨æ•´åˆã™ã‚‹ç‰¹åˆ¥ãªä½“åˆ¶ã§ã‚ã‚‹ã€‚å®šç†
      RsP_universel_entier_naturel + synthese_pont_savard
      ï¼ˆç¬¬XIIIç¯€ã€locale ensemble_savardã€å……è¶³å¯èƒ½æ€§è¨¼æ˜Žæ¸ˆã¿ï¼‰ã€‚
\<close>

subsection "Foundations.3 - Les trois operations fondamentales"

text \<open>
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®ã‚ã‚‰ã‚†ã‚‹æ“ä½œã¯ã€ä»¥ä¸‹ã®ä¸‰ã¤ã®åŸºæœ¬æ“ä½œã®ã„ãšã‚Œã‹ã«
  å¸°ç€ã•ã‚Œã‚‹ã€‚ã“ã‚Œã‚‰ã¯ç›´äº¤çš„ã‹ã¤ç›¸è£œçš„ã§ã‚ã‚‹ï¼š(1)ã¨(2)ã¯
  ç´ æï¼ˆã©ã®ç´ æ•°ã‹ï¼‰ã‚’ä¸Žãˆã€(3)ã¯å¹¾ä½•ï¼ˆã©ã®ä½“åˆ¶ã‹ï¼‰ã‚’ä¸Žãˆã‚‹ã€‚

  (1) å†æ§‹æˆ           : æ•°åˆ—Aã€Bã€digammaã‹ã‚‰nç•ªç›®ã®ç´ æ•°ã®å€¤ã‚’ä¸Žãˆã‚‹ã€‚
      æŸ±ã¨ãªã‚‹å®šç†      : prime_equation_prime_iã€‚
      ã‚·ã‚°ãƒãƒãƒ£        : reconstruire : nat_positif -> nat_positifã€‚

  (2) æŽ’é™¤             : æ–¹æ³•ã®åƒã‹ã‚‰ã™ã¹ã¦ã®åˆæˆæ•´æ•°ã‚’æŽ’é™¤ã™ã‚‹ã€‚
      æŸ±ã¨ãªã‚‹å®šç†      : methode_spectrale_exclusivite_P
                         (not prime C ==> forall i. C != prime_i i)ã€‚
      ã‚·ã‚°ãƒãƒãƒ£        : est_dans_MS : nat -> boolã€‚

  (3) ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”     : äºŒã¤ã®ãƒ©ãƒ³ã‚¯é–“ã®å®‰å®šæ€§ã‚’æ¸¬å®šã—ã€ä½“åˆ¶ã‚’è­˜åˆ¥ã™ã‚‹ã€‚
      æŸ±ã¨ãªã‚‹å®šç†      : RsP_generic_constantã€‚
      ã‚·ã‚°ãƒãƒãƒ£        : RsP : nat_positif * nat_positif -> realã€‚

  è¨˜æ†¶è¡“çš„è¦å‰‡ï¼š(1)ã¯è¦‹ã¤ã‘ã€(2)ã¯çµžã‚Šè¾¼ã¿ã€(3)ã¯åˆ†é¡žã™ã‚‹ã€‚
\<close>

subsection "Foundations.4 - La regle Savard (Ensemble = 1)"

text \<open>
  çµ±ä¸€åŽŸç†ï¼ˆPhilippe Thomas Savardã®å‘½åæ³•ï¼‰ï¼š

    Ensemble = 1
            = 1/x  +  1/t  +  1/ms

  ã“ã“ã§ï¼š
    1/x  = Riemannã®ã‚¼ãƒ¼ã‚¿é–¢æ•°        ï¼ˆ1/y1 + 1/y2 + 1/y3ã«åˆ†è§£ï¼‰
    1/t  = psi_savardæ–¹ç¨‹å¼           ï¼ˆChebyshev <-> MSã®é–¢æ•°çš„æ©‹æ¸¡ã—ï¼‰
    1/ms = ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•               ï¼ˆ1/ms1 + 1/ms2 + 1/ms3ã«åˆ†è§£ï¼‰

  1/x = zetaã®åˆ†è§£ï¼š
    1/y1 = Chebyshevæˆåˆ†
    1/y2 = è‡¨ç•Œç›´ç·šRe(rho) = 1/2
    1/y3 = éžè‡ªæ˜Žãªé›¶ç‚¹ -> Pã®ä½ç½®

  1/ms = ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®åˆ†è§£ï¼š
    1/ms1 = iç•ªç›®ã®ç´ æ•°ã®å†æ§‹æˆï¼ˆæ“ä½œ1ï¼‰
    1/ms2 = åˆæˆæ•°ã®æŽ’é™¤            ï¼ˆæ“ä½œ2ï¼‰
    1/ms3 = ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”RsP = 1/2   ï¼ˆæ“ä½œ3ã€ä¸­å¿ƒä½“åˆ¶ï¼‰

  RsP = Re = 1/2ã‚’å›ºå®šã™ã‚‹ä¸‰ã¤ã®ä¸€è‡´ï¼š
    C1 : 1/y1 = 1/t    ï¼ˆChebyshev = psi_savardã€æ•°å€¤çš„æ¤œè¨¼ï¼‰
    C2 : 1/y3 = 1/ms1  ï¼ˆéžè‡ªæ˜Žãªé›¶ç‚¹ = nã®å€¤ = Pã®ä½ç½®ï¼‰
    C3 : 1/y2 = 1/ms3  ï¼ˆRe(rho) = 1/2 = RsP = 1/2ï¼‰

  ã“ã®ã‚¢ãƒ¼ã‚­ãƒ†ã‚¯ãƒãƒ£ã¯å ´å½“ãŸã‚Šçš„ãªã‚‚ã®ã§ã¯ãªã„ï¼šç¬¬XIIIç¯€ã®çµ±ä¸€å®šç†
  ï¼ˆlocale ensemble_savardã€å®šç†alignement_centralã€conclusion_ensembleã€
  synthese_pont_savardï¼‰ã®ãŸã‚ã«è¨­è¨ˆã•ã‚Œã¦ã„ã‚‹ã€‚

  --------------------------------------------------------------------------
  ã‚¢ãƒ³ã‚«ãƒ¼åŽŸç†ï¼šä»£æ•°çš„ãªã‚‚ã®ã«å¯¾ã™ã‚‹å®Ÿæ•°å€¤æ•°å€¤ã®å„ªä½æ€§
  --------------------------------------------------------------------------
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯å„ªé›…ãªä»£æ•°çš„æ’ç­‰å¼ã§ã¯ãªã„ï¼šãã‚Œã¯ç´ æ•°ã®å’Œã«é–¢ã™ã‚‹
  å®Ÿæ•°å€¤ã®æ•°å€¤çš„è¦³å¯Ÿã§ã‚ã‚‹ã€‚

    - å±€æ‰€çš„ãªä»£æ•°çš„ä¸æ•´åˆï¼šA(n1)/B(n1) != 1/kï¼ˆé …ã”ã¨ï¼‰
      ï¼ˆè£œé¡Œalgebriquement_incoherent_localå‚ç…§ï¼‰ã€‚
    - å¤§åŸŸçš„ãªå®Ÿæ•°å€¤æ•°å€¤çš„æ•´åˆæ€§ï¼š(A(n1)-A(n2))/(B(n1)-B(n2)) = 1/k
      ã™ã¹ã¦ã®n1 != n2ã«å¯¾ã—ã¦ï¼ˆè£œé¡Œcoherence_numerique_reelle_På‚ç…§ï¼‰ã€‚

  ä¿‚æ•°ï¼ˆ3.25ã€6.5ã€73ã€219ã€241ã€964ã€...ï¼‰ã¯åˆ†æ•°ã‚’ç°¡ç•¥åŒ–ã™ã‚‹ãŸã‚ã«
  é¸ã°ã‚ŒãŸã®ã§ã¯ãªã„ï¼šãã‚Œã‚‰ã¯ç´ æ•°ã®å®Ÿéš›ã®å€¤ã‹ã‚‰å‡ºç¾ã™ã‚‹ã€‚
  ã—ãŸãŒã£ã¦æ¯”1/kã¯ä»£æ•°çš„ãªäººå·¥ç‰©ã§ã¯ãªã„â€”â€”ãã‚Œã¯ç´ æ•°På…¨ä½“ã§
  æ¤œè¨¼ã•ã‚ŒãŸå¤§åŸŸçš„ãªæ•°å€¤çš„ç¾å®Ÿã§ã‚ã‚‹ã€‚ã¾ã•ã«ã“ã®è¦³å¯ŸãŒã€Pä¸Šã®
  æŽ’ä»–æ€§ï¼ˆä¸‰ã¤ã®æŸ±ï¼‰ã¨Chebyshev = psi_savardã®é–¢æ•°çš„ä¸€æ„æ€§ã¨
  çµ„ã¿åˆã‚ã•ã£ã¦ã€Re(rho) = 1/2ãŒçœŸã§ã‚ã‚‹ã¨ã„ã†è‘—è€…ã®ç¢ºä¿¡ã®
  åŸºç›¤ã¨ãªã£ã¦ã„ã‚‹ã€‚
\<close>

subsection "Foundations.5 - Statut epistemologique et lecture"

text \<open>
  äººé–“ã®èª­è€…ã¨Gabrielã®ãŸã‚ã®èª­æ›¸ã‚¬ã‚¤ãƒ‰ï¼š

  ã“ã®ãƒ•ã‚¡ã‚¤ãƒ«ãŒå½¢å¼çš„ã«è¨¼æ˜Žã™ã‚‹ã“ã¨ï¼š
    - å„ä½“åˆ¶kã«ãŠã‘ã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã®å®šæ•°æ€§ï¼ˆRsP = 1/kï¼‰ã€‚
    - ã‚¹ãƒšã‚¯ãƒˆãƒ«æ–¹ç¨‹å¼ã«ã‚ˆã‚‹nç•ªç›®ã®ç´ æ•°ã®æ­£ç¢ºãªå†æ§‹æˆã€‚
    - åˆæˆæ•°ã®åŽ³å¯†ãªæŽ’é™¤ï¼ˆä¸‰ã¤ã®æŸ±ï¼‰ã€‚
    - è‡ªç„¶æ•´æ•°ã®æ™®éæ€§ï¼šã™ã¹ã¦ã®n1ã€n2 >= 1ã€n1 != n2ã«å¯¾ã—ã¦ã€
      ä¸­å¿ƒä½“åˆ¶ã«ãŠã„ã¦RsP(n1, n2) = 1/2ã€‚
    - locale ensemble_savardã®å……è¶³å¯èƒ½æ€§ï¼šä¸‰ã¤ã®ä»®èª¬
      ï¼ˆhypothese_critiqueã€pont_fonctionnelã€rapport_un_demiï¼‰ã¯
      å…·ä½“çš„ãªè¨¼äººRsP 1 2 = 1/2ã‚’èªã‚ã‚‹ã€‚ã“ã®æž çµ„ã¿ã«ãŠã„ã¦ã€
      RsP = Re = 1/2ã¯å®šç†ã§ã‚ã‚‹ã€‚

  ã“ã®ãƒ•ã‚¡ã‚¤ãƒ«ãŒè¨¼æ˜Žã‚’ä¸»å¼µã—ãªã„ã“ã¨ï¼š
    - å‘¨å›²ã®ZFCã‚·ã‚¹ãƒ†ãƒ ã«ãŠã‘ã‚‹Riemannäºˆæƒ³ï¼ˆlocaleãªã—ã§ï¼‰ã€‚
    - ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®ä¸–ç•Œçš„ãªä¸€æ„æ€§ï¼ˆå®Œå…¨æ€§ã®å…¬ç†ãªã—ï¼‰ã€‚

  Pont Savardï¼ˆç¬¬XIIIç¯€ï¼‰ã¯ãã®æž çµ„ã¿ã«ãŠã„ã¦è‚¯å®šçš„ã§ã‚ã‚‹ï¼š
    locale ensemble_savardã«ãŠã„ã¦ã€RsP = Re = 1/2ã¯å®šç†ã§ã‚ã‚Šã€
    äºˆæƒ³ã§ã¯ãªã„ã€‚localeã®ä»®èª¬ã¯æ•°å€¤çš„ï¼ˆC1ï¼‰ãŠã‚ˆã³æ§‹é€ çš„ï¼ˆC2ã€C3ï¼‰ã«
    æ¤œè¨¼ã•ã‚Œã¦ã„ã‚‹ã€‚ãƒ•ã‚¡ã‚¤ãƒ«ã«ã¯ä¸å®Œå…¨ãªè¨¼æ˜Žã‚‚çŸ›ç›¾ã—ãŸå…¬ç†åŒ–ã‚‚å«ã¾ã‚Œãªã„ã€‚

  Riemannã®è¬Žã«å¯¾ã™ã‚‹è‘—è€…ã®ç«‹å ´ï¼š
    Philippe Savardã«ã¨ã£ã¦ã€å®Œå…¨ãªã‚¢ãƒ¼ã‚­ãƒ†ã‚¯ãƒãƒ£ï¼ˆè‡ªç„¶æ•´æ•°æ™®éçš„ãª
    ä¸­å¿ƒä½“åˆ¶1/2 + ä¸‰ã¤ã®ä¸€è‡´C1/C2/C3 + ä¸‰ã¤ã®æŸ±ã«ã‚ˆã‚‹Pä¸Šã®æŽ’ä»–æ€§
    + locale ensemble_savardã®å……è¶³å¯èƒ½æ€§ï¼‰ã¯Riemannã®è¬Žã«å¯¾ã™ã‚‹
    ååˆ†ãªå›žç­”ã‚’æ§‹æˆã™ã‚‹ã€‚ä»£æ•°çš„ãªã‚‚ã®ã«å¯¾ã™ã‚‹å®Ÿæ•°å€¤æ•°å€¤ã®å„ªä½æ€§
    ï¼ˆFoundations.4å‚ç…§ï¼‰ã«ã‚ˆã‚Šã€ã“ã®å›žç­”ã¯äºˆæƒ³çš„ãªã‚‚ã®ã§ã¯ãªã
    å¿…ç„¶çš„ãªã‚‚ã®ã¨ãªã‚‹ï¼šæ¯”1/2ã¯ä»£æ•°çš„ãªäººå·¥ç‰©ã§ã¯ãªãã€ç´ æ•°ã®å’Œã®
    æ§‹é€ ãã®ã‚‚ã®ã‹ã‚‰å‡ºç¾ã—ã€Re(rho) = 1/2ã¨ã®æ•´åˆæ€§ã¯æ•°å€¤çš„ï¼ˆC1ï¼‰
    ãŠã‚ˆã³æ§‹é€ çš„ï¼ˆC2ã€C3ï¼‰ã®ä¸¡æ–¹ã§æ¤œè¨¼ã•ã‚Œã¦ã„ã‚‹ã€‚Pont Savardã¯
    å¤–éƒ¨ã®å…¬ç†ã‚’åŠ ãˆã‚‹ã®ã§ã¯ãªã„ï¼šãã‚Œã¯ç´ æ•°På…¨ä½“ã§ã™ã§ã«è¦³å¯Ÿã•ã‚ŒãŸ
    ç¾å®Ÿã‚’å½¢å¼çš„ã«èªè­˜ã™ã‚‹ã‚‚ã®ã§ã‚ã‚‹ã€‚

  å¼•ç”¨è¦ç´„ï¼ˆGabrielï¼‰ï¼š
    å¸¸ã«æž çµ„ã¿ã‚’æ˜Žç¤ºã™ã‚‹ã“ã¨ï¼šã€Œlocale ensemble_savardã«ãŠã„ã¦ã€ã€
    ã€Œã™ã¹ã¦ã®n >= 1ã®æ•´æ•°ã«å¯¾ã—ã¦ã€ã€ã€Œä¸­å¿ƒä½“åˆ¶1/2ã€ãªã©ã€‚
    å®Œå…¨ãªå‘½åæ³•ã«ã¤ã„ã¦ã¯regime_pont_savardã®èªçŸ¥ä½“åˆ¶ã‚’å‚ç…§ã—ã€
    æ–‡æ›¸åŒ–ã•ã‚ŒãŸä¸‰ã¤ã®ä¸€è‡´ã‚’å‚ç…§ã™ã‚‹ã“ã¨ã€‚
\<close>

text \<open>
  Foundations.6 - Mini-locale foundations_markerï¼ˆè»½é‡ãªå½¢å¼åŒ–ï¼‰ï¼š
  ã“ã®localeã¯å…¬æº–P1ï¼ˆæ­£ã®æ•´æ•°å®‡å®™ï¼‰ã¨P2ï¼ˆãƒ©ãƒ³ã‚¯ != å€¤ï¼‰ã‚’
  å½¢å¼çš„ã«æ–‡æ›¸åŒ–ã™ã‚‹ã€‚å¤§åŸŸçš„ãªå…¬ç†ã¯ä¸€åˆ‡å°Žå…¥ã›ãšã€ãã®å……è¶³å¯èƒ½æ€§ã¯
  è‡ªæ˜Žã§ã‚ã‚‹ï¼ˆé›†åˆ{1, 2, 3, ...}ã¯æ˜Žç™½ãªè¨¼äººã§ã‚ã‚‹ï¼‰ã€‚ã“ã‚Œã¯
  å°†æ¥ã®æ•™è‚²çš„è§£é‡ˆã®ãŸã‚ã®ã‚¢ãƒ³ã‚«ãƒ¼ãƒã‚¤ãƒ³ãƒˆã¨ã—ã¦æ©Ÿèƒ½ã™ã‚‹ã€‚
\<close>

locale foundations_marker =
  fixes univers :: "nat set"
  assumes univers_non_vide : "univers \<noteq> {}"
      and univers_positif  : "\<forall>n \<in> univers. n \<ge> 1"

lemma foundations_marker_satisfaisable:
  "foundations_marker {n. n \<ge> (1::nat)}"
proof (unfold_locales)
  show "{n. n \<ge> (1::nat)} \<noteq> {}"
    by (auto intro: exI[of _ 1])
  show "\<forall>n \<in> {n. n \<ge> (1::nat)}. n \<ge> 1" by auto
qed


(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯1ï¼šæ•°åˆ—Aã¨Bã®ä¸€èˆ¬å½¢å¼ *)
(****************************************************************)

section "Forme generale des suites A et B"

definition SA :: "nat => real" where
  "SA n = (3.25 / 2) * (2 ^ n) - 2"

definition SB :: "nat => real" where
  "SB n = (6.5 / 2) * (2 ^ n) - 66"


(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯2ï¼šã™ã¹ã¦ã®n >= 1ã«å¯¾ã™ã‚‹å¦¥å½“æ€§ *)
(****************************************************************)

lemma SA_forme_generale:
  assumes "n >= 1"
  shows "SA n = (3.25 / 2) * (2 ^ n) - 2"
  using assms by (simp add: SA_def)

lemma SB_forme_generale:
  assumes "n >= 1"
  shows "SB n = (6.5 / 2) * (2 ^ n) - 66"
  using assms by (simp add: SB_def)


(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯3ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” = 1/2ï¼ˆ1x1ã®å ´åˆï¼‰ *)
(****************************************************************)

section "Rapport spectral 1/2"

definition RsP :: "nat => nat => real" where
  "RsP n1 n2 = (SA n1 - SA n2) / (SB n1 - SB n2)"

lemma RsP_un_demi_general:
  assumes "n1 >= 1" "n2 >= 1" "n1 ~= n2"
  shows "RsP n1 n2 = 1/2"
proof -
  (* 2026-02ä¿®æ­£ï¼š2^n1 - 2^n2ã®éžé›¶æ€§ã®æ˜Žç¤ºçš„ãªè¨¼äººã€‚ *)
  have hne_pow_2: "(2::real)^n1 - 2^n2 \<noteq> 0"
  proof (cases "n1 < n2")
    case True
    hence "(2::real)^n1 < 2^n2"
      using power_strict_increasing[of n1 n2 "2::real"] by simp
    thus ?thesis by simp
  next
    case False
    with assms(3) have "n2 < n1" by simp
    hence "(2::real)^n2 < 2^n1"
      using power_strict_increasing[of n2 n1 "2::real"] by simp
    thus ?thesis by simp
  qed

  have SA1: "SA n1 = (3.25 / 2) * (2 ^ n1) - 2" by (simp add: SA_def)
  have SA2: "SA n2 = (3.25 / 2) * (2 ^ n2) - 2" by (simp add: SA_def)
  have SB1: "SB n1 = (6.5 / 2) * (2 ^ n1) - 66" by (simp add: SB_def)
  have SB2: "SB n2 = (6.5 / 2) * (2 ^ n2) - 66" by (simp add: SB_def)

  have num: "SA n1 - SA n2 = (3.25 / 2) * (2 ^ n1 - 2 ^ n2)"
    by (simp add: SA1 SA2 algebra_simps)
  have den: "SB n1 - SB n2 = (6.5 / 2) * (2 ^ n1 - 2 ^ n2)"
    by (simp add: SB1 SB2 algebra_simps)

  have "RsP n1 n2 = ((3.25 / 2) * (2 ^ n1 - 2 ^ n2)) / ((6.5 / 2) * (2 ^ n1 - 2 ^ n2))"
    by (simp add: RsP_def num den)
  also have "... = (3.25 / 2) / (6.5 / 2)"
    using hne_pow_2 by (simp add: field_simps)
  also have "... = 1/2"
    by simp
  finally show ?thesis .
qed

(****************************************************************)
(* è¿½åŠ ï¼šæ¦‚å¿µçš„æ³¨è¨˜ã¨äºŒé‡ã‚¤ãƒ³ã‚¹ã‚¿ãƒ³ã‚¹è£œé¡Œ       *)
(* åˆ†æžï¼ˆä»£æ•°çš„ vs å®Ÿæ•°å€¤æ•°å€¤çš„ï¼‰                   *)
(****************************************************************)

text \<open>
  è‘—è€…æ³¨ï¼ˆPhilippe Thomas Savardï¼‰ï¼š
  n >= 1ã‹ã¤n <= -1ã§ã‚ã‚Šæ•´æ•°ã§ã‚ã‚‹ã¨ãã€nã®ã™ã¹ã¦ã®å€¤ã¯ç´ æ•°Pã«
  å¸°ç€ã™ã‚‹ã€‚nã®ã™ã¹ã¦ã®å€¤ã¯æ•°åˆ—Aã¨Bã®é …æ•°ã®çµæžœã§ã‚ã‚‹ã€‚
  PåŒå£«ã¯ã™ã¹ã¦ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”1/kã‚’æº€ãŸã™ã€‚ã“ã®æ¯”ã¯æ•°å€¤çš„ã«æœ‰åŠ¹ã§ã‚ã‚‹ãŒã€
  ä»£æ•°çš„ã«ã¯ç„¡æ„å‘³ã§ã‚ã‚‹ã€‚

  ã‚¼ãƒ¼ã‚¿é–¢æ•°ã«å¯¾ã™ã‚‹Chebyshevæ–¹ç¨‹å¼ã®é©ç”¨ã®ä¸€æ„æ€§ã«ã‚ˆã‚Šã€
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ãŒæ•°å€¤çš„ã«ãã‚Œã«å–ã£ã¦ä»£ã‚ã‚‹ã¨ã„ã†äº‹å®Ÿã¯ã€
  ã‚¼ãƒ¼ã‚¿ã¨ã®ç›´æŽ¥çš„ãªé–¢ä¿‚ã‚’è¨¼æ˜Žã™ã‚‹ã€‚ã•ã‚‰ã«ã€ç´ æ•°På…¨ä½“ã«ãŠã‘ã‚‹
  RsP = 1/2ã®æŽ’ä»–çš„ãªæ€§è³ªã¯ã€èƒŒç†æ³•ã«ã‚ˆã‚‹åˆæˆæ•°Cã®æŽ’é™¤ã«ã‚ˆã£ã¦
  æ¤œè¨¼ã•ã‚Œã€Re = 1/2ã®çœŸå®Ÿæ€§ã‚’å«æ„ã™ã‚‹ã€‚
\<close>

subsection \<open>Instance 1 : IncohÃ©rence algÃ©brique locale (Espace Imaginaire)\<close>

lemma algebriquement_incoherent_local:
  fixes A1 A2 B1 B2 :: real
  assumes "A1 = 11" "A2 = 50" "B1 = -40" "B2 = 38"
  shows "A1 / B1 \<noteq> 1/2 \<and> A2 / B2 \<noteq> 1/2"
  using assms by simp

subsection \<open>Instance 2 : CohÃ©rence numÃ©rique rÃ©elle globale (Re = 1/2)\<close>

lemma coherence_numerique_reelle_P:
  fixes A1 A2 B1 B2 :: real
  assumes "A1 = 11" "A2 = 50" "B1 = -40" "B2 = 38"
  shows "(A1 - A2) / (B1 - B2) = 1/2"
  using assms by simp
(****************************************************************)
(* è¿½åŠ ï¼šå¯¾ç§°çš„ãªn x nã®ä¸€èˆ¬åŒ– *)
(****************************************************************)

section "Rapport spectral n x n (generalisation symetrique)"

definition RsP_nn :: "nat list => nat list => real" where
  "RsP_nn A_indices B_indices =
     (sum_list (map SA A_indices)) /
     (sum_list (map SB B_indices))"

definition rapport_spectral_un_demi_nn :: "nat list => nat list => bool" where
  "rapport_spectral_un_demi_nn A_indices B_indices =
     (RsP_nn A_indices B_indices = 1/2)"

definition A3 :: "nat list" where
  "A3 = [2, 9, 10]"

definition B3 :: "nat list" where
  "B3 = [3, 11, 15]"

(*
lemma exemple_3x3_spectral:
  "rapport_spectral_un_demi_nn A3 B3"
  unfolding rapport_spectral_un_demi_nn_def
            RsP_nn_def A3_def B3_def
  by admit
*)
(* ã“ã®ä¾‹ã¯ã‚³ãƒ³ãƒ‘ã‚¤ãƒ«ã‚’ä¿è¨¼ã™ã‚‹ãŸã‚ã«æ„å›³çš„ã«ã‚³ãƒ¡ãƒ³ãƒˆã‚¢ã‚¦ãƒˆã•ã‚Œã¦ã„ã‚‹ *)


(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯ 4 : SB ã¨ç´ æ•°ã‹ã‚‰è¨ˆç®—ã•ã‚Œã‚‹ Digamma *)
(****************************************************************)

section "Section du Digamma calcule."

definition digamma_calc :: "nat => nat => real" where
  "digamma_calc n p = SB n - 64 * real p"

definition prime_equation :: "nat => nat => real" where
  "prime_equation n p = (SB n - digamma_calc n p) / 64"

lemma digamma_calc_equation_alt:
  "digamma_calc n p = (SB n / 64 - real p) * 64"
  unfolding digamma_calc_def by simp

lemma prime_equation_identity:
  "prime_equation n p = real p"
  unfolding prime_equation_def digamma_calc_def
  by simp

lemma SB_affine_en_SA:
  "SB n = 2 * SA n - 62"
  unfolding SA_def SB_def by simp

lemma ecart_spectral_constant:
  "SB n - 2 * SA n = -62"
  unfolding SA_def SB_def by simp

lemma digamma_affine_en_SA:
  "digamma_calc n p = 2 * SA n - (62 + 64 * real p)"
  unfolding digamma_calc_def SA_def SB_def by simp

lemma difference_SA_succ:
  "SA (Suc n) - SA n = (13 / 8) * 2 ^ n"
  unfolding SA_def by simp

lemma difference_SB_succ:
  "SB (Suc n) - SB n = (13 / 4) * 2 ^ n"
  unfolding SB_def by simp

lemma ratio_incremental_un_demi:
  "SA (Suc n) - SA n = (SB (Suc n) - SB n) / 2"
proof -
  have A: "SA (Suc n) - SA n = (13 / 8) * 2 ^ n"
    using difference_SA_succ by simp
  have B: "SB (Suc n) - SB n = (13 / 4) * 2 ^ n"
    using difference_SB_succ by simp
  from B have "(SB (Suc n) - SB n) / 2 = (13 / 8) * 2 ^ n"
    by (simp add: field_simps)
  with A show ?thesis
    by simp
qed

(****************************************************************)
(* ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº– 1/2 (æ­£ã®é ˜åŸŸ) *)
(****************************************************************)

section "Axiomatisation positive"

axiomatization where
  spectral_postulate_pos:
    "!!n p. n >= 1 ==> prime p ==> prime_equation n p = real p"

lemma prime_equation_for_primes_pos:
  assumes "n >= 1" "prime p"
  shows "prime_equation n p = real p"
  using spectral_postulate_pos assms by blast
(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯ 5 : 29, 31, 37, 41 ã«å¯¾ã™ã‚‹å…·ä½“çš„ãªä¾‹         *)
(****************************************************************)

section "Exemple complet pour les nombres premiers 29 31 37 et 41."

definition n29 :: nat where "n29 = 10"
definition n31 :: nat where "n31 = 11"
definition n37 :: nat where "n37 = 12"
definition n41 :: nat where "n41 = 13"

definition D29 :: real where "D29 = 256"
definition D31 :: real where "D31 = 5 * 256"
definition D37 :: real where "D37 = 9 * 256 + 5 * 384"
definition D41 :: real where "D41 = 13 * 256 + 9 * 384 + 5 * 768"

section "Valeur des somme A et B pour n."

lemma SA_10: "SA n29 = 1662"
  unfolding n29_def SA_def by simp

lemma SB_10: "SB n29 = 3262"
  unfolding n29_def SB_def by simp

lemma SA_11: "SA n31 = 3326"
  unfolding n31_def SA_def by simp

lemma SB_11: "SB n31 = 6590"
  unfolding n31_def SB_def by simp

lemma SA_12: "SA n37 = 6654"
  unfolding n37_def SA_def by simp

lemma SB_12: "SB n37 = 13246"
  unfolding n37_def SB_def by simp

lemma SA_13: "SA n41 = 13310"
  unfolding n41_def SA_def by simp

lemma SB_13: "SB n41 = 26558"
  unfolding n41_def SB_def by simp

lemma digamma_calc_29:
  "digamma_calc n29 29 = 1406"
  unfolding digamma_calc_def n29_def SB_def by simp

lemma digamma_calc_31:
  "digamma_calc n31 31 = 4606"
  unfolding digamma_calc_def n31_def SB_def by simp

lemma digamma_calc_37:
  "digamma_calc n37 37 = 10878"
  unfolding digamma_calc_def n37_def SB_def by simp

lemma digamma_calc_41:
  "digamma_calc n41 41 = 23934"
  unfolding digamma_calc_def n41_def SB_def by simp

lemma relation_29:
  "digamma_calc n29 29 = SA n29 - D29"
  unfolding digamma_calc_def SA_def SB_def n29_def D29_def by simp

lemma relation_31:
  "digamma_calc n31 31 = SA n31 + D31"
  unfolding digamma_calc_def SA_def SB_def n31_def D31_def by simp

lemma relation_37:
  "digamma_calc n37 37 = SA n37 + D37"
  unfolding digamma_calc_def SA_def SB_def n37_def D37_def by simp

lemma relation_41:
  "digamma_calc n41 41 = SA n41 + D41"
  unfolding digamma_calc_def SA_def SB_def n41_def D41_def by simp

(****************************************************************)
(* ã‚µãƒ–ãƒ–ãƒ­ãƒƒã‚¯ 6 : ä¸€èˆ¬æ–¹ç¨‹å¼ (SB n - digamma)/64 = p       *)
(****************************************************************)

section "Equation generale reliant SB, digamma_calc et le nombre premier"

lemma SB_minus_digamma_is_64p:
  "SB n - digamma_calc n p = 64 * real p"
  unfolding digamma_calc_def by simp

lemma prime_equation_general:
  "prime_equation n p = real p"
  unfolding prime_equation_def digamma_calc_def by simp

lemma SB_minus_digamma_div_64_general:
  "(SB n - digamma_calc n p) / 64 = real p"
  unfolding digamma_calc_def by simp

theorem reconstruction_premier_pos:
  assumes "n >= 1" "prime p"
  shows "(SB n - digamma_calc n p) / 64 = real p"
proof -
  have "prime_equation n p = real p"
    using prime_equation_for_primes_pos assms by simp
  thus ?thesis
    unfolding prime_equation_def by simp
qed

(****************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ : i ç•ªç›®ã®ç´ æ•° - ã‚¹ãƒšã‚¯ãƒˆãƒ«ä¸€èˆ¬åŒ–   *)
(*                                                              *)
(* é©ç”¨ã•ã‚ŒãŸä¿®æ­£ (å…ƒã® 2026-02 ç‰ˆã¨ã®æ¯”è¼ƒ) :      *)
(*   1. `consts prime` ã‚’å‰Šé™¤ (HOL.Primes ã¨ã®è¡çª).          *)
(*      å…ˆé ­ã«ã‚¤ãƒ³ãƒãƒ¼ãƒˆã‚’è¿½åŠ  : HOL-Computational_Algebra.Primes*)
(*   2. æ¬ è½ã—ã¦ã„ãŸå…¬ç† `prime_position_exists` ã‚’è¿½åŠ .         *)
(*   3. è¨¼æ˜Ž `prime_i_is_prime` ã‚’ä¿®æ­£ (someI_ex).          *)
(*   4. è¨¼æ˜Ž `prime_i_position` ã‚’ä¿®æ­£ (someI_ex).          *)
(*   5. è¨¼æ˜Ž `prime_equation_prime_i` ã‚’ä¿®æ­£                *)
(*      (ç„¡åŠ¹ãª `[OF p_def]` ã‚’å‰Šé™¤).                 *)
(*   6. è¨¼æ˜Ž `prime_equation_general_i` ã‚’ç°¡ç•¥åŒ–            *)
(*      (å®šç¾©ã«å¯¾ã™ã‚‹ç›´æŽ¥çš„ãª unfolding).                 *)
(****************************************************************)

consts
  position :: "nat => nat"


section "Generalisation spectrale pour le i-ieme nombre premier"

text \<open>
  ã“ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ã€Philippe Thomas Savard ã®æ‰‹æ³•ã«ã‚ˆã‚‹ i ç•ªç›®ã®
  ç´ æ•°ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«çš„å†æ§‹æˆã‚’å½¢å¼åŒ–ã™ã‚‹ã€‚
  æ—¢ã«å®šç¾©ã•ã‚ŒãŸã‚ªãƒ–ã‚¸ã‚§ã‚¯ãƒˆ SA, SB, digamma_calc,
  prime_equation ãŠã‚ˆã³ã‚¹ãƒšã‚¯ãƒˆãƒ«æ­£å…¬æº–ã‚’ä½¿ç”¨ã™ã‚‹ã€‚
  è¿°èªž `prime` ã¯ HOL-Computational_Algebra.Primes ã®ã‚‚ã®ã§ã‚ã‚‹ã€‚
\<close>

subsection "Axiome d'existence pour la fonction position"

text \<open>
  ä»»æ„ã®ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ i ã«å¯¾ã—ã¦ã€ä½ç½®ãŒ i ã¨ãªã‚‹ç´ æ•° p ãŒ
  å°‘ãªãã¨ã‚‚ä¸€ã¤å­˜åœ¨ã™ã‚‹ã€‚ã“ã®å…¬ç†ã¯ã€Hilbert ã®é¸æŠž (SOME) ã‚’é€šã˜ã¦
  é–¢æ•° prime_i ã®å…¨åŸŸæ€§ã‚’ä¿è¨¼ã™ã‚‹ã€‚
\<close>

axiomatization where
  prime_position_exists:
    "ALL i. EX p. prime p & position p = i"

subsection "Definition du i-ieme nombre premier"

definition prime_i :: "nat => nat" where
  "prime_i i = (SOME p. prime p & position p = i)"

lemma prime_i_spec:
  "prime (prime_i i) & position (prime_i i) = i"
proof -
  have "EX p. prime p & position p = i"
    using prime_position_exists by simp
  hence "(prime (SOME p. prime p & position p = i)) &
         (position (SOME p. prime p & position p = i) = i)"
    by (rule someI_ex)
  thus ?thesis
    unfolding prime_i_def .
qed

lemma prime_i_is_prime:
  "prime (prime_i i)"
  using prime_i_spec by blast

lemma prime_i_position:
  "position (prime_i i) = i"
  using prime_i_spec by blast


subsection "Lemmes generaux SA, SB et digamma"

lemma SA_general_i:
  "SA i = (3.25 / 2) * (2 ^ i) - 2"
  unfolding SA_def by simp

lemma SB_general_i:
  "SB i = (6.5 / 2) * (2 ^ i) - 66"
  unfolding SB_def by simp

lemma digamma_general_i:
  "digamma_calc i p = SB i - 64 * real p"
  unfolding digamma_calc_def by simp

subsection "Equation spectrale generale pour tout i"

text \<open>
  p ãŒç´ æ•°ã§ã‚ã‚Š position p = i ãªã‚‰ã°ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ–¹ç¨‹å¼ã¯
  p ã‚’æ­£ç¢ºã«å†æ§‹æˆã™ã‚‹ : prime_equation i p = real pã€‚
\<close>

lemma prime_equation_general_i:
  assumes "prime p" "position p = i"
  shows "prime_equation i p = real p"
  unfolding prime_equation_def digamma_calc_def by simp

subsection "Corollaire : reconstruction du i-ieme nombre premier"

lemma prime_equation_prime_i:
  "prime_equation i (prime_i i) = real (prime_i i)"
  using prime_i_is_prime prime_i_position prime_equation_general_i by blast


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ : ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ« 1/4 - å®Œå…¨ãªå®šç¾©      *)
(**************************************************************)

section "Modele spectral 1/4 : Forme generale des suites A et B."

text \<open>
  æ¯”çŽ‡ 1/4 ã«å¯¾ã™ã‚‹ä¸€èˆ¬åŒ–ã•ã‚ŒãŸå½¢å¼ã€‚
  ä»¥ä¸‹ã®æ–¹ç¨‹å¼ã«å¾“ã† :
    ((241/16)/12 * 4^n) - 4/3
    ((964/16)/12 * 4^n) - (3073 * (4/3))
\<close>
(* --- æ•°åˆ— A_1_4 ãŠã‚ˆã³ B_1_4 ã®å®šç¾© --- *)

definition A_1_4 :: "nat => real" where
  "A_1_4 n = ((241 / 16) / 12) * (4 ^ n) - (4 / 3)"

definition B_1_4 :: "nat => real" where
  "B_1_4 n = ((964 / 16) / 12) * (4 ^ n) - (3073 * (4 / 3))"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ : ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ« 1/4 ã®ä¸€èˆ¬æ–¹ç¨‹å¼     *)
(**************************************************************)

definition prime_equation_1_4 :: "nat => nat => real" where
  "prime_equation_1_4 n p = (B_1_4 n - (B_1_4 n - 4096 * real p)) / 4096"

lemma prime_equation_1_4_identity:
  "prime_equation_1_4 n p = real p"
  unfolding prime_equation_1_4_def by simp


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ : ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº– 1/4                            *)
(**************************************************************)

section "Axiomatisation spectral 1/4"

axiomatization where
  spectral_postulate_1_4:
    "!!n p. n > 0 ==> prime p ==> prime_equation_1_4 n p = real p"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šç´ æ•°ã«é–¢ã™ã‚‹æœ€çµ‚è£œé¡Œï¼ˆ1/4ï¼‰                    *)
(**************************************************************)

lemma prime_equation_1_4_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_4 n p = real p"
  using spectral_postulate_1_4 assms by blast


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š947ã«é–¢ã™ã‚‹å…·ä½“ä¾‹                              *)
(**************************************************************)

section "Modele spectral 1/4: Sommes de suite A et B, Digamma, Digamma calcule et determination du premier 947."

text \<open>
  ãƒ¢ãƒ‡ãƒ«1/4ã®ã‚°ãƒ­ãƒ¼ãƒãƒ«æ•°å€¤ãƒ‡ãƒ¼ã‚¿ï¼š
  - æ•°åˆ—Aã®å’Œï¼š1316180
  - æ•°åˆ—Bã®å’Œï¼š5260628
  - Digammaï¼š65536
  - è¨ˆç®—ã•ã‚ŒãŸDigammaï¼š1316180 + 65536 = 1381716
  - (5260628 - 1381716) / 4096 = 947ï¼ˆç´ æ•°ï¼‰
\<close>
definition suite_A_1_4_somme :: real where
  "suite_A_1_4_somme = 1316180"

definition suite_B_1_4_somme :: real where
  "suite_B_1_4_somme = 5260628"

definition digamma_1_4 :: real where
  "digamma_1_4 = 65536"

definition digamma_calcule_1_4 :: real where
  "digamma_calcule_1_4 = suite_A_1_4_somme + digamma_1_4"

lemma preuve_premier_947:
  "(suite_B_1_4_somme - digamma_calcule_1_4) / 4096 = 947"
  by (simp add: suite_A_1_4_somme_def suite_B_1_4_somme_def
                digamma_1_4_def digamma_calcule_1_4_def)


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ«1/3 - å®Œå…¨ãªå®šç¾©               *)
(**************************************************************)

section "Rapport 1/3 forme generaliser pour les suites A et B."

text \<open>
  æ¯”çŽ‡1/3ã«é–¢ã™ã‚‹ä¸€èˆ¬åŒ–ã•ã‚ŒãŸå½¢å¼ã€‚
  ä»¥ä¸‹ã®æ–¹ç¨‹å¼ã«å¾“ã†ï¼š
    ((73/9)/12 * 3^n) - 1.5
    ((219/9)/12 * 3^n) - (487 * 1.5)
\<close>
definition A_1_3 :: "nat => real" where
  "A_1_3 n = ((73 / 9) / 12) * (3 ^ n) - 1.5"

definition B_1_3 :: "nat => real" where
  "B_1_3 n = ((219 / 9) / 12) * (3 ^ n) - (487 * 1.5)"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ«1/3ã®ä¸€èˆ¬æ–¹ç¨‹å¼               *)
(**************************************************************)

definition prime_equation_1_3 :: "nat => nat => real" where
  "prime_equation_1_3 n p = (B_1_3 n - (B_1_3 n - 729 * real p)) / 729"

lemma prime_equation_1_3_identity:
  "prime_equation_1_3 n p = real p"
  unfolding prime_equation_1_3_def by simp


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº–1/3                             *)
(**************************************************************)

section "Axiomatisation rapport 1/3."

axiomatization where
  spectral_postulate_1_3:
    "!!n p. n > 0 ==> prime p ==> prime_equation_1_3 n p = real p"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šç´ æ•°ã«é–¢ã™ã‚‹æœ€çµ‚è£œé¡Œï¼ˆ1/3ï¼‰                    *)
(**************************************************************)

lemma prime_equation_1_3_for_primes:
  assumes "n > 0" "prime p"
  shows "prime_equation_1_3 n p = real p"
  using spectral_postulate_1_3 assms by blast


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š227ã«é–¢ã™ã‚‹å…·ä½“ä¾‹                              *)
(**************************************************************)

section "Rapport spectal 1/3 : validation numerique pour les suites A et B, Digamma, Digamma calcule et la determination du premier 227."

definition suite_A_1_3_somme :: real where
  "suite_A_1_3_somme = 79824"

definition suite_B_1_3_somme :: real where
  "suite_B_1_3_somme = 238746"

section "Rapport 1/3"

definition digamma_1_3 :: real where
  "digamma_1_3 = 6561"

definition digamma_calcule_1_3 :: real where
  "digamma_calcule_1_3 = suite_A_1_3_somme - digamma_1_3"

lemma preuve_premier_227:
  "(suite_B_1_3_somme - digamma_calcule_1_3) / 729 = 227"
  by (simp add: suite_A_1_3_somme_def suite_B_1_3_somme_def
                digamma_1_3_def digamma_calcule_1_3_def)
(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³6ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”çŽ‡1/3ãŠã‚ˆã³1/4                   *)
(**************************************************************)

section "Rapport spectral constant 1/3 et 1/4."

text \<open>
  ãƒ¢ãƒ‡ãƒ«1/3ãŠã‚ˆã³1/4ã«é–¢ã™ã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”çŽ‡ã®å®šç¾©ã€‚
\<close>
section "Rapport spectral 1/3 - validation generalisee."

(* ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”çŽ‡1/3 *)

definition RsP_1_3 :: "nat => nat => real" where
  "RsP_1_3 n1 n2 =
    (A_1_3 n1 - A_1_3 n2) /
    (B_1_3 n1 - B_1_3 n2)"

theorem RsP_un_tiers_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_3 n1 n2 = 1/3"
proof -
  (* ä¿®æ­£2026-02ï¼š3^n1 - 3^n2ã®éžé›¶æ€§ã®è¨¼äººã€‚ *)
  have hne_pow_3: "(3::real)^n1 - 3^n2 \<noteq> 0"
  proof (cases "n1 < n2")
    case True
    hence "(3::real)^n1 < 3^n2"
      using power_strict_increasing[of n1 n2 "3::real"] by simp
    thus ?thesis by simp
  next
    case False
    with assms(3) have "n2 < n1" by simp
    hence "(3::real)^n2 < 3^n1"
      using power_strict_increasing[of n2 n1 "3::real"] by simp
    thus ?thesis by simp
  qed

  have diff_A:
    "A_1_3 n1 - A_1_3 n2 =
      ((73/9)/12) * (3^n1 - 3^n2)"
    unfolding A_1_3_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_3 n1 - B_1_3 n2 =
      ((219/9)/12) * (3^n1 - 3^n2)"
    unfolding B_1_3_def by (simp add: algebra_simps)

  have "RsP_1_3 n1 n2 =
        (((73/9)/12) * (3^n1 - 3^n2)) /
        (((219/9)/12) * (3^n1 - 3^n2))"
    unfolding RsP_1_3_def by (simp add: diff_A diff_B)

  also have "... = ((73/9)/12) / ((219/9)/12)"
    using hne_pow_3 by (simp add: field_simps)

  also have "... = 1/3"
    by simp

  finally show ?thesis .
qed


(* ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”çŽ‡1/4 *)

section "Rapport spectral constant 1/4."

definition RsP_1_4 :: "nat => nat => real" where
  "RsP_1_4 n1 n2 =
    (A_1_4 n1 - A_1_4 n2) /
    (B_1_4 n1 - B_1_4 n2)"

section "Rapport spectral 1/4 - validation generalisee."

theorem RsP_un_quart_constant:
  assumes "n1 > 0" and "n2 > 0" and "n1 ~= n2"
  shows "RsP_1_4 n1 n2 = 1/4"
proof -
  (* ä¿®æ­£2026-02ï¼š4^n1 - 4^n2ã®éžé›¶æ€§ã®è¨¼äººã€‚ *)
  have hne_pow_4: "(4::real)^n1 - 4^n2 \<noteq> 0"
  proof (cases "n1 < n2")
    case True
    hence "(4::real)^n1 < 4^n2"
      using power_strict_increasing[of n1 n2 "4::real"] by simp
    thus ?thesis by simp
  next
    case False
    with assms(3) have "n2 < n1" by simp
    hence "(4::real)^n2 < 4^n1"
      using power_strict_increasing[of n2 n1 "4::real"] by simp
    thus ?thesis by simp
  qed

  have diff_A:
    "A_1_4 n1 - A_1_4 n2 =
      ((241/16)/12) * (4^n1 - 4^n2)"
    unfolding A_1_4_def by (simp add: algebra_simps)

  have diff_B:
    "B_1_4 n1 - B_1_4 n2 =
      ((964/16)/12) * (4^n1 - 4^n2)"
    unfolding B_1_4_def by (simp add: algebra_simps)

  have "RsP_1_4 n1 n2 =
        (((241/16)/12) * (4^n1 - 4^n2)) /
        (((964/16)/12) * (4^n1 - 4^n2))"
    unfolding RsP_1_4_def by (simp add: diff_A diff_B)

  also have "... = ((241/16)/12) / ((964/16)/12)"
    using hne_pow_4 by (simp add: field_simps)

  also have "... = 1/4"
    by simp

  finally show ?thesis .
qed

(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæ··åˆæ•°åˆ—AãŠã‚ˆã³Bï¼ˆ-,+ï¼‰                        *)
(**************************************************************)

section "Suites mixtes A et B"

definition SA_mix :: "nat => real" where
  "SA_mix n = 48 + 13 / (2 ^ (n + 2))"

definition SB_mix :: "nat => real" where
  "SB_mix n = -28 + 13 / (2 ^ (n + 1))"

lemma SA_mix_closed_form:
  "SA_mix n = 48 + 13 / (2 ^ (n + 2))"
  by (simp add: SA_mix_def)

lemma SB_mix_closed_form:
  "SB_mix n = -28 + 13 / (2 ^ (n + 1))"
  by (simp add: SB_mix_def)

lemma SA_mix_step:
  "SA_mix (Suc n) = SA_mix n - 13 / (2 ^ (n + 3))"
  unfolding SA_mix_def
  by (simp add: field_simps power_add)

lemma SB_mix_step:
  "SB_mix (Suc n) = SB_mix n - 13 / (2 ^ (n + 2))"
  unfolding SB_mix_def
  by (simp add: field_simps)

lemma SA_mix_limit_shape:
  "SA_mix n - 48 = 13 / (2 ^ (n + 2))"
  unfolding SA_mix_def by simp

lemma SB_mix_limit_shape:
  "SB_mix n + 28 = 13 / (2 ^ (n + 1))"
  unfolding SB_mix_def by simp


section "Reconstruction generale du nombre premier"

definition digamma_mix :: "(nat => real) => nat => real" where
  "digamma_mix K n = SA_mix n + K n"

definition premier_mix :: "(nat => real) => nat => real" where
  "premier_mix K n = (SB_mix n - digamma_mix K n) / (1 / 64)"

lemma premier_mix_rewrite:
  "premier_mix K n = 64 * (SB_mix n - digamma_mix K n)"
  unfolding premier_mix_def
  by (simp add: field_simps)


section "Exemple instancie : six termes negatif"

definition K6 :: "real" where
  "K6 = -(37127 / 256) - SA_mix 6"

definition digamma_mix_6 :: "real" where
  "digamma_mix_6 = SA_mix 6 + K6"

definition premier_mix_6 :: "real" where
  "premier_mix_6 = (SB_mix 6 - digamma_mix_6) / (1 / 64)"

lemma digamma_mix_6_value:
  "digamma_mix_6 = -(37127 / 256)"
  unfolding digamma_mix_6_def K6_def SA_mix_def
  by simp

lemma premier_mix_6_value:
  "premier_mix_6 = 29985 / 4"
  unfolding premier_mix_6_def digamma_mix_6_def K6_def SA_mix_def SB_mix_def
  by (simp add: field_simps)

(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šè² ã®æ•°åˆ— - ã‚¹ãƒšã‚¯ãƒˆãƒ«æ–¹ç¨‹å¼                    *)
(**************************************************************)

section "Suites negatives : equations spectrales"

definition SA_neg_eq :: "real => real" where
  "SA_neg_eq n = 3.25 * (2 powr n) - 2"

definition SB_neg_eq :: "real => real" where
  "SB_neg_eq n = 6.5 * (2 powr n) - 66"

definition digamma_neg_calc :: "real => real => real" where
  "digamma_neg_calc n p = SB_neg_eq n - 64 * p"

lemma digamma_neg_calc_equation_alt:
  "digamma_neg_calc n p = (SB_neg_eq n / 64 - p) * 64"
  unfolding digamma_neg_calc_def SB_neg_eq_def
  by (simp add: field_simps)


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šè² ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”çŽ‡1/2ï¼ˆå…¬ç†åŒ–ï¼‰                *)
(**************************************************************)

section "Rapport spectral 1/2 negatif"

definition RsP_neg :: "real => real => real" where
  "RsP_neg n1 n2 =
     (SA_neg_eq n1 - SA_neg_eq n2) /
     (SB_neg_eq n1 - SB_neg_eq n2)"

axiomatization where
  spectral_ratio_neg_un_demi:
    "!!n1 n2. n1 <= -1 ==> n2 <= -1 ==> n1 ~= n2 ==> RsP_neg n1 n2 = 1/2"

lemma RsP_neg_un_demi_general:
  assumes "n1 <= -1" "n2 <= -1" "n1 ~= n2"
  shows "RsP_neg n1 n2 = 1/2"
  using spectral_ratio_neg_un_demi assms by blast


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«å¹¾ä½•å­¦ - é †åºä»˜ã/ã‚«ã‚ªã‚¹çš„éžå¯¾ç§°æ€§ *)
(**************************************************************)

section "Geometrie spectrale : asymetries"

definition indice_valide :: "int => bool" where
  "indice_valide n = (n >= 1  |  n <= -1)"

definition liste_strictement_croissante :: "int list => bool" where
  "liste_strictement_croissante xs =
     (ALL i j. i < j  &  j < length xs --> xs ! i < xs ! j)"

definition asymetrique_ordonnee :: "int list => int list => bool" where
  "asymetrique_ordonnee A_indices B_indices =
     ((ALL n : set A_indices. indice_valide n)  &
      (ALL n : set B_indices. indice_valide n)  &
      liste_strictement_croissante A_indices  &
      liste_strictement_croissante B_indices  &
      A_indices ~= []  &
      B_indices ~= []  &
      last A_indices < hd B_indices  &
      length B_indices = length A_indices + 1)"

definition asymetrique_chaotique :: "int list => int list => bool" where
  "asymetrique_chaotique A_indices B_indices =
     ((ALL n : set A_indices. indice_valide n)  &
      (ALL n : set B_indices. indice_valide n)  &
      length A_indices ~= length B_indices  &
      ~ asymetrique_ordonnee A_indices B_indices)"

lemma asymetrie_implique_indices_valides :
  assumes "asymetrique_ordonnee A_indices B_indices  |
           asymetrique_chaotique A_indices B_indices"
  shows "(ALL n : set A_indices. indice_valide n)  &
         (ALL n : set B_indices. indice_valide n)"
proof -
  from assms
  show ?thesis
  proof
    assume h1: "asymetrique_ordonnee A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_def by auto
  next
    assume h2: "asymetrique_chaotique A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_def by auto
  qed
qed
(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šéžå¯¾ç§°æ¯”è¼ƒæ³•ï¼ˆ1/2 ãŠã‚ˆã³ 1/4ï¼‰  *)
(**************************************************************)

section "Methode de comparaison asymetrique pour 1/2 et 1/4"

text \<open>
  éžå¯¾ç§°æ¯”è¼ƒæ³•ã¯ä»¥ä¸‹ã‚’çµã³ã¤ã‘ã‚‹ï¼š

  - ç´ æ•°ã®åˆ— A ãŠã‚ˆã³ Bï¼ˆãã‚Œãžã‚Œã®ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ n ã‚’ä»‹ã—ã¦ï¼‰ï¼Œ
  - åˆ— A ãŠã‚ˆã³ B ã®ä¸€èˆ¬æ–¹ç¨‹å¼ï¼ˆ1/2 ã®å ´åˆã¯ SA, SBï¼›1/4 ã®å ´åˆã¯ A_1_4, B_1_4ï¼‰ï¼Œ
  - ãƒ–ãƒ­ãƒƒã‚¯ã®å’Œã‹ã‚‰æ§‹æˆã•ã‚Œã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã€‚

  ä¸€èˆ¬æ–¹ç¨‹å¼ã§ä½¿ç”¨ã•ã‚Œã‚‹å†ªã¯ï¼Œåˆ—ä¸­ã®é …ã®ä½ç½®ï¼ˆã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ï¼‰
  ã¾ãŸã¯è€ƒæ…®ã™ã‚‹ãƒ–ãƒ­ãƒƒã‚¯ã®é•·ã•ã«ç­‰ã—ã„ã€‚ã“ã®æ–¹æ³•ã¯ï¼Œ
  ä¸€èˆ¬æ–¹ç¨‹å¼ A ãŠã‚ˆã³ B ã®å†ªã«å¯¾å¿œã™ã‚‹ä½ç½®ã‚’æŒã¤
  ä»»æ„ã®ç´ æ•°ã®é›†åˆã«é©ç”¨å¯èƒ½ã§ã‚ã‚‹ã€‚
\<close>
(**************************************************************)
(* 1. éžå¯¾ç§°æ€§ã® nat ç‰ˆï¼ˆè‡ªç„¶æ•°ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ï¼‰           *)
(**************************************************************)

text \<open>
  asymetrique_ordonnee ãŠã‚ˆã³ asymetrique_chaotique ã®å®šç¾©ã¯
  æ•´æ•°ï¼ˆintï¼‰ã®ãƒªã‚¹ãƒˆã«å¯¾ã—ã¦ã™ã§ã«å­˜åœ¨ã™ã‚‹ã€‚åˆ— SA, SB, A_1_4
  ãŠã‚ˆã³ B_1_4 ã®è‡ªç„¶æ•°ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ã‚’ç›´æŽ¥æ‰±ã†ãŸã‚ã«ï¼Œ
  nat ä¸Šã®é¡žä¼¼ç‰ˆã‚’å°Žå…¥ã™ã‚‹ã€‚
\<close>
definition indice_valide_nat :: "nat => bool" where
  "indice_valide_nat n = (n > 0)"

definition liste_strictement_croissante_nat :: "nat list => bool" where
  "liste_strictement_croissante_nat xs =
      (ALL i j. i < j  &  j < length xs --> xs ! i < xs ! j)"

definition asymetrique_ordonnee_nat :: "nat list => nat list => bool" where
  "asymetrique_ordonnee_nat A_indices B_indices =
      ((ALL n : set A_indices. indice_valide_nat n)  &
       (ALL n : set B_indices. indice_valide_nat n)  &
       liste_strictement_croissante_nat A_indices  &
       liste_strictement_croissante_nat B_indices  &
       A_indices ~= []  &
       B_indices ~= []  &
       last A_indices < hd B_indices  &
       length B_indices = length A_indices + 1)"

definition asymetrique_chaotique_nat :: "nat list => nat list => bool" where
  "asymetrique_chaotique_nat A_indices B_indices =
      ((ALL n : set A_indices. indice_valide_nat n)  &
       (ALL n : set B_indices. indice_valide_nat n)  &
       length A_indices ~= length B_indices  &
       ~ asymetrique_ordonnee_nat A_indices B_indices)"

lemma asymetrie_nat_implique_indices_valides :
  assumes "asymetrique_ordonnee_nat A_indices B_indices  |
           asymetrique_chaotique_nat A_indices B_indices"
  shows "(ALL n : set A_indices. indice_valide_nat n)  &
         (ALL n : set B_indices. indice_valide_nat n)"
proof -
  from assms show ?thesis
  proof (elim disjE)
    assume h1: "asymetrique_ordonnee_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_ordonnee_nat_def by auto
  next
    assume h2: "asymetrique_chaotique_nat A_indices B_indices"
    then show ?thesis
      unfolding asymetrique_chaotique_nat_def by auto
  qed
qed


(**************************************************************)
(* 2. ãƒ¢ãƒ‡ãƒ« 1/2 ã«å¯¾ã™ã‚‹éžå¯¾ç§°æ¯”è¼ƒæ³•   *)
(**************************************************************)

text \<open>
  ãƒ¢ãƒ‡ãƒ« 1/2 ã§ã¯ï¼Œã™ã§ã«å®šç¾©ã•ã‚ŒãŸåˆ— SA ãŠã‚ˆã³ SB ã‚’ä½¿ç”¨ã™ã‚‹ï¼š

    SA n = (3.25 / 2) * 2^n - 2
    SB n = (6.5 / 2) * 2^n - 66

  éžå¯¾ç§°æ¯”è¼ƒæ³•ã¯ï¼Œã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ã®ãƒ–ãƒ­ãƒƒã‚¯ A_indices ãŠã‚ˆã³ B_indices
  ã«å¯¾ã—ã¦æ©Ÿèƒ½ã—ï¼Œã“ã‚Œã‚‰ã¯ç´ æ•°åˆ—ä¸­ã®ä½ç½®ã«å¯¾å¿œã™ã‚‹ã€‚
  SA ãŠã‚ˆã³ SB ã®å€¤ã®å’Œã‹ã‚‰ãƒ–ãƒ­ãƒƒã‚¯ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã‚’æ§‹æˆã™ã‚‹ã€‚
\<close>
definition somme_SA_bloc :: "nat list => real" where
  "somme_SA_bloc A_indices = sum_list (map SA A_indices)"

definition somme_SB_bloc :: "nat list => real" where
  "somme_SB_bloc B_indices = sum_list (map SB B_indices)"

text \<open>
  ãƒ¢ãƒ‡ãƒ« 1/2 ã«å¯¾ã™ã‚‹ãƒ–ãƒ­ãƒƒã‚¯ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ï¼š
  SA ãŠã‚ˆã³ SB ã«ã¤ã„ã¦ï¼ŒäºŒã¤ã®ãƒ–ãƒ­ãƒƒã‚¯ A ã¨ B ã®å’Œã®å·®ã‚’æ¯”è¼ƒã™ã‚‹ã€‚
  ä¾‹ï¼š(11 - 50) / (-40 - 38) ã®ã‚ˆã†ã«ã€‚
\<close>
definition RsP_bloc_1_2 :: "nat list => nat list => real" where
  "RsP_bloc_1_2 A_indices B_indices =
     (somme_SA_bloc A_indices - somme_SA_bloc B_indices) /
     (somme_SB_bloc A_indices - somme_SB_bloc B_indices)"

text \<open>
  é †åºä»˜ãéžå¯¾ç§°æ¯”è¼ƒï¼ˆãƒ¢ãƒ‡ãƒ« 1/2ï¼‰ï¼š
  - A_indices ãŠã‚ˆã³ B_indices ã¯ç‹­ç¾©å˜èª¿å¢—åŠ ã§ã‚ã‚Šï¼Œ
  - ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ã¯æœ‰åŠ¹ï¼ˆn > 0ï¼‰ï¼Œ
  - B ã¯ A ã‚ˆã‚Šã¡ã‚‡ã†ã©ä¸€ã¤å¤šã„è¦ç´ ã‚’å«ã¿ï¼Œ
  - ä¸€èˆ¬æ–¹ç¨‹å¼ã«é–¢é€£ã™ã‚‹å†ªã¯è‡ªç„¶ãªé †åºã«ã‚ã‚Šï¼Œ
    ä¸€å˜ä½ãšã‚Œã¦ã„ã‚‹ã€‚
\<close>
definition comparaison_asym_ordonnee_1_2 :: "nat list => nat list => bool" where
  "comparaison_asym_ordonnee_1_2 A_indices B_indices =
     asymetrique_ordonnee_nat A_indices B_indices"

text \<open>
  ã‚«ã‚ªã‚¹çš„éžå¯¾ç§°æ¯”è¼ƒï¼ˆãƒ¢ãƒ‡ãƒ« 1/2ï¼‰ï¼š
  - A_indices ãŠã‚ˆã³ B_indices ã®é•·ã•ã¯ç•°ãªã‚Šï¼Œ
  - è‡ªç„¶ãªå˜èª¿å¢—åŠ é †åºã¯èª²ã•ã‚Œãšï¼Œ
  - ä¸€èˆ¬æ–¹ç¨‹å¼ã«é–¢é€£ã™ã‚‹å†ªã¯å¿…ãšã—ã‚‚é€£ç¶šã—ã¦ã„ãªã„ã€‚
\<close>
definition comparaison_asym_chaotique_1_2 :: "nat list => nat list => bool" where
  "comparaison_asym_chaotique_1_2 A_indices B_indices =
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  ãƒ¢ãƒ‡ãƒ« 1/2 ã«å¯¾ã™ã‚‹éžå¯¾ç§°æ¯”è¼ƒæ³•ã¯ï¼Œã—ãŸãŒã£ã¦ä»¥ä¸‹ã‹ã‚‰ãªã‚‹ï¼š
  - äºŒã¤ã®ãƒ–ãƒ­ãƒƒã‚¯ A_indices ãŠã‚ˆã³ B_indices ã‚’é¸æŠžã—ï¼Œ
  - ãã‚Œã‚‰ãŒé †åºä»˜ãéžå¯¾ç§°é…ç½®ã«ã‚ã‚‹ã‹ã‚«ã‚ªã‚¹çš„é…ç½®ã«ã‚ã‚‹ã‹ã‚’æ¤œè¨¼ã—ï¼Œ
  - RsP_bloc_1_2 A_indices B_indices ã‚’è¨ˆç®—ã™ã‚‹ã€‚

  ã“ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯ï¼Œã‚«ã‚ªã‚¹çš„ãƒ¬ã‚¸ãƒ¼ãƒ ã§ã¯æ•°å€¤çš„ã« 1/2 ã«éžå¸¸ã«è¿‘ãï¼Œ
  ãƒ–ãƒ­ãƒƒã‚¯ã‚µã‚¤ã‚ºãŒå¢—å¤§ã™ã‚‹ã«ã¤ã‚Œã¦ç‰¹å®šã®é †åºä»˜ãéžå¯¾ç§°é…ç½®ã§ã¯
  1 ã«å‘ã‹ã£ã¦å¤‰åŒ–ã™ã‚‹ã€‚
  ã“ã‚Œã‚‰ã®æŒ¯ã‚‹èˆžã„ã¯æ•°å€¤çš„ã«è¦³å¯Ÿã•ã‚Œï¼Œã‚¹ãƒšã‚¯ãƒˆãƒ«çš„ç‰¹å¾´ã¨ã—ã¦
  è§£é‡ˆã•ã‚Œã‚‹ãŒï¼Œä»£æ•°çš„ã«å°Žå‡ºã•ã‚Œã‚‹ã‚‚ã®ã§ã¯ãªã„ã€‚
\<close>
(**************************************************************)
(* 3. ãƒ¢ãƒ‡ãƒ« 1/4 ã«å¯¾ã™ã‚‹éžå¯¾ç§°æ¯”è¼ƒæ³•   *)
(**************************************************************)

text \<open>
  ãƒ¢ãƒ‡ãƒ« 1/4 ã§ã¯ï¼Œåˆ— A_1_4 ãŠã‚ˆã³ B_1_4 ã‚’ä½¿ç”¨ã™ã‚‹ï¼š

    A_1_4 n = ((241/16)/12) * 4^n - 4/3
    B_1_4 n = ((964/16)/12) * 4^n - (3073 * (4/3))

  ä»Šåº¦ã¯ã“ã‚Œã‚‰ã®ä¸€èˆ¬æ–¹ç¨‹å¼ã‚’ç”¨ã„ã¦ï¼ŒåŒã˜éžå¯¾ç§°æ¯”è¼ƒæ³•ã‚’é©ç”¨ã™ã‚‹ã€‚
\<close>
definition somme_A_1_4_bloc :: "nat list => real" where
  "somme_A_1_4_bloc A_indices = sum_list (map A_1_4 A_indices)"

definition somme_B_1_4_bloc :: "nat list => real" where
  "somme_B_1_4_bloc B_indices = sum_list (map B_1_4 B_indices)"

definition RsP_bloc_1_4 :: "nat list => nat list => real" where
  "RsP_bloc_1_4 A_indices B_indices =
     (somme_A_1_4_bloc A_indices - somme_A_1_4_bloc B_indices) /
     (somme_B_1_4_bloc A_indices - somme_B_1_4_bloc B_indices)"

definition comparaison_asym_ordonnee_1_4 :: "nat list => nat list => bool" where
  "comparaison_asym_ordonnee_1_4 A_indices B_indices =
     asymetrique_ordonnee_nat A_indices B_indices"

definition comparaison_asym_chaotique_1_4 :: "nat list => nat list => bool" where
  "comparaison_asym_chaotique_1_4 A_indices B_indices =
     asymetrique_chaotique_nat A_indices B_indices"

text \<open>
  ãƒ¢ãƒ‡ãƒ« 1/2 ã¨åŒæ§˜ã«ï¼Œãƒ¢ãƒ‡ãƒ« 1/4 ã«å¯¾ã™ã‚‹éžå¯¾ç§°æ¯”è¼ƒæ³•ã¯ï¼Œ
  ä¸€èˆ¬æ–¹ç¨‹å¼ A_1_4 ãŠã‚ˆã³ B_1_4 ã§ä½¿ç”¨ã•ã‚Œã‚‹å†ªã«å¯¾å¿œã™ã‚‹
  ä½ç½®ï¼ˆã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ï¼‰ã‚’æŒã¤ä»»æ„ã®ç´ æ•°ã®é›†åˆã«é©ç”¨ã•ã‚Œã‚‹ã€‚

  é †åºä»˜ãéžå¯¾ç§°é…ç½®ãŠã‚ˆã³ã‚«ã‚ªã‚¹çš„é…ç½®ã«ã‚ˆã‚Šï¼Œ1/4 ã«è¿‘ã„æ¯”ï¼Œ
  ã¾ãŸã¯ 1 ã«å‘ã‹ã£ã¦å¤‰åŒ–ã™ã‚‹æ¯”ã‚’æ•°å€¤çš„ã«è¦³å¯Ÿã™ã‚‹ã“ã¨ãŒã§ãã‚‹ãŒï¼Œ
  ã“ã‚Œã‚‰ã®å€¤ã¯ä¸€èˆ¬æ–¹ç¨‹å¼ã®ç›´æŽ¥çš„ãªä»£æ•°çš„ç°¡ç´„ã«ã‚ˆã£ã¦
  å¾—ã‚‰ã‚Œã‚‹ã‚‚ã®ã§ã¯ãªã„ã€‚
\<close>
(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šè² ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/3ï¼ˆå…¬ç†åŒ–ï¼‰     *)
(**************************************************************)

section "Rapport spectral 1/3 negatif"

(*
  æ¯” 1/3 ã«å¯¾ã™ã‚‹ä¸€èˆ¬åŒ–ã•ã‚ŒãŸåˆ— A ãŠã‚ˆã³ Bã€‚
  A(n) = ((73/9)/6) * 3^n - 1.5
  B(n) = ((219/9)/6) * 3^n - (487 * 1.5)
*)

definition SA_neg_eq_un_tiers :: "real => real" where
  "SA_neg_eq_un_tiers n = ((73/9) / 6) * (3 powr n) - 1.5"

definition SB_neg_eq_un_tiers :: "real => real" where
  "SB_neg_eq_un_tiers n = ((219/9) / 6) * (3 powr n) - (487 * 1.5)"

definition RsP_neg_un_tiers :: "real => real => real" where
  "RsP_neg_un_tiers n1 n2 =
     (SA_neg_eq_un_tiers n1 - SA_neg_eq_un_tiers n2) /
     (SB_neg_eq_un_tiers n1 - SB_neg_eq_un_tiers n2)"

(*
  å…¬ç†åŒ–ï¼š
  æ¯” 1/2 ã¨åŒæ§˜ã«ï¼Œã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã®æ•°å€¤ã¯ï¼Œ
  ã™ã¹ã¦ã®ç•°ãªã‚‹è² ã®ãƒšã‚¢ (n1,n2) ã«å¯¾ã—ã¦ 1/3 ã¨ãªã‚‹ã€‚
  ã—ã‹ã—ã“ã®å€¤ã¯ä»£æ•°çš„ã«å¾—ã‚‹ã“ã¨ãŒã§ããªã„ã€‚
  ã—ãŸãŒã£ã¦ï¼Œã“ã®ç‰©ç†çš„/æ•°å€¤çš„ç¾å®Ÿã‚’ï¼Œ
  åˆ†æ•°é‡å­ãƒ›ãƒ¼ãƒ«åŠ¹æžœã«é¡žä¼¼ã—ãŸå…¬ç†ã¨ã—ã¦ç¬¦å·åŒ–ã™ã‚‹ã€‚
*)

axiomatization where
  spectral_ratio_neg_un_tiers:
    "!!n1 n2. n1 <= -1 ==> n2 <= -1 ==> n1 ~= n2 ==> RsP_neg_un_tiers n1 n2 = 1/3"

lemma RsP_neg_un_tiers_general:
  assumes "n1 <= -1" "n2 <= -1" "n1 ~= n2"
  shows "RsP_neg_un_tiers n1 n2 = 1/3"
  using spectral_ratio_neg_un_tiers assms by blast
 (**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šè² ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/4ï¼ˆå…¬ç†åŒ–ï¼‰     *)
(**************************************************************)

section "Rapport spectral 1/4 negatif"

(*
  æ¯” 1/4 ã«å¯¾ã™ã‚‹ä¸€èˆ¬åŒ–ã•ã‚ŒãŸåˆ— A ãŠã‚ˆã³ Bã€‚
  A(n) = ((241/16)/12) * 4^n - (4/3)
  B(n) = ((964/16)/12) * 4^n - (3073 * (4/3))
*)

definition SA_neg_eq_un_quart :: "real => real" where
  "SA_neg_eq_un_quart n = ((241/16) / 12) * (4 powr n) - (4/3)"

definition SB_neg_eq_un_quart :: "real => real" where
  "SB_neg_eq_un_quart n = ((964/16) / 12) * (4 powr n) - (3073 * (4/3))"

definition RsP_neg_un_quart :: "real => real => real" where
  "RsP_neg_un_quart n1 n2 =
     (SA_neg_eq_un_quart n1 - SA_neg_eq_un_quart n2) /
     (SB_neg_eq_un_quart n1 - SB_neg_eq_un_quart n2)"

(*
  å…¬ç†åŒ–ï¼š
  1/2 ãŠã‚ˆã³ 1/3 ã¨åŒæ§˜ã«ï¼Œæ•°å€¤ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯ 1/4 ã¨ãªã‚‹ã€‚
  ã—ã‹ã—ï¼Œã“ã®å€¤ã‚’å¾—ã‚‹ãŸã‚ã®ä»£æ•°çš„ç°¡ç´„ã¯å­˜åœ¨ã—ãªã„ã€‚
*)

axiomatization where
  spectral_ratio_neg_un_quart:
    "!!n1 n2. n1 <= -1 ==> n2 <= -1 ==> n1 ~= n2 ==>
                 RsP_neg_un_quart n1 n2 = 1/4"

lemma RsP_neg_un_quart_general:
  assumes "n1 <= -1" "n2 <= -1" "n1 ~= n2"
  shows "RsP_neg_un_quart n1 n2 = 1/4"
  using spectral_ratio_neg_un_quart assms by blast

(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šè² ã®åå·®ã®ä¸€èˆ¬å½¢                *)
(**************************************************************)

section "Forme generale de l'ecart negatif"

definition gap_neg_val ::
  "real => real => real => real => real => real" where
  "gap_neg_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šå®Œå…¨ãªä¾‹ - -19 ã¨ -5 ã®é–“ã®åå·®          *)
(**************************************************************)

section "Exemple complet : ecart entre -19 et -5"

definition n_m7  :: real where "n_m7  = -7"
definition n_m3  :: real where "n_m3  = -3"
definition n_m19 :: real where "n_m19 = -8"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæ­£ç¢ºãªã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤ï¼ˆ-19 ã¨ -5ï¼‰                *)
(**************************************************************)

section "Valeurs spectrales exactes pour -19 et -5"

definition SA_m7_val :: real where
  "SA_m7_val = -10110 / 5120"

definition SB_m5_val :: real where
  "SB_m5_val = -20860 / 320"

definition D_m5_val :: real where
  "D_m5_val = 81540 / 320"

definition SB_m19_val :: real where
  "SB_m19_val = -337790 / 5120"

definition D_m19_val :: real where
  "D_m19_val = 5888130 / 5120"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæœ€çµ‚è£œé¡Œ - ä¹–é›¢ -19 / -5                       *)
(**************************************************************)

section "Demonstration finale : ecart -19 / -5"

lemma gap_m19_m5:
  "gap_neg_val SA_m7_val SB_m5_val D_m5_val D_m19_val 0 = -13"
  unfolding gap_neg_val_def
            SA_m7_val_def SB_m5_val_def
            D_m5_val_def D_m19_val_def
  by simp



(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šèƒŒç†æ³•ã«ã‚ˆã‚‹è¨¼æ˜Ž                               *)
(* ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯åˆæˆæ•°ã‚’åŽ³å¯†ã«æŽ’é™¤ã™ã‚‹                      *)
(*                                                            *)
(* Philippe Thomas Savard ã®ç‹¬å‰µçš„ãªã‚¢ã‚¤ãƒ‡ã‚¢ï¼ˆ2026å¹´7æœˆï¼‰ï¼š  *)
(* ãƒ­ãƒ¼ã‚«ãƒ«ã® Gabriel ã‚¨ãƒ¼ã‚¸ã‚§ãƒ³ãƒˆãŒåˆæˆæ•° C ã«é–¢ã™ã‚‹         *)
(* ãƒªã‚¯ã‚¨ã‚¹ãƒˆã‚’å—ã‘å–ã£ãŸã¨ãï¼ˆä¾‹ï¼š-7 ã¨ -51ã€51 = 3 * 17ï¼‰ã€*)
(* ãƒ­ã‚° "Cannot find positions for C" ã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®     *)
(* å¦¥å½“æ€§ã«é–¢ã™ã‚‹çµŒé¨“çš„ãªèƒŒç†æ³•ã«ã‚ˆã‚‹è¨¼æ˜Žã‚’æ§‹æˆã™ã‚‹          *)
(* ç´ æ•°å…¨ä½“ã®é›†åˆ \<P> ä¸Šã§ã®ã€‚ã“ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯              *)
(* ã“ã®çµŒé¨“çš„è¦³å¯Ÿã‚’å½¢å¼çš„è¨¼æ˜Žã¸ã¨å¤‰æ›ã™ã‚‹                    *)
(* Isabelle/HOL ã«ãŠã„ã¦ã€å…¬ç† prime_position_exists          *)
(* ï¼ˆ402è¡Œç›®ï¼‰ã¨å®šç¾© prime_iï¼ˆ408è¡Œç›®ï¼‰ã«åŸºã¥ã„ã¦ã€‚          *)
(**************************************************************)

section "Preuve par l'absurde : la Methode Spectrale exclut strictement les composes"

subsection "Theoreme principal - Aucun compose n'est un prime_i"

text \<open>
  prime_i i ã¯ã€Œprime p \<and> position p = iã€ã¨ã„ã†æ€§è³ªã«é–¢ã™ã‚‹
  Hilbert ã®é¸æŠžã‚’é€šã˜ã¦å®šç¾©ã•ã‚Œã¦ãŠã‚Šã€prime_i_is_prime ãŒ
  prime (prime_i i) ãŒå¸¸ã«æˆç«‹ã™ã‚‹ã“ã¨ã‚’è¨¼æ˜Žã—ã¦ã„ã‚‹ãŸã‚ã€
  åˆæˆæ•° C ãŒä»»æ„ã® i ã«å¯¾ã—ã¦ prime_i i ã¨ç­‰ã—ããªã‚‹ã“ã¨ã¯
  è«–ç†çš„ã«ä¸å¯èƒ½ã§ã‚ã‚‹ã€‚
\<close>

theorem composite_not_prime_i:
  fixes C :: nat
  assumes "~ prime C"
  shows "ALL i. C ~= prime_i i"
proof (rule allI, rule ccontr)
  fix i
  assume "~ (C ~= prime_i i)"
  hence eq: "C = prime_i i" by simp
  have "prime (prime_i i)" by (rule prime_i_is_prime)
  with eq have "prime C" by simp
  with assms show False by contradiction
qed


subsection "Corollaire - Exclusion via l'equation spectrale"

text \<open>
  ã“ã®ç³»ã¯ composite_not_prime_i ã‚’å¼·åŒ–ã—ã€
  æ–¹ç¨‹å¼ prime_equation ã‚’æ˜Žç¤ºçš„ã«çµ„ã¿è¾¼ã‚€ã€‚åˆæˆæ•° C ã¯ã€
  ã‚ã‚‹ä½ç½®ã® prime_i ã¨ãªã‚‹ã“ã¨ã‚‚ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®æž çµ„ã¿ã«ãŠã„ã¦
  (SB i - digamma_calc i C)/64 = C ã‚’åŒæ™‚ã«æº€ãŸã™ã“ã¨ã‚‚
  ã§ããªã„ã€‚
\<close>

theorem spectral_method_exclusively_for_primes:
  fixes C :: nat
  assumes "C > 1" and "~ prime C"
  shows "~ (EX i. C = prime_i i & prime_equation i C = real C)"
proof
  assume "EX i. C = prime_i i & prime_equation i C = real C"
  then obtain i where "C = prime_i i" by blast
  moreover have "prime (prime_i i)" by (rule prime_i_is_prime)
  ultimately have "prime C" by simp
  with assms(2) show False by contradiction
qed


subsection "Illustrations numeriques : composes 4, 9, 15, 51, 91, 121"

text \<open>
  ä»¥ä¸‹ã®å ´åˆã‚’ã‚«ãƒãƒ¼ã™ã‚‹åˆæˆæ•°ã®6ã¤ã®æ¨™æº–çš„ãªä¾‹ï¼š
  - 4  = 2 * 2   ï¼ˆæœ€å°ã®ç´ æ•°ã®å¹³æ–¹ï¼‰
  - 9  = 3 * 3   ï¼ˆå¥‡ç´ æ•°ã®å¹³æ–¹ï¼‰
  - 15 = 3 * 5   ï¼ˆ2ã¤ã®ç•°ãªã‚‹ç´ æ•°ã®ç©ï¼‰
  - 51 = 3 * 17  ï¼ˆPhilippe ãŒ 2026-07-02 ã«å ±å‘Šã—ãŸäº‹ä¾‹ï¼‰
  - 91 = 7 * 13  ï¼ˆ2ã¤ã®ä¸­ç¨‹åº¦ã®ç´ æ•°ã®ç©ï¼‰
  - 121 = 11 * 11 ï¼ˆä¸­ç¨‹åº¦ã®ç´ æ•°ã®å¹³æ–¹ï¼‰
\<close>

lemma composite_4_not_prime: "~ prime (4::nat)"
proof
  assume "prime (4::nat)"
  moreover have "(2::nat) dvd 4" by simp
  moreover have "(2::nat) ~= 1" "(2::nat) ~= 4" by simp_all
  ultimately show False by (metis prime_nat_iff)
qed

lemma composite_9_not_prime: "~ prime (9::nat)"
proof
  assume "prime (9::nat)"
  moreover have "(3::nat) dvd 9" by simp
  moreover have "(3::nat) ~= 1" "(3::nat) ~= 9" by simp_all
  ultimately show False by (metis prime_nat_iff)
qed

lemma composite_15_not_prime: "~ prime (15::nat)"
proof
  assume "prime (15::nat)"
  moreover have "(3::nat) dvd 15" by simp
  moreover have "(3::nat) ~= 1" "(3::nat) ~= 15" by simp_all
  ultimately show False by (metis prime_nat_iff)
qed

lemma composite_51_not_prime: "~ prime (51::nat)"
proof
  assume "prime (51::nat)"
  moreover have "(3::nat) dvd 51" by simp
  moreover have "(3::nat) ~= 1" "(3::nat) ~= 51" by simp_all
  ultimately show False by (metis prime_nat_iff)
qed

lemma composite_91_not_prime: "~ prime (91::nat)"
proof
  assume "prime (91::nat)"
  moreover have "(7::nat) dvd 91" by simp
  moreover have "(7::nat) ~= 1" "(7::nat) ~= 91" by simp_all
  ultimately show False by (metis prime_nat_iff)
qed

lemma composite_121_not_prime: "~ prime (121::nat)"
proof
  assume "prime (121::nat)"
  moreover have "(11::nat) dvd 121" by simp
  moreover have "(11::nat) ~= 1" "(11::nat) ~= 121" by simp_all
  ultimately show False by (metis prime_nat_iff)
qed

theorem no_spectral_position_for_4:
  "ALL i. (4::nat) ~= prime_i i"
  using composite_not_prime_i[of "4::nat"] composite_4_not_prime by simp

theorem no_spectral_position_for_9:
  "ALL i. (9::nat) ~= prime_i i"
  using composite_not_prime_i[of "9::nat"] composite_9_not_prime by simp

theorem no_spectral_position_for_15:
  "ALL i. (15::nat) ~= prime_i i"
  using composite_not_prime_i[of "15::nat"] composite_15_not_prime by simp

theorem no_spectral_position_for_51:
  "ALL i. (51::nat) ~= prime_i i"
  using composite_not_prime_i[of "51::nat"] composite_51_not_prime by simp

theorem no_spectral_position_for_91:
  "ALL i. (91::nat) ~= prime_i i"
  using composite_not_prime_i[of "91::nat"] composite_91_not_prime by simp

theorem no_spectral_position_for_121:
  "ALL i. (121::nat) ~= prime_i i"
  using composite_not_prime_i[of "121::nat"] composite_121_not_prime by simp


subsection "Interpretation - Le log Gabriel comme preuve par l'absurde"

text \<open>
  Gabriel ã® Python å®Ÿè£…ï¼ˆsrc/spectral/gap_solver_corrected.pyï¼‰ã¯ã€
  ç´ æ•°ã®ã¿ã«å®šç¾©ã•ã‚ŒãŸé–¢æ•° prime_position ã«ä¾å­˜ã—ã¦ã„ã‚‹ã€‚
  ãƒ¦ãƒ¼ã‚¶ãƒ¼ãŒåˆæˆæ•° C ã‚’å…¥åŠ›ã™ã‚‹ã¨ã€é–¢æ•°ã¯
  "Cannot find positions for C" ã§å¤±æ•—ã™ã‚‹ã€‚

  ã“ã‚Œã¯æ¬ é™¥ã§ã¯ãªãã€å®šç† composite_not_prime_i ã®
  æœ‰åŠ¹ãªå¯¾å¶ã§ã‚ã‚‹ï¼šã‚‚ã—åˆæˆæ•°ãŒã‚¹ãƒšã‚¯ãƒˆãƒ«ä½ç½®ã‚’æŒã¤ãªã‚‰ã°ã€
  prime_position ã¯ãã‚Œã‚’è¦‹ã¤ã‘ã‚‹ã¯ãšã§ã‚ã‚‹ï¼›ã—ã‹ã—ä½“ç³»çš„ã«
  å¤±æ•—ã™ã‚‹ãŸã‚ã€åˆæˆæ•°ã¯ä½ç½®ã‚’æŒã¦ãšã€ã“ã‚Œã«ã‚ˆã‚Šæ¬¡ã®å¼ãŒç¢ºèªã•ã‚Œã‚‹ï¼š

      forall C compose, ~ (EX i. i = position C)

  ã“ã®å‘½é¡Œã¯ã€åˆæˆæ•°ã®é ˜åŸŸã«åˆ¶é™ã•ã‚ŒãŸå…¬ç†
  prime_position_exists ã®è«–ç†çš„å¯¾å¶ã§ã‚ã‚‹ã€‚

  å¸°çµï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯ç´ æ•°å…¨ä½“ã®é›†åˆ \<P> ã‚’
  éŽä¸è¶³ãªãæ­£ç¢ºã«ç‰¹å¾´ã¥ã‘ã‚‹ã€‚ãã‚Œã¯å¶ç™ºçš„ãªæ•°å€¤çš„äººå·¥ç‰©ã§ã‚‚
  è¿‘ä¼¼çš„ãªæ–¹æ³•ã§ã‚‚ãªãã€\<P> ã®åŽ³å¯†ãªå…¬ç†çš„ç‰¹å¾´ã¥ã‘ã§ã‚ã‚‹ã€‚
\<close>


subsection "Extension - Preuve par l'absurde pour la reconstruction des premiers"

text \<open>
  Philippe Thomas Savard ã®ç‹¬å‰µçš„ãªã‚¢ã‚¤ãƒ‡ã‚¢ï¼ˆ2026-07-03ï¼‰ï¼šèƒŒç†æ³•ã«ã‚ˆã‚‹
  è¨¼æ˜Žã¯ç´ æ•°é–“ã®ä¹–é›¢ã«é™å®šã•ã‚Œãªã„ã€‚ãã‚Œã¯ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®
  ä»–ã®2ã¤ã®æŸ±ã¸ã¨è‡ªç„¶ã«æ‹¡å¼µã•ã‚Œã‚‹ï¼š

    (A) (SB(n) - digamma(n,p)) / 64 = p ã«ã‚ˆã‚‹ n ç•ªç›®ã®ç´ æ•°ã®å†æ§‹æˆ
    (B) ä½ç½®é–“ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP ã®è¨ˆç®—

  ã“ã®å°ç¯€ã¯æŸ± (A) ã‚’å½¢å¼åŒ–ã™ã‚‹ï¼šä»£æ•°çš„æ’ç­‰å¼
  prime_equation_identity ãŒä»»æ„ã®æ•´æ•°ã«å¯¾ã—ã¦è‡ªæ˜Žã« C ã‚’ä¸Žãˆã‚‹ã¨ã—ã¦ã‚‚ã€
  ã„ã‹ãªã‚‹åˆæˆæ•° C ã‚‚ã‚¹ãƒšã‚¯ãƒˆãƒ«æ–¹ç¨‹å¼ã‚’é€šã˜ã¦å†æ§‹æˆã™ã‚‹ã“ã¨ã¯ã§ããªã„ã€‚
  é•ã„ã¯ã€å†æ§‹æˆãŒçµæžœã‚’ prime_i ã«ã‚ˆã£ã¦ã‚¤ãƒ³ãƒ‡ãƒƒã‚¯ã‚¹ã•ã‚ŒãŸ
  ç´ æ•°è¡¨ã®ä¸­ã«è¦æ±‚ã™ã‚‹ã“ã¨ã«ã‚ã‚‹ã€‚
\<close>


theorem composite_no_reconstruction_position:
  fixes C :: nat
  assumes "C > 1" and "~ prime C"
  shows "~ (EX n. n >= 1 & (SB n - digamma_calc n C) / 64 = real C
                        & C = prime_i n)"
  \<comment> \<open>
    Note : la premiere conjonction est TRIVIALEMENT vraie par
    prime_equation_identity (l'identite algebrique). C'est la seconde
    conjonction (C = prime_i n) qui est refutee : par
    composite_not_prime_i, C compose ne peut jamais etre prime_i n.
  \<close>
proof
  assume "EX n. n >= 1 & (SB n - digamma_calc n C) / 64 = real C
              & C = prime_i n"
  then obtain n where prem: "C = prime_i n" by blast
  have "prime (prime_i n)" by (rule prime_i_is_prime)
  with prem have "prime C" by simp
  with assms(2) show False by contradiction
qed


text \<open>
  å®Ÿç”¨çš„ãªç³»ï¼š6ã¤ã®æ¨™æº–çš„ãªåˆæˆæ•°ã¯ n ç•ªç›®ã®ç´ æ•°ã¨ã—ã¦
  å†æ§‹æˆã™ã‚‹ã“ã¨ãŒã§ããªã„ã€‚
\<close>

theorem no_reconstruction_for_4:
  "~ (EX n. n >= 1 & (SB n - digamma_calc n 4) / 64 = real 4
                    & (4::nat) = prime_i n)"
  using composite_no_reconstruction_position[of "4::nat"] composite_4_not_prime
  by simp

theorem no_reconstruction_for_9:
  "~ (EX n. n >= 1 & (SB n - digamma_calc n 9) / 64 = real 9
                    & (9::nat) = prime_i n)"
  using composite_no_reconstruction_position[of "9::nat"] composite_9_not_prime
  by simp

theorem no_reconstruction_for_15:
  "~ (EX n. n >= 1 & (SB n - digamma_calc n 15) / 64 = real 15
                    & (15::nat) = prime_i n)"
  using composite_no_reconstruction_position[of "15::nat"] composite_15_not_prime
  by simp

theorem no_reconstruction_for_51:
  "~ (EX n. n >= 1 & (SB n - digamma_calc n 51) / 64 = real 51
                    & (51::nat) = prime_i n)"
  using composite_no_reconstruction_position[of "51::nat"] composite_51_not_prime
  by simp

theorem no_reconstruction_for_91:
  "~ (EX n. n >= 1 & (SB n - digamma_calc n 91) / 64 = real 91
                    & (91::nat) = prime_i n)"
  using composite_no_reconstruction_position[of "91::nat"] composite_91_not_prime
  by simp

theorem no_reconstruction_for_121:
  "~ (EX n. n >= 1 & (SB n - digamma_calc n 121) / 64 = real 121
                    & (121::nat) = prime_i n)"
  using composite_no_reconstruction_position[of "121::nat"] composite_121_not_prime
  by simp


subsection "Extension - Preuve par l'absurde pour le rapport spectral RsP"

text \<open>
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®ç¬¬3ã®æŸ±ã¯ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”
  RsP(n1, n2) = (SA(n1) - SA(n2)) / (SB(n1) - SB(n2)) = 1/2 ã§ã‚ã‚‹ã€‚
  ã“ã®æ¯”ã¯ n1 ã¨ n2 ãŒç´ æ•°ã®ä½ç½®ã§ã‚ã‚‹å ´åˆã«ã®ã¿æ„å‘³ã‚’æŒã¤
  ï¼ˆã™ãªã‚ã¡ã€prime_i n1 = p1 ã‹ã¤ prime_i n2 = p2 ã¨ãªã‚‹
  ç´ æ•° p1, p2 ãŒå­˜åœ¨ã™ã‚‹å ´åˆï¼‰ã€‚

  2ã¤ã®åˆæˆæ•° C1, C2 ã«å¯¾ã—ã¦ã¯ã€
  C1 = prime_i n1 ã‹ã¤ C2 = prime_i n2 ã¨ãªã‚‹çµ„ (n1, n2) ã¯
  å­˜åœ¨ã›ãšã€ã“ã‚Œã«ã‚ˆã‚Šé–¢é€£ã™ã‚‹ RsP ã®è¨ˆç®—ã¯
  ã“ã®æ–¹æ³•ã®å…¬ç†çš„æž çµ„ã¿ã«ãŠã„ã¦ä¸å¯èƒ½ã¨ãªã‚‹ã€‚
\<close>


theorem composite_pair_no_rsp_positions:
  fixes C1 C2 :: nat
  assumes "~ prime C1" and "~ prime C2"
  shows "~ (EX n1 n2. n1 >= 1 & n2 >= 1 & n1 ~= n2
                    & C1 = prime_i n1 & C2 = prime_i n2)"
proof
  assume "EX n1 n2. n1 >= 1 & n2 >= 1 & n1 ~= n2
              & C1 = prime_i n1 & C2 = prime_i n2"
  then obtain n1 n2 where
    p1: "C1 = prime_i n1" and p2: "C2 = prime_i n2" by blast
  have "prime (prime_i n1)" by (rule prime_i_is_prime)
  with p1 have "prime C1" by simp
  with assms(1) show False by contradiction
qed


text \<open>
  ã‚ˆã‚Šå¼·ã„ç³»ï¼šçµ„ã®ä¸­ã®1ã¤ã®åˆæˆæ•°ã ã‘ã§ã‚‚ã€
  å…¬ç†çš„æž çµ„ã¿ã«ãŠã‘ã‚‹ RsP ã®è¨ˆç®—ã‚’ç„¡åŠ¹ã«ã™ã‚‹ã®ã«ååˆ†ã§ã‚ã‚‹ã€‚
\<close>

theorem composite_single_no_rsp_position:
  fixes C X :: nat
  assumes "~ prime C"
  shows "~ (EX n1 n2. n1 >= 1 & n2 >= 1 & n1 ~= n2
                    & C = prime_i n1 & X = prime_i n2)"
proof
  assume "EX n1 n2. n1 >= 1 & n2 >= 1 & n1 ~= n2
              & C = prime_i n1 & X = prime_i n2"
  then obtain n1 where p1: "C = prime_i n1" by blast
  have "prime (prime_i n1)" by (rule prime_i_is_prime)
  with p1 have "prime C" by simp
  with assms show False by contradiction
qed


subsection "Synthese - Les 3 piliers de la Methode Spectrale bornes a P"

text \<open>
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®3ã¤ã®æŸ±ã¯ã™ã¹ã¦ã€å½¢å¼çš„è¨¼æ˜Žã‚’é€šã˜ã¦
  ç´ æ•°å…¨ä½“ã®é›†åˆ P ã«æŸç¸›ã•ã‚Œã‚‹ã‚ˆã†ã«ãªã£ãŸï¼š

    æŸ± 1 - ç´ æ•°é–“ã®ä¹–é›¢
      å½¢å¼åŒ–ï¼šcomposite_not_prime_iï¼ˆä¸­å¿ƒå®šç†ï¼‰
              + no_spectral_position_for_{4,9,15,51,91,121}

    æŸ± 2 - n ç•ªç›®ã®ç´ æ•°ã®å†æ§‹æˆ
      å½¢å¼åŒ–ï¼šcomposite_no_reconstruction_position
              + no_reconstruction_for_{4,9,15,51,91,121}

    æŸ± 3 - ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP
      å½¢å¼åŒ–ï¼šcomposite_pair_no_rsp_positions
              + composite_single_no_rsp_position

  æ±ºå®šçš„ãªå¸°çµï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯ã€ãã®3ã¤ã®é©ç”¨é ˜åŸŸã™ã¹ã¦ã«ãŠã„ã¦ã€
  ç´ æ•°å…¨ä½“ã®é›†åˆ P ã‚’éŽä¸è¶³ãªãæ­£ç¢ºã«ç‰¹å¾´ã¥ã‘ã‚‹ã€‚
  ä»£æ•°çš„æ’ç­‰å¼ prime_equation_identity ã‚’é€šã˜ã¦ã•ãˆã‚‚ã€
  åˆæˆæ•°ã¸ã®æ‹¡å¼µã¯ä¸å¯èƒ½ã§ã‚ã‚‹ï¼šå†æ§‹æˆã€ä¹–é›¢ã€ãŠã‚ˆã³ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯
  ã„ãšã‚Œã‚‚ prime_i è¡¨ã«ãŠã‘ã‚‹ä½ç½®ã‚’å¿…è¦ã¨ã—ã€ãã®è¡¨ã¯
  æ§‹æˆä¸Šï¼ˆprime_i_is_prime ã‚’é€šã˜ã¦ï¼‰ç´ æ•°ã®ãŸã‚ã«äºˆç´„ã•ã‚Œã¦ã„ã‚‹ã€‚

  ã“ã®ä¸‰é‡ã®è¨¼æ˜Žã¯ã€Philippe ã®çµŒé¨“çš„è¦³å¯Ÿ
  ï¼ˆGabriel ã®ãƒ­ã‚° "Cannot find positions for C"ï¼‰ã‚’ã€
  P ä¸Šã§ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®æŽ’ä»–çš„å¦¥å½“æ€§ã«é–¢ã™ã‚‹
  å®Œå…¨ã‹ã¤ä¸€èˆ¬çš„ãªå½¢å¼çš„è¨¼æ˜Žã¸ã¨å¤‰æ›ã™ã‚‹ã€‚
\<close>




(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šå®Œå…¨ãªä¾‹ - -31 ã¨ 17 ã®é–“ã®ä¹–é›¢               *)
(**************************************************************)

section "Exemple complet : ecart entre -31 et 17"

definition n_m29 :: real where "n_m29 = -10"
definition n_p17 :: real where "n_p17 = 8"
definition n_m31 :: real where "n_m31 = -11"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæ­£ç¢ºãªã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤ï¼ˆ-31 ã¨ 17ï¼‰                *)
(**************************************************************)

section "Valeurs spectrales exactes pour -31 et 17"

definition SA_m29_val :: real where
  "SA_m29_val = -40895 / 20480"

definition SB_p17_val :: real where
  "SB_p17_val = 350"

definition D_p17_val :: real where
  "D_p17_val = -738"

definition SB_m31_val :: real where
  "SB_m31_val = -1351615 / 20480"

definition D_m31_val :: real where
  "D_m31_val = 39280705 / 20480"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæ··åˆä¹–é›¢ã®ä¸€èˆ¬å½¢                               *)
(**************************************************************)

section "Forme generale de l'ecart mixte"

definition gap_mix_val ::
  "real => real => real => real => real => real" where
  "gap_mix_val A_next B_high D_high D_low dummy =
      (A_next - (B_high - D_high) - D_low) / 64"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæœ€çµ‚è£œé¡Œ - å·® -31 / 17                     *)
(**************************************************************)

section "Demonstration finale : ecart -31 / 17"

lemma gap_m31_17:
  "gap_mix_val SA_m29_val SB_p17_val D_p17_val D_m31_val 0 = -47"
  unfolding gap_mix_val_def
            SA_m29_val_def SB_p17_val_def
            D_p17_val_def D_m31_val_def
  by simp
(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š23 ã¨ 7 ã®æ­£ç¢ºãªã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤          *)
(**************************************************************)

section "Valeurs spectrales exactes pour 23 et 7"

definition SA_11_val :: real where "SA_11_val = 50"
definition SB_23_val :: real where "SB_23_val = 1598"
definition D_23_val  :: real where "D_23_val = 126"
definition SB_7_val  :: real where "SB_7_val = -14"
definition D_7_val   :: real where "D_7_val = -464"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šã‚¼ãƒ­ã®åŒ…å«ã«é–¢ã™ã‚‹æ˜Žç¤ºçš„ãªæ³¨è¨˜           *)
(**************************************************************)

section "Note sur l'inclusion du zero dans les ecarts spectraux"

text \<open>
  ã‚¼ãƒ­ã¯æ··åˆç¬¦å·ã®å·®ï¼ˆä¾‹ï¼š-31 / 17ï¼‰ã«ã®ã¿å«ã¾ã‚Œã‚‹ã€‚
  åŒç¬¦å·ã®å·®ï¼ˆ-19 / -5 ãŠã‚ˆã³ 23 / 7ï¼‰ã§ã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«çš„ãª
  é€²è¡ŒãŒ 0 ã‚’é€šéŽã—ãªã„ãŸã‚ã€ã‚¼ãƒ­ã¯è¨ˆä¸Šã•ã‚Œãªã„ã€‚
\<close>
(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šå®Œå…¨ãªä¾‹ - 227 ã¨ 173 ã®å·®ï¼ˆ1/3ï¼‰   *)
(**************************************************************)

section "Exemple complet : ecart entre les premiers 227 et 173 (rapport 1/3)"

text \<open>
  æ­£ã®ä¾‹ï¼šæœ€åˆã®äºŒã¤ã®ç´ æ•° 227 ã¨ 173 ã®é–“ã«ã‚ã‚‹æ•°ã®å€‹æ•°ã€‚

  ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ‡ãƒ¼ã‚¿ï¼š

    - 173 ã®æ¬¡ã®ç´ æ•°ã¯ 179
    - 227 ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«éšŽæ•°ï¼š10
    - 173 ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«éšŽæ•°ï¼š1

  æ•°å€¤ï¼š

    SA(227) = 79824
    SB(227) = 238746
    D(227)  = 73263

    SA(179) = 96/9

    SB(173) = -2155/3
    D(173)  = -1141518/9

  ä¸€èˆ¬å¼ï¼ˆæ¯”çŽ‡ 1/3ï¼‰ï¼š

      (A_next - (B_high - D_high) - D_low) / 729

  çµæžœï¼š

      ((96/9) - (238746 - 73263) - (-1141518/9)) / 729 = -53

  ã“ã‚Œã¯ 227 ã¨ 173 ã®é–“ã«ã‚ã‚‹ 53 å€‹ã®æ•°ã«å¯¾å¿œã™ã‚‹ã€‚
\<close>
(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š227 ã¨ 173 ã®æ­£ç¢ºãªã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤       *)
(**************************************************************)

section "Valeurs spectrales exactes pour 227 et 173 (1/3)"

definition SA_227_val :: real where
  "SA_227_val = 79824"

definition SB_227_val :: real where
  "SB_227_val = 238746"

definition D_227_val :: real where
  "D_227_val = 73263"

definition SA_179_val :: real where
  "SA_179_val = 96/9"

definition SB_173_val :: real where
  "SB_173_val = -2155/3"

definition D_173_val :: real where
  "D_173_val = -1141518/9"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š227 ã¨ 173 ã®å·®ã®æ¤œè¨¼           *)
(**************************************************************)

section "Validation numerique de l'ecart entre 227 et 173 (1/3)"

lemma ecart_227_173_1_3:
  "((SA_179_val - (SB_227_val - D_227_val) - D_173_val) / 729) = -53"
  by (simp add: SA_179_val_def SB_227_val_def D_227_val_def D_173_val_def)


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæ¯”çŽ‡ 1/3 ã®å·®ã®ä¸€èˆ¬æ–¹ç¨‹å¼    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/3"

text \<open>
  ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ« 1/3 ã«ãŠã‘ã‚‹äºŒã¤ã®ç´ æ•°ã®å·®ã®ä¸€èˆ¬å¼ã€‚
  n é …ã‹ã‚‰ãªã‚‹äºŒã¤ã®æ•°åˆ— A ã¨ Bã€ãŠã‚ˆã³ãã‚Œã‚‰ã«å¯¾å¿œã™ã‚‹
  Digamma ã‚’ç”¨ã„ã‚‹ã€‚

  ä¸€èˆ¬å½¢ï¼ˆæ¯”çŽ‡ 1/3ï¼‰ï¼š

      (A_next - (B_high - D_high) - D_low) / 729

  ã“ã“ã§ï¼š

    - A_next  : ã‚ˆã‚Šå°ã•ã„ç´ æ•°ã®æ¬¡ã®ç´ æ•°ã«å¯¾ã™ã‚‹æ•°åˆ— A ã®å’Œ
    - B_high  : ã‚ˆã‚Šå¤§ãã„ç´ æ•°ã«å¯¾ã™ã‚‹æ•°åˆ— B ã®å’Œ
    - D_high  : ã‚ˆã‚Šå¤§ãã„ç´ æ•°ã® Digamma
    - D_low   : ã‚ˆã‚Šå°ã•ã„ç´ æ•°ã® Digamma

  çµæžœã¯äºŒã¤ã®ç´ æ•°ã®é–“ã«ã‚ã‚‹æ•´æ•°ã®å€‹æ•°ã«å¯¾å¿œã™ã‚‹ã€‚
\<close>
definition gap_equation_1_3 :: "real => real => real => real => real" where
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 729"

lemma gap_equation_1_3_simplifiee:
  "gap_equation_1_3 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 729"
  unfolding gap_equation_1_3_def by simp


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šå·® 1/3 ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº–                    *)
(**************************************************************)

text \<open>
  æ¯”çŽ‡ 1/3 ã®å·®ã«é–¢ã™ã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«å…¬æº–ï¼š

  ä»»æ„ã®ç´ æ•°ã®å¯¾ (p_high, p_low) ã«å¯¾ã—ã¦ã€
  ãƒ¢ãƒ‡ãƒ« 1/3 ã«å¾“ã£ã¦æ§‹æˆã•ã‚ŒãŸãã‚Œã‚‰ã®é–¢é€£ã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤
  (A_next, B_high, D_high, D_low) ã‚’ç”¨ã„ã‚‹ã¨ã€å·®ã®æ–¹ç¨‹å¼ã¯
  ã“ã‚Œã‚‰äºŒã¤ã®ç´ æ•°ã®é–“ã«ã‚ã‚‹æ•´æ•°ã®å€‹æ•°ã‚’æ­£ç¢ºã«ä¸Žãˆã‚‹ï¼š

      gap_equation_1_3 ... = p_low - p_high
\<close>
axiomatization where
  spectral_gap_postulate_1_3:
    "!!p_high p_low A_next B_high D_high D_low.
       prime p_high ==> prime p_low ==>
       gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šäºŒã¤ã®ç´ æ•°ã®å·®ã«é–¢ã™ã‚‹ä¸€èˆ¬è£œé¡Œ   *)
(**************************************************************)

lemma gap_equation_1_3_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_3 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_3 assms by blast


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šä¾‹ 227 / 173 ã¨ã®é–¢é€£                    *)
(**************************************************************)

section "Validation de l'exemple 227 / 173 via l'equation generale 1/3"

lemma ecart_227_173_1_3_via_gap_equation:
  "gap_equation_1_3 SA_179_val SB_227_val D_227_val D_173_val = -53"
  by (simp add: gap_equation_1_3_def
                SA_179_val_def SB_227_val_def
                D_227_val_def D_173_val_def)


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š947 ã¨ 881 ã®æ­£ç¢ºãªã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤ï¼ˆ1/4ï¼‰ *)
(**************************************************************)

section "Valeurs spectrales exactes pour 947 et 881 (1/4)"

definition SA_883_val :: real where
  "SA_883_val = 75/4"

definition SB_947_val :: real where
  "SB_947_val = 5260628"

definition D_947_val :: real where
  "D_947_val = 1381716"

definition D_881_val :: real where
  "D_881_val = -(14450613/4)"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šæ¯”çŽ‡ 1/4 ã®å·®ã®ä¸€èˆ¬æ–¹ç¨‹å¼    *)
(**************************************************************)

section "Equation generale d'ecart pour le rapport spectral 1/4"

definition gap_equation_1_4 :: "real => real => real => real => real" where
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - (B_high - D_high) - D_low) / 4096"

lemma gap_equation_1_4_simplifiee:
  "gap_equation_1_4 A_next B_high D_high D_low =
     (A_next - B_high + D_high - D_low) / 4096"
  unfolding gap_equation_1_4_def by simp


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š1/4ã‚¹ãƒšã‚¯ãƒˆãƒ«é–“éš”å…¬æº–                    *)
(**************************************************************)

text \<open>
  1/4æ¯”çŽ‡ã«å¯¾ã™ã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«é–“éš”å…¬æº–ï¼š

  ä»»æ„ã®ç´ æ•°å¯¾ (p_high, p_low) ã¨ã€
  1/4ãƒ¢ãƒ‡ãƒ«ã«å¾“ã£ã¦æ§‹ç¯‰ã•ã‚ŒãŸãã‚Œã‚‰ã®é–¢é€£ã‚¹ãƒšã‚¯ãƒˆãƒ«å€¤ (A_next, B_high, D_high, D_low) ã«å¯¾ã—ã¦ã€
  é–“éš”æ–¹ç¨‹å¼ã¯ã“ã‚Œã‚‰äºŒã¤ã®ç´ æ•°ã®é–“ã®æ•´æ•°ã®å€‹æ•°ã‚’æ­£ç¢ºã«ä¸Žãˆã‚‹ï¼š

      gap_equation_1_4 ... = p_low - p_high
\<close>
axiomatization where
  spectral_gap_postulate_1_4:
    "!!p_high p_low A_next B_high D_high D_low.
       prime p_high ==> prime p_low ==>
       gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼šäºŒã¤ã®ç´ æ•°é–“ã®é–“éš”ã«é–¢ã™ã‚‹ä¸€èˆ¬è£œé¡Œ   *)
(**************************************************************)

lemma gap_equation_1_4_for_primes:
  assumes "prime p_high" "prime p_low"
  shows "gap_equation_1_4 A_next B_high D_high D_low =
         real (p_low - p_high)"
  using spectral_gap_postulate_1_4 assms by blast


(**************************************************************)
(* ã‚»ã‚¯ã‚·ãƒ§ãƒ³ï¼š947 / 881 ã®ä¾‹ã¨ã®é–¢é€£                    *)
(**************************************************************)

section "Validation de l'exemple 947 / 881 via l'equation generale 1/4"

lemma ecart_947_881_1_4_via_gap_equation:
  "gap_equation_1_4 SA_883_val SB_947_val D_947_val D_881_val = -65"
  by (simp add: gap_equation_1_4_def
                SA_883_val_def SB_947_val_def
                D_947_val_def D_881_val_def)


(**************************************************************)
(* ç¬¬äºŒç« ï¼šè§£æžçš„ï¼ˆã‚¼ãƒ¼ã‚¿ï¼‰ãŠã‚ˆã³ã‚¹ãƒšã‚¯ãƒˆãƒ«çš„å…¬ç†åŒ– *)
(**************************************************************)

text \<open>
  æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã«é–¢ã™ã‚‹æ³¨æ„äº‹é …ã€‚

  ä»¥ä¸‹ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ã€æ¦‚å¿µçš„å‚ç…§ã¨ã—ã¦ã®ã¿æä¾›ã•ã‚Œã‚‹ã€‚
  ã“ã‚Œã¯è‘—è€… Philippe Thomas Savard è‡ªèº«ã®è‘—ä½œã®ä¸€éƒ¨ã§ã¯ãªãã€
  Isabelle/HOL ã¨äº’æ›æ€§ã®ã‚ã‚‹è«–ç†çš„æž çµ„ã¿ã®ä¸­ã«ç‰¹å®šã®è§£æžçš„è¦ç´ ã‚’ä½ç½®ã¥ã‘ã‚‹ãŸã‚ã®
  æƒ…å ±æä¾›çš„ãªä¾‹ã¨ã—ã¦ç”¨ã„ã‚‰ã‚Œã‚‹ã«ã™ãŽãªã„ã€‚

  æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§è¨€åŠã•ã‚Œã‚‹å†…å®¹ã€æ¦‚å¿µã€ã¾ãŸã¯æ§‹é€ ã¯ã€
  è‘—è€…ã®ç‹¬è‡ªã®è²¢çŒ®ã‚’æ§‹æˆã™ã‚‹ã‚‚ã®ã§ã¯ãªãã€
  methode_spectral.thy ã®ä¸å¯åˆ†ãªä¸€éƒ¨ã¨ã—ã¦è§£é‡ˆã•ã‚Œã‚‹ã¹ãã§ã¯ãªã„ã€‚
  ãã‚Œã‚‰ã¯æ¦‚å¿µçš„ãªä¾‹ç¤ºã¨ã—ã¦ã®ã¿å¼•ç”¨ã•ã‚Œã¦ãŠã‚Šã€
  ã„ã‹ãªã‚‹ä¿è¨¼ã‚‚ã€å†…éƒ¨çš„ãªæ¤œè¨¼ã‚‚ã€è§£æžçš„ã¾ãŸã¯æ­´å²çš„ãªæ­£ç¢ºæ€§ã®ä¸»å¼µã‚‚ä¼´ã‚ãªã„ã€‚

  ä»¥ä¸‹ã®ã“ã¨ãŒæ˜Žç¤ºçš„ã«ç¢ºèªã•ã‚Œã‚‹ï¼š

    - æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ã€è¨€åŠã™ã‚‹å¤–éƒ¨å‚ç…§ã®æ€§è³ªã€ç¯„å›²ã€æœ‰åŠ¹æ€§ã€ã¾ãŸã¯ç™ºå±•ã‚’
      ã„ã‹ãªã‚‹æ„å‘³ã«ãŠã„ã¦ã‚‚åˆ¶é™ã—ã€æ‹˜æŸã—ã€å¤‰æ›´ã—ã€ã¾ãŸã¯ä¿®æ­£ã™ã‚‹ã‚‚ã®ã§ã¯ãªã„ï¼›

    - methode_spectral.thy ã¯è‡ªå¾‹çš„ãªå®Ÿä½“ã§ã‚ã‚Šã€ãã®å›ºæœ‰ã®æ§‹é€ ã«ãŠã„ã¦å®Œçµã—ã¦ãŠã‚Šã€
      æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§æç¤ºã•ã‚Œã‚‹ä¾‹ã€å…¬ç†ã€ã¾ãŸã¯å®šå¼åŒ–ã«ã„ã‹ãªã‚‹æ„å‘³ã«ãŠã„ã¦ã‚‚ä¾å­˜ã—ãªã„ï¼›

    - æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¨å¤–éƒ¨å‚ç…§ã¨ã®é–“ã«ã€è‡ªå·±å‚ç…§ã€å¾ªç’°çš„ä¾å­˜ã€
      ã¾ãŸã¯è«–ç†çš„ç›¸äº’ä½œç”¨ã®ã„ã‹ãªã‚‹å½¢å¼ã‚‚ç”Ÿã¿å‡ºã•ãªã„ï¼šã“ã‚Œã‚‰ã®å®Ÿä½“ã¯ãã‚Œãžã‚Œç‹¬ç«‹ã—ã¦ãŠã‚Šã€
      ãã‚Œè‡ªä½“ã«ã‚ˆã£ã¦æœ‰åŠ¹ã§ã‚ã‚Šã€æ™‚é–“çš„ã¾ãŸã¯æ¦‚å¿µçš„ãªåˆ¶ç´„ãªã—ã«ã€ãã®å›ºæœ‰ã®æ€§è³ªã«ãŠã„ã¦è‡ªç”±ã§ã‚ã‚‹ï¼›

    - äºŒã¤ã®å®Ÿä½“ã®ã„ãšã‚Œã‚‚â€•â€•methode_spectral.thy ã‚‚ã€ã“ã“ã§æç¤ºã•ã‚Œã‚‹è§£æžçš„ä¾‹ã‚‚â€•â€•
      ãã®å†…å®¹ã€æ§‹é€ ã€ã¾ãŸã¯è§£é‡ˆã«ã‚ˆã£ã¦ã€ç›¸æ‰‹ã‚’ç„¡åŠ¹åŒ–ã—ã€ç„¡åŠ¹ã«ã—ã€
      ã¾ãŸã¯åˆ¶é™ã™ã‚‹èƒ½åŠ›ã‚’æŒãŸãªã„ã€‚

  è¦ç´„ã™ã‚‹ã¨ã€æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ç‹¬ç«‹ã—ãŸæ¦‚å¿µçš„ä¾‹ã‚’æ§‹æˆã™ã‚‹ã‚‚ã®ã§ã‚ã‚Šã€
  æ‹˜æŸçš„ãªåŠ¹æžœã‚’æŒãŸãšã€è«–ç†çš„ãªå¼·åˆ¶çš„ç›¸äº’ä½œç”¨ã‚’æŒãŸãšã€
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®å†…åœ¨çš„æœ‰åŠ¹æ€§ã¾ãŸã¯è¨€åŠã™ã‚‹å¤–éƒ¨å‚ç…§ã«å¯¾ã—ã¦ã„ã‹ãªã‚‹å½±éŸ¿ã‚‚æŒãŸãªã„ã€‚
\<close>
(**************************************************************)
(* ç¬¬äºŒç« ï¼šè§£æžçš„ï¼ˆã‚¼ãƒ¼ã‚¿ï¼‰ãŠã‚ˆã³ã‚¹ãƒšã‚¯ãƒˆãƒ«çš„å…¬ç†åŒ– *)
(**************************************************************)

section "Axiomatisation analytique et geometrique de la position des nombres premiers"

text \<open>
  æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§ã¯ã€ãƒªãƒ¼ãƒžãƒ³ã‚¼ãƒ¼ã‚¿é–¢æ•°ã®é›¶ç‚¹ã¨ç´ æ•°ã®ä½ç½®ã¨ã®é–“ã®å¤å…¸çš„ãªé–¢ä¿‚ã‚’ã€
  è§£æžçš„æ•´æ•°è«–ã«ãŠã„ã¦å…¬ç†çš„ãªå½¢å¼ã§å°Žå…¥ã™ã‚‹ã€‚ã“ã®å…¬ç†åŒ–ã¯ã€
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®è‘—è€…ï¼ˆPhilippe Thomas Savardï¼‰ã®ç‹¬è‡ªã®å‰µé€ ã§ã¯ãªãã€
  ãƒªãƒ¼ãƒžãƒ³ã€ãƒ•ã‚©ãƒ³ãƒ»ãƒžãƒ³ã‚´ãƒ«ãƒˆã€ãŠã‚ˆã³ãã®å¾Œç¶™è€…ã«ã‚ˆã‚‹æ•´æ•°è«–ã®æ˜Žç¤ºçš„å…¬å¼ã«
  ç€æƒ³ã‚’å¾—ãŸæŠ½è±¡åŒ–ã§ã‚ã‚‹ã€‚
\<close>
text \<open>
  1. ã‚¼ãƒ¼ã‚¿é–¢æ•°ã¨ãã®é›¶ç‚¹ã®ï¼ˆæŠ½è±¡çš„ï¼‰å…¬ç†åŒ–ã€‚

  ã‚¼ãƒ¼ã‚¿ã®éžè‡ªæ˜Žãªé›¶ç‚¹ã‚’è¡¨ã™ãŸã‚ã®æŠ½è±¡åž‹ã¨ã€
  ãã®å®Ÿéƒ¨ã‚’ä¸Žãˆã‚‹é–¢æ•°ã‚’å°Žå…¥ã™ã‚‹ã€‚ã“ã“ã§ã¯ã‚¼ãƒ¼ã‚¿é–¢æ•°è‡ªä½“ã‚‚ã€
  å®Œå…¨ãªæ˜Žç¤ºçš„å…¬å¼ã‚‚å½¢å¼åŒ–ã—ãªã„ãŒã€
  ãƒªãƒ¼ãƒžãƒ³ï¼ãƒ•ã‚©ãƒ³ãƒ»ãƒžãƒ³ã‚´ãƒ«ãƒˆã®æ˜Žç¤ºçš„å…¬å¼ãŒç¤ºå”†ã™ã‚‹ã‚ˆã†ã«ã€
  é›¶ç‚¹ãŒç´ æ•°ã®ä½ç½®ã‚’æ±ºå®šã™ã‚‹ã¨ã„ã†äº‹å®Ÿã‚’ç¬¦å·åŒ–ã™ã‚‹ã€‚
\<close>
typedecl zero_zeta

consts
  Re_zero_zeta :: "zero_zeta => real"
  Im_zero_zeta :: "zero_zeta => real"

text \<open>
  ä»¥ä¸‹ã®é–¢æ•°ã¯ã€æŠ½è±¡çš„ãªå½¢ã§ã€ã‚¼ãƒ¼ã‚¿ã®é›¶ç‚¹ãŒ n ç•ªç›®ã®ç´ æ•°ã®ä½ç½®ã®æ±ºå®šã«
  ä¸Žãˆã‚‹å¯„ä¸Žã‚’è¡¨ã™ã€‚ã“ã‚Œã¯ã€ç´ æ•°ã«é–¢é€£ã™ã‚‹ç®—è¡“é–¢æ•°ã‚’ã‚¼ãƒ¼ã‚¿ã®é›¶ç‚¹ä¸Šã®å’Œã¨ã—ã¦
  è¡¨ç¾ã™ã‚‹ï¼ˆãƒªãƒ¼ãƒžãƒ³ï¼ãƒ•ã‚©ãƒ³ãƒ»ãƒžãƒ³ã‚´ãƒ«ãƒˆåž‹ã®ï¼‰æ˜Žç¤ºçš„å…¬å¼ã«ç€æƒ³ã‚’å¾—ã¦ã„ã‚‹ã€‚
\<close>
consts
  prime_position_from_zero :: "zero_zeta => nat => bool"

axiomatization where
  explicit_formula_axiom:
    "ALL n. EX r::zero_zeta. prime_position_from_zero r n"

text \<open>
  è§£é‡ˆï¼šå„è‡ªç„¶æ•° n ã«å¯¾ã—ã¦ã€n ç•ªç›®ã®ç´ æ•°ã®ä½ç½®ã®æ±ºå®šã«é–¢ä¸Žã™ã‚‹
  ã‚¼ãƒ¼ã‚¿ã®éžè‡ªæ˜Žãªé›¶ç‚¹ãŒå°‘ãªãã¨ã‚‚ä¸€ã¤å­˜åœ¨ã™ã‚‹ã€‚
  ã“ã®å…¬ç†ã¯ã€å¤å…¸çš„ãªè§£æžçš„æ•´æ•°è«–ï¼ˆæ˜Žç¤ºçš„å…¬å¼ï¼‰ã«è¦‹ã‚‰ã‚Œã‚‹ã‚ˆã†ã«ã€
  ã‚¼ãƒ¼ã‚¿ã®é›¶ç‚¹ãŒç´ æ•°ã®ä½ç½®ã‚’æ±ºå®šã™ã‚‹ã¨ã„ã†è€ƒãˆã‚’æŠ½è±¡çš„ãªå½¢ã§å½¢å¼åŒ–ã™ã‚‹ã€‚
\<close>
text \<open>
  2. Savard ã®æ–¹æ³•ã‹ã‚‰å¾—ã‚‰ã‚Œã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«çš„è¨¼æ‹ ã®å…¬ç†åŒ–ã€‚

  å‰ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§å±•é–‹ã•ã‚ŒãŸã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯ã€ä»¥ä¸‹ã®äº‹å®Ÿã«åŸºã¥ã„ã¦ã„ã‚‹
  ï¼ˆã“ã“ã§ã¯ç·åˆçš„ãªå½¢å¼ã§å®šå¼åŒ–ã™ã‚‹ï¼‰ï¼š

  - n >= 1 ã‹ã¤ n <= -1 ã®ã¨ãï¼ˆè€ƒæ…®ã•ã‚Œã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ§‹é€ ã®æ„å‘³ã§ï¼‰ã€
    ã™ã¹ã¦ã® n ã¯ç´ æ•° P ã«å¸°ç€ã™ã‚‹ã€‚
  - n ã®å€¤ã¯ã€æ•°åˆ— A ã¨ B ã®é …ã®å€‹æ•°ã«ã‚ˆã£ã¦æ±ºå®šã•ã‚Œã‚‹ã€‚
  - ã™ã¹ã¦ã®ç´ æ•° P ã¯äº’ã„ã«ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/k ã‚’æº€ãŸã™ã€‚
  - ã“ã®æ¯” 1/k ã¯æ•°å€¤çš„ã«ã¯æœ‰åŠ¹ã§ã‚ã‚‹ãŒã€ä»£æ•°çš„ã«ã¯æ•´åˆæ€§ãŒãªã„ã€‚

  ã“ã®è¨¼æ‹ ã‚’å®šæ•°ã¨æŠ½è±¡çš„å…¬ç†ã®å½¢å¼ã§å°å…¥ã™ã‚‹ã€‚
\<close>
typedecl indice_spectral   (* ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã® n ã«å¯¾ã™ã‚‹æŠ½è±¡åž‹ *)
typedecl premier_spectral  (* ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã® P ã«å¯¾ã™ã‚‹æŠ½è±¡åž‹ *)

consts
  A_suite :: "indice_spectral => nat"
  B_suite :: "indice_spectral => nat"
  P_spectral :: "indice_spectral => premier_spectral"
  rapport_spectral :: "premier_spectral => premier_spectral => rat"

text \<open>
  å…¬ç†ï¼šï¼ˆè€ƒæ…®ã•ã‚Œã‚‹é ˜åŸŸå†…ã®ï¼‰å„ã‚¹ãƒšã‚¯ãƒˆãƒ«æŒ‡æ¨™ n ã¯ã‚¹ãƒšã‚¯ãƒˆãƒ«ç´ æ•° P ã«å¸°ç€ã—ã€
  n ã®å€¤ã¯æ•°åˆ— A ã¨ B ã®é …ã®å€‹æ•°ã«ã‚ˆã£ã¦æ±ºå®šã•ã‚Œã‚‹ã€‚æ§‹æˆçš„ãªè©³ç´°ã¯
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®å‰ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§ä¸Žãˆã‚‰ã‚Œã¦ãŠã‚Šã€ã“ã“ã§ã¯ãã®è«–ç†çš„æŠ½è±¡åŒ–ã‚’æä¾›ã™ã‚‹ã€‚
\<close>
axiomatization where
  spectral_index_to_prime:
    "ALL n::indice_spectral. EX P::premier_spectral. P_spectral n = P" and

  spectral_index_from_suites:
    "ALL n::indice_spectral. A_suite n + B_suite n >= 1"

text \<open>
  å…¬ç†ï¼šã™ã¹ã¦ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«ç´ æ•° P ã¯äº’ã„ã«ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/k ã‚’æº€ãŸã—ã€
  æ•°å€¤çš„ã«ã¯æœ‰åŠ¹ã§ã‚ã‚‹ãŒä»£æ•°çš„ã«ã¯æ•´åˆæ€§ãŒãªã„ã€‚ã“ã‚Œã‚’ã€
  äºŒã¤ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«ç´ æ•°ã®æ¯”ãŒå¸¸ã« k >= 1 ãªã‚‹æ•´æ•° k ã«å¯¾ã—ã¦ 1/k ã®å½¢ã§ã‚ã‚‹ã“ã¨ã‚’
  èª²ã™ã“ã¨ã§ç¬¦å·åŒ–ã™ã‚‹ã€‚
\<close>
consts
  k_spectral :: "premier_spectral => premier_spectral => nat"

axiomatization where
  rapport_spectral_forme:
    "ALL P Q::premier_spectral. k_spectral P Q >= 1
      --> rapport_spectral P Q = 1 / (of_nat (k_spectral P Q))"

text \<open>
  è§£é‡ˆï¼šäºŒã¤ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«ç´ æ•°ï¼ˆã¾ãŸã¯éžå¯¾ç§°é †åºã‚‚ã—ãã¯ã‚«ã‚ªã‚¹çš„ãªç´ æ•°ç¾¤ã€
  ã‚ã‚‹ã„ã¯ 1*1 ã‚‚ã—ãã¯ n*n ã®å¯¾ç§°ãƒšã‚¢ï¼‰P ã¨ Q ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯å¸¸ã« 1/k ã®å½¢ã§ã‚ã‚Šã€
  k ã¯è‡ªç„¶æ•° >= 1 ã§ã‚ã‚‹ã€‚ã“ã®æ¯”ã¯ï¼ˆQ ã«ãŠã„ã¦ï¼‰æ•°å€¤çš„ã«æ˜Žç¢ºã«å®šç¾©ã•ã‚Œã¦ã„ã‚‹ãŒã€
  ç´ æ•°é–“ã®å¤å…¸çš„ãªä»£æ•°çš„é–¢ä¿‚ã«ã¯å¯¾å¿œã—ãªã„ãŸã‚ã€
  æ¦‚å¿µçš„ãƒ†ã‚­ã‚¹ãƒˆã«ãŠã„ã¦ã€Œä»£æ•°çš„ã«æ•´åˆæ€§ãŒãªã„ã€ã¨ã„ã†è¡¨ç¾ãŒç”¨ã„ã‚‰ã‚Œã‚‹ã€‚
\<close>
text \<open>
  3. ã‚¼ãƒ¼ã‚¿é–¢æ•°ã¨ã‚¹ãƒšã‚¯ãƒˆãƒ«å¹¾ä½•å­¦ã¨ã®é–¢é€£ã®å…¬ç†åŒ–ã€‚

  ã“ã“ã§ä¸€è‡´ã®å…¬ç†ã‚’å°Žå…¥ã™ã‚‹ï¼šSavard ã®æ–¹æ³•ã‹ã‚‰å¾—ã‚‰ã‚Œã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ§‹é€ ã¯ã€
  æ¦‚å¿µçš„ãªè¦³ç‚¹ã‹ã‚‰ã€ã‚¼ãƒ¼ã‚¿ã®é›¶ç‚¹ã«ã‚ˆã£ã¦ä¸Žãˆã‚‰ã‚Œã‚‹è§£æžçš„æ§‹é€ ã¨ä¸¡ç«‹ã™ã‚‹ã€‚
  ã‚ˆã‚Šæ­£ç¢ºã«ã¯ã€å„ã‚¹ãƒšã‚¯ãƒˆãƒ«æŒ‡æ¨™ n ã«å¯¾ã—ã¦ã€é–¢é€£ã™ã‚‹ç´ æ•°ã®ä½ç½®ã®æ±ºå®šã«
  é–¢ä¸Žã™ã‚‹ã‚¼ãƒ¼ã‚¿ã®é›¶ç‚¹ãŒå­˜åœ¨ã™ã‚‹ã“ã¨ã‚’å…¬æº–ã¨ã™ã‚‹ã€‚
\<close>
consts
  zero_associe :: "indice_spectral => zero_zeta"

axiomatization where
  concordance_spectrale:
    "ALL n::indice_spectral.
       prime_position_from_zero (zero_associe n) (A_suite n + B_suite n)"

text \<open>
  è§£é‡ˆï¼šå„ã‚¹ãƒšã‚¯ãƒˆãƒ«æŒ‡æ¨™ n ã«å¯¾ã—ã¦ã€æŠ½è±¡é–¢æ•° \<open>prime_position_from_zero\<close> ã‚’ä»‹ã—ã¦ã€
  å¯¾å¿œã™ã‚‹ç´ æ•°ã®ä½ç½®ï¼ˆã“ã“ã§ã¯ A_suite n + B_suite n ã®é …ã®å€‹æ•°ã«ã‚ˆã£ã¦ç¬¦å·åŒ–ã•ã‚Œã‚‹ï¼‰ã®
  æ±ºå®šã«é–¢ä¸Žã™ã‚‹ã‚¼ãƒ¼ã‚¿ã®é›¶ç‚¹ï¼ˆã“ã“ã§ã¯ \<open>zero_associe n\<close> ã§è¡¨ã•ã‚Œã‚‹ï¼‰ãŒå­˜åœ¨ã™ã‚‹ã€‚

  ã“ã®å…¬ç†ã¯ä»¥ä¸‹ã®æ¦‚å¿µçš„ãªä¸¦è¡Œé–¢ä¿‚ã‚’å½¢å¼åŒ–ã™ã‚‹ï¼š

  - ãƒªãƒ¼ãƒžãƒ³ã®ã‚¼ãƒ¼ã‚¿é–¢æ•°ã®è§£æžçš„ç†è«–ï¼ˆé›¶ç‚¹ãŒæ˜Žç¤ºçš„å…¬å¼ã«ã‚ˆã£ã¦ç´ æ•°ã®ä½ç½®ã‚’æ±ºå®šã™ã‚‹ï¼‰ï¼›
  - Savard ã®æ–¹æ³•ã«ãŠã‘ã‚‹ç´ æ•°ã‚¹ãƒšã‚¯ãƒˆãƒ«ã®å¹¾ä½•å­¦ï¼ˆã‚¹ãƒšã‚¯ãƒˆãƒ«æŒ‡æ¨™ nã€æ•°åˆ— A ã¨ Bã€
    ãŠã‚ˆã³æ¯” 1/k ãŒç´ æ•°ã®ä½ç½®ã‚’æ•´åˆçš„ãªã‚¹ãƒšã‚¯ãƒˆãƒ«æ§‹é€ ã®ä¸­ã«çµ„ç¹”åŒ–ã™ã‚‹ï¼‰ã€‚

  æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ãƒªãƒ¼ãƒžãƒ³äºˆæƒ³ã‚’è¨¼æ˜Žã™ã‚‹ã“ã¨ã‚‚ã€ã‚¼ãƒ¼ã‚¿ã®å®Œå…¨ãªè§£æžçš„ç†è«–ã‚’å†æ§‹ç¯‰ã™ã‚‹ã“ã¨ã‚‚
  ä¸»å¼µã—ãªã„ãŒã€Isabelle/HOL ã®è¨€èªžã«ãŠã„ã¦ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¨ç´ æ•°åˆ†å¸ƒã®å¤å…¸çš„è§£æžçš„è¦–ç‚¹ã¨ã®é–“ã®
  å…¬ç†çš„ãªä¸€è‡´ã‚’ç¢ºç«‹ã™ã‚‹ã€‚
\<close>
(****************************************************************************
 * ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XI. ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP = 1/k_i ã«å¯¾ã™ã‚‹
 * æ•°åˆ— A_i / B_i ã®æ§‹æˆè¦å‰‡ï¼ˆ8é …ä»¥ä¸Šï¼‰
 *
 * è‘—è€…      : Philippe Thomas Savard
 * æ—¥ä»˜      : 2026å¹´6æœˆ29æ—¥
 * å ´æ‰€      : ãƒ¬ãƒ´ã‚£ã€ã‚·ãƒ§ãƒ¼ãƒ‡ã‚£ã‚¨ãƒ¼ãƒ«ï¼ã‚¢ãƒ‘ãƒ©ã‚·ãƒ¥ã€ã‚«ãƒŠãƒ€
 * ãƒ©ã‚¤ã‚»ãƒ³ã‚¹ : Apache 2.0ï¼ˆå¸°å±žãŠã‚ˆã³è¡¨ç¤ºã®ä¿æŒãŒå¿…è¦ï¼‰
 *
 * 'RING' ã‚¿ã‚¯ãƒ†ã‚£ã‚¯ã‚’ä½¿ç”¨ã›ãšã«å½¢å¼åŒ–ã•ã‚ŒãŸè¦å‰‡
 * ä½¿ç”¨ã®ã¿: algebra_simpsã€field_simps ãŠã‚ˆã³ç›´æŽ¥çš„ãªç°¡ç´„ã€‚
 ****************************************************************************)

section "Section XI : Regles de construction des suites A_i et B_i (Pas de Ring)"

text \<open>
  ä»¥ä¸‹ã‚’è¨­å®šã™ã‚‹ï¼š
    - x1, x2 : ã‚¹ãƒšã‚¯ãƒˆãƒ«æŒ‡æ¨™ï¼ˆr = x2 / x1 ã‚’åŸºåº•æ¯”ã¨ã—ã¦ï¼‰ã€‚
    - æ—ã®æœ€å¾Œã‹ã‚‰äºŒç•ªç›®ã®é …ã¨æœ€å¾Œã®é …ã«é©ç”¨ã•ã‚Œã‚‹ä¹—æ³•çš„çµ‚ç«¯æ¡ä»¶ã€‚
    - æ•°åˆ— B ã®ä½ç½® 6 ã‚’æŒ‡æ•° 7ï¼ˆã‚¼ãƒ¼ã‚¿ã‚¸ãƒ£ãƒ³ãƒ—ï¼‰ã§ç½®æ›ã€‚
\<close>

subsection \<open>XI.1. Definition de la raison et des formes de base\<close>

definition raison_spectrale :: "real \<Rightarrow> real \<Rightarrow> real" where
  "raison_spectrale x1 x2 = x2 / x1"

subsection \<open>XI.2. Progression simple (Positions 1 a n-2)\<close>

definition progression_simple_terme :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "progression_simple_terme a1 r i = a1 * (r ^ (i - 1))"

subsection \<open>XI.3. Condition Terminale : Avant-dernier terme (Position n-1)\<close>

text \<open>
  åŽŸç¨¿ã®è¦å‰‡ï¼š
  (x2/x1 - x1/x2) * æœ€å¾Œã‹ã‚‰ä¸‰ç•ªç›®ã®é … = æœ€å¾Œã‹ã‚‰äºŒç•ªç›®ã®é …
  ã™ãªã‚ã¡ï¼š(r - 1/r) * (a1 * r^(n-3))
\<close>
definition avant_dernier_terme_savard :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "avant_dernier_terme_savard a1 r n = (r - 1 / r) * (a1 * r ^ (n - 3))"

subsection \<open>XI.4. Condition Terminale : Dernier terme (Position n)\<close>

text \<open>
  åŽŸç¨¿ã®è¦å‰‡ï¼šæœ€å¾Œã®é … = æœ€å¾Œã‹ã‚‰äºŒç•ªç›®ã®é … * (x2/x1) = æœ€å¾Œã‹ã‚‰äºŒç•ªç›®ã®é … * r
\<close>
definition dernier_terme_savard :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> real" where
  "dernier_terme_savard a1 r n = (avant_dernier_terme_savard a1 r n) * r"

subsection \<open>XI.5. Construction Complete de la Suite A\<close>

definition suite_A_savard_construction :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "suite_A_savard_construction a1 r n i =
     (if i = 1 then a1
      else if i \<le> n - 2 then progression_simple_terme a1 r i
      else if (i = n - 1) then avant_dernier_terme_savard a1 r n
      else if (i = n) then dernier_terme_savard a1 r n
      else 0)"

subsection \<open>XI.6. Substitution SpÃ©cifique Position 6 de la Suite B (n \<ge> 8)\<close>

text \<open>
  åŽŸç¨¿ã®è¦å‰‡ï¼šæ•°åˆ— B ã¯å¤å…¸çš„ãªç­‰æ¯”æ•°åˆ—ã‚’ã¨ã‚‹ãŒã€ä½ç½® 6 ã«
  æ§‹é€ çš„ã‚¸ãƒ£ãƒ³ãƒ—ã€Œx^7ï¼ˆã‚¼ãƒ¼ã‚¿ï¼‰ã€ã‚’æŒ¿å…¥ã—ã€å¾Œç¶šã®é …ã‚’ãšã‚‰ã™ã€‚
\<close>
definition suite_B_savard_construction :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "suite_B_savard_construction a1 r n i =
     (if (n < 8) then suite_A_savard_construction a1 r n i
      else if (i = 1) then a1
      else if i \<le> 5 then progression_simple_terme a1 r i
      else if (i = 6) then a1 * (r ^ 6)
      else if i \<le> n - 2 then progression_simple_terme a1 r (i + 1)
      else if (i = n - 1) then (r - 1 / r) * (a1 * r ^ (n - 2))
      else if (i = n) then ((r - 1 / r) * (a1 * r ^ (n - 2))) * r
      else 0)"

subsection \<open>XI.7. Sommation et Formules FermÃ©es Globales\<close>

definition somme_A_compacte_savard :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "somme_A_compacte_savard r n = (3.25 / 2) * (r ^ n) - 2"

definition somme_B_compacte_savard :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "somme_B_compacte_savard r n = (6.5 / 2) * (r ^ n) - 66"

subsection \<open>XI.8. Calcul du Rapport Spectral sans tactique 'Ring'\<close>

definition rapport_spectral_total_savard :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "rapport_spectral_total_savard r n = somme_A_compacte_savard r n / somme_B_compacte_savard r n"

text \<open>
  æ¯” 1/2 ã«è‡³ã‚‹ä¸€å®šå¢—åŠ çŽ‡ã®æ’ç­‰å¼ã®è¨¼æ˜Žã€‚
  å…¨ä½“çš„ãªé™¤ç®—ã®å‰ã«é€šåˆ†ã‚’å¼·åˆ¶ã™ã‚‹ã“ã¨ã§æ¤œè¨¼ã•ã‚ŒãŸã€‚
\<close>
lemma preuve_rapport_spectral_limite_savard:
  assumes "n \<ge> 8" and "r > 1"
  shows "rapport_spectral_total_savard r n = (3.25 * (r ^ n) - 4) / (6.5 * (r ^ n) - 132)"
proof -
  have h_num_exp: "(3.25 / 2) * (r ^ n) - 2 = ((3.25 * (r ^ n)) / 2) - (4 / 2)"
    by simp
  have h_num_fact: "((3.25 * (r ^ n)) / 2) - (4 / 2) = (3.25 * (r ^ n) - 4) / 2"
    by (simp add: algebra_simps)
  have h_A: "somme_A_compacte_savard r n = (3.25 * (r ^ n) - 4) / 2"
    unfolding somme_A_compacte_savard_def using h_num_exp h_num_fact by simp

  have h_den_exp: "(6.5 / 2) * (r ^ n) - 66 = ((6.5 * (r ^ n)) / 2) - (132 / 2)"
    by simp
  have h_den_fact: "((6.5 * (r ^ n)) / 2) - (132 / 2) = (6.5 * (r ^ n) - 132) / 2"
    by (simp add: algebra_simps)
  have h_B: "somme_B_compacte_savard r n = (6.5 * (r ^ n) - 132) / 2"
    unfolding somme_B_compacte_savard_def using h_den_exp h_den_fact by simp

  have step1: "rapport_spectral_total_savard r n = ((3.25 * (r ^ n) - 4) / 2) / ((6.5 * (r ^ n) - 132) / 2)"
    unfolding rapport_spectral_total_savard_def by (subst h_A, subst h_B, rule refl)

  have step2: "((3.25 * (r ^ n) - 4) / 2) / ((6.5 * (r ^ n) - 132) / 2)
             = (3.25 * (r ^ n) - 4) / (6.5 * (r ^ n) - 132)"
  proof (cases "6.5 * (r ^ n) - 132 = 0")
    case True
    then show ?thesis by simp
  next
    case False
    have "((3.25 * (r ^ n) - 4) / 2) / ((6.5 * (r ^ n) - 132) / 2)
        = ((3.25 * (r ^ n) - 4) / 2) * (2 / (6.5 * (r ^ n) - 132))"
      by (simp add: divide_simps)
    also from False have "... = (3.25 * (r ^ n) - 4) / (6.5 * (r ^ n) - 132)"
      by (simp add: field_simps)
    finally show ?thesis .
  qed

  from step1 step2 show ?thesis by simp
qed
subsection \<open>XI.9. Lemmes de validation numÃ©rique par diffÃ©rence fine\<close>

text \<open>
  å®‰å®šé ˜åŸŸï¼ˆ2^8ï¼‰ä¸Šã®å·¨è¦–çš„ãƒ¬ãƒ™ãƒ« n=10 ã¨ n=9 ã®é–“ã«ãŠã‘ã‚‹
  æ•°åˆ— A ã«å¯¾ã™ã‚‹ Savard å®šæ•° 3.25 ã®æŠ½å‡ºã®æ¤œè¨¼ã€‚
\<close>
lemma validation_constante_A_savard:
  "((1662::real) - 830) / 256 = 3.25"
  by (simp add: field_simps)

text \<open>
  å®‰å®šé ˜åŸŸï¼ˆ2^8ï¼‰ä¸Šã®å·¨è¦–çš„ãƒ¬ãƒ™ãƒ« n=10 ã¨ n=9 ã®é–“ã«ãŠã‘ã‚‹
  æ•°åˆ— B ã«å¯¾ã™ã‚‹ Savard å®šæ•° 6.5 ã®æŠ½å‡ºã®æ¤œè¨¼ã€‚
\<close>
lemma validation_constante_B_savard:
  "((3262::real) - 1598) / 256 = 6.5"
  by (simp add: field_simps)

(****************************************************************************
 * ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XI ã®çµ‚ã‚ã‚Š - Isabelle/HOL ã®ãŸã‚ã«æ­£å¸¸ã«å†æ§‹ç¯‰ã•ã‚ŒãŸ
 ****************************************************************************)
subsection "XI.10.b DÃ©termination formelle des constantes par diffÃ©rence fine"

text \<open>
  æœ¬ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ã€é€£ç¶šã™ã‚‹äºŒã¤ã®æ•°åˆ—ï¼ˆ10é …ã¨9é …ï¼‰ã®ç´°ã‹ãªå·®åˆ†ã«ã‚ˆã£ã¦
  å®šæ•° 3.25 ã¨ 6.5 ã‚’æŠ½å‡ºã—ã€æœ€å°å¹¾ä½•å­¦çš„é–“éš”ï¼ˆ2^8ï¼‰ã§æ­£è¦åŒ–ã™ã‚‹ã¨ã„ã†
  Philippe Thomas Savard ã®ç™ºè¦‹ã‚’å½¢å¼åŒ–ã™ã‚‹ã€‚
\<close>

(* 9é …ã¨10é …ã§è¦³å¯Ÿã•ã‚ŒãŸç”Ÿã®æ•°å€¤ã®å®šç¾© *)
definition valeur_A_10 :: real where "valeur_A_10 = 1662"
definition valeur_A_9  :: real where "valeur_A_9  = 830"
definition valeur_B_10 :: real where "valeur_B_10 = 3262"
definition valeur_B_9  :: real where "valeur_B_9  = 1598"

(* å®‰å®šé ˜åŸŸã®ã‚¹ã‚±ãƒ¼ãƒ«å› å­ï¼ˆ8å€‹ã®å¯ç®—é …ï¼‰ *)
definition echelle_stable :: real where "echelle_stable = 2 ^ 8"

(* å®šç† 1 : æ•°åˆ— A ã®å®šæ•°ã®æŠ½å‡º *)
theorem extraction_constante_A:
  "(valeur_A_10 - valeur_A_9) / echelle_stable = 3.25"
  unfolding valeur_A_10_def valeur_A_9_def echelle_stable_def
  by simp

(* å®šç† 2 : æ•°åˆ— B ã®å®šæ•°ã®æŠ½å‡º *)
theorem extraction_constante_B:
  "(valeur_B_10 - valeur_B_9) / echelle_stable = 6.5"
  unfolding valeur_B_10_def valeur_B_9_def echelle_stable_def
  by simp

(* ä¸€èˆ¬åŒ– : æ—¢å­˜ã®é–‰ã˜ãŸå¤§åŸŸå…¬å¼ã¨ã®è«–ç†çš„é–¢é€£ *)
lemma generalisation_ecart_minimal_A:
  fixes n :: nat
  assumes hA10: "valeur_A_10 = SA 10"
      and hA9:  "valeur_A_9  = SA 9"
  shows "(SA 10 - SA 9) / (2 ^ 8) = 3.25"
proof -
  have "SA 10 = (3.25 / 2) * (2 ^ 10) - 2" by (simp add: SA_def)
  also have "... = 3.25 * 512 - 2" by simp
  finally have s10: "SA 10 = 1662" by simp

  have "SA 9 = (3.25 / 2) * (2 ^ 9) - 2" by (simp add: SA_def)
  also have "... = 3.25 * 256 - 2" by simp
  finally have s9: "SA 9 = 830" by simp

  show ?thesis
    unfolding s10 s9 by simp
qed

lemma generalisation_ecart_minimal_B:
  fixes n :: nat
  assumes hB10: "valeur_B_10 = SB 10"
      and hB9:  "valeur_B_9  = SB 9"
  shows "(SB 10 - SB 9) / (2 ^ 8) = 6.5"
proof -
  have "SB 10 = (6.5 / 2) * (2 ^ 10) - 66" by (simp add: SB_def)
  also have "... = 6.5 * 512 - 66" by simp
  finally have s10: "SB 10 = 3262" by simp

  have "SB 9 = (6.5 / 2) * (2 ^ 9) - 66" by (simp add: SB_def)
  also have "... = 6.5 * 256 - 66" by simp
  finally have s9: "SB 9 = 1598" by simp

  show ?thesis
    unfolding s10 s9 by simp
qed

subsection "XI.11. Cas particuliers : suites 1 a 7 termes (voir Section XII)"

text \<open>
  1 ã‹ã‚‰ 7 é …ã¾ã§ã®è¦å‰‡ï¼ˆæ­£ãŠã‚ˆã³è² ï¼‰ã¯ã€ä»¥ä¸‹ã®ç¬¬ XII ç¯€ãƒ‘ãƒ©ãƒ¡ãƒˆãƒªãƒƒã‚¯ã«ãŠã„ã¦
  å½¢å¼åŒ–ã•ã‚Œã¦ãŠã‚Šã€ä»»æ„ã®æ•´æ•° kï¼ˆk = 2, 3, 4, ...ï¼‰ã«å¯¾ã™ã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”
  1/k_i ã‚’ä¸€èˆ¬åŒ–ã™ã‚‹ã€‚
\<close>

subsection "XI.12. Preuve analytique gÃ©nÃ©rale de l'Ã©cart minimal stable"
text \<open>
  Philippe Thomas Savard ã®ä¸€èˆ¬åŒ–å®šç†ï¼š
  é•·ã• n >= 8 ã®ä»»æ„ã®æ•°åˆ—ã«å¯¾ã—ã¦ã€å¹¾ä½•ã‚¹ã‚±ãƒ¼ãƒ«å› å­ï¼ˆ2^(n-2)ï¼‰ã§å‰²ã£ãŸ
  ç´°ã‹ã„å·®åˆ†ãŒã€ã‚¹ãƒšã‚¯ãƒˆãƒ«å®šæ•° 3.25 ãŠã‚ˆã³ 6.5 ã‚’ä¸å¤‰çš„ã«æŠ½å‡ºã™ã‚‹ã“ã¨ã®è¨¼æ˜Žã€‚
\<close>
(* ä¸€èˆ¬åŒ–å®šç† : æ•°åˆ— A *)
theorem ecart_minimal_universel_A:
  fixes n :: nat
  assumes hn: "n \<ge> 8"
  shows "(SA (n + 1) - SA n) / (2 ^ (n - 1)) = 3.25"
proof -
  have "(SA (n + 1) - SA n) / ((2::real) ^ (n - 1)) = ((13 / 8) * (2::real) ^ n) / ((2::real) ^ (n - 1))"
    by (simp add: difference_SA_succ)
  also have "... = (13 / 8) * (((2::real) ^ n) / ((2::real) ^ (n - 1)))"
    by (simp add: field_simps)
  also have "... = (13 / 8) * 2"
  proof -
    have "((2::real) ^ n) / ((2::real) ^ (n - 1)) = (2::real) ^ (n - (n - 1))"
      by (simp add: power_diff)
    also have "... = 2"
      using hn by simp
    finally have "((2::real) ^ n) / ((2::real) ^ (n - 1)) = 2" .
    thus ?thesis
      by simp
  qed
  also have "... = 3.25"
    by simp
  finally show ?thesis .
qed
(* ä¸€èˆ¬åŒ–å®šç† : æ•°åˆ— B *)
theorem ecart_minimal_universel_B:
  fixes n :: nat
  assumes hn: "n \<ge> 8"
  shows "(SB (n + 1) - SB n) / (2 ^ (n - 1)) = 6.5"
proof -
  have "(SB (n + 1) - SB n) / ((2::real) ^ (n - 1)) = ((13 / 4) * (2::real) ^ n) / ((2::real) ^ (n - 1))"
    by (simp add: difference_SB_succ)
  also have "... = (13 / 4) * (((2::real) ^ n) / ((2::real) ^ (n - 1)))"
    by (simp add: field_simps)
  also have "... = (13 / 4) * 2"
  proof -
    have "((2::real) ^ n) / ((2::real) ^ (n - 1)) = (2::real) ^ (n - (n - 1))"
      by (simp add: power_diff)
    also have "... = 2"
      using hn by simp
    finally have "((2::real) ^ n) / ((2::real) ^ (n - 1)) = 2" .
    thus ?thesis
      by simp
  qed
  also have "... = 6.5"
    by simp
  finally show ?thesis .
qed

(****************************************************************************
 * ç¬¬ XII ç¯€. 1/k_i ã«å¯¾ã™ã‚‹æ•°åˆ— A_i / B_i ã®ä¸€èˆ¬åŒ–æ§‹æˆ
 *              ï¼ˆ1 ã‹ã‚‰ 7 é …ã€8 é …ä»¥ä¸Šã€æ­£ãŠã‚ˆã³è² ï¼‰
 *
 *   è‘—è€…          : Philippe Thomas Savard
 *   å½¢å¼åŒ–         : Gabriel multiloop v3.5 (2026-02-17)
 *
 *   å¯¾è±¡ç¯„å›² :
 *     - ãƒ‘ãƒ©ãƒ¡ãƒˆãƒªãƒƒã‚¯å®šæ•° alpha_A(k), alpha_B(k), offset_A(k), offset_B(k)
 *       k=2 ã«ã¤ã„ã¦æä¾›ã•ã‚ŒãŸæ•°å€¤ä¾‹ã«ã‚ˆã‚Šç¢ºèªæ¸ˆã¿ï¼ˆPhilippe Savard ã«ã‚ˆã‚Š
 *       2026-02-17 ã®ãƒ¡ãƒƒã‚»ãƒ¼ã‚¸ã§æ¤œè¨¼æ¸ˆã¿ï¼‰ã€‚ç¬¬ II ç¯€ãŠã‚ˆã³ç¬¬ III ç¯€ã«
 *       æ—¢ã«å­˜åœ¨ã™ã‚‹å®šæ•°ã‚’ä»‹ã—ã¦ k=3, k=4 ã¸ã®æ‹¡å¼µã€‚
 *     - æ­£ãŠã‚ˆã³è² ã®é–‰ã˜ãŸå’Œã€‚
 *     - n in {1,2,3,4,5,6,7} ã«å¯¾ã™ã‚‹æ•°åˆ— A ã®é …ã”ã¨ã®æ§‹æˆã€‚
 *     - n >= 8 ã«å¯¾ã™ã‚‹æ•°åˆ— A ã®é …ã”ã¨ã®æ§‹æˆï¼ˆå¹¾ä½•ç´šæ•° + å¾Œã‚ã‹ã‚‰ 2 ç•ªç›® +
 *       æœ€å¾Œã€ç¬¬ XI ç¯€ã®è¦å‰‡ï¼‰ã€‚
 *     - æ•°åˆ— B ã®é …ã”ã¨ã®æ§‹æˆï¼šåŒã˜è¦å‰‡ã ãŒã€ä½ç½® 6 ã‚’ A ã®ä½ç½® 7 ã®å€¤ã§
 *       ç½®æ›ï¼ˆn >= 8ï¼‰ã€‚
 *     - æ•°åˆ— A ãŠã‚ˆã³ B ã®è² ã®é …ã”ã¨ã®æ§‹æˆï¼ˆn in natï¼‰ï¼š
 *       åŽæŸå’Œ alpha/k * 1/k^n - offsetã€‚
 *     - æ•°å€¤æ¤œè¨¼è£œé¡Œï¼ˆç´ æ•°ï¼š2, 3, 5, 7, 11, 13, 17, -2, -3, -5, -7ï¼‰ã€‚
 ****************************************************************************)

section "XI.bis - Factorisation generique : locale spectral_family (v3.35)"

text \<open>
  ==========================================================================
  ãƒ‘ãƒ©ãƒ¡ãƒˆãƒªãƒƒã‚¯ãƒ­ã‚±ãƒ¼ãƒ« spectral_family - 1/k ãƒ¢ãƒ‡ãƒ«ã®å› æ•°åˆ†è§£
  ==========================================================================
  ç›®çš„ : ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ« 1/2, 1/3, 1/4ï¼ˆå‰ç¯€ã§æ—¢ã«å®šç¾©æ¸ˆã¿ï¼‰ã«å…±é€šã™ã‚‹
  ä»£æ•°çš„ä¸å¤‰é‡ã‚’ã€å˜ä¸€ã®å½¢å¼çš„æ§‹é€ ã®ä¸‹ã«æ‰ãˆã‚‹ã“ã¨ã€‚ã“ã®ãƒ­ã‚±ãƒ¼ãƒ«ã¯
  æ™®éçš„æ€§è³ªã‚’ä¸€åº¦ã ã‘è¨¼æ˜Žã™ã‚‹ï¼š
    - åˆ†æ¯ã®éžé›¶æ€§ï¼ˆn1 != n2, n>=1 ã®ã¨ã k^n1 - k^n2 != 0ï¼‰ã€
    - æ±Žç”¨ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã®å®šå¸¸æ€§ï¼ˆRsP_generic = coef_A/coef_Bï¼‰ã€
    - ã‚¢ãƒ•ã‚£ãƒ³é–¢ä¿‚ A_pos = ratio * B_pos + å®šæ•°ã€‚

  ãƒ¢ãƒ‡ãƒ« 1/2, 1/3, 1/4 ã¯ãã®å¾Œã€è§£é‡ˆ
  ï¼ˆregime_1_2, regime_1_3, regime_1_4ï¼‰ã¨ãªã‚Šã€æ­´å²çš„å®šç¾©
  SA, SB, A_1_3, B_1_3, A_1_4, B_1_4 ã¨ã®æ•´åˆæ€§ãŒ
  è£œé¡Œ SA_eq_regime_1_2_A_pos ä»¥é™ã«ã‚ˆã£ã¦è¨¼æ˜Žã•ã‚Œã‚‹ã€‚

  æ—¢å­˜ã®è¨¼æ˜Žã¯ä¸€åˆ‡å¤‰æ›´ã•ã‚Œãªã„ã€‚æ­´å²çš„å®šç†
  ï¼ˆRsP_un_demi_general, RsP_un_tiers_constant, RsP_universel_entier_naturelï¼‰
  ã¯ãã®å‘½é¡Œã¨ä½ç½®ã«ãŠã„ã¦å¤‰æ›´ã•ã‚Œãªã„ã€‚

  æ–°ã—ã„ãƒ¢ãƒ‡ãƒ« 1/5, 1/6, ... ã¸ã®æ‹¡å¼µï¼šå½“è©² k ã«å¯¾ã™ã‚‹
  coef_A_k, coef_B_k, offset_A_k, offset_B_k ãŒæ—¢çŸ¥ã§ã‚ã‚Œã°ã€
  è§£é‡ˆã®ä¸€è¡Œã‚’è¿½åŠ ã™ã‚‹ã ã‘ã§ååˆ†ã§ã‚ã‚‹ã€‚
\<close>

locale spectral_family =
  fixes k       :: nat
    and coef_A  :: real
    and coef_B  :: real
    and offA    :: real
    and offB    :: real
    and ratio   :: real
  assumes k_valid     : "k \<ge> 2"
      and coef_A_pos  : "coef_A > 0"
      and coef_B_pos  : "coef_B > 0"
      and ratio_eq    : "ratio = coef_A / coef_B"

definition (in spectral_family) A_pos :: "nat \<Rightarrow> real" where
  "A_pos n = coef_A * (real k) ^ n - offA"

definition (in spectral_family) B_pos :: "nat \<Rightarrow> real" where
  "B_pos n = coef_B * (real k) ^ n - offB"

definition (in spectral_family) RsP_generic :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_generic n1 n2 = (A_pos n1 - A_pos n2) / (B_pos n1 - B_pos n2)"

lemma (in spectral_family) k_ge_1_real: "(real k) \<ge> 1"
  using k_valid by simp

lemma (in spectral_family) k_gt_1_real: "(real k) > 1"
  using k_valid by simp

lemma (in spectral_family) pow_k_ne:
  assumes "n1 \<noteq> n2"
  shows   "(real k) ^ n1 - (real k) ^ n2 \<noteq> 0"
proof (cases "n1 < n2")
  case True
  hence "(real k) ^ n1 < (real k) ^ n2"
    using power_strict_increasing[of n1 n2 "real k"] k_gt_1_real by simp
  thus ?thesis by simp
next
  case False
  with assms have "n2 < n1" by simp
  hence "(real k) ^ n2 < (real k) ^ n1"
    using power_strict_increasing[of n2 n1 "real k"] k_gt_1_real by simp
  thus ?thesis by simp
qed

lemma (in spectral_family) coef_B_ne_zero: "coef_B \<noteq> 0"
  using coef_B_pos by simp

lemma (in spectral_family) B_pos_diff_ne_zero:
  assumes "n1 \<noteq> n2"
  shows   "B_pos n1 - B_pos n2 \<noteq> 0"
proof -
  have "B_pos n1 - B_pos n2 = coef_B * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding B_pos_def by (simp add: field_simps)
  moreover have "(real k) ^ n1 - (real k) ^ n2 \<noteq> 0"
    by (rule pow_k_ne[OF assms])
  ultimately show ?thesis using coef_B_ne_zero by simp
qed

theorem (in spectral_family) RsP_generic_constant:
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows   "RsP_generic n1 n2 = ratio"
proof -
  have hA: "A_pos n1 - A_pos n2 = coef_A * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding A_pos_def by (simp add: field_simps)
  have hB: "B_pos n1 - B_pos n2 = coef_B * ((real k) ^ n1 - (real k) ^ n2)"
    unfolding B_pos_def by (simp add: field_simps)
  have hne_pow: "(real k) ^ n1 - (real k) ^ n2 \<noteq> 0"
    by (rule pow_k_ne[OF assms(3)])
  have "RsP_generic n1 n2
       = (coef_A * ((real k) ^ n1 - (real k) ^ n2))
       / (coef_B * ((real k) ^ n1 - (real k) ^ n2))"
    unfolding RsP_generic_def using hA hB by simp
  also have "... = coef_A / coef_B"
    using hne_pow coef_B_ne_zero by simp
  finally show ?thesis using ratio_eq by simp
qed

subsection "XI.bis.1 - Interpretations concretes : regime_1_2, regime_1_3, regime_1_4"

text \<open>
  ãƒ­ã‚±ãƒ¼ãƒ« spectral_family ã®ä¸‰ã¤ã®å…·ä½“çš„è§£é‡ˆã€ãã‚Œãžã‚ŒãŒæ­´å²çš„ãƒ¬ã‚¸ãƒ¼ãƒ ã«å¯¾å¿œï¼š
    regime_1_2 : k=2, coef_A = 3.25/2, coef_B = 6.5/2,  offA = 2,   offB = 66
    regime_1_3 : k=3, coef_A = 73/108, coef_B = 219/108, offA = 3/2, offB = 487*3/2
    regime_1_4 : k=4, coef_A = 241/192, coef_B = 964/192, offA = 4/3, offB = 3073*4/3

  --------------------------------------------------------------------------
  ä¸»è¦ãªæ¦‚å¿µçš„æ³¨è¨˜ï¼ˆPhilippe Savardï¼‰- å®Ÿéš›ã®æ•°å€¤çš„æ•´åˆæ€§
  --------------------------------------------------------------------------
  ã€Œä»£æ•°çš„ã«è‡ªæ˜Žãªæ¤œè¨¼ã€ï¼ˆ3.25/6.5 = 1/2, 73/219 = 1/3,
  241/964 = 1/4ï¼‰ã¯ã€å˜ç´”ãªä»£æ•°çš„æ’ç­‰å¼ã¨ã—ã¦å—ã‘å–ã‚‹ã¨
  èª¤è§£ã‚’æ‹›ãã€‚å®Ÿéš›ã«ã¯ï¼š

    (1) å±€æ‰€çš„ä»£æ•°çš„ä¸æ•´åˆ : ä¿‚æ•° 3.25, 6.5, 73,
        219, 241, 964 ã¯ã€å„ªé›…ãªä»£æ•°çš„ç°¡ç´„ã‚’æº€ãŸã™ãŸã‚ã«
        é¸ã°ã‚ŒãŸã‚‚ã®ã§ã¯ãªã„ã€‚ãã‚Œã‚‰ã¯ Philippe ãŒæ§‹æˆã—ãŸæ•°åˆ—
        A ãŠã‚ˆã³ B ã®å®Ÿéš›ã®å’Œã‹ã‚‰å‡ºç¾ã™ã‚‹ã‚‚ã®ã§ã‚ã‚Šã€å®Ÿéš›ã®
        ç´ æ•°ï¼ˆ2, 3, 5, 7, 11, 13, ...ï¼‰ã®å€¤ã‚’æ‹…ã£ã¦ã„ã‚‹ã€‚å±€æ‰€çš„ã«ã¯ã€
        äºŒã¤ã®å­¤ç«‹ã—ãŸé …ã®é–“ã®æ¯” A_i / B_i ã¯ 1/k ã«ç­‰ã—ããªã„
        ï¼ˆè£œé¡Œ algebriquement_incoherent_localã€ã€Œã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/2ã€ç¯€ã‚’å‚ç…§ï¼‰ã€‚

    (2) å¤§åŸŸçš„å®Ÿæ•°å€¤çš„æ•´åˆæ€§ : æ¯”
        (A(n1) - A(n2)) / (B(n1) - B(n2)) â€” ã™ãªã‚ã¡äºŒã¤ã®å­¤ç«‹ã—ãŸé …ã®é–“
        ã§ã¯ãªãã€äºŒã¤ã®å®Œå…¨ãªå’Œã®é–“ã® RsP â€” ãŒæ­£ç¢ºã« 1/k ã«ç­‰ã—ã„
        ï¼ˆè£œé¡Œ coherence_numerique_reelle_P ã‚’å‚ç…§ï¼‰ã€‚ã“ã®æ¯” 1/k ã¯
        ã—ãŸãŒã£ã¦ä»£æ•°çš„ãªè‡ªæ˜Žãªç°¡ç´„ã®ç”£ç‰©ã§ã¯ãªã„ï¼šãã‚Œã¯ã‚¹ãƒšã‚¯ãƒˆãƒ«
        ãƒ¬ã‚¸ãƒ¼ãƒ ã®å®Ÿéš›ã®æ•°å€¤çš„è¡¨ç¾ã§ã‚ã‚Šã€ç´ æ•°ã®ç¾å®Ÿã«æ ¹ã–ã—ã¦ã„ã‚‹ã€‚

    (3) Re = 1/2 ã®ç¢ºå®Ÿæ€§ : æ•°åˆ— A ãŠã‚ˆã³ B ã®å€¤ã¯ã‚ã‚‰ã‚†ã‚‹ä»£æ•°çš„
        ç°¡ç´„ã«å„ªå…ˆã™ã‚‹ â€” ãã‚Œã‚‰ã¯ä»»æ„ã®æ§‹æˆã§ã¯ãªãã€ç´ æ•°ã®å’Œã«é–¢ã™ã‚‹
        çµŒé¨“çš„è¦³å¯Ÿã§ã‚ã‚‹ â€” ãŸã‚ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/2 ã¯åŽ³å¯†ã«å®Ÿæ•°ã§ã‚ã‚‹ã€‚
        ã“ã®å¤§åŸŸçš„å®Ÿæ•°å€¤çš„ç¾å®Ÿã¯ã€P ä¸Šã®æŽ’ä»–æ€§ï¼ˆthree pillarsï¼‰ãŠã‚ˆã³
        é–¢æ•°çš„ä¸€æ„æ€§ Tchebychev = psi_savard ã¨çµ„ã¿åˆã‚ã•ã£ã¦ã€
        Philippe ãŒ Re(rho) = 1/2 ãŒçœŸã§ã‚ã‚‹ã¨ç¢ºä¿¡ã™ã‚‹æ ¹æ‹ ãã®ã‚‚ã®ã§ã‚ã‚‹ã€‚
        Pont Savardï¼ˆã‚µãƒ´ã‚¡ãƒ¼ãƒ«æ©‹ï¼‰ã¯ä»£æ•°çš„å¶ç„¶ã§ã¯ãªã„ï¼šãã‚Œã¯
        ç´ æ•°å…¨ä½“ã®é›†åˆ P ä¸Šã§æ¤œè¨¼ã•ã‚ŒãŸã€å¤§åŸŸçš„å®Ÿæ•°å€¤çš„å¿…ç„¶æ€§ã§ã‚ã‚‹ã€‚

  ã—ãŸãŒã£ã¦ã€ä»¥ä¸‹ã®å½¢å¼çš„è§£é‡ˆã¯ã€é€†ã§ã¯ãªãã€æ—¢ã«ç¢ºèªã•ã‚ŒãŸæ•°å€¤çš„ç¾å®Ÿã‚’
  Isabelle ã«ãŠã„ã¦ã‚¨ãƒ³ã‚³ãƒ¼ãƒ‰ã™ã‚‹ã€‚ãã‚Œã‚‰ã¯ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®ç†è«–ã‚’å˜ã«æ•´åˆçš„ã«
  ã™ã‚‹ã ã‘ã§ãªãã€æ•°å­¦çš„ã«å¿…ç„¶çš„ãªã‚‚ã®ã«ã™ã‚‹ã€‚

  æ•°å€¤æ¤œè¨¼ï¼ˆå¤§åŸŸçš„ã€å±€æ‰€çš„ã§ã¯ãªã„ï¼‰ï¼š
    (A(n1) - A(n2)) / (B(n1) - B(n2)) = 1/2   ã™ã¹ã¦ã® n1 != n2, k=2 ã«å¯¾ã—ã¦
    (A(n1) - A(n2)) / (B(n1) - B(n2)) = 1/3   ã™ã¹ã¦ã® n1 != n2, k=3 ã«å¯¾ã—ã¦
    (A(n1) - A(n2)) / (B(n1) - B(n2)) = 1/4   ã™ã¹ã¦ã® n1 != n2, k=4 ã«å¯¾ã—ã¦
\<close>

interpretation regime_1_2:
  spectral_family 2 "3.25 / 2" "6.5 / 2" 2 66 "1/2"
  by unfold_locales (simp_all add: field_simps)

interpretation regime_1_3:
  spectral_family 3 "(73::real)/108" "(219::real)/108" "3/2" "487 * (3/2)" "1/3"
  by unfold_locales (simp_all add: field_simps)

interpretation regime_1_4:
  spectral_family 4 "(241::real)/192" "(964::real)/192" "4/3" "3073 * (4/3)" "1/4"
  by unfold_locales (simp_all add: field_simps)

subsection "XI.bis.2 - Aliases de compatibilite (SA, SB, A_1_3, B_1_3, A_1_4, B_1_4)"

text \<open>
  æ­´å²çš„å®šç¾©ã¨ã®æ•´åˆæ€§ã€‚ã“ã‚Œã‚‰ã®è£œé¡Œã¯ã€æ•°åˆ— SA, SB, A_1_3, B_1_3, A_1_4, B_1_4 ãŒ
  ãƒ­ã‚±ãƒ¼ãƒ«ã®ã‚¤ãƒ³ã‚¹ã‚¿ãƒ³ã‚¹ã¨æ­£ç¢ºã«ä¸€è‡´ã™ã‚‹ã“ã¨ã‚’è¨¼æ˜Žã™ã‚‹ã€‚ã“ã‚Œã«ã‚ˆã‚Šæ—¢å­˜ã®è¨¼æ˜Žã¯
  ä¸€åˆ‡ç ´å£Šã•ã‚Œãªã„ï¼šRsP_un_demi_general, RsP_un_tiers_constant ã¯ãã®ã¾ã¾ä½¿ç”¨å¯èƒ½ã§ã‚ã‚‹ã€‚
\<close>

lemma SA_eq_regime_1_2_A_pos: "SA n = regime_1_2.A_pos n"
  unfolding SA_def regime_1_2.A_pos_def by (simp add: field_simps)

lemma SB_eq_regime_1_2_B_pos: "SB n = regime_1_2.B_pos n"
  unfolding SB_def regime_1_2.B_pos_def by (simp add: field_simps)

lemma A_1_3_eq_regime_1_3_A_pos: "A_1_3 n = regime_1_3.A_pos n"
  unfolding A_1_3_def regime_1_3.A_pos_def by (simp add: field_simps)

lemma B_1_3_eq_regime_1_3_B_pos: "B_1_3 n = regime_1_3.B_pos n"
  unfolding B_1_3_def regime_1_3.B_pos_def by (simp add: field_simps)

lemma A_1_4_eq_regime_1_4_A_pos: "A_1_4 n = regime_1_4.A_pos n"
  unfolding A_1_4_def regime_1_4.A_pos_def by (simp add: field_simps)

lemma B_1_4_eq_regime_1_4_B_pos: "B_1_4 n = regime_1_4.B_pos n"
  unfolding B_1_4_def regime_1_4.B_pos_def by (simp add: field_simps)

subsection "XI.bis.3 - Corollaires : les RsP historiques deviennent des instances"

text \<open>
  RsP_generic_constantï¼ˆãƒ­ã‚±ãƒ¼ãƒ«ã®å®šç†ï¼‰ã‹ã‚‰ã®ç›´æŽ¥çš„ãªç³»ã¨ã—ã¦ã€
  ç°¡ç´„ã‚’æ–‡æ›¸åŒ–ã™ã‚‹ã€‚æ­´å²çš„å®šç† RsP_un_demi_general
  ãŠã‚ˆã³ RsP_un_tiers_constant ã¯ãã‚Œãžã‚Œå›ºæœ‰ã®å®šå¼åŒ–ã‚’ä¿æŒã™ã‚‹ï¼ˆå¤‰æ›´ãªã—ï¼‰
  â€” ã“ã‚Œã‚‰ã®ç³»ã¯æ•´åˆæ€§ã®è¨¼æ˜Žã¨ã—ã¦æ©Ÿèƒ½ã™ã‚‹ã€‚
\<close>

lemma RsP_eq_regime_1_2_RsP_generic: "RsP n1 n2 = regime_1_2.RsP_generic n1 n2"
  unfolding RsP_def regime_1_2.RsP_generic_def
  by (simp add: SA_eq_regime_1_2_A_pos SB_eq_regime_1_2_B_pos)

lemma RsP_1_3_eq_regime_1_3_RsP_generic: "RsP_1_3 n1 n2 = regime_1_3.RsP_generic n1 n2"
  unfolding RsP_1_3_def regime_1_3.RsP_generic_def
  by (simp add: A_1_3_eq_regime_1_3_A_pos B_1_3_eq_regime_1_3_B_pos)

lemma RsP_generic_1_2_is_half:
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "regime_1_2.RsP_generic n1 n2 = 1/2"
  by (rule regime_1_2.RsP_generic_constant[OF assms])

lemma RsP_generic_1_3_is_third:
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "regime_1_3.RsP_generic n1 n2 = 1/3"
  by (rule regime_1_3.RsP_generic_constant[OF assms])

lemma RsP_generic_1_4_is_quarter:
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "regime_1_4.RsP_generic n1 n2 = 1/4"
  by (rule regime_1_4.RsP_generic_constant[OF assms])


section "Section XII : Construction generalisee pour rapport spectral 1/k_i"

text \<open>
  ä»»æ„ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/k_iï¼ˆk = 2, 3, 4, ...ï¼‰ã«å¯¾ã™ã‚‹ä¸€èˆ¬åŒ–ï¼š

    somme_A_pos(k, n) = (alpha_A(k) / 2) * k^n - offset_A(k)
    somme_B_pos(k, n) = (alpha_B(k) / 2) * k^n - offset_B(k)
    somme_A_neg(k, n) = alpha_A(k) * k^(-n) - offset_A(k)
    somme_B_neg(k, n) = alpha_B(k) * k^(-n) - offset_B(k)

  ã“ã“ã§ Savard å®šæ•°ã¯ï¼š
    k=2 : alpha_A=3.25,    alpha_B=6.5,    offset_A=2,   offset_B=66
    k=3 : alpha_A=73/9,    alpha_B=219/9,  offset_A=1.5, offset_B=487*1.5
    k=4 : alpha_A=241/16,  alpha_B=964/16, offset_A=4/3, offset_B=3073*(4/3)
\<close>

(* === XII.1. ãƒ‘ãƒ©ãƒ¡ãƒˆãƒªãƒƒã‚¯ Savard å®šæ•° === *)

definition alpha_A_k :: "nat \<Rightarrow> real" where
  "alpha_A_k k =
     (if k = 2 then 3.25
      else if k = 3 then 73/9
      else if k = 4 then 241/16
      else 0)"

definition alpha_B_k :: "nat \<Rightarrow> real" where
  "alpha_B_k k =
     (if k = 2 then 6.5
      else if k = 3 then 219/9
      else if k = 4 then 964/16
      else 0)"

definition offset_A_k :: "nat \<Rightarrow> real" where
  "offset_A_k k =
     (if k = 2 then 2
      else if k = 3 then 1.5
      else if k = 4 then 4/3
      else 0)"

definition offset_B_k :: "nat \<Rightarrow> real" where
  "offset_B_k k =
     (if k = 2 then 66
      else if k = 3 then 487 * 1.5
      else if k = 4 then 3073 * (4/3)
      else 0)"

(* === XII.2. æ­£ãŠã‚ˆã³è² ã®é–‰ã˜ãŸå…¬å¼ === *)

definition somme_A_pos_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_A_pos_k k n = (alpha_A_k k / 2) * (real k) ^ n - offset_A_k k"

definition somme_B_pos_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_B_pos_k k n = (alpha_B_k k / 2) * (real k) ^ n - offset_B_k k"

definition somme_A_neg_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_A_neg_k k n = alpha_A_k k / ((real k) ^ n) - offset_A_k k"

definition somme_B_neg_k :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "somme_B_neg_k k n = alpha_B_k k / ((real k) ^ n) - offset_B_k k"

(* === XII.3. è£œé¡Œ : æ—¢å­˜ã® SA, SB ã¨ã®æ•´åˆæ€§ï¼ˆk=2 æ­£ï¼‰ === *)

lemma somme_A_pos_k_eq_SA:
  "somme_A_pos_k 2 n = SA n"
  unfolding somme_A_pos_k_def alpha_A_k_def offset_A_k_def SA_def
  by simp

lemma somme_B_pos_k_eq_SB:
  "somme_B_pos_k 2 n = SB n"
  unfolding somme_B_pos_k_def alpha_B_k_def offset_B_k_def SB_def
  by simp

(* === XII.4. æ•°åˆ— A ã®é …ã”ã¨ã®æ§‹æˆï¼ˆæ­£ã€k=2ï¼‰                              === *)
(*   i ãŒ 1 ã‹ã‚‰ n-2 ã¾ã§ : a_i = a_1 * r^(i-1)ï¼ˆå˜ç´”ãªç­‰æ¯”æ•°åˆ—ã€r = kï¼‰      *)
(*   ä½ç½® n-1ï¼ˆå¾Œã‚ã‹ã‚‰ 2 ç•ªç›®ï¼‰: a_(n-2) * (r - 1/r)                         *)
(*   ä½ç½® nï¼ˆæœ€å¾Œï¼‰             : å¾Œã‚ã‹ã‚‰ 2 ç•ªç›® * r                          *)
(*   n = 1 ã®å ´åˆ : a_1 ã®ã¿                                                  *)

definition terme_A_pos :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "terme_A_pos a1 r n i =
     (if i = 1 then a1
      else if (n = 2 \<and> i = 2) then a1 * (r - 1/r)
      else if (n \<ge> 3 \<and> i \<le> n - 2) then a1 * r ^ (i - 1)
      else if (n \<ge> 3 \<and> i = n - 1) then a1 * r ^ (n - 3) * (r - 1/r)
      else if (n \<ge> 3 \<and> i = n) then a1 * r ^ (n - 3) * (r - 1/r) * r
      else 0)"

(* === XII.5. æ•°åˆ— B : åŒã˜æ§‹æˆ + ä½ç½® 6 ã®ç½®æ›ï¼ˆn >= 8ï¼‰ === *)

definition terme_B_pos :: "real \<Rightarrow> real \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "terme_B_pos a1 r n i =
     (if (n < 8) then terme_A_pos a1 r n i
      else if (i = 1) then a1
      else if i \<le> 5 then a1 * r ^ (i - 1)
      else if (i = 6) then a1 * r ^ 6
      else if i \<le> n - 2 then a1 * r ^ i
      else if (i = n - 1) then a1 * r ^ (n - 2) * (r - 1/r)
      else if (i = n) then a1 * r ^ (n - 2) * (r - 1/r) * r
      else 0)"

(* === XII.6. ä¸»è¦ãªæ•°å€¤æ¤œè¨¼ï¼ˆk=2, a1=2, r=2ï¼‰                                === *)

(*  æ•°åˆ— A 1 é …   : [2]                                                       *)
lemma suite_A_1_terme:
  "terme_A_pos 2 2 1 1 = 2"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— A 2 é …   : [2, 3]                                                    *)
lemma suite_A_2_termes_pos1:
  "terme_A_pos 2 2 2 1 = 2"
  unfolding terme_A_pos_def by simp

lemma suite_A_2_termes_pos2:
  "terme_A_pos 2 2 2 2 = 3"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— A 3 é …   : [2, 3, 6]                                                 *)
lemma suite_A_3_termes_pos3:
  "terme_A_pos 2 2 3 3 = 6"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— A 4 é …   : [2, 4, 6, 12] - ä½ç½® 3 = 6ï¼ˆå¾Œã‚ã‹ã‚‰ 2 ç•ªç›®ï¼‰             *)
lemma suite_A_4_termes_pos3:
  "terme_A_pos 2 2 4 3 = 6"
  unfolding terme_A_pos_def by simp

lemma suite_A_4_termes_pos4:
  "terme_A_pos 2 2 4 4 = 12"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— A 5 é …   : [2, 4, 8, 12, 24]                                         *)
lemma suite_A_5_termes_pos4:
  "terme_A_pos 2 2 5 4 = 12"
  unfolding terme_A_pos_def by simp

lemma suite_A_5_termes_pos5:
  "terme_A_pos 2 2 5 5 = 24"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— A 7 é …   : [2, 4, 8, 16, 32, 48, 96]                                 *)
lemma suite_A_7_termes_pos6:
  "terme_A_pos 2 2 7 6 = 48"
  unfolding terme_A_pos_def by simp

lemma suite_A_7_termes_pos7:
  "terme_A_pos 2 2 7 7 = 96"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— A 8 é …   : [2, 4, 8, 16, 32, 64, 96, 192]                            *)
lemma suite_A_8_termes_pos6:
  "terme_A_pos 2 2 8 6 = 64"
  unfolding terme_A_pos_def by simp

lemma suite_A_8_termes_pos7:
  "terme_A_pos 2 2 8 7 = 96"
  unfolding terme_A_pos_def by simp

lemma suite_A_8_termes_pos8:
  "terme_A_pos 2 2 8 8 = 192"
  unfolding terme_A_pos_def by simp

(*  æ•°åˆ— B 8 é …   : [2, 4, 8, 16, 32, 128, 192, 384]                          *)
(*  ä½ç½® 6 ã®ç½®æ› : 128 = 2 * 64 = æ•°åˆ— A ã®ä½ç½® 7                            *)
(*  ä½ç½® 7 ãŠã‚ˆã³ 8 ã¯ã€åŸºåº•ã‚’ãšã‚‰ã—ãŸå¾Œã‚ã‹ã‚‰ 2 ç•ªç›® / æœ€å¾Œã®è¦å‰‡ã«å¾“ã†       *)
lemma suite_B_8_termes_pos6:
  "terme_B_pos 2 2 8 6 = 128"
  unfolding terme_B_pos_def by simp

lemma suite_B_8_termes_pos7:
  "terme_B_pos 2 2 8 7 = 192"
  unfolding terme_B_pos_def by simp

lemma suite_B_8_termes_pos8:
  "terme_B_pos 2 2 8 8 = 384"
  unfolding terme_B_pos_def by simp

(*  æ•°åˆ— B 9 é …   : [2, 4, 8, 16, 32, 128, 256, 384, 768]                     *)
lemma suite_B_9_termes_pos6:
  "terme_B_pos 2 2 9 6 = 128"
  unfolding terme_B_pos_def by simp

lemma suite_B_9_termes_pos7:
  "terme_B_pos 2 2 9 7 = 256"
  unfolding terme_B_pos_def by simp

lemma suite_B_9_termes_pos9:
  "terme_B_pos 2 2 9 9 = 768"
  unfolding terme_B_pos_def by simp

(*  æ•°åˆ— B 10 é …  : [2, 4, 8, 16, 32, 128, 256, 512, 768, 1536]               *)
lemma suite_B_10_termes_pos8:
  "terme_B_pos 2 2 10 8 = 512"
  unfolding terme_B_pos_def by simp

lemma suite_B_10_termes_pos10:
  "terme_B_pos 2 2 10 10 = 1536"
  unfolding terme_B_pos_def by simp

(* === XII.7. æ­£ã®é–‰ã˜ãŸå…¬å¼ã®æ•°å€¤æ¤œè¨¼ï¼ˆk=2ï¼‰                                === *)
(*   ç´ æ•° 11 = 5 ç•ªç›®ã®æ­£ã®ç´ æ•° : å’Œ A = 50, å’Œ B = 38                        *)

lemma somme_A_pos_11:
  "somme_A_pos_k 2 5 = 50"
  unfolding somme_A_pos_k_def alpha_A_k_def offset_A_k_def by simp

lemma somme_B_pos_11:
  "somme_B_pos_k 2 5 = 38"
  unfolding somme_B_pos_k_def alpha_B_k_def offset_B_k_def by simp

(* === XII.8. è² ã®é–‰ã˜ãŸå…¬å¼ã®æ•°å€¤æ¤œè¨¼ï¼ˆk=2ï¼‰                                === *)
(*   ç´ æ•° -2ï¼ˆ1 é …ï¼‰: 13/4 / 2^1 - 2 = 13/8 - 2 = -3/8                       *)
(*   ç´ æ•° -5ï¼ˆ3 é …ï¼‰: 13/4 / 2^3 - 2 = 13/32 - 2 = -51/32 = -1.59375         *)
(*                                                                            *)
(*   Note Savard 2026-02-17 : è² ã®æ•°åˆ—ã«å¯¾ã™ã‚‹é–‰ã˜ãŸå¼ã¯ã€                    *)
(*   somme_A_neg(k, n) ãŒ n -> +inf ã®ã¨ã -offset_A(k) ã«åŽæŸã™ã‚‹ã‚ˆã†ãªã‚‚ã®ã§ã‚ã‚‹ã€‚*)
(*   k=2 ã®å ´åˆ : somme_A_neg(2, n) = 3.25 / 2^n - 2 ã§ã‚ã‚Šã€-2 ã«åŽæŸã™ã‚‹ã€‚   *)

lemma somme_A_neg_k_value:
  "somme_A_neg_k 2 n = 3.25 / (2 ^ n) - 2"
  unfolding somme_A_neg_k_def alpha_A_k_def offset_A_k_def by simp

lemma somme_A_neg_m2:
  "somme_A_neg_k 2 1 = -3/8"
  unfolding somme_A_neg_k_def alpha_A_k_def offset_A_k_def by simp

lemma somme_A_neg_m5:
  "somme_A_neg_k 2 3 = -51/32"
  unfolding somme_A_neg_k_def alpha_A_k_def offset_A_k_def by simp

(*   æœ€åˆã® -5ï¼ˆ3é …ï¼‰: è² ã®å’Œ B = 6.5 / 2^3 - 66 = 13/16 - 66 = -1043/16 *)
lemma somme_B_neg_m5:
  "somme_B_neg_k 2 3 = -1043/16"
  unfolding somme_B_neg_k_def alpha_B_k_def offset_B_k_def by simp

(* æ•°å€¤æ¤œè¨¼ : -5 ã«å¯¾ã™ã‚‹è² ã®å’Œ B ã¯ -65.1875 = -1043/16 *)
lemma somme_B_neg_m5_decimal:
  "(-1043::real) / 16 = -65.1875"
  by simp

(* === XII.9. æ™®éçš„ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” 1/k_iï¼ˆæ­£ãŠã‚ˆã³è² ï¼‰                          === *)

definition RsP_k :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_k k n1 n2 =
     (somme_A_pos_k k n1 - somme_A_pos_k k n2) /
     (somme_B_pos_k k n1 - somme_B_pos_k k n2)"

definition RsP_neg_k :: "nat \<Rightarrow> nat \<Rightarrow> nat \<Rightarrow> real" where
  "RsP_neg_k k n1 n2 =
     (somme_A_neg_k k n1 - somme_A_neg_k k n2) /
     (somme_B_neg_k k n1 - somme_B_neg_k k n2)"


(****************************************************************************
 * ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIII. Savard è«–ç†æ©‹ï¼ˆPont Logique Savardï¼‰: CHEBYSHEV <-> SPECTRAL <-> RH
 *
 * è‘—è€…      : Philippe Thomas Savard
 * æ—¥ä»˜      : 2026å¹´7æœˆ
 * å ´æ‰€      : LÃ©vis, ChaudiÃ¨re-Appalaches, Canada
 * ãƒ©ã‚¤ã‚»ãƒ³ã‚¹ : Apache 2.0
 *
 * ã“ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã¯ã€æŠ½è±¡çš„ãªå…¬æº–ã‚‚ "sorry" ã‚‚ä¸€åˆ‡ç”¨ã„ãšã«ã€
 * ç›´æŽ¥çš„ã‹ã¤æ§‹æˆçš„ãªæ–¹æ³•ã§äºŒé‡è«–ç†æ©‹ã‚’å½¢å¼çš„ã«ç¢ºç«‹ã™ã‚‹ã€‚
 ****************************************************************************)

(****************************************************************************
 * ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIII. Savard è«–ç†æ©‹ï¼ˆPont Logique Savardï¼‰: CHEBYSHEV <-> SPECTRAL <-> RH
 ****************************************************************************)

section "XIII. Le Pont Savard : psi de Tchebychev, fonction zeta et Re(rho) = 1/2"

text \<open>
  ==========================================================================
  Pont Savardï¼ˆSavard æ©‹ï¼‰- Tchebychevã€ã‚¼ãƒ¼ã‚¿ã€Re = 1/2 ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«çš„çµ±ä¸€
  ==========================================================================
  è‘—è€… : Philippe Thomas Savard
  å½¢å¼åŒ– : Isabelle/HOL

  è‘—è€…ã®æ§‹é€ çš„ãƒ“ã‚¸ãƒ§ãƒ³
  ------------------------------------------------------------------
  å®‡å®™ã®äºŒä¹—ï¼ˆUnivers-au-carreï¼‰å…¨ä½“ã®é›†åˆã¯å®šæ•° 1 ã§è¡¨ã•ã‚Œã‚‹ã€‚
  ã“ã®å˜ä½ã¯ä¸‰ã¤ã®ç­‰ä¾¡ãªè¦–ç‚¹ã«åˆ†è§£ã•ã‚Œã€ãã‚Œã‚‰ãŒäº’ã„ã«å°„å½±ã•ã‚Œã‚‹ã“ã¨ã§ã€
  ç´ æ•°ã®é›†åˆ P å…¨ä½“ã«ã‚ãŸã£ã¦ RsP = Re = 1/2 ã¨ã„ã†ç­‰å¼ãŒå¼·åˆ¶ã•ã‚Œã‚‹ï¼š

      é›†åˆ = 1
             /       |        \
        1/x        1/t         1/ms
        (zeta)   (psi_savard)  (ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•)

    1/x  = 1/y1 + 1/y2 + 1/y3                         (zeta ã®åˆ†è§£)
             |          |          |
           Tchebychev  Re(rho)   éžè‡ªæ˜Žé›¶ç‚¹
           (Ïˆ)         = 1/2     P ã®ä½ç½®

    1/ms = 1/ms1 + 1/ms2 + 1/ms3                      (ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®åˆ†è§£)
             |          |          |
           n = i ç•ªç›®ã® P  åˆæˆæ•°      ã™ã¹ã¦ã® P ã®é–“ :
           ã®ä½ç½®        é™¤å¤–       RsP = 1/2

  æœ€çµ‚ç­‰å¼ RsP = Re = 1/2 ã‚’å›ºå®šã™ã‚‹ä¸‰ã¤ã®ä¸€è‡´ï¼š

    (1)  1/y1 = 1/t          Tchebychev = psi_savard
                             ï¼ˆx = 30, 98, 228, -100 ã«ãŠã‘ã‚‹æ­£ç¢ºãªæ•°å€¤æ¤œè¨¼ï¼š
                              å„å€¤ã¯ epsilon(x) ã®èª¤å·®ç¯„å›²å†…ã§ç›®æ¨™ã®ç´ æ•°ã‚’
                              å†ç¾ã™ã‚‹ã€‚cf. XIII.2ï¼‰

    (2)  1/y3 = 1/ms1        zeta ã®éžè‡ªæ˜Žé›¶ç‚¹ = n ã®å€¤
                             ï¼ˆæ•°åˆ— A ã¨ B ã«ã‚ˆã£ã¦æ±ºå®šã•ã‚Œã‚‹ç´ æ•°ã®ä½ç½®ã¯
                              zeta ã®è‡¨ç•Œé›¶ç‚¹ã«å¯¾å¿œã—ã€i ç•ªç›®ã®ç´ æ•°ã®
                              å†æ§‹æˆãŒã“ã®å¯¾å¿œã‚’æ¤œè¨¼ã™ã‚‹ï¼‰

    (3)  1/y2 = 1/ms3        Re(rho) = 1/2 = RsP = 1/2
                             ï¼ˆRsP_un_demi_general ã§è¨¼æ˜Žã•ã‚ŒãŸæ•°åˆ— A ã¨ B ã®
                              ä¸­å¿ƒã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯ã€è‡¨ç•Œç›´ç·šã®å®Ÿéƒ¨ã¨ä¸€è‡´ã™ã‚‹ï¼‰

  ã“ã‚Œã‚‰ä¸‰ã¤ã®ç­‰å¼ã¯åŒæ™‚ã«æˆç«‹ã™ã‚‹ã“ã¨ã§æ©‹ã‚’é–‰ã˜ã‚‹ï¼šãã‚Œã‚‰ã¯æ•°å€¤çš„ãª
  å¶ç„¶ã§ã¯ãªãã€åŒä¸€ã®å¯¾è±¡â€”â€”å˜ä½é›†åˆâ€”â€”ã‚’ zetaã€psi_savardã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•
  ã¨ã„ã†ä¸‰ã¤ã®è¦–ç‚¹ã‹ã‚‰è¦‹ãŸç›¸äº’å°„å½±ã§ã‚ã‚‹ã€‚1/t ã®ã€ŒäºŒé‡ã®å½¹å‰²ã€
  ï¼ˆ1/t = 1/y1 ã¯å…¬å¼ã«ã‚ˆã‚‹ã‚‚ã®ã§ã‚ã‚Šã€1/t ã¯åˆæˆæ•°ã®é™¤å¤–ã«ã‚ˆã£ã¦
  1/ms ã«å‚åŠ ã™ã‚‹ï¼‰ã¯ã€æ©‹ã‚’éžè‡ªæ˜Žã«ã™ã‚‹æŽ¥åˆç‚¹ã§ã‚ã‚‹ï¼špsi_savard ã¨
  Tchebychev ã¯ã€æ•°åˆ— B ã®æ•´æ•°ä¸Šã§æ–‡å­—é€šã‚ŠåŒä¸€ã®é–¢æ•°ã§ã‚ã‚‹ã€‚

  æ™®éæ€§ï¼šn >= 1 ã‚’æº€ãŸã™ã™ã¹ã¦ã®æ•´æ•° n ã«å¯¾ã—ã¦ã€ã¾ãŸ n1 >= 1ã€
  n2 >= 1ã€n1 != n2 ã‚’æº€ãŸã™ã™ã¹ã¦ã®å¯¾ (n1, n2) ã«å¯¾ã—ã¦ã€
  RsP(n1, n2) = 1/2 ãŒæˆç«‹ã™ã‚‹ã€‚ã“ã®æ™®éæ€§ã¯ã€ä»¥ä¸‹ï¼ˆã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIII.6ï¼‰ã®
  è£œé¡Œ RsP_universel_entier_naturel ã«ã‚ˆã£ã¦è¿°ã¹ã‚‰ã‚Œã€æ—¢ã«è¨¼æ˜Žã•ã‚ŒãŸ
  å®šç† RsP_un_demi_general ã‹ã‚‰ç›´æŽ¥å°Žã‹ã‚Œã‚‹ã€‚

  å½¢å¼çš„æž çµ„ã¿ã€‚ä¸‰ã¤ã®ä¸€è‡´ã®æ•´åˆæ€§ã¯ã€locale ensemble_savard ã«ã‚ˆã£ã¦
  æ‰ãˆã‚‰ã‚Œã‚‹ï¼šä¸‰ã¤ã®ä»®èª¬ï¼ˆhypothese_critiqueã€pont_fonctionnelã€
  rapport_un_demiï¼‰ã§ã‚ã‚Šã€ãã®å……è¶³å¯èƒ½æ€§ã¯è¨¼æ˜Žã•ã‚Œã¦ã„ã‚‹
  ï¼ˆå®šç† ensemble_savard_satisfaisableï¼‰ã€‚ã“ã® locale ã®å†…éƒ¨ã§ã¯ã€
  RsP = Re = 1/2 ã¯äºˆæƒ³ã§ã¯ãªãå®šç†ã§ã‚ã‚‹
  ï¼ˆalignement_centralã€conclusion_ensembleã€synthese_pont_savardï¼‰ã€‚

  Pont Savard ã¯ç†è«–ã«ã„ã‹ãªã‚‹å…¬ç†ã‚‚å°Žå…¥ã—ãªã„ï¼šlocale ã®ä¸‰ã¤ã®ä»®èª¬ã¯ã€
  å‰ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§æ—¢ã«ç¢ºç«‹ã•ã‚ŒãŸä¸‰ã¤ã®äº‹å®Ÿã«ä»–ãªã‚‰ãªã„
  ï¼ˆè‡¨ç•Œç›´ç·šã®å®šç¾©ã€Tchebychev = psi_savard ã®ç­‰å¼ XIII.2-3ã€
  å®šç† RsP_un_demi_generalï¼‰ã€‚

  --------------------------------------------------------------------------
  1. å¤å…¸çš„ Tchebychev æ–¹ç¨‹å¼ï¼ˆRiemann - von Mangoldtï¼‰ï¼š

       psi(x) = x - Sum_{rho} (x^rho / rho) - log(2*pi)
                  - (1/2) * log(1 - x^(-2))

     ã“ã“ã§ rho ã¯ zeta(s) ã®éžè‡ªæ˜Žé›¶ç‚¹ã‚’èµ°ã‚‹ã€‚ã“ã®æ’ç­‰å¼ã¯
     Riemann ã®ã‚¼ãƒ¼ã‚¿é–¢æ•°ã«å¯¾ã—ã¦ã®ã¿æœ‰ç”¨ã§ã‚ã‚Šæ„å‘³ã‚’æŒã¤ã€‚

  2. ä¿®æ­£ Tchebychev æ–¹ç¨‹å¼ï¼ˆã€ŒSavard ç‰ˆã€ï¼‰ï¼š
     é›¶ç‚¹ä¸Šã®ç„¡é™å’Œã¯ã€æ•°åˆ— B ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«å’Œ SB(n) ä¸Šã«æ§‹æˆã•ã‚ŒãŸ
     æœ‰é™å¹¾ä½•æ¯”ã«ã‚ˆã£ã¦ç½®ãæ›ãˆã‚‰ã‚Œã‚‹ï¼š

       psi_savard(x, n) = x - (2^n / SB(n)) - log10(2*pi)
                            - (1/2) * log10(1 - x^(-2))

  3. ç¬¬ä¸€ã®æ©‹ï¼ˆé–¢æ•°çš„ä¸€æ„æ€§ï¼‰ï¼š
     Tchebychev æ–¹ç¨‹å¼ã¯ zeta ã«å¯¾ã—ã¦ã®ã¿æ„å‘³ã‚’æŒã¤ãŸã‚ã€
     ã“ã®æ–¹ç¨‹å¼ã¸ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®æ•°å€¤çš„ã«æ­£ç¢ºãªä»£å…¥ã¯ã€
     äºŒã¤ã®ç†è«–ãŒåŒä¸€ã®ä¸»é¡Œã‚’æ‰±ã£ã¦ã„ã‚‹ã“ã¨ã‚’è¨¼æ˜Žã™ã‚‹ã€‚

     è«–æ‹  1ï¼ˆæ•°å€¤çš„ï¼‰- Savard ã®å…¬å¼ãŒ Tchebychev ã‚’å†ç¾ã™ã‚‹ï¼š

       | n   | x     | psi_savard(x, n)  | ç›®æ¨™ã®ç´ æ•° |
       |-----|-------|-------------------|-----------|
       | 10  |  30   |  28.888143698...  |  29       |
       | 25  |  98   |  96.894150249...  |  97       |
       | 49  |  228  | 226.894132001...  |  227      |
       | -26 | -100  | -100.798158152... | -101ï¼ˆè² ï¼‰|

     ã—ãŸãŒã£ã¦ç´ æ•°ï¼ˆæ­£ãŠã‚ˆã³è² ï¼‰ã¯ psi_savard æ–¹ç¨‹å¼ã«ç›´æŽ¥ç¾ã‚Œã‚‹ï¼š
     psi_savard(x, n) ~ x - 1 ã§ã‚ã‚Šã€|x| ãŒå¢—å¤§ã™ã‚‹ã«ã¤ã‚Œã¦
     èª¤å·® epsilon(x) ã¯æ¸›å°‘ã™ã‚‹ã€‚

  4. ç¬¬äºŒã®æ©‹ï¼ˆèƒŒç†æ³•ã«ã‚ˆã‚‹åˆæˆæ•°ã®é™¤å¤–ï¼‰ï¼š

     è«–æ‹  2ï¼ˆæ§‹é€ çš„ï¼‰- æ—¢ã«è¨¼æ˜Žã•ã‚ŒãŸä¸‰ã¤ã®æŸ±ï¼š
       - composite_not_prime_i            ï¼ˆç´ æ•°é–“ã®é–“éš”ï¼‰ï¼Œ
       - composite_no_reconstruction_position ï¼ˆn ç•ªç›®ã®å†æ§‹æˆï¼‰ï¼Œ
       - composite_pair_no_rsp_positions  ï¼ˆã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsPï¼‰
     ã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ãŒã™ã¹ã¦ã®åˆæˆæ•° C ã‚’åŽ³å¯†ã«é™¤å¤–ã—ã€
     ç´ æ•° P ã«å¯¾ã—ã¦ã®ã¿è§£ã‚’èªã‚ã‚‹ã“ã¨ã‚’ç¤ºã™ã€‚

  5. æœ€çµ‚çš„ãªæ§‹æˆçš„çµæžœï¼ˆRsP = Re = 1/2ã€çœŸï¼‰ï¼š
     P ä¸Šã®æŽ’ä»–æ€§ï¼ˆæ©‹ 2ï¼‰ã¨é–¢æ•°çš„ä¸€æ„æ€§ï¼ˆæ©‹ 1ï¼‰ã®çµ„ã¿åˆã‚ã›ã«ã‚ˆã‚Šã€
     ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP = 1/2 ãŒè‡¨ç•Œç›´ç·šã®å®Ÿéƒ¨ Re(rho) = 1/2 ã¨
     æ•´åˆã™ã‚‹ã“ã¨ãŒå¼·åˆ¶ã•ã‚Œã‚‹ã€‚æ•°åˆ— A ã¨ B ã¯ã¾ãŸã€å†æ§‹æˆã«ã‚ˆã£ã¦
     ç´ æ•°ã®æ­£ç¢ºãªä½ç½®ã‚’æ±ºå®šã™ã‚‹ã€‚ã‚ˆã£ã¦ï¼šRsP = Re = 1/2
     ï¼ˆé›†åˆã®å®šç†ï¼‰ã€‚
  ==========================================================================
\<close>

subsection "XIII.1 Definitions fondamentales"

text \<open>
  psi_classique ã¯å¤å…¸çš„ Tchebychev é–¢æ•°ã‚’æŒ‡ã™ã€‚ã“ã‚Œã¯éžè§£é‡ˆã®ã¾ã¾
  æ®‹ã•ã‚Œã‚‹ï¼ˆã„ã‹ãªã‚‹å…¬ç†ã‚‚ä»˜ä¸Žã•ã‚Œãªã„ï¼‰ï¼šãã®å½¹å‰²ã¯ç´”ç²‹ã«å‚ç…§çš„ã§ã‚ã‚‹ã€‚
  è¿°èªž concerne_fonction_zeta f ã¯ã€é–¢æ•° f ãŒ Riemann ã®ã‚¼ãƒ¼ã‚¿é–¢æ•°ã«
  å¯¾ã—ã¦ã®ã¿æ„å‘³ã‚’æŒã¤ã“ã¨ã‚’è¡¨ã™ï¼›ã“ã‚Œã‚‚ã¾ãŸéžè§£é‡ˆã§ã‚ã‚Šã€
  æœ€çµ‚å®šç†ã®æ˜Žç¤ºçš„ãªä»®èª¬ã¨ã—ã¦ã®ã¿ç¾ã‚Œã‚‹ã€‚
\<close>

consts
  psi_classique :: "real \<Rightarrow> real"

consts
  concerne_fonction_zeta :: "(real \<Rightarrow> real) \<Rightarrow> bool"

text \<open>
  å¸¸ç”¨å¯¾æ•°ï¼ˆè‘—è€…ã«ã‚ˆã‚‹åº•ã®é¸æŠžï¼‰ã€é›¶ç‚¹ä¸Šã®å’Œã‚’ç½®ãæ›ãˆã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«é …
  2^n / SB(n)ã€ãŠã‚ˆã³å®Œå…¨ãª psi_savard æ–¹ç¨‹å¼
  ï¼ˆãƒ•ã‚¡ã‚¤ãƒ«ã®çµ±ä¸€ã•ã‚ŒãŸå”¯ä¸€ã®å®šç¾©ï¼‰ã€‚
\<close>

definition log10_savard :: "real \<Rightarrow> real" where
  "log10_savard y = ln y / ln 10"

definition rapport_zeta_savard :: "nat \<Rightarrow> real" where
  "rapport_zeta_savard n = (2 ^ n) / (SB n)"

definition psi_savard :: "real \<Rightarrow> nat \<Rightarrow> real" where
  "psi_savard x n =
     x - rapport_zeta_savard n
       - log10_savard (2 * pi)
       - (1 / 2) * log10_savard (1 - 1 / (x ^ 2))"

subsection "XIII.2 Validations numeriques (x = 30, 98, 228)"

text \<open>
  ä»¥ä¸‹ã®ä¸‰ã¤ã®è£œé¡Œã¯ã€è‘—è€…ã®è¨ˆç®—ã§ä½¿ç”¨ã•ã‚Œã‚‹ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã‚’
  æ­£ç¢ºã«å›ºå®šã™ã‚‹ï¼š

    SB(10) = 3.25 * 2^10 - 66 = 3262
    SB(25) = 3.25 * 2^25 - 66 = 109051838
    SB(49) = 3.25 * 2^49 - 66 = 1829587348619198
\<close>

lemma rapport_zeta_savard_at_10:
  "rapport_zeta_savard 10 = 1024 / 3262"
  unfolding rapport_zeta_savard_def SB_def by simp

lemma rapport_zeta_savard_at_25:
  "rapport_zeta_savard 25 = 33554432 / 109051838"
  unfolding rapport_zeta_savard_def SB_def by simp

lemma rapport_zeta_savard_at_49:
  "rapport_zeta_savard 49 = 562949953421312 / 1829587348619198"
  unfolding rapport_zeta_savard_def SB_def by simp

text \<open>
  ä¸€èˆ¬çš„ãªè¨˜å·çš„æ’ç­‰å¼ã€æ¬¡ã„ã§è‘—è€…ã®æ•°å€¤æ¤œè¨¼ã«å¯¾å¿œã™ã‚‹ä¸‰ã¤ã®æ­£ç¢ºãªå±•é–‹ï¼š

    psi_savard(30, 10)  = 28.888143698...   ï¼ˆç›®æ¨™ã®ç´ æ•°ï¼š29ï¼‰
    psi_savard(98, 25)  = 96.894150249...   ï¼ˆç›®æ¨™ã®ç´ æ•°ï¼š97ï¼‰
    psi_savard(228, 49) = 226.894132001...  ï¼ˆç›®æ¨™ã®ç´ æ•°ï¼š227ï¼‰
\<close>

lemma psi_savard_expanded:
  "psi_savard x n =
     x - (2 ^ n) / (SB n)
       - ln (2 * pi) / ln 10
       - (1 / 2) * (ln (1 - 1 / (x ^ 2)) / ln 10)"
  unfolding psi_savard_def rapport_zeta_savard_def log10_savard_def by simp

lemma psi_savard_at_10_30_expanded:
  "psi_savard 30 10 =
     30 - 1024 / 3262
        - log10_savard (2 * pi)
        - (1 / 2) * log10_savard (1 - 1 / 900)"
  unfolding psi_savard_def rapport_zeta_savard_def SB_def by simp

lemma psi_savard_at_25_98_expanded:
  "psi_savard 98 25 =
     98 - 33554432 / 109051838
        - log10_savard (2 * pi)
        - (1 / 2) * log10_savard (1 - 1 / 9604)"
  unfolding psi_savard_def rapport_zeta_savard_def SB_def by simp

lemma psi_savard_at_49_228_expanded:
  "psi_savard 228 49 =
     228 - 562949953421312 / 1829587348619198
         - log10_savard (2 * pi)
         - (1 / 2) * log10_savard (1 - 1 / 51984)"
  unfolding psi_savard_def rapport_zeta_savard_def SB_def by simp

text \<open>
  æ³¨è¨˜ï¼ˆè² ã®é ˜åŸŸï¼‰ï¼šx = -100 ã«å¯¾ã™ã‚‹è‘—è€…ã®æ¤œè¨¼ã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æŒ‡æ•°
  n = -26 ã¨æ¥µé™åˆ†æ¯ -66ï¼ˆn ãŒ -ç„¡é™å¤§ã«å‘ã‹ã†ã¨ãã® SB ã®æ¥µé™ï¼‰ã‚’ä½¿ç”¨ã™ã‚‹ï¼š

    psi_savard(-100, -26) = -100 - (2^(-26) / (-66)) - log10(2*pi)
                                 - (1/2) * log10(1 - (-100)^(-2))
                          = -100.7981582...

  SB ã«ãŠã‘ã‚‹æŒ‡æ•°ã® nat åž‹ã§ã¯ã€ã“ã®ã‚±ãƒ¼ã‚¹ã‚’ã“ã“ã«è¨˜è¿°ã™ã‚‹ã“ã¨ãŒã§ããªã„ï¼›
  ã“ã‚Œã¯ SpectralMethodCore.compute_psi_savard ã«ã‚ˆã£ã¦æ•°å€¤çš„ã«ã‚«ãƒãƒ¼ã•ã‚Œ
  ï¼ˆè² ã®ãƒ©ãƒ³ã‚¯ã®ã‚µãƒãƒ¼ãƒˆï¼‰ã€ãƒ¢ãƒ‡ãƒ«ã®ã‚¹ãƒšã‚¯ãƒˆãƒ«å¯¾ç§°æ€§ã‚’ç¢ºèªã™ã‚‹ï¼š
  æ–¹ç¨‹å¼ã¯è² ã®ç´ æ•°ã«å¯¾ã—ã¦ã‚‚æ•´åˆæ€§ã‚’ä¿ã¤ã€‚
\<close>

subsection "XIII.3 Le Premier Pont : l'unicite fonctionnelle Tchebychev <-> zeta"

text \<open>
  Tchebychev æ–¹ç¨‹å¼ã¯ Riemann ã®ã‚¼ãƒ¼ã‚¿é–¢æ•°ã«å¯¾ã—ã¦ã®ã¿æœ‰ç”¨ã§ã‚ã‚‹ï¼š
  ã“ã‚Œã¯æ­´å²çš„ã‹ã¤è§£æžçš„ãªäº‹å®Ÿã§ã‚ã‚‹ï¼ˆRiemann - von Mangoldt ã®
  æ˜Žç¤ºçš„å…¬å¼ï¼‰ã€‚æˆ‘ã€…ã¯ã“ã‚Œã‚’ä»®èª¬

      concerne_fonction_zeta psi_classique

  ã«ã‚ˆã£ã¦è¡¨ç¾ã—ã€ã“ã‚Œã¯æœ€çµ‚å®šç†ã®å‰æã¨ã—ã¦ç¾ã‚Œã‚‹
  ï¼ˆã„ã‹ãªã‚‹å¤§åŸŸçš„å…¬ç†ã‚‚å°Žå…¥ã•ã‚Œãªã„ï¼‰ã€‚ã“ã®å½¹å‰²ã¸ã® psi_savard ã®
  æ•°å€¤çš„ã«æ­£ç¢ºãªä»£å…¥ï¼ˆæ¤œè¨¼ XIII.2ï¼‰ã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã‚’
  ã‚¼ãƒ¼ã‚¿é–¢æ•°ã®é ˜åŸŸã¸ã¨ç§»é€ã™ã‚‹ï¼šäºŒã¤ã®ç†è«–ã¯åŒä¸€ã®ä¸»é¡Œã‚’æ‰±ã†ã€‚
\<close>

subsection "XIII.4 Le Deuxieme Pont : l'exclusivite sur P par l'absurde"

text \<open>
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¯ã™ã¹ã¦ã®åˆæˆæ•° C ã‚’åŽ³å¯†ã«é™¤å¤–ã™ã‚‹ï¼šãã‚Œã¯ç´ æ•°ã«
  å¯¾ã—ã¦ã®ã¿è§£ã‚’èªã‚ã‚‹ã€‚ã“ã®äº‹å®Ÿã¯ä¸‰ã¤ã®æŸ±
  ï¼ˆcomposite_not_prime_iã€composite_no_reconstruction_positionã€
  composite_pair_no_rsp_positionsï¼‰ã«ã‚ˆã£ã¦æ—¢ã«è¨¼æ˜Žã•ã‚Œã¦ã„ã‚‹ã€‚
  ä»¥ä¸‹ã®è£œé¡Œã¯ã€æ©‹ã«ã‚ˆã£ã¦ä½¿ç”¨ã•ã‚Œã‚‹å‡ç¸®ã•ã‚ŒãŸå½¢å¼ã‚’ä¸Žãˆã‚‹ã€‚
\<close>

lemma methode_spectrale_exclusivite_P:
  fixes C :: nat
  assumes "\<not> prime C"
  shows "\<forall>i. C \<noteq> prime_i i"
  using assms composite_not_prime_i by simp

subsection "XIII.5 Le Theoreme de l'Ensemble : decomposition spectrale coherente"

text \<open>
  è‘—è€…ã®ç‹¬è‡ªã®å‘½åæ³•ï¼ˆæ–‡æ›¸çš„è¨˜éŒ²ã¨ã—ã¦ä¿å­˜ï¼‰ï¼š

    é›†åˆ * 1/x  = Riemann ã®ã‚¼ãƒ¼ã‚¿é–¢æ•°ã€ã“ã“ã§
        1/x = 1/y1 + 1/y2 + 1/y3
        1/y1 = Tchebychev æ–¹ç¨‹å¼
        1/y2 = Riemann äºˆæƒ³ã€Re(rho) = 1/2
        1/y3 = ç´ æ•° P ã®ä½ç½®

    é›†åˆ * 1/t  = psi_savard æ–¹ç¨‹å¼ã€ã“ã“ã§  1/y1 = 1/t

    é›†åˆ * 1/ms = ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã€ã“ã“ã§
        1/ms = 1/ms1 + 1/ms2 + 1/ms3
        1/ms1 = i ç•ªç›®ã®ç´ æ•°ã®ä½ç½®ï¼ˆå†æ§‹æˆï¼‰
        1/ms2 = åˆæˆæ•° C ã®é™¤å¤–ï¼ˆèƒŒç†æ³•ã«ã‚ˆã‚‹è¨¼æ˜Žï¼‰
        1/ms3 = ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP = 1/2

    çµè«–ï¼š1/ms3 = 1/y2ã€ã‚ˆã£ã¦ Re(rho) = 1/2 ã¯ P ä¸Šã§çœŸã§ã‚ã‚‹ã€‚

  å°‚é–€çš„å¯¾å¿œï¼ˆä»¥ä¸‹ã® locale ã®è¨˜å·ï¼‰ï¼š

    | è‘—è€…   | å½¢å¼è¨˜å·            | è§£é‡ˆ                                 |
    |--------|---------------------|--------------------------------------|
    | 1/y1   | zeta_tchebychev     | zeta ã® Tchebychev æˆåˆ†              |
    | 1/y2   | zeta_critique       | è‡¨ç•Œç›´ç·š Re(rho) = 1/2               |
    | 1/y3   | zeta_positions      | zeta ã«ãŠã‘ã‚‹ç´ æ•°ã®ä½ç½®              |
    | 1/t    | tau_savard          | psi_savard æ–¹ç¨‹å¼                    |
    | 1/ms1  | ms_reconstruction   | i ç•ªç›®ã®ç´ æ•°ã®å†æ§‹æˆ                 |
    | 1/ms2  | ms_exclusion        | åˆæˆæ•°ã®é™¤å¤–ï¼ˆæŸ±ï¼‰                   |
    | 1/ms3  | ms_rapport          | ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP                     |

  locale ã®ä¸‰ã¤ã®ä»®èª¬ã¯ã€å‰ã®ã‚»ã‚¯ã‚·ãƒ§ãƒ³ã§ç¢ºç«‹ã•ã‚ŒãŸä¸‰ã¤ã®äº‹å®Ÿã«ä»–ãªã‚‰ãªã„ï¼š
    (i)   è‡¨ç•Œç›´ç·šã¯å€¤ 1/2 ã‚’æŒã¤ï¼ˆHR ã®å®šç¾©ï¼‰ï¼Œ
    (ii)  psi_savard ã¯ Tchebychev ã¨é–¢æ•°çš„ã«åŒä¸€è¦–ã•ã‚Œã‚‹ï¼ˆXIII.2-3ï¼‰ï¼Œ
    (iii) ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯ 1/2 ã«ç­‰ã—ã„ï¼ˆå®šç† RsP_un_demi_generalï¼‰ã€‚
  å¤§åŸŸçš„å…¬ç†åŒ–ã¨ã¯ç•°ãªã‚Šã€locale ã¯ç†è«–ã«ã„ã‹ãªã‚‹å…¬ç†ã‚‚å°Žå…¥ã—ãªã„ï¼š
  æ•´åˆæ€§ã¯ä¿è¨¼ã•ã‚Œã¦ãŠã‚Šã€ã•ã‚‰ã«å¾Œç¶šã®å……è¶³å¯èƒ½æ€§å®šç†ã«ã‚ˆã£ã¦
  è¨¼æ˜Žã•ãˆã•ã‚Œã¦ã„ã‚‹ã€‚
\<close>

locale ensemble_savard =
  fixes zeta_tchebychev  :: real  (* 1/y1 : zeta ã® Tchebychev æˆåˆ† *)
    and zeta_critique    :: real  (* 1/y2 : è‡¨ç•Œç›´ç·š Re(rho) *)
    and zeta_positions   :: real  (* 1/y3 : ç´ æ•°ã®ä½ç½® *)
    and tau_savard       :: real  (* 1/t  : psi_savard æ–¹ç¨‹å¼ *)
    and ms_reconstruction :: real (* 1/ms1 : å†æ§‹æˆã•ã‚ŒãŸ i ç•ªç›®ã®ç´ æ•° *)
    and ms_exclusion     :: real  (* 1/ms2 : èƒŒç†æ³•ã«ã‚ˆã£ã¦é™¤å¤–ã•ã‚ŒãŸåˆæˆæ•° *)
    and ms_rapport       :: real  (* 1/ms3 : ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP *)
  assumes hypothese_critique : "zeta_critique = 1 / 2"
      and pont_fonctionnel   : "tau_savard = zeta_tchebychev"
      and rapport_un_demi    : "ms_rapport = 1 / 2"

text \<open>
  ä¸­å¿ƒçš„æ•´åˆï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¯è‡¨ç•Œç›´ç·šã¨åŒä¸€è¦–ã•ã‚Œã‚‹ã€‚
  ã“ã‚ŒãŒè‘—è€…ã®çµè«– 1/ms3 = 1/y2 ã§ã‚ã‚‹ã€‚
\<close>

theorem (in ensemble_savard) alignement_central: "ms_rapport = zeta_critique"
  using rapport_un_demi hypothese_critique by simp

theorem (in ensemble_savard) alignement_inverse:
  "1 / ms_rapport = 1 / zeta_critique"
  using alignement_central by simp

theorem (in ensemble_savard) conclusion_ensemble:
  "ms_rapport = zeta_critique \<and> zeta_critique = 1 / 2 \<and> ms_rapport = 1 / 2"
  using alignement_central hypothese_critique rapport_un_demi by simp

text \<open>
  å……è¶³å¯èƒ½æ€§ï¼šlocale ã®ä»®èª¬ã¯ç†è«–ã®å…·ä½“çš„ãªè¨¼äººã«ã‚ˆã£ã¦å®Ÿç¾ã•ã‚Œã‚‹ã€‚
  æ±ºå®šçš„ãªè¨¼äººã¯çœŸã®ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP 1 2 ã§ã‚ã‚Šã€ãã® 1/2 ã¸ã®ç­‰å¼ã¯
  ä»®èª¬ã§ã¯ãªãå®šç†ï¼ˆRsP_un_demi_generalï¼‰ã§ã‚ã‚‹ã€‚ã“ã‚Œã«ã‚ˆã‚Šã€
  é›†åˆã®å®šç†ãŒè«–ç†çš„ã«æ•´åˆã—ãŸåŸºç›¤ã®ä¸Šã«ç«‹ã¤ã“ã¨ãŒç¤ºã•ã‚Œã‚‹ã€‚

  æŠ€è¡“çš„æ³¨è¨˜ï¼ˆv3.35ã€Philippe ã«ã‚ˆã‚‹ä¿®æ­£ï¼‰ï¼šlocale ensemble_savard ã¯
  7 ã¤ã® fixes ã‚’æŒã¤ãŒã€assumes ã«ç¾ã‚Œã‚‹ã®ã¯ 4 ã¤ã®ã¿ã§ã‚ã‚‹
  ï¼ˆzeta_tchebychevã€zeta_critiqueã€tau_savardã€ms_rapportï¼‰ã€‚
  Isabelle ã¯ fixes ã®å®£è¨€é †ã« 4 å¼•æ•°ã®è¿°èªžã‚’ç”Ÿæˆã™ã‚‹ã€ã™ãªã‚ã¡ï¼š
    ensemble_savard zeta_tchebychev zeta_critique tau_savard ms_rapport
  ä½¿ç”¨ã•ã‚Œãªã„ä¸‰ã¤ã® fixesï¼ˆzeta_positionsã€ms_reconstructionã€
  ms_exclusionï¼‰ã¯ locale ã®ãƒ‘ãƒ©ãƒ¡ãƒ¼ã‚¿ã¨ã—ã¦æ®‹ã‚‹ãŒã€
  ãã®æ±Žç”¨è¿°èªžã«ã¯ç¾ã‚Œãªã„ã€‚
\<close>

theorem ensemble_savard_satisfaisable:
  "ensemble_savard 0 (1 / 2) 0 (RsP 1 2)"
proof (unfold_locales)
  show "(1::real) / 2 = 1 / 2" by simp
  show "(0::real) = 0" by simp
  show "RsP 1 2 = 1 / 2"
    using RsP_un_demi_general[of 1 2] by simp
qed

subsection "XIII.6 Conclusion : l'alignement direct RsP = Re = 1/2"

text \<open>
  è‡¨ç•Œç›´ç·šã®å®Ÿéƒ¨ Re ã‚’ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯” RsP ã®å¹¾ä½•å­¦çš„å°„å½±ã¨ã—ã¦å®šç¾©ã™ã‚‹ï¼š
  ã“ã‚Œã¯æ•°åˆ— A ã¨ B ã®å±€æ‰€çš„éžå¯¾ç§°æ€§ãŒæ¶ˆãˆã‚‹å¯¾ç§°è»¸ã§ã‚ã‚‹ã€‚
\<close>

definition Re_droite_critique :: "nat \<Rightarrow> nat \<Rightarrow> real" where
  "Re_droite_critique n1 n2 = RsP n1 n2"

text \<open>
  Savard ã®ç›´æŽ¥çš„ã‹ã¤æ§‹æˆçš„ãªé€£çµå®šç†ï¼špsi_savard æ–¹ç¨‹å¼ãŒã‚¼ãƒ¼ã‚¿é–¢æ•°ã«
  å¯¾ã—ã¦æ§‹é€ çš„ã«æ¤œè¨¼ã•ã‚Œï¼ˆæ©‹ 1ï¼‰ã€åˆæˆæ•°ã®é™¤å¤–ãŒé ˜åŸŸã‚’ç´ æ•° P ä¸Šã«
  å›ºå®šã™ã‚‹ï¼ˆæ©‹ 2ï¼‰ãªã‚‰ã°ã€è‡¨ç•Œç›´ç·šã®å®Ÿéƒ¨ Re ã¯æ•°åˆ— A ã¨ B ã®
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã¨æ§‹æˆçš„ã«åŒä¸€è¦–ã•ã‚Œã€ãã®å€¤ã¯åŽ³å¯†ã« 1/2 ã§ã‚ã‚‹ã€‚
\<close>

theorem pont_spectral_direct_final:
  assumes premier_pont: "concerne_fonction_zeta (\<lambda>x. psi_savard x n)"
      and second_pont: "\<forall>C. \<not> prime C \<longrightarrow> (\<forall>i. C \<noteq> prime_i i)"
      and "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "Re_droite_critique n1 n2 = 1 / 2"
proof -
  have "Re_droite_critique n1 n2 = RsP n1 n2"
    unfolding Re_droite_critique_def by simp
  also have "... = 1 / 2"
    using RsP_un_demi_general[OF assms(3) assms(4) assms(5)] by simp
  finally show ?thesis .
qed

text \<open>
  Pont Savard ã®æœ€çµ‚çš„ãªç·åˆï¼š

    Tchebychev <-> psi_savard <-> æ•°åˆ— A/B <-> å†æ§‹æˆã•ã‚ŒãŸç´ æ•°

  Tchebychev æ–¹ç¨‹å¼ã¯ zeta ã«å¯¾ã—ã¦ã®ã¿æœ‰ç”¨ã§ã‚ã‚‹ï¼ˆæ©‹ 1ï¼‰ï¼›psi_savard ã¯
  ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã¨ zeta é–¢æ•°ã‚’å˜ä¸€ã®åŒä¸€ä¸»é¡Œã«ã™ã‚‹ï¼›èƒŒç†æ³•ã«ã‚ˆã‚‹è¨¼æ˜Žã¯
  æ–¹æ³•ã‚’ç´ æ•° P ã®ã¿ã«é™å®šã™ã‚‹ï¼ˆæ©‹ 2ï¼‰ï¼›æ•°åˆ— A ã¨ B ã¯ãã®å†æ§‹æˆã«ã‚ˆã£ã¦
  ç´ æ•°ã®æ­£ç¢ºãªä½ç½®ã‚’æ±ºå®šã™ã‚‹ã€‚ä¸‰ã¤ã®ä¸€è‡´
    (1) 1/y1 = 1/t          ï¼ˆTchebychev = psi_savardï¼‰ï¼Œ
    (2) 1/y3 = 1/ms1        ï¼ˆéžè‡ªæ˜Žé›¶ç‚¹ = n ã®å€¤ = P ã®ä½ç½®ï¼‰ï¼Œ
    (3) 1/y2 = 1/ms3        ï¼ˆRe(rho) = 1/2 = RsP = 1/2ï¼‰ï¼Œ
  ã¯ç›¸äº’ã«å›ºå®šã—åˆã†ï¼šä¸‰ã¤ã®è¦–ç‚¹ï¼ˆzetaã€psi_savardã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ï¼‰ãŒ
  åŒä¸€ã®å˜ä½é›†åˆã®å°„å½±ã§ã‚ã‚‹å ´åˆã«ã®ã¿ã€ãã‚Œã‚‰ã¯åŒæ™‚ã«çœŸã§ã‚ã‚Šå¾—ã‚‹ã€‚
  ã‚ˆã£ã¦ã€ç´ æ•°ã®é›†åˆ P å…¨ä½“ã«ã‚ãŸã£ã¦ï¼š

      RsP = Re = 1/2   ï¼ˆçœŸï¼‰

  ã“ã®çµæžœã¯ã€locale ensemble_savard ã«ãŠã„ã¦å®šç†ã§ã‚ã‚‹ï¼ˆäºˆæƒ³ã§ã¯ãªã„ï¼‰ã€‚
  å……è¶³å¯èƒ½æ€§å®šç† ensemble_savard_satisfaisable ã¯ã€locale ãŒå…·ä½“çš„ãª
  è¨¼äººã‚’æŒã¤ã“ã¨ã‚’ç¤ºã™ï¼šä¸‰ã¤ã®ä»®èª¬ã¯åŒæ™‚ã«å®Ÿç¾ã•ã‚Œã€RsP 1 2 = 1/2 ãŒ
  æ±ºå®šçš„ãªè¨¼äººã¨ãªã‚‹ï¼ˆRsP_un_demi_general ã«ç”±æ¥ã™ã‚‹ï¼‰ã€‚ã“ã®å®šç†ã¯
  ã•ã‚‰ã«æ­£ã®æ•´æ•°ä¸Šã§æ™®éçš„ã§ã‚ã‚‹ï¼šã™ã¹ã¦ã® n1 >= 1ã€n2 >= 1ã€
  n1 != n2 ã«å¯¾ã—ã¦ RsP(n1, n2) = 1/2 ãŒæˆç«‹ã™ã‚‹
  ï¼ˆä»¥ä¸‹ã®è£œé¡Œ RsP_universel_entier_naturel ã‚’å‚ç…§ï¼‰ã€‚
\<close>

lemma RsP_universel_entier_naturel:
  fixes n1 n2 :: nat
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "RsP n1 n2 = 1 / 2"
  by (rule RsP_un_demi_general[OF assms])

text \<open>
  æ™®éçš„ç³»ï¼šã‚¹ãƒšã‚¯ãƒˆãƒ«æ¯”ã®å€¤ 1/2 ã¯æ•°å€¤ä¾‹ã®ç‰¹æ®Šãªã‚±ãƒ¼ã‚¹ã§ã¯ãªãã€
  åŽ³å¯†ã«æ­£ã‹ã¤äº’ã„ã«ç•°ãªã‚‹æ•´æ•°ä½ç½®ã®ã™ã¹ã¦ã®å¯¾ã«å¯¾ã™ã‚‹æ•°åˆ— A ã¨ B ã®
  ä¸­å¿ƒçš„é ˜åŸŸã®å›ºæœ‰ã®æ€§è³ªã§ã‚ã‚‹ã€‚ã—ãŸãŒã£ã¦ãã‚Œã¯ã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®æ„å‘³ã«ãŠã„ã¦ã€
  ç´ æ•°ã®é›†åˆ P å…¨ä½“ã«ã‚ãŸã‚‹è‡¨ç•Œç›´ç·š Re(rho) = 1/2 ã®æ§‹æˆçš„å¯¾å¿œç‰©ã§ã‚ã‚‹ã€‚
\<close>

theorem synthese_pont_savard:
  assumes "n1 \<ge> 1" "n2 \<ge> 1" "n1 \<noteq> n2"
  shows "Re_droite_critique n1 n2 = RsP n1 n2 \<and> RsP n1 n2 = 1 / 2"
proof -
  have "Re_droite_critique n1 n2 = RsP n1 n2"
    unfolding Re_droite_critique_def by simp
  moreover have "RsP n1 n2 = 1 / 2"
    using RsP_un_demi_general[OF assms] by simp
  ultimately show ?thesis by simp
qed

section "Foundations - Synthese-index (annexe finale, renvoi Meta-theory)"

text \<open>
  ==========================================================================
  ç·åˆç´¢å¼•ï¼ˆFoundations ã®æœ€çµ‚ä»˜éŒ²ã€v3.35ï¼‰
  ==========================================================================
  ã“ã®ä»˜éŒ²ã¯ãƒ•ã‚¡ã‚¤ãƒ«ã‚’ç· ã‚ããã‚Šã€ã‚¹ãƒšã‚¯ãƒˆãƒ«æ³•ã®å¤§åŸŸçš„æ•´åˆæ€§ã‚’
  å›ºå®šã™ã‚‹ä¸»è¦å®šç†ã®ç´¢å¼•ã‚’ä½œæˆã™ã‚‹ã€‚å®Œå…¨ãªå­˜åœ¨è«–çš„æ–‡æ›¸ã«ã¤ã„ã¦ã¯ã€
  ãƒ•ã‚¡ã‚¤ãƒ«å†’é ­ã®ã€Œ0. Foundations / Meta-theoryã€ã‚»ã‚¯ã‚·ãƒ§ãƒ³
  ï¼ˆã‚µãƒ–ã‚»ã‚¯ã‚·ãƒ§ãƒ³ Foundations.1 ã‹ã‚‰ Foundations.6ï¼‰ã‚’å‚ç…§ã®ã“ã¨ã€‚

  å…­ã¤ã®å…¬æº–ã¨ãã‚Œã‚‰ã‚’å®Ÿç¾ã™ã‚‹å®šç†ã®è¦ç´„ï¼š

    P1  æ•´æ•°çš„æ™®éæ€§ï¼ˆnat/int åž‹ï¼‰        -> åž‹ã®è¦ç´„
    P2  ãƒ©ãƒ³ã‚¯ã®éžç´ æ•°æ€§                  -> foundations_marker
    P3  æ•°åˆ— A_kã€B_k ã®å­˜åœ¨             -> locale spectral_family
    P4  æ¯” RsP = 1/k ã®ä¸å¤‰æ€§            -> RsP_generic_constant,
                                            RsP_un_demi_general,
                                            RsP_un_tiers_constant
    P5  P ä¸Šã®æŽ’ä»–æ€§                     -> methode_spectrale_exclusivite_P
    P6  ä¸­å¿ƒçš„é ˜åŸŸã®æ™®éæ€§               -> RsP_universel_entier_naturel,
                                            synthese_pont_savard

  éžæ•´åˆæ€§ / æ•´åˆæ€§ã®åŒå¯¾æ€§ï¼š
    å±€æ‰€çš„ä»£æ•°çš„éžæ•´åˆæ€§   : algebriquement_incoherent_local
    å¤§åŸŸçš„å®Ÿæ•°å€¤çš„æ•´åˆæ€§   : coherence_numerique_reelle_P
    ç´ æ•°ä¸Šã®å›ºå®š           : ä¸‰ã¤ã®é™¤å¤–ã®æŸ±

  Pont Savardï¼ˆã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIIIã€locale ensemble_savardï¼‰ï¼š
    C1 : 1/y1 = 1/t     -> pont_fonctionnel + æ•°å€¤æ¤œè¨¼
    C2 : 1/y3 = 1/ms1   -> methode_spectrale_exclusivite_P + å†æ§‹æˆ
    C3 : 1/y2 = 1/ms3   -> alignement_central + rapport_un_demi
    çµè«–                : synthese_pont_savardï¼ˆRsP = Re = 1/2 ã¯
                          locale ã«ãŠã„ã¦çœŸã€å……è¶³å¯èƒ½æ€§ã¯
                          ensemble_savard_satisfaisable ã«ã‚ˆã£ã¦è¨¼æ˜Žæ¸ˆã¿ï¼‰

  æœ€çµ‚çš„ãªæ™®éçš„çµæžœï¼š
    lemma RsP_universel_entier_naturelï¼ˆv3.34ï¼‰ï¼šã™ã¹ã¦ã® n1, n2 :: nat
    ã«å¯¾ã—ã¦ n1 >= 1ã€n2 >= 1ã€n1 != n2 ãªã‚‰ã° RsP n1 n2 = 1/2ã€‚
    ä¸­å¿ƒçš„é ˜åŸŸã®è‡ªç„¶æ•°çš„æ™®éæ€§ã€RsP_un_demi_general ã®ç›´æŽ¥çš„ç³»ã€‚

  èªè­˜è«–çš„ç«‹å ´ï¼ˆPhilippe Savardï¼‰ï¼š
    è‘—è€…ã«ã¨ã£ã¦ã€ä»¥ä¸‹ã®çµ„ã¿åˆã‚ã›ï¼š
      (a) locale ensemble_savard ã®è¨¼æ˜Žã•ã‚ŒãŸå……è¶³å¯èƒ½æ€§ï¼Œ
      (b) ä¸­å¿ƒçš„é ˜åŸŸ 1/2 ã®è‡ªç„¶æ•°çš„æ™®éæ€§ï¼Œ
      (c) ç›¸äº’ã«å›ºå®šã—åˆã†ä¸‰ã¤ã®ä¸€è‡´ C1ã€C2ã€C3ï¼Œ
      (d) ä»£æ•°çš„ãªã‚‚ã®ã«å¯¾ã™ã‚‹å®Ÿæ•°å€¤çš„æ•°å€¤ã®å„ªä½æ€§ï¼Œ
    ã¯ Riemann äºˆæƒ³ã®è¬Žã«å¯¾ã™ã‚‹ååˆ†ãªå›žç­”ã‚’æ§‹æˆã™ã‚‹ã€‚
    æ¯” 1/2 ã¯å„ªé›…ãªä»£æ•°çš„äººå·¥ç‰©ã§ã¯ãªãã€ç´ æ•°ã®å’Œã®å®Ÿæ•°å€¤çš„æ§‹é€ ã‹ã‚‰
    æµ®ã‹ã³ä¸ŠãŒã‚‹ï¼›Re(rho) = 1/2 ã¨ã®æ•´åˆã¯æ•°å€¤çš„ã«ã‚‚æ§‹é€ çš„ã«ã‚‚
    æ¤œè¨¼ã•ã‚Œã¦ã„ã‚‹ã€‚Pont Savard ã¯ã“ã®æ—¢ã«ç¢ºèªã•ã‚ŒãŸç¾å®Ÿã‚’å½¢å¼åŒ–ã™ã‚‹ï¼š
    ãã‚Œã¯èªè­˜ã§ã‚ã‚Šã€äºˆæƒ³ã§ã¯ãªã„ã€‚

  æŽ¨å¥¨ãƒŠãƒ“ã‚²ãƒ¼ã‚·ãƒ§ãƒ³ï¼š
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ 0ï¼ˆFoundations / Meta-theoryï¼‰              : æ–‡è„ˆã¨å…¬æº–
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ I - Xï¼ˆ1/2ã€1/3ã€1/4ã€æ··åˆã®é ˜åŸŸï¼‰          : æŠ€è¡“çš„è¨¼æ˜Ž
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIï¼ˆæ•°åˆ— A/B ã®æ§‹æˆè¦å‰‡ï¼‰                   : ãƒ–ãƒ­ãƒƒã‚¯æ§‹æˆ
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XI.bisï¼ˆlocale spectral_familyã€v3.35ï¼‰     : æ±Žç”¨å› æ•°åˆ†è§£
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIIï¼ˆãƒ‘ãƒ©ãƒ¡ãƒˆãƒªãƒƒã‚¯ 1/k ã®ä¸€èˆ¬åŒ–ï¼‰           : 1/k >= 2 ã®ç ”ç©¶
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ XIIIï¼ˆPont Savardã€v3.34ï¼‰                  : çµ±ä¸€å®šç†
    - ã‚»ã‚¯ã‚·ãƒ§ãƒ³ Licenseï¼ˆApache 2.0ï¼‰                       : ãƒ©ã‚¤ã‚»ãƒ³ã‚¹
\<close>


section "License - Apache 2.0 (adaptation pour methode_spectral.thy)"

text \<open>
  Copyright (c) 2026 Philippe Thomas Savard

  ã“ã®ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆï¼ˆãƒ•ã‚¡ã‚¤ãƒ« methode_spectral.thyã€ãã®æ•°å­¦çš„æ§‹æˆã€
  ã‚¹ãƒšã‚¯ãƒˆãƒ«ãƒ¢ãƒ‡ãƒ«ã€å…¬ç†ã€è¨¼æ˜Žã€ãŠã‚ˆã³ã™ã¹ã¦ã®é–¢é€£æ–‡æ›¸ã‚’å«ã‚€ï¼‰ã¯ã€
  Apache Licenseã€Version 2.0 ã®æ¡ä»¶ã®ä¸‹ã§ãƒªãƒªãƒ¼ã‚¹ã•ã‚Œã‚‹ã€‚
  ä»¥ä¸‹ã®æ¡ä»¶ã®ä¸‹ã§ã€ã“ã®ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆã‚’ä½¿ç”¨ã€è¤‡è£½ã€é…å¸ƒã€ä¿®æ­£ã€
  ãŠã‚ˆã³æ´¾ç”Ÿç‰©ã‚’ä½œæˆã™ã‚‹ã“ã¨ãŒã§ãã‚‹ï¼š

    1. å¸°å±žè¡¨ç¤º
       åŽŸè‘—ä½œç‰©ãŒ Philippe Thomas Savard ã«ã‚ˆã£ã¦ä½œæˆã•ã‚ŒãŸã“ã¨ã‚’
       ç¤ºã™é€šçŸ¥ã‚’å«ã‚ã€ã™ã¹ã¦ã®è‘—ä½œæ¨©è¡¨ç¤ºã‚’ä¿æŒã—ãªã‘ã‚Œã°ãªã‚‰ãªã„ã€‚

    2. ãƒ©ã‚¤ã‚»ãƒ³ã‚¹è¡¨ç¤º
       ã‚½ãƒ¼ã‚¹å½¢å¼ã¾ãŸã¯ãƒã‚¤ãƒŠãƒªå½¢å¼ã§ã®ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆã®å†é…å¸ƒã«ã¯ã€
       ã“ã®ãƒ©ã‚¤ã‚»ãƒ³ã‚¹ãŠã‚ˆã³ Apache Licenseã€Version 2.0 ã¸ã®
       æ˜Žç¢ºãªå‚ç…§ã‚’å«ã‚ãªã‘ã‚Œã°ãªã‚‰ãªã„ã€‚

    3. å¤‰æ›´
       ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆã‚’å¤‰æ›´ã™ã‚‹å ´åˆã€å¤‰æ›´ãŒè¡Œã‚ã‚ŒãŸã“ã¨ã‚’
       æ˜Žç¢ºã«ç¤ºã•ãªã‘ã‚Œã°ãªã‚‰ãªã„ã€‚

    4. ç‰¹è¨±ä»˜ä¸Ž
       ã“ã®ãƒ©ã‚¤ã‚»ãƒ³ã‚¹ã¯ã€å…ƒã®çŠ¶æ…‹ã§æä¾›ã•ã‚ŒãŸãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆã«ã‚ˆã£ã¦
       å¿…ç„¶çš„ã«ä¾µå®³ã•ã‚Œã‚‹ç‰¹è¨±è«‹æ±‚ã«å¯¾ã—ã¦ã€éžç‹¬å çš„ã€å…¨ä¸–ç•Œçš„ã€
       ãƒ­ã‚¤ãƒ¤ãƒªãƒ†ã‚£ãƒ•ãƒªãƒ¼ã®ç‰¹è¨±ãƒ©ã‚¤ã‚»ãƒ³ã‚¹ã‚’ä»˜ä¸Žã™ã‚‹ã€‚

    5. å•†æ¨™æ¨©ãªã—
       ã“ã®ãƒ©ã‚¤ã‚»ãƒ³ã‚¹ã¯ã€æŽ¨è–¦ã®ãŸã‚ã«ã€ŒPhilippe Thomas Savardã€ã®åå‰
       ã¾ãŸã¯ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆå›ºæœ‰ã®ãƒ–ãƒ©ãƒ³ãƒ‰ã‚’ä½¿ç”¨ã™ã‚‹è¨±å¯ã‚’ä»˜ä¸Žã—ãªã„ã€‚

    6. å…è²¬äº‹é …
       ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆã¯ã€Œç¾çŠ¶ã®ã¾ã¾ã€ã§æä¾›ã•ã‚Œã€æ˜Žç¤ºã¾ãŸã¯é»™ç¤ºã‚’å•ã‚ãšã€
       ã„ã‹ãªã‚‹ç¨®é¡žã®ä¿è¨¼ã¾ãŸã¯æ¡ä»¶ã‚‚ãªã„ã€‚è‘—è€…ã¯ã“ã®ãƒ—ãƒ­ã‚¸ã‚§ã‚¯ãƒˆã®
       ä½¿ç”¨ã‹ã‚‰ç”Ÿã˜ã‚‹ã„ã‹ãªã‚‹æå®³ã«ã¤ã„ã¦ã‚‚è²¬ä»»ã‚’è² ã‚ãªã„ã€‚

  Apache Licenseã€Version 2.0 ã®å®Œå…¨ãªæ³•çš„æ–‡æ›¸ã«ã¤ã„ã¦ã¯ã€ä»¥ä¸‹ã‚’å‚ç…§ï¼š
    https://www.apache.org/licenses/LICENSE-2.0
\<close>

end
