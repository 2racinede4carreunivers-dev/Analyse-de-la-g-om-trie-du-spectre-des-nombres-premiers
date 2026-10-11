"""Axe 5 - Meta-raisonnement : auto-evaluation + memoire d'erreur.

Gabriel mesure sa confiance par categorie de question et apprend de ses erreurs
via un fichier `data/learning/errors.jsonl` append-only.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"        # >= 90% historique de succes
    MEDIUM = "MEDIUM"    # 60-90%
    LOW = "LOW"          # < 60%
    UNKNOWN = "UNKNOWN"  # pas assez de donnees


@dataclass
class CategoryStats:
    """Statistiques de succes pour une categorie de question."""
    category: str
    total: int = 0
    successes: int = 0

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.successes / self.total

    @property
    def confidence_level(self) -> ConfidenceLevel:
        if self.total < 3:
            return ConfidenceLevel.UNKNOWN
        rate = self.success_rate
        if rate >= 0.9:
            return ConfidenceLevel.HIGH
        if rate >= 0.6:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW


class MetaReasoner:
    """Auto-evaluation de Gabriel : confiance par categorie + memoire d'erreur."""

    DEFAULT_CATEGORIES = (
        "reconstruction_1_2", "reconstruction_1_3", "reconstruction_1_4",
        "gap_pos_pos", "gap_neg_neg", "gap_mixed",
        "ratio_1x1", "ratio_nxn_sym", "ratio_chaos", "ratio_ordonne",
        "riemann_conjecture", "isabelle_proof", "general",
    )

    def __init__(
        self,
        errors_file: Path | str = "data/learning/errors.jsonl",
        stats_file: Path | str = "data/learning/stats.json",
    ):
        self.errors_file = Path(errors_file)
        self.stats_file = Path(stats_file)
        self.stats: dict[str, CategoryStats] = {
            c: CategoryStats(category=c) for c in self.DEFAULT_CATEGORIES
        }
        self._load()

    def record(self, category: str, success: bool, details: dict | None = None) -> None:
        """Enregistre le resultat d'une interaction."""
        if category not in self.stats:
            self.stats[category] = CategoryStats(category=category)
        self.stats[category].total += 1
        if success:
            self.stats[category].successes += 1
        if not success:
            self._append_error(category, details or {})
        self._save_stats()

    def get_confidence(self, category: str) -> ConfidenceLevel:
        if category not in self.stats:
            return ConfidenceLevel.UNKNOWN
        return self.stats[category].confidence_level

    def report(self) -> dict[str, dict]:
        """Rapport global d'auto-evaluation."""
        return {
            cat: {
                "total": s.total,
                "successes": s.successes,
                "rate": round(s.success_rate, 3),
                "confidence": s.confidence_level.value,
            }
            for cat, s in self.stats.items()
        }

    def should_activate_slow_motion(self, category: str) -> bool:
        """Decide d'activer le Slow-Motion Debugger si confiance basse."""
        return self.get_confidence(category) == ConfidenceLevel.LOW

    # ----------------------------------------------------------------------
    # Persistence
    # ----------------------------------------------------------------------
    def _load(self) -> None:
        if self.stats_file.exists():
            try:
                data = json.loads(self.stats_file.read_text(encoding="utf-8"))
                for cat, s in data.items():
                    self.stats[cat] = CategoryStats(
                        category=cat,
                        total=int(s.get("total", 0)),
                        successes=int(s.get("successes", 0)),
                    )
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning(f"Impossible de charger {self.stats_file} : {exc}")

    def _save_stats(self) -> None:
        try:
            self.stats_file.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                cat: {"total": s.total, "successes": s.successes}
                for cat, s in self.stats.items()
            }
            self.stats_file.write_text(
                json.dumps(payload, indent=2), encoding="utf-8"
            )
        except OSError as exc:
            logger.warning(f"Impossible de sauvegarder stats : {exc}")

    def _append_error(self, category: str, details: dict) -> None:
        try:
            self.errors_file.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "category": category,
                "details": details,
            }
            with self.errors_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError as exc:
            logger.warning(f"Impossible d'append erreur : {exc}")
