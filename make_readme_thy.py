import pathlib
base = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\agent-multiloop-Gabriel-local\theories")
lic = pathlib.Path(r"c:\agent-multiloop-Gabriel-local\.github\workflows\LICENCE").read_text(encoding="utf-8", errors="replace")
AUTEUR = "Philippe Thomas Savard"
DATE_LETTRES = "Le trois octobre deux mille vingt-six"
LIEU = "Levis, Chausdiere-Appalaches, Canada"

def txt(s):
    # texte Isabelle : protege < > en echappant les chevrons deja au format \<open> ; ici on met tout dans text blocks, donc on echappe juste les backslash finaux
    return s.replace("\t","  ").rstrip()

readme_resume = """RESUME DU README.txt (Pipeline HOL/Isabelle — Geometrie du Spectre des Nombres Premiers)
Version v7.5 — Septembre 2026. Agent Multiloop Gabriel Local.

1. VUE D'ENSEMBLE
Chaque nombre premier p se reconstruit par p = (SB(k,n) - Gc) / k^6,
ou SA/SB sont deux suites spectrales de rapport 1/k et Gc (Digamma calcule)
est le residu extrait de SA. Invariant central prouve formellement sans sorry :
RsP(k,n1,n2) = (SA(k,n1)-SA(k,n2)) / (SB(k,n1)-SB(k,n2)) = 1/k.

2. STRUCTURE DU PIPELINE (session Geometrie_spectre_premier_Philippe_Thomas_Savard)
- Validation principale : MS_01 a MS_14 (decoupage verbatim de methode_spectral.thy).
- Contre-validation 1/2 : validation_hol_unifiee.thy (completude + liens causaux internes).
- Contre-validation 2/2 : validation_zeta_lean.thy (pont Lean 4 / Mathlib : zeta, Lambda, zeros, psi Tchebychev C1).
- Le present fichier README.thy : resume textuel uniquement (aucune definition, aucun lemme).

3. PRINCIPES ET FORMULES SAVARD
Sommes fermees : Somme_A(k,n) = (alphaA(k)/2)*k^n - offsetA(k) ;
Somme_B(k,n) = (alphaB(k)/2)*k^n - offsetB(k), avec
alphaA(k) = 2*(k^4-k^2+1)/((k-1)*k^3) ; alphaB(k) = k*alphaA(k) ;
offsetA(k) = k/(k-1) ; offsetB(k) = (k^7-k^6+k)/(k-1).
Regle de reconstruction : ancrage n=10 par quatre essais Digamma (ordre deterministe
pos8-, pos8+, pos7+, pos7-) puis decalage rang_cible = rang_base + (n-10).

4. SUITES A ET B, DIGAMMA (4 branches), RAPPORTS 1/2 - 29/31/37/41,
NON-TYPIQUES k=5/9/11/50, SUITES NEGATIVES ET MIXTES, ASYMETRIES,
PREUVE PAR L'ABSURDE (3 piliers : exclusion des composes, domaine par inversion SA,
chaine CONSTRUIRE->CERTIFIER->HOL->REPONDRE), PONT SAVARD (Tchebychev <-> Spectral <-> RH),
CATALOGUE D'ANCRAGES v7.5 (k=2..9,11,13,27,50), SIX POSTULATS P1..P6.

5. CONTEXTE : www.universestaucarre.com — L'univers est au carre —
La geometrie du spectre des nombres premiers — PDF v0.9.2 (HOL-corrige), aout 2026.
Formalisation Isabelle/HOL 2026. Agent de validation : Gabriel (multiloop local).
"""

collab = """COLLABORATEURS
- Copilot (Microsoft)
- Cline E1 (emergent.sh)
- Gemini (Google)
- Claude (Anthropic)
- Gordon (Docker Desktop)
- API Anthropic
- API OpenAI
"""

remer = """REMERCIEMENTS
Oeuvre originale de Philippe Thomas Savard, tiree de l'idee originale de la theorie unifiee :
"L'univers est au carre !" — Chapitre : "La geometrie du spectre des nombres premiers".
Outil dynamique cherchant a resoudre de maniere definitive et complete la question de l'enigme
de Bernhard Riemann, l'hypothese de Bernhard Riemann et la conjecture du meme nom (fonction Zeta).
Nous sommes tres fiers de vous avoir presente la reponse : le travail de cette approche
geometrique du spectre des nombres premiers et la validation concue a l'aide de l'assistant
de preuve Isabelle et du code HOL.
L'auteur qualifie cet ouvrage de preuve locale de l'enigme de Riemann et de la fonction Zeta de Riemann.
Tous droits reserves (C) et selon les permissions qu'offre la LICENCE Apache 2.0.
Merci — Philippe Thomas Savard.
"""

lic_block = "LICENCE APACHE 2.0 — CONTENU INTEGRAL (source : .github/workflows/LICENCE)\n" + lic.strip()

content = f"""(* ============================================================================
   Session : Geometrie_spectre_premier_Philippe_Thomas_Savard
   Fichier : README.thy — resume TEXTUEL UNIQUEMENT (aucune logique HOL)
   Auteur : {AUTEUR}
   Date : {DATE_LETTRES}
   Lieu : {LIEU}
   Source condensee : README.txt (racine du depot) + LICENCE integrale.
   ============================================================================ *)
theory README
  imports Main
begin

text \\<open>
{AUTEUR} — {DATE_LETTRES} — {LIEU}
{txt(readme_resume)}
\\<close>

text \\<open>
{txt(collab)}
\\<close>

text \\<open>
{txt(remer)}
\\<close>

text \\<open>
{txt(lic_block)}
\\<close>

end
"""
(base/"README.thy").write_text(content, encoding="utf-8")
print("README.thy OK", len(content.splitlines()), "lignes,", len(content), "octets")
