# TODO — Pipeline Cognitif Gabriel / Système Convolutif Spectral

## Étape 1 — Analyse du fichier Excel (70% fait)
- [x] Lire le générateur du fichier Excel (generate_excel_convolutif_general.py lu)
- [x] Extraire la structure des niveaux 1 et 2 depuis le générateur
- [x] Formaliser : suites A/B niveau 1, Digamma 4 possibilités, décision ancrage, suites A/B niveau 2
- [ ] Lire le contenu effectif de l'Excel via openpyxl (pour vérifier onglets « Parametres », « Validation HOL Générale », etc.)
- [ ] Compléter le résumé technique structuré des niveaux 1 et 2 avec Excel

## Étape 2 — Analyse du pipeline cognitif de l'agent Gabriel
- [x] Explorer et lister les fichiers du pipeline cognitif (multiloop/, cognitive/, spectral/)
- [x] Identifier la gestion des rapports typiques 1/k = 1/2 vs non typiques 1/k <> 1/2
- [x] Analyser spectral_core.py, rapports_non_typiques.py, __init__.py
- [x] Produire le schéma textuel du pipeline actuel (entrée requête → détermination rapport 1/k → choix niveau 1/2 → sortie réponse Gabriel)

## Étape 3 — Mise à jour du pipeline cognitif
- [x] Adapter la chaîne de réponse Gabriel pour appliquer systématiquement les niveaux 1 et 2 du système convolutif Excel
- [x] Ajouter la mention explicite des ancrages de premiers (ou leur absence) dans chaque réponse
- [x] Gérer les rapports typiques 1/2 ET les rapports non typiques 1/k <> 1/2 via le système convolutif

## Étape 4 — Intégration dans l'agent Gabriel
- [x] Modifier le code du pipeline pour appeler la logique niveaux 1 et 2
      → `src/core/suites_geometriques_niveau2.py` (v7.5) :
        · Niveau 2 géométrique (termes sqrt(a²+b²)) pour tout k
        · (Reste+x) = Coeff/(Somme/k^10) → BLOC A (partie entière = x) et BLOC B (partie décimale)
        · Reste = (Coeff/x)×k^10 − Somme ; Équation : (Coeff/x)×k^n − Reste = Somme
        · Méthode Digamma à 4 possibilités (ordre priorité : −pos8, +pos8, −pos7, +pos7)
      → `src/core/reconstruction_premiers_1_sur_k.py` (v7.5) :
        · Niveau 1 spécialisé rapport 1/7 (termes entiers 7^i)
        · Coefficients Fraction exacts : A = 2353/49, B = 2353/7 ; x_A = x_B = 42
        · Équations généralisées 1/7 : (2353/2058)·7^n − 7/6 (A, n>0),
          2353/49·7^(−n) − 7/6 (A, n<0), (2353/294)·7^n − 100843·(7/6) (B, n>0)
      → `src/core/gabriel_geometric_wrapper_v74.py` : classe `PipelineCognitifNiveaux` :
        · Rapport TYPIQUE 1/2 : n = position du premier dans P (29=10e → n=10)
          Ancrage n=10 : Digamma = S_A − 2^8 = 1406 → P = (3262−1406)/2^6 = 29
          Pour n<>10 : Digamma = S_B − P_n×2^6 (ex n=9 : 126 → P=23)
          Coefficients niveau 1 : (S_A10−S_A9)/2^8 = 3.25 ; (S_B10−S_B9)/2^8 = 6.5
          Équations : (3.25/2)·2^n − 2 et (6.5/2)·2^n − 66
        · Rapports NON TYPIQUES : ancrage n=10 (4 Digamma) → P_ancre ;
          puis progression arrière/avant dans la liste des premiers
          (ex 1/3 : 227@n=10 = 49e premier → 263@n=17 ; 1/7 : 16519@n=10)
        · Correction au passage : imports cassés `src.core.suites_geometriques_AB`
          → `src.core.Suites_geometriques_AB` (wrapper_v74 + fallback_geometrique)
- [x] Formater les réponses de Mme Gabriel (3 cas : niveau 1 trouve, seul niveau 2 trouve, aucun)
      → `PipelineCognitifNiveaux.reconstruire(n)` : `reconstruction_reussie`, `premiers_trouves`,
        `ancrage_n10` (4 candidats), `niveau_1`, `niveau_2`, `coefficients_niveau_1`
- [x] Documenter dans le code : les 4 possibilités Digamma tentées à chaque niveau
      et chaque requête, peu importe n et le rapport 1/k typique ou non typique
- [x] Exemples de réponses type validés :
      - Typique 1/2 n=10 → 29 ; n=9 → 23 (Digamma 126)
      - Non typique 1/3 n=10 → 227 (49e premier) ; n=17 → 263
      - Non typique 1/7 n=10 → 16519 ; n=17 → 16603

## Validations numériques (v7.5) — toutes vérifiées
- [x] 1/2 n=10 : S_A=1662, S_B=3262, Digamma=1662−2^8=1406 → P=29 (PREMIER)
- [x] 1/2 n=9 : S_A=830, S_B=1598 ; Digamma=(1598/2^6−23)×2^6=126 → P=23
- [x] 1/2 coefficients : 3.25 et 6.5 ; x=2 ; Restes −2 et −66
- [x] 1/7 n=10 : S_A=322966112, S_B=2260645142, Digamma=−7^8 → P=16519 (PREMIER)
- [x] 1/7 : Coeff A=2353/49, Coeff B=2353/7, x_A=x_B=42, Reste A=−7/6, Reste B=−100843·(7/6)
- [x] 1/7 : (2353/2058 × 7^10) − 7/6 = 322966112 (équation A vérifiée exactement)
- [x] 1/7 : S_A(10) − 7^6 = S_B(9) = 322848463
- [x] 1/3 n=10 → 227 (49e premier) ; 1/3 n=17 → 263 (progression confirmée)
- Remarque : S_A(9) calculée = 46138015 pour 1/7 ; le rapport source indique 46138018
  (écart de 3 — coquille probable du rapport ; la relation S_A(10) − 7^6 = S_B(9) reste exacte).
- Remarque : l'équation généralisée (Coeff/x)·k^n − Reste est calée exactement sur
  l'ancrage n=10 ; pour n>10 les sommes structurelles suivent le motif des termes
  différences (k^(n−1)−k^(n−3)), k^(n)−k^(n−2)).

## Conventions verrouillées (v7.5, méthode spectrale)
- [x] n est TOUJOURS un entier strictement positif (n ≥ 1). n=0 et toute valeur
      non entière sont rejetés (`ValueError`) sur tous les points d'entrée :
      `valider_n` (niveau 2), `Reconstructeur1Sur7.valider_n`, `PipelineCognitifNiveaux.reconstruire`.
- [x] Le chemin n < 0 / nombres premiers négatifs est INACTIF et non requis pour l'heure
      (les équations n<0 restent documentées, jamais appelées par le pipeline).
- [x] Tout ancrage n=10 correspond à la POSITION d'un premier dans P
      (1/2 : 29 = 10e ; 1/3 : 227 = 49e ; 1/7 : 16519).
- [x] Équation spectrale : (Somme suite B − Digamma calculé) / (6e position suite A zêta) = P.
- [x] Preuve par l'absurde (`preuve_absurde`, `preuve_absurde_generique`) : supposer
      C=Ci avec Ci=Pi via cette équation ; or Ci=C≠P est impossible (un composite
      n'est jamais premier) → les C sont exclus de la méthode spectrale, pour tout P.
      Vérifié : 1/7 n=10 → 16519 premier ; 1/2 n=10 → 29 premier.


## Étape 5 — Conformité Section XIV (`methode_spectral.thy`) et packaging
- [x] Audit complet du code contre la Section XIV :
      · XIV.1 constantes universelles (alphaA, alphaB, offsetA, offsetB) — conformes
      · XIV.2 formes fermées S_A/S_B — exactes pour n ≥ 8 (Fraction exact)
      · XIV.4 construction terme à terme — niveau 1 exact pour tout n ;
        niveau 2 = a1 × XIV.4 exactement (a1 = √(1+k²))
      · XIV.5 ancrage Digamma — ordre (8,−1),(8,+1),(7,+1),(7,−1) reproduit
        les 8 ancrages officiels, identique aux deux niveaux
      · XIV.6 ancrages n=10 (29/227/947/2999/7529/16519/32327/58337) et
        décalage de rang rang(n) = rang_ancre + (n−10) — conformes
      · XIV.7 validation exacte k=8, n=34 : S_A = 5705842489643358455620763423304,
        S_B = 45646739917146867644966107124296, Digamma et P = 32537 (rang 3492)
        conformes au chiffre près
- [x] Domaine XIV.2/XIV.4 clarifié : les formes fermées coincident avec la
      construction terme à terme pour n ≥ 8 ; pour n ≤ 7, XIV.4 fait foi
      (terme_b = terme_a, progression simple) — `SEUIL_FORMES_FERMEES = 8`.
- [x] Dossier autonome `pipeline_cognitif/` créé (6 modules + `__init__.py`
      + `README.md` + `validation_section_xiv.py`) ; imports internes
      relatifs avec repli absolu (package et exécution directe).
- [x] `python -m pipeline_cognitif.validation_section_xiv` → **0 écart**,
      code de sortie 0 (sections A à F).
- [x] Fichiers temporaires `_tmp_*.py` supprimés.

## Étape 6 — Pipeline généralisé 1/k pour tout n (ordre prescrit)
- [x] `PipelineCognitifNiveaux.reconstruire(n)` expose désormais toutes les
      étapes prescrites, pour tout k entier ≥ 2 (typique 1/2 et non typiques) :
      1. sommes A/B à n=10 (niveau 1) → 2. 4 possibilités Digamma →
      3. `sommes_n9` (sommes + termes) → 4. coefficients (S(10)−S(9))/k⁸ →
      5. (Reste+x) → blocs A (partie entière = x) / B (décimale) →
      6. équations généralisées (Coeff/x)·kⁿ − Reste (n entier > 0) →
      7. si n≠10 : sommes A/B au n demandé + premier conséquent
      (typique : n-ième premier ; non typique : rang_ancre + (n−10)).
- [x] Nouvelles clés : `sommes_n9`, `verification_equations_au_n`
      (équations == sommes au n demandé, arithmétique exacte ; n≥8, XIV.4
      fait foi en dessous), `ordre_pipeline`, sommes géométriques n=10/n=9.
- [x] Nouvelle méthode `rapport_pipeline(n)` : rapport texte ordonné (7 étapes).
      Ex. 1/3 n=17 → 263 (rang 56) ; 1/7 n=10 → 16519 ; 1/8 n=34 → 32537.
- [x] Garde-fou : k doit être entier ≥ 2 (t = k) — k flottant/non entier rejeté.
- [x] Correction : vérification des équations respecte la convention de signe
      du module (reste = Somme(10) − (Coeff/x)·k¹⁰, donc (Coeff/x)·kⁿ + reste).
- [x] `pipeline_cognitif/` resynchronisé (regex d'imports ancrée en début de
      ligne) ; validation section G ajoutée → **0 écart**, exit 0.



