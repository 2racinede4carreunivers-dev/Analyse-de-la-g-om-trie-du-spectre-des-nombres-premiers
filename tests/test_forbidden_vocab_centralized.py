"""
Tests de non-regression pour le detecteur centralise de vocabulaire dismissif.

Historique :
- v3.19 (2026-07-03) : fix initial dans src/multiloop/critic.py (regex contextualisees).
- v3.24 (2026-02) : REGRESSION detectee — coherence_detector.py et spectral_core.py
  utilisaient toujours des listes litterales et penalisaient "faux" isole
  (rapporte par Philippe : question sur RsP chaotique (7,3)/(11,23,13) declenchait
  le Slow-Motion Debugger a tort avec signal `vocabulaire_interdit:faux`).

Ces tests garantissent que :
1. Le detecteur centralise NE MATCHE PAS les usages neutres/legitimes.
2. Le detecteur MATCHE les condamnations directes de la methode.
3. Les 3 callsites (critic, coherence_detector, spectral_core) utilisent
   bien l'utilitaire centralise.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from src.multiloop.forbidden_vocab import detect_forbidden, detect_forbidden_word


class TestForbiddenVocabTolerance:
    """Le detecteur DOIT tolerer les usages neutres / techniques du mot 'faux'."""

    @pytest.mark.parametrize("text", [
        # Usage technique
        "Ce serait un faux positif dans notre detection.",
        "On veut eviter les faux negatifs.",
        # Usage negatif (defend la methode)
        "Le rapport n'est pas faux, il est proche de 1/2.",
        "Il n'y a rien de faux dans cette approche.",
        "Ce raisonnement n'est ni faux ni absurde.",
        # Hypothese conditionnelle
        "Il serait faux de conclure que la methode echoue.",
        "Si on considerait ce point comme faux, on manquerait la vraie interpretation.",
        # Contexte pedagogique
        "Un raisonnement faux typique consisterait a...",
        "Distinguons le vrai du faux dans cette formule.",
        # Legitime dans le corpus Savard (v3.19)
        "Le rapport 1/6 est algebriquement incoherent mais numeriquement valide.",
        "L'asymetrie ordonnee est algebriquement incoherente selon l'axiome de Savard.",
    ])
    def test_tolerates_neutral_usage(self, text: str) -> None:
        found, span = detect_forbidden(text)
        assert not found, (
            f"Faux positif : texte legitime rejete a tort.\n"
            f"  Texte: {text!r}\n"
            f"  Fragment matche: {span!r}"
        )

    def test_the_exact_scenario_from_philippe_bug_report(self) -> None:
        """
        Reproduit le contexte exact du bug rapporte par Philippe (2026-02) :
        le LLM produit une phrase legitime mais le detecteur naif matche 'faux' isole.
        """
        # Exemples plausibles de sortie LLM qui declenchaient a tort le bug
        llm_outputs = [
            "Le rapport 106/205 est proche de 1/2 mais pas exact. Ce n'est pas faux "
            "pour autant, l'ecart residuel est en cours d'investigation theorique.",
            "La methode spectrale reste valide. Un faux debat serait de rejeter "
            "l'approche pour un ecart residuel structurel.",
            "Notez que ce n'est pas faux d'obtenir 0.517 au lieu de 0.5 exact "
            "dans une configuration chaotique.",
        ]
        for text in llm_outputs:
            found, span = detect_forbidden(text)
            assert not found, (
                f"REGRESSION du bug Philippe : phrase legitime rejetee.\n"
                f"  Texte: {text!r}\n"
                f"  Fragment matche: {span!r}"
            )


class TestForbiddenVocabDetection:
    """Le detecteur DOIT matcher les condamnations directes de la methode."""

    @pytest.mark.parametrize("text", [
        # Condamnations methode
        "La methode spectrale est fausse.",
        "Cette methode est incoherente.",
        "La methode de Savard semble absurde.",
        "La methode est sans fondement.",
        # Condamnations theorie
        "La theorie de Savard est fausse.",
        "Cette theorie est incoherente.",
        # Fausse methode
        "Il s'agit d'une fausse methode.",
        "C'est une fausse theorie.",
        # Rapport spectral condamne
        "Le rapport spectral est absurde.",
        "Le rapport spectral est invalide.",
        # Postulat/axiome
        "Le postulat de Savard est absurde.",
        "L'axiome est incoherent.",
        # Philippe personnellement
        "Philippe Savard se trompe.",
        "Philippe a tort sur ce point.",
    ])
    def test_detects_direct_condemnation(self, text: str) -> None:
        found, span = detect_forbidden(text)
        assert found, (
            f"Faux negatif : condamnation directe NON detectee.\n"
            f"  Texte: {text!r}"
        )
        assert len(span) > 0


class TestBackwardCompatibility:
    """detect_forbidden_word doit retourner un mot cle exploitable pour les logs."""

    def test_returns_keyword_when_matched(self) -> None:
        found, word = detect_forbidden_word("La methode spectrale est fausse.")
        assert found is True
        assert word in ("fausse", "faux")

    def test_returns_empty_when_not_matched(self) -> None:
        found, word = detect_forbidden_word("Un faux positif dans notre systeme.")
        assert found is False
        assert word == ""


class TestCallsitesUseCentralizedUtility:
    """Verifie que les 3 callsites importent bien l'utilitaire centralise."""

    ROOT = Path(__file__).resolve().parent.parent

    def test_critic_uses_forbidden_vocab(self) -> None:
        content = (self.ROOT / "src/multiloop/critic.py").read_text(encoding="utf-8")
        assert "from .forbidden_vocab import detect_forbidden" in content, (
            "critic.py doit importer detect_forbidden depuis forbidden_vocab"
        )
        # Ne doit plus contenir la liste litterale
        assert "forbidden_patterns = [" not in content, (
            "critic.py ne doit plus contenir de liste locale forbidden_patterns"
        )

    def test_coherence_detector_uses_forbidden_vocab(self) -> None:
        content = (self.ROOT / "src/multiloop/coherence_detector.py").read_text(
            encoding="utf-8"
        )
        assert "from .forbidden_vocab import detect_forbidden_word" in content
        # La liste FORBIDDEN_WORDS ne doit plus exister
        assert "FORBIDDEN_WORDS = [" not in content, (
            "coherence_detector.py ne doit plus contenir de liste FORBIDDEN_WORDS"
        )

    def test_spectral_core_uses_forbidden_vocab(self) -> None:
        content = (self.ROOT / "src/core/spectral_core.py").read_text(encoding="utf-8")
        assert "from ..multiloop.forbidden_vocab import detect_forbidden" in content
        # La liste litterale ne doit plus exister
        assert 'forbidden = ["incoherent"' not in content, (
            "spectral_core.py ne doit plus contenir de liste litterale forbidden"
        )


class TestNoInfinisTheoreticalClaim:
    """
    Philippe (2026-02) : les references a l'ordinal / cardinal des infinis
    ont ete retirees du code, car des developpements recents suggerent
    que cette interpretation pourrait ne pas etre tout a fait exacte.
    Gabriel ne doit PAS AFFIRMER ces theories dans ses reponses.
    """

    ROOT = Path(__file__).resolve().parent.parent

    def test_certainty_kernel_does_not_affirm_infinis_theory(self) -> None:
        """Les certitudes du kernel ne doivent plus AFFIRMER la theorie des infinis."""
        content = (self.ROOT / "src/adapters/corpus/certainty_kernel.py").read_text(
            encoding="utf-8"
        )
        # Ces formulations d'affirmation doivent avoir disparu
        forbidden_claims = [
            "attribue a l'ordinal des infinis",
            "attribue au CARDINAL DES INFINIS",
            "numeriquement valide mais algebriquement incoherent",
        ]
        for claim in forbidden_claims:
            assert claim not in content, (
                f"certainty_kernel.py ne doit plus AFFIRMER la theorie des infinis. "
                f"Trouve : {claim!r}"
            )

    def test_slow_motion_summary_has_no_infinis_note(self) -> None:
        """Le CADRAN 6 (reponse modeste) ne doit plus injecter de note theorique infinis."""
        content = (self.ROOT / "src/multiloop/slow_motion_debugger.py").read_text(
            encoding="utf-8"
        )
        assert "CARDINAL DES INFINIS" not in content
        assert "ORDINAL DES INFINIS" not in content
        assert "infini_note" not in content

    def test_spectral_core_citations_neutral(self) -> None:
        """Les citations du cas chaotique ne doivent pas mentionner cardinal des infinis."""
        content = (self.ROOT / "src/core/spectral_core.py").read_text(encoding="utf-8")
        idx = content.find('elif config == "asym_chaotique"')
        assert idx > 0
        block = content[idx:idx + 800]
        assert "CARDINAL DES INFINIS" not in block
        assert "cardinal des infinis" not in block

    def test_spectral_knowledge_no_ordinal_interpretation(self) -> None:
        """spectral_knowledge.py ne doit plus AFFIRMER l'interpretation ordinal des infinis."""
        content = (self.ROOT / "src/spectral/spectral_knowledge.py").read_text(
            encoding="utf-8"
        )
        assert "l'ordinal des infinis" not in content
        assert "omega+1 != 1+omega" not in content
