import csv
from collections import Counter
from pathlib import Path
CSV=Path(r"c:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\_ancres_uniques.csv")
c=Counter(); br=Counter(); n=0
with CSV.open(encoding="utf-8") as fh:
    for row in csv.reader(fh):
        n+=1; c[len(row)]+=1
        if len(row)>3: c[row[3]]+=1
        br[row[1]]+=1
print("lignes:",n,"| longueur des lignes:",dict(c))
print("branches:",dict(br))
