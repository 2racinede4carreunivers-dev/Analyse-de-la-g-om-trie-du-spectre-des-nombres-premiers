# pythonLLM — pipeline computationnaliste de commandes Cline CLI

Remplace la **statistique floue** (connexionnisme probabiliste, propice aux
illusions et hallucinations) par la **rigueur du code et de la logique
formelle**. Vous écrivez une demande en langage naturel ; le pipeline la
traduit en une commande `cline` **typée, validée et tracée**, ou **refuse
formellement** plutôt que d'inventer.

> Principe : aucun tirage aléatoire, aucune similarité approximative, aucun
> complément probabiliste. Uniquement de l'appartenance ensembliste exacte,
> des scores en `fractions.Fraction` (zéro erreur d'arrondi), des règles
> ordonnées à ordre total, et une validation grammaticale + déontique.

## Analogie pythontex

Comme `pythontex` produit un `.tex` à partir d'un document et d'une banque de
données encodée, `pythonLLM` produit une **commande shell** à partir d'une
requête empirique et d'une base SQLite de corpus normatif. Si la requête est
floue par nature, sa traduction est rigoureuse parce qu'elle s'appuie sur des
faits formels encodés, pas sur une génération probabiliste.

## Architecture

```
requete langage naturel
  → normalisation (NFKC, sans accents, tokens)
  → reconnaissance contre la .db SQLite (appartenance ensembliste exacte)
  → scoring exact par champ (fractions.Fraction)
  → classification d'intention (règles ordonnées, ordre total)
  → sélection du gabarit → AST CommandeCline (pas de concaténation de texte)
  → validation grammaticale (arité/types/énums) + logique déontique (exclusions)
  → réparation déterministe, ou REFUS FORMEL justifié (pas d'invention)
  → trace de dérivation chaînée par SHA-256
  → émission .ps1 / .sh / .md
```

## Arborescence

| Fichier | Rôle |
|---|---|
| `modele/entites.py` | Dataclasses figées (immuables) du domaine |
| `corpus/corpus_computationnel.py` | Corpus : 6 champs, invariants, règles |
| `corpus/institutions.py` | 9 institutions traçées (licence + accès + URL) |
| `corpus/notions.py` | Lexique manuel (101 termes) |
| `corpus/extraire_mathlib.py` | Extraction déterministe Mathlib (provenance fichier:ligne) |
| `corpus/construire_db.py` | Construit la base SQLite (`corpus_computationnel.db`) |
| `moteur/normalisation.py` | NFKC + suppression d'accents + tokens |
| `moteur/grammaire.py` | Grammaire formelle du CLI Cline (options typées) |
| `moteur/reconnaissance.py` | Appartenance ensembliste exacte |
| `moteur/scoring.py` | Scores exacts (`Fraction`) |
| `moteur/intention.py` | Classification par règles ordonnées |
| `moteur/construction.py` | Instanciation du gabarit → AST |
| `moteur/validation.py` | Validation grammaticale + déontique |
| `moteur/trace.py` | Traçage SHA-256 chaîné |
| `moteur/emission.py` | Émission `.ps1` / `.sh` / `.md` |
| `moteur/pipeline.py` | Orchestration tracée |

## Usage

```bash
# (Re)construire la base SQLite du corpus
python pythonLLM_computationnel.py --construire-db

# Requête en langage naturel → commande cline (émission seule)
python pythonLLM_computationnel.py "analyse ce graphe de dependances et sa connexite"
#   → cline --thinking high --auto-approve true --json "analyse ce graphe..."

# Exécution réelle si le binaire `cline` est installé
python pythonLLM_computationnel.py --executer "verifie la preuve Lean"

# Fixer le répertoire de travail transmis à cline (-c)
python pythonLLM_computationnel.py --cwd C:\mon\projet "calcule en arithmetique modulaire"
```

**Code de retour** : `0` si une commande valide est produite, `2` en cas de
refus formel (requête hors cadre du corpus).

## Enrichissement traçable des sources

À chaque `--construire-db`, la base est enrichie à partir de **sources réelles
et vérifiables**, jamais inventées (`schema 1.2.0`, SHA-256 des documents dans
`corpus/snapshots/SOURCES.sha256` et dans la table `meta`) :

| Source | Statut d'accès | Traitement |
|---|---|---|
| **Mathlib** (`~/OneDrive/Mathlib`, Apache 2.0) | direct (dépôt local) | ~23 600 notions extraites des `.lean` du paquet `Mathlib/`, provenance `fichier:ligne (identifiant complet)`, champ déduit du dossier thématique |
| **AI Act** (CELEX 32024R1689) | **direct** (dépôt Cellar officiel, Décision 2011/833/UE) | texte intégral 1,26 Mo téléchargé (SHA-256 vérifié), 34 définitions de l'art. 3 encodées |
| **RGPD** (CELEX 32016R0679) | **direct** (dépôt Cellar officiel) | texte intégral 807 Ko (SHA-256 vérifié), 15 définitions de l'art. 4 encodées |
| **W3C SKOS Reference** | direct (W3C Document License) | document vérifié (SHA-256), vocabulaire `skos:*` encodé (17 lemmes) |
| **SMC–CMC** (*Canadian Mathematical Communications*, Gold OA, ISSN 2976-8594) | direct (Cambridge Core) | page journal vérifiée (SHA-256), **18 notions** issues des titres d'articles du vol. 1, classement par règles fermées |
| **SMC–Crux** (Crux Mathematicorum) | **référence seule** (copyright : copie usage personnel) | aucune ingération — conformément aux conditions CMS |
| **ISO/IEC 22989, 2382 ; IEEE 754** | référence seule (payant) | numéro + titre + autorité, **aucun texte ingéré** |

Régénération des snapshots + module `sources_ouvertes.py` :
`python _outils/generer_sources_ouvertes.py` (échoue sans réseau plutôt que
d'inventer).

Garanties : les 101 notions manuelles gardent la priorité (`INSERT OR IGNORE`) ;
les sous-mots Mathlib issus d'identifiants sont dédoublonnés ; un **ensemble
ferme de mots vides français** (`MOTS_VIDES_FR`) est exclu pour ne jamais
faire passer une question hors corpus pour une reconnaissance. Dépôt Mathlib
absent → enrichissement simplement abstenu (variable `PYTHONLLM_MATHLIB`
possible pour pointer ailleurs).

## Les six champs de connaissance

1. **LOGIQUE** — calculabilité, Curry-Howard, logiques modale/temporelle/déontique
2. **ALGEBRE** — théorie des types, catégories, Boole, sous-typage
3. **ARITHMETIQUE** — modulaire, corps finis, IEEE 754
4. **GEOMETRIE** — géométrie algorithmique, topologie, théorie des graphes
5. **STATISTIQUES** — inférence, Markov, entropie de Shannon
6. **COMPILATION** — sémantiques, analyse statique, méthodes formelles

## Réponse à la question sur `(-1)^(1/2) = i`

Oui : en logique computationnelle, **inventer un nombre est possible** — c'est
même le fondement. `i` n'est pas tiré au hasard : il est **défini** comme la
racine de `x² + 1 = 0`, dans une structure de corps (`ℂ`) dont les axiomes
sont fixes. Ce n'est pas une hallucination connexionniste, c'est une
**construction formelle** : le symbole a une définition rigoureuse et un
domaine de validité borné. C'est exactement ce que reflète ce pipeline — il
n'émet que ce qui est défini dans un cadre formel, et refuse le reste.

## Tests

```bash
python -m pytest test_pythonLLM_computationnel.py -q   # 30 tests
```

Dépendances : **bibliothèque standard Python uniquement** (aucune).
