"""
Mémoire conversationnelle courte : ring-buffer des N derniers échanges Q&A.

Ce module fournit un « souvenir immédiat » injecté dans le prompt LLM pour
que Gabriel garde le fil de la conversation entre deux tours consécutifs
(ex. l'utilisateur dit « Le plan trifocal » après avoir posé une question
sur les régimes, et Gabriel comprend qu'il s'agit du même sujet).

Le buffer est volontairement LIMITÉ (défaut 3 tours) pour :
- ne pas exploser le contexte du LLM,
- garder la latence basse,
- éviter que d'anciens échanges polluent les nouvelles questions.

La mémoire N'EST PAS persistée entre exécutions : c'est un contexte
strictement de session (in-memory). Pour la mémoire longue durée, se
référer au RAG sémantique via IntegrateurMemoireGabriel.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ConversationTurn:
    """Un tour complet (question utilisateur + réponse assistant)."""

    question: str
    answer: str


class ConversationalMemory:
    """Ring-buffer des N derniers tours Q&A pour injection dans le prompt LLM.

    Attributes:
        max_turns: Nombre maximum de tours conservés (>= 1).
        max_chars_per_field: Troncature défensive de chaque question/réponse
            pour éviter d'exploser le prompt en cas de réponse LLM verbeuse.
    """

    def __init__(self, max_turns: int = 3, max_chars_per_field: int = 1500):
        if max_turns < 1:
            raise ValueError(
                f"max_turns doit être >= 1, obtenu {max_turns}"
            )
        if max_chars_per_field < 100:
            raise ValueError(
                f"max_chars_per_field doit être >= 100, obtenu "
                f"{max_chars_per_field}"
            )
        self.max_turns = max_turns
        self.max_chars_per_field = max_chars_per_field
        self._turns: deque[ConversationTurn] = deque(maxlen=max_turns)

    # ------------------------------------------------------------------
    # Écriture
    # ------------------------------------------------------------------
    def add(self, question: str, answer: str) -> None:
        """Ajoute un tour au buffer (le plus ancien est évincé si plein)."""
        if not isinstance(question, str) or not isinstance(answer, str):
            raise TypeError(
                "question et answer doivent être des chaînes de caractères"
            )
        q = self._truncate(question.strip())
        a = self._truncate(answer.strip())
        if not q and not a:
            # Rien à mémoriser : on ignore silencieusement
            return
        self._turns.append(ConversationTurn(question=q, answer=a))

    def clear(self) -> None:
        """Réinitialise complètement la mémoire (utilisé par la commande CLI
        `reset` ou en début de session)."""
        self._turns.clear()

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self._turns)

    def is_empty(self) -> bool:
        return len(self._turns) == 0

    def turns(self) -> list[ConversationTurn]:
        """Retourne une copie ordonnée du plus ancien au plus récent."""
        return list(self._turns)

    def last(self) -> ConversationTurn | None:
        """Retourne le tour le plus récent, ou None si mémoire vide."""
        return self._turns[-1] if self._turns else None

    # ------------------------------------------------------------------
    # Injection prompt LLM
    # ------------------------------------------------------------------
    def build_context_block(self, header: str | None = None) -> str:
        """Construit le bloc texte à injecter dans le prompt LLM.

        Retourne "" (chaîne vide) si la mémoire est vide, pour que
        l'appelant puisse concatener sans se soucier du cas dégénéré.

        Exemple de sortie::

            [CONTEXTE CONVERSATIONNEL RÉCENT — 2 tours précédents]
            (du plus ancien au plus récent)

            [Tour -2]
            Utilisateur : Quels sont les 3 régimes RsP ?
            Gabriel    : Il y a le régime symétrique, chaotique et...

            [Tour -1]
            Utilisateur : Le plan trifocal, c'est bien ça ?
            Gabriel    : Oui, le plan trifocal correspond au régime...

            [Fin du contexte — répondre à la NOUVELLE question ci-dessous]
        """
        if self.is_empty():
            return ""

        default_header = (
            f"[CONTEXTE CONVERSATIONNEL RÉCENT — {len(self._turns)} tour"
            f"{'s' if len(self._turns) > 1 else ''} précédent"
            f"{'s' if len(self._turns) > 1 else ''}]\n"
            "(du plus ancien au plus récent)"
        )
        lines: list[str] = [header or default_header, ""]

        total = len(self._turns)
        for offset, turn in enumerate(self._turns):
            # Marqueur relatif : le plus ancien est -N, le plus récent est -1
            rel = -(total - offset)
            lines.append(f"[Tour {rel}]")
            lines.append(f"Utilisateur : {turn.question}")
            lines.append(f"Gabriel    : {turn.answer}")
            lines.append("")  # ligne vide entre tours

        lines.append(
            "[Fin du contexte — répondre à la NOUVELLE question ci-dessous]"
        )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Interne
    # ------------------------------------------------------------------
    def _truncate(self, s: str) -> str:
        if len(s) <= self.max_chars_per_field:
            return s
        return s[: self.max_chars_per_field - 3].rstrip() + "..."

    # ------------------------------------------------------------------
    # Debug / introspection
    # ------------------------------------------------------------------
    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"ConversationalMemory(turns={len(self._turns)}/"
            f"{self.max_turns}, chars_cap={self.max_chars_per_field})"
        )

    def snapshot(self) -> list[dict[str, str]]:
        """Représentation sérialisable (pour audit/logs)."""
        return [
            {"question": t.question, "answer": t.answer}
            for t in self._turns
        ]


def merge_context_into_prompt(
    prompt: str,
    context_block: str,
) -> str:
    """Helper : préfixe le prompt avec le bloc de contexte conversationnel.

    Si `context_block` est vide, retourne `prompt` inchangé.
    Sinon insère le bloc AVANT le prompt, séparé par une ligne vide.
    """
    if not context_block:
        return prompt
    return f"{context_block}\n\n{prompt}"


__all__ = [
    "ConversationTurn",
    "ConversationalMemory",
    "merge_context_into_prompt",
]
