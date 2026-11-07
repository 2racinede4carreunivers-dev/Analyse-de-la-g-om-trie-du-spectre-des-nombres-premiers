"""
DebugSession — Mode debugger manuel interactif (terminal).

Active par la commande CLI `debug "<question>"`.

Flux interactif :
  1. Valide la longueur de la requete (max 1600 caracteres).
  2. Decompose la requete et affiche les segments avec lettres A..Z.
  3. Boucle interactive :
       [A..Z]   bascule un segment entre garde ✓ et bypass ✗
       c        ajoute un commentaire a la requete (max 400 caracteres)
       r        recalcule decomposition apres modifications
       e        execute le debugger avec la configuration courante
       q        annule et retourne au prompt principal
  4. Affiche la timeline + reponse certifiee.

Limites strictes :
  - Requete initiale : 1600 caracteres max
  - Commentaire : 400 caracteres max (un seul commentaire cumulatif)
  - Total combine : 2000 caracteres max (1600 + 400)
  Ces limites empechent qu'un commentaire ajoute change le sens de la
  requete au point de re-declencher une autre boucle d'incoherence.
"""
from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..adapters.corpus.certainty_kernel import CertaintyKernel
from ..audit import AuditStore
from ..core.spectral_core import SpectralMethodCore
from ..core.spectral_types import CandidateAnswer, FinalAnswer
from ..debug_toolkit import (
    MpmathValidator, SympyValidator, ToolkitRegistry, Z3Prover,
)
from ..multiloop.coherence_detector import CoherenceDetector, CoherenceReport
from ..multiloop.request_decomposer import (
    DecomposedRequest, RequestDecomposer, Segment,
)
from ..multiloop.slow_motion_debugger import SlowMotionDebugger


MAX_REQUEST_CHARS = 1600
MAX_COMMENT_CHARS = 400


@dataclass
class _DebugState:
    """Etat mutable d'une session de debug."""
    base_question: str
    comment: str = ""
    # Pour chaque segment de la decomposition, etat "bypass force" par lettre
    # True = forcer bypass (segment ignore meme s'il etait coherent)
    # False = laisser etat initial (cohérent ou incoherent selon le decomposer)
    forced_bypass: dict[str, bool] = field(default_factory=dict)
    # Rapports collectes par la commande 't' (toolkit) au cours de la session
    last_toolkit_reports: dict[str, Any] = field(default_factory=dict)

    @property
    def combined_question(self) -> str:
        """Concatene la requete initiale + commentaire eventuel."""
        if self.comment.strip():
            return f"{self.base_question.strip()} ({self.comment.strip()})"
        return self.base_question.strip()


class DebugSession:
    """
    Session interactive de debugger manuel ralenti.
    
    Utilisation :
        session = DebugSession(console)
        await session.run("Reconstruis le 26eme premier en rapport 1/2 avec n=10")
    """

    def __init__(
        self,
        console: Console,
        certainty_kernel: Optional[CertaintyKernel] = None,
        spectral_core: Optional[SpectralMethodCore] = None,
        audit_store: Optional[AuditStore] = None,
    ):
        self.console = console
        self.kernel = certainty_kernel or CertaintyKernel()
        self.core = spectral_core or SpectralMethodCore()
        self.audit_store = audit_store
        self.decomposer = RequestDecomposer()
        self.detector = CoherenceDetector(threshold=0.99)  # toujours actif en mode manuel
        self.debugger = SlowMotionDebugger(
            certainty_kernel=self.kernel,
            spectral_core=self.core,
            audit_store=self.audit_store,
        )
        # Toolkit de vrais debuggers (lazy : registry detecte ce qui est installe)
        self.toolkit_registry = ToolkitRegistry()
        self._sympy: Optional[SympyValidator] = None
        self._mpmath: Optional[MpmathValidator] = None
        self._z3: Optional[Z3Prover] = None

    # ---------- Validation des limites ----------

    @staticmethod
    def validate_question_length(question: str) -> tuple[bool, str]:
        n = len(question)
        if n == 0:
            return False, "Requete vide."
        if n > MAX_REQUEST_CHARS:
            return False, (
                f"Requete trop longue : {n} caracteres "
                f"(maximum autorise : {MAX_REQUEST_CHARS}). "
                f"En mode debug, jusqu'a {MAX_COMMENT_CHARS} caracteres "
                f"supplementaires peuvent etre ajoutes via la commande 'c'."
            )
        return True, ""

    @staticmethod
    def validate_comment_length(comment: str) -> tuple[bool, str]:
        n = len(comment)
        if n > MAX_COMMENT_CHARS:
            return False, (
                f"Commentaire trop long : {n}/{MAX_COMMENT_CHARS} caracteres. "
                f"Raccourcissez pour preserver le sens de la requete initiale."
            )
        return True, ""

    # ---------- Affichage ----------

    def _print_header(self, state: _DebugState) -> None:
        chars = len(state.base_question)
        com_chars = len(state.comment)
        title = (
            f"[bold yellow]MODE DEBUG MANUEL[/bold yellow]  "
            f"requete={chars}/{MAX_REQUEST_CHARS}ch  "
            f"commentaire={com_chars}/{MAX_COMMENT_CHARS}ch"
        )
        body = state.base_question
        if state.comment:
            body += f"\n\n[dim]+ commentaire :[/dim] {state.comment}"
        self.console.print(Panel(body, title=title, border_style="yellow"))

    def _print_decomposition(
        self,
        decomposed: DecomposedRequest,
        letters: list[str],
        state: _DebugState,
    ) -> None:
        table = Table(
            title="[bold]Decomposition pedagogique[/bold]",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
        )
        table.add_column("Lettre", justify="center", style="bold")
        table.add_column("Etat", justify="center")
        table.add_column("Type", style="magenta")
        table.add_column("Valeur")
        table.add_column("Note", style="dim")

        for letter, seg in zip(letters, decomposed.segments):
            forced = state.forced_bypass.get(letter, False)
            effective_coherent = seg.coherent and not forced
            if effective_coherent:
                state_marker = "[green]GARDE ✓[/green]"
            else:
                state_marker = "[red]BYPASS ✗[/red]"
            note = seg.reason if seg.reason else ""
            if forced and seg.coherent:
                note = "(bypass manuel)"
            table.add_row(letter, state_marker, seg.kind, str(seg.value), note)

        self.console.print(table)
        # Resume intent/ratio
        info = (
            f"[dim]intent[/dim] = [cyan]{decomposed.detected_intent}[/cyan]   "
            f"[dim]ratio[/dim] = [cyan]{decomposed.detected_ratio or 'aucun'}[/cyan]"
        )
        self.console.print(info)

    def _print_menu(self) -> None:
        menu = (
            "[bold]Actions disponibles[/bold] :\n"
            "  [bold magenta][A-Z][/bold magenta]  bascule le segment correspondant (GARDE <-> BYPASS)\n"
            "  [bold magenta]c[/bold magenta]      ajoute / remplace le commentaire (max 400 caracteres)\n"
            "  [bold magenta]r[/bold magenta]      re-decompose apres ajout du commentaire\n"
            "  [bold magenta]t[/bold magenta]      lance le toolkit (sympy / mpmath / z3) sur la position courante\n"
            "  [bold magenta]e[/bold magenta]      execute le debugger avec la configuration actuelle\n"
            "  [bold magenta]q[/bold magenta]      annule et retourne au prompt principal"
        )
        self.console.print(Panel(menu, border_style="dim", title="[dim]Menu[/dim]"))

    def _print_canonical_preview(self, decomposed: DecomposedRequest, state: _DebugState, letters: list[str]) -> None:
        # On simule l'effet du bypass force pour la preview
        effective = DecomposedRequest(original=decomposed.original)
        effective.detected_intent = decomposed.detected_intent
        effective.detected_ratio = decomposed.detected_ratio
        effective.tuple_A = decomposed.tuple_A
        effective.tuple_B = decomposed.tuple_B
        effective.config_size = decomposed.config_size
        for letter, seg in zip(letters, decomposed.segments):
            new_seg = Segment(
                kind=seg.kind, text=seg.text, value=seg.value,
                coherent=seg.coherent and not state.forced_bypass.get(letter, False),
                reason=seg.reason,
            )
            effective.segments.append(new_seg)
        canonical = self.debugger._rewrite_canonical(effective)
        self.console.print(
            Panel(
                canonical,
                title="[green]Apercu de la requete canonique[/green]",
                border_style="green",
            )
        )

    # ---------- Boucle interactive ----------

    async def run(self, question: str) -> Optional[FinalAnswer]:
        """
        Lance la session de debug manuel sur une question donnee.
        
        Returns:
            FinalAnswer si l'utilisateur execute (e), None s'il annule (q).
        """
        ok, err = self.validate_question_length(question)
        if not ok:
            self.console.print(f"[red]{err}[/red]")
            return None

        state = _DebugState(base_question=question.strip())

        while True:
            # Re-decomposer a chaque iteration pour refleter le commentaire
            decomposed = self.decomposer.decompose(state.combined_question)
            letters = list(string.ascii_uppercase[:len(decomposed.segments)])

            self.console.print()  # blank line
            self._print_header(state)
            self._print_decomposition(decomposed, letters, state)
            self._print_canonical_preview(decomposed, state, letters)
            self._print_menu()

            try:
                choice = self.console.input("\n[bold yellow]debug>[/bold yellow] ").strip()
            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[dim]Annulation.[/dim]")
                return None

            if not choice:
                continue

            # Action lettre : toggle segment (UNIQUEMENT en majuscule strict)
            # Les minuscules sont reservees aux commandes (c, e, q, r).
            if len(choice) == 1 and choice in letters:
                state.forced_bypass[choice] = not state.forced_bypass.get(choice, False)
                continue

            cmd = choice.lower()

            if cmd == "q":
                self.console.print("[dim]Mode debug annule. Retour au prompt principal.[/dim]")
                return None

            if cmd == "c":
                self.console.print(
                    f"[dim]Tapez le commentaire (max {MAX_COMMENT_CHARS} caracteres). "
                    f"Vide = effacer le commentaire actuel.[/dim]"
                )
                try:
                    new_comment = self.console.input("[yellow]commentaire>[/yellow] ").strip()
                except (EOFError, KeyboardInterrupt):
                    continue
                ok, err = self.validate_comment_length(new_comment)
                if not ok:
                    self.console.print(f"[red]{err}[/red]")
                    continue
                state.comment = new_comment
                self.console.print(f"[green]Commentaire mis a jour ({len(new_comment)} caracteres).[/green]")
                continue

            if cmd == "r":
                # On re-decompose au prochain tour de boucle (deja le cas)
                self.console.print("[dim]Re-decomposition...[/dim]")
                continue

            if cmd == "t":
                # Stocke les rapports toolkit pour les inclure dans l'audit final
                state.last_toolkit_reports = self._run_toolkit(decomposed)
                continue

            if cmd == "e":
                return await self._execute(state, decomposed, letters)

            self.console.print(f"[red]Commande inconnue : '{choice}'[/red]")

    # ---------- Toolkit (vrais debuggers : sympy, mpmath, z3) ----------

    def _run_toolkit(self, decomposed: DecomposedRequest) -> dict[str, Any]:
        """
        Lance les vrais outils de verification sur la position deduite.
        Retourne un dict des rapports collectes (pour audit ulterieur).
        Si position absente -> affiche juste l'etat du toolkit.
        """
        # Etat du toolkit
        self.console.print(Panel(
            self.toolkit_registry.render_table(),
            title="[cyan]Toolkit installe[/cyan]",
            border_style="cyan",
        ))

        # Trouve position et ratio
        position = None
        ratio = decomposed.detected_ratio or "1/2"
        for s in decomposed.coherent_segments:
            if s.kind == "position":
                position = s.value
                break
        collected: dict[str, Any] = {}
        if position is None:
            self.console.print(
                "[yellow]Aucune position detectee dans la requete -> "
                "le toolkit affiche uniquement son etat.[/yellow]"
            )
            return collected

        # Prime attendu pour cross-validation
        from ..spectral.prime_table import nth_prime
        expected_prime = nth_prime(position)

        self.console.print(
            f"\n[bold]Validation croisee pour position={position}, ratio={ratio}, "
            f"prime_attendu={expected_prime}[/bold]\n"
        )

        # 1. sympy
        if self.toolkit_registry.is_available("sympy"):
            if self._sympy is None:
                self._sympy = SympyValidator()
            report = self._sympy.validate(position, ratio, expected_prime)
            collected["sympy"] = report
            self.console.print(Panel(
                self._sympy.render(report),
                title="[green]sympy : validation symbolique[/green]",
                border_style="green",
            ))

        # 2. mpmath
        if self.toolkit_registry.is_available("mpmath"):
            if self._mpmath is None:
                self._mpmath = MpmathValidator()
            report = self._mpmath.validate(position, ratio, expected_prime)
            collected["mpmath"] = report
            self.console.print(Panel(
                self._mpmath.render(report),
                title="[blue]mpmath : precision arbitraire[/blue]",
                border_style="blue",
            ))

        # 3. z3
        if self.toolkit_registry.is_available("z3"):
            if self._z3 is None:
                self._z3 = Z3Prover()
            report = self._z3.validate(position, ratio, expected_prime)
            collected["z3"] = report
            self.console.print(Panel(
                self._z3.render(report),
                title="[magenta]z3 : preuve formelle SMT[/magenta]",
                border_style="magenta",
            ))

        return collected

    async def verifier_position(self, position: int, ratio: str = "1/2") -> Optional[str]:
        """
        Commande CLI directe : lance le toolkit et cree un audit citable
        SANS passer par toute la session interactive.
        
        Returns:
            L'id de l'audit cree (ou None si echec).
        """
        if ratio != "1/2":
            self.console.print(
                f"[yellow]La commande 'verifier' supporte uniquement le rapport 1/2 "
                f"pour le moment (recu : {ratio}).[/yellow]"
            )
            return None
        from ..spectral.prime_table import nth_prime
        expected_prime = nth_prime(position)
        if expected_prime is None:
            self.console.print(f"[red]Position {position} hors table (1..1000).[/red]")
            return None
        # Construit une DecomposedRequest minimale
        dec = DecomposedRequest(
            original=f"verifier {position} {ratio}",
            detected_intent="reconstruction",
            detected_ratio=ratio,
        )
        dec.segments.append(Segment(
            kind="position", text=f"{position}", value=position, coherent=True,
        ))
        dec.segments.append(Segment(
            kind="ratio", text=ratio, value=ratio, coherent=True,
        ))
        toolkit_reports = self._run_toolkit(dec)
        # Sauvegarde l'audit si store disponible
        if self.audit_store is None:
            self.console.print("[yellow]Audit non sauvegarde (audit_store absent).[/yellow]")
            return None
        try:
            citations = [
                "methode_spectral.thy::prime_equation_identity",
                "geometrie_spectre_premier.thy::reconstruction_P",
                "plan_cognitif::INVARIANT_1_2",
            ]
            record = AuditStore.build_record(
                intervention_type="verifier",
                question=f"verifier {position} {ratio}",
                certified_answer=(
                    f"Le {position}-eme nombre premier est {expected_prime}. "
                    f"En rapport {ratio}, n = {position} (INVARIANT)."
                ),
                position=position,
                prime_value=expected_prime,
                citations_thy=citations,
                toolkit_reports=toolkit_reports,
                ratio=ratio,
            )
            path = self.audit_store.save(record)
            self.console.print(
                f"\n[green]Audit cree : id={record.id}  ->  {path.name}[/green]"
            )
            self.console.print(
                f"[dim]Pour citer cet audit : tapez 'citer {record.id}'[/dim]\n"
            )
            return record.id
        except Exception as exc:
            self.console.print(f"[red]Erreur lors de la sauvegarde de l'audit : {exc}[/red]")
            return None

    # ---------- Exécution finale ----------

    async def _execute(
        self,
        state: _DebugState,
        decomposed: DecomposedRequest,
        letters: list[str],
    ) -> FinalAnswer:
        """Construit la decomposition effective et lance le SlowMotionDebugger."""
        # On reconstruit une DecomposedRequest avec le bypass force applique
        effective = DecomposedRequest(original=state.combined_question)
        effective.detected_intent = decomposed.detected_intent
        effective.detected_ratio = decomposed.detected_ratio
        # Preserve tuples et config_size pour le ratio_spectral_nxn
        effective.tuple_A = decomposed.tuple_A
        effective.tuple_B = decomposed.tuple_B
        effective.config_size = decomposed.config_size
        for letter, seg in zip(letters, decomposed.segments):
            new_seg = Segment(
                kind=seg.kind, text=seg.text, value=seg.value,
                coherent=seg.coherent and not state.forced_bypass.get(letter, False),
                reason=seg.reason or ("bypass manuel" if state.forced_bypass.get(letter) else ""),
            )
            effective.segments.append(new_seg)

        # Construit un FinalAnswer "vide" et un report toujours-incoherent
        # (en mode manuel, le user a explicitement demande le debugger)
        final = FinalAnswer(
            question_id="debug-manual",
            answer_text="(en cours de generation par le debugger manuel)",
            structured_data={},
            confidence=0.0,
            iterations_used=0,
            best_score=0.0,
            candidates=[CandidateAnswer(
                iteration=0, text="", structured_data={}, used_engines=["debug"],
                score=0.0, critique="mode manuel",
            )],
            explanation="",
        )
        manual_report = CoherenceReport(
            score=0.0,
            incoherent=True,
            signals=["mode_debug_manuel"],
            best_candidate_score=0.0,
        )

        # On contourne le decomposer en injectant directement notre version
        # via un monkey-patch local : sauvegarde -> remplace -> appel -> restaure
        original_decompose = self.debugger.decomposer.decompose
        self.debugger.decomposer.decompose = lambda _q: effective

        try:
            result = self.debugger.debug(
                question=state.combined_question,
                final=final,
                coherence_report=manual_report,
                precomputed_facts=None,
                skip_auto_audit=True,   # on cree notre propre audit "debug_manual"
            )
        finally:
            self.debugger.decomposer.decompose = original_decompose

        # Annoter le resultat avec le commentaire et l'intervention manuelle
        result.structured_data["manual_debug"] = True
        if state.comment:
            result.structured_data["user_comment"] = state.comment
        forced_list = [l for l, v in state.forced_bypass.items() if v]
        result.structured_data["forced_bypass"] = forced_list

        # Sauvegarde de l'audit "debug_manual" avec toutes les infos saisies
        if self.audit_store is not None:
            certified = result.structured_data.get("certified", {})
            timeline_data = result.structured_data.get("debug_timeline", [])
            # Reconstitue un DebugTimeline-like pour passer au _maybe_save_audit
            try:
                record = AuditStore.build_record(
                    intervention_type="debug_manual",
                    question=state.combined_question,
                    certified_answer=result.answer_text,
                    position=self._extract_position_from_segments(effective),
                    prime_value=certified.get("value"),
                    decomposition=result.structured_data.get("decomposition", {}),
                    timeline=timeline_data,
                    citations_thy=certified.get("citations", []),
                    toolkit_reports=state.last_toolkit_reports or {},
                    user_comment=state.comment if state.comment else None,
                    forced_bypass=forced_list,
                    ratio=effective.detected_ratio or "1/2",
                )
                path = self.audit_store.save(record)
                result.structured_data["audit_id"] = record.id
                result.structured_data["audit_path"] = str(path)
                self.console.print(
                    f"\n[green]Audit cree : id={record.id}  ->  {path.name}[/green]"
                )
                self.console.print(
                    f"[dim]Pour citer cet audit : tapez 'citer {record.id}'[/dim]\n"
                )
            except ValueError as exc:
                # ratio non-1/2 -> on saute silencieusement (en v1)
                self.console.print(f"[dim]{exc}[/dim]")
            except Exception as exc:
                self.console.print(f"[red]Audit non sauve : {exc}[/red]")
        return result

    @staticmethod
    def _extract_position_from_segments(dec: DecomposedRequest) -> Optional[int]:
        for s in dec.segments:
            if s.kind == "position" and s.coherent:
                try:
                    return int(s.value)
                except (TypeError, ValueError):
                    return None
        return None

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
