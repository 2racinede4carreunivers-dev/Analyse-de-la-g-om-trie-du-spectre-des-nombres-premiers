ANALYSE DU PIPELINE LLM COMPUTATIONNEL (pythonLLM)

1. VUE D'ENSEMBLE
Le pipeline pythonLLM traduit une requete en langage naturel en commande cline typee, validee et tracee, ou refuse formellement.
Aucun tirage aleatoire, aucune similarite approximative : appartenance ensembliste exacte, scores Fraction, regles ordonnees, validation grammaticale + deontique, trace SHA-256.

2. ENCHAINEMENT (pipeline.py)
normalisation -> reconnaissance -> scoring exact -> classification intention -> construction AST -> validation -> emission.
Refus formel a chaque etape en cas d'echec (reconnaissance, intention, construction, validation).

3. NORMALISATION (normalisation.py)
NFD + suppression accents + minuscule + decoupage [0-9a-z]+. Ex: L'Arbre de Cayley ! -> (l, arbre, de, cayley). Fonction pure deterministe.

4. RECONNAISSANCE (reconnaissance.py)
Appartenance ensembliste exacte contre banque.lemmes. Tri deterministe par poids de champ puis lemme.

5. SCORING (scoring.py)
Score champ = Fraction(nb reconnus / total champ). Zero erreur arrondi. Ordre total pour departage.

6. INTENTION (intention.py)
Regles evaluees par priorite croissante. Premiere condition satisfaite gagne. Regle par defaut -> analyse_generale.

7. CONSTRUCTION (construction.py)
Gabarits par intention -> AST CommandeCline. Requete normalisee rejointe = prompt. Pas de concat text.

8. VALIDATION (validation.py)
Grammaire (option, arite, domaine, doublon) + deontique (exclusions, obligations). Tuple violations.

9. TRACE (trace.py)
SHA-256(empreinte_precedente + donnee). Genese = 0*64. Chaine inalterable.

10. EMISSION (emission.py)
commande_cline.ps1, commande_cline.sh, rapport_derivation.md. Citations surees par shell.

11. BANQUE/CORPUS (banque.py)
SQLite read-only charge en memoire. 6 champs: LOGIQUE, ALGEBRE, ARITHMETIQUE, GEOMETRIE, STATISTIQUES, COMPILATION.

12. MODELE (entites.py)
dataclass(frozen=True). Scores Fraction. CommandeCline.argv() type.

13. WRAPPER (pythonLLM_computationnel.py)
CLI: python pythonLLM_computationnel.py "requete" ; --executer ; --construire-db ; --cwd ; --sorties. Retour 0/2.

14. INVARIANTS
INV-EXACTITUDE, INV-CURRY-HOWARD, INV-DEONTIQUE. Determinisme, tracabilite, refus formel.

15. TESTS
30 tests. python -m pytest test_pythonLLM_computationnel.py -q. Stdlib uniquement.

FIN
