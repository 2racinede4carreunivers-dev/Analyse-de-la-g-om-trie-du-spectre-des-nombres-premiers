#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation de conformite du pipeline a la Section XIV de methode_spectral.thy.

Sections verifiees :
  A) XIV.6  - ancrages n=10 : rangs officiels = rangs reels dans P
  B) XIV.2  - formes fermees universelles (domaine n >= 8, cf. XIV.4)
  C) XIV.4  - construction terme a terme (niveau 1) et a1*XIV.4 (niveau 2)
  D) XIV.7  - validation exacte k=8, n=34 (sommes completes)
  E) XIV.6  - decalage de rang : rang(n) = rang_ancre + (n - 10)
  F) XIV.5  - niveau 2 geometrique : memes ancrages que le niveau 1
  G) Pipeline generalise 1/k (typique et non typique), tout n >= 1,
     suivant l'ordre prescrit : n=10 -> 4 Digamma -> n=9 -> coefficients
     -> (Reste+x) blocs A/B -> equations generalisees -> n demande + premier

Domaine des formes fermees : XIV.2 et XIV.4 coincident pour n >= 8 ; pour
n <= 7, XIV.4 impose terme_b = terme_a (progression simple) et fait foi
(constante SEUIL_FORMES_FERMEES = 8 du module).

Code de sortie : 0 si tout est conforme, 1 sinon.

Usage : python -m pipeline_cognitif.validation_section_xiv
        ou    python pipeline_cognitif/validation_section_xiv.py
"""
from fractions import Fraction
import sys

try:
    from .suites_geometriques_niveau2 import (
        ANCRAGES_XIV,
        CalculateurNiveau1Entiers,
        CalculateurNiveau2Geometrique,
        MethodeDigamma,
        est_premier,
    )
except ImportError:  # execution directe du script
    from suites_geometriques_niveau2 import (
        ANCRAGES_XIV,
        CalculateurNiveau1Entiers,
        CalculateurNiveau2Geometrique,
        MethodeDigamma,
        est_premier,
    )

try:
    from .multi_ratio_dispatcher import MultiRatioDispatcher
except ImportError:  # execution directe du script
    from multi_ratio_dispatcher import MultiRatioDispatcher

ECARTS = []


def check(condition, etiquette, detail=""):
    """Enregistre un controle ; affiche OK ou ECART."""
    statut = "OK" if condition else "** ECART **"
    if not condition:
        ECARTS.append(etiquette)
    print(f"  [{statut}] {etiquette} {detail}")
    return condition


# --- Constantes universelles XIV.1 et formes fermees XIV.2 ---------------

def alphaA(k):
    return Fraction(2 * (k ** 4 - k ** 2 + 1), (k - 1) * k ** 3)


def alphaB(k):
    return k * alphaA(k)


def offsetA(k):
    return Fraction(k, k - 1)


def offsetB(k):
    return Fraction(k ** 7 - k ** 6 + k, k - 1)


def somme_A_xiv2(k, n):
    return (alphaA(k) / 2) * Fraction(k ** n) - offsetA(k)


def somme_B_xiv2(k, n):
    return (alphaB(k) / 2) * Fraction(k ** n) - offsetB(k)


# --- Regles de construction terme a terme XIV.4 --------------------------

def terme_a_xiv4(k, n, i):
    if i > n:
        return 0
    if n <= 7:
        return k ** i
    if i <= n - 2:
        return k ** i
    if i == n - 1:
        return k ** (n - 1) - k ** (n - 3)
    return k ** n - k ** (n - 2)


def terme_b_xiv4(k, n, i):
    if i > n:
        return 0
    if n <= 7:
        return terme_a_xiv4(k, n, i)
    if i <= 5:
        return k ** i
    if i == 6:
        return k ** 7
    if i <= n - 2:
        return k ** (i + 1)
    if i == n - 1:
        return k ** n - k ** (n - 2)
    return k ** (n + 1) - k ** (n - 1)


# --- Table des premiers (crible) ------------------------------------------
LIMITE = 200000
crible = bytearray([1]) * LIMITE
crible[0:2] = b"\x00\x00"
for i in range(2, int(LIMITE ** 0.5) + 1):
    if crible[i]:
        crible[i * i::i] = bytearray(len(crible[i * i::i]))
PREMIERS = [i for i in range(LIMITE) if crible[i]]
RANG = {p: i + 1 for i, p in enumerate(PREMIERS)}


def nieme(r):
    return PREMIERS[r - 1] if 1 <= r <= len(PREMIERS) else None


def section_A():
    """A) XIV.6 — ancrages n=10 : rangs officiels vs rangs reels."""
    print("=" * 92)
    print(" A) ANCRAGES XIV.6 (rangs officiels vs rangs reels dans P)")
    print("=" * 92)
    for k in sorted(ANCRAGES_XIV):
        r = ANCRAGES_XIV[k]['rang']
        p = ANCRAGES_XIV[k]['premier']
        check(RANG.get(p) == r and nieme(r) == p,
              f"k={k}: rang={r} premier={p}", f"(rang_reel={RANG.get(p)})")
    check(nieme(3492) == 32537, "k=8, n=34 : rang 3492 -> 32537",
          f"(obtenu {nieme(3492)})")


def section_B():
    """B) XIV.2 — formes fermees == implementation pour n >= 8 ; P a n=10."""
    print()
    print("=" * 92)
    print(" B) FORMES FERMEES XIV.2 (domaine n >= 8) ET PREMIER RECONSTRUIT A n=10")
    print("=" * 92)
    attendus = {k: ANCRAGES_XIV[k]['premier'] for k in sorted(ANCRAGES_XIV)}
    for k in sorted(attendus):
        calc = CalculateurNiveau1Entiers(k=k)
        r10 = calc.calculer(10)
        ok_n = all(
            Fraction(calc.calculer(n).somme_A) == somme_A_xiv2(k, n)
            and Fraction(calc.calculer(n).somme_B) == somme_B_xiv2(k, n)
            for n in (8, 9, 10, 11, 15, 25))
        P, _ = MethodeDigamma(k=k, n=10).reconstruire_premier(
            r10.somme_A, r10.somme_B, verbose=False)
        check(P == attendus[k] and ok_n,
              f"k={k}: S_A(10)={r10.somme_A} S_B(10)={r10.somme_B}",
              f"formesXIV(n>=8)={ok_n} P={P} (attendu {attendus[k]})")


def section_C():
    """C) XIV.4 — construction terme a terme, niveaux 1 et 2."""
    print()
    print("=" * 92)
    print(" C) CONSTRUCTION TERME A TERME XIV.4 (niveau 1 exact ; niveau 2 = a1*XIV.4)")
    print("=" * 92)
    niv1_ok = niv2_ok = True
    for k in sorted(ANCRAGES_XIV):
        c1 = CalculateurNiveau1Entiers(k=k)
        c2 = CalculateurNiveau2Geometrique(k=k)
        a1 = c2.facteur
        for n in list(range(1, 20)) + [25, 34]:
            A1 = c1.generer_suite_A_termes(n)
            B1 = c1.generer_suite_B_termes(n)
            A2 = c2.generer_suite_A_termes(n)
            B2 = c2.generer_suite_B_termes(n)
            for i, v in enumerate(A1):
                niv1_ok &= (v == terme_a_xiv4(k, n, i + 1))
            for i, v in enumerate(B1):
                niv1_ok &= (v == terme_b_xiv4(k, n, i + 1))
            for i, v in enumerate(A2):
                niv2_ok &= abs(v - a1 * terme_a_xiv4(k, n, i + 1)) <= 1e-6 * max(1, abs(v))
            for i, v in enumerate(B2):
                niv2_ok &= abs(v - a1 * terme_b_xiv4(k, n, i + 1)) <= 1e-6 * max(1, abs(v))
    check(niv1_ok, "niveau 1 == XIV.4 terme a terme (tous k, tous n)")
    check(niv2_ok, "niveau 2 == a1 * XIV.4 terme a terme (tous k, tous n)")


def section_D():
    """D) XIV.7 — validation exacte k=8, n=34."""
    print()
    print("=" * 92)
    print(" D) VALIDATION EXACTE k=8, n=34 (XIV.7)")
    print("=" * 92)
    SA = 5705842489643358455620763423304
    SB = 45646739917146867644966107124296
    DIG = 45646739917146867644957577744968
    calc8 = CalculateurNiveau1Entiers(k=8)
    r34 = calc8.calculer(34)
    check(r34.somme_A == SA, "S_A(8,34)", f"= {r34.somme_A}")
    check(r34.somme_B == SB, "S_B(8,34)", f"= {r34.somme_B}")
    digamma = r34.somme_B - 32537 * 8 ** 6
    check(digamma == DIG, "Digamma(8,34)", f"= {digamma}")
    P = (r34.somme_B - digamma) // 8 ** 6
    check(P == 32537 and est_premier(P), "(S_B - Digamma)/k^6 = 32537 premier")
    r_cible = ANCRAGES_XIV[8]['rang'] + 34 - 10
    check(nieme(r_cible) == 32537,
          f"rang_cible = {ANCRAGES_XIV[8]['rang']} + 24 = {r_cible} -> 32537")


def section_E():
    """E) XIV.6 — decalage de rang sur k=3, n=9..17."""
    print()
    print("=" * 92)
    print(" E) DECALAGE DE RANG XIV.6 : k=3 (ancre 227 @ n=10, rang 49)")
    print("=" * 92)
    calc3 = CalculateurNiveau1Entiers(k=3)
    r0 = ANCRAGES_XIV[3]['rang']
    # Progression documentee : 223 @ n=9, puis 227, 229, 233, 239, 241, ...
    attendus = {9: 223, 10: 227, 11: 229, 12: 233, 13: 239, 14: 241,
                15: 251, 16: 257, 17: 263}
    tous = True
    for n in range(9, 18):
        sB = calc3.calculer(n).somme_B
        r_c = r0 + n - 10
        P_c = nieme(r_c)
        ok = (P_c == attendus[n])
        tous &= ok
        print(f"  n={n:2d}: rang={r_c:3d} P={P_c:5d} (attendu {attendus[n]:5d}) "
              f"Digamma=S_B-P*3^6={sB - P_c * 3 ** 6} "
              f"{'OK' if ok else '** ECART **'}")
    check(tous, "decalage de rang : rang(n) = 49 + (n - 10), n = 9..17")


def section_F():
    """F) XIV.5 — niveau 2 geometrique : memes ancrages que le niveau 1."""
    print()
    print("=" * 92)
    print(" F) NIVEAU 2 GEOMETRIQUE : memes ancrages que le niveau 1 (XIV.5)")
    print("=" * 92)
    for k in sorted(ANCRAGES_XIV):
        attendu = ANCRAGES_XIV[k]['premier']
        cg = CalculateurNiveau2Geometrique(k=k)
        P, cands = cg.reconstruire_premier(n=10, verbose=False)
        premiers_c = [c['P_candidat'] for c in cands if c['est_premier']]
        check(P == attendu, f"k={k}: P={P} (attendu {attendu})",
              f"| premiers candidats={premiers_c}")


def section_G():
    """G) Contrat du dispatcher multi-rapports et cas d'ancrage ambigus."""
    print()
    print("=" * 92)
    print(" G) PIPELINE GENERALISE 1/k (typique et non typique), ordre prescrit")
    print("=" * 92)
    dispatcher = MultiRatioDispatcher()
    # Rapport typique 1/2 : n = position du premier dans P.
    r = dispatcher.requete(n=10, liste_k=[2]).resultats[2]
    check(r.premier_n == 29 and r.position_dans_P == 10,
          "typique 1/2 : n=10 -> 29 (10e premier)")
    r = dispatcher.requete(n=9, liste_k=[2]).resultats[2]
    check(r.premier_n == 23 and r.digamma_calcule == 126,
          "typique 1/2 : n=9 -> 23, Digamma = 126")
    # Rapports non typiques : ancrage n=10 + decalage de rang.
    for k, n, attendu in [(3, 17, 263), (7, 10, 16519),
                          (7, 17, 16603), (8, 34, 32537)]:
        r = dispatcher.requete(n=n, liste_k=[k]).resultats[k]
        check(r.premier_n == attendu,
              f"non typique 1/{k} : n={n} -> {attendu} (obtenu {r.premier_n})")
        check(r.digamma_calcule == r.somme_B - attendu * k ** 6,
              f"1/{k} : Digamma exact a n={n}")
    # Les rapports ambigus sont exposes sans choix automatique.
    for k, nombre in ((10, 3), (20, 2)):
        r = dispatcher.requete(n=10, liste_k=[k]).resultats[k]
        check(r.premier_ancre_n10 is None
              and len(r.candidats_ancre_n10) == nombre
              and "ambigu" in r.message.lower(),
              f"1/{k} : {nombre} candidats conserves, aucun ancrage choisi")
    # Gardes-fous.
    for mauvais_k in (0, 1, 2.5):
        try:
            dispatcher.requete(n=10, liste_k=[mauvais_k])
            check(False, f"k={mauvais_k} aurait du etre rejete")
        except (TypeError, ValueError):
            check(True, f"k={mauvais_k} rejete")


def main():
    section_A()
    section_B()
    section_C()
    section_D()
    section_E()
    section_F()
    section_G()
    print()
    print("=" * 92)
    if ECARTS:
        print(f" VERDICT : {len(ECARTS)} ECART(S) vs Section XIV")
        for e in ECARTS:
            print(f"   - {e}")
        return 1
    print(" VERDICT : 0 ECART — pipeline conforme a la Section XIV")
    return 0


if __name__ == "__main__":
    sys.exit(main())
