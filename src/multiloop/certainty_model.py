"""Modele de Certitude de la Methode Spectrale Savard.

Le modele de certitude formalise les 3 QUESTIONS essentielles qu'une requete
spectrale doit satisfaire pour etre repondue avec EXACTITUDE par Gabriel,
declinees en 8 CRITERES verifiables :

  Q1 - POSITION (localisation du premier)
    C1. La position n est-elle dans la table (1 <= n <= N_max) ?
    C2. Le n-ieme premier est-il connu de spectral_core ?

  Q2 - MODELE (calibration spectrale)
    C3. Le ratio annonce est-il dans {1/2, 1/3, 1/4} ?
    C4. L'intent est-il compatible avec le ratio
        (reconstruction <-> modele exact, gap <-> indep du ratio, etc.) ?

  Q3 - CONFIGURATION (arrangement des tuples spectraux)
    C5. Si tuples annonces, au moins deux sont presents et non-vides ?
    C6. Si "symetrique NxN" annonce, |A| == |B| ?
    C7. Tous les elements des tuples sont-ils des PREMIERS connus ?
    C8. Si rapport 1/2 annonce, la taille des tuples permet un RsP proche de 1/2 ?
        (|A| == |B| et premiers distincts -> ratio exact 1/2 garanti)

Pour chaque critere viole, la `LogicalLoop` (logical_loop.py) sait
GENERIQUEMENT proposer un "sursaut" : retirer ou simplifier le segment
correspondant pour produire une REQUETE MODESTE qui satisfait tous les
criteres et donc devient repondable avec certitude.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .request_decomposer import DecomposedRequest


# --------------------------------------------------------------------------
# Questions et criteres
# --------------------------------------------------------------------------
class CertaintyQuestion(str, Enum):
    """Les 3 questions essentielles de la Methode Spectrale."""
    Q1_POSITION = "Q1_POSITION"
    Q2_MODELE = "Q2_MODELE"
    Q3_CONFIGURATION = "Q3_CONFIGURATION"


QUESTION_DESCRIPTIONS: dict[CertaintyQuestion, str] = {
    CertaintyQuestion.Q1_POSITION:
        "Localisation : quelle est la position n du premier en jeu ?",
    CertaintyQuestion.Q2_MODELE:
        "Calibration : quel modele spectral (1/2, 1/3, 1/4) appliquer ?",
    CertaintyQuestion.Q3_CONFIGURATION:
        "Arrangement : quels tuples spectraux A et B et avec quelle structure ?",
}


@dataclass(frozen=True)
class CriterionSpec:
    """Specification immuable d'un des 8 criteres."""
    code: str                              # "C1" ... "C8"
    question: CertaintyQuestion
    name: str
    description: str
    # Type de sursaut associe (sert a LogicalLoop)
    skip_strategy: str                     # "drop_position", "drop_symmetry", etc.


CRITERIA: tuple[CriterionSpec, ...] = (
    CriterionSpec(
        code="C1", question=CertaintyQuestion.Q1_POSITION,
        name="position_dans_table",
        description="La position n doit etre dans la table (1 <= n <= N_max).",
        skip_strategy="drop_position",
    ),
    CriterionSpec(
        code="C2", question=CertaintyQuestion.Q1_POSITION,
        name="premier_connu",
        description="Le n-ieme premier doit etre connu de spectral_core.",
        skip_strategy="drop_position",
    ),
    CriterionSpec(
        code="C3", question=CertaintyQuestion.Q2_MODELE,
        name="ratio_supporte",
        description="Le ratio doit etre dans {1/2, 1/3, 1/4}.",
        skip_strategy="default_to_half",
    ),
    CriterionSpec(
        code="C4", question=CertaintyQuestion.Q2_MODELE,
        name="intent_compatible_ratio",
        description="L'intent doit etre compatible avec le ratio "
                    "(reconstruction <-> modele explicite, gap indep, etc.).",
        skip_strategy="normalize_intent",
    ),
    CriterionSpec(
        code="C5", question=CertaintyQuestion.Q3_CONFIGURATION,
        name="tuples_presents",
        description="Si tuples annonces, deux tuples non-vides doivent etre fournis.",
        skip_strategy="drop_tuples",
    ),
    CriterionSpec(
        code="C6", question=CertaintyQuestion.Q3_CONFIGURATION,
        name="symetrie_respectee",
        description="Si 'symetrique NxN' annonce, |A| doit etre egal a |B|.",
        skip_strategy="drop_symmetry",
    ),
    CriterionSpec(
        code="C7", question=CertaintyQuestion.Q3_CONFIGURATION,
        name="elements_premiers",
        description="Tous les elements des tuples doivent etre des premiers connus.",
        skip_strategy="filter_to_primes",
    ),
    CriterionSpec(
        code="C8", question=CertaintyQuestion.Q3_CONFIGURATION,
        name="ratio_atteignable",
        description="Si rapport 1/2 annonce, la configuration doit permettre "
                    "RsP exactement 1/2 (|A| == |B| et premiers distincts).",
        skip_strategy="downgrade_to_1x1",
    ),
)


CRITERIA_BY_CODE: dict[str, CriterionSpec] = {c.code: c for c in CRITERIA}


# --------------------------------------------------------------------------
# Resultat d'evaluation
# --------------------------------------------------------------------------
@dataclass
class CriterionResult:
    code: str
    name: str
    question: CertaintyQuestion
    passed: bool
    detail: str
    # Donnees brutes utiles pour la LogicalLoop
    evidence: dict = field(default_factory=dict)


@dataclass
class CertaintyEvaluation:
    """Resultat complet de l'evaluation de la requete contre les 8 criteres."""
    results: list[CriterionResult] = field(default_factory=list)

    @property
    def passed_codes(self) -> list[str]:
        return [r.code for r in self.results if r.passed]

    @property
    def violated_codes(self) -> list[str]:
        return [r.code for r in self.results if not r.passed]

    @property
    def is_fully_certain(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def certainty_ratio(self) -> float:
        if not self.results:
            return 0.0
        return sum(1 for r in self.results if r.passed) / len(self.results)

    def by_question(self) -> dict[CertaintyQuestion, list[CriterionResult]]:
        out: dict[CertaintyQuestion, list[CriterionResult]] = {q: [] for q in CertaintyQuestion}
        for r in self.results:
            out[r.question].append(r)
        return out


# --------------------------------------------------------------------------
# Evaluateur
# --------------------------------------------------------------------------
class CertaintyModel:
    """Evalue une DecomposedRequest contre les 8 criteres."""

    SUPPORTED_RATIOS: frozenset[str] = frozenset({"1/2", "1/3", "1/4"})

    def __init__(self, spectral_core=None):
        self.spectral_core = spectral_core

    # ------------------------------------------------------------------
    @staticmethod
    def questions() -> dict[str, str]:
        return {q.value: QUESTION_DESCRIPTIONS[q] for q in CertaintyQuestion}

    @staticmethod
    def criteria() -> tuple[CriterionSpec, ...]:
        return CRITERIA

    # ------------------------------------------------------------------
    def evaluate(self, decomposed: DecomposedRequest) -> CertaintyEvaluation:
        """Evalue la requete decomposee contre les 8 criteres."""
        ev = CertaintyEvaluation()

        # ----- Q1: POSITION -----
        pos = self._extract_position(decomposed)
        n_max = self._n_max()

        # C1
        if pos is None:
            ev.results.append(CriterionResult(
                code="C1", name="position_dans_table",
                question=CertaintyQuestion.Q1_POSITION,
                passed=True,  # aucun n annonce -> critere non applicable, on ne penalise pas
                detail="Aucune position annoncee (critere non applicable).",
                evidence={"position": None},
            ))
        elif 1 <= pos <= n_max:
            ev.results.append(CriterionResult(
                code="C1", name="position_dans_table",
                question=CertaintyQuestion.Q1_POSITION,
                passed=True,
                detail=f"Position n={pos} dans la table (1 <= n <= {n_max}).",
                evidence={"position": pos, "n_max": n_max},
            ))
        else:
            ev.results.append(CriterionResult(
                code="C1", name="position_dans_table",
                question=CertaintyQuestion.Q1_POSITION,
                passed=False,
                detail=f"Position n={pos} HORS table (table = 1..{n_max}).",
                evidence={"position": pos, "n_max": n_max},
            ))

        # C2
        prime_known = False
        if pos is not None and 1 <= pos <= n_max:
            prime_known = (self._prime_at(pos) is not None)
        if pos is None:
            ev.results.append(CriterionResult(
                code="C2", name="premier_connu",
                question=CertaintyQuestion.Q1_POSITION, passed=True,
                detail="Aucune position annoncee (critere non applicable).",
            ))
        elif prime_known:
            ev.results.append(CriterionResult(
                code="C2", name="premier_connu",
                question=CertaintyQuestion.Q1_POSITION, passed=True,
                detail=f"Le {pos}-eme premier = {self._prime_at(pos)} (connu).",
                evidence={"position": pos, "prime": self._prime_at(pos)},
            ))
        else:
            ev.results.append(CriterionResult(
                code="C2", name="premier_connu",
                question=CertaintyQuestion.Q1_POSITION, passed=False,
                detail=f"Le {pos}-eme premier introuvable dans spectral_core.",
                evidence={"position": pos},
            ))

        # ----- Q2: MODELE -----
        ratio = decomposed.detected_ratio
        # C3
        if ratio is None:
            ev.results.append(CriterionResult(
                code="C3", name="ratio_supporte",
                question=CertaintyQuestion.Q2_MODELE, passed=True,
                detail="Aucun ratio annonce (defaut 1/2 utilise).",
                evidence={"ratio": None},
            ))
        elif ratio in self.SUPPORTED_RATIOS:
            ev.results.append(CriterionResult(
                code="C3", name="ratio_supporte",
                question=CertaintyQuestion.Q2_MODELE, passed=True,
                detail=f"Ratio {ratio} dans la liste supportee {{1/2,1/3,1/4}}.",
                evidence={"ratio": ratio},
            ))
        else:
            ev.results.append(CriterionResult(
                code="C3", name="ratio_supporte",
                question=CertaintyQuestion.Q2_MODELE, passed=False,
                detail=f"Ratio '{ratio}' non supporte (attendu : 1/2, 1/3 ou 1/4).",
                evidence={"ratio": ratio},
            ))

        # C4
        intent_ok, intent_msg = self._intent_compatible_with_ratio(decomposed)
        ev.results.append(CriterionResult(
            code="C4", name="intent_compatible_ratio",
            question=CertaintyQuestion.Q2_MODELE, passed=intent_ok,
            detail=intent_msg,
            evidence={"intent": decomposed.detected_intent, "ratio": ratio},
        ))

        # ----- Q3: CONFIGURATION -----
        a, b = decomposed.tuple_A, decomposed.tuple_B
        announces_tuples = (
            decomposed.detected_intent in ("ratio_spectral_nxn", "ratio_spectral")
            and decomposed.announced_size is not None
        )
        # C5
        if not announces_tuples and a is None and b is None:
            ev.results.append(CriterionResult(
                code="C5", name="tuples_presents",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                detail="Aucun tuple annonce (critere non applicable).",
            ))
        elif a and b and len(a) >= 1 and len(b) >= 1:
            ev.results.append(CriterionResult(
                code="C5", name="tuples_presents",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                detail=f"Tuples presents : |A|={len(a)}, |B|={len(b)}.",
                evidence={"len_A": len(a), "len_B": len(b)},
            ))
        else:
            ev.results.append(CriterionResult(
                code="C5", name="tuples_presents",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=False,
                detail="Tuples A et/ou B manquants ou vides.",
                evidence={"len_A": len(a) if a else 0, "len_B": len(b) if b else 0},
            ))

        # C6
        if decomposed.announced_symmetric is None:
            ev.results.append(CriterionResult(
                code="C6", name="symetrie_respectee",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                detail="Aucune symetrie annoncee (critere non applicable).",
            ))
        elif decomposed.announced_symmetric is False:
            ev.results.append(CriterionResult(
                code="C6", name="symetrie_respectee",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                detail="Asymetrie explicitement annoncee par l'utilisateur.",
            ))
        else:  # symmetric annonce
            if a is None or b is None:
                ev.results.append(CriterionResult(
                    code="C6", name="symetrie_respectee",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=False,
                    detail="Symetrie annoncee mais tuples introuvables.",
                ))
            elif len(a) == len(b):
                ev.results.append(CriterionResult(
                    code="C6", name="symetrie_respectee",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                    detail=f"Symetrie respectee : |A|=|B|={len(a)}.",
                    evidence={"len_A": len(a), "len_B": len(b)},
                ))
            else:
                ev.results.append(CriterionResult(
                    code="C6", name="symetrie_respectee",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=False,
                    detail=f"Annonce symetrique {decomposed.announced_size}*"
                           f"{decomposed.announced_size} mais |A|={len(a)} != |B|={len(b)}.",
                    evidence={"announced_size": decomposed.announced_size,
                              "len_A": len(a), "len_B": len(b)},
                ))

        # C7
        if a is None and b is None:
            ev.results.append(CriterionResult(
                code="C7", name="elements_premiers",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                detail="Aucun tuple annonce (critere non applicable).",
            ))
        else:
            all_elements = list(a or []) + list(b or [])
            non_primes = [x for x in all_elements if not self._is_known_prime(x)]
            if not non_primes:
                ev.results.append(CriterionResult(
                    code="C7", name="elements_premiers",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                    detail=f"Tous les {len(all_elements)} elements sont des premiers connus.",
                    evidence={"non_primes": []},
                ))
            else:
                ev.results.append(CriterionResult(
                    code="C7", name="elements_premiers",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=False,
                    detail=f"Elements non-premiers detectes : {non_primes}.",
                    evidence={"non_primes": non_primes},
                ))

        # C8
        if (decomposed.detected_ratio == "1/2" and announces_tuples
                and a is not None and b is not None):
            if len(a) == len(b) and len(set(a)) == len(a) and len(set(b)) == len(b):
                ev.results.append(CriterionResult(
                    code="C8", name="ratio_atteignable",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                    detail=f"Configuration {len(a)}*{len(b)} symetrique avec "
                           "elements distincts : RsP exactement 1/2 atteignable.",
                ))
            else:
                ev.results.append(CriterionResult(
                    code="C8", name="ratio_atteignable",
                    question=CertaintyQuestion.Q3_CONFIGURATION, passed=False,
                    detail="Configuration asymetrique ou doublons : RsP=1/2 "
                           "non garanti exactement (rapport effectif sera "
                           "asym_chaotique, proche mais != 1/2).",
                ))
        else:
            ev.results.append(CriterionResult(
                code="C8", name="ratio_atteignable",
                question=CertaintyQuestion.Q3_CONFIGURATION, passed=True,
                detail="Critere non applicable (pas de ratio 1/2 + tuples annonces).",
            ))

        return ev

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _n_max(self) -> int:
        try:
            from ..spectral.prime_table import max_position
            return max_position()
        except Exception:
            return 1000

    def _prime_at(self, n: int) -> Optional[int]:
        try:
            from ..spectral.prime_table import nth_prime
            return nth_prime(n)
        except Exception:
            return None

    def _is_known_prime(self, x: int) -> bool:
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

    @staticmethod
    def _extract_position(decomposed: DecomposedRequest) -> Optional[int]:
        for s in decomposed.coherent_segments + decomposed.incoherent_segments:
            if s.kind == "position" and isinstance(s.value, int):
                return s.value
        return None

    @staticmethod
    def _intent_compatible_with_ratio(decomposed: DecomposedRequest) -> tuple[bool, str]:
        intent = decomposed.detected_intent
        ratio = decomposed.detected_ratio
        if intent == "gap":
            return (True, "Intent 'gap' : independant du ratio (toujours coherent).")
        if intent in ("reconstruction", "ratio_spectral", "ratio_spectral_nxn"):
            if ratio in {"1/2", "1/3", "1/4"}:
                return (True, f"Intent '{intent}' compatible avec ratio {ratio}.")
            if ratio is None:
                return (True, f"Intent '{intent}' : ratio par defaut 1/2 utilise.")
            return (False, f"Intent '{intent}' incompatible avec ratio '{ratio}'.")
        return (True, f"Intent '{intent}' : compatibilite ratio non verifiable.")

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
