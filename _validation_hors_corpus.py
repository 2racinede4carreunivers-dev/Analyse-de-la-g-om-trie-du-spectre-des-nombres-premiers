"""VALIDATION HORS-CORPUS de la regle de branche (criblage modulaire).

Objectif : tester la regle sur des k qui ne figurent PAS dans le corpus
d'ancres, en utilisant une VERITE INDEPENDANTE = primalite reelle (sympy),
et non la parite (controle trop faible).

Protocole (par k) :
  V1. crible = branches non eliminees par les petits premiers {3..23}
  V2. vrais  = branches dont le candidat est reellement premier
  K admissible si V2 est non vide  (sinon k hors du "jeu" : aucun premier)
  Sur K admissible :
     - si |V1| == 1  -> la regle se prononce : verifier V1[0] == V2[0]
     - si |V1| >  1  -> la regle est muette (indeterminee), cas attendu

Lancement : python _validation_hors_corpus.py
"""
import sys
import sympy

sys.path.insert(0, r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers")
from _regle_branche import (  # noqa: E402
    BRANCHES, PRIMES_CRIBLAGE, candidats,
)

DEBUT = 4_000_001      # hors du corpus d'ancres (k max = 3 999 996)
NB = 3000


def crible(k):
    c = candidats(k)
    return [BRANCHES[i] for i in range(4)
            if all(c[i] % p for p in PRIMES_CRIBLAGE)]


def vrais_premiers(k):
    c = candidats(k)
    return [BRANCHES[i] for i in range(4) if sympy.isprime(c[i])]


def main():
    ks = range(DEBUT, DEBUT + NB)
    hors_jeu = 0
    muet = 0
    exact = 0
    faux = 0
    for k in ks:
        v2 = vrais_premiers(k)
        if not v2:
            hors_jeu += 1          # aucun candidat premier : k hors du jeu
            continue
        v1 = crible(k)
        if len(v1) != 1:
            muet += 1              # la regle ne se prononce pas
            continue
        if v1[0] == v2[0]:
            exact += 1
        else:
            faux += 1

    total = NB
    admissibles = total - hors_jeu
    print("=== VALIDATION HORS-CORPUS (verite = primalite reelle) ===")
    print(f"  k testes                        : {total}")
    print(f"  hors jeu (aucun premier)        : {hors_jeu}")
    print(f"  k admissibles (>=1 vrai premier): {admissibles}")
    print(f"  regle muette (ambigu)           : {muet}")
    print(f"  regle se prononce               : {exact + faux}")
    print(f"  -> designation CORRECTE         : {exact}")
    print(f"  -> designation FAUSSE           : {faux}")
    if exact + faux:
        print(f"  exactitude hors corpus          : {exact}/{exact+faux} "
              f"= {exact/(exact+faux):.4%}")
    return 0 if faux == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
