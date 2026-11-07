"""
llm_reformulator.py - Reformulateur LLM contextuel pour le Slow-Motion Debugger.

CONTEXTE (Philippe 2026-02) :
Le slow-motion debugger actuel propose TOUJOURS la meme reformulation
("reconstruction de nombres premiers") pour n'importe quelle requete
declenchant une incoherence multiloop. Cette rigidite vient de la logique
purement heuristique dans `SlowMotionDebugger._build_reformulations` qui
depend uniquement de `dec.detected_intent`.

OBJECTIF :
Utiliser un LLM (Claude / OpenAI via LLMManager) pour :
  1. Analyser la question ORIGINALE dans son contexte semantique.
  2. Segmenter la requete en unites logiques (intention + parametres).
  3. Proposer N reformulations concretes, VARIEES, qui :
     - Preservent la semantique de la requete originale
     - Couvrent des angles mathematiques distincts (reconstruction, ratio,
       gap, digamma, invariant, RsP asymetrique, etc.)
     - Sont MODESTES en portee (evitent l'overreach)
     - Font reference a des elements concrets (positions, primes, ratios)

STRATEGIE :
- Prompt system explicite avec exemples few-shot.
- Temperature basse (0.3) pour rester factuel.
- Timeout court (5s par defaut) pour ne pas bloquer le pipeline.
- Fallback silencieux vers liste vide si LLM indisponible / timeout / erreur.
- Deduplication et nettoyage des reponses.
"""
from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from ..core.llm_manager import LLMManager
from .request_decomposer import DecomposedRequest

logger = logging.getLogger(__name__)


# =====================================================================
# PROMPT TEMPLATES
# =====================================================================


_SYSTEM_PROMPT = """Tu es un assistant mathematique specialise dans la Methode Spectrale de Philippe Thomas Savard (reconstruction des nombres premiers).

Ton unique role dans cette session : reformuler la requete d'un utilisateur en plusieurs variantes PLUS MODESTES et CONCRETES, en preservant strictement le sens original.

REGLES STRICTES :
1. Chaque reformulation doit rester COHERENTE avec l'intention originale.
2. Propose des angles DIFFERENTS : reconstruction, rapport spectral, ecart, digamma, invariant, cas elementaire.
3. Chaque reformulation doit etre CONCRETE (mentionner un ratio, une position, ou des primes precis).
4. Reste MODESTE : evite les generalisations, prefere le cas particulier verifiable.
5. Format : liste numerotee de 3 a 5 reformulations, une par ligne, sans commentaire.

NE JAMAIS :
- Inventer de nouveaux concepts absents de la requete.
- Utiliser un vocabulaire dismissif (faux, absurde, incoherent, sans sens, etc.).
- Repondre a la question ; tu ne fais que reformuler.
- Depasser 200 caracteres par reformulation.

EXEMPLES :

Requete : "Explique-moi la methode spectrale"
Reponse :
1. Quelle est la formule generale de la Methode Spectrale 1/2 pour reconstruire le n-ieme premier ?
2. Comment SA(n) et SB(n) permettent-elles la reconstruction ? Exemple sur n=10.
3. Quel est le rapport spectral 1/2 entre A=(2,3) et B=(5,7) ?
4. Verifier RsP_1x1(2, 3) = 1/2 comme cas elementaire.

Requete : "Rapport spectral entre A=(7,3) et B=(11,23,13)"
Reponse :
1. Calculer le rapport spectral asymetrique CHAOTIQUE entre A=(7,3) (2 elts) et B=(11,23,13) (3 elts).
2. Cas elementaire : verifier RsP_1x1(7, 11) en rapport 1/2 (doit donner EXACTEMENT 1/2).
3. Reformuler en symetrique 3x3 en completant A avec un premier supplementaire.
4. Quelle est la difference numerique |RsP(A,B) - 1/2| pour cette configuration ?
"""


_USER_PROMPT_TEMPLATE = """QUESTION ORIGINALE :
"{question}"

ANALYSE PREALABLE DE L'AGENT :
- Intent detecte : {intent}
- Ratio detecte  : {ratio}
- Tuple A        : {tuple_a}
- Tuple B        : {tuple_b}
- Segments coherents : {n_coherent}
- Segments incoherents : {n_incoherent}

Genere entre 3 et 5 reformulations MODESTES et CONCRETES qui preservent le sens original.
Format : liste numerotee, une reformulation par ligne, pas de commentaire."""


# =====================================================================
# STRUCTURES
# =====================================================================


@dataclass
class ReformulationResult:
    """Resultat de l'appel au reformulateur LLM."""
    reformulations: list[str] = field(default_factory=list)
    used_llm: bool = False
    latency_ms: int = 0
    error: Optional[str] = None
    fallback_reason: Optional[str] = None

    def is_useful(self) -> bool:
        return len(self.reformulations) > 0


# =====================================================================
# REFORMULATEUR PRINCIPAL
# =====================================================================


class LLMReformulator:
    """Genere des reformulations contextuelles via LLM (Claude/OpenAI/Ollama).

    Utilise par le SlowMotionDebugger quand une incoherence multiloop est
    detectee. Fournit des variantes semanticalement proches de la requete
    originale, contrairement aux reformulations heuristiques rigides
    proposees par _build_reformulations.
    """

    DEFAULT_TIMEOUT_S: float = 5.0
    DEFAULT_NUM_VARIANTS: int = 4
    DEFAULT_TEMPERATURE: float = 0.3
    MAX_REFORMULATION_LEN: int = 220  # marge sur les 200 chars du prompt

    def __init__(
        self,
        llm_manager: Optional[LLMManager] = None,
        timeout_s: float = DEFAULT_TIMEOUT_S,
        num_variants: int = DEFAULT_NUM_VARIANTS,
        temperature: float = DEFAULT_TEMPERATURE,
    ):
        self.llm = llm_manager
        self.timeout_s = timeout_s
        self.num_variants = num_variants
        self.temperature = temperature
        logger.info(
            "LLMReformulator initialise (timeout=%.1fs, n_variants=%d, temp=%.2f, llm=%s)",
            timeout_s, num_variants, temperature,
            "ON" if llm_manager else "OFF (mode heuristique seul)"
        )

    # ------------------------------------------------------------------
    async def reformulate(
        self,
        question: str,
        decomposed: DecomposedRequest,
    ) -> ReformulationResult:
        """
        Genere des reformulations modestes de `question` via LLM.

        Args:
            question: La requete originale de l'utilisateur.
            decomposed: L'analyse deja produite par RequestDecomposer.

        Returns:
            ReformulationResult avec :
            - reformulations: liste (peut etre vide en cas de fallback)
            - used_llm: True si le LLM a repondu
            - latency_ms: temps d'execution
            - error / fallback_reason: si non vide, indique une degradation.
        """
        import time
        start = time.perf_counter()

        if self.llm is None:
            return ReformulationResult(
                fallback_reason="Aucun LLMManager fourni, mode heuristique seul."
            )
        if not question or not question.strip():
            return ReformulationResult(
                fallback_reason="Question vide, rien a reformuler."
            )

        user_prompt = self._build_user_prompt(question, decomposed)
        try:
            raw = await asyncio.wait_for(
                self.llm.generate(
                    prompt=user_prompt,
                    system=_SYSTEM_PROMPT,
                    temperature=self.temperature,
                    domaine="reformulation_spectrale",
                ),
                timeout=self.timeout_s,
            )
        except asyncio.TimeoutError:
            latency_ms = int((time.perf_counter() - start) * 1000)
            logger.warning(
                "LLMReformulator : timeout LLM apres %.1fs. Fallback heuristique.",
                self.timeout_s,
            )
            return ReformulationResult(
                latency_ms=latency_ms,
                error=f"timeout ({self.timeout_s}s)",
                fallback_reason="Timeout LLM depasse.",
            )
        except Exception as exc:
            latency_ms = int((time.perf_counter() - start) * 1000)
            logger.warning("LLMReformulator : erreur LLM (%s). Fallback.", exc)
            return ReformulationResult(
                latency_ms=latency_ms,
                error=str(exc),
                fallback_reason=f"Erreur LLM : {type(exc).__name__}",
            )

        latency_ms = int((time.perf_counter() - start) * 1000)
        reformulations = self._parse_response(raw)
        # Filtrage : rejette vocabulaire dismissif eventuellement genere
        reformulations = self._filter_forbidden_vocab(reformulations)
        # Limite au nombre demande
        reformulations = reformulations[: self.num_variants]

        logger.info(
            "LLMReformulator : %d reformulations extraites en %d ms (LLM=%s)",
            len(reformulations), latency_ms,
            "succes" if reformulations else "vide-parse",
        )
        return ReformulationResult(
            reformulations=reformulations,
            used_llm=True,
            latency_ms=latency_ms,
        )

    # ------------------------------------------------------------------
    def _build_user_prompt(
        self,
        question: str,
        decomposed: DecomposedRequest,
    ) -> str:
        """Formate le prompt utilisateur avec les segments deja decomposes."""
        return _USER_PROMPT_TEMPLATE.format(
            question=question.strip()[:500],  # tronquage defensif
            intent=decomposed.detected_intent or "inconnu",
            ratio=decomposed.detected_ratio or "non-detecte",
            tuple_a=decomposed.tuple_A or "non-fourni",
            tuple_b=decomposed.tuple_B or "non-fourni",
            n_coherent=len(decomposed.coherent_segments),
            n_incoherent=len(decomposed.incoherent_segments),
        )

    # ------------------------------------------------------------------
    def _parse_response(self, raw: str) -> list[str]:
        """
        Extrait les reformulations de la reponse LLM.

        Accepte les formats :
          "1. Xxxx", "1) Xxxx", "- Xxxx", "* Xxxx"
        Filtre les lignes vides, les commentaires, et les trop longues.
        """
        if not raw:
            return []

        candidates: list[str] = []
        for raw_line in raw.strip().splitlines():
            line = raw_line.strip()
            if not line:
                continue
            # Enleve les marqueurs "1.", "1)", "-", "*" en debut de ligne
            m = re.match(r"^(?:\d+[\.\)]\s*|[-*]\s+|\u2022\s*)(.*)$", line)
            if m:
                content = m.group(1).strip()
            else:
                # Ligne sans marqueur : accepter si elle ressemble a une phrase
                if line.endswith("?") or line.endswith(".") or len(line) > 30:
                    content = line
                else:
                    continue
            if not content:
                continue
            if len(content) > self.MAX_REFORMULATION_LEN:
                content = content[: self.MAX_REFORMULATION_LEN - 3] + "..."
            candidates.append(content)

        # Deduplication naive (case-insensitive)
        seen: set[str] = set()
        unique: list[str] = []
        for c in candidates:
            key = c.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(c)
        return unique

    # ------------------------------------------------------------------
    def _filter_forbidden_vocab(self, reformulations: list[str]) -> list[str]:
        """Retire les reformulations contenant un vocabulaire dismissif.

        Reutilise le detecteur centralise `forbidden_vocab` pour eviter que
        le LLM ne generalise via des tournures rejetees ("methode absurde",
        "theorie fausse", etc.).
        """
        try:
            from .forbidden_vocab import detect_forbidden
        except ImportError:
            return reformulations
        clean: list[str] = []
        for r in reformulations:
            found, _ = detect_forbidden(r)
            if not found:
                clean.append(r)
            else:
                logger.debug("Reformulation rejetee (vocab dismissif): %r", r[:80])
        return clean


# =====================================================================
# FONCTION SYNC DE COMMODITE (pour appel depuis contexte sync)
# =====================================================================


def merge_reformulations(
    llm_reformulations: list[str],
    heuristic_reformulations: list[str],
    max_total: int = 6,
) -> list[str]:
    """
    Fusionne les reformulations LLM et heuristiques en preservant :
      - Priorite LLM en tete (car contextuelles a la requete precise)
      - Heuristiques en repli (garantissent au moins une suggestion)
      - Deduplication insensible a la casse
      - Cap sur `max_total` pour eviter la surcharge de l'utilisateur
    """
    seen: set[str] = set()
    merged: list[str] = []
    for source in (llm_reformulations, heuristic_reformulations):
        for r in source:
            r_stripped = r.strip()
            if not r_stripped:
                continue
            key = r_stripped.lower()
            if key not in seen:
                seen.add(key)
                merged.append(r_stripped)
            if len(merged) >= max_total:
                return merged
    return merged
