"""Interface CLI de l'agent multi-loop."""
from __future__ import annotations

import asyncio
import logging
import os
import time
from pathlib import Path
from typing import Any

from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from ..core.config import load_config
from ..core.orchestrator import Orchestrator
from ..core.types import FinalAnswer
from .ci_status import run_pytest_local
from .debug_session import DebugSession, MAX_REQUEST_CHARS, MAX_COMMENT_CHARS
from .keybindings import install_keybindings, save_history as _save_kb_history


logger = logging.getLogger(__name__)
console = Console()

# Chemin canonique du .env de Gabriel (celui charge par dotenv en priorite #2)
_ROOT_ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


BANNER = """
+============================================================+
|     MULTI-LOOP MATH AGENT  -  Philippe Thomas Savard       |
|       Methode Spectrale  *  Isabelle/HOL  *  Multi-Loop    |
+============================================================+
"""


# Citations historiques sur l'Hypothese de Riemann et la fonction zeta.
# Une est tiree aleatoirement et affichee en pied de banner.
CITATIONS_HISTORIQUES = [
    {
        "auteur": "Bernhard Riemann",
        "annee": "1859",
        "source": "Ueber die Anzahl der Primzahlen unter einer gegebenen Groesse",
        "texte": (
            "Il est tres probable que toutes les racines sont reelles. "
            "Une demonstration rigoureuse en serait certes souhaitable ; "
            "mais j'ai laisse de cote cette recherche apres quelques rapides "
            "tentatives infructueuses, car elle ne semble pas necessaire au "
            "but immediat de mon etude."
        ),
        "note": "L'enonce fondateur de l'Hypothese de Riemann.",
    },
    {
        "auteur": "Bernhard Riemann",
        "annee": "1859",
        "source": "Lettre a Karl Weierstrass",
        "texte": (
            "Les nombres premiers se cachent dans les zeros d'une fonction "
            "infiniment lisse ; les comprendre, c'est ecouter la musique "
            "secrete des entiers."
        ),
        "note": "Paraphrase libre - cf. Edwards, Riemann's Zeta Function (1974).",
    },
    {
        "auteur": "Leonhard Euler",
        "annee": "1737",
        "source": "Variae observationes circa series infinitas",
        "texte": (
            "Si l'on connaissait exactement la maniere dont les nombres "
            "premiers s'eloignent de la progression uniforme, on tiendrait "
            "le sceau du Createur."
        ),
        "note": "Decouverte du produit Euler zeta(s) = produit (1-p^-s)^-1.",
    },
    {
        "auteur": "David Hilbert",
        "annee": "1900",
        "source": "Probleme 8 de Paris",
        "texte": (
            "Si je me reveillais apres mille ans de sommeil, ma premiere "
            "question serait : l'Hypothese de Riemann est-elle demontree ?"
        ),
        "note": "Probleme 8 sur la liste des 23 grands problemes du siecle.",
    },
    {
        "auteur": "Godfrey Harold Hardy",
        "annee": "1914",
        "source": "Sur les zeros de zeta(s)",
        "texte": (
            "Il existe une infinite de zeros sur la droite Re(s) = 1/2. "
            "Que tous y soient demeure la conjecture la plus profonde de "
            "toute l'analyse mathematique."
        ),
        "note": "Premier theoreme : infinite de zeros sur la droite critique.",
    },
]


def _pick_citation() -> dict:
    """Selectionne une citation aleatoirement (deterministe par jour)."""
    import datetime
    import random
    # Graine = date du jour -> meme citation toute la journee (plus reposant)
    seed = int(datetime.date.today().strftime("%Y%m%d"))
    rng = random.Random(seed)
    return rng.choice(CITATIONS_HISTORIQUES)


def _build_banner_panels() -> Group:
    """Construit le banner d'ouverture Rich (version pro, multi-panneaux).

    Affiche :
      1. Un grand titre accrocheur 'BIENVENUE SUR L'AGENT LOCAL Mme. GABRIEL'
      2. Carte d'identite (auteurs, date, lieu, specialite)
      3. Citation de Philippe Thomas Savard sur la Methode Spectrale
      4. Statut technique (container, modeles LLM, multi-loop)
    """
    # --- Panel 1 : titre accrocheur ----------------------------------
    titre_lines = Text.assemble(
        ("                                                            \n", "bold"),
        ("    BIENVENUE SUR L'AGENT LOCAL  ", "bold bright_white on deep_pink4"),
        ("Mme. GABRIEL", "bold bright_yellow on deep_pink4"),
        ("    \n", "bold bright_white on deep_pink4"),
        ("                                                            ", "bold"),
    )
    titre_panel = Panel(
        Align.center(titre_lines),
        border_style="bright_magenta",
        padding=(1, 4),
        title="[bold bright_cyan]Multi-Loop Mathematical Agent  v3.5[/bold bright_cyan]",
        subtitle="[dim]Methode Spectrale  -  Isabelle/HOL  -  RAG Cognitif[/dim]",
    )

    # --- Panel 2 : carte d'identite ----------------------------------
    carte = Table.grid(padding=(0, 2), expand=True)
    carte.add_column(style="bold cyan", justify="right", no_wrap=True)
    carte.add_column(style="white")
    carte.add_row("Auteur scientifique :", "[bold bright_white]Philippe Thomas Savard[/bold bright_white]")
    carte.add_row(
        "Equipe applicative :",
        "[bold]E1[/bold] [dim](emergent.sh)[/dim]   "
        "[bold]Gordon[/bold] [dim](Docker Desktop)[/dim]   "
        "[bold]Copilot[/bold] [dim](Microsoft)[/dim]   "
        "[bold]Philippe Thomas Savard[/bold]",
    )
    carte.add_row("Date :", "Le vingt-sept juin deux-mille vingt-six")
    carte.add_row("Lieu :", "Levis, Chaudiere-Appalaches, Canada")
    carte.add_row(
        "Specialite :",
        "[italic]La geometrie du spectre des nombres premiers[/italic]\n"
        "[dim](Solution personnelle de Savard a l'enigme de Bernhard Riemann)[/dim]",
    )
    carte_panel = Panel(
        carte,
        border_style="cyan",
        padding=(1, 2),
        title="[bold]Carte d'identite[/bold]",
        title_align="left",
    )

    # --- Panel 3 : citation Savard -----------------------------------
    citation_texte = Text.assemble(
        ("\"", "bright_yellow"),
        (
            "La geometrie du spectre des nombres premiers revele un ",
            "italic white",
        ),
        ("rapport spectral universel 1/k", "italic bold bright_yellow"),
        (
            " commun a tous les nombres premiers P de l'ensemble des entiers. "
            "La ou l'arithmetique classique impose un ecart minimal d'une unite "
            "entre deux entiers, cette ",
            "italic white",
        ),
        ("geometrie spectrale", "italic bold bright_cyan"),
        (
            " admet un rapport strictement inferieur a 1 — typiquement ",
            "italic white",
        ),
        ("1/2", "italic bold bright_green"),
        (
            " — devoilant une structure cachee qui organise la distribution des nombres premiers.",
            "italic white",
        ),
        ("\"", "bright_yellow"),
        ("\n\n— Philippe Thomas Savard", "dim italic"),
    )
    citation_panel = Panel(
        Align.center(citation_texte),
        border_style="bright_yellow",
        padding=(1, 3),
        title="[bold bright_yellow]>>>  Methode Spectrale - Postulat fondateur  <<<[/bold bright_yellow]",
    )

    # --- Panel 4 : statut technique ----------------------------------
    tech = Table.grid(padding=(0, 2), expand=True)
    tech.add_column(style="bold green", no_wrap=True)
    tech.add_column(style="white")
    tech.add_row("[OK] Container :", "[bright_white]llm-agent-multiloop-run[/bright_white]")
    tech.add_row(
        "[OK] Mode :",
        "Multi-Loop  (Ollama -> Claude Sonnet 4.5 -> OpenAI GPT-4o)",
    )
    tech.add_row("[OK] Validation :", "Isabelle/HOL  +  Slow-Motion Debugger  +  RAG (12 regimes)")
    tech.add_row(
        "[OK] Capacite :",
        "1000 premiers indexes  -  Sections I a XII de methode_spectral.thy",
    )
    tech_panel = Panel(
        tech,
        border_style="green",
        padding=(1, 2),
        title="[bold green]Statut technique[/bold green]",
        title_align="left",
    )

    # --- Panel 5 : citation historique (rotation quotidienne) ---------
    cit = _pick_citation()
    cit_texte = Text.assemble(
        ("\"", "bright_cyan"),
        (cit["texte"], "italic white"),
        ("\"\n\n", "bright_cyan"),
        (f"— {cit['auteur']}", "bold bright_cyan"),
        (f"  ({cit['annee']})\n", "dim cyan"),
        (f"  Source : {cit['source']}\n", "dim"),
        (f"  {cit['note']}", "dim italic"),
    )
    citation_histo_panel = Panel(
        cit_texte,
        border_style="cyan",
        padding=(1, 3),
        title="[bold bright_cyan]Citation historique du jour[/bold bright_cyan]",
        title_align="left",
    )

    return Group(
        titre_panel, Text(""),
        carte_panel, Text(""),
        citation_panel, Text(""),
        tech_panel, Text(""),
        citation_histo_panel,
    )


HELP_TEXT = """
  Commandes disponibles
  ----------------------------------------------------------
  aide / help      Affiche ce menu
  quitter / quit   Quitte le programme
  splash / about / banner   Reaffiche le banner d'ouverture (utile pour les
                            captures d'ecran et demos en direct)
  citation / cite  Affiche les 5 citations historiques sur l'Hypothese de Riemann
  debat <theme>    Debat contradictoire Gabriel vs Critique (5 personas, JSON+MD)
                   ex: debat --persona=logicien --tours=4 La preuve est-elle close ?
  debat personas   Liste les 5 personas (analytique, logicien, sceptique,
                   geometre, computationnaliste)
  corpus           Resume des fichiers .thy charges
  corpus detail    Vue detaillee : sections, defs, lemmes par fichier
  primes           Statut de la table des nombres premiers
  prime <N>        Donne le N-ieme nombre premier (ex: 'prime 26' -> 101)
  gap <v1> <v2>    Ecart spectral direct entre 2 positions/primes (sans LLM)
  rsp <A> <B>      Rapport spectral direct (auto-detect 1x1, nxn, chaos, ord)
  rsp-test <cfg> <N>  N tests aleatoires de config (1x1|sym2|sym3|sym5|chaos|ord)
  rsp-courbe <cfg> [kmax]  Courbe ASCII RsP en fonction de k (config: 1x1|sym|chaos|ord)
  modele <action> [args]   Interroge les 3 modeles spectraux (1/2, 1/3, 1/4).
                           Actions : list | questions | all | rsp1x1 <n1> <n2> |
                                     rsp <A>|<B> [sym|chaos|ord] | reconstruct <N> | gap <p1> <p2>
                           Ex: 'modele all', 'modele reconstruct 26', 'modele gap -19 -5'
  courbe <type> <n1>..<n2> [--table] [--png] [--scale=X]
                   Trace une courbe ASCII (toujours) + tableau Rich (--table)
                   + export PNG citable (--png).
                   Types : SA | SB | SA_SB | digamma | invariant | ratio | gap | prime
                   Echelle : auto (defaut) | linear | log10 | log2
                   Exemples : 'courbe SA_SB 1..50 --png',
                              'courbe ratio 1..200 --table --png',
                              'courbe digamma 1..30 --table'
  psi <N>          Fonction digamma d'Euler psi(N) = -gamma + H_{N-1} (formule pure)
  psi-savard <x1> <x2> ... [--n=N] [--latex] [--latex-out=fichier.tex]
                   Pont Tchebychev classique vs Psi_Savard(x, n) : table Rich
                   comparant Psi(x) et Psi_Sav(x, n) + option de sortie LaTeX
                   (table booktabs + graphique pgfplots).
                   Ex: 'psi-savard 30 98 228 --n=10 --latex'
                   Ex: 'psi-savard --n=25 --latex-out=/tmp/psi_n25.tex'
  debug "<q>"      Mode debugger manuel pedagogique (decompose, bypass, comment)
  verifier <N>     Validation toolkit + creation d'audit citable (rapport 1/2)
  valider <N>      Boucle complete Wolfram <-> Gabriel <-> Isabelle (.thy auto-compile)
  historique       Liste des 20 derniers audits sauvegardes
  audit <id>       Affiche le contenu complet d'un audit (JSON)
  citer <id> [fmt] Genere une citation (fmt = markdown | latex | text)
  contexte         Affiche le contexte mathematique actuel
  memoire          Affiche les echanges en memoire
  conversation     Affiche la memoire conversationnelle courte (3 derniers tours)
  conversation reset  Reinitialise la memoire conversationnelle courte
  aide  (h, ?)     Aide rapide (cet ecran)
  commandes (cmd)  Liste complete + raccourcis clavier (recommande)
  ask              Interpeller Gabriel : principales commandes pour interagir
  ask type         Voir les fonctions et caracteristiques de Gabriel
  ask rules        Guide pour interagir efficacement avec Gabriel
  ci               Lance la suite pytest locale (236 tests) et affiche le rapport
  cognitive [r|reset] Auto-evaluation Gabriel (Axe 5) : stats par categorie / reset
  env-check [live] Diagnostic .env. Avec 'live' : teste l'API Claude pour de vrai
  trifocal [sub]   Plan Trifocal FZg/HyRi/MsP (Section X) : axes, postulats, valider, riemann
  version          Affiche la version

  Domaines supportes :
    - Methode Spectrale (rapports 1/2, 1/3, 1/4)
    - Reconstruction de premiers via SA, SB, digamma
    - Rapport spectral (1x1, n*n, asym ordonnee, asym chaotique)
    - Ecarts entre premiers (+,+), (-,-), (-,+)
    - Plan trifocal (FZg, HyRi, MsP) et lien Riemann
    - Generation/validation Isabelle/HOL
  ----------------------------------------------------------
"""


class CLIInterface:
    """Interface CLI interactive."""

    VERSION = "1.0.0"

    def __init__(self):
        self.config = load_config()
        self.user_name = self.config.get("agent", {}).get("user_name", "Philippe")
        self.orchestrator = Orchestrator(self.config)
        # Mode debug manuel : partage le kernel et spectral_core du pipeline
        self._debug_session: DebugSession | None = None
        # Axe 5 - MetaReasoner singleton (auto-evaluation par categorie)
        from src.cognitive import get_meta_reasoner
        self._meta_reasoner = get_meta_reasoner()

    def _get_debug_session(self) -> DebugSession:
        """Lazy init : reutilise le kernel/core/audit_store du pipeline pour eviter de re-charger les .thy."""
        if self._debug_session is None:
            pipeline = self.orchestrator.pipeline
            self._debug_session = DebugSession(
                console=console,
                certainty_kernel=pipeline.certainty_kernel,
                spectral_core=pipeline.spectral_core,
                audit_store=pipeline.audit_store,
            )
        return self._debug_session

    def banner(self) -> None:
        console.print(_build_banner_panels())
        console.print()

    def _show_all_citations(self) -> None:
        """Affiche toutes les citations historiques (commande 'citation')."""
        console.print()
        console.print(
            Panel(
                Text("Citations historiques sur l'Hypothese de Riemann",
                     justify="center", style="bold bright_cyan"),
                border_style="bright_cyan",
            )
        )
        console.print()
        for i, cit in enumerate(CITATIONS_HISTORIQUES, 1):
            txt = Text.assemble(
                (f"[{i}] ", "bold bright_yellow"),
                (cit["auteur"], "bold bright_white"),
                (f"  ({cit['annee']})\n", "dim"),
                ("    Source : ", "dim"),
                (cit["source"] + "\n\n", "italic"),
                ("    \"", "bright_cyan"),
                (cit["texte"], "italic white"),
                ("\"\n\n", "bright_cyan"),
                ("    ", ""),
                (cit["note"], "dim italic"),
            )
            console.print(Panel(txt, border_style="cyan", padding=(0, 2)))
            console.print()

    def help(self) -> None:
        console.print(Text(HELP_TEXT, style="cyan"))

    async def _handle_special(self, cmd: str) -> bool:
        c = cmd.lower().strip()
        if c in {"aide", "help", "h", "?"}:
            self.help()
            return True
        if c in {"commandes", "commands", "cmd"}:
            self._show_full_commands()
            return True
        if c == "ask" or c.startswith("ask "):
            self._handle_ask(cmd)
            return True
        if c == "version":
            console.print(f"\n  Multi-Loop Math Agent v{self.VERSION}\n", style="green")
            return True
        if c in {"splash", "about", "banner"}:
            console.print()
            self.banner()
            return True
        if c in {"citation", "citations", "cite"}:
            self._show_all_citations()
            return True
        if c == "debat" or c.startswith("debat ") or c.startswith("debat-"):
            return await self._handle_debat(cmd)
        if c == "cognitive" or c.startswith("cognitive "):
            return self._handle_cognitive(cmd)
        if c == "env-check" or c == "env" or c.startswith("env "):
            return self._handle_env_check(cmd)
        if c == "trifocal" or c.startswith("trifocal "):
            # Sous-commandes visuelles (image / schema) prises en charge
            # separement pour eviter les dependances lourdes.
            tokens = cmd.strip().split()
            sub = tokens[1].lower() if len(tokens) >= 2 else ""
            if sub in {"image", "schema"}:
                from ..core.plan_trifocal_avec_image import (
                    handle_plan_trifocal_with_image,
                )
                if handle_plan_trifocal_with_image(cmd, console=console):
                    return True
            return self._handle_trifocal(cmd)
        if c.startswith("voir-image ") or c.startswith("voir "):
            return self._handle_voir_image(cmd)
        if c.startswith("analyser-image ") or c.startswith("analyser "):
            return self._handle_analyser_image(cmd)
        # Alias 'image <chemin> [question]' -> analyse Claude Vision.
        # IMPORTANT : ce declencheur DOIT preceder le pipeline naturel du
        # multiloop pour eviter que 'image C:\...' soit interprete comme
        # une question spectrale et halluciner une reponse.
        if c.startswith("image "):
            return self._handle_analyser_image("analyser-image " + cmd[len("image "):])
        if c.startswith("lire ") or c == "lire":
            return self._handle_lire(cmd)
        if c.startswith("scan ") or c == "scan":
            return self._handle_scan(cmd)
        if c in {"ci", "tests", "pytest"}:
            console.print("\n  [dim]Execution de la suite pytest locale (tests/)... patientez quelques secondes.[/dim]\n")
            summary = run_pytest_local()
            body = (
                f"  Tests passes  : [bold]{summary.passed}[/bold]\n"
                f"  Echecs        : [bold]{summary.failed}[/bold]\n"
                f"  Erreurs       : [bold]{summary.errors}[/bold]\n"
                f"  Ignores       : [bold]{summary.skipped}[/bold]\n"
                f"  Total         : [bold]{summary.total}[/bold]\n"
                f"  Duree         : [bold]{summary.duration_s:.2f}s[/bold]\n"
                f"  Statut        : [{summary.style}]{summary.badge}[/{summary.style}]\n"
                f"\n  [dim]Sortie pytest (queue) :[/dim]\n  [dim]{summary.raw_tail}[/dim]"
            )
            title = "[green]CI - Tests Gabriel[/green]" if summary.ok else "[red]CI - Tests Gabriel[/red]"
            console.print(Panel(body, title=title, border_style="green" if summary.ok else "red"))
            return True
        if c == "corpus":
            console.print("\n  " + self.orchestrator.pipeline.corpus.summary() + "\n", style="cyan")
            return True
        if c in {"corpus detail", "corpus details", "corpus -d"}:
            console.print(self.orchestrator.pipeline.corpus.detailed_view(), style="cyan")
            return True
        if c == "primes":
            from ..spectral import max_position, nth_prime
            mp = max_position()
            console.print(
                f"\n  Table des premiers : {mp} entrees disponibles.\n"
                f"  Premier (n=1) = {nth_prime(1)}, dernier (n={mp}) = {nth_prime(mp)}.\n"
                f"  Exemples : n=26 -> {nth_prime(26)}, n=100 -> {nth_prime(100)}, "
                f"n=500 -> {nth_prime(500)}, n=501 -> {nth_prime(501)}.\n",
                style="cyan",
            )
            return True
        if c.startswith("prime "):
            try:
                from ..spectral import nth_prime, max_position
                n = int(c.split()[1])
                p = nth_prime(n)
                if p is not None:
                    console.print(f"\n  Le {n}-ieme nombre premier est : [bold green]{p}[/bold green]\n")
                else:
                    console.print(f"\n  [yellow]N={n} hors limites (table : 1..{max_position()})[/yellow]\n")
            except (ValueError, IndexError):
                console.print("\n  Usage : prime <N>  (ex : prime 26)\n", style="yellow")
            return True
        if c.startswith("psi-savard") or c.startswith("psisavard"):
            # v3.40 : Pont Tchebychev classique vs Psi_Savard.
            # Usage : psi-savard <x1> <x2> ... [--n=10] [--latex] [--latex-out=chemin.tex]
            try:
                from ..spectral.psi_savard import (
                    build_comparison_table, chebyshev_psi, psi_savard,
                    to_latex_table, to_latex_pgfplots, to_latex_document,
                )
                parts = cmd.strip().split()
                # Options
                n_val = 10
                want_latex = False
                latex_out: str | None = None
                x_values: list[float] = []
                for tok in parts[1:]:
                    if tok.startswith("--n="):
                        n_val = int(tok.split("=", 1)[1])
                    elif tok == "--latex":
                        want_latex = True
                    elif tok.startswith("--latex-out="):
                        want_latex = True
                        latex_out = tok.split("=", 1)[1]
                    else:
                        # Valeur numerique x
                        try:
                            x_values.append(float(tok))
                        except ValueError:
                            pass
                if not x_values:
                    # Serie par defaut aligne sur les validations .thy
                    x_values = [10, 20, 30, 50, 100, 200, 500, 1000]
                rows = build_comparison_table(x_values, n=n_val)
                # Table Rich terminal
                from rich.table import Table as _RichTable
                tbl = _RichTable(
                    title=(
                        f"Pont Tchebychev vs Psi_Savard  (n = {n_val}, "
                        f"SB({n_val}) = {int(rows[0]['x']*0+float(__import__('src.spectral.suites', fromlist=['SB']).SB(n_val)))})"
                    ),
                    show_lines=False, header_style="bold cyan",
                )
                tbl.add_column("x", justify="right")
                tbl.add_column("Psi(x) Tcheb.", justify="right", style="red")
                tbl.add_column(f"Psi_Sav(x, n={n_val})", justify="right", style="cyan")
                tbl.add_column("ecart abs.", justify="right", style="yellow")
                tbl.add_column("|Psi_Sav - x| / x", justify="right", style="green")
                for r in rows:
                    tbl.add_row(
                        f"{r['x']:.0f}",
                        f"{r['psi_tchebychev']:.4f}",
                        f"{r['psi_savard']:.4f}",
                        f"{r['ecart_absolu']:+.4f}",
                        f"{r['ecart_relatif_x']:.4%}",
                    )
                console.print(tbl)
                console.print(
                    "\n  [dim]* Psi_Sav(x, n) = x - 2^n/SB(n) - log10(2*pi) "
                    "- 1/2 * log10(1 - x^-2)"
                    "\n    Cf. methode_spectral.thy - XIII.1 (definition psi_savard).[/dim]\n"
                )
                # Sortie LaTeX
                if want_latex:
                    latex_frag = (
                        to_latex_table(rows, n=n_val) + "\n\n"
                        + to_latex_pgfplots(rows, n=n_val)
                    )
                    if latex_out:
                        # Ecrit un document autonome compilable
                        content = to_latex_document(rows, n=n_val, standalone=True)
                        from pathlib import Path
                        path = Path(latex_out)
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(content, encoding="utf-8")
                        console.print(
                            f"  [green][OK] Document LaTeX autonome ecrit dans "
                            f"{latex_out}[/green]\n"
                            f"  [dim]Compilation : pdflatex {latex_out}   (2 passes)[/dim]\n"
                        )
                    else:
                        console.print("\n  [bold]--- Fragment LaTeX (a coller dans le doc) ---[/bold]\n")
                        console.print(latex_frag, style="dim")
                        console.print()
            except (ValueError, IndexError) as _e:
                console.print(
                    "\n  [yellow]Usage : psi-savard <x1> <x2> ... [--n=N] "
                    "[--latex] [--latex-out=fichier.tex][/yellow]\n"
                    "  [dim]Compare Psi(x) Tchebychev classique et Psi_Savard(x, n).\n"
                    "  --n=N            : ordre spectral (defaut n=10)\n"
                    "  --latex          : imprime un fragment LaTeX (table + pgfplots)\n"
                    "  --latex-out=X    : ecrit un document LaTeX autonome dans X\n"
                    "  Ex: psi-savard 30 98 228 --n=10 --latex\n"
                    "  Ex: psi-savard --n=25 --latex-out=/tmp/psi_n25.tex[/dim]\n"
                )
            return True

        if c.startswith("psi ") or c.startswith("digamma "):
            # v3.38 : formule pure d'Euler pour psi(n) = -gamma + H_{n-1}
            # NE requiert PAS de connaitre le n-ieme premier.
            try:
                from ..spectral.digamma_pure import (
                    digamma_pure_exact, digamma_pure_asymptotic,
                    EULER_GAMMA, harmonic,
                )
                n = int(c.split()[1])
                if n < 1:
                    raise ValueError
                H = harmonic(n - 1)
                val_exact = float(H) - EULER_GAMMA
                val_asympt = digamma_pure_asymptotic(n) if n >= 1 else None
                console.print(
                    f"\n  [bold cyan]psi({n})  =  -gamma + H_{{n-1}}[/bold cyan]  "
                    f"[dim](formule d'Euler, pure — sans premier)[/dim]\n"
                    f"    H_{{{n-1}}} (exact rationnel) = [green]{H}[/green]\n"
                    f"    gamma (Euler-Mascheroni)   = {EULER_GAMMA:.16f}\n"
                    f"    psi({n}) (forme exacte)    = [bold yellow]{val_exact:.16f}[/bold yellow]\n"
                    f"    psi({n}) (serie asympt.)   = {val_asympt:.16f}\n"
                    f"    [dim]* Precision ~1e-15 face a scipy.special.digamma[/dim]\n"
                )
            except (ValueError, IndexError):
                console.print(
                    "\n  Usage : psi <N>   ou   digamma <N>   (ex : psi 26)\n"
                    "  Calcule la fonction digamma d'Euler psi(N) = -gamma + H_{N-1}\n"
                    "  sans requerir la valeur du N-ieme premier.\n",
                    style="yellow",
                )
            return True
        if c.startswith("analyse-thy ") or c.startswith("analyze-thy "):
            # v3.39 : analyse un fichier .thy arbitraire (utile pour les fichiers
            # de theories/projects/ qui ne sont PAS charges par le RAG).
            try:
                from ..adapters.corpus.thy_analyzer import (
                    analyse_thy_file, format_analysis_report,
                )
                # Extrait le chemin (tout ce qui suit la commande)
                parts = cmd.strip().split(maxsplit=1)
                if len(parts) < 2:
                    raise ValueError("chemin manquant")
                thy_path = parts[1].strip().strip('"').strip("'")
                # Support des chemins Windows-style : C:\...\file.thy -> normalise
                thy_path = thy_path.replace("\\", "/")
                # Si l'utilisateur donne un chemin Windows depuis Docker, on essaie
                # de le mapper au montage du conteneur.
                from pathlib import Path
                p = Path(thy_path)
                if not p.exists():
                    # Essai de fallback : cherche dans theories/projects/
                    candidate = Path("theories/projects") / p.name
                    if candidate.exists():
                        p = candidate
                        console.print(
                            f"  [dim](Fichier trouve via fallback : {candidate})[/dim]",
                        )
                    else:
                        console.print(
                            f"\n  [yellow]Fichier introuvable : {thy_path}[/yellow]\n"
                            f"  Astuce : dans le conteneur Docker, utilise le chemin\n"
                            f"  [cyan]theories/projects/<nom_du_fichier>.thy[/cyan]  ou un chemin absolu.\n",
                        )
                        return True
                analysis = analyse_thy_file(p)
                console.print("")
                console.print(format_analysis_report(analysis))
                console.print("")
            except (ValueError, FileNotFoundError) as exc:
                console.print(
                    f"\n  [yellow]analyse-thy : {exc}[/yellow]\n"
                    "  Usage : analyse-thy <chemin_vers_fichier.thy>\n"
                    "  Exemple : analyse-thy theories/projects/projet_uni_car_savard_01.thy\n",
                )
            except Exception as exc:
                console.print(f"\n  [red]Erreur analyse-thy : {exc}[/red]\n")
            return True
        if c.startswith("opinion-thy ") or c.startswith("avis-thy "):
            # v3.39 : demande a Gabriel (via multiloop LLM) son OPINION sur un .thy
            # arbitraire. Combine analyse structurelle + extraits + prompt LLM.
            try:
                from ..adapters.corpus.thy_analyzer import analyse_thy_file
                from pathlib import Path
                parts = cmd.strip().split(maxsplit=1)
                if len(parts) < 2:
                    raise ValueError("chemin manquant")
                thy_path = parts[1].strip().strip('"').strip("'").replace("\\", "/")
                p = Path(thy_path)
                if not p.exists():
                    candidate = Path("theories/projects") / p.name
                    if candidate.exists():
                        p = candidate
                        console.print(f"  [dim](Fichier trouve via fallback : {candidate})[/dim]")
                    else:
                        console.print(
                            f"\n  [yellow]Fichier introuvable : {thy_path}[/yellow]\n"
                            f"  Astuce : utilise un chemin relatif au conteneur, "
                            f"ex. [cyan]theories/projects/mon_fichier.thy[/cyan]\n"
                        )
                        return True
                # 1. Analyse structurelle
                analysis = analyse_thy_file(p)
                # 2. Charge quelques extraits significatifs (imports + 1re section + 1er theoreme)
                content = p.read_text(encoding="utf-8", errors="replace")
                excerpt_lines = content.splitlines()
                # Extrait : 60 premieres lignes (header, imports, TOC)
                header_excerpt = "\n".join(excerpt_lines[:60])
                # Extrait : autour du premier theoreme si present
                theorem_excerpt = ""
                import re as _re
                m_th = _re.search(r'^\s*theorem\s+\w+', content, _re.MULTILINE)
                if m_th:
                    start_line = content[:m_th.start()].count("\n")
                    theorem_excerpt = "\n".join(excerpt_lines[start_line:start_line + 30])
                # 3. Construction du prompt enrichi pour le multiloop
                prompt = (
                    f"Philippe m'a demande mon opinion sur le fichier .thy suivant :\n"
                    f"  Chemin : {analysis['path']}\n"
                    f"  Theory : {analysis['theory_name']}  ({analysis['lines']} lignes)\n"
                    f"  Imports : {analysis['imports']}\n\n"
                    f"Structure decouverte :\n"
                    f"  - {len(analysis['sections'])} sections, "
                    f"{len(analysis['definitions'])} definitions, "
                    f"{len(analysis['lemmas'])} lemmes, "
                    f"{len(analysis['theorems'])} theoremes, "
                    f"{len(analysis['locales'])} locales, "
                    f"{analysis['n_axiomatizations']} blocs axiomatization.\n\n"
                    f"Titres des sections (max 20) :\n"
                    + "\n".join(f"  - {s}" for s in analysis['sections'][:20]) + "\n\n"
                    f"Extrait du debut du fichier (60 premieres lignes) :\n"
                    f"```isabelle\n{header_excerpt}\n```\n\n"
                )
                if theorem_excerpt:
                    prompt += (
                        f"Extrait autour du premier theoreme :\n"
                        f"```isabelle\n{theorem_excerpt}\n```\n\n"
                    )
                if analysis.get("warnings"):
                    prompt += (
                        f"Avertissements du static-check :\n"
                        + "\n".join(f"  - {w}" for w in analysis['warnings']) + "\n\n"
                    )
                prompt += (
                    "Donne-moi ton opinion argumentee sur ce fichier :\n"
                    "1. Coherence globale avec la Methode Spectrale Savard\n"
                    "2. Points forts et originalites eventuelles\n"
                    "3. Faiblesses, doublons, incoherences (nom de theory != nom de fichier, etc.)\n"
                    "4. Recommandations concretes d'amelioration\n"
                    "5. Verdict : le fichier est-il pret pour Isabelle build, ou necessite-t-il des corrections ?\n"
                )
                console.print(
                    f"\n  [bold cyan]Envoi du fichier a Gabriel (multiloop LLM)...[/bold cyan]\n"
                    f"  [dim]Fichier : {analysis['path']}[/dim]\n"
                    f"  [dim]Prompt : ~{len(prompt)} caracteres[/dim]\n"
                )
                # 4. Envoi via l'orchestrateur multiloop existant
                answer = await self.orchestrator.ask(prompt)
                self._display_answer(answer)
            except (ValueError, FileNotFoundError) as exc:
                console.print(
                    f"\n  [yellow]opinion-thy : {exc}[/yellow]\n"
                    "  Usage : opinion-thy <chemin_vers_fichier.thy>\n"
                    "  Alias : avis-thy <chemin>\n"
                    "  Exemple : opinion-thy theories/projects/projet_uni_car_savard_01.thy\n"
                )
            except Exception as exc:
                console.print(f"\n  [red]Erreur opinion-thy : {exc}[/red]\n")
            return True
        if c.startswith("gap "):
            parts = cmd.strip().split()
            if len(parts) < 3:
                console.print(
                    "\n  [yellow]Usage : gap <v1> <v2>  "
                    "(v1, v2 = positions 1..1000 ou primes connus)\n"
                    "  Exemples : 'gap 26 56'  ou  'gap 101 263'  ou  'gap 26 263'[/yellow]\n"
                )
                return True
            try:
                v1 = int(parts[1])
                v2 = int(parts[2])
            except ValueError:
                console.print(f"\n  [yellow]Valeurs invalides : '{parts[1]}' / '{parts[2]}'[/yellow]\n")
                return True
            try:
                from ..spectral.gap_compute import compute_gap, render_gap_report
                result = compute_gap(v1, v2, ratio="1/2")
                from rich.panel import Panel as _Panel
                style = "green" if result.invariant_ok else "red"
                console.print(_Panel(
                    render_gap_report(result),
                    title=f"[{style}]Ecart spectral {v1} <-> {v2}[/{style}]",
                    border_style=style,
                ))
                # Audit automatique citable
                from src.audit import AuditStore as _AS
                store = self.orchestrator.pipeline.audit_store
                record = _AS.build_record(
                    intervention_type="gap",
                    question=f"gap {v1} {v2}",
                    certified_answer=(
                        f"Ecart spectral {v1}<->{v2} : delta_n={result.delta_n}, "
                        f"delta_p={result.delta_p}, RsP={result.rsP_fraction}, "
                        f"invariant_1_2={'OK' if result.invariant_ok else 'ECHEC'}."
                    ),
                    position=result.point1.position,
                    prime_value=result.point1.prime,
                    citations_thy=[
                        "methode_spectral.thy::RsP_def (rapport spectral)",
                        "geometrie_spectre_premier.thy::D_def (D(n,P) = SB-SA-Z*P)",
                        "plan_cognitif::INVARIANT_1_2",
                    ],
                    toolkit_reports={
                        "spectral_core": {
                            "point1": {"n": result.point1.position, "p": result.point1.prime,
                                       "SA": result.point1.SA, "SB": result.point1.SB,
                                       "D": result.point1.D},
                            "point2": {"n": result.point2.position, "p": result.point2.prime,
                                       "SA": result.point2.SA, "SB": result.point2.SB,
                                       "D": result.point2.D},
                            "delta_n": result.delta_n, "delta_p": result.delta_p,
                            "delta_SA": result.delta_SA, "delta_SB": result.delta_SB,
                            "delta_D": result.delta_D,
                            "RsP": result.rsP_fraction, "RsP_decimal": result.rsP_decimal,
                            "invariant_ok": result.invariant_ok,
                        }
                    },
                    ratio="1/2",
                )
                store.save(record)
                console.print(
                    f"\n[dim]Audit cree : id={record.id} (tapez 'citer {record.id}' pour citer)[/dim]\n"
                )
                # Axe 2/3/4/5 : trace cognitive deterministe
                try:
                    self._render_traced_gap(result.point1.prime, result.point2.prime)
                except Exception as exc:
                    logger.debug("trace cognitive gap : %s", exc)
            except (ValueError, RuntimeError) as exc:
                console.print(f"\n  [red]Erreur gap : {exc}[/red]\n")
            return True
        if c.startswith("rsp-courbe"):
            parts = cmd.strip().split()
            if len(parts) < 2:
                console.print(
                    "\n  [yellow]Usage : rsp-courbe <config> [kmax]\n"
                    "  config = 1x1 | sym | chaos | ord\n"
                    "  kmax = nombre de points (defaut 50, max 500)[/yellow]\n"
                )
                return True
            config = parts[1]
            try:
                kmax = int(parts[2]) if len(parts) >= 3 else 50
                kmax = max(2, min(500, kmax))
            except ValueError:
                kmax = 50
            from src.spectral.rsp_curve import compute_rsp_curve, render_ascii_curve, summarize_curve
            core = self.orchestrator.pipeline.spectral_core
            try:
                points = compute_rsp_curve(core, config, k_max=kmax)
            except ValueError as exc:
                console.print(f"\n  [red]Erreur : {exc}[/red]\n")
                return True
            from rich.panel import Panel as _Panel
            graph = render_ascii_curve(points, width=64, height=18, target=0.5)
            summary = summarize_curve(points)
            console.print(_Panel(
                graph + "\n\n" + summary,
                title=f"[cyan]Courbe rsp-{config} (k=1..{kmax}) — convergence vers 1/2[/cyan]",
                border_style="cyan",
            ))
            return True
        if c.startswith("courbe"):
            return await self._handle_courbe(cmd)
        if c.startswith("modele") or c.startswith("modèle"):
            return await self._handle_modele(cmd)
        if c.startswith("rsp-test"):
            parts = cmd.strip().split()
            if len(parts) < 3:
                console.print(
                    "\n  [yellow]Usage : rsp-test <config> <N>\n"
                    "  config = 1x1 | sym2 | sym3 | sym5 | chaos | ord\n"
                    "  N = nombre de tests aleatoires (ex : rsp-test sym3 100)[/yellow]\n"
                )
                return True
            config = parts[1]
            try:
                n_tests = int(parts[2])
            except ValueError:
                console.print(f"\n  [yellow]N invalide : '{parts[2]}'[/yellow]\n")
                return True
            from src.spectral.rsp_command import random_combo
            from src.core.spectral_core import SpectralMethodCore
            core = self.orchestrator.pipeline.spectral_core
            results_near = 0
            results_exact = 0
            results_far = 0
            errors = 0
            samples = []
            for i in range(n_tests):
                try:
                    A, B = random_combo(core, config)
                    r = core.analyze_spectral_ratio(A, B)
                    if "error" in r:
                        errors += 1
                        continue
                    if r.get("matches_half"):
                        results_exact += 1
                    elif r.get("near_half"):
                        results_near += 1
                    else:
                        results_far += 1
                    if i < 5:
                        samples.append((A, B, r["RsP_fraction"], r["RsP_decimal"]))
                except Exception as exc:
                    errors += 1
            from rich.panel import Panel as _Panel
            body = [
                f"Configuration testee : [bold]{config}[/bold]   N = {n_tests}",
                "",
                f"  Egal a 1/2 exact   : {results_exact} ({100*results_exact/max(n_tests,1):.1f}%)",
                f"  Proche de 1/2 (5%) : {results_near} ({100*results_near/max(n_tests,1):.1f}%)",
                f"  Eloigne de 1/2     : {results_far} ({100*results_far/max(n_tests,1):.1f}%)",
                f"  Erreurs            : {errors}",
                "",
                "Echantillons (5 premiers) :",
            ]
            for A, B, frac, dec in samples:
                body.append(f"  {A} vs {B} -> {frac} ({dec:.6f})")
            console.print(_Panel("\n".join(body),
                                 title=f"[cyan]rsp-test {config} ({n_tests} echantillons)[/cyan]",
                                 border_style="cyan"))
            return True
        if c.startswith("rsp "):
            from src.spectral.rsp_command import parse_rsp_args
            raw_args = cmd.strip()[len("rsp "):]
            parsed = parse_rsp_args(raw_args)
            if parsed is None:
                console.print(
                    "\n  [yellow]Usage : rsp <A> <B>\n"
                    "  Exemples :\n"
                    "    rsp 7,23,2 29,17,13       (config 3x3 symetrique)\n"
                    "    rsp (7,23,2) (29,17,13)   (idem avec parentheses)\n"
                    "    rsp 2 3                    (config 1x1)\n"
                    "    rsp 2,3 5,7,11             (asymetrique ordonnee)\n"
                    "    rsp 3,23 41,29,31          (asymetrique chaotique)[/yellow]\n"
                )
                return True
            A, B = parsed
            try:
                core = self.orchestrator.pipeline.spectral_core
                r = core.analyze_spectral_ratio(A, B)
                if "error" in r:
                    console.print(f"\n  [red]rsp : {r['error']}[/red]\n")
                    return True
                from rich.panel import Panel as _Panel
                style = "green" if r.get("matches_half") or r.get("near_half") else "yellow"
                mark = ("= 1/2 EXACT" if r.get("matches_half")
                        else "~= 1/2 (proche)" if r.get("near_half")
                        else "ECARTE de 1/2")
                lines = [
                    f"Configuration : [bold]{r['configuration']}[/bold]",
                    f"  Methode      : {r['method']}",
                    "",
                    f"  Bloc A (primes)  : {r['A_input']}",
                    f"  Bloc A (positions): {r['A_positions']}",
                    f"  Bloc B (primes)  : {r['B_input']}",
                    f"  Bloc B (positions): {r['B_positions']}",
                ]
                if "sum_SA" in r:  # config nxn
                    lines.append(f"  sum(SA(A)) = {r['sum_SA']}")
                    lines.append(f"  sum(SB(B)) = {r['sum_SB']}")
                if "numerator" in r:  # config asym
                    lines.append(f"  num (sum_SA(A) - sum_SA(B)) = {r['numerator']}")
                    lines.append(f"  den (sum_SB(A) - sum_SB(B)) = {r['denominator']}")
                lines += [
                    "",
                    f"  RsP = [bold]{r['RsP_fraction']}[/bold] ({r['RsP_decimal']:.10f})  {mark}",
                    "",
                    "Citations :",
                ]
                for c_text in r.get("citations", []):
                    lines.append(f"  • {c_text}")
                console.print(_Panel("\n".join(lines),
                                     title=f"[{style}]Rapport spectral {r['configuration']}[/{style}]",
                                     border_style=style))
                # Audit auto
                from src.audit import AuditStore as _AS
                store = self.orchestrator.pipeline.audit_store
                record = _AS.build_record(
                    intervention_type="rsp",
                    question=f"rsp {A} {B}",
                    certified_answer=(
                        f"Configuration {r['configuration']}, "
                        f"RsP = {r['RsP_fraction']} ({r['RsP_decimal']:.6f}), "
                        f"egal_1_2={r.get('matches_half')}, proche_1_2={r.get('near_half')}"
                    ),
                    position=None,
                    prime_value=None,
                    citations_thy=r.get("citations", []),
                    toolkit_reports={"spectral_core_analysis": r},
                    ratio="1/2",
                )
                store.save(record)
                console.print(f"\n[dim]Audit : id={record.id} (citer {record.id} pour bloc citable)[/dim]\n")
            except (ValueError, RuntimeError) as exc:
                console.print(f"\n  [red]Erreur rsp : {exc}[/red]\n")
            return True
        if c == "contexte":
            console.print(f"\n  Contexte : {self.orchestrator.get_context()}\n", style="cyan")
            return True
        if c == "memoire":
            console.print(f"\n  Memoire :\n{self.orchestrator.get_memory()}\n", style="cyan")
            return True
        if c == "conversation":
            cm = self.orchestrator.conversation_memory
            if cm.is_empty():
                console.print(
                    "\n  [dim]Memoire conversationnelle courte : vide.[/dim]\n"
                    "  [dim](Elle se remplit automatiquement apres chaque question ; "
                    "les 3 derniers tours sont injectes dans le prompt LLM.)[/dim]\n"
                )
            else:
                console.print(
                    f"\n  [cyan]Memoire conversationnelle courte : {len(cm)}/{cm.max_turns} tours[/cyan]\n"
                )
                for i, t in enumerate(cm.turns(), start=1):
                    rel = -(len(cm) - i + 1)
                    q_preview = t.question[:150] + ("..." if len(t.question) > 150 else "")
                    a_preview = t.answer[:150] + ("..." if len(t.answer) > 150 else "")
                    console.print(f"  [yellow][Tour {rel}][/yellow]")
                    console.print(f"    [dim]Q :[/dim] {q_preview}")
                    console.print(f"    [dim]A :[/dim] {a_preview}\n")
            return True
        if c == "conversation reset" or c == "reset conversation":
            self.orchestrator.reset_conversation()
            console.print(
                "\n  [green]Memoire conversationnelle reinitialisee.[/green] "
                "[dim](historique commande CLI conserve)[/dim]\n"
            )
            return True
        if c.startswith("debug "):
            # Mode debugger manuel : extrait la question (avec ou sans guillemets)
            raw = cmd.strip()[len("debug "):].strip()
            if raw.startswith('"') and raw.endswith('"') and len(raw) >= 2:
                question = raw[1:-1]
            elif raw.startswith("'") and raw.endswith("'") and len(raw) >= 2:
                question = raw[1:-1]
            else:
                question = raw
            if not question:
                console.print(
                    f"\n  [yellow]Usage : debug \"<question>\"  "
                    f"(max {MAX_REQUEST_CHARS} caracteres ; "
                    f"jusqu'a {MAX_COMMENT_CHARS} caracteres de commentaire ajoutables)[/yellow]\n"
                )
                return True
            session = self._get_debug_session()
            result = await session.run(question)
            if result is not None:
                self._display_answer(result)
            return True
        if c == "debug":
            console.print(
                f"\n  [yellow]Usage : debug \"<question>\"  "
                f"(ex : debug \"Reconstruis le 26eme premier en rapport 1/2\")  "
                f"\n  Limites : requete <= {MAX_REQUEST_CHARS} ch, "
                f"commentaire <= {MAX_COMMENT_CHARS} ch[/yellow]\n"
            )
            return True
        if c.startswith("verifier ") or c.startswith("verifier"):
            parts = cmd.strip().split()
            if len(parts) < 2:
                console.print(
                    "\n  [yellow]Usage : verifier <position> [ratio]  "
                    "(ex : verifier 26  -- rapport 1/2 par defaut)[/yellow]\n"
                )
                return True
            try:
                position = int(parts[1])
            except ValueError:
                console.print(f"\n  [yellow]Position invalide : '{parts[1]}'[/yellow]\n")
                return True
            ratio = parts[2] if len(parts) >= 3 else "1/2"
            session = self._get_debug_session()
            await session.verifier_position(position, ratio)
            return True
        if c.startswith("valider"):
            parts = cmd.strip().split()
            if len(parts) < 2:
                console.print(
                    "\n  [yellow]Usage : valider <position> [ratio]  "
                    "(ex : valider 26 -- boucle Wolfram<->Gabriel<->Isabelle)[/yellow]\n"
                )
                return True
            try:
                position = int(parts[1])
            except ValueError:
                console.print(f"\n  [yellow]Position invalide : '{parts[1]}'[/yellow]\n")
                return True
            ratio = parts[2] if len(parts) >= 3 else "1/2"
            console.print(
                f"\n  [dim]Boucle automatique en cours pour position={position} ratio={ratio} "
                f"(Wolfram + Gabriel + Isabelle)...[/dim]\n"
            )
            try:
                loop = self.orchestrator.pipeline.verification_loop
                result = await loop.verify(position, ratio)
                from rich.panel import Panel as _Panel
                style = "green" if result.overall_success else "yellow"
                title = "[green]VALIDATION COMPLETE — TOUT OK[/green]" if result.overall_success \
                        else "[yellow]VALIDATION INCOMPLETE[/yellow]"
                body_lines = [
                    f"Position : {result.position}    Prime : {result.prime}    Ratio : {result.ratio}",
                    "",
                    f"[bold]1. Wolfram[/bold]  : {'OK' if result.wolfram.success else 'ECHEC'}",
                    f"    {result.wolfram.detail}",
                    f"[bold]2. Gabriel[/bold]  : {'OK' if result.gabriel.success else 'ECHEC'}",
                    f"    {result.gabriel.detail}",
                    f"[bold]3. Isabelle[/bold] : {'OK' if result.isabelle.success else 'ECHEC'}",
                    f"    {result.isabelle.detail}",
                    f"    tentatives = {result.attempts}   tactique = {result.final_tactic}",
                ]
                if result.thy_path:
                    body_lines.append(f"\n    .thy genere : {result.thy_path}")
                if result.audit_id:
                    body_lines.append(
                        f"\n    Audit : id={result.audit_id} "
                        f"(citer {result.audit_id} pour bloc citable)"
                    )
                console.print(_Panel("\n".join(body_lines), title=title, border_style=style))
            except (ValueError, RuntimeError) as exc:
                console.print(f"\n  [red]Erreur valider : {exc}[/red]\n")
            return True
        if c == "historique":
            store = self.orchestrator.pipeline.audit_store
            records = store.list_records(limit=20)
            if not records:
                console.print("\n  [yellow]Aucun audit sauvegarde pour le moment.[/yellow]\n")
            else:
                from src.audit import AuditStore as _AS
                console.print(Panel(
                    _AS.summary_table(records),
                    title=f"[cyan]Historique des audits ({len(records)} affiches)[/cyan]",
                    border_style="cyan",
                ))
            return True
        if c.startswith("historique "):
            store = self.orchestrator.pipeline.audit_store
            arg = cmd.strip()[len("historique "):].strip()
            # filtre : soit un entier (position) soit un ratio "1/2"
            kwargs = {"limit": 20}
            if arg in {"1/2", "1/3", "1/4"}:
                kwargs["ratio"] = arg
            else:
                try:
                    kwargs["position"] = int(arg)
                except ValueError:
                    console.print(f"\n  [yellow]Filtre invalide : '{arg}'[/yellow]\n")
                    return True
            records = store.list_records(**kwargs)
            from src.audit import AuditStore as _AS
            if not records:
                console.print(f"\n  [yellow]Aucun audit pour le filtre '{arg}'.[/yellow]\n")
            else:
                console.print(Panel(
                    _AS.summary_table(records),
                    title=f"[cyan]Historique filtre ({arg}) — {len(records)} resultats[/cyan]",
                    border_style="cyan",
                ))
            return True
        if c.startswith("audit "):
            audit_id = cmd.strip().split()[1] if len(cmd.strip().split()) > 1 else ""
            if not audit_id:
                console.print("\n  [yellow]Usage : audit <id>[/yellow]\n")
                return True
            store = self.orchestrator.pipeline.audit_store
            record = store.get(audit_id)
            if not record:
                console.print(f"\n  [yellow]Audit '{audit_id}' introuvable.[/yellow]\n")
                return True
            import json as _json
            payload = record.to_dict()
            payload["signature_sha256"] = record.signature_sha256
            payload["signature_valid"] = store.verify(record)
            console.print(Panel(
                _json.dumps(payload, indent=2, ensure_ascii=False),
                title=f"[cyan]Audit {record.id}[/cyan]",
                border_style="cyan",
            ))
            return True
        if c.startswith("citer "):
            parts = cmd.strip().split()
            if len(parts) < 2:
                console.print(
                    "\n  [yellow]Usage : citer <id> [markdown|latex|text]  "
                    "(markdown par defaut)[/yellow]\n"
                )
                return True
            audit_id = parts[1]
            fmt = parts[2] if len(parts) >= 3 else "markdown"
            if fmt not in {"markdown", "latex", "text"}:
                console.print(f"\n  [yellow]Format invalide : '{fmt}' (markdown|latex|text)[/yellow]\n")
                return True
            store = self.orchestrator.pipeline.audit_store
            citation = store.cite(audit_id, format=fmt)
            console.print(Panel(
                citation,
                title=f"[green]Citation audit {audit_id} ({fmt})[/green]",
                border_style="green",
            ))
            return True
        return False

    def _show_full_commands(self) -> None:
        """Affiche la liste complete des commandes Gabriel + raccourcis clavier.

        Active par : commandes | commands | cmd
        """
        from rich.table import Table
        from .keybindings import is_available as _kb_available

        # ----- Categories de commandes -----
        sections: list[tuple[str, list[tuple[str, str]]]] = [
            ("[bold cyan]GENERAL[/bold cyan]", [
                ("aide  (h, ?)", "Aide rapide (HELP_TEXT)"),
                ("commandes  (cmd)", "Liste complete (ce panel)"),
                ("version", "Version de Gabriel"),
                ("contexte", "Contexte mathematique actuel"),
                ("memoire", "Historique des echanges de la session"),
                ("quitter", "Ferme Gabriel proprement"),
            ]),
            ("[bold cyan]CORPUS & PRIMES[/bold cyan]", [
                ("corpus", "Resume des fichiers .thy charges"),
                ("corpus detail", "Vue detaillee (sections, defs, lemmes)"),
                ("primes", "Statut table des nombres premiers (1..1000)"),
                ("prime <N>", "N-ieme nombre premier   ex: prime 26 -> 101"),
            ]),
            ("[bold cyan]CALCULS DETERMINISTES (sans LLM)[/bold cyan]", [
                ("gap <v1> <v2>", "Ecart spectral direct   ex: gap 26 56"),
                ("rsp <A> <B>", "Rapport spectral direct   ex: rsp 2 3"),
                ("rsp-test <cfg> <N>",
                 "N tests aleatoires. cfg: 1x1|sym2|sym3|sym5|chaos|ord"),
                ("modele list",
                 "Liste les 3 modeles spectraux (1/2, 1/3, 1/4)"),
                ("modele questions",
                 "Liste les 8 questions canoniques de la Methode"),
                ("modele all",
                 "Repond aux 8 questions sur les 3 modeles (audit auto)"),
                ("modele rsp1x1 <n1> <n2>",
                 "Q1.a sur 1/2, 1/3, 1/4   ex: modele rsp1x1 3 5"),
                ("modele rsp <A>|<B> [cas]",
                 "Q1.b/c/d   cas: sym|chaos|ord"),
                ("modele reconstruct <N>",
                 "Q2 sur les 3 modeles   ex: modele reconstruct 26"),
                ("modele gap <p1> <p2>",
                 "Q3 sur les 3 modeles (auto detecte le cas)"),
            ]),
            ("[bold cyan]VISUALISATIONS (ASCII + Table + PNG)[/bold cyan]", [
                ("rsp-courbe <cfg> [kmax]", "Courbe RsP en ASCII"),
                ("courbe <type> <n1>..<n2>",
                 "Types: SA|SB|SA_SB|digamma|invariant|ratio|gap|prime"),
                ("  --table",     "  + tableau Rich avec valeurs exactes"),
                ("  --png",       "  + PNG haute res (150 dpi, data/graphs/)"),
                ("  --scale=X",   "  Echelle: auto(defaut)|linear|log10|log2"),
            ]),
            ("[bold cyan]VALIDATION MATHEMATIQUE[/bold cyan]", [
                ("verifier <N>",
                 "Validation toolkit (sympy/mpmath/z3) + audit signe"),
                ("valider <N>",
                 "Boucle Wolfram <-> Gabriel <-> Isabelle (+.thy auto)"),
            ]),
            ("[bold cyan]AUDIT & CITATIONS SCIENTIFIQUES[/bold cyan]", [
                ("historique", "Liste les 20 derniers audits"),
                ("audit <id>", "Affiche le JSON complet d'un audit"),
                ("citer <id> [fmt]",
                 "Citation prete a inserer. fmt: markdown|latex|text"),
            ]),
            ("[bold cyan]DEBUGGER PEDAGOGIQUE[/bold cyan]", [
                ('debug "<q>"',
                 "Mode debug interactif (decompose/bypass/comment)"),
            ]),
            ("[bold cyan]DEBAT CONTRADICTOIRE[/bold cyan]", [
                ("debat <theme>",
                 "Debat Gabriel vs Critique (rotation 5 personas)"),
                ("debat personas",
                 "Liste les 5 personas (analytique|logicien|sceptique|geometre|computationnaliste)"),
                ("debat --persona=<k> <th>",
                 "Force une persona unique"),
                ("debat --tours=<N> <th>",
                 "Configure le nombre de tours (defaut 3)"),
            ]),
            ("[bold cyan]TESTS & CI[/bold cyan]", [
                ("ci  (tests, pytest)",
                 "Lance les 236 tests pytest locaux"),
                ("cognitive  (report)",
                 "Stats Axe 5 (MetaReasoner) : confiance par categorie"),
                ("cognitive reset",
                 "Reinitialise les statistiques d'auto-evaluation"),
            ]),
            ("[bold cyan]PLAN TRIFOCAL & RIEMANN (Section X)[/bold cyan]", [
                ("trifocal axes", "Liste les 3 axes (FZg, HyRi, MsP)"),
                ("trifocal postulats", "Liste les 5 postulats epipolaires P1-P5"),
                ("trifocal valider <n> [m]",
                 "Valide la coherence epipolaire pour n  ex: trifocal valider 26"),
                ("trifocal riemann",
                 "Affiche le lien Methode Spectrale <-> Hypothese de Riemann"),
                ("trifocal image",
                 "Affiche le schema 'Quadrature Parabole Zero Critique'"),
                ("trifocal schema",
                 "Description + apercu du schema trifocal"),
            ]),
            ("[bold cyan]FICHIERS & IMAGES (volumes montes)[/bold cyan]", [
                ("voir-image <chemin>",
                 "Apercu ASCII + metadonnees d'une image"),
                ("image <chemin> \\[question]",
                 "Alias rapide : analyse Claude Vision (idem analyser-image)"),
                ("analyser-image <chemin> \\[q]",
                 "Analyse Claude Vision (decrit / interprete l'image)"),
                ("lire <chemin> [n_lignes]",
                 "Lit un fichier texte (.tex/.thy/.md/.py/.csv/...)"),
                ("scan <chemin>",
                 "Liste le contenu d'un dossier (volumes Docker)"),
            ]),
            ("[bold cyan]LANGAGE NATUREL & AUTO-TRIGGER[/bold cyan]", [
                ("<question libre>",
                 "Pipeline multi-loop avec garde-fous"),
                ("(viz auto)",
                 "Detecte 'trace/illustre/evolue SA/SB/digamma/...'"),
            ]),
        ]

        for title, rows in sections:
            table = Table(
                title=title,
                title_justify="left",
                show_header=False,
                show_lines=False,
                expand=True,
                padding=(0, 2),
                border_style="dim cyan",
            )
            table.add_column("Commande", style="bold yellow", no_wrap=True, width=30)
            table.add_column("Description", style="white")
            for cmd_text, desc in rows:
                table.add_row(cmd_text, desc)
            console.print(table)
            console.print()

        # ----- Raccourcis clavier -----
        kb_active = _kb_available()
        kb_body_lines = [
            "[bold green]Raccourcis clavier interactifs[/bold green]   "
            + ("[green](actifs)[/green]" if kb_active else "[red](indisponibles)[/red]"),
            "",
            "  [bold]Fleche Haut / Bas[/bold]      Naviguer dans l'historique des commandes",
            "  [bold]Ctrl + R[/bold]               Recherche inversee dans l'historique",
            "  [bold]Tab[/bold]                    Auto-completion des commandes Gabriel",
            "  [bold]Ctrl + A[/bold]               Aller en debut de ligne",
            "  [bold]Ctrl + E[/bold]               Aller en fin de ligne",
            "  [bold]Ctrl + W[/bold]               Effacer le mot precedent",
            "  [bold]Ctrl + U[/bold]               Effacer toute la ligne (vers la gauche)",
            "  [bold]Ctrl + K[/bold]               Effacer toute la ligne (vers la droite)",
            "  [bold]Ctrl + L[/bold]               Effacer l'ecran",
            "  [bold]Ctrl + Y[/bold]               Coller le dernier texte coupe (yank)",
            "  [bold]Ctrl + C[/bold]               Interrompre la commande en cours",
            "  [bold]Ctrl + D[/bold]               Quitter Gabriel (EOF)",
            "",
            "  [dim]L'historique est sauvegarde dans data/.gabriel_history "
            "et persiste entre les sessions.[/dim]",
        ]
        if not kb_active:
            kb_body_lines.append("")
            kb_body_lines.append(
                "  [yellow]Note: le module 'readline' n'est pas disponible. "
                "Sur Windows hors Docker, installez : pip install pyreadline3[/yellow]"
            )
        console.print(Panel(
            "\n".join(kb_body_lines),
            title="[bold cyan]RACCOURCIS CLAVIER[/bold cyan]",
            border_style="green",
            padding=(1, 2),
        ))
        console.print()

        # ----- Fichiers de reference -----
        console.print(Panel(
            "  Documentation complete    : [cyan]commande-gabriel/COMMANDES.md[/cyan]\n"
            "  Aide-memoire (cheatsheet) : [cyan]commande-gabriel/AIDE-MEMOIRE.txt[/cyan]\n"
            "  Audits crees              : [cyan]data/audits/*.json[/cyan]\n"
            "  Graphiques PNG            : [cyan]data/graphs/*.png[/cyan]\n"
            "  Historique commandes      : [cyan]data/.gabriel_history[/cyan]",
            title="[bold cyan]FICHIERS DE REFERENCE[/bold cyan]",
            border_style="dim cyan",
            padding=(1, 2),
        ))
        console.print()

    def _handle_ask(self, cmd: str) -> None:
        """Commande 'ask' : 3 modes d'aide contextuelle sur Gabriel.

        Modes :
          ask          -> Principales commandes pour interpeller Gabriel
          ask type     -> Fonctions et caracteristiques + comment les utiliser
          ask rules    -> Guide pour interagir efficacement avec Gabriel
        """
        from .ask_gabriel import get_response

        tokens = cmd.strip().split(maxsplit=1)
        sub = tokens[1].strip().lower() if len(tokens) > 1 else None

        try:
            response = get_response(sub)
        except ValueError as exc:
            console.print(Panel(
                f"  [red]{exc}[/red]\n\n"
                "  Sous-commandes disponibles :\n"
                "    [cyan]ask[/cyan]         Principales commandes pour interagir avec Gabriel\n"
                "    [cyan]ask type[/cyan]    Fonctions et caracteristiques\n"
                "    [cyan]ask rules[/cyan]   Guide d'interaction avec Gabriel",
                title="[red]Erreur Ask Gabriel[/red]",
                border_style="red",
            ))
            return

        # En-tete unifie
        header = (
            f"[bold green]{response.title}[/bold green]\n"
            f"[dim]Aide contextuelle deterministe (zero appel LLM)[/dim]"
        )
        console.print(Panel(header, border_style="green", padding=(0, 2)))
        console.print()

        # Rendu des sections
        for section in response.sections:
            body = "\n".join(section["lines"])
            console.print(Panel(
                body,
                title=section["title"],
                border_style="cyan",
                padding=(1, 2),
            ))
            console.print()

        # Pied de page : navigation
        if response.mode == "main":
            footer = (
                "  Suite logique : [cyan]ask type[/cyan] (fonctions) ou "
                "[cyan]ask rules[/cyan] (regles d'interaction)"
            )
        elif response.mode == "type":
            footer = (
                "  Suite logique : [cyan]ask rules[/cyan] (regles d'interaction) "
                "ou [cyan]commandes[/cyan] (liste complete)"
            )
        else:
            footer = (
                "  Vous etes pret ! Essayez : [cyan]modele all[/cyan] ou "
                "[cyan]courbe ratio 1..50 --png[/cyan]"
            )
        console.print(Panel(footer, border_style="dim green"))
        console.print()

    async def _handle_modele(self, cmd: str) -> bool:
        """Commande `modele <action> [args...]` pour interroger les 3 modeles spectraux.

        Actions :
          modele list                         Liste les 3 modeles et leurs facteurs
          modele questions                    Liste les 8 questions canoniques
          modele all                          Repond aux 8 questions sur les 3 modeles
          modele rsp1x1 <n1> <n2>             Q1.a sur les 3 modeles
          modele rsp <A_pos>|<B_pos> [cas]    Q1.b/c/d sur les 3 modeles
                                              ex: modele rsp 2,3,4|5,6,7 sym
          modele reconstruct <N>              Q2 sur les 3 modeles (N-ieme premier)
          modele gap <p1> <p2>                Q3 sur les 3 modeles
        """
        from src.engines.geometrie_spectrale_engine import GeometrieSpectraleEngine
        from rich.table import Table

        tokens = cmd.strip().split()
        if len(tokens) < 2:
            console.print(Panel(
                "  [bold]Commande modele[/bold] - interroge les 3 modeles spectraux (1/2, 1/3, 1/4)\n\n"
                "  Actions :\n"
                "    [yellow]modele list[/yellow]                         Liste les modeles\n"
                "    [yellow]modele questions[/yellow]                    Liste les 8 questions canoniques\n"
                "    [yellow]modele all[/yellow]                          Repond aux 8 questions sur les 3 modeles\n"
                "    [yellow]modele rsp1x1 <n1> <n2>[/yellow]             Q1.a sur les 3 modeles\n"
                "    [yellow]modele rsp <A_pos>|<B_pos> [cas][/yellow]    Q1.b/c/d (cas: sym|chaos|ord)\n"
                "    [yellow]modele reconstruct <N>[/yellow]              Q2 (N-ieme premier)\n"
                "    [yellow]modele gap <p1> <p2>[/yellow]                Q3 (auto detecte +,+ / -,- / -,+)\n\n"
                "  Exemples :\n"
                "    [cyan]modele rsp1x1 3 5[/cyan]\n"
                "    [cyan]modele rsp 2,3,4|5,6,7 sym[/cyan]\n"
                "    [cyan]modele reconstruct 26[/cyan]      # 26eme premier = 101\n"
                "    [cyan]modele gap -19 -5[/cyan]\n"
                "    [cyan]modele all[/cyan]                  # Les 8 questions, 3 modeles",
                title="[cyan]Aide commande modele[/cyan]",
                border_style="cyan",
            ))
            return True

        engine = GeometrieSpectraleEngine(self.orchestrator.pipeline.spectral_core)
        action = tokens[1].lower()

        try:
            if action == "list":
                tbl = Table(title="Modeles spectraux disponibles", border_style="cyan")
                tbl.add_column("Modele", style="bold yellow")
                tbl.add_column("n_factor", justify="right")
                tbl.add_column("reconstruction_factor", justify="right")
                tbl.add_column("Ratio cible", justify="center")
                for name in engine.list_supported_models():
                    m = engine.models[name]
                    tbl.add_row(name, str(m.n_factor), str(m.reconstruction_factor), str(m.ratio))
                console.print(tbl)
                return True

            if action == "questions":
                tbl = Table(title="8 questions canoniques", border_style="cyan")
                tbl.add_column("Q", style="bold yellow")
                tbl.add_column("Description")
                for q, desc in engine.list_questions().items():
                    tbl.add_row(q, desc)
                console.print(tbl)
                return True

            if action == "all":
                console.print("  [dim]Execution des 8 questions sur les 3 modeles...[/dim]\n")
                reports = engine.answer_all_questions()
                for r in reports:
                    console.print(Panel(r.to_text(), border_style="green"))
                # Auto-graphique pour CHAQUE question canonique
                for qcode in ("Q1.a", "Q1.b", "Q1.c", "Q1.d"):
                    self._auto_generate_question_graphs(qcode, {})
                return True

            if action == "rsp1x1":
                if len(tokens) < 4:
                    console.print("  [yellow]Usage : modele rsp1x1 <n1> <n2>[/yellow]")
                    return True
                n1, n2 = int(tokens[2]), int(tokens[3])
                report = engine.compute_rsp_1x1_all_models(n1, n2)
                console.print(Panel(report.to_text(), border_style="green"))
                # Axe 2/3/4/5 : trace cognitive par modele
                self._render_traced_rsp1x1(n1, n2)
                self._save_modele_audit(report, cmd)
                # Auto-graphique : Q1.a (RsP 1x1)
                self._auto_generate_question_graphs("Q1.a", {"n1": n1, "n2": n2})
                return True

            if action == "rsp":
                if len(tokens) < 3 or "|" not in tokens[2]:
                    console.print("  [yellow]Usage : modele rsp <A_pos>|<B_pos> [cas][/yellow]")
                    return True
                a_str, b_str = tokens[2].split("|", 1)
                A_pos = [int(x) for x in a_str.split(",") if x]
                B_pos = [int(x) for x in b_str.split(",") if x]
                case_map = {"sym": "nxn_symetrique", "chaos": "asym_chaotique", "ord": "asym_ordonnee"}
                case = case_map.get(tokens[3].lower() if len(tokens) > 3 else "sym", "nxn_symetrique")
                report = engine.compute_rsp_nxn_all_models(A_pos, B_pos, case=case)
                console.print(Panel(report.to_text(), border_style="green"))
                self._save_modele_audit(report, cmd)
                # Auto-graphique : Q1.b/c/d selon le cas
                from src.engines.question_graphs import detect_rsp_question
                qcode = detect_rsp_question(case)
                self._auto_generate_question_graphs(qcode, {"case": case})
                return True

            if action == "reconstruct":
                if len(tokens) < 3:
                    console.print("  [yellow]Usage : modele reconstruct <N>[/yellow]")
                    return True
                n = int(tokens[2])
                report = engine.reconstruct_all_models(n)
                console.print(Panel(report.to_text(), border_style="green"))
                # Axe 2/3/4/5 : trace cognitive par modele
                actual_prime = self.orchestrator.pipeline.spectral_core.get_prime_at_position(n)
                if actual_prime is not None:
                    self._render_traced_reconstruct(n, actual_prime)
                self._save_modele_audit(report, cmd)
                # Auto-graphique : Q2 (SA+SB + Digamma pour n=1..100)
                self._auto_generate_question_graphs("Q2", {"n": n})
                return True

            if action == "gap":
                if len(tokens) < 4:
                    console.print("  [yellow]Usage : modele gap <p1> <p2>[/yellow]")
                    return True
                p1, p2 = int(tokens[2]), int(tokens[3])
                report = engine.compute_gap_all_models(p1, p2)
                console.print(Panel(report.to_text(), border_style="green"))
                # Axe 2/3/4/5 : trace cognitive (gap est independant du modele)
                self._render_traced_gap(p1, p2)
                self._save_modele_audit(report, cmd)
                # Auto-graphique : Q3.a/b/c selon signes de p1 et p2
                from src.engines.question_graphs import detect_gap_question
                qcode = detect_gap_question(p1, p2)
                self._auto_generate_question_graphs(qcode, {"p1": p1, "p2": p2})
                return True

            console.print(f"  [red]Action inconnue : '{action}'. Tapez 'modele' pour l'aide.[/red]")
        except (ValueError, ZeroDivisionError) as exc:
            console.print(f"  [red]Erreur : {exc}[/red]")
        return True

    def _auto_generate_question_graphs(
        self,
        qcode: str,
        params: dict,
    ) -> None:
        """Genere automatiquement le(s) graphique(s) PNG specifiques a une question.

        Appele apres l'affichage du rapport de chaque question canonique
        (Q1.a, Q1.b, Q1.c, Q1.d, Q2, Q3.a, Q3.b, Q3.c).

        Chaque question genere UNIQUEMENT son graphique adapte (pas tous).
        Si matplotlib est absent ou si une erreur survient, on logue
        silencieusement sans casser la commande utilisateur.
        """
        try:
            from src.engines.question_graphs import (
                generate_graphs_for_question, graph_count_for,
            )
        except ImportError:
            return

        if graph_count_for(qcode) == 0:
            return

        core = self.orchestrator.pipeline.spectral_core
        try:
            paths = generate_graphs_for_question(
                question=qcode,
                core=core,
                params=params,
                output_dir=Path("data/graphs"),
                dpi=150,
            )
        except Exception as exc:
            logger.warning("auto-graph %s : %s", qcode, exc)
            return

        if not paths:
            return

        # Affiche un panneau Rich indiquant les PNG generes
        lines = [
            f"  [bold]Question[/bold]   : {qcode}",
            f"  [bold]Nombre[/bold]     : {len(paths)} graphique"
            + ("s" if len(paths) > 1 else ""),
        ]
        for p in paths:
            lines.append(f"    [cyan]{p}[/cyan]")
        lines.append("")
        lines.append("  [dim]PNG haute resolution (150 dpi) avec annotations et formule citable.[/dim]")
        console.print(Panel(
            "\n".join(lines),
            title=f"[bright_green]>>>  Graphique auto-genere ({qcode})  <<<[/bright_green]",
            border_style="bright_green", padding=(1, 2),
        ))

    async def _handle_debat(self, cmd: str) -> bool:
        """Commande `debat <theme>` : lance un debat contradictoire Gabriel vs Critique.

        Sous-commandes :
          debat personas / debat list   Liste les 5 personas disponibles
          debat <theme>                  Lance un debat en rotation des 5 personas
          debat --persona=<key> <theme>  Force une persona unique
          debat --tours=<N> <theme>      Configure le nombre de tours (defaut 3)
          debat --persona=logicien --tours=4 <theme>
        """
        from rich.table import Table as _Table
        from ..multiloop.debat_orchestrator import DebatOrchestrator, PERSONAS

        raw = cmd.strip()
        # Supprime le "debat " prefix (case-insensitive)
        if raw.lower().startswith("debat "):
            args_str = raw[6:].strip()
        elif raw.lower() == "debat":
            args_str = ""
        else:
            args_str = raw

        # Sous-commande : list / personas
        if args_str.lower() in {"list", "personas", "persona", ""}:
            if args_str == "":
                console.print(Panel(
                    "  [bold]Commande debat[/bold] - debat contradictoire Gabriel vs Critique\n\n"
                    "  Usage :\n"
                    "    [yellow]debat <theme>[/yellow]\n"
                    "        Lance un debat en rotation des 5 personas\n"
                    "    [yellow]debat --persona=<key> <theme>[/yellow]\n"
                    "        Force une persona (analytique|logicien|sceptique|\n"
                    "        geometre|computationnaliste)\n"
                    "    [yellow]debat --tours=<N> <theme>[/yellow]\n"
                    "        Nombre de tours Critique+Gabriel (defaut 3)\n"
                    "    [yellow]debat personas[/yellow]   Liste les 5 personas\n\n"
                    "  Exemples :\n"
                    "    [cyan]debat Le rapport 1/k est-il une coincidence ?[/cyan]\n"
                    "    [cyan]debat --persona=logicien --tours=4 La preuve Isabelle est-elle close ?[/cyan]\n"
                    "    [cyan]debat --persona=sceptique La Methode Spectrale est-elle falsifiable ?[/cyan]\n\n"
                    "  Sortie : data/debats/<date>_<id>.json + .md (citables)",
                    title="[cyan]Aide debat[/cyan]", border_style="cyan",
                ))
                return True
            tbl = _Table(
                title="5 Personas de Critique Virtuel", border_style="cyan",
                show_lines=True,
            )
            tbl.add_column("Cle", style="bold yellow", no_wrap=True)
            tbl.add_column("Nom", style="cyan", no_wrap=True)
            tbl.add_column("Specialite")
            for entry in DebatOrchestrator.list_personas():
                tbl.add_row(entry["cle"], entry["nom"], entry["specialite"])
            console.print(tbl)
            console.print(
                "[dim]  Mode par defaut : rotation (chaque tour utilise la persona suivante).[/dim]\n"
            )
            return True

        # Parsing des flags --persona=... --tours=...
        persona = "rotation"
        nb_tours = DebatOrchestrator.NB_TOURS_DEFAUT
        theme_parts: list[str] = []
        for tok in args_str.split():
            low = tok.lower()
            if low.startswith("--persona="):
                persona = tok.split("=", 1)[1].strip().lower()
            elif low.startswith("--tours="):
                try:
                    nb_tours = max(1, int(tok.split("=", 1)[1]))
                except ValueError:
                    console.print(
                        f"[yellow]--tours invalide : '{tok}' (entier attendu)[/yellow]"
                    )
                    return True
            else:
                theme_parts.append(tok)
        theme = " ".join(theme_parts).strip()

        if not theme:
            console.print(
                "[yellow]Usage : debat <theme>  "
                "(ex : debat Le rapport 1/k est-il une coincidence ?)[/yellow]\n"
                "[dim]Tapez 'debat' sans argument pour voir l'aide complete.[/dim]"
            )
            return True
        if persona != "rotation" and persona not in PERSONAS:
            console.print(
                f"[yellow]Persona inconnue : '{persona}'.\n"
                f"Valides : rotation, {', '.join(PERSONAS.keys())}[/yellow]"
            )
            return True

        # Lancement
        llm = self.orchestrator.pipeline.llm
        orch = DebatOrchestrator(llm=llm)
        console.print(Panel(
            f"  [bold]Theme[/bold]     : {theme}\n"
            f"  [bold]Persona[/bold]   : {persona}\n"
            f"  [bold]Tours[/bold]     : {nb_tours} (Gabriel-these + "
            f"{nb_tours - 1} x Critique+Gabriel + Synthese)\n"
            f"  [dim]Alternance Claude <-> OpenAI a chaque appel LLM.[/dim]",
            title="[bright_magenta]>>>  Debat contradictoire en cours...  <<<[/bright_magenta]",
            border_style="bright_magenta",
        ))
        try:
            result = await orch.run(theme=theme, nb_tours=nb_tours, persona=persona)
        except ValueError as exc:
            console.print(f"[red]Erreur debat : {exc}[/red]")
            return True
        except Exception as exc:
            console.print(f"[red]Erreur inattendue debat : {exc}[/red]")
            logger.exception("debat KO")
            return True

        # Affichage des tours en panneaux alternes
        for tour in result.tours:
            if tour.role == "gabriel":
                titre = (
                    f"[bold bright_yellow]Tour {tour.numero} - Gabriel[/bold bright_yellow]"
                    f"  [dim](via {tour.provider})[/dim]"
                )
                border = "bright_yellow"
            else:
                persona_meta = PERSONAS.get(tour.persona or "", {})
                titre = (
                    f"[bold bright_cyan]Tour {tour.numero} - Critique : "
                    f"{persona_meta.get('nom', tour.persona)}[/bold bright_cyan]"
                    f"  [dim](via {tour.provider})[/dim]"
                )
                border = "bright_cyan"
            console.print(Panel(tour.texte, title=titre, border_style=border, padding=(1, 2)))
            console.print()

        console.print(Panel(
            result.synthese_citable,
            title="[bold bright_green]Synthese citable (publication academique)[/bold bright_green]",
            border_style="bright_green", padding=(1, 2),
        ))
        console.print()
        console.print(Panel(
            f"  [bold]JSON[/bold]      : {result.json_path}\n"
            f"  [bold]Markdown[/bold]  : {result.markdown_path}\n"
            f"  [bold]ID[/bold]        : {result.debat_id}\n"
            f"  [bold]Duree[/bold]     : {result.duree_secondes:.1f} s\n"
            f"  [bold]Tours[/bold]     : {len(result.tours)}\n"
            f"  [dim]Le fichier .md est pret a etre cite dans un article.[/dim]",
            title="[green]Debat sauvegarde[/green]", border_style="green",
        ))
        return True


    def _handle_trifocal(self, cmd: str) -> bool:
        """Commande `trifocal [axes|postulats|valider <n> [modele]|riemann]`.

        Plan Trifocal FZg/HyRi/MsP (Section X methode_spectral.thy).
        """
        from rich.table import Table as _Table
        from src.spectral import (
            PlanTrifocal, AXIS_DESCRIPTIONS, POSTULATES, TrifocalAxis,
        )

        tokens = cmd.strip().split()
        sub = tokens[1].lower() if len(tokens) > 1 else "menu"

        plan = PlanTrifocal(spectral_core=self.orchestrator.pipeline.spectral_core)

        # --- Menu d'aide
        if sub == "menu":
            console.print(Panel(
                "  [bold]trifocal[/bold] - Plan trifocal FZg/HyRi/MsP (Section X)\n\n"
                "  Sous-commandes :\n"
                "    [yellow]trifocal axes[/yellow]                 Liste les 3 axes (FZg, HyRi, MsP)\n"
                "    [yellow]trifocal postulats[/yellow]            Liste les 5 postulats epipolaires (P1-P5)\n"
                "    [yellow]trifocal valider <n> [modele][/yellow] Valide la coherence epipolaire pour n\n"
                "    [yellow]trifocal riemann[/yellow]              Affiche le lien avec l'Hypothese de Riemann\n"
                "    [yellow]trifocal image[/yellow]                Affiche le schema quadrature (image)\n"
                "    [yellow]trifocal schema[/yellow]               Description + apercu du schema\n\n"
                "  Exemples :\n"
                "    [cyan]trifocal valider 26[/cyan]       (modele 1/2 par defaut)\n"
                "    [cyan]trifocal valider 10 1/3[/cyan]\n"
                "    [cyan]trifocal riemann[/cyan]",
                title="[cyan]Aide trifocal[/cyan]", border_style="cyan",
            ))
            return True

        # --- axes
        if sub in {"axes", "axis"}:
            tbl = _Table(
                title="Plan Trifocal - 3 Axes", border_style="cyan", show_lines=True,
            )
            tbl.add_column("Axe", style="bold yellow", no_wrap=True)
            tbl.add_column("Description")
            for axis in TrifocalAxis:
                tbl.add_row(axis.value, AXIS_DESCRIPTIONS[axis])
            console.print(tbl)
            return True

        # --- postulats
        if sub in {"postulats", "postulates"}:
            tbl = _Table(
                title="Plan Trifocal - 5 Postulats epipolaires",
                border_style="cyan", show_lines=True,
            )
            tbl.add_column("Code", style="bold yellow", no_wrap=True)
            tbl.add_column("Nom", style="cyan", no_wrap=True)
            tbl.add_column("Enonce")
            tbl.add_column("Axes", no_wrap=True)
            for p in POSTULATES:
                axes_str = "+".join(a.value for a in p.axes)
                tbl.add_row(p.code, p.name, p.statement, axes_str)
            console.print(tbl)
            return True

        # --- valider <n> [modele]
        if sub in {"valider", "validate"}:
            if len(tokens) < 3:
                console.print(
                    "\n  [yellow]Usage : trifocal valider <n> [modele]\n"
                    "  modele = 1/2 (defaut) | 1/3 | 1/4[/yellow]\n"
                )
                return True
            try:
                n = int(tokens[2])
            except ValueError:
                console.print(f"\n  [yellow]Position invalide : '{tokens[2]}'[/yellow]\n")
                return True
            model = tokens[3] if len(tokens) >= 4 else "1/2"

            try:
                v = plan.validate(n=n, model_name=model)
            except ValueError as exc:
                console.print(f"\n  [red]Erreur : {exc}[/red]\n")
                return True

            style = "green" if v.epipolar_coherent else "yellow"
            console.print(Panel(
                v.to_text(),
                title=f"[{style}]Validation epipolaire trifocale n={n} ({model})[/{style}]",
                border_style=style,
            ))
            # Claim epistemique
            claim = plan.epistemic_claim(v)
            color = {"CERTAIN": "green", "CONJECTURE": "yellow",
                     "HORS_DOMAINE": "red"}.get(claim.certainty.value, "white")
            body = (
                f"[bold {color}]{claim.certainty.value}[/bold {color}]   "
                f"citable={'oui' if claim.can_cite() else 'non'}\n"
                f"  {claim.statement}\n"
                f"  Provenance : {', '.join(p.value for p in claim.provenance) or '—'}"
            )
            if claim.limits:
                body += "\n  Limites :\n" + "\n".join(
                    f"    - {lim}" for lim in claim.limits
                )
            console.print(Panel(
                body, title="[bold]Claim epistemique (Axe 4)[/bold]",
                border_style=color,
            ))

            # Audit JSON citable
            try:
                from src.audit import AuditStore as _AS
                store = self.orchestrator.pipeline.audit_store
                record = _AS.build_record(
                    intervention_type="trifocal",
                    question=cmd.strip(),
                    certified_answer=(
                        f"Validation trifocale n={n} model={model} : "
                        f"{'VALIDE' if v.epipolar_coherent else 'BRISEE'}. "
                        f"P1={v.p1_positions_match}, P2={v.p2_demi_equal}, "
                        f"MsP={v.msp_equation_holds}."
                    ),
                    position=n, prime_value=v.prime,
                    citations_thy=[
                        "methode_spectral.thy::Section X (Validation epipolaire)",
                        "methode_spectral.thy::SA_def, SB_def, prime_equation",
                        "riemann_spectral.thy::RiemannHypothesis",
                    ],
                    toolkit_reports={"plan_trifocal": {
                        "n": v.n, "prime": v.prime, "model": v.model_name,
                        "msp_demi": str(v.msp_demi),
                        "hypR_demi": str(v.hypR_demi),
                        "p1_positions_match": v.p1_positions_match,
                        "p2_demi_equal": v.p2_demi_equal,
                        "msp_equation_holds": v.msp_equation_holds,
                        "epipolar_coherent": v.epipolar_coherent,
                        "details": v.details,
                    }},
                    ratio=model,
                )
                store.save(record)
                console.print(
                    f"\n[dim]Audit cree : id={record.id} "
                    f"(citer {record.id} pour bloc citable)[/dim]\n"
                )
            except Exception as exc:
                logger.warning("Audit trifocal non sauvegarde : %s", exc)
            return True

        # --- riemann
        if sub == "riemann":
            from src.spectral import PlanTrifocal as _PT
            console.print(Panel(
                _PT.riemann_link_statement(),
                title="[magenta]Lien Methode Spectrale <-> Hypothese de Riemann[/magenta]",
                border_style="magenta", padding=(1, 2),
            ))
            return True

        console.print(
            f"\n  [yellow]Sous-commande inconnue : '{sub}'. "
            "Tapez 'trifocal' pour l'aide.[/yellow]\n"
        )
        return True

    # ------------------------------------------------------------------
    # Acces filesystem : voir-image / analyser-image / lire / scan
    # ------------------------------------------------------------------

    def _split_path_arg(self, cmd: str, prefix_options: list[str]) -> tuple[str, str]:
        """Retourne (chemin, reste) apres avoir enleve le prefixe (voir/lire/...)."""
        raw = cmd.strip()
        for prefix in prefix_options:
            if raw.lower().startswith(prefix.lower() + " "):
                rest = raw[len(prefix) + 1:].strip()
                # On accepte des chemins avec espaces si entoures de guillemets
                if rest.startswith('"') and '"' in rest[1:]:
                    end = rest.index('"', 1)
                    return rest[1:end], rest[end + 1:].strip()
                if rest.startswith("'") and "'" in rest[1:]:
                    end = rest.index("'", 1)
                    return rest[1:end], rest[end + 1:].strip()
                parts = rest.split(None, 1)
                return parts[0], (parts[1] if len(parts) > 1 else "")
        return "", ""

    def _handle_voir_image(self, cmd: str) -> bool:
        """Commande `voir-image <chemin>` : apercu ASCII + metadonnees."""
        from ..core.filesystem_access import voir_image, format_image
        chemin, _ = self._split_path_arg(cmd, ["voir-image", "voir"])
        if not chemin:
            console.print(
                "\n  [yellow]Usage : voir-image <chemin>\n"
                "  Exemple : voir-image /home/agent/app/data/graphs/mon_image.png[/yellow]\n"
            )
            return True
        try:
            result = voir_image(chemin, cols=70)
            console.print(Panel(
                format_image(result),
                title="[cyan]Apercu image[/cyan]",
                border_style="cyan",
            ))
        except (FileNotFoundError, IsADirectoryError, RuntimeError, ValueError) as exc:
            console.print(f"\n  [red]{exc}[/red]\n")
        return True

    def _handle_analyser_image(self, cmd: str) -> bool:
        """Commande `analyser-image <chemin> [question]` : Claude Vision."""
        from ..core.filesystem_access import analyser_image
        chemin, question = self._split_path_arg(cmd, ["analyser-image", "analyser"])
        if not chemin:
            console.print(
                "\n  [yellow]Usage : analyser-image <chemin> [question]\n"
                "  Exemple : analyser-image /home/agent/app/data/graphs/sa.png\n"
                "            analyser-image /path/schema.png \"quels axes ?\"[/yellow]\n"
            )
            return True
        console.print(
            "\n  [dim]Analyse Claude Vision en cours (peut prendre 10-30s)...[/dim]\n"
        )
        try:
            texte = analyser_image(chemin, question=question or None)
            console.print(Panel(
                texte,
                title=f"[cyan]Analyse Claude Vision : {chemin}[/cyan]",
                border_style="cyan",
                padding=(1, 2),
            ))
        except (FileNotFoundError, IsADirectoryError, RuntimeError, ValueError) as exc:
            console.print(f"\n  [red]{exc}[/red]\n")
        return True

    def _handle_lire(self, cmd: str) -> bool:
        """Commande `lire <chemin> [n_lignes]` : lecture d'un fichier texte."""
        from ..core.filesystem_access import lire_fichier, format_file
        chemin, reste = self._split_path_arg(cmd, ["lire"])
        if not chemin:
            console.print(
                "\n  [yellow]Usage : lire <chemin> [n_lignes]\n"
                "  Exemples :\n"
                "    lire /home/agent/app/theories/methode_spectral.thy\n"
                "    lire docs/geometrie_spectre_premiers.tex 100[/yellow]\n"
            )
            return True
        n_lignes = 200
        if reste:
            try:
                n_lignes = int(reste.split()[0])
            except (ValueError, IndexError):
                pass
        try:
            result = lire_fichier(chemin, max_lignes=n_lignes)
            console.print(Panel(
                format_file(result),
                title=f"[cyan]Contenu fichier[/cyan]",
                border_style="cyan",
            ))
        except (FileNotFoundError, IsADirectoryError, RuntimeError, ValueError) as exc:
            console.print(f"\n  [red]{exc}[/red]\n")
        return True

    def _handle_scan(self, cmd: str) -> bool:
        """Commande `scan <chemin>` : liste un dossier (volumes montes)."""
        from ..core.filesystem_access import scanner_dossier, format_scan
        chemin, _ = self._split_path_arg(cmd, ["scan"])
        if not chemin:
            console.print(
                "\n  [yellow]Usage : scan <chemin>\n"
                "  Exemples :\n"
                "    scan /home/agent/app/data\n"
                "    scan /home/agent/app/theories\n"
                "    scan /workspace[/yellow]\n"
            )
            return True
        try:
            result = scanner_dossier(chemin)
            console.print(Panel(
                format_scan(result),
                title=f"[cyan]Scan dossier[/cyan]",
                border_style="cyan",
            ))
        except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError) as exc:
            console.print(f"\n  [red]{exc}[/red]\n")
        return True



    def _handle_env_check(self, cmd: str) -> bool:
        """Commande `env-check` : diagnostic complet des fichiers .env.

        Montre :
          - tous les fichiers .env presents dans le projet
          - lequel est ACTIF (charge par dotenv)
          - quelles cles API sont configurees (sans afficher la valeur)
          - le marqueur exact pour la cle Anthropic Claude
        """
        from rich.table import Table as _Table
        from rich.text import Text as _Text
        from src.core.config import LOADED_ENV_PATH

        # 1. Lister tous les .env du projet (et alentours)
        roots_to_scan = [
            Path("/app/agent-multiloop-Gabriel-local"),
            Path("/app"),
            Path.cwd(),
        ]
        found: dict[Path, dict] = {}
        for root in roots_to_scan:
            if not root.exists():
                continue
            for pattern in (".env", ".env.example", ".env.local"):
                for p in root.glob(pattern):
                    if p.is_file():
                        found.setdefault(p.resolve(), {
                            "size": p.stat().st_size,
                            "has_anthropic": False,
                            "has_openai": False,
                            "has_real_key": False,
                        })

        # Analyser le contenu (sans afficher les valeurs)
        for path, info in found.items():
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                for line in content.splitlines():
                    if line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, _, val = line.partition("=")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key in ("CLAUDE_API_KEY", "ANTHROPIC_API_KEY"):
                        info["has_anthropic"] = True
                        if val.startswith("sk-ant-") and len(val) > 30:
                            info["has_real_key"] = True
                    if key == "OPENAI_API_KEY":
                        info["has_openai"] = True
            except Exception as exc:
                info["error"] = str(exc)

        # 2. Affichage Rich
        header = _Text()
        header.append("DIAGNOSTIC DES FICHIERS .env\n", style="bold bright_cyan")
        header.append("(carte complete + cle ACTIVEMENT chargee par Gabriel)",
                      style="dim italic")
        console.print(Panel(header, border_style="bright_cyan", padding=(1, 2)))

        # Tableau des .env trouves
        tbl = _Table(
            title="Fichiers .env detectes",
            border_style="cyan", show_lines=True,
        )
        tbl.add_column("Chemin", style="bold", overflow="fold")
        tbl.add_column("Taille", justify="right")
        tbl.add_column("CLAUDE_API_KEY", justify="center")
        tbl.add_column("Cle reelle ?", justify="center")
        tbl.add_column("ACTIF", justify="center", style="bold")

        for path in sorted(found.keys(), key=str):
            info = found[path]
            is_active = (LOADED_ENV_PATH is not None
                         and Path(LOADED_ENV_PATH).resolve() == path)
            tbl.add_row(
                str(path),
                f"{info['size']}o",
                "[green]V[/green]" if info["has_anthropic"] else "[red]X[/red]",
                "[green]sk-ant-...[/green]" if info["has_real_key"]
                else "[yellow]placeholder[/yellow]" if info["has_anthropic"]
                else "[red]aucune[/red]",
                "[bold green]<- CHARGE[/bold green]" if is_active else "—",
            )
        console.print(tbl)

        # 3. Cle ANTHROPIC en memoire actuellement
        env_claude = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY") or ""
        env_openai = os.environ.get("OPENAI_API_KEY") or ""
        is_claude_valid = env_claude.startswith("sk-ant-") and len(env_claude) > 30
        is_openai_valid = env_openai.startswith("sk-") and len(env_openai) > 30

        runtime = _Text()
        runtime.append("CLES EFFECTIVEMENT CHARGEES EN MEMOIRE\n",
                       style="bold bright_cyan")
        runtime.append("\n")
        runtime.append("  CLAUDE_API_KEY  : ", style="bold yellow")
        if is_claude_valid:
            runtime.append(f"OK ({env_claude[:10]}...{env_claude[-4:]})\n",
                           style="bold green")
        elif env_claude:
            runtime.append(
                f"INVALIDE (valeur='{env_claude[:30]}...', "
                "doit commencer par 'sk-ant-')\n", style="bold yellow",
            )
        else:
            runtime.append("ABSENTE -> Claude DESACTIVE\n", style="bold red")
        # CLAUDE_MODEL : signaler les modeles obsoletes
        env_claude_model = os.environ.get("CLAUDE_MODEL", "")
        if env_claude_model:
            valid_2026_models = {
                "claude-sonnet-4-5-20250929",
                "claude-opus-4-5",
                "claude-haiku-4-5",
                "claude-sonnet-4-5",
                "claude-opus-4-1",
                "claude-3-5-haiku-latest",
            }
            deprecated_prefixes = (
                "claude-3-5-sonnet-2024", "claude-3-haiku-2024",
                "claude-3-opus-2024", "claude-3-sonnet-",
            )
            runtime.append("  CLAUDE_MODEL    : ", style="bold yellow")
            if env_claude_model in valid_2026_models:
                runtime.append(f"OK ({env_claude_model})\n",
                               style="bold green")
            elif any(env_claude_model.startswith(p) for p in deprecated_prefixes):
                runtime.append(
                    f"OBSOLETE ({env_claude_model}) -> changer pour "
                    "'claude-sonnet-4-5-20250929'\n",
                    style="bold red",
                )
            else:
                runtime.append(f"INCONNU ({env_claude_model})\n",
                               style="yellow")
        runtime.append("  OPENAI_API_KEY  : ", style="bold yellow")
        if is_openai_valid:
            runtime.append(f"OK ({env_openai[:7]}...{env_openai[-4:]})\n",
                           style="bold green")
        elif env_openai:
            runtime.append(
                f"INVALIDE (valeur='{env_openai[:20]}...')\n",
                style="bold yellow",
            )
        else:
            runtime.append("ABSENTE\n", style="bold red")

        console.print(Panel(
            runtime, title="[bold]Etat runtime[/bold]",
            border_style="green" if is_claude_valid else "red",
            padding=(1, 2),
        ))

        # 4. Instructions
        # Detection du package anthropic dans le container
        try:
            import anthropic  # noqa: F401
            anthropic_ok = True
        except ImportError:
            anthropic_ok = False

        if not anthropic_ok:
            warn = _Text()
            warn.append("PACKAGE ANTHROPIC NON INSTALLE\n",
                        style="bold bright_red")
            warn.append("\n")
            warn.append(
                "  Le module Python 'anthropic' n'est pas dans le container.\n"
                "  Cause : ", style="white",
            )
            warn.append("'anthropic' absent de requirements.txt\n",
                        style="yellow")
            warn.append("  Solution :\n", style="bold yellow")
            warn.append(
                "    1. Verifier requirements.txt contient : ",
                style="white",
            )
            warn.append("anthropic>=0.40.0\n", style="cyan")
            warn.append("    2. Rebuild l'image :  ", style="white")
            warn.append(
                "docker-compose down && docker-compose up --build\n",
                style="cyan",
            )
            console.print(Panel(
                warn, title="[bold red]Anthropic SDK manquant[/bold red]",
                border_style="red", padding=(1, 2),
            ))

        if not is_claude_valid:
            instr = _Text()
            instr.append("COMMENT AJOUTER VOTRE CLE ANTHROPIC\n",
                         style="bold bright_yellow")
            instr.append("\n")
            instr.append("  1. Ouvrir le fichier  : ", style="bold")
            instr.append(
                f"{_ROOT_ENV_PATH}\n", style="bold cyan",
            )
            instr.append("  2. Chercher la balise : ", style="bold")
            instr.append(">>>  COLLEZ VOTRE CLE ANTHROPIC CLAUDE ICI  <<<\n",
                         style="bold cyan")
            instr.append("  3. Remplacer la ligne :\n", style="bold")
            instr.append(
                "       CLAUDE_API_KEY=COLLEZ-VOTRE-CLE-ICI\n",
                style="dim",
            )
            instr.append("     par :\n", style="bold")
            instr.append(
                "       CLAUDE_API_KEY=sk-ant-api03-xxxx...vos-vraies-donnees\n",
                style="green",
            )
            instr.append("\n  4. ", style="bold")
            instr.append("Redemarrer Gabriel ", style="bold")
            instr.append("(le .env n'est lu qu'au demarrage) :\n", style="dim")
            instr.append(
                "       docker-compose down && docker-compose up --build\n",
                style="cyan",
            )
            instr.append("\n  5. ", style="bold")
            instr.append("Re-executer 'env-check' pour confirmer.", style="dim")
            console.print(Panel(
                instr, title="[bold yellow]Action requise[/bold yellow]",
                border_style="yellow", padding=(1, 2),
            ))
        else:
            console.print(
                "\n  [bold green]Gabriel est pret a utiliser Claude (Anthropic).[/bold green]\n"
            )

        # 5. TEST LIVE de l'API Claude (si demande)
        tokens = cmd.strip().split()
        if len(tokens) > 1 and tokens[1].lower() in ("live", "test", "ping"):
            self._test_claude_live()
        elif is_claude_valid:
            console.print(
                "  [dim]Pour tester en live l'API Claude (consomme 1 appel) : "
                "[/dim][cyan]env-check live[/cyan]\n"
            )
        return True

    def _test_claude_live(self) -> None:
        """Test live de l'API Claude (1 appel reel, ~1 cent)."""
        from rich.text import Text as _Text

        env_claude = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        env_model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
        if not env_claude or not env_claude.startswith("sk-ant-"):
            console.print(
                "  [red]Impossible de tester : pas de cle Claude valide.[/red]\n"
            )
            return
        console.print(
            f"\n  [dim]Test live -> appel API Claude ({env_model})...[/dim]\n"
        )
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=env_claude, timeout=30)
            response = client.messages.create(
                model=env_model,
                max_tokens=80,
                messages=[{
                    "role": "user",
                    "content": "Reponds en 1 phrase exacte : quel est le 17e nombre premier ?",
                }],
            )
            txt = response.content[0].text if response.content else "(vide)"
            body = _Text()
            body.append("APPEL LIVE REUSSI\n\n", style="bold bright_green")
            body.append(f"  Modele utilise : ", style="bold yellow")
            body.append(f"{env_model}\n", style="cyan")
            body.append(f"  Reponse Claude : ", style="bold yellow")
            body.append(f"{txt[:200]}\n", style="white")
            body.append(f"  Tokens         : ", style="bold yellow")
            body.append(
                f"{response.usage.input_tokens} in + "
                f"{response.usage.output_tokens} out\n",
                style="dim",
            )
            console.print(Panel(
                body, title="[bold bright_green]Claude LIVE ✓[/bold bright_green]",
                border_style="bright_green", padding=(1, 2),
            ))
        except Exception as exc:
            err_msg = str(exc)
            body = _Text()
            body.append("APPEL LIVE ECHOUE\n\n", style="bold red")
            body.append(f"  Erreur : ", style="bold yellow")
            body.append(f"{type(exc).__name__}\n", style="red")
            body.append(f"  Detail : ", style="bold yellow")
            body.append(f"{err_msg[:300]}\n", style="white")
            body.append("\n  Diagnostic :\n", style="bold yellow")
            if "not_found_error" in err_msg or "404" in err_msg:
                body.append(
                    f"    -> Le modele '{env_model}' n'existe plus.\n"
                    "    -> Ajoutez dans .env :  "
                    "CLAUDE_MODEL=claude-sonnet-4-5-20250929\n",
                    style="white",
                )
            elif "authentication" in err_msg.lower() or "401" in err_msg:
                body.append(
                    "    -> Cle API invalide ou revoquee.\n"
                    "    -> Generez une nouvelle cle sur "
                    "console.anthropic.com/settings/keys\n",
                    style="white",
                )
            elif "rate_limit" in err_msg.lower() or "429" in err_msg:
                body.append(
                    "    -> Quota atteint ou rate-limit.\n"
                    "    -> Verifiez votre tier sur console.anthropic.com\n",
                    style="white",
                )
            else:
                body.append(
                    "    -> Erreur inattendue. Verifiez la connexion reseau et "
                    "console.anthropic.com.\n", style="white",
                )
            console.print(Panel(
                body, title="[bold red]Claude LIVE ✗[/bold red]",
                border_style="red", padding=(1, 2),
            ))

    def _handle_cognitive(self, cmd: str) -> bool:
        """Commande `cognitive [report|reset]` : statistiques Axe 5 (MetaReasoner)."""
        from rich.table import Table as _Table

        tokens = cmd.strip().split()
        sub = tokens[1].lower() if len(tokens) > 1 else "report"

        if sub == "reset":
            for cat in list(self._meta_reasoner.stats.keys()):
                stats = self._meta_reasoner.stats[cat]
                stats.total = 0
                stats.successes = 0
            self._meta_reasoner._save_stats()
            console.print("  [green]Statistiques MetaReasoner reinitialisees.[/green]\n")
            return True

        if sub not in {"report", "stats", "show"}:
            console.print(
                "\n  [yellow]Usage : cognitive [report|reset]\n"
                "    report  Affiche les stats d'auto-evaluation (defaut)\n"
                "    reset   Reinitialise toutes les categories a 0[/yellow]\n"
            )
            return True

        report = self._meta_reasoner.report()
        tbl = _Table(
            title="Auto-evaluation Gabriel (Axe 5 - MetaReasoner)",
            border_style="cyan", show_lines=False,
        )
        tbl.add_column("Categorie", style="bold yellow", no_wrap=True)
        tbl.add_column("Total", justify="right")
        tbl.add_column("Succes", justify="right")
        tbl.add_column("Taux", justify="right")
        tbl.add_column("Confiance", justify="center")
        for cat, data in sorted(report.items()):
            conf = data["confidence"]
            conf_color = {
                "HIGH": "green", "MEDIUM": "yellow",
                "LOW": "red", "UNKNOWN": "dim",
            }.get(conf, "white")
            tbl.add_row(
                cat,
                str(data["total"]),
                str(data["successes"]),
                f"{data['rate']*100:.1f}%" if data["total"] else "—",
                f"[{conf_color}]{conf}[/{conf_color}]",
            )
        console.print(tbl)
        console.print(
            f"\n  [dim]Fichier stats : {self._meta_reasoner.stats_file}[/dim]\n"
            f"  [dim]Fichier erreurs : {self._meta_reasoner.errors_file}[/dim]\n"
        )
        return True

        """Commande `cognitive [report|reset]` : statistiques Axe 5 (MetaReasoner)."""
        from rich.table import Table as _Table

        tokens = cmd.strip().split()
        sub = tokens[1].lower() if len(tokens) > 1 else "report"

        if sub == "reset":
            for cat in list(self._meta_reasoner.stats.keys()):
                stats = self._meta_reasoner.stats[cat]
                stats.total = 0
                stats.successes = 0
            self._meta_reasoner._save_stats()
            console.print("  [green]Statistiques MetaReasoner reinitialisees.[/green]\n")
            return True

        if sub not in {"report", "stats", "show"}:
            console.print(
                "\n  [yellow]Usage : cognitive [report|reset]\n"
                "    report  Affiche les stats d'auto-evaluation (defaut)\n"
                "    reset   Reinitialise toutes les categories a 0[/yellow]\n"
            )
            return True

        report = self._meta_reasoner.report()
        tbl = _Table(
            title="Auto-evaluation Gabriel (Axe 5 - MetaReasoner)",
            border_style="cyan", show_lines=False,
        )
        tbl.add_column("Categorie", style="bold yellow", no_wrap=True)
        tbl.add_column("Total", justify="right")
        tbl.add_column("Succes", justify="right")
        tbl.add_column("Taux", justify="right")
        tbl.add_column("Confiance", justify="center")
        for cat, data in sorted(report.items()):
            conf = data["confidence"]
            conf_color = {
                "HIGH": "green", "MEDIUM": "yellow",
                "LOW": "red", "UNKNOWN": "dim",
            }.get(conf, "white")
            tbl.add_row(
                cat,
                str(data["total"]),
                str(data["successes"]),
                f"{data['rate']*100:.1f}%" if data["total"] else "—",
                f"[{conf_color}]{conf}[/{conf_color}]",
            )
        console.print(tbl)
        console.print(
            f"\n  [dim]Fichier stats : {self._meta_reasoner.stats_file}[/dim]\n"
            f"  [dim]Fichier erreurs : {self._meta_reasoner.errors_file}[/dim]\n"
        )
        return True

    def _render_cognitive_result(self, result, header: str) -> None:
        """Rendu Rich d'un CognitiveResult (Axe 2/3/4/5)."""
        from rich.table import Table as _Table

        trace = result.proof_trace
        # Panneau invariants
        if trace.invariants_checked:
            inv_tbl = _Table(
                title="Invariants verifies", border_style="cyan", show_lines=False,
            )
            inv_tbl.add_column("Nom", style="bold")
            inv_tbl.add_column("Statut", justify="center")
            inv_tbl.add_column("Detail")
            for inv in trace.invariants_checked:
                statut = "[green]OK[/green]" if inv["passed"] else "[red]FAIL[/red]"
                inv_tbl.add_row(inv["name"], statut, inv.get("details", ""))
            console.print(inv_tbl)

        # Claim epistemique
        claim = result.claim
        marker_color = {
            "CERTAIN": "green",
            "CONJECTURE": "yellow",
            "HORS_DOMAINE": "red",
        }.get(claim.certainty.value, "white")
        body = (
            f"[bold {marker_color}]{claim.certainty.value}[/bold {marker_color}]  "
            f"{claim.statement}\n\n"
            f"  Provenance : {', '.join(p.value for p in claim.provenance) or '—'}\n"
            f"  Regime     : {result.regime or '—'}\n"
            f"  Categorie  : {result.category}\n"
            f"  Citable    : {'oui' if claim.can_cite() else 'non'}"
        )
        if claim.limits:
            body += "\n  Limites    :\n" + "\n".join(f"    - {lim}" for lim in claim.limits)
        console.print(Panel(body, title=header, border_style=marker_color))

        # Enregistrement MetaReasoner
        try:
            from src.cognitive import record_cognitive_result
            record_cognitive_result(result, meta=self._meta_reasoner)
        except Exception as exc:
            logger.debug("MetaReasoner record : %s", exc)

    def _render_traced_gap(self, p1: int, p2: int) -> None:
        from src.cognitive import build_gap_result
        result = build_gap_result(p1, p2)
        self._render_cognitive_result(
            result, header=f"[cyan]Axe cognitif - gap({p1}, {p2})[/cyan]",
        )

    def _render_traced_reconstruct(self, n: int, actual_prime: int) -> None:
        from src.cognitive import build_reconstruct_result
        for model_name in ("1/2", "1/3", "1/4"):
            res = build_reconstruct_result(n, actual_prime, model_name)
            self._render_cognitive_result(
                res,
                header=f"[cyan]Axe cognitif - reconstruct(n={n}) modele {model_name}[/cyan]",
            )

    def _render_traced_rsp1x1(self, n1: int, n2: int) -> None:
        from src.cognitive import build_rsp_1x1_result
        for model_name in ("1/2", "1/3", "1/4"):
            res = build_rsp_1x1_result(n1, n2, model_name)
            self._render_cognitive_result(
                res,
                header=f"[cyan]Axe cognitif - RsP_1x1({n1}, {n2}) modele {model_name}[/cyan]",
            )

    def _save_modele_audit(self, report, cmd_text: str) -> None:
        """Sauvegarde un audit JSON citable pour les commandes modele."""
        try:
            from src.audit import AuditStore as _AS
            store = self.orchestrator.pipeline.audit_store
            results_summary = {}
            for name, res in report.results_by_model.items():
                # Convertir Fraction en str pour serialisation
                results_summary[name] = {
                    k: (str(v) if not isinstance(v, (int, float, bool, str, list, dict, type(None))) else v)
                    for k, v in res.__dict__.items()
                }
            record = _AS.build_record(
                intervention_type="modele_spectral",
                question=cmd_text,
                certified_answer=f"{report.question} : {report.description}",
                citations_thy=[
                    "methode_spectral.thy::SA_def, SB_def, RsP_def",
                    "methode_spectral.thy::A_1_3, B_1_3, A_1_4, B_1_4",
                    "methode_spectral.thy::digamma_calc, prime_equation",
                ],
                toolkit_reports={
                    "geometrie_spectrale_engine": {
                        "question": report.question,
                        "description": report.description,
                        "results_by_model": results_summary,
                        "notes": report.notes,
                    }
                },
                ratio="1/2,1/3,1/4",
            )
            store.save(record)
            console.print(f"  [dim]Audit cree : id={record.id} (citer {record.id})[/dim]\n")
        except Exception as exc:
            logger.warning(f"Audit modele non sauvegarde : {exc}")

    async def _handle_courbe(self, cmd: str) -> bool:
        """Commande `courbe <type> <n_min>..<n_max> [--table] [--png] [--scale=...]`.

        Types : SA, SB, SA_SB, digamma, invariant, ratio, gap, prime.
        Flags :
          --table    : ajoute un tableau Rich apres l'ASCII.
          --png      : exporte un PNG haute resolution + cree un audit JSON citable.
          --scale=X  : force l'echelle (linear|log10|log2|auto, defaut: auto).
        """
        from pathlib import Path as _Path
        from src.visualization import (
            compute_curve, render_ascii, render_table, render_png,
            list_supported_kinds, MATPLOTLIB_AVAILABLE,
        )

        tokens = cmd.strip().split()
        if len(tokens) < 3:
            console.print(
                "\n  [yellow]Usage : courbe <type> <n_min>..<n_max> [--table] [--png] [--scale=X]\n"
                f"  Types disponibles : {' | '.join(list_supported_kinds())}\n"
                "  Exemples :\n"
                "    courbe SA 1..50\n"
                "    courbe SA_SB 1..30 --table\n"
                "    courbe digamma 1..100 --png\n"
                "    courbe ratio 1..200 --table --png\n"
                "    courbe invariant 1..50 --scale=linear[/yellow]\n"
            )
            return True

        kind = tokens[1]
        range_spec = tokens[2]
        # Parsing range "n_min..n_max"
        if ".." not in range_spec:
            console.print(f"\n  [yellow]Range invalide : '{range_spec}'. "
                          f"Format attendu : n_min..n_max (ex: 1..50)[/yellow]\n")
            return True
        try:
            n_min_s, n_max_s = range_spec.split("..", 1)
            n_min, n_max = int(n_min_s), int(n_max_s)
        except ValueError:
            console.print(f"\n  [yellow]Range invalide : '{range_spec}'[/yellow]\n")
            return True

        # Flags
        want_table = "--table" in tokens
        want_png = "--png" in tokens
        scale = "auto"
        for tok in tokens[3:]:
            if tok.startswith("--scale="):
                scale = tok.split("=", 1)[1]

        # Calcul
        core = self.orchestrator.pipeline.spectral_core
        try:
            curve = compute_curve(core, kind, n_min, n_max, scale=scale)
        except ValueError as exc:
            console.print(f"\n  [red]Erreur : {exc}[/red]\n")
            return True

        # 1) ASCII (toujours)
        ascii_view = render_ascii(curve, width=70, height=18)
        console.print(Panel(
            ascii_view,
            title=f"[cyan]Courbe {curve.kind.value} (n={n_min}..{n_max})[/cyan]",
            border_style="cyan",
        ))

        # 2) Table Rich (optionnel)
        if want_table:
            console.print(render_table(curve, max_rows=30))

        # 3) PNG (optionnel) + audit JSON citable
        png_path = None
        if want_png:
            if not MATPLOTLIB_AVAILABLE:
                console.print(
                    "\n  [red]matplotlib non installe. Installation : "
                    "'pip install matplotlib'[/red]\n"
                )
            else:
                output_dir = _Path("data/graphs")
                try:
                    png_path = render_png(curve, output_dir=output_dir, dpi=150)
                    console.print(
                        f"\n  [green]PNG cree :[/green] [bold]{png_path}[/bold]  "
                        f"(taille : {png_path.stat().st_size // 1024} Ko, dpi=150)\n"
                    )
                except (ImportError, ValueError) as exc:
                    console.print(f"\n  [red]Erreur PNG : {exc}[/red]\n")

        # Audit citable
        from src.audit import AuditStore as _AS
        store = self.orchestrator.pipeline.audit_store
        record = _AS.build_record(
            intervention_type="courbe",
            question=cmd.strip(),
            certified_answer=(
                f"Courbe {curve.kind.value} sur n={n_min}..{n_max} "
                f"(echelle {curve.scale}). {len(curve.points)} points. "
                f"Formule : {curve.formula}."
            ),
            position=n_min,
            prime_value=core.get_prime_at_position(n_min),
            citations_thy=[
                "methode_spectral.thy::SA_def (suite alternee A)",
                "methode_spectral.thy::SB_def (suite alternee B)",
                "geometrie_spectre_premier.thy::D_def (invariant spectral)",
            ],
            toolkit_reports={
                "visualization": {
                    "kind": curve.kind.value,
                    "n_min": n_min, "n_max": n_max,
                    "scale": curve.scale,
                    "formula": curve.formula,
                    "summary": curve.summary(),
                    "png_path": str(png_path) if png_path else None,
                }
            },
            ratio="1/2",
        )
        store.save(record)
        console.print(
            f"\n[dim]Audit cree : id={record.id} (tapez 'citer {record.id}' pour citer)[/dim]\n"
        )
        return True

    def _display_answer(self, answer: FinalAnswer) -> None:
        # Detecter le mode slow-motion -> rendu instrument de precision
        is_slow_motion = bool(
            answer.structured_data
            and answer.structured_data.get("slow_motion_triggered")
        )
        if is_slow_motion:
            return self._display_slow_motion(answer)

        # Affichage principal standard
        console.print(
            Panel(
                answer.answer_text,
                title=f"[bold green]Reponse[/bold green]  "
                f"(score {answer.best_score:.1f}/10, iter {answer.iterations_used})",
                border_style="green",
            )
        )
        # Calculs intermediaires
        if answer.structured_data:
            facts = []
            for k, v in answer.structured_data.items():
                if isinstance(v, (int, float, str, bool)):
                    facts.append(f"  {k} = {v}")
            if facts:
                console.print(
                    Panel("\n".join(facts), title="[cyan]Chiffres calcules[/cyan]", border_style="cyan")
                )
        # Axe 4 : niveau de certitude epistemique
        if answer.epistemic_claim:
            ec = answer.epistemic_claim
            cert = ec.get("certainty", "?")
            color = {"CERTAIN": "green", "CONJECTURE": "yellow",
                     "HORS_DOMAINE": "red"}.get(cert, "white")
            body = (
                f"[bold {color}]{cert}[/bold {color}]   "
                f"citable={'oui' if ec.get('can_cite') else 'non'}\n"
                f"  Provenance : {', '.join(ec.get('provenance', [])) or '—'}"
            )
            if ec.get("limits"):
                body += "\n  Limites :\n" + "\n".join(
                    f"    - {lim}" for lim in ec["limits"]
                )
            console.print(Panel(
                body,
                title=f"[{color}]Niveau de certitude (Axe 4)[/{color}]",
                border_style=color,
            ))
        # Script HOL
        if answer.hol_script:
            console.print(
                Panel(answer.hol_script, title="[yellow]Fragment HOL genere[/yellow]", border_style="yellow")
            )

    # ====================================================================
    # Rendu SLOW-MOTION : "Kit de reparation spectrale" (instrument precis)
    # ====================================================================
    def _display_slow_motion(self, answer: FinalAnswer) -> None:
        """Rendu dedie pour les reponses produites par le Slow-Motion Debugger.

        Theme : kit de reparation metrologique. Chaque panneau = un cadran.
        Couleur dominante : turquoise/teal profond (precision) + accents ambre
        (alerte / instrument calibre). Espacement aere pour lecture critique.
        """
        from rich.text import Text as _Text
        from rich.rule import Rule as _Rule

        sd = answer.structured_data or {}
        certified = sd.get("certified") or {}
        decomposition = sd.get("decomposition") or {}
        timeline_events = sd.get("debug_timeline") or []
        suggestions = sd.get("reformulations") or []
        bypassed = decomposition.get("incoherent_segments") or []
        coherence_score = sd.get("coherence_score")
        coherence_signals = sd.get("coherence_signals") or []

        # ----- HEADER : "KIT DE REPARATION SPECTRALE" (autorite) -----
        console.print()  # ligne de respiration avant le panneau
        header_text = _Text()
        header_text.append("KIT DE REPARATION SPECTRALE\n",
                           style="bold bright_cyan")
        header_text.append("MODE INSTRUMENT DE PRECISION  ",
                           style="bold cyan")
        header_text.append("\u2014  ", style="dim")
        header_text.append("Debugger Ralenti active\n",
                           style="italic yellow")
        if coherence_score is not None:
            header_text.append(
                f"\nIncoherence detectee  -  score multiloop = "
                f"{coherence_score:.2f}/1.00\n",
                style="bold red",
            )
        if coherence_signals:
            header_text.append("Signaux declencheurs :\n", style="dim")
            for sig in coherence_signals[:3]:
                header_text.append(f"   * {sig}\n", style="yellow")
        console.print(Panel(
            header_text,
            title="[bold bright_cyan]+- GABRIEL // KIT METRIQUE -+[/bold bright_cyan]",
            border_style="bright_cyan",
            padding=(1, 3),
        ))

        # ----- CADRAN 1 : REFERENCE CERTIFIEE (lecture de l'instrument) -----
        ref_lines = self._parse_certified_summary(certified)
        ref_text = _Text()
        ref_text.append("LECTURE DE L'INSTRUMENT  ", style="bold bright_cyan")
        ref_text.append("(deterministe, sans LLM)\n", style="dim italic")
        ref_text.append("\n")
        for label, value in ref_lines:
            ref_text.append(f"  {label:<14}", style="bold yellow")
            ref_text.append(f"  {value}\n", style="white")
        if certified.get("method") and not any(
            "methode" in lab.lower() for lab, _ in ref_lines
        ):
            ref_text.append("\n  ")
            ref_text.append("Methode      ", style="bold yellow")
            ref_text.append(f"  {certified['method']}\n", style="cyan")
        console.print(Panel(
            ref_text,
            title="[bold]CADRAN 1  -  REFERENCE CERTIFIEE[/bold]",
            subtitle="[dim italic]source : kernel + spectral_core[/dim italic]",
            border_style="bright_cyan",
            padding=(1, 3),
        ))

        # ----- CADRAN 2 : SOURCES DE CERTITUDE (axiomes calibrants) -----
        citations = certified.get("citations") or []
        if citations:
            cit_text = _Text()
            cit_text.append("AXIOMES DE CALIBRATION\n",
                            style="bold bright_cyan")
            cit_text.append("\n")
            for i, cit in enumerate(citations, 1):
                cit_text.append(f"  [{i:>2}]  ", style="bold yellow")
                cit_text.append(f"{cit}\n", style="white")
                if i < len(citations):
                    cit_text.append("\n")
            console.print(Panel(
                cit_text,
                title="[bold]CADRAN 2  -  SOURCES DE CERTITUDE[/bold]",
                subtitle="[dim italic]autorite : methode_spectral.thy + corpus Savard[/dim italic]",
                border_style="cyan",
                padding=(1, 3),
            ))

        # ----- CADRAN 3 : SEGMENTS EN QUARANTAINE (si bypass) -----
        if bypassed:
            byp_text = _Text()
            byp_text.append("SEGMENTS MIS EN QUARANTAINE\n",
                            style="bold bright_red")
            byp_text.append("(ignores pour preserver la coherence)\n",
                            style="dim italic")
            byp_text.append("\n")
            for i, seg in enumerate(bypassed, 1):
                byp_text.append("  [X] ", style="bold red")
                byp_text.append(f"{seg.get('text', '?')}\n", style="white")
                if seg.get("reason"):
                    byp_text.append("      Motif : ", style="dim")
                    byp_text.append(f"{seg['reason']}\n", style="italic yellow")
                if i < len(bypassed):
                    byp_text.append("\n")
            console.print(Panel(
                byp_text,
                title="[bold red]CADRAN 3  -  SEGMENTS REJETES[/bold red]",
                border_style="red",
                padding=(1, 3),
            ))

        # ----- CADRAN 4 : SUGGESTIONS DE REFORMULATION -----
        if suggestions:
            sug_text = _Text()
            sug_text.append("RECALIBRAGE PROPOSE\n",
                            style="bold bright_cyan")
            sug_text.append("(reformulez pour obtenir un resultat plus precis)\n",
                            style="dim italic")
            sug_text.append("\n")
            for i, s in enumerate(suggestions, 1):
                sug_text.append("  -> ", style="bold green")
                sug_text.append(f"{s}\n", style="white")
                if i < len(suggestions):
                    sug_text.append("\n")
            console.print(Panel(
                sug_text,
                title="[bold green]CADRAN 4  -  SUGGESTIONS DE REFORMULATION[/bold green]",
                border_style="green",
                padding=(1, 3),
            ))

        # ----- CADRAN 5 : MODELE DE CERTITUDE (8 criteres / 3 questions) -----
        self._render_certainty_panel(sd.get("certainty_evaluation"))

        # ----- CADRAN 6 : BOUCLE LOGIQUE + REPONSE MODESTE -----
        self._render_modest_panel(
            sd.get("modest_request"), sd.get("modest_certified"),
        )

        # ----- CADRAN 7 : TIMELINE DEBUGGER (chronologie) -----
        if timeline_events:
            console.print()
            console.print(_Rule(
                "[bold bright_cyan]CADRAN 7  -  TIMELINE DEBUGGER (chronologie)[/bold bright_cyan]",
                style="bright_cyan",
            ))
            for ev in timeline_events:
                step = ev.get("step", "?")
                label = ev.get("label", "?")
                detail = ev.get("detail", "")
                title = _Text()
                title.append(f"  T{step:<2}  ", style="bold bright_cyan")
                title.append(f"[{label}]", style="bold yellow")
                console.print(title)
                # detail sur plusieurs lignes, indente
                for line in str(detail).splitlines() or [str(detail)]:
                    if line.strip():
                        console.print(f"        [dim]{line}[/dim]")
                console.print()  # respiration entre etapes
            console.print(_Rule(style="bright_cyan"))

        # ----- CADRAN 8 : Niveau de certitude (Axe 4) -----
        if answer.epistemic_claim:
            ec = answer.epistemic_claim
            cert = ec.get("certainty", "?")
            color = {"CERTAIN": "bright_green", "CONJECTURE": "yellow",
                     "HORS_DOMAINE": "red"}.get(cert, "white")
            body = _Text()
            body.append(f"{cert}", style=f"bold {color}")
            body.append(f"   citable={'oui' if ec.get('can_cite') else 'non'}\n\n",
                        style="dim")
            body.append("  Provenance : ", style="bold yellow")
            body.append(
                f"{', '.join(ec.get('provenance', [])) or '—'}\n",
                style="white",
            )
            if ec.get("limits"):
                body.append("\n  Limites :\n", style="bold yellow")
                for lim in ec["limits"]:
                    body.append(f"     - {lim}\n", style="italic")
            console.print(Panel(
                body,
                title=f"[bold {color}]CADRAN 8  -  NIVEAU DE CERTITUDE (Axe 4)[/bold {color}]",
                border_style=color,
                padding=(1, 3),
            ))

        # ----- Audit ID en bas (si dispo) -----
        if sd.get("audit_id"):
            console.print(
                f"\n  [dim]Audit signe : id={sd['audit_id']} "
                f"(tapez 'citer {sd['audit_id']}' pour bloc citable)[/dim]\n"
            )

    def _render_certainty_panel(self, evaluation: dict | None) -> None:
        """CADRAN 5 — Modele de Certitude (8 criteres / 3 questions).

        Affiche un tableau compact (regroupe par question) avec OK/FAIL + detail.
        """
        if not evaluation or not evaluation.get("results"):
            return
        from rich.table import Table as _Table
        from rich.text import Text as _Text

        ratio = evaluation.get("certainty_ratio", 0.0)
        violated = evaluation.get("violated_codes", [])
        passed = evaluation.get("passed_codes", [])
        # Couleur dynamique selon le ratio
        if ratio >= 1.0:
            color = "bright_green"
            verdict = "TOUS LES CRITERES PASSENT"
        elif ratio >= 0.75:
            color = "yellow"
            verdict = "PARTIEL - quelques criteres violes"
        else:
            color = "red"
            verdict = "INSUFFISANT - reformulation requise"

        header = _Text()
        header.append("MODELE DE CERTITUDE  ", style="bold bright_cyan")
        header.append("(8 criteres / 3 questions essentielles)\n",
                      style="dim italic")
        header.append("\n  Score : ", style="bold yellow")
        header.append(f"{len(passed)}/{len(evaluation['results'])}  ",
                      style=f"bold {color}")
        header.append(f"({ratio*100:.0f}%)  -  ", style=color)
        header.append(f"{verdict}\n", style=f"bold {color}")
        if violated:
            header.append("  Critères violes : ", style="bold yellow")
            header.append(", ".join(violated) + "\n", style="bold red")

        # Tableau par question
        tbl = _Table(border_style=color, show_lines=False, padding=(0, 1))
        tbl.add_column("Q", style="bold yellow", no_wrap=True)
        tbl.add_column("Code", style="bold", no_wrap=True)
        tbl.add_column("Critère", no_wrap=True)
        tbl.add_column("OK", justify="center", no_wrap=True)
        tbl.add_column("Detail")

        q_labels = {
            "Q1_POSITION": "Q1",
            "Q2_MODELE": "Q2",
            "Q3_CONFIGURATION": "Q3",
        }
        for r in evaluation["results"]:
            mark = "[green]V[/green]" if r["passed"] else "[red]X[/red]"
            tbl.add_row(
                q_labels.get(r["question"], "?"),
                r["code"],
                r["name"],
                mark,
                r["detail"],
            )

        from rich.console import Group as _Group
        console.print(Panel(
            _Group(header, tbl),
            title=f"[bold {color}]CADRAN 5  -  MODELE DE CERTITUDE[/bold {color}]",
            subtitle=("[dim italic]Q1=Position | Q2=Modele | "
                      "Q3=Configuration[/dim italic]"),
            border_style=color,
            padding=(1, 2),
        ))

    def _render_modest_panel(
        self, modest: dict | None, modest_certified: dict | None,
    ) -> None:
        """CADRAN 6 — Boucle Logique + Requete Modeste + Reponse Modeste."""
        if not modest:
            return
        from rich.text import Text as _Text

        skips = modest.get("skips_applied") or []
        canonical_text = modest.get("canonical_text", "")

        body = _Text()
        # Section 1 : boucle logique (sursauts)
        body.append("BOUCLE LOGIQUE  ", style="bold bright_cyan")
        body.append("(sursauts appliques pour atteindre la coherence)\n",
                    style="dim italic")
        body.append("\n")
        if skips:
            for i, skip in enumerate(skips, 1):
                body.append(f"  [{i}] ", style="bold yellow")
                body.append(
                    f"{skip.get('criterion')} -> {skip.get('strategy')}\n",
                    style="bold white",
                )
                body.append("      ", style="dim")
                body.append(
                    f"{skip.get('rationale', '')}\n", style="italic",
                )
                if i < len(skips):
                    body.append("\n")
        else:
            body.append(
                "  (aucun sursaut necessaire - la requete satisfait deja les 8 criteres)\n",
                style="dim italic green",
            )

        body.append("\n")
        body.append("REQUETE MODESTE REFORMULEE\n", style="bold bright_cyan")
        body.append(f"  \"{canonical_text}\"\n", style="bold white")

        if modest_certified:
            body.append("\n")
            body.append("REPONSE MODESTE  ", style="bold bright_green")
            body.append("(certifiee par spectral_core, sans LLM)\n",
                        style="dim italic")
            body.append("\n")
            for line in (modest_certified.get("summary") or "").splitlines():
                if line.strip():
                    body.append(f"  {line}\n", style="white")
            if modest_certified.get("method"):
                body.append("\n  Methode : ", style="bold yellow")
                body.append(modest_certified["method"] + "\n",
                            style="cyan")
            cits = modest_certified.get("citations") or []
            if cits:
                body.append("\n  Citations :\n", style="bold yellow")
                for c in cits[:5]:
                    body.append(f"     - {c}\n", style="dim italic")

        console.print(Panel(
            body,
            title="[bold bright_green]CADRAN 6  -  BOUCLE LOGIQUE & REPONSE MODESTE[/bold bright_green]",
            subtitle=("[dim italic]juste milieu : requete originale "
                      "raffinee par les 8 criteres[/dim italic]"),
            border_style="bright_green",
            padding=(1, 3),
        ))

    @staticmethod
    def _parse_certified_summary(certified: dict) -> list[tuple[str, str]]:
        """Decompose le 'summary' du certified en (label, value) pour affichage.

        Le summary suit typiquement le format :
          'Rapport spectral configuration X.\\n  A = [...]\\n  B = [...]\\n
           RsP = num/den (...)\\n  Methode : ...'
        On extrait chaque ligne en (label_avant_=, valeur_apres).
        """
        summary = certified.get("summary", "") or ""
        lines: list[tuple[str, str]] = []
        # Premiere ligne -> "Resume" si elle ne contient pas '=' / ':'
        first, *rest = summary.splitlines()
        if first.strip():
            lines.append(("Resume", first.strip()))
        for raw in rest:
            line = raw.strip()
            if not line:
                continue
            # Format "Methode : ..."
            if line.lower().startswith("methode") and ":" in line:
                label, val = line.split(":", 1)
                lines.append((label.strip().capitalize(), val.strip()))
                continue
            # Format "Foo = bar"
            if "=" in line:
                label, val = line.split("=", 1)
                lines.append((label.strip(), val.strip()))
                continue
            lines.append(("", line))
        # Aussi : ajouter RsP_decimal explicite si dispo et pas deja inclus
        rsp_dec = certified.get("RsP_decimal")
        if rsp_dec is not None and not any("decimal" in lab.lower() for lab, _ in lines):
            lines.append(("RsP (decimal)", f"{rsp_dec:.10f}"))
        # Et la config detectee
        cfg = certified.get("configuration")
        if cfg and not any("configuration" in lab.lower() for lab, _ in lines):
            lines.append(("Configuration", cfg))
        return lines

    @staticmethod
    def _env_enabled(var_name: str, default: bool = False) -> bool:
        raw = os.environ.get(var_name)
        if raw is None:
            return default
        return raw.strip().lower() in {"1", "true", "yes", "on"}

    def _render_live_progress_panel(self, state: dict[str, object]) -> Panel:
        phase = str(state.get("phase", "Initialisation"))
        detail = str(state.get("detail", ""))
        iteration = int(state.get("iteration", 0) or 0)
        max_iterations = int(state.get("max_iterations", 0) or 0)
        best_score = state.get("best_score")
        verbose = bool(state.get("verbose_trace", False))
        assumptions = state.get("assumptions", [])
        options = state.get("options", [])
        recent_events = state.get("recent_events", [])

        # v3.34 : Timer temps reel + ETA + itérations planifiées par PreReasoner
        start_ts = state.get("start_ts")
        eta_sec = state.get("eta_sec")
        planned_iterations = state.get("planned_iterations")
        pre_mode = state.get("pre_mode")
        forced = bool(state.get("pre_forced", False))

        elapsed_str = ""
        eta_str = ""
        if isinstance(start_ts, (int, float)):
            elapsed = max(0.0, time.time() - float(start_ts))
            mm, ss = divmod(int(elapsed), 60)
            elapsed_str = f"{mm:02d}:{ss:02d}"
            if isinstance(eta_sec, (int, float)) and eta_sec > 0:
                remaining = max(0, int(float(eta_sec) - elapsed))
                emm, ess = divmod(remaining, 60)
                eta_str = f"{emm:02d}:{ess:02d}"

        body = Text()
        body.append(" Analyse en cours...\n", style="bold bright_cyan")

        # Ligne dédiée PreReasoner : mode + iterations prévues + timer + ETA
        if pre_mode or planned_iterations or elapsed_str:
            body.append("\n  Plan : ", style="bold magenta")
            if pre_mode:
                label = str(pre_mode).upper()
                if forced:
                    label += " (forcé)"
                body.append(label, style="bright_magenta")
            if planned_iterations:
                body.append(f"  •  itérations prévues : {planned_iterations}",
                            style="bright_white")
            if elapsed_str:
                body.append(f"\n  ⏱ Écoulé : ", style="bold yellow")
                body.append(elapsed_str, style="bright_white")
                if eta_str:
                    body.append(f"  /  ETA restant ~ ", style="dim")
                    body.append(eta_str, style="bright_white")

        body.append("\n\n  Phase : ", style="bold yellow")
        body.append(phase, style="white")

        if iteration and max_iterations:
            body.append("\n  Multi-loop : ", style="bold yellow")
            body.append(f"iteration {iteration}/{max_iterations}", style="bright_white")
            if isinstance(best_score, (int, float)):
                body.append(f"   meilleur score={best_score:.1f}/10", style="dim")

        if detail:
            body.append("\n  Detail : ", style="bold yellow")
            body.append(detail, style="dim")

        if verbose and isinstance(assumptions, list) and assumptions:
            body.append("\n\n  Hypotheses : ", style="bold yellow")
            for item in assumptions[-3:]:
                body.append("\n    - ", style="yellow")
                body.append(str(item), style="dim")

        if verbose and isinstance(options, list) and options:
            body.append("\n\n  Choix evalues : ", style="bold yellow")
            for item in options[-4:]:
                body.append("\n    - ", style="yellow")
                body.append(str(item), style="bright_white")

        if verbose and isinstance(recent_events, list) and recent_events:
            body.append("\n\n  Journal live : ", style="bold yellow")
            for item in recent_events[-5:]:
                body.append("\n    * ", style="cyan")
                body.append(str(item), style="dim")

        return Panel(
            Group(
                Spinner("dots", text="Execution pipeline + multiloop"),
                Text(""),
                body,
            ),
            title="[bold cyan]Gabriel Live Trace[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )

    def _make_progress_callback(
        self,
        state: dict[str, object],
        live_handle: list[Live | None],
        cinematic: bool,
        verbose_trace: bool,
    ):
        phase_labels = {
            "wrapper_start": "Preparation",
            "wrapper_delegate_pipeline": "Delegation pipeline",
            "pipeline_start": "Initialisation pipeline",
            "pre_reasoning_done": "Pré-raisonnement (plan)",
            "abstraction_done": "Abstraction",
            "meta_reasoning_done": "Meta-raisonnement",
            "navigation_done": "Navigation conceptuelle",
            "spectral_compute_done": "Calcul spectral",
            "generalization_done": "Generalisation",
            "multiloop_start": "Demarrage multiloop",
            "multiloop_iteration_start": "Generation de candidats",
            "multiloop_iteration_end": "Selection du meilleur candidat",
            "multiloop_early_stop": "Arret anticipe (score suffisant)",
            "silent_audit_done": "Audit silencieux",
            "silent_audit_skipped": "Audit silencieux (skip)",
            "pipeline_done": "Finalisation",
            "wrapper_done": "Termine",
            "multi_objective_start": "Mode multi-objectifs",
            "multi_objective_item_done": "Objectif traite",
            "gap_detected": "Detection GAP",
            "intent_hypotheses": "Hypotheses d'intent",
            "assumptions_detected": "Hypotheses de travail",
            "decision_gate": "Arbitrage de route",
            "spectral_parse_strategy": "Choix d'interpretation",
        }

        def _push_list(key: str, value: str, limit: int) -> None:
            buf = state.get(key)
            if not isinstance(buf, list):
                buf = []
            buf.append(value)
            if len(buf) > limit:
                buf = buf[-limit:]
            state[key] = buf

        def _on_progress(event: dict[str, Any]) -> None:
            ev = str(event.get("event", ""))
            state["phase"] = phase_labels.get(ev, ev or "Traitement")
            state["verbose_trace"] = verbose_trace

            # v3.34 : evenement du PreReasoner - alimente le timer + ETA + itérations
            if ev == "pre_reasoning_done":
                state["pre_mode"] = event.get("mode")
                state["planned_iterations"] = event.get("n_iterations")
                state["eta_sec"] = event.get("estimated_duration_sec")
                state["pre_forced"] = bool(event.get("is_forced"))
                reason = event.get("reason", "")
                state["detail"] = f"plan={state['pre_mode']} · {reason}"
                if verbose_trace:
                    _push_list("options", f"PreReasoner: {state['pre_mode']} · {reason}", 8)

            if ev == "multiloop_iteration_start":
                state["iteration"] = int(event.get("iteration", 0) or 0)
                state["max_iterations"] = int(event.get("max_iterations", 0) or 0)
                state["detail"] = "Generation et critique des candidats"
            elif ev == "multiloop_candidate_scored" and cinematic:
                cand = int(event.get("candidate", 0) or 0)
                total = int(event.get("num_candidates", 0) or 0)
                score = event.get("score")
                if isinstance(score, (int, float)):
                    state["detail"] = f"candidat {cand}/{total} evalue a {score:.1f}/10"
                else:
                    state["detail"] = f"candidat {cand}/{total} evalue"
            elif ev == "multiloop_iteration_end":
                state["best_score"] = event.get("best_score")
                state["detail"] = "Meilleur candidat retenu pour ce tour"
            elif ev == "multi_objective_item_done":
                idx = int(event.get("index", 0) or 0)
                intent = str(event.get("intent", ""))
                state["detail"] = f"objectif #{idx} termine ({intent})"
            elif ev == "abstraction_done":
                intent = event.get("intent")
                state["detail"] = f"intent detecte: {intent}"
            elif ev == "meta_reasoning_done":
                strategy = event.get("strategy")
                state["detail"] = f"strategie: {strategy}"
                if verbose_trace and strategy:
                    _push_list("options", f"Strategie retenue: {strategy}", 8)
            elif ev == "spectral_compute_done":
                has_error = bool(event.get("has_error"))
                state["detail"] = "calcul spectral termine" if not has_error else "calcul spectral avec incident"
            elif ev == "intent_hypotheses":
                candidates = event.get("candidates")
                if isinstance(candidates, list) and candidates:
                    state["detail"] = "candidats intent: " + ", ".join(str(c) for c in candidates[:4])
                    if verbose_trace:
                        _push_list("options", "Intents candidats: " + ", ".join(str(c) for c in candidates[:4]), 8)
            elif ev == "assumptions_detected":
                assumptions = event.get("assumptions")
                if isinstance(assumptions, list) and assumptions:
                    state["detail"] = assumptions[0]
                    if verbose_trace:
                        for a in assumptions:
                            _push_list("assumptions", str(a), 8)
            elif ev == "decision_gate":
                strategy = str(event.get("strategy", ""))
                goal_intent = str(event.get("goal_intent", ""))
                needs_comp = bool(event.get("needs_computation"))
                model = str(event.get("model", ""))
                state["detail"] = (
                    f"route={goal_intent or 'general'} | calcul={'oui' if needs_comp else 'non'} | modele={model}"
                )
                if verbose_trace:
                    _push_list("options", f"Arbitrage: {strategy} -> {goal_intent}", 8)
            elif ev == "spectral_parse_strategy":
                detail = str(event.get("detail", "")).strip()
                strategy = str(event.get("strategy", "")).strip()
                state["detail"] = detail or strategy or "strategie d'interpretation appliquee"
                if verbose_trace:
                    _push_list("options", f"Parser: {strategy} ({detail})", 8)
            elif ev == "pipeline_done":
                mode = event.get("mode")
                state["detail"] = f"mode final: {mode}"
            elif ev == "wrapper_done":
                mode = event.get("mode")
                state["detail"] = f"route finale: {mode}"

            if verbose_trace:
                msg = state.get("detail")
                if isinstance(msg, str) and msg.strip():
                    _push_list("recent_events", f"{state.get('phase', '')}: {msg.strip()}", 12)

            live = live_handle[0]
            if live is not None:
                live.update(self._render_live_progress_panel(state), refresh=True)

        return _on_progress

    async def interactive_mode(self) -> None:
        self.banner()
        # Installation des raccourcis clavier (readline) + historique persistant
        kb = install_keybindings(history_file="data/.gabriel_history")
        # Affichage du statut CI dans l'en-tete d'ouverture (tests pytest locaux)
        console.print("  [dim]Verification de la suite de tests (pytest local)...[/dim]")
        try:
            ci_summary = run_pytest_local(timeout_s=60)
            status_line = (
                f"  [bold]Statut CI Gabriel :[/bold] "
                f"[{ci_summary.style}]{ci_summary.badge}[/{ci_summary.style}] "
                f"[dim](pytest local, {ci_summary.duration_s:.2f}s - tapez 'ci' pour le rapport detaille)[/dim]"
            )
        except Exception as exc:
            logger.warning("Impossible d'executer pytest a l'ouverture : %s", exc)
            status_line = "  [yellow]Statut CI Gabriel : indisponible (pytest a echoue au demarrage)[/yellow]"
        console.print(status_line)
        # Statut clavier
        if kb._installed:
            console.print(
                "  [dim]Raccourcis clavier actifs (Tab=completion, Ctrl+R=recherche, "
                "Up/Down=historique). Tapez 'commandes' pour tout voir.[/dim]"
            )
        console.print(
            Panel(
                Text.assemble(
                    ("  Agent pret  -  ", "bold bright_green"),
                    (f"Bonjour {self.user_name} !\n", "bold bright_white"),
                    ("  Tapez ", "dim"),
                    ("'aide'", "bold cyan"),
                    (" pour le menu rapide, ", "dim"),
                    ("'commandes'", "bold cyan"),
                    (" pour tout voir, ", "dim"),
                    ("'quitter'", "bold cyan"),
                    (" pour sortir.\n", "dim"),
                    ("  Decouverte guidee : ", "dim"),
                    ("ask", "bold magenta"),
                    (" / ", "dim"),
                    ("ask type", "bold magenta"),
                    (" / ", "dim"),
                    ("ask rules", "bold magenta"),
                ),
                border_style="bright_green",
                padding=(0, 2),
            )
        )
        console.print()

        while True:
            try:
                user_input = console.input(f"\n[bold magenta]{self.user_name} >[/bold magenta] ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print(f"\n\n  Au revoir {self.user_name} !", style="bold green")
                _save_kb_history()
                break

            if not user_input:
                continue
            if user_input.lower() in {"quitter", "exit", "quit", "q", ":q"}:
                console.print(f"\n  Au revoir {self.user_name} !", style="bold green")
                _save_kb_history()
                break

            if await self._handle_special(user_input):
                continue

            # v3.34 : Parse commandes d'override /rapide /standard /approfondi /complet
            from ..multiloop.pre_reasoner import parse_cli_force_mode
            forced_mode, user_input = parse_cli_force_mode(user_input)
            if not user_input:
                console.print(
                    "\n  [yellow]Mode forcé demandé sans question. "
                    "Utilisez `/rapide <votre question>` par exemple.[/yellow]\n"
                )
                continue

            try:
                # Limite de longueur pour eviter des requetes monstrueuses
                # (compatible avec la limite du mode debug : 1600 + 400 = 2000)
                if len(user_input) > MAX_REQUEST_CHARS + MAX_COMMENT_CHARS:
                    console.print(
                        f"\n  [yellow][Requete trop longue] "
                        f"{len(user_input)} caracteres (max {MAX_REQUEST_CHARS + MAX_COMMENT_CHARS}). "
                        f"Reformulez plus brievement ou utilisez 'debug \"<question>\"' "
                        f"pour ajouter un commentaire structure.[/yellow]\n"
                    )
                    continue
                live_trace = self._env_enabled("GABRIEL_LIVE_TRACE", default=True)
                cinematic = self._env_enabled("GABRIEL_CINEMATIC", default=True)
                verbose_trace = self._env_enabled("GABRIEL_TRACE_VERBOSE", default=True)

                if not live_trace:
                    console.print("\n  [dim]Reflexion en cours (multi-loop self-critique)...[/dim]")
                    answer = await self.orchestrator.ask(user_input, force_mode=forced_mode)
                else:
                    progress_state: dict[str, object] = {
                        "phase": "Initialisation",
                        "detail": "Preparation de la requete",
                        "iteration": 0,
                        "max_iterations": 0,
                        "best_score": None,
                        "verbose_trace": verbose_trace,
                        "assumptions": [],
                        "options": [],
                        "recent_events": [],
                        # v3.34 : timer temps réel + ETA + itérations planifiées
                        "start_ts": time.time(),
                        "eta_sec": None,
                        "planned_iterations": None,
                        "pre_mode": None,
                        "pre_forced": bool(forced_mode is not None),
                    }
                    live_handle: list[Live | None] = [None]
                    progress_cb = self._make_progress_callback(
                        progress_state,
                        live_handle,
                        cinematic=cinematic,
                        verbose_trace=verbose_trace,
                    )
                    with Live(
                        self._render_live_progress_panel(progress_state),
                        console=console,
                        refresh_per_second=8,
                        transient=True,
                    ) as live:
                        live_handle[0] = live

                        # v3.34 : tache de rafraichissement du timer (2 Hz)
                        # pour que le chrono avance meme entre 2 events pipeline
                        stop_flag = {"stop": False}

                        async def _tick_timer():
                            while not stop_flag["stop"]:
                                try:
                                    live.update(
                                        self._render_live_progress_panel(progress_state),
                                        refresh=False,
                                    )
                                except Exception:
                                    pass
                                await asyncio.sleep(0.5)

                        tick_task = asyncio.create_task(_tick_timer())
                        try:
                            answer = await self.orchestrator.ask(
                                user_input,
                                progress_cb=progress_cb,
                                force_mode=forced_mode,
                            )
                        finally:
                            stop_flag["stop"] = True
                            try:
                                await asyncio.wait_for(tick_task, timeout=1.0)
                            except (asyncio.TimeoutError, Exception):
                                tick_task.cancel()
                self._display_answer(answer)
            except Exception as exc:
                logger.error("Erreur traitement : %s", exc, exc_info=True)
                console.print(f"\n  [red][Erreur] {exc}[/red]\n")


def run_cli() -> None:
    """Point d'entree synchrone."""
    cli = CLIInterface()
    asyncio.run(cli.interactive_mode())
