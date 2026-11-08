# -*- coding: utf-8 -*-
"""
corpus/institutions.py — institutions du corpus, avec sources verifiables.

Chaque institution porte :
- son identifiant, nom, type et autorite (rang normatif) ;
- son perimetre d'usage dans le pipeline ;
- sa provenance exacte : ``licence`` + ``acces`` (telechargeable, manuel,
  reference-seule) + ``url`` de verification.

Convention de traçabilite (aucune invention) :
- ``acces="direct"`` : texte integral librement telechargeable ;
- ``acces="manuel"`` : l'utilisateur fournit le fichier (PDF/HTML) une fois,
  le SHA-256 est consigne ici ;
- ``acces="reference"`` : on ne cite que numero/titre (texte payant/ferme).
"""
from __future__ import annotations

from ..modele.entites import Institution

INSTITUTIONS: tuple[Institution, ...] = (
    # --- Droit UE : acces manuel (EUR-Lex bloque les robots) ---
    Institution(
        "UE-AI-ACT",
        "Reglement (UE) 2024/1689 — Intelligence Artificielle (AI Act)",
        "droit", autorite=1,
        perimetre="Cadre juridique europeen sur l'IA ; empeche la redefinition unilateral de notions fondamentales.",
    ),
    Institution(
        "UE-RGPD",
        "Reglement (UE) 2016/679 — Protection des donnees (RGPD)",
        "droit", autorite=2,
        perimetre="Consentement, vie privee, responsabilite du traitement automatise.",
    ),
    # --- Normes payantes : reference seule (aucun texte ingere) ---
    Institution(
        "ISO-IEC-22989",
        "ISO/IEC 22989 — Concepts et terminologie de l'IA",
        "norme", autorite=3,
        perimetre="Fixation des definitions rigoureuses des termes techniques de l'IA.",
    ),
    Institution(
        "ISO-IEC-2382",
        "ISO/IEC 2382 — Vocabulaire des technologies de l'information",
        "norme", autorite=4,
        perimetre="Frontieres lexicales etanches entre concepts numeriques.",
    ),
    Institution(
        "IEEE",
        "IEEE — Institut des ingenieurs electriciens et electroniciens",
        "norme", autorite=5,
        perimetre="Standards techniques ; norme IEEE 754 (nombres flottants).",
    ),
    # --- W3C : textes integraux libres (telechargeables) ---
    Institution(
        "W3C",
        "W3C — World Wide Web Consortium",
        "norme", autorite=6,
        perimetre="Standards du web et semantique formelle des donnees liees.",
    ),
    # --- Philosophie : pas d'instance unique ---
    Institution(
        "PHILO-LANGAGE",
        "Philosophie du langage et epistemologie (Wittgenstein, Bachelard)",
        "philosophie", autorite=7,
        perimetre="Sens et usage des mots ; rupture epistemologique ; critique du glissement semantique.",
    ),
    # --- Mathlib : depot local Apache 2.0 (extraction deterministe) ---
    Institution(
        "MATHLIB",
        "Mathlib — bibliotheque formelle Lean 4 (Apache 2.0, depot local)",
        "universite", autorite=8,
        perimetre="Comparable universitaire : notions extraites REELLEMENT des .lean, provenance fichier:ligne.",
    ),
    # --- SMC : deux revues DISTINCTES (verifiees sur licence.rnbm.org) ---
    # Crux Mathematicorum : libre en lecture, MAIS copie = usage personnel
    # uniquement (copyright CMS) -> reference seule, aucun corpus ingere.
    Institution(
        "SMC-CRUX",
        "SMC — Crux Mathematicorum (lecture libre, copie usage personnel)",
        "universite", autorite=9,
        perimetre="Problemes et solutions ; consultation seule (copyright : "
                  "copie strictement personnelle, aucune reutilisation).",
    ),
    # Canadian Mathematical Communications : Gold OA verifie (ISSN 2976-8594).
    Institution(
        "SMC-CMC",
        "SMC — Canadian Mathematical Communications (Gold OA, ISSN 2976-8594)",
        "universite", autorite=10,
        perimetre="Comparable canadien ouvert : articles longs (>= 41 pages), "
                  "anglais ou francais ; titres d'articles encodes avec "
                  "provenance et SHA-256 de la page journal.",
    ),
)

# Provenance exacte par institution : (licence, acces, url).
PROVENANCE: dict[str, tuple[str, str, str]] = {
    "UE-AI-ACT": ("droit public UE, Decision 2011/833/UE (reutilisation libre)",
                  "direct",
                  "http://publications.europa.eu/resource/celex/32024R1689"),
    "UE-RGPD": ("droit public UE, Decision 2011/833/UE (reutilisation libre)",
                "direct",
                "http://publications.europa.eu/resource/celex/32016R0679"),
    "ISO-IEC-22989": ("payante (boutique ISO)", "reference",
                      "https://www.iso.org/standard/74296.html"),
    "ISO-IEC-2382": ("payante (boutique ISO)", "reference",
                     "https://www.iso.org/standard/63598.html"),
    "IEEE": ("payante (IEEE Xplore)", "reference",
             "https://standards.ieee.org/ieee/754/6210/"),
    "W3C": ("W3C Document License (libre)", "direct",
            "https://www.w3.org/TR/skos-reference/"),
    "PHILO-LANGAGE": ("droits variables selon editions", "reference", ""),
    "MATHLIB": ("Apache 2.0", "direct",
                "C:/Users/Utilisateur/OneDrive/Mathlib"),
    "SMC-CRUX": ("copyright SMC — copie pour usage personnel uniquement",
                 "reference", "https://cms.math.ca/crux/"),
    "SMC-CMC": ("Gold OA (Cambridge Core, ISSN 2976-8594)", "direct",
                "https://www.cambridge.org/core/journals/"
                "canadian-mathematical-communications"),
}
