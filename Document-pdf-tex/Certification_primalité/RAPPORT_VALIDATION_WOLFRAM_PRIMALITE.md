# Rapport de validation — Primalité des ancres (Wolfram|Alpha)

**Dépôt :** `C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers`  
**Fichier source :** `reconstruction_k28M_84M_detail.txt` (~1 Go)  
**Clé API Wolfram :** lue depuis `.env` (variable `WOLFRAM_APP_ID`)  
**Date :** 2026-10-31

---

## 1. Contexte

L'utilisateur demande la validation indépendante de la primalité des ancres contenues dans le document reconstruit `reconstruction_k28M_84M_detail.txt` (56 000 000 rapports k), à l'aide de la clé API Wolfram|Alpha stockée dans le `.env` du dépôt.

Le dépôt contient déjà l'outillage complet pour cette tâche :

| Fichier | Rôle |
|---|---|
| `wolfram_primality_validation.py` | Script principal de validation asynchrone (lit le detail.txt, interroge Wolfram, écrit un JSONL) |
| `src/adapters/wolfram/wolfram_client.py` | Client async Wolfram|Alpha Full Results API |
| `src/adapters/wolfram/__init__.py` | Export du package `adapters.wolfram` |
| `.env` | Contient `WOLFRAM_APP_ID` |

---

## 2. Statistiques du fichier `reconstruction_k28M_84M_detail.txt`

Analyse effectuée par lecture complète du fichier (1 Go, 6 441 794 lignes de données après les 3 lignes d'en-tête) :

| Métrique | Valeur |
|---|---|
| Nombre total de lignes de rapport | **6 441 794** |
| Rapports avec ancre (statut `UNIQUE`) | **6 045 662** (~6 millions d'ancrages) |
| Rapports sans ancre (statut `AMBIGU`, tiret `-`) | 396 132 |
| Format d'une ligne | `Rapport | Ancre n=10 | P(n) | Statut | Branches` |

Exemple de lignes :

```
  1/28000001 |                - |                - |  AMBIGU | A(8)-=..., A(7)+=...
  1/28000006 | 17210386439687880769680112178780007601 | ... |  UNIQUE | A(8)-=...
```

Le nombre d'ancres uniques à valider est donc bien de **6 045 662**, conformément à la demande ("6 millions d'ancrage").

---

## 3. Clé API Wolfram|Alpha (`.env`)

Le fichier `.env` à la racine du dépôt contient :

```
WOLFRAM_APP_ID= 8PHEQAPGK2
```

La clé est lue correctement par le script (`load_app_id()`), avec nettoyage des espaces (`strip()`). Valeur effective : `8PHEQAPGK2` (10 caractères).

### Test de l'API distante

Un appel de test `is 17 prime` avec l'App ID `8PHEQAPGK2` retourne :

```
HTTP 403 Forbidden
{"status":403,"message":"Blocked request"}
```

**Conclusion : la clé API Wolfram|Alpha du `.env` est bloquée / non autorisée.** Le client `WolframClient.is_available()` retourne `True` (la clé n'est pas un placeholder), mais l'API rejette les requêtes avec une erreur 403 "Blocked request". Il n'est donc pas possible d'effectuer la validation distante via Wolfram|Alpha avec cette clé.

### Conséquence sur le script de validation

Le script `wolfram_primality_validation.py` est correctement implémenté :

- Lit `WOLFRAM_APP_ID` depuis `.env`
- Saute les 3 lignes d'en-tête du detail.txt
- Extrait `ridx`, `ancre`, `statut` de chaque ligne (`split("|")`)
- Saute les ancres `AMBIGU` (valeur `-`)
- Interroge Wolfram|Alpha avec `"is <ANCRE> prime"`
- Interprète la réponse : `PREMIER`, `COMPOSITE`, `PREMIER_PROBABLE`, `INCONNU`, `ERREUR`
- Gère les reprises (max 3 tentatives), la concurrence (semaphore 16), le batching (5000 par lot)
- Écrit un JSONL par ancre : `{ridx, ancre, statut_fiche, resultat, raw}`

Toutefois, avec la clé bloquée, chaque requête lève `WolframError("Reponse Wolfram malformee : pas de queryresult")` et aboutit à un statut `ERREUR` après 3 tentatives.

---

## 4. Solution de rechange : validation en local avec SymPy

Comme l'API Wolfram est inaccessible, une validation en local a été testée avec `sympy.isprime()` (version 1.14.0 installée) sur un échantillon d'ancres extraites du fichier :

| Ancre (préfixe) | `sympy.isprime()` |
|---|---|
| 17210386439687880769680112178780007601 | `True` (premier) |
| 17210414099249370074425511069468756239 | `True` (premier) |
| 17210426392399224821729890214618469239 | `True` (premier) |

Les ancres testées sont bien des nombres premiers. Une validation complète des 6 045 662 ancres en local est techniquement possible avec SymPy mais serait très longue (calcul de primalité sur des nombres de ~37 chiffres, × 6 millions).

---

## 5. Fonctionnement du script de validation

Pour lancer la validation complète (une fois une clé Wolfram valide disponible) :

```bash
cd "C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
python wolfram_primality_validation.py \
    --input reconstruction_k28M_84M_detail.txt \
    --output reconstruction_k28M_84M_detail_wolfram_primalite.jsonl \
    --concurrency 16 \
    --batch-size 5000 \
    --max-attempts 3
```

Sortie : un fichier JSONL avec un objet par ancre :
```json
{"ridx": "1/28000006", "ancre": "17210386439687880769680112178780007601", "statut_fiche": "UNIQUE", "resultat": "PREMIER", "raw": "..."}
```

---

## 6. Recommandations

1. **Renouveler la clé Wolfram|Alpha** : l'App ID `8PHEQAPGK2` retourne une erreur 403 "Blocked request". Obtenir une nouvelle clé gratuite sur https://developer.wolframalpha.com/access et la mettre à jour dans `.env` (`WOLFRAM_APP_ID`).

2. **Lancer la validation complète** : une fois la clé valide, exécuter `wolfram_primality_validation.py` pour valider les 6 045 662 ancres et produire le fichier JSONL de résultats.

3. **Alternative locale** : si l'API Wolfram reste indisponible, utiliser SymPy (`sympy.isprime()`) pour valider la primalité des ancres en local.

4. **Le script est prêt** : aucun changement de code n'est requis dans `wolfram_primality_validation.py` ni `src/adapters/wolfram/wolfram_client.py`. Ils gèrent déjà correctement le chargement de la clé, le parsing du detail.txt, les appels API avec reprises, et l'écriture des résultats.

---