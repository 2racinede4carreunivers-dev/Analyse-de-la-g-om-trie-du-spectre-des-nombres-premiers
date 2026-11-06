"""Banc d'essai C1 : la fonction digamma est-elle une regle calculable de n SEUL ?

1. Verification integrale de tous les exemples du message utilisateur
   (listes de termes, formules fermees, identites digamma).
2. Test du motif de coefficients (1, 5, 9, 13 ... pas de 4) sur la base
   {256, 384, 768, 1536, ...} : prediction d(n) SANS liste de premiers,
   confrontation a la verite prime(n) pour n = 9..16.
3. Demonstration que prime_equation est une tautologie (vraie aussi pour
   un composé) — c'est ce que formalisent les lemmes "... by simp".
"""
import sympy

F = sympy.Rational


def SA(n: int) -> F:
    """(3.25/2)*2^n - 2  (n entier, positif)."""
    return F(13, 8) * 2**n - 2


def SB(n: int) -> F:
    """(6.5/2)*2^n - 66."""
    return F(13, 4) * 2**n - 66


print("=" * 78)
print("1. VERIFICATION DES EXEMPLES DU MESSAGE")
print("=" * 78)

# (n, p, liste A, liste B) telles que recopiees dans le message
exemples = [
    (9,  23, [2, 4, 8, 16, 32, 64, 128, 192, 384],
             [2, 4, 8, 16, 32, 128, 256, 384, 768]),
    (10, 29, [2, 4, 8, 16, 32, 64, 128, 256, 384, 768],
             [2, 4, 8, 16, 32, 128, 256, 512, 768, 1536]),
    (11, 31, [2, 4, 8, 16, 32, 64, 128, 256, 512, 768, 1536],
             [2, 4, 8, 16, 32, 128, 256, 512, 1024, 1536, 3072]),
    (12, 37, [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 1536, 3072],
             [2, 4, 8, 16, 32, 128, 256, 512, 1024, 2048, 3072, 6144]),
    (13, 41, [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 3072, 6144],
             [2, 4, 8, 16, 32, 128, 256, 512, 1024, 2048, 4096, 6144, 12288]),
]
for n, p, la, lb in exemples:
    okA = sum(la) == SA(n)
    okB = sum(lb) == SB(n)
    okP = sympy.prime(n) == p
    print(f" n={n:<3} p={p:<4} sommeA={sum(la):<8}(formule {SA(n)}) {'OK' if okA else 'ECHEC'}"
          f" | sommeB={sum(lb):<8}(formule {SB(n)}) {'OK' if okB else 'ECHEC'}"
          f" | prime({n})={sympy.prime(n)} {'OK' if okP else 'ECHEC'}")

# Coquille de transcription signalee : le message ecrit pour 23
#   "2+3+4+8+16+32+64+128+192+384=830"
liste_23_msg = [2, 3, 4, 8, 16, 32, 64, 128, 192, 384]
print(f"\n A(23) recopiee dans le message : somme={sum(liste_23_msg)} "
      f"(message annonce 830) -> {'OK' if sum(liste_23_msg)==830 else 'ECHEC'}")
print(f"   sans le '3' parasite : {sum([2,4,8,16,32,64,128,192,384])} = 830 "
      f"(formule {SA(9)}) -> OK")

# Exemples <= 7 termes et cas negatif -5
print(f" n=5  : liste A [2,4,8,12,24]={sum([2,4,8,12,24])} vs formule {SA(5)}"
      f" | liste B [-59.5,6.5,13,26,52]={sum(map(F,[-595,65,130,260,520]))/10} vs {SB(5)}")
sa_neg = F(13, 4) * F(1, 2**3) - 2          # 3.25*2^-3 - 2
sb_neg = F(13, 2) * F(1, 2**3) - 66         # 6.5*2^-3  - 66
print(f" n=-3 : SA={sa_neg} (message -1.59375) {'OK' if sa_neg==F(-51,32) else 'ECHEC'}"
      f" | SB={sb_neg} (message -65.1875) {'OK' if sb_neg==F(-1043,16) else 'ECHEC'}")

# Identites digamma des 4 exemples principaux
print("\n Identites digamma (les 4 exemples) :")
dig_ex = {10: (256, "-"), 11: (1280, "+"), 12: (4224, "+"), 13: (10624, "+")}
for n, (d, sens) in dig_ex.items():
    p = sympy.prime(n)
    calc = SA(n) - d if sens == "-" else SA(n) + d
    recon = (SB(n) - calc) / 64
    taut  = SB(n) - 64 * p                      # digamma_calc defini par SB - 64p
    print(f"  n={n}: SA{'-' if sens=='+' else '+'}{d}={calc} ; (SB-calc)/64={recon}"
          f" {'OK' if recon==p else 'ECHEC'} ; SB-64p={taut} "
          f"{'(egaux)' if taut==calc else '(DIFFERENTS)'}")

print()
print("=" * 78)
print("2. PREDICTION d(n) SANS LISTE DE PREMIERS — motif (1,5,9,13... pas de 4)")
print("=" * 78)
# Base supposee fixe = suite A de n=10 prolongee : 256, 384, 768, 1536, ...
base_t = [256] + [384 * 2**j for j in range(8)]


def d_pred(n: int) -> int:
    """Regle tiree des 4 exemples : coeff_j = 4*(n-10-j)+1, retenu si >= 5
    (avec le special 1*256 a n=10). Aucune connaissance de p."""
    total = 0
    for j, t in enumerate(base_t):
        c = 4 * (n - 10 - j) + 1
        if c >= 5 or (j == 0 and n == 10):
            total += c * t
    return total


print(f"{'n':>3} {'p vrai':>7} {'|g(n)| = |64p-(SB-SA)|':>24} {'d_pred(n)':>12} "
      f"{'p_pred':>8} {'verdict':>8}")
nb_ok = 0
for n in range(9, 17):
    p = int(sympy.prime(n))
    g = int(64 * p - (SB(n) - SA(n)))            # digamma implicite (verite)
    dp = int(d_pred(n))
    base = (SB(n) - SA(n)) / 64                   # 13*2^(n-9) - 1
    signe = 1 if n <= 10 else -1                  # convention des exemples
    p_pred = base + F(signe * dp, 64)
    p_pred_i = int(p_pred)
    ok = (abs(g) == dp) and (p_pred_i == p)
    nb_ok += ok
    print(f"{n:>3} {p:>7} {abs(g):>24} {dp:>12} {p_pred_i:>8} "
          f"{'MATCH' if ok else 'ECHEC':>8}")
print(f"\n Score du motif sur n=9..16 : {nb_ok}/8  (match parfait attendu si "
      f"la regle est la bonne)")

print()
print("=" * 78)
print("3. prime_equation EST UNE TAUTOLOGIE (le « by simp » des lemmes .thy)")
print("=" * 78)
q = 100                                                    # COMPOSE, volontairement
dig = SB(10) - 64 * q                                      # digamma_calc(n,p) defini par SB-64p
val = (SB(10) - dig) / 64
print(f" digamma_calc(10, {q}) = SB(10) - 64*{q} = {dig}")
print(f" prime_equation(10, {q}) = (SB - digamma_calc)/64 = {val}")
print(f" -> prime_equation(10, {q}) = {q} : IDENTIQUE pour un COMPOSÉ.")
print("    Le lemme Isabelle 'prime_equation n p = real p ... by simp' est donc")
print("    vrai pour tout p (premier ou non) : il ne contient aucun contenu de")
print("    primalite ni de prediction — c'est la circularite formalisee.")
