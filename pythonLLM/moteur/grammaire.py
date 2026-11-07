# -*- coding: utf-8 -*-
"""
moteur/grammaire.py — grammaire formelle du CLI Cline (options typees).

Encodage direct de la reference officielle ``docs.cline.bot/cli/cli-reference``.
Chaque option porte un TypeOption (domaine de valeurs ferme). Aucune option
inventee. Pieges documentes et respectes :

- ``-t`` / ``--timeout`` (secondes) — ce n'est PAS ``--task`` ;
- il n'existe plus de commande ``task`` : la tache est l'argument positionnel ;
- ``--yolo`` / ``-y`` n'existe plus : c'est ``--auto-approve <boolean>`` (def.
  true) ; le prompt nu demarre deja en mode act avec auto-approbation ;
- ``--thinking`` nu = ``medium`` ; omis = niveau choisi via ``/model`` ;
- exclusifs : ``-p/--plan`` (mode plan) vs mode act (defaut) ; ``-i/--tui``
  (interactif) exclusif avec ``--json`` et ``-z/--zen``.
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

from ..modele.entites import OptionCline, TypeOption

# -----------------------------------------------------------------------------
# Types de base (domaines fermes)
# -----------------------------------------------------------------------------
_T_BOOL = TypeOption(nom="booleen", defaut=None)
_T_BOOL_VAL = TypeOption(nom="booleen_valeur", enum_valeurs=("true", "false"), defaut="true")
_T_ENTIER = TypeOption(nom="entier", defaut="0")
_T_CHEMIN = TypeOption(nom="chemin")
_T_TEXTE = TypeOption(nom="texte")
_T_REFLEXION = TypeOption(
    nom="niveau_reflexion",
    enum_valeurs=("none", "low", "medium", "high", "xhigh"),
    defaut=None,
)
_T_COMPACTION = TypeOption(
    nom="mode_compaction",
    enum_valeurs=("agentic", "basic", "off"),
    defaut="agentic",
)

# -----------------------------------------------------------------------------
# Registre des options globales de ``cline``
# -----------------------------------------------------------------------------
GRAMMAIRE_CLINE: Tuple[OptionCline, ...] = (
    OptionCline("--version", _T_BOOL, court="-V", aide="Affiche le numero de version."),
    OptionCline("--plan", _T_BOOL, court="-p", aide="Execute en mode plan (vs act par defaut)."),
    OptionCline("--json", _T_BOOL, aide="Sort les messages en JSON (une ligne par evenement)."),
    OptionCline("--auto-approve", _T_BOOL_VAL, prend_valeur=True, aide="Auto-approbation des outils (defaut true)."),
    OptionCline("--cwd", _T_CHEMIN, court="-c", prend_valeur=True, aide="Repertoire de travail."),
    OptionCline("--thinking", _T_REFLEXION, prend_valeur=True, aide="Effort de raisonnement none|low|medium|high|xhigh."),
    OptionCline("--compaction", _T_COMPACTION, prend_valeur=True, aide="Mode de compaction agentic|basic|off."),
    OptionCline("--tui", _T_BOOL, court="-i", aide="Ouvre la TUI interactive."),
    OptionCline("--id", _T_TEXTE, aide="Reprend une session existante par son identifiant."),
    OptionCline("--provider", _T_TEXTE, court="-P", aide="Identifiant de fournisseur (defaut cline)."),
    OptionCline("--key", _T_TEXTE, court="-k", aide="Cle d'API pour cette execution."),
    OptionCline("--model", _T_TEXTE, court="-m", aide="Modele a utiliser pour la session."),
    OptionCline("--system", _T_TEXTE, court="-s", aide="Remplace l'invite systeme par defaut."),
    OptionCline("--zen", _T_BOOL, court="-z", aide="Demarre une session en arriere-plan."),
    OptionCline("--retries", _T_ENTIER, aide="Nb max d'erreurs consecutives (defaut 3)."),
    OptionCline("--timeout", _T_ENTIER, court="-t", aide="Delai maximal en secondes (0 = aucun)."),
    OptionCline("--acp", _T_BOOL, aide="Mode Agent Client Protocol (integration editeur)."),
    OptionCline("--config", _T_CHEMIN, aide="Repertoire de configuration (defaut ~/.cline)."),
    OptionCline("--data-dir", _T_CHEMIN, aide="Etat local isole (defaut ~/.cline/data)."),
    OptionCline("--hooks-dir", _T_CHEMIN, aide="Repertoire de hooks supplementaires."),
    OptionCline("--worktree", _T_BOOL, aide="Cree un worktree git detache pour la tache."),
    OptionCline("--update", _T_BOOL, aide="Verifie les mises a jour et les installe."),
    OptionCline("--kanban", _T_BOOL, aide="Lance l'application Kanban."),
    OptionCline("--verbose", _T_BOOL, court="-v", aide="Sortie detaillee."),
    OptionCline("--help", _T_BOOL, court="-h", aide="Affiche l'aide."),
)

# Sous-commandes de premier niveau reconnues (ensemble ferme).
SOUS_COMMANDES: Tuple[str, ...] = (
    "auth", "config", "plugin", "skill", "connect", "mcp",
    "doctor", "history", "h", "hook", "schedule", "hub", "dashboard",
    "update", "version", "kanban",
)

# Relations d'exclusion mutuelle (logique deontique negative).
# Chaque paire : ces deux options ne peuvent pas coexister.
EXCLUSIONS: Tuple[Tuple[str, str], ...] = (
    ("--tui", "--json"),
    ("--tui", "--zen"),
    ("--tui", "--acp"),
    ("--json", "--acp"),
)


def option_par_long(nom_long: str) -> Optional[OptionCline]:
    """Retourne l'OptionCline de nom long donne, ou None (appartenance au
    registre : aucune option hors grammaire n'est acceptee)."""
    for opt in GRAMMAIRE_CLINE:
        if opt.long == nom_long:
            return opt
    return None


def options_obligatoires() -> Tuple[OptionCline, ...]:
    """Options formellement obligatoires (actuellement aucune : le prompt nu
    est valide). Present pour la completude deontique du validateur."""
    return tuple(o for o in GRAMMAIRE_CLINE if o.obligatoire)


def index_par_court() -> Dict[str, str]:
    """Table courte -> longue, pour resoudre les alias d'emission."""
    table: Dict[str, str] = {}
    for opt in GRAMMAIRE_CLINE:
        if opt.court:
            table[opt.court] = opt.long
    return table
