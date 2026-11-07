# 🎯 GABRIEL PARAMETRIC VALIDATION - EXEMPLES PRATIQUES

## Exemple 1: Validation simple avec rayons

**Demande utilisateur:**
```
"Vérifie si C:\schema\beau_soleil.png a des rayons"
```

**Code Gabriel:**
```python
from complete_validation_integration import validate_image_parametric

result = validate_image_parametric(
    "C:/schema/beau_soleil.png",
    criteria=['rayons']
)

if result.success:
    print(result.combined_report)
    print(f"✓ Rayons détectés: {result.confidence:.1%} confiance")
```

**Résultat attendu:**
```
✓ Figure valide - 8 rayons uniformes
Confiance: 92%
Variation: 3.2%
```

---

## Exemple 2: Validation en langage naturel

**Demande utilisateur:**
```
"C:\figures\mon_triangle.png est-il équilatéral avec des rayons?"
```

**Code Gabriel:**
```python
from complete_validation_integration import validate_image_natural_language

result = validate_image_natural_language(
    "C:/figures/mon_triangle.png",
    "est-il équilatéral avec des rayons?"
)

print(result.combined_report)
```

**Résultat attendu:**
```
✓ FIGURE VALIDE
  - Équilatéral: ✓ (variation 1.2%)
  - Rayons: ✓ (3 rayons uniformes)
Confiance globale: 95%
```

---

## Exemple 3: Validation de cercle parfait

**Demande utilisateur:**
```
"Valide si C:/cercle.png est un cercle avec rayons uniformes"
```

**Code Gabriel:**
```python
from complete_validation_integration import get_complete_validation_system

system = get_complete_validation_system()

# Créer dataset théorique
theoretical = system.create_theoretical_dataset(
    figure='circle',
    radius=100,
    center=(200, 200)
)

# Valider
result = system.validate_image_complete(
    "C:/cercle.png",
    criteria=['cercle', 'rayons'],
    theoretical_data=theoretical
)

print(result.combined_report)
```

**Résultat attendu:**
```
✓ CERCLE DÉTECTÉ
  - Radius théorique: 100
  - Radius mesuré: 99.8
  - Rayons uniformes: ✓
  - Erreur: 0.2%
Confiance: 97%
```

---

## Exemple 4: Validation de triangle théorique

**Demande utilisateur:**
```
"C:/triangle.png respecte-t-il un triangle équilatéral de côté 150?"
```

**Code Gabriel:**
```python
system = get_complete_validation_system()

# Dataset théorique
theoretical = system.create_theoretical_dataset(
    figure='triangle',
    side_length=150
)

result = system.validate_image_complete(
    "C:/triangle.png",
    criteria=['équilatéral', 'distances'],
    theoretical_data=theoretical
)

print(result.combined_report)
```

**Résultat attendu:**
```
✓ TRIANGLE ÉQUILATÉRAL
  Côtés théoriques: 150
  Côtés mesurés: 150.2, 149.8, 150.1
  Variation max: 0.2%
  
✓ Distances validées
Confiance: 96%
```

---

## Exemple 5: Validation avec symétrie

**Demande utilisateur:**
```
"Vérifie que C:/figure.png a une symétrie verticale et des rayons"
```

**Code Gabriel:**
```python
result = validate_image_parametric(
    "C:/figure.png",
    criteria=['symétrie', 'rayons']
)

for validation in result.validation_results.get('validations', []):
    print(f"{validation.criterion_name}: {'✓' if validation.valid else '✗'}")

print(result.combined_report)
```

**Résultat attendu:**
```
✓ symétrie: ✓ (verticale détectée)
✓ rayons: ✓ (8 rayons)
Figure valide: OUI
```

---

## Exemple 6: Validation comparée (Image vs Théorie)

**Demande utilisateur:**
```
"Compare C:/rectangle.png avec un rectangle 200x150"
```

**Code Gabriel:**
```python
system = get_complete_validation_system()

theoretical = system.create_theoretical_dataset(
    figure='rectangle',
    width=200,
    height=150
)

result = system.validate_image_complete(
    "C:/rectangle.png",
    criteria=['rectangle', 'distance'],
    theoretical_data=theoretical
)

# Afficher les détails
print(f"Validations effectuées:")
for v in result.validation_results['validations']:
    if v.valid:
        print(f"  ✓ {v.criterion_name}")
        print(f"    Attendu: {v.expected_value}")
        print(f"    Mesuré: {v.actual_value}")
```

**Résultat attendu:**
```
✓ rectangle
  Attendu: 90°
  Mesuré: 89.8°

✓ distance
  P0-P1 attendu: 200, mesuré: 199.9
  P0-P3 attendu: 150, mesuré: 150.1
```

---

## Exemple 7: Validation de plusieurs critères

**Demande utilisateur:**
```
"Valide si C:/etoile.png a des rayons, de la symétrie et est régulière"
```

**Code Gabriel:**
```python
result = validate_image_parametric(
    "C:/etoile.png",
    criteria=['rayons', 'symétrie', 'régulier']
)

print(f"Critères vérifiés: {result.validation_criteria}")
print(f"Nombre de validations: {len(result.validation_results['validations'])}")

# Afficher un résumé
for v in result.validation_results['validations']:
    status = "✓" if v.valid else "✗"
    print(f"{status} {v.criterion_name}: {v.confidence:.1%}")

print(f"\nRésultat global: {'VALIDE' if result.is_valid else 'INVALIDE'}")
```

**Résultat attendu:**
```
✓ rayons: 98%
✓ symétrie: 92%
✓ régulier: 88%

Résultat global: VALIDE (confiance 92%)
```

---

## Exemple 8: Détection de rayons dans soleil

**Demande utilisateur:**
```
"Combien de rayons a C:/soleil.png? Sont-ils uniformes?"
```

**Code Gabriel:**
```python
result = validate_image_parametric(
    "C:/soleil.png",
    criteria=['rayons']
)

# Extraire les détails des rayons
validation = [v for v in result.validation_results['validations'] 
              if v.criterion_name == 'rayons'][0]

if validation.valid:
    details = validation.details
    print(f"✓ Rayons détectés: {details['count']}")
    print(f"  Rayon moyen: {details['average_radius']:.1f}px")
    print(f"  Écart-type: {details['std_deviation']:.1f}px")
    print(f"  Variation: {details['variation_percent']:.1f}%")
    
    if details['variation_percent'] < 5:
        print("  ✓ Rayons uniformes")
    elif details['variation_percent'] < 10:
        print("  ⚠ Rayons peu uniformes")
    else:
        print("  ✗ Rayons très irréguliers")
```

**Résultat attendu:**
```
✓ Rayons détectés: 12
  Rayon moyen: 95.5px
  Écart-type: 2.1px
  Variation: 2.2%
  ✓ Rayons uniformes
```

---

## Exemple 9: Validation avec tolerance personnalisée

**Code Gabriel:**
```python
# Créer un validateur personnalisé
from parametric_validation_module import ParametricValidator

validator = ParametricValidator()

# Valider avec tolerance élevée (15%)
result = validator.validate_figure(
    points=[(0,0), (100,0), (50,86.6)],
    criteria='équilatéral',
    theoretical_data={'expected_distances': {
        'P0_P1': 100,
        'P0_P2': 100,
        'P1_P2': 100,
    }}
)

for v in result['validations']:
    print(f"{v.criterion_name}: {v.tolerance}% tolérance")
```

---

## Exemple 10: Chaîne complète (Vision + Validation)

**Demande utilisateur:**
```
"Analyse C:/schema/complexe.png et valide si c'est un hexagone régulier
avec des rayons uniformes depuis le centre"
```

**Code Gabriel:**
```python
from complete_validation_integration import validate_image_natural_language

result = validate_image_natural_language(
    "C:/schema/complexe.png",
    "hexagone régulier avec rayons uniformes"
)

if result.success:
    print("=== ANALYSE VISION ===")
    print(result.analysis_report)
    
    print("\n=== VALIDATION PARAMÉTRIQUE ===")
    print(result.validation_report)
    
    print("\n=== RAPPORT COMBINÉ ===")
    print(result.combined_report)
    
    print(f"\n✓ RÉSULTAT: {'VALIDE' if result.is_valid else 'INVALIDE'}")
    print(f"Confiance: {result.confidence:.1%}")
else:
    print(f"✗ Erreur: {result.error_message}")
```

**Résultat attendu:**
```
=== ANALYSE VISION ===
Figure détectée: Hexagone
Points: 6
...

=== VALIDATION PARAMÉTRIQUE ===
✓ régulier: Côtés égaux, angles égaux
✓ rayons: 6 rayons uniformes
...

=== RAPPORT COMBINÉ ===
HEXAGONE RÉGULIER VALIDE
Tous les critères passés
Confiance globale: 94%
```

---

## Usage dans Gabriel Chat

```
Utilisateur: "Valide C:/image.png pour des rayons"
Gabriel: ✓ Image accessible (520 KB)
Gabriel: [Lance analyse vision]
Gabriel: [Extrait points géométriques]
Gabriel: [Valide critères]
Gabriel: "Figure valide! 8 rayons détectés avec variation 2.3%"

Utilisateur: "Compare avec radius=100"
Gabriel: [Crée dataset théorique]
Gabriel: [Valide: radius=99.8]
Gabriel: "Conforme à la théorie (erreur 0.2%)"
```

---

**Status: ✅ PRÊT À L'EMPLOI**
