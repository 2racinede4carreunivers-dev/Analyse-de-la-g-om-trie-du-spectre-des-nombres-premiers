# Validation prouvee des ancrages du rapport k28M-84M

Le script `valider_primalite_ancres.py` extrait chaque valeur des branches
`A(...)=...`, y compris les deux branches des lignes `AMBIGU`, puis la verifie
avec `isprime` de PARI/GP. Le pipeline n'utilise pas SymPy ni un test
probabiliste comme preuve.

## Prerequis

Installer PARI/GP depuis la [page de telechargement officielle](https://pari.math.u-bordeaux.fr/download.html)
et rendre la commande `gp` accessible dans `PATH`, ou passer le chemin de
l'executable avec `--gp-executable`. Le script effectue d'abord un controle
sur 17 et 21. Si PARI/GP est absent ou renvoie des resultats inattendus, le
traitement s'arrete sans substituer une validation moins forte.

## Execution

Depuis le dossier du projet :

```powershell
python .\valider_primalite_ancres.py
```

Par defaut, le pipeline lit `reconstruction_k28M_84M_detail.txt`, produit un
audit JSONL avec un verdict par ancrage, et cree une copie du rapport avec le
tableau de synthese au debut et a la fin. Le fichier source n'est jamais
remplace.

```powershell
python .\valider_primalite_ancres.py `
  --input .\reconstruction_k28M_84M_detail.txt `
  --audit .\reconstruction_k28M_84M_detail_primalite.jsonl `
  --report .\reconstruction_k28M_84M_detail_primalite.txt `
  --gp-executable "$env:LOCALAPPDATA\Programs\PARI-GP\gp64-2-19-0.exe" `
  --batch-size 10000
```

Le tableau distingue premiers demontres, composes, score de primalite et
couverture. `Validation integrale` reste `NON` si une ligne est mal formee,
meme si toutes les valeurs numeriques qui ont pu en etre extraites ont ete
verifiees. Le code de sortie est `0` pour un rapport integralement valide,
`2` pour un rapport traite mais structurellement incomplet, et `1` en cas
d'erreur ou d'impossibilite de prouver les resultats.

## Constat sur la copie actuelle

Le balayage du fichier actuel a trouve 6 441 794 lignes de rapports :
6 045 662 `UNIQUE` et 396 132 `AMBIGU`. Les branches contiennent 6 849 578
valeurs distinctes; une derniere ligne `UNIQUE` est tronquee mais contient
encore une ancre numerique, ce qui porte a 6 849 579 le nombre de candidats
numeriques a verifier dans cette copie. La ligne tronquee empeche de declarer
le rapport integralement valide tant que la source n'est pas complete.

Un benchmark deterministe de 1 200 ancrages echantillonnes dans tout le
rapport a pris 2,57 s en un seul lot (environ 468 validations/s). Les lots de
100 et 500 ont donne respectivement environ 281 et 416 validations/s; le
traitement complet est donc lance avec des lots de 10 000 pour reduire les
redemarrages du processus GP. L'extrapolation indicative est d'environ 4,1 h,
hors variations de charge et de disque.
