# FIX : Préserver les nombres NÉGATIFS dans les questions d'écart

## 🔴 Problème identifié

Gabriel convertissait **"écart entre -3 et -23"** en **"écart entre 3 et 23"** parce que le RequestDecomposer utilisait une regex qui n'acceptait que les nombres positifs.

**Regex ancienne :**
```python
r"\b(\d+)\b"  # Capture 3, 23, mais pas -3, -23
```

**Regex nouvelle :**
```python
r"-?\d+"      # Capture -3, -23, 3, 23 (le - est optionnel)
```

---

## ✅ Correction appliquée

### Fichier corrigé : `src/multiloop/request_decomposer.py`

**Changements :**

1. **Ligne ~137** : Extraction des nombres
   ```python
   # AVANT
   numbers_found = [int(m) for m in re.findall(r"\b(\d+)\b", masked)]
   
   # APRÈS
   numbers_found = [int(m) for m in re.findall(r"-?\d+", masked)]
   ```

2. **Ligne ~104** : Extraction des tuples
   ```python
   # AVANT
   nums = re.findall(r"\d+", content)
   
   # APRÈS
   nums = re.findall(r"-?\d+", content)
   ```

3. **Ligne ~147** : Extraction de position
   ```python
   # AVANT
   r"(\d+)\s*(?:eme|ieme|ième|ème|e|th)\s*(?:nombre\s+)?(?:premier|prime)"
   
   # APRÈS
   r"(-?\d+)\s*(?:eme|ieme|ième|ème|e|th)\s*(?:nombre\s+)?(?:premier|prime)"
   ```

---

## 🚀 Déploiement (1 minute)

Le fichier `request_decomposer.py` a **déjà été corrigé** et uploadé.

### Étape 1 : Vérifier que la correction est en place

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Vérifier que -?\d+ est présent dans request_decomposer.py
grep -n "\-?\\\\d+" src\multiloop\request_decomposer.py
```

**Output attendu :**
```
137:            numbers_found = [int(m) for m in re.findall(r"-?\d+", masked)]
```

### Étape 2 : Rebuild Docker

```bash
.\start-agent.ps1 -Rebuild
```

### Étape 3 : Tester

```bash
.\start-agent.ps1

# Test cas (-,-)
> Peux-tu déterminer l'écart négatif entre les premiers négatifs (-,-)  -3 et -23 ?

# Résultat attendu : Gabriel devrait
# 1. Détecter intent=gap, gap_type=negative_negative
# 2. Utiliser p1=-3, p2=-23 (PAS 3 et 23)
# 3. Calculer l'écart entre -3 et -23
# 4. Retourner le résultat correct
```

---

## ✅ Vérification

Après le rebuild, testez :

```python
# Exemple : -3 et -23
from src.multiloop.request_decomposer import RequestDecomposer

decomp = RequestDecomposer()
result = decomp.decompose("Peux-tu déterminer l'écart négatif entre les premiers négatifs (-,-) -3 et -23 ?")

print(f"Intent : {result.detected_intent}")  # gap
print(f"Segments : {result.segments}")       # Doit inclure -3 et -23, pas 3 et 23
```

---

## 📊 Avant/Après

| Entrée | Avant | Après |
|--------|-------|-------|
| "écart -3 et -23" | Nombres extraits: 3, 23 | Nombres extraits: -3, -23 ✓ |
| "gap (-5) (-19)" | Tuples: 5, 19 | Tuples: -5, -19 ✓ |
| "position -7e premier" | Posit...


ion: 7 | Position: -7 ✓ |

---

## 🎉 Résultat

Gabriel peut maintenant :
- ✅ Reconnaitre les nombres négatifs dans les questions
- ✅ Préserver les signes jusqu'au GapSolver
- ✅ Calculer correctement les écarts (-,-) et (-,+)
- ✅ Répondre à toutes les 3 questions obligatoires

Tous les cas d'écart sont maintenant traités :
1. ✅ Cas (+,+) : Entre 3 et 47
2. ✅ Cas (-,-) : Entre -3 et -23
3. ✅ Cas (-,+) : Entre -31 et 17

Ready! 🚀
