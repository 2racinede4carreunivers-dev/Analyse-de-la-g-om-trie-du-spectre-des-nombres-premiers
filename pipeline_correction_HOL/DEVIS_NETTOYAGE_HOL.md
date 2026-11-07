# DEVIS DE NETTOYAGE — Pipeline HOL/Isabelle « Géométrie du spectre des nombres premiers »
Auteur : Philippe Thomas Savard — Lévis, Chaudière-Appalaches, Canada
Date : Le trois octobre deux mille vingt-six
Session cible : Geometrie_Spectre_Premier_Philippe_Thomas_Savard (identifiant sans espaces : `Geometrie_Spectre_Premier_Philippe_Thomas_Savard`)

## 1. Constats (mesures sur `methode_spectral.thy` : 5015 lignes, 201710 octets, 58 `section`, 179 `definition`, 183 `lemma`, 33 `theorem`, 15 `axiomatization`)
- Redondance rapports 1/2, 1/3, 1/4 : occurrences « Rapport spectral 1/2 »=8, « 1/3 »=6, « 1/4 »=6. Blocs L352-1039 (~688 lignes), L1135, L1659-1737, L2389-2630 (~240 lignes) se recouvrent.
- Le système convolutif (Section XIV, L4233-4950, 718 lignes, 27 def + 27 lem/thm) subsume algébriquement les trois régimes via `alphaA_conv / alphaB_conv / offsetA_conv / offsetB_conv` + `somme_A_conv / somme_B_conv` + rapport 1/k universel. Les lemmes `somme_A_conv_k2_eq_SA` et `somme_B_conv_k2_eq_SB` prouvent l'identité k=2 = modèle 1/2.
- Écarts numériques dispersés : 46 occurrences de « ecart », exemples -19/-5 (L1750-1782), -31/17 (L2308-2364), 23/7, 227/173, 947/881. Chacun redéfinit SA/SB ad hoc au lieu d'instancier l'équation générale d'écart 1/3 (L2461) et 1/4 (L2560).
- Preuve par l'absurde (L1979-2307, 329 lignes, 23 lem/thm, 0 axiome) : À CONSERVER INTÉGRALEMENT.
- Reconstruction Ai/Bi (Section XI, L2631-2925, 295 lignes) + `spectral_family` (XI.bis, L2926-3224) : À CONSERVER. C'est la base du pipeline cognitif terme-à-terme.
- Pont Savard (XIII, L3493-4143, 651 lignes) : À CONSERVER COMPLET (concordances C1, psi Tchebychev, zeta, Re=1/2).
- Digamma (169 occurrences), incohérence algébrique, `prime_i` (104 occurrences) : À CONSERVER, mais factoriser les 4 branches Digamma en un seul prédicat paramétré par k.
- `sorry` unique : Section XII (L3225-3492). À traiter en priorité mémoire (avec les 21 `by eval` lourds de `validation_hol_unifiee.thy`, cause du `Run out of store` à ~15,8 Go / plafond 16 Go Poly/ML 32-in-64).
- Contre-validations : `validation_hol_unifiee.thy` (878 lignes, 15 sections) et `validation_zeta_lean.thy` (474 lignes, 6 sections) : structure saine, pas de duplication interne. Action = seul enrichissement d'en-tête + TOC avec N° de lignes, pas de découpage.

## 2. Règles d'allègement décidées avec l'auteur
1. RETIRER (phase 2, après validation du découpage phase 1) : les instantiations numériques 1/2, 1/3, 1/4 redondantes (L352-1039 détails, L1659-1737, L2389-2630 exemples) — remplacées par UNE section unifiée « Rapports typiques / non-typiques 1/k » qui instancie le système convolutif + règle d'ancrage n=10 + décalage de rang (XIV.5/XIV.6).
2. CONSERVER INTÉGRALEMENT : preuve par l'absurde (F09), reconstruction Ai/Bi + `spectral_family` (F11), Pont Savard (F13), système convolutif (F14).
3. GÉNÉRALISER (phase 2) : écarts positifs / négatifs / mixtes. Remplacer les 5 exemples numériques par : `gap_equation_1k` paramétrée en k + `gap_positif / gap_negatif / gap_mixte` + théorèmes `gap_correct_pos/neg/mix` valables pour tout P premier et tout rapport 1/k typique ou non-typique. Les définitions `SA_..._val` ad hoc seront supprimées.
4. METTRE À JOUR (phase 2) : section convolutive — ajouter la réconciliation typique (n = position du premier) vs non-typique (n = quantité de termes, ancrage 4 essais Digamma, ordre déterministe pos8-/pos8+/pos7+/pos7-) déjà présente en texte (L4274-4302) sous forme de lemmes `ancrage_typique` / `ancrage_nontypique` + règle `rang_cible = rang_base + (n - 10)`.
5. CONSERVER : Digamma (factorisé), incohérence algébrique, `prime_i`, asymétries/blocs (allégés, pas supprimés).
6. MÉMOIRE : le découpage en 14 fichiers NE FAIT PAS baisser le pic mémoire (1 session = 1 tas partagé). Le gain viendra de (a) l'extraction des `by eval` géants (Pocklington 368939/1883429, `~prime(3_486_xxx_xxx)`) dans une session annexe, (b) `ML_OPTIONS="--minheap 1200 --maxheap 14000"` (jamais `--maxheap 4000` = plafond 4 Go), (c) `isabelle build -j1`.

## 3. Plan de découpage phase 1 (verbatim, sans perte sémantique — la suppression phase 2 viendra après ton feu vert)
Ordre chaîné (chaque fichier importe le précédent, donc l'ordre logique est préservé) :
- F01 L118-351 Fondements / Méta-théorie
- F02 L352-491 Suites A/B + RsP 1/2 + n×n
- F03 L492-676 Digamma + axiomatisation positive + exemples 29/31/37/41 + équation générale
- F04 L677-761 Généralisation prime_i
- F05 L762-1039 Modèles 1/4 + 1/3 + validations généralisées [CANDIDAT SUPPRESSION phase 2 → convolutif]
- F06 L1040-1204 Mixtes + négatives + asymétries
- F07 L1205-1658 Comparaison asymétrique + Blocs A_k/B_k
- F08 L1659-1978 Rapports négatifs + écarts négatifs + -19/-5 [CANDIDAT GÉNÉRALISATION]
- F09 L1979-2307 Preuve par l'absurde [INTÉGRAL]
- F10 L2308-2630 Écarts mixtes/positifs + 227/173 + 947/881 [CANDIDAT GÉNÉRALISATION]
- F11 L2631-3224 Règles construction + spectral_family [INTÉGRAL]
- F12 L3225-3492 Construction généralisée 1/k [contient l'unique sorry]
- F13 L3493-4232 Pont Savard + synthèse-index [INTÉGRAL]
- F14 L4233-5015 Système convolutif + références + licence [CŒUR, À ÉTENDRE phase 2]
En-têtes : `theory MS_XX_...`, Auteur / Date en lettres / Lieu / Note « Pipeline HOL / Validation principale methode_spectral.thy section X/14 », TOC globale des 14 + TOC locale.
Contre-validations : 1 fichier chacune, en-tête Auteur/Date/Lieu + « Pipeline HOL / Contre-validation HOL 1/2 » (resp. 2/2), TOC avec N° de ligne début-fin.
README.thy : `text` uniquement, résumé README.txt + LICENCE intégrale + collaborateurs + remerciements.
ROOT : session `Geometrie_Spectre_Premier_Philippe_Thomas_Savard`, theories chaînées 14 + 2 + README. `methode_spectral.thy` d'origine conservée hors ROOT (archive) pour traçabilité.
