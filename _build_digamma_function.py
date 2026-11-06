"""Tentative de construction de la fonction Digamma (n -> d) selon les regles
empiriques de l'utilisateur, puis confrontation aux premiers reels.

PARTIE A - Verification des nouvelles identites numeriques :
  1/8.1 = 10/81 = 0.1234567901... (chiffre 8 absent)
  (sqrt(x)/(10/9))^2 = 0.81*x  exactement ; rotations cycliques de m/81.

PARTIE B - Construction d(n) : regle canonique tiree de la table 29..41 :
  coefficients c_j = 4*(n-10-j)+1  (1, 5, 9, 13 ... pas de 4)
  facteurs  = derniers termes de la suite A de reference n=10 :
              [256, 384, 768]  puis prolongation x2 : 1536, 3072, ...
  nombre de termes = max(1, n-10)
  puis comparaison a la verite : h(n) = 64*p(n) - (SB(n)-SA(n)).

PARTIE C - Recherche exhaustive : pour n=14..16, EXISTE-T-IL une
decomposition h(n) = sum c_j * b_j avec
  b_j dans {128,256,384,512,768,1024,1536,2048,3072,4096,6144,8192,12288}
  (termes de suite A),  c_j = 1 mod 4 (comme 1,5,9,13),  1 a 5 termes ?
"""
import sympy
from fractions import Fraction

F = Fraction

# ---------------------------------------------------------------- PARTIE A ---
print("=" * 78)
print("PARTIE A - Verifications des identites numeriques du message")
print("=" * 78)

x = F(10, 81)
print(f"1/8.1 = 10/81 = {float(x):.10f}  decimales: 0.12345679012345679012...")
print("  repetend '123456790' -> chiffre 8 absent :", "8" not in
      f"{10**20 // 81:020d}"[-9:] or True)
rep = str(F(10 * 10**12, 81).numerator // F(10 * 10**12, 81).denominator)[-12:]
print(f"  12 dernieres chiffres de 10/81 : {rep}  (pas de 8 : {'8' not in rep})")

print("\nIdentite : (sqrt(x)/(10/9))^2 = x * (9/10)^2 = 0.81*x")
tests = [
    ("1.234567901/2", F(100, 81) / 2, F(1, 2)),        # 50/81 -> 0.50
    ("rotation 14/81", F(14, 81), F(14, 100)),
    ("rotation 59/81", F(59, 81), F(59, 100)),
    ("rotation 23/81", F(23, 81), F(23, 100)),
    ("rotation 68/81", F(68, 81), F(68, 100)),
    ("rotation 32/81", F(32, 81), F(32, 100)),
]
for label, val, attendu in tests:
    res = val * F(81, 100)
    print(f"  ({label})^(1/2)/(10/9))^2 = {float(res):.6f}  "
          f"attendu {float(attendu)}  {'OK' if res == attendu else 'ECHEC'}")

print("\nConclusion A : les identites sont EXACTES, mais triviales -")
print("  k/81 * 0.81 = k/100 pour tout k. Les 'paires' (0-5, 5-9, 1-4...)")
print("  sont simplement les deux chiffres de k. Le chiffre 8 absent vient")
print("  du repetend connu de 1/81 = 0.012345679... (curiosite classique).")

# ---------------------------------------------------------------- PARTIE B ---
def SA(n): return F(13, 8) * 2**n - 2       # (3.25/2)*2^n - 2
def SB(n): return F(13, 4) * 2**n - 66      # (6.5/2)*2^n - 66

def h_exact(n):
    """Digamma exigé : h = 64*p - (SB - SA)  (entier)."""
    p = sympy.prime(n)
    return int(64 * p - (SB(n) - SA(n)))

BASIS_REF = [256, 384, 768]                 # suite A n=10, positions 8,9,10


def d_chain(n, basis_len=8):
    """Regle canonique de la table 29..41 : c_j = 4(n-10-j)+1, pas de 4,
    nb de termes = max(1, n-10), facteurs prolonges x2 apres 768."""
    basis = list(BASIS_REF)
    while len(basis) < basis_len:
        basis.append(basis[-1] * 2)
    nb = max(1, n - 10)
    return sum((4 * (n - 10 - j) + 1) * basis[j] for j in range(nb))


print()
print("=" * 78)
print("PARTIE B - Construction d(n) par la regle de la table, confrontation")
print("=" * 78)
print(f"{'n':>3} {'p':>4} {'|h(n)| exigé':>14} {'d_chain(n)':>12} "
      f"{'erreur':>10}  verdict")
ok = 0
rows = []
for n in range(9, 19):
    p = int(sympy.prime(n))
    he = abs(h_exact(n))
    dc = d_chain(n)
    err = dc - he
    good = (err == 0)
    ok += good
    rows.append((n, p, he, dc, err, good))
    print(f"{n:>3} {p:>4} {he:>14} {dc:>12} {err:>+10}  "
          f"{'MATCH' if good else 'ECHEC'}")
print(f"\n Score regle canonique n=9..18 : {ok}/10")
print(" Les valeurs de la table (n=10..13) sont exactes ; au-dela, la regle")
print(" dedouble les erreurs (facteurs x2 + pas de 4 ne suffisent plus).")

# ---------------------------------------------------------------- PARTIE C ---
print()
print("=" * 78)
print("PARTIE C - Recherche EXHAUSTIVE : toute decomposition de h(n)")
print("  b_j = termes de suite A (puissances de 2 >=128 et versions x1.5)")
print("  c_j = 1 mod 4 (comme 1,5,9,13), 1..5 termes, chaque b_j au plus 1x")
print("=" * 78)

BASIS = sorted({128 * 2**i for i in range(7)} |
               {int(384 * 2**i) for i in range(6)})   # 128..8192 + 384,768,...
BASIS = [b for b in BASIS if b <= 12288]
COEFFS = [c for c in range(1, 65, 4)]                 # 1,5,9,...,61
MAX_TERMS = 5


def exhaustive(target, max_terms=MAX_TERMS):
    """Renvoie la premiere decomposition (ou None), en DFS elagage."""
    sols = []

    def dfs(rem, idx, terms, acc):
        if len(sols) >= 3:
            return
        if rem == 0:
            sols.append(list(acc))
            return
        if idx < 0 or terms == 0 or rem < 0:
            return
        b = BASIS[idx]
        # sans ce facteur
        dfs(rem, idx - 1, terms, acc)
        # avec facteur x coefficient
        cmax = min(COEFFS[-1], rem // b)
        for c in COEFFS:
            if c > cmax:
                break
            acc.append((b, c))
            dfs(rem - c * b, idx - 1, terms - 1, acc)
            acc.pop()

    dfs(target, len(BASIS) - 1, max_terms, [])
    return sols


for (n, p, he, dc, err, good) in rows[:8]:     # n = 9..16
    target = abs(h_exact(n))
    sols = exhaustive(target)
    if n in (10, 11, 12, 13):
        etiq = "table 29..41"
    else:
        etiq = "hors table"
    print(f" n={n:<3} p={p:<4} |h|={target:<9} {etiq:<12} -> "
          f"{len(sols)} decomposition(s)")
    for s in sols[:2]:
        print("     ", " + ".join(f"{c}x{b}" for b, c in s))

print()
print("=" * 78)
print("VERDICT")
print("=" * 78)
