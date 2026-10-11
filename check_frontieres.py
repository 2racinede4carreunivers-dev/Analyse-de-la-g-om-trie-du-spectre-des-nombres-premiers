import pathlib, re
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
names = ["Fondements","Suites_AB_RsP_1_2","Digamma_Equation_Generale","Generalisation_Prime_i",
"Modeles_1_3_1_4","Mixtes_Negatives_Asymetries","Comparaison_Blocs","Ecarts_Negatifs",
"Preuve_Absurde","Ecarts_Mixtes_Positifs","Construction_SpectralFamily",
"Construction_Generalisee_1k","Pont_Savard","Systeme_Convolutif"]
files = [f"MS_{i+1:02d}_{n}.thy" for i,n in enumerate(names)]
KWS = ["locale","interpretation","context","proof","qed","axiomatization"]
for fn in files:
    ls=(base/fn).read_text(encoding="utf-8",errors="replace").splitlines()
    # ne regarder que le corps verbatim (apres TOC locale, avant 'end' final)
    print("="*30, fn)
    for i,l in enumerate(ls, start=1):
        s=l.strip()
        for k in KWS:
            if s.startswith(k+" ") or s==k or s.startswith(k+":") or (k in ("proof","qed") and s.startswith(k)):
                print(f"  L{i}: {s[:110]}")
                break
