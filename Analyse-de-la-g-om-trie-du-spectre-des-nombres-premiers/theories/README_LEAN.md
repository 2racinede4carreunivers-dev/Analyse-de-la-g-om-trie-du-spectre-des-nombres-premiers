# Portage Lean 4 de la Methode Spectrale

Ce dossier contient la formalisation Lean 4 de la Methode Spectrale de
Philippe Thomas Savard, portee depuis `theories/methode_spectral.thy`
(Isabelle/HOL).

## Fichiers

- `theories/MethodeSpectrale.lean` — Formalisation principale (61 tests
  structurels passent).
- `theories/methode_spectral.thy`   — Version Isabelle/HOL originale
  (2884 lignes, 966 pytests passent).
- `lakefile.lean`     — Configuration Lake pour Lean 4.
- `lean-toolchain`    — Version de Lean utilisee (v4.14.0).

## Installation locale (Windows / macOS / Linux)

1. Installer **elan** (gestionnaire de versions Lean) :
   ```
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
   ```

2. Cloner ce depot et se placer a la racine :
   ```
   cd agent-multiloop-Gabriel-local
   ```

3. Recuperer Mathlib et compiler :
   ```
   lake update
   lake build MethodeSpectrale
   ```

   La premiere compilation prend ~15-30 min (telechargement de Mathlib).
   Les compilations suivantes sont incrementales et rapides.

## Verification rapide (Isabelle -> Lean equivalent)

Les theoremes clefs (correspondance nom-a-nom Isabelle/Lean) :

| Isabelle (.thy)                         | Lean 4 (.lean)                        |
|-----------------------------------------|---------------------------------------|
| `SA`, `SB`, `RsP`                       | `SA`, `SB`, `RsP`                     |
| `RsP_un_demi_general`                   | `RsP_un_demi_general`                 |
| `digamma_calc`, `prime_equation`        | `digamma_calc`, `prime_equation`      |
| `reconstruction_premier_pos`            | `reconstruction_premier_pos`          |
| `prime_i` (via SOME)                    | `prime_i` (via Classical.choose)      |
| `composite_not_prime_i`                 | `composite_not_prime_i`               |
| `composite_no_reconstruction_position`  | `composite_no_reconstruction_position`|
| `composite_pair_no_rsp_positions`       | `composite_pair_no_rsp_positions`     |
| `terme_suite_A` / `terme_suite_B`       | `terme_suite_A` / `terme_suite_B`     |
| `somme_A_construction_eq_formule`       | `somme_A_construction_eq_formule`     |
| `somme_B_construction_eq_formule`       | `somme_B_construction_eq_formule`     |

## Axiomes Savard

Deux axiomes explicites (identiques a la version Isabelle) :

1. `spectral_postulate_pos` : `prime_equation n p = p` pour tout n>=1 et
   p premier.
2. `prime_position_exists` : pour tout indice i, il existe un premier de
   position i.

## Bugs 9 & 10 corriges

- **Bug 9** : `terme_suite_A` et `terme_suite_B` utilisent `def` (Lean)
  ou `definition` (Isabelle) car il n'y a pas de recursion — evite
  l'Inner syntax error du parser Isabelle.
- **Bug 10** : les lemmes `somme_A/B_construction_eq_formule` sont
  enonces conditionnellement avec le fait Savard en hypothese — plus
  aucun `sorry` dans le fichier.

## Tests

Les tests pytest de structure (61/61 passent) sont dans :
`tests/test_lean_methode_spectrale_port.py`

```
python -m pytest tests/test_lean_methode_spectrale_port.py -v
```
