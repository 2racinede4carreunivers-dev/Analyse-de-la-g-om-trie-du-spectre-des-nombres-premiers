import re, pathlib
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
t = (base/"methode_spectral.thy").read_text(encoding="utf-8", errors="replace")
lines = t.splitlines()
# section boundaries
bounds=[]
for i,l in enumerate(lines, start=1):
    if l.strip().startswith("section "):
        m=re.search(r'section\s+"(.*)"',l)
        bounds.append((i, m.group(1) if m else l.strip()[:120]))
bounds.append((len(lines)+1,"END"))
print(f"{len(bounds)-1} sections de niveau 'section'")
for k in range(len(bounds)-1):
    l0,l1=bounds[k][0],bounds[k+1][0]-1
    chunk="\n".join(lines[l0-1:l1])
    n_eval=len(re.findall(r'\bby\s+eval\b',chunk))
    n_sorry=len(re.findall(r'\bsorry\b',chunk))
    n_axiom=len(re.findall(r'axiomatization',chunk))
    n_lem=len(re.findall(r'^(?:lemma|theorem)\b',chunk,flags=re.M))
    n_def=len(re.findall(r'^definition\b',chunk,flags=re.M))
    print(f"{k+1:02d} L{l0:5d}-L{l1:5d} ({l1-l0+1:4d}l) eval={n_eval:3d} sorry={n_sorry} ax={n_axiom} lem/thm={n_lem:3d} def={n_def:3d} | {bounds[k][1][:110]}")
print()
# occurrences mots cles redondance
for kw in ["Rapport spectral 1/2","Rapport spectral 1/3","Rapport spectral 1/4","ecart","digamma","convolutif","Pont Savard","preuve par","absurde","prime_i","spectral_family","non-typique","non_typique","mixtes","negatif","asymetrie"]:
    c=len(re.findall(kw,t,flags=re.I))
    print(f"  '{kw}': {c}")
