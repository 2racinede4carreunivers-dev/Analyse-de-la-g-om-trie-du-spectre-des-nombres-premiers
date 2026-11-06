"""Verification croisee des deux derniers ancres (k = 3999995 et 3999996).

Double controle :
  1. sympy.isprime (test de primalite BPSW de sympy)
  2. Miller-Rabin maison, bases = 200 premiers nombres premiers + bases aleatoires
"""
import random
import sympy

NUMS = [
    ("1/3999995", 1023993600015935980240012199996999),
    ("1/3999996", 1023994880010175989952004927999039),
]


def miller_rabin(n, bases):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in bases:
        a %= n
        if a == 0:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


first_primes = list(sympy.primerange(2, 1100))  # 200 premiers premiers (< 1100)
rng = random.Random(20261019)
random_bases = [rng.randrange(2, 10**6) for _ in range(100)]

fail = False
for label, n in NUMS:
    s = sympy.isprime(n)
    mr = miller_rabin(n, first_primes + random_bases)
    digits = len(str(n))
    print(f"{label} | {n}")
    print(f"   digits={digits} | pair={n % 2 == 0} | sympy.isprime={s} | "
          f"Miller-Rabin({len(first_primes)}+100 bases)={mr}")
    print(f"   factorint (sympy) = {sympy.factorint(n)}")
    if not (s and mr):
        fail = True

print()
print("VALIDATION LOCALE : OK" if not fail else "VALIDATION LOCALE : ECHEC")
