import pathlib, re
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
src = (base/"methode_spectral.thy").read_text(encoding="utf-8", errors="replace")
lines = src.splitlines()

splits = [
 ("MS_01_Fondements", "Fondements / Meta-theory", 118, 351),
 ("MS_02_Suites_AB_RsP_1_2", "Suites A et B + Rapport 1-2 + n x n", 352, 491),
 ("MS_03_Digamma_Equation_Generale", "Digamma + Axiomatisation positive + Exemples 29 31 37 41 + Equation generale", 492, 676),
 ("MS_04_Generalisation_Prime_i", "Generalisation i-eme nombre premier (prime_i)", 677, 761),
 ("MS_05_Modeles_1_3_1_4", "Modeles 1-4 et 1-3 + Validations generalisees", 762, 1039),
 ("MS_06_Mixtes_Negatives_Asymetries", "Suites mixtes + Reconstruction + Negatives + Asymetries", 1040, 1204),
 ("MS_07_Comparaison_Blocs", "Comparaison asymetrique + Blocs A_k B_k", 1205, 1658),
 ("MS_08_Ecarts_Negatifs", "Rapports negatifs 1-3 1-4 + Ecarts negatifs (-19 / -5)", 1659, 1978),
 ("MS_09_Preuve_Absurde", "Preuve par l'absurde — exclusion des composes (INTEGRAL)", 1979, 2307),
 ("MS_10_Ecarts_Mixtes_Positifs", "Ecarts mixtes (-31 / 17) + Ecarts 1-3 (227 / 173) + Ecarts 1-4 (947 / 881)", 2308, 2630),
 ("MS_11_Construction_SpectralFamily", "Regles construction A_i B_i (XI) + spectral_family (XI.bis) (INTEGRAL)", 2631, 3224),
 ("MS_12_Construction_Generalisee_1k", "Construction generalisee 1-k_i (XII)", 3225, 3492),
 ("MS_13_Pont_Savard", "Pont Savard : psi Tchebychev, zeta, Re = 1-2 + Synthese-index (INTEGRAL)", 3493, 4232),
 ("MS_14_Systeme_Convolutif", "Systeme convolutif 1-k (XIV) + References + Licence (COEUR)", 4233, 5014),
]
AUTEUR = "Philippe Thomas Savard"
DATE_LETTRES = "Le trois octobre deux mille vingt-six"
LIEU = "Levis Chausdiere-Appalaches Canada"
# NOTE: keep ascii in headers to avoid encoding issues in Isabelle; accents in text blocks below are utf-8 safe
TOC_GLOB = "\n".join([f"   {i+1:2d}/14 : {th}  — {titre}  (lignes origine {a}-{b})" for i,(th,titre,a,b) in enumerate(splits)])

created=[]
for idx,(th,titre,a,b) in enumerate(splits, start=1):
    chunk = "\n".join(lines[a-1:b])
    if idx==1:
        imp = '  imports Complex_Main "HOL-Computational_Algebra.Primes"'
    else:
        imp = f'  imports {splits[idx-2][0]}'
    header = f"""(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Pipeline HOL / Validation principale methode_spectral.thy — section {idx}/14
   Fichier : {th}.thy  (section : {titre})
   Origine : methode_spectral.thy lignes {a}-{b} (verbatim phase 1, sans perte)
   Auteur : {AUTEUR}
   Date : {DATE_LETTRES}
   Lieu : {LIEU}
   Titre ouvrage : L'univers est au carre !
   Chapitre : La geometrie du spectre des nombres premiers
   ----------------------------------------------------------------------------
   TABLE DES MATIERES GLOBALE (14 fichiers de validation principale) :
{TOC_GLOB}
   ----------------------------------------------------------------------------
   STATUT : F09 preuve par l'absurde / F11 reconstruction + spectral_family /
   F13 Pont Savard / F14 convolutif = A CONSERVER INTEGRAUX.
   F05 rapports 1-2/1-3/1-4 + F08/F10 ecarts numeriques = CANDIDATS
   suppression / generalisation phase 2 (voir pipeline_correction_HOL/DEVIS_NETTOYAGE_HOL.md).
   Memoire : le decoupage ne reduit pas le pic (1 session = 1 tas partage).
   ============================================================================ *)
theory {th}
{imp}
begin
"""
    # local TOC: list subsections inside chunk
    subsecs = []
    for i,l in enumerate(lines[a-1:b], start=a):
        s=l.strip()
        if s.startswith("section ") or s.startswith("subsection "):
            m=re.search(r'"(.*)"',s)
            lab = m.group(1) if m else s[:100]
            subsecs.append(f"   L{i} : {lab}")
    local_toc = "(* TOC locale (origine) :\n" + ("\n".join(subsecs) if subsecs else "   (aucune sous-section)") + "\n*)"
    content = header + "\n" + local_toc + "\n\n" + chunk + "\n\nend\n"
    (base/(th+".thy")).write_text(content, encoding="utf-8")
    created.append((th,a,b,len(chunk.splitlines())))
print("CREES:", len(created))
for th,a,b,n in created:
    print(f"  {th}.thy  origine L{a}-L{b}  ({n} lignes)")
