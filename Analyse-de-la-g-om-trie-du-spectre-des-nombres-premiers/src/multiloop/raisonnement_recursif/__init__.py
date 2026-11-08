"""raisonnement_recursif - Auto-programmation encadree de l'agent fusionne.

Copie du pipeline de correction (variateur mecanique / transformateur toroidal)
adaptee au raisonnement recursif : lorsque l'agent ne possede pas le necessaire
pour repondre a une requete VALIDE (dans le sujet), il genere un patch de
correction .json, l'applique via le pipeline - dans une SANDBOX isolee, en
dry-run par defaut - puis se verifie et peut se rollback.

SECURITE : jamais d'ecriture sur le depot vivant par defaut.
"""
from __future__ import annotations

from .archiveur_timeline import ArchiveurTimeline, CHEMIN_DB
from .decomposeur_lexical import AnalyseLexicale, analyser
from .detecteur_manque import (
    DiagnosticManque,
    detecter_manque,
    tenter_raisonnement_recursif,
)
from .engine_recursif_background import (
    MoteurRecursifBackground,
    ResultatMoteurRecursif,
)
from .generateur_question_modeste import (
    construire_questions_modestes,
    meilleure_question_modeste,
    choix_scores,
)
from .messages import MESSAGE_AUTOPROGRAMMATION
from .oracle_numerique import OracleNumerique, ResultatOracle
from .pipeline_auto_programmation import (
    OPERATIONS_VALIDES,
    PipelineAutoProgrammation,
    RapportApplication,
    VariateurSandboxError,
    construire_contrat_squelette,
)
from .proposition_code import (
    DevenirCode,
    PropositionCode,
    composer_message,
    evaluer_possibilite,
    proposer_amelioration,
)

__all__ = [
    # Messages
    "MESSAGE_AUTOPROGRAMMATION",
    # Auto-programmation sandboxee
    "detecter_manque",
    "DiagnosticManque",
    "tenter_raisonnement_recursif",
    "PipelineAutoProgrammation",
    "RapportApplication",
    "construire_contrat_squelette",
    "OPERATIONS_VALIDES",
    "VariateurSandboxError",
    # 8e moteur (raisonnement recursif)
    "MoteurRecursifBackground",
    "ResultatMoteurRecursif",
    "AnalyseLexicale",
    "analyser",
    "construire_questions_modestes",
    "meilleure_question_modeste",
    "choix_scores",
    "OracleNumerique",
    "ResultatOracle",
    "ArchiveurTimeline",
    "CHEMIN_DB",
    # Phase 3 : proposition d'amelioration du depot apres un blocage
    "PropositionCode",
    "DevenirCode",
    "evaluer_possibilite",
    "proposer_amelioration",
    "composer_message",
]