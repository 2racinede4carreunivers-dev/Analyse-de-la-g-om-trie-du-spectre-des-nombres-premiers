"""LogicalLoop - boucle logique de sursaut + reformulation modeste.

A partir d'une `DecomposedRequest` et d'une `CertaintyEvaluation`, applique
les strategies de sursaut (skip_strategy) associees a chaque critere viole
pour produire une `ModestRequest` :

  - REQUETE_MODESTE = juste milieu entre la requete originale (incoherente)
    et une version triviale, qui satisfait tous les criteres du modele
    de certitude tout en preservant l'INTENT principal de l'utilisateur.

  - La requete modeste est ENSUITE resolue par spectral_core (deterministe)
    pour produire une "reponse modeste" qui est CERTAINEMENT correcte.

Strategies de sursaut implementees :

  - drop_position    : oublier la position si hors table -> ramener a 1
  - default_to_half  : forcer ratio = 1/2 si ratio invalide
  - normalize_intent : forcer intent = reconstruction si conflit
  - drop_tuples      : retirer les tuples vides
  - drop_symmetry    : passer en asymetrique si |A| != |B|
  - filter_to_primes : enlever les non-premiers des tuples
  - downgrade_to_1x1 : si rapport 1/2 inatteignable en NxN, basculer en 1x1
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .certainty_model import CertaintyEvaluation, CRITERIA_BY_CODE
from .request_decomposer import DecomposedRequest


@dataclass
class ModestRequest:
    """Requete reformulee modeste, satisfaisant tous les criteres."""
    # Texte humain lisible de la requete reformulee
    canonical_text: str
    # Intent retenu
    intent: str
    ratio: str  # "1/2" | "1/3" | "1/4"
    # Position (si reconstruction)
    position: Optional[int] = None
    # Tuples (si ratio_spectral_nxn / ratio_spectral)
    tuple_A: Optional[list[int]] = None
    tuple_B: Optional[list[int]] = None
    # Trace des sursauts appliques
    skips_applied: list[dict[str, Any]] = field(default_factory=list)
    # Texte de la chaine de raisonnement (pour la timeline)
    reasoning: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_text": self.canonical_text,
            "intent": self.intent,
            "ratio": self.ratio,
            "position": self.position,
            "tuple_A": self.tuple_A,
            "tuple_B": self.tuple_B,
            "skips_applied": self.skips_applied,
            "reasoning": self.reasoning,
        }


class LogicalLoop:
    """Boucle logique qui produit une requete modeste a partir d'une evaluation."""

    def __init__(self, spectral_core=None):
        self.spectral_core = spectral_core

    # ------------------------------------------------------------------
    def derive_modest_request(
        self,
        decomposed: DecomposedRequest,
        evaluation: CertaintyEvaluation,
    ) -> ModestRequest:
        """Applique iterativement les strategies de sursaut.

        Returns une ModestRequest qui :
          - retient l'intent et le maximum d'information utile
          - retire/simplifie ce qui viole les criteres
          - est garantie cohérente (tous les criteres satisfaits par construction)
        """
        # Etat de travail (copie modifiable)
        state = _WorkingState.from_decomposed(decomposed)
        reasoning: list[str] = []
        skips: list[dict[str, Any]] = []

        for crit_result in evaluation.results:
            if crit_result.passed:
                continue
            spec = CRITERIA_BY_CODE[crit_result.code]
            applied = self._apply_skip(state, spec.skip_strategy, crit_result)
            if applied:
                skips.append({
                    "criterion": spec.code,
                    "strategy": spec.skip_strategy,
                    "before": applied["before"],
                    "after": applied["after"],
                    "rationale": applied["rationale"],
                })
                reasoning.append(applied["rationale"])

        # Synthese : produire le texte canonique de la requete modeste
        canonical_text = self._render_canonical(state)
        reasoning.append(f"Requete modeste construite : {canonical_text}")

        return ModestRequest(
            canonical_text=canonical_text,
            intent=state.intent,
            ratio=state.ratio,
            position=state.position,
            tuple_A=state.tuple_A,
            tuple_B=state.tuple_B,
            skips_applied=skips,
            reasoning=reasoning,
        )

    # ------------------------------------------------------------------
    def _apply_skip(
        self,
        state: "_WorkingState",
        strategy: str,
        crit: Any,
    ) -> Optional[dict[str, Any]]:
        """Applique UN sursaut sur l'etat ; retourne le diff ou None si non applicable."""

        # ---------- drop_position ----------
        if strategy == "drop_position":
            before = state.position
            # Si la position est hors table, on la ramene a min(N_max, 10)
            n_max = self._n_max()
            if before is None:
                return None
            new_pos = min(max(1, before), n_max) if before > n_max else 1
            # Cas plus simple : si hors table, on bascule vers position=10 (cas pedagogique)
            new_pos = 10 if (before > n_max or before < 1) else before
            state.position = new_pos
            return {
                "before": before, "after": new_pos,
                "rationale": (
                    f"Position {before} hors table (max={n_max}) -> sursaut "
                    f"vers position={new_pos} (cas elementaire repondable)."
                ),
            }

        # ---------- default_to_half ----------
        if strategy == "default_to_half":
            before = state.ratio
            state.ratio = "1/2"
            return {
                "before": before, "after": "1/2",
                "rationale": (
                    f"Ratio '{before}' non supporte -> sursaut vers ratio canonique 1/2."
                ),
            }

        # ---------- normalize_intent ----------
        if strategy == "normalize_intent":
            before = state.intent
            state.intent = "reconstruction" if state.position else "ratio_spectral_nxn"
            return {
                "before": before, "after": state.intent,
                "rationale": (
                    f"Intent '{before}' incompatible -> sursaut vers '{state.intent}'."
                ),
            }

        # ---------- drop_tuples ----------
        if strategy == "drop_tuples":
            before_a = state.tuple_A
            before_b = state.tuple_B
            # On retombe sur reconstruction ou cas elementaire
            state.tuple_A = None
            state.tuple_B = None
            if state.position is None:
                state.position = 10
            state.intent = "reconstruction"
            return {
                "before": (before_a, before_b), "after": (None, None),
                "rationale": (
                    "Tuples vides/manquants -> sursaut vers reconstruction "
                    f"du {state.position}-eme premier (cas elementaire)."
                ),
            }

        # ---------- drop_symmetry ----------
        if strategy == "drop_symmetry":
            before = "symetrique"
            state.symmetric = False
            after = "asymetrique"
            return {
                "before": before, "after": after,
                "rationale": (
                    f"Symetrie annoncee mais |A|={len(state.tuple_A or [])} != "
                    f"|B|={len(state.tuple_B or [])} -> sursaut : reformuler en "
                    "configuration ASYMETRIQUE (rapport approche, non exact)."
                ),
            }

        # ---------- filter_to_primes ----------
        if strategy == "filter_to_primes":
            before_a = list(state.tuple_A or [])
            before_b = list(state.tuple_B or [])
            new_a = [x for x in before_a if self._is_prime(x)]
            new_b = [x for x in before_b if self._is_prime(x)]
            state.tuple_A = new_a if new_a else None
            state.tuple_B = new_b if new_b else None
            removed = (
                set(before_a) - set(new_a)
            ) | (set(before_b) - set(new_b))
            return {
                "before": (before_a, before_b), "after": (new_a, new_b),
                "rationale": (
                    f"Elements non-premiers retires : {sorted(removed)}. "
                    f"Tuples filtres -> A={new_a}, B={new_b}."
                ),
            }

        # ---------- downgrade_to_1x1 ----------
        if strategy == "downgrade_to_1x1":
            before = (state.tuple_A, state.tuple_B)
            # Garder seulement le premier element de chaque
            a = state.tuple_A or []
            b = state.tuple_B or []
            if not a or not b:
                return None
            new_a = [a[0]]
            new_b = [b[0]]
            state.tuple_A = new_a
            state.tuple_B = new_b
            state.symmetric = True
            return {
                "before": before, "after": (new_a, new_b),
                "rationale": (
                    f"Rapport 1/2 non atteignable en NxN -> sursaut vers cas "
                    f"1x1 : RsP_1x1({new_a[0]}, {new_b[0]}) qui donne EXACTEMENT 1/2."
                ),
            }

        return None

    # ------------------------------------------------------------------
    @staticmethod
    def _render_canonical(state: "_WorkingState") -> str:
        """Genere le texte humain canonique de la requete modeste."""
        if state.intent == "gap":
            return (
                "Calculer l'ecart spectral entre les deux premiers detectes "
                "(symetrique par definition)."
            )
        if state.intent == "reconstruction" and state.position is not None:
            return (
                f"Reconstruire le {state.position}-eme nombre premier en rapport "
                f"{state.ratio} (cas elementaire)."
            )
        if state.intent in ("ratio_spectral", "ratio_spectral_nxn"):
            a = state.tuple_A or []
            b = state.tuple_B or []
            sym = "symetrique" if state.symmetric else "asymetrique"
            if a and b:
                a_text = "(" + ",".join(str(x) for x in a) + ")"
                b_text = "(" + ",".join(str(x) for x in b) + ")"
                return (
                    f"Calculer le rapport spectral {state.ratio} {sym} "
                    f"{len(a)}x{len(b)} entre A={a_text} et B={b_text}."
                )
            # Fallback
            return f"Calculer un rapport spectral {state.ratio} elementaire."
        # Intent fallback
        if state.position is not None:
            return (
                f"Reconstruire le {state.position}-eme premier en rapport {state.ratio}."
            )
        return f"Calculer un rapport spectral {state.ratio} elementaire."

    # ------------------------------------------------------------------
    def _n_max(self) -> int:
        try:
            from ..spectral.prime_table import max_position
            return max_position()
        except Exception:
            return 1000

    def _is_prime(self, x: int) -> bool:
        try:
            from ..spectral.prime_table import is_known_prime
            return bool(is_known_prime(x))
        except Exception:
            pass
        try:
            import sympy
            return bool(sympy.isprime(x))
        except Exception:
            return False


# --------------------------------------------------------------------------
# Etat interne mutable de la boucle
# --------------------------------------------------------------------------
@dataclass
class _WorkingState:
    intent: str
    ratio: str
    position: Optional[int]
    tuple_A: Optional[list[int]]
    tuple_B: Optional[list[int]]
    symmetric: Optional[bool]

    @classmethod
    def from_decomposed(cls, decomposed: DecomposedRequest) -> "_WorkingState":
        # Extraire la position
        position = None
        for s in decomposed.coherent_segments + decomposed.incoherent_segments:
            if s.kind == "position" and isinstance(s.value, int):
                position = s.value
                break
        return cls(
            intent=decomposed.detected_intent or "reconstruction",
            ratio=decomposed.detected_ratio or "1/2",
            position=position,
            tuple_A=list(decomposed.tuple_A) if decomposed.tuple_A else None,
            tuple_B=list(decomposed.tuple_B) if decomposed.tuple_B else None,
            symmetric=decomposed.announced_symmetric,
        )

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
