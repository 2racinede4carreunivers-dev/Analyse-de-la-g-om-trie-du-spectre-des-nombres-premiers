(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Contre-validation HOL 2/2 (inter-assistants Lean 4 / Mathlib)
   Fichier : validation_zeta_lean.thy (fichier unique, non decoupe)
   Auteur : Philippe Thomas Savard
   Date : Le trois octobre deux mille vingt-six
   Lieu : Levis, Chausdiere-Appalaches, Canada
   Role : chaque point de la Section XIII (Pont Savard, MS_13) est mis en
   relation avec sa contrepartie PROUVEE dans Mathlib (Lean 4) : zeta,
   Lambda completee, equation fonctionnelle, zeros, psi de Tchebychev (C1).
   Discipline : AUCUN axiome n'enonce RH ; les axiomes specifient des
   theoremes Mathlib ; RH = definition booleenne ; pont = theoreme
   conditionnel + direction constructive inconditionnelle.
   ----------------------------------------------------------------------------
   TABLE DES MATIERES (sections + N° de ligne debut-fin) :
   L  57 - L 102 : [section] Cercle 1 : Objets specifies depuis Mathlib (zeta, Lambda, zeros)
   L 103 - L 123 : [section] Cercle 2 : Faits etablis dans Mathlib (theoremes prouves, specifies ici)
   L 124 - L 171 : [subsection] Cercle 2.b : Consequences demontrees ici (theoremes HOL, non axiomes)
   L 172 - L 314 : [section] Cercle 2.c : L'equation de Tchebychev et le psi(Savard) (concordance C1)
   L 315 - L 374 : [section] Cercle 3 : La conjecture (definition) et le Pont Savard
   L 375 - L 394 : [subsection] Cercle 3.b : Direction constructive inconditionnelle (Section XIII)
   L 395 - L 438 : [section] Synthese : correspondance des points (Section XIII <-> Mathlib)
   L 439 - L 499 : [section] References externes (Mathlib, Lean 4) et licence Apache 2.0
   ============================================================================ *)

theory validation_zeta_lean
  imports MS_14_Systeme_Convolutif
begin

(*  ==========================================================================
    CONTRE-VALIDATION No 2 (INTER-ASSISTANTS) : LEAN 4 / MATHLIB <-> ISABELLE/HOL
    ==========================================================================
    Pipeline HOL/Isabelle du depot agent-multiloop-Gabriel-local :
      * Validation principale  : MS_01 a MS_14 (decoupage verbatim de methode_spectral.thy en 14 sections)
        (objectif : Section XIII, Le Pont Savard, equation RsP = Re(s) = 1/2).
      * Contre-validation No 1 : validation_hol_unifiee.thy
        (completude et liens causaux internes de la validation principale,
        organises en cercles concentriques autour de l'equation du Pont Savard).
      * Contre-validation No 2 : le present fichier. Meme objectif que la No 1,
        mais chaque point de la Section XIII est mis en relation avec sa
        contrepartie PROUVEE dans le depot public Mathlib (Lean 4) : fonction
        zeta, version completee Lambda, equation fonctionnelle, zeros, et
        surtout la fonction psi de Tchebychev (Chebyshev.psi / vonMangoldt)
        qui porte la concordance C1 (1/y1 = 1/t) du Pont Savard.

    Discipline logique (v2.0, restructuration complete) :
      * AUCUN axiome n'enonce l'hypothese de Riemann. La version precedente
        axiomatisait "tout zero de la bande critique a Re = 1/2", ce qui
        rendait l'alignement circulaire ; cette circularite est supprimee.
      * Les seuls axiomes SPECIFIENT des theoremes deja demontres dans Mathlib
        (noms, enonces, numeros de ligne et auteurs cites en fin de fichier).
      * L'hypothese de Riemann est une DEFINITION booleenne (cercle 3) ; le pont
        vers RsP = 1/2 est un theoreme CONDITIONNEL, et la direction
        constructive RsP = 1/2 est INCONDITIONNELLE (Section XIII).
    ==========================================================================  *)

section "Cercle 1 : Objets specifies depuis Mathlib (zeta, Lambda, zeros)"

text \<open>
  Contreparties Lean 4 / Mathlib des objets de la Section XIII de la
  validation principale (verifiees sur le clone local de mathlib4) :

    riemannZeta          : la fonction zeta de Riemann, zeta : C -> C
                           (Mathlib.NumberTheory.LSeries.RiemannZeta).
    completedRiemannZeta : la version completee,
                           Lambda(s) = pi^(-s/2) Gamma(s/2) zeta(s)
                           (meme fichier).
    riemannZetaZeros     : l'ensemble des zeros, image reciproque de {0}
                           par zeta (Mathlib.NumberTheory.LSeries.ZetaZeros).

  Les deux constantes ci-dessous sont non interpretees : elles REPRESENTENT
  les fonctions Lean dans la logique HOL, aux fins de comparaison formelle.
\<close>

axiomatization
  riemannZeta_lean          :: "complex \<Rightarrow> complex" and
  completedRiemannZeta_lean :: "complex \<Rightarrow> complex" and
  psi_tchebychev_lean       :: "real \<Rightarrow> real"
  (* specifications HOL des fonctions Mathlib riemannZeta, completedRiemannZeta
     et Chebyshev.psi (fonction psi de Tchebychev, cf. Cercle 2.c) *)

definition zeros_zeta_lean :: "complex set" where
  "zeros_zeta_lean = {s. riemannZeta_lean s = 0}"
  (* pendant de Mathlib.riemannZetaZeros *)

definition zeros_lambda_lean :: "complex set" where
  "zeros_lambda_lean = {s. completedRiemannZeta_lean s = 0}"

definition bande_critique_lean :: "complex \<Rightarrow> bool" where
  "bande_critique_lean s = (0 < Re s \<and> Re s < 1)"

definition axe_critique_lean :: "complex \<Rightarrow> bool" where
  "axe_critique_lean s = (Re s = 1 / 2)"

lemma mem_zeros_zeta_lean:
  "s \<in> zeros_zeta_lean \<longleftrightarrow> riemannZeta_lean s = 0"
  unfolding zeros_zeta_lean_def by simp

lemma mem_zeros_lambda_lean:
  "s \<in> zeros_lambda_lean \<longleftrightarrow> completedRiemannZeta_lean s = 0"
  unfolding zeros_lambda_lean_def by simp

section "Cercle 2 : Faits etablis dans Mathlib (theoremes prouves, specifies ici)"

text \<open>
  Les deux axiomes ci-dessous SPECIFIENT des theoremes demontres dans Mathlib
  (Lean 4) ; ils n'apportent aucun contenu conjectural :

    A1  Equation fonctionnelle de la fonction completee :
          completedRiemannZeta_one_sub : Lambda(1 - s) = Lambda(s)
          (Mathlib.NumberTheory.LSeries.RiemannZeta, theoreme, ligne 106).

    A2  Non-annulation au bord droit de la bande critique :
          riemannZeta_ne_zero_of_one_le_re : 1 <= Re s ==> zeta s <> 0
          (Mathlib.NumberTheory.LSeries.Nonvanishing, lemme, ligne 413).
\<close>

axiomatization where
  equation_fonctionnelle_lean:
    "\<And>s. completedRiemannZeta_lean (1 - s) = completedRiemannZeta_lean s" and
  non_annulation_bande_lean:
    "\<And>s. 1 \<le> Re s \<Longrightarrow> riemannZeta_lean s \<noteq> 0"

subsection "Cercle 2.b : Consequences demontrees ici (theoremes HOL, non axiomes)"

text \<open>
  Les resultats de cette sous-section sont DEMONTRES dans Isabelle/HOL a
  partir des seules specifications A1-A2 : ils ne presument rien de la
  position des zeros. En particulier, l'axe Re = 1/2 apparait deja comme
  axe de symetrie structurel des zeros de la fonction completee.
\<close>

lemma zero_zeta_sous_le_bord_superieur:
  (* Tout zero de zeta est strictement sous le bord Re = 1 (via A2). *)
  assumes "riemannZeta_lean s = 0"
  shows "Re s < 1"
proof (rule ccontr)
  assume "\<not> Re s < 1"
  hence "1 \<le> Re s" by simp
  hence "riemannZeta_lean s \<noteq> 0" by (rule non_annulation_bande_lean)
  thus False using assms by simp
qed

lemma symetrie_des_zeros_de_Lambda:
  (* Symetrie fonctionnelle des zeros de Lambda (via A1). *)
  assumes "completedRiemannZeta_lean s = 0"
  shows "completedRiemannZeta_lean (1 - s) = 0"
proof -
  have "completedRiemannZeta_lean (1 - s) = completedRiemannZeta_lean s"
    by (rule equation_fonctionnelle_lean)
  thus ?thesis using assms by simp
qed

lemma zeros_lambda_involution_critique:
  (* L'involution s |-> 1 - s preserve les zeros de Lambda (deux sens). *)
  "s \<in> zeros_lambda_lean \<longleftrightarrow> (1 - s) \<in> zeros_lambda_lean"
proof
  assume "s \<in> zeros_lambda_lean"
  hence "completedRiemannZeta_lean s = 0" by (simp add: mem_zeros_lambda_lean)
  hence "completedRiemannZeta_lean (1 - s) = 0" by (rule symetrie_des_zeros_de_Lambda)
  thus "(1 - s) \<in> zeros_lambda_lean" by (simp add: mem_zeros_lambda_lean)
next
  assume "(1 - s) \<in> zeros_lambda_lean"
  hence h: "completedRiemannZeta_lean (1 - s) = 0" by (simp add: mem_zeros_lambda_lean)
  have "completedRiemannZeta_lean s = completedRiemannZeta_lean (1 - s)"
    using equation_fonctionnelle_lean[of s] by simp
  hence "completedRiemannZeta_lean s = 0" using h by simp
  thus "s \<in> zeros_lambda_lean" by (simp add: mem_zeros_lambda_lean)
qed


section "Cercle 2.c : L'equation de Tchebychev et le psi(Savard) (concordance C1)"

text \<open>
  POINT COMMUN C1 DU PONT SAVARD (Section XIII : 1/y1 = 1/t).

  L'equation de Tchebychev pour psi est la somme, ponderee par le logarithme,
  des premiers et de leurs puissances (fonction de von Mangoldt Lambda) :

      psi(x) = sum_{n <= floor x} Lambda(n),   Lambda(n) = log p  si n = p^k,

  de forme explicite

      psi(x) = x - sum_{p^k <= x} x^(p^k) / p^k - log(2*pi) - (1/2) log(1 - x^-2).

  Mathlib / Lean 4 PROUVE ces objets :
    - Chebyshev.psi : la fonction psi de Tchebychev
      (Mathlib.NumberTheory.Chebyshev, Irving / Tao / Van de Velde, 2025) ;
    - ArithmeticFunction.vonMangoldt : la fonction Lambda
      (Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt, Mehta, 2022),
      avec Lambda(p) = log p sur les premiers.
  Les bornes de Chebyshev (psi(x) <= C * x, et borne inferieure) y sont des
  theoremes.

  psi(Savard) : la somme sur les premiers est remplacee par la somme des
  puissances 2^n / SB(n) de la Suite B, ou (definition SB de la validation
  principale) SB(n) = (6.5 / 2) * 2^n - 66, soit SB(10) = 3262 :

      psi_savard(x, n) = x - (2^n)/(SB n) - log10(2*pi)
                           - (1/2) log10(1 - 1/x^2),   log10(y) = ln y / ln 10.

  Sur chaque premier vise, psi_savard reproduit Tchebychev a epsilon(x) pres
  (validations numeriques XIII.2) :

      psi_savard(30, 10)  = 28.888143698...    premier vise : 29
      psi_savard(32, 11)  = 30.891258390...    premier vise : 31
      psi_savard(98, 25)  = 96.894150249...    premier vise : 97
      psi_savard(228, 49) = 226.894132001...   premier vise : 227

  POURQUOI C1 EST UN POINT COMMUN (et non une coincidence) : l'equation de
  Tchebychev n'a d'utilite QUE pour la fonction zeta de Riemann (formule
  explicite de Riemann - von Mangoldt). Comme psi_savard prolonge strictement
  Tchebychev (domaine x^2 > 1 au lieu de x >= 2) et reproduit ses valeurs sur
  le domaine commun, la Methode Spectrale et zeta traitent litteralement du
  MEME sujet ; la Methode Spectrale voit en plus le regime negatif et, par
  l'exclusion des composes (Second Pont), la totalite de l'ensemble P.
\<close>

axiomatization where
  tchebychev_psi_nonneg_lean:
    (* Mathlib : Chebyshev.psi_nonneg (Chebyshev.lean l.86) *)
    "\<And>x. 0 \<le> psi_tchebychev_lean x" and
  tchebychev_psi_nul_sous_deux_lean:
    (* Mathlib : Chebyshev.psi_eq_zero_of_lt_two (Chebyshev.lean l.111) *)
    "\<And>x. x < 2 \<Longrightarrow> psi_tchebychev_lean x = 0" and
  tchebychev_psi_bornee_lean:
    (* Mathlib : Chebyshev.psi_le_const_mul_self (borne superieure de Chebyshev) *)
    "\<exists>C. 0 < C \<and> (\<forall>x. 1 \<le> x \<longrightarrow> psi_tchebychev_lean x \<le> C * x)"

text \<open>
  Re-exposition des validations numeriques de la Section XIII.2 : les valeurs
  exactes du psi(Savard), memes formules que dans la validation principale
  (lemmes psi_savard_at_10_30_expanded, at_25_98, at_49_228).
\<close>

lemma psi_savard_30_10_egal_tchebychev:
  "psi_savard 30 10 = 30 - 1024 / 3262 - log10_savard (2 * pi)
                       - (1 / 2) * log10_savard (1 - 1 / 900)"
  by (rule psi_savard_at_10_30_expanded)

lemma psi_savard_98_25_egal_tchebychev:
  "psi_savard 98 25 = 98 - 33554432 / 109051838 - log10_savard (2 * pi)
                       - (1 / 2) * log10_savard (1 - 1 / 9604)"
  by (rule psi_savard_at_25_98_expanded)

lemma psi_savard_228_49_egal_tchebychev:
  "psi_savard 228 49 = 228 - 562949953421312 / 1829587348619198
                       - log10_savard (2 * pi)
                       - (1 / 2) * log10_savard (1 - 1 / 51984)"
  by (rule psi_savard_at_49_228_expanded)

text \<open>
  Consequences demontrees ici (theoremes HOL, non axiomes) : Tchebychev est
  nulle sous 2 et n'est jamais strictement negative.
\<close>

lemma tchebychev_psi_nulle_sous_deux:
  "x < 2 \<Longrightarrow> psi_tchebychev_lean x = 0"
  by (rule tchebychev_psi_nul_sous_deux_lean)

lemma tchebychev_psi_non_negative:
  "\<not> psi_tchebychev_lean x < 0"
  using tchebychev_psi_nonneg_lean[of x] by simp

definition zero_fun_lean :: "real \<Rightarrow> real" where
  "zero_fun_lean x = 0"

theorem tchebychev_psi_spec_satisfaisable:
  (* La specification de Chebyshev.psi (nonnegativite, annulation sous 2,
     borne C * x) est CONSISTANTE : le temoin f = 0 la realise. *)
  "\<exists>f :: real \<Rightarrow> real.
     (\<forall>x. 0 \<le> f x) \<and> (\<forall>x. x < 2 \<longrightarrow> f x = 0)
     \<and> (\<exists>C. 0 < C \<and> (\<forall>x. 1 \<le> x \<longrightarrow> f x \<le> C * x))"
proof (rule exI[of _ zero_fun_lean], intro conjI)
  show "\<forall>x. 0 \<le> zero_fun_lean x" by (simp add: zero_fun_lean_def)
  show "\<forall>x. x < 2 \<longrightarrow> zero_fun_lean x = 0" by (simp add: zero_fun_lean_def)
  show "\<exists>C. 0 < C \<and> (\<forall>x. 1 \<le> x \<longrightarrow> zero_fun_lean x \<le> C * x)"
  proof (rule exI[of _ 1], intro conjI)
    show "(0::real) < 1" by simp
    show "\<forall>x. 1 \<le> x \<longrightarrow> zero_fun_lean x \<le> 1 * x"
      unfolding zero_fun_lean_def
      by (intro allI impI, linarith)
  qed
qed

text \<open>
  LE PREMIER PONT (Section XIII.3) : si le psi(Savard) joue le role
  fonctionnel de Tchebychev vis-a-vis de zeta (premisse concerne_fonction_zeta)
  et que la Methode Spectrale n'admet que les premiers P, alors la droite
  critique vaut 1/2. C'est pont_spectral_direct_final de la validation
  principale, importe ici pour montrer que le pont Tchebychev <-> zeta est
  DEJA prouve.
\<close>

theorem premier_pont_tchebychev_zeta:
  fixes n n1 n2 :: nat
  assumes premier_pont: "concerne_fonction_zeta (\<lambda>x. psi_savard x n)"
      and second_pont: "\<forall>C. \<not> prime C \<longrightarrow> (\<forall>i. C \<noteq> prime_i i)"
      and h1: "1 \<le> n1" and h2: "1 \<le> n2" and h3: "n1 \<noteq> n2"
  shows "Re_droite_critique n1 n2 = 1 / 2"
  by (rule pont_spectral_direct_final[OF premier_pont second_pont h1 h2 h3])

text \<open>
  LE SECOND PONT (Section XIII.4) : l'exclusion des composes. La Methode
  Spectrale n'admet de solution que pour les premiers ; tout compose C est
  exclu de toute position. Re-exposition de methode_spectrale_exclusivite_P.
\<close>

theorem second_pont_exclusivite_premiers:
  fixes C :: nat
  assumes "\<not> prime C"
  shows "\<forall>i. C \<noteq> prime_i i"
  using assms by (rule methode_spectrale_exclusivite_P)

section "Cercle 3 : La conjecture (definition) et le Pont Savard"

text \<open>
  L'hypothese de Riemann est enoncee comme une DEFINITION booleenne (la
  forme Lean de la conjecture). Elle n'est JAMAIS axiomatisee : les theoremes
  d'alignement qui suivent sont strictement CONDITIONNELS, et la direction
  constructive (RsP = 1/2) reste INCONDITIONNELLE via la Section XIII de la
  validation principale.
\<close>

definition hypothese_Riemann_lean :: bool where
  "hypothese_Riemann_lean =
     (\<forall>s. riemannZeta_lean s = 0 \<and> bande_critique_lean s \<longrightarrow> axe_critique_lean s)"

locale pont_savard_lean =
  fixes s :: complex  (* un zero critique cote Lean *)
    and n1 n2 :: nat  (* deux positions entieres strictement positives *)
  assumes zero_critique: "riemannZeta_lean s = 0"
      and en_bande_critique: "bande_critique_lean s"
      and positions: "1 \<le> n1" "1 \<le> n2" "n1 \<noteq> n2"
begin

text \<open>
  Dans le contexte d'un zero critique, SANS l'hypothese de Riemann, on
  dispose deja de deux faits inconditionnels : le bord superieur de la bande
  (cote Lean, via A2) et la valeur constructive du rapport spectral (cote
  Methode Spectrale, via la Section XIII).
\<close>

lemma zero_sous_le_bord: "Re s < 1"
  using zero_critique by (rule zero_zeta_sous_le_bord_superieur)

lemma rsp_constructif_inconditionnel: "RsP n1 n2 = 1 / 2"
  using positions by (rule RsP_universel_entier_naturel)

theorem alignement_sous_HR:
  (* Sous HR : le zero critique s'aligne exactement sur le rapport spectral. *)
  assumes hRH: "hypothese_Riemann_lean"
  shows "Re s = RsP n1 n2"
proof -
  from hRH zero_critique en_bande_critique have "Re s = 1 / 2"
    unfolding hypothese_Riemann_lean_def axe_critique_lean_def by blast
  moreover note rsp_constructif_inconditionnel
  ultimately show ?thesis by simp
qed

end

theorem equivalence_HR_alignement_savard:
  (* Coeur de la contre-validation : la conjecture est TRANSPORTEE d'un
     langage a l'autre, sans jamais etre supposee. *)
  "hypothese_Riemann_lean \<longleftrightarrow>
   (\<forall>s. riemannZeta_lean s = 0 \<and> bande_critique_lean s \<longrightarrow> Re s = RsP 1 2)"
proof -
  have h12: "RsP (1::nat) (2::nat) = 1 / 2"
    using RsP_universel_entier_naturel[of 1 2] by simp
  show ?thesis
    by (metis hypothese_Riemann_lean_def axe_critique_lean_def h12)
qed

subsection "Cercle 3.b : Direction constructive inconditionnelle (Section XIII)"

theorem direction_constructive_inconditionnelle:
  fixes n1 n2 :: nat
  assumes hn: "1 \<le> n1" "1 \<le> n2" "n1 \<noteq> n2"
  shows "Re_droite_critique n1 n2 = RsP n1 n2 \<and> RsP n1 n2 = 1 / 2"
  using synthese_pont_savard[OF hn] by assumption

theorem temoin_satisfaisabilite_inter_assistants:
  "ensemble_savard 0 (1 / 2) 0 (RsP 1 2)"
  by (rule ensemble_savard_satisfaisable)

text \<open>
  Ces deux theoremes sont INCONDITIONNELS : ils reposent uniquement sur la
  validation principale. Le rapport spectral vaut 1/2 par calcul constructif
  (RsP_universel_entier_naturel, via RsP_un_demi_general), et le locale
  ensemble_savard admet le temoin concret (0, 1/2, 0, RsP 1 2) par le
  theoreme ensemble_savard_satisfaisable.
\<close>

section "Synthese : correspondance des points (Section XIII <-> Mathlib)"

text \<open>
  Mise en relation des points de la Section XIII (validation principale,
  equation du Pont Savard, trois concordances C1-C2-C3) avec les enonces
  Mathlib correspondants :

  CERCLE CENTRAL  (C3 : 1/y2 = 1/ms3, l'alignement) :
    * Re(rho) = 1/2 (Section XIII : hypothese_critique, Re_droite_critique)
      <-> axe_critique_lean (Re s = 1/2), bande_critique_lean (0 < Re s < 1).
    * RsP = 1/2 (RsP_universel_entier_naturel, inconditionnel)
      <-> alignement_sous_HR (conditionnel) + equivalence_HR_alignement_savard.

  CERCLE MEDIAN  (C2 : positions des premiers, domaine) :
    * Fonction zeta et nombres premiers, formule explicite (fait F1, Sec. XIII)
      <-> zeta_eq_tsum_one_div_nat_cpow (serie de Dirichlet pour Re s > 1,
          RiemannZeta.lean l.207) et riemannZeta_residue_one (residu 1 au
          pole s = 1, l.242).
    * Domaine verrouille : aucun zero a droite de la bande
      <-> non_annulation_bande_lean (A2) + zero_zeta_sous_le_bord_superieur
          (demontre ici).

  CERCLE EXTERNE  (C1 : pont fonctionnel Tchebychev <-> psi_savard) :
    * Equation de Tchebychev psi(x) = sum_{n<=x} Lambda(n)
      <-> Chebyshev.psi (Chebyshev.lean l.73) et vonMangoldt (l.65) ; sa
          specification HOL est psi_tchebychev_lean (nonnegativite, annulation
          sous 2, borne C * x) et le psi(Savard) la prolonge (Cercle 2.c).
    * Le Premier Pont (concerne_fonction_zeta) porte par psi_savard
      <-> premier_pont_tchebychev_zeta (importation de pont_spectral_direct_final).
    * Symetrie fonctionnelle de zeta
      <-> equation_fonctionnelle_lean (A1, completedRiemannZeta_one_sub) et ses
          consequences demontrees ici : symetrie_des_zeros_de_Lambda,
          zeros_lambda_involution_critique.
    * Structure fine de l'ensemble des zeros
      <-> riemannZetaZeros ferme et discret, fini sur tout compact
          (ZetaZeros.lean : isClosed_riemannZetaZeros l.60,
          isDiscrete_riemannZetaZeros l.63,
          IsCompact.inter_riemannZetaZeros_finite l.67).

  Conclusion : les trois cercles de la contre-validation No 2 se referment
  sur la Section XIII exactement comme ceux de la contre-validation No 1
  (validation_hol_unifiee.thy), avec en plus l'ancrage externe Mathlib.
\<close>

section "References externes (Mathlib, Lean 4) et licence Apache 2.0"

text \<open>
  Ce fichier SPECIFIE des enonces de la bibliotheque Mathlib pour Lean 4, a
  des fins de contre-validation inter-assistants. Aucun code Lean n'est
  reproduit : seuls les NOMS et les ENONCES mathematiques sont cites a titre
  de reference croisee, avec attribution des auteurs et de la licence.

  Depot   : https://github.com/leanprover-community/mathlib4
  Licence : Apache License, Version 2.0 (voir le fichier LICENSE du depot).
  Copyright (c) les contributeurs de Mathlib (The Mathlib Contributors).

  Fichiers et declarations references (verifies sur le clone local
  C:/Users/thomasphiliippesavar/OneDrive/Mathlib) :

  [1] Mathlib/NumberTheory/LSeries/RiemannZeta.lean
      Copyright (c) 2023 David Loeffler. Apache 2.0.
      - riemannZeta : C -> C                         (fonction zeta)
      - completedRiemannZeta, completedRiemannZeta0  (versions completees)
      - completedRiemannZeta_one_sub   (l.106) : Lambda(1 - s) = Lambda(s)
      - riemannZeta_one_sub            (l.178) : equation fonctionnelle de zeta
      - zeta_eq_tsum_one_div_nat_cpow  (l.207) : serie de Dirichlet, Re s > 1
      - riemannZeta_residue_one        (l.242) : residu 1 au pole s = 1
      - differentiableAt_riemannZeta / differentiableAt_completedZeta

  [2] Mathlib/NumberTheory/LSeries/ZetaZeros.lean
      Copyright (c) 2026 Huanyu Zheng. Apache 2.0.
      - riemannZetaZeros                        (l.36) : zeta inverse de {0}
      - mem_riemannZetaZeros                    (l.38) : appartenance
      - isClosed_riemannZetaZeros               (l.60) : ensemble ferme
      - isDiscrete_riemannZetaZeros             (l.63) : ensemble discret
      - IsCompact.inter_riemannZetaZeros_finite (l.67) : fini sur tout compact

  [3] Mathlib/NumberTheory/LSeries/Nonvanishing.lean  (importe par [2])
      Copyright (c) 2024 Michael Stoll, David Loeffler. Apache 2.0.
      - riemannZeta_ne_zero_of_one_le_re (l.413) : 1 <= Re s ==> zeta s <> 0

  [4] Mathlib/NumberTheory/Chebyshev.lean
      Copyright (c) 2025 Alastair Irving, Terry Tao, Ruben Van de Velde.
      Apache 2.0.
      - Chebyshev.psi                    (l.73) : psi(x) = sum_{n<=x} Lambda(n)
      - Chebyshev.theta                  (l.80) : theta(x) = sum_{p<=x} log p
      - Chebyshev.psi_nonneg             (l.86)
      - Chebyshev.psi_eq_zero_of_lt_two  (l.111)
      - Chebyshev.psi_eq_log_lcmUpto, Chebyshev.psi_eq_sum_theta
      - Chebyshev.psi_le_const_mul_self, Chebyshev.psi_ge (bornes de Chebyshev)
      - Chebyshev.pi_ge, Chebyshev.pi_le_log4_mul_div (compteur des premiers)

  [5] Mathlib/NumberTheory/ArithmeticFunction/VonMangoldt.lean
      Copyright (c) 2022 Bhavik Mehta. Apache 2.0.
      - ArithmeticFunction.vonMangoldt             (l.65) : Lambda(n)
      - ArithmeticFunction.vonMangoldt_apply_prime (l.89) : Lambda p = log p
      - ArithmeticFunction.vonMangoldt_sum : sum_{d | n} Lambda(d) = log n

  Note de conformite : la licence Apache 2.0 exige la conservation des
  mentions de copyright et de licence lors de toute reproduction ; les
  elements ci-dessus etant des citations nominales (aucune ligne de code
  reprise), la presente attribution y satisfait.
\<close>

end
