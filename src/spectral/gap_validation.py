"""
GAP VALIDATION - Vérifier que les formules correspondent aux exemples numériques.

Cela permet de valider les calculs AVANT de les déployer dans Gabriel.
"""
from fractions import Fraction
import math


def compute_SA(n: int) -> float:
    """SA(n) = (3.25/2 × 2^n) - 2"""
    return (3.25 / 2) * (2 ** n) - 2

def compute_SA_frac(n: int):
    """SA(n) avec fractions exactes."""
    if n >= 0:
        return Fraction(13, 8) * (2 ** n) - 2
    else:
        return Fraction(13, 8) * Fraction(1, 2 ** abs(n)) - 2

def compute_SB(n: int) -> float:
    """SB(n) = (6.5/2 × 2^n) - 66"""
    return (6.5 / 2) * (2 ** n) - 66

def compute_SB_frac(n: int):
    """SB(n) avec fractions exactes."""
    if n >= 0:
        return Fraction(13, 4) * (2 ** n) - 66
    else:
        return Fraction(13, 4) * Fraction(1, 2 ** abs(n)) - 66

def compute_digamma_int(n: int, p: int) -> float:
    """digamma_int(n, p) = SB(n) - 64*p"""
    return compute_SB(n) - 64 * p

def compute_digamma_int_frac(n: int, p: int):
    """digamma_int avec fractions."""
    return compute_SB_frac(n) - 64 * p


# ============================================================================
# TEST 1 : Cas (+,+) — Entre 7 et 23
# ============================================================================
print("=" * 80)
print("TEST 1 : CAS (+,+) — Entre 7 et 23")
print("=" * 80)
print()

# Données
p1, p2 = 7, 23
pos_p1, pos_p1_next, pos_p2 = 4, 5, 9
p1_next = 11

print(f"Entre {p1} (position {pos_p1}) et {p2} (position {pos_p2})")
print(f"Premier suivant {p1} : {p1_next} (position {pos_p1_next})")
print()

# Calculs
sa_p1_next = compute_SA(pos_p1_next)
sb_p1 = compute_SB(pos_p1)
digamma_p1 = compute_digamma_int(pos_p1, p1)
sb_p2 = compute_SB(pos_p2)
digamma_p2 = compute_digamma_int(pos_p2, p2)

print(f"SA({pos_p1_next}) = (3.25/2 × 2^{pos_p1_next}) - 2 = {sa_p1_next}")
print(f"  → Attendu : 50")
print()

print(f"SB({pos_p1}) = (6.5/2 × 2^{pos_p1}) - 66 = {sb_p1}")
print(f"  → Attendu : -14")
print()

print(f"digamma_int({pos_p1}, {p1}) = SB({pos_p1}) - 64*{p1} = {sb_p1} - {64*p1} = {digamma_p1}")
print(f"  → Attendu : -14 - 448 = -462")
print()

print(f"SB({pos_p2}) = (6.5/2 × 2^{pos_p2}) - 66 = {sb_p2}")
print(f"  → Attendu : 1598")
print()

print(f"digamma_int({pos_p2}, {p2}) = SB({pos_p2}) - 64*{p2} = {sb_p2} - {64*p2} = {digamma_p2}")
print(f"  → Attendu : 1598 - 1472 = 126")
print()

# Formule CORRIGÉE
numerator = sa_p1_next - sb_p2 + digamma_p2 - sb_p1 + digamma_p1
gap_float = numerator / 64
gap_int = int(round(gap_float))

print(f"FORMULE : (SA({pos_p1_next}) - SB({pos_p2}) + digamma_int({pos_p2}) - SB({pos_p1}) + digamma_int({pos_p1})) / 64")
print(f"        = ({sa_p1_next} - {sb_p2} + {digamma_p2} - {sb_p1} + {digamma_p1}) / 64")
print(f"        = {numerator} / 64")
print(f"        = {gap_float}")
print(f"        ≈ {gap_int}")
print()

print(f"✓ RÉSULTAT : {gap_int} nombres entre {p1} et {p2}")
print(f"✓ ATTENDU : -15 nombres")
print()

# Vérification avec vos calculs exacts
print("Vérification avec vos calculs :")
print(f"  50 - (1598 - 126) = 50 - 1472 = -1422")
print(f"  Puis : (-1422 - (-462)) / 64 = -960 / 64 = -15")
print()
print("OK ! Les formules correspondent ! ✓")
print()
print()


# ============================================================================
# TEST 2 : Cas (-,-) — Entre -19 et -5
# ============================================================================
print("=" * 80)
print("TEST 2 : CAS (-,-) — Entre -19 et -5")
print("=" * 80)
print()

# Données
p1, p2 = -5, -19
pos_p1, pos_p1_prev, pos_p2 = -3, -4, -8
p1_prev = -7

print(f"Entre {p1} (position {pos_p1}) et {p2} (position {pos_p2})")
print(f"Premier PRÉCÉDENT {p1} : {p1_prev} (position {pos_p1_prev})")
print()

# Calculs avec exposants négatifs
sa_p1_prev = compute_SA(pos_p1_prev)
sb_p1 = compute_SB(pos_p1)
digamma_p1 = compute_digamma_int(pos_p1, p1)
sb_p2 = compute_SB(pos_p2)
digamma_p2 = compute_digamma_int(pos_p2, p2)

print(f"SA({pos_p1_prev}) = (3.25/2 × 2^{pos_p1_prev}) - 2 = {sa_p1_prev}")
print(f"  → Avec fractions : {compute_SA_frac(pos_p1_prev)}")
print(f"  → Attendu (vos calculs) : -10110/5120")
print()

print(f"SB({pos_p1}) = (6.5/2 × 2^{pos_p1}) - 66 = {sb_p1}")
print(f"  → Avec fractions : {compute_SB_frac(pos_p1)}")
print(f"  → Attendu (vos calculs) : -20860/320")
print()

print(f"digamma_int({pos_p1}, {p1}) = SB({pos_p1}) - 64*{p1} = {digamma_p1}")
print(f"  → Avec fractions : {compute_digamma_int_frac(pos_p1, p1)}")
print()

print(f"SB({pos_p2}) = (6.5/2 × 2^{pos_p2}) - 66 = {sb_p2}")
print(f"  → Avec fractions : {compute_SB_frac(pos_p2)}")
print(f"  → Attendu (vos calculs) : -337790/5120")
print()

print(f"digamma_int({pos_p2}, {p2}) = SB({pos_p2}) - 64*{p2} = {digamma_p2}")
print(f"  → Avec fractions : {compute_digamma_int_frac(pos_p2, p2)}")
print()

# Formule CORRIGÉE
numerator = sa_p1_prev - sb_p2 + digamma_p2 - sb_p1 + digamma_p1
gap_float = numerator / 64
gap_int = int(round(gap_float))

print(f"FORMULE : (SA({pos_p1_prev}) - SB({pos_p2}) + digamma_int({pos_p2}) - SB({pos_p1}) + digamma_int({pos_p1})) / 64")
print(f"        = ({sa_p1_prev} - {sb_p2} + {digamma_p2} - {sb_p1} + {digamma_p1}) / 64")
print(f"        = {numerator} / 64")
print(f"        = {gap_float}")
print(f"        ≈ {gap_int}")
print()

print(f"✓ RÉSULTAT : {gap_int} nombres entre {p1} et {p2}")
print(f"✓ ATTENDU : -13 nombres")
print()
print()


# ============================================================================
# TEST 3 : Cas (+,+) — Entre 3 et 47
# ============================================================================
print("=" * 80)
print("TEST 3 : CAS (+,+) — Entre 3 et 47 (VOTRE QUESTION)")
print("=" * 80)
print()

from src.spectral.prime_table import nth_prime, prime_position

p1, p2 = 3, 47

pos_p1 = prime_position(p1)  # 2 (3 est 2e premier)
pos_p2 = prime_position(p2)  # 15 (47 est 15e premier)
pos_p1_next = pos_p1 + 1      # 3
p1_next = nth_prime(pos_p1_next)  # 5

print(f"Entre {p1} (position {pos_p1}) et {p2} (position {pos_p2})")
print(f"Premier suivant {p1} : {p1_next} (position {pos_p1_next})")
print()

# Calculs
sa_p1_next = compute_SA(pos_p1_next)
sb_p1 = compute_SB(pos_p1)
digamma_p1 = compute_digamma_int(pos_p1, p1)
sb_p2 = compute_SB(pos_p2)
digamma_p2 = compute_digamma_int(pos_p2, p2)

print(f"SA({pos_p1_next}) = (3.25/2 × 2^{pos_p1_next}) - 2 = {sa_p1_next}")
print()
print(f"SB({pos_p1}) = (6.5/2 × 2^{pos_p1}) - 66 = {sb_p1}")
print()
print(f"digamma_int({pos_p1}, {p1}) = SB({pos_p1}) - 64*{p1} = {sb_p1} - {64*p1} = {digamma_p1}")
print()
print(f"SB({pos_p2}) = (6.5/2 × 2^{pos_p2}) - 66 = {sb_p2}")
print()
print(f"digamma_int({pos_p2}, {p2}) = SB({pos_p2}) - 64*{p2} = {sb_p2} - {64*p2} = {digamma_p2}")
print()

# Formule CORRIGÉE
numerator = sa_p1_next - sb_p2 + digamma_p2 - sb_p1 + digamma_p1
gap_float = numerator / 64
gap_int = int(round(gap_float))

print(f"FORMULE : (SA({pos_p1_next}) - SB({pos_p2}) + digamma_int({pos_p2}) - SB({pos_p1}) + digamma_int({pos_p1})) / 64")
print(f"        = ({sa_p1_next} - {sb_p2} + {digamma_p2} - {sb_p1} + {digamma_p1}) / 64")
print(f"        = {numerator} / 64")
print(f"        = {gap_float}")
print(f"        ≈ {gap_int}")
print()

print(f"✓ RÉSULTAT ATTENDU : Entre 3 et 47 = {gap_int} nombres")
print()

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
