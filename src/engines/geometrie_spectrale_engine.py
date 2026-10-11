"""GeometrieSpectraleEngine : moteur cognitif unifie sur les 3 modeles spectraux.

Repond aux **8 questions canoniques** de la Methode Spectrale de Philippe Thomas
Savard, pour les **3 modeles** (1/2, 1/3, 1/4), avec exactitude infinie
(Fraction).

Les 8 questions :
  Q1. Rapport spectral - 4 sous-cas :
        a) 1x1                       -> RsP(n1, n2)
        b) n×n symetrique            -> RsP(A_pos, B_pos), |A|=|B|
        c) asymetrique chaotique     -> RsP(A_pos, B_pos), tailles arbitraires
        d) asymetrique ordonnee      -> RsP(A_pos, B_pos), ordre croissant
  Q2. Reconstruction du N-ieme nombre premier
  Q3. Calcul de gap - 3 sous-cas :
        a) (+,+)
        b) (-,-)
        c) (-,+)

Ce moteur centralise toutes les capacites et permet la comparaison entre
modeles (ex : Quelle est la difference entre le modele 1/2 et 1/4 pour
reconstruire 101 ?).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional, Sequence

from ..spectral.spectral_models import (
    SpectralModel,
    get_model,
    list_models,
    all_models,
    RatioResult,
    ReconstructionResult,
    GapResult,
)

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Rapports unifies
# --------------------------------------------------------------------------
@dataclass
class ComparativeReport:
    """Rapport comparant le meme calcul sur les 3 modeles."""
    question: str                                       # "Q1.a" | "Q2" | "Q3.a" ...
    description: str                                    # Description en francais
    results_by_model: dict[str, object] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_text(self) -> str:
        """Rendu textuel pret pour la CLI Gabriel."""
        lines = [
            f"=== {self.question} : {self.description} ===",
            "",
        ]
        for model_name, res in self.results_by_model.items():
            lines.append(f"  [Modele {model_name}]")
            if isinstance(res, RatioResult):
                lines.append(
                    f"    ratio = {res.ratio}  (attendu {res.expected}, "
                    f"exact={res.is_exact}, close={res.is_close}, "
                    f"delta={float(res.convergence_delta):.6e})"
                )
                lines.append(f"    formule : {res.formula}")
            elif isinstance(res, ReconstructionResult):
                lines.append(
                    f"    reconstruct({res.n}) = {res.reconstructed_prime}  "
                    f"(actuel : {res.actual_prime}, exact={res.is_exact})"
                )
                lines.append(f"    digamma = {res.digamma}")
                lines.append(f"    formule : {res.formula}")
            elif isinstance(res, GapResult):
                lines.append(
                    f"    gap({res.p1}, {res.p2}) = {res.gap_count}  (cas {res.case})"
                )
                lines.append(f"    formule : {res.formula}")
            lines.append("")
        if self.notes:
            lines.append("  Notes :")
            for n in self.notes:
                lines.append(f"    - {n}")
        return "\n".join(lines)


# --------------------------------------------------------------------------
# Moteur principal
# --------------------------------------------------------------------------
class GeometrieSpectraleEngine:
    """Moteur cognitif unifie sur les 3 modeles spectraux.

    Usage typique :
        engine = GeometrieSpectraleEngine(spectral_core)

        # Q1.a : RsP 1x1 sur tous les modeles
        report = engine.compute_rsp_1x1_all_models(3, 5)
        print(report.to_text())

        # Q2 : reconstruction sur tous les modeles
        report = engine.reconstruct_all_models(26)  # 26eme prime = 101
        print(report.to_text())
    """

    QUESTIONS = {
        "Q1.a": "Rapport spectral 1x1",
        "Q1.b": "Rapport spectral n×n symetrique",
        "Q1.c": "Rapport spectral asymetrique chaotique",
        "Q1.d": "Rapport spectral asymetrique ordonnee",
        "Q2":   "Reconstruction du N-ieme nombre premier",
        "Q3.a": "Gap (+,+)",
        "Q3.b": "Gap (-,-)",
        "Q3.c": "Gap (-,+)",
    }

    def __init__(self, spectral_core=None):
        """Initialise le moteur.

        Args:
            spectral_core: instance de SpectralMethodCore (optionnel) pour
              acceder a `get_prime_at_position`. Si None, on n'utilise que
              les modeles purs.
        """
        self.spectral_core = spectral_core
        self.models: dict[str, SpectralModel] = {
            name: get_model(name) for name in list_models()
        }

    # ------------------------------------------------------------------
    # Q1 - Rapports spectraux (4 sous-cas)
    # ------------------------------------------------------------------
    def compute_rsp_1x1(self, model_name: str, n1: int, n2: int) -> RatioResult:
        """Q1.a sur un seul modele."""
        return self.models[model_name].RsP_1x1(n1, n2)

    def compute_rsp_1x1_all_models(self, n1: int, n2: int) -> ComparativeReport:
        """Q1.a sur les 3 modeles."""
        report = ComparativeReport(
            question="Q1.a",
            description=self.QUESTIONS["Q1.a"] + f" pour (n1={n1}, n2={n2})",
        )
        for name, model in self.models.items():
            report.results_by_model[name] = model.RsP_1x1(n1, n2)
        report.notes.append(
            "Le ratio 1/{n} est EXACT pour le cas 1x1 (calcul en Fraction)."
        )
        return report

    def compute_rsp_nxn(
        self,
        model_name: str,
        A_positions: Sequence[int],
        B_positions: Sequence[int],
        case: str = "nxn_symetrique",
    ) -> RatioResult:
        """Q1.b/c/d sur un seul modele."""
        return self.models[model_name].RsP_nxn(A_positions, B_positions, case)

    def compute_rsp_nxn_all_models(
        self,
        A_positions: Sequence[int],
        B_positions: Sequence[int],
        case: str = "nxn_symetrique",
    ) -> ComparativeReport:
        """Q1.b/c/d sur les 3 modeles."""
        q_map = {
            "nxn_symetrique": "Q1.b",
            "asym_chaotique": "Q1.c",
            "asym_ordonnee":  "Q1.d",
        }
        q = q_map.get(case, "Q1.b")
        report = ComparativeReport(
            question=q,
            description=(
                f"{self.QUESTIONS[q]}  "
                f"A_pos={list(A_positions)}  B_pos={list(B_positions)}"
            ),
        )
        for name, model in self.models.items():
            report.results_by_model[name] = model.RsP_nxn(A_positions, B_positions, case)
        # Note explicative selon le cas
        if case == "nxn_symetrique":
            report.notes.append("Cas symetrique (|A|=|B|) : ratio EXACT en Fraction.")
        else:
            report.notes.append(
                "Cas asymetrique : convergence vers le ratio cible "
                "(|delta| diminue quand n augmente). Le calcul est exact, "
                "mais le ratio n'est pas exactement 1/{n} pour des petits n."
            )
        return report

    # ------------------------------------------------------------------
    # Q2 - Reconstruction du N-ieme nombre premier
    # ------------------------------------------------------------------
    def reconstruct_nth_prime(
        self,
        model_name: str,
        n: int,
        actual_prime: Optional[int] = None,
    ) -> ReconstructionResult:
        """Q2 sur un seul modele. Si actual_prime non fourni, le prend dans la table."""
        if actual_prime is None:
            if self.spectral_core is None:
                raise ValueError(
                    "actual_prime requis si spectral_core non fourni au moteur"
                )
            actual_prime = self.spectral_core.get_prime_at_position(n)
            if actual_prime is None:
                raise ValueError(f"Position {n} hors de la table primes")
        return self.models[model_name].reconstruct_nth_prime(n, actual_prime)

    def reconstruct_all_models(
        self,
        n: int,
        actual_prime: Optional[int] = None,
    ) -> ComparativeReport:
        """Q2 sur les 3 modeles."""
        if actual_prime is None:
            if self.spectral_core is None:
                raise ValueError(
                    "actual_prime requis si spectral_core non fourni au moteur"
                )
            actual_prime = self.spectral_core.get_prime_at_position(n)
            if actual_prime is None:
                raise ValueError(f"Position {n} hors de la table primes")
        report = ComparativeReport(
            question="Q2",
            description=(
                f"{self.QUESTIONS['Q2']}  "
                f"(n={n}, prime de reference={actual_prime})"
            ),
        )
        for name, model in self.models.items():
            report.results_by_model[name] = model.reconstruct_nth_prime(n, actual_prime)
        report.notes.append(
            "Les 3 modeles doivent reconstruire EXACTEMENT le meme nombre premier."
        )
        return report

    # ------------------------------------------------------------------
    # Q3 - Gap (3 cas)
    # ------------------------------------------------------------------
    def compute_gap(self, model_name: str, p1: int, p2: int) -> GapResult:
        """Q3 sur un seul modele."""
        return self.models[model_name].gap(p1, p2)

    def compute_gap_all_models(self, p1: int, p2: int) -> ComparativeReport:
        """Q3 sur les 3 modeles (resultat identique : le gap ne depend pas du modele)."""
        # Detection du cas
        if p1 >= 0 and p2 >= 0:
            q, case_desc = "Q3.a", "(+,+)"
        elif p1 < 0 and p2 < 0:
            q, case_desc = "Q3.b", "(-,-)"
        else:
            q, case_desc = "Q3.c", "(-,+)"
        report = ComparativeReport(
            question=q,
            description=(
                f"{self.QUESTIONS[q]}  entre p1={p1} et p2={p2} (cas {case_desc})"
            ),
        )
        for name, model in self.models.items():
            report.results_by_model[name] = model.gap(p1, p2)
        report.notes.append(
            "Le gap est independant du modele (formule purement entiere)."
        )
        return report

    # ------------------------------------------------------------------
    # Methode unifiee : answer_all_questions(...)
    # ------------------------------------------------------------------
    def answer_all_questions(
        self,
        n_for_reconstruction: int = 26,
        rsp_n1: int = 3,
        rsp_n2: int = 5,
        nxn_A: Sequence[int] = (2, 3, 4),
        nxn_B: Sequence[int] = (5, 6, 7),
        chaos_A: Sequence[int] = (2, 9, 11),
        chaos_B: Sequence[int] = (7, 5, 10, 15),
        ord_A: Sequence[int] = (2, 4, 6),
        ord_B: Sequence[int] = (3, 5, 7),
        gap_pp: tuple[int, int] = (11, 23),
        gap_nn: tuple[int, int] = (-19, -5),
        gap_np: tuple[int, int] = (-7, 11),
    ) -> list[ComparativeReport]:
        """Repond aux 8 questions canoniques sur les 3 modeles. Total : 8 rapports."""
        reports: list[ComparativeReport] = []
        # Q1.a
        reports.append(self.compute_rsp_1x1_all_models(rsp_n1, rsp_n2))
        # Q1.b
        reports.append(
            self.compute_rsp_nxn_all_models(nxn_A, nxn_B, case="nxn_symetrique")
        )
        # Q1.c
        reports.append(
            self.compute_rsp_nxn_all_models(chaos_A, chaos_B, case="asym_chaotique")
        )
        # Q1.d
        reports.append(
            self.compute_rsp_nxn_all_models(ord_A, ord_B, case="asym_ordonnee")
        )
        # Q2
        reports.append(self.reconstruct_all_models(n_for_reconstruction))
        # Q3.a
        reports.append(self.compute_gap_all_models(*gap_pp))
        # Q3.b
        reports.append(self.compute_gap_all_models(*gap_nn))
        # Q3.c
        reports.append(self.compute_gap_all_models(*gap_np))
        return reports

    # ------------------------------------------------------------------
    # Helpers de presentation
    # ------------------------------------------------------------------
    def list_questions(self) -> dict[str, str]:
        """Liste des 8 questions canoniques."""
        return dict(self.QUESTIONS)

    def list_supported_models(self) -> list[str]:
        """Liste des 3 modeles supportes."""
        return list(self.models.keys())

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
