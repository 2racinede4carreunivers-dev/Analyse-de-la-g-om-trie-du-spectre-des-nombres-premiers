# Corpus mathématique — Méthode Spectrale de Philippe Thomas Savard

## Concepts fondamentaux

### Suites de base (Rapport 1/2)
- `SA n = (3.25/2) * 2^n - 2`
- `SB n = (6.5/2) * 2^n - 66`
- `SB n = 2 * SA n - 62` (relation affine)

### Rapport spectral 1/2
- `RsP n1 n2 = (SA n1 - SA n2) / (SB n1 - SB n2) = 1/2`
- Valide pour `n1 >= 1`, `n2 >= 1`, `n1 ≠ n2`

### Digamma calculé
- `digamma_calc n p = SB n - 64 * p`
- `prime_equation n p = (SB n - digamma_calc n p) / 64 = p`

### Modèle 1/3
- `A_1_3 n = ((73/9)/12) * 3^n - 1.5`
- `B_1_3 n = ((219/9)/12) * 3^n - (487 * 1.5)`
- Facteur de normalisation : 729 = 3^6
- Exemple validé : premier 227 (n=10)

### Modèle 1/4
- `A_1_4 n = ((241/16)/12) * 4^n - 4/3`
- `B_1_4 n = ((964/16)/12) * 4^n - (3073 * 4/3)`
- Facteur de normalisation : 4096 = 4^6
- Exemple validé : premier 947

### Suites mixtes (-,+)
- `SA_mix n = 48 + 13/(2^(n+2))`
- `SB_mix n = -28 + 13/(2^(n+1))`
- Permet la reconstruction de premiers via configurations mixtes

### Suites négatives
- `SA_neg_eq n = 3.25 * 2^n - 2` (n réel)
- `SB_neg_eq n = 6.5 * 2^n - 66`
- Rapport spectral 1/2 négatif (axiomatique)

## Géométrie spectrale

### Asymétrie ordonnée
- A_indices et B_indices strictement croissants
- length(B) = length(A) + 1
- last(A) < hd(B)

### Asymétrie chaotique
- length(A) ≠ length(B)
- Pas d'ordre strict imposé

## Plan trifocal — Validation épipolaire

Trois axes :
1. **FZg** : Fonction Zêta (globale)
2. **HyRi** : Hypothèse de Riemann
3. **MsP** : Méthode spectrale + position des premiers

Postulats clés :
- `FZg_posP p = Ms_posP p` (positions coïncident)
- `HypR_demi = Ms_demi = 1/2`
- `T_area = T_tr_area + T_restant_area`
- `Com_Pinit_Re < Com_ident` (sur-combinatoire mixte)
- Courbure de droite critique : `Aire_parab = T_restant_area` → `HypR_demi_solFinal`

## Lien avec Riemann

- Conjecture : `∀ρ. Re(ρ) = 1/2`
- Formule explicite : `ψ(x) = x - Σ_ρ x^ρ/ρ + ...`
- Concordance spectrale : `∀n. prime_position_from_zero (zero_associe n) (A_suite n + B_suite n)`

## Exemples numériques validés

| Premier | Modèle | n | Vérification |
|---------|--------|---|--------------|
| 29      | 1/2    | 10 | `(SB(10) - digamma_calc(10,29))/64 = 29` |
| 31      | 1/2    | 11 | `(SB(11) - digamma_calc(11,31))/64 = 31` |
| 37      | 1/2    | 12 | `(SB(12) - digamma_calc(12,37))/64 = 37` |
| 41      | 1/2    | 13 | `(SB(13) - digamma_calc(13,41))/64 = 41` |
| 227     | 1/3    | -  | `(suite_B_1_3 - digamma_calcule_1_3)/729 = 227` |
| 947     | 1/4    | -  | `(suite_B_1_4 - digamma_calcule_1_4)/4096 = 947` |

## Écarts entre premiers

### Modèle 1/3
`gap_equation_1_3 A_next B_high D_high D_low = (A_next - B_high + D_high - D_low)/729 = p_low - p_high`

### Modèle 1/4
`gap_equation_1_4 A_next B_high D_high D_low = (A_next - B_high + D_high - D_low)/4096 = p_low - p_high`

Exemples :
- Écart 227 ↔ 173 (1/3) = -53
- Écart 947 ↔ 881 (1/4) = -65
- Écart -19 ↔ -5 (négatif) = -13
- Écart -31 ↔ 17 (mixte) = -47
