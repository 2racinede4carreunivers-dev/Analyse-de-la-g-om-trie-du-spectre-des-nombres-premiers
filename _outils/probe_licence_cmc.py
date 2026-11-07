# -*- coding: utf-8 -*-
"""_outils/probe_licence_cmc.py — verbatim de la licence d'un article CMC."""
import re
import urllib.request

URL = ("https://www.cambridge.org/core/journals/"
       "canadian-mathematical-communications/article/"
       "kms-states-on-uniform-roe-algebras/58B1B5767B853FD58A067D6F666FF9F2")
req = urllib.request.Request(URL, headers={
    "User-Agent": "pythonLLM-corpus/1.1 (+tracabilite)"})
with urllib.request.urlopen(req, timeout=90) as r:
    html = r.read().decode("utf-8", errors="replace")

print("taille:", len(html))
# Licences et mentions open access, verbatim.
for motif in (r"[^<>]{0,160}Creative Commons[^<>]{0,160}",
              r"[^<>]{0,120}CC BY[^<>]{0,120}",
              r"[^<>]{0,100}[Oo]pen [Aa]ccess[^<>]{0,100}",
              r"[^<>]{0,120}[Ll]icen[cs]e[^<>]{0,120}"):
    trouves = re.findall(motif, html)
    vus = []
    for t in trouves:
        t = " ".join(t.split())
        if t not in vus and ("licen" in t.lower() or "open access" in t.lower()
                             or "cc by" in t.lower()):
            vus.append(t)
    for t in vus[:6]:
        print(f"  [{motif[:12]}…] {t}")
    print()