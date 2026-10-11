"""proposition_code.py - Le 8e moteur propose d'ameliorer son propre depot.

Brique de la phase 3 : quand le moteur de raisonnement recursif a DEJTA
constate un blocage (il n'a pas pu repondre), Gabriel ne se contente pas de
l'archiver : il confronte ce manque a sa banque d'analyste informatique
(Gabriel_Dev_analyste_informatique.py) et, si le depot n'offre pas encore la
capacite requise, il PROPOSE une modification de son propre code.

Principes :
  * PROPOSITION uniquement : le depot vivant n'est jamais ecrit ;
  * les patches sont SIMULES dans la sandbox data/analyste/sandbox (dry-run),
    GABRIEL_RECURSIVE_APPLY=1 pour une ecriture sandboxee reelle ;
  * kill-switch GABRIEL_DEV_ANALYSTE=0 ;
  * message en francais, dans le sujet (compatible fiancee_guard).

ADDITIF : stdlib seul, script d'analyste charge par chemin de fichier
(l'import du paquet src.multiloop tire httpx, absent de cet environnement).
"""
from __future__ import annotations

import importlib.util
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

RACINE_DEPOT = Path(__file__).resolve().parents[3]
SCRIPT_ANALYSTE = RACINE_DEPOT / "Gabriel_Dev_analyste_informatique.py"

KILL_SWITCH = "GABRIEL_DEV_ANALYSTE"

MESSAGE_BLOCAGE_REPERE = (
    "Blocage du 8e moteur : la requete depasse le perimetre de connaissance "
    "actuel et aucune question modeste n'a pu etre resolue."
)


def analyste_actif() -> bool:
    """Kill-switch partage avec Gabriel_Dev_analyste_informatique.py."""
    return os.environ.get(KILL_SWITCH, "1").strip().lower() not in (
        "0", "false", "non", "off", "no",
    )


def charger_analyste() -> Any:
    """Charge le script d'analyste par chemin, HORS paquet (pas de httpx).

    Enregistre le module dans sys.modules avant exec_module : Python >= 3.12
    exige cette resolution pour les @dataclass.
    """
    nom = "_gabriel_dev_analyste"
    deja = sys.modules.get(nom)
    if deja is not None:
        return deja
    if not SCRIPT_ANALYSTE.is_file():
        return None
    try:
        spec = importlib.util.spec_from_file_location(nom, SCRIPT_ANALYSTE)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[nom] = module
        spec.loader.exec_module(module)
        return module
    except Exception:
        sys.modules.pop(nom, None)
        return None


@dataclass
class PropositionCode:
    """Une amelioration envisageable du depot, avec son patch eventuel."""
    categorie: str
    fichier: str
    titre: str
    justification: str
    ligne: int = 0
    operation: Optional[dict[str, Any]] = None
    competences: list[str] = field(default_factory=list)

    @property
    def patchable(self) -> bool:
        return self.operation is not None

    @property
    def cible(self) -> str:
        if not self.operation:
            return self.fichier
        return str(self.operation.get("cible", self.fichier))

    @property
    def op(self) -> str:
        return str(self.operation.get("op", "")) if self.operation else "—"

    def to_dict(self) -> dict[str, Any]:
        return {
            "categorie": self.categorie, "fichier": self.fichier,
            "ligne": self.ligne, "titre": self.titre,
            "justification": self.justification,
            "patchable": self.patchable, "cible": self.cible, "op": self.op,
            "competences": list(self.competences),
        }


@dataclass
class DevenirCode:
    """Resultat du tirage de propositions apres un blocage du 8e moteur."""
    declenche: bool
    requete: str
    message: str = ""
    raison: str = ""
    propositions: list[PropositionCode] = field(default_factory=list)
    contexte: list[dict[str, Any]] = field(default_factory=list)
    contrats: int = 0
    simulations: list[dict[str, Any]] = field(default_factory=list)
    erreurs: list[str] = field(default_factory=list)

    @property
    def patchables(self) -> list[PropositionCode]:
        return [p for p in self.propositions if p.patchable]

    @property
    def simulations_propres(self) -> int:
        return sum(
            1 for s in self.simulations
            if (s.get("simules", 0) or s.get("ok", 0)) and not s.get("echouees")
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "declenche": self.declenche, "requete": self.requete,
            "raison": self.raison, "message": self.message,
            "propositions": [p.to_dict() for p in self.propositions],
            "contexte": self.contexte, "contrats": self.contrats,
            "simulations": self.simulations,
            "simulations_propres": self.simulations_propres,
            "erreurs": list(self.erreurs),
        }


# ── declencheur : y a-t-il une possibilite d'amelioration ? ───────────────
def evaluer_possibilite(resultat_moteur: Any) -> tuple[bool, str]:
    """Le 8e moteur a-t-il percu une possibilite d'ameliorer le depot ?

    Le 8e moteur ne repond PAS a la requete initiale : il l'explique
    (`blocage`). Un blocage explicite signifie donc que le depot ne dispose
    pas encore de la capacite demandee — c'est exactement le moment ou une
    amelioration est concevable.

    `reponse_modeste` et `citable` sont RETENUS comme contexte, jamais comme
    bloquants : l'oracle repond presque toujours a la question modeste
    (repli local), ce qui ne resout pas la requete d'origine.
    """
    if not analyste_actif():
        return False, f"{KILL_SWITCH}=0"
    if not getattr(resultat_moteur, "declenche", False):
        return False, "8e moteur non declenche"
    if not str(getattr(resultat_moteur, "blocage", "") or "").strip():
        return False, "aucun blocage explique : requete couverte"
    contexte = []
    if getattr(resultat_moteur, "reponse_modeste", None):
        contexte.append("question modeste resolue")
    if getattr(resultat_moteur, "citable", False):
        contexte.append("timeline deja citable")
    detail = " ; ".join(contexte)
    return True, (
        "blocage non resolu : le depot n'offre pas la capacite"
        + (f" ({detail})" if detail else "")
    )


# ── tirage des propositions ──────────────────────────────────────────────
def proposer_amelioration(
    requete: str,
    resultat_moteur: Any = None,
    plafond: int = 5,
    banque: Any = None,
) -> DevenirCode:
    """Confronte le blocage a la banque d'analyste et propose un patch.

    Retourne toujours un DevenirCode ; `declenche=False` si la possibilite
    d'amelioration n'existe pas (aucun blocage, kill-switch, script absent).
    """
    ok, raison = evaluer_possibilite(resultat_moteur) if resultat_moteur is not None \
        else (analyste_actif(), "analyse a la demande")
    devenir = DevenirCode(declenche=ok, requete=requete, raison=raison)
    if not ok:
        devenir.message = f"Analyse du depot non declenchee : {raison}."
        return devenir

    analyseur = charger_analyste()
    if analyseur is None:
        devenir.declenche = False
        devenir.raison = "script Gabriel_Dev_analyste_informatique.py introuvable"
        devenir.message = f"Analyse du depot non declenchee : {devenir.raison}."
        return devenir

    try:
        base = banque or analyseur.BanqueAnalyste()
        if base.stats()["noeuds"] == 0:
            base.amorcer()
        devenir.contexte = base.rechercher(requete, limite=5)
        bruts = analyseur.construire_propositions(
            base, requete, racine=analyseur.RACINE, plafond=plafond,
        )
    except Exception as exc:                     # jamais fatal pour le pipeline
        devenir.erreurs.append(f"analyse : {exc}")
        devenir.message = (
            "Mm. Gabriel a percu une possibilite d'amelioration, mais "
            f"l'analyse du depot a echoue ({exc}). Rien n'a ete modifie."
        )
        return devenir

    contrats: list[dict[str, Any]] = []
    for p in bruts:
        devenir.propositions.append(PropositionCode(
            categorie=p.categorie, fichier=p.fichier, titre=p.titre,
            justification=p.justification, ligne=p.ligne,
            operation=dict(p.operation) if p.operation else None,
            competences=list(p.noeuds_connaissance),
        ))
        contrat = getattr(analyseur, "contrat_pour", None)
        if contrat is not None and p.operation:
            c = contrat(p, requete)
            if c is not None:
                contrats.append(c)
    devenir.contrats = len(contrats)

    try:
        devenir.simulations = analyseur.simuler(contrats, ecrire=False)
    except Exception as exc:
        devenir.erreurs.append(f"simulation : {exc}")

    devenir.message = composer_message(devenir, resultat_moteur)
    return devenir


def composer_message(
    devenir: DevenirCode, resultat_moteur: Any = None,
) -> str:
    """Message de projection affiche par le CLI (sujet, factuel, non agressif)."""
    if not devenir.propositions:
        return (
            "Mm. Gabriel a percu un blocage mais n'a identifie aucune "
            "amelioration de son depot : le code est conforme a l'analyse. "
            "La timeline reste archivee pour resolution ulterieure."
        )
    archive = getattr(resultat_moteur, "archive_id", None)
    lignes = [
        "Mm. Gabriel a percu une POSSIBILITE d'ameliorer son propre code "
        f"apres le blocage du 8e moteur"
        + (f" (timeline #{archive})" if archive else "") + " :",
        f"  {len(devenir.propositions)} point(s), "
        f"{len(devenir.patchables)} patch(s), "
        f"{devenir.simulations_propres} simulation(s) propre(s) en sandbox "
        "(dry-run, depot vivant intact).",
    ]
    for i, p in enumerate(devenir.propositions, start=1):
        emplacement = f"{p.fichier}" + (f":{p.ligne}" if p.ligne else "")
        lignes.append(
            f"  {i}. [{p.op}] {emplacement} — {p.titre}"
            + ("" if p.patchable else "  (note, sans patch automatique)")
        )
        if p.competences:
            lignes.append(f"     competences : {', '.join(p.competences)}")
    lignes.append(
        "  Aucune ecriture n'a eu lieu. Pour appliquer en sandbox : "
        "GABRIEL_RECURSIVE_APPLY=1 (dossier data/analyste/sandbox)."
    )
    return "\n".join(lignes)


def resume_cinematique(devenir: DevenirCode) -> dict[str, Any]:
    """Evenements a injecter dans le CinematicDisplay (informatif)."""
    return {
        "step": "proposition_code",
        "declenche": devenir.declenche,
        "propositions": len(devenir.propositions),
        "patchables": len(devenir.patchables),
        "simulations_propres": devenir.simulations_propres,
        "categorie_principale": (
            devenir.propositions[0].categorie if devenir.propositions else ""
        ),
    }


__all__ = [
    "SCRIPT_ANALYSTE", "KILL_SWITCH", "analyste_actif", "charger_analyste",
    "PropositionCode", "DevenirCode", "evaluer_possibilite",
    "proposer_amelioration", "composer_message", "resume_cinematique",
    "MESSAGE_BLOCAGE_REPERE",
]
