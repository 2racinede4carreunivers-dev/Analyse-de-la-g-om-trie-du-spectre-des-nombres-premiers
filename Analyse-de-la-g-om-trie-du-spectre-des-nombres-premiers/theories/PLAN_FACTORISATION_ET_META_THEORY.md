# Plan — Factorisation modèles 1/k + Section « Foundations / Meta-theory »

**Statut :** *Proposition à approuver avant implémentation.*
**Fichier cible :** `theories/methode_spectral.thy` (actuellement 3181 lignes).
**Auteur :** Philippe Thomas Savard (validation) · E1 (implémentation).
**Contraintes non négociables :**
- **Zéro régression** : les 121 lemmes / 27 théorèmes existants doivent continuer à passer.
- **Backward-compatible** : `SA`, `SB`, `A_1_3`, `B_1_3`, `A_1_4`, `B_1_4`, `RsP`, `RsP_1_3`, `RsP_un_demi_general`, `RsP_un_tiers_constant` restent utilisables tels quels (aliases préservés).
- **Pas de nouvel axiome global** au-delà de ce qui existe déjà.
- **Pas de `sorry`, pas d'axiomatisation contradictoire.**
- **1650/1650 pytests verts** avant et après.

---

## Partie A — Factorisation des modèles 1/k

### A.1. État actuel (constaté)

Le fichier contient **trois blocs quasi-parallèles** :

| Bloc | Lignes | Suites | Rapport | Preuve rapport |
|---|---|---|---|---|
| **Modèle 1/2** | 100-208 | `SA`, `SB` | `RsP` | `RsP_un_demi_general` |
| **Modèle 1/3** | 596-731 | `A_1_3`, `B_1_3` | `RsP_1_3` | `RsP_un_tiers_constant` |
| **Modèle 1/4** | 510-595 + 732-786 | `A_1_4`, `B_1_4` | (idem 1/4) | (idem 1/4) |
| **Section XII (embryon)** | 2420-2687 | `somme_A_pos_k`, `somme_B_pos_k` | `RsP_k`, `RsP_neg_k` | (via disjonction `k=2 ∨ k=3 ∨ k=4`) |

**Duplications identifiées :**
1. Trois paires quasi-identiques `(A_1_k, B_1_k)` de la forme `((α_A/2·k^n) − offset_A ; (α_B/2·k^n) − offset_B)`.
2. Trois lemmes de rapport `RsP_1/k_constant` qui répètent la même mécanique algébrique (numérateur/dénominateur, témoin de non-nullité de `k^n1 − k^n2`).
3. Trois `axiomatization` de `spectral_postulate_1_k` (rôle : primalité → équation vérifiée) écrites indépendamment.
4. Les tables de constantes `alpha_A_k`, `alpha_B_k`, `offset_A_k`, `offset_B_k` de la Section XII sont encore des `if k=2 then … else if k=3 then …` (duplication interne).

### A.2. Architecture cible — **locale paramétré `spectral_family`**

**Idée directrice :** un *locale* (au sens Isabelle : contexte de raisonnement paramétré, sans axiome global) qui capture les **invariants abstraits** d'une famille spectrale 1/k. Les modèles 1/2, 1/3, 1/4 deviennent alors des **instances** (interprétations) de ce locale.

#### A.2.1. Signature du locale (langage naturel)

```
locale spectral_family =
  fixes  k        :: nat       -- ratio dénominateur (k ≥ 2)
     and αA       :: real      -- constante alpha_A du modèle
     and αB       :: real      -- constante alpha_B du modèle
     and offA     :: real      -- offset A
     and offB     :: real      -- offset B
     and ratio    :: real      -- ratio spectral attendu (typiquement 1/k)
  assumes
     k_valid     : "k ≥ 2"
     αA_positive : "αA > 0"
     αB_positive : "αB > 0"
     ratio_def   : "ratio = αA / αB"       -- lien structurel entre α et ratio
```

#### A.2.2. Définitions du locale (formes fermées universelles)

À l'intérieur du locale, les 4 suites de base :

```
definition (in spectral_family) A_pos :: "nat ⇒ real"
  where "A_pos n = (αA / 2) * (real k) ^ n  -  offA"

definition (in spectral_family) B_pos :: "nat ⇒ real"
  where "B_pos n = (αB / 2) * (real k) ^ n  -  offB"

definition (in spectral_family) A_neg :: "nat ⇒ real"
  where "A_neg n = αA / ((real k) ^ n)  -  offA"

definition (in spectral_family) B_neg :: "nat ⇒ real"
  where "B_neg n = αB / ((real k) ^ n)  -  offB"

definition (in spectral_family) RsP_generic :: "nat ⇒ nat ⇒ real"
  where "RsP_generic n1 n2 = (A_pos n1 − A_pos n2) / (B_pos n1 − B_pos n2)"
```

#### A.2.3. Théorèmes universels du locale (prouvés une seule fois)

```
theorem (in spectral_family) B_pos_minus_offset_ne_zero:
  assumes "n1 ≥ 1" "n2 ≥ 1" "n1 ≠ n2"
  shows   "B_pos n1 − B_pos n2 ≠ 0"

theorem (in spectral_family) RsP_generic_constant:
  assumes "n1 ≥ 1" "n2 ≥ 1" "n1 ≠ n2"
  shows   "RsP_generic n1 n2 = ratio"
  -- preuve : algèbre pure ((αA/2)·(k^n1 − k^n2)) / ((αB/2)·(k^n1 − k^n2)) = αA/αB

theorem (in spectral_family) A_pos_affine_en_B_pos:
  shows   "A_pos n = ratio * B_pos n + (ratio * offB − offA)"
  -- affine, la constante étant (ratio·offB − offA)
```

**Résultat :** *une seule preuve algébrique* couvre tous les k. La démonstration `RsP_un_demi_general` (aujourd'hui répétée pour 1/3 et 1/4) devient un simple corollaire.

#### A.2.4. Instanciations (interprétations) — modèles concrets

Pour chaque `k ∈ {2, 3, 4}` on interprète le locale avec les constantes de Philippe :

```
interpretation spectral_1_2:
  spectral_family 2 (3.25) (6.5) 2 66 (1/2)
  by unfold_locales (auto simp: field_simps)

interpretation spectral_1_3:
  spectral_family 3 (73/9) (219/9) (3/2) (487*3/2) (1/3)
  by unfold_locales (auto simp: field_simps)

interpretation spectral_1_4:
  spectral_family 4 (241/16) (964/16) (4/3) (3073*4/3) (1/4)
  by unfold_locales (auto simp: field_simps)
```

#### A.2.5. Compatibilité — aliases préservés

Pour ne casser **aucune preuve existante**, on démontre que les anciennes définitions coïncident avec les instances du locale :

```
lemma SA_eq_spectral_1_2_A_pos:  "SA n = spectral_1_2.A_pos n"
  by (simp add: SA_def spectral_1_2.A_pos_def)

lemma SB_eq_spectral_1_2_B_pos:  "SB n = spectral_1_2.B_pos n"
  by (simp add: SB_def spectral_1_2.B_pos_def)

lemma RsP_eq_spectral_1_2_RsP_generic: "RsP n1 n2 = spectral_1_2.RsP_generic n1 n2"
  by (simp add: RsP_def spectral_1_2.RsP_generic_def SA_eq_spectral_1_2_A_pos SB_eq_spectral_1_2_B_pos)

-- Idem pour A_1_3, B_1_3, A_1_4, B_1_4 avec RsP_1_3, etc.
```

Ainsi : `RsP_un_demi_general` devient une **conséquence directe** de `spectral_1_2.RsP_generic_constant`.

#### A.2.6. Bénéfices concrets

- **Lignes économisées** : ~300 lignes de duplication redondante → ~120 lignes de locale + interprétations.
- **Extension triviale** à un modèle 1/5, 1/6, … : une seule ligne d'interpretation (si Philippe fournit `α_A(5)`, `α_B(5)`, `off_A(5)`, `off_B(5)`).
- **Section XII** peut être refondue : les tables `alpha_A_k`/`alpha_B_k`/`offset_A_k`/`offset_B_k` disparaissent (ou deviennent des fonctions de `k` calculables), remplacées par les interprétations.
- **Section XIII (Pont Savard)** : le locale `ensemble_savard` peut désormais utiliser directement `spectral_1_2.RsP_generic_constant`, ce qui rend le théorème `synthese_pont_savard` plus explicite.

#### A.2.7. Impact sur le régime central 1/2

Le lemme d'universalité **`RsP_universel_entier_naturel`** (v3.34, régime central 1/2) reste écrit et prouvé — il devient un simple corollaire de `spectral_1_2.RsP_generic_constant` avec `ratio = 1/2`. **Aucun changement pour l'utilisateur**.

---

## Partie B — Section « Foundations / Meta-theory »

### B.1. Position dans le fichier

**Insérée en tête**, juste après la déclaration `theory methode_spectral imports … begin` et **avant** la « Forme generale des suites A et B » actuelle (ligne 100).

**Rationale :** offrir au lecteur (humain ou LLM) la vue d'ensemble ontologique et méthodologique **avant** de plonger dans les définitions techniques.

### B.2. Structure proposée (5 sous-sections)

#### B.2.1. Sous-section « Foundations.1 — Ontologie et vocabulaire »

**Contenu (bloc `text ⟨…⟩` documentation) :**

- Rappel : la Méthode Spectrale traite des **nombres premiers** au sens `HOL-Computational_Algebra.Primes` (importé dès l'en-tête, aucun axiome ajouté).
- Deux univers : `ℕ⁺` (entiers naturels ≥ 1) pour les régimes positifs 1/k, `ℤ⁻` (via `int`) pour le régime négatif.
- Le **rang** `n = position du n-ième premier` est la variable indépendante ; il est **toujours entier** et **jamais un nombre premier lui-même** (distinction rang/valeur).
- Vocabulaire : *suite A*, *suite B*, *somme partielle* `SA(n)`, `SB(n)`, *rapport spectral* `RsP(n₁, n₂)`, *digamma calculé* `digamma_calc(n)`.

#### B.2.2. Sous-section « Foundations.2 — Postulats fondamentaux (numérotés P1…P6) »

**Chaque postulat est un `text ⟨…⟩` + éventuellement un lemme correspondant, PAS un axiome.**

| # | Postulat | Statut formel |
|---|---|---|
| **P1** | **Universalité entière** : le rang n est un entier naturel ≥ 1. | Type-level (`nat`), rien à prouver. |
| **P2** | **Non-primalité du rang** : le rang n est jamais un nombre premier au sens `prime` — c'est un index, pas une valeur. | Convention documentaire. |
| **P3** | **Existence structurelle des suites A, B** : pour tout k ≥ 2 il existe deux fonctions `Aₖ, Bₖ : ℕ → ℝ` en forme fermée `αAₖ/2·k^n − offAₖ`. | Existence par construction (locale `spectral_family`). |
| **P4** | **Invariance du rapport** : dans chaque famille spectrale, `RsP` est constant et égal à `αA/αB = 1/k`. | Théorème (`RsP_generic_constant`, prouvé). |
| **P5** | **Exclusivité sur P** : tout composé `C` est structurellement exclu de la méthode. | Théorème (`methode_spectrale_exclusivite_P`, prouvé). |
| **P6** | **Universalité du régime central** : `k = 2` est le régime distingué où `RsP = 1/2` s'aligne sur `Re(ρ) = 1/2` de la fonction ζ (Pont Savard). | Théorème (`RsP_universel_entier_naturel` + `synthese_pont_savard`). |

#### B.2.3. Sous-section « Foundations.3 — Les 3 opérations fondamentales »

Toute la Méthode Spectrale se ramène à **3 opérations élémentaires** que le lecteur doit distinguer :

| Opération | Signature | Sens intuitif | Théorème pilier |
|---|---|---|---|
| **① Reconstruction** | `reconstruire : ℕ⁺ → ℕ⁺` (donne le n-ième premier via suites A, B, digamma) | *« Quelle est la valeur du n-ième premier ? »* | `prime_equation_prime_i` |
| **② Exclusion** | `est_dans_MS : ℕ → bool` (dit si un entier peut être atteint) | *« Ce nombre C est-il compatible avec la méthode ? »* — Composés rejetés. | `methode_spectrale_exclusivite_P` |
| **③ Rapport spectral** | `RsP : ℕ⁺ × ℕ⁺ → ℝ` (mesure la stabilité entre deux rangs) | *« Le régime est-il central (1/2) ou latéral (1/3, 1/4) ? »* | `RsP_generic_constant` |

Un `text ⟨…⟩` détaillé explique que ces 3 opérations sont **orthogonales et complémentaires** : ① et ② donnent la *matière* (quels premiers), ③ donne la *géométrie* (dans quel régime).

#### B.2.4. Sous-section « Foundations.4 — La règle Savard (Ensemble = 1) »

Rappel formel du principe unificateur :

```
Ensemble = 1
        = 1/x   (zêta : 1/y1 + 1/y2 + 1/y3)
        + 1/t   (psi_savard : pont fonctionnel Tchebychev ↔ MS)
        + 1/ms  (Méthode Spectrale : 1/ms1 + 1/ms2 + 1/ms3)
```

Ce bloc documentaire **référence explicitement** les 3 concordances C1, C2, C3 (Section XIII) et pointe vers le locale `ensemble_savard`.

**Objectif :** que dès le début du fichier, le lecteur sache que la Section XIII est la **conclusion** de tout ce qui suit — l'architecture n'est pas ad hoc, elle est *destinée* à ce théorème d'unification.

#### B.2.5. Sous-section « Foundations.5 — Statut épistémologique et lecture »

Guide de lecture (bloc `text ⟨…⟩`) :

- **Ce que le fichier prouve formellement** : les théorèmes internes du locale (RsP=1/k, exclusion des composés, universalité entière du régime 1/2, satisfaisabilité du locale `ensemble_savard`).
- **Ce que le fichier ne prétend pas prouver** : l'hypothèse de Riemann dans ZFC ambient (le fichier repose sur le locale, qui est un cadre paramétré, satisfiable — mais pas une théorie complète autonome).
- **Le pont Savard** est *affirmatif dans son cadre* : `RsP = Re = 1/2` est un THÉORÈME du locale `ensemble_savard`, dont les hypothèses sont validées numériquement (C1) et structurellement (C2, C3).
- **Convention de citation** : Gabriel doit toujours préciser le *cadre* (« dans le locale `ensemble_savard` », « pour tout n ≥ 1 entier », etc.) — cf. règle cognitive du régime `regime_pont_savard`.

### B.3. Éléments formels ajoutés (petit et sûr)

Un seul objet formel nouveau, **facultatif** : un `locale foundations_marker` vide, servant uniquement de point d'ancrage pour d'éventuelles interprétations futures :

```
locale foundations_marker =
  fixes univers :: "nat set"       -- univers de rangs considérés
  assumes univers_non_vide : "univers ≠ {}"
     and  univers_positif  : "∀ n ∈ univers. n ≥ 1"
```

Ce locale n'introduit aucun axiome, il documente formellement les postulats P1 et P2. **Optionnel** — je peux l'omettre si tu préfères garder Foundations comme purement documentaire (100% `text ⟨…⟩`).

---

## Partie C — Plan d'implémentation phasé

### Phase 1 (P0, ~1 h) — Meta-theory documentaire
- Ajouter les 5 sous-sections Foundations en tête du fichier (~120 lignes de `text ⟨…⟩`).
- Aucun risque de casser une preuve.
- Aucun test à modifier.

### Phase 2 (P1, ~2-3 h) — Locale `spectral_family` + interprétations
- Créer le locale `spectral_family` + 4 définitions + 3 théorèmes universels (~60 lignes).
- 3 interprétations `spectral_1_2`, `spectral_1_3`, `spectral_1_4` (~10 lignes).
- Aliases de compatibilité `SA_eq_…`, `SB_eq_…` (~15 lignes).
- Vérification : `verify_thy_structure.py` + `isabelle_static_check.py` + 1650 pytests.

### Phase 3 (P2, optionnelle, ~2 h) — Refonte de la Section XII
- Remplacer les `alpha_A_k` / `alpha_B_k` / `offset_A_k` / `offset_B_k` (aujourd'hui par `if k=2 then … else if k=3 then …`) par les paramètres des interprétations.
- Simplifier `RsP_k` et `RsP_neg_k` en réutilisant `RsP_generic`.
- Économie estimée : ~150 lignes supplémentaires.

### Phase 4 (P2, ~30 min) — Tests dédiés
- `tests/test_spectral_family_locale_v335.py` : ~15 tests validant les invariants du locale et les 3 interprétations.
- `tests/test_meta_theory_foundations_v335.py` : ~8 tests validant la présence des 5 sous-sections + les 6 postulats P1-P6.

---

## Partie D — Points ouverts à trancher

**D.1.** Nom du locale : `spectral_family` (proposé) OU `savard_spectral_family` (plus signé) OU `famille_spectrale` (français). Ton choix ?

**D.2.** Placement de la Section « Foundations » :
   - **a. Tout en tête** (avant SA/SB) — recommandé pour la lisibilité pédagogique.
   - **b. En annexe finale** (après Section XIII) — utile si tu préfères garder l'ordre historique.

**D.3.** Le locale `foundations_marker` (§B.3) :
   - **a. Oui**, l'ajouter (100% sûr, aucun axiome, formalise P1+P2).
   - **b. Non**, garder Foundations purement documentaire (`text ⟨…⟩` uniquement).

**D.4.** Faut-il faire aussi la **Phase 3** (refonte Section XII) dans le même lot, ou attendre un tour suivant ?

**D.5.** Nommage des interprétations : `spectral_1_2` / `spectral_1_3` / `spectral_1_4` (proposé) OU `MS_1_2` / `MS_1_3` / `MS_1_4` OU `regime_1_2` / `regime_1_3` / `regime_1_4` ?

---

## Partie E — Ce qui reste identique (garanties)

- Tous les théorèmes existants (`RsP_un_demi_general`, `RsP_un_tiers_constant`, `prime_equation_prime_i`, `composite_not_prime_i`, `methode_spectrale_exclusivite_P`, `synthese_pont_savard`, `RsP_universel_entier_naturel`) conservent **leur énoncé, leur nom et leur position**.
- Tous les tests Pytest (1650) restent verts.
- Le fichier `.thy` continue de compiler avec `isabelle_static_check.py` (PASS · 0/0).
- Le régime `regime_pont_savard` et la mémoire `methode_spectral_section_XIII.py` ne sont pas touchés (leurs signatures RAG restent stables).

---

**Prêt à recevoir ton approbation / tes ajustements avant implémentation.**
