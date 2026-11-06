"""Permutation atomique : gap_solver_corrected_new.py -> gap_solver_corrected.py."""
import os

BASE = (
    r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers"
    r"\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
    r"\src\spectral"
)
old = os.path.join(BASE, "gap_solver_corrected.py")
new = os.path.join(BASE, "gap_solver_corrected_new.py")
tmp = os.path.join(BASE, "gap_solver_old_broken.py")

assert os.path.exists(new), "fichier nouveau manquant : " + new
if os.path.exists(old):
    os.replace(old, tmp)
    print("ancien fichier mis en veillese :", tmp)
os.replace(new, old)
print("OK ->", old)
print("lignes :", sum(1 for _ in open(old, encoding="utf-8")))
