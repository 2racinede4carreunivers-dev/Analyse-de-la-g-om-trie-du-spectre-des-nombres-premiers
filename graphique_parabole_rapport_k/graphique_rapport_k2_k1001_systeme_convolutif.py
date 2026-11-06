import re
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

# ------------------------------------------------------------
# 1. Définition du chemin complet du fichier
# ------------------------------------------------------------
racine = os.path.dirname(os.path.abspath(__file__))
fichier = os.path.join(racine, "liste_k2_k1001_n10.txt")

# ------------------------------------------------------------
# 2. Extraction des rapports k et des ancrages premiers
# ------------------------------------------------------------
k_vals = []
ancre_vals = []

# Exemple de ligne dans le fichier :
# 1/9 (non typique) | ancre=58337 | P(n=10)=58337 | [PREMIER TROUVE]
pattern = re.compile(r"1/(\d+).*?ancre=([0-9]+).*?\[PREMIER TROUVE\]")

with open(fichier, "r", encoding="utf-8") as f:
    for ligne in f:
        m = pattern.search(ligne)
        if m:
            k = int(m.group(1))
            ancre = int(m.group(2))
            k_vals.append(k)
            ancre_vals.append(ancre)

# ------------------------------------------------------------
# 3. Tracé des points (k, ancre)
# ------------------------------------------------------------
plt.figure(figsize=(12, 7))
plt.scatter(k_vals, ancre_vals, s=12, color="blue",
            label="Ancrages retournant un premier (n=10)")

plt.xlabel("Rapport typique / non typique (k)")
plt.ylabel("Ancrage retournant un premier (n=10)")
plt.title("Progression des ancrages premiers pour n=10")

# ------------------------------------------------------------
# 4. Ajustement hyperbolique : y = A / (x - x0)
# ------------------------------------------------------------
def hyperbole(x, A, x0):
    return A / (x - x0)

k_array = np.array(k_vals)
ancre_array = np.array(ancre_vals)

params, _ = curve_fit(hyperbole, k_array, ancre_array, maxfev=10000)
A, x0 = params

x_fit = np.linspace(min(k_vals), max(k_vals), 2000)
y_fit = hyperbole(x_fit, A, x0)

plt.plot(x_fit, y_fit, color="red", linewidth=2,
         label=f"Hyperbole ajustée : y = {A:.3e} / (x - {x0:.3f})")

plt.legend()
plt.grid(True)
sortie = os.path.join(racine, "graphique_parabole_rapport_k.png")
plt.savefig(sortie, dpi=150, bbox_inches="tight")
print(f"Graphique sauvegarde : {sortie}")

# ------------------------------------------------------------
# 5. Affichage de la règle de l’hyperbole
# ------------------------------------------------------------
print("\n=== RÈGLE DE L'HYPERBOLE OBTENUE ===")
print(f"y = {A:.10e} / (x - {x0:.10f})")
print("Structure similaire à la géométrie analytique de s = 1/2 + it (Zêta de Riemann).")
