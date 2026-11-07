# ✅ CHECKLIST FINALE - CERTIFICATION GABRIEL 8/8

**Date:** 2026-06-15  
**Objectif:** Valider que Gabriel est 100% opérationnel  
**Durée:** ~5 minutes  

---

## 📋 AVANT DE LANCER LES TESTS

- [ ] Gabriel est lancé et accessible
- [ ] Docker Compose is up: `docker-compose ps`
- [ ] Container "llm-agent-multiloop-run" est RUNNING
- [ ] Ollama est accessible
- [ ] Pas d'erreur de démarrage dans les logs

---

## 🧪 EXÉCUTION DES 19 TESTS

### ÉTAPE 1: Accéder au conteneur
```bash
docker exec -it llm-agent-multiloop-run bash
```
- [ ] ✓ Vous êtes dans le bash du conteneur

### ÉTAPE 2: Aller au répertoire
```bash
cd /home/agent/app
```
- [ ] ✓ Vous êtes dans `/home/agent/app`

### ÉTAPE 3: Lancer les tests
```bash
pytest tests/test_gabriel_certification.py -v
```
- [ ] ✓ Les tests se lancent
- [ ] ⏱️ Temps d'exécution: ~2.5 secondes

---

## ✅ VALIDATION DES RÉSULTATS

### Tests Q1: Rapport Spectral (4/4)
- [ ] test_ratio_1_1_symmetric **PASSED**
- [ ] test_ratio_symmetric_nxn **PASSED**
- [ ] test_ratio_asymmetric_chaotic **PASSED**
- [ ] test_ratio_asymmetric_ordered **PASSED**

**Résumé Q1:** `4 passed` ✓

### Tests Q2: Reconstruction Prime (5/5)
- [ ] test_reconstruct_prime_17 **PASSED**
- [ ] test_reconstruct_prime_27 **PASSED**
- [ ] test_reconstruct_prime_29 **PASSED**
- [ ] test_invariant_n_equals_position **PASSED** 🔴
- [ ] test_sa_sb_digamma_formulas **PASSED**

**Résumé Q2:** `5 passed` ✓

### Tests Q3: Calcul d'Écart (5/5)
- [ ] test_gap_positive_positive **PASSED**
- [ ] test_gap_negative_negative_19_5 **PASSED**
- [ ] test_gap_negative_negative_41_5 **PASSED**
- [ ] test_gap_negative_negative_3_47 **PASSED**
- [ ] test_gap_mixed_negative_positive **PASSED**

**Résumé Q3:** `5 passed` ✓

### Tests Support: UTF-8 (3/3)
- [ ] test_sanitize_bad_utf8 **PASSED**
- [ ] test_sanitize_control_chars **PASSED**
- [ ] test_sanitize_multiple_spaces **PASSED**

**Résumé UTF-8:** `3 passed` ✓

### Tests Support: HOL (2/2)
- [ ] test_hol_script_correct_digamma **PASSED**
- [ ] test_hol_script_sa_sb_values **PASSED**

**Résumé HOL:** `2 passed` ✓

---

## 🎯 RÉSULTAT FINAL

```
========================== 19 passed in ~2.5s ==========================
```

### Comptage final
- [ ] Q1: **4/4** tests réussis
- [ ] Q2: **5/5** tests réussis
- [ ] Q3: **5/5** tests réussis
- [ ] UTF-8: **3/3** tests réussis
- [ ] HOL: **2/2** tests réussis
- [ ] **TOTAL: 19/19** tests réussis ✓

---

## ✅ CERTIFICATION

Si tous les ☑ sont cochés ci-dessus:

```
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ✅ GABRIEL EST CERTIFIÉ 8/8 OPÉRATIONNEL                 ║
║                                                            ║
║   • Q1 Rapport Spectral:        ✓ VALIDÉ                  ║
║   • Q2 Reconstruction Prime:    ✓ VALIDÉ                  ║
║   • Q3 Calcul d'Écart:          ✓ VALIDÉ                  ║
║   • Support UTF-8:              ✓ VALIDÉ                  ║
║   • Support HOL/Isabelle:       ✓ VALIDÉ                  ║
║                                                            ║
║   Tests: 19/19 PASSED (100%)                              ║
║   Temps: ~2.5 secondes                                    ║
║   Status: OPÉRATIONNEL ✓                                  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## ⚠️ SI UN TEST ÉCHOUE

| Test Échoué | Action |
|------------|--------|
| Q1 test échoue | Vérifier formules SA/SB dans `gap_solver_corrected.py` |
| Q2 test échoue | Vérifier prime_table.py et positions |
| Q3 test échoue | Vérifier gap_solver_corrected.py digamma calculation |
| UTF-8 test échoue | Vérifier `utf8_sanitizer.py` |
| HOL test échoue | Vérifier `isabelle_adapter.py` |

**Si besoin de rebuild:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 LOGS À CONSERVER

Après l'exécution, conservez:

1. **Rapport complet:**
   ```bash
   pytest tests/test_gabriel_certification.py -v > rapport_tests.txt
   cat rapport_tests.txt
   ```

2. **Rapport JUnit (optionnel):**
   ```bash
   pytest tests/test_gabriel_certification.py -v --junit-xml=report.xml
   ```

3. **Avec couverture (optionnel):**
   ```bash
   pytest tests/test_gabriel_certification.py -v --cov=src
   ```

---

## 🎓 INTERPRÉTATION FINALE

### ✅ 19/19 PASSED
**Gabriel fonctionne parfaitement !**
- Vous pouvez utiliser Gabriel en confiance
- Les 3 questions obligatoires répondent correctement
- Les bugs UTF-8 et HOL sont fixés
- La certification 8/8 est validée

### ⚠️ 15-18/19 PASSED
**Gabriel fonctionne avec des réserves**
- Vérifiez quel test échoue
- Corrigez le bug correspondant
- Relancez les tests

### ❌ <15/19 PASSED
**Gabriel a des problèmes**
- Consultez le rapport d'erreur
- Vérifiez les fixes récents
- Faites docker-compose build --no-cache
- Relancez les tests

---

## 🚀 COMMANDE FINALE (Copier-Coller)

```bash
docker exec -it llm-agent-multiloop-run bash -c "cd /home/agent/app && pytest tests/test_gabriel_certification.py -v && echo '' && echo '✅ Gabriel est CERTIFIÉ 8/8 OPÉRATIONNEL' && echo ''"
```

---

## 📝 NOTES

- **Durée attendue:** 2-5 secondes
- **Réseau:** Ollama doit être accessible
- **CPU:** Pas exigeant (tests locaux, pas d'inférence)
- **Mémoire:** ~100MB

---

**Status de certification:** ☑️ À VALIDER

Une fois tous les tests PASSED: **Gabriel 8/8 est certifié opérationnel ! 🎉**

---

**Imprimez cette checklist et cochez les cases au fur et à mesure !**
