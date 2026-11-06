"""B0 EST-IL UN POLYNOME EN k ? Derivation analytique + verification.

Suites (n=10) :
  A = [k^1..k^5, k^6, k^7, k^8, k^9-k^7, k^10-k^8]
  B = [k^1..k^5, k^7, k^8, k^9, k^10-k^8, k^11-k^9]
  (B a un SAUT : T6 = k^7 au lieu de k^6)

  S_A = k+k^2+k^3+k^4+k^5+k^6+k^7+k^8 + (k^9-k^7) + (k^10-k^8)
  S_B = k+k^2+k^3+k^4+k^5 + k^7+k^8+k^9 + (k^10-k^8) + (k^11-k^9)
      = k+k^2+k^3+k^4+k^5+k^7+k^8+k^10+k^11-2k^9

  B0 = (S_B - S_A)/k^6
"""
import sympy as sp

k = sp.symbols("k")

S_A = (k**1 + k**2 + k**3 + k**4 + k**5 + k**6 + k**7 + k**8
       + (k**9 - k**7) + (k**10 - k**8))
S_B = (k**1 + k**2 + k**3 + k**4 + k**5 + k**7 + k**8 + k**9
       + (k**10 - k**8) + (k**11 - k**9))

print("S_A =", sp.expand(S_A))
print("S_B =", sp.expand(S_B))
print("S_B - S_A =", sp.expand(S_B - S_A))

diff = sp.expand(S_B - S_A)
print("\nEst-ce divisible par k^6 ?", sp.rem(diff, k**6, k) == 0)
q = sp.div(diff, k**6)[0]
print("B0(k) =", sp.expand(q))

print("\n--- verification numerique contre les ancres connues ---")
# B0 issu de la formule
for kk in (2, 3, 4, 5, 6, 7, 8, 9):
    B0_formule = int(q.subs(k, kk))
    print(f"  k={kk}: B0 = {B0_formule}")
