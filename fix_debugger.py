#!/usr/bin/env python3
# Fix debugger - annuler completement et definitivement

import os

os.chdir(r"C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\src\core")

with open('pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Bloc a remplacer
old_block = '''            if coherence.incoherent and not conversational_bypass:
                logger.warning("Q[%s] INCOHERENCE => Slow-Motion Debugger active", qid)
                # v3.27 : Reformulations LLM contextuelles calculees en amont
                # (pipeline async) pour eviter la rigidite du fallback heuristique
                # qui proposait toujours "reconstruction de nombres premiers".
                llm_reformulations = await self._compute_llm_reformulations(
                    question, decomposition, qid,
                )
                final = self.slow_motion.debug(
                    question=question,
                    final=final,
                    coherence_report=coherence,
                    precomputed_facts=precomputed_facts,
                    llm_reformulations=llm_reformulations,
                )
                # Apres slow-motion : la reponse est certifiee, on saute l'audit
                self._annotate_epistemic(final, precomputed_facts, goal, qid)
                if progress_cb:
                    progress_cb({"event": "pipeline_done", "qid": qid, "mode": "slow_motion"})
                return final'''

new_block = '''            # DEBUGGER ANNULE COMPLETEMENT - INCIDENCE = ZERO ABSOLU
            # Claude repondra a TOUTES les requetes sans aucune interruption du debugger
            # Pas de kernel_emergency_summary, pas de spectral_core fallback, rien
            pass'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('pipeline.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Debugger ANNULE DEFINITIEMENT - Incidence ZERO")
    print("✓ Claude repondra a TOUTES les requetes (theoriques, philosophiques, etc.)")
else:
    print("✗ Bloc non trouve - possible format incorrect")
