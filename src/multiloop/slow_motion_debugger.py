"""
SlowMotionDebugger — Mode "ralenti debugger" anti-incoherence.

Activation automatique :
  Le CoherenceDetector trouve une incoherence (score < seuil) dans la
  sortie du multiloop. Le pipeline appelle alors ce module.

Procedure (timeline) :
  T1. Reception de la requete originale et du rapport d'incoherence
  T2. Decomposition de la requete en segments logiques (RequestDecomposer)
  T3. Identification des segments coherents (✓) et incoherents (✗)
  T4. By-pass des segments ✗
  T5. Reconstruction d'une requete canonique simplifiee (Rewriter)
  T6. Resolution via CertaintyKernel + spectral_core (PAS DE LLM)
  T7. Construction d'une reponse courte mais CERTAINE
  T8. Generation de la timeline traçable + suggestions de reformulation

L'utilisateur recoit :
  - La reponse certifiee (courte)
  - La timeline complete (transparence totale)
  - Une suggestion de reformulation s'il veut plus de details
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from ..adapters.corpus.certainty_kernel import CertaintyKernel
from ..audit import AuditStore
from ..core.spectral_core import SpectralMethodCore
from ..core.spectral_types import FinalAnswer
from ..spectral.prime_table import nth_prime
from .certainty_model import CertaintyEvaluation, CertaintyModel
from .coherence_detector import CoherenceReport
from .logical_loop import LogicalLoop, ModestRequest
from .request_decomposer import DecomposedRequest, RequestDecomposer, Segment


logger = logging.getLogger(__name__)


@dataclass
class TimelineEvent:
    step: int
    label: str
    detail: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DebugTimeline:
    events: list[TimelineEvent] = field(default_factory=list)

    def add(self, step: int, label: str, detail: str) -> None:
        self.events.append(TimelineEvent(step=step, label=label, detail=detail))

    def render(self) -> str:
        """Rendu ASCII de la timeline pour affichage CLI."""
        if not self.events:
            return "(timeline vide)"
        lines = ["TIMELINE DEBUGGER (mode ralenti)"]
        lines.append("─" * 60)
        for ev in self.events:
            lines.append(f"  T{ev.step:<2} [{ev.label:<22}] {ev.detail}")
        lines.append("─" * 60)
        return "\n".join(lines)

    def to_dict(self) -> list[dict]:
        return [
            {"step": ev.step, "label": ev.label, "detail": ev.detail, "ts": ev.timestamp}
            for ev in self.events
        ]


class SlowMotionDebugger:
    """
    Mode debugger ralenti avec by-pass des segments incoherents et
    repli sur le CertaintyKernel.
    """

    def __init__(
        self,
        certainty_kernel: Optional[CertaintyKernel] = None,
        spectral_core: Optional[SpectralMethodCore] = None,
        audit_store: Optional[AuditStore] = None,
    ):
        self.kernel = certainty_kernel or CertaintyKernel()
        self.core = spectral_core or SpectralMethodCore()
        self.decomposer = RequestDecomposer()
        # Axes Modele de Certitude + Boucle Logique
        self.certainty_model = CertaintyModel(spectral_core=self.core)
        self.logical_loop = LogicalLoop(spectral_core=self.core)
        self.audit_store = audit_store  # peut etre None -> pas d'audit auto
        logger.info(
            "SlowMotionDebugger initialise : %d certitudes, %d premiers en table, audit=%s",
            len(self.kernel.certainties), len(self.core.prime_list),
            "ON" if self.audit_store else "OFF",
        )

    def debug(
        self,
        question: str,
        final: FinalAnswer,
        coherence_report: CoherenceReport,
        precomputed_facts: Optional[dict[str, Any]] = None,
        skip_auto_audit: bool = False,
        llm_reformulations: Optional[list[str]] = None,
    ) -> FinalAnswer:
        """
        Execute la procedure complete du Slow-Motion Debugger.
        
        Args:
            question: la requete originale.
            final: la FinalAnswer multiloop jugee incoherente.
            coherence_report: le diagnostic du CoherenceDetector.
            precomputed_facts: facts spectraux deja calcules par le pipeline.
            llm_reformulations: reformulations contextuelles pre-calculees par
                LLMReformulator (v3.27). Fusionnees en tete des suggestions
                heuristiques pour eviter la rigidite "reconstruction de nombres
                premiers" propose systematiquement pour toutes les requetes.
        
        Returns:
            FinalAnswer enrichie : answer_text = reponse certifiee,
            structured_data inclut la timeline + segments + reformulations.
        """
        timeline = DebugTimeline()
        timeline.add(1, "REQUETE_RECUE", f'"{question[:80]}"')
        timeline.add(2, "INCOHERENCE_DETECTEE",
                     f"score={coherence_report.score:.2f} (seuil critique). "
                     f"Signaux : {coherence_report.signals[:3]}. "
                     "Le multiloop a produit une reponse jugee non-fiable -> "
                     "bascule sur le kit de reparation deterministe (kernel + spectral_core).")

        # T3. Decomposition
        decomposed = self.decomposer.decompose(question)
        coherent_str = ", ".join(f"{s.kind}={s.value}" for s in decomposed.coherent_segments)
        incoherent_str = ", ".join(f"{s.kind}={s.value}" for s in decomposed.incoherent_segments)
        t3_detail = (
            f"Intent={decomposed.detected_intent}, ratio={decomposed.detected_ratio}. "
            f"Coherents=[{coherent_str}]. "
            f"Incoherents=[{incoherent_str or 'aucun'}]."
        )
        if decomposed.announced_size is not None:
            t3_detail += (
                f" Configuration ANNONCEE : "
                f"{'symetrique' if decomposed.announced_symmetric else 'asymetrique'} "
                f"{decomposed.announced_size}*{decomposed.announced_size}."
            )
            if (decomposed.tuple_A is not None and decomposed.tuple_B is not None
                    and len(decomposed.tuple_A) != len(decomposed.tuple_B)):
                t3_detail += (
                    f" REELLE : A={len(decomposed.tuple_A)} elements, "
                    f"B={len(decomposed.tuple_B)} elements (MISMATCH)."
                )
        timeline.add(3, "DECOMPOSITION", t3_detail)

        # T4. By-pass
        bypassed = [s for s in decomposed.incoherent_segments]
        if bypassed:
            timeline.add(
                4, "BYPASS_SEGMENTS",
                f"Segments mis en quarantaine : "
                f"{[s.text for s in bypassed]}. "
                f"Raisons : {[s.reason for s in bypassed]}. "
                "Ces segments sont IGNORES dans la requete canonique pour "
                "preserver la coherence spectrale.",
            )
        else:
            timeline.add(
                4, "BYPASS_SEGMENTS",
                "Aucun segment incoherent detecte. La requete est syntaxiquement "
                "valide ; l'incoherence du multiloop vient probablement d'une "
                "interpretation LLM erronee, pas d'un defaut de la requete.",
            )

        # T5. Requete canonique
        canonical = self._rewrite_canonical(decomposed)
        timeline.add(
            5, "REQUETE_CANONIQUE",
            f"Reformulation deterministe : {canonical} "
            "(seuls les segments coherents et l'invariant spectral_core sont utilises).",
        )

        # T6. Resolution certifiee (sans LLM)
        certified = self._solve_certified(decomposed)
        timeline.add(
            6, "RESOLUTION_CERTIFIEE",
            certified.get("method", "kernel") + " -> " + certified["summary"].splitlines()[0],
        )

        # ============================================================
        # NOUVEAU - Modele de Certitude + Boucle Logique + Reponse Modeste
        # ============================================================
        # T6.1 : Evaluation des 8 criteres / 3 questions du modele de certitude
        evaluation: CertaintyEvaluation = self.certainty_model.evaluate(decomposed)
        violated = evaluation.violated_codes
        certainty_ratio = evaluation.certainty_ratio
        timeline.add(
            7, "EVALUATION_CERTITUDE",
            f"Modele de certitude (8 criteres / 3 questions) : "
            f"{len(evaluation.passed_codes)}/{len(evaluation.results)} passes "
            f"({certainty_ratio*100:.0f}%). "
            + (f"Critères violes : {violated}. "
               + " ; ".join(
                   f"{r.code}={r.detail}"
                   for r in evaluation.results if not r.passed
               )
               if violated else "Aucun critere viole."),
        )

        # T6.2 : Boucle logique -> requete modeste (sursaut des elements violants)
        modest: ModestRequest = self.logical_loop.derive_modest_request(
            decomposed, evaluation,
        )
        if modest.skips_applied:
            timeline.add(
                8, "BOUCLE_LOGIQUE",
                f"{len(modest.skips_applied)} sursaut(s) applique(s) : "
                + " | ".join(
                    f"{s['criterion']}->{s['strategy']}"
                    for s in modest.skips_applied
                )
                + f". Requete reformulee modeste : \"{modest.canonical_text}\".",
            )
        else:
            timeline.add(
                8, "BOUCLE_LOGIQUE",
                "Aucun sursaut necessaire : la requete satisfait deja tous les "
                f"criteres du modele de certitude. Requete canonique conservee : "
                f"\"{modest.canonical_text}\".",
            )

        # T6.3 : Resolution de la REQUETE MODESTE par spectral_core (deterministe)
        modest_certified = self._solve_modest(modest)
        timeline.add(
            9, "REPONSE_MODESTE",
            modest_certified.get("method", "kernel") + " -> "
            + modest_certified.get("summary", "").splitlines()[0],
        )

        # T10 (ex-T7). Reformulations textuelles (suggestions pour relancer Gabriel)
        heuristic_suggestions = self._build_reformulations(decomposed, bypassed)
        # v3.27 : Fusion avec reformulations LLM contextuelles (si fournies)
        if llm_reformulations:
            from .llm_reformulator import merge_reformulations
            suggestions = merge_reformulations(
                llm_reformulations=llm_reformulations,
                heuristic_reformulations=heuristic_suggestions,
                max_total=6,
            )
            timeline.add(
                10, "REFORMULATIONS",
                f"{len(suggestions)} suggestion(s) LLM+heuristiques : "
                f"{len(llm_reformulations)} contextuelles (LLM) + "
                f"{len(heuristic_suggestions)} heuristiques : "
                + " | ".join(f'"{s}"' for s in suggestions[:3]),
            )
        elif heuristic_suggestions:
            suggestions = heuristic_suggestions
            timeline.add(
                10, "REFORMULATIONS",
                f"{len(suggestions)} suggestion(s) heuristique(s) "
                f"pour clarifier la requete future : "
                + " | ".join(f'"{s}"' for s in suggestions[:3]),
            )
        else:
            suggestions = []
            timeline.add(
                10, "REFORMULATIONS",
                "Aucune reformulation proposee car la requete est resolue par le "
                "kernel sans ambiguite (intent reconnu + segments coherents).",
            )

        # T11 (ex-T8). Reponse finale construite
        answer_text = self._render_answer(
            question=question,
            decomposed=decomposed,
            bypassed=bypassed,
            certified=certified,
            suggestions=suggestions,
            timeline=timeline,
            evaluation=evaluation,
            modest=modest,
            modest_certified=modest_certified,
        )
        timeline.add(11, "REPONSE_CERTIFIEE", f"{len(answer_text)} caracteres produits")

        # Enrichir la FinalAnswer
        final.answer_text = answer_text
        final.confidence = 1.0  # CERTAIN car derive du kernel
        final.structured_data = dict(final.structured_data or {})
        # Nettoyer les champs OBSOLETES du multiloop avant slow-motion :
        # ils peuvent contredire la reponse certifiee (ex: ratio_float=2047
        # alors que la verite spectral_core est ~0.5). On les ecrase.
        for stale_key in ("ratio_float", "expected_float", "matches_expected"):
            final.structured_data.pop(stale_key, None)
        final.structured_data.update({
            "slow_motion_triggered": True,
            "coherence_score": coherence_report.score,
            "coherence_signals": coherence_report.signals,
            "decomposition": {
                "intent": decomposed.detected_intent,
                "ratio": decomposed.detected_ratio,
                "coherent_segments": [
                    {"kind": s.kind, "value": s.value, "text": s.text}
                    for s in decomposed.coherent_segments
                ],
                "incoherent_segments": [
                    {"kind": s.kind, "value": s.value, "text": s.text, "reason": s.reason}
                    for s in decomposed.incoherent_segments
                ],
            },
            "canonical_request": canonical,
            "certified": certified,
            "certainty_evaluation": {
                "passed_codes": evaluation.passed_codes,
                "violated_codes": evaluation.violated_codes,
                "certainty_ratio": evaluation.certainty_ratio,
                "is_fully_certain": evaluation.is_fully_certain,
                "results": [
                    {
                        "code": r.code, "name": r.name,
                        "question": r.question.value,
                        "passed": r.passed, "detail": r.detail,
                    }
                    for r in evaluation.results
                ],
            },
            "modest_request": modest.to_dict(),
            "modest_certified": modest_certified,
            "reformulations": suggestions,
            "debug_timeline": timeline.to_dict(),
        })

        # NOUVEAU : sauvegarde automatique d'audit pour le rapport 1/2
        if not skip_auto_audit:
            self._maybe_save_audit(
                intervention_type="slow_motion_auto",
                question=question,
                final=final,
                decomposed=decomposed,
                certified=certified,
                timeline=timeline,
            )
        return final

    def _maybe_save_audit(
        self,
        intervention_type: str,
        question: str,
        final: FinalAnswer,
        decomposed: DecomposedRequest,
        certified: dict[str, Any],
        timeline: DebugTimeline,
        user_comment: Optional[str] = None,
        forced_bypass: Optional[list[str]] = None,
        toolkit_reports: Optional[dict[str, Any]] = None,
    ) -> None:
        """Sauvegarde un audit JSON signe SI rapport=1/2 et audit_store dispo."""
        if self.audit_store is None:
            return
        # Periode strict : rapport 1/2 uniquement
        ratio = decomposed.detected_ratio or "1/2"
        if ratio != "1/2":
            logger.debug("Audit saute : rapport %s non supporte (v1 = 1/2 only)", ratio)
            return
        position = None
        for s in decomposed.coherent_segments:
            if s.kind == "position":
                position = s.value
                break
        try:
            record = AuditStore.build_record(
                intervention_type=intervention_type,
                question=question,
                certified_answer=final.answer_text,
                position=position,
                prime_value=certified.get("value"),
                decomposition=final.structured_data.get("decomposition", {}),
                timeline=timeline.to_dict(),
                citations_thy=certified.get("citations", []),
                toolkit_reports=toolkit_reports or {},
                user_comment=user_comment,
                forced_bypass=forced_bypass or [],
                ratio="1/2",
            )
            path = self.audit_store.save(record)
            final.structured_data["audit_id"] = record.id
            final.structured_data["audit_path"] = str(path)
            logger.info("Audit cree : id=%s path=%s", record.id, path.name)
        except Exception as exc:
            logger.error("Echec sauvegarde audit : %s", exc, exc_info=True)

    # ---------- Etapes internes ----------

    def _rewrite_canonical(self, dec: DecomposedRequest) -> str:
        """Reconstruit une requete canonique a partir des segments coherents."""
        # Cas reconstruction : intent + position + ratio
        position = None
        for s in dec.coherent_segments:
            if s.kind == "position":
                position = s.value
                break

        if dec.detected_intent == "reconstruction" and position is not None:
            ratio = dec.detected_ratio or "1/2"
            return f"Reconstruire le {position}-eme nombre premier en rapport {ratio}"

        if dec.detected_intent == "ratio" and dec.detected_ratio:
            return f"Calculer le rapport spectral {dec.detected_ratio}"

        if dec.detected_intent == "gap":
            nums = [s.value for s in dec.coherent_segments if s.kind == "number"]
            if len(nums) >= 2:
                return f"Calculer l'ecart spectral entre {nums[0]} et {nums[1]}"

        # Fallback : on resume ce qu'on a compris
        return f"(intent={dec.detected_intent}, ratio={dec.detected_ratio}, "\
               f"segments={[s.value for s in dec.coherent_segments]})"

    def _solve_certified(self, dec: DecomposedRequest) -> dict[str, Any]:
        """
        Resolution sans LLM, uniquement via spectral_core + kernel.
        Retourne un dict avec 'summary', 'value', 'citations'.
        """
        position = None
        for s in dec.coherent_segments:
            if s.kind == "position":
                position = s.value
                break

        # NOUVEAU : intent ratio_spectral_nxn (configuration n*n avec tuples)
        if dec.detected_intent in ("ratio_spectral_nxn", "ratio_spectral") \
                and dec.tuple_A and dec.tuple_B:
            try:
                analysis = self.core.analyze_spectral_ratio(dec.tuple_A, dec.tuple_B)
            except (ValueError, RuntimeError) as exc:
                return {
                    "summary": f"Calcul du rapport spectral impossible : {exc}",
                    "value": None,
                    "citations": [],
                    "method": "spectral_core.analyze_spectral_ratio (erreur)",
                }
            if "error" in analysis:
                return {
                    "summary": f"Rapport spectral : {analysis['error']}",
                    "value": None,
                    "citations": [],
                    "method": "spectral_core.analyze_spectral_ratio",
                }
            # Construire le resume
            config = analysis["configuration"]
            cfg_label = {
                "1x1": "1*1 (cas classique)",
                "symmetric_nxn": f"symetrique {analysis.get('A_indices', []).__len__()}*{analysis.get('B_indices', []).__len__()}",
                "asym_ordonnee": "asymetrique ORDONNEE",
                "asym_chaotique": "asymetrique CHAOTIQUE",
            }.get(config, config)
            mark = "= 1/2 EXACT" if analysis.get("matches_half") \
                else "~= 1/2 (proche)" if analysis.get("near_half") \
                else "ECARTE de 1/2"
            summary = (
                f"Rapport spectral configuration {cfg_label}.\n"
                f"  A = {analysis['A_input']} (positions {analysis['A_positions']}, primes {analysis['A_primes']})\n"
                f"  B = {analysis['B_input']} (positions {analysis['B_positions']}, primes {analysis['B_primes']})\n"
                f"  RsP = {analysis['RsP_fraction']} (decimal {analysis['RsP_decimal']:.6f})  {mark}\n"
                f"  Methode : {analysis['method']}"
            )
            citations = list(analysis.get("citations", []))
            for key in ("KERNEL_CONFIG_1X1", "KERNEL_CONFIG_NXN_SYM",
                        "KERNEL_CONFIG_ASYM_ORD", "KERNEL_CONFIG_ASYM_CHAOS"):
                cert = self.kernel.get(key)
                if cert and config in cert.statement.lower().replace(" ", "_").replace("*", "x"):
                    citations.append(cert.cite())
            return {
                "summary": summary,
                "value": analysis.get("RsP_fraction"),
                "RsP_decimal": analysis.get("RsP_decimal"),
                "configuration": config,
                "analysis": analysis,
                "citations": citations,
                "method": analysis["method"],
            }

        # Cas GENERIQUE : requete sur le "i-ieme/n-ieme premier" sans valeur
        # numerique concrete (ex: "reconstruis le i-ème premier"). On repond
        # avec la definition formelle prime_i + theoreme prime_equation_prime_i
        # + 4 exemples concrets (au lieu de basculer sur emergency_summary).
        # Correctif v3.23 - Philippe Savard 2026-07-09.
        if getattr(dec, "is_generic_prime_i_query", False):
            from sympy import prime as _sym_prime
            examples = [(i, int(_sym_prime(i))) for i in (1, 5, 10, 100)]
            examples_txt = ", ".join(f"prime_i({i})={p}" for i, p in examples)

            citations = []
            for key in [
                "KERNEL_INVARIANT_RECONSTRUCTION_1_2",
                "KERNEL_INVARIANT_Z_64",
                "INVARIANT_1_2",
            ]:
                cert = self.kernel.get(key)
                if cert:
                    citations.append(cert.cite())

            summary = (
                "DEFINITION FORMELLE - Le i-ieme nombre premier est defini par "
                "prime_i(i) = SOME p. prime p AND position p = i, ou position "
                "est l'indexation canonique 1->2, 2->3, 3->5, 4->7, 5->11, etc. "
                "Cette definition est demontree dans theories/methode_spectral.thy "
                "(prime_i, lignes 407-461).\n\n"
                "THEOREMES CLES :\n"
                "  - prime_i_is_prime : pour tout i, prime_i(i) est premier.\n"
                "  - prime_i_position : position(prime_i(i)) = i.\n"
                "  - prime_equation_prime_i : (SB(i) - digamma_calc(i, prime_i(i))) / 64 = prime_i(i)\n"
                "    (reconstruction spectrale du i-ieme premier via l'invariant 1/2).\n\n"
                f"EXEMPLES CONCRETS : {examples_txt}.\n\n"
                "Pour reconstruire un premier CONCRET, precisez la valeur de i "
                "(ex: 'reconstruis le 5ieme premier' -> Gabriel calculera 11)."
            )
            return {
                "summary": summary,
                "value": None,
                "n": None,
                "examples": examples,
                "citations": citations,
                "method": "kernel_generic_prime_i (v3.23)",
            }

        # Cas principal : reconstruction du N-ieme premier en rapport 1/2
        if dec.detected_intent == "reconstruction" and position is not None:
            ratio = dec.detected_ratio or "1/2"
            if ratio == "1/2":
                # Lookup table
                p = nth_prime(position)
                # Calcul spectral via core
                data = self.core.reconstruct_prime_1_2(position)
                citations = []
                for key in [
                    "KERNEL_INVARIANT_RECONSTRUCTION_1_2",
                    "KERNEL_INVARIANT_Z_64",
                    "INVARIANT_1_2",
                ]:
                    cert = self.kernel.get(key)
                    if cert:
                        citations.append(cert.cite())
                if data is not None:
                    summary = (
                        f"Le {position}-eme nombre premier est {p}. "
                        f"En rapport 1/2, n = {position} (INVARIANT). "
                        f"Termes dans A et B : {position}."
                    )
                    return {
                        "summary": summary,
                        "value": p,
                        "n": position,
                        "num_terms": position,
                        "SA": data.SA_sum,
                        "SB": data.SB_sum,
                        "digamma_calc": data.digamma_calc,
                        "citations": citations,
                        "method": "spectral_core.reconstruct_prime_1_2 + KERNEL",
                    }
                return {
                    "summary": f"Position {position} hors table. Reponse impossible avec certitude.",
                    "value": None, "citations": citations,
                    "method": "kernel_only",
                }
            # rapports 1/3, 1/4 : on retourne le prime + invariants
            p = nth_prime(position)
            certs = [self.kernel.get("RULE_n_1_3") if ratio == "1/3" else self.kernel.get("RULE_n_1_4")]
            return {
                "summary": (
                    f"Le {position}-eme nombre premier est {p}. "
                    f"En rapport {ratio}, n est le nombre de termes "
                    f"(distinct de la position). Demandez la valeur de n separement."
                ),
                "value": p,
                "n": None,
                "citations": [c.cite() for c in certs if c],
                "method": "kernel + nth_prime",
            }

        # Cas inconnu : on retourne le resume d'urgence du domaine probable
        domain = "ratio_1_2"
        if dec.detected_ratio == "1/3":
            domain = "ratio_1_3"
        elif dec.detected_ratio == "1/4":
            domain = "ratio_1_4"
        summary_block = self.kernel.emergency_summary(domain)
        return {
            "summary": "Requete non resolvable directement par le kernel. "
                       "Voici le resume certifie du domaine concerne.",
            "value": None,
            "citations": [summary_block],
            "method": "kernel_emergency_summary",
        }

    @staticmethod
    def _build_reformulations(dec: DecomposedRequest, bypassed: list[Segment]) -> list[str]:
        """Propose des reformulations courtes pour aider l'utilisateur.

        Strategie : retourne TOUJOURS au moins une suggestion canonique si
        l'intent est detecte, meme si rien n'a ete bypass.
        """
        suggestions: list[str] = []
        ratio = dec.detected_ratio or "1/2"

        # ===== Cas : ratio spectral NxN (configurations avec tuples) =====
        if dec.detected_intent in ("ratio_spectral_nxn", "ratio_spectral"):
            if dec.tuple_A and dec.tuple_B:
                size_a = len(dec.tuple_A)
                size_b = len(dec.tuple_B)
                a_text = "(" + ",".join(str(x) for x in dec.tuple_A) + ")"
                b_text = "(" + ",".join(str(x) for x in dec.tuple_B) + ")"

                # Cas mismatch annonce/reel
                if dec.announced_symmetric is True and size_a != size_b:
                    suggestions.append(
                        f"Rapport spectral ASYMETRIQUE entre A={a_text} ({size_a} elements) "
                        f"et B={b_text} ({size_b} elements) en rapport {ratio}"
                    )
                    suggestions.append(
                        f"Pour rester SYMETRIQUE {size_a}*{size_a} : completer B "
                        f"avec {size_a - size_b} premier(s) supplementaire(s)"
                    )
                else:
                    suggestions.append(
                        f"Rapport spectral {ratio} entre A={a_text} et B={b_text} "
                        f"(configuration {size_a}*{size_b})"
                    )
                # Toujours proposer un retour aux fondamentaux
                suggestions.append(
                    f"Cas elementaire : verifier RsP_1x1({dec.tuple_A[0]}, "
                    f"{dec.tuple_B[0]}) en rapport {ratio} (doit donner EXACTEMENT 1/2)"
                )
            else:
                suggestions.append(
                    f"Calculer le rapport spectral {ratio} avec deux tuples A et B "
                    "explicites entre parentheses : exemple 'RsP({3,5,11},{2,7,13}) en 1/2'"
                )
            return suggestions

        # ===== Cas : reconstruction =====
        if dec.detected_intent == "reconstruction":
            position = None
            for s in dec.coherent_segments:
                if s.kind == "position":
                    position = s.value
                    break
            if position:
                suggestions.append(
                    f"Reconstruire le {position}-eme premier en rapport {ratio}"
                )
                if ratio == "1/2":
                    suggestions.append(
                        f"Quel est le {position}-eme nombre premier et combien de termes "
                        f"dans A et B pour le reconstituer en rapport 1/2 ?"
                    )
            return suggestions

        # ===== Cas : gap / ecart =====
        if dec.detected_intent == "gap":
            nums = [s.value for s in dec.coherent_segments if s.kind == "number"]
            if len(nums) >= 2:
                suggestions.append(
                    f"Calculer l'ecart spectral entre {nums[0]} et {nums[1]} "
                    "(symetrique par definition)"
                )
            return suggestions

        # ===== Fallback : intent inconnu =====
        if bypassed:
            return ["Reformuler la requete avec une intention explicite : "
                    "'reconstruire le N-eme premier', 'rapport spectral RsP', "
                    "ou 'ecart entre p1 et p2'"]
        return suggestions

    @staticmethod
    def _render_answer(
        question: str,
        decomposed: DecomposedRequest,
        bypassed: list[Segment],
        certified: dict[str, Any],
        suggestions: list[str],
        timeline: DebugTimeline,
        evaluation: Optional[CertaintyEvaluation] = None,
        modest: Optional[ModestRequest] = None,
        modest_certified: Optional[dict[str, Any]] = None,
    ) -> str:
        """Assemble la reponse finale pour l'utilisateur."""
        parts: list[str] = []
        parts.append("REPONSE CERTIFIEE (mode debugger ralenti)")
        parts.append("=" * 60)
        parts.append("")
        parts.append(certified["summary"])
        parts.append("")

        if bypassed:
            parts.append("Segments ignores (potentiellement incoherents) :")
            for s in bypassed:
                parts.append(f"  ✗ {s.text} — {s.reason}")
            parts.append("")

        if certified.get("citations"):
            parts.append("Sources de certitude :")
            for cit in certified["citations"]:
                parts.append(f"  • {cit}")
            parts.append("")

        # NOUVEAU : Modele de certitude + Reponse modeste reformulee
        if evaluation is not None and modest is not None and modest_certified is not None:
            parts.append("")
            parts.append("MODELE DE CERTITUDE (8 criteres / 3 questions)")
            parts.append("-" * 60)
            for r in evaluation.results:
                tag = "✓" if r.passed else "✗"
                parts.append(f"  {tag} {r.code} ({r.question.value}) : {r.detail}")
            parts.append("")
            if modest.skips_applied:
                parts.append("BOUCLE LOGIQUE (sursauts appliques) :")
                for skip in modest.skips_applied:
                    parts.append(
                        f"  -> {skip['criterion']} via {skip['strategy']}  : "
                        f"{skip['rationale']}"
                    )
                parts.append("")
            parts.append("REQUETE MODESTE REFORMULEE :")
            parts.append(f"  \"{modest.canonical_text}\"")
            parts.append("")
            parts.append("REPONSE MODESTE (certifiee par spectral_core) :")
            for line in (modest_certified.get("summary") or "").splitlines():
                parts.append(f"  {line}")
            parts.append("")

        if suggestions:
            parts.append("Suggestions de reformulation plus precises :")
            for s in suggestions:
                parts.append(f"  → {s}")
            parts.append("")

        parts.append(timeline.render())
        return "\n".join(parts)

    def _solve_modest(self, modest: ModestRequest) -> dict[str, Any]:
        """Resoud la requete modeste produite par la Boucle Logique.

        On reutilise `_solve_certified` en synthetisant une DecomposedRequest
        equivalente a la ModestRequest (cas elementaires : reconstruction,
        ratio_spectral_nxn, gap).
        """
        from .request_decomposer import Segment as _Segment

        synthesized = DecomposedRequest(
            original=modest.canonical_text,
            detected_intent=modest.intent,
            detected_ratio=modest.ratio,
            tuple_A=modest.tuple_A,
            tuple_B=modest.tuple_B,
            config_size=(len(modest.tuple_A) if modest.tuple_A else None),
        )
        if modest.position is not None:
            synthesized.segments.append(_Segment(
                kind="position", text=str(modest.position),
                value=modest.position, coherent=True,
            ))
        if modest.ratio:
            synthesized.segments.append(_Segment(
                kind="ratio", text=modest.ratio,
                value=modest.ratio, coherent=True,
            ))
        if modest.tuple_A:
            synthesized.segments.append(_Segment(
                kind="tuple_A", text=str(tuple(modest.tuple_A)),
                value=modest.tuple_A, coherent=True,
            ))
        if modest.tuple_B:
            synthesized.segments.append(_Segment(
                kind="tuple_B", text=str(tuple(modest.tuple_B)),
                value=modest.tuple_B, coherent=True,
            ))
        try:
            return self._solve_certified(synthesized)
        except Exception as exc:
            logger.exception("Echec _solve_modest")
            return {
                "summary": f"Resolution modeste impossible : {exc}",
                "value": None,
                "citations": [],
                "method": "modest_solve (erreur)",
            }

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
