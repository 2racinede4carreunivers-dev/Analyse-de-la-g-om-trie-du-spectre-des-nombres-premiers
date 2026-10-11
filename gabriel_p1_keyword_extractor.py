#!/usr/bin/env python3
# =============================================================================
#  gabriel_p1_keyword_extractor.py
#  PIPELINE COGNITIF GABRIEL — ÉTAPE 1
#  Extracteur de mots-clés HOL depuis methode_spectral.thy +
#  validation_hol_unifiee.thy — Association aux Q&R techniques
#
#  Dépôt   : C:\agent-multiloop-Gabriel-local-final
#  Entrées : theories/methode_spectral.thy
#            theories/validation_hol_unifiee.thy
#  Sortie  : gabriel_keywords_qr_map.json
#  Usage   : python gabriel_p1_keyword_extractor.py
# =============================================================================

import re, os, sys, json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# ─────────────────────────────────────────────────────────────────────────────
#  CHEMINS RÉELS (issus de gabriel_repo_map.json)
# ─────────────────────────────────────────────────────────────────────────────

RACINE = Path(r"C:\agent-multiloop-Gabriel-local-final")

# Chemins candidats — le script teste dans l'ordre et prend le premier valide
CANDIDATS_MS = [
    RACINE / "theories" / "methode_spectral.thy",
    RACINE / "agent-multiloop-Gabriel-local" / "theories" / "methode_spectral.thy",
    RACINE / "methode_spectral.thy",
]
CANDIDATS_VAL = [
    RACINE / "theories" / "validation_hol_unifiee.thy",
    RACINE / "agent-multiloop-Gabriel-local" / "theories" / "validation_hol_unifiee.thy",
    RACINE / "validation_hol_unifiee.thy",
]

SORTIE = RACINE / "gabriel_keywords_qr_map.json"


def trouver_fichier(candidats: list[Path]) -> Path | None:
    for c in candidats:
        if c.exists():
            return c
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  PATTERNS D'EXTRACTION HOL — issus de l'analyse réelle des .thy
# ─────────────────────────────────────────────────────────────────────────────

PATTERNS_HOL = {
    "definition":    re.compile(r'\bdefinition\s+(\w+)\s*(?:::|where)', re.I),
    "lemme":         re.compile(r'\blemma\s+(\w+)\b', re.I),
    "theoreme":      re.compile(r'\btheorem\s+(\w+)\b', re.I),
    "corollaire":    re.compile(r'\bcorollary\s+(\w+)\b', re.I),
    "proposition":   re.compile(r'\bproposition\s+(\w+)\b', re.I),
    "axiome":        re.compile(r'\b(\w+)\s*:\s*\n?\s*"[^"]*?==>.*?"', re.S),
    "axiomatisation":re.compile(r'axiomatization\s+where\s+(\w+)\s*:', re.I),
    "section":       re.compile(r'\b(?:section|subsection)\s+[‹\u2039\u203a"](.*?)[›\u2039\u203a"]'),
    "locale":        re.compile(r'\blocale\s+(\w+)\s*=', re.I),
}

# ─────────────────────────────────────────────────────────────────────────────
#  ENTITÉS HOL CONNUES (extraites de l'analyse réelle des deux .thy)
#  Structure : (nom, type, source, sphère, cercle)
# ─────────────────────────────────────────────────────────────────────────────

# Sphère 1/ms — Méthode Spectrale (154 définitions, 148 lemmes)
ENTITES_MS = [
    # Cercle 1 — Suites fondamentales
    ("SA",                              "definition",    "methode_spectral.thy", "1/ms", 1),
    ("SB",                              "definition",    "methode_spectral.thy", "1/ms", 1),
    ("A_1_3",                           "definition",    "methode_spectral.thy", "1/ms", 1),
    ("B_1_3",                           "definition",    "methode_spectral.thy", "1/ms", 1),
    ("A_1_4",                           "definition",    "methode_spectral.thy", "1/ms", 1),
    ("B_1_4",                           "definition",    "methode_spectral.thy", "1/ms", 1),
    ("SA_mix",                          "definition",    "methode_spectral.thy", "1/ms", 1),
    ("SB_mix",                          "definition",    "methode_spectral.thy", "1/ms", 1),
    ("SA_neg_eq",                       "definition",    "methode_spectral.thy", "1/ms", 1),
    ("SB_neg_eq",                       "definition",    "methode_spectral.thy", "1/ms", 1),
    ("digamma_calc",                    "definition",    "methode_spectral.thy", "1/ms", 1),
    ("digamma_neg_calc",                "definition",    "methode_spectral.thy", "1/ms", 1),
    ("prime_equation",                  "definition",    "methode_spectral.thy", "1/ms", 1),
    ("prime_equation_1_3",              "definition",    "methode_spectral.thy", "1/ms", 1),
    ("prime_equation_1_4",              "definition",    "methode_spectral.thy", "1/ms", 1),
    ("prime_i",                         "definition",    "methode_spectral.thy", "1/ms", 1),
    # Cercle 2 — Rapports spectraux
    ("RsP",                             "definition",    "methode_spectral.thy", "1/ms", 2),
    ("RsP_nn",                          "definition",    "methode_spectral.thy", "1/ms", 2),
    ("RsP_1_3",                         "definition",    "methode_spectral.thy", "1/ms", 2),
    ("RsP_1_4",                         "definition",    "methode_spectral.thy", "1/ms", 2),
    ("RsP_neg",                         "definition",    "methode_spectral.thy", "1/ms", 2),
    ("RsP_bloc_1_2",                    "definition",    "methode_spectral.thy", "1/ms", 2),
    ("somme_SA_bloc",                   "definition",    "methode_spectral.thy", "1/ms", 2),
    ("somme_SB_bloc",                   "definition",    "methode_spectral.thy", "1/ms", 2),
    ("rapport_spectral_un_demi_nn",     "definition",    "methode_spectral.thy", "1/ms", 2),
    # Cercle 3 — Conditions et indices
    ("indice_valide",                   "definition",    "methode_spectral.thy", "1/ms", 3),
    ("indice_valide_nat",               "definition",    "methode_spectral.thy", "1/ms", 3),
    ("liste_strictement_croissante",    "definition",    "methode_spectral.thy", "1/ms", 3),
    ("asymetrique_ordonnee",            "definition",    "methode_spectral.thy", "1/ms", 3),
    ("asymetrique_chaotique",           "definition",    "methode_spectral.thy", "1/ms", 3),
    ("asymetrique_ordonnee_nat",        "definition",    "methode_spectral.thy", "1/ms", 3),
    ("asymetrique_chaotique_nat",       "definition",    "methode_spectral.thy", "1/ms", 3),
    # Cercle 4 — Postulats axiomatiques
    ("spectral_postulate_pos",          "axiome",        "methode_spectral.thy", "1/ms", 4),
    ("spectral_postulate_1_3",          "axiome",        "methode_spectral.thy", "1/ms", 4),
    ("spectral_postulate_1_4",          "axiome",        "methode_spectral.thy", "1/ms", 4),
    ("spectral_ratio_neg_un_demi",      "axiome",        "methode_spectral.thy", "1/ms", 4),
    ("spectral_ratio_neg_un_tiers",     "axiome",        "methode_spectral.thy", "1/ms", 4),
    ("spectral_ratio_neg_un_quart",     "axiome",        "methode_spectral.thy", "1/ms", 4),
    ("prime_position_exists",           "axiome",        "methode_spectral.thy", "1/ms", 4),
]

# Sphère 1/t — Théorèmes HOL (27 théorèmes, 148 lemmes)
ENTITES_THY = [
    # Cercle 1 — Lemmes algébriques fondamentaux
    ("SA_forme_generale",               "lemme",  "methode_spectral.thy", "1/t", 1),
    ("SB_forme_generale",               "lemme",  "methode_spectral.thy", "1/t", 1),
    ("SB_affine_en_SA",                 "lemme",  "methode_spectral.thy", "1/t", 1),
    ("ecart_spectral_constant",         "lemme",  "methode_spectral.thy", "1/t", 1),
    ("digamma_affine_en_SA",            "lemme",  "methode_spectral.thy", "1/t", 1),
    ("difference_SA_succ",              "lemme",  "methode_spectral.thy", "1/t", 1),
    ("difference_SB_succ",              "lemme",  "methode_spectral.thy", "1/t", 1),
    ("ratio_incremental_un_demi",       "lemme",  "methode_spectral.thy", "1/t", 1),
    ("digamma_calc_equation_alt",       "lemme",  "methode_spectral.thy", "1/t", 1),
    ("prime_equation_identity",         "lemme",  "methode_spectral.thy", "1/t", 1),
    # Cercle 2 — Théorèmes spectraux centraux
    ("RsP_un_demi_general",             "lemme",    "methode_spectral.thy", "1/t", 2),
    ("RsP_un_tiers_constant",           "theoreme", "methode_spectral.thy", "1/t", 2),
    ("RsP_un_quart_constant",           "theoreme", "methode_spectral.thy", "1/t", 2),
    ("prime_equation_for_primes_pos",   "lemme",    "methode_spectral.thy", "1/t", 2),
    ("reconstruction_premier_pos",      "theoreme", "methode_spectral.thy", "1/t", 2),
    ("asymetrie_implique_indices_valides","lemme",  "methode_spectral.thy", "1/t", 2),
    # Cercle 3 — Théorèmes d'exclusivité (preuve par l'absurde)
    ("composite_not_prime_i",           "theoreme", "methode_spectral.thy", "1/t", 3),
    ("spectral_method_exclusively_for_primes","theoreme","methode_spectral.thy","1/t",3),
    ("composite_no_reconstruction_position","theoreme","methode_spectral.thy","1/t",3),
    ("extraction_constante_A",          "theoreme", "methode_spectral.thy", "1/t", 3),
    ("extraction_constante_B",          "theoreme", "methode_spectral.thy", "1/t", 3),
    ("ecart_minimal_universel_A",       "theoreme", "methode_spectral.thy", "1/t", 3),
    ("ecart_minimal_universel_B",       "theoreme", "methode_spectral.thy", "1/t", 3),
    # Cercle 4 — Pont Savard (Section XIII) — cœur de RH
    ("ensemble_savard",                 "locale",   "methode_spectral.thy", "1/t", 4),
    ("ensemble_savard_satisfaisable",   "theoreme", "methode_spectral.thy", "1/t", 4),
    ("alignement_central",              "theoreme", "methode_spectral.thy", "1/t", 4),
    ("conclusion_ensemble",             "theoreme", "methode_spectral.thy", "1/t", 4),
    ("pont_spectral_direct_final",      "theoreme", "methode_spectral.thy", "1/t", 4),
    ("synthese_pont_savard",            "theoreme", "methode_spectral.thy", "1/t", 4),
    ("RsP_universel_entier_naturel",    "lemme",    "methode_spectral.thy", "1/t", 4),
]

# Sphère 1/x — Extensions géométriques + validation HOL unifiée
ENTITES_VAL = [
    # Cercle 1 — Redéfinitions validation (validation_hol_unifiee.thy)
    ("A_validation",                    "definition", "validation_hol_unifiee.thy", "1/x", 1),
    ("B_validation",                    "definition", "validation_hol_unifiee.thy", "1/x", 1),
    ("digamma_validation",              "definition", "validation_hol_unifiee.thy", "1/x", 1),
    ("Sr2_validation",                  "definition", "validation_hol_unifiee.thy", "1/x", 1),
    ("rsr_validation",                  "definition", "validation_hol_unifiee.thy", "1/x", 1),
    ("spectral_equation",               "definition", "validation_hol_unifiee.thy", "1/x", 1),
    ("prime_nth_reconstruction",        "definition", "validation_hol_unifiee.thy", "1/x", 1),
    # Cercle 2 — Rapports spectraux asymétriques (RSA)
    ("alternating_block_sum",           "definition", "validation_hol_unifiee.thy", "1/x", 2),
    ("RSA_ratio",                       "definition", "validation_hol_unifiee.thy", "1/x", 2),
    ("rsa_converges_to_half",           "definition", "validation_hol_unifiee.thy", "1/x", 2),
    ("RSA_convergence_implies_distance_decreasing","lemme","validation_hol_unifiee.thy","1/x",2),
    ("RSA_ratio_well_defined",          "lemme",      "validation_hol_unifiee.thy", "1/x", 2),
    # Cercle 3 — Zéros de Riemann et opérateur de Hilbert
    ("riemann_zero_critical",           "definition", "validation_hol_unifiee.thy", "1/x", 3),
    ("spectral_hilbert_operator",       "definition", "validation_hol_unifiee.thy", "1/x", 3),
    ("riemann_zeros_as_eigenvalues",    "definition", "validation_hol_unifiee.thy", "1/x", 3),
    ("spectral_hilbert_operator_on_critical_line","lemme","validation_hol_unifiee.thy","1/x",3),
    ("riemann_zeros_eigenvalues_correspondence","theoreme","validation_hol_unifiee.thy","1/x",3),
    ("classify_convergence_state",      "definition", "validation_hol_unifiee.thy", "1/x", 3),
    # Cercle 4 — Cohérence globale et reconstruction
    ("global_consistency",              "lemme",      "validation_hol_unifiee.thy", "1/x", 4),
    ("consistency_A_B_definitions",     "lemme",      "validation_hol_unifiee.thy", "1/x", 4),
    ("consistency_digamma_reconstruction","lemme",    "validation_hol_unifiee.thy", "1/x", 4),
    ("prime_reconstruction_validity",   "theoreme",   "validation_hol_unifiee.thy", "1/x", 4),
    ("Sr2_normalization_property",      "theoreme",   "validation_hol_unifiee.thy", "1/x", 4),
    ("distance_to_half_metric",         "lemme",      "validation_hol_unifiee.thy", "1/x", 4),
]

TOUTES_ENTITES = ENTITES_MS + ENTITES_THY + ENTITES_VAL

# ─────────────────────────────────────────────────────────────────────────────
#  Q&R TECHNIQUES (liste technique — 12 Q&R)
# ─────────────────────────────────────────────────────────────────────────────

QR_TECHNIQUES = [
    {
        "id": "QR_T01", "niveau": "expert",
        "source": "geometrie_du_spectre_premier.pdf",
        "question": "Calcul de la somme des éléments de la 1ère suite jusqu'à la position 11 — vérification √13827845",
        "resume": "Somme des racines carrées successives (√5 … √3932160) jusqu'au 11ème nombre premier",
        "categorie": "mathematique/calcul",
        "mots_cles": ["suite", "racine carree", "somme", "position", "premier", "tableau",
                      "SA", "SB", "digamma_calc"],
        "spheres": ["1/ms"],
    },
    {
        "id": "QR_T02", "niveau": "intermediaire",
        "source": "geometrie_du_spectre_premier.tex",
        "question": "Projection géométrique des nombres premiers vs isomorphisme harmonique",
        "resume": "Distinction projection géométrique / isomorphisme harmonique dans la Mécanique Harmonique du Chaos Discret",
        "categorie": "mathematique/comparaison",
        "mots_cles": ["projection", "geometrique", "isomorphisme", "harmonique", "chaos discret",
                      "SA_forme_generale", "SB_forme_generale"],
        "spheres": ["1/ms", "1/t"],
    },
    {
        "id": "QR_T03", "niveau": "avance",
        "source": "geometry_prime_spectrum.tex",
        "question": "Réduction successive par puissances de 2 — General Form of Sequences HOL Script",
        "resume": "Invariance numérique par réduction par facteurs de 2 dans les séquences HOL",
        "categorie": "mathematique/relation",
        "mots_cles": ["puissance", "reduction", "sequence", "HOL", "invariance",
                      "difference_SA_succ", "difference_SB_succ", "ratio_incremental_un_demi"],
        "spheres": ["1/ms", "1/t"],
    },
    {
        "id": "QR_T04", "niveau": "avance",
        "source": "geometry_prime_spectrum.tex",
        "question": "Constance du rapport spectral RsP_neg = 1/2 pour les suites négatives",
        "resume": "RsP_neg n1 n2 = 1/2 via axiome spectral_ratio_neg_un_demi pour n1,n2 ≤ -1",
        "categorie": "mathematique/geometrie",
        "mots_cles": ["RsP_neg", "rapport spectral", "1/2", "suite negative",
                      "SA_neg_eq", "SB_neg_eq", "spectral_ratio_neg_un_demi", "symetrie"],
        "spheres": ["1/ms", "1/x"],
    },
    {
        "id": "QR_T05", "niveau": "avance",
        "source": "geometry_prime_spectrum.tex",
        "question": "Théorème RsP_un_tiers_constant — rapport spectral 1/3 validation généralisée",
        "resume": "((73/9)/12)/(( 219/9)/12) = 1/3 via différences A_1_3 et B_1_3",
        "categorie": "mathematique/theoreme",
        "mots_cles": ["RsP_un_tiers_constant", "RsP_1_3", "1/3", "A_1_3", "B_1_3",
                      "rapport spectral", "theoreme", "validation"],
        "spheres": ["1/ms", "1/t"],
    },
    {
        "id": "QR_T06", "niveau": "intermediaire",
        "source": "geometry_prime_spectrum.tex",
        "question": "Quadrature parabolique d'Archimède vs modèle de Savard — aires géométriques",
        "resume": "Comparaison aires Tn/T_rest — ratio effectif 1/4 vs quadrature d'Archimède (4/3)",
        "categorie": "mathematique/comparaison",
        "mots_cles": ["quadrature", "parabole", "Archimede", "aire", "zeros critiques",
                      "droite critique", "1/4", "RSA_ratio", "RSA_convergence_implies_distance_decreasing",
                      "riemann_zero_critical"],
        "spheres": ["1/x"],
    },
    {
        "id": "QR_T07", "niveau": "avance",
        "source": "geometry_prime_spectrum.tex",
        "question": "Axiome mixed_gap_surplus et condition géométrique équivalente à la conjecture de Riemann",
        "resume": "mixed_gap_surplus → aires complémentaires → all_zeros_on_critical_line Re(s)=1/2",
        "categorie": "mathematique/theoreme",
        "mots_cles": ["conjecture Riemann", "zeros non triviaux", "1/2",
                      "all_zeros_on_critical_line", "riemann_zero_critical",
                      "riemann_zeros_as_eigenvalues", "ligne critique",
                      "pont_spectral_direct_final", "synthese_pont_savard"],
        "spheres": ["1/t", "1/x"],
    },
    {
        "id": "QR_T08", "niveau": "avance",
        "source": "geometry_prime_spectrum.tex",
        "question": "Démonstration de l'écart entre -31 et 17 via digamma — résultat 47",
        "resume": "(-22323135/20480 - 39280705/20480)/64 = -47 → 47 nombres entre -31 et 17",
        "categorie": "mathematique/demonstration",
        "mots_cles": ["digamma", "ecart", "demonstration", "64", "premiers negatifs",
                      "digamma_calc", "digamma_neg_calc", "SA_neg_eq", "SB_neg_eq",
                      "ecart_spectral_constant"],
        "spheres": ["1/ms", "1/x"],
    },
    {
        "id": "QR_T09", "niveau": "expert",
        "source": "methode_spectral.thy",
        "question": "Formalisation Isabelle/HOL — spectral_postulate_pos assure prime_equation n p = real p",
        "resume": "Axiome spectral_postulate_pos valide prime_equation via SB_affine_en_SA et ecart_spectral_constant",
        "categorie": "mathematique/structure_hol",
        "mots_cles": ["spectral_postulate_pos", "prime_equation", "Isabelle", "HOL",
                      "SB_affine_en_SA", "ecart_spectral_constant", "prime_equation_for_primes_pos",
                      "digamma_affine_en_SA", "axiome", "formalisation"],
        "spheres": ["1/ms", "1/t"],
    },
    {
        "id": "QR_T10", "niveau": "avance",
        "source": "methode_spectral.thy",
        "question": "Théorème comparaison asymétrique modèle 1/2 — signatures spectrales",
        "resume": "RsP_bloc_1_2 oscille près de 1/2 en mode chaotique — asymetrique_ordonnee_nat vs chaotique",
        "categorie": "mathematique/theoreme",
        "mots_cles": ["RsP_bloc_1_2", "asymetrique_ordonnee_nat", "asymetrique_chaotique_nat",
                      "1/2", "somme_SA_bloc", "somme_SB_bloc", "signature spectrale",
                      "indice_valide_nat", "RsP_un_demi_general"],
        "spheres": ["1/ms", "1/t"],
    },
    {
        "id": "QR_T11", "niveau": "expert",
        "source": "methode_spectral.thy",
        "question": "Validation Isabelle/HOL de spectral_ratio_neg_un_demi — indices asymétriques",
        "resume": "RsP_neg(n1,n2)=1/2 pour n1,n2 ≤ -1 via lemme RsP_un_demi_general et locale ensemble_savard",
        "categorie": "mathematique/structure_hol",
        "mots_cles": ["spectral_ratio_neg_un_demi", "RsP_un_demi_general", "Isabelle", "HOL",
                      "indice negatif", "asymetrique", "ensemble_savard",
                      "ensemble_savard_satisfaisable", "alignement_central",
                      "pont_spectral_direct_final"],
        "spheres": ["1/ms", "1/t"],
    },
    {
        "id": "QR_T12", "niveau": "avance",
        "source": "methode_spectral.thy",
        "question": "Formalisation HOL de la Geometry of Sequences — Section XIII Pont Savard",
        "resume": "Pont Savard : Ensemble=1/x+1/t+1/ms → RsP = Re(ρ) = 1/2 (theoreme synthese_pont_savard)",
        "categorie": "mathematique/demonstration",
        "mots_cles": ["Geometry of Sequences", "Isabelle", "HOL", "convergence",
                      "ensemble_savard", "synthese_pont_savard", "pont_spectral_direct_final",
                      "conclusion_ensemble", "RsP_universel_entier_naturel",
                      "reconstruction_premier_pos", "spectral_method_exclusively_for_primes"],
        "spheres": ["1/t", "1/x"],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
#  STRUCTURE ENSEMBLE = 1/ms + 1/t + 1/x  (Section XIII réelle)
# ─────────────────────────────────────────────────────────────────────────────

SPHERES = {
    "Ensemble": {
        "nom":        "Ensemble — Disque englobant",
        "equation":   "Ensemble = 1  ↔  1/x + 1/t + 1/ms",
        "description":"L'ensemble complet Univers-au-carré représenté par la constante 1. Trois vues équivalentes forcent RsP = Re(ρ) = 1/2.",
        "rayon":      100,
        "qr":         [],
    },
    "1/ms": {
        "nom":        "1/ms — Méthode Spectrale",
        "equation":   "1/ms = 1/ms1 + 1/ms2 + 1/ms3",
        "description":"Noyau algorithmique : suites SA/SB, rapports RsP, digamma. 154 définitions, 148 lemmes.",
        "rayon":      70,
        "concordance":"(2) 1/y3 = 1/ms1 — Zéros non-triviaux de zeta = valeurs de n",
        "qr":         ["QR_T01","QR_T02","QR_T03","QR_T04","QR_T05","QR_T08","QR_T09","QR_T10","QR_T11"],
        "cercles": [
            {"niveau": 1, "nom": "Suites fondamentales SA/SB",
             "entites": ["SA","SB","A_1_3","B_1_3","A_1_4","B_1_4","digamma_calc","prime_equation"]},
            {"niveau": 2, "nom": "Rapports spectraux RsP",
             "entites": ["RsP","RsP_1_3","RsP_1_4","RsP_nn","RsP_neg","RsP_bloc_1_2"]},
            {"niveau": 3, "nom": "Conditions et indices",
             "entites": ["indice_valide","asymetrique_ordonnee","asymetrique_chaotique","asymetrique_ordonnee_nat","asymetrique_chaotique_nat"]},
            {"niveau": 4, "nom": "Postulats axiomatiques",
             "entites": ["spectral_postulate_pos","spectral_postulate_1_3","spectral_postulate_1_4","spectral_ratio_neg_un_demi","spectral_ratio_neg_un_tiers"]},
        ],
    },
    "1/t": {
        "nom":        "1/t — psi_savard / Théorèmes HOL",
        "equation":   "1/t  (psi_savard ≡ Tchebychev sur la Suite B)",
        "description":"27 théorèmes formels Isabelle/HOL. Section XIII : Pont Savard → RsP = Re(ρ) = 1/2.",
        "rayon":      70,
        "concordance":"(1) 1/y1 = 1/t — Tchebychev = psi_savard (validations XIII.2)",
        "qr":         ["QR_T02","QR_T03","QR_T05","QR_T07","QR_T09","QR_T10","QR_T11","QR_T12"],
        "cercles": [
            {"niveau": 1, "nom": "Lemmes algébriques fondamentaux",
             "entites": ["SA_forme_generale","SB_forme_generale","SB_affine_en_SA","ecart_spectral_constant","digamma_affine_en_SA"]},
            {"niveau": 2, "nom": "Théorèmes spectraux centraux",
             "entites": ["RsP_un_demi_general","RsP_un_tiers_constant","RsP_un_quart_constant","prime_equation_for_primes_pos"]},
            {"niveau": 3, "nom": "Preuves par l'absurde (exclusivité P)",
             "entites": ["composite_not_prime_i","spectral_method_exclusively_for_primes","composite_no_reconstruction_position"]},
            {"niveau": 4, "nom": "Pont Savard — Section XIII",
             "entites": ["ensemble_savard","ensemble_savard_satisfaisable","alignement_central","pont_spectral_direct_final","synthese_pont_savard"]},
        ],
    },
    "1/x": {
        "nom":        "1/x — zeta / Extensions géométriques",
        "equation":   "1/x = 1/y1 + 1/y2 + 1/y3  (décomposition de zeta)",
        "description":"Extensions géométriques + validation HOL unifiée. La correspondance aux zéros de Riemann est réfutée pour l'opérateur défini.",
        "rayon":      70,
        "concordance":"(3) 1/y2 = 1/ms3 — Re(ρ) = 1/2 = RsP = 1/2",
        "qr":         ["QR_T04","QR_T06","QR_T07","QR_T08","QR_T12"],
        "cercles": [
            {"niveau": 1, "nom": "Redéfinitions de validation",
             "entites": ["A_validation","B_validation","digamma_validation","spectral_equation","prime_nth_reconstruction"]},
            {"niveau": 2, "nom": "Rapports spectraux asymétriques (RSA)",
             "entites": ["alternating_block_sum","RSA_ratio","rsa_converges_to_half","RSA_convergence_implies_distance_decreasing"]},
            {"niveau": 3, "nom": "Zéros de Riemann — opérateur de Hilbert",
             "entites": ["riemann_zero_critical","spectral_hilbert_operator","riemann_zeros_as_eigenvalues","riemann_zeros_eigenvalues_correspondence"]},
            {"niveau": 4, "nom": "Cohérence globale et reconstruction",
             "entites": ["global_consistency","prime_reconstruction_validity","Sr2_normalization_property","distance_to_half_metric"]},
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
#  CLASSE EXTRACTEUR
# ─────────────────────────────────────────────────────────────────────────────

class ExtracteurKeywordsHOL:

    def __init__(self):
        self.entites_extraites: dict[str, list[dict]] = defaultdict(list)
        self.occurrences: dict[str, int] = defaultdict(int)
        self.associations: list[dict] = []

    def lire(self, chemin: Path) -> str:
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                txt = chemin.read_text(encoding=enc)
                print(f"    ✓ {chemin.name}  ({len(txt):,} chars, {txt.count(chr(10))} lignes, {enc})")
                return txt
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        print(f"    ✗ Impossible de lire {chemin}")
        return ""

    def extraire_depuis_contenu(self, contenu: str, source: str):
        """Extrait toutes les entités HOL nommées d'un fichier .thy"""
        lignes = contenu.split('\n')
        for type_hol, pat in PATTERNS_HOL.items():
            for m in pat.finditer(contenu):
                nom = m.group(1)
                if not nom or len(nom) < 2:
                    continue
                ligne_num = contenu[:m.start()].count('\n') + 1
                debut = max(0, ligne_num - 2)
                fin   = min(len(lignes), ligne_num + 3)
                ctx   = ' '.join(lignes[debut:fin]).strip()[:250]
                self.entites_extraites[type_hol].append({
                    "nom":     nom,
                    "ligne":   ligne_num,
                    "source":  source,
                    "contexte": ctx,
                })
                self.occurrences[nom] += 1

    def score_assoc(self, mots_cles: list[str], nom_entite: str) -> float:
        n = nom_entite.lower()
        score = 0.0
        for mc in mots_cles:
            m = mc.lower().replace(' ', '_')
            if m == n:                                         score += 1.0
            elif m in n or n in m:                             score += 0.6
            elif any(t in n for t in m.split('_') if len(t)>3): score += 0.3
        return min(round(score, 3), 1.0)

    def associer_qr(self):
        # Index : nom_entite → (type, sphere, cercle)
        idx_entites = {e[0]: e for e in TOUTES_ENTITES}
        # Enrichir avec entités extraites dynamiquement
        for t, lst in self.entites_extraites.items():
            for e in lst:
                if e["nom"] not in idx_entites:
                    idx_entites[e["nom"]] = (e["nom"], t, e["source"], None, None)

        for qr in QR_TECHNIQUES:
            assocs = []
            for nom, (nom2, type_hol, src, sphere, cercle) in idx_entites.items():
                sc = self.score_assoc(qr["mots_cles"], nom)
                if sc >= 0.3:
                    assocs.append({
                        "entite": nom, "type": type_hol,
                        "source": src, "sphere": sphere,
                        "cercle": cercle, "score": sc,
                    })
            assocs.sort(key=lambda x: x["score"], reverse=True)
            self.associations.append({
                "qr_id":             qr["id"],
                "niveau":            qr["niveau"],
                "source_thy":        qr["source"],
                "question":          qr["question"],
                "resume":            qr["resume"],
                "categorie":         qr["categorie"],
                "mots_cles":         qr["mots_cles"],
                "spheres_ensemble":  qr["spheres"],
                "entites_top15":     assocs[:15],
                "nb_entites":        len(assocs),
            })

    def exporter(self, sortie: Path):
        data = {
            "meta": {
                "date_generation":  datetime.now().isoformat(),
                "description":      "Pipeline cognitif Gabriel — Étape 1 : Q&R ↔ entités HOL",
                "equation_centrale":"Ensemble = 1  ↔  1/x + 1/t + 1/ms",
                "nb_qr":            len(QR_TECHNIQUES),
                "nb_entites_connues": len(TOUTES_ENTITES),
                "nb_entites_extraites": sum(len(v) for v in self.entites_extraites.values()),
            },
            "spheres_ensemble":           SPHERES,
            "entites_fondamentales": [
                {"nom": e[0], "type": e[1], "source": e[2], "sphere": e[3], "cercle": e[4]}
                for e in TOUTES_ENTITES
            ],
            "entites_extraites_dynamiques": {k: v for k, v in self.entites_extraites.items()},
            "occurrences_top30":          dict(sorted(self.occurrences.items(), key=lambda x: -x[1])[:30]),
            "associations_qr_entites":    self.associations,
        }
        sortie.parent.mkdir(parents=True, exist_ok=True)
        with open(sortie, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ gabriel_keywords_qr_map.json → {sortie}")
        print(f"     {len(self.associations)} associations Q&R ↔ entités HOL")

    def executer(self):
        print("\n" + "="*70)
        print("  GABRIEL P1 — EXTRACTEUR MOTS-CLÉS HOL")
        print("  Équation : Ensemble = 1  ↔  1/x + 1/t + 1/ms")
        print("="*70)

        # Lecture des .thy
        print("\n[1/4] Lecture des fichiers Isabelle/HOL...")
        ms_path  = trouver_fichier(CANDIDATS_MS)
        val_path = trouver_fichier(CANDIDATS_VAL)

        if ms_path:
            self.extraire_depuis_contenu(self.lire(ms_path),  "methode_spectral.thy")
        else:
            print("    ⚠  methode_spectral.thy introuvable — utilisation du catalogue intégré")

        if val_path:
            self.extraire_depuis_contenu(self.lire(val_path), "validation_hol_unifiee.thy")
        else:
            print("    ⚠  validation_hol_unifiee.thy introuvable — catalogue intégré uniquement")

        # Résumé extraction
        print("\n[2/4] Entités extraites dynamiquement :")
        for t, lst in self.entites_extraites.items():
            print(f"    {t:25s} : {len(lst):4d}")

        print("\n[3/4] Association Q&R ↔ entités HOL...")
        self.associer_qr()
        for a in self.associations:
            sph = ", ".join(a["spheres_ensemble"])
            print(f"    {a['qr_id']} | {a['nb_entites']:3d} entités | sphères: {sph}")

        print("\n[4/4] Export JSON...")
        self.exporter(SORTIE)
        print("\n  ⏭  Prochaine étape : python gabriel_p2_sqlite_builder.py")
        print("="*70 + "\n")


if __name__ == "__main__":
    ExtracteurKeywordsHOL().executer()
