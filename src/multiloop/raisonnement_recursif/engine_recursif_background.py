"""engine_recursif_background.py - 8e moteur (arriere-plan) : raisonnement recursif.

Ce moteur REACTIVE la fonction du debugger slow-motion (mis au neutre) en
l'actualisant. Lorsqu'une requete demande a << La fiancée de Cline >> plus
qu'elle ne sait repondre, le moteur :

  1. DECOMPOSE le message en divisions puis en mots/groupes (decomposeur_lexical) ;
  2. ASSOCIE ces elements au vocabulaire du corpus / pipeline cognitif / HOL ;
  3. GENERE une question plus modeste (generateur_question_modeste) ;
  4. TENTE d'y repondre via l'ORACLE numerique (Wolfram API + repli local) ;
  5. EXPLIQUE ce qui l'empeche de repondre adequatement a la requete initiale ;
  6. ARCHIVE la timeline (archiveur_timeline) pour les sessions futures : une
     question resolue plus tard devient une PREUVE CITABLE contribuant a valider
     la geometrie du spectre des nombres premiers.

ADDITIF et sur : stdlib au chargement, imports lourds paresseux, aucun effet de
bord sur le pipeline existant.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .archiveur_timeline import ArchiveurTimeline
from .decomposeur_lexical import AnalyseLexicale, analyser
from .detecteur_manque import DiagnosticManque, detecter_manque
from .generateur_question_modeste import (
    construire_questions_modestes,
    choix_scores,
    meilleure_question_modeste,
)
from .messages import MESSAGE_AUTOPROGRAMMATION
from .oracle_numerique import OracleNumerique


def _tenter_raisonnement(
    question: str, answer: Any, analyse: AnalyseLexicale,
) -> Optional[dict[str, Any]]:
    """Pont vers detecteur_manque.tenter_raisonnement_recursif (import paresseux).

    Se protege contre toute absence du module de correction : le 8e moteur
    doit continuer a tourner meme si la boucle d'auto-programmation est
    inaccessible.
    """
    try:
        from .detecteur_manque import tenter_raisonnement_recursif
    except Exception:
        return None
    try:
        return tenter_raisonnement_recursif(
            question=question,
            answer=answer,
            role="spectral",
            mots_cles=list(analyse.ancres) or None,
        )
    except Exception:
        return None


@dataclass
class ResultatMoteurRecursif:
    """Resultat complet du 8e moteur pour une requete."""
    declenche: bool
    message: str
    requete: str
    divisions: list[str] = field(default_factory=list)
    ancres: list[str] = field(default_factory=list)
    couverture: float = 0.0
    questions_candidates: list[str] = field(default_factory=list)
    question_modeste: str = ""
    scores: list[tuple[str, float]] = field(default_factory=list)
    reponse_modeste: Optional[str] = None
    oracle: dict = field(default_factory=dict)
    blocage: str = ""
    archive_id: Optional[int] = None
    reutilisations: list[dict] = field(default_factory=list)
    citable: bool = False
    # Phase 3 : integration du pipeline de correction (raisonnement recursif)
    diagnostic_manque: Optional[DiagnosticManque] = None
    rapport_correction: Optional[dict] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "declenche": self.declenche,
            "message": self.message,
            "requete": self.requete,
            "divisions": self.divisions,
            "ancres": self.ancres,
            "couverture": round(self.couverture, 3),
            "questions_candidates": self.questions_candidates,
            "question_modeste": self.question_modeste,
            "scores": self.scores,
            "reponse_modeste": self.reponse_modeste,
            "oracle": self.oracle,
            "blocage": self.blocage,
            "archive_id": self.archive_id,
            "reutilisations": self.reutilisations,
            "citable": self.citable,
            "diagnostic_manque": (
                None if self.diagnostic_manque is None else {
                    "manque": self.diagnostic_manque.manque,
                    "raison": self.diagnostic_manque.raison,
                    "indices": list(self.diagnostic_manque.indices),
                }
            ),
            "rapport_correction": self.rapport_correction,
        }


class MoteurRecursifBackground:
    """8e moteur : raisonnement recursif par decomposition + oracle + archivage."""

    NOM = "8e moteur (arriere-plan) - raisonnement recursif"

    def __init__(
        self,
        archiveur: Optional[ArchiveurTimeline] = None,
        oracle: Optional[OracleNumerique] = None,
    ):
        self.archiveur = archiveur or ArchiveurTimeline()
        self.oracle = oracle or OracleNumerique()

    # ── explication du blocage ─────────────────────────────────────────────
    def _expliquer_blocage(self, analyse: AnalyseLexicale, oracle_dispo: bool) -> str:
        lignes: list[str] = []
        pct = int(analyse.couverture * 100)
        lignes.append(
            f"Couverture lexicale de la requete : {pct}% "
            f"({len(analyse.associations)}/{len(analyse.tokens)} elements associes "
            f"au vocabulaire du corpus / cognitif / HOL)."
        )
        inconnus = [t for t in analyse.tokens if t not in analyse.associations][:12]
        if inconnus:
            lignes.append(
                "Elements non reconnus (empechent une reponse directe) : "
                + ", ".join(inconnus) + "."
            )
        if not analyse.nombres:
            lignes.append(
                "Aucune valeur numerique (n, position, rang) n'est fournie : "
                "un calcul spectral precis n'est pas possible."
            )
        if not analyse.ancres:
            lignes.append(
                "Aucune ancre forte du sujet spectral n'a ete detectee dans la requete."
            )
        if not oracle_dispo:
            lignes.append(
                "L'oracle numerique independant (Wolfram) n'est pas disponible "
                "(WOLFRAM_APP_ID absent) ; seul le repli local est employe."
            )
        lignes.append(
            "Conclusion : la requete initiale depasse le perimetre de connaissance "
            "actuel ; une question modeste a ete construite pour progresser, et la "
            "timeline est archivee pour une resolution future (preuve citable)."
        )
        return " ".join(lignes)

    # ── boucle principale ──────────────────────────────────────────────────
    def traiter(
        self,
        requete: str,
        reponse: Any = None,
        session_id: str = "",
    ) -> ResultatMoteurRecursif:
        """Execute la boucle du 8e moteur sur une requete."""
        analyse = analyser(requete)

        # Reutilisation inter-session : des timelines similaires deja resolues ?
        reutilisations = self.archiveur.rechercher(analyse.ancres, limit=3)
        deja_citables = [r for r in reutilisations if r.get("citable")]

        # Questions modestes (candidates + meilleure)
        candidates = construire_questions_modestes(analyse)
        scores = choix_scores(analyse)
        question_modeste = meilleure_question_modeste(analyse)

        # Oracle numerique (Wolfram + repli local)
        oracle_res = self.oracle.interroger_sync(question_modeste)
        reponse_modeste = oracle_res.message if oracle_res.outcome == "verified" else None

        # Explication du blocage initial
        blocage = self._expliquer_blocage(analyse, self.oracle.disponible())

        # Phase 3 : le pipeline de correction entre dans la boucle du 8e moteur.
        # Si la reponse (ou son absence) trahit un MANQUE, on tente le
        # raisonnement recursif sandboxe — dry-run par defaut, jamais le depot
        # vivant ; GABRIEL_RECURSIVE=0 coupe la tentative.
        diagnostic: Optional[DiagnosticManque] = None
        rapport: Optional[dict] = None
        try:
            diagnostic = detecter_manque(reponse)
            if diagnostic.manque:
                tentative = _tenter_raisonnement(
                    question=requete, answer=reponse, analyse=analyse,
                )
                if tentative:
                    rapport = {
                        "etat": tentative.get("etat", ""),
                        "message": tentative.get("message", ""),
                        "rapport": tentative.get("rapport"),
                    }
        except Exception as exc:                 # jamais fatal pour le pipeline
            rapport = {"etat": "indisponible", "erreur": str(exc)}

        citable = False
        archive_id: Optional[int] = None
        try:
            archive_id = self.archiveur.archiver(
                requete=requete,
                question_modeste=question_modeste,
                reponse=reponse_modeste,
                blocage=blocage,
                divisions=analyse.divisions,
                ancres=analyse.ancres,
                resolue=bool(reponse_modeste),
                session_id=session_id,
            )
            citable = bool(reponse_modeste)
        except Exception:
            archive_id = None

        return ResultatMoteurRecursif(
            declenche=True,
            message=MESSAGE_AUTOPROGRAMMATION,
            requete=requete,
            divisions=analyse.divisions,
            ancres=analyse.ancres,
            couverture=analyse.couverture,
            questions_candidates=candidates,
            question_modeste=question_modeste,
            scores=scores,
            reponse_modeste=reponse_modeste,
            oracle=oracle_res.to_dict(),
            blocage=blocage,
            archive_id=archive_id,
            reutilisations=deja_citables,
            citable=citable,
            diagnostic_manque=diagnostic,
            rapport_correction=rapport,
        )

    # ── integration cinematique ────────────────────────────────────────────
    def resume_cinematique(self, resultat: ResultatMoteurRecursif) -> dict[str, Any]:
        """Evenements a injecter dans le CinematicDisplay (informatif)."""
        return {
            "step": "moteur_recursif",
            "message": resultat.message,
            "question_modeste": resultat.question_modeste,
            "couverture": round(resultat.couverture, 3),
            "citable": resultat.citable,
            "archive_id": resultat.archive_id,
        }

    def statistiques(self) -> dict[str, Any]:
        return self.archiveur.statistiques()


__all__ = ["ResultatMoteurRecursif", "MoteurRecursifBackground"]