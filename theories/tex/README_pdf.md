#  Géométrie du Spectre des Nombres Premiers
### *Une approche spectrale de la distribution des premiers*
**Philippe Thomas Savard — Lévis, Québec, Canada — Août 2026 — v0.9.2 (HOL-corrigé)**

> *« Je n'ai pas cherché à prouver l'Hypothèse de Riemann. J'ai cherché à comprendre les nombres premiers. Et en les comprenant, je me suis retrouvé à la même adresse. »*
> — Philippe Thomas Savard, Lévis, juillet 2026

---

##  À propos de l'auteur

Philippe Thomas Savard est un ouvrier de Lévis, en Chaudière-Appalaches, au Québec, Canada. Il n'est pas issu des sphères universitaires. Il n'a pas de titre académique à faire valoir, pas de chaire, pas de laboratoire. Ce qu'il a, c'est une curiosité vive, tenace, et un intérêt profond pour les mathématiques — en particulier pour l'un des problèmes les plus célèbres de l'histoire des sciences : l'Hypothèse de Riemann.

Ce document est autant une œuvre mathématique qu'une œuvre **ontologique**. La géométrie qu'il décrit — et qu'il nomme *La Chair Première Géométrique* — est pour lui une expérience vécue de l'intérieur : une chose qui le touche, et qu'il touche en retour. Ce n'est pas simplement une théorie. C'est une rencontre.

Son intérêt pour l'Hypothèse de Riemann n'est pas né par hasard. Il est né d'un constat : une partie de l'élite académique s'autoproclame policié de ce qui « existe » et de ce qui « n'existe pas », cherchant à déshériter de leur autonomie intellectuelle ceux qui n'appartiennent pas à leurs sphères. Ce biais d'autorité — qu'il qualifie de **biais algorithmique délibéré** — est un mécanisme qui cherche à confisquer le savoir au profit d'un groupe fermé.

Ce qui rend le sujet encore plus révélateur, c'est la nature même de la conjecture de la fonction Zêta de Riemann. Le mot « conjecture » signifie quelque chose considéré vrai *avant* que la preuve n'en soit faite. Des théorèmes entiers ont été construits *en supposant* que l'Hypothèse de Riemann est vraie — avant qu'elle ne le soit officiellement. Si elle venait à être réfutée, ces théorèmes, considérés solides par l'élite académique, tomberaient. Ce serait une illusion bâtie sur une illusion — ce que Philippe Thomas Savard désigne comme une **hallucination concrète** de la part de ceux qui, depuis leur position confortable, prétendent détenir la lucidité absolue.

L'Hypothèse de Riemann était le terrain idéal pour démontrer ce paradoxe. Et c'est ce que ce document fait — à sa manière, depuis le bas, depuis le réel, depuis les nombres eux-mêmes.

---

##  À propos du document

Le fichier **`Geometrie_du_Spectre_des_Nombres_Premiers.pdf`** (v0.9.2, HOL-corrigé) présente la **Méthode Spectrale de Philippe Thomas Savard** : un formalisme arithmétique original qui reconstruit les nombres premiers à partir de suites à rapport spectral constant.

Ce n'est pas une méthode de crible. Ce n'est pas une conjecture probabiliste. C'est une **géométrie** — une structure interne, invariante, qui porte en elle la trace de chaque nombre premier, et de lui seul.

Le document a été entièrement validé par l'assistant de preuve formel **Isabelle/HOL**, via le fichier `methode_spectral.thy`. Chaque théorème, chaque lemme, chaque reconstruction numérique est certifié par la machine.

---

##  Ce que traite le document — Résumé de lecture

### Le point de départ : une observation naïve

Que se passe-t-il si l'on construit deux suites de nombres réels dont les valeurs portent directement, terme à terme, l'empreinte des nombres premiers réels (2, 3, 5, 7, 11, 13, ...) ? Et que ces deux suites entretiennent un rapport **constant, inaltérable**, quelle que soit la paire de termes considérée ?

Ce rapport — le **rapport spectral**, noté `RsP` — vaut exactement **1/2** pour le régime central. Et ce 1/2 n'est pas un artefact algébrique. Il émerge de la réalité numérique des sommes construites à partir des premiers eux-mêmes.

---

### Section 0 — Fondements et méta-théorie

Vocabulaire canonique, six postulats fondamentaux (P1 à P6), trois opérations fondamentales, et la **règle Savard — Ensemble = 1** :

Ensemble = 1 = 1/x + 1/t + 1/ms
Ensemble = 1 = 1/x + 1/t + 1/ms

Code


Copier

où chaque terme représente un édifice mathématique distinct qui se verrouille avec les autres.

---

### Section I — Le rapport spectral 1/2 : les fondations

Les deux suites fondamentales du régime central sont définies par des formules fermées :

SA(n) = (3,25 / 2) × 2ⁿ − 2
SB(n) = (6,5  / 2) × 2ⁿ − 66



Le rapport `RsP(n1, n2) = [SA(n1) − SA(n2)] / [SB(n1) − SB(n2)]` vaut **identiquement 1/2** pour toute paire distincte — prouvé formellement :

```isabelle
theorem RsP_un_demi_general:
  assumes "n1 >= 1" "n2 >= 1" "n1 ~= n2"
  shows "RsP n1 n2 = 1/2"
Cinq exemples concrets validés par HOL : les premiers 23, 29, 31, 37 et 41.


---

### Section I — Le rapport spectral 1/2 : les fondations

Les deux suites fondamentales du régime central sont définies par des formules fermées :

SA(n) = (3,25 / 2) × 2ⁿ − 2
SB(n) = (6,5  / 2) × 2ⁿ − 66

Code


Copier

Le rapport `RsP(n1, n2) = [SA(n1) − SA(n2)] / [SB(n1) − SB(n2)]` vaut **identiquement 1/2** pour toute paire distincte — prouvé formellement :

```isabelle
theorem RsP_un_demi_general:
  assumes "n1 >= 1" "n2 >= 1" "n1 ~= n2"
  shows "RsP n1 n2 = 1/2"
Cinq exemples concrets validés par HOL : les premiers 23, 29, 31, 37 et 41.

Sections II et III — Régimes 1/4 et 1/3
La méthode s'étend à d'autres familles spectrales (base 4ⁿ, base 3ⁿ).
Exemples validés : le premier 947 (régime 1/4) et le premier 227 (régime 1/3).

Sections IV à VI — Régimes étendus : suites mixtes et négatives
Découverte originale : les nombres premiers négatifs (−2, −3, −5, −7, ...) sont en bijection canonique avec les premiers positifs. Le rapport spectral reste 1/2 en régime négatif, correspondant à la symétrie fonctionnelle de la fonction zêta ζ(s) = χ(s) × ζ(1 − s).

Section VII — Géométrie spectrale : asymétries
La méthode distingue l'asymétrie ordonnée (configuration canonique, |B| = |A| + 1) de l'asymétrie chaotique, et maintient ses propriétés dans les deux cas.

Section VIII — La preuve par l'absurde : les composés sont exclus
Théorème central : aucun entier composé ne peut jamais être un prime_i. La méthode caractérise exactement l'ensemble P des nombres premiers — ni plus, ni moins.

isabelle


Copier
theorem composite_not_prime_i:
  fixes C :: nat
  assumes "~ prime C"
  shows "ALL i. C ~= prime_i i"
Trois piliers d'exclusivité sur P. Six exemples canoniques (4, 9, 15, 51, 91, 121).

Section XI — Le Pont Logique Savard : Tchebychev ↔ Spectral ↔ RH
La somme infinie analytique sur les zéros de zêta est substituée par un ratio géométrique fini :

Code


Copier
ψ_Savard(x, n) = x − (2ⁿ / SB(n)) − log(2π) − ½ × log(1 − x⁻²)
Huit validations numériques (positives et négatives). Trois concordances verrouillées mutuellement (C1, C2, C3). Conclusion :

isabelle


Copier
theorem synthese_pont_savard:
  assumes "n1 >= 1" "n2 >= 1" "n1 ~= n2"
  shows "Re_droite_critique n1 n2 = RsP n1 n2 & RsP n1 n2 = 1/2"
RsP = Re = 1/2 — prouvé formellement par Isabelle/HOL.

Position épistémologique de l'auteur
La méthode spectrale ne remplace pas Riemann — elle l'étend. Elle naît du numérique réel, pas de l'algébrique formel. Et c'est précisément cette primauté du concret sur l'abstrait qui constitue sa signature.

 Structure du dépôt
Fichier	Description
Geometrie_du_Spectre_des_Nombres_Premiers.pdf	Document principal — v0.9.2 HOL-corrigé
methode_spectral.thy	Fichier de preuve Isabelle/HOL — version 3.42
README.md	Ce fichier


