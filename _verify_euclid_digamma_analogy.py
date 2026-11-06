"""Verification de l'analogie 'division euclidienne -> fonction Digamma'.

A. Analogies donnees (division euclidienne, division polynomiale, racines).
B. La recette 1406 = 55*29 - 189 : exacte ? generale ? non circulaire ?
C. Forme fermee de la division euclidienne spectrale :
      SB = k^6 * P + Digamma  =>  P in {B0+k^2, B0-k^2, B0+k, B0-k}
   verifiee sur k=2..9 contre le catalogue ANCHORS_N10.
D. Le point d'annulation : k=2 produit DEUX premiers (29 ET 23) ->
   aucune equation annulante sur {candidats} ne peut choisir sans
   primalite ou rang.
"""
import sympy
from sympy import sqrt, Rational, simplify, nsimplify

F = sympy.Rational

print("=" * 78)
print("A. ANALOGIES ALGEBRIQUES DU MESSAGE")
print("=" * 78)
print(f" 23/45 : 1 - 22/45  -> 45*1 - 22 = {45*1 - 22}  (23)  OK")
print(f" 32/26 : 1 + 6/26   -> 26*1 + 6  = {26*1 + 6}   (32)  OK")

x = sympy.symbols("x")
f = 3*x**2 + 6*x + 2
div, quo, rem = 2*x + 2, Rational(3, 2)*x + Rational(3, 2), -1
print(f"\n Division polynomiale : (3x^2+6x+2)/(2x+2) = 1.5x+1.5, reste -1")
print("  controles : div*quo + rem =",
      sympy.expand(div*quo + rem), "= f ?", sympy.expand(div*quo + rem) == f)

d1 = (Rational(3, 2)*x + Rational(3, 2))
x1 = (-6 - sqrt(12)) / 6          # racine 'moins'
x2 = (-6 + sqrt(12)) / 6          # racine 'plus'
x1_user = -(1 + Rational(1, 3)**Rational(1, 2))    # lecture '3^-1/2'
x2_user = -(Rational(1, 12)**Rational(1, 2) + (sqrt(12) + 4)**-1)
print(f"  x1 = {simplify(x1)} = {float(x1):.6f}")
print(f"  lecture user -(1+(1/3)^1/2) = {simplify(x1_user)} = {float(x1_user):.6f}"
      f"  -> {'IDENTIQUE' if simplify(x1 - x1_user) == 0 else 'different'}")
print(f"  x2 = {simplify(x2)} = {float(x2):.6f}")
print(f"  lecture user -((1/12)^1/2+(12^1/2+4)^-1) = {simplify(x2_user)}"
      f" = {float(x2_user):.6f}"
      f"  -> {'IDENTIQUE' if simplify(x2 - x2_user) == 0 else 'different'}")
for nom, xr in (("x1", x1), ("x2", x2)):
    prod = (2*xr + 2) * (Rational(3, 2)*xr + Rational(3, 2))
    somme = (2*xr + 2) + (Rational(3, 2)*xr + Rational(3, 2) - 1)
    print(f"  Annulation en {nom} : div*quo = {simplify(prod)} (=1 attendu)"
          f" | lecture '+' = {simplify(somme)} ({float(somme):.3f})")
print("  -> l'annulation exacte est div*quo = -reste (=1) ; la lecture '+'")
print("     du message donne -3.02 : coquille, il faut un PRODUIT.")

print()
print("=" * 78)
print("B. LA RECETTE 1406 = 55*29 - 189")
print("=" * 78)
T10 = 10 * 11 // 2
print(f" 10(10+)/2 = T10 = {T10}  OK ; 55*29 = {55*29} ; 1595-189 = {1595-189}")
lit = F(2, 55) + F(29, 10) + F(1, 2) * 55
print(f" formule LITTERALE (2/55)+2.9+0.5*55 = {float(lit):.4f}  -> 189 ? NON")
alt = 2 + F(29, 10) * 55 + F(1, 2) * 55
print(f" lecture qui donne 189 : 2 + 2.9*55 + 0.5*55 = {alt}  -> 189 ? OUI")
print(" MAIS 2.9 = 29/10 = P/10 : la recette contient le premier P qu'on")
print(" cherche -> circulaire (elle reecrit Digamma = T10*P - (T10*P-Digamma)).")
print("\n Generalisation aux autres exemples : C_n = T_n*P - Digamma_calc :")
for n, p, D in ((10, 29, 1406), (11, 31, 4606), (12, 37, 10878), (13, 41, 23934)):
    Tn = n * (n + 1) // 2
    print(f"  n={n}: T_n={Tn:3}  T_n*P={Tn*p:6}  Digamma={D:6}  C_n={Tn*p - D:+7}")
print("  -> 189, -2560, -7992, -20203 : aucun motif; la recette s'arrete la.")

print()
print("=" * 78)
print("C. FORME FERMEE DE LA DIVISION EUCLIDIENNE SPECTRALE")
print("   SB = k^6*P + Digamma  =>  P = B0 +/- k^2, B0 +/- k")
print("=" * 78)
import sys
PROJ = (r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
        r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers")
sys.path.insert(0, PROJ + r"\pipeline_cognitif")
from suites_geometriques_niveau2 import CalculateurNiveau1Entiers
from multi_ratio_dispatcher import ANCHORS_N10

print(f"{'k':>3} {'B0':>10} {'B0+k^2':>10} {'B0-k^2':>10} {'B0+k':>10} "
      f"{'B0-k':>10}  premiers           choix(ordre)  catalogue")
for k in range(2, 10):
    calc = CalculateurNiveau1Entiers(k=k)
    r10 = calc.calculer(10)
    k6 = k ** 6
    B0 = (r10.somme_B - r10.somme_A) / k6
    assert B0 == int(B0), f"B0 non entier pour k={k}"
    B0 = int(B0)
    cands = [B0 + k**2, B0 - k**2, B0 + k, B0 - k]  # ordre (8-, 8+, 7+, 7-)
    prem = [c for c in cands if sympy.isprime(c)]
    choix = prem[0] if prem else None
    cat = ANCHORS_N10.get(k, "-")
    ok = (choix == cat) if isinstance(cat, int) else True
    print(f"{k:>3} {B0:>10} {cands[0]:>10} {cands[1]:>10} {cands[2]:>10} "
          f"{cands[3]:>10}  {str(prem):<20} {str(choix):>10}  {cat} "
          f"{'OK' if ok else 'ECHEC'}")

print()
print("=" * 78)
print("D. LE POINT D'ANNULATION : k=2, n=10")
print("=" * 78)
r10 = CalculateurNiveau1Entiers(k=2).calculer(10)
B0 = int((r10.somme_B - r10.somme_A) / 64)
cands = [B0 + 4, B0 - 4, B0 + 2, B0 - 2]
print(f" SA={r10.somme_A}, SB={r10.somme_B}, B0={B0}")
print(f" 4 candidats (B0+k^2, B0-k^2, B0+k, B0-k) = {cands}")
print(f" primalites                = {[bool(sympy.isprime(c)) for c in cands]}")
t = sympy.symbols("t")
poly = sympy.prod(t - c for c in cands)
print(f" polynome d'annulation     = {sympy.expand(poly)}")
print(f" racines : {cands} -> DEUX racines premieres (29 ET 23).")
print(" Une equation annulante sur les candidats ne peut pas distinguer")
print(" 29 de 23 : les deux verifient toutes les congruences de SA/SB.")
print(" Le critere de choix reel = test de primalite + ordre calibre.")
