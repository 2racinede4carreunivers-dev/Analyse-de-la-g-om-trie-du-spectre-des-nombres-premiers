import pathlib, re
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
names = ["Fondements","Suites_AB_RsP_1_2","Digamma_Equation_Generale","Generalisation_Prime_i",
"Modeles_1_3_1_4","Mixtes_Negatives_Asymetries","Comparaison_Blocs","Ecarts_Negatifs",
"Preuve_Absurde","Ecarts_Mixtes_Positifs","Construction_SpectralFamily",
"Construction_Generalisee_1k","Pont_Savard","Systeme_Convolutif"]
files = [f"MS_{i+1:02d}_{n}.thy" for i,n in enumerate(names)] + ["validation_hol_unifiee.thy","validation_zeta_lean.thy","README.thy"]
for fn in files:
    t=(base/fn).read_text(encoding="utf-8",errors="replace")
    opens=t.count("\\<open>"); closes=t.count("\\<close>")
    copen=t.count("(*"); cclose=t.count("*)")
    ths=re.findall(r"^theory\s+(\S+)",t,flags=re.M)
    imps=re.findall(r"^\s*imports\s+(.+)$",t,flags=re.M)
    nbegin=len(re.findall(r"^begin\b",t,flags=re.M)); nend=len(re.findall(r"^end\b",t,flags=re.M))
    nproof=len(re.findall(r"\bproof\b",t)); nqed=len(re.findall(r"\bqed\b",t))
    ok = (opens==closes and copen==cclose and nbegin==nend)
    print(fn, "| theory=",ths, "| imports=",imps, "| begin/end=",nbegin,nend,
          "| open/close=",opens,closes, "| comment=",copen,cclose,
          "| proof/qed=",nproof,nqed, "| OK" if ok else "| <-- DESEQUILIBRE")
