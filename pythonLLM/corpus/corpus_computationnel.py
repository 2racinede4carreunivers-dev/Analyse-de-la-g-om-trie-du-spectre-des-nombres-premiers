# -*- coding: utf-8 -*-
"""
corpus/corpus_computationnel.py — corpus normatif encode (source de verite).

Ce module ne contient aucune logique : uniquement des donnees. Il est la
« matiere » que le constructeur de base SQLite va encoder. Le corpus reflete
la demande : six champs de connaissance computationnelle, des institutions de
normalisation/reglementation (ISO, IEEE, W3C, droit UE, philosophie), des
notions (termes de reconnaissance), des invariants deontiques et des regles
d'intention ordonnees.

Aucune donnee n'est probabiliste : chaque liste est un ensemble ferme et
ordonne de maniere deterministe.
"""
from __future__ import annotations

from ..modele.entites import (
    ChampConnaissance,
    Institution,
    Invariant,
    RegleIntention,
)
from .notions import (
    TOUTES_NOTIONS,
    NOTIONS_LOGIQUE,
    NOTIONS_ALGEBRE,
    NOTIONS_ARITHMETIQUE,
    NOTIONS_GEOMETRIE,
    NOTIONS_STATISTIQUES,
    NOTIONS_COMPILATION,
)
# 9 institutions tracees (licence + acces + url) : source unique verifiee.
from .institutions import INSTITUTIONS, PROVENANCE

__all__ = [
    "CHAMPS",
    "INSTITUTIONS",
    "INVARIANTS",
    "REGLES_INTENTION",
    "TOUTES_NOTIONS",
    "NOTIONS_LOGIQUE",
    "NOTIONS_ALGEBRE",
    "NOTIONS_ARITHMETIQUE",
    "NOTIONS_GEOMETRIE",
    "NOTIONS_STATISTIQUES",
    "NOTIONS_COMPILATION",
]

# =============================================================================
# SIX CHAMPS DE CONNAISSANCE COMPUTATIONNELLE
# (poids = ordre total de priorite en cas d'egalite de score)
# =============================================================================
CHAMPS: tuple[ChampConnaissance, ...] = (
    ChampConnaissance(
        code="LOGIQUE",
        libelle="Logique formelle et demonstration",
        poids=1,
        description=(
            "Socle ontologique du code : calculabilite, correspondance de "
            "Curry-Howard, logiques modale, temporelle et deontique."
        ),
    ),
    ChampConnaissance(
        code="ALGEBRE",
        libelle="Algebre et theorie des types",
        poids=2,
        description=(
            "Structure des donnees et des contraintes : algebre universelle, "
            "categories, algebre de Boole, sous-typage."
        ),
    ),
    ChampConnaissance(
        code="ARITHMETIQUE",
        libelle="Arithmetique et theorie des nombres",
        poids=3,
        description=(
            "Calcul discret et securise : arithmetique modulaire, corps finis, "
            "analyse numerique et erreurs d'arrondi (IEEE 754)."
        ),
    ),
    ChampConnaissance(
        code="GEOMETRIE",
        libelle="Geometrie et topologie",
        poids=4,
        description=(
            "Espace, forme et structures relationnelles : geometrie "
            "algorithmique, topologie computationnelle, theorie des graphes."
        ),
    ),
    ChampConnaissance(
        code="STATISTIQUES",
        libelle="Statistiques et probabilites computationnelles",
        poids=5,
        description=(
            "Calcul de l'incertain : inference, chaines de Markov, theorie de "
            "l'information et entropie de Shannon."
        ),
    ),
    ChampConnaissance(
        code="COMPILATION",
        libelle="Analyse formelle et compilation",
        poids=6,
        description=(
            "Pipeline de validation : semantiques (denotationnelle, "
            "operationnelle, axiomatique) et analyse statique de code."
        ),
    ),
)

# =============================================================================
# INSTITUTIONS — defini dans corpus/institutions.py (9 institutions tracees :
# UE AI Act, RGPD, ISO/IEC, IEEE, W3C, philosophie, MATHLIB, SMC-CMC).
# Chaque institution y porte sa provenance exacte (PROVENANCE : licence,
# acces, url). Voir : from .institutions import INSTITUTIONS, PROVENANCE
# =============================================================================

# =============================================================================
# INVARIANTS DEONTIQUES — regles formelles permanentes par champ
# (severite dans l'ensemble ferme : obligation | interdiction | permission)
# =============================================================================
INVARIANTS: tuple[Invariant, ...] = (
    Invariant(
        "INV-NO-INVENTION", "LOGIQUE",
        "Toute commande emise doit reposer sur des termes reconnus du corpus ; "
        "a defaut, le pipeline emet un refus formel et n'invente aucune option.",
        "obligation",
    ),
    Invariant(
        "INV-NO-ALEATOIRE", "STATISTIQUES",
        "Aucun tirage aleatoire ni similarite approxee : la classification est "
        "un ordre total deterministe.",
        "interdiction",
    ),
    Invariant(
        "INV-EXACTITUDE", "ARITHMETIQUE",
        "Les scores sont calcules en arithmetique exacte (Fraction), jamais en "
        "flottant IEEE 754, pour maitriser toute erreur d'arrondi.",
        "obligation",
    ),
    Invariant(
        "INV-CURRY-HOWARD", "LOGIQUE",
        "Les types de la commande generee correspondent a des propositions "
        "valides : aucune option hors de sa grammaire de valeurs.",
        "obligation",
    ),
    Invariant(
        "INV-DEONTIQUE", "LOGIQUE",
        "Les obligations, interdictions et permissions du corpus normatif "
        "regissent les combinaisons d'options (exclusions mutuelles).",
        "obligation",
    ),
    Invariant(
        "INV-SOUS-TYPAGE", "ALGEBRE",
        "Deux champs de types distincts ne sont jamais amalgames : chaque "
        "option porte une valeur de son propre domaine.",
        "obligation",
    ),
    Invariant(
        "INV-754", "ARITHMETIQUE",
        "Les valeurs numeriques emises respectent la representation discrete "
        "des machines (norme IEEE 754) : pas de flottant non maitrise.",
        "obligation",
    ),
    Invariant(
        "INV-GRAPHE", "GEOMETRIE",
        "Une requete portant sur une structure relationnelle (graphe, arbre) "
        "est classee selon sa connexite, jamais melangee a un calcul scalaire.",
        "obligation",
    ),
    Invariant(
        "INV-ENTROPIE", "STATISTIQUES",
        "La probabilite ne sert qu'a nommer l'incertain, jamais a choisir une "
        "branche : la decision reste reglee par les regles ordonnees.",
        "interdiction",
    ),
    Invariant(
        "INV-ANALYSE-STATIQUE", "COMPILATION",
        "La commande est validee sans execution, par verification d'invariants "
        "de grammaire et de deontologie avant emission.",
        "obligation",
    ),
    Invariant(
        "INV-CONFORMITE", "COMPILATION",
        "La commande doit rester conforme au cadre normatif (droit, normes) "
        "encode dans le corpus.",
        "obligation",
    ),
)

# =============================================================================
# REGLES D'INTENTION ORDONNEES
# (ordre total : priorite distincte. La 1re regle dont la condition est
#  satisfaite gagne ; jamais d'egalite, jamais de tirage.)
# =============================================================================
REGLES_INTENTION: tuple[RegleIntention, ...] = (
    RegleIntention(
        priorite=1,
        intention="structure_graphe",
        condition="La requete nomme une structure relationnelle (graphe, arbre, foret, reseau, AST).",
        champ_requis="GEOMETRIE",
        mots_declencheurs=("graphe", "graphes", "arbre", "arbres", "foret",
                           "reseau", "connexite", "ast"),
    ),
    RegleIntention(
        priorite=2,
        intention="preuve_formelle",
        condition="La requete nomme la demonstration, la preuve ou un assistant de preuve.",
        champ_requis="LOGIQUE",
        mots_declencheurs=("demonstration", "demontrable", "preuve", "assistant",
                           "isabelle", "lean", "verification", "certitude"),
    ),
    RegleIntention(
        priorite=3,
        intention="calcul_exact",
        condition="La requete nomme un calcul discret ou securise (modulaire, corps fini, entier).",
        champ_requis="ARITHMETIQUE",
        mots_declencheurs=("modulaire", "modulo", "corps", "entier", "discret",
                           "cryptographie", "chiffrement"),
    ),
    RegleIntention(
        priorite=4,
        intention="conformite_normative",
        condition="La requete nomme une regle, une conformite ou une obligation normative.",
        champ_requis="COMPILATION",
        mots_declencheurs=("regle", "conformite", "obligation", "interdiction",
                           "permission", "specification"),
    ),
    RegleIntention(
        priorite=5,
        intention="validation_code",
        condition="La requete nomme la compilation, l'analyse statique ou la semantique.",
        champ_requis="COMPILATION",
        mots_declencheurs=("compilation", "compilateur", "statique", "analyse",
                           "semantique", "moteur"),
    ),
    RegleIntention(
        priorite=6,
        intention="modelisation_incertaine",
        condition="La requete nomme le probabiliste, l'inference ou l'entropie.",
        champ_requis="STATISTIQUES",
        mots_declencheurs=("probabilite", "probabiliste", "inference", "markov",
                           "entropie", "shannon", "stochastique"),
    ),
    RegleIntention(
        priorite=7,
        intention="analyse_generale",
        condition="Regle par defaut : au moins une notion du corpus est reconnue, sans specialisation.",
        champ_requis=None,
        mots_declencheurs=(),
    ),
)

