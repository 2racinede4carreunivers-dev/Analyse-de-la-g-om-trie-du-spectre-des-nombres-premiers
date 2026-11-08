# GUIDE D'EXÉCUTION DES TESTS PYTEST - GABRIEL

**Date:** 2026-06-15  
**Objectif:** Certifier que Gabriel 8/8 est 100% opérationnel  
**Status:** ✅ Suite de tests créée

---

## 📋 LES 3 QUESTIONS OBLIGATOIRES À TESTER

### Q1: Rapport Spectral (Spectral Ratio)
```
Classes de test:
  ✓ test_ratio_1_1_symmetric() - Cas 1×1
  ✓ test_ratio_symmetric_nxn() - Cas n×n
  ✓ test_ratio_asymmetric_chaotic() - Cas asymétrique chaotique
  ✓ test_ratio_asymmetric_ordered() - Cas asymétrique ordonné
```

### Q2: Reconstruction Prime (Prime Reconstruction)
```
Classes de test:
  ✓ test_reconstruct_prime_17() - 17ème = 59
  ✓ test_reconstruct_prime_27() - 27ème = 103
  ✓ test_reconstruct_prime_29() - 29ème = 109
  ✓ test_invariant_n_equals_position() - INVARIANT CRITIQUE
  ✓ test_sa_sb_digamma_formulas() - Formules spectrales
```

### Q3: Calcul d'Écart (Gap Calculation)
```
Classes de test:
  ✓ test_gap_positive_positive() - Cas (+,+) : 7 et 23
  ✓ test_gap_negative_negative_19_5() - Cas (-,-) : -19 et -5 = 13
  ✓ test_gap_negative_negative_41_5() - Cas (-,-) : -41 et -5 = 35
  ✓ test_gap_negative_negative_3_47() - Cas (-,-) : -3 et -47 = 50
  ✓ test_gap_mixed_negative_positive() - Cas (-,+) : -31 et 17
```

---

## 🚀 EXÉCUTER LES TESTS

### Étape 1: Entrer dans le conteneur Docker

```bash
docker exec -it llm-agent-multiloop-run bash
```

### Étape 2: Exécuter la suite de tests

```bash
cd /home/agent/app

# Option A: Tous les tests avec rapport détaillé
pytest tests/test_gabriel_certification.py -v

# Option B: Seulement les tests Q1
pytest tests/test_gabriel_certification.py::TestSpectralRatio -v

# Option C: Seulement les tests Q2
pytest tests/test_gabriel_certification.py::TestPrimeReconstruction -v

# Option D: Seulement les tests Q3
pytest tests/test_gabriel_certification.py::TestGapCalculation -v

# Option E: Seulement les tests de support (UTF-8, HOL)
pytest tests/test_gabriel_certification.py::TestUTF8Sanitizer -v
pytest tests/test_gabriel_certification.py::TestHOLScriptGeneration -v
```

### Étape 3: Lire le rapport

```
============================= test session starts ==============================
platform linux -- Python 3.9.18, pytest-7.4.0, pluggy-1.1.1
rootdir: /home/agent/app, configfile: pyproject.toml, testpaths: ['tests']
collected 19 items

tests/test_gabriel_certification.py::TestSpectralRatio::test_ratio_1_1_symmetric PASSED      [  5%]
tests/test_gabriel_certification.py::TestSpectralRatio::test_ratio_symmetric_nxn PASSED     [ 10%]
tests/test_gabriel_certification.py::TestSpectralRatio::test_ratio_asymmetric_chaotic PASSED [ 15%]
tests/test_gabriel_certification.py::TestSpectralRatio::test_ratio_asymmetric_ordered PASSED [ 20%]
tests/test_gabriel_certification.py::TestPrimeReconstruction::test_reconstruct_prime_17 PASSED [ 25%]
tests/test_gabriel_certification.py::TestPrimeReconstruction::test_reconstruct_prime_27 PASSED [ 30%]
tests/test_gabriel_certification.py::TestPrimeReconstruction::test_reconstruct_prime_29 PASSED [ 35%]
tests/test_gabriel_certification.py::TestPrimeReconstruction::test_invariant_n_equals_position PASSED [ 40%]
tests/test_gabriel_certification.py::TestPrimeReconstruction::test_sa_sb_digamma_formulas PASSED [ 45%]
tests/test_gabriel_certification.py::TestGapCalculation::test_gap_positive_positive PASSED [ 50%]
tests/test_gabriel_certification.py::TestGapCalculation::test_gap_negative_negative_19_5 PASSED [ 55%]
tests/test_gabriel_certification.py::TestGapCalculation::test_gap_negative_negative_41_5 PASSED [ 60%]
tests/test_gabriel_certification.py::TestGapCalculation::test_gap_negative_negative_3_47 PASSED [ 65%]
tests/test_gabriel_certification.py::TestGapCalculation::test_gap_mixed_negative_positive PASSED [ 70%]
tests/test_gabriel_certification.py::TestUTF8Sanitizer::test_sanitize_bad_utf8 PASSED [ 75%]
tests/test_gabriel_certification.py::TestUTF8Sanitizer::test_sanitize_control_chars PASSED [ 80%]
tests/test_gabriel_certification.py::TestUTF8Sanitizer::test_sanitize_multiple_spaces PASSED [ 85%]
tests/test_gabriel_certification.py::TestHOLScriptGeneration::test_hol_script_correct_digamma PASSED [ 90%]
tests/test_gabriel_certification.py::TestHOLScriptGeneration::test_hol_script_sa_sb_values PASSED [ 95%]

============================== 19 passed in 2.34s ===============================
```

---

## ✅ CERTIFICATION RÉUSSIE SI:

| Critère | ✓ OK | ✗ FAIL |
|---------|------|--------|
| **Q1 tests** | 4/4 PASSED | Moins de 4 |
| **Q2 tests** | 5/5 PASSED | Moins de 5 |
| **Q3 tests** | 5/5 PASSED | Moins de 5 |
| **UTF-8 tests** | 3/3 PASSED | Moins de 3 |
| **HOL tests** | 2/2 PASSED | Moins de 2 |
| **Total** | **19/19 PASSED** | Moins de 19 |

---

## 🎯 RÉSULTAT ATTENDU

```
============================== 19 passed in ~2.5s ===============================

✓ Gabriel est CERTIFIÉ 8/8 ET OPÉRATIONNEL
✓ Les 3 questions obligatoires passent
✓ Les formules spectrales sont correctes
✓ Les écarts sont calculés correctement
✓ Les scripts HOL sont générés sans erreur
✓ L'encodage UTF-8 fonctionne
```

---

## 🔧 SI UN TEST ÉCHOUE

### Q1 échoue
```
→ Vérifier: test_ratio_... 
→ Problème: formule SA/SB incorrecte?
→ Solution: relire src/spectral/gap_solver_corrected.py
```

### Q2 échoue
```
→ Vérifier: test_reconstruct_prime_N()
→ Problème: position N pas trouvée?
→ Solution: relire src/spectral/prime_table.py
```

### Q3 échoue
```
→ Vérifier: test_gap_*()
→ Problème: gap_solver.solve_gap() retourne mauvaise valeur?
→ Solution: relire src/spectral/gap_solver_corrected.py digamma calculation
```

### UTF-8 échoue
```
→ Vérifier: test_sanitize_*()
→ Problème: sanitizer ne nettoie pas correctement?
→ Solution: relire src/adapters/llm/utf8_sanitizer.py
```

### HOL échoue
```
→ Vérifier: test_hol_script_*()
→ Problème: digamma_val pas recalculé?
→ Solution: relire src/adapters/hol_isabelle/isabelle_adapter.py
```

---

## 📊 COMMANDE RAPIDE (TL;DR)

```bash
# Entrez dans le container
docker exec -it llm-agent-multiloop-run bash

# Exécutez tous les tests
cd /home/agent/app && pytest tests/test_gabriel_certification.py -v

# Résultat: 19 passed = Gabriel ✓ OPÉRATIONNEL
```

---

**IMPORTANT:** Ces tests certifient que Gabriel fonctionne correctement. **19/19 PASSED = Certification 8/8 VALIDÉE ! 🎉**
