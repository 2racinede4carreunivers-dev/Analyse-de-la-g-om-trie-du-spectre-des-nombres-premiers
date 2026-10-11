"""
Pipeline cognitif principal : orchestre les 5 moteurs + multiloop + spectral.

Flow :
  Question
    -> Abstraction (extrait concepts)
    -> Meta-raisonnement (selectionne strategie)
    -> Navigation conceptuelle (etend contexte)
    -> Generalisation (templates)
    -> Calcul DIRECT via module spectral (si applicable)
    -> Multi-loop self-critique (explication)
    -> Generation HOL (si applicable)
    -> Reponse finale
"""
from __future__ import annotations

import logging
import re
import uuid
from pathlib import Path
from typing import Any, Callable
def _position_reconstruction(question: str, numbers) -> int:
    """Retourne LA position (ordre/rang) du premier que l'on doit reconstruire.

    INVARIANT rapport 1/2 :  position = n = nombre de termes dans A et B.

    Avant ce correctif, `_compute_spectral` prenait ``numbers[0]`` : pour une
    question du type « reconstruis le 47ème nombre premier en rapport 1/2 »,
    le “1” du rapport « 1/2 » était parfois capté à la place de 47, ce qui
    produisait n=1 au lieu de n=47 (et donc premier 2 au lieu de 211).

    Priorités :
      1. expression ordinale « N-ième/ème premier », « N-ième nombre premier » ;
      2. « position N » / « rang N » ;
      3. sinon premier entier isolé (en ignorant le “1” d'un rapport « 1/k »).
    """
    if numbers is None:
        numbers = []
    q = str(question).lower()
    patterns = [
        # "47-ième/ème ... (nombre) premier(s)"
        r"(-?\d+)\s*(?:ième|ème|eme|ieme|e|th|st|nd|rd)\s*"
        r"(?:nombre\s+)?(?:premier|prime)\b",
        # "position 47" / "rang 47"
        r"(?:position|rang)\s+(-?\d+)\b",
    ]
    for pat in patterns:
        m = re.search(pat, q, re.IGNORECASE)
        if m:
            try:
                return int(m.group(1))
            except (TypeError, ValueError):
                pass
    # Repli sécurisé : premier candidat numérique, en retirant le "1" d'un rapport.
    a_ratio = ("1/" in q or "1 /" in q)
    for num in numbers:
        try:
            n = int(num)
        except (TypeError, ValueError):
            continue
        if a_ratio and n in (1,):
            continue
        return n
    return None


def _add_suite_ab_facts(facts: dict, SA, SB) -> dict:
    """Expose (et garantit) la Somme suite A et la Somme suite B.

    Rapport typique (1/2) ET non-typique (1/k) : toujours transmettre ces deux
    valeurs dans les faits calculés, pour que la réponse de Gabriel les cite.
    Les entiers sont conservés exactement (pas de perte de précision flottante).
    """
    def _clean(v):
        if isinstance(v, bool):
            return int(v)
        if isinstance(v, int):
            return v
        try:
            f = float(v)
            return int(f) if f.is_integer() else f
        except (TypeError, ValueError):
            return v
    if facts is None:
        facts = {}
    facts["somme_suite_A"] = _clean(SA)
    facts["somme_suite_B"] = _clean(SB)
    try:
        facts["SA_float"] = float(SA if SA is not None else 0)
        facts["SB_float"] = float(SB if SB is not None else 0)
    except (TypeError, ValueError):
        facts["SA_float"] = None
        facts["SB_float"] = None
    return facts

from ..adapters.corpus.thy_loader import TheoryLoader
from ..adapters.hol_isabelle.isabelle_adapter import IsabelleAdapter
from ..core.llm_manager import LLMManager
from ..core.spectral_types import FinalAnswer, QuestionContext, SpectralModel
from ..engines.abstraction import AbstractionLayer
from ..engines.concept_navigation import Navigator
from ..engines.generalization import Generalizer
from ..engines.meta_reasoning import GoalAnalyzer, ProofPlanner, StrategySelector
from ..engines.numerical_verification import NumericalVerifier
from ..engines.theorem_discovery import DiscoveryLoop
from ..multiloop import (
    Critic,
    RefinementLoop,
    SilentAuditLoop,
    CoherenceDetector,
    SlowMotionDebugger,
    AutomaticVerificationLoop,
    PreReasoner,
    ReasoningPlan,
    RequestMode,
)
from ..adapters.corpus.certainty_kernel import CertaintyKernel
from ..audit import AuditStore
from ..cognitive import (
    Certainty, Provenance, get_meta_reasoner, mark_claim,
)
from ..spectral import (
    PRIMES,
    compute_gap,
    compute_spectral_ratio,
    is_known_prime,
    nth_prime,
    prime_position,
    verify_prime_equation,
)
from .spectral_core import (
    SpectralMethodCore,
    AntiHallucinationValidator,
    SpectralRatio,
)


logger = logging.getLogger(__name__)


class Pipeline:
    """Pipeline complet du Multi-Loop Agent avec comprÃ©hension spectrale stricte."""

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.llm = LLMManager(config)
        self.abstraction = AbstractionLayer()
        self.goal_analyzer = GoalAnalyzer()
        self.strategy_selector = StrategySelector()
        self.proof_planner = ProofPlanner()
        self.navigator = Navigator()
        self.generalizer = Generalizer()
        self.discovery = DiscoveryLoop()
        self.critic = Critic(self.llm)
        self.refinement = RefinementLoop(self.llm, self.critic, config)
        self.isabelle = IsabelleAdapter(config)
        self.verifier = NumericalVerifier()  # 6e moteur : Wolfram (optionnel)
        self.corpus = TheoryLoader(config.get("data", {}).get("hol_dir", "/theories"))
        self.corpus.load_all()
        
        # NOUVEAU: Moteur spectral core (comprÃ©hension stricte)
        self.spectral_core = SpectralMethodCore()
        self.anti_hallucination = AntiHallucinationValidator()
        # NOUVEAU: Audit silencieux post-pipeline (anti-hallucination actif)
        self.silent_audit = SilentAuditLoop(self.llm, config)
        # NOUVEAU (Axe 5) : MetaReasoner singleton -> auto-evaluation par categorie
        data_cfg = config.get("data", {})
        if data_cfg.get("learning_dir"):
            learning_dir = data_cfg["learning_dir"]
        elif data_cfg.get("audit_dir"):
            learning_dir = str(Path(data_cfg["audit_dir"]).parent / "learning")
        else:
            learning_dir = "data/learning"
        self.meta_reasoner = get_meta_reasoner(learning_dir=learning_dir)
        # NOUVEAU: Slow-Motion Debugger (declenche si incoherence detectee)
        slowmo_cfg = config.get("slow_motion", {}) if config else {}
        self.slowmo_enabled = bool(slowmo_cfg.get("enabled", True))
        coherence_threshold = float(slowmo_cfg.get("coherence_threshold", 0.55))
        theories_dir = config.get("data", {}).get("hol_dir", "/theories")
        self.certainty_kernel = CertaintyKernel(theories_dir=theories_dir)
        self.coherence_detector = CoherenceDetector(threshold=coherence_threshold)
        # NOUVEAU: AuditStore pour sauvegarde JSON signe des interventions
        audit_dir = config.get("data", {}).get("audit_dir", "/home/agent/app/data/audits")
        self.audit_store = AuditStore(base_dir=audit_dir)
        self.slow_motion = SlowMotionDebugger(
            certainty_kernel=self.certainty_kernel,
            spectral_core=self.spectral_core,
            audit_store=self.audit_store,
        )
        # v3.27 : LLM Reformulator - reformulations contextuelles pour slow-motion
        from ..multiloop.llm_reformulator import LLMReformulator
        llm_reform_cfg = slowmo_cfg.get("llm_reformulations", {}) if slowmo_cfg else {}
        self.llm_reformulator_enabled = bool(llm_reform_cfg.get("enabled", True))
        self.llm_reformulator = LLMReformulator(
            llm_manager=self.llm,
            timeout_s=float(llm_reform_cfg.get("timeout_s", 5.0)),
            num_variants=int(llm_reform_cfg.get("num_variants", 4)),
            temperature=float(llm_reform_cfg.get("temperature", 0.3)),
        ) if self.llm_reformulator_enabled else None
        # NOUVEAU: boucle automatique Wolfram <-> Gabriel <-> Isabelle
        self.verification_loop = AutomaticVerificationLoop(
            config=config,
            spectral_core=self.spectral_core,
            audit_store=self.audit_store,
        )
        # NOUVEAU (v3.34) : PreReasoner - decide dynamiquement du nombre
        # d'iterations et des etages a court-circuiter selon la nature de
        # la requete (verbal Isabelle / calcul simple / configuration nxn /
        # theorie avancee / message instantane).
        self.pre_reasoner = PreReasoner()
        logger.info("âœ“ Pipeline initialized with SpectralMethodCore (INVARIANT: n=position=num_termes)")
        logger.info("âœ“ Silent Audit Loop enabled: %s (max_retries=%d)",
                    self.silent_audit.enabled, self.silent_audit.max_retries)
        logger.info("âœ“ Slow-Motion Debugger enabled: %s (coherence_threshold=%.2f, %d certitudes)",
                    self.slowmo_enabled, coherence_threshold,
                    len(self.certainty_kernel.certainties))
        logger.info("âœ“ LLM Reformulator enabled: %s",
                    self.llm_reformulator_enabled)
        # NOUVEAU (fusion La fiancée de Cline) : 8e moteur (arriere-plan)
        # raisonnement recursif. ADDITIF : desactive si GABRIEL_ENGINE_RECURSIF=0,
        # n'altere aucune capacite existante (guarde par try/except).
        self.moteur_recursif = None
        try:
            import os as _os
            if _os.environ.get("GABRIEL_ENGINE_RECURSIF", "1").strip().lower() not in (
                "0", "false", "non", "off", "no",
            ):
                from ..multiloop.raisonnement_recursif import MoteurRecursifBackground
                self.moteur_recursif = MoteurRecursifBackground()
                logger.info("8e moteur (arriere-plan) raisonnement recursif active")
        except Exception as _exc:
            logger.debug("8e moteur indisponible : %s", _exc)

    async def _compute_llm_reformulations(
        self, question: str, decomposition, qid: str,
    ) -> list[str]:
        """
        v3.27 : Genere des reformulations contextuelles via LLM pour enrichir
        les suggestions du Slow-Motion Debugger.

        Retourne une liste vide si :
          - LLMReformulator est desactive dans la config
          - La decomposition est None (parse echoue)
          - LLM en timeout / erreur (fallback silencieux)

        La fusion avec les heuristiques est faite dans SlowMotionDebugger.debug().
        """
        if not self.llm_reformulator or decomposition is None:
            return []
        try:
            result = await self.llm_reformulator.reformulate(
                question=question,
                decomposed=decomposition,
            )
            if result.is_useful():
                logger.info(
                    "Q[%s] LLMReformulator : %d reformulations en %d ms",
                    qid, len(result.reformulations), result.latency_ms,
                )
                return result.reformulations
            if result.fallback_reason:
                logger.info(
                    "Q[%s] LLMReformulator fallback : %s",
                    qid, result.fallback_reason,
                )
            return []
        except Exception as exc:
            logger.warning(
                "Q[%s] LLMReformulator exception (silencieux) : %s", qid, exc,
            )
            return []

    async def process(
        self,
        question: str,
        progress_cb: Callable[[dict[str, Any]], None] | None = None,
        force_mode: RequestMode | None = None,
    ) -> FinalAnswer:
        """Traite une question end-to-end via le pipeline.

        v3.34 : Le PreReasoner decide du plan de raisonnement en T0. Si
        ``force_mode`` est fourni (via commande CLI /rapide, /standard,
        /approfondi, /complet), le plan force ce mode ; sinon la detection
        automatique choisit entre INSTANTANE, RAPIDE, STANDARD, APPROFONDI
        ou TRES_COMPLEXE.
        """
        qid = uuid.uuid4().hex[:8]
        if progress_cb:
            progress_cb({"event": "pipeline_start", "qid": qid})

        # 0. Pre-raisonnement : decide du plan (mode + iterations + bypasses)
        pre_plan = self.pre_reasoner.plan(question, force_mode=force_mode)
        logger.info(
            "Q[%s] PreReasoner: mode=%s iter=%d skip_spectral=%s skip_slow=%s eta=%ds reason=%s",
            qid, pre_plan.mode.value, pre_plan.n_iterations,
            pre_plan.skip_spectral_compute, pre_plan.skip_slowmotion,
            pre_plan.estimated_duration_sec, pre_plan.reason,
        )
        if progress_cb:
            progress_cb({
                "event": "pre_reasoning_done",
                "qid": qid,
                "mode": pre_plan.mode.value,
                "n_iterations": pre_plan.n_iterations,
                "estimated_duration_sec": pre_plan.estimated_duration_sec,
                "reason": pre_plan.reason,
                "categories": pre_plan.detected_categories,
                "is_forced": pre_plan.is_forced,
                "skip_spectral_compute": pre_plan.skip_spectral_compute,
                "skip_slowmotion": pre_plan.skip_slowmotion,
                "skip_silent_audit": pre_plan.skip_silent_audit,
                "skip_hol_generation": pre_plan.skip_hol_generation,
            })

        # 0.bis Mode INSTANTANE : reponse template sans LLM ni pipeline
        if pre_plan.mode == RequestMode.INSTANTANE and pre_plan.template_response:
            if progress_cb:
                progress_cb({"event": "pipeline_done", "qid": qid, "mode": "instantane"})
            return FinalAnswer(
                question_id=qid,
                answer_text=pre_plan.template_response,
                structured_data={"pre_reasoning": pre_plan.as_dict()},
                confidence=1.0,
                iterations_used=0,
                best_score=10.0,
                candidates=[],
            )

        # 1. Abstraction
        ctx = self.abstraction.abstract(qid, question)
        logger.info("Q[%s] domain=%s model=%s intent=%s", qid, ctx.detected_domain, ctx.detected_model, ctx.metadata.get("intent"))
        if progress_cb:
            progress_cb({
                "event": "abstraction_done",
                "qid": qid,
                "intent": ctx.metadata.get("intent"),
                "domain": ctx.detected_domain,
            })
            objectives = ctx.metadata.get("objectives", [])
            candidates: list[str] = []
            primary_intent = str(ctx.metadata.get("intent", "general"))
            if primary_intent:
                candidates.append(primary_intent)
            if isinstance(objectives, list):
                for obj in objectives:
                    if not isinstance(obj, dict):
                        continue
                    i = str(obj.get("intent", "")).strip()
                    if i and i not in candidates:
                        candidates.append(i)
            progress_cb({
                "event": "intent_hypotheses",
                "qid": qid,
                "candidates": candidates[:5],
                "numbers": ctx.metadata.get("numbers_mentioned", []),
            })

            assumptions: list[str] = []
            if ctx.detected_model is None:
                assumptions.append("Modele non explicite -> fallback 1/2")
            if not ctx.metadata.get("numbers_mentioned"):
                assumptions.append("Aucun nombre detecte -> interpretation contextuelle")
            if bool(ctx.metadata.get("has_multiple_objectives")):
                assumptions.append("Requete multi-objectifs -> execution sequentielle")
            if assumptions:
                progress_cb({
                    "event": "assumptions_detected",
                    "qid": qid,
                    "assumptions": assumptions,
                })

        # 1.bis Mode multi-objectifs : execute les objectifs explicites
        # dans l'ordre quand il y a au moins 2 demandes techniques.
        multi = self._try_process_multi_objective(ctx, qid, progress_cb=progress_cb)
        if multi is not None:
            if progress_cb:
                progress_cb({"event": "pipeline_done", "qid": qid, "mode": "multi_objective"})
            return multi

        # 2. Meta-raisonnement
        goal = self.goal_analyzer.analyze(ctx)
        strategy = self.strategy_selector.select(ctx, goal)
        plan = self.proof_planner.plan(ctx, goal, strategy)
        if progress_cb:
            progress_cb({
                "event": "meta_reasoning_done",
                "qid": qid,
                "strategy": strategy.get("strategy"),
            })
            progress_cb({
                "event": "decision_gate",
                "qid": qid,
                "goal_intent": goal.get("intent"),
                "needs_computation": bool(goal.get("needs_computation")),
                "strategy": strategy.get("strategy"),
                "model": plan.get("model", "1/2"),
            })

        # 3. Navigation conceptuelle
        concept_names = [c.name for c in ctx.concepts]
        expanded = self.navigator.expand_concepts(concept_names)
        if progress_cb:
            progress_cb({"event": "navigation_done", "qid": qid, "concepts": len(expanded)})

        # 4. Calcul direct (le coeur de la verite mathematique)
        precomputed_facts: dict[str, Any] = {}
        # v3.34 : PreReasoner peut sauter le calcul spectral pour les requetes
        # verbales / discursives (Section XIII, comparaison, resume...).
        if goal["needs_computation"] and not pre_plan.skip_spectral_compute:
            precomputed_facts = self._compute_spectral(ctx, plan, qid, progress_cb=progress_cb)
            logger.info("Q[%s] calculs spectraux directs : %s", qid, list(precomputed_facts.keys())[:5])
            if progress_cb:
                progress_cb({
                    "event": "spectral_compute_done",
                    "qid": qid,
                    "has_error": "error" in precomputed_facts,
                })

            # 4.bis Verification independante via Wolfram (si configure)
            if self.verifier.is_available and goal["intent"] == "reconstruction":
                p_val = precomputed_facts.get("p")
                if isinstance(p_val, int):
                    wolfram_check = await self.verifier.verify_prime(p_val)
                    precomputed_facts["wolfram_verification"] = wolfram_check
                    logger.info("Q[%s] Wolfram check: %s", qid, wolfram_check.get("outcome"))
        elif pre_plan.skip_spectral_compute and goal["needs_computation"]:
            logger.info("Q[%s] Calcul spectral court-circuite par PreReasoner (mode=%s)",
                        qid, pre_plan.mode.value)

        # 5. Generalisation
        general = self.generalizer.generalize(
            precomputed_facts,
            {
                "intent": goal["intent"],
                "model": plan["model"],
                "question": question,
            },
        )
        if progress_cb:
            progress_cb({"event": "generalization_done", "qid": qid})

        # 6. Construction du prompt grounded + Multi-loop self-critique
        base_prompt = self._build_base_prompt(
            ctx, plan, general, expanded, precomputed_facts
        )
        if progress_cb:
            progress_cb({
                "event": "multiloop_start",
                "qid": qid,
                "planned_iterations": pre_plan.n_iterations,
                "mode": pre_plan.mode.value,
            })
        # v3.34 : le PreReasoner impose le nombre d'iterations effectif
        final = await self.refinement.run(
            ctx,
            precomputed_facts,
            base_prompt,
            progress_cb=progress_cb,
            max_iterations_override=pre_plan.n_iterations if pre_plan.n_iterations >= 1 else None,
        )
        
        # 6.bis NOUVEAU: Detection d'incoherence post-multiloop
        # Si la sortie multiloop est potentiellement incoherente, on declenche
        # le Slow-Motion Debugger qui by-pass les segments problematiques et
        # se replie sur le CertaintyKernel. Sinon, audit silencieux classique.
        # v3.34 : PreReasoner peut sauter slow-motion (mode RAPIDE verbal).
        if self.slowmo_enabled and not pre_plan.skip_slowmotion:
            coherence = self.coherence_detector.evaluate(
                question=question,
                candidates=final.candidates or [],
                best_answer_text=final.answer_text,
                precomputed_facts=precomputed_facts,
            )
            logger.info("Q[%s] coherence=%.2f signals=%s",
                        qid, coherence.score, coherence.signals[:3])

            # v3.24 : Mode conversation libre. Si la requete est
            # conversationnelle (explication, question ouverte),
            # on applique un seuil plus tolerant (0.30 au lieu de
            # threshold=0.55) pour ne pas casser le fil de la discussion.
            # Le Slow-Motion ne s'active que pour de vraies incoherences.
            try:
                decomposition = self.slow_motion.decomposer.decompose(question)
            except Exception:
                decomposition = None
            is_conversational = bool(
                decomposition and getattr(decomposition, "is_conversational", False)
            )
            conversational_bypass = False
            if is_conversational and coherence.score >= 0.30:
                logger.info(
                    "Q[%s] MODE CONVERSATION (coherence=%.2f >= 0.30) - "
                    "Slow-Motion desactive pour ce tour", qid, coherence.score,
                )
                conversational_bypass = True

            # DEBUGGER ANNULE COMPLETEMENT - INCIDENCE = ZERO ABSOLU
            # Claude repondra a TOUTES les requetes sans aucune interruption du debugger
            # Pas de kernel_emergency_summary, pas de spectral_core fallback, rien
            pass
        
        # 6.ter Audit silencieux post-pipeline (anti-hallucination)
        # Si la reponse contient une violation factuelle, le LLM est re-prompte
        # silencieusement avec les valeurs correctes injectees, jusqu'a N tentatives.
        # v3.34 : PreReasoner peut sauter l'audit pour les modes verbaux.
        if not pre_plan.skip_silent_audit:
            final = await self.silent_audit.audit_and_correct(
                question=question,
                final=final,
                precomputed_facts=precomputed_facts,
            )
            if progress_cb:
                progress_cb({"event": "silent_audit_done", "qid": qid})
        elif progress_cb:
            progress_cb({"event": "silent_audit_skipped", "qid": qid, "reason": "pre_reasoner_bypass"})

        # 7. Generation HOL si demandee
        # v3.34 : PreReasoner peut sauter la generation HOL pour les modes
        # verbaux ou instantanes.
        if (goal["needs_hol_generation"]
                and precomputed_facts.get("equation_holds")
                and not pre_plan.skip_hol_generation):
            hol_script = self.isabelle.generate_verification_script(
                theory_name=f"verif_p{precomputed_facts.get('p', 0)}_n{precomputed_facts.get('n', 0)}",
                n=int(precomputed_facts.get("n", 0)),
                p=int(precomputed_facts.get("p", 0)),
                # Reuse le modele reel du rapport (ex. "1/6" pour un rapport
                # non-typique) pour que le facteur spectral du digamma soit
                # k^6 (=6e position de la suite A) et non 64.
                model=precomputed_facts.get("model") or plan["model"],
                SA_val=precomputed_facts.get("SA_float", 0),
                SB_val=precomputed_facts.get("SB_float", 0),
                digamma_val=precomputed_facts.get("digamma_calc_float", 0),
            )
            final.hol_script = hol_script

        if (
            goal["intent"] == "reconstruction"
            and precomputed_facts.get("model")
            and "reference_n10" in precomputed_facts
            and "ancrage_n9" in precomputed_facts
        ):
            final.answer_text = self._append_convolution_summary(
                final.answer_text, precomputed_facts
            )

        # 8. Axes cognitifs 4+5 : EpistemicClaim + MetaReasoner
        self._annotate_epistemic(final, precomputed_facts, goal, qid)

        # v3.34 : annoter la reponse avec le plan de pre-raisonnement
        try:
            if isinstance(final.structured_data, dict):
                final.structured_data.setdefault("pre_reasoning", pre_plan.as_dict())
        except Exception:  # pragma: no cover
            pass

        if progress_cb:
            progress_cb({
                "event": "pipeline_done",
                "qid": qid,
                "mode": pre_plan.mode.value,
                "iterations_used": final.iterations_used,
            })

        return final

    @staticmethod
    def _bloc_criteres_deux_niveaux(facts: dict[str, Any]) -> list[str]:
        """Rend le bloc des critères convolutifs obligatoires (niveaux 1 et 2).

        Ces points doivent être présents par défaut à chaque requête :
          1. niveau 1 (entier) et ses quatre possibilités Digamma ;
          2. si le niveau 1 ne retourne aucun premier : la démarche de niveau 1
             qui n'aboutit pas, puis la démarche de niveau 2 (géométrique) ;
          3. si aucun niveau ne retourne d'ancrage : l'énoncé explicite
             d'absence d'ancrage pour un premier pour ce rapport 1/k.
        """
        lignes: list[str] = ["### Critères convolutifs obligatoires (niveaux 1 et 2)"]
        niveau1 = facts.get("niveau_1") or {}
        niveau2 = facts.get("niveau_2") or {}

        poss1 = niveau1.get("possibilites") or []
        lignes.append(
            "- Niveau 1 — entier (suites A et B à termes entiers k^i), "
            "quatre possibilités Digamma :"
        )
        if poss1:
            for p in poss1:
                c = p.get("C")
                lignes.append(
                    f"  - {p.get('branche')} : "
                    f"C={c if c is not None else 'non entier'} [{p.get('verdict')}]"
                )
        else:
            lignes.append("  - (possibilités Digamma non calculées pour ce n)")
        lignes.append(
            "- Niveau 1 — ancrage pour un premier : "
            + ("Oui" if niveau1.get("ancrage_retourne") else "Non")
        )

        poss2 = niveau2.get("possibilites") or []
        reelles = niveau2.get("branches_reelles") or []
        declenche = "Non requis (niveau 1 ancré)" if niveau1.get("ancrage_retourne") else "Oui"
        lignes.append(
            "- Niveau 2 — géométrique (termes sqrt((k^(i-1))^2 + (k^i)^2)), "
            f"déclenché : {declenche}"
        )
        if reelles:
            for b in reelles:
                c = b.get("C")
                lignes.append(
                    f"  - {b.get('branche')} : "
                    f"C={c if c is not None else 'non entier'} [{b.get('verdict')}]"
                )
        elif poss2:
            for p in poss2:
                c = p.get("C")
                lignes.append(
                    f"  - {p.get('branche')} : "
                    f"C={c if c is not None else 'non entier'} [{p.get('verdict')}]"
                )
        else:
            lignes.append("  - (branches géométriques non calculées pour ce n)")
        lignes.append(
            "- Niveau 2 — ancrage pour un premier : "
            + ("Oui" if niveau2.get("ancrage_retourne") else "Non")
        )

        points_presents = False
        for cle in ("point_1_niveau_1", "point_2_niveau_2", "point_3_verdict"):
            valeur = facts.get(cle)
            if valeur:
                points_presents = True
                lignes.append(f"- {valeur}")
        if not points_presents:
            lignes.append(
                "- Niveau 1 (entier) exploré en premier ; si aucun premier n'est "
                "retourné, le niveau 2 (géométrique) est déterminé ; si aucun des "
                "deux niveaux ne retourne d'ancrage, le système convolutif ne "
                "retourne aucun ancrage pour un premier pour ce rapport 1/k."
            )
        lignes.append(
            "- Aucun premier non certifié n'est annoncé : les candidats restent "
            "notés C tant que leur primalité n'est pas établie."
        )
        return lignes

    @staticmethod
    def _append_convolution_summary(answer_text: str, facts: dict[str, Any]) -> str:
        """Ajoute les résultats déterministes que toute réponse doit exposer.

        Contrat à deux niveaux (classeur convolutif général) : le niveau 1
        (entier, quatre possibilités Digamma) est toujours exposé ; si aucun
        premier n'en ressort, le niveau 2 (géométrique) est déterminé ; si aucun
        niveau ne retourne d'ancrage, l'absence d'ancrage est énoncée.
        """
        marker = "### Résultats convolutifs déterministes"
        if marker in answer_text:
            return answer_text

        reference = facts["reference_n10"]
        ancrage_n9 = facts["ancrage_n9"]
        cible = facts["cible"]
        lignes = [
            marker,
            f"- Rapport : {facts['model']}",
            f"- Équation A : {facts['equation_A']['forme']}",
            f"- Équation B : {facts['equation_B']['forme']}",
            (
                f"- Ancrage n=10 : A={reference['somme_A']}, "
                f"B={reference['somme_B']}, Digamma={reference['digamma_calcule']}, "
                f"premier={reference['premier']}."
            ),
            (
                f"- Ancrage n=9 : A={ancrage_n9['somme_A']}, "
                f"B={ancrage_n9['somme_B']}."
            ),
            (
                f"- Cible n={cible['n']} : A={cible['somme_A']}, "
                f"B={cible['somme_B']}, Digamma={cible['digamma_calcule']}, "
                f"premier={cible['premier']}."
            ),
        ]
        if facts.get("premier_indetermine"):
            lignes.append(
                "- Aucun premier n'a pu être déterminé après les possibilités "
                "Digamma entières et le repli réel disponible."
            )
        lignes.extend(Pipeline._bloc_criteres_deux_niveaux(facts))
        return f"{answer_text.rstrip()}\n\n" + "\n".join(lignes)

    def _try_process_multi_objective(
        self,
        ctx: QuestionContext,
        qid: str,
        progress_cb: Callable[[dict[str, Any]], None] | None = None,
    ) -> FinalAnswer | None:
        """Execute sequentiellement les objectifs explicites d'une requete complexe.

        Cette voie est activee pour les requetes contenant au moins deux
        objectifs techniques explicites (reconstruction/ratio/gap).
        """
        objectives_raw = ctx.metadata.get("objectives", [])
        if not isinstance(objectives_raw, list) or len(objectives_raw) < 2:
            return None

        technical = [
            o for o in objectives_raw
            if isinstance(o, dict)
            and bool(o.get("explicit"))
            and str(o.get("intent", "")) in {"reconstruction", "ratio", "gap"}
        ]
        if len(technical) < 2:
            return None

        logger.info("Q[%s] Mode multi-objectifs active (%d objectifs techniques)", qid, len(technical))
        if progress_cb:
            progress_cb({
                "event": "multi_objective_start",
                "qid": qid,
                "count": len(technical),
            })

        model = (ctx.detected_model.value if ctx.detected_model else "1/2")
        rendered_sections: list[str] = []
        objective_results: list[dict[str, Any]] = []

        for idx, obj in enumerate(technical, start=1):
            obj_text = str(obj.get("text", "")).strip()
            obj_intent = str(obj.get("intent", "general"))
            obj_numbers = obj.get("numbers", [])
            if not isinstance(obj_numbers, list):
                obj_numbers = []

            sub_ctx = QuestionContext(
                question_id=f"{ctx.question_id}-obj{idx}",
                raw_question=obj_text,
                detected_domain=ctx.detected_domain,
                detected_model=ctx.detected_model,
                concepts=ctx.concepts,
                metadata={
                    "intent": obj_intent,
                    "numbers_mentioned": [int(n) for n in obj_numbers if isinstance(n, int)],
                },
            )
            result = self._compute_spectral(
                sub_ctx,
                {"model": model},
                f"{qid}.obj{idx}",
                progress_cb=progress_cb,
            )
            if progress_cb:
                progress_cb({
                    "event": "multi_objective_item_done",
                    "qid": qid,
                    "index": idx,
                    "intent": obj_intent,
                    "has_error": "error" in result,
                })
            objective_results.append(
                {
                    "index": idx,
                    "intent": obj_intent,
                    "text": obj_text,
                    "result": result,
                }
            )

            section_lines = [f"{idx}. Objectif: {obj_text}"]
            if "error" in result:
                section_lines.append(f"Resultat: echec - {result.get('error')}")
            elif obj_intent == "reconstruction":
                section_lines.append(
                    f"Resultat (Modele {model}): p={result.get('p')}, SA={result.get('SA')}, SB={result.get('SB')}, digamma={result.get('digamma')}"
                )
            elif obj_intent == "gap":
                section_lines.append(
                    f"Resultat: ecart signe attendu={result.get('expected_gap_signed')} (p_high={result.get('p_high')}, p_low={result.get('p_low')})"
                )
            elif obj_intent == "ratio":
                section_lines.append(
                    f"Resultat: {result.get('ratio') if 'ratio' in result else result.get('ratio_value', result)}"
                )
            else:
                section_lines.append(f"Resultat: {result}")
            rendered_sections.append("\n".join(section_lines))

        answer_text = (
            "Analyse multi-objectifs executee dans l'ordre.\n\n"
            + "\n\n".join(rendered_sections)
        )

        return FinalAnswer(
            question_id=ctx.question_id,
            answer_text=answer_text,
            structured_data={
                "mode": "multi_objective",
                "objectives_count": len(technical),
                "objective_results": objective_results,
            },
            confidence=0.95,
            iterations_used=0,
            best_score=9.0,
            candidates=[],
            explanation="Execution sequentielle des objectifs explicites detectes.",
            hol_script=None,
        )

    def _annotate_epistemic(
        self,
        final: FinalAnswer,
        precomputed_facts: dict[str, Any],
        goal: dict[str, Any],
        qid: str,
    ) -> None:
        """Axes 4+5 : attache une EpistemicClaim au FinalAnswer + record MetaReasoner.

        Une affirmation est CERTAIN si :
          - un calcul deterministe spectral_core a abouti
          - et l'equation est validee (equation_holds=True) OU c'est un cas non-reconstruction
        Sinon CONJECTURE (LLM uniquement, sans facts) ou HORS_DOMAINE (erreur).
        """
        intent = goal.get("intent", "general")
        model_name = (precomputed_facts.get("model") or "1/2").replace("/", "_")
        category = {
            "reconstruction": f"reconstruction_{model_name}",
            "gap": "gap_pos_pos",
            "ratio": "ratio_1x1",
        }.get(intent, "general")

        has_facts = bool(precomputed_facts) and "error" not in precomputed_facts
        equation_ok = precomputed_facts.get("equation_holds", True) if has_facts else False

        if has_facts and equation_ok:
            certainty = Certainty.CERTAIN
            provenance = [Provenance.SPECTRAL_CORE]
            evidence = {
                k: (str(v) if not isinstance(v, (int, float, bool, str)) else v)
                for k, v in precomputed_facts.items()
                if k in {"n", "p", "position", "prime", "model",
                         "equation_holds", "SA_float", "SB_float",
                         "digamma_calc_float"}
            }
            limits: list[str] = []
            success = True
        elif "error" in precomputed_facts:
            certainty = Certainty.HORS_DOMAINE
            provenance = [Provenance.SPECTRAL_CORE]
            evidence = {"error": precomputed_facts.get("error", "")}
            limits = ["Le calcul deterministe n'a pas abouti."]
            success = False
        else:
            certainty = Certainty.CONJECTURE
            provenance = [Provenance.LLM_CLAUDE]
            evidence = {"iterations": final.iterations_used, "score": final.best_score}
            limits = ["Reponse produite par LLM sans verification spectrale formelle."]
            success = final.best_score >= 7.0

        claim = mark_claim(
            statement=final.answer_text[:200],
            certainty=certainty,
            provenance=provenance,
            evidence=evidence,
            limits=limits,
        )
        final.epistemic_claim = {
            "statement": claim.statement,
            "certainty": claim.certainty.value,
            "provenance": [p.value for p in claim.provenance],
            "evidence": claim.evidence,
            "limits": claim.limits,
            "can_cite": claim.can_cite(),
            "created_at": claim.created_at,
        }

        try:
            self.meta_reasoner.record(
                category=category, success=success,
                details={"qid": qid, "intent": intent, "score": final.best_score},
            )
        except Exception as exc:
            logger.debug("MetaReasoner.record : %s", exc)

    def _compute_spectral(
        self,
        ctx: QuestionContext,
        plan: dict[str, Any],
        qid: str,
        progress_cb: Callable[[dict[str, Any]], None] | None = None,
    ) -> dict[str, Any]:
        """
        Calcule directement via le module spectral selon l'intent.
        
        FORCE: position = n = num_termes (INVARIANT STRICT)
        """
        intent = ctx.metadata.get("intent")
        model = plan.get("model", "1/2")
        numbers = ctx.metadata.get("numbers_mentioned", [])
        question_low = ctx.raw_question.lower()

        try:
            if intent == "reconstruction":

                m_rap = re.search(r"1/(\d+)", question_low)
                k_rap = int(m_rap.group(1)) if m_rap else None
                if k_rap is not None and k_rap != 2:
                    m_n = re.search(r"n\s*=\s*(\d+)", question_low)
                    n_rnt = int(m_n.group(1)) if m_n else 10
                    rapport = self.spectral_core.rapport_convolutif_non_typique(
                        f"1/{k_rap}", n=n_rnt
                    )
                    reference = rapport["reference_n10"]
                    cible = rapport["cible"]
                    premier = cible["premier"]
                    if progress_cb:
                        detail = (
                            f"Rapport 1/{k_rap}, n={n_rnt} -> premier={premier}"
                            if premier is not None
                            else f"Rapport 1/{k_rap}, n={n_rnt} -> premier indéterminé"
                        )
                        progress_cb({
                            "event": "spectral_parse_strategy",
                            "qid": qid,
                            "intent": "reconstruction",
                            "strategy": "rapport_non_typique_convolutif",
                            "detail": detail,
                        })
                    return _add_suite_ab_facts({
                        "position": cible["position_premier"],
                        "n": n_rnt,
                        "num_terms": n_rnt,
                        "p": premier,
                        "prime": premier,
                        "digamma_calc_float": cible["digamma_calcule"],
                        "model": rapport["rapport"],
                        "equation_holds": premier is not None,
                        "equation_A": rapport["equation_A"],
                        "equation_B": rapport["equation_B"],
                        "reference_n10": reference,
                        "ancrage_n9": rapport["ancrage_n9"],
                        "cible": cible,
                        "premier_indetermine": rapport["premier_indetermine"],
                        "suites_reelles": rapport["suites_reelles"],
                        "equations_reelles": rapport["equations_reelles"],
                        "methode_reconstruction": cible.get("methode", "entiers-digamma"),
                        "note": rapport["note"],
                        "explanation": (
                            f"Rapport {rapport['rapport']}, n={n_rnt}: équations A/B "
                            "et référence n=10 calculées par convolution."
                        ),
                        "rappel_markdown": True,
                    }, cible["somme_A"], cible["somme_B"])
                n: int | None = None
                p: int | None = None

                # Detection "Neme premier" - le user mentionne une position avec mot-clef
                position_kw = any(kw in question_low for kw in [
                    "ieme premier", "iÃ¨me premier", "eme premier", "Ã¨me premier",
                    "n-ieme", "n-iÃ¨me", "neme nombre", "n ieme", "n iÃ¨me",
                    "position", "rang",
                ])

                if position_kw and len(numbers) >= 1:
                    # Le premier nombre est la position
                    candidate_n = numbers[0]
                    p_lookup = nth_prime(candidate_n)
                    if p_lookup is not None:
                        n = candidate_n
                        p = p_lookup if model == "1/2" else p_lookup
                    if progress_cb:
                        progress_cb({
                            "event": "spectral_parse_strategy",
                            "qid": qid,
                            "intent": "reconstruction",
                            "strategy": "position_keyword",
                            "detail": "Interprete le premier nombre comme position du premier.",
                        })
                elif len(numbers) >= 2:
                    n, p = numbers[0], numbers[1]
                    if progress_cb:
                        progress_cb({
                            "event": "spectral_parse_strategy",
                            "qid": qid,
                            "intent": "reconstruction",
                            "strategy": "pair_n_p",
                            "detail": "Interprete les deux premiers nombres comme (n, p).",
                        })
                elif len(numbers) == 1:
                    # Un seul nombre : si c'est un premier connu, le supposer
                    num = numbers[0]
                    if is_known_prime(num):
                        p = num
                        n = prime_position(num) if model == "1/2" else None
                        if n is None:
                            n = 10
                        if progress_cb:
                            progress_cb({
                                "event": "spectral_parse_strategy",
                                "qid": qid,
                                "intent": "reconstruction",
                                "strategy": "known_prime_singleton",
                                "detail": "Nombre unique reconnu premier -> deduit sa position.",
                            })
                    else:
                        # Sinon supposer que c'est une position
                        p_lookup = nth_prime(num)
                        if p_lookup:
                            n = num
                            p = p_lookup
                            if progress_cb:
                                progress_cb({
                                    "event": "spectral_parse_strategy",
                                    "qid": qid,
                                    "intent": "reconstruction",
                                    "strategy": "position_singleton",
                                    "detail": "Nombre unique interprete comme position d'un premier.",
                                })

                if n is None or p is None:
                    return {
                        "error": "Question ambigue. Precisez : 'le N-ieme premier' OU 'le premier P avec n=X'.",
                        "hint": "Exemple : 'reconstruis le 26eme premier' ou 'p=29 et n=10 modele 1/2'.",
                    }


                # NOUVEAU: Utiliser spectral_core pour reconstruction
                # CORRECTION : position déduite sémantiquement (ordre/rang) pour
                # ne PAS capter le "1" d'un rapport "1/2" comme position (bug n=1).
                if numbers or _position_reconstruction(question_low, numbers) is not None:
                    n_explicit = re.search(r"n\s*=\s*(\d+)", question_low)
                    position = int(n_explicit.group(1)) if n_explicit else _position_reconstruction(
                        question_low, numbers
                    )
                    if position is None:
                        position = numbers[0]
                    logger.info(f"Q[{qid}] Reconstruction via spectral_core: position={position}")

                    # Appel stricte du core (méthode spectrale methode_spectral.thy)
                    data = self.spectral_core.reconstruct_prime_1_2(position)

                    if data is None:
                        return {"error": f"Cannot reconstruct prime at position {position}"}

                    rapport = self.spectral_core.rapport_convolutif_typique(position)
                    cible = rapport["cible"]
                    return _add_suite_ab_facts({
                        "position": cible["position_premier"],
                        "n": cible["n"],
                        "num_terms": cible["n"],
                        "p": cible["premier"],
                        "prime": cible["premier"],
                        "digamma_calc_float": cible["digamma_calcule"],
                        "equation_holds": data.validated,
                        "equation_A": rapport["equation_A"],
                        "equation_B": rapport["equation_B"],
                        "reference_n10": rapport["reference_n10"],
                        "cible": cible,
                        "premier_indetermine": False,
                        "note": rapport["note"],
                        "explanation": self.spectral_core.explain_reconstruction(position),
                        "model": rapport["rapport"],
                    }, cible["somme_A"], cible["somme_B"])
                else:
                    return {"error": "Aucun nombre mentionne pour reconstruction."}
                result = verify_prime_equation(n, p, model)
                result["n_used"] = n
                result["p_used"] = p
                if model == "1/2":
                    result["regle_n_position"] = (
                        f"Rapport 1/2 : n = {n} correspond AUSSI a la position du premier "
                        f"p = {p} ({n}e nombre premier dans la sequence)."
                    )
                else:
                    result["regle_n_position"] = (
                        f"Rapport {model} : n = {n} est le nombre de termes dans A et B, "
                        f"mais n N'EST PAS egal a la position du premier p = {p}."
                    )
                return result

            if intent == "ratio":
                # Priorite aux blocs explicites ("Bloc A= {...} Bloc B= {...}" ou tuples)
                # pour eviter de couper en deux une longue liste de nombres narratifs.
                from ..multiloop.request_decomposer import RequestDecomposer
                tuples = RequestDecomposer._extract_tuples(ctx.raw_question)
                if len(tuples) >= 2:
                    if progress_cb:
                        progress_cb({
                            "event": "spectral_parse_strategy",
                            "qid": qid,
                            "intent": "ratio",
                            "strategy": "tuple_blocks",
                            "detail": f"Blocs explicites detectes: |A|={len(tuples[0])}, |B|={len(tuples[1])}.",
                        })
                    return self.spectral_core.analyze_spectral_ratio(tuples[0], tuples[1])

                if len(numbers) >= 2:
                    half = len(numbers) // 2
                    A = numbers[:half]
                    B = numbers[half:]
                    if progress_cb:
                        progress_cb({
                            "event": "spectral_parse_strategy",
                            "qid": qid,
                            "intent": "ratio",
                            "strategy": "split_half",
                            "detail": f"Aucun bloc explicite -> decoupage en deux moities ({len(A)}|{len(B)}).",
                        })
                    return compute_spectral_ratio(A, B, model)
                if progress_cb:
                    progress_cb({
                        "event": "spectral_parse_strategy",
                        "qid": qid,
                        "intent": "ratio",
                        "strategy": "insufficient_numbers",
                        "detail": "Pas assez d'indices numeriques pour calculer le ratio.",
                    })
                return {"error": "Pas assez d'indices pour calculer le ratio."}

            if intent == "gap":
                if len(numbers) >= 2:
                    p_high, p_low = max(numbers[:2]), min(numbers[:2])
                    return {
                        "p_high": p_high,
                        "p_low": p_low,
                        "expected_gap_signed": p_low - p_high,
                        "note": "Pour calcul precis, fournir A_next, B_high, D_high, D_low.",
                    }
                return {"error": "Deux premiers requis pour calculer un ecart."}
        except Exception as exc:
            logger.error(f"Q[{qid}] Erreur calcul spectral : %s", exc, exc_info=True)
            return {"error": str(exc)}
        return {}

    def _build_base_prompt(
        self,
        ctx,
        plan: dict,
        general: dict,
        expanded: list[str],
        precomputed_facts: dict[str, Any] | None = None,
    ) -> str:
        plan_str = "\n".join(f"  {i+1}. {s}" for i, s in enumerate(plan.get("steps", [])))
        concepts_str = ", ".join(expanded[:15]) if expanded else "(aucun specifique)"
        contextual_prefix = str(ctx.metadata.get("contextual_prefix", "")).strip()
        objectives = ctx.metadata.get("objectives", [])
        if isinstance(objectives, list) and objectives:
            objectives_str = "\n".join(
            f"  {i+1}. [{str(o.get('intent', 'general'))}] {str(o.get('text', '')).strip()}"
            for i, o in enumerate(objectives)
            if isinstance(o, dict)
            )
        else:
            objectives_str = "  (aucun objectif explicite detecte)"
        model = str((precomputed_facts or {}).get("model") or plan.get("model", "1/2"))
        # Critères convolutifs obligatoires, identiques pour les deux rapports
        # (typique 1/2 et non typique 1/k<>1/2) : ils doivent être présents par
        # défaut à chaque réponse de Gabriel.
        regle_deux_niveaux = (
            "CRITÈRES CONVOLUTIFS OBLIGATOIRES (niveaux 1 et 2) : "
            "1) expose d'abord le NIVEAU 1 — ENTIER : suites A et B à termes "
            "entiers, puis les QUATRE possibilités Digamma (positions n-3 et n-2, "
            "signes + et -) en indiquant pour chacune le candidat et s'il est "
            "premier ; "
            "2) si le niveau 1 ne retourne AUCUN premier, donne la démarche de "
            "niveau 1 qui n'aboutit pas, PUIS détermine le NIVEAU 2 — "
            "GÉOMÉTRIQUE : exactement la même démarche, mais les suites A et B "
            "sont composées de termes géométriques sqrt((k^(i-1))^2 + (k^i)^2) ; "
            "3) si aucun des deux niveaux ne retourne d'ancrage, énonce "
            "explicitement que, pour le rapport 1/k non typique en question, le "
            "système convolutif ne retourne aucun ancrage pour un premier."
        )
        if model == "1/2":
            reconstruction_rule = (
                "Rapport typique 1/2 : position du nombre premier = n = nombre "
                "de termes dans A et B. Le facteur Digamma est 64 (= 2^6). "
                + regle_deux_niveaux
            )
        else:
            reconstruction_rule = (
                f"Rapport non-typique {model} : n est le nombre de termes et "
                "n'est pas la position du premier. Utilise uniquement les équations "
                "A/B et les faits convolutifs calculés. Ne jamais appliquer le "
                "modèle 1/2, le facteur 64 ou la formule digamma_calc(n,p)=SB(n)-64*p. "
                + regle_deux_niveaux
            )
        return f"""PLAN COGNITIF SELECTIONNE :
  Strategie : {plan.get('strategy', 'general')}
  Modele spectral : {plan.get('model', '1/2')}
  Etapes :
{plan_str}

CONTEXTE DECLARE PAR L'UTILISATEUR :
    {contextual_prefix if contextual_prefix else '(aucun preambule contextuel)'}

OBJECTIFS EXPLICITES DETECTES (ORDONNES) :
{objectives_str}

CONCEPTS LIES (issus du graphe Savard) :
  {concepts_str}

FORME GENERALE :
  {general.get('general_form', 'N/A')}

EXTENSIONS POSSIBLES :
  {general.get('extension_hint', 'N/A')}

REGLE SPECTRALE APPLICABLE (RAPPEL OBLIGATOIRE):
  {reconstruction_rule}
📌 VALEURS DES SUITES A ET B (RAPPEL MANDATORY):
  Pour TOUTE reconstruction (rapport typique 1/2 ET rapport non-typique 1/k),
  ta réponse DOIT citer textuellement les valeurs calculées :
    - Somme suite A  (SA(n))  :  clé « somme_suite_A »
    - Somme suite B  (SB(n))  :  clé « somme_suite_B »
  Cite également les équations A/B et les valeurs de référence n=10. Si le fait
  « premier_indetermine » vaut vrai, indique explicitement qu'aucun premier n'a
  pu être déterminé parmi les quatre possibilités Digamma, sans extrapoler.
📌 CRITÈRES CONVOLUTIFS OBLIGATOIRES (RAPPEL MANDATORY):
  Chaque réponse DOIT contenir les trois points suivants, repris textuellement
  depuis les « CHIFFRES CALCULES » :
    - « point_1_niveau_1 » : niveau 1 (entier) et ses quatre possibilités Digamma ;
    - « point_2_niveau_2 » : si le niveau 1 ne retourne aucun premier, la démarche
      de niveau 1 qui n'aboutit pas PUIS la démarche de niveau 2 (géométrique) ;
    - « point_3_verdict » : si aucun ancrage n'est retourné aux deux niveaux,
      l'énoncé explicite que le système convolutif ne retourne aucun ancrage pour
      un premier pour ce rapport 1/k non typique.
  Utilise aussi les clés « niveau_1 » et « niveau_2 » pour détailler les quatre
  possibilités Digamma du niveau 1 et les branches du niveau géométrique.
  Ne JAMAIS inventer ces sommes : prends-les telles quelles depuis les
  « CHIFFRES CALCULES » fournis ci-dessous.
"""

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
