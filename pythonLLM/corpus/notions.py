# -*- coding: utf-8 -*-
"""
corpus/notions.py — lexique de reconnaissance (termes -> champ de connaissance).

Chaque ``lemme`` est la forme deja normalisee (minuscule, sans accents, un seul
mot) que produit ``moteur.normalisation``. La reconnaissance est une simple
appartenance a un ensemble : aucun rapprochement approximatif.

``graphe=True`` marque les termes designant une structure relationnelle
(arbre, graphe, foret) : ils orientent la construction vers une intention
« structure / analyse de relations » plutot que « calcul ».
"""
from __future__ import annotations

from ..modele.entites import Notion

# LOGIQUE — calculabilite, Curry-Howard, logiques modale/temporelle/deontique
NOTIONS_LOGIQUE: tuple[Notion, ...] = (
    Notion("demonstration", "LOGIQUE", "PHILO-LANGAGE"),
    Notion("demontrable", "LOGIQUE", "PHILO-LANGAGE"),
    Notion("calculabilite", "LOGIQUE"),
    Notion("turing", "LOGIQUE", "IEEE"),
    Notion("recursive", "LOGIQUE"),
    Notion("recursif", "LOGIQUE"),
    Notion("indecidabilite", "LOGIQUE"),
    Notion("godel", "LOGIQUE"),
    Notion("arret", "LOGIQUE"),
    Notion("curry", "LOGIQUE", "PHILO-LANGAGE"),
    Notion("howard", "LOGIQUE"),
    Notion("isomorphisme", "LOGIQUE"),
    Notion("proposition", "LOGIQUE"),
    Notion("preuve", "LOGIQUE", "PHILO-LANGAGE"),
    Notion("assistant", "LOGIQUE"),
    Notion("isabelle", "LOGIQUE"),
    Notion("lean", "LOGIQUE"),
    Notion("modal", "LOGIQUE"),
    Notion("temporelle", "LOGIQUE"),
    Notion("deontique", "LOGIQUE", "UE-AI-ACT"),
    Notion("obligation", "LOGIQUE", "UE-AI-ACT"),
    Notion("interdiction", "LOGIQUE", "UE-AI-ACT"),
    Notion("permission", "LOGIQUE", "UE-AI-ACT"),
    Notion("verification", "LOGIQUE"),
    Notion("certitude", "LOGIQUE"),
)

# ALGEBRE — theorie des types, categories, Boole, sous-typage
NOTIONS_ALGEBRE: tuple[Notion, ...] = (
    Notion("type", "ALGEBRE", "ISO-IEC-2382"),
    Notion("types", "ALGEBRE", "ISO-IEC-2382"),
    Notion("categorie", "ALGEBRE"),
    Notion("foncteur", "ALGEBRE"),
    Notion("monade", "ALGEBRE"),
    Notion("monoide", "ALGEBRE"),
    Notion("boole", "ALGEBRE"),
    Notion("booleen", "ALGEBRE"),
    Notion("bool", "ALGEBRE"),
    Notion("combinatoire", "ALGEBRE"),
    Notion("sous", "ALGEBRE"),
    Notion("typage", "ALGEBRE"),
    Notion("contrainte", "ALGEBRE"),
    Notion("invariant", "ALGEBRE"),
    Notion("algebre", "ALGEBRE"),
    Notion("masque", "ALGEBRE"),
)

# ARITHMETIQUE — modulaire, corps finis, analyse numerique / IEEE 754
NOTIONS_ARITHMETIQUE: tuple[Notion, ...] = (
    Notion("modulaire", "ARITHMETIQUE"),
    Notion("modulo", "ARITHMETIQUE"),
    Notion("corps", "ARITHMETIQUE"),
    Notion("fini", "ARITHMETIQUE"),
    Notion("cryptographie", "ARITHMETIQUE"),
    Notion("chiffrement", "ARITHMETIQUE"),
    Notion("hachage", "ARITHMETIQUE"),
    Notion("signature", "ARITHMETIQUE"),
    Notion("numerique", "ARITHMETIQUE"),
    Notion("arrondi", "ARITHMETIQUE", "IEEE"),
    Notion("flottant", "ARITHMETIQUE", "IEEE"),
    Notion("754", "ARITHMETIQUE", "IEEE"),
    Notion("ieee", "ARITHMETIQUE", "IEEE"),
    Notion("entier", "ARITHMETIQUE"),
    Notion("discret", "ARITHMETIQUE"),
)

# GEOMETRIE — geometrie algorithmique, topologie, theorie des graphes
NOTIONS_GEOMETRIE: tuple[Notion, ...] = (
    Notion("geometrie", "GEOMETRIE"),
    Notion("geometrique", "GEOMETRIE"),
    Notion("espace", "GEOMETRIE"),
    Notion("vectoriel", "GEOMETRIE"),
    Notion("vecteur", "GEOMETRIE"),
    Notion("matrice", "GEOMETRIE"),
    Notion("coordonnee", "GEOMETRIE"),
    Notion("topologie", "GEOMETRIE"),
    Notion("graphe", "GEOMETRIE", graphe=True),
    Notion("graphes", "GEOMETRIE", graphe=True),
    Notion("arbre", "GEOMETRIE", graphe=True),
    Notion("arbres", "GEOMETRIE", graphe=True),
    Notion("foret", "GEOMETRIE", graphe=True),
    Notion("reseau", "GEOMETRIE", graphe=True),
    Notion("connexite", "GEOMETRIE", graphe=True),
    Notion("maille", "GEOMETRIE"),
    Notion("surface", "GEOMETRIE"),
    Notion("rendu", "GEOMETRIE"),
)

# STATISTIQUES — inference, chaines de Markov, theorie de l'information
NOTIONS_STATISTIQUES: tuple[Notion, ...] = (
    Notion("probabilite", "STATISTIQUES"),
    Notion("probabiliste", "STATISTIQUES"),
    Notion("statistique", "STATISTIQUES"),
    Notion("inference", "STATISTIQUES"),
    Notion("markov", "STATISTIQUES"),
    Notion("stochastique", "STATISTIQUES"),
    Notion("entropie", "STATISTIQUES"),
    Notion("shannon", "STATISTIQUES"),
    Notion("information", "STATISTIQUES"),
    Notion("compression", "STATISTIQUES"),
    Notion("aleatoire", "STATISTIQUES"),
    Notion("transition", "STATISTIQUES"),
    Notion("incertain", "STATISTIQUES"),
)

# COMPILATION — semantiques, analyse statique, methodes formelles
NOTIONS_COMPILATION: tuple[Notion, ...] = (
    Notion("semantique", "COMPILATION"),
    Notion("denotationnelle", "COMPILATION"),
    Notion("operationnelle", "COMPILATION"),
    Notion("axiomatique", "COMPILATION"),
    Notion("compilation", "COMPILATION"),
    Notion("compilateur", "COMPILATION"),
    Notion("statique", "COMPILATION"),
    Notion("analyse", "COMPILATION"),
    Notion("specification", "COMPILATION"),
    Notion("conformite", "COMPILATION", "UE-AI-ACT"),
    Notion("regle", "COMPILATION", "UE-AI-ACT"),
    Notion("moteur", "COMPILATION"),
    Notion("ast", "COMPILATION", graphe=True),
    Notion("syntaxique", "COMPILATION", graphe=True),
)

# Agregat ordonne et deterministe de toutes les notions.
TOUTES_NOTIONS: tuple[Notion, ...] = (
    NOTIONS_LOGIQUE
    + NOTIONS_ALGEBRE
    + NOTIONS_ARITHMETIQUE
    + NOTIONS_GEOMETRIE
    + NOTIONS_STATISTIQUES
    + NOTIONS_COMPILATION
)
