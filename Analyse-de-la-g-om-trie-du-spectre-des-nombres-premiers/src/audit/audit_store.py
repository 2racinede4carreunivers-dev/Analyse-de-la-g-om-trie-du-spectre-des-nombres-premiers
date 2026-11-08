"""
AuditStore — Base de fiches d'audit JSON signees (citables) - AVEC CORRECTION UTF-8.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

from ..adapters.llm.utf8_sanitizer import UTF8Sanitizer


logger = logging.getLogger(__name__)


SUPPORTED_RATIOS = {"1/2", "1/3", "1/4", "1/2,1/3,1/4"}  # v2 : 3 modeles + combine
SUPPORTED_RATIO = "1/2"  # Compat retro : valeur par defaut


@dataclass
class AuditRecord:
    """Une fiche d'audit citable."""
    id: str                           # 8 caracteres hex (debut du sha256)
    timestamp: str                    # ISO 8601 UTC
    intervention_type: str            # "slow_motion_auto" | "debug_manual" | "toolkit" | "verifier"
    question: str
    ratio: str                        # toujours "1/2" dans cette v1
    position: Optional[int]
    prime_value: Optional[int]
    certified_answer: str
    decomposition: dict[str, Any] = field(default_factory=dict)
    timeline: list[dict[str, Any]] = field(default_factory=list)
    citations_thy: list[str] = field(default_factory=list)
    toolkit_reports: dict[str, Any] = field(default_factory=dict)
    user_comment: Optional[str] = None
    forced_bypass: list[str] = field(default_factory=list)
    signature_sha256: str = ""        # calcule a la sauvegarde

    def to_dict(self) -> dict[str, Any]:
        """Vue dict, AVANT signature (pour calcul de signature)."""
        d = asdict(self)
        # On exclut la signature elle-meme du payload signe
        d.pop("signature_sha256", None)
        return d

    def compute_signature(self) -> str:
        """SHA-256 sur le JSON canonique (cles triees, separateurs compacts).
        
        CORRECTION (2026-06-15): Nettoyer les surrogates UTF-8 mal formes.
        """
        sanitizer = UTF8Sanitizer()
        
        # Nettoyer tous les strings avant JSON
        d = self.to_dict()
        d_clean = self._sanitize_dict(d, sanitizer)
        
        # Créer le payload JSON
        payload = json.dumps(d_clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        
        # Double-check: nettoyer encore les surrogates si présents
        payload_clean = payload.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        
        return hashlib.sha256(payload_clean.encode('utf-8')).hexdigest()
    
    @staticmethod
    def _sanitize_dict(d: dict, sanitizer: UTF8Sanitizer) -> dict:
        """Récursivement nettoyer tous les strings d'un dict."""
        result = {}
        for k, v in d.items():
            if isinstance(v, str):
                result[k] = sanitizer.sanitize(v)
            elif isinstance(v, dict):
                result[k] = AuditRecord._sanitize_dict(v, sanitizer)
            elif isinstance(v, list):
                result[k] = AuditRecord._sanitize_list(v, sanitizer)
            else:
                result[k] = v
        return result
    
    @staticmethod
    def _sanitize_list(lst: list, sanitizer: UTF8Sanitizer) -> list:
        """Récursivement nettoyer tous les strings d'une liste."""
        result = []
        for item in lst:
            if isinstance(item, str):
                result.append(sanitizer.sanitize(item))
            elif isinstance(item, dict):
                result.append(AuditRecord._sanitize_dict(item, sanitizer))
            elif isinstance(item, list):
                result.append(AuditRecord._sanitize_list(item, sanitizer))
            else:
                result.append(item)
        return result


class AuditStore:
    """
    Persistance et acces aux fiches d'audit.
    
    Usage :
        store = AuditStore(base_dir="/home/agent/app/data/audits")
        record = AuditRecord(...)
        path = store.save(record)
        loaded = store.get(record.id)
        store.verify(loaded)   # True si signature valide
        store.list_records()   # tous
        store.cite(record.id, format="markdown")
    """

    FILENAME_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})_(\d{6})_([a-f0-9]{8})\.json$")

    def __init__(self, base_dir: str | Path = "/home/agent/app/data/audits"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.sanitizer = UTF8Sanitizer()
        logger.info("AuditStore initialise : %s", self.base_dir)

    # ---------- Construction / sauvegarde ----------

    @staticmethod
    def build_record(
        intervention_type: str,
        question: str,
        certified_answer: str,
        position: Optional[int] = None,
        prime_value: Optional[int] = None,
        decomposition: Optional[dict[str, Any]] = None,
        timeline: Optional[list[dict[str, Any]]] = None,
        citations_thy: Optional[list[str]] = None,
        toolkit_reports: Optional[dict[str, Any]] = None,
        user_comment: Optional[str] = None,
        forced_bypass: Optional[list[str]] = None,
        ratio: str = SUPPORTED_RATIO,
    ) -> AuditRecord:
        """Construit une AuditRecord avec id et timestamp auto-generes."""
        if ratio not in SUPPORTED_RATIOS:
            raise ValueError(
                f"AuditStore v2 supporte les rapports {SUPPORTED_RATIOS} "
                f"(recu : {ratio})."
            )
        record_id = uuid.uuid4().hex[:8]
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        record = AuditRecord(
            id=record_id,
            timestamp=ts,
            intervention_type=intervention_type,
            question=question,
            ratio=ratio,
            position=position,
            prime_value=prime_value,
            certified_answer=certified_answer,
            decomposition=decomposition or {},
            timeline=timeline or [],
            citations_thy=citations_thy or [],
            toolkit_reports=toolkit_reports or {},
            user_comment=user_comment,
            forced_bypass=forced_bypass or [],
        )
        try:
            record.signature_sha256 = record.compute_signature()
        except Exception as e:
            logger.warning(f"Erreur calcul signature audit : {e}")
            record.signature_sha256 = "ERROR_ENCODING"
        return record

    def save(self, record: AuditRecord) -> Path:
        """Persiste un audit sous YYYY-MM-DD_HHMMSS_<id>.json."""
        dt = datetime.fromisoformat(record.timestamp.replace("Z", "+00:00"))
        filename = f"{dt.strftime('%Y-%m-%d_%H%M%S')}_{record.id}.json"
        path = self.base_dir / filename
        full = record.to_dict()
        full["signature_sha256"] = record.signature_sha256
        
        # Nettoyer les strings avant sauvegarde
        full_clean = AuditRecord._sanitize_dict(full, self.sanitizer)
        
        path.write_text(json.dumps(full_clean, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Audit sauvegarde : %s (id=%s)", path.name, record.id)
        return path

    # ---------- Lecture ----------

    def _path_for(self, record_id: str) -> Optional[Path]:
        for p in self.base_dir.glob(f"*_{record_id}.json"):
            return p
        return None

    def get(self, record_id: str) -> Optional[AuditRecord]:
        path = self._path_for(record_id)
        if not path:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return AuditRecord(**data)

    def verify(self, record: AuditRecord) -> bool:
        """Verifie la signature SHA-256."""
        return record.compute_signature() == record.signature_sha256

    def list_records(
        self,
        position: Optional[int] = None,
        ratio: Optional[str] = None,
        intervention_type: Optional[str] = None,
        limit: int = 20,
    ) -> list[AuditRecord]:
        """Liste les audits avec filtres optionnels, tries du plus recent au plus ancien."""
        files = sorted(self.base_dir.glob("*.json"), reverse=True)
        out: list[AuditRecord] = []
        for p in files:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                rec = AuditRecord(**data)
            except Exception as exc:
                logger.warning("Audit illisible %s : %s", p.name, exc)
                continue
            if position is not None and rec.position != position:
                continue
            if ratio is not None and rec.ratio != ratio:
                continue
            if intervention_type is not None and rec.intervention_type != intervention_type:
                continue
            out.append(rec)
            if len(out) >= limit:
                break
        return out

    # ---------- Citation ----------

    def cite(self, record_id: str, format: str = "markdown") -> str:
        """Produit un bloc citable. format = 'markdown' | 'latex' | 'text'."""
        rec = self.get(record_id)
        if not rec:
            return f"(audit {record_id} introuvable)"
        valid = self.verify(rec)
        if format == "latex":
            return self._cite_latex(rec, valid)
        if format == "text":
            return self._cite_text(rec, valid)
        return self._cite_markdown(rec, valid)

    @staticmethod
    def _cite_markdown(rec: AuditRecord, signature_valid: bool) -> str:
        mark = "✓ verifiee" if signature_valid else "✗ INVALIDE"
        lines = [
            f"> **Audit `{rec.id}`** ({rec.timestamp})",
            f"> ",
            f"> **Question :** {rec.question}",
            f"> **Rapport :** {rec.ratio}",
        ]
        if rec.position is not None:
            lines.append(f"> **Position :** {rec.position}")
        if rec.prime_value is not None:
            lines.append(f"> **Nombre premier reconstruit :** {rec.prime_value}")
        lines.append(f"> **Reponse certifiee :** {rec.certified_answer.splitlines()[0][:200]}")
        if rec.citations_thy:
            lines.append(f"> ")
            lines.append(f"> **Citations (.thy + plan cognitif) :**")
            for c in rec.citations_thy[:5]:
                lines.append(f"> - {c}")
        if rec.toolkit_reports:
            lines.append(f"> ")
            lines.append(f"> **Validation croisee (toolkit) :**")
            for tool, report in rec.toolkit_reports.items():
                ok = (report.get("identity_verified") or report.get("all_proven")
                      or report.get("proven"))
                mark2 = "✓" if ok else "?"
                lines.append(f"> - {mark2} {tool}")
        lines.append(f"> ")
        lines.append(f"> **Signature SHA-256 :** `{rec.signature_sha256}` ({mark})")
        return "\n".join(lines)

    @staticmethod
    def _cite_latex(rec: AuditRecord, signature_valid: bool) -> str:
        mark = "verifiee" if signature_valid else "INVALIDE"
        body = [
            "\\begin{quote}",
            f"\\textbf{{Audit \\texttt{{{rec.id}}}}} ({rec.timestamp})\\\\",
            f"\\textbf{{Question :}} {rec.question}\\\\",
            f"\\textbf{{Rapport :}} ${rec.ratio}$\\\\",
        ]
        if rec.position is not None:
            body.append(f"\\textbf{{Position :}} {rec.position}\\\\")
        if rec.prime_value is not None:
            body.append(f"\\textbf{{Nombre premier reconstruit :}} {rec.prime_value}\\\\")
        body.append(f"\\textbf{{Reponse certifiee :}} {rec.certified_answer.splitlines()[0][:200]}\\\\")
        if rec.citations_thy:
            body.append("\\textbf{Citations :} \\begin{itemize}")
            for c in rec.citations_thy[:5]:
                body.append(f"\\item {c}")
            body.append("\\end{itemize}")
        body.append(f"\\textbf{{Signature SHA-256 :}} \\texttt{{{rec.signature_sha256}}} ({mark})")
        body.append("\\end{quote}")
        return "\n".join(body)

    @staticmethod
    def _cite_text(rec: AuditRecord, signature_valid: bool) -> str:
        mark = "verifiee" if signature_valid else "INVALIDE"
        lines = [
            f"AUDIT {rec.id} ({rec.timestamp})",
            "-" * 60,
            f"Question : {rec.question}",
            f"Rapport  : {rec.ratio}",
        ]
        if rec.position is not None:
            lines.append(f"Position : {rec.position}")
        if rec.prime_value is not None:
            lines.append(f"Premier  : {rec.prime_value}")
        lines.append(f"Reponse  : {rec.certified_answer.splitlines()[0][:200]}")
        if rec.citations_thy:
            lines.append("Citations :")
            for c in rec.citations_thy[:5]:
                lines.append(f"  - {c}")
        lines.append(f"Signature SHA-256 : {rec.signature_sha256} ({mark})")
        return "\n".join(lines)

    @staticmethod
    def summary_table(records: Iterable[AuditRecord]) -> str:
        """Rendu texte compact d'une liste d'audits."""
        rows = [f"{'ID':<10} {'DATE':<20} {'TYPE':<18} {'POS':<6} {'PRIME':<7} {'RATIO':<6}"]
        rows.append("-" * 70)
        for r in records:
            pos = str(r.position) if r.position is not None else "-"
            pr = str(r.prime_value) if r.prime_value is not None else "-"
            rows.append(
                f"{r.id:<10} {r.timestamp[:19]:<20} {r.intervention_type:<18} "
                f"{pos:<6} {pr:<7} {r.ratio:<6}"
            )
        return "\n".join(rows)
