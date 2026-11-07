"""
PIPELINE INTEGRATION FIX - Détecter les écarts AVANT le multiloop.
"""
from __future__ import annotations

import logging
import re
import uuid
from typing import Any, Optional, Callable

from ..core.spectral_types import FinalAnswer, QuestionContext
from ..spectral.composite_absurdity_prover import (
    build_composite_rejection,
    detect_composite_in_gap_request,
)
from ..spectral.gap_solver_corrected import GapSolver, GapResult
from ..spectral.prime_table import prime_position, nth_prime


logger = logging.getLogger(__name__)


def detect_gap_from_question(question: str) -> tuple[bool, Optional[str], list[int]]:
    """
    Détecte si la question demande un écart (GAP) entre DEUX premiers.
    
    CRUCIAL : Distinguer entre :
      - "écart entre 3 et 23" → GAP (deux nombres)
      - "rapport spectral... bloc A (3,23,31) bloc B (17,11,29)" → RATIO (deux blocs)
    
    Returns:
        (is_gap, gap_type, [p1, p2])
    """
    q_low = question.lower()
    
    # Si c'est un rapport spectral (bloc), ne pas détecter comme gap
    if "rapport spectral" in q_low or "bloc" in q_low:
        return False, None, []
    
    # Vérifier les mots-clés d'écart
    if not any(kw in q_low for kw in ["écart", "gap", "entre"]):
        return False, None, []
    
    # S'assurer qu'on a exactement 2 nombres
    numbers = re.findall(r'-?\d+', question)
    
    if len(numbers) != 2:
        return False, None, []
    
    try:
        p1, p2 = int(numbers[0]), int(numbers[1])
    except ValueError:
        return False, None, []
    
    # Classifier le type
    if p1 > 0 and p2 > 0:
        gap_type = "positive_positive"
    elif p1 < 0 and p2 < 0:
        gap_type = "negative_negative"
    elif (p1 < 0 and p2 > 0) or (p1 > 0 and p2 < 0):
        gap_type = "mixed"
    else:
        gap_type = None
    
    if gap_type:
        logger.info(f"ÉCART détecté : {gap_type} (p1={p1}, p2={p2})")
        return True, gap_type, [p1, p2]
    
    return False, None, []


class PipelineWithGapDetection:
    """
    Wrapper du Pipeline qui détecte et résout les écarts AVANT multiloop.
    """
    
    def __init__(self, base_pipeline):
        self.pipeline = base_pipeline
        self.gap_solver = GapSolver(spectral_core=base_pipeline.spectral_core)
        logger.info("✓ PipelineWithGapDetection initialized")

    def __getattr__(self, name):
        """Delegation transparente vers le pipeline de base.

        Permet a l'UI / aux autres modules d'acceder a `spectral_core`,
        `audit_store`, `corpus`, `verification_loop`, etc. sans connaitre
        ce wrapper. Toute commande historique du CLI continue de fonctionner.
        """
        # __getattr__ n'est appele que si l'attribut n'existe pas sur self.
        # On evite la recursion infinie si self.pipeline n'est pas encore set.
        if name == "pipeline":
            raise AttributeError(name)
        try:
            return getattr(self.pipeline, name)
        except AttributeError:
            raise AttributeError(
                f"'PipelineWithGapDetection' et son base_pipeline n'ont pas d'attribut '{name}'"
            )
    
    async def process(
        self,
        question: str,
        previous_answer: Optional[FinalAnswer] = None,
        progress_cb: Callable[[dict[str, Any]], None] | None = None,
        force_mode: Any = None,
    ) -> FinalAnswer:
        """
        Processus amélioré :
          0. Détecter si c'est une demande de VISUALISATION (auto-trigger graphique)
          1. Détecter si c'est une question d'écart (GAP)
          2. Si OUI à 0 ou 1 : résoudre directement (pas multiloop, certitude 1.0)
          3. Sinon : pipeline standard
        """
        qid = uuid.uuid4().hex[:8]
        if progress_cb:
            progress_cb({"event": "wrapper_start", "qid": qid})

        # --- 0) AUTO-TRIGGER VISUALISATION ---
        viz_answer = self._try_visualization(qid, question)
        if viz_answer is not None:
            if progress_cb:
                progress_cb({"event": "wrapper_done", "qid": qid, "mode": "visualization"})
            return viz_answer

        # --- 1) ÉCART (GAP) ---
        is_gap, gap_type, numbers = detect_gap_from_question(question)

        if is_gap and gap_type and len(numbers) >= 2:
            logger.info(f"Q[{qid}] ÉCART DÉTECTÉ : {gap_type}")
            if progress_cb:
                progress_cb({"event": "gap_detected", "qid": qid, "gap_type": gap_type})

            p1, p2 = numbers[0], numbers[1]

            # --- Preuve par l'absurde : composés interceptés en amont ---
            # Idée Philippe Thomas Savard (2026-07-02) : si l'un des deux
            # nombres n'est pas premier, on ne cherche PAS à résoudre l'écart
            # (échec silencieux) ; on retourne un message pédagogique qui
            # explique pourquoi la Méthode Spectrale exclut strictement les
            # composés (cf. theories/methode_spectral.thy, theorem
            # composite_not_prime_i).
            rejections = detect_composite_in_gap_request([p1, p2])
            if rejections:
                logger.info(
                    f"Q[{qid}] Composé(s) détecté(s) : "
                    f"{[r.value for r in rejections]} — preuve par l'absurde"
                )
                answer = self._build_composite_rejection_answer(
                    qid, question, rejections, p1, p2
                )
                if progress_cb:
                    progress_cb({"event": "wrapper_done", "qid": qid, "mode": "composite_rejection"})
                return answer

            gap_result = self.gap_solver.solve_gap(p1, p2)

            if gap_result is not None:
                logger.info(f"Q[{qid}] Écart résolu : {gap_result.gap_count} nombres")
                answer = self._build_gap_answer(qid, question, gap_result)
                if progress_cb:
                    progress_cb({"event": "wrapper_done", "qid": qid, "mode": "gap"})
                return answer
            else:
                logger.error(f"Q[{qid}] GapSolver échoué pour {gap_type}")

        # --- 2) PIPELINE STANDARD ---
        logger.info(f"Q[{qid}] Pas d'écart détecté, pipeline standard")
        if progress_cb:
            progress_cb({"event": "wrapper_delegate_pipeline", "qid": qid})
        result = await self.pipeline.process(question, progress_cb=progress_cb, force_mode=force_mode)

        # --- 3) AUTO-GRAPHIQUES POST-RECONSTRUCTION (Q2, Q1.x, Q3.x) ---
        # Si le pipeline standard vient de repondre a une question canonique,
        # on declenche les graphes adaptes (Q2=SA+SB+Digamma, Q1.x=courbe RsP,
        # Q3.x=courbe gap). Pas d'impact sur la reponse principale.
        try:
            result = self._maybe_attach_question_graphs(qid, question, result)
        except Exception as exc:
            logger.warning(f"Q[{qid}] auto-graphs post-pipeline echec : {exc}")

        if progress_cb:
            progress_cb({"event": "wrapper_done", "qid": qid, "mode": "standard"})
        return result

    def _maybe_attach_question_graphs(
        self, qid: str, question: str, result: FinalAnswer
    ) -> FinalAnswer:
        """Detecte la question canonique repondue et ajoute les graphes en consequence.

        Logique :
          - structured_data contient 'position'/'prime' + intent 'reconstruction' -> Q2
          - structured_data contient un cas RsP (sym/chaos/ord) -> Q1.b/c/d
          - structured_data contient delta_p / gap_type -> Q3.a/b/c

        Le path PNG est appendu a la fin de answer_text avec un panneau lisible.
        """
        from ..visualization import detect_visualization_intent
        from ..engines.question_graphs import (
            generate_graphs_for_question, detect_gap_question, detect_rsp_question,
        )

        # Garde-fou: pas d'auto-graphes post-reponse si la question d'origine
        # n'exprimait pas explicitement une demande de visualisation.
        viz_intent = detect_visualization_intent(question)
        if viz_intent is None:
            return result

        data = result.structured_data or {}
        qcode: Optional[str] = None
        params: dict[str, Any] = {}

        # Heuristique de detection : intent reconstruction + position dans data
        # Le pipeline expose souvent {position, n, num_terms, p, prime, model}
        if "position" in data and ("prime" in data or "p" in data):
            qcode = "Q2"
            params = {"n": data.get("position")}
        elif "configuration" in data:
            cfg = str(data.get("configuration", "")).lower()
            if "ord" in cfg:
                qcode = "Q1.d"
            elif "chao" in cfg:
                qcode = "Q1.c"
            elif "sym" in cfg and "1x1" not in cfg:
                qcode = "Q1.b"
            elif "1x1" in cfg:
                qcode = "Q1.a"
        elif "delta_p" in data or "gap_type" in data:
            gtype = str(data.get("gap_type", "")).lower()
            if "++" in gtype or "+,+" in gtype:
                qcode = "Q3.a"
            elif "--" in gtype or "-,-" in gtype:
                qcode = "Q3.b"
            else:
                qcode = "Q3.c"

        # Si la question canonique est une RsP (Q1.x), on propage n_max detecte
        # par l'intent viz. Cela permet d'honorer explicitement "n=1 a n=100"
        # au lieu d'imposer le fallback de la map (ex: Q1.c = 1..15).
        if qcode in {"Q1.a", "Q1.b", "Q1.c", "Q1.d"}:
            params["k_max"] = int(viz_intent.n_max)

        if qcode is None:
            return result

        # Generer les PNG correspondants
        from pathlib import Path
        paths = generate_graphs_for_question(
            question=qcode,
            core=self.pipeline.spectral_core,
            params=params,
            output_dir=Path("data/graphs"),
            dpi=150,
        )
        if not paths:
            return result

        logger.info(
            f"Q[{qid}] auto-graphs {qcode} : {len(paths)} PNG genere(s)"
        )
        # Annexe au answer_text : mini panneau Markdown
        lines = ["", "", "---", "", f"### Graphique(s) auto-genere(s) ({qcode})"]
        for p in paths:
            lines.append(f"- `{p}`")
        lines.append("")
        lines.append(
            "_Genere automatiquement par Gabriel : un seul graphique pour la "
            "question correspondante, PNG haute resolution citable (150 dpi)._"
        )
        result.answer_text = result.answer_text + "\n".join(lines)
        # Ajout dans structured_data pour audit
        result.structured_data = {
            **(result.structured_data or {}),
            "auto_graphs_question": qcode,
            "auto_graphs_paths": [str(p) for p in paths],
        }
        return result

    def _try_visualization(self, qid: str, question: str) -> Optional[FinalAnswer]:
        """Detecte et execute une visualisation si la question le demande.

        Returns: FinalAnswer si une visualisation a ete generee, None sinon.
        """
        try:
            from ..visualization import detect_visualization_intent
        except ImportError as exc:
            logger.warning(f"Q[{qid}] Module visualization indisponible : {exc}")
            return None

        intent = detect_visualization_intent(question)
        if intent is None:
            return None

        logger.info(
            f"Q[{qid}] VISUALISATION DETECTEE : {intent.kind.value} "
            f"n={intent.n_min}..{intent.n_max} png={intent.want_png}"
        )

        try:
            return self._build_visualization_answer(qid, question, intent)
        except Exception as exc:
            logger.error(f"Q[{qid}] Echec generation visualisation : {exc}", exc_info=True)
            return None

    def _build_visualization_answer(
        self, qid: str, question: str, intent
    ) -> FinalAnswer:
        """Calcule la courbe demandee et construit un FinalAnswer riche."""
        from pathlib import Path
        from ..core.spectral_types import CandidateAnswer
        from ..visualization import (
            compute_curve, render_ascii, render_png, MATPLOTLIB_AVAILABLE,
        )

        # Si une config RsP est detectee (chaos-savard / ord / sym / 1x1),
        # on utilise compute_rsp_curve via le helper de question_graphs
        # plutot que la courbe classique compute_curve.
        if getattr(intent, "rsp_config", None) is not None:
            from ..engines.question_graphs import _build_rsp_curve_data
            curve = _build_rsp_curve_data(
                self.pipeline.spectral_core,
                intent.rsp_config,
                intent.n_min,
                intent.n_max,
            )
        else:
            # Calcul classique (entiers exacts)
            curve = compute_curve(
                self.pipeline.spectral_core,
                intent.kind,
                intent.n_min,
                intent.n_max,
                scale="auto",
            )

        # Rendu ASCII inclus dans la reponse texte
        ascii_view = render_ascii(curve, width=70, height=16)

        # PNG optionnel
        png_path: Optional[Path] = None
        if intent.want_png and MATPLOTLIB_AVAILABLE:
            try:
                png_path = render_png(curve, output_dir=Path("data/graphs"), dpi=150)
                logger.info(f"Q[{qid}] PNG genere : {png_path}")
            except Exception as exc:
                logger.warning(f"Q[{qid}] PNG echec : {exc}")

        # Construction du texte de reponse
        text_lines = [
            f"### Visualisation auto-generee : {curve.kind.value} (n={intent.n_min}..{intent.n_max})",
            "",
            f"**Detection** : {intent.reasoning}",
            "",
            "```",
            ascii_view,
            "```",
            "",
        ]
        summary = curve.summary()
        text_lines.extend([
            "**Resume statistique** :",
            f"  - Points calcules : {summary['n_points']}",
            f"  - Echelle : {summary['scale']}",
            f"  - y(n={summary['n_min']}) = {summary['y_first']:.6g}",
            f"  - y(n={summary['n_max']}) = {summary['y_last']:.6g}",
            f"  - y_min = {summary['y_min']:.6g}    y_max = {summary['y_max']:.6g}",
            "",
            f"**Formule** : {curve.formula}",
            "",
        ])
        if png_path:
            text_lines.append(f"**PNG exporte** : `{png_path}` (qualite article scientifique, 150 dpi)")
            text_lines.append("")
        text_lines.append(
            "_Astuce_ : pour controle complet, utilisez la commande explicite "
            f"`courbe {curve.kind.value} {intent.n_min}..{intent.n_max} --table --png`"
        )
        answer_text = "\n".join(text_lines)

        # Audit citable
        try:
            from ..audit import AuditStore as _AS
            store = self.pipeline.audit_store
            record = _AS.build_record(
                intervention_type="visualization_auto",
                question=question,
                certified_answer=(
                    f"Visualisation auto-declenchee : courbe {curve.kind.value} "
                    f"sur n={intent.n_min}..{intent.n_max} (echelle {curve.scale}). "
                    f"Formule : {curve.formula}."
                ),
                position=intent.n_min,
                prime_value=self.pipeline.spectral_core.get_prime_at_position(intent.n_min),
                citations_thy=[
                    "methode_spectral.thy::SA_def",
                    "methode_spectral.thy::SB_def",
                    "geometrie_spectre_premier.thy::D_def",
                ],
                toolkit_reports={
                    "visualization_auto": {
                        "intent": {
                            "kind": curve.kind.value,
                            "n_min": intent.n_min, "n_max": intent.n_max,
                            "want_png": intent.want_png,
                            "confidence": intent.confidence,
                            "reasoning": intent.reasoning,
                            "matched_keywords": intent.matched_keywords,
                        },
                        "curve_summary": summary,
                        "png_path": str(png_path) if png_path else None,
                    }
                },
                ratio="1/2",
            )
            store.save(record)
            answer_text += f"\n\n_Audit citable cree : id={record.id}_"
        except Exception as exc:
            logger.warning(f"Q[{qid}] Audit non sauvegarde : {exc}")

        candidate = CandidateAnswer(
            iteration=1,
            text=answer_text,
            structured_data={
                "viz_kind": curve.kind.value,
                "n_min": intent.n_min, "n_max": intent.n_max,
                "n_points": summary["n_points"],
                "scale": curve.scale,
                "y_first": summary["y_first"],
                "y_last": summary["y_last"],
                "formula": curve.formula,
                "png_path": str(png_path) if png_path else None,
                "confidence": intent.confidence,
            },
            score=10.0,
            critique="Visualisation auto-declenchee (deterministe, pas LLM)",
            grounded=True,
            used_engines=["auto_trigger", "spectral_core", "visualization"],
        )

        return FinalAnswer(
            question_id=qid,
            answer_text=answer_text,
            structured_data=candidate.structured_data,
            confidence=1.0,
            iterations_used=1,
            best_score=10.0,
            candidates=[candidate],
            explanation=f"Visualisation deterministe : {intent.reasoning}",
        )

    
    def _build_gap_answer(self, qid: str, question: str, result: GapResult) -> FinalAnswer:
        """Convertit GapResult en FinalAnswer."""
        from ..core.spectral_types import CandidateAnswer
        
        answer_text = self._render_gap_result(result)
        
        candidate = CandidateAnswer(
            iteration=1,
            text=answer_text,
            structured_data={
                "gap_type": result.gap_type,
                "p1": result.p1,
                "p2": result.p2,
                "gap_count": result.gap_count,
                "gap_float": result.gap_float,
                "position_min": result.position_min,
                "position_max": result.position_max,
                "position_suivant_min": result.position_suivant_min,
                "p_suivant_min": result.p_suivant_min,
                "SA_suivant_min": result.SA_suivant_min,
                "SB_max": result.SB_max,
                "digamma_max": result.digamma_max,
                "digamma_min": result.digamma_min,
                "formula_used": result.formula_used,
                "validation": result.validation,
            },
            score=10.0,
            critique="Calcul spectral certifié (kernel + spectral_core, pas LLM)",
            grounded=True,
            used_engines=["gap_solver", "spectral_core"],
        )
        
        return FinalAnswer(
            question_id=qid,
            answer_text=answer_text,
            structured_data=candidate.structured_data,
            confidence=1.0,
            iterations_used=1,
            best_score=10.0,
            candidates=[candidate],
            explanation=result.explanation,
        )

    def _build_composite_rejection_answer(
        self,
        qid: str,
        question: str,
        rejections: list,
        p1: int,
        p2: int,
    ) -> FinalAnswer:
        """Construit un FinalAnswer pédagogique quand l'un des nombres
        d'une requête d'écart est un entier composé.

        La réponse explique la preuve par l'absurde (aucune position
        spectrale possible pour un composé) et référence les théorèmes
        Isabelle/HOL correspondants (composite_not_prime_i, etc.).
        """
        from ..core.spectral_types import CandidateAnswer

        lines: list[str] = []
        lines.append("### Requete rejetee : entier compose detecte")
        lines.append("")
        lines.append(
            f"La Methode Spectrale ne s'applique qu'aux nombres premiers. "
            f"L'un ou les deux nombres de votre requete (`{p1}`, `{p2}`) "
            f"n'est pas premier."
        )
        lines.append("")
        for rej in rejections:
            lines.append(rej.to_pedagogical_text())
            lines.append("")

        lines.append("### Reference formelle (Isabelle/HOL)")
        lines.append(
            "Ce rejet est la contraposition effective du theoreme "
            "`composite_not_prime_i` demontre dans "
            "`theories/methode_spectral.thy`. La Methode Spectrale "
            "caracterise EXACTEMENT ℙ (l'ensemble des premiers) — ni plus, "
            "ni moins."
        )

        answer_text = "\n".join(lines)

        candidate = CandidateAnswer(
            iteration=1,
            text=answer_text,
            structured_data={
                "rejection_type": "composite_detected",
                "p1": p1,
                "p2": p2,
                "composites": [
                    {
                        "value": r.value,
                        "factors": r.factors,
                        "decomposition": r.decomposition_str,
                        "nearest_below": r.nearest_prime_below,
                        "nearest_above": r.nearest_prime_above,
                        "thy_reference": r.thy_reference,
                    }
                    for r in rejections
                ],
                "thy_theorem": "composite_not_prime_i",
                "thy_corollary": "spectral_method_exclusively_for_primes",
            },
            score=10.0,
            critique=(
                "Rejet certifie (preuve par l'absurde ancree sur "
                "composite_not_prime_i, theories/methode_spectral.thy)"
            ),
            grounded=True,
            used_engines=["composite_absurdity_prover", "isabelle_reference"],
        )

        return FinalAnswer(
            question_id=qid,
            answer_text=answer_text,
            structured_data=candidate.structured_data,
            confidence=1.0,
            iterations_used=1,
            best_score=10.0,
            candidates=[candidate],
            explanation=(
                f"Rejet pedagogique : {len(rejections)} entier(s) compose(s) "
                f"detecte(s) dans la requete d'ecart. Preuve par l'absurde "
                f"via composite_not_prime_i."
            ),
        )

    
    def _render_gap_result(self, result: GapResult) -> str:
        """Affiche le résultat d'écart."""
        lines = []
        lines.append(f"### Écart spectral {result.gap_type.upper()}")
        lines.append("")
        lines.append(f"**Entre {result.p1} et {result.p2}** : **{result.gap_count} nombres**")
        lines.append("")
        
        lines.append("**Détail du calcul** :")
        lines.append(f"  - Type : {result.gap_type}")
        lines.append(f"  - Position min : {result.position_min}")
        lines.append(f"  - Position max : {result.position_max}")
        lines.append(f"  - Position suivant min : {result.position_suivant_min}")
        lines.append(f"  - Premier suivant min : {result.p_suivant_min}")
        lines.append("")
        
        lines.append("**Valeurs spectrales** :")
        lines.append(f"  - SA(suivant_min) : {result.SA_suivant_min:.6f}")
        lines.append(f"  - SB(max) : {result.SB_max:.6f}")
        lines.append(f"  - digamma(max) : {result.digamma_max:.6f}")
        lines.append(f"  - digamma(min) : {result.digamma_min:.6f}")
        lines.append("")
        
        lines.append("**Formule** :")
        lines.append(f"  {result.formula_used}")
        lines.append("")
        
        lines.append("**Sources** :")
        sources = result.validation.get("source", [])
        if isinstance(sources, str):
            lines.append(f"  • {sources}")
        elif isinstance(sources, list):
            for src in sources:
                lines.append(f"  • {src}")
        
        if result.validation.get("zero_special"):
            lines.append("")
            lines.append("⚠️ **CAS SPÉCIAL** : Zéro a un rôle particulier (lien Riemann)")
        
        lines.append("")
        lines.append(f"**RÉSULTAT** : {result.gap_count} nombres entre {result.p1} et {result.p2}")
        
        return "\n".join(lines)

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
