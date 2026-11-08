import pathlib, re
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
AUTEUR = "Philippe Thomas Savard"
DATE_LETTRES = "Le trois octobre deux mille vingt-six"
LIEU = "Levis, Chausdiere-Appalaches, Canada"

def toc_sections(fn):
    lines = (base/fn).read_text(encoding="utf-8", errors="replace").splitlines()
    secs=[]
    for i,l in enumerate(lines, start=1):
        s=l.strip()
        if s.startswith("section ") or s.startswith("subsection "):
            m=re.search(r'"(.*)"',s)
            lab=m.group(1) if m else s[:110]
            kind="section" if s.startswith("section") else "subsection"
            secs.append((i,kind,lab))
    # fin = ligne avant section suivante - 1, derniere = fin fichier (avant 'end')
    n=len(lines)
    out=[]
    for k,(ln,kind,lab) in enumerate(secs):
        nxt = secs[k+1][0]-1 if k+1<len(secs) else n
        out.append((ln,nxt,kind,lab))
    return lines, out

# ---- CV 1/2 ----
fn1="validation_hol_unifiee.thy"
lines1, secs1 = toc_sections(fn1)
toc1="\n".join([f"   L{a:4d} - L{b:4d} : [{kind}] {lab}" for a,b,kind,lab in secs1])
head1=f"""(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Contre-validation HOL 1/2
   Fichier : validation_hol_unifiee.thy (fichier unique, non decoupe)
   Auteur : {AUTEUR}
   Date : {DATE_LETTRES}
   Lieu : {LIEU}
   Role : contre-validation independante de la validation principale
   (MS_01 a MS_14), approche formelle rigoureuse dans Isabelle/HOL.
   ----------------------------------------------------------------------------
   TABLE DES MATIERES (sections + N° de ligne debut-fin, origine v7.5) :
{toc1}
   ============================================================================ *)
"""
t1=(base/fn1).read_text(encoding="utf-8", errors="replace")
# remplace l'ancien commentaire d'en-tete (lignes 1-31) + change imports methode_spectral -> MS_14
t1_new = re.sub(r'\(\* =+\n.*?=+ \*\)\s*\n\s*theory validation_hol_unifiee',
                head1.strip()+"\n\ntheory validation_hol_unifiee",
                t1, count=1, flags=re.S)
t1_new = t1_new.replace("imports methode_spectral", "imports MS_14_Systeme_Convolutif")
(base/fn1).write_text(t1_new, encoding="utf-8")
print("CV1 OK", len(secs1), "entrees TOC")

# ---- CV 2/2 ----
fn2="validation_zeta_lean.thy"
lines2, secs2 = toc_sections(fn2)
toc2="\n".join([f"   L{a:4d} - L{b:4d} : [{kind}] {lab}" for a,b,kind,lab in secs2])
head2=f"""(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Contre-validation HOL 2/2 (inter-assistants Lean 4 / Mathlib)
   Fichier : validation_zeta_lean.thy (fichier unique, non decoupe)
   Auteur : {AUTEUR}
   Date : {DATE_LETTRES}
   Lieu : {LIEU}
   Role : chaque point de la Section XIII (Pont Savard, MS_13) est mis en
   relation avec sa contrepartie PROUVEE dans Mathlib (Lean 4) : zeta,
   Lambda completee, equation fonctionnelle, zeros, psi de Tchebychev (C1).
   Discipline : AUCUN axiome n'enonce RH ; les axiomes specifient des
   theoremes Mathlib ; RH = definition booleenne ; pont = theoreme
   conditionnel + direction constructive inconditionnelle.
   ----------------------------------------------------------------------------
   TABLE DES MATIERES (sections + N° de ligne debut-fin) :
{toc2}
   ============================================================================ *)
"""
t2=(base/fn2).read_text(encoding="utf-8", errors="replace")
t2_new = re.sub(r'theory validation_zeta_lean\s*\n\s*imports methode_spectral\s*\nbegin\s*\n\s*\(\* =+\n.*?=+ \*\)',
                head2.strip()+f"\n\ntheory validation_zeta_lean\n  imports MS_14_Systeme_Convolutif\nbegin",
                t2, count=1, flags=re.S)
if t2_new == t2:  # repli si le motif ne colle pas : insertion simple
    t2_new = t2.replace("theory validation_zeta_lean",
                        head2.strip()+"\n\ntheory validation_zeta_lean", 1)
    t2_new = t2_new.replace("imports methode_spectral", "imports MS_14_Systeme_Convolutif")
else:
    pass
(base/fn2).write_text(t2_new, encoding="utf-8")
print("CV2 OK", len(secs2), "entrees TOC")
