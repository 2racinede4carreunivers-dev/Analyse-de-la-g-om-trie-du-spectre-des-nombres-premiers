"""Verification integrite de la table PRIMES_RAW contre un crible local."""
import sys

N = 100001
sieve = bytearray([1]) * N
sieve[0] = sieve[1] = 0
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]:
        sieve[i * i::i] = bytearray(len(range(i * i, N, i)))
true = [i for i in range(N) if sieve[i]]

sys.path.insert(0, (
    r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
    r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
))
from src.spectral._primes_data import PRIMES_RAW

print("true count", len(true), "table", len(PRIMES_RAW))
tset = set(true)
pset = set(PRIMES_RAW)
print("missing from table:", [p for p in true if p not in pset])
print("extra in table:", [p for p in PRIMES_RAW if p not in tset])
first_diff = next(
    (i for i, (a, b) in enumerate(zip(true, PRIMES_RAW)) if a != b), None
)
print("first diff index:", first_diff)
if first_diff is not None:
    print("around diff:", true[first_diff - 3:first_diff + 4],
          PRIMES_RAW[first_diff - 3:first_diff + 4])
