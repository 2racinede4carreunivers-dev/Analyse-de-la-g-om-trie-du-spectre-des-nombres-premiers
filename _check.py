"""Validation du GapSolver reconstruit (formule .thy, Fraction exacte)."""
import sys

OUT = open(
    r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
    r"\_check_result.txt",
    "w",
    encoding="utf-8",
)


class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()


sys.stdout = Tee(sys.__stdout__, OUT)
sys.stderr = Tee(sys.__stderr__, OUT)

PROJ = (
    r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
    r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
)
sys.path.insert(0, PROJ)

import py_compile

py_compile.compile(
    PROJ + r"\src\spectral\gap_solver_corrected.py", doraise=True
)
print("COMPILE OK")

from src.spectral.gap_solver_corrected import GapSolver

solver = GapSolver()
failures = []


def check(name, cond, detail=""):
    if cond:
        print("PASS", name)
    else:
        print("FAIL", name, detail)
        failures.append(name)


# --- Exemples .thy ---
r = solver.solve_gap(23, 7)
check("thy (23,7)=-15", r is not None and r.gap_count == -15,
      r.gap_count if r else None)
r = solver.solve_gap(-19, -5)
check("thy (-19,-5)=-13", r is not None and r.gap_count == -13,
      r.gap_count if r else None)
r = solver.solve_gap(-31, 17)
check("thy (-31,17)=-47", r is not None and r.gap_count == -47,
      r.gap_count if r else None)

# --- Certification : types + normalisation ---
r = solver.solve_gap(7, 23)
check("cert (+,+) type", r is not None and r.gap_type == "positive_positive")
check("cert (+,+) p1=7,p2=23", r.p1 == 7 and r.p2 == 23)
r = solver.solve_gap(-19, -5)
check("cert (-,-) p1=-19,p2=-5", r.p1 == -19 and r.p2 == -5)
check("cert (-,-) |gap|=13", abs(r.gap_count) == 13, r.gap_count)
r = solver.solve_gap(-41, -5)
check("cert (-41,-5) |gap|=35", r is not None and abs(r.gap_count) == 35)
r = solver.solve_gap(-3, -47)
check("cert (-3,-47) |gap|=43", r is not None and abs(r.gap_count) == 43)

# --- Mixte + pont ZERO (tests non-regression) ---
r = solver.solve_gap(-31, 17)
check("mixed type", r.gap_type == "mixed")
check("mixed p1=-31,p2=17", r.p1 == -31 and r.p2 == 17)
check("mixed |gap|=47", abs(r.gap_count) == 47, r.gap_count)
check("mixed digamma_max=-738", abs(r.digamma_max - (-738.0)) < 1e-6,
      r.digamma_max)

r = solver.solve_gap(-2, 37)
check("bridge (-2,37) not None", r is not None)
check("bridge |gap|=38", r is not None and abs(r.gap_count) == 38)
check("bridge zero_bridge", r.validation.get("zero_bridge") is True)
check("bridge zero_special", r.validation.get("zero_special") is True)
check("bridge pos_suivant=0", r.position_suivant_min == 0)
check("bridge p_suivant=0", r.p_suivant_min == 0)
check("bridge expl ZÉRO", "ZÉRO" in r.explanation)
check("bridge expl pont", "pont" in r.explanation.lower())

r2 = solver.solve_gap(37, -2)
check("bridge order-independent",
      r2 is not None and r2.gap_count == r.gap_count
      and r2.p1 == r.p1 and r2.p2 == r.p2)

for p_max, exp in [(3, 4), (5, 6), (7, 8), (11, 12), (13, 14), (17, 18),
                   (19, 20), (23, 24), (37, 38), (41, 42), (97, 98)]:
    r = solver.solve_gap(-2, p_max)
    ok = (r is not None and abs(r.gap_count) == exp
          and r.validation.get("zero_bridge") is True)
    check("bridge (-2,%d)=%d" % (p_max, exp), ok,
          r.gap_count if r else None)

for p_min, p_max, exp in [(-3, 5, 7), (-5, 7, 11), (-7, 11, 17),
                          (-11, 13, 23), (-13, 17, 29), (-17, 19, 35),
                          (-19, 23, 41), (-23, 29, 51), (-29, 31, 59),
                          (-31, 17, 47)]:
    r = solver.solve_gap(p_min, p_max)
    ok = (r is not None and abs(r.gap_count) == exp
          and r.validation.get("zero_bridge") is False)
    check("mixed (%d,%d)=%d" % (p_min, p_max, exp), ok,
          r.gap_count if r else None)

# --- SA(0) ---
sa0 = solver._compute_SA_negative(0)
check("SA(0)=-0.375", abs(float(sa0) - (-0.375)) < 1e-9)

# --- Bornes superieures / cas limites ---
for a, b, exp in [(58, 59, -1), (541, 547, -5), (881, 947, -65),
                  (99991, 99989, -1), (99991, 99979, -11),
                  (169, 171, -1), (99991, 99991, 1)]:
    r = solver.solve_gap(a, b)
    check("bornes (%d,%d)=%d" % (a, b, exp), r is not None
          and r.gap_count == exp, r.gap_count if r else None)

r = solver.solve_gap(-99989, -99991)
check("bornes (-99989,-99991)=-1", r is not None and r.gap_count == -1,
      r.gap_count if r else None)

r = solver.solve_gap(0, 0)
check("(0,0) -> None", r is None)

# --- Instantiation pipeline ---
r = solver.solve_gap(-101, 2)
check("(-101,2)=-102", r is not None and r.gap_count == -102)
r = solver.solve_gap(2, -101)
check("(2,-101)=-102", r is not None and r.gap_count == -102)

try:
    GapSolver(spectral_core=None)
    check("GapSolver(spectral_core=...)", True)
except TypeError as exc:
    check("GapSolver(spectral_core=...)", False, str(exc))

# --- Overflow : grandes positions sans crash ---
r = solver.solve_gap(99991, 99989)
check("grand n sans OverflowError", r is not None and r.gap_count == -1)

print()
if failures:
    print("ECHECS :", failures)
    sys.exit(1)
print("TOUS LES TESTS PASSENT")
