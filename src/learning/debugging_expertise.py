"""
DEBUGGING EXPERTISE MEMORY - Meta-learning du 7ème loop.

Objectif :
  Archiver non seulement la SOLUTION (reformulation) mais aussi
  la STRATEGIE, les ETAPES, les DECISONS du debugger.
  
  Creer une "memoire d'expertise" que Gabriel peut consulter
  et appliquer pour des problemes similaires futurs.

Architecture :
  DebugSession
    ├─ question_pattern (regex + keywords)
    ├─ coherence_signature (type d'incoherence detectée)
    ├─ timeline_steps (les 8 etapes T1-T8 EXECUTEES)
    ├─ toolkit_reports (sympy, z3, spectral_core utilisés)
    ├─ reformulation_applied (la transformation effectuée)
    └─ success_metrics (score avant/après, validation)
  
  ExpertiseLibrary (en-mémoire + DB)
    └─ [DebugSession] x N (cumul des sessions reussies)

Utilisation future :
  1. Nouvelle question Q' → detect pattern + coherence_signature
  2. Chercher dans ExpertiseLibrary les sessions avec même pattern
  3. Si trouvée : proposer les mêmes etapes/tactiques
  4. Appliquer la strategie AVANT de relancer multiloop
  5. Valider résultat → mettre à jour expertise (incremental)
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


logger = logging.getLogger(__name__)


@dataclass
class ToolkitUsage:
    """Enregistre l'utilisation d'un outil du toolkit (sympy, z3, spectral_core, etc.)."""
    toolkit_name: str  # "spectral_core", "sympy", "z3", "isabelle"
    operation: str     # "reconstruct_prime_1_2", "solve_equation", etc.
    input_values: dict[str, Any]
    output_values: dict[str, Any]
    success: bool
    execution_time_ms: float
    notes: str = ""


@dataclass
class TimelineStep:
    """Une étape du timeline slow-motion (T1-T8)."""
    step: int
    label: str
    detail: str
    decision_taken: str = ""  # La décision/action Gabriel a pris à cette étape
    toolkit_used: Optional[ToolkitUsage] = None


@dataclass
class CoherenceSignature:
    """Signature d'incoherence pour matching futur."""
    incoherence_type: str  # "value_mismatch", "logical_contradiction", "incomplete_definition", etc.
    affected_concepts: list[str] = field(default_factory=list)  # ["digamma_calc", "prime_equation", ...]
    affected_sections: list[str] = field(default_factory=list)  # ["narrative", "HOL", "calculation", ...]
    severity: float = 0.0  # 0.0-1.0


@dataclass
class ReformulationStrategy:
    """La stratégie de reformulation appliquée."""
    segments_bypassed: list[str]  # Quels segments ont été ignorés
    canonical_form: str            # La forme canonique de la question
    decomposition_method: str       # Comment la question a été décomposée
    reconstruction_steps: list[str] # Les étapes pour reconstruire la réponse
    key_insight: str               # La clé pour résoudre le problème


@dataclass
class DebugSessionRecord:
    """Enregistrement complet d'une session de débogage réussie."""
    session_id: str
    timestamp: str
    
    # Question + contexte
    original_question: str
    question_pattern: str           # Regex utilisée pour matcher les questions similaires
    domain: str                     # "spectral", "ratio", "gap", etc.
    ratio_model: str                # "1/2", "1/3", "1/4"
    
    # Problème détecté
    coherence_signature: CoherenceSignature
    coherence_score_before: float
    
    # Processus de débogage
    timeline_steps: list[TimelineStep] = field(default_factory=list)
    toolkit_usages: list[ToolkitUsage] = field(default_factory=list)
    reformulation_strategy: Optional[ReformulationStrategy] = None
    
    # Résultat
    reformulated_question: str
    final_answer: str
    coherence_score_after: float
    success_validation: dict[str, Any] = field(default_factory=dict)
    
    # Meta-learning
    lessons_learned: list[str] = field(default_factory=list)
    similar_patterns_seen: list[str] = field(default_factory=list)
    confidence: float = 1.0
    
    def to_dict(self) -> dict:
        """Convertit en dict sérializable."""
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "original_question": self.original_question,
            "question_pattern": self.question_pattern,
            "domain": self.domain,
            "ratio_model": self.ratio_model,
            "coherence_signature": asdict(self.coherence_signature),
            "coherence_score_before": self.coherence_score_before,
            "timeline_steps": [
                {
                    "step": ts.step,
                    "label": ts.label,
                    "detail": ts.detail,
                    "decision_taken": ts.decision_taken,
                    "toolkit_used": asdict(ts.toolkit_used) if ts.toolkit_used else None,
                }
                for ts in self.timeline_steps
            ],
            "toolkit_usages": [asdict(tu) for tu in self.toolkit_usages],
            "reformulation_strategy": asdict(self.reformulation_strategy) if self.reformulation_strategy else None,
            "reformulated_question": self.reformulated_question,
            "final_answer": self.final_answer,
            "coherence_score_after": self.coherence_score_after,
            "success_validation": self.success_validation,
            "lessons_learned": self.lessons_learned,
            "similar_patterns_seen": self.similar_patterns_seen,
            "confidence": self.confidence,
        }


class ExpertiseLibrary:
    """
    Bibliothèque d'expertise en débogage.
    
    En mémoire : les sessions récentes + les plus fréquentes
    Sur disque : archive complète JSON
    """
    
    def __init__(self, base_dir: Path = Path("/home/agent/app/data/expertise")):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Index en mémoire
        self.sessions: dict[str, DebugSessionRecord] = {}
        self.pattern_index: dict[str, list[str]] = {}  # pattern_regex -> [session_id, ...]
        self.signature_index: dict[str, list[str]] = {}  # coherence_sig_hash -> [session_id, ...]
        
        self._load_from_disk()
        logger.info(
            "ExpertiseLibrary initialized : base_dir=%s, %d sessions loaded",
            self.base_dir, len(self.sessions),
        )
    
    def add_session(self, record: DebugSessionRecord) -> str:
        """Ajoute une session de débogage réussie à la bibliothèque."""
        self.sessions[record.session_id] = record
        
        # Index par pattern
        if record.question_pattern not in self.pattern_index:
            self.pattern_index[record.question_pattern] = []
        self.pattern_index[record.question_pattern].append(record.session_id)
        
        # Index par signature d'incoherence
        sig_hash = self._hash_signature(record.coherence_signature)
        if sig_hash not in self.signature_index:
            self.signature_index[sig_hash] = []
        self.signature_index[sig_hash].append(record.session_id)
        
        # Sauvegarder sur disque
        self._save_session_to_disk(record)
        
        logger.info("Session ajoutée : id=%s, pattern=%s", record.session_id, record.question_pattern)
        return record.session_id
    
    def find_similar_sessions(
        self,
        question: str,
        coherence_sig: Optional[CoherenceSignature] = None,
        limit: int = 5,
    ) -> list[DebugSessionRecord]:
        """
        Cherche les sessions de débogage similaires pour réutiliser la stratégie.
        
        Critères :
          1. Pattern de question (regex match)
          2. Signature d'incoherence similaire
          3. Score de confiance élevé
        """
        candidates = []
        
        # Test 1 : pattern matching
        for pattern, session_ids in self.pattern_index.items():
            try:
                if re.search(pattern, question, re.IGNORECASE):
                    for sid in session_ids:
                        record = self.sessions[sid]
                        candidates.append((record, "pattern_match", record.confidence))
            except re.error:
                pass
        
        # Test 2 : signature matching
        if coherence_sig:
            sig_hash = self._hash_signature(coherence_sig)
            if sig_hash in self.signature_index:
                for sid in self.signature_index[sig_hash]:
                    record = self.sessions[sid]
                    if record not in [c[0] for c in candidates]:
                        candidates.append((record, "signature_match", record.confidence * 1.2))
        
        # Trier par confiance et retourner les top
        candidates.sort(key=lambda x: x[2], reverse=True)
        return [rec for rec, _, _ in candidates[:limit]]
    
    def get_reformulation_strategy_for_pattern(
        self,
        question: str,
    ) -> Optional[ReformulationStrategy]:
        """
        Récupère la stratégie de reformulation pour une question similaire.
        Si trouvée, Gabriel peut l'appliquer directement sans relancer le debugger.
        """
        similar = self.find_similar_sessions(question, limit=1)
        if similar and similar[0].reformulation_strategy:
            logger.info(
                "Stratégie reformulation trouvée : session=%s, confidence=%.2f",
                similar[0].session_id, similar[0].confidence,
            )
            return similar[0].reformulation_strategy
        return None
    
    def get_lessons_learned(self, domain: str = "", ratio_model: str = "") -> list[str]:
        """Récupère les leçons apprises pour un domaine/ratio."""
        lessons = []
        for record in self.sessions.values():
            if (not domain or record.domain == domain) and \
               (not ratio_model or record.ratio_model == ratio_model):
                lessons.extend(record.lessons_learned)
        return list(set(lessons))  # Déduplicate
    
    def _hash_signature(self, sig: CoherenceSignature) -> str:
        """Hash une signature d'incoherence pour indexation rapide."""
        payload = f"{sig.incoherence_type}:{'|'.join(sorted(sig.affected_concepts))}"
        return hashlib.md5(payload.encode()).hexdigest()[:8]
    
    def _save_session_to_disk(self, record: DebugSessionRecord) -> None:
        """Sauvegarde une session sur disque en JSON."""
        file_path = self.base_dir / f"{record.session_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record.to_dict(), f, indent=2, ensure_ascii=False)
        logger.debug("Session sauvegardée : %s", file_path)
    
    def _load_from_disk(self) -> None:
        """Charge toutes les sessions depuis le disque."""
        for json_file in self.base_dir.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Reconstruction partielle (load rapide)
                record = DebugSessionRecord(
                    session_id=data["session_id"],
                    timestamp=data["timestamp"],
                    original_question=data["original_question"],
                    question_pattern=data["question_pattern"],
                    domain=data.get("domain", "spectral"),
                    ratio_model=data.get("ratio_model", "1/2"),
                    coherence_signature=CoherenceSignature(**data.get("coherence_signature", {})),
                    coherence_score_before=data.get("coherence_score_before", 0.0),
                    reformulated_question=data.get("reformulated_question", ""),
                    final_answer=data.get("final_answer", ""),
                    coherence_score_after=data.get("coherence_score_after", 1.0),
                    lessons_learned=data.get("lessons_learned", []),
                    confidence=data.get("confidence", 1.0),
                )
                self.sessions[record.session_id] = record
                
                # Rebuild index
                if record.question_pattern not in self.pattern_index:
                    self.pattern_index[record.question_pattern] = []
                self.pattern_index[record.question_pattern].append(record.session_id)
                
                sig_hash = self._hash_signature(record.coherence_signature)
                if sig_hash not in self.signature_index:
                    self.signature_index[sig_hash] = []
                self.signature_index[sig_hash].append(record.session_id)
            except (json.JSONDecodeError, KeyError, TypeError) as exc:
                logger.warning("Erreur chargement session %s : %s", json_file, exc)
    
    def export_summary(self) -> dict[str, Any]:
        """Exporte un résumé de l'expertise pour affichage."""
        return {
            "total_sessions": len(self.sessions),
            "patterns_known": len(self.pattern_index),
            "incoherence_types": len(self.signature_index),
            "avg_confidence": sum(r.confidence for r in self.sessions.values()) / max(len(self.sessions), 1),
            "domains": list(set(r.domain for r in self.sessions.values())),
            "most_common_pattern": max(
                self.pattern_index.items(),
                key=lambda x: len(x[1]),
                default=("", [])
            )[0],
        }
