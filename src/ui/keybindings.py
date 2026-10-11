"""Keybindings & historique persistant pour Gabriel CLI.

Active les raccourcis clavier interactifs (fleches haut/bas, Ctrl+R, Tab...)
via le module `readline` (standard Python sur Linux/macOS, disponible via
`pyreadline3` sur Windows).

Aucune nouvelle dependance n'est requise puisque Gabriel tourne dans Docker
(Linux) ou dans WSL.

Fonctionnalites :
  - Historique persistant entre sessions  (data/.gabriel_history)
  - Navigation dans l'historique          (Up/Down)
  - Recherche inversee                    (Ctrl+R)
  - Auto-completion des commandes         (Tab)
  - Edition de ligne emacs                (Ctrl+A/E/W/U/L/K/Y...)
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable, Optional

logger = logging.getLogger(__name__)

# Tentative d'import readline. Si indisponible, on retourne silencieusement.
try:
    import readline
    _READLINE_AVAILABLE = True
except ImportError:
    _READLINE_AVAILABLE = False
    readline = None  # type: ignore


# Liste canonique des commandes Gabriel pour auto-completion (Tab).
# Synchronise avec HELP_TEXT dans cli.py. L'ordre importe pour le matching prefix.
DEFAULT_COMMANDS = (
    # Generaux
    "aide", "commandes", "version", "contexte", "memoire", "quitter",
    "splash", "about", "banner", "citation", "citations", "cite",
    # Ask Gabriel (aide contextuelle)
    "ask", "ask type", "ask rules",
    # Corpus & primes
    "corpus", "corpus detail", "primes", "prime ",
    # Calculs deterministes
    "gap ", "rsp ", "rsp-test ", "rsp-courbe ",
    # Visualisations
    "courbe SA ", "courbe SB ", "courbe SA_SB ", "courbe digamma ",
    "courbe invariant ", "courbe ratio ", "courbe gap ", "courbe prime ",
    # Validation
    "verifier ", "valider ",
    # Audit
    "historique", "audit ", "citer ",
    # Debugger
    "debug ",
    # Tests CI
    "ci", "tests", "pytest",
)


class GabrielKeybindings:
    """Configure readline pour Gabriel : historique persistant + Tab completion."""

    def __init__(
        self,
        history_file: Path | str = "data/.gabriel_history",
        commands: Iterable[str] = DEFAULT_COMMANDS,
        history_size: int = 1000,
    ) -> None:
        self.history_file = Path(history_file)
        self.commands = sorted(set(commands))
        self.history_size = history_size
        self._installed = False

    def install(self) -> bool:
        """Installe readline (historique + completer). Retourne True si OK."""
        if not _READLINE_AVAILABLE:
            logger.warning("readline indisponible : pas de raccourcis clavier")
            return False
        if self._installed:
            return True

        # 1) Historique persistant
        self._load_history()
        readline.set_history_length(self.history_size)

        # 2) Auto-completion via Tab
        readline.set_completer(self._completer)
        # Sur Linux/macOS : libreadline (Tab par defaut)
        # Sur Windows (pyreadline3) : on doit forcer
        try:
            readline.parse_and_bind("tab: complete")
        except Exception:
            pass
        # Ne pas couper sur les caracteres speciaux dans les arguments
        readline.set_completer_delims(" \t\n")

        self._installed = True
        logger.info(
            f"Keybindings installes : historique={self.history_file}, "
            f"{len(self.commands)} commandes auto-completables"
        )
        return True

    def save_history(self) -> None:
        """Sauvegarde l'historique sur disque. Appeler avant quitter."""
        if not _READLINE_AVAILABLE or not self._installed:
            return
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            readline.write_history_file(str(self.history_file))
        except (IOError, OSError) as exc:
            logger.warning(f"Echec sauvegarde historique : {exc}")

    # ----------------------------------------------------------------------
    # Internes
    # ----------------------------------------------------------------------
    def _load_history(self) -> None:
        """Charge l'historique depuis le disque si present."""
        if not self.history_file.exists():
            return
        try:
            readline.read_history_file(str(self.history_file))
            logger.debug(f"Historique charge : {self.history_file}")
        except (IOError, OSError) as exc:
            logger.warning(f"Echec chargement historique : {exc}")

    def _completer(self, text: str, state: int) -> Optional[str]:
        """Completer readline : retourne les commandes dont le prefixe matche `text`."""
        # On regarde la ligne entiere pour gerer "courbe SA<TAB>"
        try:
            line = readline.get_line_buffer()
        except Exception:
            line = text
        # Si l'utilisateur est au debut de ligne -> propose les commandes
        # Sinon : ne propose rien (les arguments sont libres)
        line_l = line.lstrip().lower()
        text_l = text.lower()
        matches = [c for c in self.commands if c.lower().startswith(line_l or text_l)]
        # On enleve la partie deja tapee dans la ligne pour completer juste le suffixe
        # Mais readline gere ca via set_completer_delims. On retourne juste le match brut.
        if state < len(matches):
            return matches[state]
        return None


# Singleton convenience pour la CLI
_singleton: Optional[GabrielKeybindings] = None


def install_keybindings(
    history_file: Path | str = "data/.gabriel_history",
    commands: Iterable[str] = DEFAULT_COMMANDS,
) -> GabrielKeybindings:
    """Installe les keybindings Gabriel (singleton). Idempotent."""
    global _singleton
    if _singleton is None:
        _singleton = GabrielKeybindings(history_file=history_file, commands=commands)
        _singleton.install()
    return _singleton


def save_history() -> None:
    """Sauvegarde l'historique du singleton si installe."""
    if _singleton is not None:
        _singleton.save_history()


def is_available() -> bool:
    """Retourne True si readline est disponible (et donc les raccourcis actifs)."""
    return _READLINE_AVAILABLE
