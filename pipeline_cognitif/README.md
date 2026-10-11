# Pipeline Cognitif Gabriel — Niveaux 1 et 2

Reconstruction des nombres premiers a partir des rapports `1/k`, par le
systeme convolutif spectral :

- **Niveau 1 (entier)** : suites A et B a termes entiers (`k^i`), regles
  Savard terme a terme, 4 possibilites Digamma, division par `k^6`.
- **Niveau 2 (geometrique)** : memes suites en forme `sqrt(a^2 + b^2)` avec
  `a1 = sqrt(1 + k^2)`. Chaque terme geometrique vaut exactement
  `a1 x terme entier`, donc le facteur s'annule dans
  `(Somme_B - Digamma) / k^6` : **les deux niveaux ont les memes utilites**.

Dépendances : `sympy` pour les tests de primalité et les rangs du dispatcher;
`numpy` est utilisé par `metaphore_geometrique.py`. Le healthcheck lit aussi le
classeur avec `openpyxl` et inspecte le PDF avec `pypdf`.

## Contenu

| Fichier | Role |
|---|---|
| `suites_geometriques_niveau2.py` | Coeur : calculateurs niveaux 1 et 2, Digamma, formes fermees, ancrages XIV |
| `reconstruction_premiers_1_sur_k.py` | Reconstructeur de reference 1/7 (16519 via `S_A - 7^8`) |
| `multi_ratio_dispatcher.py` | API multi-rapports publique, rapports typiques et non typiques |
| `gabriel_geometric_wrapper_v74.py` | Wrapper `reconstruire_multi_k` autour du dispatcher |
| `Suites_geometriques_AB.py` | Suites A/B geometriques generales |
| `fallback_geometrique.py` | Repli geometrique si l'approche algebrique echoue |
| `metaphore_geometrique.py` | Bloc « Structure Geometrique Spatiale » des reponses |
| `validation_section_xiv.py` | Validation de conformite a la Section XIV (exit 0 = conforme) |
| `Healthcheck_convolutif_HOL.py` | Healthcheck des sources, dependances, calculs et session Isabelle |

## Usage

```python
from pipeline_cognitif import (
  MultiRatioDispatcher, CalculateurNiveau1Entiers,
  CalculateurNiveau2Geometrique,
)

# Une requete groupe plusieurs rapports 1/k pour un meme n.
p = MultiRatioDispatcher()
r = p.requete(n=10, liste_k=[2, 7, 10, 20])
print(r.rapport_texte())
# k=2 et k=7 utilisent leurs branches cataloguees ; k=10 et k=20
# exposent plusieurs candidats sans en choisir un automatiquement.

# Niveau 1 direct
calc = CalculateurNiveau1Entiers(k=7)
res = calc.calculer(10)    # S_A = 322966112, S_B = 2260645142

# Validation de conformite (0 ecart attendu)
#   python -m pipeline_cognitif.validation_section_xiv
# ou, en execution directe :
#   python pipeline_cognitif/validation_section_xiv.py
# Healthcheck des dependances et de la session Isabelle :
#   python pipeline_cognitif/Healthcheck_convolutif_HOL.py
#   python pipeline_cognitif/Healthcheck_convolutif_HOL.py --build-hol
```


## Conformite a la Section XIV de `methode_spectral.thy`

Verifiee par `validation_section_xiv.py` (**0 ecart**, code de sortie 0) :

| Controle | Reference | Resultat |
|---|---|---|
| Ancrages n=10 : rangs officiels = rangs reels dans P | XIV.6 | k=2..9 conformes (29, 227, 947, 2999, 7529, 16519, 32327, 58337) |
| Formes fermees universelles `S_A`, `S_B` | XIV.2 | exactes pour n >= 8 (arithmetique `Fraction`) |
| Construction terme a terme | XIV.4 | niveau 1 exact pour tout n ; niveau 2 = `a1 x XIV.4` |
| Validation exacte k=8, n=34 | XIV.7 | `S_A`, `S_B`, Digamma conformes au chiffre pres ; P = 32537 (rang 3492) |
| Decalage de rang `rang(n) = rang_ancre + (n - 10)` | XIV.6 | k=3, n=9..17 : 223, 227, 229, 233, 239, 241, 251, 257, 263 |
| Niveau 2 : memes ancrages que le niveau 1 | XIV.5 | 8/8 conformes |

### Constantes universelles (XIV.1)

```
C = k^4 - k^2 + 1            m = k^6 - k^5 + 1
alphaA = 2C / ((k-1) k^3)    alphaB = k * alphaA
offsetA = k / (k-1)          offsetB = m k / (k-1)
S_A(n) = (alphaA/2) k^n - offsetA      S_B(n) = (alphaB/2) k^n - offsetB
```

### Domaine des formes fermees (XIV.2 vs XIV.4)

XIV.2 et XIV.4 coincident exactement a partir de **n = 8** (seuil ou les
deux termes terminaux Savard et le saut Zeta s'appliquent). Pour **n <= 7**,
XIV.4 impose `terme_b = terme_a` (progression simple sans condition
terminale) et fait foi : l'implementation retourne la construction XIV.4
telle quelle (`SEUIL_FORMES_FERMEES = 8` dans `suites_geometriques_niveau2.py`).

### Convention Digamma (XIV.5)

Ordre d'evaluation : `(8,-1), (8,+1), (7,+1), (7,-1)`. Les branches
premieres sont toutes conservees. Pour les rapports k=2..9, le catalogue
choisit explicitement l'ancre documentee; hors catalogue, plusieurs branches
premieres produisent un statut ambigu, sans selection automatique.

## Notes

- `n` est toujours un entier strictement positif (`valider_n` le garantit).
- Toute l'arithmetique du niveau 1 est exacte (`int` / `Fraction`) ; le
  niveau 2 calcule le Digamma sur les composantes zeta entieres pour eviter
  toute erreur d'arrondi flottant.
- Les imports internes sont relatifs avec repli absolu : le dossier
  fonctionne comme package (`from pipeline_cognitif import ...`) et en
  execution directe des scripts.
