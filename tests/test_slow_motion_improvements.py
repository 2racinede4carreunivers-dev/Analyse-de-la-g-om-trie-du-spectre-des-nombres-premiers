"""Tests pour les ameliorations Slow-Motion + Decomposer (Philippe feedback).

Couvre :
  - Decomposer detecte le mismatch 'symetrique NxN' annonce vs tuples reels
  - _build_reformulations propose des reformulations pour ratio_spectral_nxn
  - Timeline T4/T7 explique son raisonnement (n'est plus vide)
  - structured_data efface les champs obsoletes (ratio_float, etc.)
"""
from __future__ import annotations

from src.multiloop.request_decomposer import RequestDecomposer
from src.multiloop.slow_motion_debugger import SlowMotionDebugger
from src.multiloop.coherence_detector import CoherenceReport
from src.core.types import FinalAnswer


# ==========================================================================
# Decomposer : mismatch annonce vs reel
# ==========================================================================
class TestDecomposerMismatch:
    def setup_method(self):
        self.dec = RequestDecomposer()

    def test_symetrique_4x4_avec_tuples_4_et_3_flags_incoherent(self):
        """Cas Philippe : annonce 'symetrique 4*4' mais tuples (4 elem, 3 elem)."""
        q = ("Peux-tu determiner le rapport spectral symetrique 4*4 entre "
             "(7, 23, 79, 31) et (17, 11, 3) ?")
        res = self.dec.decompose(q)
        assert res.announced_size == 4
        assert res.announced_symmetric is True
        assert res.tuple_A == [7, 23, 79, 31]
        assert res.tuple_B == [17, 11, 3]
        # Les segments tuple_A et tuple_B doivent etre marques INCOHERENTS
        incoherent_kinds = {s.kind for s in res.incoherent_segments}
        assert "tuple_A" in incoherent_kinds
        assert "tuple_B" in incoherent_kinds
        # Le motif doit mentionner le mismatch
        for s in res.incoherent_segments:
            assert "mismatch" in s.reason.lower() or "asymetrique" in s.reason.lower()

    def test_symetrique_3x3_avec_tuples_equilibres_coherent(self):
        q = "rapport spectral symetrique 3*3 entre (3, 5, 11) et (2, 7, 13)"
        res = self.dec.decompose(q)
        assert res.announced_size == 3
        assert res.announced_symmetric is True
        # Pas d'incoherence sur les tuples
        for s in res.segments:
            if s.kind in ("tuple_A", "tuple_B"):
                assert s.coherent is True, f"tuple {s.kind} doit etre coherent"

    def test_asymetrique_explicite_pas_de_flag(self):
        q = "rapport spectral asymetrique 4*3 entre (7, 23, 79, 31) et (17, 11, 3)"
        res = self.dec.decompose(q)
        assert res.announced_symmetric is False
        # Pas de mismatch puisque l'utilisateur a annonce asymetrique
        for s in res.segments:
            if s.kind in ("tuple_A", "tuple_B"):
                assert s.coherent is True

    def test_pas_d_annonce_pas_de_flag(self):
        """Sans annonce explicite, pas de mismatch a flaguer."""
        q = "calcule RsP entre (7, 23) et (17, 11)"
        res = self.dec.decompose(q)
        assert res.announced_size is None
        for s in res.segments:
            if s.kind in ("tuple_A", "tuple_B"):
                assert s.coherent is True


# ==========================================================================
# Slow-Motion : reformulations pour ratio_spectral_nxn
# ==========================================================================
class TestReformulationsNxN:
    def setup_method(self):
        self.dec = RequestDecomposer()

    def test_reformulations_nxn_mismatch_propose_canonical(self):
        q = ("rapport spectral symetrique 4*4 entre (7, 23, 79, 31) "
             "et (17, 11, 3)")
        decomposed = self.dec.decompose(q)
        bypassed = decomposed.incoherent_segments
        suggestions = SlowMotionDebugger._build_reformulations(decomposed, bypassed)
        # Au moins 2 suggestions doivent etre produites
        assert len(suggestions) >= 2
        # Une suggestion doit proposer "asymetrique" (verite mathematique)
        assert any("asymetrique" in s.lower() for s in suggestions)
        # Une suggestion doit proposer de COMPLETER B pour rester symetrique
        assert any("completer" in s.lower() or "symetrique" in s.lower()
                   for s in suggestions)

    def test_reformulations_nxn_equilibre_propose_quand_meme(self):
        """Meme sans bypass, on doit avoir au moins 1 suggestion canonique."""
        q = "rapport spectral 3*3 entre (3, 5, 11) et (2, 7, 13)"
        decomposed = self.dec.decompose(q)
        bypassed = decomposed.incoherent_segments
        suggestions = SlowMotionDebugger._build_reformulations(decomposed, bypassed)
        assert len(suggestions) >= 1

    def test_reformulations_reconstruction_inchange(self):
        """Regression : la branche reconstruction continue de fonctionner."""
        q = "reconstruire le 10eme nombre premier en rapport 1/2"
        decomposed = self.dec.decompose(q)
        suggestions = SlowMotionDebugger._build_reformulations(
            decomposed, decomposed.incoherent_segments,
        )
        assert len(suggestions) >= 1


# ==========================================================================
# Timeline T4/T7 : ne sont plus vides
# ==========================================================================
class TestTimelineExplains:
    def test_t4_no_bypass_explique(self):
        """Sans bypass, T4 doit expliquer (pas juste 'aucun segment')."""
        from src.multiloop.slow_motion_debugger import SlowMotionDebugger
        from src.adapters.corpus.certainty_kernel import CertaintyKernel
        from src.core.spectral_core import SpectralMethodCore

        dbg = SlowMotionDebugger(
            certainty_kernel=CertaintyKernel(),
            spectral_core=SpectralMethodCore(),
        )
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        report = CoherenceReport(
            score=0.5, incoherent=True, signals=["test"],
            best_candidate_score=5.0,
        )
        res = dbg.debug(
            question="reconstruire le 10eme premier en rapport 1/2",
            final=final, coherence_report=report, skip_auto_audit=True,
        )
        timeline = res.structured_data["debug_timeline"]
        t4 = next(ev for ev in timeline if ev["step"] == 4)
        # Ne contient plus simplement "aucun segment a ignorer"
        assert "aucun segment incoherent" in t4["detail"].lower() \
               or "syntaxiquement valide" in t4["detail"].lower() \
               or "preserver" in t4["detail"].lower() \
               or "quarantaine" in t4["detail"].lower()

    def test_t7_no_bypass_explique(self):
        from src.multiloop.slow_motion_debugger import SlowMotionDebugger
        from src.adapters.corpus.certainty_kernel import CertaintyKernel
        from src.core.spectral_core import SpectralMethodCore

        dbg = SlowMotionDebugger(
            certainty_kernel=CertaintyKernel(),
            spectral_core=SpectralMethodCore(),
        )
        final = FinalAnswer(question_id="q1", answer_text="x", best_score=5.0)
        report = CoherenceReport(
            score=0.5, incoherent=True, signals=["test"],
            best_candidate_score=5.0,
        )
        # Cas reconstruction -> _build_reformulations va proposer 2 suggestions
        res = dbg.debug(
            question="reconstruire le 10eme premier en rapport 1/2",
            final=final, coherence_report=report, skip_auto_audit=True,
        )
        timeline = res.structured_data["debug_timeline"]
        # REFORMULATIONS est maintenant a T10 (apres l'insertion du modele de
        # certitude T7 + boucle logique T8 + reponse modeste T9).
        t_reformulations = next(
            ev for ev in timeline if ev["label"] == "REFORMULATIONS"
        )
        assert "suggestion" in t_reformulations["detail"].lower()


# ==========================================================================
# structured_data : champs obsoletes effaces
# ==========================================================================
class TestStaleDataCleaned:
    def test_ratio_float_efface_apres_slow_motion(self):
        from src.multiloop.slow_motion_debugger import SlowMotionDebugger
        from src.adapters.corpus.certainty_kernel import CertaintyKernel
        from src.core.spectral_core import SpectralMethodCore

        dbg = SlowMotionDebugger(
            certainty_kernel=CertaintyKernel(),
            spectral_core=SpectralMethodCore(),
        )
        final = FinalAnswer(
            question_id="q1", answer_text="x", best_score=5.0,
            structured_data={
                "ratio_float": 2047.999,        # OBSOLETE
                "expected_float": 0.5,          # OBSOLETE
                "matches_expected": False,      # OBSOLETE
                "other_field": "preserve_me",   # doit etre garde
            },
        )
        report = CoherenceReport(
            score=0.5, incoherent=True, signals=["test"],
            best_candidate_score=5.0,
        )
        res = dbg.debug(
            question="rapport spectral 3*3 (3,5,11) et (2,7,13)",
            final=final, coherence_report=report, skip_auto_audit=True,
        )
        assert "ratio_float" not in res.structured_data
        assert "expected_float" not in res.structured_data
        assert "matches_expected" not in res.structured_data
        assert res.structured_data.get("other_field") == "preserve_me"
        # Et le slow_motion_triggered est present
        assert res.structured_data["slow_motion_triggered"] is True

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
