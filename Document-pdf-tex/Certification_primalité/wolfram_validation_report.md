# Rapport — Validation de primalité des ancres via Wolfram|Alpha

## 1. Objet de la tâche
Valider, à l'aide de l'API **Wolfram|Alpha**, la primalité des **ancres** du fichier
`reconstruction_k28M_84M_detail.txt` du dépôt
`C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers`.

> Note : le fichier contient **6 045 662 ancres uniques** (pas 4 M ; les 4 M figurent
> dans le fichier `reconstruction_4M.txt` du même dépôt).

## 2. Clé API Wolfram — récupération et vérification
- Fichier `.env` : `...\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\.env`
- Variable : `WOLFRAM_APP_ID=8PHEQAPGK2` (la valeur brute contenait un espace après `=` ;
  il a été retiré).
- Test d'ouverture de l'API (appels `is <n> prime`) :
  - `17` → « 17 is a prime number » ✅
  - `15` → « 15 is not a prime number » ✅
  - `999983` → « 999983 is a prime number » ✅
  - nombre de 39 chiffres → réponse correcte ✅

## 3. Fichier source
- `C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\reconstruction_k28M_84M_detail.txt`
- Taille : ~1,007 Go | 6 441 797 lignes
- Structure d'une ligne de donnée :
  `RINDICE | Ancre n=10 | P(n) | Statut | Branches`
- Nombre d'ancres extraites : **6 045 662** (toutes uniques).
- Ancre = deuxième colonne, seulement quand elle est un nombre (les ancres `AMBIGU`
  sont rejetées car marquées par un tiret `-`).

## 4. Solution mise en œuvre
Script : `...\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\wolfram_primality_validation.py`

Fonctionnalités :
- Lecture du `.env` pour obtenir `WOLFRAM_APP_ID` (et vérification qu'il n'est pas un
  placeholder).
- Utilisation du client Wolfram du dépôt (`src/adapters/wolfram/wolfram_client.py`).
- Appels `is <ANCORE> prime` par flux streaming (pas de chargement en mémoire du fichier).
- Concurrence asynchrone (`asyncio.Semaphore`), retry avec backoff, timeout 30 s.
- Résultats écrits **incrémentalement** dans un fichier JSONL.

Usage :
```bat
python wolfram_primality_validation.py ^
  --input "C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\reconstruction_k28M_84M_detail.txt" ^
  --output "C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers\reconstruction_k28M_84M_detail_wolfram_primalite.jsonl" ^
  --concurrency 8 --batch-size 500 --log-every 100
```

Champs du JSONL :
```json
{"ridx":"1/28003083","ancre":"17219845008982963979683894918974781049","statut_fiche":"UNIQUE","resultat":"PREMIER","raw":"17219845008982963979683894918974781049 is a prime number"}
```
- `resultat` : `PREMIER` / `COMPOSITE` / `PREMIER_PROBABLE` / `INCONNU` / `ERREUR`.

## 5. Résultats partiels (échantillon démarrage du travail)
- Fichier de travail : `C:\tmp\wolfram_sample.jsonl`
- Ancres traitées depuis le lancement : **2 494** environ
- Résultats : **2 494 PREMIER** (0 COMPOSITE, 0 INCONNU, 0 ERREUR)
- Taille des ancres traitées : 38 chiffres
- Rythme observé : ~7 ancres/s

## 6. Statut du travail complet (en arrière-plan)
Un processus Python est lancé en arrière-plan et traite la totalité des 6 045 662
ancres du fichier source, en écrivant dans le fichier JSONL décrit ci-dessus.

- Démarrage : 2026-10-31 06:47:58 (heure locale)
- Ancres traitées depuis le lancement : ~2 000
- Point critique : **le nombre total d'appels Wolfram est immense**. À ~7 ancres/s,
  la validation complète des 6 045 662 ancres durerait **~23-24 jours de calcul
  continu** (limitée par le débit de l'API Wolfram|Alpha, pas par la mémoire).

Il est donc impossible de terminer ce traitement en une session. Le script et le
processus en arrière-plan constituent la solution : le travail avance
incrémentalement et peut être relancé à tout moment (l'upgrade du fichier de sortie
n'écrase pas ; il faut un nouveau fichier de sortie ou réorganiser).

## 7. Cache / sortie définitive
- Fichier JSONL de résultat (incrémental) :
  `reconstruction_k28M_84M_detail_wolfram_primalite.jsonl` (généré par le script).
- Pour une démonstration propre et bornée, lancer un second processus avec un petit
  `--batch-size` et un `--output` dédié.

## 8. Recommandations
1. Laire le résultat final à partir du JSONL (comptage `PREMIER`/`COMPOSITE`, etc.).
2. Si le débit de l'API est un goulot, augmenter `--concurrency` et/ou modifier le
   fichier de sortie fréquemment.
3. Le fichier `reconstruction_4M.txt` (4 000 001 ancres) peut être traité de la même
   manière avec l'option `--input` adéquate.
