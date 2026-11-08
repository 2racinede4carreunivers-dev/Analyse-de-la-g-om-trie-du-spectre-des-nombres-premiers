#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
formateur_multi_ratio.py — Reponse formelle GENERALISEE multi-rapports 1/k.
================================================================================
CABLAGE SEUL : ne contient aucun calcul spectral, aucune equation modifiee.
Reutilise exclusivement les API existantes du pipeline cognitif :
  - MultiRatioDispatcher.requete_plage(n, k_debut, k_fin) / rapport_texte / tableau_texte
  - gabriel_multi_ratio_n_commun(n, liste_k)
  - Suites_geometriques_AB / metaphore_geometrique (gabarits de presentation)

Limite agent : K_MAX_AGENT = 1_000_000 (commodite d'affichage / temps session).
Le pipeline supporte jusqu'a 1e13 : ce module plafonne uniquement la reponse
interactive (refus formel + conseil de sous-plages au-dela).

Format de reponse impose (demande utilisateur) :
  1. resultat reconstruction P(n) par rapport (systeme convolutif + 2 niveaux)
  2. pour non-typiques : sommes A/B n=10 et n=9 + extrait HOL du rapport 1/k
  3. pour non-typiques multiples : exemple generalise (suites geometriques,
     4 Digamma, coefficients A/B, equations (Coeff)/x*k^n-Reste=Somme)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

_RACINE = Path(__file__).resolve().parents[2]
if str(_RACINE) not in sys.path:
    sys.path.insert(0, str(_RACINE))

from src.dispatch.multi_ratio_parser import K_MAX_AGENT, SpecMultiRatio  # noqa: E402

_GABARIT_HOL = """HOL (Section XIV, extrait 1/k, k={k}) :
  alphaA(k) = 2(k^4 - k^2 + 1)/((k-1)*k^3) ; alphaB(k) = k*alphaA(k)
  deltaA(k) = k/(k-1) ; deltaB(k) = (k^7 - k^6 + k)/(k-1)
  SA(k,n) = (alphaA(k)/2)*k^n - deltaA(k)
  SB(k,n) = (alphaB(k)/2)*k^n - deltaB(k)
  Invariant : (SA(k,n1)-SA(k,n2))/(SB(k,n1)-SB(k,n2)) = 1/k
  Ancrage n=10 (4 Digamma, ordre deterministe) :
    1) SA- k^8  2) SA + k^8  3) SA + k^7  4) SA - k^7
  P(1/{k},n=10) = (SB - Digamma)/k^6  [premier candidat premier]
  n != 10 : rang_cible = rang_base + (n-10) ; P = premier(rang_cible)"""

_GABARIT_SUITES_GENERALISE = """Exemple generalise non-typiques (n=10 / n=9, niveau 1 entier) :
Suites A/B 10 termes (n=10) et 9 termes (n=9) : construction terme a terme
  i<=n-2 : k^i (avec saut Zeta i=6 -> k^7 cote B) ;
  i=n-1 : k^(n-1)-k^(n-3) / k^n-k^(n-2) ; i=n : k^n-k^(n-2) / k^(n+1)-k^(n-1).
4 Digamma : SA-t^8, SA+t^8, SA-t^7, SA+t^7 (t=k).
Coefficients : CoeffA = (SA(10)-SA(9))/k^8 ; CoeffB = (SB(10)-SB(9))/k^8.
Equations : (CoeffA)/x*k^n - Reste = SommeA ; (CoeffB)/x*k^n - Reste = SommeB
  (n entier strictement positif ; cf. S=1+q+...+q^n=(1-q^(n+1))/(1-q)).
Niveau 2 geometrique : memes utilites (facteur a1=sqrt(1+k^2) s'annule)."""


def construire_reponse_multi(
    spec: SpecMultiRatio,
    resultat=None,
    tableau: str = "",
    rapport: str = "",
) -> str:
    """Assemble la reponse formelle a partir d'un resultat pipeline existant."""
    lignes: List[str] = []
    lignes.append("=" * 100)
    lignes.append(
        f" REPONSE MULTI-RAPPORTS GENERALISEE | n={spec.n} "
        f"| 1/{spec.k_debut} a 1/{spec.k_fin} ({spec.taille} rapports)"
    )
    lignes.append(f" Limite agent : k <= {K_MAX_AGENT:,} | Moteur : pipeline cognitif (convolutif, 2 niveaux)")
    lignes.append("=" * 100)
    if rapport:
        lignes.append(rapport)
    # Synthese P(n) par rapport
    if resultat is not None:
        lignes.append("")
        lignes.append("--- Premiers reconstruits P(n) ---")
        for k in sorted(resultat.resultats):
            r = resultat.resultats[k]
            tag = "typique" if r.typique else "non typique"
            lignes.append(
                f"1/{k} ({tag}) : ancre n=10={r.premier_ancre_n10} | "
                f"P(n={spec.n})={r.premier_n} | "
                f"{'SUCCES' if r.reconstruction_reussie else 'ECHEC'}"
            )
        # Details non-typiques demandes : sommes n=10/n=9 + HOL
        non_typ = [k for k, r in sorted(resultat.resultats.items()) if not r.typique]
        if non_typ:
            lignes.append("")
            lignes.append("--- Details non-typiques (sommes A/B n=10, n=9 + HOL) ---")
            for k in non_typ:
                r = resultat.resultats[k]
                lignes.append(
                    f"1/{k} : SA(n=10)={r.somme_A} | SB(n=10)={r.somme_B} | "
                    f"ancre={r.premier_ancre_n10} | P={r.premier_n}"
                )
                lignes.append(_GABARIT_HOL.format(k=k))
            lignes.append("")
            lignes.append(_GABARIT_SUITES_GENERALISE)
    if tableau:
        lignes.append("")
        lignes.append(tableau)
    lignes.append("=" * 100)
    return "\n".join(lignes)


def repondre_multi_ratio(texte: str, echantillon_max: int = 1000) -> str:
    """Point d'entree agent : parse -> pipeline existant -> reponse formelle.

    CABLAGE SEUL : les calculs restent dans MultiRatioDispatcher (v7.9 O(1)).
    Au-dela de `echantillon_max` rapports, le calcul complet est sauvegarde
    en fichier (meme dossier que vos listes) et la reponse affiche le resume
    + un echantillon, pour rester utilisable en session terminal.
    """
    from src.dispatch.multi_ratio_parser import parser_multi_ratio
    try:
        spec = parser_multi_ratio(texte)
    except ValueError as e:
        msg = str(e)
        if "K_MAX_AGENT" in msg or "depasse la limite agent" in msg:
            # Extrait k_fin pour message formel
            import re as _re
            m = _re.search(r"k_fin=(\d+)", msg)
            kf = int(m.group(1)) if m else K_MAX_AGENT + 1
            return reponse_hors_limite(kf)
        return f"Requete multi-rapports incomprise : {e}"

    # Appel pipeline existant (aucune equation ici)
    from pipeline_cognitif.multi_ratio_dispatcher import MultiRatioDispatcher
    dispatcher = MultiRatioDispatcher(verbose=False)
    resultat = dispatcher.requete_plage(n=spec.n, k_debut=spec.k_debut, k_fin=spec.k_fin)

    if spec.taille <= echantillon_max:
        return construire_reponse_multi(
            spec, resultat=resultat,
            tableau=resultat.tableau_texte(), rapport=resultat.rapport_texte(),
        )

    # Grande plage : sauvegarde integrale + reponse resumee
    out = chemin_sortie_multi(spec.n, spec.k_debut, spec.k_fin)
    with open(out, "w", encoding="utf-8") as f:
        f.write(resultat.rapport_texte() + "\n\n" + resultat.tableau_texte() + "\n")
    # Echantillon : debut + fin
    ids = sorted(resultat.resultats)
    extrait_ids = ids[:50] + ids[-20:]
    lignes = [
        "=" * 100,
        f" REPONSE MULTI-RAPPORTS GENERALISEE (grande plage) | n={spec.n} "
        f"| 1/{spec.k_debut} a 1/{spec.k_fin} ({spec.taille} rapports)",
        f" Succes : {resultat.nb_succes}/{spec.taille} | Fichier integral : {out}",
        "=" * 100,
        "--- Echantillon (50 premiers + 20 derniers) ---",
    ]
    for k in extrait_ids:
        r = resultat.resultats[k]
        tag = "typique" if r.typique else "non typique"
        lignes.append(
            f"1/{k} ({tag}) : ancre={r.premier_ancre_n10} | P={r.premier_n} | "
            f"{'SUCCES' if r.reconstruction_reussie else 'ECHEC'}"
        )
    lignes.append("")
    lignes.append(_GABARIT_SUITES_GENERALISE)
    lignes.append("=" * 100)
    return "\n".join(lignes)


def reponse_hors_limite(k_fin: int) -> str:
    """Refus formel au-dela de la limite agent (sans troncature silencieuse)."""
    return (
        f"Plage refusee : k_fin={k_fin} depasse la limite agent K_MAX_AGENT={K_MAX_AGENT:,}. "
        "Reformulez en sous-plages (ex. 1/2 a 1/1000000). "
        "Le pipeline supporte jusqu'a 1e13 ; l'agent plafonne a 1 million par commodite."
    )


def chemin_sortie_multi(n: int, k_debut: int, k_fin: int) -> Path:
    dossier = _RACINE / "Liste_Premier_Multi_Rapports_K"
    dossier.mkdir(exist_ok=True)
    return dossier / f"liste_k{k_debut}_k{k_fin}_n{n}.txt"
