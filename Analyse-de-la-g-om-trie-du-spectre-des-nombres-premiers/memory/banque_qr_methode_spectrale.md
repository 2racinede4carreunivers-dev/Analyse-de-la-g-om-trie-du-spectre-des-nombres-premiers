# Banque Q&R — Méthode Spectrale (curation Philippe)

**Origine** : catalogue de 184 Q&R sur les théories de Philippe Thomas Savard.
**Sélection** : 15 Q&R **strictement mathématiques**, filtrées selon les critères :
- ✅ Contenu mathématique concret (formules, lemmes, exemples numériques)
- ❌ **Rejet** : questions philosophiques, ontologiques, téléosémantiques
- ❌ **Rejet** : questions moyennes / vagues / redondantes
- ❌ **Rejet** : questions sur d'autres théories (Espace de Philippôt, univers au carré, spirale de Théodore) sans lien direct avec la Méthode Spectrale

**Sources retenues** : `geometry_prime_spectrum.tex` et `methode_spectral.thy` (les deux fichiers cœur de la Méthode Spectrale).

**Instructions pour Philippe** : pour chaque Q&R, remplacer `[ ] à valider` par **`[OK]`** ou **`[KO]`**. Une fois marquées `[OK]`, ces Q&R alimenteront le RAG cognitif de Gabriel (`memory/dictionnaire_spectral.py`).

---

## Q1 — Rapport spectral 1/2 négatif : constance
**Statut** : [Ok] à valider  →  [OK] / [KO]
**Domaine** : régime négatif, formules SA/SB
**Source** : `geometry_prime_spectrum.tex` (section "Rapport spectral 1/2 négatif")

**Q** : Comment est démontrée la constance du rapport spectral (1/2) pour les suites négatives ?

**R** : `RsP_neg n1 n2 = (SA_neg_eq n1 - SA_neg_eq n2) / (SB_neg_eq n1 - SB_neg_eq n2)`,
avec **SA_neg_eq(n) = 3.25·2^n − 2** et **SB_neg_eq(n) = 6.5·2^n − 66**.
L'axiome `spectral_ratio_neg_un_demi` stipule `RsP_neg(n1, n2) = 1/2` pour n1 ≤ −1, n2 ≤ −1, n1 ≠ n2. Prouvé formellement par le lemme `RsP_neg_un_demi_general` (Isabelle/HOL).

---

## Q2 — Rapport spectral 1/3 : théorème `RsP_un_tiers_constant`
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : régime 1/3, modèle spectral
**Source** : `geometry_prime_spectrum.tex` (section "Rapport spectral 1/3 – validation généralisée")

**Q** : Comment est démontrée la constance du rapport spectral 1/3 ?

**R** : Différence des suites : `A_1_3(n1) − A_1_3(n2) = ((73/9)/12) · (3^n1 − 3^n2)` et `B_1_3(n1) − B_1_3(n2) = ((219/9)/12) · (3^n1 − 3^n2)`. Le rapport se simplifie en `(73/9) / (219/9) = 73/219 = 1/3`. Cette constance est démontrée par le théorème `RsP_un_tiers_constant`.

---

## Q3 — Axiome `mixed_gap_surplus` et Riemann
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : écart mixte, conjecture de Riemann
**Source** : `geometry_prime_spectrum.tex` (section "Axiomatization")

**Q** : Comment l'axiome `mixed_gap_surplus` lie-t-il les écarts mixtes à la conjecture de Riemann ?

**R** : L'axiome stipule `relative_value(Pn) > relative_value(P)` : l'intervalle Tn (premiers à densité de zéros plus élevée) a une valeur relative supérieure à l'intervalle T complet. L'aire restante `T_rest = T − Tn` correspond alors à `geometric_area(relative_value(Pn) − relative_value(P))`. Cette relation géométrique suggère que tous les zéros non triviaux de ζ ont partie réelle = 1/2, soutenant Riemann.

---

## Q4 — Écart entre −31 et 17 : calcul détaillé
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : écart mixte (−, +), exemple numérique clé
**Source** : `geometry_prime_spectrum.tex` (référence pour le fix « pont ZÉRO » de Gabriel)

**Q** : Comment est établie la relation `(−22323135/20480 − 39280705/20480) / 64 = −47`, et que signifie ce résultat ?

**R** : Calcul :
- SA_suivant(−29) = (3.25 × 2^−10) − 2 = **−40895/20480**
- SB(17) = (6.5/2) × 2^7 − 66 = **350**
- Digamma(17) = (350/64 − 17) × 64 = **−738**
- SB(−31) = (6.5 × 2^−11) − 66 = −1351615/20480
- Digamma(−31) = ((−1351615/20480)/64 − (−31)) × 64 = **39280705/20480**
- Terme A = −40895/20480 − (350 − (−738)) = **−22323135/20480**
- gap = (−22323135/20480 − 39280705/20480) / 64 = **−47**

Résultat : **47 nombres entre −31 et 17** (30 négatifs + 0 [1 unité] + 16 positifs = 47).

---

## Q5 — 37 est le 12ᵉ nombre premier : équation
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : reconstruction, modèle 1/2 positif
**Source** : `geometry_prime_spectrum.tex`

**Q** : Comment l'équation `(13246 − 10878) / 64 = 37` démontre-t-elle que 37 est le 12ᵉ premier ?

**R** :
- **13246** = SB(12) = (6.5/2) × 2^12 − 66 (somme suite B au 12ᵉ terme)
- **10878** = SA(12) + Digamma(37) = 6654 + 4224
- **64** = facteur de normalisation (2^6)

Formule : `p = (SB(n) − SA(n) − Digamma(p)) / 64 = (13246 − 10878) / 64 = 37`.
Chaque terme provient de la progression géométrique des suites SA/SB et de la contribution Digamma.

---

## Q6 — Lemme `ratio_spectral_local` (rapport 1/2 termes consécutifs)
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : structure spectrale générale, invariant 1/2
**Source** : `geometry_prime_spectrum.tex` (section "Structure spectrale générale pour n termes")

**Q** : Comment le lemme `ratio_spectral_local` valide-t-il que le rapport entre termes consécutifs vaut toujours 1/2 ?

**R** : Définition : `terme_spectral(i) = 1 / 2^i`. Le rapport `terme_spectral(Suc i) / terme_spectral(i) = (1 / 2^(i+1)) / (1 / 2^i) = 1/2`. Utilise le lemme auxiliaire `ratio_puissances_de_deux`. Implication géométrique : chaque étape divise l'aire par 2, structure fractale/hiérarchique parfaitement définie.

---

## Q7 — RsP_1_3 (= 1/3) et RsP_1_4 (= 1/4) : parallèle
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : modèles 1/3 et 1/4, généralisation
**Source** : `geometry_prime_spectrum.tex`

**Q** : Comment sont établis RsP_1_3 = 1/3 et RsP_1_4 = 1/4 via les différences A_1_k et B_1_k ?

**R** :
- **RsP_1_3** : `(73/108) / (219/108) = 1/3` (après simplification par les puissances de 3)
- **RsP_1_4** : `(241/192) / (964/192) = 1/4` (après simplification par les puissances de 4)
Ces ratios s'obtiennent par des différences de séries géométriques. En étendant aux séquences négatives (SA_neg_eq / SB_neg_eq), on obtient `RsP_neg = 1/2` via l'axiome `spectral_ratio_neg_un_demi`.

---

## Q8 — Axiome `spectral_postulate_pos` (validité positive)
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : fondement axiomatique, régime positif
**Source** : `geometry_prime_spectrum.tex` (section "Axiomatisation positive")

**Q** : Quelle est l'hypothèse axiomatique garantissant la validité de l'équation des nombres premiers dans le cas positif ?

**R** : L'axiome **`spectral_postulate_pos`** : pour tout n ≥ 1 et tout p premier, `prime_equation(n, p) = real(p)`. Base pour toutes les dérivations dans le régime positif. Validé formellement dans Isabelle/HOL à travers les configurations spectrales avec suites SA et SB.

---

## Q9 — Axiome « 1/k numérique mais algébriquement incohérent »
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : fondement axiomatique, particularité de la Méthode
**Source** : `geometry_prime_spectrum.tex` (section "Axiomatization")

**Q** : Que signifie l'axiome selon lequel « le rapport spectral 1/k est numériquement valide mais algébriquement incohérent » ?

**R** : Le rapport 1/k, obtenu via les suites A(n) et B(n), est **numériquement exact** lorsqu'on effectue les calculs sur des indices concrets. Cependant, il **ne respecte pas les lois algébriques standard** lorsqu'on tente une manipulation générale. Cette dualité (validité numérique / incohérence algébrique) est un trait spécifique de la Méthode Spectrale : les propriétés se vérifient par calcul mais ne se déduisent pas par manipulation algébrique classique.

---

## Q10 — Formes générales SA/SB (modèle 1/2)
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : définitions fondamentales
**Source** : `methode_spectral.thy`

**Q** : Comment sont définies les formes générales SA(n) et SB(n), et comment mènent-elles au rapport 1/2 ?

**R** :
- **SA(n) = (3.25 / 2) · 2^n − 2**
- **SB(n) = (6.5 / 2) · 2^n − 66**

Pour deux indices n1, n2 distincts :
`RsP(n1, n2) = (SA(n1) − SA(n2)) / (SB(n1) − SB(n2)) = 1/2`

Démonstration : les termes constants (−2 et −66) s'annulent dans la différence, et le rapport (3.25/2) / (6.5/2) = 3.25/6.5 = 1/2. Validé par le lemme `RsP_un_demi_general`.

---

## Q11 — Constante `k_spectral` et calcul explicite du rapport
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : axiome `rapport_spectral_forme`
**Source** : `methode_spectral.thy`

**Q** : Comment calculer explicitement le rapport spectral entre deux premiers P, Q via `k_spectral` ? Exemple `k_spectral(P, Q) = 3`.

**R** : L'axiome `rapport_spectral_forme` stipule : `rapport_spectral(P, Q) = 1 / int(k_spectral(P, Q))` lorsque `k_spectral(P, Q) ≥ 1`. Pour `k_spectral(P, Q) = 3`, on a directement `rapport_spectral(P, Q) = 1/3`. Confirme la nature **numérique mais non algébrique** du rapport.

---

## Q12 — Rapport spectral 1/3 négatif : `RsP_neg_un_tiers_general`
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : régime négatif, modèle 1/3
**Source** : `methode_spectral.thy` (section "Rapport spectral 1/3 négatif")

**Q** : Comment est démontrée la constance de `RsP_neg_un_tiers` ?

**R** : Définitions :
- **SA_neg_eq_un_tiers(n) = ((73/9)/6) · 3^n − 1.5**
- **SB_neg_eq_un_tiers(n) = ((219/9)/6) · 3^n − (487 · 1.5)**

Rapport : `RsP_neg_un_tiers(n1, n2) = (SA_neg_eq_un_tiers(n1) − SA_neg_eq_un_tiers(n2)) / (SB_neg_eq_un_tiers(n1) − SB_neg_eq_un_tiers(n2)) = 1/3`

Axiome : `spectral_ratio_neg_un_tiers` pour n1 ≤ −1, n2 ≤ −1, n1 ≠ n2.
Formalisé par le lemme `RsP_neg_un_tiers_general`.

---

## Q13 — Écart entre 227 et 173 en modèle 1/3 : lemme `ecart_227_173_1_3`
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : écart (+, +), modèle 1/3
**Source** : `methode_spectral.thy`

**Q** : Que signifie l'équation `((SA_179_val − (SB_227_val − D_227_val) − D_173_val) / 729) = −53` ?

**R** :
- **SA_179_val** = 96/9 (somme suite A pour 179, le premier suivant 173 dans le régime 1/3)
- **SB_227_val** = somme suite B pour le plus grand premier (227)
- **D_227_val** = **73263** (Digamma pour 227)
- **D_173_val** = **−1141518/9** (Digamma pour 173)
- Diviseur **729** = 3^6 (facteur de normalisation pour le modèle 1/3, analogue à 64 = 2^6 pour le modèle 1/2)

Résultat : **−53 nombres entre 173 et 227** (avec signe indicant la direction). Généralisation du modèle 1/2 au modèle 1/3.

---

## Q14 — Vérification que 947 est premier (modèle 1/4) : lemme `preuve_premier_947`
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : reconstruction, modèle 1/4
**Source** : `methode_spectral.thy` (section "Modèle spectral 1/4 : Sommes de suite A et B, Digamma")

**Q** : Comment vérifier via les définitions du modèle 1/4 que 947 est premier ?

**R** : Constantes du modèle 1/4 :
- **suite_A_1_4_somme = 1316180**
- **suite_B_1_4_somme = 5260628**
- **digamma_1_4 = 65536**
- **digamma_calcule_1_4 = suite_A_1_4_somme + digamma_1_4 = 1316180 + 65536 = 1381716**

Équation `preuve_premier_947` :
`(suite_B_1_4_somme − digamma_calcule_1_4) / 4096 = (5260628 − 1381716) / 4096 = 947` ✓

Diviseur **4096 = 2^12** (spécifique au modèle 1/4, cohérent avec 64 = 2^6 pour 1/2 et 729 = 3^6 pour 1/3).

---

## Q15 — Écart mixte `gap_m31_17` : formule `gap_mix_val`
**Statut** : [ok] à valider  →  [OK] / [KO]
**Domaine** : écart mixte (−, +), formalisation Isabelle/HOL
**Source** : `methode_spectral.thy` (lemme `gap_m31_17`)

**Q** : Comment le lemme `gap_m31_17` illustre-t-il le calcul d'écart mixte via `gap_mix_val` ?

**R** : Valeurs spectrales exactes :
- **SA_m29_val = −40895 / 20480** (suite A pour −29, le prochain premier après −31 vers zéro)
- **SB_p17_val = 350** (suite B pour 17)
- **D_p17_val = −738** (Digamma pour 17)
- **D_m31_val = 39280705 / 20480** (Digamma pour −31)

Formule : **`gap_mix_val = (A_next − (B_high − D_high) − D_low) / 64`**

Substitution : `(−40895/20480 − (350 − (−738)) − 39280705/20480) / 64 = −47`.
La preuve utilise `unfolding` puis `simp`.

**Note importante** : cette formule est celle qui a servi de référence pour corriger le bug « pont ZÉRO » dans Gabriel (`_solve_mixed(-2, 37)` — voir Changelog v3.13).

---

## Résumé de la sélection

| # | Thème | Formule/Lemme clé | Régime |
|---|---|---|---|
| Q1 | RsP négatif | `RsP_neg_un_demi_general` | 1/2 négatif |
| Q2 | RsP 1/3 positif | `RsP_un_tiers_constant` | 1/3 |
| Q3 | Axiome mixed_gap | `mixed_gap_surplus` → Riemann | mixte |
| Q4 | Exemple (−31, 17) | Calcul complet = −47 | mixte |
| Q5 | Reconstruction 37 | `(13246 − 10878)/64 = 37` | 1/2 positif |
| Q6 | Ratio consécutifs | `ratio_spectral_local = 1/2` | général |
| Q7 | RsP 1/3 vs 1/4 | Différences A_1_k, B_1_k | 1/3, 1/4 |
| Q8 | Postulat positif | `spectral_postulate_pos` | 1/2 positif |
| Q9 | Nature du 1/k | numérique ≠ algébrique | tous |
| Q10 | SA/SB générales | `SA(n)=(3.25/2)·2^n−2` | 1/2 |
| Q11 | k_spectral | `rapport_spectral_forme` | tous |
| Q12 | RsP_neg 1/3 | `RsP_neg_un_tiers_general` | 1/3 négatif |
| Q13 | Écart 227−173 | `ecart_227_173_1_3 = −53` | 1/3 positif |
| Q14 | Reconstruction 947 | `preuve_premier_947` | 1/4 |
| Q15 | Écart −31/17 | `gap_m31_17` (formalisation) | mixte |

**Couverture** : les 5 régimes (1/2 positif, 1/2 négatif, 1/3 positif, 1/3 négatif, 1/4) + écart mixte + fondements axiomatiques.

**Prochaine étape (après validation)** : les Q&R marquées `[OK]` seront intégrées dans le RAG cognitif de Gabriel (`memory/dictionnaire_spectral.py`) pour enrichir automatiquement les prompts LLM avec ce corpus canonique.
