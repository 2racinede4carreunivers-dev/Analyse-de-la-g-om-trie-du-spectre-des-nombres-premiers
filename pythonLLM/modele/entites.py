# -*- coding: utf-8 -*-
"""
modele/entites.py — modele de donnees fige du pipeline computationnaliste.

Toutes les structures sont des ``dataclass(frozen=True)`` : aucune mutation
apres construction. Cela materialise le principe computationnaliste : un objet
numerique, une fois defini, ne derive pas. Les scores sont portes par des
``fractions.Fraction`` (arithnetique exacte, zero erreur d'arrondi) plutot que
par des flottants IEEE 754.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Optional, Tuple


# =============================================================================
# CORPUS NORMATIF — entites encodees dans la base SQLite
# =============================================================================

@dataclass(frozen=True)
class ChampConnaissance:
    """Un des six champs de connaissance computationnelle.

    ``code`` court stable (ex. ``LOGIQUE``), ``libelle`` affichable UTF-8.
    ``poids`` est un entier strictement positif : il fixe l'ordre total de
    priorite entre champs en cas d'egalite de score (jamais de tirage).
    """
    code: str
    libelle: str
    poids: int
    description: str = ""


@dataclass(frozen=True)
class Institution:
    """Une institution de normalisation / reglementation source du corpus.

    ``type_institution`` appartient a un ensemble ferme : ``norme``,
    ``droit``, ``philosophie``. ``autorite`` est un entier (rang de priorite
    normative : plus petit = plus contraignant).
    """
    identifiant: str
    nom: str
    type_institution: str  # norme | droit | philosophie
    autorite: int
    perimetre: str = ""


@dataclass(frozen=True)
class Notion:
    """Un terme reconnu, rattache a un champ et eventuellement a une source.

    ``lemme`` est la forme normalisee (minuscule, sans accents) servant a
    l'appartenance ensembliste exacte. ``graphe`` indique si le terme designe
    une structure relationnelle (arbre, graphe) plutot qu'une valeur.
    """
    lemme: str
    champ_code: str
    source_id: Optional[str] = None
    graphe: bool = False
    definition: str = ""


@dataclass(frozen=True)
class Invariant:
    """Une regle formelle permanente attachee a un champ.

    ``code`` stable, ``enonce`` lisible, ``severite`` dans un ensemble ferme
    (``obligation`` | ``interdiction`` | ``permission``). Sert a la logique
    deontique de validation de la commande generee.
    """
    code: str
    champ_code: str
    enonce: str
    severite: str  # obligation | interdiction | permission


@dataclass(frozen=True)
class RegleIntention:
    """Une regle ordonnee de classification d'intention.

    Les regles sont evaluees dans l'ordre de ``priorite`` (ordre total, pas
    d'egalite : deux regles ne peuvent pas partager la meme priorite). Une
    regle porte des ``mots_declencheurs`` exacts et une ``intention`` cible.
    ``champ_requis`` impose la presence d'une notion de ce champ pour activer.
    """
    priorite: int
    intention: str
    condition: str  # description lisible de la condition
    champ_requis: Optional[str] = None
    mots_declencheurs: Tuple[str, ...] = ()


# =============================================================================
# GRAMMAIRE DU CLI CLINE — options typees
# =============================================================================

@dataclass(frozen=True)
class TypeOption:
    """Type formel d'une option CLI (domaine de valeurs)."""
    nom: str  # booleen | entier | chemin | enum | texte | niveau_reflexion | mode_compaction
    enum_valeurs: Tuple[str, ...] = ()
    defaut: Optional[str] = None
    regex: Optional[str] = None  # motif de validation pour les libres


@dataclass(frozen=True)
class OptionCline:
    """Une option du CLI Cline, avec son type et sa cardinalite.

    ``long`` (ex. ``--cwd``) et ``court`` (ex. ``-c``) sont les deux formes.
    ``prend_valeur`` indique si l'option attend un argument. ``obligatoire``
    et ``exclusif_avec`` alimentent la logique deontique de validation.
    """
    long: str
    type: TypeOption
    court: Optional[str] = None
    prend_valeur: bool = False
    obligatoire: bool = False
    exclusif_avec: Tuple[str, ...] = ()
    aide: str = ""


@dataclass(frozen=True)
class CommandeCline:
    """AST d'une commande ``cline`` : executable + sous-commande + options.

    ``options`` est un tuple de paires ``(nom_long, valeur)``. L'ordre est
    stable (ordre d'insertion) pour une emission reproductible.
    """
    executable: str = "cline"
    sous_commande: Optional[str] = None
    options: Tuple[Tuple[str, Optional[str]], ...] = ()
    arguments: Tuple[str, ...] = ()

    def argv(self) -> Tuple[str, ...]:
        """Materialise la commande en argv typé (pas de concaténation de texte)."""
        parties = [self.executable]
        if self.sous_commande:
            parties.append(self.sous_commande)
        for nom, val in self.options:
            parties.append(nom)
            if val is not None:
                parties.append(val)
        parties.extend(self.arguments)
        return tuple(parties)


# =============================================================================
# PIPELINE — reconnaissance, trace, resultats
# =============================================================================

@dataclass(frozen=True)
class ResultatReconnaissance:
    """Issue de la reconnaissance de la requete contre le corpus.

    ``scores`` associe un code de champ a un ``Fraction`` exact. ``termes``
    conserve les lemmes reconnus (preuve d'appartenance ensembliste).
    """
    scores: Tuple[Tuple[str, Fraction], ...] = ()
    termes_reconnus: Tuple[str, ...] = ()
    aucun_terme: bool = True

    def score_champ(self, code: str) -> Fraction:
        for c, s in self.scores:
            if c == code:
                return s
        return Fraction(0)

    def champ_dominant(self) -> Optional[str]:
        """Champ de score maximal ; egalite departagee par l'ordre du tuple
        (qui suit l'ordre de poids du corpus : deterministe)."""
        if not self.scores:
            return None
        best_code, best_score = self.scores[0]
        for code, score in self.scores[1:]:
            if score > best_score:
                best_code, best_score = code, score
        return best_code


@dataclass(frozen=True)
class TraceEtape:
    """Une etape de la trace de derivation, chainee par SHA-256.

    ``empreinte`` = SHA-256(empreinte_precedente + donnee). Chaine inalterable.
    """
    ordre: int
    nom: str
    donnee: str
    empreinte_precedente: str
    empreinte: str


@dataclass(frozen=True)
class RefusFormel:
    """Refus formel et justifie : le pipeline n'invente jamais.

    ``motif`` explicite, ``etape`` l'endroit du pipeline, ``invariants`` les
    regles violees le cas echeant.
    """
    motif: str
    etape: str
    invariants: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ResultatPipeline:
    """Resultat complet d'une traversee du pipeline.

    Soit ``commande`` est renseignee (avec ``argv``), soit ``refus`` l'est.
    ``trace`` est toujours present.
    """
    requete: str
    intention: Optional[str]
    reconnaissance: ResultatReconnaissance
    commande: Optional[CommandeCline]
    refus: Optional[RefusFormel]
    trace: Tuple[TraceEtape, ...]
    argv: Tuple[str, ...] = ()

    @property
    def est_refus(self) -> bool:
        return self.refus is not None

    mots_declencheurs: Tuple[str, ...] = ()
