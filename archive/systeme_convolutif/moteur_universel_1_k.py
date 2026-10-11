# -*- coding: utf-8 -*-
"""
Moteur convolutif spectral INTERACTIF et UNIVERSEL — rapport non typique 1/k.

Contrairement à un tableau pré-rempli par rapport (1/3, 1/4, 1/5, ...), ce
programme ne contient AUCUNE valeur numérique propre à un k particulier. Il
applique une seule méthode algébrique, valable pour n'importe quel rapport
1/k (k entier >= 3), conforme :
  - aux règles de construction terme-à-terme des suites A_i / B_i formalisées
    dans agent-multiloop-Gabriel-local/theories/methode_spectral.thy,
    Section XI (lignes ~2815-3120) : progression simple + "avant-dernier
    Savard" + "dernier Savard", avec le "saut Zêta" (substitution de la
    position 6) pour la suite B ;
  - à la méthode manuscrite (extraits numériques 1/3..1/7) pour dériver les
    équations généralisées à partir de DEUX points de mesure (n=10 et
    n=9 termes), puis reconstruire le nombre premier via le test Digamma.

Déroulement du programme :
  1. L'utilisateur indique le rapport non typique (k dans 1/k).
  2. Le programme construit et affiche la table de convolution formelle
     (termes signés c1*k^e1 + c2*k^e2) des suites A et B pour n=10, PUIS
     pour n=9 (9 termes).
  3. Le programme dérive, à partir de CES DEUX SEULS points (n=10, n=9),
     les coefficients et restes des équations généralisées (méthode des
     deux points, strictement analogue à la méthode manuscrite) :
         Somme A(k,n) = CoeffA(k) * k^(n-3) - ResteA(k)
         Somme B(k,n) = CoeffB(k) * k^(n-3) - ResteB(k)
     valables pour tout n entier, positif ou négatif.
  4. Le programme calcule le Digamma et reconstruit le nombre premier
     associé à n=10 (et, à titre de contrôle, à n=9).
  5. Le programme demande une valeur n=? (entier positif quelconque,
     ex. 45) et reconstruit, à l'aide des équations généralisées dérivées
     à l'étape 3, la somme des suites A et B ainsi que le nombre premier
     correspondant (si n >= 8).

Aucune valeur k n'est câblée en dur : le même code s'applique à 1/3, 1/17,
1/128, etc. Seule la structure de la méthode (positions 6, n-3, n-2, n-1, n,
n+1) est fixe, conformément au manuscrit.
"""

from __future__ import annotations
from fractions import Fraction
from typing import NamedTuple


# ===========================================================================
# 1. TABLE DE CONVOLUTION FORMELLE (construction terme-à-terme, tout k, tout n)
#    Conforme à methode_spectral.thy, Section XI :
#      suite_A_savard_construction / suite_B_savard_construction
# ===========================================================================

class Terme(NamedTuple):
    ordre: int      # position (1..n, ou n+1 pour le dernier terme de B)
    c1: int
    e1: int
    c2: int
    e2: int

    def valeur(self, k: int) -> int:
        return self.c1 * k ** self.e1 + self.c2 * k ** self.e2

    def expression(self) -> str:
        if self.c2 == 0:
            return f"k^{self.e1}"
        signe = "+" if self.c2 > 0 else "-"
        return f"k^{self.e1} {signe} k^{abs(self.e2) and self.e2}"


def table_convolution(suite: str, n: int) -> list[Terme]:
    """Construit la table de convolution formelle de la suite 'A' ou 'B'
    pour une longueur n >= 4 (règle générale, Section XI du manuscrit) :

    Suite A : progression simple k^1..k^(n-2)
              + avant-dernier "Savard" : k^(n-1) - k^(n-3)
              + dernier "Savard"       : k^n     - k^(n-2)

    Suite B : progression simple k^1..k^(n-1), SAUF la position 6
              (saut Zêta : le terme d'exposant 6 est omis)
              + avant-dernier "Savard" : k^n     - k^(n-2)
              + dernier "Savard"       : k^(n+1) - k^(n-1)
    """
    suite = suite.upper()
    if n < 4:
        raise ValueError("n doit être >= 4 pour construire la table de convolution.")
    termes: list[Terme] = []
    if suite == "A":
        for i in range(1, n - 1):
            termes.append(Terme(i, 1, i, 0, 0))
        termes.append(Terme(n - 1, 1, n - 1, -1, n - 3))
        termes.append(Terme(n, 1, n, -1, n - 2))
    elif suite == "B":
        for i in range(1, n):
            if i == 6:
                continue  # saut Zêta
            termes.append(Terme(i, 1, i, 0, 0))
        termes.append(Terme(n, 1, n, -1, n - 2))
        termes.append(Terme(n + 1, 1, n + 1, -1, n - 1))
    else:
        raise ValueError("suite doit être 'A' ou 'B'.")
    return termes


def somme_convolution(suite: str, k: int, n: int) -> int:
    return sum(t.valeur(k) for t in table_convolution(suite, n))


# ===========================================================================
# 2. DÉRIVATION DES ÉQUATIONS GÉNÉRALISÉES PAR LA MÉTHODE DES DEUX POINTS
#    (n=10 et n=9), strictement analogue à la méthode manuscrite : on ne
#    suppose JAMAIS une formule fermée connue à l'avance, on la RECONSTRUIT
#    à partir des deux sommes mesurées, pour un k quelconque fourni par
#    l'utilisateur.
# ===========================================================================

class EquationsGeneralisees(NamedTuple):
    k: int
    A10: int
    A9: int
    B10: int
    B9: int
    coeff_A: Fraction   # CoeffA(k)
    reste_A: Fraction   # ResteA(k)
    coeff_B: Fraction   # CoeffB(k)
    reste_B: Fraction   # ResteB(k)

    def somme_A(self, n: int) -> Fraction:
        return self.coeff_A * Fraction(self.k) ** (n - 3) - self.reste_A

    def somme_B(self, n: int) -> Fraction:
        return self.coeff_B * Fraction(self.k) ** (n - 3) - self.reste_B


def deriver_equations(k: int) -> EquationsGeneralisees:
    """Reproduit, pour un k quelconque, EXACTEMENT la démarche manuscrite :

      1. Construire Somme A et Somme B pour n=10 (10 termes) par la table de
         convolution formelle.
      2. Construire Somme A et Somme B pour n=9 (9 termes) de la même façon.
      3. Poser Somme(n) = Coeff * k^(n-3) - Reste, et résoudre le système
         à 2 équations / 2 inconnues formé par les valeurs à n=10 et n=9 :
             Somme(10) = Coeff * k^7 - Reste
             Somme(9)  = Coeff * k^6 - Reste
         d'où (par soustraction, exactement l'« écart minimal » du
         manuscrit) :
             Coeff = (Somme(10) - Somme(9)) / (k^6 * (k - 1))
             Reste = Coeff * k^7 - Somme(10)
    """
    A10 = somme_convolution("A", k, 10)
    A9 = somme_convolution("A", k, 9)
    B10 = somme_convolution("B", k, 10)
    B9 = somme_convolution("B", k, 9)

    denom = Fraction(k) ** 6 * (k - 1)
    coeff_A = Fraction(A10 - A9, 1) / denom
    reste_A = coeff_A * Fraction(k) ** 7 - A10

    coeff_B = Fraction(B10 - B9, 1) / denom
    reste_B = coeff_B * Fraction(k) ** 7 - B10

    return EquationsGeneralisees(k, A10, A9, B10, B9, coeff_A, reste_A, coeff_B, reste_B)


# ===========================================================================
# 3. DIGAMMA ET RECONSTRUCTION DU NOMBRE PREMIER (n >= 8)
# ===========================================================================

def _est_premier(m: int) -> bool:
    if m < 2:
        return False
    if m in (2, 3):
        return True
    if m % 2 == 0:
        return False
    i = 3
    while i * i <= m:
        if m % i == 0:
            return False
        i += 2
    return True


def _rang_premier(p: int) -> int | None:
    if not _est_premier(p):
        return None
    rang = 0
    c = 1
    while c < p:
        c += 1
        if _est_premier(c):
            rang += 1
    return rang


class CandidatDigamma(NamedTuple):
    position: int
    signe: int
    digamma: Fraction
    p_candidat: Fraction
    entier: bool
    premier: bool
    rang: int | None


def candidats_digamma(eq: EquationsGeneralisees, n: int) -> list[CandidatDigamma]:
    """Teste les 4 candidats Digamma(k,n,pos,signe) = SommeA(n) + signe*k^pos,
    pos in {n-3, n-2}, signe in {+1,-1}, et P_candidat = (SommeB(n)-Digamma)/k^6.
    """
    if n < 8:
        raise ValueError("Le test Digamma n'est défini que pour n >= 8.")
    k = eq.k
    A = eq.somme_A(n)
    B = eq.somme_B(n)
    resultats = []
    # Ordre de test conforme au manuscrit : position n-2 d'abord (le cas le
    # plus fréquent dans les exemples fournis), puis n-3.
    for pos in (n - 2, n - 3):
        for signe in (1, -1):
            digamma = A + signe * Fraction(k) ** pos
            p = (B - digamma) / Fraction(k) ** 6
            entier = p.denominator == 1
            premier = entier and _est_premier(int(p))
            rang = _rang_premier(int(p)) if premier else None
            resultats.append(CandidatDigamma(pos, signe, digamma, p, entier, premier, rang))
    return resultats


def resoudre_digamma(eq: EquationsGeneralisees, n: int):
    """Résout l'ambiguïté Digamma de façon purement algébrique quand c'est
    possible, en suivant la logique du manuscrit :
      - on teste d'abord la position n-2 (les deux signes) ;
      - si un SEUL des deux candidats à cette position est premier, on le
        retient (c'est le cas le plus fréquent) ;
      - sinon on teste la position n-3 de la même façon ;
      - si aucune des deux positions ne tranche seule (0 ou plusieurs
        candidats premiers à chaque position), le programme signale une
        ambiguïté structurelle authentique et affiche tous les candidats
        premiers trouvés (sélection par essai-erreur, comme prévu par le
        manuscrit lui-même pour n >= 8).

    Retourne (candidat_retenu_ou_None, tous_les_candidats, note_methode).

    IMPORTANT : on ne "replie" vers l'autre position (n-3) QUE si la position
    n-2 ne fournit AUCUN candidat premier. Si la position n-2 fournit PLUSIEURS
    candidats premiers simultanément, c'est une ambiguïté réelle qu'il ne faut
    pas masquer en sautant vers n-3 (une position qui, elle, pourrait donner
    un résultat unique mais FAUX) : le manuscrit original documente lui-même
    cette situation comme nécessitant un "essai-erreur" (Parametres/RÈGLES
    ACTIVES : "Sélection par essai-erreur").
    """
    tous = candidats_digamma(eq, n)
    sous_n2 = [c for c in tous if c.position == n - 2]
    premiers_n2 = [c for c in sous_n2 if c.premier]

    if len(premiers_n2) == 1:
        return premiers_n2[0], tous, f"Résolu sans ambiguïté à la position n-2={n-2}."

    if len(premiers_n2) == 0:
        sous_n3 = [c for c in tous if c.position == n - 3]
        premiers_n3 = [c for c in sous_n3 if c.premier]
        if len(premiers_n3) == 1:
            return premiers_n3[0], tous, f"Résolu sans ambiguïté à la position n-3={n-3}."
        if len(premiers_n3) == 0:
            return None, tous, "Aucun candidat entier premier trouvé pour ce (k, n)."
        return None, tous, (
            f"{len(premiers_n3)} candidats premiers simultanés à la position "
            f"n-3={n-3} : ambiguïté authentique. Sélection par essai-erreur "
            "requise (voir méthode manuscrite, Parametres/RÈGLES ACTIVES)."
        )

    # len(premiers_n2) > 1 : ambiguïté réelle à la position n-2, ne pas replier.
    return None, tous, (
        f"{len(premiers_n2)} candidats premiers simultanés à la position "
        f"n-2={n-2} : ambiguïté authentique (deux nombres premiers proches). "
        "Sélection par essai-erreur requise (voir méthode manuscrite, "
        "Parametres/RÈGLES ACTIVES)."
    )


# ===========================================================================
# 4. AFFICHAGE PÉDAGOGIQUE (reproduit le style des exemples manuscrits)
# ===========================================================================

def _fmt(x: Fraction) -> str:
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def afficher_table(suite: str, k: int, n: int) -> int:
    termes = table_convolution(suite, n)
    expr = " + ".join(t.expression().replace("+ -", "- ") for t in termes)
    total = sum(t.valeur(k) for t in termes)
    print(f"  Suite {suite}({n} termes, k={k}) :")
    print(f"    {expr}")
    print(f"    = {total}")
    return total


def afficher_candidats(cands: list[CandidatDigamma], k: int, n: int) -> None:
    print(f"  Candidats Digamma testés pour k={k}, n={n} :")
    for c in cands:
        statut = "PREMIER" if c.premier else ("entier" if c.entier else "non entier")
        rang = f", {c.rang}e nombre premier" if c.rang else ""
        print(f"    position={c.position:>3}  signe={c.signe:+d}  "
              f"P={_fmt(c.p_candidat):>10}  [{statut}{rang}]")


def executer_pour_k(k: int) -> EquationsGeneralisees:
    print(f"\n===== Rapport non typique 1/{k} =====\n")

    print("Étape 1 — Construction des suites A et B pour n=10 (table de "
          "convolution formelle) :")
    A10 = afficher_table("A", k, 10)
    B10 = afficher_table("B", k, 10)

    print("\nÉtape 2 — Construction des suites A et B pour n=9 (9 termes) :")
    A9 = afficher_table("A", k, 9)
    B9 = afficher_table("B", k, 9)

    print("\nÉtape 3 — Dérivation des équations généralisées (méthode des "
          "deux points n=10 / n=9) :")
    eq = deriver_equations(k)
    print(f"  CoeffA(k) = (SommeA(10) - SommeA(9)) / (k^6*(k-1)) = "
          f"({A10} - {A9}) / ({k}^6*({k}-1)) = {_fmt(eq.coeff_A)}")
    print(f"  ResteA(k) = CoeffA(k)*k^7 - SommeA(10) = {_fmt(eq.reste_A)}")
    print(f"  CoeffB(k) = (SommeB(10) - SommeB(9)) / (k^6*(k-1)) = "
          f"({B10} - {B9}) / ({k}^6*({k}-1)) = {_fmt(eq.coeff_B)}")
    print(f"  ResteB(k) = CoeffB(k)*k^7 - SommeB(10) = {_fmt(eq.reste_B)}")
    print(f"\n  Forme générale (n entier positif) :")
    print(f"    Somme A(k,n) = ({_fmt(eq.coeff_A)}) * {k}^(n-3) - {_fmt(eq.reste_A)}")
    print(f"    Somme B(k,n) = ({_fmt(eq.coeff_B)}) * {k}^(n-3) - {_fmt(eq.reste_B)}")
    print(f"  Forme générale (n entier négatif) :")
    print(f"    Somme A négative(k,n) = ({_fmt(eq.coeff_A)}) * {k}^(-n) - {_fmt(eq.reste_A)}")
    print(f"    Somme B négative(k,n) = ({_fmt(eq.coeff_B)}) * {k}^(-n) - {_fmt(eq.reste_B)}")

    print("\nÉtape 4 — Reconstruction du nombre premier pour n=10 :")
    cand, tous, note = resoudre_digamma(eq, 10)
    afficher_candidats(tous, k, 10)
    print(f"  {note}")
    if cand is not None:
        print(f"  ==> Nombre premier reconstruit pour 1/{k}, n=10 : "
              f"{int(cand.p_candidat)} ({cand.rang}e nombre premier), "
              f"position Digamma={cand.position}, signe={cand.signe:+d}")

    return eq


def executer_pour_n(eq: EquationsGeneralisees, n: int) -> None:
    k = eq.k
    if n < 4:
        print(f"\nPour n={n} < 4, la table de convolution formelle standard "
              f"(section XI) ne s'applique pas telle quelle ; seule la forme "
              f"fermée négative/positive générale peut être évaluée si n est "
              f"strictement négatif.")
    A = eq.somme_A(n)
    B = eq.somme_B(n)
    print(f"\n===== Résultat pour 1/{k}, n={n} =====")
    print(f"  Somme A({k},{n}) = {_fmt(A)}")
    print(f"  Somme B({k},{n}) = {_fmt(B)}")

    if n >= 8:
        cand, tous, note = resoudre_digamma(eq, n)
        afficher_candidats(tous, k, n)
        print(f"  {note}")
        if cand is not None:
            print(f"  ==> Nombre premier reconstruit pour 1/{k}, n={n} : "
                  f"{int(cand.p_candidat)} ({cand.rang}e nombre premier), "
                  f"position Digamma={cand.position}, signe={cand.signe:+d}")
    else:
        print(f"  (n={n} < 8 : le test Digamma / reconstruction du premier "
              f"n'est défini que pour n >= 8, conformément à la règle "
              f"'RÈGLES ACTIVES' du manuscrit.)")


def main() -> None:
    print(__doc__)
    while True:
        brut = input(
            "\nQuel rapport non typique voulez-vous reconstruire ? "
            "Entrez la valeur de k pour 1/k (k entier >= 3), ex. 17 pour 1/17 : "
        ).strip()
        try:
            k = int(brut)
            if k < 3:
                raise ValueError
            break
        except ValueError:
            print("Veuillez entrer un entier k >= 3 (le rapport typique 1/2 "
                  "n'est pas traité par ce moteur).")

    eq = executer_pour_k(k)

    while True:
        brut = input(
            "\nEntrez une valeur de n (entier positif) pour reconstruire la "
            "somme des suites A et B (et le nombre premier si n >= 8), ou "
            "appuyez sur Entrée pour quitter : "
        ).strip()
        if brut == "":
            break
        try:
            n = int(brut)
            if n <= 0:
                raise ValueError
        except ValueError:
            print("Veuillez entrer un entier strictement positif.")
            continue
        executer_pour_n(eq, n)


if __name__ == "__main__":
    main()
